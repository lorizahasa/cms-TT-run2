import ROOT
import os
import sys
import json
import itertools
from optparse import OptionParser
import CombineHarvester.CombineTools.ch as ch
from FitInputs import *
from array import array

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--years", dest="years", default="2016Pre",type='str',
                     help="Specify the years of the data taking" )
parser.add_option("-d", "--decayMode", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decayMode moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channels", dest="channels", default="Mu",type='str',
		  help="Specify which channels Mu or Ele? default is Mu" )
parser.add_option("-m", "--mass", dest="mass", default="800",type='str',
                     help="Specify the mass of charged Higgs")
parser.add_option("--method", "--method", dest="method", default="BDTA",type='str',
                     help="Specify MVA method") 
parser.add_option("-r", "--regions", dest="regions", default="ttyg_Enriched_SR_Resolved",type='str', 
                     help="which control selection and regions"), 
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_T",type='str', 
                     help="which histogram to be used for making datacard")
parser.add_option("--isT2W","--isT2W",dest="isT2W", default=False, action="store_true",
		  help="create text2workspace datacards")
parser.add_option("--isFD","--isFD",dest="isFD", default=False, action="store_true",
		  help="run FitDiabnostics")
parser.add_option("--isImpact","--isImpact",dest="isImpact", default=False, action="store_true",
		  help="run impacts")
parser.add_option("--isLimit","--isLimit",dest="isLimit", default=False, action="store_true",
		  help="run impacts")
parser.add_option("--isCM","--isCM",dest="isCM", default=False, action="store_true",
		  help="make plot of covariance matrix")
parser.add_option("--isTP","--isTP",dest="isTP", default=False, action="store_true",
		  help="generate toys")
parser.add_option("--isPlotTP","--isPlotTP",dest="isPlotTP", default=False, action="store_true",
		  help="plot generated toys")
(options, args) = parser.parse_args()
years           = options.years
decayMode       = options.decayMode
channels        = options.channels
mass            = options.mass
method            = options.method
regions          = options.regions
hName           = options.hName

isT2W 			= options.isT2W
isFD            = options.isFD
isImpact        = options.isImpact
isLimit         = options.isLimit
isCM            = options.isCM
isTP            = options.isTP
isPlotTP        = options.isPlotTP
#-----------------------------------------
#Various functions
#----------------------------------------
def runCmd(cmd):
    print("\n\033[01;32m Excecuting: \033[00m %s"%cmd)
    os.system(cmd)

#-----------------------------------------
#For separate datacards
#----------------------------------------
def getDataCard(year, decayMode, channel, region, hName):
    args = "-y %s -d %s -c %s -m %s -r %s --hist %s --method %s"%(year, decayMode, channel, mass, region, hName, method)
    runCmd("python3 makeDataCard.py  %s "%args)
    inDirDC = "./output/Fit_Disc/FitMain/%s/%s/%s/%s/%s/%s/%s"%(year, decayMode, channel, mass, method, region, hName)
    name = "%s/Datacard_Alone.txt"%inDirDC
    return name
#-----------------------------------------
#For combination of datacards
#----------------------------------------
dcList = []
for y in years.split("__"):
    for ch in channels.split("__"):
        for r in regions.split("__"):
            pathDC = getDataCard(y, decayMode, ch, r, hName)
            dcList.append(pathDC)
combDCText = ' '.join(dcList)
dirDC = "./output/Fit_Disc/FitMain/%s/%s/%s/%s/%s/%s/%s"%(years, decayMode, channels, mass, method, regions, hName)
if not os.path.exists(dirDC):
    os.makedirs(dirDC)
pathDC  = "%s/Datacard.txt"%(dirDC)
pathT2W = "%s/Text2W.root"%(dirDC)
runCmd("combineCards.py %s > %s"%(combDCText, pathDC))
print(pathDC)

if isT2W:
        runCmd("text2workspace.py %s -o %s"%(pathDC, pathT2W))
        print(pathT2W)

#-----------------------------------------
#Fit diagnostics
#----------------------------------------
rMin = 0
rMax = 20
#paramList = ["r", "nonPromptSF", "TTbarSF", "WGSF", "ZGSF", "OtherSF", "lumi_13TeV"]
#paramList = ["r", "WGammaSF", "ZGammaSF"]
paramList = ["r"]
params    = ','.join([str(param) for param in paramList])
if isFD:
    runCmd("combine -M FitDiagnostics  %s --out %s --robustHesse 1  --expectSignal 1 --plots --redefineSignalPOIs %s -v2 --cminDefaultMinimizerStrategy 0 --rMin=%s --rMax=%s"%(pathT2W, dirDC, params, rMin, rMax))
    #runCmd("python3 diffNuisances.py --all %s/fitDiagnostics.root -g %s/diffNuisances.root"%(dirDC,dirDC))
    print(dirDC)
    #store rateparams in a json file 
    myfile = ROOT.TFile("%s/fitDiagnostics.root"%dirDC,"read")
    fit_s = myfile.Get("fit_s")
    fit_s.Print()
    with open ('RateParams.json') as jsonFile:
        jsonData = json.load(jsonFile)
    rateParamKey = "AAA"
    jsonData[rateParamKey] = []
    for param in paramList:
        fit_s.floatParsFinal().find(param).Print()
        valLow = fit_s.floatParsFinal().find(param).getErrorLo()
        valNom = fit_s.floatParsFinal().find(param).getVal()
        valHi  = fit_s.floatParsFinal().find(param).getErrorHi()
        paramDict = {}
        paramDict[param] = [valLow, valNom, valHi] 
        jsonData[rateParamKey].append(paramDict)
    #plot covariant matrix
    with open ('RateParams.json', 'w') as jsonFile:
        json.dump(jsonData, jsonFile)

if isTP:
    runCmd("combine -M FitDiagnostics %s --name TP -t -1 --out %s --seed=314159 --plots --saveNLL --rMin=-5 --rMax=5 --setParameterRanges nonPromptSF=-10,10 --expectSignal=1 -t 500 -v3 --skipBOnlyFit --trackParameters r,BTagSF_b,BTagSF_l,EleEff,MuEff,PhoEff,lumi_13TeV,ZGSF,TTbarSF,OtherSF,WGSF,nonPromptSF &"%(pathT2W, dirDC))
    print(dirDC)

if isLimit:
    #https://github.com/cms-analysis/CombineHarvester/blob/master/docs/Limits.md
    #runCmd("combine --rAbsAcc 0.000001 %s -M AsymptoticLimits --mass %s --name _TT_run2"%(pathT2W, mass))
    runCmd("combineTool.py -d %s -M AsymptoticLimits --mass %s -n _TT_run2 --run blind --there --parallel 4 "%(pathT2W, mass))
    nameLimitOut = "higgsCombine_TT_run2.AsymptoticLimits.mH%s.root"%(mass)
    runCmd("combineTool.py -M CollectLimits %s/%s -o %s/limits.json"%(dirDC, nameLimitOut, dirDC))
    print(dirDC)

#-----------------------------------------
#Impacts of Systematics
#----------------------------------------
if isImpact:
    runCmd("combineTool.py -M Impacts -d %s  -m 125 --doInitialFit --robustFit 1 --cminDefaultMinimizerStrategy 0 -t -1  --redefineSignalPOIs %s --setParameterRanges r=-1,1"%(pathT2W, params)) 
    runCmd("combineTool.py -M Impacts -d %s  -m 125  --doFits --robustFit 1 --cminDefaultMinimizerStrategy 0  -t -1  --redefineSignalPOIs %s --setParameterRanges r=-1,1 --parallel 10"%(pathT2W, params))
    #runCmd("combineTool.py -M Impacts -d %s  -m 125 --doInitialFit --robustFit 1 --cminDefaultMinimizerStrategy 0 --expectSignal 1 -t -1  --redefineSignalPOIs %s --setParameterRanges r=0,20"%(pathT2W, params)) 
    #runCmd("combineTool.py -M Impacts -d %s  -m 125  --doFits --robustFit 1 --cminDefaultMinimizerStrategy 0 --expectSignal 1 -t -1  --redefineSignalPOIs %s --setParameterRanges r=0,20 --parallel 10"%(pathT2W, params))
    runCmd("combineTool.py -M Impacts -d %s -m 125 -o %s/nuisImpact.json --redefineSignalPOIs %s "%(pathT2W, dirDC, params))
    runCmd("python3 ./plotImpacts.py --cms-label \"   Internal\" -i %s/nuisImpact.json -o %s/nuisImpact.pdf"%(dirDC, dirDC))


#-----------------------------------------
# Make covariance matrix
#----------------------------------------
if isCM:
    ROOT.gROOT.SetBatch(True)
    Red    = [ 1.00, 0.00, 0.00, 0.87, 1.00, 0.51 ]
    Green  = [ 1.00, 0.00, 0.81, 1.00, 0.20, 0.00 ]
    Blue   = [ 1.00, 0.51, 1.00, 0.12, 0.00, 0.00 ]
    Length = [ 0.00, 0.02, 0.34, 0.51, 0.64, 1.00 ]
    lengthArray = array('d', Length)
    redArray = array('d', Red)
    greenArray = array('d', Green)
    blueArray = array('d', Blue)

    #ROOT.TColor.CreateGradientColorTable(6,lengthArray,redArray,greenArray,blueArray,99)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaintTextFormat('5.1f');
    canvas = ROOT.TCanvas()
    canvas.SetFillColor(10);
    canvas.SetBorderMode(0);
    canvas.SetBorderSize(0);
    canvas.SetTickx();
    canvas.SetTicky();
    canvas.SetLeftMargin(0.15);
    canvas.SetRightMargin(0.15);
    canvas.SetTopMargin(0.15);
    canvas.SetBottomMargin(0.15);
    canvas.SetFrameFillColor(0);
    canvas.SetFrameBorderMode(0);
       
    f1 = ROOT.TFile.Open('%s/fitDiagnostics.root'%(dirDC),'read')
    h_background = f1.Get('covariance_fit_b')
    h_signal = f1.Get('covariance_fit_s')
    h_signal.GetYaxis().SetLabelSize(0.02)
    h_signal.GetXaxis().SetLabelSize(0.02)
    h_signal.GetZaxis().SetLabelSize(0.03)
    h_signal.SetMarkerSize(0.7)
    h_signal.LabelsOption("v", "X")
    h_signal.SetContour(99)
    h_signal.Draw('colz, Y+, TEXT0')

    mypal = h_signal.GetListOfFunctions().FindObject('palette')
    print(mypal)
    mypal.SetX1NDC(0.02);
    mypal.SetX2NDC(0.06);
    mypal.SetY1NDC(0.1);
    mypal.SetY2NDC(0.9);
    canvas.Modified();
    canvas.Update();
    #ROOT.gApplication.Run()
    #canvas.SaveAs('%s/covarianceMatrix.pdf'%dirDC) 
    canvas.SaveAs('%s/covarianceMatrix.png'%dirDC) 

if isPlotTP:
    ROOT.gROOT.SetBatch(True)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(1)
    c1 = ROOT.TCanvas( 'c1', '', 800,800 )
    c1.SetFillColor(10)
    c1.SetBorderMode(0)
    c1.SetBorderSize(0)
    c1.SetTickx()
    c1.SetTicky()
    c1.SetLeftMargin(0.15)
    c1.SetRightMargin(0.15)
    c1.SetTopMargin(0.15)
    c1.SetBottomMargin(0.15)
    c1.SetFrameFillColor(0)
    c1.SetFrameBorderMode(0)
    c1.SetGrid()
    outputDir = "%s/NuisancePlots"%dirDC
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    listOfParameters = ["r","BTagSF_b","BTagSF_l","EleEff","MuEff","PhoEff","lumi_13TeV","ZGSF","TTbarSF","OtherSF","WGSF"]#,"nonPromptSF"]
    myfile = ROOT.TFile("%s/fitDiagnosticsTP.root"%dirDC,"read")
    mytree=myfile.tree_fit_sb
    for param in listOfParameters:
        hist = ROOT.TH1F("hist","",100,-2,2)
        mytree.Draw("%s >> hist"%(param))
        hist.Fit("gaus")
        hist.SetTitle("%s;"%param)
        hist.GetYaxis().SetLabelSize(0.03)
        hist.GetXaxis().SetLabelSize(0.03)
        ROOT.gPad.Update()
        mypal = hist.GetListOfFunctions().FindObject('stats')
        mypal.SetX1NDC(0.17)
        mypal.SetX2NDC(0.4)
        mypal.SetY1NDC(0.7)
        mypal.SetY2NDC(0.9)
        c1.Draw()
        c1.Modified()
        c1.Update()
        c1.Print("%s/%s.pdf"%(outputDir,param))
        hist.Delete()

