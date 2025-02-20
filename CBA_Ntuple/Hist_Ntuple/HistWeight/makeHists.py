import os
import sys
import numpy
sys.dont_write_bytecode = True
from HistInfo import *
from HistInputs import Regions, condorNtupleDir
from optparse import OptionParser
from ROOT import TH1F, TFile, TChain, TCanvas, gDirectory, gROOT 

sys.path.insert(0, os.getcwd().replace("HistWeight", ""))
from SampleInfo import *
#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016Pre",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decay", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="Signal_M800",type='str',
                     help="Specify which sample to run on" )
parser.add_option("-r", "--region", dest="region", default="tty_Enriched_le4j_a1b_e1y",type='str', 
                     help="which control selection and region"), 
parser.add_option("--syst", "--systematic", dest="systematic", default="Weight_lumi",type='str',
                     help="Specify which systematic to run on")
parser.add_option("--hist", "--hist", dest="hName", default="Reco_st",type='str', 
                     help="which histogram to be plottted")
parser.add_option("--allHists","--allHists", dest="makeAllHists",action="store_true",default=False,
                     help="Make full list of hists in histogramDict" )
(options, args) = parser.parse_args()
year = options.year
decayMode = options.decayMode
channel = options.channel
sample = options.sample
region = options.region
syst = options.systematic
makeAllHists = options.makeAllHists
print(parser.parse_args())

weights = "Weight_lumi"
systDir = "JetBase"
if "Uncorr" not in syst: 
    weights = "%s*%s"%("Weight_lumi", syst)
    if "JE" in syst:
        systDir = syst
        weights = "Weight_lumi"

isData = False
if "data_obs" in sample:
    isData  = True
    weights = "1.0"
samples = getSamples(year, decayMode, systDir)
analysisNtupleLocation = "%s/%s/%s/%s"%(condorNtupleDir, year, decayMode, systDir) 


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
isQCD = False

histDirInFile = "%s/%s/Base"%(sample, region)
if "Data" in sample:
    histDirInFile = "data_obs/%s/Base"%(region)
sample_ = sample
if isData or "QCD" in sample:
    sample_ = "%s%s"%(sample, channel)
#-----------------------------------------
#For Systematics
#----------------------------------------
histDirInFile = "%s/%s/%s"%(sample, region, syst) 
toPrint("Running for systematics", "%s"%(syst))

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
    print("Unknown final state, options are Mu and Ele")
    sys.exit()

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


tfs = []
for fileName in fileList:
    fullPath = "%s/%s"%(analysisNtupleLocation, fileName)
    print(fullPath)
    tree.Add(fullPath)
    tfs.append(TFile.Open(fullPath,"read"))

#Eff hists    
hForEff = []
for h in list(hForEffs.values()):
    hForEff = hForEff + h

hForEff_ = []
if "Uncorr" in syst:
    for h in hForEff:
        for ind, _file in enumerate(tfs):
            if(ind==0):
                h_ = _file.Get(h)
            else:
                h_.Add(_file.Get(h))
        hForEff_.append(h_)

print("Number of events:", tree.GetEntries())
for index, hist in enumerate(histogramsToMake, start=1):
    hInfo = histogramInfo[hist]
    if isData and not hInfo[2]: continue
    toPrint("Final event weight ", "%s"%(weights))
    toPrint("%s/%s: Filling the histogram"%(index, len(histogramsToMake)), hist)
    toPrint("Extra cuts ", extraCuts)
    histograms.append(TH1F("%s"%(hist),"%s"%(hist),hInfo[1][0],hInfo[1][1],hInfo[1][2]))
    tree.Draw("%s>>%s"%(hist,hist), "%s%s"%(extraCuts, weights), "goff")

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

if "Uncorr" in syst:
    for h in hForEff_:
        toPrint("Trigger Integral %s = "%h.GetName(), h.Integral())
        h.Write()

for h in histograms:
    toPrint("Integral of Histogram %s = "%h.GetName(), h.Integral())
    outputFile.cd(histDirInFile)
    gDirectory.Delete("%s;*"%(h.GetName()))
    h.Write()
print("Path of output root file:\n%s/%s"%(os.getcwd(), outFileFullPath))
outputFile.Close()
