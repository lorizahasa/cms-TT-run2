#-----------------------------------------------------------------
outHistDir = "/store/user/rverma/Output/cms-TT-run2/CBA_Ntuple/Hist_Ntuple/HistWeight"
#-----------------------------------------------------------------
Years 	      =	["2016PreVFP", "2016PostVFP", "2017", "2018"]
#Years 	      =	["2017"]
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
##Samples.append("Data")

Systematics   =	[]
Systematics.append("1")              
Systematics.append("Weight_lumi")              
Systematics.append("Weight_pu")                
Systematics.append("Weight_ttag")                
Systematics.append("Weight_prefire")           
Systematics.append("Weight_btag_b")              
Systematics.append("Weight_btag_l")              
Systematics.append("Weight_mu_id")             
Systematics.append("Weight_mu_iso")            
Systematics.append("Weight_mu_trig")           
Systematics.append("Weight_ele_id")            
Systematics.append("Weight_ele_reco")          
Systematics.append("Weight_ele_trig")          
Systematics.append("Weight_pho_id")            
Systematics.append("Weight_pho_ps")        
Systematics.append("Weight_pho_cs")        
Systematics.append("Weight_jes")
Systematics.append("Weight_jer")
Systematics.append("Weight_q2")                
Systematics.append("Weight_pdf")               
Systematics.append("Weight_isr")                
Systematics.append("Weight_fsr")                

SystLevels = []
SystLevels.append("Base")
SystLevels.append("Down")
SystLevels.append("Up")

Regions = {}
#Regions['tt_Enriched_a3j_a1b_e0y']   = "Jet_size>=3 && Jet_b_size>=1 && Photon_size==0"
Regions['tty_Enriched_le4j_a1b_e1y'] = "Jet_size<=4 && Jet_b_size>=1 && Photon_size==1 && FatJet_size==0"
