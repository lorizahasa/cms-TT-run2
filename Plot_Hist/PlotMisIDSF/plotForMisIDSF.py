from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors
import os
import sys
sys.path.insert(0, os.getcwd().replace("Plot_Hist/PlotMisIDSF", "Hist_Ntuple/HistMisIDSF"))
sys.path.insert(0, os.getcwd().replace("PlotMisIDSF", ""))
from HistInputs import Regions
from HistInfo import GetHistogramInfo
from optparse import OptionParser
from collections import OrderedDict
from PlotFunc import *
from PlotInputs import *
from PlotCMSLumi import *
from PlotTDRStyle import *

hInfo = GetHistogramInfo()
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
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decayMode", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decayMode moded of ttbar Semilep or DiLep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Ele",type='str',
		  help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-r", "--region", dest="region", default="MisID_Enriched_e3j_e0b_e1y",type='str', 
                     help="which control selection and region"), 
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_lgamma",type='str', 
                     help="which histogram to be plottted")
(options, args) = parser.parse_args()
year            = options.year
decayMode       = options.decayMode
channel         = options.channel
region = options.region
hName           = options.hName
stage = "forMisIDSF"
#-----------------------------------------
#Path of the I/O histrograms/plots
#----------------------------------------
inHistSubDir = "/Hist_Ntuple/HistMisIDSF/%s/%s/%s/%s/Merged"%(stage, year, decayMode, channel)
inHistFullDir = "%s/%s"%(condorHistDir, inHistSubDir)
inFile = TFile("%s/AllInc.root"%(inHistFullDir), "read")
outPlotSubDir = "Plot_Hist/PlotMisIDSF/%s/%s/%s/%s/%s"%(stage, year, decayMode, channel, region)
outPlotFullDir = "%s/%s"%(condorHistDir, outPlotSubDir)
if not os.path.exists(outPlotFullDir):
    os.makedirs(outPlotFullDir)
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
    bkgHists = getBkgBaseHists(inFile, hName, region)
    #Stack nominal hists
    xTitle = hName
    binWidth = (hInfo[hName][1][2] - hInfo[hName][1][1])/hInfo[hName][1][0]
    #yTitle = "Events/%s"%str(binWidth)
    yTitle = "Events/%s"%str(2)
    hStack = THStack(hName,hName)
    hForStack = sortHists(bkgHists, False)
    lumi_13TeV = "35.9 fb^{-1}"
    col_depth = 0
    col_year = SampleBkg["MisIDEle"][0]
    if "16" in year:
        col_depth = -2
        lumi_13TeV = "35.9 fb^{-1} (#color[%i]{2016})"%(col_year+col_depth)
    if "17" in year:
        col_depth = -1
        lumi_13TeV = "41.5 fb^{-1} (#color[%i]{2017})"%(col_year + col_depth)
    if "18" in year:
        col_depth = 0
        lumi_13TeV = "59.7 fb^{-1} (#color[%i]{2018})"%(col_year + col_depth)
    if "Run2" in year:
        col_depth = 1
        lumi_13TeV = "137.2 fb^{-1} (#color[%i]{Run2})"%(col_year + col_depth)
    yDict = {}
    sList = []
    if isData:
        sList.append("Data")
    for h in hForStack: 
        sampleName = h.GetName().split("_")[0]
        decoHist(h, xTitle, yTitle, SampleBkg[sampleName][0]+col_depth)
        hStack.Add(h)
        yDict[sampleName] = getYield(h)
    hStack.Draw("HIST")
    
    #Data hists
    if isData:
        dataHist = getDataHists(inFile, hName, region)
        decoHist(dataHist[0], xTitle, yTitle, SampleData["Data"][0])
        dataHist[0].SetMarkerStyle(20)
        dataHist[0].Draw("EPsame")
    
    #Signal hists
    if isSig:
        sigHists  = getSigBaseHists(inFile, hName, region)
        sortedSigHists = sortHists(sigHists, True)
        for hSig in sigHists:
            hSig.Draw("HISTsame")
    
    # Unc band
    if isUnc:
        hSumBkgUps =  getSystHists(inFile, hName, region, "Up")
        hSumBkgDowns = getSystHists(inFile, hName, region, "Down")
        hDiffUp = hSumBkg.Clone("hDiffUp")
        hDiffUp.Reset()
        hDiffDown = hSumBkg.Clone("hDiffDown")
        hDiffDown.Reset()
        for hUp in hSumBkgUps:
            hDiff = hUp.Clone("hDiff")
            hDiff.Add(hSumBkg, -1)    
            hDiffUp.Add(hDiff)
            print "hDiffUp = ", hDiffUp.Integral()
        for hDown in hSumBkgDowns:
            hDiff = hSumBkg.Clone("hDiff")
            hDiff.Add(hDown, -1)    
            hDiffDown.Add(hDiff)
            #Get unc band for the top plot
            uncGraphTop = getUncBand(hSumAllBkg, hDiffUp, hDiffDown,False)
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
        plotLegend.AddEntry(dataHist[0], SampleData["Data"][1], "PEL")
        yDict["Data"] = getYield(dataHist[0]) 
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
            s2 = hSig.GetName().split("_")[2]
            sName = "%s_%s_%s"%(s0, s1, s2)
            yDict[sName] = getYield(hSig) 
            sList.append(sName)
            plotLegendName = SampleSignal[sName][1] 
            decoHistSig(hSig, xTitle, yTitle, SampleSignal[sName][0]+col_depth)
            plotLegend.AddEntry(hSig, plotLegendName, "PL")
    plotLegend.Draw()
    hStack.SetMinimum(0.1)
    yDict["Bkgs"] = getYield(hSumAllBkg)
    if isLog and hSumAllBkg.Integral() !=0:
        gPad.SetLogy(True)
        if isData:
            hStack.SetMaximum(500*dataHist[0].GetMaximum())
        else:
            hStack.SetMaximum(500*hStack.GetMaximum())
    else: 
        #hStack.SetMaximum(1.3*hStack.GetMaximum())
        hStack.SetMaximum(1.5*dataHist[0].GetMaximum())
    hStack.GetXaxis().SetTitle(xTitle)
    hStack.GetYaxis().SetTitle(yTitle)

    #Draw CMS, Lumi, channel
    chColor = 1
    if channel in ["mu", "Mu", "m"]:
        chColor = rt.kCyan+col_depth
        chName = "1#color[%i]{#mu}, p_{T}^{miss} > 20"%chColor
    elif channel in ["ele", "Ele"]:
        chColor = rt.kRust+col_depth
        chName = "1#color[%i]{e}, p_{T}^{miss}  > 20"%chColor
    else:
        chColor = rt.kRed + col_depth
        chName = "1#color[%i]{#mu + e}, p_{T}^{miss}  > 20"%chColor
    #chName = "#splitline{%s}{%s}"%(chName, region)
    chName = "%s, #bf{%s}"%(chName, region)
    crName = formatCRString(Regions[region])
    crName = "%s, #color[2]{%s}"%(crName, stage)
    chCRName = "#splitline{#font[42]{%s}}{#font[42]{(%s)}}"%(chName, crName)
    extraText   = "#splitline{Preliminary}{%s}"%chCRName
    if isData and isRatio:
        nData  = str(int(dataHist[0].Integral()))
        nRatio = str(round(dataHist[0].Integral()/hSumAllBkg.Integral(),2))
        extraText   = "#splitline{Preliminary, Data = %s, Ratio = %s}{%s}"%(nData, nRatio, chCRName)
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
        hRatio = dataHist[0].Clone("hRatio")
        hRatio.Divide(hSumAllBkg)
        decoHistRatio(hRatio, xTitle, "Data/Bkgs", chColor)
        sList.append("Data/Bkgs")
        yDict["Data/Bkgs"] = ["---", round(dataHist[0].Integral()/hSumAllBkg.Integral(),2), " --- (---)"]
        hRatio.GetYaxis().SetRangeUser(0.5, 1.5);
        hRatio.Draw()
        if isUnc:
            uncGraphRatio = getUncBand(hSumAllBkg, hDiffUp, hDiffDown,True)
            uncGraphRatio.SetFillColor(2);
            uncGraphRatio.SetFillStyle(3001);
            uncGraphRatio.Draw("E2same");
        baseLine = TF1("baseLine","1", -100, 10000);
        #baseLine.SetLineColor(kRed+1);
        baseLine.SetLineColor(3);
        baseLine.Draw("SAME");
        hRatio.Draw("same")
    #canvas.SaveAs("%s/%s.pdf"%(outPlotFullDir, hName))
    canvas.SaveAs("%s/%s_%s_%s.pdf"%(outPlotFullDir, hName, year, channel))
    #canvas.SaveAs("PlotFromHist/pdf/%s_%s_%s.png"%(hName, year, channel))
    cap = "%s, %s, %s, %s"%(year, channel, region, hName)
    tHead = "Process & Entry & Yield & Stat (Syst)\\%\\\\\n" 
    table = createTable(yDict, sList, 4, tHead, cap.replace("_", "\\_"))
    tableFile = open("%s/%s_%s_%s.tex"%(outPlotFullDir, hName, year, channel), "w")
    print table
    tableFile.write(table)

#-----------------------------------------
#Finally make the plot for each histogram
#----------------------------------------
isData   = True
isRatio  = True
if "SR" in region or len(region)==13:
    isData  = False
    isRatio = False
isSig    = True
isUnc    = False
isLog    = False
makePlot(hName, region, isSig,  isData, isLog, isRatio, isUnc)
