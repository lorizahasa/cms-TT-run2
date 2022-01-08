import ROOT

import os
import sys
sys.path.insert(0, "%s/%s"%(os.getcwd(), "sample"))
from SampleInfo import getSamples
from DiscInputs import *
from VarInfo import GetVarInfo

#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decay", dest="decayMode", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched_SR",type='str', 
                     help="which control selection and region"), 
parser.add_option("-m", "--mass", dest="mass", default="800",type='str',
                     help="Specify the mass of charged Higgs")
parser.add_option("--method", "--method", dest="methodMVA", default="BDTG",type='str', 
                     help="Which MVA method to be used")
parser.add_option("--syst", "--systematic", dest="systematic", default="JetBase",type='str',
                     help="Specify which systematic to run on")
parser.add_option("--level", "--level", dest="level", default="",type='str',
                     help="Specify up/down of systematic")
parser.add_option("--isCheck", "--isCheck", dest="isCheck", action="store_true", default=False, help="")
parser.add_option("--isSep", "--isSep", dest="isSep", action="store_true", default=False, help="")
(options, args) = parser.parse_args()
year        = options.year
decayMode   = options.decayMode
channel     = options.channel
region      = options.region
syst        = options.systematic
level       = options.level
mass        = options.mass
method      = options.methodMVA
isCheck     = options.isCheck
isSep       = options.isSep
print parser.parse_args()

#-----------------------------------------
#INPUT AnalysisNtuples Directory
#----------------------------------------
package = "TMVA"
dirNtuple = "root://cmseos.fnal.gov//store/user/rverma/Output/cms-TT-run2/Ntuple_Skim/"
dirFile = "%s/%s/%s"%(year, decayMode, syst) 
allSamples = getSamples(year, decayMode, syst)

if isSep:
    outDir = "discs/Class/Classification/%s/%s/%s/%s/%s/%s"%(year, decayMode, channel, mass, method,region)
else:
    outDir = "discs/Class/Classification/%s/%s/%s/CombMass/%s/%s"%(year, decayMode, channel, method, region)

os.system("mkdir -p %s"%outDir)
os.system("mkdir -p %s/plots"%outDir)
sigList = []
bkgList = []
for s in allSamples.keys():
    if 'TT_tytg' in s:
        sigs = allSamples[s]
        for sigF in sigs:
            sigList.append(sigF)
    else:
        if "Data" not in s:
            bkgs = allSamples[s]
            print("%s, files: %s"%(s, len(bkgs)))
            for bkgF in bkgs:
                bkgList.append(bkgF)
if isCheck:
    bkgList = ["Semilep_JetBase__TTGamma_SingleLept_2016_Ntuple.root"]

#-----------------------------------------
#Add trees in the TChain
#----------------------------------------
sigTree = ROOT.TChain("AnalysisTree")
if isSep:
    sigs = allSamples["TT_tytg_M%s"%mass]
    for sigF in sigs:
        sigTree.Add("%s/%s/%s"%(dirNtuple, dirFile, sigF))
else:
    for s in sigList:
        sigTree.Add("%s/%s/%s"%(dirNtuple, dirFile, s))
bkgTree = ROOT.TChain("AnalysisTree")
for b in bkgList:
    bkgTree.Add("%s/%s/%s"%(dirNtuple, dirFile, b))
print(sigList)
print("Total files from all bkgs = %s, Entries = %s "%(len(bkgList), bkgTree.GetEntries()))
print("Total files from all sigs = %s, Entries = %s "%(len(sigList), sigTree.GetEntries()))

#-----------------------------------------
#Load variables and apply event weights
#----------------------------------------
loader = ROOT.TMVA.DataLoader(outDir)
sigWeight = 1.0
bkgWeight = 1.0
loader.AddSignalTree(sigTree, sigWeight)
loader.AddBackgroundTree(bkgTree, bkgWeight)

varDict = GetVarInfo()
print("\nTotal vars = %s \n"%len(varDict.keys()))
for var in varDict.keys():
    print(varDict[var][0])
    loader.AddVariable(varDict[var][0], 'F')

#evtWeights = "Weight_lumi*Weight_pu*Weight_mu*Weight_ele*Weight_prefire*Weight_btag*Weight_pho[0]"
evtWeights = "Weight_lumi*Weight_mu*Weight_ele*Weight_prefire*Weight_btag*Weight_pho[0]"
loader.SetSignalWeightExpression(evtWeights)
loader.SetBackgroundWeightExpression(evtWeights)

#-----------------------------------------
#Apply event selection
#----------------------------------------
#evtSel = ROOT.TCut("pt_j1 > 50")
if "u" in channel: 
    selStr = "Event_pass_presel_mu && %s"%Regions[region]
else:
    selStr = "Event_pass_presel_ele && %s"%Regions[region]
print(selStr)
evtSel = ROOT.TCut(selStr.replace("e.", ""))
loader.PrepareTrainingAndTestTree(evtSel,"SplitMode=Random:!V")

#-----------------------------------------
#Do classification
#----------------------------------------
m = method
print("Method: %s"%m)
ROOT.TMVA.Tools.Instance()
## For PYMVA methods
ROOT.TMVA.PyMethodBase.PyInitialize()
fName ="%s/%s_Classification.root"%(outDir, package)
outputFile = ROOT.TFile.Open(fName, "RECREATE")
factory = ROOT.TMVA.Factory("%s_Classification"%(package), outputFile,
                      "!V:ROC:!Silent:Color:!DrawProgressBar:AnalysisType=Classification" )
factory.BookMethod(loader, methodDict[m][0], m, methodDict[m][1])
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

#-----------------------------------------
#Grab AUC and write to a text file
#----------------------------------------
ROOT.gROOT.SetBatch(True)
roc = factory.GetROCCurve(loader)
roc.Write()
auc = factory.GetROCIntegral(loader, m)
auc_ = "Year = %s\nDecay = %s\nChannel = %s\nRegion = %s\nMethod = %s\nAUC = %s"%(year, decayMode, channel, region, m, auc)
print("RESULT:%s,%s,%s,%s,%s,%s"%(year, decayMode, channel, region, m, auc))
aucFile = open("./%s/AUC.txt"%outDir, "w")
aucFile.write(auc_)
aucFile.close()
outputFile.Close()

#------------------------------------------
#Grab basic plots from the output of TMVA
#------------------------------------------
ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libTMVAGui")
ROOT.TMVA.variables(outDir,fName)
ROOT.TMVA.mvas(outDir,fName)
ROOT.TMVA.mvas(outDir,fName, ROOT.TMVA.kCompareType)
ROOT.TMVA.efficiencies(outDir,fName)
ROOT.TMVA.correlations(outDir,fName)

