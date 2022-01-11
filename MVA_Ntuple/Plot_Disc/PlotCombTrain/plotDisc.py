#!/usr/bin/env python
from ROOT import gROOT, TGraph, TCanvas, TLegend, TFile
import os
import sys
sys.path.insert(0, os.getcwd().replace("MVA_Ntuple/Plot_Disc/PlotCombTrain", "CBA_Ntuple/Plot_Hist/PlotMain"))
sys.path.insert(0, os.getcwd().replace("Plot_Disc/PlotCombTrain", "Disc_Ntuple/DiscCombTrain"))
import json
from PlotCMSLumi import *
from PlotTDRStyle import *
from array import array
from PlotInputs import *
from optparse import OptionParser
from DiscInputs import methodDict

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
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched_SR_Resolved",type='str', 
                     help="which control selection and region"), 
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_T",type='str', 
                     help="which histogram to be used for making datacard")
parser.add_option("--mass","--mass",dest="mass", default='800', type='str', 
		  help="mass of the Tprime")
parser.add_option("--method","--method",dest="method", default='DNN', type='str', 
		  help="MVA method")
(options, args) = parser.parse_args()
year            = options.year
decayMode       = options.decayMode
channel         = options.channel
mass           = options.mass
method           = options.method
region          = options.region
hName           = options.hName
gROOT.SetBatch(True)

limits = "tex/allLimits.json"
pDict = {}
#-----------------------------------------------------------------
condorHistDir  = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/MVA_Ntuple" 
#-----------------------------------------------------------------
path = "%s/Disc_Ntuple/DiscMain/Reader/%s/%s/%s"%(condorHistDir, year, decayMode, channel)
print path
discFile = TFile.Open("%s/CombMass/%s/Merged/AllInc_forMain.root"%(path, method))

plotPath = path.replace("Disc_Ntuple/Disc", "Plot_Disc/Plot")
plotPath = "%s/%s/%s/%s"%(plotPath, mass, method, region)
os.system("mkdir -p %s"%plotPath)

sigDisc = discFile.Get("TT_tytg_M%s/%s/Base/%s"%(mass, region, hName))
sigDisc.Scale(1/sigDisc.Integral())
bkgDisc = discFile.Get("TTGamma/%s/Base/%s"%(region, hName))
bkgDisc.Scale(1/bkgDisc.Integral())
pDict["Signal, M%s"%mass] = sigDisc
pDict["All Background"] = bkgDisc

canvas = TCanvas()
legend = TLegend(0.70,0.65,0.85,0.90);
legend.SetFillStyle(0);
legend.SetBorderSize(0);
legend.SetTextFont(42);
legend.SetTextAngle(0);
legend.SetTextSize(0.04);
legend.SetTextAlign(12);
canvas.cd()
maxInt = 0.0;
for index, s in enumerate(pDict.keys()):
    pDict[s].SetLineColor(index+1)
    pDict[s].SetLineWidth(3)
    pDict[s].SetMarkerStyle(20+index);
    pDict[s].SetMarkerColor(index+1);
    pDict[s].GetYaxis().SetTitle("Events (normalized to 1)")
    pDict[s].GetYaxis().SetLabelSize(.040)
    pDict[s].GetXaxis().SetLabelSize(.035)
    if "Disc" in hName:
        pDict[s].GetXaxis().SetTitle("%s_%s"%(hName, method))
    else:
        pDict[s].GetXaxis().SetTitle("%s"%hName)
    if index==0:
        print s
        pDict[s].SetMaximum(1.0)
        #pDict[s].SetMinimum(0.0001)
        pDict[s].Draw("HIST")
    else:
        pDict[s].Draw("Histsame")
    #legName = "%s, mean = %i, int = %i"%(econDict[s][1], pDict[s].GetMean(), pDict[s].Integral())
    legend.AddEntry(pDict[s], s,  "LP")
    canvas.Update()
    
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
chCRName = "#splitline{#font[42]{%s}}{#font[42]{%s}}"%(chName, "")
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
canvas.SaveAs("%s/%s.pdf"%(plotPath, hName))

