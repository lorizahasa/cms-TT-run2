import itertools
from FitInputs import *
import json

#-----------------------------------------
# Get dySF from the JSON file
#-----------------------------------------
path = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Fit_Hist/FitMain/forMain/"
def getLimit(jsonData, exp, m):
    paramDict   = jsonData["%s.0"%m]
    lim = 1.0
    for key, val in paramDict.iteritems():
        if exp==key:
            lim= val
    return lim

def roundMe(value, place):
    upStr = '{:.%sf}'%place
    upVal = round(value, place)
    final = upStr.format(upVal)
    return final

#Put SF in reformated dicts
chDict = {}
for c in Channel:
    yearDict = {}
    for y, decay in itertools.product(Year, Decay): 
        print "%s, %s"%(c, y)
        histDict = {}
        for h in histList:
            regionDict = {}
            for r in regionList:
                limits = []
                for m in Mass:
                    limitJSON = "%s/%s/Semilep/%s/%s/%s/mH%s/limits.json"%(path, y, c, r, h, m)
                    with open (limitJSON) as jsonFile:
                        jsonData  = json.load(jsonFile)
                        limit     = getLimit(jsonData,"exp0", m)
                        limits.append(limit*xss[m])
                regionDict[r] = limits
            histDict[h] = regionDict
        yearDict[y] = histDict
    chDict[c] = yearDict
    #print lepDict
print chDict
with open ('tex/allLimits.json', 'w') as jsonFile:
    json.dump(chDict, jsonFile)

