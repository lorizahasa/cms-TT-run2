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
parser.add_option("--level", "--level", dest="level", default="",type='str',
                     help="Specify up/down of systematic")
parser.add_option("--syst", "--systematic", dest="systematic", default="JetBase",type='str',
                     help="Specify which systematic to run on")
parser.add_option("--mass", "--mass", dest="sigMass", default="800",type='str', 
                     help="mass of the signal sample")
parser.add_option("--method", "--method", dest="methodMVA", default="BDTP",type='str', 
                     help="Which MVA method to be used")
(options, args) = parser.parse_args()
year = options.year
decayMode = options.decayMode
channel = options.channel
region = options.region
syst = options.systematic
level =options.level
mass = options.sigMass
method = options.methodMVA
print parser.parse_args()

#-----------------------------------------
#INPUT AnalysisNtuples Directory
#----------------------------------------
package = "TMVA"
dirNtuple = "root://cmseos.fnal.gov//store/user/rverma/Output/cms-TT-run2/Ntuple_Skim/"
dirFile = "%s/%s/%s"%(year, decayMode, syst) 
sigFile = "Semilep_JetBase__TstarTstarToTgammaTgluon_M%s_2016_Ntuple.root"%mass
inputFileS = ROOT.TFile.Open("%s/%s/%s"%(dirNtuple, dirFile, sigFile))
sig = inputFileS.Get("AnalysisTree")

allSamples = getSamples(year, decayMode, syst)
bkgList = []
for s in allSamples.keys():
    if "TT_tytg" not in s and "Data" not in s:
        bkgs = allSamples[s]
        print("%s, files: %s"%(s, len(bkgs)))
        for b in bkgs:
            bkgList.append(b)
bkgList = ["Semilep_JetBase__TTGamma_SingleLept_2016_Ntuple.root"]
print("\nTotal files from all bkgs = %s"%len(bkgList))

bkg = ROOT.TChain("AnalysisTree")
for b in bkgList:
    bkg.Add("%s/%s/%s"%(dirNtuple, dirFile, b))
print(bkg.GetEntries())


loader = ROOT.TMVA.DataLoader("dataset")
sigWeight = 1.0
bkgWeight = 1.0
loader.AddSignalTree(sig, sigWeight)
loader.AddBackgroundTree(bkg, bkgWeight)

varDict = GetVarInfo()
print("\nTotal vars = %s \n"%len(varDict.keys()))
for var in varDict.keys():
    print(varDict[var][0])
    loader.AddVariable(varDict[var][0], 'F')

loader.SetSignalWeightExpression("Weight_lumi")
loader.SetBackgroundWeightExpression("Weight_lumi")

#evtSel = ROOT.TCut("pt_j1 > 50")
if "u" in channel: 
    evtSel = ROOT.TCut("Event_pass_presel_mu && %s"%Regions[region])
else:
    evtSel = ROOT.TCut("Event_pass_presel_ele && %s"%Regions[region])
loader.PrepareTrainingAndTestTree(evtSel,"SplitMode=Random:!V")

m = method
print("Method: %s"%m)
ROOT.TMVA.Tools.Instance()
## For PYMVA methods
ROOT.TMVA.PyMethodBase.PyInitialize();
outputFile = ROOT.TFile.Open("%s_Classification.root"%(package), "RECREATE")
factory = ROOT.TMVA.Factory("%s_Classification_%s"%(package, mass), outputFile,
                      "!V:ROC:!Silent:Color:!DrawProgressBar:AnalysisType=Classification" )
factory.BookMethod(loader, methodList[m][0], m, methodList[m][1])
factory.TrainAllMethods();
factory.TestAllMethods();
factory.EvaluateAllMethods();

ROOT.gROOT.SetBatch(True)
roc = factory.GetROCCurve(loader);
roc.Write()
outputFile.Close()
