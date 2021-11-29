#!/usr/bin/env python
from ROOT import gROOT, TGraph, TCanvas, TLegend
import os
import sys
sys.path.insert(0, os.getcwd().replace("MVA_Ntuple/Fit_Disc", "CBA_Ntuple/Plot_Hist/PlotMain"))
sys.path.insert(0, os.getcwd().replace("Fit_Disc", "Disc_Ntuple"))
import json
from PlotCMSLumi import *
from PlotTDRStyle import *
from array import array
from FitInputs import *
from optparse import OptionParser
from DiscInputs import methodList
import pandas as pd

padGap = 0.01
iPeriod = 4;
iPosX = 10;
setTDRStyle()
xPadRange = [0.0,1.0]
yPadRange = [0.0,0.30-padGap, 0.30+padGap,1.0]

parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specify the year of the data taking" )
parser.add_option("-d", "--decayMode", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decayMode moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
		  help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched_SR",type='str', 
                     help="which control selection and region"), 
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_T",type='str', 
                     help="which histogram to be used for making datacard")
parser.add_option("--byCR","--byCR",dest="byCR", default=False, action="store_true",
		  help="run FitDiabnostics")
parser.add_option("--byVar","--byVar",dest="byVar", default=False, action="store_true",
		  help="run FitDiabnostics")
(options, args) = parser.parse_args()
year            = options.year
decayMode       = options.decayMode
channel         = options.channel
region          = options.region
hName           = options.hName
byCR           = options.byCR
byVar           = options.byVar
gROOT.SetBatch(True)

limits = "tex/allLimits.json"
gDict = {}
limDict={}
path = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/MVA_Ntuple/Fit_Disc/%s/%s/%s"%(year, decayMode, channel)
def getLimit(jsonFile, exp, m):
    with open(jsonFile) as jsonFile_:
        jsonData = json.load(jsonFile_)
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

for h in histList:
    x = array( 'd' )
    y = array( 'd' )
    for m in Mass:
        x.append(float(m))
        limFile      = "%s/%s/%s/%s/%s/limits.json"%(path, m, "MLP", region, h)
        print(limFile)
        y.append(float(xss[m]*getLimit(limFile, "exp0", m)))
    graph = TGraph(len(x), x, y)
    gDict[h] = graph
    limDict["mT"] = x
    limDict[h] = y

aucDict = {}
for method in methodList.keys():
    x = array( 'd' )
    y = array( 'd' )
    auc = []
    for m in Mass:
        x.append(float(m))
        limFile      = "%s/%s/%s/%s/%s/limits.json"%(path, m, method, region, "Disc")
        print(limFile)
        y.append(float(xss[m]*getLimit(limFile, "exp0", m)))
        aucFile      = open("%s/%s/%s/AUC.txt"%(path.replace("Fit_Disc", "Disc_Ntuple"), m, method))
        for line in aucFile:
            if "AUC" in line:
                auc.append(roundMe(100*float(line.split(" ")[-1]), 1))
    graph = TGraph(len(x), x, y)
    gDict[method] = graph
    limDict["mT"] = x
    limDict[method] = y
    aucDict[method] = auc
    aucDict['mT'] = x

print limDict
df = pd.DataFrame.from_dict(limDict)
print(df)
roundDict = {}
roundBy = 1
for m in methodList.keys():
    df[m] =100*(df[m] - df['Reco_mass_T'])/df['Reco_mass_T']
    roundDict[m] = roundBy
for h in histList:
    if "Reco_mass_T" not in h:
        df[h] =100*(df[h] - df['Reco_mass_T'])/df['Reco_mass_T']
        roundDict[h] = roundBy
df.set_index('mT', inplace=True)
print df.round(roundDict)

aucDF = pd.DataFrame.from_dict(aucDict)
aucDF.set_index('mT', inplace=True)
print(aucDF)
canvas = TCanvas()
legend = TLegend(0.70,0.60,0.85,0.90);
legend.SetFillStyle(0);
legend.SetBorderSize(0);
legend.SetTextFont(42);
legend.SetTextAngle(0);
legend.SetTextSize(0.035);
legend.SetTextAlign(12);
canvas.cd()
maxInt = 0.0;
for index, s in enumerate(gDict.keys()):
    if index==9: index=10
    gDict[s].SetLineColor(index+1)
    gDict[s].SetLineWidth(3)
    gDict[s].SetMarkerStyle(20+index);
    gDict[s].SetMarkerColor(index+1);
    gDict[s].GetYaxis().SetTitle("#sigma_{TT} B(T #rightarrow t#gamma)B(T #rightarrow tg) [pb]")
    gDict[s].GetYaxis().SetLabelSize(.035)
    gDict[s].GetXaxis().SetLabelSize(.035)
    gDict[s].GetXaxis().SetTitle("m_{T} (GeV)")
    gDict[s].Draw("P")
    if index==0:
        gDict[s].SetMaximum(0.02)
        gDict[s].SetMinimum(0.0001)
        gDict[s].Draw()
    else:
        gDict[s].Draw("same")
    #legName = "%s, mean = %i, int = %i"%(econDict[s][1], gDict[s].GetMean(), gDict[s].Integral())
    legend.AddEntry(gDict[s], s,  "LP")
    canvas.Update()
    
#Theory
x, y = array( 'd' ), array( 'd' )
for m in Mass:
    x.append(float(m))
    y.append(xss[m])
gTheory = TGraph(len(x), x, y)
gTheory.SetLineColor(7)
gTheory.SetLineWidth(3)
gTheory.SetMarkerStyle(15);
gTheory.SetMarkerColor(7);
gTheory.Draw("Lsame")
legend.AddEntry(gTheory, "Theory", "L")
legend.Draw()
#---------------------------
#Draw CMS, Lumi, channel
#---------------------------
chColor = 1
if channel in ["mu", "Mu", "m"]:
    chColor = 3 #ROOT.kCyan
    chName = "1 #color[%i]{#mu}, p_{T}^{miss} > 20"%chColor
elif channel in ["ele", "Ele"]:
    chColor = 2#ROOT.kRust - 1
    chName = "1 #color[%i]{e}, p_{T}^{miss}  > 20"%chColor
else:
    chColor = 4#ROOT.kRed + 1
    chName = "1 #color[%i]{#mu + e}, p_{T}^{miss}  > 20"%chColor
#chName = "#splitline{%s}{%s}"%(chName, region)
chName = "%s, #bf{%s}"%(chName, region)
crName = region 
#chCRName = "#splitline{#font[42]{%s}}{#font[42]{(%s)}}"%(chName, crName)
chCRName = "#splitline{#font[42]{%s}}{#font[42]{%s}}"%(chName, "95% CL expected upper limit")
extraText   = "#splitline{Preliminary}{%s}"%chCRName
lumi_13TeV = "35.9 fb^{-1}"
col_year = 3 
if year=="2016":
    lumi_13TeV = "35.9 fb^{-1} (#color[%i]{2016})"%(col_year)
elif year=="2016":
    lumi_13TeV = "41.5 fb^{-1} (#color[%i]{2017})"%(col_year)
elif year=="2016":
    lumi_13TeV = "59.7 fb^{-1} (#color[%i]{2018})"%(col_year)
else:
    lumi_13TeV = "137.2 fb^{-1} (#color[%i]{Run2})"%(col_year)
CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
#canvas.SaveAs("tex/limit.pdf"%(""))
if byVar:
    name = "byVar"
elif byCR:
    name = "byCR"
else:
    name = "by"
#canvas.SaveAs("%s/Fit_Hist/FitMain/forMain/%s/Semilep/%s/limit_%s.pdf"%(condorHistDir, year, channel, name))
canvas.SaveAs("limit.pdf")

