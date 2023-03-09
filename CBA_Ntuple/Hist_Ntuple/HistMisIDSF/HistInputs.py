#-----------------------------------------------------------------
dirNtuple = "/store/user/rverma/Output/cms-TT-run2/Ntuple_Skim"
dirHist   = "/store/user/rverma/Output/cms-TT-run2/CBA_Ntuple/Hist_Ntuple/HistMisIDSF"
#-----------------------------------------------------------------
Years 	      =	["2016Pre", "2016Post", "2017", "2018"]
#Years 	      =	["2017"]
Channels 	  =	["Mu", "Ele"]
#Channels 	  =	["Ele"]
Decays 	      =	["Semilep"]

#Years and channels to be commbined
Years_         = ["2016Pre__2016Post__2017__2018"]
Channels_      = ["Mu", "Ele", "Mu__Ele"]
#Channels_      = ["Mu__Ele"]

Samples = []
#bkg and data
Samples.append("SignalSpin32_M800")
Samples.append("SignalSpin32_M1200")
Samples.append("SignalSpin32_M1500")
Samples.append("TTbar")
Samples.append("TTGamma")
Samples.append("WJets")
Samples.append("DYJets")
Samples.append("WGamma")
Samples.append("ZGamma")
Samples.append("Others")
Samples.append("QCD")
Samples.append("data_obs")

Systematics   =	[]
Systematics.append("Weight_pu")
Systematics.append("Weight_mu")
Systematics.append("Weight_ele")
Systematics.append("Weight_pho")
Systematics.append("Weight_btag_b")
Systematics.append("Weight_btag_l")
Systematics.append("Weight_prefire")
Systematics.append("Weight_q2")
Systematics.append("Weight_pdf")
Systematics.append("Weight_isr")
Systematics.append("Weight_fsr")
Systematics.append("Weight_jes")
Systematics.append("Weight_jer")
#Systematics   =	[]

SystLevels = []
SystLevels.append("Up")
SystLevels.append("Down")
phoCat = {}
phoCat["genuine"]          = "Photon_genuine"         
phoCat["misid_ele"]        = "Photon_misid_ele"      
phoCat["hadronic_photon"]  = "Photon_hadronic_photon"
phoCat["hadronic_fake"]    = "Photon_hadronic_fake"  

Regions = {}
Regions['MisID_Enriched_a2j_e0b_e1y']              = "Jet_size>=2 && Jet_b_size==0 && Photon_size==1" 
Regions['MisID_Enriched_e3j_e0b_e1y']              = "Jet_size==3 && Jet_b_size==0 && Photon_size==1" 
Regions['MisID_Enriched_a3j_e0b_e1y']              = "Jet_size>=3 && Jet_b_size==0 && Photon_size==1" 
Regions['MisID_Enriched_a4j_e0b_e1y']              = "Jet_size>=4 && Jet_b_size==0 && Photon_size==1" 
