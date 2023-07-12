import os
import sys
import json
import math
import numpy
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("PlotWeight", "")) 
sys.path.insert(0, os.getcwd().replace("Plot_Hist/PlotWeight", "Hist_Ntuple/HistWeight/")) 
import itertools
from HistInfo import hForEffs
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
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Merge for combined years and channels")
parser.add_option("--isSep","--isSep", dest="isSep",action="store_true",default=True, help="Merge for separate years and channels")
parser.add_option("--isComb","--isComb", dest="isMerge",action="store_true",default=False, help="Merge for combined years and channels")
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep = options.isSep
isComb = options.isMerge

if isCheck:
    isSep  = False
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
if isSep: 
    isComb = False
if isComb:
    isSep = False
    Years = Years_
    Channels = Channels_
if not isCheck and not isSep and not isComb:
    print("Add either --isCheck or --isSep or --isComb in the command line")
    exit()

os.system("mkdir -p %s"%dirPlot)
fPath = open("%s/effPlot.txt"%dirPlot, 'w')
gROOT.SetBatch(True)

for year, decay, channel in itertools.product(Years, Decays, Channels):
    ydc = "%s/%s/%s"%(year, decay, channel)
    print("--------------------------------------------")
    print(ydc)
    print("--------------------------------------------")
    inHistFullDir  = "%s/%s"%(dirHist, ydc)
    outPlotFullDir = "%s/%s/%s"%(dirPlot, ydc, region)
    if not os.path.exists(outPlotFullDir):
        os.makedirs(outPlotFullDir)
    rootFile = TFile("%s/AllInc.root"%(inHistFullDir), "read")
    if isCheck: 
        print(rootFile)

    hForEff = []
    for h in hForEffs.keys():
        if channel in h: hForEff = hForEffs[h]
    print(hForEff)
    hForEff_ = {}
    hForEff_["exclusive_trigger"] = [hForEff[0], hForEff[1]]
    hForEff_["trigger_flow"]      = [hForEff[0], hForEff[2]]
    print(hForEff_)

    for (var, hs) in hForEff_.items():
        canvas = TCanvas()
        canvas.cd()
        gPad.SetLogy(True)
        
        #get effs 
        effs = []
        for samp in overlayEff:
            eff, labels   = getEff(rootFile, samp, region, hs)
            effs.append(eff)
        #plot effs
        leg = TLegend(0.65,0.75,0.95,0.92); 
        decoLegend(leg, 4, 0.03)
        for index, eff in enumerate(effs): 
            xTitle = var
            yTitle = "Acceptance"
            name = eff.GetName()
            decoEff(eff, xTitle, yTitle, sampAll[name][0])
            if "flow" in var:
                eff.SetMaximum(10)
                eff.SetMinimum(0.01)
            else:
                eff.SetMaximum(100)
                eff.SetMinimum(0.0001)
            #eff.GetXaxis().SetRangeUser(10, 400)
            if index==0:
                eff.Draw("ALP")
                #eff.GetXaxis().SetBinLabel(4, "ss")
            else:
                eff.Draw("LPsame")
            leg.AddEntry(eff, "%s"%(sampAll[name][1]), "APL")
        
        #Draw CMS, Lumi, channel
        extraText  = "Preliminary"
        lumi_13TeV = getLumiLabel(year)
        chName = getChLabel(decay, channel)
        #extraText   = "#splitline{Preliminary}{#splitline{%s}{%s}}"%(chName, region)
        extraText = "Preliminary"
        for b in labels.keys():
            extraText = "#splitline{%s}{%s = %s}"%(extraText, b, labels[b])
        CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
        leg.Draw()
        
        pdf = "%s/%s/eff_%s.pdf"%(dirPlot, ydc, var)
        png = pdf.replace("pdf", "png")
        canvas.SaveAs(pdf)
        canvas.SaveAs(png)
        fPath.write("%s\n"%pdf)

print(fPath)
