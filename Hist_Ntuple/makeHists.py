from ROOT import TH1F, TFile, TChain, TCanvas, gDirectory, gROOT 
import sys
import os
from optparse import OptionParser
sys.path.insert(0, os.getcwd()+"/sample")
from SampleInfo import *
from HistInfo import *
from HistFunc import *

#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decay", dest="ttbarDecayMode", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="TTbar",type='str',
                     help="Specify which sample to run on" )
parser.add_option("--level", "--level", dest="level", default="",type='str',
                     help="Specify up/down of systematic")
parser.add_option("--syst", "--systematic", dest="systematic", default="Base",type='str',
                     help="Specify which systematic to run on")
parser.add_option("--cr", "--controlRegion", dest="controlRegion", default="",type='str', 
                     help="which control selection and region such as Tight, VeryTight, Tight0b, looseCR2e1, looseCRe2g1")
parser.add_option("--plot", dest="plotList",action="append",
                     help="Add plots" )
parser.add_option("--allPlots","--allPlots", dest="makeAllPlots",action="store_true",default=False,
                     help="Make full list of plots in histogramDict" )
(options, args) = parser.parse_args()
year = options.year
ttbarDecayMode = options.ttbarDecayMode
channel = options.channel
sample = options.sample
level =options.level
controlRegion = options.controlRegion
makeAllPlots = options.makeAllPlots
toPrint("Running for Year, Channel, Sample", "%s, %s, %s"%(year, channel, sample))
print parser.parse_args()
samples = getSamples(year)

#-----------------------------------------
#INPUT AnalysisNtuples Directory
#----------------------------------------
ntupleDirBase       = "%s/%s"%(dirBase,      year) 
ntupleDirBaseCR     = "%s/%s"%(dirBaseCR,    year)
ntupleDirSyst       = "%s/%s"%(dirSyst,      year)
ntupleDirSystCR     = "%s/%s"%(dirSystCR,    year)
if "Di" in ttbarDecayMode:
    ntupleDirBase  = "%s/%s"%(dirBaseDilep, year)
    ntupleDirSyst       = "%s/%s"%(dirSystDilep,year)
analysisNtupleLocation = ntupleDirBase

#-----------------------------------------
#OUTPUT Histogram Directory
#----------------------------------------
outFileMainDir = "./hists"
gROOT.SetBatch(True)
nJets = 3
isQCD = False
evtWeight ="evtWeight"
Pileup ="PUweight"
MuEff = "muEffWeight"
EleEff= "eleEffWeight"
Q2 = 1.0 
Pdf = 1.0
#Pdf = "pdfWeight"
prefire ="prefireSF"
isr = 1.
fsr = 1.
btagWeight="btagWeight_1a"
PhoEff= "phoEffWeight"
loosePhoEff= "loosePhoEffWeight"
histDirInFile = "%s/Base"%sample
variation = "Base"
if "Data" in sample:
    histDirInFile = "data_obs/Base"
if "QCD%s"%channel in sample:
    histDirInFile = "QCD/Base"

nJets, nBJets, nJetSel, nBJetSel, bothJetSel = getJetMultiCut(controlRegion, False)

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
    histDirInFile = "%s/%s%s"%(sample,syst,level) 
    if "QCD%s"%channel in sample:
        histDirInFile = "QCD/%s%s"%(syst, level)
    variation = "%s%s"%(syst,level) 
    toPrint("Running for systematics", syst+level)
    if syst=="PU":
        if levelUp:
            Pileup = "PUweight_Up"
        else:
            Pileup = "PUweight_Do"
    elif 'Q2' in syst:
        if levelUp:
            Q2="q2weight_Up"
        else:
            Q2="q2weight_Do"
    elif 'Pdf' in syst:
    	if syst=="Pdf":
    	    if levelUp:
    	    	Pdf="pdfweight_Up"
    	    else:
    	    	Pdf="pdfweight_Do"
    	else:
    	    if type(eval(syst[3:]))==type(int()):
    	    	pdfNumber = eval(syst[3:])
    	    	Pdf="pdfSystWeight[%i]/pdfWeight"%(pdfNumber-1)
    elif 'MuEff' in syst:
        if levelUp:
            MuEff = "muEffWeight_Up"
        else:
            MuEff = "muEffWeight_Do"
    elif 'EleEff' in syst:
        if levelUp:
            EleEff = "eleEffWeight_Up"
        else:
            EleEff = "eleEffWeight_Do"
    elif 'PhoEff' in syst:
        if levelUp:
            PhoEff = "phoEffWeight_Up"
            loosePhoEff = "loosePhoEffWeight_Up"
        else:
            PhoEff = "phoEffWeight_Do"
            loosePhoEff = "loosePhoEffWeight_Do"
    elif 'fsr' in syst:
    	if levelUp:
    	    fsr = "FSRweight_Up"
    	else:
    	    fsr = "FSRweight_Do"
    elif 'isr' in syst:
    	if levelUp:
    	    isr = "ISRweight_Up"
    	else:
    	    isr = "ISRweight_Do"
    elif 'prefireEcal' in syst:
	if levelUp:
	    prefire = "prefireSF_Up"
	else:
	    prefire = "prefireSF_Do"
    elif 'BTagSF_b' in syst:
        if levelUp:
			btagWeight = "btagWeight_1a_b_Up"
        else:
			btagWeight = "btagWeight_1a_b_Do"
    elif 'BTagSF_l' in syst:
        if levelUp:
			btagWeight = "btagWeight_1a_l_Up"
        else:
			btagWeight = "btagWeight_1a_l_Do"
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
    outFileFullDir = outFileMainDir+"/%s/%s/Mu"%(year,ttbarDecayMode)
    #extraCuts            = "(passPresel_Mu && %s && chi2<50)*"%(bothJetSel)
    extraCuts            = "(passPresel_Mu && %s)*"%(bothJetSel)
    #extraCuts            = ""

elif channel=="Ele":
    if sample=="Data":
        sample = "DataEle"
    if sample=="QCD":
        sample = "QCDEle"
    outFileFullDir = outFileMainDir+"/%s/%s/Ele"%(year,ttbarDecayMode)
    extraCuts            = "(passPresel_Ele && %s)*"%(bothJetSel)
else:
    print "Unknown final state, options are Mu and Ele"
    sys.exit()

weights = "%s*%s*%s*%s*%s*%s*%s*%s*%s"%(evtWeight,Pileup,MuEff,EleEff,Q2,Pdf,isr,fsr,btagWeight)
#weights = "%s*%s"%(evtWeight,Pileup)
toPrint("Extra cuts ", extraCuts)
toPrint("Final event weight ", weights)

#-----------------------------------------
#Get list of empty histograms
#----------------------------------------
histogramInfo = GetHistogramInfo(extraCuts,nBJets)
plotList = options.plotList
if plotList is None:
    if makeAllPlots:
        plotList = allPlotList 
plotList.sort()
for p in plotList: print "%s,"%p,
histogramsToMake = plotList
allHistsDefined = True
for hist in histogramsToMake:
    if not hist in histogramInfo:
        print "Histogram %s is not defined in HistInfo.py"%hist
        allHistsDefined = False
if not allHistsDefined:
    sys.exit()

#-----------------------------------------
# Fill histograms
#----------------------------------------
histograms=[]
if not "QCD_DD" in sample:
    if not sample in samples:
        print "Sample isn't in list"
        print samples.keys()
        sys.exit()
    tree = TChain("AnalysisTree")
    fileList = samples[sample]
    for fileName in fileList:
        if "Dilep" in ttbarDecayMode:
            fullPath = "%s/Dilep_%s"%(analysisNtupleLocation, fileName)
            if "JE" in syst and levelUp:
                fullPath = "%s/Dilep_%s_up_%s"%(analysisNtupleLocation, syst, fileName)
            if "JE" in syst and not levelUp: 
                fullPath = "%s/Dilep_%s_down_%s"%(analysisNtupleLocation, syst, fileName)
        else:
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
        if ('Data' in sample or isQCD) and not hInfo[5]: continue
        toPrint("%s/%s: Filling the histogram"%(index, len(histogramsToMake)), hInfo[1])
        evtWeight = ""
        histograms.append(TH1F("%s"%(hInfo[1]),"%s"%(hInfo[1]),hInfo[2][0],hInfo[2][1],hInfo[2][2]))
        if hInfo[4]=="":
            evtWeight = "%s%s"%(hInfo[3],weights)
        else:
            evtWeight = hInfo[4]
        if "Data" in sample:
            evtWeight = "%s%s"%(hInfo[3],weights)
        if evtWeight[-1]=="*":
            evtWeight= evtWeight[:-1]
        ### Correctly add the photon weights to the plots
        if 'phosel' in hInfo[1]:
            if hInfo[0][:8]=="loosePho":
                evtWeight = "%s*%s"%(evtWeight,loosePhoEff)
            elif hInfo[0][:3]=="pho":
                evtWeight = "%s*%s"%(evtWeight,PhoEff)
            else:
                evtWeight = "%s*%s[0]"%(evtWeight,PhoEff)
        print evtWeight
        print hInfo[0]
        print hInfo[1]
        tree.Draw("%s>>%s"%(hInfo[0],hInfo[1]),evtWeight, "goff")

#-----------------------------------------
#Final output Linux and ROOT directories
#----------------------------------------
if not os.path.exists(outFileFullDir):
    os.makedirs(outFileFullDir)
outFileFullPath = "%s/%s_%s_SR.root"%(outFileFullDir, sample, variation)
if not controlRegion =="":
    outFileFullPath = "%s/%s_%s_CR_%s.root"%(outFileFullDir, sample, variation, controlRegion)
outputFile = TFile(outFileFullPath,"update")
if not controlRegion =="":
    histDirInFile  = "%s/CR/%s"%(histDirInFile,  controlRegion)
else:
    histDirInFile  = "%s/SR"%histDirInFile 
toPrint ("The histogram directory inside the root file is", histDirInFile) 


#-----------------------------------------
# QCD in SR = TF * (data - nonQCDBkg from CR)
#----------------------------------------
qcdTFDirInFile = "%s/TF"%histDirInFile
qcdShapeDirInFile = "%s/Shape"%histDirInFile
transferFactor = 1.0
if sample =="QCD_DD" and "Semi" in ttbarDecayMode:
        toPrint("Determining QCD Transfer factor from CR", "")
	#transferFactor = getQCDTransFact(year, channel, nBJets, outputFile, qcdTFDirInFile)
	print "Transfer factor = ", transferFactor
        for hist in histogramsToMake:
            if not histogramInfo[hist][5]: continue
            toPrint("Determining QCD shape from CR", "")
	    dataMinusOtherBkg = getShapeFromCR(year, channel, nJetSel, nBJets, histogramInfo[hist], outputFile, qcdShapeDirInFile)
            histograms.append(dataMinusOtherBkg)
	    print histogramInfo[hist][1]
            histograms[-1].Scale(transferFactor)

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
    h.Write()
toPrint("Path of output root file", outFileFullPath)
outputFile.Close()
