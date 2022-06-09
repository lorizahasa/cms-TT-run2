#!/usr/bin/env python
from ROOT import gROOT, TGraph, TCanvas, TLegend, gPad
import os
import sys
sys.path.insert(0, os.getcwd().replace("condor", ""))
sys.path.insert(0, os.getcwd().replace("Fit_Disc/condor", "Disc_Ntuple"))
sys.path.insert(0, os.getcwd().replace("MVA_Ntuple/Fit_Disc/condor", "CBA_Ntuple/Plot_Hist"))
import json
import itertools
from PlotCMSLumi import *
from PlotTDRStyle import *
from PlotFunc import *
from array import array
from FitInputs import *
from optparse import OptionParser
from DiscInputs import methodDict
import pandas as pd

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
parser.add_option("--byCR","--byCR",dest="byCR", default=False, action="store_true",
		  help="run FitDiabnostics")
parser.add_option("--byVar","--byVar",dest="byVar", default=False, action="store_true",
		  help="run FitDiabnostics")
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep = options.isSep
byCR           = options.byCR
byVar           = options.byVar
gROOT.SetBatch(True)

if isCheck:
    Year  = [Year[0]]
    Decay = [Decay[0]]
    Channel = [Channel[0]]
    regionList  = [regionList[0]]
if not isCheck and not isSep:
    print("Add either --isCheck or --isSep in the command line")
    exit()

def getLimit(jsonFile, exp, m):
    with open(jsonFile) as jsonFile_:
        jsonData = json.load(jsonFile_)
        paramDict   = jsonData[m]
        lim = 1.0
        for key, val in paramDict.iteritems():
            if exp==key:
                lim= val
        return lim

def roundMe(value, place):
    upStr = '{:.%sf}'%place
    upVal = round(value, place)
    final = upStr.format(upVal)
    return final

#----------------------------------------
#Path of the I/O histrograms/plots
#----------------------------------------
fPath = open("%s/compareLimit.txt"%dirFit, 'w')
for decay, region, channel, year in itertools.product(Decay, regionList, Channel, Year):
    limits = "tex/allLimits.json"
    gDict = {}
    limDict={}
    ydc = "%s/%s/%s"%(year, decay, channel)
    path = "%s/%s"%(dirFit, ydc) 
    outPath = "%s/%s"%(path, region)
    os.system('mkdir -p %s'%outPath)
    for h in histList:
        x = array( 'd' )
        y = array( 'd' )
        for m in xss.keys():
            x.append(float(m))
            limFile      = "%s/%s/%s/%s/%s/limits.json"%(path, int(float(m)), "BDTA", region, h)
            print(limFile)
            #print(limFile)
            y.append(float(xss[m]*getLimit(limFile, "exp0", m)))
        graph = TGraph(len(x), x, y)
        gDict[h] = graph
        limDict["mT"] = x
        limDict[h] = y

    for method in methodDict.keys():
        x = array( 'd' )
        y = array( 'd' )
        for m in xss.keys():
            x.append(float(m))
            limFile      = "%s/%s/%s/%s/%s/limits.json"%(path, int(float(m)), method, region, "Disc")
            #print(limFile)
            y.append(float(xss[m]*getLimit(limFile, "exp0", m)))
        graph = TGraph(len(x), x, y)
        gDict[method] = graph
        limDict["mT"] = x
        limDict[method] = y

    print limDict
    df = pd.DataFrame.from_dict(limDict)
    print(df)
    roundDict = {}
    roundBy = 1
    for m in methodDict.keys():
        df[m] =100*(df[m] - df['Reco_mass_T'])/df['Reco_mass_T']
        roundDict[m] = roundBy
    for h in histList:
        if "Reco_mass_T" not in h:
            df[h] =100*(df[h] - df['Reco_mass_T'])/df['Reco_mass_T']
            roundDict[h] = roundBy
    df.set_index(['mT', 'Reco_mass_T'], inplace=True)
    #df.rename(columns={"BDTA": "BDTA (%)"}, inplace=True)
    print df.round(roundDict)

    canvas = TCanvas()
    legend = TLegend(0.70,0.60,0.85,0.90);
    legend.SetFillStyle(0);
    legend.SetBorderSize(0);
    legend.SetTextFont(42);
    legend.SetTextAngle(0);
    legend.SetTextSize(0.035);
    legend.SetTextAlign(12);
    canvas.cd()
    gPad.SetLogy(True)
    maxInt = 0.0;
    for index, s in enumerate(gDict.keys()):
        if index==9: index=10
        gDict[s].SetLineColor(index+1)
        gDict[s].SetLineWidth(3)
        gDict[s].SetMarkerStyle(20+index);
        gDict[s].SetMarkerColor(index+1);
        gDict[s].GetYaxis().SetTitle("#sigma_{TT} B(T #rightarrow t#gamma)B(T #rightarrow tg) [pb]")
        gDict[s].GetYaxis().SetLabelSize(.035)
        gDict[s].GetXaxis().SetLabelSize(.035)
        gDict[s].GetXaxis().SetTitle("m_{T} (GeV)")
        gDict[s].Draw("P")
        if index==0:
            gDict[s].SetMaximum(1)
            if "Boosted" in region:
                pass
                #gDict[s].SetMaximum(0.04)
            gDict[s].SetMinimum(0.001)
            gDict[s].Draw()
        else:
            gDict[s].Draw("same")
        #legName = "%s, mean = %i, int = %i"%(econDict[s][1], gDict[s].GetMean(), gDict[s].Integral())
        legend.AddEntry(gDict[s], s,  "LP")
        canvas.Update()
        
    #Theory
    x, y = array( 'd' ), array( 'd' )
    for m in xss.keys():
        x.append(float(m))
        y.append(xss[m])
    gTheory = TGraph(len(x), x, y)
    gTheory.SetLineColor(7)
    gTheory.SetLineWidth(3)
    gTheory.SetMarkerStyle(15);
    gTheory.SetMarkerColor(7);
    gTheory.Draw("Lsame")
    legend.AddEntry(gTheory, "Theory", "L")
    legend.Draw()
    #---------------------------
    #Draw CMS, Lumi, channel
    #---------------------------
    chName = getChLabel(decay, channel)
    #chName = "#splitline{%s}{%s}"%(chName, region)
    chName = "%s, #bf{%s}"%(chName, region)
    crName = region 
    #chCRName = "#splitline{#font[42]{%s}}{#font[42]{(%s)}}"%(chName, crName)
    chCRName = "#splitline{#font[42]{%s}}{#font[42]{%s}}"%(chName, "95% CL expected upper limit")
    extraText   = "#splitline{Preliminary}{%s}"%chCRName
    lumi_13TeV = getLumiLabel(year)
    CMS_lumi(lumi_13TeV, canvas, iPeriod, iPosX, extraText)
    #canvas.SaveAs("tex/limit.pdf"%(""))
    if byVar:
        name = "byVar"
    elif byCR:
        name = "byCR"
    else:
        name = "by"
    pdf = "%s/compareLimit.pdf"%(outPath)
    canvas.SaveAs(pdf)
    fPath.write("%s\n"%pdf)
    latex = pdf.replace(".pdf", '.tex') 
    with open(latex, 'w') as f:
        table = "\\begin{minipage}[c]{0.32\\textwidth}\n"
        table += "\\centering\n"
        table += "\\tiny{\n"
        f.write(table)
        f.write(df.round(roundDict).to_latex())
        #print df.round(roundDict)
        table  = "}\n"
        table += "\\end{minipage}\n"
        f.write(table)
    print(latex)
    f.close()
print(fPath)
