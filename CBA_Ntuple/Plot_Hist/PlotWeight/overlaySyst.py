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

rList = list(Regions.keys())
print(rList)
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

if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
    rList  = [rList[0]]
    Systematics   = [Systematics[0]]
    SampleSyst = [SampleSyst[0]]
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
fPath = open("%s/overlaySyst_%s_%s.txt"%(dirPlot, dir_, outTxt), 'w')

for decay, region, channel, year, samp, syst in itertools.product(Decays, rList, Channels, Years, SampleSyst, Systematics):
    hInfo = GetVarInfo(region, channel)
    hList = list(hInfo.keys()) + ['Disc']
    hList = ["Disc"]
    if isCheck:
        hList = ["Disc"]
        pass
    for hName in hList:
        #-----------------------------------------
        #Basic flags
        #----------------------------------------
        isData   = True
        isRatio  = True
        print("----------------------------------------------")
        print("%s, %s, %s, %s, %s"%(decay, hName, region, channel, year))
        if "tt_" in region and ("gamma" in hName or "Pho" in hName): 
            continue 
        if ("Ele" in hName and "Mu" in channel):
            continue
        if ("Mu" in hName and "Ele" in channel):
            continue
        if "CR" in region: 
            continue
        if "lgamma" in hName:
            isLog = False
        ydc = "%s/%s/%s"%(year, decay, channel)
        inHistDir  = "%s/%s/%s/CombMass/BDTA"%(dirDisc, dir_, ydc)
        outPlotDir = "%s/%s/%s/CombMass/BDTA"%(dirPlot, dir_, ydc)
        os.system("mkdir -p %s"%outPlotDir)
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
            hPathBase   = "%s/%s/Base/%s"%(sample, region, hName)
            hPathUp     = "%s/%s/%sUp/%s"%(sample, region, syst, hName)
            hPathDown   = "%s/%s/%sDown/%s"%(sample, region, syst, hName)
            #print(hPathBase)
            #print(hPathUp)
            if isCheck:
                print(hPathBase)
            hBase = inFile.Get(hPathBase).Clone("Base_")
            hUp   = inFile.Get(hPathUp).Clone("%sUp_"%syst) 
            hDown = inFile.Get(hPathDown).Clone("%sDown_"%syst) 
            xTitle = hName
            yTitle = "Events"
            #decoHist(hBase, xTitle, yTitle, myGreen)
            #decoHist(hUp, xTitle, yTitle, myRed)
            #decoHist(hDown, xTitle, yTitle, myBlue)
            hBase.SetLineColor(myCyan)
            hUp.SetLineColor(myRed)
            hDown.SetLineColor(myBlue)

            hBase.Draw("HIST")
            hUp.Draw("hist same")
            hDown.Draw("hist same")
            lumi_13TeV = getLumiLabel(year)

            plotLegend = TLegend(0.75,0.40,0.95,0.88); 
            decoLegend(plotLegend, 4, 0.035)
            plotLegend.AddEntry(hBase, "nominal", "PEL")
            plotLegend.AddEntry(hUp, "%s_up"%syst, "PEL")
            plotLegend.AddEntry(hDown, "%s_down"%syst, "PEL")
            plotLegend.Draw()
            hBase.SetMaximum(1.3*hBase.GetMaximum())
            hBase.GetXaxis().SetTitle(xTitle)
            hBase.GetYaxis().SetTitle(yTitle)
        
            #Draw CMS, Lumi, channel
            chName = getChLabel(decay, channel)
            chName = "%s, #bf{%s}"%(chName, region)
            crName = formatCRString(Regions[region])
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
                hRatioUp = hUp.Clone("hRatioUp")
                hRatioUp.Divide(hBase)
                decoHistRatio(hRatioUp, xTitle, "Ratio", myRed)
                hRatioUp.GetYaxis().SetRangeUser(0.9, 1.1)
                hRatioUp.Draw("HIST")

                hRatioDown = hDown.Clone("hRatioDown")
                hRatioDown.Divide(hBase)
                decoHistRatio(hRatioDown, xTitle, "Ratio", myBlue)
                hRatioDown.Draw("hist same")

                baseLine = TF1("baseLine","1", -100, 10000);
                baseLine.SetLineColor(3);
                baseLine.Draw("SAME");
            pdf = "%s/overlaySyst_%s_%s_%s_%s_%s.pdf"%(outPlotDir, dir_, hName, region, sample, syst)
            canvas.SaveAs(pdf)
            fPath.write("%s\n"%pdf)
        makePlot(hName, region, samp, syst)
print(fPath)
