import os
import sys
import math
import numpy
import itertools
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("PlotMisIDSF", "")) 
sys.path.insert(0, os.getcwd().replace("Plot_Hist/PlotMisIDSF", "Hist_Ntuple/HistMisIDSF"))
from optparse import OptionParser
from PlotFunc import *
from PlotCMSLumi import *
from PlotTDRStyle import *
from HistInputs import Regions, SystLevels
from HistInfo import GetHistogramInfo 
from PlotInputs import *
from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, TF1, TH1F

hInfo = GetHistogramInfo()
hList = hInfo.keys()
rList = Regions.keys()
padGap = 0.01
iPeriod = 4;
iPosX = 10;
setTDRStyle()
xPadRange = [0.0,1.0]
yPadRange = [0.0,0.30-padGap, 0.30+padGap,1.0]

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Check for minimum inputs")
parser.add_option("--isSep","--isSep", dest="isSep",action="store_true",default=False, help="Merge for separate years and channels")
parser.add_option("--isComb","--isComb", dest="isComb",action="store_true",default=False, help="Merge for combined years and channels")
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep = options.isSep
isComb = options.isComb
outTxt = ""

if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
    rList  = [rList[0]]
    hList = [hList[0]]
if isSep: 
    isComb = False
    outTxt = "SepYears"
if isComb:
    isSep  = False
    outTxt = "CombYears"
    Years = Years_
    Channels = Channels_
if not isCheck and not isSep and not isComb:
    print("Add either --isCheck or --isSep or --isComb in the command line")
    exit()

def checkNanInBins(hist):
    checkNan = False
    for b in range(hist.GetNbinsX()):
        if math.isnan(hist.GetBinContent(b)):
            print "%s: bin %s is nan"%(hist.GetName(), b)
            checkNan = True
    return checkNan
                
#-----------------------------------------
#Path of the I/O histrograms/plots
#----------------------------------------
#dir_ = "Merged"
#dir_ = "Rebin"
dir_ = "ForMisIDSF"
os.system("mkdir -p %s"%dirPlot)
fPath = open("%s/syst%s_%s.txt"%(dirPlot, dir_, outTxt), 'w')

allBkgs = True
sample  = "WGamma"
for decay, region, hName, channel, year in itertools.product(Decays, rList, hList, Channels, Years):
    print("----------------------------------------------")
    print("%s, %s, %s, %s, %s"%(decay, hName, region, channel, year))
    if "tt_" in region and ("gamma" in hName or "Pho" in hName): 
        continue 
    if ("Ele" in hName and "Mu" in channel):
        continue
    if ("Mu" in hName and "Ele" in channel):
        continue
    ydc = "%s/%s/%s"%(year, decay, channel)
    inHistDir  = "%s/%s/%s"%(dirHist, dir_, ydc)
    outPlotDir = "%s/%s/%s"%(dirPlot, dir_, ydc)
    os.system("mkdir -p %s"%outPlotDir)
    inFile = TFile("%s/AllInc.root"%(inHistDir), "read")
    if isCheck:
        print(inFile)
    gROOT.SetBatch(True)
    #canvas = TCanvas("ImpactOfSyst", "ImpactOfSyst", 1600, 1000)
    canvas = TCanvas()
    canvas.cd()
    gPad.SetRightMargin(0.17);
    gPad.SetTopMargin(0.09);
    #gPad.SetLeftMargin(0.10);
    #gPad.SetBottomMargin(0.15);
    #gPad.SetTickx(0);
    #gPad.SetLogy(True);
    gPad.RedrawAxis();
    #print("%10s %10s %10s %10s, %10s"%("Systematics", "Down", "Base", "Up", "RelativeUnc"))
    print("%10s %22s %22s %22s %10s"%("Syst", "Down", "Base", "Up", "Unc"))
    print("%10s %6s %8s %8s %6s %8s %8s %6s %8s %8s %5s"%("", 
    "UnderF", "Int", "OverF", 
    "UnderF", "Int", "OverF", 
    "UnderF", "Int", "OverF", ""))
    allHistUp = []
    allHistDown = []
    allSystPercentage = {}
    print Systematics
    for index, syst in enumerate(Systematics):
        if "ele" in syst and "u" in channel: continue
        if "mu" in syst and "e" in channel: continue
        if allBkgs:
            for i, s in enumerate(Samples):
                hPathBase   = "%s/%s/Base/%s"%(s, region, hName)
                hPathUp     = "%s/%s/%sUp/%s"%(s, region, syst, hName)
                hPathDown   = "%s/%s/%sDown/%s"%(s, region, syst, hName)
                if i==0:
                    hBase = inFile.Get(hPathBase).Clone("Base_")
                    hUp   = inFile.Get(hPathUp).Clone("%sUp_"%syst) 
                    hDown = inFile.Get(hPathDown).Clone("%sDown_"%syst)
                else:
                    hBase.Add(inFile.Get(hPathBase))
                    hUp.Add(inFile.Get(hPathUp))
                    hDown.Add(inFile.Get(hPathDown))
        else:
            hPathBase   = "%s/%s/Base/%s"%(sample, region, hName)
            hPathUp     = "%s/%s/%sUp/%s"%(sample, region, syst, hName)
            hPathDown   = "%s/%s/%sDown/%s"%(sample, region, syst, hName)
            #print hPathBase
            #print hPathUp
            if isCheck:
                print(hPathBase)
            hBase = inFile.Get(hPathBase).Clone("Base_")
            hUp   = inFile.Get(hPathUp).Clone("%sUp_"%syst) 
            hDown = inFile.Get(hPathDown).Clone("%sDown_"%syst) 
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
            print "%s: Base:  Overflow or Undeflow is more than 1000"%syst
        if uEvtUp >1000 or oEvtUp >1000:
            print "%s: Up:  Overflow or Undeflow is more than 1000"%syst
        if uEvtDown >1000 or oEvtDown >1000:
            print "%s: Down:  Overflow or Undeflow is more than 1000"%syst
        if evtBase ==0.0:
            print "evtBase is zero"
            continue
        #check if intergal is NaN
        if math.isnan(evtUp) or math.isnan(evtDown):
            print "Inegral is nan"
            continue
        #check if bins are nan
        if checkNanInBins(hUp) or checkNanInBins(hBase) or checkNanInBins(hDown):
            print "Some of the bins are nan"
            continue
        allSystPercentage[syst] = 100*max(abs(evtUp -evtBase),abs(evtBase-evtDown))/evtBase
        print("%10s" 
               "|%6.0f %8.0f %8.0f"
               "|%6.0f %8.0f %8.0f"
               "|%6.0f %8.0f %8.0f"
               "|%5.0f%%"%(syst, 
             uEvtDown, iEvtDown, oEvtDown, 
             uEvtBase, iEvtBase, oEvtBase, 
             uEvtUp, iEvtUp, oEvtUp,
            allSystPercentage[syst]))
        if allSystPercentage[syst] > 100.0:
            print "Large uncertainty for %s: %10.2f"%(syst, allSystPercentage[syst])
        #Ratio Up
        hRatioUp = hUp.Clone(syst)
        hRatioUp.Divide(hBase)
        myColor = index
        if myColor >9:
            myColor = 32+index
        decoHistRatio(hRatioUp, hName, "RatioUp (solid), RatioDown (dashed)", myColor)
        hRatioUp.SetMarkerStyle(20+index)
        hRatioUp.SetMarkerColor(myColor)
        hRatioUp.GetXaxis().SetTitleSize(0.045)
        hRatioUp.GetXaxis().SetLabelSize(0.040)
        hRatioUp.GetYaxis().SetTitleSize(0.045)
        hRatioUp.GetYaxis().SetLabelSize(0.040)
        #hRatioUp.GetYaxis().SetRangeUser(0.1, 2)
        hRatioUp.GetYaxis().SetTitleOffset(1.5)
        hRatioUp.GetXaxis().SetTitleOffset(1.2)
        hRatioUp.SetMarkerStyle(index)
        hRatioUp.SetLineWidth(2)
        #Ratio Down
        hRatioDown = hDown.Clone(syst)
        hRatioDown.Divide(hBase)
        #decoHistRatio(hRatioDown, hName, "#frac{Up}{Nom} (solid), #frac{Down}{Nom} (dashed)", myColor)
        decoHistRatio(hRatioDown, hName, "RatioUp (solid), RatioDown (dashed)", myColor)
        hRatioDown.SetMarkerStyle(20+index)
        hRatioDown.SetMarkerColor(myColor)
        hRatioDown.SetLineStyle(2)
        hRatioDown.SetLineWidth(2)
        hRatioDown.SetMarkerStyle(index)
        allHistUp.append(hRatioUp)#Don't comment
        allHistDown.append(hRatioDown)#Don't comment

    #Draw Leg
    leg = TLegend(0.83,0.15,0.93,0.90)
    decoLegend(leg, 5, 0.034)
    #leg.SetNColumns(3)
    allHistUpSorted = sortHists(allHistUp, True)
    maxRatio = []
    for h in allHistUpSorted:
        ratio = []
        for i in range(h.GetNbinsX()):
            ratio.append(round(h.GetBinContent(i),2))
        maxRatio.append(max(ratio))
        #print h.GetName(), ratio
    yMax = max(maxRatio)
    print yMax
    for i, h in enumerate(allHistUpSorted):
        #h.GetYaxis().SetRangeUser(1-0.2*yMax, 1+0.2*yMax)
        h.GetYaxis().SetRangeUser(1-0.2, 1+0.4)
        systPercentage = int(round(allSystPercentage[h.GetName()]))
        legName = "%s%% %s"%(str(systPercentage), h.GetName().split("Weight_")[1])
        leg.AddEntry(h, legName, "L")
        if(i==0):
            h.Draw("hist")
        else:
            h.Draw("hist same")
        allHistDown[i].Draw("hist same")
    leg.Draw("same")

    lumi_13TeV = getLumiLabel(year)
    #Draw CMS, Lumi, channel
    chName = getChLabel(decay, channel)
    selName = formatCRString(region)
    if allBkgs:
        sample = "AllBkgs"
    nBase = "#font[42]{%s (N=%s)}"%(sample, str(round(evtBase,1)))
    #line1 = "Preliminary, %s, %s"%(chName, region)
    line1 = "#splitline{Preliminary, %s}{%s}"%(chName, nBase)
    line2 = selName
    line3 = region
    extraText = "#splitline{%s}{%s}"%(line1, line3)
    #extraText = "#splitline{%s}{#splitline{%s}{%s}}"%(line1, line2, line3)

    CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
    #Draw Baseline
    baseLine = TF1("baseLine","1", -100, 10000);
    baseLine.SetLineColor(1);
    baseLine.Draw("same");

    pdf = "%s/systRatio_%s_%s_%s.pdf"%(outPlotDir, sample, hName, region)
    fPath.write("%s\n"%pdf)
    canvas.SaveAs(pdf)
print(fPath)
