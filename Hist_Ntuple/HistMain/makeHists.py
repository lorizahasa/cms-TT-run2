from ROOT import TH1F, TFile, TChain, TCanvas, gDirectory, gROOT 
import sys
import os
sys.path.insert(0, os.getcwd()+"/sample")
from optparse import OptionParser
from HistInfo import *
from HistInputs import Regions, phoCat
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
parser.add_option("-r", "--region", dest="region", default="tty_Enriched_a3j_e0b_e1y",type='str', 
                     help="which control selection and region"), 
parser.add_option("--level", "--level", dest="level", default="",type='str',
                     help="Specify up/down of systematic")
parser.add_option("--syst", "--systematic", dest="systematic", default="Base",type='str',
                     help="Specify which systematic to run on")
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_T",type='str', 
                     help="which histogram to be plottted")
parser.add_option("--allHists","--allHists", dest="makeAllHists",action="store_true",default=False,
                     help="Make full list of hists in histogramDict" )
parser.add_option("--isCat","--isCat", dest="isCat",action="store_true",default=False,
                     help="Make full list of hists in histogramDict" )
(options, args) = parser.parse_args()
year = options.year
decayMode = options.decayMode
channel = options.channel
sample = options.sample
region = options.region
syst = options.systematic
level =options.level
makeAllHists = options.makeAllHists
isCat = options.isCat
print parser.parse_args()

#-----------------------------------------
#INPUT AnalysisNtuples Directory
#----------------------------------------
condorNtupleDir = "root://cmseos.fnal.gov//store/user/rverma/Output/cms-TT-run2/Ntuple_Skim"
systDir = "JetBase"
if "jes" in syst and "Up" in level:
    systDir = "JECTotal_up"
if "jes" in syst and "Down" in level:
    systDir = "JECTotal_down"
if "jer" in syst and "Up" in level:
    systDir = "JER_up"
if "jer" in syst and "Down" in level:
    systDir = "JER_down"
if "Data" in sample:
    systDir = "JetBase"
samples = getSamples(year, decayMode, systDir)
analysisNtupleLocation = "%s/%s/%s/%s"%(condorNtupleDir, year, decayMode, systDir) 

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
w_lumi ="Weight_lumi"
w_pu ="Weight_pu"
w_mu = "Weight_mu"
w_ele= "Weight_ele"
w_q2 = 1.0 
w_pdf = 1.0
w_prefire ="Weight_prefire"
w_isr = 1.
w_fsr = 1.
w_btag="Weight_btag"
histDirInFile = "%s/%s/Base"%(sample, region)
variation = "Base"
if "Data" in sample:
    histDirInFile = "data_obs/%s/Base"%(region)
sample_ = sample
if "Data" in sample or "QCD" in sample:
    sample_ = "%s%s"%(sample, channel)
#-----------------------------------------
#For Systematics
#----------------------------------------
levelUp = False
if level in ["up", "UP", "uP", "Up"]: 
	levelUp = True
	level= "Up"
else:
	level = "Down"
if not syst=="Base":
    histDirInFile = "%s/%s/%s%s"%(sample, region, syst,level) 
    variation = "%s_%s"%(syst,level) 
    toPrint("Running for systematics", syst+level)
    if syst=="Weight_pu":
        if levelUp:
            w_pu = "Weight_pu_up"
        else:
            w_pu = "Weight_pu_down"
    elif 'Weight_q2' in syst:
        if levelUp:
            w_q2="Weight_q2_up"
        else:
            w_q2="Weight_q2_down"
    elif 'Weight_pdf' in syst:
    	if levelUp:
    		w_pdf="Weight_pdf_up"
    	else:
    		w_pdf="Weight_pdf_down"
    elif 'Weight_mu' in syst:
        if levelUp:
            w_mu = "Weight_mu_up"
        else:
            w_mu = "Weight_mu_down" 
    elif 'Weight_ele' in syst:
        if levelUp:
            w_ele = "Weight_ele_up"
        else:
            w_ele = "Weight_ele_down"
    elif 'Weight_fsr' in syst:
    	if levelUp:
    	    w_fsr = "Weight_fsr_up"
    	else:
    	    w_fsr = "Weight_fsr_down"
    elif 'Weight_isr' in syst:
    	if levelUp:
    	    w_isr = "Weight_isr_up"
    	else:
    	    w_isr = "Weight_isr_down"
    elif 'Weight_prefire' in syst:
	if levelUp:
	    w_prefire = "Weight_prefire_up"
	else:
	    w_prefire = "Weight_prefire_down"
    elif 'Weight_btag_b' in syst:
        if levelUp:
			w_btag = "Weight_btag_b_up"
        else:
			w_btag = "Weight_btag_b_down"
    elif 'Weight_btag_l' in syst:
        if levelUp:
			w_btag = "Weight_btag_l_up"
        else:
			w_btag = "Weight_btag_l_down" 
    else:
        print "Running Jet Syst"

#-----------------------------------------
#Select channels
#----------------------------------------
if channel=="Mu":
    outFileFullDir = outFileMainDir+"/%s/%s/Mu"%(year,decayMode)
    extraCuts            = "(Event_pass_presel_mu && %s)*"%Regions[region]

elif channel=="Ele":
    outFileFullDir = outFileMainDir+"/%s/%s/Ele"%(year,decayMode)
    extraCuts            = "(Event_pass_presel_ele && %s)*"%Regions[region]
else:
    print "Unknown final state, options are Mu and Ele"
    sys.exit()

weights = "%s*%s*%s*%s*%s*%s*%s*%s*%s*%s"%(w_lumi,w_pu,w_mu,w_ele,w_q2,w_pdf,w_isr,w_fsr,w_btag,w_prefire)
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
if not sample_ in samples:
    print "Sample isn't in list"
    print samples.keys()
    sys.exit()
tree = TChain("AnalysisTree")
fileList = samples[sample_]
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
    if "tt_Enriched" in region:
        w_pho = "1.0"
    else:
        if "Pho" in hist:
            w_pho= "Weight_pho"
            if 'Weight_pho' in syst:
                if levelUp:
                    w_pho = "Weight_pho_up"
                else:
                    w_pho = "Weight_pho_down"
        else:
            w_pho= "Weight_pho[0]"
            if 'Weight_pho' in syst:
                if levelUp:
                    w_pho = "Weight_pho_up[0]"
                else:
                    w_pho = "Weight_pho_down[0]"
    toPrint("Final event weight ", "%s*%s"%(weights, w_pho))
    toPrint("%s/%s: Filling the histogram"%(index, len(histogramsToMake)), hist)
    toPrint("Extra cuts ", extraCuts)
    histograms.append(TH1F("%s"%(hist),"%s"%(hist),hInfo[1][0],hInfo[1][1],hInfo[1][2]))
    if "Data" in sample:
        tree.Draw("%s>>%s"%(hist,hist), "%s%s"%(extraCuts, "1.0"), "goff")
    else:
        tree.Draw("%s>>%s"%(hist,hist), "%s%s*%s"%(extraCuts, weights, w_pho), "goff")
        if isCat and "tty" in region:
            for cat in phoCat.keys():
                histograms.append(TH1F("%s_%s"%(hist, cat),"%s_%s"%(hist, cat),hInfo[1][0],hInfo[1][1],hInfo[1][2]))
                extraCuts_ = extraCuts.replace(")", " && %s[0] )"%phoCat[cat])
                toPrint("Extra cuts ", extraCuts_)
                tree.Draw("%s>>%s_%s"%(hist,hist,cat), "%s%s*%s"%(extraCuts_, weights, w_pho), "goff")

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
    h.Write()
print("Path of output root file:\n%s/%s"%(os.getcwd(), outFileFullPath))
outputFile.Close()
