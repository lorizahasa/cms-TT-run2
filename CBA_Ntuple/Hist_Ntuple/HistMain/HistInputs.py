#-----------------------------------------------------------------
dirNtuple = "/store/user/rverma/Output/cms-TT-run2/Ntuple_Skim"
dirHist   = "/store/user/rverma/Output/cms-TT-run2/CBA_Ntuple/Hist_Ntuple/HistMain"
#-----------------------------------------------------------------
Years 	      =	["2016PreVFP", "2016PostVFP", "2017", "2018"]
#Years 	      =	["2016PreVFP"]
Channels 	  =	["Mu", "Ele"]
#Channels 	  =	["Mu"]
Decays 	      =	["Semilep"]

#Years and channels to be commbined
Years_         = ["2016PreVFP__2016PostVFP__2017__2018"]
Channels_      = ["Mu", "Ele", "Mu__Ele"]
#Channels_      = ["Mu__Ele"]

Samples = []
#Samples.append("Signal_M700")
Samples.append("Signal_M800")
#Samples.append("Signal_M900")
#Samples.append("Signal_M1000")
##Samples.append("Signal_M1100")
Samples.append("Signal_M1200")
#Samples.append("Signal_M1300")
#Samples.append("Signal_M1400")
#Samples.append("Signal_M1500")
Samples.append("Signal_M1600")
#bkg and data
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
Systematics.append("Weight_pho")
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
#Systematics.append("Weight_ttag")                
#Systematics   =	[]

SystLevels = []
SystLevels.append("up")
SystLevels.append("down")

phoCat = {}
phoCat["genuine"]          = "Photon_genuine"         
phoCat["misid_ele"]        = "Photon_misid_ele"      
phoCat["hadronic_photon"]  = "Photon_hadronic_photon"
phoCat["hadronic_fake"]    = "Photon_hadronic_fake"  

Regions = {}
rForDYSF = {}
isTT  = True 
isTTY = True 

#--------------------------------
#Validation region (0 photon) 
#(TOP-18-010, AN2019_227_v20)
#tt control regions
#--------------------------------
if isTT:
    Regions['tt_Enriched_e2j_e0b_e0y']          = "Jet_size==2 && Jet_b_size==0 && Photon_size==0" 
    Regions['tt_Enriched_a3j_e0b_e0y']          = "Jet_size>=3 && Jet_b_size==0 && Photon_size==0" 
    Regions['tt_Enriched_e2j_e1b_e0y']          = "Jet_size==2 && Jet_b_size==1 && Photon_size==0" 
    Regions['tt_Enriched_a3j_e1b_e0y']          = "Jet_size>=3 && Jet_b_size==1 && Photon_size==0" 

#--------------------------------
#tt+gamma control regions
#--------------------------------
if isTTY:
    Regions['tty_Enriched_e2j_e0b_e1y']             = "Jet_size ==2 && Jet_b_size ==0 && Photon_size==1"
    Regions['tty_Enriched_a3j_e0b_e1y']             = "Jet_size >=3 && Jet_b_size ==0 && Photon_size==1"
    Regions['tty_Enriched_e2j_e2b_e1y']             = "Jet_size ==2 && Jet_b_size ==2 && Photon_size==1"
    Regions['tty_Enriched_le4j_a1b_e1y']            = "Jet_size <=4 && Jet_b_size >=1 && Photon_size==1"

