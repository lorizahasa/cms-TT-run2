#-----------------------------------------------------------------
condorHistDir  = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Hist_Ntuple"
#-----------------------------------------------------------------
Year 	      =	["2016", "2017", "2018"]
#Year 	      =	["2016"]
Channel 	  =	["Mu", "Ele"]
#Channel 	  =	["Mu"]
Decay 	  =	["Semilep"]
#Samples = ['TTbar', 'TTGamma', 'TT_tgtg_M800', 'TT_tytg_M800', 'TT_tgtg_M1200', 'TT_tytg_M1200', 'TT_tyty_M800', 'TT_tyty_M1200', 'DataMu']
Samples = ['TT_tytg_M1300', 'TT_tytg_M1400', 'QCDMu', 'QCDEle', 'TT_tytg_M900', 'TT_tytg_M1200', 'DataMu', 'TT_tytg_M1600', 'TT_tytg_M1100', 'DataEle', 'TTGamma', 'TT_tytg_M1500', 'Others', 'TT_tytg_M700', 'TTbar', 'TT_tytg_M1000', 'SingleTop', 'TT_tytg_M800']
#Systematics   =	["PU","MuEff","BTagSF_b","BTagSF_l","EleEff","Q2","Pdf","isr","fsr"]
#Systematics   =	["PU","MuEff","BTagSF_b","BTagSF_l","PhoEff","EleEff","Q2","Pdf","isr","fsr"]
#Systematics   =	["EleEff"]
Systematics   =	[]
#Systematics   =	["isr","fsr"]
SystLevel     = ["Up", "Down"]
#ControlRegion = ['tight_a5j_e2b']
#PhaseSpace = ['Boosted_SR', 'Boosted_CR', 'Resolved_SR', 'Resolved_CR']
PhaseSpace = ['Boosted_SR']

