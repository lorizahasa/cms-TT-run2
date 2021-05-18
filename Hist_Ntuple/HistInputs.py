#-----------------------------------------------------------------
condorHistDir = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Hist_Ntuple"
#-----------------------------------------------------------------
#Years 	      =	["2016", "2017", "2018"]
Years 	      =	["2016"]
#Channels 	  =	["Mu", "Ele"]
Channels 	  =	["Mu"]
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

SystLevels = []
SystLevels.append("Up")
SystLevels.append("Down")

Regions = {}
Regions['tt_Enriched']              = "Jet_size >=4 && Jet_b_size >=2 && Photon_size==0"
Regions['tty_Enriched']             = "Jet_size ==4 && Jet_b_size >=2 && Photon_size==1"
Regions['ttyg_Enriched']            = "Jet_size >=5 && Jet_b_size >=1 && Photon_size==1"

Regions['ttyg_Enriched_SR']         = "Jet_size >=5 && Jet_b_size >=1 && Photon_size==1 && Photon_et > 100"
Regions['ttyg_Enriched_SR_Resolved']= "Jet_size >=5 && Jet_b_size >=1 && Photon_size==1 && Photon_et > 100 && FatJet_size ==0"
Regions['ttyg_Enriched_SR_Boosted'] = "Jet_size >=2 && Jet_b_size >=1 && Photon_size==1 && Photon_et > 100 && FatJet_size >=1"

Regions['ttyg_Enriched_CR']         = "Jet_size >=5 && Jet_b_size >=1 && Photon_size==1 && Photon_et > 20 && Photon_et < 75"
Regions['ttyg_Enriched_CR_Resolved']= "Jet_size >=5 && Jet_b_size >=1 && Photon_size==1 && Photon_et > 20 && Photon_et < 75 && FatJet_size ==0"
Regions['ttyg_Enriched_CR_Boosted'] = "Jet_size >=2 && Jet_b_size >=1 && Photon_size==1 && Photon_et > 20 && Photon_et < 75 && FatJet_size >=1"
