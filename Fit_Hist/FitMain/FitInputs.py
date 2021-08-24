import ROOT as rt
#-----------------------------------------------------------------
condorHistDir  = "/eos/uscms/store/user/rverma/Output/cms-TT-run2"
#-----------------------------------------------------------------
Year 	      =	["2016", "2017", "2018"]
#Year 	      =	["2017", "2018"]
Channel 	  =	["Mu", "Ele"]
#Channel 	  =	["Ele"]
Decay 	  =	["Semilep"]
Mass      = ["700", "800", "900", "1000", "1200", "1300", "1400", "1500", "1600"]

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
SystLevels.append("up")
SystLevels.append("down")

Regions = []
Regions.append("ttyg_Enriched_SR_Boosted")
Regions.append("ttyg_Enriched_SR_Resolved")
