from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors
import os
import numpy
import sys
import math
sys.path.insert(0, os.getcwd().replace("Plot_Hist/PlotSF", "Hist_Ntuple/HistSF"))
from optparse import OptionParser
from PlotFunc import *
from PlotCMSLumi import *
from PlotTDRStyle import *
from HistInputs import Regions

padGap = 0.01
iPeriod = 4;
iPosX = 0;
setTDRStyle()
xPadRange = [0.0,1.0]

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
parser.add_option("-s", "--sample", dest="sample", default="TTGamma",type='str',
		  help="name of the MC sample" )
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched_SR",type='str', 
                     help="which control selection and region"), 
parser.add_option("--hist", "--hist", dest="hName", default="Reco_st",type='str', 
                     help="which histogram to be plottted")
(options, args) = parser.parse_args()
year            = options.year
decayMode       = options.decayMode
channel         = options.channel
sample          = options.sample
region = options.region
hName           = options.hName

print "------------------------------------"
print "%s, %s, %s, %s, %s"%(year, decayMode, channel, sample, hName)
print "------------------------------------"
#-----------------------------------------
#Path of the I/O histrograms/plots
#----------------------------------------
inHistSubDir = "Hist_Ntuple/HistSF/Rebin/%s/%s/%s/Merged"%(year, decayMode, channel)
inHistFullDir = "%s/%s"%(condorHistDir, inHistSubDir)
outPlotSubDir = "Plot_Hist/PlotSF/Rebin/%s/%s/%s/%s"%(year, decayMode, channel, region)
outPlotFullDir = "%s/%s"%(condorHistDir, outPlotSubDir)
if not os.path.exists(outPlotFullDir):
    os.makedirs(outPlotFullDir)

gROOT.SetBatch(True)
rootFile = TFile("%s/AllInc.root"%(inHistFullDir), "read")
print rootFile
#print("%10s %10s %10s %10s, %10s"%("Systematics", "Down", "Base", "Up", "RelativeUnc"))
print("%10s %22s %22s %22s %10s"%("Syst", "Down", "Base", "Up", "Unc"))
print("%10s %6s %8s %8s %6s %8s %8s %6s %8s %8s %5s"%("", 
"UnderF", "Int", "OverF", 
"UnderF", "Int", "OverF", 
"UnderF", "Int", "OverF", ""))
def checkNanInBins(hist):
    checkNan = False
    for b in range(hist.GetNbinsX()):
        if math.isnan(hist.GetBinContent(b)):
            print "%s: bin %s is nan"%(hist.GetName(), b)
            checkNan = True
    return checkNan
            
histDict = {}
sfDict = {}
allSystPercentage = {}
for key in systDict.keys():
    for index, syst in enumerate(systDict[key]):
        hPathBase   = "%s/%s/1_base/%s"%(sample, region, hName)
        hPathNom    = "%s/%s/%s_base/%s"%(sample, region, syst, hName)
        hPathUp     = "%s/%s/%s_up/%s"%(sample, region, syst, hName)
        hPathDown   = "%s/%s/%s_down/%s"%(sample, region, syst, hName)
        print(hPathBase)
        hBase = rootFile.Get(hPathBase).Clone("Base_")
        hNom   = rootFile.Get(hPathNom).Clone("%sNom_"%syst) 
        hUp   = rootFile.Get(hPathUp).Clone("%sUp_"%syst) 
        hDown = rootFile.Get(hPathDown).Clone("%sDown_"%syst) 
        evtBase = hBase.Integral()
        evtNom = hNom.Integral()
        evtUp   = hUp.Integral()
        evtDown = hDown.Integral()
        #check if intergal is 0
        #if evtUp ==0.0 or evtBase ==0.0 or evtDown ==0.0:
        #i = integral, u = undeflow, o = overflow
        iEvtBase = round(hBase.Integral(),0)
        iEvtNom = round(hNom.Integral(),0)
        iEvtUp   = round(hUp.Integral(),0)
        iEvtDown = round(hDown.Integral(),0)
        uEvtBase = round(hBase.GetBinContent(0),0)
        uEvtNom = round(hNom.GetBinContent(0),0)
        uEvtUp   = round(hUp.GetBinContent(0),0)
        uEvtDown = round(hDown.GetBinContent(0),0)
        oEvtBase = round(hBase.GetBinContent(hBase.GetNbinsX()+1),0)
        oEvtNom = round(hNom.GetBinContent(hNom.GetNbinsX()+1),0)
        oEvtUp   = round(hUp.GetBinContent(hUp.GetNbinsX()+1),0)
        oEvtDown = round(hDown.GetBinContent(hDown.GetNbinsX()+1),0)
        if uEvtBase >1000 or oEvtBase >1000:
            print "%s: Base:  Overflow or Undeflow is more than 1000"%syst
        if uEvtNom >1000 or oEvtNom >1000:
            print "%s: Nom:  Overflow or Undeflow is more than 1000"%syst
        if uEvtUp >1000 or oEvtUp >1000:
            print "%s: Up:  Overflow or Undeflow is more than 1000"%syst
        if uEvtDown >1000 or oEvtDown >1000:
            print "%s: Down:  Overflow or Undeflow is more than 1000"%syst
        if evtBase ==0.0:
            print "evtBase is zero"
            continue
        #check if intergal is NaN
        if math.isnan(evtUp) or math.isnan(evtDown):
            print "Inegral is nan"
            continue
        #check if bins are nan
        if checkNanInBins(hUp) or checkNanInBins(hBase) or checkNanInBins(hDown):
            print "Some of the bins are nan"
            continue
        allSystPercentage[syst] = 100*max(abs(evtUp -evtBase),abs(evtBase-evtDown))/evtBase
        print("%10s" 
               "|%6.0f %8.0f %8.0f"
               "|%6.0f %8.0f %8.0f"
               "|%6.0f %8.0f %8.0f"
               "|%5.0f%%"%(syst, 
             uEvtDown, iEvtDown, oEvtDown, 
             uEvtBase, iEvtBase, oEvtBase, 
             uEvtUp, iEvtUp, oEvtUp,
            allSystPercentage[syst]))
        if allSystPercentage[syst] > 100.0:
            print "Large uncertainty for %s: %10.2f"%(syst, allSystPercentage[syst])
        #Ratio Up
        hRatioUp = hUp.Clone("%s_up"%syst)
        hRatioNom = hNom.Clone("%s_base"%syst)
        hRatioDown = hDown.Clone("%s_down"%syst)
        hRatioUp.Divide(hBase)
        hRatioNom.Divide(hBase)
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
        decoHistRatio(hRatioNom, hName, syst, 1)
        decoHistRatio(hRatioDown, hName, syst, 8)
        hRatioUp.SetLineWidth(1)
        hRatioNom.SetLineWidth(1)
        hRatioDown.SetLineWidth(1)
        hRatioUp.SetLineStyle(index+1)
        hRatioNom.SetLineStyle(index+1)
        hRatioDown.SetLineStyle(index+1)
        histDict[syst] = [hRatioUp, hRatioNom, hRatioDown]
        sfDict[syst] = [iEvtUp/iEvtBase, iEvtNom/iEvtBase, iEvtDown/iEvtBase]

nSyst = len(systDict.keys())
canvas = TCanvas("sfRatio", "sfRatio", 300, 100*nSyst)
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
for i, key in enumerate(systDict.keys()):
    canvas.cd(i+1)
    gPad.SetPad(xPadRange[0],yPadRange[i],xPadRange[1],yPadRange[i+1]);
    #gPad.SetLogy(True);
    if(i+1==nSyst):
        gPad.SetBottomMargin(0.17)
    else:
        gPad.SetBottomMargin(0.0)
    #Draw Leg
    leg = TLegend(0.20,0.15,0.93,0.45)
    decoLegend(leg, 5, 0.09)
    leg.SetNColumns(3)
    for k, syst in enumerate(systDict[key]):
        for j, h in enumerate(histDict[syst]):
            h.GetYaxis().SetTitle(key)
            h.GetYaxis().SetRangeUser(0.5, 1.5)
            sysName = "%s %s"%(syst.split("_")[-1], h.GetName().split("_")[-1])
            legName = "%s=%s"%(sysName, round(sfDict[syst][j],3))
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

lumi_13TeV = "35.9 fb^{-1}"
col_year = rt.kGreen 
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
chColor = 1
col_depth = 0
if channel in ["mu", "Mu", "m"]:
    chColor = rt.kCyan+col_depth
    chName = "1#color[%i]{#mu}, p_{T}^{miss} #geq 20"%chColor
else:
    chColor = rt.kPink+col_depth
    chName = "1#color[%i]{e}, p_{T}^{miss} #geq 20"%chColor
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

#canvas.SaveAs("%s/%s_%s_%s.png"%(outPlotFullDir, hName, year, channel))
canvas.SaveAs("%s/SystRatio_%s_%s_%s_%s.pdf"%(outPlotFullDir, hName, year, channel, sample))
