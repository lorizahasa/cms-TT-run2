import ROOT as rt
#-----------------------------------------------------------------
dirCBA  = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/CBA_Ntuple"
dirHist = "%s/Hist_Ntuple/HistWeight/Rebin"%dirCBA
dirPlot = "%s/Plot_Hist/PlotWeight/Rebin"%dirCBA
dirTwiki= "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Twiki"
#-----------------------------------------------------------------
Years 	      =	["2016Pre", "2016Post", "2017", "2018"]
#Years 	      =	["2018"]
Channels 	  =	["Mu", "Ele"]
#Channels 	  =	["Mu"]
Decays 	      =	["Semilep"]

#Years and channels to be commbined
Years_         = ["2016Pre__2016Post__2017__2018"]
#Channels_      = ["Mu", "Ele", "Mu__Ele"]
#Channels_      = ["Mu__Ele"]
Channels_      = ["Mu", "Ele"]

systDict = {}
systDict["Weight_mu"]   = ["Weight_mu_id", "Weight_mu_iso", "Weight_mu_trig"]
systDict["Weight_ele"]  = ["Weight_ele_id", "Weight_ele_reco", "Weight_ele_trig"]
systDict["Weight_btag"] = ["Weight_btag_b", "Weight_btag_l"]
systDict["Weight_ttag"] = ["Weight_ttag"]
systDict["Weight_pho"]  = ["Weight_pho_id", "Weight_pho_ps", "Weight_pho_cs"]
systDict["Weight_jet"]  = ["Weight_jes", "Weight_jer"]
systDict["Weight_pu"]   = ["Weight_pu"]
systDict["Weight_prefire"]  = ["Weight_prefire"]
systDict["Weight_q2_pdf"]   = ["Weight_q2", "Weight_pdf"]
systDict["Weight_isr_fsr"]  = ["Weight_isr", "Weight_fsr"]

SystLevels = []
SystLevels.append("up")
SystLevels.append("base")
SystLevels.append("down")

hName  = "Reco_st"
region = "tty_Enriched_le4j_a1b_e1y"

sampSig = {
         "SignalSpin32_M700"    : [rt.kGreen,  "m_{t*} = 700"],
         #"SignalSpin32_M1500"   : [rt.kGreen+2,     "m_{t*} = 1500"],
         #"SignalSpin32_M3000"   : [rt.kCyan,     "m_{t*} = 3000"],
         }
sampBkg = {
         "TTGamma"   : [rt.kRed+2, "t#bar{t}#gamma"],
         "TTbar"     : [rt.kRed, "t/t#bar{t}"],
         "WJets"     : [rt.kOrange, "W+jets"],
         "DYJets"    : [rt.kYellow, "DY+jets"],
         "WGamma"    : [rt.kGray, "W+#gamma"],
         "ZGamma"    : [rt.kMagenta, "Z+#gamma"],
         "QCD"       : [rt.kCyan, "QCD"],
         "Others"    : [rt.kBlue, "Others"]
         }
sampData = {
         "data_obs"   : [rt.kBlack, "Data"]
         }

sampAll = {**sampSig, **sampBkg, **sampData}


#---------------
# Plotting 
#---------------
overlayEff = []
#overlayEff.append("data_obs")
overlayEff.append("TTbar")
overlayEff.append("TTGamma")
overlayEff.append("SignalSpin32_M700")
overlayEff.append("SignalSpin32_M1500")
#overlayEff.append("SignalSpin32_M3000")

colData     = rt.kBlack
colUncorr  = rt.kCyan +1
colUp   = rt.kRed+1
colCorr = rt.kGreen+1
colDown = rt.kBlue +1
