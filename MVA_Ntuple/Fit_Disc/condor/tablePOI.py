import os
import sys
import itertools
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor", ""))
sys.path.insert(0, os.getcwd().replace("Fit_Disc/condor", "Disc_Ntuple"))
from FitInputs import *
import json


hName = "Disc"
#-----------------------------------------
# Get poi from the JSON file
#-----------------------------------------
def getDisc(jsonData):
    sfs = jsonData['POIs'][0]['fit']
    down= sfs[1] - sfs[0]
    nom = sfs[1]
    up  = sfs[2] - sfs[1]
    return [down, nom, up]

def roundMe(value, place):
    upStr = '{:.%sf}'%str(place)
    upVal = round(value, place)
    return upStr.format(upVal)

txtFile = open("%s/FitDisc_nuisImpact.txt"%dirFit, 'w')
texFile = open("%s/FitDisc_tableDisc.tex"%dirFit, 'w')
pyFile  = open("%s/FitDisc_dictDisc.py"%dirFit, 'w')
sfDict = {}
regionList = list(rDict.keys())
#Put SF in reformated dicts
lepDicts = {}
for c in Channel:
    lepDict = {}
    for r in regionList:
        sfList = []
        for y, decay in itertools.product(Year, Decay): 
            print("===> %s, %s, %s"%(c, r, y))
            dirJSON =  "%s/%s/%s/%s/800/BDTA/%s/%s"%(dirFit, y, decay, c, r, hName)
            #print(dirJSON)
            pdf = "%s/nuisImpact.pdf"%dirJSON
            txtFile.write("%s\n"%pdf)
            with open ("%s/nuisImpact.json"%dirJSON) as jsonFile:
                jsonData = json.load(jsonFile)
                #poi   = getDisc(name,"r")
                poi   = getDisc(jsonData)
                sfList.append(poi)
                sfDict["Disc_%s_%s_%s_%s"%(y, decay, c, r)] = round(poi[1], 3)
            jsonFile.close()
        lepDict[r] = sfList
    lepDicts[c] = lepDict
    #print(lepDict)

#make table from reformated dicts
#---------------------
#    regionList Year
#    ----------------
# mu
#    ----------------
#---------------------
'''
nCol = 3 + len(Year)
col = ""
for i in range(nCol):
    col += "c"
table ="\\begin{table}"
table += "\\cmsTable{\n"
table += "\\centering\n"
table += "\\begin{tabular}{%s}\n"%col
table += "\\hline\n"
tHead = "Channel & Regions & Data " 
for y in Year:
    tHead += "& %s"%y.replace("_", "+")
tHead += "\\\\\n"
table += tHead
table += "\\hline\n"
row = ""
#print(Samples.keys())
#for ch in lepDicts.keys():
for ch in Channel: 
    row ="\\multirow{%s}{*}{%s}"%(len(regionList), ch.replace("__", "+"))
    chDict = lepDicts[ch]
    for l in chDict.keys():
        #row += "& %s"%formatCRString(regionList).replace("#", "\\")
        row += "& %s"%rDict[l]
        #row += "& %s"%l.replace("_", "\\_")
        row += "& %s"%getType(l)
        for sf in chDict[l]:
            valNom = roundMe(sf[1], 2) # 0 = down, 1 = up, 2 = down
            #perUp  = roundMe(abs(100*sf[2]/sf[1]),1)
            #perDown  = roundMe(abs(100*sf[0]/sf[1]),1)
            errUp  = roundMe(sf[2],2)
            errDown  = roundMe(abs(sf[0]),2)
            row += "& $%s^{+%s}_{-%s}$"%(valNom, errUp, errDown)
            #row += "& $%s^{+%s%s}_{-%s%s}$"%(valNom, perUp, '\\%', perDown, '\\%')
            #row += "& $%s^{+%s(%s%s)}_{-%s(%s%s)}$"%(valNom, errUp, perUp, "\\%", errDown, perDown, "\\%")
        row += "\\\\\n"
    table += "%s\\hline\n"%row
table += "\\end{tabular}\n"
table += "}"
table += "\\caption{Signal strength}"
table += "\\end{table}"
print(table)
texFile.write(table)
pyFile.write("Disc = %s"%sfDict)
print(pyFile)
print(texFile)
pyFile.close()
texFile.close()
'''
print(txtFile)
txtFile.close()
