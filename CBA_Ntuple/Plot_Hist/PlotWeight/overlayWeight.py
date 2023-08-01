import os
import sys
import json
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("PlotWeight", "")) 
sys.path.insert(0, os.getcwd().replace("Plot_Hist/PlotWeight", "Hist_Ntuple/HistWeight")) 
import itertools
from HistInputs import Corrs, Regions
from PlotFunc import *
from PlotInputs import *
from PlotCMSLumi import *
from PlotTDRStyle import *
from optparse import OptionParser
from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors

padGap = 0.0#0.01
iPeriod = 4;
iPosX = 10;
ModTDRStyle()
xPadRange  = [0.0,1.0]
rW = 0.25
yPadRange1 = [2*rW+padGap,1.0]
yPadRange2 = [rW+padGap,2*rW]
yPadRange3 = [0.0,rW]

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
systKeys = list(Corrs.keys()) 
if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
    #systKeys = ["JEC_FlavorQCD"]
    systKeys = [systKeys[1]]
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

#-----------------------------------------
#Path of the I/O histrograms/plots
#----------------------------------------
os.system("mkdir -p %s"%dirPlot)
fPath = open("%s/overlayWeight.txt"%dirPlot, 'w')

for channel, decay, systKey, year in itertools.product(Channels, Decays, systKeys, Years):
    systs  = Corrs[systKey]
    if len(systs) < 2 : continue
    print(systs)
    hList = ["Reco_st"]
    for hName in hList:
        #-----------------------------------------
        #Basic flags
        #----------------------------------------
        isData   = True
        isRatio  = True
        isLog    = True
        print("----------------------------------------------")
        print("%s, %s, %s, %s, %s, %s"%(year, decay, channel, region, systs, hName))
        print("----------------------------------------------")
        if "tt_" in region and ("gamma" in hName or "Pho" in hName): 
            continue 
        if ("ele" in systKey and "Mu" in channel):
            continue
        if ("mu" in systKey and "Ele" in channel):
            continue
        if "CR" in region: 
            continue
        ydc = "%s/%s/%s"%(year, decay, channel)
        inHistDir  = "%s/%s"%(dirHist, ydc)
        outPlotDir = "%s/%s/%s"%(dirPlot, ydc, region)
        if not os.path.exists(outPlotDir):
            os.makedirs(outPlotDir)
        inFile = TFile("%s/AllInc.root"%(inHistDir), "read")
        if isCheck:
            print(inFile)
        
        gROOT.SetBatch(True)
        
        for i, samp in enumerate(sampBkg.keys()):
            hPathUncorr = "%s/%s/%s/%s"%(samp, region, systs[0], hName)
            hPathCorr   = "%s/%s/%s/%s"%(samp, region, systs[1], hName)
            hPathUp     = "%s/%s/%s/%s"%(samp, region, systs[2], hName)
            hPathDown   = "%s/%s/%s/%s"%(samp, region, systs[3], hName)
            hUncorr_  = inFile.Get(hPathUncorr)
            hCorr_    = inFile.Get(hPathCorr)
            hUp_      = inFile.Get(hPathUp)
            hDown_    = inFile.Get(hPathDown)
            if i==0:
                systUnc = getSystUnc(hUp_, hCorr_, hDown_, samp, True) 
                hUncorr = hUncorr_.Clone("Bkgs_Uncorr")
                hCorr   = hCorr_.Clone("Bkgs_Corr")
                hUp     = hUp_.Clone("Bkgs_CorrUp") 
                hDown   = hDown_.Clone("Bkgs_CorrDown")
            else:
                systUnc = getSystUnc(hUp_, hCorr_, hDown_, samp)
                hUncorr . Add(hUncorr_)
                hCorr   . Add(hCorr_)
                hUp     . Add(hUp_)
                hDown   . Add(hDown_)

        #-----------------------------------------
        #Make a plot for one histogram
        #----------------------------------------
        def makePlot(hName, region, systs):
            '''
            We first draw stacked histograms then data then unc band.
            The ratio of data and background is drawn next in a separate
            pad.
            '''
            canvas = TCanvas("Canvas", "Canvas", 600, 750)
            if isData and isRatio:
                canvas.Divide(1, 3)
                canvas.cd(1)
                gPad.SetRightMargin(0.03);
                gPad.SetPad(xPadRange[0],yPadRange1[0],xPadRange[1],yPadRange1[1]);
                gPad.SetTopMargin(0.11);
                gPad.SetBottomMargin(padGap);
                #gPad.SetTickx(0);
                if isLog:
                    gPad.SetLogy(True)
                gPad.RedrawAxis();
            else:
                canvas.cd()
            #Get nominal histograms
            hPathData   = "%s/%s/%s/%s"%("data_obs", region, systs[0], hName)
            hData = inFile.Get(hPathData).Clone("Uncorr")
            evtData = hData.Integral()
            evtUncorr = hUncorr.Integral()
            evtCorr = hCorr.Integral()
            evtUp   = hUp.Integral()
            evtDown = hDown.Integral()
            rData   = round(evtData/evtUncorr, 3)
            rCorr   = round(evtCorr/evtUncorr, 3)
            rUp     = round(evtUp/evtUncorr , 3)
            rDown   = round(evtDown/evtUncorr, 3)
            print("evtUncorr = %s, rCorr = %s, rUp = %s, rDown = %s"%(evtUncorr, rCorr, rUp, rDown))

            xTitle = hName
            yTitle = "Events"
            decoHistSyst(hData, xTitle, yTitle, colData) 
            hData.SetMarkerStyle(20)
            decoHistSyst(hUncorr, xTitle, yTitle, colUncorr) 
            decoHistSyst(hCorr, xTitle, yTitle, colCorr) 
            decoHistSyst(hUp, xTitle, yTitle, colUp) 
            decoHistSyst(hDown, xTitle, yTitle, colDown) 

            hUncorr.Draw("HIST")
            hCorr.Draw("hist same")
            hUp.Draw("hist same")
            hDown.Draw("hist same")
            hData.Draw("EPsame")
            lumi_13TeV = getLumiLabel(year)

            plotLegend = TLegend(0.45,0.60,0.90,0.88); 
            decoLegend(plotLegend, 1, 0.045)
            plotLegend.AddEntry(hData, "Data", "PEL")
            plotLegend.AddEntry(hUncorr,"Bkgs_Uncorr", "L")
            plotLegend.AddEntry(hUp,    "Bkgs_%s(%s)"%(systs[2], rUp), "L")
            plotLegend.AddEntry(hCorr,  "Bkgs_%s(%s)"%(systs[1], rCorr), "L")
            plotLegend.AddEntry(hDown,  "Bkgs_%s(%s)"%(systs[3], rDown), "L")
            plotLegend.Draw()
            hUncorr.SetMaximum(1.6*hData.GetMaximum())
            if isLog:
                hUncorr.SetMaximum(20*hData.GetMaximum())
            hUncorr.GetXaxis().SetTitle(xTitle)
            hUncorr.GetYaxis().SetTitle(yTitle)
        
            #Draw CMS, Lumi, channel
            chName = getChLabel(decay, channel)
            #chName = "%s, #bf{%s}"%(chName, region)
            crName = formatCRString(Regions[region])
            chCRName = "#splitline{#font[42]{%s}}{#font[42]{(%s)}}"%(chName, crName)
            extraText   = "#splitline{Preliminary}{%s}"%chCRName
            CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
        
            #Draw the ratio of data and all background
            #Divide canvas for the ratio plot
            if isData and isRatio:
                canvas.cd(2)
                gPad.SetTopMargin(padGap); 
                gPad.SetBottomMargin(padGap); 
                gPad.SetRightMargin(0.03);
                #gPad.SetTickx(0);
                gPad.SetPad(xPadRange[0],yPadRange2[0],xPadRange[1],yPadRange2[1]);
                gPad.RedrawAxis();

                hRatioUncorr = hData.Clone("hRatioUnCorr")
                hRatioUncorr.Divide(hUncorr)
                rLabel = "#frac{Data}{Bkgs}"
                print(rData)
                decoHistRatio(hRatioUncorr, xTitle, rLabel, colUncorr)
                hRatioUncorr.GetYaxis().SetRangeUser(0.6, 1.4)

                hRatioCorr = hData.Clone("hRatioCorr")
                hRatioCorr.Divide(hCorr)
                decoHistRatio(hRatioCorr, xTitle, rLabel, colCorr)

                hRatioUp = hData.Clone("hRatioUp")
                hRatioUp.Divide(hUp)
                decoHistRatio(hRatioUp, xTitle, rLabel, colUp)

                hRatioDown = hData.Clone("hRatioDown")
                hRatioDown.Divide(hDown)
                decoHistRatio(hRatioDown, xTitle, rLabel, colDown)

                hRatioUncorr.Draw("HIST")
                hRatioCorr.Draw("hist same")
                hRatioUp.Draw("hist same")
                hRatioDown.Draw("hist same")

                #The ratio of Bkgs Corr/Uncorr
                rLabel = "#frac{Bkgs Corr.}{Bkgs Uncorr.}"
                canvas.cd(3)
                gPad.SetTopMargin(padGap); 
                gPad.SetBottomMargin(0.25); 
                gPad.SetRightMargin(0.03);
                gPad.SetPad(xPadRange[0],yPadRange3[0],xPadRange[1],yPadRange3[1]);
                gPad.RedrawAxis();

                hRatioCorr2 = hCorr.Clone("hRatioCorr2")
                hRatioCorr2.Divide(hUncorr)
                decoHistRatio(hRatioCorr2, xTitle, rLabel, colCorr)

                hRatioUp2 = hUp.Clone("hRatioUp2")
                hRatioUp2.Divide(hUncorr)
                decoHistRatio(hRatioUp2, xTitle, rLabel, colUp)

                hRatioDown2 = hDown.Clone("hRatioDown2")
                hRatioDown2.Divide(hUncorr)
                decoHistRatio(hRatioDown2, xTitle, rLabel, colDown)

                binCons = getContent(hRatioCorr2) + getContent(hRatioUp2) + getContent(hRatioDown2) 
                yMin = min(binCons)
                yMax = max(binCons)
                hRatioCorr2.GetYaxis().SetRangeUser(yMin*(1-1/100),yMax*(1+1/100))# -+2%
                hRatioCorr2.Draw("HIST")
                hRatioUp2.Draw("hist same")
                hRatioDown2.Draw("hist same")

                baseLine = TF1("baseLine","1", -100, 10000);
                baseLine.SetLineColor(colData);
                #baseLine.Draw("SAME");
            pdf = "%s/overlaySyst_%s_%s.pdf"%(outPlotDir, hName, systKey)
            canvas.SaveAs(pdf)
            fPath.write("%s\n"%pdf)
        makePlot(hName, region, systs)
print(fPath)
