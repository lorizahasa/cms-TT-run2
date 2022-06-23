import os
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.getcwd().replace("condor", ""))
import itertools
from HistInputs import *
from optparse import OptionParser
from HistInfo import GetHistogramInfo
from ROOT import TFile, TH1F, gDirectory

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("--isCheck","--isCheck", dest="isCheck",action="store_true",default=False, help="Merge for combined years and channels")
parser.add_option("--isSep","--isSep", dest="isSep",action="store_true",default=False, help="Merge for separate years and channels")
parser.add_option("--isComb","--isComb", dest="isMerge",action="store_true",default=False, help="Merge for combined years and channels")
(options, args) = parser.parse_args()
isCheck = options.isCheck
isSep = options.isSep
isComb = options.isMerge

#----------------------------------------------
#Bkg scale factors: DY, MisID, ZGamma, WGamma
#----------------------------------------------
dictSFs = {}
dictSFs['2016PreVFP']  = [1.34, 1.79, 1.11, 1.20]
dictSFs['2016PostVFP'] = [1.47, 2.22, 0.54, 1.64]
dictSFs['2017']        = [1.38, 1.01, 1.17, 1.01]
dictSFs['2018']        = [1.38, 1.42, 0.66, 1.23]
dictSFs['2016PreVFP__2016PostVFP__2017__2018'] = [1.38, 1.40, 0.96, 1.22]

rList = Regions.keys()
#hists = GetHistogramInfo().keys()
hists = ['Reco_mass_lgamma']
#-----------------------------------------
#Collect all syst
#----------------------------------------
sysList = []
sysList.append("Base")
#for syst, level in itertools.product(Systematics, SystLevels):
for syst, level in itertools.product(Systematics, ['_up', '_down']):
    sysType = "%s%s"%(syst, level)
    sysList.append(sysType)

if isCheck:
    isSep  = True
    isComb = False
    Years  = [Years[0]]
    Decays = [Decays[0]]
    Channels = [Channels[0]]
    rList   = [Regions.keys()[0]]
    sysList = [sysList[0]]
    #Samples = [Samples[0]]
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

def getHistDir(sample, region, sysType):
    histDir = "%s/%s/%s"%(sample, region, sysType)
    return histDir

def writeHist(sample, sysType, hist_, outFile):
    outHistDir = getHistDir(sample, region, sysType)
    if not outFile.GetDirectory(outHistDir):
        outFile.mkdir(outHistDir)
    #print gDirectory.ls()
    outFile.cd(outHistDir)
    gDirectory.Delete("%s;*"%(hist_.GetName()))
    #print "%10s :/%s/%s/%s/%s"%(round(hist_.Integral(), 1), sample, region, sysType, hist_.GetName()) 
    hist_.Write()
    outFile.cd()

for year, decay, channel in itertools.product(Years, Decays, Channels):
    #-----------------------------------------
    #Path of the I/O histograms
    #----------------------------------------
    inDir = "%s/Rebin/%s/%s/%s"%(dirHist, year, decay, channel)
    inFile = TFile.Open("root://cmseos.fnal.gov/%s/AllInc.root"%inDir, "read")
    outDir = inDir.replace("Rebin", "ForMain")
    os.system("eos root://cmseos.fnal.gov mkdir -p %s"%outDir)
    outFile = TFile("/eos/uscms/%s/AllInc.root"%outDir,"update")
    if isCheck:
        print inFile
    DYJetsSF  = dictSFs[year][0]
    MisIDSF   = dictSFs[year][1]
    WGammaSF  = dictSFs[year][2]
    ZGammaSF  = dictSFs[year][3]
    print("==> %s, %s, %s"%(year, decay, channel))
    for region, sample, hName in itertools.product(rList, Samples, hists):
        if "tt_" in region:
            continue
        if "data" in sample:
            histDir = getHistDir("data_obs", region, "Base")
            hist = inFile.Get("%s/%s"%(histDir, hName))
            writeHist("data_obs", "Base", hist, outFile)
        else:
            for sysType in sysList:
               hList = []
               histDir = getHistDir(sample, region, sysType)
               h1 = inFile.Get("%s/%s_hadronic_fake"%(histDir, hName))
               h2 = inFile.Get("%s/%s_hadronic_photon"%(histDir, hName))
               h3 = inFile.Get("%s/%s_genuine"%(histDir, hName))
               h4 = inFile.Get("%s/%s_misid_ele"%(histDir, hName))
               h4.Scale(MisIDSF)
               if isCheck:
                   print(histDir, hName)
               if "DYJets" in sample:
                   h1.Scale(DYJetsSF)
                   h2.Scale(DYJetsSF)
                   h3.Scale(DYJetsSF)
                   h4.Scale(DYJetsSF)
               if "ZGamma" in sample:
                   h1.Scale(ZGammaSF)
                   h2.Scale(ZGammaSF)
                   h3.Scale(ZGammaSF)
                   h4.Scale(ZGammaSF)
               if "WGamma" in sample:
                   h1.Scale(WGammaSF)
                   h2.Scale(WGammaSF)
                   h3.Scale(WGammaSF)
                   h4.Scale(WGammaSF)
               hList.append(h1)
               hList.append(h2)
               hList.append(h3)
               hList.append(h4)
               h = addHist(hList, hName)
               #write
               writeHist(sample, sysType, h,  outFile)
               writeHist(sample, sysType, h1, outFile)
               writeHist(sample, sysType, h2, outFile)
               writeHist(sample, sysType, h3, outFile)
               writeHist(sample, sysType, h4, outFile)
    outFile.Close()
    print "/eos/uscms/%s/AllInc.root"%outDir
