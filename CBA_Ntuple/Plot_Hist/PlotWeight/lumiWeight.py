import os
import sys
sys.path.insert(0, os.getcwd().replace("PlotWeight", ""))
sys.dont_write_bytecode = True
import numpy
import itertools
from PlotInputs import *
from PlotFunc import *
from PlotCMSLumi import *
from PlotTDRStyle import *
from optparse import OptionParser
from ROOT import TFile, TLegend, gPad, TGraph, gROOT, TCanvas, TH1F

padGap = 0.01
iPeriod = 4;
iPosX = 10;
#setTDRStyle()
ModTDRStyle()
#ModTDRStyle(600, 300, 0.10, 0.12, 0.16, 0.04);
xPadRange = [0.0,1.0]
yPadRange = [0.0,0.30-padGap, 0.30+padGap,1.0]

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Merge for combined years and channels")
(options, args) = parser.parse_args()
isCheck = options.isCheck

Samples = sampDict.keys()
if isCheck:
    Years   = [Years[0]]
    Decays  = [Decays[0]]
    Channels= [Channels[0]]
    Samples = [sampDict.keys()[0]]


print("%25s %10s %10s %10s %10s"%("YDC", "Sample", "Integral", "Entry", "Weight"))
for decay, channel in itertools.product(Decays, Channels):
    weights = {}
    for sample in Samples:
        weight = []
        print("")
        for year in Years:
            ydc    = "%s/%s/%s"%(year, decay, channel)
            inDir  = "%s/%s"%(dirHist, ydc)
            outDir = dirPlot
            if not os.path.exists(outDir):
                os.makedirs(outDir)
            rootFile = TFile("%s/AllInc.root"%(inDir), "read")
            if isCheck:
                print(rootFile)
            hPathBase = "%s/%s/Weight_lumiBase/%s"%(sample, region, hName)
            hBase = rootFile.Get(hPathBase).Clone("Base_")
            #-----------------------------------------
            # Sanity checks
            #----------------------------------------
            #check if intergal is 0
            #i = integral, u = undeflow, o = overflow
            int_ = hBase.Integral()
            ent  = hBase.GetEntries() 
            uEvt = round(hBase.GetBinContent(0),0)
            oEvt = round(hBase.GetBinContent(hBase.GetNbinsX()+1),0)
            w = int_/ent
            weight.append(w)
            if uEvt > 0 or oEvt > 0:
                print("WE: Overflow for %s: %s, %s"%(sample, uEvt, oEvt))
            print("%25s %10s %10s %10s %10s"%(ydc, sample, round(int_, 3), ent, round(w, 5)))
        weights[sample] = weight

    xArray = numpy.array([2016., 2016.5, 2017.,2018.])
    graphs = []
    if isCheck:
        print(weights)
    col = 0
    for key in weights.keys():
        col+=1
        yArray = numpy.array(weights[key])
        graph = TGraph(len(xArray), xArray, yArray)
        graph.GetYaxis().SetTitle("Luminosity weight")
        graph.GetXaxis().SetTitle("Year of data taking")
        graph.SetLineColor(sampDict[key][0])
        graph.SetMarkerColor(sampDict[key][0]) 
        graph.SetMarkerStyle(col)
        graph.SetMarkerSize(2)
        #graph.SetMarkerStyle(sampDict[key][0]) 
        graph.SetLineWidth(4)
        graph.SetName(key)
        graphs.append(graph)

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
    gPad.SetLogy(True)
    if isCheck:
        print(graphs)
    leg = TLegend(0.70,0.15,1.0,0.75)
    decoLegend(leg, 5, 0.034)
    list_ = []
    for vals in weights.values():
        list_.extend(vals)
    
    graphs_ = sortGraphs(graphs)
    for index, graph_ in enumerate(graphs_):
        graph_.GetYaxis().SetRangeUser(0.1*min(list_), 100000*max(list_))
        #graph_.GetYaxis().SetRangeUser(0.1*min(list_), 1.1*max(list_))
        graph_.GetXaxis().SetNdivisions(3)
        if index ==0:
            graph_.Draw("ALP")
        else:
            graph_.Draw("LPsame")
        leg.AddEntry(graph_, graph_.GetName(), "EPL")
    leg.Draw("same")

    #Draw CMS, Lumi, channel
    lumi_13TeV = ""
    chName = getChLabel(decay, channel)
    extraText   = "#splitline{Preliminary}{#splitline{%s}{%s}}"%(chName, region)
    CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
    canvas.SaveAs("%s/lumiWeight_%s_%s.pdf"%(outDir, decay, channel))
