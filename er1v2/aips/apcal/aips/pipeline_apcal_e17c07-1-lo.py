'''
This is a AIPS/ParselTongue APCAL pipeline script for EHT 2017 data,
used for Rev1-cal ER1 v2 data release.

Developer: Kazu Akiyama
Ver: 2017/10/30
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
param["aipsdir"]="/usr/local/aips"
#   AIPS USER NO
param["userno"]=2
#   AIPS DISK
param["disk"]=1

# ParselTongue Parameters
#   ParselTongue Python Directory
param["ptdir"]="/usr/share/parseltongue/python"
#   Obit Python Directory
param["obitdir"]="/usr/lib/obit/python"

# Observational Parameters
param["obscode"]="e17c07"
param["rev"]=1
param["band"]="lo"

# Workdir where output files will be saved.
param["workdir"]='./%s-%d-%s'%(param["obscode"],param["rev"],param["band"])

# FITS Files
#   we assume that input fits files are correlation coefficients products.
param["fitsdir"]='../../coeff/products'

# ANTAB files
#   please don't forget running ../antab/runme.bash
param["antabdir"]='../antab'
#-------------------------------------------------------------------------------
# Run Pipelines
#-------------------------------------------------------------------------------
import pipeline_apcal_rev1cal_er1v2 as pipeline
print(param)
pipeline.pipeline(**param)
