import os
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor", ""))
pathDYSF = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/CBA_Ntuple/Fit_Hist/FitDYSF"
sys.path.insert(0, pathDYSF) 
from FitDYSF_dictDYSF import DYSF
import itertools
from HistInputs import *
from optparse import OptionParser
from HistInfo import GetHistogramInfo
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

hists = GetHistogramInfo()
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

def getHist(inFile, hPath, hName):
    hPath_ = "%s/%s"%(hPath, hName)
    try:
        hist = inFile.Get(hPath_)
        hist = hist.Clone(hName)
    except Exception:
        print ("Error: Hist not found. \nFile: %s \nHistName: %s"%(inFile, hPath_))
        sys.exit()
    return hist

#-----------------------------------------
#Functions for misID 
#----------------------------------------
def getHistMisID(inFile, reg, syst, hName):
    hList = []
    for s in Samples:
        if ("Signal" in s) or ("data_obs" in s): 
            continue
        hPath = "%s/%s/%s"%(s, reg, syst)
        hist = getHist(inFile, hPath, "%s_misid_ele"%hName) 
        if "DYJets" in hPath:
            hist.Scale(sfVal)
        hList.append(hist)
    return addHist(hList, hName)

def getHistVGamma(inFile, samp, reg, syst, hName):
    hList = []
    for s in Samples:
        if samp not in s:
            continue
        hPath = "%s/%s/%s"%(s, reg, syst)
        hist1 = getHist(inFile, hPath, "%s_genuine"%hName) 
        hist2 = getHist(inFile, hPath, "%s_hadronic_photon"%hName) 
        hist3 = getHist(inFile, hPath, "%s_hadronic_fake"%hName) 
        hList.append(hist1)
        hList.append(hist2)
        hList.append(hist3)
    return addHist(hList, hName)


def getHistOther(inFile, reg, syst, hName):
    hList = []
    for s in Samples:
        if ("Signal" in s) or ("data_obs" in s) or ("WGamma" in s) or ("ZGamma" in s): 
            continue
        hPath = "%s/%s/%s"%(s, reg, syst)
        hist1 = getHist(inFile, hPath, "%s_genuine"%hName) 
        hist2 = getHist(inFile, hPath, "%s_hadronic_photon"%hName) 
        hist3 = getHist(inFile, hPath, "%s_hadronic_fake"%hName) 
        if "DYJets" in s:
            hist1.Scale(sfVal)
            hist2.Scale(sfVal)
            hist3.Scale(sfVal)
        hList.append(hist1)
        hList.append(hist2)
        hList.append(hist3)
    return addHist(hList, hName)

def writeHist(outFile, hPath, hist):
    if not outFile.GetDirectory(hPath):
        outFile.mkdir(hPath)
    outFile.cd(hPath)
    gDirectory.Delete("%s;*"%(hist.GetName()))
    if isCheck:
        print("%60s, %20s, %10s"%(hPath, hist.GetName(), round(hist.Integral())))
    hist.Write()


#-----------------------------------------
# Do the rebining here
#----------------------------------------
for year, decay, channel in itertools.product(Years, Decays, Channels):
    inDir = "%s/Rebin/%s/%s/%s"%(dirHist, year, decay, channel)
    inFile = TFile.Open("root://cmseos.fnal.gov/%s/AllInc.root"%inDir, "read")
    if isCheck:
        print(inFile)
    outDir = inDir.replace("Rebin", "ForMisIDSF")
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%outDir)
    outFile = TFile("/eos/uscms/%s/AllInc.root"%outDir,"update")
    print("==> %s, %s, %s"%(year, decay, channel))
    for r, syst, hName in itertools.product(rList, sysList, hists.keys()):
        sfKey = "DYSF_%s_%s_%s_%s"%(year, "Dilep", "Mu__Ele", "DY_Enriched_a2j_e0b_e0y")
        sfVal  = DYSF[sfKey]
        print(sfKey, sfVal)

        hPath = "%s/%s/%s"%("MisIDEle", r, syst)
        writeHist(outFile,  hPath, getHistMisID(inFile, r, syst, hName))

        hPath = "%s/%s/%s"%("WGamma", r, syst)
        writeHist(outFile,  hPath, getHistVGamma(inFile, "WGamma", r, syst, hName))

        hPath = "%s/%s/%s"%("ZGamma", r, syst)
        writeHist(outFile,  hPath, getHistVGamma(inFile, "ZGamma", r, syst, hName))

        #OtherBkgs
        hPath = "%s/%s/%s"%("OtherPhotons", r, syst)
        writeHist(outFile, hPath, getHistOther(inFile, r, syst, hName))

        #Signal
        hPath = "%s/%s/%s"%("SignalSpin12_M800", r, syst)
        writeHist(outFile,  hPath, getHist(inFile, hPath, hName))
        hPath = "%s/%s/%s"%("SignalSpin12_M1200", r, syst)
        writeHist(outFile,  hPath, getHist(inFile, hPath, hName))
        hPath = "%s/%s/%s"%("SignalSpin12_M1500", r, syst)
        writeHist(outFile,  hPath, getHist(inFile, hPath, hName))

        #data_obs for base
        if "Base" in syst:
            hPath = "%s/%s/%s"%("data_obs", r, syst)
            writeHist(outFile,  hPath, getHist(inFile, hPath, hName))
    outFile.Close()
    print("/eos/uscms/%s/AllInc.root\n"%outDir)
