import ROOT as rt
from PlotInputs import *
import numpy as np
import sys
#-----------------------------------------
#Get historgams from the root files 
#-----------------------------------------
def getDataHists(inFile, hName, CR):
    dataHist     = []
    for sample in SampleData.keys():
        #hPath = "data_obs/%s/Base/%s"%(CR, hName)
        hPath = "data_obs/%s/Base/%s"%(CR, hName)
        try:
            hist = inFile.Get(hPath)
            hist = hist.Clone("%s_%s_%s"%(sample, CR, hName))
        except Exception:
            print ("Error: Hist not found. \nFile: %s \nHistName: %s"%(inFile, hPath))
            sys.exit()
        dataHist.append(hist)
    return dataHist

def getBkgBaseHists(inFile, hName, CR):
    bkgHists     = []
    for sample in SampleBkg.keys():
        #hPath = "%s/%s/Base/%s"%(sample, CR, hName)
        hPath = "%s/%s/Base/%s"%(sample, CR, hName)
        try:
            hist = inFile.Get(hPath)
            hist = hist.Clone("%s_%s_%s"%(sample, CR, hName))
        except Exception:
            print ("Error: Hist not found. \nFile: %s \nHistName: %s"%(inFile, hPath))
            sys.exit()
        bkgHists.append(hist)
    return bkgHists

def getSigBaseHists(inFile, hName, CR):
    sigHists     = []
    for sample in SampleSignal.keys():
        #hPath = "%s/%s/Base/%s"%(sample, CR, hName)
        hPath = "%s/%s/Base/%s"%(sample, CR, hName)
        try:
            hist = inFile.Get(hPath)
            hist = hist.Clone("%s_%s_%s"%(sample, CR, hName))
        except Exception:
            print ("Error: Hist not found. \nFile: %s \nHistName: %s"%(inFile, hPath))
            sys.exit()
        sigHists.append(hist)
    return sigHists

def getBkgSystHists(inFile, hName, CR, level):
    hSumBkgs = []
    for syst in Systematics:
        hBkg = []
        for sample in SampleSyst:
            hPath = "%s/%s/%s%s/%s"%(sample, syst, level, CR, hName)
            try:
                hist = inFile.Get(hPath)
                hist = hist.Clone("%s_%s/%s%s_%s"%(sample, CR, syst,level,hName))
            except Exception:
                print ("Error: Hist not found. \nFile: %s \nHistName: %s"%(inFile, hPath))
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
    uncGraph = rt.TGraphAsymmErrors( nBins, 
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

#-----------------------------------------
#Sort graph w.r.t to the maximum y-value 
#-----------------------------------------
def sortGraphs(graphs, isReverse = True):
    yieldDict = {}
    for g in graphs:
        yieldDict[g.GetName()] = max(g.GetY())
    if isReverse:
        newDict = sorted(yieldDict.items(), key=lambda x: x[1], reverse=True)
    else:
        newDict = sorted(yieldDict.items(), key=lambda x: x[1])
    gSorted = []
    for i in newDict:
        for g in graphs:
            if i[0]==g.GetName():
                gSorted.append(g)
    return gSorted

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

def createTable(tDict, sList, nCol, tHead, tCaption):
    table = "\\begin{minipage}[c]{0.32\\textwidth}\n"
    table += "\\centering\n"
    table += "\\tiny{\n"
    col = ""
    for i in range(nCol):
        col += "c"
    table += "\\begin{tabular}{%s}\n"%col
    table += "\\hline\n"
    table += tHead 
    table += "\\hline\n"
    row = ""
    #print Samples.keys()
    for key in sList:
        if key in Samples.keys():
            row += "$ %s $"%Samples[key][1].replace("#", "\\")
        else:
            row += key
        for r in tDict[key]:
            row = " %s &  %s"%(row, r)
        row += "\\\\\n"
    table += "%s\\hline\n"%row
    table += "\\end{tabular}\n"
    #table += "\\caption*{table}{%s}\n"%tCaption
    table += "}\n"
    table += "\\end{minipage}\n"
    return table

def getYield(h):
    err = rt.Double(0.0)
    norm = h.IntegralAndError(1, h.GetNbinsX(), err)
    entry = h.GetEntries()
    if(norm!=0):
        y = [int(entry), round(norm, 1), str(round(100*err/norm, 1)) + " (---)"]
    else:
        y = ["0", "0", "0 (---)"]
    #y = [round(norm, 2), round(100*err/norm, 2)]
    return y

def makeRowCat(catHists, hName):
    inc = catHists[hName].Integral()
    gen = catHists["%s_genuine"%hName].Integral()
    nonP = catHists["%s_hadronic_photon"%hName].Integral()
    misid = catHists["%s_misid_ele"%hName].Integral()
    fake = catHists["%s_hadronic_fake"%hName].Integral()
    if(inc==0):
        y = ["0", "0", "0", "0", "0"]
    else:
        y = [round(inc, 1), round(100*gen/inc, 1), round(100*nonP/inc, 1), round(100*misid/inc, 1), round(100*fake/inc, 1)]
    return y

def getRowCat(sample, hName, hDict, catDict):
    oneBkg = {}
    for h in hDict[hName]:
        if sample in h.GetName():
            oneBkg[hName] = h
    for cat in catDict.keys():
        for h in hDict["%s_%s"%(hName, cat)]:
            if sample in h.GetName():
                oneBkg["%s_%s"%(hName, cat)] = h
    row = makeRowCat(oneBkg, hName)
    return row

def getRowCatBkgs(hName, hSum, catBkgs, catDict):
    allBkgs = {}
    allBkgs[hName] = hSum
    for cat in catDict.keys():
        for h in catBkgs:
            if cat in h.GetName():
                allBkgs["%s_%s"%(hName, cat)] = h
    row = makeRowCat(allBkgs, hName)
    return row

def getLumiLabel(year):
    lumi = "35.9 fb^{-1}"
    if "16Pre" in year:
        lumi = "19.7 fb^{-1} (2016PreVFP)"
    if "16Post" in year:
        lumi = "16.2 fb^{-1} (2016PostVFP)"
    if "17" in year:
        lumi = "41.5 fb^{-1} (2017)"
    if "18" in year:
        lumi = "59.7 fb^{-1} (2018)"
    if "__" in year:
        lumi = "137.2 fb^{-1} (Run2)"
    return lumi

def getChLabel(decay, channel):
    nDict   = {"Semilep": "1", "Dilep":2}
    chDict  = {"Mu": "#mu", "Ele": "e"}
    colDict = {"Mu": rt.kBlue, "Ele": rt.kRed}
    name = ""
    for ch in channel.split("__"):
        name += "%s#color[%i]{%s}"%(nDict[decay], colDict[ch], chDict[ch])
    name += ", p_{T}^{miss} #geq 20 GeV"
    return name
