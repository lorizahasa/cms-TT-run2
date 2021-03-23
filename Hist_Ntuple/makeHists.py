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
parser.add_option("--ps", "--phaseSpace", dest="phaseSpace", default="Boosted_SR",type='str', 
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
phaseSpace = options.phaseSpace
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
analysisNtupleLocation = ntupleDirBase

#-----------------------------------------
#OUTPUT Histogram Directory
#----------------------------------------
outFileMainDir = "./hists"
gROOT.SetBatch(True)
nJets = 3
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
btagWeight="Weight_btag_1a"
PhoEff= "Weight_pho"
histDirInFile = "%s/%s/Base"%(sample, phaseSpace)
variation = "Base"
if "Data" in sample:
    histDirInFile = "data_obs/%s/Base"%(phaseSpace)
if "QCD%s"%channel in sample:
    histDirInFile = "QCD/%s/Base"%(phaseSpace)

nJets, nBJets, nJetSel, nBJetSel, bothJetSel = getJetMultiCut(phaseSpace)

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
    histDirInFile = "%s/%s/%s%s"%(sample, phaseSpace, syst,level) 
    if "QCD%s"%channel in sample:
        histDirInFile = "QCD/%s/%s%s"%(phaseSpace, syst, level)
    variation = "%s%s"%(syst,level) 
    toPrint("Running for systematics", syst+level)
    if syst=="PU":
        if levelUp:
            Pileup = "Weight_pu_up"
        else:
            Pileup = "Weight_pu_down"
    elif 'Q2' in syst:
        if levelUp:
            Q2="Weight_q2_up"
        else:
            Q2="Weight_q2_down"
    elif 'Pdf' in syst:
    	if levelUp:
    		Pdf="Weight_pdf_up"
    	else:
    		Pdf="Weight_pdf_down"
    elif 'MuEff' in syst:
        if levelUp:
            MuEff = "Weight_mu_up"
        else:
            MuEff = "Weight_mu_down" 
    elif 'EleEff' in syst:
        if levelUp:
            EleEff = "Weight_ele_up"
        else:
            EleEff = "Weight_ele_down"
    elif 'PhoEff' in syst:
        if levelUp:
            PhoEff = "Weight_pho_up"
        else:
            PhoEff = "Weight_pho_down"
    elif 'fsr' in syst:
    	if levelUp:
    	    fsr = "Weight_fsr_up"
    	else:
    	    fsr = "Weight_fsr_down"
    elif 'isr' in syst:
    	if levelUp:
    	    isr = "Weight_isr_up"
    	else:
    	    isr = "Weight_isr_down"
    elif 'prefireEcal' in syst:
	if levelUp:
	    prefire = "Weight_prefire_up"
	else:
	    prefire = "Weight_prefire_down"
    elif 'BTagSF_b' in syst:
        if levelUp:
			btagWeight = "Weight_btag_1a_b_up"
        else:
			btagWeight = "Weight_btag_1a_b_down"
    elif 'BTagSF_l' in syst:
        if levelUp:
			btagWeight = "Weight_btag_1a_l_up"
        else:
			btagWeight = "Weight_btag_1a_l_down" 
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
    extraCuts            = "(Event_pass_presel_mu && Photon_size >=1 && "
    if "Boosted" in phaseSpace:
        if "SR" in phaseSpace:
            extraCuts += "FatJet_size >=1 && Photon_et>100 && %s)*"%(bothJetSel)
        if "CR" in phaseSpace:
            extraCuts += "FatJet_size >=1 && Photon_et > 20 && Photon_et < 50 && %s)*"%(bothJetSel)
    if "Resolved" in phaseSpace:
        if "SR" in phaseSpace:
            extraCuts += "FatJet_size ==0 && Photon_et>100 && %s)*"%(bothJetSel)
        if "CR" in phaseSpace:
            extraCuts += "FatJet_size ==0 && Photon_et > 20 && Photon_et < 50 && %s)*"%(bothJetSel)

elif channel=="Ele":
    if sample=="Data":
        sample = "DataEle"
    if sample=="QCD":
        sample = "QCDEle"
    outFileFullDir = outFileMainDir+"/%s/%s/Ele"%(year,ttbarDecayMode)
    extraCuts            = "(Event_pass_presel_ele && Photon_size >=1 && "
    if "Boosted" in phaseSpace:
        if "SR" in phaseSpace:
            extraCuts += "FatJet_size >=1 && Photon_et>100 && %s)*"%(bothJetSel)
        if "CR" in phaseSpace:
            extraCuts += "FatJet_size >=1 && Photon_et > 20 && Photon_et < 50 && %s)*"%(bothJetSel)
    if "Resolved" in phaseSpace:
        if "SR" in phaseSpace:
            extraCuts += "FatJet_size ==0 && Photon_et>100 && %s)*"%(bothJetSel)
        if "CR" in phaseSpace:
            extraCuts += "FatJet_size ==0 && Photon_et > 20 && Photon_et < 50 && %s)*"%(bothJetSel)
else:
    print "Unknown final state, options are Mu and Ele"
    sys.exit()

weights = "%s*%s*%s*%s*%s*%s*%s*%s*%s"%(evtWeight,Pileup,MuEff,EleEff,Q2,Pdf,isr,fsr,btagWeight)
#weights = "%s"%(evtWeight)
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
outFileFullPath = "%s/%s_%s_%s.root"%(outFileFullDir, sample, phaseSpace, variation)
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
    h.Write()
toPrint("Path of output root file", outFileFullPath)
outputFile.Close()
