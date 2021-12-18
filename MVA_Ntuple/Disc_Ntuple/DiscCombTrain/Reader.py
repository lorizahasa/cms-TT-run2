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
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched_SR",type='str', 
                     help="which control selection and region"), 
parser.add_option("--level", "--level", dest="level", default="",type='str',
                     help="Specify up/down of systematic")
parser.add_option("--syst", "--systematic", dest="systematic", default="Base",type='str',
                     help="Specify which systematic to run on")
parser.add_option("--method", "--method", dest="methodMVA", default="BDTP",type='str', 
                     help="Which MVA method to be used")
parser.add_option("--isCheck", "--isCheck", dest="isCheck", action="store_true", default=False, help="")
(options, args) = parser.parse_args()
year = options.year
decayMode = options.decayMode
channel = options.channel
sample = options.sample
region = options.region
syst = options.systematic
level =options.level
method = options.methodMVA
isCheck = options.isCheck
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

outFileMainDir = "./discs"
outputFile = ROOT.TFile("%s_Reader.root"%(package),"RECREATE")
ROOT.gROOT.SetBatch(True)

#-----------------------------------------
#TMVA specific
#-----------------------------------------
package = "TMVA"
weightfile = "dataset/weights/%s_Classification_%s.weights.xml"%(package, method)
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
reader.BookMVA(method, weightfile)


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
#Final output Linux and ROOT directories
#----------------------------------------
if not os.path.exists(outFileFullDir):
    os.makedirs(outFileFullDir)
outFileFullPath = "%s/%s_%s_%s.root"%(outFileFullDir, sample, region, variation)
outputFile = ROOT.TFile(outFileFullPath, "RECREATE")
print("The histogram directory inside the root file is", histDirInFile) 

#-----------------------------------------
#Declare histograms
#-----------------------------------------
nBins, xMin, xMax = 25, -1, 1
if method in ["DNN", 'MLP']: xMin, xMax = 0, 1 
if method in ['PDEFoam']: nBins, xMin, xMax = 4, -2, 2 
dictHist = {}
dictHist["Disc"] = ROOT.TH1D("Disc","Disc",nBins, xMin, xMax)
for var in vars.keys():
    nBins  = vars[var][1][0]
    xMin   = vars[var][1][1]
    xMax   = vars[var][1][2]
    #cuts = ["", "_cut"]
    cuts = [""]
    for cut in cuts:
        hist = 'ROOT.TH1D("%s%s", "%s%s", %s, %s, %s)'%(var, cut, var, cut, nBins, xMin, xMax)
        exec("h%s%s = %s"%(var, cut, hist))
        exec("dictHist[\"%s\"] = h%s%s"%(var, var, cut))

#-----------------------------------------
#Fill hists for signal
#-----------------------------------------
print("\nRunning for sample: %s\n"%sample_) 
tree = ROOT.TChain("AnalysisTree")
for s in allSamples[sample_]:
    tree.Add("%s/%s/%s"%(dirNtuple, dirFile, s))
print("%s, Entries = %s "%(sample_, tree.GetEntries()))

for ievt, e in enumerate(tree):
    eventSel = int(e.Event_pass_presel_mu and ((e.Jet_size>=5 and e.FatJet_size==0) or (e.Jet_size>=2 and e.FatJet_size==1))  and e.Jet_b_size >=1 and e.Photon_size==1 and e.Photon_et[0] > 100)
    if eventSel>0:
        for var in vars.keys():
            exec("%s[0] = e.%s"%(var, vars[var][0]))
            exec("dictHist[\"%s\"].Fill(e.%s, e.Weight_lumi)"%(var, vars[var][0]))
        disc = reader.EvaluateMVA(method)
        exec("dictHist[\"Disc\"].Fill(%s, e.Weight_lumi)"%disc)
        if disc>0:
            for var in vars.keys():
                #exec("h%s_cut.Fill(e.%s, e.Weight_lumi)"%(var, vars[var][0]))
                pass
        if (ievt%100)==0:
            print('Event = %i/%i, Disc = %s'%(ievt, tree.GetEntries(), disc))

#-----------------------------------------
#Rebin and write discs and hists
#-----------------------------------------
dictRebin = {}

phoArray = np.array([(i)*100 for i in range(15)])
stArray  = np.array([(i)*250 for i in range(20)])
massArray = np.array([(i)*100 for i in range(20)])
massArrayTT = np.array([(2*i)*100 for i in range(25)])

dictRebin["Reco_mass_T"] = np.concatenate((massArray, np.array([2200.,2500,3000,6000.])))
dictRebin["Reco_mass_TT"] = np.concatenate((massArrayTT, np.array([5500.,6500,9000.])))
dictRebin["Reco_ht"]     = np.concatenate((stArray, np.array([5000,6000.,9000.])))
dictRebin["Reco_st"]     = np.concatenate((stArray, np.array([5000,5500,6500.,9000.])))
dictRebin["Photon_et"]   = np.concatenate((phoArray, np.array([1700,2000.,2500.])))

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
    hName = h.GetName()
    if hName in dictRebin.keys():
        hNew = h.Rebin(len(dictRebin[hName])-1, hName, dictRebin[hName]) 
        hNew.Write()
    else:
        h.Write()
print("Path of output root file:\n%s/%s"%(os.getcwd(), outFileFullPath))
outputFile.Close()

