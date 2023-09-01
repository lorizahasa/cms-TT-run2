import os
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("PlotWeight", "")) 
import itertools
import pandas as pd
from PlotInputs import *
from optparse import OptionParser
from ROOT import TFile, TLegend, gPad, gROOT, TCanvas, THStack, TF1, TH1F, TGraphAsymmErrors

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

def pMe(val, digit):#percent me
    v = 100*val
    r = round(v, digit)
    return("%s\\%s"%(r, "%"))

os.system("mkdir -p %s"%dirPlot)
olT     = open("%s/overlapTable.tex"%dirPlot, "w")
vetoT   = open("%s/vetoTable.tex"%dirPlot, "w")

olD      = {}
vetoD    = {}
allD     = {}

for samp in sampAll.keys():
    olL      = []
    maskL    = []
    hemL     = []
    allL     = []
    for channel, decay, year in itertools.product(Channels, Decays, Years):
        ydc = "%s/%s/%s"%(year, decay, channel)
        inHistFullDir  = "%s/%s"%(dirHist, ydc)
        outPlotFullDir = "%s/%s/%s"%(dirPlot, ydc, region)
        if not os.path.exists(outPlotFullDir):
            os.makedirs(outPlotFullDir)
        rootFile = TFile("%s/AllInc.root"%(inHistFullDir), "read")
        if isCheck: 
            print(rootFile)

        hCount = rootFile.Get("%s/%s/Uncorr/hCount"%(samp, region))
        nTot   = hCount.GetBinContent(1)
        nOL    = hCount.GetBinContent(2)
        nLumi  = hCount.GetBinContent(4)
        nHEM   = hCount.GetBinContent(3)
        allL.append([nTot, pMe(nOL/nTot, 2), pMe(nLumi/nTot, 2), pMe(nHEM/nTot, 2)])
        if "data" in samp:
            maskL.append(pMe(nLumi/nTot, 2))
            hemL.append(pMe(nHEM/nTot, 2))
        else:
            olL.append(pMe(nOL/nTot, 2))
    allD[samp] = allL
    if "data" in samp:
        vetoD["data_lumiMasked"]   = maskL
        vetoD["data_hemVeto"]      = hemL
    else:
        olD[samp]   = olL

allDF = pd.DataFrame.from_dict(allD)

olDF = pd.DataFrame.from_dict(olD)
#olT.write(olDF.T.to_latex(index=False, header=['Removed events (mu)', 'Removed events (e)']))
olT.write(olDF.T.style.to_latex())

vetoDF = pd.DataFrame.from_dict(vetoD)
#vetoT.write(vetoDF.T.to_latex(index=False, header=['Removed events(mu)', 'Removed events (e)']))
vetoT.write(vetoDF.T.style.to_latex())

print(olDF)
print(vetoDF)

print(olT)
print(vetoT)

