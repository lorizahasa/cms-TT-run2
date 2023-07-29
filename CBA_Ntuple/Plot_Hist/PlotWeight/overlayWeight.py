import os
import sys
import json
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("PlotWeight", "")) 
sys.path.insert(0, os.getcwd().replace("Plot_Hist/PlotWeight", "Hist_Ntuple/HistWeight")) 
import itertools
from HistInputs import Corrs
from PlotFunc import *
from PlotInputs import *
from PlotCMSLumi import *
from PlotTDRStyle import *
from optparse import OptionParser
from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors

padGap = 0.01
iPeriod = 4;
iPosX = 10;
ModTDRStyle()
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
Samples  = list(sampMC.keys())
systKeys = list(Corrs.keys()) 
if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
    Samples = [Samples[0]]
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

for channel, decay, samp, systKey, year in itertools.product(Channels, Decays, Samples, systKeys, Years):
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
        print("----------------------------------------------")
        print("%s, %s, %s, %s, %s, %s, %s"%(year, decay, channel, samp, region, systs, hName))
        print("----------------------------------------------")
        if "tt_" in region and ("gamma" in hName or "Pho" in hName): 
            continue 
        if ("ele" in systKey and "Mu" in channel):
            continue
        if ("mu" in systKey and "Ele" in channel):
            continue
        if "CR" in region: 
            continue
        if "lgamma" in hName:
            isLog = False
        ydc = "%s/%s/%s"%(year, decay, channel)
        inHistDir  = "%s/%s"%(dirHist, ydc)
        outPlotDir = "%s/%s/%s"%(dirPlot, ydc, region)
        if not os.path.exists(outPlotDir):
            os.makedirs(outPlotDir)
        inFile = TFile("%s/AllInc.root"%(inHistDir), "read")
        if isCheck:
            print(inFile)
        
        gROOT.SetBatch(True)
        #-----------------------------------------
        #Make a plot for one histogram
        #----------------------------------------
        def makePlot(hName, region, sample, systs):
            '''
            We first draw stacked histograms then data then unc band.
            The ratio of data and background is drawn next in a separate
            pad.
            '''
            canvas = TCanvas()
            if isData and isRatio:
                canvas.Divide(1, 2)
                canvas.cd(1)
                gPad.SetRightMargin(0.03);
                gPad.SetPad(xPadRange[0],yPadRange[2],xPadRange[1],yPadRange[3]);
                gPad.SetTopMargin(0.09);
                gPad.SetBottomMargin(padGap);
                #gPad.SetTickx(0);
                gPad.RedrawAxis();
            else:
                canvas.cd()
            #Get nominal histograms
            hPathUncorr = "%s/%s/%s/%s"%(sample, region, systs[0], hName)
            hPathCorr   = "%s/%s/%s/%s"%(sample, region, systs[1], hName)
            hPathUp     = "%s/%s/%s/%s"%(sample, region, systs[2], hName)
            hPathDown   = "%s/%s/%s/%s"%(sample, region, systs[3], hName)
            #print(hPathCorr)
            #print(hPathUp)
            if isCheck:
                print(hPathCorr)
            hUncorr = inFile.Get(hPathUncorr).Clone("Uncorr")
            hCorr = inFile.Get(hPathCorr).Clone("Corr")
            hUp   = inFile.Get(hPathUp).Clone("CorrUp") 
            hDown = inFile.Get(hPathDown).Clone("CorrDown")

            evtUncorr = hUncorr.Integral()
            evtCorr = hCorr.Integral()
            evtUp   = hUp.Integral()
            evtDown = hDown.Integral()
            rCorr   = round(evtCorr/evtUncorr, 3)
            rUp     = round(evtUp/evtUncorr , 3)
            rDown   = round(evtDown/evtUncorr, 3)
            rMax = min(rCorr, rUp, rDown)
            print("evtUncorr = %s, rCorr = %s, rUp = %s, rDown = %s"%(evtUncorr, rCorr, rUp, rDown))

            xTitle = hName
            yTitle = "Events"
            decoHistSyst(hUncorr, xTitle, yTitle, colUncorr) 
            decoHistSyst(hCorr, xTitle, yTitle, colCorr) 
            decoHistSyst(hUp, xTitle, yTitle, colUp) 
            decoHistSyst(hDown, xTitle, yTitle, colDown) 

            hUncorr.Draw("HIST")
            hCorr.Draw("hist same")
            hUp.Draw("hist same")
            hDown.Draw("hist same")
            lumi_13TeV = getLumiLabel(year)

            plotLegend = TLegend(0.57,0.60,0.95,0.88); 
            decoLegend(plotLegend, 1, 0.04)
            plotLegend.AddEntry(hUncorr, "%s"%systs[0], "L")
            plotLegend.AddEntry(hUp,    "%s(%s)"%(systs[1], rUp), "L")
            plotLegend.AddEntry(hCorr,  "%s(%s)"%(systs[2], rCorr), "L")
            plotLegend.AddEntry(hDown,  "%s(%s)"%(systs[3], rDown), "L")
            plotLegend.Draw()
            hUncorr.SetMaximum(1.6*hUp.GetMaximum())
            hUncorr.GetXaxis().SetTitle(xTitle)
            hUncorr.GetYaxis().SetTitle(yTitle)
        
            #Draw CMS, Lumi, channel
            chName = getChLabel(decay, channel)
            #chName = "%s, #bf{%s}"%(chName, region)
            crName = formatCRString(region)
            chCRName = "#splitline{#font[42]{%s}}{#font[42]{(%s)}}"%(chName, crName)
            extraText   = "#splitline{Preliminary}{%s}"%chCRName
            CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
        
            #Draw the ratio of data and all background
            #Divide canvas for the ratio plot
            if isData and isRatio:
                canvas.cd(2)
                gPad.SetTopMargin(padGap); 
                gPad.SetBottomMargin(0.30); 
                gPad.SetRightMargin(0.03);
                #gPad.SetTickx(0);
                gPad.SetPad(xPadRange[0],yPadRange[0],xPadRange[1],yPadRange[2]);
                gPad.RedrawAxis();
                hRatio = hCorr.Clone("hRatio")
                hRatio.Divide(hUncorr)
                decoHistRatio(hRatio, xTitle, "Corr./Uncorr.", colCorr)

                hRatioUp = hUp.Clone("hRatioUp")
                hRatioUp.Divide(hUncorr)
                decoHistRatio(hRatioUp, xTitle, "Corr./Uncorr.", colUp)

                hRatioDown = hDown.Clone("hRatioDown")
                hRatioDown.Divide(hUncorr)
                decoHistRatio(hRatioDown, xTitle, "Corr./Uncorr.", colDown)

                rRange = 1.2*abs(rMax -1)
                hRatio.GetYaxis().SetRangeUser(1-rRange, 1+rRange)
                #hRatio.GetYaxis().SetRangeUser(0.9, 1.1)

                hRatio.Draw("HIST")
                hRatioUp.Draw("hist same")
                hRatioDown.Draw("hist same")

                baseLine = TF1("baseLine","1", -100, 10000);
                baseLine.SetLineColor(colUncorr);
                baseLine.Draw("SAME");
            pdf = "%s/overlaySyst_%s_%s_%s.pdf"%(outPlotDir, hName, sample, systKey)
            canvas.SaveAs(pdf)
            fPath.write("%s\n"%pdf)
        makePlot(hName, region, samp, systs)
print(fPath)
