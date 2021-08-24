from ROOT import TFile, TH1F, gDirectory
import os
import sys
import json
import itertools
from optparse import OptionParser
import CombineHarvester.CombineTools.ch as ch
from FitInputs import *

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specify the year of the data taking" )
parser.add_option("-d", "--decayMode", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decayMode moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
		  help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-m", "--mass", dest="mass", default="800",type='str',
                     help="Specify the mass of charged Higgs")
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_T",type='str', 
                     help="which histogram to be used for making datacard")
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched_SR_Resolved",type='str', 
                     help="which control selection and region"), 
parser.add_option("--isQCDMC","--qcdMC",dest="isQCDMC", default=False, action="store_true",
		  help="")
(options, args) = parser.parse_args()
year            = options.year
decayMode       = options.decayMode
channel         = options.channel
mass            = options.mass
hName           = options.hName
region          = options.region
isQCDMC         = options.isQCDMC

#-----------------------------------------
#Path of the I/O histograms/datacards
#----------------------------------------
inFileName = "%s/Hist_Ntuple/HistMain/forMain/%s/%s/%s/Merged/AllInc.root"%(condorHistDir, year, decayMode, channel)
print inFileName
inHistDirBase   = "$PROCESS/%s/Base/$BIN"%region
inHistDirSys    = "$PROCESS/%s/$SYSTEMATIC/$BIN"%region
outFileDir      = "%s/Fit_Hist/HistMain/forMain/%s/%s/%s/%s/%s/mH%s"%(condorHistDir, year, decayMode, channel, region, hName, mass)

outFilePath     = "%s/Shapes_Inc.root"%(outFileDir)
datacardPath    = "%s/Datacard_Inc.txt"%(outFileDir)
if not os.path.exists(outFileDir):
    os.makedirs(outFileDir)

#-----------------------------------
# Make datacard 
#-----------------------------------
cb = ch.CombineHarvester()
#cb.SetVerbosity(4)
AllBkgs = ["TTbar", "TTGamma", "WJets", "DYJets", "WGamma", "ZGamma", "Others","QCD"]
#AllBkgs = ["TTGamma", "TTbar", "SingleTop", "Others"] 
Signal  = ["TT_tytg_M%s"%mass]
allMC   = Signal + AllBkgs
#------------------
#Add observed data
#------------------
cb.AddObservations(["*"],["TT"],["13TeV"],[channel],[(-1, hName)])
#------------------
#Add sig& bkgs
#------------------
cb.AddProcesses(["*"],["TT"],["13TeV"],[channel],Signal,[(-1, hName)], True)
cb.AddProcesses(["*"],["TT"],["13TeV"],[channel],AllBkgs,[(-1, hName)], False)
#------------------
#Add systematics
#------------------
cb.cp().process(allMC).AddSyst(cb, "lumi_$ERA", "lnN",ch.SystMap("era") (["13TeV"], 1.025))
cb.cp().process(["TTGamma"]).AddSyst(cb, "CMS_norm_tty", "lnN",ch.SystMap("era") (["13TeV"], 1.07))
cb.cp().process(["TTbar"]).AddSyst(cb, "CMS_norm_tt", "lnN",ch.SystMap("era") (["13TeV"], 1.055))
cb.cp().process(["Others"]).AddSyst(cb, "CMS_norm_o", "lnN",ch.SystMap("era") (["13TeV"], 1.07))
cb.cp().process(allMC).AddSyst(cb, "Weight_pu",     "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_mu",     "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_pho",    "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_ele",    "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_btag_b", "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_btag_l", "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_prefire","shape",ch.SystMap("era") (["13TeV"], 1.0))
#cb.cp().process(allMC).AddSyst(cb, "Weight_q2",     "shape",ch.SystMap("era") (["13TeV"], 1.0))
#cb.cp().process(allMC).AddSyst(cb, "Weight_pdf",    "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_isr",    "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_fsr",    "shape",ch.SystMap("era") (["13TeV"], 1.0))
#------------------
#Add rateParam
#------------------
##cb.cp().process(["TTbar"]).bin([hName]).AddSyst(cb, 'TTbarSF', 'rateParam', ch.SystMap()(1.0))
#------------------
#Add syst groups
#------------------
cb.SetGroup("mySyst", ["lumi_13TeV", "Weight_pu"]) 
#------------------
#Add autoMCStat
#------------------
cb.SetAutoMCStats(cb, 0, True, 1)
#------------------
#Get shape hists
#------------------
cb.cp().backgrounds().ExtractShapes(inFileName, inHistDirBase, inHistDirSys)
cb.cp().signals().ExtractShapes(inFileName, inHistDirBase, inHistDirSys)
cb.WriteDatacard(datacardPath, outFilePath) 
#------------------
#print various info
#------------------
#print cb.PrintAll()
#print cb.PrintObs();
#print cb.PrintProcs();
#print cb.PrintSysts();
#print cb.PrintParams();
print datacardPath
print outFilePath

#------------------
#Add param
#------------------
#dc = open(datacardPath, "a")
#dc.write("TTbarSF \t param \t 1.0 \t 0.05\n")
#dc.write("WGSF    \t param \t 1.0 \t 0.10\n")
#dc.write("ZGSF    \t param \t 1.0 \t 0.10\n")
#dc.close()

#------------------------
#Save DC path in a file
#------------------------
name  = "DC_%s_%s_%s_%s_%s_mH%s"%(year, decayMode, channel, region, hName, mass)
if not os.path.exists("./DataCards.json"):
    with open("DataCards.json", "w") as f:
        data = {}
        json.dump(data, f)
with open ('DataCards.json') as jsonFile:
    jsonData = json.load(jsonFile)
jsonData[name] = []
jsonData[name].append(datacardPath)
with open ('DataCards.json', 'w') as jsonFile:
    json.dump(jsonData, jsonFile)
