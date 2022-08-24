import ROOT as rt
#-----------------------------------------------------------------
dirCBA  = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/MVA_Ntuple"
dirDisc = "%s/Disc_Ntuple/DiscMain"%dirCBA
dirPlot = "%s/Plot_Disc/PlotMain"%dirCBA
dirTwiki= "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Twiki"
#-----------------------------------------------------------------
Years 	      =	["2016Pre", "2016Post", "2017", "2018"]
#Year 	      =	["2017"]
Channels 	  =	["Mu", "Ele"]
#Channel 	  =	["Ele"]
Decays 	      =	["Semilep"]

#Years and channels to be commbined
Years_         = ["2016Pre__2016Post__2017__2018"]
#Channels_      = ["Mu", "Ele", "Mu__Ele"]
Channels_      = ["Mu__Ele"]
#Channels_      = ["Mu__Ele"]

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
Systematics.append("Weight_ttag")

SystLevels = []
SystLevels.append("Up")
SystLevels.append("Down")

SampleSignal = {
         "Signal_M800"    : [rt.kMagenta,  "m_{T} = 800"],
         "Signal_M1200"   : [rt.kCyan,     "m_{T} = 1200"],
         "Signal_M1600"   : [rt.kPink,     "m_{T} = 1600"],
         }

SampleBkg = {
         "TTGamma"   : [rt.kGreen, "t#bar{t}#gamma"],
         "OtherBkgs"    : [rt.kRed, "OtherBkgs"]
         }
'''
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
'''
SampleData = {
         "Data"   : [rt.kBlack, "Data"]
         }
SampleWeight = ["TTGamma", "TTbar", "Signal_M800"]
SampleLumi = SampleBkg
#SampleLumi.update(SampleSignal)
SampleSyst = ["TTGamma", "TTbar", "WJets", "DYJets", "WGamma", "ZGamma", "QCD", "Others"] 
#SampleSyst = SampleBkg.keys()
Samples = SampleSignal.keys() + SampleBkg.keys() + SampleData.keys()
Samples = dict(SampleSignal.items() + SampleBkg.items() + SampleData.items())

