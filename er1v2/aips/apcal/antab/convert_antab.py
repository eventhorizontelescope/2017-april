import eat.aips.antab as eaa
import copy
import pandas as pd

def edit_antab(data, lowband=True):
    dataout = copy.deepcopy(data)
    Ntab = len(dataout)
    
    for i in xrange(Ntab):
        tab = dataout[i]

        # Check Group
        if tab["GROUP"] == "GAIN":
            continue
        
        # Edit Tables
        if tab["ANT"] not in  ["AA", "SM"]:
            tab["DATA"] =pd.DataFrame()
            tab["INDEX"] = []
            if "R1:64" in data[i]["INDEX"]:
                tab["INDEX"].append('R1:32')
                tab["DATA"]["R1:32"] = data[i]["DATA"]["R1:64"]
            if "L1:64" in data[i]["INDEX"]:
                tab["INDEX"].append('L1:32')
                tab["DATA"]["L1:32"] = data[i]["DATA"]["L1:64"]
            tab["DATA"]["DOY"] = data[i]["DATA"]["DOY"]
            tab["DATA"]["TIME"] = data[i]["DATA"]["TIME"]
        else:
            if lowband:
                tab["INDEX"] = ["R1:32", "L1:32"]
                tab["DATA"] =pd.DataFrame()
                tab["DATA"]["DOY"] = data[i]["DATA"]["DOY"]
                tab["DATA"]["TIME"] = data[i]["DATA"]["TIME"]
                tab["DATA"]["R1:32"] = data[i]["DATA"]["R1:32"]
                tab["DATA"]["L1:32"] = data[i]["DATA"]["L1:32"]
            else:
                tab["INDEX"] = ['R1:32', 'L1:32']
                tab["DATA"] =pd.DataFrame()
                tab["DATA"]["DOY"] = data[i]["DATA"]["DOY"]
                tab["DATA"]["TIME"] = data[i]["DATA"]["TIME"]
                tab["DATA"]["R1:32"] = data[i]["DATA"]["R33:64"]
                tab["DATA"]["L1:32"] = data[i]["DATA"]["L33:64"]
        dataout[i] = tab
    return dataout

for track in "A,B,C,D,E".split(","):
    filename = "./eht_2017_april_%s.AN"%(track)
    data = eaa.read_antab(filename)
    dataout1 = edit_antab(data, lowband=True)
    dataout2 = edit_antab(data, lowband=False)
    eaa.write_antab(dataout1, filename=filename.replace(".AN","_L.AN"))
    eaa.write_antab(dataout2, filename=filename.replace(".AN","_H.AN"))

