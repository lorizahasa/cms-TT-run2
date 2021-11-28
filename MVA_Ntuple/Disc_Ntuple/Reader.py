import ROOT
import os
import sys
import numpy as np
from array import array
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
parser.add_option("--mass", "--mass", dest="mass", default="800",type='str', 
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
mass = options.mass
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

weightfile = "dataset/weights/%s_Classification_%s_%s.weights.xml"%(package, mass, method)
ROOT.TMVA.Tools.Instance()
reader = ROOT.TMVA.Reader("!Color:!Silent")

vars = GetVarInfo()
#Convert strings to variables
for var in vars.keys():
    exec('%s = %s'%(var, array('f',[0])))
    print('%s = %s'%(var, eval(var)))
Weight_lumi = array('f',[0])

print("\nTotal vars = %s\n"%len(vars.keys()))
for var in vars.keys():
    reader.AddVariable(vars[var][0], eval(var))
reader.BookMVA(method, weightfile)

#Declare histograms
hSig_disc = ROOT.TH1D("Disc","Disc",25,-1,1)
hBkg_disc = ROOT.TH1D("Disc","Disc",25,-1,1)
for var in vars.keys():
    nBins  = vars[var][1][0]
    xMin   = vars[var][1][1]
    xMax   = vars[var][1][2]
    cut = ["", "_cut"]
    for cut in cut:
        histSig = 'ROOT.TH1D("%s%s", "%s%s", %s, %s, %s)'%(var, cut, var, cut, nBins, xMin, xMax)
        histBkg = 'ROOT.TH1D("%s%s", "%s%s", %s, %s, %s)'%(var, cut, var, cut, nBins, xMin, xMax)
        exec("hSig_%s%s = %s"%(var, cut, histSig))
        exec("hBkg_%s%s = %s"%(var, cut, histBkg))
        print("hBkg_%s%s = %s"%(var, cut, histBkg))

#Fill hists for signal
print("\nRunning for Sig...\n") 
for ievt, e in enumerate(sig):
    eventSel = int(e.Event_pass_presel_mu and ((e.Jet_size>=5 and e.FatJet_size==0) or (e.Jet_size>=2 and e.FatJet_size==1))  and e.Jet_b_size >=1 and e.Photon_size==1 and e.Photon_et[0] > 100)
    if eventSel>0:
        for var in vars.keys():
            exec("%s[0] = e.%s"%(var, vars[var][0]))
            exec("hSig_%s.Fill(e.%s, e.Weight_lumi)"%(var, vars[var][0]))
        disc = reader.EvaluateMVA(method)
        hSig_disc.Fill(disc, e.Weight_lumi)
        if disc>0:
            for var in vars.keys():
                exec("hSig_%s_cut.Fill(e.%s, e.Weight_lumi)"%(var, vars[var][0]))
                pass
        if (ievt%100)==0:
            print('Event = %i/%i, Disc = %s'%(ievt, sig.GetEntries(), disc))
            
#Fill hists for background
print("\nRunning for Bkg...\n")    
for ievt, e in enumerate(bkg):
    eventSel = int(e.Event_pass_presel_mu and ((e.Jet_size>=5 and e.FatJet_size==0) or (e.Jet_size>=2 and e.FatJet_size==1))  and e.Jet_b_size >=1 and e.Photon_size==1 and e.Photon_et[0] > 100)
    if eventSel>0:
        for var in vars.keys():
            exec("%s[0] = e.%s"%(var, vars[var][0]))
            exec("hBkg_%s.Fill(e.%s, e.Weight_lumi)"%(var, vars[var][0]))
        disc = reader.EvaluateMVA(method)
        hBkg_disc.Fill(disc, e.Weight_lumi)
        if disc>0:
            for var in vars.keys():
                exec("hBkg_%s_cut.Fill(e.%s, e.Weight_lumi)"%(var, vars[var][0]))
        if (ievt%1000)==0:
            progress = "%s%s"%(100*ievt/bkg.GetEntries(), "%")
            print('Event(%s) = %i/%i, Disc = %s'%(progress, ievt, bkg.GetEntries(), disc)) 


outputFile = ROOT.TFile("%s_Reader.root"%(package),"RECREATE")
CR = "ttyg_Enriched_SR"
dictRebin = {}

phoArray = np.array([(i)*100 for i in range(15)])
stArray  = np.array([(i)*250 for i in range(20)])
massArray = np.array([(i)*100 for i in range(20)])

dictRebin["Reco_mass_T"] = np.concatenate((massArray, np.array([2300.,3000,6000.])))
dictRebin["Reco_ht"]     = np.concatenate((stArray, np.array([5000,6000.,9000.])))
dictRebin["Reco_st"]     = np.concatenate((stArray, np.array([5000,6000.,9000.])))
dictRebin["Photon_et"]   = np.concatenate((phoArray, np.array([1700,2000.,2500.])))

def getHistDir(sample, sysType, CR):
    histDir = "%s/%s/%s"%(sample, CR, sysType)
    return histDir

def writeHist(hist, procDir, outputFile):
    outHistDir = getHistDir(procDir, "Base", CR)
    if not outputFile.GetDirectory(outHistDir):
        outputFile.mkdir(outHistDir)
    outputFile.cd(outHistDir)
    hName = hist.GetName()
    ROOT.gDirectory.Delete("%s;*"%(hName))
    print "%20s, %10s, %10s"%(hName, procDir, round(hist.Integral()))
    if hName in dictRebin.keys():
        hNew = hist.Rebin(len(dictRebin[hName])-1, hName, dictRebin[hName]) 
        hNew.Write()
    else:
        hist.Write()

writeList = []
writeList.append([hSig_disc, "Sig", "Base"])
writeList.append([hBkg_disc, "Bkg", "Base"])

for var in vars.keys():
    exec("writeList.append([hSig_%s, \"Sig\", \"Base\"])"%var)
    exec("writeList.append([hBkg_%s, \"Bkg\", \"Base\"])"%var)
    exec("writeList.append([hSig_%s_cut, \"Sig\", \"Base\"])"%var)
    exec("writeList.append([hBkg_%s_cut, \"Bkg\", \"Base\"])"%var)

for write in writeList:
    writeHist(write[0], write[1], outputFile)
    if "Bkg" in write[1]:
        writeHist(write[0], "data_obs", outputFile)
#outputFile.ls()
outputFile.Close()
