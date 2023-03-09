import os
import sys
import itertools
from optparse import OptionParser
import json

def getSF(jsonData, index):
    sfs = jsonData['POIs'][index]['fit']
    down= sfs[1] - sfs[0]
    nom = sfs[1]
    up  = sfs[2] - sfs[1]
    return [down, nom, up]

def roundMe(value, place):
    upStr = '{:.%sf}'%str(place)
    upVal = round(value, place)
    return upStr.format(upVal)

#Put SF in reformated dicts
lepDicts = {}
sfList = []
dirFit = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/CBA_Ntuple/Fit_Hist/"
dictYear = {}
for y in ['2016Pre', '2016Post', '2017', '2018']: 
    dirDY    =  "%s/FitDYSF/%s/%s/%s/%s/%s"%(dirFit, y, 'Dilep', 'Mu__Ele', 'DY_Enriched_a2j_e0b_e0y', 'Reco_mass_dilep')
    dirMisID =  "%s/FitMisIDSF/%s/%s/%s/%s/%s"%(dirFit, y, 'Semilep', 'Mu__Ele', 'MisID_Enriched_a2j_e0b_e1y', 'Reco_mass_lgamma')
    with open ("%s/nuisImpact.json"%dirMisID) as jsonFile:
        jsonData = json.load(jsonFile)
        sfMisID   = getSF(jsonData, 0)
        sfWGamma  = getSF(jsonData, 1)
        sfZGamma  = getSF(jsonData, 2)
    with open ("%s/nuisImpact.json"%dirDY) as jsonFile:
        jsonData = json.load(jsonFile)
        sfDY   = getSF(jsonData, 0)
    outList = [sfDY, sfMisID, sfZGamma, sfWGamma]
    sfList.append(outList)
    dictYear[y] = outList

print(dictYear)
for sfs in sfList:
    row = ""
    for sf in sfs:
        valNom = roundMe(sf[1], 2) # 0 = down, 1 = up, 2 = down
        perUp  = roundMe(sf[2],2)
        perDown  = roundMe(abs(sf[0]),2)
        row += " & $%s^{+%s}_{-%s}$"%(valNom, perUp, perDown)
    row += "\\\\"
    print(row)


