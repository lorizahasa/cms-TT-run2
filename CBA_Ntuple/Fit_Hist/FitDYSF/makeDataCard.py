import os
import sys
import json
import itertools
from optparse import OptionParser
from ROOT import TFile, TH1F, gDirectory
import CombineHarvester.CombineTools.ch as ch
sys.dont_write_bytecode = True
from FitInputs import *

#-----------------------------------------
#INPUT command-line arguments 
#----------------------------------------
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016Pre",type='str',
                     help="Specify the year of the data taking" )
parser.add_option("-d", "--decay", dest="decay", default="Dilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
		  help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("--hist", "--hist", dest="hName", default="Reco_mass_dilep",type='str', 
                     help="which histogram to be used for making datacard")
parser.add_option("-r", "--region", dest="region", default="DY_Enriched_e3j_e0b_e0y",type='str', 
                     help="which control selection and region") 
(options, args) = parser.parse_args()
year            = options.year
decay           = options.decay
channel         = options.channel
region          = options.region
hName           = options.hName

#-----------------------------------------
#Path of the I/O histograms/datacards
#----------------------------------------
#dir_ = "Merged"
#dir_ = "Rebin"
dir_        = "ForDYSF"
ydc         = "%s/%s/%s"%(year, decay, channel)
inFile      = "AllInc.root"
inFileDir   = "%s/%s/%s"%(dirHist, dir_, ydc)
outFileDir  = "%s/%s/%s/%s"%(dirFit, ydc, region, hName)
os.system("mkdir -p %s"%outFileDir)
inFileName  = "%s/%s"%(outFileDir, inFile)#We copy the input file here
print(inFileDir)
os.system("xrdcp -f root://cmseos.fnal.gov/%s/%s %s"%(inFileDir, inFile, outFileDir))
print(outFileDir)
inHistDirBase   = "$PROCESS/%s/Base/$BIN"%region
inHistDirSys    = "$PROCESS/%s/$SYSTEMATIC/$BIN"%region

outFilePath     = "%s/Shapes.root"%(outFileDir)
datacardPath    = "%s/Datacard_Alone.txt"%(outFileDir)

#-----------------------------------
# Make datacard 
#-----------------------------------
cb = ch.CombineHarvester()
#cb.SetVerbosity(4)
AllBkgs = ["OtherBkgs"]
Signal  = ["DYJets"]
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
cb.cp().process(allMC).AddSyst(cb, "Weight_ele",    "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_btag_l", "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_prefire","shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_isr",    "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_fsr",    "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_pu",     "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_mu",     "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_btag_b", "shape",ch.SystMap("era") (["13TeV"], 1.0))
#cb.cp().process(allMC).AddSyst(cb, "Weight_q2",     "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_jer",    "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_jes",    "shape",ch.SystMap("era") (["13TeV"], 1.0))
cb.cp().process(allMC).AddSyst(cb, "Weight_pdf",    "shape",ch.SystMap("era") (["13TeV"], 1.0))
#------------------
#Add rateParam
#------------------
##cb.cp().process(["TTbar"]).bin([hName]).AddSyst(cb, 'TTbarSF', 'rateParam', ch.SystMap()(1.0))
#------------------
#Add syst groups
#------------------
## cb.SetGroup("mySyst", ["lumi_13TeV", "Weight_pu"]) 
#------------------
#Add autoMCStat
#------------------
cb.SetAutoMCStats(cb, 0, True, 1)
#------------------
#Get shape hists
#------------------
cb.cp().backgrounds().ExtractShapes(inFileName, inHistDirBase, inHistDirSys)
cb.cp().signals().ExtractShapes(inFileName, inHistDirBase, inHistDirSys)
#f_ = TFile.Open(inFileName)
#print type(f_)
#cb.cp().backgrounds().ExtractShapes(f_, inHistDirBase, inHistDirSys)
#cb.cp().signals().ExtractShapes(f_, inHistDirBase, inHistDirSys)
cb.WriteDatacard(datacardPath, outFilePath) 
#------------------
#print various info
#------------------
#print(cb.PrintAll())
#print(cb.PrintObs())
#print(cb.PrintProcs())
#print(cb.PrintSysts())
#print(cb.PrintParams())
print(datacardPath)
print(outFilePath)

#------------------
#Add param
#------------------
#dc = open(datacardPath, "a")
#dc.write("TTbarSF \t param \t 1.0 \t 0.05\n")
#dc.write("WGSF    \t param \t 1.0 \t 0.10\n")
#dc.write("ZGSF    \t param \t 1.0 \t 0.10\n")
#dc.close()
