import os
import sys
import itertools
sys.path.insert(0, os.getcwd().replace('Plot_Hist/PlotMisIDSF', 'Hist_Ntuple/HistMisIDSF'))
from PlotInputs import *
from PlotFunc import formatCRString
from HistInputs import Regions
from optparse import OptionParser
import json

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_lgamma",type='str', 
                     help="which histogram to be plottted")
(options, args) = parser.parse_args()
hName           = options.hName
#-----------------------------------------
# Get dySF from the JSON file
#-----------------------------------------
path = "/uscms_data/d3/rverma/codes/CMSSW_10_2_13/src/TopRunII/cms-TT-run2/Fit_Hist/FitMisIDSF/"
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
    upStr = '{:.%sf}'%place
    upVal = round(value, place)
    final = upStr.format(upVal)
    return final

#Put SF in reformated dicts
lepDicts = {}
for c in Channel:
    lepDict = {}
    for r in Regions:
        sfList = []
        for y, decay in itertools.product(Year, Decay): 
            name  = "RP_%s_%s_%s_%s_%s"%(y, decay, c, r, hName)
            misIDSF   = getRateParam(name,"r")
            zGammaSF  = getRateParam(name, "ZGammaSF")
            wGammaSF  = getRateParam(name, "WGammaSF")
            sfList.append([misIDSF, zGammaSF, wGammaSF])
        lepDict[r] = sfList
    lepDicts[c] = lepDict
    #print lepDict


print lepDicts
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
table = "\\setlength{\\tabcolsep}{12pt}\n"
table +="\\begin{table}"
table += "\\cmsTable{\n"
table += "\\centering\n"
table += "\\begin{tabular}{%s}\n"%col
table += "\\hline\n"
tHead = "Channel & Regions" 
for y in Year:
    tHead += "& %s"%y
tHead += "\\\\\n"
table += tHead
table += "\\hline\n"
row = ""
#print Samples.keys()
for ch in lepDicts.keys():
    row ="\\multirow{%s}{*}{%s}"%(len(Regions.keys()), ch)
    chDict = lepDicts[ch]
    for l in chDict.keys():
        #row += "& %s"%formatCRString(Regions[l]).replace("#", "\\")
        row += "& %s"%l.replace("_", "\\_")
        for sfs in chDict[l]:
            newList = []
            for sf in sfs:
                valNom = roundMe(sf[1], 2) # 0 = down, 1 = up, 2 = down
                #perUp  = roundMe(abs(100*sf[2]/sf[1]),1)
                #perDown  = roundMe(abs(100*sf[0]/sf[1]),1)
                #row += "& $%s^{+%s%s}_{-%s%s}$"%(valNom, perUp,"\\%", perDown, "\\%")
                perUp  = roundMe(sf[2],2)
                perDown  = roundMe(abs(sf[0]),2)
                newList.append("$%s^{+%s}_{-%s}$"%(valNom, perUp, perDown))
            row += "& %s"%newList
        row += "\\\\\n"
    table += "%s\\hline\n"%row
table += "\\end{tabular}\n"
table += "}"
table += "\\caption{[MisIDSF, ZGammaSF, WGammaSF]}\n"
table += "\\end{table}"
print table
tableFile = open("tex/tableMisIDSF.tex", "w")
tableFile.write(table)
