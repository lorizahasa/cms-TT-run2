import os
import sys
import math
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor_read", ""))
import itertools
from DiscInputs import *
from optparse import OptionParser
from VarInfo import GetVarInfo
from ROOT import TFile, TH1F, gDirectory
import numpy as np

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
sysList.append("JetBase")
if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Spin  = [Spin[0]]
    Channels = [Channels[0]]
    rList   = [rList[0]]
    sysList = [sysList[0], 'Weight_pdfUp', 'JERUp']
if isSep: 
    isComb = False
if isComb:
    isSep = False
    Years = Years_
    Channels = Channels_

#    split_year = year.split("__")
    # union of systs over eras
#    base = []
#    for y in split_year:
#        base.extend(systVar_by_year[y])

    # expand per-era names for JER and JEC 2016*
#    expanded = []
#    for s in base:
#        sN = s.replace("_up","Up").replace("_down","Down")

#        if sN.startswith("JER"):
            # JERUp -> JER_<era>Up for each era
#            for y in split_year:
#                expanded.append(sN.replace("JER", f"JER_{y}"))

#        elif ("JE" in sN) and ("2016" in sN):
            # Only 2016 eras get injected (Pre/Post)
#            for y in split_year:
#                if y.startswith("2016"):
#                    expanded.append(sN.replace("2016", y))

#        else:
#            expanded.append(sN)

    # de-dup while preserving order
#    sysList = list(dict.fromkeys(expanded))
#else:
#    sysList = systVar_by_year[year]
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
        sanitize_hist(hist, eps=1e-9)    
        return hist

def getHist(inFile, hPath, hName):
    hPath_ = "%s/%s"%(hPath, hName)
    try:
        hist = inFile.Get(hPath_)
        hist = hist.Clone(hName)
        sanitize_hist(hist, eps=1e-9)
    except Exception:
        print ("Error: Hist not found. \nFile: %s \nHistName: %s"%(inFile, hPath_))
        sys.exit()
    return hist

#def getHistOther(inFile, reg, syst, hName):
def getHistOther(inFile, year, reg, syst, hName):
    hList = []
    for s in Samples:
        if ("Signal" in s) or ("data_obs" in s) or ("TTGamma" in s): 
            continue
        #if "QCD" in s or "data" in s:
           # s = f"{s}{channel}"
        hPath = "%s/%s/%s"%(s, reg, syst)
        hList.append(getHist(inFile, hPath, hName))
    return addHist(hList, hName)

def writeHist(outFile, hPath, hist):
    sanitize_hist(hist, eps=1e-9)
    if not outFile.GetDirectory(hPath):
        outFile.mkdir(hPath)
    outFile.cd(hPath)
    gDirectory.Delete("%s;*"%(hist.GetName()))
    if isCheck:
        print("%60s, %20s, %10s"%(hPath, hist.GetName(), round(hist.Integral())))
    hist.Write()

def sanitize_hist(hist, eps=1e-9):
    if not hist:
        return
    if hist.GetSumw2N() == 0:
        hist.Sumw2()

    n = hist.GetNbinsX()
    for b in range(0, n + 2):
        c = hist.GetBinContent(b)
        e = hist.GetBinError(b)

        if (not math.isfinite(c)) or (c <= 0.0):
            c = eps
            hist.SetBinContent(b, c)

        if (not math.isfinite(e)) or (e <= 0.0):
            e = max(eps, math.sqrt(c) * 1e-6)
            hist.SetBinError(b, e)
#-----------------------------------------
# Do the rebining here
#----------------------------------------
for year, decay, spin,  channel, r in itertools.product(Years, Decays, Spin, Channels, rList):
    #inDir = "%s/Paper_AdjustForMain_Paper/%s/%s/%s/%s/CombMass/BDTA"%(dirRead, year, decay, spin, channel) #SR remove Paper for normal
    inDir = "%s/AdjustForMain/%s/%s/%s/%s/CombMass/BDTA"%(dirRead, year, decay, spin, channel) #SR remove Paper for normal
    #inDir = "%s/AdjustForMain/%s/%s/%s/%s/CR/CombMass/BDTA"%(dirRead, year, decay, spin, channel) #CR
    #inDir = "%s/Rebin/%s/%s/%s/%s/CombMass/BDTA"%(dirRead, year, decay,spin, channel)

    inFile = TFile.Open("root://cmseos.fnal.gov/%s/AllInc.root"%inDir, "read")
    outDir = inDir.replace("AdjustForMain", "ForMain")#Paper 
    #outDir = inDir.replace("Paper_AdjustForMain_Paper", "ForMain_Paper")#Paper 
    #outDir = inDir.replace("Rebin", "ForMain")
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%outDir)
    outFile = TFile("/eos/uscms/%s/AllInc.root"%outDir,"update")
    print("==> %s, %s, %s, %s"%(year, decay, channel, r))
   # hList = list(GetVarInfo(r, channel).keys())
    hList = []
    hList.append('Disc')
    #hList.append('Reco_mass_T')
    if isCheck:
        print(inFile)
        hList = ['Disc']
    if isComb:
        split_year = year.split("__")
        syst_Comb = []
        for y in split_year:
            syst_Comb.append(systVar_by_year[y]) 
        sysList = list(np.unique(syst_Comb))
    else:
        sysList = systVar_by_year[year]
    sysList.append("JetBase")
    for syst, hName in itertools.product(sysList, hList):
        print(syst, hName)
        if "JE" in syst:
            syst = syst.replace("_up", "Up")
            syst = syst.replace("_down", "Down")
            if "2016" in syst:
                syst = syst.replace("2016", "%s"%year)
        if "JER" in syst:
            syst = syst.replace("JER", "JER_%s"%year)
            #if isComb: FIX
        #Signal and TTGamma
        for sample in Samples:
            #if "QCD" in sample or "data" in sample:
               # sample =f"{sample}{channel}"
            if "Signal" in sample or 'TTGamma' in sample:
                hPath = "%s/%s/%s"%(sample, r, syst)
                if syst in systToNorm:
                    h = getHist(inFile, hPath, hName)
                    hPath_ = "%s/%s/%s"%(sample, r, "JetBase")
                    h_ = getHist(inFile, hPath_, hName)
                    sysInt  = h.Integral()
                    if sysInt ==0 or math.isnan(sysInt):
                        print(year, channel, sample, r, syst, sysInt)
                    else:
                        h.Scale(h_.Integral()/sysInt)
                    sanitize_hist(h, eps=1e-9)    
                    writeHist(outFile,  hPath, h)
                else:
                    h = getHist(inFile, hPath, hName)
                    writeHist(outFile,  hPath, h)

        #OtherBkgs
        hPath = "%s/%s/%s"%("OtherBkgs", r, syst)
        if syst in systToNorm:
            #h = getHistOther(inFile, year, channel, r, syst, hName)
            h = getHistOther(inFile, year, r, syst, hName)
            hPath_ = "%s/%s/%s"%("OtherBkgs", r, "JetBase")
            #h_ = getHistOther(inFile, year, channel, r, "JetBase", hName)
            h_ = getHistOther(inFile, year, r, "JetBase", hName)
            sysInt  = h.Integral()
            if sysInt ==0 or math.isnan(sysInt):
                print(year, channel, sample, r, syst, sysInt)
            else:
                h.Scale(h_.Integral()/sysInt)
            sanitize_hist(h, eps=1e-9)    
            writeHist(outFile,  hPath, h)
        else:
            #h = getHistOther(inFile, year, channel, r, syst, hName)
            h = getHistOther(inFile, year, r, syst, hName)
            writeHist(outFile,  hPath, h)
        #writeHist(outFile, hPath, getHistOther(inFile, r, syst, hName))
        #data_obs for base
        if "Base" in syst:
            #hPath = "%s%s/%s/%s"%("data_obs",channel, r, syst)
            hPath = "%s/%s/%s"%("data_obs", r, syst)
            writeHist(outFile,  hPath, getHist(inFile, hPath, hName))
    outFile.Close()
    print("/eos/uscms/%s/AllInc.root\n"%outDir)
