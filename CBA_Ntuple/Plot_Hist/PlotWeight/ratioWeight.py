import os
import sys
import math
import numpy
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
iPosX = 0;
ModTDRStyle()
xPadRange = [0.0,1.0]

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Merge for combined years and channels")
parser.add_option("--isSep","--isSep", dest="isSep",action="store_true",default=False, help="Merge for separate years and channels")
parser.add_option("--isComb","--isComb", dest="isMerge",action="store_true",default=False, help="Merge for combined years and channels")
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep = options.isSep
isComb = options.isMerge

Samples = list(sampMC.keys())
if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
    Samples = [Samples[0]]
if isSep: 
    isComb = False
if isComb:
    isSep = False
    Years = Years_
    Channels = Channels_
if not isCheck and not isSep and not isComb:
    print("Add either --isCheck or --isSep or --isComb in the command line")
    exit()

def checkNanInBins(hist):
    checkNan = False
    for b in range(hist.GetNbinsX()):
        if math.isnan(hist.GetBinContent(b)):
            print("%s: bin %s is nan"%(hist.GetName(), b))
            checkNan = True
    return checkNan

gROOT.SetBatch(True)

os.system("mkdir -p %s"%dirPlot)
fPath = open("%s/ratioWeight.txt"%dirPlot, 'w')
for sample, decay, channel, year in itertools.product(Samples, Decays, Channels, Years):
    ydc = "%s/%s/%s"%(year, decay, channel)
    print("--------------------------------------------")
    print("%s, %s, %s"%(ydc, sample, hName))
    print("--------------------------------------------")
    inHistFullDir  = "%s/%s"%(dirHist, ydc)
    outPlotFullDir = "%s/%s/%s"%(dirPlot, ydc, region)
    if not os.path.exists(outPlotFullDir):
        os.makedirs(outPlotFullDir)
    rootFile = TFile("%s/AllInc.root"%(inHistFullDir), "read")
    if isCheck: 
        print(rootFile)
    #print("%10s %10s %10s %10s, %10s"%("Systematics", "Down", "Base", "Up", "RelativeUnc"))
    print("%20s %14s %22s %22s %10s"%("Syst", "Down", "Base", "Up", "Unc"))
    print("%20s %6s %8s %8s %6s %8s %8s %6s %8s %8s %5s"%("", 
    "UnderF", "Integral", "OverF", 
    "UnderF", "Integral", "OverF", 
    "UnderF", "Integral", "OverF", ""))
                
    histDict = {}
    sfDict = {}
    allSystPercentage = {}
    systDict_ = {}
    for key in systDict.keys():
        systList = []
        for index, syst in enumerate(systDict[key]):
            hPathNoSF   = "%s/%s/1Base/%s"%(sample, region, hName)
            hPathBase   = "%s/%s/%sBase/%s"%(sample, region, syst, hName)
            hPathUp     = "%s/%s/%sUp/%s"%(sample, region, syst, hName)
            hPathDown   = "%s/%s/%sDown/%s"%(sample, region, syst, hName)
            if isCheck:
                print(hPathBase)
            hBase = rootFile.Get(hPathBase).Clone("Base_")
            hNoSF   = rootFile.Get(hPathNoSF).Clone("%sNoSF_"%syst) 
            hUp   = rootFile.Get(hPathUp).Clone("%sUp_"%syst) 
            hDown = rootFile.Get(hPathDown).Clone("%sDown_"%syst) 
            evtBase = hBase.Integral()
            evtNoSF = hNoSF.Integral()
            evtUp   = hUp.Integral()
            evtDown = hDown.Integral()
            #check if intergal is 0
            #if evtUp ==0.0 or evtBase ==0.0 or evtDown ==0.0:
            #i = integral, u = undeflow, o = overflow
            iEvtBase = round(hBase.Integral(),0)
            iEvtNoSF = round(hNoSF.Integral(),0)
            iEvtUp   = round(hUp.Integral(),0)
            iEvtDown = round(hDown.Integral(),0)
            uEvtBase = round(hBase.GetBinContent(0),0)
            uEvtNoSF = round(hNoSF.GetBinContent(0),0)
            uEvtUp   = round(hUp.GetBinContent(0),0)
            uEvtDown = round(hDown.GetBinContent(0),0)
            oEvtBase = round(hBase.GetBinContent(hBase.GetNbinsX()+1),0)
            oEvtNoSF = round(hNoSF.GetBinContent(hNoSF.GetNbinsX()+1),0)
            oEvtUp   = round(hUp.GetBinContent(hUp.GetNbinsX()+1),0)
            oEvtDown = round(hDown.GetBinContent(hDown.GetNbinsX()+1),0)
            errFrom  = "%s, %s, %s"%(ydc, sample, syst)
            if uEvtBase >1000 or oEvtBase >1000:
                print("WE: %s: Base:  Overflow or Undeflow is more than 1000"%errFrom)
            if uEvtNoSF >1000 or oEvtNoSF >1000:
                print("WE: %s: NoSF:  Overflow or Undeflow is more than 1000"%errFrom)
            if uEvtUp >1000 or oEvtUp >1000:
                print("WE: %s: Up:  Overflow or Undeflow is more than 1000"%errFrom)
            if uEvtDown >1000 or oEvtDown >1000:
                print("WE: %s: Down:  Overflow or Undeflow is more than 1000"%errFrom)
            if evtBase ==0.0:
                print("WE: %s evtBase is zero"%errFrom)
                continue
            #check if intergal is NaN
            if math.isnan(evtUp) or math.isnan(evtDown):
                print("WE: %s: Inegral is nan"%errFrom)
                continue
            #check if bins are nan
            if checkNanInBins(hUp) or checkNanInBins(hBase) or checkNanInBins(hDown):
                print("WE: %s: Some of the bins are nan"%errFrom)
                continue
            allSystPercentage[syst] = 100*max(abs(evtUp -evtBase),abs(evtBase-evtDown))/evtBase
            print("%18s" 
                   "|%6.0f %8.0f %8.0f"
                   "|%6.0f %8.0f %8.0f"
                   "|%6.0f %8.0f %8.0f"
                   "|%5.1f%%"%(syst, 
                 uEvtDown, iEvtDown, oEvtDown, 
                 uEvtBase, iEvtBase, oEvtBase, 
                 uEvtUp, iEvtUp, oEvtUp,
                allSystPercentage[syst]))
            if allSystPercentage[syst] > 100.0:
                print("WE: Large uncertainty for %s: %10.2f"%(errFrom, allSystPercentage[syst]))
            #Ratio Up
            hRatioUp = hUp.Clone("%s_up"%syst)
            hRatioNoSF = hNoSF.Clone("%s_base"%syst)
            hRatioDown = hDown.Clone("%s_down"%syst)
            hRatioUp.Divide(hBase)
            hRatioNoSF.Divide(hBase)
            hRatioDown.Divide(hBase)
            decoHistRatio(hRatioUp, hName, syst, 6)
            hRatioUp.GetXaxis().SetTitleSize(0.07)
            hRatioUp.GetXaxis().SetLabelSize(0.07)
            #hRatioUp.GetYaxis().SetTitleSize(0.045)
            #hRatioUp.GetYaxis().SetLabelSize(0.045)
            #hRatioUp.GetYaxis().SetRangeUser(0.1, 2)
            #hRatioUp.GetYaxis().SetTitleOffset(1.5)
            hRatioUp.GetXaxis().SetTitleOffset(1.2)
            #Ratio Down
            decoHistRatio(hRatioNoSF, hName, syst, 1)
            decoHistRatio(hRatioDown, hName, syst, 8)
            hRatioUp.SetLineWidth(1)
            hRatioNoSF.SetLineWidth(1)
            hRatioDown.SetLineWidth(1)
            hRatioUp.SetLineStyle(index+1)
            hRatioNoSF.SetLineStyle(index+1)
            hRatioDown.SetLineStyle(index+1)
            histDict[syst] = [hRatioUp, hRatioNoSF, hRatioDown]
            sfDict[syst] = [iEvtUp/iEvtBase, iEvtNoSF/iEvtBase, iEvtDown/iEvtBase]
            systList.append(syst)
        systDict_[key] = systList

    nSyst = len(systDict_.keys())
    canvas = TCanvas("sfRatio", "sfRatio", 280, 100*nSyst)
    #canvas = TCanvas()
    canvas.Divide(1, nSyst) 
    gPad.SetRightMargin(0.03);
    #gPad.SetTopMargin(0.07);
    #gPad.SetTickx(0);
    gPad.RedrawAxis();

    yPadRange = [0.0,0.30-padGap, 0.30+padGap,1.0]
    start = 1.0
    yPadRange = [start]
    for n in range(nSyst):
        yPadRange.append(start - (n+start)/(nSyst))

    legDict = {}
    for i, key in enumerate(systDict_.keys()):
        canvas.cd(i+1)
        gPad.SetPad(xPadRange[0],yPadRange[i],xPadRange[1],yPadRange[i+1]);
        #gPad.SetLogy(True);
        if(i+1==nSyst):
            gPad.SetBottomMargin(0.17)
        else:
            gPad.SetBottomMargin(0.0)
        #Draw Leg
        leg = TLegend(0.20,0.15,0.93,0.45)
        decoLegend(leg, 5, 0.12)
        leg.SetNColumns(3)
        sysLabel = {"down":"-", "base":"0", "up":"+"}
        for k, syst in enumerate(systDict_[key]):
            for j, h in enumerate(histDict[syst]):
                h.GetYaxis().SetTitle(key)
                h.GetYaxis().SetRangeUser(0.5, 1.5)
                sysName = syst.split("_")[-1]
                sysType = sysLabel[h.GetName().split("_")[-1]]
                legName = "%s=%s%s"%(round(sfDict[syst][j],2), sysName, sysType)
                leg.AddEntry(h, legName, "L")
                if(k==0 and j==0):
                    h.Draw("hist")
                else:
                    h.Draw("hist same")
        legDict[key] = leg

    for i, syst in enumerate(legDict.keys()):
        canvas.cd(i+1)
        legDict[syst].Draw()
        #leg.Draw("same")

    #Draw CMS, Lumi, channel
    lumi_13TeV = getLumiLabel(year) 
    chName = getChLabel(decay, channel)
    selName = formatCRString(region)
    nBase = "#font[42]{%s (N=%s)}"%(sample, str(round(evtBase,2)))
    #line1 = "Preliminary, %s, %s"%(chName, region)
    line1 = "Preliminary, %s"%(chName)
    line2 = selName
    line3 = nBase
    #extraText = "#splitline{%s, %s}{%s}"%(line1, line2, line3)
    #`extraText = "#splitline{%s}{#splitline{%s}{%s}}"%(line1, line2, line3)
    extraText = "#splitline{%s}{#splitline{%s}{%s, %s}}"%(line3, "", line1, line2)

    CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
    #Draw Baseline
    baseLine = TF1("baseLine","1", -100, 10000);
    baseLine.SetLineColor(1);
    baseLine.Draw("same");
    pdf = "%s/ratioWeight_%s_%s_%s.pdf"%(outPlotFullDir, ydc.replace("/","_"), sample, hName)
    canvas.SaveAs(pdf)
    fPath.write("%s\n"%pdf)
print(fPath)
