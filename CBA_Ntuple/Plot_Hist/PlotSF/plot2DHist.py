#from ROOT import T2HF

import pandas as pd

years = ["16", "17", "18"]
dict2D = {} 
dictText = {} 

#Muon
muIso = []
muIsoName = "NUM_TightMiniIso_DEN_TightIDandIPCut/pt_abseta_ratio"
muIso.append(["Mu_RunBCDEFGH_SF_MiniIso_2016.root", muIsoName])
muIso.append(["Mu_RunBCDEF_SF_MiniIso_2017.root", muIsoName])
muIso.append(["Mu_RunABCD_SF_MiniIso_2018.root", muIsoName])

muID1 = []
muID1.append(["Mu_RunBCDEF_SF_ID_2016.root", "NUM_TightID_DEN_genTracks_eta_pt"])
muID1.append(["Mu_RunBCDEF_SF_ID_2017.root","NUM_TightID_DEN_genTracks_pt_abseta"])
muID1.append(["Mu_RunABCD_SF_ID_2018.root", "NUM_TightID_DEN_TrackerMuons_pt_abseta"])

muID2 = []
muID2.append(["Mu_RunGH_SF_ID_2016", "NUM_TightID_DEN_genTracks_eta_pt"])
muID2.append(["NA","NA"])
muID2.append(["NA","NA"])
dict2D["MuIso"] = muIso
dict2D["MuID1"] = muID1
dict2D["MuID2"] = muID2

#Electron
muTrig  = []
eleTrig = []
eleIso  = []
eleReco = []
for y in years:
    muTrig.append(["muon_%s.root"%y, "h2D_SF"])
    eleTrig.append(["electron_%s"%y, "h2D_SF"])
    eleIso.append(["EGM2D_MiniIso_SF_20%s.root"%y, "EGamma_SF2D"])
    eleReco.append(["EGM2D_RECO_SF_20%s"%y, "EGamma_SF2D"])
dict2D["MuTrig"] = muTrig
dict2D["EleTrig"] = eleTrig
dict2D["EleIso"] = eleIso
dict2D["EleReco"] = eleReco

#Photon
phoID = []
phoID.append(["Fall17V2_2016_MVAwp90_photons.root", "EGamma_SF2D"])
phoID.append(["2017_PhotonsMVAwp90.root", "EGamma_SF2D"])
phoID.append(["2018_PhotonsMVAwp90.root", "EGamma_SF2D"])

phoScale = []
phoScale.append(["ScalingFactors_80X_Summer16.root", "Scaling_Factors_HasPix_R9 Inclusive"])
phoScale.append(["PixelSeed_ScaleFactors_2017.root", "MVA_ID"])
phoScale.append(["HasPix_2018.root", "eleVeto_SF"])
dict2D["PhoID"] = phoID
dict2D["PhoScale"] = phoScale

#L1 Prefire
L1jet = []
L1jet.append(["L1prefiring_jetpt_2016BtoH.root", "L1prefiring_jetpt_2016BtoH"])
L1jet.append(["L1prefiring_jetpt_2017BtoF.root", "L1prefiring_jetpt_2016BtoH"])
L1jet.append(["NA", "NA"])
L1pho = []
L1pho.append(["L1prefiring_photonpt_2016BtoH.root", "L1prefiring_photonpt_2016BtoH"])
L1pho.append(["L1prefiring_photonpt_2017BtoF.root", "L1prefiring_photonpt_2016BtoH"])
L1pho.append(["NA", "NA"])
dict2D["L1Jet"] = L1jet
dict2D["L1Pho"] = L1pho


#The folllowing are mentioned in the table
#Pileup
pileUp = []
pileUp.append(["NanoAOD", "--"])
pileUp.append(["NanoAOD", "--"])
pileUp.append(["NanoAOD", "--"])
dictText["Pileup"] = pileUp

#bTag
bTag = []
bTag.append(["DeepCSV_2016LegacySF_V1.csv", "--"])
bTag.append(["DeepCSV_94XSF_V3_B_F.csv", "--"])
bTag.append(["DeepCSV_102XSF_V1.csv", "--"])
dictText["bTag"] = bTag

#JER
jer1AK4 = []
jer1AK4.append(["Summer16_25nsV1_MC_PtResolution_AK4PFchs.txt", "--"])
jer1AK4.append(["Fall17_V3_MC_PtResolution_AK4PFchs.txt", "--"])
jer1AK4.append(["Autumn18_V7b_MC_PtResolution_AK4PFchs.txt", "--"])

jer2AK4 = []
jer2AK4.append(["Summer16_25nsV1_MC_SF_AK4PFchs.txt", "--"])
jer2AK4.append(["Fall17_V3_MC_SF_AK4PFchs.txt", "--"])
jer2AK4.append(["Autumn18_V7b_MC_SF_AK4PFchs.txt", "--"])
dictText["JetReso"] = jer1AK4
dictText["jetMCSF"] = jer2AK4

jer1AK8 = []
jer1AK8.append(["Summer16_25nsV1_MC_PtResolution_AK8PFchs.txt", "--"])
jer1AK8.append(["Fall17_V3_MC_PtResolution_AK8PFchs.txt", "--"])
jer1AK8.append(["Autumn18_V7b_MC_PtResolution_AK8PFchs.txt", "--"])

jer2AK8 = []
jer2AK8.append(["Summer16_25nsV1_MC_SF_AK8PFchs.txt", "--"])
jer2AK8.append(["Fall17_V3_MC_SF_AK8PFchs.txt", "--"])
jer2AK8.append(["Autumn18_V7b_MC_SF_AK8PFchs.txt", "--"])
#dictText["jer1AK8"] = jer1AK8
#dictText["jer2AK8"] = jer2AK8

#JES
jes = []
jes.append(["Summer16_07Aug2017_V11_MC_Uncertainty_AK4PFchs.txt", "--"])
jes.append(["Fall17_17Nov2017_V32_MC_Uncertainty_AK4PFchs.txt", "--"])
jes.append(["Autumn18_V19_MC_Uncertainty_AK4PFchs.txt", "--"])
dictText["JES"] = jes

#isr, fsr, q2, pdf
isr = []
isr.append(["NanoAOD", "--"])
isr.append(["NanoAOD", "--"])
isr.append(["NanoAOD", "--"])

fsr = []
fsr.append(["NanoAOD", "--"])
fsr.append(["NanoAOD", "--"])
fsr.append(["NanoAOD", "--"])

q2 = []
q2.append(["NanoAOD", "--"])
q2.append(["NanoAOD", "--"])
q2.append(["NanoAOD", "--"])

pdf = []
pdf.append(["NanoAOD", "--"])
pdf.append(["NanoAOD", "--"])
pdf.append(["NanoAOD", "--"])
dictText["ISR"] = isr
dictText["FSR"] = fsr
dictText["Q2"] = q2
dictText["PDF"] = pdf

for k in dict2D.keys():
    print(k, len(dict2D[k]))
dict2D.update(dictText)
dfs = pd.DataFrame.from_dict(dict2D)
sfPath = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/CBA_Ntuple/Plot_Hist/PlotSF/allSF.tex"
f = open(sfPath, "w")
with pd.option_context("max_colwidth", 1000):
    f.write("\\cmsTable{\n")
    f.write("\\begin{tabular}{p{0.10\\textwidth}p{0.30\\textwidth}p{0.30\\textwidth}p{0.30\\textwidth}}\n")
    f.write("\\hline\n")
    f.write("SFs & 2016 & 2017 & 2018 \\\\\n")
    f.write("\\hline\n")
    f.write(dfs.T.to_latex())
    f.write("\n}")
    print(dfs.T.to_latex())
f.close()
print(sfPath)

