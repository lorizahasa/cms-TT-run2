#-----------------------------------------------------------------
dirNtuple = "/store/user/rverma/Output/cms-TT-run2/Ntuple_Skim"
dirHist   = "/store/user/rverma/Output/cms-TT-run2/CBA_Ntuple/Hist_Ntuple/HistDYSF"
#-----------------------------------------------------------------
Years 	      =	["2016Pre", "2016Post", "2017", "2018"]
#Years 	      =	["2017"]
Channels 	  =	["Mu", "Ele"]
#Channels 	  =	["Ele"]
Decays 	      =	["Dilep"]

#Years and channels to be commbined
Years_         = ["2016Pre__2016Post__2017__2018"]
Channels_      = ["Mu", "Ele", "Mu__Ele"]
#Channels_      = ["Mu__Ele"]

Samples = []
#bkg and data
Samples.append("SignalSpin12_M800")
Samples.append("SignalSpin12_M1200")
Samples.append("SignalSpin12_M1500")
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

Regions = {}
Regions['DY_Enriched_a2j_e0b_e0y']              = "Jet_size>=2 && Jet_b_size==0 && Photon_size==0" 
Regions['DY_Enriched_e3j_e0b_e0y']              = "Jet_size==3 && Jet_b_size==0 && Photon_size==0" 
Regions['DY_Enriched_a3j_e0b_e0y']              = "Jet_size>=3 && Jet_b_size==0 && Photon_size==0" 
Regions['DY_Enriched_a4j_e0b_e0y']              = "Jet_size>=4 && Jet_b_size==0 && Photon_size==0" 
