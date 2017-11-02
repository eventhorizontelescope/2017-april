'''
This is a AIPS/ParselTongue APCAL pipeline script for EHT 2017 data,
used for Rev1-cal ER1 v2 data release.

Developer: Kazu Akiyama
Ver: 2017/10/30
'''
# -------------------------------------------------------------------------
# Load Modules
# -------------------------------------------------------------------------
import os
import numpy as np
import pandas as pd
import eat.aips as ea

def pipeline(
        obscode,
        rev,
        band,
        # AIPS Parameters
        aipsdir="/usr/local/aips",
        userno=2,
        disk=1,
        clint=1/60.,
        # ParselTongue Parameters
        ptdir="/usr/share/parseltongue/python",
        obitdir="/usr/lib/obit/python",
        # Pipeline parameters
        workdir="none",
        fitsdir="fitsdir",
        antabdir="antabdir"):
    # Use AIPS VER 31DEC17
    ea.setenv(aipsdir=aipsdir, aipsver="31DEC17", ptdir=ptdir, obitdir=obitdir)
    from eat.aips.aipsutil import *
    from eat.aips.ehtutil  import *

    # -------------------------------------------------------------------------
    # Initialize AIPS and AIPS parameters
    # -------------------------------------------------------------------------
    if os.path.isdir(workdir) is False:
        os.system("mkdir -p %s"%(workdir))

    # -------------------------------------------------------------------------
    # Initialize AIPS and AIPS parameters
    # -------------------------------------------------------------------------
    setuser(userno)   # userid

    #-------------------------------------------------------------------------------
    # Pipeline Parameters
    #-------------------------------------------------------------------------------
    # UVNAME
    fileheader="%s-%d%s"%(obscode,rev,band[0])
    fileheader=fileheader.lower()
    uvname=fileheader.upper()

    # track
    track=obscode[3].upper()

    # FILENAME
    if band[0].lower()=="l":
        antabfile=os.path.join(
            antabdir,
            "eht_2017_april_%s_L.AN"%(track))
    elif band[0].lower()=="h":
        antabfile=os.path.join(
            antabdir,
            "eht_2017_april_%s_H.AN"%(track))
    else:
        raise ValueError("Invalid band %s"%(band))

    #-------------------------------------------------------------------------------
    # Set User Name
    #-------------------------------------------------------------------------------
    setuser(userno)
    fileid=1

    #---------------------------------------------------------------------------
    # GET FITS FILES
    #---------------------------------------------------------------------------
    sources = []
    fitsfiles = []
    filenames = os.listdir(fitsdir)
    for filename in filenames:
        if not fileheader in filename:
            continue
        if not "uvfits" in filename:
            continue
        sources.append(filename.split(".")[2])
        fitsfiles.append(filename)
        print("%s will be loaded."%(filename))
    Nsrc = len(sources)

    #-------------------------------------------------------------------------------
    # DATA LOADING
    #-------------------------------------------------------------------------------
    # FITLD
    for i in range(Nsrc):
        srcdata = AIPSUVData(sources[i], 'FITLD', disk, 1)
        fitsfile = os.path.join(fitsdir,fitsfiles[i])
        zap(srcdata)
        task = tget("fitld")
        task.datain = fitsfile
        task.geton(srcdata)
        task.check()
        task()

    # MULTI
    for i in range(Nsrc):
        srcdata1 = AIPSUVData(sources[i], 'FITLD', disk, 1)
        srcdata2 = AIPSUVData(sources[i], 'MULTI', disk, 1)
        zap(srcdata2)
        task = tget("multi")
        task.getn(srcdata1)
        task.geton(srcdata2)
        task.aparm[1]=clint
        task()
        zap(srcdata1)

    # DBCON
    if   Nsrc == 1:
        dbcdata = AIPSUVData(sources[0], 'MULTI', disk, 1)
    else:
        dbconver=1
        for i in range(1,Nsrc):
            if i==1:
                dbcdataold = AIPSUVData(sources[i-1], 'MULTI', disk, 1)
            else:
                dbcdataold = AIPSUVData(uvname, 'DBCON', disk, dbconver-1)
            srcdata = AIPSUVData(sources[i], 'MULTI', disk, 1)
            dbcdata = AIPSUVData(uvname, 'DBCON', disk, dbconver)
            print(dbcdataold.uvdataname())
            print(srcdata.uvdataname())
            print(dbcdata.uvdataname())
            print("")
            zap(dbcdata)
            task = tget("dbcon")
            task.getn(dbcdataold)
            task.get2n(srcdata)
            task.geton(dbcdata)
            task()
            zap(srcdata)
            zap(dbcdataold)
            dbconver+=1
    # MSORT & INDXR
    msortdata = AIPSUVData(uvname, 'MSORT', disk, 1)
    zap(msortdata)
    ehtsort(indata=dbcdata,outdata=msortdata,clint=clint)
    zap(dbcdata)
    msortdata = AIPSUVData(uvname, 'MSORT', disk, 1)

    #-------------------------------------------------------------------------------
    # Data Apriori Calibration
    #-------------------------------------------------------------------------------
    ehtsumm(
        indata=msortdata,
        prtanout=os.path.join(workdir,"%s.apcal.%02d.prtan.txt"%(fileheader, fileid)),
        listrout=os.path.join(workdir,"%s.apcal.%02d.lisr.scan.txt"%(fileheader, fileid+1)),
        dtsumout=os.path.join(workdir,"%s.apcal.%02d.dtsum.txt"%(fileheader, fileid+2)),
    )
    fileid+=3

    #-------------------------------------------------------------------------------
    # Apriori Calibration
    #-------------------------------------------------------------------------------
    # ANTAB
    #ehtantab(msortdata, antabfileNA, antabfileAA1, antabfileAA2)
    indata=msortdata
    task = tget("antab")
    task.getn(indata)
    task.tyver=indata.table_highver("TY")+1
    task.gcver=indata.table_highver("GC")+1
    task.calin=antabfile
    task.check()
    task()

    # Plot Tsys
    ehtsnplt(
        indata=msortdata,
        pltifs=1,
        inext="TY",
        invers=1,
        optypes="TSYS",
        outfile=os.path.join(workdir,"%s.apcal.%02d.ty.ps"%(fileheader, fileid)),
        nplots=len(msortdata.antennas),
        overwrite=True,
        zappltabs=True)
    fileid += 1

    # APCAL
    ehtapcal(msortdata, dif=32)

    # Plot CL table
    ehtsnplt(
        indata=msortdata,
        pltifs=1,
        inext="CL",
        invers=msortdata.table_highver("CL"),
        optypes="AMP",
        outfile=os.path.join(workdir,"%s.apcal.%02d.cl.ps"%(fileheader, fileid)),
        nplots=len(msortdata.antennas),
        overwrite=True,
        zappltabs=True)
    fileid += 1

    #-------------------------------------------------------------------------------
    # SPLIT DATA
    #-------------------------------------------------------------------------------
    sources = msortdata.sources
    for source in sources:
        splitdata = AIPSUVData(source, "SPLIT", disk, 1)
        zap(splitdata)

    task = tget("split")
    task.getn(msortdata)
    task.docal=1
    task.gainu=msortdata.table_highver("CL")
    task.outclass="SPLIT"
    task()

    for source in sources:
        splitdata = AIPSUVData(source, "SPLIT", disk, 1)
        task=tget("fittp")
        task.getn(splitdata)
        task.dataout=os.path.join(workdir,"%s.apcal.%s.uvfits"%(fileheader, source))
        task.check(overwrite=True)
        task()
        zap(splitdata)

    for stokes in ["RR", "LL"]:
        task = tget("split")
        task.getn(msortdata)
        task.docal=1
        task.stokes=stokes
        task.gainu=msortdata.table_highver("CL")
        task.outclass="SPLIT"
        task()

        for source in sources:
            splitdata = AIPSUVData(source, "SPLIT", disk, 1)
            if splitdata.exists():
                task=tget("fittp")
                task.getn(splitdata)
                task.dataout=os.path.join(workdir,"%s.apcal.%s.%s.uvfits"%(fileheader,source,stokes))
                task.check(overwrite=True)
                task()
                zap(splitdata)
    zap(msortdata)
