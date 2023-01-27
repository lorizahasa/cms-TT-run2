import os
import sys
systPath = '/eos/uscms/store/user/rverma/Output/cms-TT-run2/MVA_Ntuple/Plot_Disc/PlotMain'
sys.path.insert(0, systPath) 
from PlotInputs import *
from systRatioDisc_ForMain_SepYears import systDict
from collections import OrderedDict

def roundMe(value, place):
    upStr = '{:.%sf}'%place
    upVal = round(value, place)
    final = upStr.format(upVal)
    return final

def getRange(vals):
    newVals = []
    for val in vals:
        newVals.append(abs(1-val))
    min_ = min(newVals)
    max_ = max(newVals)
    min__ = int(round(100*min_, 1))
    max__ = int(round(100*max_, 1))
    return "%s--%s"%(min__, max__)

sysDict_ = {}
toSort   = {}
for sys in Systematics:
    yList = []
    yMax  = []
    for y in Years:
        muR  = getRange(systDict["%s_%s_%s_%s"%(y, "Mu", "ttyg_Enriched_SR_Resolved", sys)])
        eleR = getRange(systDict["%s_%s_%s_%s"%(y, "Ele","ttyg_Enriched_SR_Resolved", sys)])
        muB  = getRange(systDict["%s_%s_%s_%s"%(y, "Mu", "ttyg_Enriched_SR_Boosted", sys)])
        eleB = getRange(systDict["%s_%s_%s_%s"%(y, "Ele","ttyg_Enriched_SR_Boosted", sys)])
        yList.append("%s, %s, %s, %s"%(muR, eleR, muB,  eleB))
        yMax.append(float(muR.split("--")[1]))
        yMax.append(float(eleR.split("--")[1]))
        yMax.append(float(muB.split("--")[1]))
        yMax.append(float(eleB.split("--")[1]))
    sysDict_[sys] = yList
    toSort[sys] = max(yMax)

label = {}
label["Weight_pu"] = 'PU' 
label["Weight_mu"] = '$\\mu$'
label["Weight_pho"] = '$\\gamma$'
label["Weight_ele"] = 'e'
label["Weight_btag_b"] = 'b' 
label["Weight_btag_l"] = 'non-b'
label["Weight_prefire"] = 'PF'
label["Weight_q2"] = 'Q2'
label["Weight_pdf"] = 'PDF'
label["Weight_isr"] = 'ISR'
label["Weight_fsr"] = 'FSR'
label["Weight_jes"] = 'JES'
label["Weight_jer"] = 'JER'
label["Weight_ttag"] = 't'

col = "c|"
nCol = 4*len(Years)
for i in range(nCol):
    col += "c"
    if i==3 or i==7 or i==11:
        col += "|"

table  = "\\cmsTable{\n"
table += "\\centering\n"
table += "\\begin{tabular}{%s}\n"%col
table += "\\hline\n"
#first header line
tHead = ""
for y in Years:
    tHead += " & \\multicolumn{4}{c}{%s}"%y.replace("_", "+")
tHead += "\\\\\n"
table += tHead

#second header line
tHead = "Systematics"
for i in range(4):
    tHead += "& $\\mu_R$ & $e_R$ & $\\mu_B$ & $e_B$"
tHead += "\\\\\n"
table += tHead

#third header line
tHead = ""
for i in range(4):
    tHead += "& (\\%) & (\\%) & (\\%) & (\\%)"
tHead += "\\\\\n"
table += tHead

table += "\\hline\n"
row = ""
toSort = OrderedDict(sorted(toSort.items(), key=lambda t: t[1]))
for sys in list(toSort.keys()):
    row += " \\SF{%s}"%label[sys]
    yVals = sysDict_[sys]
    for vals in yVals:
        for val in vals.split(','):
            row += "& %s"%val
    row += "\\\\\n"
table += "%s\\hline\n"%row
table += "\\end{tabular}\n"
table += "}"
print(table)
tableFile = open("%s/systRatioDisc_ForMain_SepYears.tex"%systPath, "w")
tableFile.write(table)
print(tableFile)
