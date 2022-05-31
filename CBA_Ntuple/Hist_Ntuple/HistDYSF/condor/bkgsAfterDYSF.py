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

rList = Regions.keys()
#-----------------------------------------
# Collect all syst 
#----------------------------------------
sysList = []
sysList.append("Base")
for syst, level in itertools.product(Systematics, ["up", "down"]): 
    sysList.append("%s_%s"%(syst, level))

if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
    rList   = [Regions.keys()[0]]
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
    if "DYJets" in hPath:
        hist.Scale(sfVal)
    return hist

def getHistOther(inFile, reg, syst, hName):
    hList = []
    for s in Samples:
        if ("Singal" in s) or ("data_obs" in s) or ("DYJets" in s): 
            continue
        hPath = "%s/%s/%s"%(s, reg, syst)
        hList.append(getHist(inFile, hPath, hName))
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
for year, decay, channel in itertools.product(Years, Decays, Channels):
    inDir = "%s/Rebin/%s/%s/%s"%(dirHist, year, decay, channel)
    inFile = TFile.Open("root://cmseos.fnal.gov/%s/AllInc.root"%inDir, "read")
    if isCheck:
        print inFile
    outDir = inDir.replace("Rebin", "AfterDYSF")
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%outDir)
    outFile = TFile("/eos/uscms/%s/AllInc.root"%outDir,"update")
    print("==> %s, %s, %s"%(year, decay, channel))
    for r, syst, hName in itertools.product(rList, sysList, hists.keys()):
        sfKey = "DYSF_%s_%s_%s_%s"%(year, decay, channel, r)
        sfVal  = DYSF[sfKey]
        print(sfKey, sfVal)
        #DY
        hPath = "%s/%s/%s"%("DYJets", r, syst)
        writeHist(outFile,  hPath, getHist(inFile, hPath, hName))
        #Signal
        hPath = "%s/%s/%s"%("Signal_M800", r, syst)
        writeHist(outFile,  hPath, getHist(inFile, hPath, hName))
        hPath = "%s/%s/%s"%("Signal_M1200", r, syst)
        writeHist(outFile,  hPath, getHist(inFile, hPath, hName))
        hPath = "%s/%s/%s"%("Signal_M1600", r, syst)
        writeHist(outFile,  hPath, getHist(inFile, hPath, hName))
        #OtherBkgs
        hPath = "%s/%s/%s"%("OtherBkgs", r, syst)
        writeHist(outFile, hPath, getHistOther(inFile, r, syst, hName))
        #data_obs for base
        if "Base" in syst:
            hPath = "%s/%s/%s"%("data_obs", r, syst)
            writeHist(outFile,  hPath, getHist(inFile, hPath, hName))
    outFile.Close()
    print "/eos/uscms/%s/AllInc.root\n"%outDir
