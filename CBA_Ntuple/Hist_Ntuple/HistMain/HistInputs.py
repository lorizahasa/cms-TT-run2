#-----------------------------------------------------------------
condorHistDir = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/CBA_Ntuple/Hist_Ntuple/HistMain/Raw"
#-----------------------------------------------------------------
Years 	      =	["2016", "2017", "2018"]
#Years 	      =	["2017"]
Channels 	  =	["Mu", "Ele"]
#Channels 	  =	["Mu"]
Decays 	      =	["Semilep"]

Samples = []
Samples.append("Signal_M700")
Samples.append("Signal_M800")
Samples.append("Signal_M900")
Samples.append("Signal_M1000")
##Samples.append("Signal_M1100")
Samples.append("Signal_M1200")
Samples.append("Signal_M1300")
Samples.append("Signal_M1400")
Samples.append("Signal_M1500")
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
Samples.append("Data")

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
rForDYSF = {}
isTT = False
isTTY = True 
isTTYG = True 

#--------------------------------
#Validation region (0 photon) 
#(TOP-18-010, AN2019_227_v20)
#tt control regions
#--------------------------------
if isTT:
    Regions['tt_Enriched_e2j_e0b_e0y']          = "Jet_size==2 && Jet_b_size==0 && Photon_size==0" 
    Regions['tt_Enriched_e3j_e0b_e0y']          = "Jet_size==3 && Jet_b_size==0 && Photon_size==0" 
    Regions['tt_Enriched_a3j_e0b_e0y']          = "Jet_size>=3 && Jet_b_size==0 && Photon_size==0" 
    Regions['tt_Enriched_a4j_e0b_e0y']          = "Jet_size>=4 && Jet_b_size==0 && Photon_size==0" 

    Regions['tt_Enriched_e2j_e1b_e0y']          = "Jet_size==2 && Jet_b_size==1 && Photon_size==0" 
    Regions['tt_Enriched_e3j_e1b_e0y']          = "Jet_size==3 && Jet_b_size==1 && Photon_size==0" 
    Regions['tt_Enriched_a3j_e1b_e0y']          = "Jet_size>=3 && Jet_b_size==1 && Photon_size==0" 
    Regions['tt_Enriched_a4j_e1b_e0y']          = "Jet_size>=4 && Jet_b_size==1 && Photon_size==0" 

#--------------------------------
#tt+gamma control regions
#--------------------------------
if isTTY:
    Regions['tty_Enriched_e2j_e0b_e1y']             = "Jet_size ==2 && Jet_b_size ==0 && Photon_size==1 && FatJet_size==0"
    Regions['tty_Enriched_e3j_e0b_e1y']             = "Jet_size ==3 && Jet_b_size ==0 && Photon_size==1 && FatJet_size==0"
    Regions['tty_Enriched_a3j_e0b_e1y']             = "Jet_size >=3 && Jet_b_size ==0 && Photon_size==1 && FatJet_size==0"
    Regions['tty_Enriched_a4j_e0b_e1y']             = "Jet_size >=4 && Jet_b_size ==0 && Photon_size==1 && FatJet_size==0"

    Regions['tty_Enriched_e2j_e2b_e1y']             = "Jet_size ==2 && Jet_b_size ==2 && Photon_size==1 && FatJet_size==0"
    Regions['tty_Enriched_e4j_a1b_e1y']             = "Jet_size ==4 && Jet_b_size >=1 && Photon_size==1 && FatJet_size==0"
    Regions['tty_Enriched_e4j_a2b_e1y']             = "Jet_size ==4 && Jet_b_size >=2 && Photon_size==1 && FatJet_size==0"
    Regions['tty_Enriched_le4j_a1b_e1y']            = "Jet_size <=4 && Jet_b_size >=1 && Photon_size==1 && FatJet_size==0"

#--------------------------------
#tt+gamma+gluon control regions
#--------------------------------
if isTTYG:
    Regions['ttyg_Enriched_CR']         = "((Jet_size>=5 && FatJet_size==0) || (Jet_size>=2 && FatJet_size==1)) && Jet_b_size >=1 && Photon_size==1 && Photon_et < 75"
    Regions['ttyg_Enriched_CR_Resolved']= "Jet_size >=5 && Jet_b_size >=1 && Photon_size==1 && Photon_et < 75 && FatJet_size ==0"
    Regions['ttyg_Enriched_CR_Boosted'] = "Jet_size >=2 && Jet_b_size >=1 && Photon_size==1 && Photon_et < 75 && FatJet_size >=1"

    #--------------------------------
    #signal regions
    #--------------------------------
    Regions['ttyg_Enriched_SR']         = "((Jet_size>=5 && FatJet_size==0) || (Jet_size>=2 && FatJet_size==1)) && Jet_b_size >=1 && Photon_size==1 && Photon_et > 100"
    Regions['ttyg_Enriched_SR_Resolved']= "Jet_size >=5 && Jet_b_size >=1 && Photon_size==1 && Photon_et > 100 && FatJet_size ==0"
    Regions['ttyg_Enriched_SR_Boosted'] = "Jet_size >=2 && Jet_b_size >=1 && Photon_size==1 && Photon_et > 100 && FatJet_size >=1"
