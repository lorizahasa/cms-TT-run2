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
import multiprocessing

package = "TMVA"
#-----------------------------------------
#INPUT Command Line Arguments 
#----------------------------------------
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-y", "--year", dest="year", default="2016Pre",type='str',
                     help="Specifyi the year of the data taking" )
parser.add_option("-d", "--decay", dest="decay", default="Semilep",type='str',
                     help="Specify which decay moded of ttbar Semilep or Dilep? default is Semilep")
parser.add_option("-c", "--channel", dest="channel", default="Mu",type='str',
                     help="Specify which channel Mu or Ele? default is Mu" )
parser.add_option("-s", "--sample", dest="sample", default="SignalSpin32_M800",type='str',
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
print(parser.parse_args())

#-----------------------------------------
#I/O Ntuples/Disc Directory
#----------------------------------------
systDir = "JetBase"
if "JE" in syst:
    systDir = syst
    syst = syst.replace("_up", "Up")
    syst = syst.replace("_down", "Down")
if "data" in sample:
    systDir = "JetBase"
inDirNtuple = "root://cmseos.fnal.gov/%s"%dirNtuple
dirFile = "%s/%s/%s"%(year, decay, systDir) 
print(dirFile)
allSamples = getSamples(year, decay, systDir)

#----------------------------------------
#Path of the I/O histograms/datacards
#----------------------------------------
inFileName = "%s_Classification_%s.weights.xml"%(package, method)
inFileDir = "%s/Classification/%s/%s/%s/CombMass/%s/%s/weights"%(dirClass, year, decay, channel, method, region.replace("CR", "SR"))#Evaluation in CR from SR's xml file
outFileDir      = "./discs/Reader/%s/%s/%s/CombMass/%s"%(year, decay, channel, method)
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
print("\nRunning for sample: %s\n"%sample_) 
def evalTree(sList, i):
    #Print 1% of events each time
    isPrint = False
    tree = ROOT.TChain("AnalysisTree")
    for s in sList:
        tree.Add("%s/%s/%s"%(inDirNtuple, dirFile, s))
        print("%s/%s: %s"%(dirFile, s, tree.GetEntries()))
    nEnt = tree.GetEntries()
    print("%s, Entries = %s "%(sList, nEnt))

    outFileFullPath = "%s/%s_%s_job_%s.root"%(outFileDir, region, syst, i)
    outputFile = ROOT.TFile(outFileFullPath, "RECREATE")
    print("The histogram directory inside the root file is", histDirInFile) 
    for ievt, e in enumerate(tree):
        eventSel = int(eval(selStr))
        #print(ievt, eventSel)
        if eventSel>0:
            evtWeights = "%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s*%s"%(w_lumi,w_pu,w_mu,w_ele,w_q2,w_pdf,w_isr,w_fsr,w_btag,w_prefire,w_pho,w_ttag)
            if "data" in sample_:
                evtWeights = "1.0"
            else: 
                if "DYJets" in sample:
                    sf = str(dictSFs[year][0])
                    evtWeights = "%s*%s"%(evtWeights, sf)
                isMisID = eval("e.Photon_misid_ele[0]")
                if isMisID>0: 
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
                eval("dictHist[\"%s\"].Fill(e.%s, %s)"%(var, vars[var][0], evtWt))
            disc = reader.EvaluateMVA(method)
            exec("dictHist[\"Disc\"].Fill(%s, %s)"%(disc, evtWt))
            if isCut and disc>0:
                for var in vars.keys():
                    #exec("h%s_cut.Fill(e.%s, e.Weight_lumi)"%(var, vars[var][0]))
                    pass

        if(nEnt> 100):
            isPrint = int(ievt%(int(nEnt/100)) == 1)
        else:
            isPrint = True
        if isPrint:
            totalTime = time.time() - start_time
            sec_ = (int)(totalTime)%60
            min_ = int(totalTime/60)
            print('    %s%s   %sm %ss'%(int(100*ievt/nEnt), "%", min_, sec_))
            
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
 
# Create a list to store the processes or threads
processes = []
fMulti = split_list(allSamples[sample_], nMulti)
haddIn_ = []
for i, s_ in enumerate(fMulti):
    process = multiprocessing.Process(target=evalTree, args=(s_,i,))
    processes.append(process)
    process.start()
    o_ = "%s/%s_%s_job_%s.root"%(outFileDir, region, syst, i)
    haddIn_.append(o_)

# Wait for all processes or threads to finish
for process in processes:
    process.join()
print("All processes or threads finished.")

haddIn = ' '.join(i_ for i_ in haddIn_)
haddOut = "%s/%s_%s_%s.root"%(outFileDir, sample, region, syst)
os.system("hadd -f %s %s"%(haddOut, haddIn))
os.system("rm %s"%weightFile)
for i_ in haddIn_:
    os.system("rm %s"%i_)
print("--- Total time: %sm %ss ---" %(int((time.time() - start_time)/60), int((time.time() - start_time)%60)))
