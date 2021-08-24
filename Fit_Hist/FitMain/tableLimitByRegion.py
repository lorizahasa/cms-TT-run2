import os
import sys
import itertools
sys.path.insert(0, os.getcwd().replace("Fit_Hist/FitMain", "Hist_Ntuple/HistMain"))
from FitInputs import *
from HistInputs import Regions
from optparse import OptionParser
import json

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_T",type='str', 
                     help="which histogram to be plottted")
parser.add_option("--isComb","--isComb",dest="isComb", default=False, action="store_true",
		  help="run impacts")
(options, args) = parser.parse_args()
hName           = options.hName
isComb        = options.isComb
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
lepDicts = {}
if isComb:
    Channel.append("Mu_Ele")
    Year.append("2016_2017_2018")
for c in Channel:
    lepDict = {}
    for m in Mass:
        sfList = []
        for y, decay in itertools.product(Year, Decay): 
            limit_I = "%s/%s/Semilep/%s/ttyg_Enriched_SR/%s/mH%s/limits.json"%(path, y, c, hName, m)
            limit_R = "%s/%s/Semilep/%s/ttyg_Enriched_SR_Resolved/%s/mH%s/limits.json"%(path, y, c, hName, m)
            limit_B = "%s/%s/Semilep/%s/ttyg_Enriched_SR_Boosted/%s/mH%s/limits.json"%(path, y, c, hName, m)
            limit_RB = "%s/%s/Semilep/%s/ttyg_Enriched_SR_Resolved_ttyg_Enriched_SR_Boosted/%s/mH%s/limits.json"%(path, y, c, hName, m)
            with open (limit_I) as jsonFile_I:
                jsonData_I = json.load(jsonFile_I)
            with open (limit_R) as jsonFile_R:
                jsonData_R = json.load(jsonFile_R)
            with open (limit_B) as jsonFile_B:
                jsonData_B = json.load(jsonFile_B)
            with open (limit_RB) as jsonFile_RB:
                jsonData_RB = json.load(jsonFile_RB)
            lim_I   = getLimit(jsonData_I,"exp0", m)
            lim_R   = getLimit(jsonData_R,"exp0", m)
            lim_B   = getLimit(jsonData_B,"exp0", m)
            lim_RB   = getLimit(jsonData_RB,"exp0", m)
            sfList.append([lim_I, lim_R, lim_B, lim_RB])
        lepDict[m] = sfList
    lepDicts[c] = lepDict
    #print lepDict


#print lepDicts
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
    col += "l"
table ="\\begin{table}"
table += "\\cmsTable{\n"
table += "\\centering\n"
table += "\\begin{tabular}{%s}\n"%col
table += "\\hline\n"
tHead = "Channel & Mass" 
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
    print ch
    #for l in chDict.keys():
    for l in Mass: 
        #row += "& %s"%formatCRString(Regions[l]).replace("#", "\\")
        row += "& %s"%l.replace("_", "\\_")
        for sfs in chDict[l]:
            newList = []
            for sf in sfs:
                valNom = roundMe(sf, 2) # 0 = down, 1 = up, 2 = down
                #perUp  = roundMe(abs(100*sf[2]/sf[1]),1)
                #perDown  = roundMe(abs(100*sf[0]/sf[1]),1)
                #row += "& $%s^{+%s%s}_{-%s%s}$"%(valNom, perUp,"\\%", perDown, "\\%")
                #perUp  = roundMe(sf,2)
                #perDown  = roundMe(abs(sf[0]),2)
                #newList.append("$%s^{+%s}_{-%s}$"%(valNom, perUp, perDown))
                newList.append(valNom)
            row += "& %s"%newList
        row += "\\\\\n"
    table += "%s\\hline\n"%row
table += "\\end{tabular}\n"
table += "}"
table += "\\caption{95\\% CL median limit from regions: [Inclusive, Resolved, Boosted, Resolved+Boosted]}\n"
table += "\\end{table}"
print table
tableFile = open("tex/tableLimitByRegion.tex", "w")
tableFile.write(table)
