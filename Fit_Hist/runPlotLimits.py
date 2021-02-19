import os
import itertools
import json
from FitInputs import *

scaleLimits =True
def runCmd(cmd):
    print "\n\033[01;32m Excecuting: %s \033[00m"%cmd
    os.system(cmd)

for year, decay, channel in itertools.product(Year, Decay, Channel): 
    hName = "presel_TopStar_mass"
    dirDC = "%s/Fit_Hist/%s/%s/%s/%s/SR"%(condorCBADir, year, decay, channel, hName)
    nameDC = "mH*/higgsCombine_hcs_run2.AsymptoticLimits.mH*.root" 
    #runCmd("%s/%s"%(dirDC, nameDC))
    print hName
    ##runCmd("combineTool.py -M CollectLimits %s/%s -o %s/limits.json"%(dirDC, nameDC, dirDC))
    if scaleLimits:
        xss = {}
        xss["700.0"]   =  4.92
        xss["800.0"]   =  1.68
        xss["900.0"]   =  0.636
        xss["1000.0"]  =  0.262
        xss["1100.0"]  =  0.116
        xss["1200.0"]  =  0.0537
        xss["1300.0"]  =  0.0261
        xss["1400.0"]  =  0.0131
        xss["1500.0"]  =  0.00677
        xss["1600.0"]  =  0.00359
        with open ("%s/limits.json"%dirDC) as old_limit:
            new_limit = json.load(old_limit)
            print "OLD: ", new_limit
            for mass in xss.keys():
                for limit in new_limit[mass]:
                    new_limit[mass][limit] = xss[mass]*new_limit[mass][limit] 
        with open ('%s/scaled_limits.json'%dirDC, 'w') as newLimitFile:
            print "\nNEW: ", new_limit
            json.dump(new_limit, newLimitFile)

    title_right = "35.9 fb^{-1} (13 TeV)"
    if "16" in year:
        title_right = "35.9 fb^{-1} (2016) (13 TeV)"
    if "17" in year:
        title_right = "41.5 fb^{-1} (2017) (13 TeV)"
    if "18" in year:
        title_right = "59.7 fb^{-1} (2018) (13 TeV)"
    title_left = "e + jets"
    if "Mu" in channel:
        title_left = "#mu + jets"
    out = "limit_%s_%s"%(year, channel)
    #runCmd("python plotLimits.py --title-left \"%s\" --title-right \"%s\" %s/limits.json -o %s/limits"%(title_left, title_right, dirDC, dirDC))
    if scaleLimits:
        limitFile = "scaled_limits.json"
    else:
        limitFile = "limits.json"
    runCmd("python plotLimits.py --title-left \"%s\" --title-right \"%s\" %s/%s -o %s --logy"%(title_left, title_right, dirDC, limitFile, out))
    #print args
