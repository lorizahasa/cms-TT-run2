#-----------------------------------------------------------------
condorHistDir = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Hist_Ntuple"
#-----------------------------------------------------------------
Years 	      =	["2016", "2017", "2018"]
#Years 	      =	["2018"]
Channels 	  =	["Mu", "Ele"]
#Channels 	  =	["Mu"]
Decays 	      =	["Semilep"]

Samples = []
Samples.append("TT_tytg_M700")
Samples.append("TT_tytg_M800")
Samples.append("TT_tytg_M900")
Samples.append("TT_tytg_M1000")
#Samples.append("TT_tytg_M1100")
Samples.append("TT_tytg_M1200")
Samples.append("TT_tytg_M1300")
Samples.append("TT_tytg_M1400")
Samples.append("TT_tytg_M1500")
Samples.append("TT_tytg_M1600")
#bkg and data
Samples.append("TTGamma")
Samples.append("TTbar")
Samples.append("SingleTop")
Samples.append("Others")
Samples.append("QCDEle")
Samples.append("QCDMu")
Samples.append("DataMu")
Samples.append("DataEle")

Systematics   =	[]
Systematics.append("Weight_pu")
Systematics.append("Weight_mu")
Systematics.append("Weight_pho")
Systematics.append("Weight_ele")
Systematics.append("Weight_btag_b")
Systematics.append("Weight_btag_l")
Systematics.append("Weight_prefire")
Systematics.append("Weight_q2")
Systematics.append("Weight_pdf")
Systematics.append("Weight_isr")
Systematics.append("Weight_fsr")
Systematics   =	[]

SystLevels = []
SystLevels.append("Up")
SystLevels.append("Down")

phoCat = {}
phoCat["genuine"]          = "Photon_genuine"         
phoCat["misid_ele"]        = "Photon_misid_ele"      
phoCat["hadronic_photon"]  = "Photon_hadronic_photon"
phoCat["hadronic_fake"]    = "Photon_hadronic_fake"  

Regions = {}
Regions['tty_Enriched_e2j_e2b']             = "Jet_size ==2 && Jet_b_size ==2 && Photon_size==1 && FatJet_size==0"
Regions['tty_Enriched_e4j_e0b']             = "Jet_size ==4 && Jet_b_size ==0 && Photon_size==1 && FatJet_size==0"
Regions['tty_Enriched_e4j_a1b']             = "Jet_size ==4 && Jet_b_size >=1 && Photon_size==1 && FatJet_size==0"
Regions['tty_Enriched_e4j_a2b']             = "Jet_size ==4 && Jet_b_size >=2 && Photon_size==1 && FatJet_size==0"

#Regions['tt_Enriched']              = "Jet_size >=4 && Jet_b_size >=1 && Photon_size==0"
#Regions['tty_Enriched']             = "Jet_size ==4 && Jet_b_size >=0 && Photon_size==1 && FatJet_size==0"
#Regions['ttyg_Enriched']            = "Jet_size >=5 && Jet_b_size >=1 && Photon_size==1"

#Regions['ttyg_Enriched_SR']         = "((Jet_size>=5 && FatJet_size==0) || (Jet_size>=2 && FatJet_size==1)) && Jet_b_size >=1 && Photon_size==1 && Photon_et > 100"
#Regions['ttyg_Enriched_SR_Resolved']= "Jet_size >=5 && Jet_b_size >=1 && Photon_size==1 && Photon_et > 100 && FatJet_size ==0"
#Regions['ttyg_Enriched_SR_Boosted'] = "Jet_size >=2 && Jet_b_size >=1 && Photon_size==1 && Photon_et > 100 && FatJet_size >=1"

#Regions['ttyg_Enriched_CR']         = "((Jet_size>=5 && FatJet_size==0) || (Jet_size>=2 && FatJet_size==1)) && Jet_b_size >=1 && Photon_size==1 && Photon_et < 75"
#Regions['ttyg_Enriched_CR_Resolved']= "Jet_size >=5 && Jet_b_size >=1 && Photon_size==1 && Photon_et < 75 && FatJet_size ==0"
#Regions['ttyg_Enriched_CR_Boosted'] = "Jet_size >=2 && Jet_b_size >=1 && Photon_size==1 && Photon_et < 75 && FatJet_size >=1"
