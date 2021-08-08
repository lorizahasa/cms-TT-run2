from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors
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
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
		  help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="TTbar",type='str',
		  help="name of the MC sample" )
parser.add_option("--ps", "--phaseSpace", dest="phaseSpace", default="Boosted_SR",type='str', 
                     help="which control selection and region")
parser.add_option("--plot", "--plot", dest="hName", default="Weight_lumi",type='str', 
                     help="name of the histogram")
(options, args) = parser.parse_args()
year            = options.year
decayMode       = options.decayMode
channel         = options.channel
sample          = options.sample
hName            = options.hName
phaseSpace = options.phaseSpace
def checkNanInBins(hist):
    checkNan = False
    for b in range(hist.GetNbinsX()):
        if math.isnan(hist.GetBinContent(b)):
            print "%s: bin %s is nan"%(hist.GetName(), b)
            checkNan = True
    return checkNan
#-----------------------------------------
#Get histograms
#----------------------------------------
print("%10s %6s %8s %8s %6s %8s %8s %6s %8s %8s %5s"%("", 
"UnderF", "Int", "OverF", 
"UnderF", "Int", "OverF", 
"UnderF", "Int", "OverF", ""))
weights = {}
for s in SampleLumi.keys():
    weight = []
    for y in ["2016", "2017", "2018"]:
        sample = s
        year = y
        inHistSubDir = "%s/%s/%s/Merged"%(year, decayMode, channel)
        inHistFullDir = "%s/Hist_Ntuple/%s"%(condorHistDir, inHistSubDir)
        outPlotSubDir = "Plot_Hist/%s/Syst/%s/%s/%s"%(year, decayMode, channel, phaseSpace)
        outPlotFullDir = "%s/%s"%(condorHistDir, outPlotSubDir)
        if not os.path.exists(outPlotFullDir):
            os.makedirs(outPlotFullDir)
        rootFile = TFile("%s/AllInc.root"%(inHistFullDir), "read")
        print rootFile
        hPathBase = "%s/%s/Base/%s"%(sample, phaseSpace, hName)
        hBase = rootFile.Get(hPathBase).Clone("Base_")
        #-----------------------------------------
        # Sanity checks
        #----------------------------------------
        #check if intergal is 0
        #i = integral, u = undeflow, o = overflow
        iEvtBase = round(hBase.Integral(),0)
        uEvtBase = round(hBase.GetBinContent(0),0)
        oEvtBase = round(hBase.GetBinContent(hBase.GetNbinsX()+1),0)
        weight.append(hBase.GetMean())
    weights[sample] = weight

xArray = numpy.array([2016.,2017.,2018.])
graphs = {}
print weights
col = 0
for key in weights.keys():
    col+=1
    yArray = numpy.array(weights[key])
    graph = rt.TGraph(len(xArray), xArray, yArray)
    graph.GetYaxis().SetTitle("Luminosity weight")
    graph.GetXaxis().SetTitle("Year of data taking")
    graph.SetLineColor(SampleBkg[key][0])
    graph.SetMarkerColor(SampleBkg[key][0]) 
    graph.SetMarkerStyle(col)
    graph.SetMarkerSize(2)
    #graph.SetMarkerStyle(SampleBkg[key][0]) 
    graph.SetLineWidth(4)
    graphs[key] = graph

#-----------------------------------------
# Draw graphs 
#----------------------------------------
gROOT.SetBatch(True)
canvas = TCanvas()
canvas.cd()
gPad.SetRightMargin(0.30);
#gPad.SetPad(xPadRange[0],yPadRange[2],xPadRange[1],yPadRange[3]);
gPad.SetTopMargin(0.09);
#gPad.SetBottomMargin(padGap);
#gPad.SetTickx(0);
gPad.RedrawAxis();
#gPad.SetLogy(True)
print graphs
leg = TLegend(0.70,0.15,1.0,0.75)
decoLegend(leg, 5, 0.034)
list_ = []
for vals in weights.values():
    list_.extend(vals)
for index, name in enumerate(graphs.keys()):
    graph_ = graphs[name]
    #graph_.GetYaxis().SetRangeUser(0.1*min(list_), 100*max(list_))
    graph_.GetYaxis().SetRangeUser(0.1*min(list_), 1.1*max(list_))
    graph_.GetXaxis().SetNdivisions(3)
    if index ==0:
        graph_.Draw("ALP")
    else:
        graph_.Draw("LPsame")
    leg.AddEntry(graph_, name, "EPL")
leg.Draw("same")

#Draw CMS, Lumi, channel
lumi_13TeV = ""
if channel in ["mu", "Mu", "m"]:
    chName = "1 #color[2]{#mu}"
else:
    chName = "1 #color[6]{e}"
chCRName = "%s"%chName
extraText   = "#splitline{Preliminary}{%s}"%chCRName
#CMS_lumi(canvas, iPeriod, iPosX, extraText)
CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
canvas.SaveAs("%s/%s_%s.pdf"%(outPlotFullDir, hName, channel))
#canvas.SaveAs("SystRatio_%s_%s_%s_%s_%s_%s.pdf"%(year, decayMode, channel, hName, sample, phaseSpace))
