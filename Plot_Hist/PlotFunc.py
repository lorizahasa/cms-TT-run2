from ROOT import TLegend, TGraphAsymmErrors
from PlotInputs import *
import numpy as np
import sys
#-----------------------------------------
#Get historgams from the root files 
#-----------------------------------------
def getDataHists(fileDict, hName, CR):
    dataHist     = []
    for sample in SampleData.keys():
        hPath = "data_obs/%s/Base/%s"%(CR, hName)
        try:
            hist = fileDict[sample].Get(hPath)
            hist = hist.Clone("%s_%s_%s"%(sample, CR, hName))
        except Exception:
            print ("Error: Hist not found. \nFile: %s \nHistName: %s"%(fileDict[sample], hPath))
            sys.exit()
        dataHist.append(hist)
    return dataHist

def getBkgBaseHists(fileDict, hName, CR):
    bkgHists     = []
    for sample in SampleBkg.keys():
        hPath = "%s/%s/Base/%s"%(sample, CR, hName)
        try:
            hist = fileDict[sample].Get(hPath)
            hist = hist.Clone("%s_%s_%s"%(sample, CR, hName))
        except Exception:
            print ("Error: Hist not found. \nFile: %s \nHistName: %s"%(fileDict[sample], hPath))
            sys.exit()
        bkgHists.append(hist)
    return bkgHists

def getSigBaseHists(fileDict, hName, CR):
    sigHists     = []
    for sample in SampleSignal.keys():
        hPath = "%s/%s/Base/%s"%(sample, CR, hName)
        try:
            hist = fileDict[sample].Get(hPath)
            hist = hist.Clone("%s_%s_%s"%(sample, CR, hName))
        except Exception:
            print ("Error: Hist not found. \nFile: %s \nHistName: %s"%(fileDict[sample], hPath))
            sys.exit()
        sigHists.append(hist)
    return sigHists

def getBkgSystHists(fileDict, hName, CR, level):
    hSumBkgs = []
    for syst in Systematics:
        hBkg = []
        for sample in SampleSyst:
            hPath = "%s/%s/%s%s/%s"%(sample, syst, level, CR, hName)
            try:
                hist = fileDict[sample].Get(hPath)
                hist = hist.Clone("%s_%s/%s%s_%s"%(sample, CR, syst,level,hName))
            except Exception:
                print ("Error: Hist not found. \nFile: %s \nHistName: %s"%(fileDict[sample], hPath))
                sys.exit()
            hBkg.append(hist)
            hSum.Add(h)
        hSum = hist.Clone("hSumBkgs_%s_%s%s_%s"%(CR, syst,level,hName))
        hSum.Reset()
        for h in hBkg:
            hSum.Add(h)
        hSumBkgs.append(hSum)
    return hSumBkgs

#-----------------------------------------
#Decorate a histogram
#-----------------------------------------
def decoHist(hist, xTit, yTit, color):
    hist.GetXaxis().SetTitle(xTit);
    hist.GetYaxis().SetTitle(yTit);
    hist.SetFillColor(color);
    hist.GetXaxis().SetTitle(xTit);
    hist.GetYaxis().SetTitle(yTit)
    hist.GetYaxis().CenterTitle()
    hist.GetXaxis().SetTitleOffset(1.0)
    hist.GetYaxis().SetTitleOffset(1.0)
    hist.GetXaxis().SetTitleSize(0.05);
    hist.GetYaxis().SetTitleSize(0.05);
    hist.GetXaxis().SetTitleSize(0.05);
    hist.GetYaxis().SetTitleSize(0.05);

def decoHistSig(hist, xTit, yTit, color):
    hist.GetXaxis().SetTitle(xTit);
    hist.GetYaxis().SetTitle(yTit);
    hist.SetFillColor(color);
    #hist.Scale(10)
    hist.SetLineColor(color)
    hist.SetLineStyle(2)
    hist.SetLineWidth(4) 
    hist.SetFillColor(0)

def decoHistRatio(hist, xTit, yTit, color):
    #hist.SetFillColor(color);
    hist.SetLineColor(color);
    hist.GetXaxis().SetTitle(xTit);
    hist.GetYaxis().SetTitle(yTit);
    hist.GetXaxis().SetTitleSize(0.11);
    hist.GetXaxis().SetLabelSize(0.10);
    hist.GetXaxis().SetLabelFont(42);
    #hist.GetXaxis().SetLabelColor(kBlack);
    #hist.GetXaxis().SetAxisColor(kBlack);
    hist.GetYaxis().SetRangeUser(0.0, 2.0);
    hist.GetXaxis().SetTitleOffset(1);
    hist.GetXaxis().SetLabelOffset(0.01);
    hist.SetMarkerStyle(20); 
    hist.SetMarkerColor(color)
    #hist.SetMarkerSize(1.2);
    hist.GetYaxis().SetTitleSize(0.11);
    hist.GetYaxis().SetLabelSize(0.10);
    hist.GetYaxis().SetLabelFont(42);
    #hist.GetYaxis().SetAxisColor(1);
    hist.GetYaxis().SetNdivisions(6,5,0);
    #hist.GetXaxis().SetTickLength(0.06);
    hist.GetYaxis().SetTitleOffset(0.6);
    hist.GetYaxis().SetLabelOffset(0.01);
    hist.GetYaxis().CenterTitle();

#-----------------------------------------
#Get uncertainty band for the total bkg
#-----------------------------------------
def getUncBand(hBase, hDiffUp, hDiffDown, isRatio):
    '''
    The uncertainty band is formed by up and down
    fluctuation of nominal event yield. In every
    bin we have a nominal value from the base
    histogram and up/down values from other two.
    We draw nominal + up and nominal - down as 
    error band on the top pannel. On the bottom (ratio)
    pannel, we draw 1+ up/nominal, 1-nominal/down as
    error band.
    '''
    yValues     = []
    yErrorsUp   = []
    yErrorsDown = []
    xValues     = []
    xErrorsUp   = []
    xErrorsDown = []
    nBins = hBase.GetNbinsX()
    for i in range(nBins):
        yValue      = hBase.GetBinContent(i+1)
        statError   = hBase.GetBinError(i+1)
        yErrorUp    = abs(hDiffUp.GetBinContent(i+1))+statError 
        yErrorDown  = abs(hDiffDown.GetBinContent(i+1))+statError 
        if isRatio:
            yValues.append(1)
            if yValue >0:
                yErrorsUp.append(abs(yErrorUp)/yValue)
                yErrorsDown.append(abs(yErrorDown)/yValue)
            else:
                yErrorsUp.append(0.0)
                yErrorsDown.append(0.0)
        else:
            yValues.append (yValue)
            yErrorsUp.append(abs(yErrorUp))
            yErrorsDown.append(abs(yErrorDown))
    
        xValues.append(hBase.GetBinCenter(i+1))
        xErrorsUp.append(hBase.GetBinWidth(i+1)/2)
        xErrorsDown.append(hBase.GetBinWidth(i+1)/2)
    uncGraph = TGraphAsymmErrors( nBins, 
            np.array(xValues    , dtype='double'),
            np.array(yValues    , dtype='double'),
            np.array(xErrorsDown, dtype='double'),
            np.array(xErrorsUp  , dtype='double'),
            np.array(yErrorsDown, dtype='double'),
            np.array(yErrorsUp  , dtype='double'))
    return uncGraph

#-----------------------------------------
#Legends for all histograms, graphs
#-----------------------------------------
def decoLegend(legend, nCol, textSize):
    #legend.SetNColumns(nCol);
    legend.SetFillStyle(0);
    legend.SetBorderSize(0);
    #legend.SetFillColor(kBlack);
    legend.SetTextFont(42);
    legend.SetTextAngle(0);
    legend.SetTextSize(textSize);
    legend.SetTextAlign(12);
    return legend

#-----------------------------------------
#Sort histograms w.r.t to the event yield
#-----------------------------------------
def sortHists(hAllBkgs, isReverse):
    '''
    We sort the histograms in both orders.
    They are sorted in acending/decending
    orders for stack/legend.
    '''
    yieldDict = {}
    for h in hAllBkgs:
        yieldDict[h.GetName()] = h.Integral()
    if isReverse:
        newDict = sorted(yieldDict.items(), key=lambda x: x[1], reverse=True)
    else:
        newDict = sorted(yieldDict.items(), key=lambda x: x[1])
    hSorted = []
    for i in newDict:
        for h in hAllBkgs:
            if i[0]==h.GetName():
                hSorted.append(h)
    return hSorted

#----------------------------------------------------------
#Reformat jet multiplicity string 
#----------------------------------------------------------
#Jet selection naming: a3j_e2b = atleast 3 jet, out of which 2 are b jets: nJet >= 3, nBJet ==2
def formatCRString(region):
    name = region
    name = name.replace("FatJet_size", "AK8")
    name = name.replace("Jet_size", "AK4")
    name = name.replace("Jet_b_size", "b")
    name = name.replace("Photon_size", "#gamma")
    name = name.replace("Photon_et", "p_{T}^{#gamma}")
    name = name.replace(" &&", ",")
    name = name.replace(">=", "#geq ")
    name = name.replace("==", "=")
    return name 
