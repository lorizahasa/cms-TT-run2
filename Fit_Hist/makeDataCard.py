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
parser.add_option("--hist", "--hist", dest="hName", default="presel_TopStar_mass",type='str', 
                     help="which histogram to be used for making datacard")
parser.add_option("--cr", "--CR", dest="CR", default="",type='str', 
                     help="which control selection and region")
parser.add_option("--isQCDMC","--qcdMC",dest="isQCDMC", default=False, action="store_true",
		  help="")
(options, args) = parser.parse_args()
year            = options.year
decayMode  = options.decayMode
channel         = options.channel
mass            = options.mass
hName        = options.hName
CR   = options.CR
isQCDMC        = options.isQCDMC

#-----------------------------------------
#Path of the I/O histograms/datacards
#----------------------------------------
inFileName = "%s/%s/%s/%s/Merged/AllInc.root"%(condorHistDir, year, decayMode, channel)
print inFileName
if CR=="":
    inHistDirBase   = "$PROCESS/Base/SR/$BIN"
    inHistDirSys    = "$PROCESS/$SYSTEMATIC/SR/$BIN"
    outFileDir      = "%s/Fit_Hist/%s/%s/%s/%s/SR/mH%s"%(condorCBADir, year, decayMode, channel, hName, mass)
else:
    inHistDirBase   = "$PROCESS/Base/CR/%s/$BIN"%CR
    inHistDirSys    = "$PROCESS/$SYSTEMATIC/CR/%s/$BIN"%CR
    outFileDir      = "%s/Fit_Hist/%s/%s/%s/%s/CR/%s/mH%s"%(condorCBADir, year, decayMode, channel, hName, CR, mass)

outFilePath     = "%s/Shapes_Inc.root"%(outFileDir)
datacardPath    = "%s/Datacard_Inc.txt"%(outFileDir)
if not os.path.exists(outFileDir):
    os.makedirs(outFileDir)

#-----------------------------------
# Make datacard 
#-----------------------------------
cb = ch.CombineHarvester()
#cb.SetVerbosity(4)
#AllBkgs = ["TTbar", "Wjets", "ZJets", "Diboson", "SingleTop", "TTV","QCD"]
AllBkgs = ["TTGamma", "TTbar", "SingleTop"] 
Signal  = ["TT_tgtg_M%s"%mass]
allMC   = Signal + AllBkgs
#------------------
#Add observed data
#------------------
cb.AddObservations(["*"],["hcs"],["13TeV"],[channel],[(-1, hName)])
#------------------
#Add sig& bkgs
#------------------
cb.AddProcesses(["*"],["hcs"],["13TeV"],[channel],Signal,[(-1, hName)], True)
cb.AddProcesses(["*"],["hcs"],["13TeV"],[channel],AllBkgs,[(-1, hName)], False)
#------------------
#Add systematics
#------------------
cb.cp().process(allMC).AddSyst(cb, "lumi_$ERA", "lnN",ch.SystMap("era") (["13TeV"], 1.025))
cb.cp().process(allMC).AddSyst(cb, "BTagSF_b" , "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "BTagSF_l" , "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "PU"       , "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "EleEff"   , "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "MuEff"   , "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Pdf"   , "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Q2"   , "shape",ch.SystMap("era") (["13TeV"], 1.0))
#------------------
#Add rateParam
#------------------
##cb.cp().process(["TTbar"]).bin([hName]).AddSyst(cb, 'TTbarSF', 'rateParam', ch.SystMap()(1.0))
#------------------
#Add syst groups
#------------------
cb.SetGroup("mySyst", ["lumi_13TeV", "BTagSF_b", "BTagSF_l", "PU"])
#cb.SetGroup("otherSyst", ["TTBarSF", "WGSF", "ZGSF", "PhoEff"])
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
if CR=="":
    name  = "DC_%s_%s_%s_%s_SR_mH%s"%(year, decayMode, channel, hName, mass)
else:
    name  = "DC_%s_%s_%s_%s_CR_%s_mH%s"%(year, decayMode, channel, hName, CR, mass)
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
