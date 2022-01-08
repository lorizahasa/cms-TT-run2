import ROOT
import os
import sys
import numpy as np
from array import array
sys.path.insert(0, "%s/%s"%(os.getcwd(), "sample"))
from SampleInfo import getSamples
from DiscInputs import *
from VarInfo import GetVarInfo

package = "TMVA"
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
parser.add_option("-s", "--sample", dest="sample", default="TT_tytg_M800",type='str',
                     help="Specify which sample to run on" )
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched_SR_Resolved",type='str', 
                     help="which control selection and region"), 
parser.add_option("--level", "--level", dest="level", default="",type='str',
                     help="Specify up/down of systematic")
parser.add_option("--syst", "--systematic", dest="systematic", default="Base",type='str',
                     help="Specify which systematic to run on")
parser.add_option("--method", "--method", dest="method", default="BDTG",type='str', 
                     help="Which MVA method to be used")
(options, args) = parser.parse_args()
year = options.year
decayMode = options.decayMode
channel = options.channel
sample = options.sample
region = options.region
syst = options.systematic
level =options.level
method = options.method
print parser.parse_args()

#-----------------------------------------
#I/O Ntuples/Disc Directory
#----------------------------------------
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
dirNtuple = "root://cmseos.fnal.gov//store/user/rverma/Output/cms-TT-run2/Ntuple_Skim/"
dirFile = "%s/%s/%s"%(year, decayMode, systDir) 
allSamples = getSamples(year, decayMode, systDir)

#-----------------------------------------
#Path of the I/O histograms/datacards
#----------------------------------------
inFileName = "%s_Classification_%s.weights.xml"%(package, method)
inFileDir = "%s/Classification/%s/%s/%s/CombMass/%s/%s/weights"%(condorOutDir, year, decayMode, channel, method, region)
outFileDir      = "./discs/Read/Reader/%s/%s/%s/CombMass/%s"%(year, decayMode, channel, method)
os.system("mkdir -p %s"%outFileDir)
print(inFileDir)
print(outFileDir)
method = options.method
os.system("xrdcp -rf root://cmseos.fnal.gov/%s/%s %s"%(inFileDir, inFileName, outFileDir))
weightFile = "%s/%s"%(outFileDir, inFileName)

#-----------------------------------------
#TMVA specific
#-----------------------------------------
ROOT.gROOT.SetBatch(True)
package = "TMVA"
ROOT.TMVA.Tools.Instance()
reader = ROOT.TMVA.Reader("!Color:!Silent")
vars = GetVarInfo()
#Convert strings to variables
for var in vars.keys():
    exec('%s = %s'%(var, array('f',[0])))
    #print('%s = %s'%(var, eval(var)))
Weight_lumi = array('f',[0])
print("\nTotal vars = %s\n"%len(vars.keys()))
for var in vars.keys():
    reader.AddVariable(vars[var][0], eval(var))
reader.BookMVA(method, weightFile)

#-----------------------------------------
#Systematic specific
#----------------------------------------
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
w_pho= "Weight_pho[0]"
histDirInFile = "%s/%s/Base"%(sample, region)
variation = "Base"
if "Data" in sample:
    histDirInFile = "data_obs/%s/Base"%(region)
sample_ = sample
if "Data" in sample or "QCD" in sample:
    sample_ = "%s%s"%(sample, channel)

#-----------------------------------------
#For up/down 
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
    print("Running for systematics", syst+level)
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
    elif 'Weight_pho' in syst:
        if levelUp:
            w_pho = "Weight_pho_up[0]"
        else:
            w_pho = "Weight_pho_down[0]"
    else:
        print "Running Jet Syst"

#evtWeights = "%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s"%(w_lumi,w_pu,w_mu,w_ele,w_q2,w_pdf,w_isr,w_fsr,w_btag,w_prefire, w_pho)
evtWeights = "%s*%s*%s*%s*%s*%s*%s*%s*%s*%s"%(w_lumi,w_mu,w_ele,w_q2,w_pdf,w_isr,w_fsr,w_btag,w_prefire, w_pho)

#-----------------------------------------
#Final output Linux and ROOT directories
#----------------------------------------
if not os.path.exists(outFileDir):
    os.makedirs(outFileDir)
outFileFullPath = "%s/%s_%s_%s.root"%(outFileDir, sample, variation, region)
outputFile = ROOT.TFile(outFileFullPath, "RECREATE")
print("The histogram directory inside the root file is", histDirInFile) 

#-----------------------------------------
#Declare histograms
#-----------------------------------------
nBins, xMin, xMax = 25, -1, 1
if method in ["DNN", 'MLP']: xMin, xMax = 0, 1 
if method in ['PDEFoam']: nBins, xMin, xMax = 4, -2, 2 
dictHist = {}
dictHist["Disc"] = ROOT.TH1F("Disc","Disc",nBins, xMin, xMax)
for var in vars.keys():
    nBins  = vars[var][1][0]
    xMin   = vars[var][1][1]
    xMax   = vars[var][1][2]
    #cuts = ["", "_cut"]
    cuts = [""]
    for cut in cuts:
        hist = 'ROOT.TH1F("%s%s", "%s%s", %s, %s, %s)'%(var, cut, var, cut, nBins, xMin, xMax)
        exec("h%s%s = %s"%(var, cut, hist))
        exec("dictHist[\"%s\"] = h%s%s"%(var, var, cut))

#-----------------------------------------
#Add all trees
#-----------------------------------------
print("\nRunning for sample: %s\n"%sample_) 
tree = ROOT.TChain("AnalysisTree")
for s in allSamples[sample_]:
    print("%s/%s/%s"%(dirNtuple, dirFile, s))
    tree.Add("%s/%s/%s"%(dirNtuple, dirFile, s))
print("%s, Entries = %s "%(sample_, tree.GetEntries()))

#-----------------------------------------
#Event selection and loop
#-----------------------------------------
if "u" in channel: 
    selStr = "e.Event_pass_presel_mu && %s"%Regions[region]
else:
    selStr = "e.Event_pass_presel_ele && %s"%Regions[region]
selStr = selStr.replace("&&", "and")
selStr = selStr.replace("||", "or")
print(selStr)

for ievt, e in enumerate(tree):
    exec("eventSel = int(%s)"%selStr)
    evtWt = evtWeights.replace("Weight", "e.Weight")
    #print(ievt, eventSel)
    if eventSel>0:
        for var in vars.keys():
            exec("%s[0] = e.%s"%(var, vars[var][0]))
            exec("dictHist[\"%s\"].Fill(e.%s, %s)"%(var, vars[var][0], evtWt))
        disc = reader.EvaluateMVA(method)
        exec("dictHist[\"Disc\"].Fill(%s, %s)"%(disc, evtWt))
        if disc>0:
            for var in vars.keys():
                #exec("h%s_cut.Fill(e.%s, e.Weight_lumi)"%(var, vars[var][0]))
                pass
        if (ievt%100)==0:
            print('Event = %i/%i, Disc = %s'%(ievt, tree.GetEntries(), disc))

#-----------------------------------
# Write final histograms in the file
#-----------------------------------
if not outputFile.GetDirectory(histDirInFile):
    outputFile.mkdir(histDirInFile)
outputFile.cd(histDirInFile)
print("Integral of Histogram =  %s"%dictHist["Disc"].Integral())
for h in dictHist.values():
    outputFile.cd(histDirInFile)
    #ROOT.gDirectory.Delete("%s;*"%(h.GetName()))
    h.Write()
print("Path of output root file:\n%s/%s"%(os.getcwd(), outFileFullPath))
outputFile.Close()

