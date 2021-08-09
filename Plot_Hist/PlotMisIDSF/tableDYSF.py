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

#Put SF in reformated dicts
lepDicts = {}
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
table = "\\setlength{\\tabcolsep}{12pt}\n"
table += "\\centering"
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
        for sf in chDict[l]:
            row += "& %s"%sf
        row += "\\\\\n"
    table += "%s\\hline\n"%row
table += "\\end{tabular}\n"
table += "\\caption{Normalization scale factors for DYJets sample}"
print table
tableFile = open("tex/tableMisIDSF.tex", "w")
tableFile.write(table)
