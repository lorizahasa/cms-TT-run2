#-----------------------------------------------------------------
condorHistDir  = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/tytg/Hist_Ntuple"
#-----------------------------------------------------------------
#Year 	      =	["2016", "2017", "2018"]
Year 	      =	["2016"]
#Channel 	  =	["Mu", "Ele"]
Channel 	  =	["Mu"]
#Decay 	  =	["Semilep", "Dilep"]
Decay 	  =	["Semilep"]
#Samples = ['TTbar', 'TTGamma', 'TT_tgtg_M800', 'TT_tytg_M800', 'TT_tgtg_M1200', 'TT_tytg_M1200', 'TT_tyty_M800', 'TT_tyty_M1200', 'DataMu']
Samples = ['TTbar', 'TT_tytg_M700', 'TT_tytg_M800','TT_tytg_M900','TT_tytg_M1000','TT_tytg_M1100','TT_tytg_M1200','TT_tytg_M1300','TT_tytg_M1400','TT_tytg_M1500','TT_tytg_M1600','SingleTop', 'DataMu', 'TTGamma']
#Samples = ['Diboson', 'HplusM155', 'HplusM140', 'HplusM150', 'HplusM090', 'HplusM080', 'DataMu', 'DataEle', 'HplusM160', 'TTV', 'HplusM120', 'Wjets', 'QCDMu', 'QCDEle', 'HplusM100', 'TTbar', 'ZJets', 'SingleTop']
Systematics   =	["PU","MuEff","BTagSF_b","BTagSF_l","EleEff","Q2","Pdf","isr","fsr"]
#Systematics   =	[]
#Systematics   =	["isr","fsr"]
SystLevel     = ["Up", "Down"]
ControlRegion = []

