import os
import sys
import itertools
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor", ""))
sys.path.insert(0, os.getcwd().replace("Fit_Hist/FitDYSF/condor", "Hist_Ntuple/HistDYSF"))
from FitInputs import *
from HistInputs import Regions
from optparse import OptionParser
import json

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Merge for combined years and channels")
parser.add_option("--isSep","--isSep", dest="isSep",action="store_true",default=False, help="Merge for separate years and channels")
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep = options.isSep

if isCheck:
    isSep  = True
    Year  = [Year[0]]
    Decay = [Decay[0]]
    Channel = [Channel[0]]
if not isCheck and not isSep:
    print("Add either --isCheck or --isSep in the command line")
    exit()

hName = "Reco_mass_dilep"
#-----------------------------------------
# Get dySF from the JSON file
#-----------------------------------------
def getDYSF(jsonData):
    sfs = jsonData['POIs'][0]['fit']
    down= sfs[1] - sfs[0]
    nom = sfs[1]
    up  = sfs[2] - sfs[1]
    return [down, nom, up]

def roundMe(value, place):
    upStr = '{:.%sf}'%str(place)
    upVal = round(value, place)
    return upStr.format(upVal)

txtFile = open("%s/FitDYSF_nuisImpact.txt"%dirFit_, 'w')
texFile = open("%s/FitDYSF_tableDYSF.tex"%dirFit_, 'w')
pyFile  = open("%s/FitDYSF_dictDYSF.py"%dirFit_, 'w')
sfDict = {}
#Put SF in reformated dicts
lepDicts = {}
for c in Channel:
    lepDict = {}
    for r in Regions:
        sfList = []
        for y, decay in itertools.product(Year, Decay): 
            print("===> %s, %s, %s"%(c, r, y))
            dirJSON =  "%s/%s/%s/%s/%s/%s"%(dirFit_, y, decay, c, r, hName)
            pdf = "%s/nuisImpact.pdf"%dirJSON
            txtFile.write("%s\n"%pdf)
            with open ("%s/nuisImpact.json"%dirJSON) as jsonFile:
                jsonData = json.load(jsonFile)
                #dySF   = getDYSF(name,"r")
                dySF   = getDYSF(jsonData)
                sfList.append(dySF)
                sfDict["DYSF_%s_%s_%s_%s"%(y, decay, c, r)] = round(dySF[1], 3)
            jsonFile.close()
        lepDict[r] = sfList
    lepDicts[c] = lepDict
    #print lepDict

#make table from reformated dicts
#---------------------
#    Regions Year
#    ----------------
# mu
#    ----------------
#---------------------
nCol = 2 + len(Year)
col = ""
for i in range(nCol):
    col += "c"
table ="\\begin{table}"
table += "\\cmsTable{\n"
table += "\\centering\n"
table += "\\begin{tabular}{%s}\n"%col
table += "\\hline\n"
tHead = "Channel & Regions" 
for y in Year:
    tHead += "& %s"%y.replace("_", "+")
tHead += "\\\\\n"
table += tHead
table += "\\hline\n"
row = ""
#print Samples.keys()
#for ch in lepDicts.keys():
for ch in Channel: 
    row ="\\multirow{%s}{*}{%s}"%(len(Regions.keys()), ch.replace("__", "+"))
    chDict = lepDicts[ch]
    for l in chDict.keys():
        #row += "& %s"%formatCRString(Regions[l]).replace("#", "\\")
        row += "& %s"%l.replace("_", "\\_")
        for sf in chDict[l]:
            valNom = roundMe(sf[1], 2) # 0 = down, 1 = up, 2 = down
            perUp  = roundMe(abs(100*sf[2]/sf[1]),1)
            perDown  = roundMe(abs(100*sf[0]/sf[1]),1)
            errUp  = roundMe(sf[2],2)
            errDown  = roundMe(abs(sf[0]),2)
            #row += "& $%s^{+%s}_{-%s}$"%(valNom, errUp, errDown)
            row += "& $%s^{+%s%s}_{-%s%s}$"%(valNom, perUp, '\\%', perDown, '\\%')
            #row += "& $%s^{+%s(%s%s)}_{-%s(%s%s)}$"%(valNom, errUp, perUp, "\\%", errDown, perDown, "\\%")
        row += "\\\\\n"
    table += "%s\\hline\n"%row
table += "\\end{tabular}\n"
table += "}"
table += "\\caption{DYJetsSF}"
table += "\\end{table}"
print table
texFile.write(table)
pyFile.write("DYSF = %s"%sfDict)
print(txtFile)
print(pyFile)
print(texFile)
txtFile.close()
pyFile.close()
texFile.close()
