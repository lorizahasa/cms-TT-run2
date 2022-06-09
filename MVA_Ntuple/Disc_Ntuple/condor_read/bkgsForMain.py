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

rList = Regions.keys()


#-----------------------------------------
# Collect all syst 
#----------------------------------------
sysList = []
sysList.append("Base")
for syst, level in itertools.product(Systematics, SystLevels): 
    sysList.append("%s%s"%(syst, level))

if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
    rList   = [Regions.keys()[0]]
    sysList = [sysList[0], 'Weight_pdfUp', 'Weight_jesUp']
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
        print "Hist list | %s, %s | is empty"%(histList, name)
        sys.exit()
    else:
        hist = histList[0].Clone(name)
        hist.Reset()
        for h in histList:
            hist.Add(h)
        return hist

def getHist(inFile, hPath, hName):
    hPath_ = "%s/%s"%(hPath, hName)
    try:
        hist = inFile.Get(hPath_)
        hist = hist.Clone(hName)
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
        hPath = "%s/%s/%s"%(s, reg, syst)
        #-----------Remove me------------
        hTemp = getHist(inFile, hPath, hName)
        if "TTbar" in s:
            ttbarSF = 1+dictSFs[year][1]*25/100 #Assuming 25% misID in ttbar
            if isCheck:
                print(ttbarSF)
            hTemp.Scale(ttbarSF)
        hList.append(hTemp)
        #-------------------------------
        #hList.append(getHist(inFile, hPath, hName))
    return addHist(hList, hName)

def writeHist(outFile, hPath, hist):
    if not outFile.GetDirectory(hPath):
        outFile.mkdir(hPath)
    outFile.cd(hPath)
    gDirectory.Delete("%s;*"%(hist.GetName()))
    if isCheck:
        print "%60s, %20s, %10s"%(hPath, hist.GetName(), round(hist.Integral()))
    hist.Write()


#-----------------------------------------
# Do the rebining here
#----------------------------------------
for year, decay, channel, r in itertools.product(Years, Decays, Channels, rList):
    inDir = "%s/Rebin/%s/%s/%s/CombMass/BDTA"%(dirRead, year, decay, channel)
    inFile = TFile.Open("root://cmseos.fnal.gov/%s/AllInc.root"%inDir, "read")
    outDir = inDir.replace("Rebin", "ForMain")
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%outDir)
    outFile = TFile("/eos/uscms/%s/AllInc.root"%outDir,"update")
    print("==> %s, %s, %s, %s"%(year, decay, channel, r))
    hList = GetVarInfo(r, channel).keys()
    hList.append('Disc')
    if isCheck:
        print inFile
        hList = ['Disc']
    for syst, hName in itertools.product(sysList, hList):
        #Signal and TTGamma
        for sample in Samples:
            if "Signal" in sample or 'TTGamma' in sample:
                hPath = "%s/%s/%s"%(sample, r, syst)
                if syst in systToNorm:
                    h = getHist(inFile, hPath, hName)
                    hPath_ = "%s/%s/%s"%(sample, r, "Base")
                    h_ = getHist(inFile, hPath_, hName)
                    sysInt  = h.Integral()
                    if sysInt ==0 or math.isnan(sysInt):
                        print(year, channel, sample, r, syst, sysInt)
                    else:
                        h.Scale(h_.Integral()/sysInt)
                    writeHist(outFile,  hPath, h)
                else:
                    h = getHist(inFile, hPath, hName)
                    writeHist(outFile,  hPath, h)

        #OtherBkgs
        hPath = "%s/%s/%s"%("OtherBkgs", r, syst)
        if syst in systToNorm:
            h = getHistOther(inFile, year, r, syst, hName)
            hPath_ = "%s/%s/%s"%("OtherBkgs", r, "Base")
            h_ = getHistOther(inFile, year, r, "Base", hName)
            sysInt  = h.Integral()
            if sysInt ==0 or math.isnan(sysInt):
                print(year, channel, sample, r, syst, sysInt)
            else:
                h.Scale(h_.Integral()/sysInt)
            writeHist(outFile,  hPath, h)
        else:
            h = getHistOther(inFile, year, r, syst, hName)
            writeHist(outFile,  hPath, h)
        #writeHist(outFile, hPath, getHistOther(inFile, r, syst, hName))
        #data_obs for base
        if "Base" in syst:
            hPath = "%s/%s/%s"%("data_obs", r, syst)
            writeHist(outFile,  hPath, getHist(inFile, hPath, hName))
    outFile.Close()
    print "/eos/uscms/%s/AllInc.root\n"%outDir
