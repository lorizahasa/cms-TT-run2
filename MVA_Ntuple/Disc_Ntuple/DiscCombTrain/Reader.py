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
parser.add_option("--method", "--method", dest="methodMVA", default="BDTP",type='str', 
                     help="Which MVA method to be used")
parser.add_option("--isCheck", "--isCheck", dest="isCheck", action="store_true", default=False, help="")
(options, args) = parser.parse_args()
year = options.year
decayMode = options.decayMode
channel = options.channel
region = options.region
syst = options.systematic
level =options.level
method = options.methodMVA
isCheck = options.isCheck
print parser.parse_args()

#-----------------------------------------
#INPUT AnalysisNtuples Directory
#----------------------------------------
package = "TMVA"
dirNtuple = "root://cmseos.fnal.gov//store/user/rverma/Output/cms-TT-run2/Ntuple_Skim/"
dirFile = "%s/%s/%s"%(year, decayMode, syst) 
allSamples = getSamples(year, decayMode, syst)

sigDict = {}
bkgDict = {}
for s in allSamples.keys():
    if 'TT_tytg' in s:
        sigDict[s] = allSamples[s] 
    else:
        if "Data" not in s:
            bkgDict[s] = allSamples[s]
            print("%s, files: %s"%(s, len(bkgDict[s])))

#bkgList = ["Semilep_JetBase__TTGamma_SingleLept_2016_Ntuple.root"]

weightfile = "dataset/weights/%s_Classification_%s.weights.xml"%(package, method)
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
nBins, xMin, xMax = 25, -1, 1
if method in ["DNN", 'MLP']: xMin, xMax = 0, 1 
if method in ['PDEFoam']: nBins, xMin, xMax = 4, -2, 2 
hBkg_disc = ROOT.TH1D("Disc","Disc",nBins, xMin, xMax)
for samp in sigDict.keys():
    histSig = 'ROOT.TH1D("Disc", "Disc", %s, %s, %s)'%(nBins, xMin, xMax)
    exec("hSig_%s_disc = %s"%(samp, histSig))
for samp in bkgDict.keys():
    histBkg = 'ROOT.TH1D("Disc", "Disc", %s, %s, %s)'%(nBins, xMin, xMax)
    exec("hBkg_%s_disc = %s"%(samp, histSig))
for var in vars.keys():
    nBins  = vars[var][1][0]
    xMin   = vars[var][1][1]
    xMax   = vars[var][1][2]
    #cuts = ["", "_cut"]
    cuts = [""]
    for cut in cuts:
        for samp in sigDict.keys():
            histSig = 'ROOT.TH1D("%s%s", "%s%s", %s, %s, %s)'%(var, cut, var, cut, nBins, xMin, xMax)
            exec("hSig_%s_%s%s = %s"%(samp, var, cut, histSig))
        for samp in bkgDict.keys():
            histBkg = 'ROOT.TH1D("%s%s", "%s%s", %s, %s, %s)'%(var, cut, var, cut, nBins, xMin, xMax)
            exec("hBkg_%s_%s%s = %s"%(samp, var, cut, histBkg))

#Fill hists for signal
print("\nRunning for Sig...\n") 
for samp in sigDict.keys():
    sig = ROOT.TChain("AnalysisTree")
    for s in sigDict[samp]:
        sig.Add("%s/%s/%s"%(dirNtuple, dirFile, s))
    print("%s, Entries = %s "%(samp, sig.GetEntries()))
    for ievt, e in enumerate(sig):
        eventSel = int(e.Event_pass_presel_mu and ((e.Jet_size>=5 and e.FatJet_size==0) or (e.Jet_size>=2 and e.FatJet_size==1))  and e.Jet_b_size >=1 and e.Photon_size==1 and e.Photon_et[0] > 100)
        if isCheck and ievt >1000:
            break
        if eventSel>0:
            for var in vars.keys():
                exec("%s[0] = e.%s"%(var, vars[var][0]))
                exec("hSig_%s_%s.Fill(e.%s, e.Weight_lumi)"%(samp, var, vars[var][0]))
            disc = reader.EvaluateMVA(method)
            exec("hSig_%s_disc.Fill(%s, e.Weight_lumi)"%(samp, disc))
            if disc>0:
                for var in vars.keys():
                    #exec("hSig_%s_%s_cut.Fill(e.%s, e.Weight_lumi)"%(samp, var, vars[var][0]))
                    pass
            if (ievt%100)==0:
                print('Event = %i/%i, Disc = %s'%(ievt, sig.GetEntries(), disc))
                if isCheck:
                    break
            
#Fill hists for background
print("\nRunning for Bkg...\n")    
for samp in bkgDict.keys():
    bkg = ROOT.TChain("AnalysisTree")
    for b in bkgDict[samp]:
        bkg.Add("%s/%s/%s"%(dirNtuple, dirFile, b))
    bkg.Add("%s/%s/%s"%(dirNtuple, dirFile, b))
    print("%s, Entries = %s "%(samp, bkg.GetEntries()))
    for ievt, e in enumerate(bkg):
        eventSel = int(e.Event_pass_presel_mu and ((e.Jet_size>=5 and e.FatJet_size==0) or (e.Jet_size>=2 and e.FatJet_size==1))  and e.Jet_b_size >=1 and e.Photon_size==1 and e.Photon_et[0] > 100)
        if isCheck and ievt >1000:
            break
        if eventSel>0:
            for var in vars.keys():
                exec("%s[0] = e.%s"%(var, vars[var][0]))
                exec("hBkg_%s_%s.Fill(e.%s, e.Weight_lumi)"%(samp, var, vars[var][0]))
            disc = reader.EvaluateMVA(method)
            exec("hBkg_%s_disc.Fill(%s, e.Weight_lumi)"%(samp, disc))
            if disc>0:
                for var in vars.keys():
                    #exec("hBkg_%s_%s_cut.Fill(e.%s, e.Weight_lumi)"%(samp, var, vars[var][0]))
                    pass
            if (ievt%1000)==0:
                progress = "%s%s"%(100*ievt/bkg.GetEntries(), "%")
                print('Event(%s) = %i/%i, Disc = %s'%(progress, ievt, bkg.GetEntries(), disc)) 

outputFile = ROOT.TFile("%s_Reader.root"%(package),"RECREATE")
CR = "ttyg_Enriched_SR"
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
for samp in sigDict.keys():
    exec("writeList.append([hSig_%s_disc, \"Sig_%s\", \"Base\"])"%(samp, samp))
    for var in vars.keys():
        exec("writeList.append([hSig_%s_%s, \"Sig_%s\", \"Base\"])"%(samp, var, samp))
for samp in bkgDict.keys():
    exec("writeList.append([hBkg_%s_disc, \"Bkg_%s\", \"Base\"])"%(samp, samp))
    for var in vars.keys():
        exec("writeList.append([hBkg_%s_%s, \"Bkg_%s\", \"Base\"])"%(samp, var, samp))

for write in writeList:
    writeHist(write[0], write[1], outputFile)
    if "TTGamma" in write[1]:
        writeHist(write[0], "data_obs", outputFile)
#outputFile.ls()
outputFile.Close()
