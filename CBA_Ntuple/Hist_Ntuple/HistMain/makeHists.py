import os
import sys
import numpy
sys.dont_write_bytecode = True
from HistInfo import *
from HistInputs import *
from optparse import OptionParser
from ROOT import TH1F, TFile, TChain, TCanvas, gDirectory, gROOT 

sys.path.insert(0, os.getcwd().replace("HistMain", ""))
from SampleInfo import *

#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016Pre",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decay", dest="decay", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="Signal_M800",type='str',
                     help="Specify which sample to run on" )
parser.add_option("-r", "--region", dest="region", default="tty_Enriched_a3j_e0b_e1y",type='str', 
                     help="which control selection and region"), 
parser.add_option("--syst", "--systematic", dest="systematic", default="Base",type='str',
                     help="Specify which systematic to run on")
parser.add_option("--hist", "--hist", dest="hName", default="Jet_pt",type='str', 
                     help="which histogram to be plottted")
parser.add_option("--allHists","--allHists", dest="makeAllHists",action="store_true",default=False,
                     help="Make full list of hists in histogramDict" )
parser.add_option("--isCat","--isCat", dest="isCat",action="store_true",default=False,
                     help="Make full list of hists in histogramDict" )
(options, args) = parser.parse_args()
year = options.year
decay = options.decay
channel = options.channel
sample = options.sample
region = options.region
syst = options.systematic
makeAllHists = options.makeAllHists
isCat = options.isCat
print(parser.parse_args())

#-----------------------------------------
#INPUT AnalysisNtuples Directory
#----------------------------------------
systDir = "JetBase"
if "jesUp" in syst:
    systDir = "JECTotal_up"
if "jesDown" in syst:
    systDir = "JECTotal_down"
if "jerUp" in syst:
    systDir = "JER_up"
if "jerDown" in syst:
    systDir = "JER_down"

isData = False
if "data_obs" in sample:
    isData  = True
    systDir = "JetBase"
samples = getSamples(year, decay, systDir)
inDirNtuple = "root://cmseos.fnal.gov/%s/%s/%s/%s"%(dirNtuple, year, decay, systDir) 

#----------------------------------------------------------
#NICE WAY TO PRINT STRINGS
#----------------------------------------------------------
def toPrint(string, value):
    length = (len(string)+len(str(value))+2)
    line = "-"*length
    print("")
    print("* "+ line +                    " *")
    print("| "+ " "*length +              " |")
    print("| "+ string+ ": "+ str(value)+ " |")
    print("| "+ " "*length +              " |")
    print("* "+ line +                    " *")
toPrint("Running for Year, Channel, Sample", "%s, %s, %s"%(year, channel, sample))

#-----------------------------------------
#OUTPUT Histogram Directory
#----------------------------------------
outFileMainDir = "./hists"
gROOT.SetBatch(True)
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
w_ttag="Weight_ttag"
histDirInFile = "%s/%s/Base"%(sample, region)
sample_ = sample
if isData or "QCD" in sample:
    sample_ = "%s%s"%(sample, channel)

#-----------------------------------------
#For Systematics
#----------------------------------------
if not syst=="Base":
    histDirInFile = "%s/%s/%s"%(sample, region, syst) 
    toPrint("Running for systematics: ", syst)
    if "Weight_pu"  in syst: w_pu = syst 
    if "Weight_q2"  in syst: w_q2 = syst 
    if "Weight_pdf" in syst: w_pdf = syst 
    if "Weight_mu"  in syst: w_mu = syst 
    if "Weight_ele" in syst: w_ele = syst 
    if "Weight_fsr" in syst: w_fsr = syst 
    if "Weight_isr" in syst: w_isr = syst 
    if "Weight_prefire" in syst: w_prefire = syst 
    if "Weight_btag" in syst: w_btag = syst 
    if "Weight_ttag" in syst: w_ttag = syst 

#-----------------------------------------
#Select channels
#----------------------------------------
if channel=="Mu":
    outFileFullDir = outFileMainDir+"/%s/%s/Mu"%(year,decay)
    extraCuts            = "(Event_pass_presel_mu && %s)*"%Regions[region]

elif channel=="Ele":
    outFileFullDir = outFileMainDir+"/%s/%s/Ele"%(year,decay)
    extraCuts            = "(Event_pass_presel_ele && %s)*"%Regions[region]
else:
    print("Unknown final state, options are Mu and Ele")
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
        print("Histogram %s is not defined in HistInfo.py"%hist)
        sys.exit()

#-----------------------------------------
# Fill histograms
#----------------------------------------
histograms=[]
if not sample_ in samples:
    print("Sample isn't in list")
    print(samples.keys())
    sys.exit()
tree = TChain("AnalysisTree")
fileList = samples[sample_]
for fileName in fileList:
    fullPath = "%s/%s"%(inDirNtuple, fileName)
    print(fullPath)
    tree.Add("%s/%s"%(inDirNtuple,fileName))
print("Number of events:", tree.GetEntries())
for index, hist in enumerate(histogramsToMake, start=1):
    hInfo = histogramInfo[hist]
    if isData and not hInfo[2]: continue
    if "tt_Enriched" in region:
        w_pho = "1.0"
    else:
        if "Pho" in hist:
            w_pho= "Weight_pho"
            if 'Weight_pho' in syst:
                w_pho = syst
        else:
            w_pho= "Weight_pho[0]"
            if 'Weight_pho' in syst:
                w_pho = "%s[0]"%syst
    toPrint("Final event weight ", "%s*%s"%(weights, w_pho))
    toPrint("%s/%s: Filling the histogram"%(index, len(histogramsToMake)), hist)
    toPrint("Extra cuts ", extraCuts)
    histograms.append(TH1F("%s"%(hist),"%s"%(hist),hInfo[1][0],hInfo[1][1],hInfo[1][2]))
    if isData: 
        tree.Draw("%s>>%s"%(hist,hist), "%s%s"%(extraCuts, "1.0"), "goff")
    else:
        tree.Draw("%s>>%s"%(hist,hist), "%s%s*%s"%(extraCuts, weights, w_pho), "goff")
        if isCat and "tty" in region and "mass_lgamma" in hist:
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
outFileFullPath = "%s/%s_%s_%s.root"%(outFileFullDir, sample, region, syst)
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
