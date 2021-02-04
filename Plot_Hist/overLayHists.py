from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors
import os
import sys
from optparse import OptionParser
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
parser.add_option("--hName", "--hName", dest="hName", default="presel_M3",type='str',
                     help="Specifyi the histogram to be overlayed" )
(options, args) = parser.parse_args()
hName            = options.hName
fDir             = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Hist_Ntuple/2016/Semilep/Mu/"

sampleName = []
sampleName.append('TTbar')
sampleName.append('TTGamma')
sampleName.append('TT_tgtg_M800')
sampleName.append('TT_tytg_M800')
sampleName.append('TT_tyty_M800')


gROOT.SetBatch(True)
#-----------------------------------------
#Decorate a histogram
#-----------------------------------------
def decoHist(hist, xTit, yTit, color):
    hist.GetXaxis().SetTitle(xTit);
    hist.GetYaxis().SetTitle(yTit);
    hist.GetXaxis().SetTitleOffset(1.15)
    hist.GetYaxis().SetTitleOffset(1.15)
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
def makePlot(hName, isLog, isRatio):
    #Divide canvas for the ratio plot
    canvas = TCanvas()
    if isRatio:
        canvas.Divide(1,2)
        canvas.cd(1)
        gPad.SetRightMargin(0.03);
        gPad.SetPad(xPadRange[0],yPadRange[2],xPadRange[1],yPadRange[3]);
        gPad.SetTopMargin(0.09);
        gPad.SetBottomMargin(padGap);
        #gPad.SetTickx(0);
        gPad.RedrawAxis();
    if isLog:
        gPad.SetLogy(True);

    #Get nominal histograms
    file1 = TFile("%s/%s_Base_SR.root"%(fDir, sampleName[0]))
    file2 = TFile("%s/%s_Base_SR.root"%(fDir, sampleName[1]))
    file3 = TFile("%s/%s_Base_SR.root"%(fDir, sampleName[2]))
    file4 = TFile("%s/%s_Base_SR.root"%(fDir, sampleName[3]))
    file5 = TFile("%s/%s_Base_SR.root"%(fDir, sampleName[4]))
    hist1 = file1.Get("%s/Base/SR/%s"%(sampleName[0], hName))
    hist2 = file2.Get("%s/Base/SR/%s"%(sampleName[1], hName))
    hist3 = file3.Get("%s/Base/SR/%s"%(sampleName[2], hName))
    hist4 = file4.Get("%s/Base/SR/%s"%(sampleName[3], hName))
    hist5 = file5.Get("%s/Base/SR/%s"%(sampleName[4], hName))

    #Draw data
    xTitle = hName
    yTitle = "Events"
    decoHist(hist1, xTitle, yTitle, 2)
    decoHist(hist2, xTitle, yTitle, 3)
    decoHist(hist3, xTitle, yTitle, 4)
    decoHist(hist4, xTitle, yTitle, 6)
    decoHist(hist5, xTitle, yTitle, 7)
    hist1.SetMarkerStyle(20)
    hist1.Draw("Histsame")
    hist2.Draw("Histsame")
    hist3.Draw("Histsame")
    hist4.Draw("Histsame")
    hist5.Draw("Histsame")

    #Draw legend
    legend = TLegend(0.45,0.70,0.92,0.88);
    legend.SetFillStyle(0);
    legend.SetBorderSize(0);
    #legend.SetFillColor(kBlack);
    legend.SetTextFont(42);
    legend.SetTextAngle(0);
    legend.SetTextSize(0.030);
    legend.SetTextAlign(12);
    legend.AddEntry(hist1, "tt   ,mean = %i, entries = %i"%(hist1.GetMean(), hist1.GetEntries()), "PEL")
    legend.AddEntry(hist2, "tty  ,mean = %i, entries = %i"%(hist2.GetMean(), hist2.GetEntries()), "PEL")
    legend.AddEntry(hist3, "tgtg ,mean = %i, entries = %i"%(hist3.GetMean(), hist3.GetEntries()), "PEL")
    legend.AddEntry(hist4, "tytg ,mean = %i, entries = %i"%(hist4.GetMean(), hist4.GetEntries()), "PEL")
    legend.AddEntry(hist5, "tyty ,mean = %i, entries = %i"%(hist5.GetMean(), hist5.GetEntries()), "PEL")
    legend.Draw("same")
    chCRName = "#splitline{#font[42]{%s}}{#font[42]{%s}}"%("mu", "extra")
    extraText   = "#splitline{Preliminary}{%s}"%("#mu + jets")
    CMS_lumi(canvas, iPeriod, iPosX, extraText)

    #Draw the ratio 
    if isRatio:
        canvas.cd(2)
        gPad.SetTopMargin(padGap); 
        gPad.SetBottomMargin(0.30); 
        gPad.SetRightMargin(0.03);
        #gPad.SetTickx(0);
        gPad.SetPad(xPadRange[0],yPadRange[0],xPadRange[1],yPadRange[2]);
        gPad.RedrawAxis();
        hRatio = hist1.Clone("hRatio")
        hRatio.Divide(hist2)
        decoHistRatio(hRatio, xTitle, "hist1/hist2", 1)
        hRatio.Draw("EP")
        baseLine = TF1("baseLine","1", -100, 2000);
        baseLine.SetLineColor(1);
        baseLine.Draw("same");
        #hRatio.Draw("EPsame")
    canvas.SaveAs("pdf/%s.pdf"%( hName))

#-----------------------------------------
#Finally make the plot for each histogram
#----------------------------------------
isLog    = True
isRatio  = False
makePlot(hName, isLog, isRatio)
