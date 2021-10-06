from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors
import os
import numpy
import sys
import math
sys.path.insert(0, os.getcwd().replace("Plot_Hist/PlotMain", "Hist_Ntuple/HistMain"))
from optparse import OptionParser
from PlotFunc import *
from PlotCMSLumi import *
from PlotTDRStyle import *
from HistInputs import Regions, Systematics, SystLevels

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
                     help="Specify which decayMode moded of ttbar SemiLep or DiLep? default is SemiLep")
parser.add_option("-c", "--channel", dest="channel", default="Ele",type='str',
		  help="Specify which channel Mu or Ele? default is Ele" )
parser.add_option("-s", "--sample", dest="sample", default="TTGamma",type='str',
		  help="name of the MC sample" )
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched_SR",type='str', 
                     help="which control selection and region"), 
parser.add_option("--hist", "--hist", dest="hName", default="Photon_et",type='str', 
                     help="which histogram to be plottted")
(options, args) = parser.parse_args()
year            = options.year
decayMode       = options.decayMode
channel         = options.channel
sample          = options.sample
region = options.region
hName           = options.hName

isRebin = False
print "------------------------------------"
print "%s, %s, %s, %s, %s"%(year, decayMode, channel, sample, hName)
print "------------------------------------"
#-----------------------------------------
#Path of the I/O histrograms/plots
#----------------------------------------
inHistSubDir = "Hist_Ntuple/HistMain/forMain/%s/%s/%s/Merged"%(year, decayMode, channel)
inHistFullDir = "%s/%s"%(condorHistDir, inHistSubDir)
outPlotSubDir = "Plot_Hist/PlotMain/forMain/%s/%s/%s/%s"%(year, decayMode, channel, region)
outPlotFullDir = "%s/%s"%(condorHistDir, outPlotSubDir)
if not os.path.exists(outPlotFullDir):
    os.makedirs(outPlotFullDir)

gROOT.SetBatch(True)
#canvas = TCanvas("ImpactOfSyst", "ImpactOfSyst", 1600, 1000)
canvas = TCanvas()
canvas.cd()
gPad.SetRightMargin(0.03);
gPad.SetTopMargin(0.09);
gPad.SetLeftMargin(0.15);
#gPad.SetBottomMargin(0.15);
#gPad.SetTickx(0);
#gPad.SetLogy(True);
gPad.RedrawAxis();
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
            
allHistUp = []
allHistDown = []
allSystPercentage = {}
print Systematics
for index, syst in enumerate(Systematics):
    hPathBase   = "%s/%s/Base/%s"%(sample, region, hName)
    hPathUp     = "%s/%s/%sUp/%s"%(sample, region, syst, hName)
    hPathDown   = "%s/%s/%sDown/%s"%(sample, region, syst, hName)
    #print hPathBase
    #print hPathUp
    hBase = rootFile.Get(hPathBase).Clone("Base_")
    hUp   = rootFile.Get(hPathUp).Clone("%sUp_"%syst) 
    hDown = rootFile.Get(hPathDown).Clone("%sDown_"%syst) 
    evtBase = hBase.Integral()
    evtUp   = hUp.Integral()
    evtDown = hDown.Integral()
    #check if intergal is 0
    #if evtUp ==0.0 or evtBase ==0.0 or evtDown ==0.0:
    #i = integral, u = undeflow, o = overflow
    iEvtBase = round(hBase.Integral(),0)
    iEvtUp   = round(hUp.Integral(),0)
    iEvtDown = round(hDown.Integral(),0)
    uEvtBase = round(hBase.GetBinContent(0),0)
    uEvtUp   = round(hUp.GetBinContent(0),0)
    uEvtDown = round(hDown.GetBinContent(0),0)
    oEvtBase = round(hBase.GetBinContent(hBase.GetNbinsX()+1),0)
    oEvtUp   = round(hUp.GetBinContent(hUp.GetNbinsX()+1),0)
    oEvtDown = round(hDown.GetBinContent(hDown.GetNbinsX()+1),0)
    if uEvtBase >1000 or oEvtBase >1000:
        print "%s: Base:  Overflow or Undeflow is more than 1000"%syst
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
    if isRebin:
        xAxis = hBase.GetXaxis()
        lowBinEdge = xAxis.GetBinLowEdge(1)
        upBinEdge = xAxis.GetBinUpEdge(hBase.GetNbinsX())
        #print lowBinEdge, upBinEdge
        newWidth = int((upBinEdge - lowBinEdge)/10)
        if int(newWidth) ==0: 
            newWidth = 1
        newBins = numpy.arange(lowBinEdge,upBinEdge,newWidth)
        newBins = numpy.concatenate([newBins, [upBinEdge]])
        hBase = hBase.Rebin(len(newBins)-1, "RebinnedBase", newBins)
        hUp = hUp.Rebin(len(newBins)-1, "RebinnedUp", newBins)
        hDown = hDown.Rebin(len(newBins)-1, "RebinnedDown", newBins)
    #Ratio Up
    hRatioUp = hUp.Clone(syst)
    hRatioUp.Divide(hBase)
    myColor = index+2
    if myColor >9:
        myColor = 32+index
    decoHistRatio(hRatioUp, hName, "#frac{Up}{Nom} (solid), #frac{Down}{Nom} (dashed)", myColor)
    hRatioUp.GetXaxis().SetTitleSize(0.045)
    hRatioUp.GetXaxis().SetLabelSize(0.045)
    hRatioUp.GetYaxis().SetTitleSize(0.045)
    hRatioUp.GetYaxis().SetLabelSize(0.045)
    #hRatioUp.GetYaxis().SetRangeUser(0.1, 2)
    hRatioUp.GetYaxis().SetTitleOffset(1.5)
    hRatioUp.GetXaxis().SetTitleOffset(1.2)
    hRatioUp.SetMarkerStyle(index)
    hRatioUp.SetLineWidth(2)
    #Ratio Down
    hRatioDown = hDown.Clone(syst)
    hRatioDown.Divide(hBase)
    decoHistRatio(hRatioDown, hName, "#frac{Up}{Nom} (solid), #frac{Down}{Nom} (dashed)", myColor)
    hRatioDown.SetLineStyle(2)
    hRatioDown.SetLineWidth(2)
    hRatioDown.SetMarkerStyle(index)
    allHistUp.append(hRatioUp)#Don't comment
    allHistDown.append(hRatioDown)#Don't comment

#Draw Leg
leg = TLegend(0.20,0.15,0.93,0.35)
decoLegend(leg, 5, 0.034)
leg.SetNColumns(3)
allHistUpSorted = sortHists(allHistUp, True)
maxRatio = []
for h in allHistUpSorted:
    ratio = []
    for i in range(h.GetNbinsX()):
        ratio.append(round(h.GetBinContent(i),2))
    maxRatio.append(max(ratio))
    #print h.GetName(), ratio
yMax = max(maxRatio)
print yMax
for i, h in enumerate(allHistUpSorted):
    h.GetYaxis().SetRangeUser(1-0.5*yMax, 1+0.5*yMax)
    systPercentage = int(round(allSystPercentage[h.GetName()]))
    legName = "%s (%s%%)"%(h.GetName().split("_")[1], str(systPercentage))
    leg.AddEntry(h, legName, "L")
    if(i==0):
        h.Draw("hist")
    else:
        h.Draw("hist same")
    allHistDown[i].Draw("hist same")
leg.Draw("same")

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
    chName = "2#color[%i]{#mu}, p_{T}^{miss} #geq 20"%chColor
else:
    chColor = rt.kPink+col_depth
    chName = "2#color[%i]{e}, p_{T}^{miss} #geq 20"%chColor
selName = formatCRString(region)
nBase = "#font[42]{%s (N=%s)}"%(sample, str(round(evtBase,2)))
#line1 = "Preliminary, %s, %s"%(chName, region)
line1 = "Preliminary, %s"%(chName)
line2 = selName
line3 = nBase
extraText = "#splitline{%s}{#splitline{%s}{%s}}"%(line1, line2, line3)

CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
#Draw Baseline
baseLine = TF1("baseLine","1", -100, 10000);
baseLine.SetLineColor(1);
baseLine.Draw("same");

#canvas.SaveAs("%s/%s_%s_%s.png"%(outPlotFullDir, hName, year, channel))
canvas.SaveAs("%s/SystRatio_%s_%s_%s_%s.pdf"%(outPlotFullDir, hName, year, channel, sample))
