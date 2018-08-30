'''
This is a AIPS/ParselTongue pipeline script for EHT 2017 data, used for Rev3 cal+sci
ER4 data release.

Developer: Kazu Akiyama, Sara Issaoun
Ver: 2018/01/05
'''
#-------------------------------------------------------------------------------
# Load Modules
#-------------------------------------------------------------------------------
import os
import numpy as np
import pandas as pd

#-------------------------------------------------------------------------------
# Pipeline Parameters
#   *** Please edit following parameters ***
#-------------------------------------------------------------------------------
param = {}

# AIPS Parameters
#   AIPS_ROOT Directory
#   (if you already loaded LOGIN.SH, you don't have to set this)
param["aipsdir"]="/usr/local/AIPS_ROOT"
#   AIPS USER NO
param["userno"]=100
#   AIPS DISK
param["disk"]=1

# ParselTongue Parameters
#   ParselTongue Python Directory
param["ptdir"]="/usr/share/parseltongue/python"
#   Obit Python Directory
param["obitdir"]="/usr/lib/obit/python"

# Observational Parameters
param["obscode"]="e17e11"
param["rev"]=3
param["band"]="lo"
param["ver"]=1

# Workdir where output files will be saved.
param["workdir"]='./%s-%d-%s-ver%d'%(param["obscode"],param["rev"],param["band"],param["ver"])
param["fileheader"]="%s-%d%s"%(param["obscode"],param["rev"],param["band"][0])

# FITS Files
#   Here FITS files are assumed to be unpacked with unpack_rev1_fitsidi.py
#   in eat/exampls/aips/scripts.
#
#   FITS Directories for High and Low bands
param["fitsdir"]='/xxxxx/%s-%d-%s'%(param["obscode"],param["rev"],param["band"])

# AIPS AN table correction file
param["ancortab"]=os.path.join("ancortab_2017apr.csv")

# Flagging
param["interactive"]=True
# preloaded flags if non-interactive run 

if param["interactive"] == False:
    param["prefgtab"]="%s.fg.preload.csv"%(param["fileheader"])

#-------------------------------------------------------------------------------
# Run Pipelines
#-------------------------------------------------------------------------------
import pipeline_rev3_er4_ver1 as pipeline
print(param)
pipeline.pipeline(**param)
