import os
import sys
import json
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("MVA_Ntuple/Plot_Disc", "CBA_Ntuple/Plot_Hist")) 
sys.path.insert(0, os.getcwd().replace("Plot_Disc", "Disc_Ntuple"))
from DiscInputs import Regions
from VarInfo import GetVarInfo
from optparse import OptionParser
from collections import OrderedDict
import itertools
from PlotFunc import *
from PlotInputs import *
from PlotCMSLumi import *
from PlotTDRStyle import *
from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors

rList = Regions.keys()
print(rList)
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
#dir_ = "Merged"
#dir_ = "Rebin"
dir_ = "ForMain"
os.system("mkdir -p %s"%dirPlot)
fPath = open("%s/plotDisc_%s_%s.txt"%(dirPlot, dir_, outTxt), 'w')

for decay, region, channel, year in itertools.product(Decays, rList, Channels, Years):
    hInfo = GetVarInfo(region, channel)
    hList = hInfo.keys() + ['Disc']
    if isCheck:
        hList = ["Disc"]
        pass
    for hName in hList:
        #-----------------------------------------
        #Basic flags
        #----------------------------------------
        isData   = True
        isRatio  = True
        isSig    = True
        isUnc    = True 
        isLog    = True
        print("----------------------------------------------")
        print("%s, %s, %s, %s, %s"%(decay, hName, region, channel, year))
        if "tt_" in region and ("gamma" in hName or "Pho" in hName): 
            continue 
        if ("Ele" in hName and "Mu" in channel):
            continue
        if ("Mu" in hName and "Ele" in channel):
            continue
        if "SR" in region: 
            isData  = False
            isRatio = False
            isUnc   = False
        if "lgamma" in hName:
            isLog = False
        ydc = "%s/%s/%s"%(year, decay, channel)
        inHistDir  = "%s/%s/%s/CombMass/BDTA"%(dirDisc, dir_, ydc)
        outPlotDir = "%s/%s/%s/CombMass/BDTA"%(dirPlot, dir_, ydc)
        os.system("mkdir -p %s"%outPlotDir)
        inFile = TFile("%s/AllInc.root"%(inHistDir), "read")
        if isCheck:
            print(inFile)
        
        DYJetsSF  = 1.0 
        MisIDSF   = 1.0 
        WGammaSF  = 1.0
        ZGammaSF  = 1.0
        
        gROOT.SetBatch(True)
        #-----------------------------------------
        #Make a plot for one histogram
        #----------------------------------------
        def makePlot(hName, region, isSig, isData, isLog, isRatio, isUnc):
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
            bkgHists = getHists(inFile, SampleBkg, region, "Base", hName)
            #Stack nominal hists
            xTitle = hName
            #binWidth = (hInfo[hName][1][2] - hInfo[hName][1][1])/hInfo[hName][1][0]
            #yTitle = "Events/%s"%str(binWidth)
            yTitle = "Events"
            hStack = THStack(hName,hName)
            hForStack = sortHists(bkgHists, False)
            lumi_13TeV = getLumiLabel(year)
            yDict = {}
            sList = []
            if isData:
                sList.append("Data")
            for h in hForStack: 
                sampleName = h.GetName().split("_")[0]
                decoHist(h, xTitle, yTitle, SampleBkg[sampleName][0])
                hStack.Add(h)
                yDict[sampleName] = getYield(h)
            hStack.Draw("HIST")
            
            #Data hists
            if isData:
                dataHist = getHist(inFile, "data_obs", region, "Base", hName)
                decoHist(dataHist, xTitle, yTitle, SampleData["Data"][0])
                dataHist.SetMarkerStyle(20)
                dataHist.Draw("EPsame")
            
            #Signal hists
            if isSig:
                sigHists  = getHists(inFile, SampleSignal, region, "Base", hName)
                sortedSigHists = sortHists(sigHists, True)
                for hSig in sigHists:
                    hSig.Draw("HISTsame")
            
            # Unc band
            if isUnc:
                hSumBkgs, hUncUp, hUncDown = getHistSyst(inFile, SampleBkg, region, Systematics, hName)
                print("Nom, uncUp, uncDown:", hSumBkgs.Integral(), hUncUp.Integral(), hUncDown.Integral())
                uncGraphTop  = getUncBand(hSumBkgs, hUncUp, hUncDown, False)
                uncGraphTop.SetFillColor(2);
                uncGraphTop.SetFillStyle(3001);
                uncGraphTop.Draw(" E2 same ");
        
            #Draw plotLegend
            hForLegend = sortHists(bkgHists, True)
            #plotLegend = TLegend(0.55,0.60,0.92,0.88); for 3 col
            plotLegend = TLegend(0.75,0.40,0.95,0.88); 
            decoLegend(plotLegend, 4, 0.035)
            hSumAllBkg = bkgHists[0].Clone("AllBkg")
            hSumAllBkg.Reset()
            if isData:
                plotLegend.AddEntry(dataHist, SampleData["Data"][1], "PEL")
                yDict["Data"] = getYield(dataHist) 
            for bkgHist in hForLegend:
                hSumAllBkg.Add(bkgHist)
            for bkgHist in hForLegend:
                nBkg = str(round(100*bkgHist.Integral()/hSumAllBkg.Integral(), 1))
                plotLegendName = SampleBkg[bkgHist.GetName().split("_")[0]][1] 
                plotLegend.AddEntry(bkgHist, "%s%s %s"%(nBkg, "%", plotLegendName), "F")
                sList.append(bkgHist.GetName().split("_")[0])
            sList.append("Bkgs")
            if isSig:
                for hSig in sortedSigHists:
                    s0 = hSig.GetName().split("_")[0]
                    s1 = hSig.GetName().split("_")[1]
                    sName = "%s_%s"%(s0, s1)
                    yDict[sName] = getYield(hSig) 
                    sList.append(sName)
                    plotLegendName = SampleSignal[sName][1] 
                    decoHistSig(hSig, xTitle, yTitle, SampleSignal[sName][0])
                    plotLegend.AddEntry(hSig, plotLegendName, "PL")
            if isUnc:
                #plotLegend.AddEntry(uncGraphTop, "#splitline{Pre-fit unc.}{(Bkg. stat. #oplus sys.)}","F") 
                plotLegend.AddEntry(uncGraphTop, "Bkg. stat. #oplus sys.","F") 
            plotLegend.Draw()
            hStack.SetMinimum(0.1)
            yDict["Bkgs"] = getYield(hSumAllBkg)
            if isLog and hSumAllBkg.Integral() !=0:
                gPad.SetLogy(True)
                if isData:
                    hStack.SetMaximum(500*dataHist.GetMaximum())
                else:
                    hStack.SetMaximum(500*hStack.GetMaximum())
            else: 
                if isData:
                    hStack.SetMaximum(1.5*dataHist.GetMaximum())
                else:
                    hStack.SetMaximum(1.3*hStack.GetMaximum())
            hStack.GetXaxis().SetTitle(xTitle)
            hStack.GetYaxis().SetTitle(yTitle)
        
            #Draw CMS, Lumi, channel
            chName = getChLabel(decay, channel)
            chName = "%s, #bf{%s}"%(chName, region)
            crName = formatCRString(Regions[region])
            #crName = "#splitline{(%s)}{#color[4]{DYSF=%s, MisIDSF=%s, ZGSF=%s, WGSF=%s}}"%(crName, round(DYJetsSF,2), round(MisIDSF, 2), round(ZGammaSF, 2), round(WGammaSF,2))
            chCRName = "#splitline{#font[42]{%s}}{#font[42]{(%s)}}"%(chName, crName)
            extraText   = "#splitline{Preliminary}{%s}"%chCRName
            if isData and isRatio:
                nData  = str(int(dataHist.Integral()))
                nRatio = str(round(dataHist.Integral()/hSumAllBkg.Integral(),2))
                extraText   = "#splitline{Preliminary, Data = %s, Ratio = %s}{%s}"%(nData, nRatio, chCRName)
            else:
                nBkg  = str(round(hSumAllBkg.Integral(), 2))
                extraText   = "#splitline{Preliminary, Bkgs = %s}{%s}"%(nBkg, chCRName)
            #CMS_lumi(canvas, iPeriod, iPosX, extraText)
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
                hRatio = dataHist.Clone("hRatio")
                hRatio.Divide(hSumAllBkg)
                decoHistRatio(hRatio, xTitle, "Data/Bkgs", 1)
                sList.append("Data/Bkgs")
                yDict["Data/Bkgs"] = ["---", round(dataHist.Integral()/hSumAllBkg.Integral(),2), " --- (---)"]
                hRatio.Draw()
                if isUnc:
                    uncGraphRatio  = getUncBand(hSumBkgs, hUncUp, hUncDown, True)
                    uncGraphRatio.SetFillColor(2);
                    uncGraphRatio.SetFillStyle(3001);
                    uncGraphRatio.Draw("E2same");
                baseLine = TF1("baseLine","1", -100, 10000);
                baseLine.SetLineColor(3);
                baseLine.Draw("SAME");
                hRatio.Draw("same")
            pdf = "%s/plotDisc_%s_%s_%s.pdf"%(outPlotDir, dir_, hName, region)
            canvas.SaveAs(pdf)
            fPath.write("%s\n"%pdf)
            cap = "%s, %s, %s, %s"%(year, channel, region, hName)
            tHead = "Process & Entry & Yield & Stat (Syst)\\%\\\\\n" 
            table = createTable(Samples, yDict, sList, 4, tHead, cap.replace("_", "\\_"))
            tableFile = open(pdf.replace(".pdf", ".tex"), "w")
            print table
            tableFile.write(table)
        makePlot(hName, region, isSig,  isData, isLog, isRatio, isUnc)
print(fPath)
