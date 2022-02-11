from ROOT import TFile, TH1F, gDirectory
import os
import sys
import math
sys.path.insert(0, os.getcwd().replace("condor_read", ""))
from DiscInputs import *
from VarInfo import GetVarInfo
import numpy
import itertools
import json
from optparse import OptionParser

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
parser.add_option("--method", "--method", dest="method", default="BDTG",type='str', 
                     help="Which MVA method to be used")
(options, args) = parser.parse_args()
year            = options.year
decayMode       = options.decayMode
channel         = options.channel
method          = options.method

#-----------------------------------------
#Path of the I/O histograms/datacards
#----------------------------------------
inDir = "/eos/uscms/%s/Reader/%s/%s/%s/CombMass/%s/Merged"%(condorOutDir, year, decayMode, channel, method)
inFile = TFile.Open("%s/AllInc.root"%inDir)
outputFile = TFile("%s/AllInc_forMain.root"%inDir,"RECREATE")
print inFile

#-----------------------------------------
#Read SFs
#----------------------------------------
pathDY = "/uscms_data/d3/rverma/codes/CMSSW_10_2_13/src/TopRunII/cms-TT-run2/CBA_Ntuple/Fit_Hist/FitDYSF/"
nameDY  = "RP_%s_%s_%s_%s_%s"%(year, "Dilep", "Mu_Ele", "DY_Enriched_a2j_e0b_e0y", "Reco_mass_dilep")
with open ("%s/RateParams.json"%pathDY) as jsonFileDY:
    jsonDataDY = json.load(jsonFileDY)

path = "/uscms_data/d3/rverma/codes/CMSSW_10_2_13/src/TopRunII/cms-TT-run2/CBA_Ntuple/Fit_Hist/FitMisIDSF/"
name  = "RP_%s_%s_%s_%s_%s"%(year, "Semilep", "Mu_Ele", "MisID_Enriched_a2j_e0b_e1y", "Reco_mass_lgamma")
with open ("%s/RateParams.json"%path) as jsonFile:
    jsonData = json.load(jsonFile)

def getRateParam(jsonData_, name, param):
    paramDicts = jsonData_[name]
    rateParam = 1.0
    for paramDict in paramDicts:
        for key, val in paramDict.iteritems():
            if param==key:
                rateParam = val
    return rateParam
DYJetsSF      = getRateParam(jsonDataDY, nameDY,"r")[1]
#MisIDSF   = getRateParam(jsonData, name,"r")[1]
MisIDSF   = 1.0 # Need to fix this 
WGammaSF  = getRateParam(jsonData, name,"WGammaSF")[1]
ZGammaSF  = getRateParam(jsonData, name,"ZGammaSF")[1]
print "Year = %s, DYJetsSF = %s, MisIDSF = %s, WGammaSF = %s, ZGammaSF = %s"%(year, DYJetsSF, MisIDSF, WGammaSF, ZGammaSF)

dictRebin = {}
dictRebin["Reco_mass_T"] = numpy.array([0,200,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1800.,2500.,6000.])
dictRebin["Photon_et"]   = numpy.array([0,100,200,300,400,500,600,700,900,1200,2000.])
dictRebin["Reco_ht"]     = numpy.array([0,500,700,900,1100,1300,1500,1700,1900,2200,2500,3000,5000,9000.])
dictRebin["Reco_st"]     = numpy.array([0,500,700,900,1100,1300,1500,1700,1900,2200,2500,3000,5000,9000.])

#-----------------------------------------
#Functions to read/write histograms
#----------------------------------------
def getHistDir(sample, region, sysType):
    histDir = "%s/%s/%s"%(sample, region, sysType)
    return histDir

def writeHist(sample, region, sysType, hist_, outputFile):
    print "%s, %s, %s, %s, %s"%(sample, region, hist_.GetName(), round(hist_.Integral(),2), sysType)
    outHistDir = getHistDir(sample, region, sysType)
    if not outputFile.GetDirectory(outHistDir):
        outputFile.mkdir(outHistDir)
    #print gDirectory.ls()
    outputFile.cd(outHistDir)
    #gDirectory.Delete("%s;*"%(hist_.GetName()))
    #print "%10s :/%s/%s/%s/%s"%(round(hist_.Integral(), 1), sample, region, sysType, hist_.GetName()) 
    if hName in dictRebin.keys():
        hNew = hist_.Rebin(len(dictRebin[hName])-1, hist_.GetName(), dictRebin[hName]) 
        hNew.Write()
    else:
        hist_.Write()
    outputFile.cd()

#-----------------------------------------
#Categorise hists here
#----------------------------------------
systToNorm = []
systToNorm.append("Weight_q2Up")
systToNorm.append("Weight_q2Down")
systToNorm.append("Weight_pdfUp")
systToNorm.append("Weight_pdfDown")
systToNorm.append("Weight_isrUp")
systToNorm.append("Weight_isrDown")
systToNorm.append("Weight_fsrUp")
systToNorm.append("Weight_fsrDown")

allSysType = []
allSysType.append("Base")
for syst, level in itertools.product(Systematics, SystLevels):
    sysType = "%s%s"%(syst, level)
    allSysType.append(sysType)

#for sample, region, hName in itertools.product(['TTbar'], Regions.keys(), ['Disc']): 
for sample, region in itertools.product(Samples, Regions.keys()): 
    hists = GetVarInfo(region, channel).keys()
    hists.append("Disc")
    for hName in hists:
        if "Data" in sample:
            histDir = getHistDir("data_obs", region, "Base")
            hist = inFile.Get("%s/%s"%(histDir, hName))
            writeHist("data_obs", region, "Base", hist, outputFile)
        else:
            for sysType in allSysType:
               histDir = getHistDir(sample, region, sysType)
               hist = inFile.Get("%s/%s"%(histDir, hName))
               if "DYJets" in sample:
                   hist.Scale(DYJetsSF)
               if "ZGamma" in sample:
                   hist.Scale(ZGammaSF)
               if "WGamma" in sample:
                   hist.Scale(WGammaSF)
               #write
               hist.Scale(MisIDSF)#Need to fix this
               if sysType in systToNorm:
                   histBase = inFile.Get("%s/%s"%(getHistDir(sample, region, "Base"), hName))
                   histBase.Scale(MisIDSF)#Need to fix this
                   sysInt = hist.Integral()
                   if sysInt ==0 or math.isnan(sysInt):
                       print("\nWarning: %s, %s, %s, %s, syst = %s, integral = %s\n"%(year, channel, sample, region, sysType, sysInt))
                   else:
                       hist.Scale(histBase.Integral()/sysInt)
               writeHist(sample, region, sysType, hist,  outputFile)
outputFile.Close()
print "%s/AllInc_forMain.root"%inDir
