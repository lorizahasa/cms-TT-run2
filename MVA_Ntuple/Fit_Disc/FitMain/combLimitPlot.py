import os
import json
import itertools
import collections
from FitInputs import *
import numpy as np

scaleLimits =True
def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

hName = "Reco_mass_T"
dirDC = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Fit_Hist/Combined/"
nameDC = "higgsCombine_TT_run2.AsymptoticLimits.mH*.root" 
print hName
runCmd("combineTool.py -M CollectLimits %s/%s -o %s/limits.json"%(dirDC, nameDC, dirDC))
if scaleLimits:
    xss = {}
    xss["700.0"]   = 0.03*0.97*2*4.92
    xss["800.0"]   = 0.03*0.97*2*1.68
    xss["900.0"]   = 0.03*0.97*2*0.636
    xss["1000.0"]  = 0.03*0.97*2*0.262
    #xss["1100.0"]  = 0.03*0.97*2*0.116
    xss["1200.0"]  = 0.03*0.97*2*0.0537
    xss["1300.0"]  = 0.03*0.97*2*0.0261
    xss["1400.0"]  = 0.03*0.97*2*0.0131
    xss["1500.0"]  = 0.03*0.97*2*0.00677
    xss["1600.0"]  = 0.03*0.97*2*0.00359
    with open ("%s/limits.json"%dirDC) as old_limit:
        new_limit = json.load(old_limit)
        print "OLD: ", new_limit
        for mass in xss.keys():
            for limit in new_limit[mass]:
                new_limit[mass][limit] = xss[mass]*new_limit[mass][limit] 
    with open ('%s/scaled_limits.json'%dirDC, 'w') as newLimitFile:
        print "\nNEW: ", new_limit
        json.dump(new_limit, newLimitFile)

title_right = "137 fb^{-1} (13 TeV)"
title_left = "1 #mu/e, 1 #gamma"
ps = "Boosted + Resolved"
out = "%s/limit"%(dirDC)
if scaleLimits:
    limitFile = "scaled_limits.json"
else:
    limitFile = "limits.json"
runCmd("python plotLimits.py --title-left \"%s\" --title-right \"%s\" %s/%s -o %s --logy --cms-sub \"%s\""%(title_left, title_right, dirDC, limitFile, out, ps))
plotPath = "%s.pdf"%(out)

