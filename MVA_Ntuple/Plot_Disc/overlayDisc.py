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
fPath = open("%s/overlayDisc_%s_%s.txt"%(dirPlot, dir_, outTxt), 'w')

hName = 'Reco_mass_T'
for decay, region, channel, year in itertools.product(Decays, rList, Channels, Years):
    isLog    = False
    print("----------------------------------------------")
    print("%s, %s, %s, %s, %s"%(decay, hName, region, channel, year))
    ydc = "%s/%s/%s"%(year, decay, channel)
    inHistDir  = "%s/%s/%s/CombMass/BDTA"%(dirDisc, dir_, ydc)
    outPlotDir = "%s/%s/%s/CombMass/BDTA"%(dirPlot, dir_, ydc)
    os.system("mkdir -p %s"%outPlotDir)
    inFile = TFile("%s/AllInc.root"%(inHistDir), "read")
    if isCheck:
        print(inFile)
    gROOT.SetBatch(True)
    legend = TLegend(0.60,0.60,0.80,0.88); 
    decoLegend(legend, 4, 0.030)
    pDict = {}
    #pDict["data_obs"] = inFile.Get("data_obs/%s/Base/%s"%(region, hName))
    for i, s in enumerate(SampleBkg.keys()):
        dPath   = "%s/%s/Base/%s"%(s, region, hName)
        if i==0:
            bkgDisc = inFile.Get(dPath)
        else:
            bkgDisc.Add(inFile.Get(dPath))
    name = "All Background (%s)"%(round(bkgDisc.Integral(), 3))
    bkgDisc.Scale(1/bkgDisc.Integral())
    pDict[name] = bkgDisc
    legend.AddEntry(bkgDisc, name,  "L")
    
    #Mass = ["700", "1200"]
    Mass  = ["800", '1100', "1200", "1500", "2750"]
    for mass in Mass: 
        sigDisc = inFile.Get("SignalSpin12_M%s/%s/Base/%s"%(mass, region, hName))
        int_ = sigDisc.Integral()
        if int_==0.0:
            continue
        name = "Signal, M%s (%s)"%(mass, round(sigDisc.Integral(), 3))
        sigDisc.Scale(1/int_)
        pDict[name] = sigDisc
        legend.AddEntry(sigDisc, name,  "L")

    canvas = TCanvas()
    canvas.cd()
    if isLog:
        gPad.SetLogy(True);
    maxInt = 0.0;
    pDict = OrderedDict(sorted(pDict.items(), key=lambda t: t[0]))
    for index, s in enumerate(pDict.keys()):
        pDict[s].SetLineColor(index+1)
        pDict[s].SetLineWidth(3)
        pDict[s].SetMarkerStyle(20+index);
        pDict[s].SetMarkerColor(index+1);
        pDict[s].GetYaxis().SetTitle("Events (norm. to 1)") 
        pDict[s].GetYaxis().SetLabelSize(.040)
        pDict[s].GetXaxis().SetLabelSize(.035)
        pDict[s].GetXaxis().SetTitle("%s"%hName)
        if index==0 and not "data_obs" in s:
            print(s)
            pDict[s].SetMaximum(0.5)
            pDict[s].GetXaxis().SetRangeUser(0, 2000)
            #pDict[s].SetMaximum(100*pDict["All Background"].GetMaximum())
            #pDict[s].SetMinimum(0.01)
            pDict[s].Draw("HIST")
        elif "data_obs" in s:
            pDict[s].Draw("EPsame")
            pDict[s].SetMarkerStyle(20)
            pDict[s].SetMarkerColor(1)
            pDict[s].SetLineColor(1)
        else:
            pDict[s].Draw("Histsame")
        #legName = "%s, mean = %i, int = %i"%(econDict[s][1], pDict[s].GetMean(), pDict[s].Integral())
        canvas.Update()
        
    legend.Draw()
    #---------------------------
    #Draw CMS, Lumi, channel
    #---------------------------
    chName = getChLabel(decay, channel)
    chCRName = "#splitline{#font[42]{%s}}{#font[42]{%s}}"%(chName, region)
    extraText   = "#splitline{Preliminary}{%s}"%chCRName
    lumi_13TeV = getLumiLabel(year)
    CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
    pdf = "%s/overlayDisc_%s_%s_%s.pdf"%(outPlotDir, dir_, hName, region)
    canvas.SaveAs(pdf)
    fPath.write("%s\n"%pdf)
print(fPath)
