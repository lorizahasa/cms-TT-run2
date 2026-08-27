import os
import sys
systPath = '/eos/uscms/store/user/lhasa/Output/cms-TT-run2/MVA_Ntuple/C/Plot_Disc/PlotMain'
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
    min__ = round(100*min_, 1) #wrap it in int() if you want whole number
    max__ = round(100*max_, 1)
    #return "%s--%s"%(min__, max__)
    return f"{min__:.1f}--{max__:.1f}"

sysDict_ = {}
toSort   = {}

    #syst = SystList_by_year[year]
for year in Years:
    syst = Syst_w_JER[year]
for sys in syst:
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
label["JEC_Total"] = 'JES'
#label["JER_%s"%year] = 'JER'
label["Weight_ttag"] = 't'
#label["JEC_Absolute"] = 'JEC_Absolute'
#label["JEC_BBEC1"] = 'JEC_BBEC1'
#label["JEC_EC2"] = 'JEC_EC2'
#label["JEC_HF"] = 'JEC_HF'
#label["JEC_RelativeBal"] = 'JEC_RelativeBal'
#label["JEC_FlavorQCD"] = 'JEC_FlavorQCD'

for y in Years:
    label[f"JER_{y}"] = f"JER-{y}"
    #label[f"JEC_Absolute_{y}"] = f"JEC_Absolute_{y}"
    #label[f"JEC_BBEC1_{y}"]    = f"JEC_BBEC1_{y}"
    #label[f"JEC_EC2_{y}"]      = f"JEC_EC2_{y}"
    #label[f"JEC_HF_{y}"]       = f"JEC_HF_{y}"
    #label[f"JEC_RelativeSample_{y}"] = f"JEC_RelativeSample_{y}"
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
tHead = "Systematic Uncertainties on"
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
