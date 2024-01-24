import os
import sys
import subprocess
import itertools
sys.dont_write_bytecode = True
#-----------------------------------------------------------------
condorNtupleDir = "root://cmseos.fnal.gov//store/user/lpctop/Output/cms-TT-run2/Ntuple_Skim"
#condorNtupleDir = "root://cmseos.fnal.gov//store/user/rverma/Output/cms-TT-run2/Ntuple_Skim"
#-----------------------------------------------------------------
outHistDir = "/store/user/lhasa/Output/cms-TT-run2/CBA_Ntuple/Hist_Ntuple/HistWeight"
#-----------------------------------------------------------------
Years 	      =	["2016Pre", "2016Post", "2017", "2018"]
#Years 	      =	["2016Pre"]
#Channels 	  =	["Mu", "Ele"]
Channels 	  =	["Mu"]
Decays 	      =	["Semilep"]

#Years and channels to be commbined
Years_         = ["2016Pre__2016Post__2017__2018"]
#Channels_      = ["Mu__Ele"]
Channels_      = ["Mu", "Ele"]
#Channels_      = ["Mu", "Ele", "Mu__Ele"]

Samples = []
#Samples.append("SignalSpin12_M700")
#Samples.append("SignalSpin12_M1700")

Samples.append("SignalSpin32_M700")
#Samples.append("SignalSpin32_M1700")

#bkg and data
Samples.append("TTbar")
Samples.append("TTGamma")
Samples.append("TTGamma_TuneUp")
Samples.append("TTGamma_TuneDown")
Samples.append("WJets")
Samples.append("DYJets")
Samples.append("WGamma")
Samples.append("ZGamma")
Samples.append("Others")
Samples.append("QCD")
Samples.append("data_obs")

CorrAndSyst   =	[]
CorrAndSyst.append("Weight_pu")                
CorrAndSyst.append("Weight_ttag")                
CorrAndSyst.append("Weight_prefire")           
CorrAndSyst.append("Weight_mu")             
CorrAndSyst.append("Weight_mu_id")             
CorrAndSyst.append("Weight_mu_iso")            
CorrAndSyst.append("Weight_mu_trig")           
CorrAndSyst.append("Weight_ele")            
CorrAndSyst.append("Weight_ele_id")            
CorrAndSyst.append("Weight_ele_reco")          
CorrAndSyst.append("Weight_ele_trig")          
CorrAndSyst.append("Weight_pho")            
CorrAndSyst.append("Weight_pho_id")            
CorrAndSyst.append("Weight_pho_ps")        
CorrAndSyst.append("Weight_pho_cs")        

CorrOnlySyst = []
CorrOnlySyst.append("Weight_q2")                
CorrOnlySyst.append("Weight_tpt")                
CorrOnlySyst.append("Weight_pdf")               
CorrOnlySyst.append("Weight_isr")                
CorrOnlySyst.append("Weight_fsr")                

SepSyst = []
SepSyst.append("Weight_btag_b")              
SepSyst.append("Weight_btag_l")              

JMEs    = ["JEC_Total", "JEC_SubTotalPileUp", "JEC_SubTotalRelative", "JEC_SubTotalAbsolute", "JEC_FlavorQCD", "JEC_TimePtEta", "JER"]

Corrs = {}
uc = "Uncorr"
Corrs[uc] = [uc]
#Both
for c in CorrAndSyst:
    Corrs[c] = [uc, c, "%sUp"%c, "%sDown"%c]

#OnlySyst
for c in CorrOnlySyst:
    Corrs[c] = [uc, uc, "%sUp"%c, "%sDown"%c]
Corrs["Weight_q2_UN_DN"] = [uc, uc, "Weight_q2_UN", "Weight_q2_DN"]
Corrs["Weight_q2_NU_ND"] = [uc, uc, "Weight_q2_NU", "Weight_q2_ND"]
Corrs["Weight_q2_UU_DD"] = [uc, uc, "Weight_q2_UU", "Weight_q2_DD"]

#BTag
for c in SepSyst:
    Corrs[c] = [uc, "Weight_btag", "%sUp"%c, "%sDown"%c]

#JME
for c in JMEs: 
    Corrs[c] = [uc, uc, "%s_up"%c, "%s_down"%c]

#Lumi has no up or down
Corrs["Weight_lumi"] = [uc, "Weight_lumi", uc, uc]


Regions = {}
#Regions['tt_Enriched_a3j_a1b_e0y']   = "Jet_size>=3 && Jet_b_size>=1 && Photon_size==0"
Regions['tty_Enriched_le4j_a1b_e1y'] = "Jet_size<=4 && Jet_b_size>=1 && Photon_size==1" 
