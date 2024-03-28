import os
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor_read", ""))
import itertools
from DiscInputs import *
from HistRebins import dictRebin
from optparse import OptionParser
from VarInfo import GetVarInfo
from ROOT import TFile, TH1F, gDirectory

#----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Merge for combined years and channels")
parser.add_option("--isSep","--isSep", dest="isSep",action="store_true",default=False, help="Merge for separate years and channels")
parser.add_option("--isComb","--isComb", dest="isMerge",action="store_true",default=False, help="Merge for combined years and channels")
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep = options.isSep
isComb = options.isMerge

rList = list(Regions.keys())
#-----------------------------------------
# Collect all syst 
#----------------------------------------
sysList = systVar
sysList.append("Base")
if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
    #Samples = [Samples[0]]
    Samples = ["TTGamma"]
    rList   = [rList[0]]
    sysList = [sysList[0]]
if isSep: 
    isComb = False
if isComb:
    isSep = False
    Years = Years_
    Channels = Channels_
if not isCheck and not isSep and not isComb:
    print("Add either --isCheck or --isSep or --isComb in the command line")
    exit()

#-----------------------------------------
#Functions to read/write histograms
#----------------------------------------
def addHist(histList, name):
    if len(histList) ==0:
        print("Hist list | %s, %s | is empty"%(histList, name))
        sys.exit()
    else:
        hist = histList[0].Clone(name)
        hist.Reset()
        for h in histList:
            hist.Add(h)
        return hist

def getHistDir(sample, CR, sysType):
    histDir = "%s/%s/%s"%(sample, CR, sysType)
    return histDir

def writeHist(sample, CR, sysType, hist_, outputFile):
    outHistDir = getHistDir(sample, CR, sysType)
    if not outputFile.GetDirectory(outHistDir):
        outputFile.mkdir(outHistDir)
    #print(gDirectory.ls())
    outputFile.cd(outHistDir)
    hName = hist_.GetName() if hist_ is not None else None
    if hName is not None:
        gDirectory.Delete("%s;*"%(hName))
    else:
        print("Error: hist_ is null. Skipping deletion")
    #print("%10s :/%s/%s/%s/%s"%(round(hist_.Integral(), 1), sample, CR, sysType, hist_.GetName()))
    if hName in dictRebin.keys():
        hNew = hist_.Rebin(len(dictRebin[hName])-1, hist_.GetName(), dictRebin[hName]) 
        hNew.Write()
    else:
        hist_.Write()
    outputFile.cd()

#-----------------------------------------
# Do the rebining here
#----------------------------------------
for year, decay, channel, r in itertools.product(Years, Decays, Channels, rList):
    inDir = "%s/Merged/%s/%s/%s/CombMass/BDTA"%(dirRead, year, decay, channel)
    inFile = TFile.Open("root://cmseos.fnal.gov/%s/AllInc.root"%inDir, "read")
    outDir = inDir.replace("Merged", "Rebin")
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%outDir)
    outputFile = TFile("/eos/uscms/%s/AllInc.root"%outDir,"update")
    print("==> %s, %s, %s, %s"%(year, decay, channel, r))
    hists = list(GetVarInfo(r, channel).keys())
    hists.append('Disc')
    if isCheck:
        print(inFile)
        hists = ["Disc", "Reco_mass_T"]
    hists = ["Reco_mass_T"]
    for s, h, syst, in itertools.product(Samples, hists, sysList):
        if "data_obs" in s and "Base" not in syst:
            continue
        if "JE" in syst:
            syst = syst.replace("_up", "Up")
            syst = syst.replace("_down", "Down")
        if isCheck:
            print("%s, %s, %s, %s"%(s, r, syst, h))
        histDir = getHistDir(s, r, syst)
        print(histDir, h)
        h4 = inFile.Get("%s/%s"%(histDir, h))
        writeHist(s, r, syst, h4, outputFile)
        if "MisID_" in r and "mass_lgamma" in h:
            if "data_obs" in s:
                continue
            for cat in phoCat.keys():
                newName = "%s_%s"%(h, cat)
                hNew = inFile.Get("%s/%s"%(histDir, newName))
                writeHist(s, r, syst, hNew, outputFile)
    outputFile.Close()
    print("/eos/uscms/%s/AllInc.root\n"%outDir)
