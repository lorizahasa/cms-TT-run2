from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors
import os
import sys
from optparse import OptionParser
from PlotCMSLumi import *
from PlotTDRStyle import *
from collections import OrderedDict

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
parser.add_option("--hName", "--hName", dest="hName", default="presel_TopStar_mass",type='str',
                     help="Specifyi the histogram to be overlayed" )
(options, args) = parser.parse_args()
hName            = options.hName
fDir             = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Hist_Ntuple/2016/Semilep/Mu"

sampleDict = {}
#sampleDict['DataMu']        = ['data_obs', 'Data_obs', 1]
sampleDict['TTGamma']         = ['TTGamma', 'TTGamma', 63]
#sampleDict['TTbar']         = ['TTbar', 'SM ttbar', 2]
#sampleDict['SingleTop']         = ['SingleTop', 'Single t', 53]
#sampleDict['TT_tytg_M700']  = ['TT_tytg_M700', 'tytg (700)', 3]
sampleDict['TT_tytg_M800']  = ['TT_tytg_M800', 'tytg (800)', 4]
#sampleDict['TT_tytg_M900']  = ['TT_tytg_M900', 'tytg (900)', 5]
#sampleDict['TT_tytg_M1000'] = ['TT_tytg_M1000', 'tytg (1000)', 6]
#sampleDict['TT_tytg_M1100'] = ['TT_tytg_M1100', 'tytg (1100)', 7]
sampleDict['TT_tytg_M1200'] = ['TT_tytg_M1200', 'tytg (1200)', 8]
#sampleDict['TT_tytg_M1300'] = ['TT_tytg_M1300', 'tytg (1300)', 9]
#sampleDict['TT_tytg_M1400'] = ['TT_tytg_M1400', 'tytg (1400)', 10]
#sampleDict['TT_tytg_M1500'] = ['TT_tytg_M1500', 'tytg (1500)', 30]
sampleDict['TT_tytg_M1600'] = ['TT_tytg_M1600', 'tytg (1600)', 40]
sampleDict = OrderedDict(sorted(sampleDict.items()))


gROOT.SetBatch(True)
#-----------------------------------------
#Decorate a histogram
#-----------------------------------------
def decoHist(hist, xTit, yTit, color):
    hist.GetXaxis().SetTitle(xTit);
    hist.GetYaxis().SetTitle(yTit);
    hist.GetXaxis().SetTitleOffset(1.15)
    hist.GetYaxis().SetTitleOffset(1.35)
    hist.GetYaxis().SetTitleSize(0.055)
    hist.GetYaxis().SetLabelSize(0.055)
    hist.GetXaxis().SetTitleSize(0.055)
    #hist.SetFillColor(color);
    hist.SetLineWidth(4)
    hist.SetMinimum(1)
    hist.SetLineColor(color);

#def decoHist(hist, xTit, yTit, color):
def decoHistRatio(hist, xTit, yTit, color):
    hist.GetXaxis().SetTitle(xTit);
    hist.GetYaxis().SetTitle(yTit);
    hist.GetXaxis().SetTitleSize(0.11);
    hist.GetXaxis().SetLabelSize(0.10);
    hist.GetXaxis().SetLabelFont(42);
    #hist.GetXaxis().SetLabelColor(kBlack);
    #hist.GetXaxis().SetAxisColor(kBlack);
    hist.GetYaxis().SetRangeUser(0, 2);
    hist.GetXaxis().SetTitleOffset(1);
    hist.GetXaxis().SetLabelOffset(0.01);
    hist.SetMarkerStyle(20); 
    #hist.SetMarkerSize(1.2);
    hist.GetYaxis().SetTitleSize(0.11);
    hist.GetYaxis().SetLabelSize(0.10);
    hist.GetYaxis().SetLabelFont(42);
    #hist.GetYaxis().SetAxisColor(1);
    hist.GetYaxis().SetNdivisions(6,5,0);
    hist.GetXaxis().SetTickLength(0.06);
    hist.GetYaxis().SetTitleOffset(0.6);
    hist.GetYaxis().SetLabelOffset(0.01);
    hist.GetYaxis().CenterTitle();

#-----------------------------------------
#Make a plot for one histogram
#----------------------------------------
#Divide canvas for the ratio plot
isLog    = False
canvas = TCanvas()
gPad.SetRightMargin(1.0)
if isLog:
    gPad.SetLogy(True);
xTitle = hName
yTitle = "Events"
fDict = {}
for s in sampleDict.keys():
    file_ = TFile("%s/%s_Base_SR.root"%(fDir, s))
    fDict[s] = file_

hDict = {}
for s in sampleDict.keys():
    h = fDict[s].Get("%s/Base/SR/%s"%(sampleDict[s][0], hName))
    decoHist(h, xTitle, yTitle, sampleDict[s][2])
    h.Scale(1/h.Integral())
    hDict[s] = h

legend = TLegend(0.45,0.70,0.92,0.88);
legend.SetFillStyle(0);
legend.SetBorderSize(0);
legend.SetTextFont(42);
legend.SetTextAngle(0);
legend.SetTextSize(0.030);
legend.SetTextAlign(12);
canvas.cd()
maxInt = 0.0;
for index, s in enumerate(sampleDict.keys()):
    if index==0:
        #hDict[s].SetMarkerStyle(20)
        #hDict[s].Draw("EP")
        hDict[s].SetMaximum(1.1* hDict[s].Integral())
        hDict[s].Draw("HIST")
    else:
        hDict[s].Draw("Histsame")
    #legName = "%s, mean = %i, int = %i"%(sampleDict[s][1], hDict[s].GetMean(), hDict[s].Integral())
    legName = "%s, mean = %i"%(sampleDict[s][1], hDict[s].GetMean())
    legend.AddEntry(hDict[s], legName,  "PEL")
    if maxInt<hDict[s].Integral():
        maxInt = hDict[s].Integral()
    if isLog:
        hDict[s].GetYaxis().SetRangeUser(0.1, 100*maxInt);
    else:
        #hDict[s].GetYaxis().SetRangeUser(0, 1.5*maxInt);
        hDict[s].GetYaxis().SetRangeUser(0, 0.3);
    #hDict[s].GetXaxis().SetRangeUser(0, 300);
    #hDict[s].SetMaximum(0.5)
    canvas.Update()
legend.Draw()
chCRName = "#splitline{#font[42]{%s}}{#font[42]{%s}}"%("mu", "extra")
extraText   = "#splitline{Preliminary}{%s}"%("#splitline{1 #mu, >= 1 #gamma}{>= 5 jets, ==2 b}")
CMS_lumi(canvas, iPeriod, iPosX, extraText)
canvas.SaveAs("pdf/%s.png"%( hName))

