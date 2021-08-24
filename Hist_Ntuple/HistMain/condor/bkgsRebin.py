from ROOT import TFile, TH1F, gDirectory
import os
import sys
sys.path.insert(0, os.getcwd().replace("condor", ""))
from HistInputs import *
from HistInfo import GetHistogramInfo
import numpy
import itertools
import json
from optparse import OptionParser

#Samples = ["TTbar"]
#Systematics = []
#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specify the year of the data taking" )
parser.add_option("-d", "--decayMode", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decayMode moded of ttbar Semilep or ? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Ele",type='str',
		  help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("--cr", "--CR", dest="CR", default="ttyg_Enriched_SR",type='str', 
                     help="which control selection and region")
(options, args) = parser.parse_args()
year            = options.year
decayMode       = options.decayMode
channel         = options.channel
CR              = options.CR
hists           = GetHistogramInfo()

#-----------------------------------------
#Path of the I/O histograms/datacards
#----------------------------------------
inDir = "%s/%s/%s/%s/Merged"%(condorHistDir, year, decayMode, channel)
inFile = TFile.Open("%s/AllInc.root"%inDir, "read")
outDir = inDir.replace("Raw", "Rebin")
if not os.path.exists(outDir):
    os.system("mkdir -p %s"%outDir)
outputFile = TFile("%s/AllInc.root"%outDir,"update")
print inFile

DYJetsSF = 1.0      
MisIDSF  = 1.0 
WGammaSF = 1.0 
ZGammaSF = 1.0 
print "%s: DYJetsSF = %s, MisIDSF = %s, WGammaSF = %s, ZGammaSF = %s"%(CR, DYJetsSF, MisIDSF, WGammaSF, ZGammaSF)

dictRebin = {}
dictRebin["Reco_mass_T"] = numpy.array([0,200,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1800.,2500.,6000.])
dictRebin["Photon_et"]   = numpy.array([0,100,200,300,400,500,600,700,900,1200,2000.])
dictRebin["Reco_ht"]     = numpy.array([0,500,700,900,1100,1300,1500,1700,1900,2200,2500,3000,5000,9000.])
dictRebin["Reco_st"]     = numpy.array([0,500,700,900,1100,1300,1500,1700,1900,2200,2500,3000,5000,9000.])

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

def getHistDir(sample, CR, sysType):
    histDir = "%s/%s/%s"%(sample, CR, sysType)
    return histDir

def writeHist(sample, sysType, hist_, outputFile):
    outHistDir = getHistDir(sample, CR, sysType)
    if not outputFile.GetDirectory(outHistDir):
        outputFile.mkdir(outHistDir)
    #print gDirectory.ls()
    outputFile.cd(outHistDir)
    gDirectory.Delete("%s;*"%(hist_.GetName()))
    #print "%10s :/%s/%s/%s/%s"%(round(hist_.Integral(), 1), sample, CR, sysType, hist_.GetName()) 
    if hName in dictRebin.keys():
        hNew = hist_.Rebin(len(dictRebin[hName])-1, hist_.GetName(), dictRebin[hName]) 
        hNew.Write()
    else:
        hist_.Write()
    outputFile.cd()

#-----------------------------------------
#Categorise hists here
#----------------------------------------
allSysType = []
allSysType.append("Base")
for syst, level in itertools.product(Systematics, SystLevels):
    sysType = "%s%s"%(syst, level)
    allSysType.append(sysType)

for sample in Samples:
#for sample in ["TTbar"]: 
    for hName in hists.keys():
        print "-----------------------"
        print "%s, %s"%(sample, CR)
        print "-----------------------"
        if "Data" in sample:
            histDir = getHistDir("data_obs", CR, "Base")
            hist = inFile.Get("%s/%s"%(histDir, hName))
            writeHist("data_obs", "Base", hist, outputFile)
        else:
            for sysType in allSysType:
               hList = []
               histDir = getHistDir(sample, CR, sysType)
               h1 = inFile.Get("%s/%s_hadronic_fake"%(histDir, hName))
               h2 = inFile.Get("%s/%s_hadronic_photon"%(histDir, hName))
               h3 = inFile.Get("%s/%s_genuine"%(histDir, hName))
               h4 = inFile.Get("%s/%s_misid_ele"%(histDir, hName))
               h4.Scale(MisIDSF)
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
               writeHist(sample, sysType, h,  outputFile)
               writeHist(sample, sysType, h1, outputFile)
               writeHist(sample, sysType, h2, outputFile)
               writeHist(sample, sysType, h3, outputFile)
               writeHist(sample, sysType, h4, outputFile)
outputFile.Close()
print "%s/AllInc.root"%outDir
