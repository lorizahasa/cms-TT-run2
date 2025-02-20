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
import numpy as np

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

rList = list(Regions.keys())
#-----------------------------------------
# Collect all syst 
#----------------------------------------
sysList = systVar
sysList.append("JetBase")
if isCheck:
    isSep  = False
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
    Spin = [Spin[0]]
    Samples = ["TTGamma"]
    rList   = [rList[0]]
    sysList = [sysList[0]]
if isComb:
    isSep = False
    Years = Years_
    Channels = Channels_
if isSep: 
    isComb = False
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
    # Function to fill empty regular bins with 1e-8

    def fillEmptyBins(hist, fill_value=1e-9):
        # Iterate over regular bins only (from 1 to N)
        for bin in range(0, hist.GetNbinsX() + 1):
            content = hist.GetBinContent(bin)
            if content <= 0: #Fill bin if 0 or negative
                hist.SetBinContent(bin, fill_value)
                hist.SetBinError(bin, fill_value)
                print(f"Replaced bin {bin} in histogram {hist.GetName()} with {fill_value} (original content: {content})")
                      # if hist.GetBinContent(bin) == 0:
           #     hist.SetBinContent(bin, fill_value)
           #     print(f"Filled bin {bin} in histogram {hist.GetName()} with {fill_value}")

    if hName in dictRebin.keys():
        hNew = hist_.Rebin(len(dictRebin[hName])-1, hist_.GetName(), dictRebin[hName]) 
        # Check and fill empty regular bins in the rebinned histogram
        #fillEmptyBins(hNew, fill_value=1e-9)
        hNew.Write()
        #print(hName)
        #print(dictRebin[hName])
    else:
        # If not rebinned, check and fill empty regular bins in the original histogram
        #fillEmptyBins(hist_, fill_value=1e-9)
        hist_.Write()
    outputFile.cd()

#-----------------------------------------
# Do the rebining here
#----------------------------------------
for year, decay, spin, channel  in itertools.product(Years, Decays, Spin, Channels):
    inDir = "%s/Merged/%s/%s/%s/%s/CombMass/BDTA"%(dirRead, year, decay, spin, channel)
    inFile = TFile.Open("root://cmseos.fnal.gov/%s/AllInc.root"%inDir, "read")
    outDir = inDir.replace("Merged", "Rebin")
    print(outDir)
    #os.system("eos root://cmseos.fnal.gov rm -r %s"%outDir)
    #os.system("eos root://cmseos.fnal.gov mkdir -p %s"%outDir)
    os.system("rm -r /eos/uscms/%s"%outDir)
    os.system("mkdir -p /eos/uscms/%s"%outDir)
    outputFile = TFile("/eos/uscms/%s/AllInc.root"%outDir,"update")
    for r in rList:
        print("==> %s, %s, %s, %s"%(year, decay, channel, r))
        hists = list(GetVarInfo(r, channel).keys())
        hists.append('Disc')
        if isCheck:
            print(inFile)
        hists = ["Disc", "Reco_mass_T"]
        if isComb:
            split_year = year.split("__")
            syst_Comb = []
            for y in split_year:
                syst_Comb.append(systVar_by_year[y])    
            sysList = list(np.unique(syst_Comb))            
        else:    
            sysList = systVar_by_year[year]
        sysList.append("JetBase")
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

            if "2016" in syst:
                syst = syst.replace("2016", "%s"%year)
            if "JER" in syst:
                syst = syst.replace("JER", "JER_%s"%year)    

            writeHist(s, r, syst, h4, outputFile)
            if "MisID_" in r and "mass_lgamma" in h:
                if "data_obs" in s:
                    continue
                for cat in phoCat.keys():
                    newName = "%s_%s"%(h, cat)
                    hNew = inFile.Get("%s/%s"%(histDir, newName))
                    writeHist(s, r, syst, hNew, outputFile)
    #print(outputFile.ls())
    outputFile.Close()
    print("/eos/uscms/%s/AllInc.root\n"%outDir)
