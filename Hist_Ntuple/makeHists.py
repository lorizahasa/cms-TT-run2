from ROOT import TH1F, TFile, TChain, TCanvas, gDirectory, gROOT 
import sys
import os
sys.path.insert(0, os.getcwd()+"/sample")
from optparse import OptionParser
from HistInfo import *
from HistInputs import Regions
import numpy

from SampleInfo import *
#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decay", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="TT_tytg_M800",type='str',
                     help="Specify which sample to run on" )
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched",type='str', 
                     help="which control selection and region"), 
parser.add_option("--level", "--level", dest="level", default="",type='str',
                     help="Specify up/down of systematic")
parser.add_option("--syst", "--systematic", dest="systematic", default="Base",type='str',
                     help="Specify which systematic to run on")
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_T",type='str', 
                     help="which histogram to be plottted")
parser.add_option("--allHists","--allHists", dest="makeAllHists",action="store_true",default=False,
                     help="Make full list of hists in histogramDict" )
(options, args) = parser.parse_args()
year = options.year
decayMode = options.decayMode
channel = options.channel
sample = options.sample
region = options.region
level =options.level
makeAllHists = options.makeAllHists
print parser.parse_args()
samples = getSamples(year)

#-----------------------------------------
#INPUT AnalysisNtuples Directory
#----------------------------------------
ntupleDirBase       = "%s/%s"%(dirBase,      year) 
ntupleDirBaseCR     = "%s/%s"%(dirBaseCR,    year)
ntupleDirSyst       = "%s/%s"%(dirSyst,      year)
ntupleDirSystCR     = "%s/%s"%(dirSystCR,    year)
analysisNtupleLocation = ntupleDirBase

#----------------------------------------------------------
#NICE WAY TO PRINT STRINGS
#----------------------------------------------------------
def toPrint(string, value):
    length = (len(string)+len(str(value))+2)
    line = "-"*length
    print ""
    print "* "+ line +                    " *"
    print "| "+ " "*length +              " |"
    print "| "+ string+ ": "+ str(value)+ " |"
    print "| "+ " "*length +              " |"
    print "* "+ line +                    " *"
toPrint("Running for Year, Channel, Sample", "%s, %s, %s"%(year, channel, sample))
#-----------------------------------------
#OUTPUT Histogram Directory
#----------------------------------------
outFileMainDir = "./hists"
gROOT.SetBatch(True)
isQCD = False
evtWeight ="Weight_lumi"
Pileup ="Weight_pu"
MuEff = "Weight_mu"
EleEff= "Weight_ele"
Q2 = 1.0 
Pdf = 1.0
#Pdf = "pdfWeight"
prefire ="Weight_prefire"
isr = 1.
fsr = 1.
btagWeight="Weight_btag"
PhoEff= "Weight_pho"
histDirInFile = "%s/%s/Base"%(sample, region)
variation = "Base"
if "Data" in sample:
    histDirInFile = "data_obs/%s/Base"%(region)
if "QCD%s"%channel in sample:
    histDirInFile = "QCD/%s/Base"%(region)

#-----------------------------------------
#For Systematics
#----------------------------------------
syst = options.systematic
levelUp = False
if level in ["up", "UP", "uP", "Up"]: 
	levelUp = True
	level= "Up"
else:
	level = "Down"
if not syst=="Base":
    histDirInFile = "%s/%s/%s%s"%(sample, region, syst,level) 
    if "QCD%s"%channel in sample:
        histDirInFile = "QCD/%s/%s%s"%(region, syst, level)
    variation = "%s_%s"%(syst,level) 
    toPrint("Running for systematics", syst+level)
    if syst=="Weight_pu":
        if levelUp:
            Pileup = "Weight_pu_up"
        else:
            Pileup = "Weight_pu_down"
    elif 'Weight_q2' in syst:
        if levelUp:
            Q2="Weight_q2_up"
        else:
            Q2="Weight_q2_down"
    elif 'Weight_pdf' in syst:
    	if levelUp:
    		Pdf="Weight_pdf_up"
    	else:
    		Pdf="Weight_pdf_down"
    elif 'Weight_mu' in syst:
        if levelUp:
            MuEff = "Weight_mu_up"
        else:
            MuEff = "Weight_mu_down" 
    elif 'Weight_ele' in syst:
        if levelUp:
            EleEff = "Weight_ele_up"
        else:
            EleEff = "Weight_ele_down"
    elif 'Weight_pho' in syst:
        if levelUp:
            PhoEff = "Weight_pho_up"
        else:
            PhoEff = "Weight_pho_down"
    elif 'Weight_fsr' in syst:
    	if levelUp:
    	    fsr = "Weight_fsr_up"
    	else:
    	    fsr = "Weight_fsr_down"
    elif 'Weight_isr' in syst:
    	if levelUp:
    	    isr = "Weight_isr_up"
    	else:
    	    isr = "Weight_isr_down"
    elif 'Weight_prefire' in syst:
	if levelUp:
	    prefire = "Weight_prefire_up"
	else:
	    prefire = "Weight_prefire_down"
    elif 'Weight_btag_b' in syst:
        if levelUp:
			btagWeight = "Weight_btag_b_up"
        else:
			btagWeight = "Weight_btag_b_down"
    elif 'Weight_btag_l' in syst:
        if levelUp:
			btagWeight = "Weight_btag_l_up"
        else:
			btagWeight = "Weight_btag_l_down" 
    else:
    	if  levelUp:
            analysisNtupleLocation = ntupleDirSyst
    	else:
            analysisNtupleLocation = ntupleDirSyst

#-----------------------------------------
#Select channels
#----------------------------------------
if channel=="Mu":
    if sample=="Data":
        sample = "DataMu"
    if sample=="QCD":
        sample = "QCDMu"
    outFileFullDir = outFileMainDir+"/%s/%s/Mu"%(year,decayMode)
    extraCuts            = "(Event_pass_presel_mu && %s)*"%Regions[region]

elif channel=="Ele":
    if sample=="Data":
        sample = "DataEle"
    if sample=="QCD":
        sample = "QCDEle"
    outFileFullDir = outFileMainDir+"/%s/%s/Ele"%(year,decayMode)
    extraCuts            = "(Event_pass_presel_ele && %s)*"%Regions[region]
else:
    print "Unknown final state, options are Mu and Ele"
    sys.exit()

weights = "%s*%s*%s*%s*%s*%s*%s*%s*%s"%(evtWeight,Pileup,MuEff,EleEff,Q2,Pdf,isr,fsr,btagWeight)
#weights = "1"
if "Data" in sample:
    weights = "1"
toPrint("Extra cuts ", extraCuts)
toPrint("Final event weight ", weights)

#-----------------------------------------
#Get list of empty histograms
#----------------------------------------
histogramInfo = GetHistogramInfo()
histogramsToMake = [options.hName]
if makeAllHists:
    histogramsToMake = allHistList
for hist in histogramsToMake:
    if not hist in histogramInfo:
        print "Histogram %s is not defined in HistInfo.py"%hist
        sys.exit()

#-----------------------------------------
# Fill histograms
#----------------------------------------
histograms=[]
if not sample in samples:
    print "Sample isn't in list"
    print samples.keys()
    sys.exit()
tree = TChain("AnalysisTree")
fileList = samples[sample]
for fileName in fileList:
    fullPath = "%s/%s"%(analysisNtupleLocation, fileName)
    if "JE" in syst and levelUp:
        fullPath = "%s/%s_up_%s"%(analysisNtupleLocation, syst, fileName)
    if "JE" in syst and not levelUp: 
        fullPath = "%s/%s_down_%s"%(analysisNtupleLocation, syst, fileName)
    print fullPath
    tree.Add("%s/%s"%(analysisNtupleLocation,fileName))
print "Number of events:", tree.GetEntries()
for index, hist in enumerate(histogramsToMake, start=1):
    hInfo = histogramInfo[hist]
    if ('Data' in sample or isQCD) and not hInfo[2]: continue
    toPrint("%s/%s: Filling the histogram"%(index, len(histogramsToMake)), hist)
    histograms.append(TH1F("%s"%(hist),"%s"%(hist),hInfo[1][0],hInfo[1][1],hInfo[1][2]))
    tree.Draw("%s>>%s"%(hist,hist), "%s%s"%(extraCuts, weights), "goff")

#-----------------------------------------
#Final output Linux and ROOT directories
#----------------------------------------
if not os.path.exists(outFileFullDir):
    os.makedirs(outFileFullDir)
outFileFullPath = "%s/%s_%s_%s.root"%(outFileFullDir, sample, region, variation)
outputFile = TFile(outFileFullPath,"update")
toPrint ("The histogram directory inside the root file is", histDirInFile) 

#-----------------------------------
# Write final histograms in the file
#-----------------------------------
if not outputFile.GetDirectory(histDirInFile):
    outputFile.mkdir(histDirInFile)
outputFile.cd(histDirInFile)
for h in histograms:
    toPrint("Integral of Histogram %s = "%h.GetName(), h.Integral())
    outputFile.cd(histDirInFile)
    gDirectory.Delete("%s;*"%(h.GetName()))
    #h.Sumw2()
    #h.Write()
    #toBeBinned = ['_pt', '_met', '_chi2', '_st', '_ht', '_mass']
    toBeBinned = ['_st', '_ht', '_mass_T']
    isRebin = False
    for var in toBeBinned:
        if var in h.GetName():
            isRebin = True
    if "TT" in h.GetName(): 
        isRebin = False
    if isRebin:
        if "_pt" in h.GetName() or '_met' in h.GetName():
            halfBins = numpy.arange(0,500,20.)
            restBins = numpy.array([600.,1000.,2000.])
            newBins  = numpy.concatenate((halfBins, restBins), axis=None)
        elif "_chi2" in h.GetName():
            halfBins = numpy.arange(0,300,20.)
            restBins = numpy.array([400.,600.,1000.])
            newBins  = numpy.concatenate((halfBins, restBins), axis=None)
        elif "_mass_T" in h.GetName():
            halfBins = numpy.arange(0,1700,100.)
            restBins = numpy.array([1800.,2100.,2500.,3000.,6000.])
            newBins  = numpy.concatenate((halfBins, restBins), axis=None)
        else:
            halfBins = numpy.arange(0,2100,100.)
            restBins = numpy.array([2200.,2500.,2900.,3400.,4000.,6000.])
            newBins  = numpy.concatenate((halfBins, restBins), axis=None)
        hNew = h.Rebin(len(newBins) - 1, h.GetName(), newBins)
        hNew.Write()
    else:
        h.Write()
print("Path of output root file:\n%s/%s"%(os.getcwd(), outFileFullPath))
outputFile.Close()
