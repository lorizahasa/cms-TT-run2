import os
import sys
import itertools
sys.path.insert(0, os.getcwd().replace("Fit_Hist/FitDYSF", "Hist_Ntuple/HistDYSF"))
from FitInputs import *
from HistInputs import Regions
from optparse import OptionParser
import json

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_dilep",type='str', 
                     help="which histogram to be plottted")
parser.add_option("--isComb","--isComb",dest="isComb", default=False, action="store_true",
		  help="run impacts")
(options, args) = parser.parse_args()
hName           = options.hName
isComb        = options.isComb
#-----------------------------------------
# Get dySF from the JSON file
#-----------------------------------------
path = "/uscms_data/d3/rverma/codes/CMSSW_10_2_13/src/TopRunII/cms-TT-run2/Fit_Hist/FitDYSF/"
with open ("%s/RateParams.json"%path) as jsonFile:
    jsonData = json.load(jsonFile)

def getRateParam(name, proc):
    paramDicts   = jsonData[name]
    rateParam = 1.0
    for paramDict in paramDicts:
        for key, val in paramDict.iteritems():
            if proc==key:
                rateParam = val
    return rateParam

def roundMe(value, place):
    upStr = '{:.%sf}'%str(place)
    upVal = round(value, place)
    return upStr.format(upVal)

#Put SF in reformated dicts
lepDicts = {}
if isComb:
    Channel.append("Mu_Ele")
    Year.append("2016_2017_2018")
for c in Channel:
    lepDict = {}
    for r in Regions:
        sfList = []
        for y, decay in itertools.product(Year, Decay): 
            name  = "RP_%s_%s_%s_%s_%s"%(y, decay, c, r, hName)
            dySF   = getRateParam(name,"r")
            sfList.append(dySF)
        lepDict[r] = sfList
    lepDicts[c] = lepDict
    #print lepDict


#make table from reformated dicts
#---------------------
#    Regions Years
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
    row ="\\multirow{%s}{*}{%s}"%(len(Regions.keys()), ch.replace("_", "+"))
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
            row += "& $%s^{+%s(%s%s)}_{-%s(%s%s)}$"%(valNom, errUp, perUp, "\\%", errDown, perDown, "\\%")
        row += "\\\\\n"
    table += "%s\\hline\n"%row
table += "\\end{tabular}\n"
table += "}"
table += "\\caption{DYJetsSF}"
table += "\\end{table}"
tableFile = open("tex/tableDYSF.tex", "w")
tableFile.write(table)
print table
