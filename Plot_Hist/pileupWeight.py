from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F 
import ROOT as rt
import os
import numpy
import sys
import math
from optparse import OptionParser
from PlotInputs import *
from PlotFunc import *
from PlotCMSLumi import *
from PlotTDRStyle import *
sys.path.insert(0, os.getcwd().replace("Plot_Hist", "Ntuple_Skim/sample"))
from Skim_NanoAOD_FileLists_cff_danny import *

padGap = 0.01
iPeriod = 4;
iPosX = 10;
setTDRStyle()
xPadRange = [0.0,1.0]
yPadRange = [0.0,0.30-padGap, 0.30+padGap,1.0]
xMin = 1.0
xMax = 75.0
yMinRatio = 0.0001 
yMaxRatio = 100.0

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decayMode", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decayMode moded of ttbar SemiLep or DiLep? default is SemiLep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
		  help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="TTbar",type='str',
		  help="name of the MC sample" )
parser.add_option("--ps", "--phaseSpace", dest="phaseSpace", default="Boosted_SR",type='str', 
                     help="which control selection and region")
parser.add_option("--plot", "--plot", dest="hName", default="Weight_pileup",type='str', 
                     help="name of the histogram")
(options, args) = parser.parse_args()
year            = options.year
decayMode       = options.decayMode
channel         = options.channel
sample          = options.sample
hName            = options.hName
phaseSpace = options.phaseSpace
print "------------------------------------"
print "%s, %s, %s, %s, %s"%(year, decayMode, channel, sample, hName)
print "------------------------------------"

outPlotSubDir = "Plot_Hist/%s/Syst/%s/%s/%s"%(year, decayMode, channel, phaseSpace)
outPlotFullDir = "%s/%s"%(condorHistDir, outPlotSubDir)
if not os.path.exists(outPlotFullDir):
    os.makedirs(outPlotFullDir)

#-----------------------------------------
#Get histograms
#----------------------------------------
pathData = "../Ntuple_Skim/weight/PileupSF"
fDataDown = "Data_2016BCDGH_Pileup_scaledDown.root"
fDataBase = "Data_2016BCDGH_Pileup.root"
fDataUp   = "Data_2016BCDGH_Pileup_scaledUp.root"
if year=="2017":
    fDataDown = "Data_2017BCDEF_Pileup_scaledDown.root"
    fDataBase = "Data_2017BCDEF_Pileup.root"
    fDataUp   = "Data_2017BCDEF_Pileup_scaledUp.root"
if year=="2018":
    fDataDown = "Data_2018ABCD_Pileup_scaledDown.root"
    fDataBase = "Data_2018ABCD_Pileup.root"
    fDataUp   = "Data_2018ABCD_Pileup_scaledUp.root"

fileDataDown = TFile(pathData+"/"+fDataDown, "read")
fileDataBase = TFile(pathData+"/"+fDataBase, "read")
fileDataUp   = TFile(pathData+"/"+fDataUp, "read")

hDataDown = fileDataDown.Get("pileup")
hDataBase = fileDataBase.Get("pileup")
hDataUp   = fileDataUp.Get("pileup")
col_depth = 0
if year=="2017":col_depth = 1
if year=="2018":col_depth = 2

hDataBase.GetYaxis().SetTitle("Events (normalised to unity)")
hDataBase.GetYaxis().SetTitleSize(0.06)
hDataBase.GetYaxis().SetLabelSize(0.05)
hDataBase.SetLineColor(rt.kOrange + col_depth)
hDataBase.SetMarkerColor(rt.kOrange + col_depth)
hDataBase.SetMarkerStyle(20)
hDataBase.GetXaxis().SetRangeUser(xMin, xMax)
hDataBase.GetYaxis().SetRangeUser(0.0, 0.8)

hDataUp.SetMarkerColor(rt.kAzure  + col_depth)
hDataUp.SetLineColor(rt.kAzure  + col_depth)
hDataUp.SetMarkerStyle(20)
hDataUp.GetXaxis().SetRangeUser(xMin, xMax) 
hDataUp.GetYaxis().SetRangeUser(0.0, 0.8)

hDataDown.SetMarkerColor(rt.kViolet + col_depth)
hDataDown.SetLineColor(rt.kViolet + col_depth)
hDataDown.SetMarkerStyle(20)
hDataDown.GetXaxis().SetRangeUser(xMin, xMax)
hDataDown.GetYaxis().SetRangeUser(0.0, 0.8)

hDataDown.Scale(1.0/hDataDown.Integral())
hDataBase.Scale(1.0/hDataBase.Integral())
hDataUp.Scale(1.0/hDataUp.Integral())


#-----------------------------------------
# MC Histograms
#-----------------------------------------
#mcName = eval("TTbarPowheg_Dilepton_%s_%s"%("FileList", year))
mcName = eval("TTbarPowheg_Semilept_%s_%s"%("FileList", year))
#mcName = eval("TTbarPowheg_Hadronic_%s_%s"%("FileList", year))
mcNameArray = mcName.split(" ")
hMC = hDataBase.Clone("hMC")
hMC.Reset()
for mc in mcNameArray:
    fMC = TFile.Open(mc, "read")
    hMC_ = fMC.Get("hPUTrue")
    hMC.Add(hMC_, 1)
#print hMC.Integral()
#mcPU for some reason seems to be 1000 bins, rebin by 1000/200 (factor of 5) to get same binning in both to allow the scaling to work
if (hMC.GetNbinsX()!=hDataBase.GetNbinsX()):
    if (hMC.GetNbinsX()>hDataBase.GetNbinsX()):
        hMC.Rebin(hMC.GetNbinsX()/hDataBase.GetNbinsX());
hMC.Scale(1.0/hMC.Integral());
hMC.SetLineWidth(4)
hMC.SetLineColor(rt.kBlack + col_depth)
hMC.GetXaxis().SetRangeUser(xMin, xMax)
hMC.GetYaxis().SetRangeUser(0.0, 0.8)

#-----------------------------------------
# Draw histograms 
#----------------------------------------
gROOT.SetBatch(True)
canvas = TCanvas()
canvas.Divide(1, 2)
canvas.cd(1)
gPad.SetRightMargin(0.03);
gPad.SetPad(xPadRange[0],yPadRange[2],xPadRange[1],yPadRange[3]);
gPad.SetTopMargin(0.09);
gPad.SetBottomMargin(padGap);
#gPad.SetTickx(0);
gPad.RedrawAxis();
#gPad.SetLogy(True)
gPad.SetLogx(True)
hDataBase.Draw("EP")
hDataUp.Draw("EPsame")
hDataDown.Draw("EPsame")
hMC.Draw("Histsame")
lumi_13TeV = "35.9 fb^{-1}"
col_year  = rt.kGreen
if "16" in year:
    col_depth = -3
    lumi_13TeV = "35.9 fb^{-1} (#color[%i]{2016})"%(col_year+col_depth)
if "17" in year:
    col_depth = -2
    lumi_13TeV = "41.5 fb^{-1} (#color[%i]{2017})"%(col_year + col_depth)
if "18" in year:
    col_depth = -1
    lumi_13TeV = "59.7 fb^{-1} (#color[%i]{2018})"%(col_year + col_depth)
#Draw CMS, Lumi, channel
if channel in ["mu", "Mu", "m"]:
    chName = "1 #color[2]{#mu}, %s"%sample
else:
    chName = "1 #color[6]{e}, %s"%sample
#crName = formatCRString(phaseSpace)
#chName = "%s, %s"%(chName, phaseSpace)
#chCRName = "#splitline{#font[42]{%s}}{#font[42]{%s}}"%(chName, crName)
chCRName = "%s"%chName
extraText   = "#splitline{Preliminary}{%s}"%chCRName
#CMS_lumi(canvas, iPeriod, iPosX, extraText)
CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
#Draw Leg
leg = TLegend(0.20,0.40,0.35,0.80)
leg.AddEntry(hDataDown, "#splitline{Data down}{(mean = %s)}"%str(round(hDataDown.GetMean(),1)), "EPL")
leg.AddEntry(hDataBase, "#splitline{Data nominal}{(mean = %s)}"%str(round(hDataBase.GetMean(),1)), "EPL")
leg.AddEntry(hDataUp,   "#splitline{Data up}{(mean = %s)}"%str(round(hDataUp.GetMean(),1)), "EPL")
leg.AddEntry(hMC,   "#splitline{ TTbar}{(mean = %s)}"%str(round(hMC.GetMean(),1)), "L")
decoLegend(leg, 5, 0.034)
leg.Draw("same")

canvas.cd(2)
gPad.SetTopMargin(padGap); 
gPad.SetBottomMargin(0.30); 
gPad.SetRightMargin(0.03);
#gPad.SetTickx(0);
gPad.SetPad(xPadRange[0],yPadRange[0],xPadRange[1],yPadRange[2]);
gPad.RedrawAxis();
gPad.SetLogy(True)
gPad.SetLogx(True)

hRatioBase = hDataBase.Clone("hRatio_base")
hRatioBase.Divide(hMC)
decoHistRatio(hRatioBase, "Number of primary vertices", "Data/Bkg", col_depth + rt.kOrange)
#hRatioBase.SetLineWidth(2)
hRatioBase.GetYaxis().SetRangeUser(yMinRatio, yMaxRatio)
hRatioBase.GetXaxis().SetRangeUser(xMin, xMax)

hRatioUp = hDataUp.Clone("hRatio_up")
hRatioUp.Divide(hMC)
decoHistRatio(hRatioUp, "Number of primary vertices", "Data/Bkg", col_depth + rt.kAzure)
#hRatioUp.SetLineWidth(2)
hRatioUp.GetYaxis().SetRangeUser(yMinRatio, yMaxRatio)
hRatioUp.GetXaxis().SetRangeUser(xMin, xMax)

hRatioDown = hDataDown.Clone("hRatio_up")
hRatioDown.Divide(hMC)
#hRatioDown.SetLineWidth(2)
decoHistRatio(hRatioDown, "Number of primary vertices", "Data/Bkg", col_depth + rt.kViolet)
hRatioDown.GetYaxis().SetRangeUser(yMinRatio, yMaxRatio)
hRatioDown.GetXaxis().SetRangeUser(xMin, xMax)

hRatioBase.Draw("EP")
hRatioUp.Draw("EPsame")
hRatioDown.Draw("EPsame")

#Draw Baseline
baseLine = TF1("baseLine","1", -100, 2000);
baseLine.SetLineColor(1);
baseLine.Draw("same");
#canvas.SaveAs("%s/%s.pdf"%(outPlotFullDir, hName))
canvas.SaveAs("%s/%s_%s_%s_%s.pdf"%(outPlotFullDir, hName, year, channel, sample))
#canvas.SaveAs("SystRatio_%s_%s_%s_%s_%s_%s.pdf"%(year, decayMode, channel, hName, sample, phaseSpace))
