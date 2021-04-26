from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors
import ROOT as rt
import os
import numpy
import sys
import math
from optparse import OptionParser
from PlotInputs import *
from PlotFunc import *
from PlotCMSLumi import *
from PlotTDRStyle import *

padGap = 0.01
iPeriod = 4;
iPosX = 10;
setTDRStyle()
xPadRange = [0.0,1.0]
yPadRange = [0.0,0.30-padGap, 0.30+padGap,1.0]

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decayMode", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decayMode moded of ttbar SemiLep or DiLep? default is SemiLep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
		  help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="TTbar",type='str',
		  help="name of the MC sample" )
parser.add_option("--ps", "--phaseSpace", dest="phaseSpace", default="Boosted_SR",type='str', 
                     help="which control selection and region")
parser.add_option("--plot", "--plot", dest="hName", default="Weight_mu",type='str', 
                     help="name of the histogram")
(options, args) = parser.parse_args()
year            = options.year
decayMode       = options.decayMode
channel         = options.channel
sample          = options.sample
hName            = options.hName
phaseSpace = options.phaseSpace
print "------------------------------------"
print "%s, %s, %s, %s, %s"%(year, decayMode, channel, sample, hName)
print "------------------------------------"

#-----------------------------------------
#Get histograms
#----------------------------------------
inHistSubDir = "%s/%s/%s/Merged"%(year, decayMode, channel)
inHistFullDir = "%s/Hist_Ntuple/%s"%(condorHistDir, inHistSubDir)
outPlotSubDir = "Plot_Hist/%s/Syst/%s/%s/%s"%(year, decayMode, channel, phaseSpace)
outPlotFullDir = "%s/%s"%(condorHistDir, outPlotSubDir)
if not os.path.exists(outPlotFullDir):
    os.makedirs(outPlotFullDir)
rootFile = TFile("%s/AllInc.root"%(inHistFullDir), "read")
print rootFile
#print("%10s %10s %10s %10s, %10s"%("Systematics", "Down", "Base", "Up", "RelativeUnc"))
print("%10s %22s %22s %22s %10s"%("Syst", "Down", "Base", "Up", "Unc"))
print("%10s %6s %8s %8s %6s %8s %8s %6s %8s %8s %5s"%("", 
"UnderF", "Int", "OverF", 
"UnderF", "Int", "OverF", 
"UnderF", "Int", "OverF", ""))
def checkNanInBins(hist):
    checkNan = False
    for b in range(hist.GetNbinsX()):
        if math.isnan(hist.GetBinContent(b)):
            print "%s: bin %s is nan"%(hist.GetName(), b)
            checkNan = True
    return checkNan
            
allHistUp = []
allHistDown = []
allSystPercentage = {}
hPathBase = "%s/%s/Base/%s"%(sample, phaseSpace, hName)
hPathUp   = "%s/%s/Base/%s_up"%(sample, phaseSpace, hName)
hPathDown   = "%s/%s/Base/%s_down"%(sample, phaseSpace, hName)
if "btag" in hName:
    hPathUp   = "%s/%s/Base/%s_b_up"%(sample, phaseSpace, hName)
    hPathDown   = "%s/%s/Base/%s_b_down"%(sample, phaseSpace, hName)
print hPathBase
hBase = rootFile.Get(hPathBase).Clone("Base_")
hUp   = rootFile.Get(hPathUp).Clone("%sUp_") 
hDown = rootFile.Get(hPathDown).Clone("%sDown_") 
hBase.Sumw2(1)
hUp.Sumw2(1)
hDown.Sumw2(1)
col_depth = 0
hBase.GetYaxis().SetTitle("Events")
hBase.SetLineColor(rt.kOrange + col_depth)
hUp.SetLineColor(rt.kSpring  + col_depth)
hDown.SetLineColor(rt.kPink + col_depth)
hBase.SetMarkerColor(rt.kOrange + col_depth)
hUp.SetMarkerColor(rt.kSpring  + col_depth)
hDown.SetMarkerColor(rt.kPink + col_depth)
hBase.SetLineWidth(4)
hUp.SetLineWidth(4)
hDown.SetLineWidth(4)
#decoHist(hBase, hName, "Events", rt.kOrange + col_depth)
#decoHist(hUp, hName, "Events", rt.kSpring + col_depth)
#decoHist(hDown, hName, "Events", rt.kPink + col_depth)
#-----------------------------------------
# Sanity checks
#----------------------------------------
evtBase = hBase.Integral()
evtUp   = hUp.Integral()
evtDown = hDown.Integral()
#check if intergal is 0
#if evtUp ==0.0 or evtBase ==0.0 or evtDown ==0.0:
#i = integral, u = undeflow, o = overflow
iEvtBase = round(hBase.Integral(),0)
iEvtUp   = round(hUp.Integral(),0)
iEvtDown = round(hDown.Integral(),0)
uEvtBase = round(hBase.GetBinContent(0),0)
uEvtUp   = round(hUp.GetBinContent(0),0)
uEvtDown = round(hDown.GetBinContent(0),0)
oEvtBase = round(hBase.GetBinContent(hBase.GetNbinsX()+1),0)
oEvtUp   = round(hUp.GetBinContent(hUp.GetNbinsX()+1),0)
oEvtDown = round(hDown.GetBinContent(hDown.GetNbinsX()+1),0)
if uEvtBase >1000 or oEvtBase >1000:
    print "%s: Base:  Overflow or Undeflow is more than 1000"%hName
if uEvtUp >1000 or oEvtUp >1000:
    print "%s: Up:  Overflow or Undeflow is more than 1000"%hName
if uEvtDown >1000 or oEvtDown >1000:
    print "%s: Down:  Overflow or Undeflow is more than 1000"%hName
if evtBase ==0.0:
    print "evtBase is zero"
#check if intergal is NaN
if math.isnan(evtUp) or math.isnan(evtDown):
    print "Inegral is nan"
#check if bins are nan
if checkNanInBins(hUp) or checkNanInBins(hBase) or checkNanInBins(hDown):
    print "Some of the bins are nan"
allSystPercentage[hName] = 100*max(abs(evtUp -evtBase),abs(evtBase-evtDown))/evtBase
print("%10s" 
       "|%6.0f %8.0f %8.0f"
       "|%6.0f %8.0f %8.0f"
       "|%6.0f %8.0f %8.0f"
       "|%5.0f%%"%(hName, 
     uEvtDown, iEvtDown, oEvtDown, 
     uEvtBase, iEvtBase, oEvtBase, 
     uEvtUp, iEvtUp, oEvtUp,
    allSystPercentage[hName]))
if allSystPercentage[hName] > 100.0:
    print "Large uncertainty for %s: %10.2f"%(hName, allSystPercentage[hName])

#-----------------------------------------
# Draw histograms 
#----------------------------------------
gROOT.SetBatch(True)
canvas = TCanvas()
canvas.Divide(1, 2)
canvas.cd(1)
gPad.SetRightMargin(0.03);
gPad.SetPad(xPadRange[0],yPadRange[2],xPadRange[1],yPadRange[3]);
gPad.SetTopMargin(0.09);
gPad.SetBottomMargin(padGap);
#gPad.SetTickx(0);
gPad.RedrawAxis();
gPad.SetLogy(True)
hBase.Draw("EP")
hUp.Draw("EPsame")
hDown.Draw("EPsame")
lumi_13TeV = "35.9 fb^{-1}"
col_year  = rt.kGreen
if "16" in year:
    col_depth = -3
    lumi_13TeV = "35.9 fb^{-1} (#color[%i]{2016})"%(col_year+col_depth)
if "17" in year:
    col_depth = -2
    lumi_13TeV = "41.5 fb^{-1} (#color[%i]{2017})"%(col_year + col_depth)
if "18" in year:
    col_depth = -1
    lumi_13TeV = "59.7 fb^{-1} (#color[%i]{2018})"%(col_year + col_depth)
#Draw CMS, Lumi, channel
if channel in ["mu", "Mu", "m"]:
    chName = "1 #color[2]{#mu}, %s"%sample
else:
    chName = "1 #color[6]{e}, %s"%sample
#crName = formatCRString(phaseSpace)
#chName = "%s, %s"%(chName, phaseSpace)
#chCRName = "#splitline{#font[42]{%s}}{#font[42]{%s}}"%(chName, crName)
chCRName = "%s"%chName
extraText   = "#splitline{Preliminary}{%s}"%chCRName
#CMS_lumi(canvas, iPeriod, iPosX, extraText)
CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
#Draw Leg
leg = TLegend(0.20,0.45,0.35,0.75)
leg.AddEntry(hDown, "#splitline{down}{(mean = %s)}"%str(round(hDown.GetMean(),4)), "EPL")
leg.AddEntry(hBase, "#splitline{nominal}{(mean = %s)}"%str(round(hBase.GetMean(),4)), "EPL")
leg.AddEntry(hUp,   "#splitline{up}{(mean = %s)}"%str(round(hUp.GetMean(),4)), "EPL")
decoLegend(leg, 5, 0.034)
leg.Draw("same")

canvas.cd(2)
gPad.SetTopMargin(padGap); 
gPad.SetBottomMargin(0.30); 
gPad.SetRightMargin(0.03);
#gPad.SetTickx(0);
gPad.SetPad(xPadRange[0],yPadRange[0],xPadRange[1],yPadRange[2]);
gPad.RedrawAxis();
hRatioUp = hUp.Clone("hRatio_up")
hRatioUp.Divide(hBase)
print "hBaseCont = ", hBase.GetBinContent(20);
print "hBaseErr = ",  hBase.GetBinError(20);
print "hUpCont = ", hUp.GetBinContent(20);
print "hUpErr = ",  hUp.GetBinError(20);
print "hRatioUpCont = ", hRatioUp.GetBinContent(20);
print "hRatioUpErr = ",  hRatioUp.GetBinError(20);

decoHistRatio(hRatioUp, hName, "#frac{(up or down)}{nominal}", rt.kSpring)
hRatioUp.SetLineWidth(4)
hRatioDown = hDown.Clone("hRatio_up")
hRatioDown.Divide(hBase)
hRatioDown.SetLineWidth(4)
decoHistRatio(hRatioDown, hName, "Ratio", rt.kPink)
hRatioUp.Draw("EP")
hRatioDown.Draw("EPsame")

#Draw Baseline
baseLine = TF1("baseLine","1", -100, 2000);
baseLine.SetLineColor(1);
baseLine.Draw("same");
#canvas.SaveAs("%s/%s.pdf"%(outPlotFullDir, hName))
canvas.SaveAs("%s/%s_%s_%s_%s.pdf"%(outPlotFullDir, hName, year, channel, sample))
#canvas.SaveAs("SystRatio_%s_%s_%s_%s_%s_%s.pdf"%(year, decayMode, channel, hName, sample, phaseSpace))
