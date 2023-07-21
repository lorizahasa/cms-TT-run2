import os
import sys
import json
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("PlotWeight", "")) 
import itertools
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
Samples = list(sampMC.keys())
systList = []
for key in systDict.keys():
    for syst in systDict[key]:
        systList.append(syst)
if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
    Samples = [Samples[0]]
    systList = [systList[0]]
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

for channel, decay, samp, syst, year in itertools.product(Channels, Decays, Samples, systList, Years):
    hList = ["Reco_st"]
    for hName in hList:
        #-----------------------------------------
        #Basic flags
        #----------------------------------------
        isData   = True
        isRatio  = True
        print("----------------------------------------------")
        print("%s, %s, %s, %s, %s, %s, %s"%(year, decay, channel, samp, region, syst, hName))
        print("----------------------------------------------")
        if "tt_" in region and ("gamma" in hName or "Pho" in hName): 
            continue 
        if ("ele" in syst and "Mu" in channel):
            continue
        if ("mu" in hName and "Ele" in channel):
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
        def makePlot(hName, region, sample, syst):
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
            hPathNoSF   = "%s/%s/1Base/%s"%(sample, region, hName)
            hPathBase   = "%s/%s/%sBase/%s"%(sample, region, syst, hName)
            hPathUp     = "%s/%s/%sUp/%s"%(sample, region, syst, hName)
            hPathDown   = "%s/%s/%sDown/%s"%(sample, region, syst, hName)
            #print(hPathBase)
            #print(hPathUp)
            if isCheck:
                print(hPathBase)
            hNoSF = inFile.Get(hPathNoSF).Clone("NoSF_")
            hBase = inFile.Get(hPathBase).Clone("Base_")
            hUp   = inFile.Get(hPathUp).Clone("%sUp_"%syst) 
            hDown = inFile.Get(hPathDown).Clone("%sDown_"%syst) 

            evtNoSF = hNoSF.Integral()
            evtBase = hBase.Integral()
            evtUp   = hUp.Integral()
            evtDown = hDown.Integral()
            rBase   = round(evtBase/evtNoSF, 3)
            rUp     = round(evtUp/evtNoSF , 3)
            rDown   = round(evtDown/evtNoSF, 3)
            rMax = min(rBase, rUp, rDown)
            print("evtNoSF = %s, rBase = %s, rUp = %s, rDown = %s"%(evtNoSF, rBase, rUp, rDown))

            xTitle = hName
            yTitle = "Events"
            decoHistSyst(hNoSF, xTitle, yTitle, colNoSF) 
            decoHistSyst(hBase, xTitle, yTitle, colBase) 
            decoHistSyst(hUp, xTitle, yTitle, colUp) 
            decoHistSyst(hDown, xTitle, yTitle, colDown) 

            hNoSF.Draw("HIST")
            hBase.Draw("hist same")
            hUp.Draw("hist same")
            hDown.Draw("hist same")
            lumi_13TeV = getLumiLabel(year)

            plotLegend = TLegend(0.57,0.60,0.95,0.88); 
            decoLegend(plotLegend, 1, 0.04)
            plotLegend.AddEntry(hNoSF, "Uncorrected", "L")
            sLabel = syst.replace("Weight", "Corr")
            plotLegend.AddEntry(hUp, "%s_up (%s)"%(sLabel, rUp), "L")
            plotLegend.AddEntry(hBase, "%s (%s)"%(sLabel, rBase), "L")
            plotLegend.AddEntry(hDown, "%s_down (%s)"%(sLabel, rDown), "L")
            plotLegend.Draw()
            hNoSF.SetMaximum(1.5*hUp.GetMaximum())
            hNoSF.GetXaxis().SetTitle(xTitle)
            hNoSF.GetYaxis().SetTitle(yTitle)
        
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
                hRatio = hBase.Clone("hRatio")
                hRatio.Divide(hNoSF)
                decoHistRatio(hRatio, xTitle, "Corr./Uncorr.", colBase)

                hRatioUp = hUp.Clone("hRatioUp")
                hRatioUp.Divide(hNoSF)
                decoHistRatio(hRatioUp, xTitle, "Corr./Uncorr.", colUp)

                hRatioDown = hDown.Clone("hRatioDown")
                hRatioDown.Divide(hNoSF)
                decoHistRatio(hRatioDown, xTitle, "Corr./Uncorr.", colDown)

                rRange = 1.2*abs(rMax -1)
                hRatio.GetYaxis().SetRangeUser(1-rRange, 1+rRange)
                #hRatio.GetYaxis().SetRangeUser(0.9, 1.1)

                hRatio.Draw("HIST")
                hRatioUp.Draw("hist same")
                hRatioDown.Draw("hist same")

                baseLine = TF1("baseLine","1", -100, 10000);
                baseLine.SetLineColor(colNoSF);
                baseLine.Draw("SAME");
            pdf = "%s/overlaySyst_%s_%s_%s_%s.pdf"%(outPlotDir, hName, region, sample, syst)
            canvas.SaveAs(pdf)
            fPath.write("%s\n"%pdf)
        makePlot(hName, region, samp, syst)
print(fPath)
