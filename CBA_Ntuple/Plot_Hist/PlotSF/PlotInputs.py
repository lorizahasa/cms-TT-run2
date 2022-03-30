import ROOT as rt
#-----------------------------------------------------------------
condorHistDir  = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/CBA_Ntuple"
#-----------------------------------------------------------------
#Year 	      =	["2016", "2017", "2018"]
Year 	      =	["2016"]
#Channel 	  =	["Mu", "Ele"]
Channel 	  =	["Mu"]
Decay 	      =	["Semilep"]

systDict = {}
systDict["Weight_mu"]   = ["Weight_mu_id", "Weight_mu_iso", "Weight_mu_trig"]
systDict["Weight_ele"]  = ["Weight_ele_id", "Weight_ele_reco", "Weight_ele_trig"]
systDict["Weight_btag"] = ["Weight_btag_b", "Weight_btag_l"]
systDict["Weight_pho"]  = ["Weight_pho_id", "Weight_pho_e_veto"]
systDict["Weight_jet"]  = ["Weight_jes", "Weight_jer"]
systDict["Weight_pu"]   = ["Weight_pu"]
systDict["Weight_prefire"]  = ["Weight_prefire"]
systDict["Weight_q2_pdf"]   = ["Weight_q2", "Weight_pdf"]
#systDict["Weight_isr_fsr"]  = ["Weight_isr", "Weight_fsr"]

SystLevels = []
SystLevels.append("up")
SystLevels.append("base")
SystLevels.append("down")

SampleSignal = {
         "TT_tytg_M800"    : [rt.kMagenta,  "m_{T} = 800"],
         "TT_tytg_M1200"   : [rt.kCyan,     "m_{T} = 1200"],
         "TT_tytg_M1600"   : [rt.kPink,     "m_{T} = 1600"],
         }

SampleBkg = {
         "TTGamma"   : [rt.kGreen, "t#bar{t}#gamma"],
         "TTbar"     : [rt.kRed, "t/t#bar{t}"],
         "WJets"     : [rt.kOrange, "W+jets"],
         "DYJets"    : [rt.kYellow, "DY+jets"],
         "WGamma"    : [rt.kGray, "W+#gamma"],
         "ZGamma"    : [rt.kMagenta, "Z+#gamma"],
         "QCD"       : [rt.kCyan, "QCD"],
         "Others"    : [rt.kBlue, "Others"]
         }
SampleData = {
         "Data"   : [rt.kBlack, "Data"]
         }
