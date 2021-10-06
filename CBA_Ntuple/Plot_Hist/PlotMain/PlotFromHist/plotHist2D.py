from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors
import os
import sys
from optparse import OptionParser
from PlotCMSLumi import *
from PlotTDRStyle import *
from array import array

padGap = 0.01
iPeriod = 4;
iPosX = 10;
setTDRStyle()
xPadRange = [0.0,1.0]
yPadRange = [0.0,0.30-padGap, 0.30+padGap,1.0]

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
gROOT.SetBatch(True)
#-----------------------------------------
#Decorate a histogram
#-----------------------------------------
def decoHist(hist, xTit, yTit, color):
    hist.GetXaxis().SetTitle(yTit);
    hist.GetYaxis().SetTitle(xTit);
    hist.GetXaxis().SetTitleOffset(1.15)
    hist.GetYaxis().SetTitleOffset(1.15)
    hist.GetYaxis().SetTitleSize(0.055)
    hist.GetXaxis().SetTitleSize(0.055)
    hist.GetYaxis().SetLabelSize(0.040)
    hist.GetXaxis().SetLabelSize(0.040)
    #hist.SetFillColor(color);
    hist.SetLineWidth(4)
    hist.SetMinimum(1)
    hist.SetLineColor(color);

#def decoHist(hist, xTit, yTit, color):
def makePlot(xName, yName):
    Red    = [ 1.00, 0.00, 0.00, 0.87, 1.00, 0.51 ]
    Green  = [ 1.00, 0.00, 0.81, 1.00, 0.20, 0.00 ]
    Blue   = [ 1.00, 0.51, 1.00, 0.12, 0.00, 0.00 ]
    Length = [ 0.00, 0.02, 0.34, 0.51, 0.64, 1.00 ]
    lengthArray = array('d', Length)
    redArray = array('d', Red)
    greenArray = array('d', Green)
    blueArray = array('d', Blue)

    #gStyle.SetOptStat(0)
    #gStyle.SetPaintTextFormat('5.1f');
    canvas = TCanvas()
    canvas.SetFillColor(10);
    canvas.SetBorderMode(0);
    canvas.SetBorderSize(0);
    canvas.SetTickx();
    canvas.SetTicky();
    canvas.SetLeftMargin(0.15);
    canvas.SetRightMargin(0.15);
    canvas.SetTopMargin(0.15);
    canvas.SetBottomMargin(0.15);
    canvas.SetFrameFillColor(0);
    canvas.SetFrameBorderMode(0);
       
    #Get nominal histograms
    #file1 = TFile("TTbar_Base_SR.root")
    file1 = TFile("/uscms_data/d3/rverma/codes/CMSSW_10_2_13/src/TopRunII/cms-TT-run2/Hist_Ntuple/hists/2016/Semilep/Mu/TT_tgtg_M800_Base_SR.root")
    #hist = file1.Get("TTbar/Base/SR/%s__%s"%(xName, yName))
    hist = file1.Get("TT_tgtg_M800/Base/SR/%s__%s"%(xName, yName))
    decoHist(hist, xName, yName, 2)
    hist.SetContour(99)
    #hist.Draw('colz, Y+, TEXT0')
    hist.Draw('colz')

    mypal = hist.GetListOfFunctions().FindObject('palette')
    #mypal.SetX1NDC(0.02);
    #mypal.SetX2NDC(0.06);
    #mypal.SetY1NDC(0.1);
    #mypal.SetY2NDC(0.9);
    canvas.Modified();
    canvas.Update();
    chCRName = "#splitline{#font[42]{%s}}{#font[42]{%s}}"%("mu", "extra")
    extraText   = "#splitline{Preliminary}{%s}"%("#mu + jets")
    #CMS_lumi(canvas, iPeriod, iPosX, extraText)

    canvas.SaveAs("pdf/2d_%s_%s.png"%(xName, yName))

#-----------------------------------------
#Finally make the plot for each histogram
#----------------------------------------
#makePlot("presel_M3", "presel_chi2")        
#makePlot("presel_TopHad_mass", "presel_chi2")
#makePlot("presel_TopTop_mass", "presel_chi2")
#makePlot("presel_TopLep_mass", "presel_chi2")

makePlot("presel_TopHad_mass", "presel_chi2")
makePlot("presel_TopLep_mass", "presel_chi2")
makePlot("presel_TopStarHad_mass", "presel_chi2")
makePlot("presel_TopStarLep_mass", "presel_chi2")
makePlot("presel_TopStar_mass", "presel_chi2")
makePlot("presel_TopHad_mass", "presel_TopLep_mass")
makePlot("presel_TopStarHad_mass", "presel_TopStarLep_mass")

#makePlot("presel_chi2","presel_M3"          )        
#makePlot("presel_chi2","presel_TopHad_mass" )
#makePlot("presel_chi2","presel_TopTop_mass" )
#makePlot("presel_chi2","presel_TopLep_mass" )
