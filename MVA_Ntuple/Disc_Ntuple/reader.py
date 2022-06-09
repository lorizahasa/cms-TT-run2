import ROOT
import os
import sys
sys.dont_write_bytecode = True
import numpy as np
from array import array
import time
start_time = time.time()
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
parser.add_option("-y", "--year", dest="year", default="2016PreVFP",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decay", dest="decay", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="Signal_M800",type='str',
                     help="Specify which sample to run on" )
parser.add_option("-r", "--region", dest="region", default="ttyg_Enriched_SR_Resolved",type='str', 
                     help="which control selection and region"), 
parser.add_option("--syst", "--systematic", dest="systematic", default="Base",type='str',
                     help="Specify which systematic to run on")
parser.add_option("--method", "--method", dest="method", default="BDTA",type='str', 
                     help="Which MVA method to be used")
parser.add_option("--isCut", "--isCut", dest="isCut", action="store_true", default=False, help="")
(options, args) = parser.parse_args()
year = options.year
decay = options.decay
channel = options.channel
sample = options.sample
region = options.region
syst = options.systematic
method = options.method
isCut     = options.isCut
print parser.parse_args()

#-----------------------------------------
#I/O Ntuples/Disc Directory
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
if "data" in sample:
    systDir = "JetBase"
inDirNtuple = "root://cmseos.fnal.gov/%s"%dirNtuple
dirFile = "%s/%s/%s"%(year, decay, systDir) 
allSamples = getSamples(year, decay, systDir)

#----------------------------------------
#Path of the I/O histograms/datacards
#----------------------------------------
inFileName = "%s_Classification_%s.weights.xml"%(package, method)
inFileDir = "%s/Classification/%s/%s/%s/CombMass/%s/%s/weights"%(dirClass, year, decay, channel, method, region.replace("CR", "SR"))#Evaluation in CR from SR's xml file
outFileDir      = "./discs/Read/Reader/%s/%s/%s/CombMass/%s"%(year, decay, channel, method)
os.system("mkdir -p %s"%outFileDir)
print(inFileDir)
print(outFileDir)
method = options.method
os.system("xrdcp -rf root://cmseos.fnal.gov/%s/%s %s"%(inFileDir, inFileName, outFileDir))
weightFile = "%s/weights/%s"%(outFileDir, inFileName)

#-----------------------------------------
#TMVA specific
#-----------------------------------------
ROOT.gROOT.SetBatch(True)
package = "TMVA"
ROOT.TMVA.Tools.Instance()
reader = ROOT.TMVA.Reader("!Color:!Silent")
vars = GetVarInfo(region, channel)
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
w_pho ="Weight_pho[0]"
w_ttag="Weight_ttag"
histDirInFile = "%s/%s/Base"%(sample, region)
sample_ = sample
if "data" in sample or "QCD" in sample:
    sample_ = "%s%s"%(sample, channel)

#-----------------------------------------
#For Systematics
#----------------------------------------
if not syst=="Base":
    histDirInFile = "%s/%s/%s"%(sample, region, syst) 
    #Remove me ----------
    syst = syst.replace("Up", "_up")
    syst = syst.replace("Down", "_down")
    #--------------------
    print("Running for systematics: ", syst)
    if "Weight_pu"  in syst: w_pu = syst 
    if "Weight_q2"  in syst: w_q2 = syst 
    if "Weight_pdf" in syst: w_pdf = syst 
    if "Weight_mu"  in syst: w_mu = syst 
    if "Weight_ele" in syst: w_ele = syst 
    if "Weight_pho" in syst: w_pho = "%s[0]"%syst 
    if "Weight_fsr" in syst: w_fsr = syst 
    if "Weight_isr" in syst: w_isr = syst 
    if "Weight_prefire" in syst: w_prefire = syst 
    if "Weight_btag" in syst: w_btag = syst 
    if "Weight_ttag" in syst: w_ttag = syst 

#----------------------------------------
#Final output Linux and ROOT directories
#----------------------------------------
if not os.path.exists(outFileDir):
    os.makedirs(outFileDir)
#Remove me ----------
syst = syst.replace("_up", "Up")
syst = syst.replace("_down", "Down")
#--------------------
outFileFullPath = "%s/%s_%s_%s.root"%(outFileDir, sample, region, syst)
outputFile = ROOT.TFile(outFileFullPath, "RECREATE")
print("The histogram directory inside the root file is", histDirInFile) 

#-----------------------------------------
#Declare histograms
#-----------------------------------------
nBins, xMin, xMax = 100, -1, 1
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
    print("%s/%s/%s"%(inDirNtuple, dirFile, s))
    tree.Add("%s/%s/%s"%(inDirNtuple, dirFile, s))
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

totalTime = 0
for ievt, e in enumerate(tree):
    exec("eventSel = int(%s)"%selStr)
    #print(ievt, eventSel)
    if eventSel>0:
        evtWeights = "%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s"%(w_lumi,w_pu,w_mu,w_ele,w_q2,w_pdf,w_isr,w_fsr,w_btag,w_prefire,w_pho,w_ttag)
        if "data" in sample_:
            evtWeights = "1.0"
        else: 
            if "DYJets" in sample:
                sf = str(dictSFs[year][0])
                evtWeights = "%s*%s"%(evtWeights, sf)
            #if e.Photon_misid_ele[0]>0: 
            if False: #FIXME 
                sf = str(dictSFs[year][1])
                evtWeights = "%s*%s"%(evtWeights, sf)
            else:
                if "ZGamma" in sample:
                    sf = str(dictSFs[year][2])
                    evtWeights = "%s*%s"%(evtWeights, sf)
                if "WGamma" in sample:
                    sf = str(dictSFs[year][3])
                    evtWeights = "%s*%s"%(evtWeights, sf)
        evtWt = evtWeights.replace("Weight", "e.Weight")
        
        #Fill the histogram
        for var in vars.keys():
            exec("%s[0] = e.%s"%(var, vars[var][0]))
            exec("dictHist[\"%s\"].Fill(e.%s, %s)"%(var, vars[var][0], evtWt))
        disc = reader.EvaluateMVA(method)
        exec("dictHist[\"Disc\"].Fill(%s, %s)"%(disc, evtWt))
        if isCut and disc>0:
            for var in vars.keys():
                #exec("h%s_cut.Fill(e.%s, e.Weight_lumi)"%(var, vars[var][0]))
                pass

    #Print 1% of events each time
    isPrint = False
    if(tree.GetEntries()> 100):
        isPrint = (ievt%(tree.GetEntries()/100) == 0)
    else:
        isPrint = True
    if isPrint:
        totalTime = time.time() - start_time
        sec_ = (int)(totalTime)%60
        min_ = (int)(totalTime)/60
        print('Event = %s%s %10sm %ss'%(100*ievt/tree.GetEntries(), "%", min_, sec_))
        
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
print("--- %s seconds ---" % (time.time() - start_time))
