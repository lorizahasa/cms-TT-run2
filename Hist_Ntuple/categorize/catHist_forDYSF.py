from ROOT import TFile, TH1F, gDirectory
import os
import sys
sys.path.insert(0, os.getcwd().replace("category", ""))
import numpy
import itertools
import json
from optparse import OptionParser
from HistInputs import *

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specify the year of the data taking" )
parser.add_option("-d", "--decayMode", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decayMode moded of ttbar Semilep or ? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
		  help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("--hist", "--hist", dest="inHistName", default="Reco_mass_lgamma",type='str',
		  help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("--cr", "--CR", dest="CR", default="",type='str', 
                     help="which control selection and region")
(options, args) = parser.parse_args()
year            = options.year
decayMode       = options.decayMode
channel         = options.channel
inHistName      = options.inHistName
CR              = options.CR

#-----------------------------------------
#Path of the I/O histograms/datacards
#----------------------------------------
inFile = TFile.Open("%s/%s/%s/%s/Merged/AllInc.root"%(condorHistDir, year, decayMode, channel), "read")
outFileName = "All_forDYSF.root"
print inFile
outputFile = TFile(outFileName,"update")
#-----------------------------------------
#Functions to read/write histograms
#----------------------------------------
newBins = numpy.arange(70.,120.,10) #dont put space

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

def getHistDir(sample, sysType, CR):
    histDir = "%s/%s/%s"%(sample, CR, sysType)
    return histDir

def writeHist(hist, procDir, histNewName, outputFile):
    outHistDir = getHistDir(procDir, inHistName, CR)
    if not outputFile.GetDirectory(outHistDir):
        outputFile.mkdir(outHistDir)
    outputFile.cd(outHistDir)
    gDirectory.Delete("%s;*"%(hist.GetName()))
    print "%20s, %15s, %10s, %10s"%(inHistName, procDir, histNewName, round(hist.Integral()))
    hNew = hist.Rebin(len(newBins)-1, histNewName, newBins) 
    hNew.Write()
    #hist.Write()

def getHistData(inHistName, procDir, sysType):
    histDir = getHistDir(procDir, sysType, CR)
    print "Hist: %s/%s"%(histDir, inHistName)
    hist = inFile.Get("%s/%s"%(histDir, inHistName)).Clone(sysType)
    return hist, procDir, sysType

#-----------------------------------------
#Functions 
#----------------------------------------
def getHistAlone(inHistName, procDir, sysType):
    for sample in Samples:
        histDir = getHistDir(sample, sysType, CR)
        if sample in procDir:
            h = inFile.Get("%s/%s"%(histDir, inHistName)).Clone(sysType)
    return h, procDir, sysType

def getHistOther(inHistName, procDir, sysType):
    SampleOther = []
    for s in Samples:
        others = True
        if "TT_tytg" in s: others = False
        if "Data" in s: others = False
        if "QCD" in s: others = False
        if others: 
            SampleOther.append(s)
    SampleOther.append("QCD")
    hList = []
    sysType_ = sysType
    for sample in SampleOther:
        histDir = getHistDir(sample, sysType, CR)
        h = inFile.Get("%s/%s"%(histDir, inHistName))
        hList.append(h)
        #print "%s = %s"%(sample, h.Integral())
    return addHist(hList, sysType), procDir, sysType_

#-----------------------------------------
#Categorise hists here
#----------------------------------------
allSysType = []
allSysType.append("Base")
for syst, level in itertools.product(Systematics, SystLevels):
    sysType = "%s%s"%(syst, level)
    allSysType.append(sysType)
writeList = []
#for sysType in allSysType:
for sysType in ["Base"]: 
    writeList.append(getHistData(inHistName, "data_obs", "Base"))
    writeList.append(getHistAlone(inHistName,  "DYJets",  sysType))
    writeList.append(getHistOther(inHistName,  "OtherBkgs",   sysType))
    # signal sample for plotting purpose
    writeList.append(getHistAlone(inHistName,  "TT_tytg_M800",   sysType))
    writeList.append(getHistAlone(inHistName,  "TT_tytg_M1200",  sysType))
    writeList.append(getHistAlone(inHistName,  "TT_tytg_M1600",  sysType))
for write in writeList:
    writeHist(write[0], write[1], write[2], outputFile)
outputFile.Close()
print outFileName
