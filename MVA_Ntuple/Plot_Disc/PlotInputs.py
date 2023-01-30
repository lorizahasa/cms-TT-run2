import ROOT as rt
#-----------------------------------------------------------------
dirCBA  = "/eos/uscms/store/user/rverma/Output/cms-TT-run2/MVA_Ntuple"
dirDisc = "%s/Disc_Ntuple/DiscMain"%dirCBA
dirPlot = "%s/Plot_Disc/PlotMain"%dirCBA
dirTwiki= "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Twiki"
#-----------------------------------------------------------------
#Years 	      =	["2016Pre", "2016Post", "2017", "2018"]
Years 	      =	["2016Pre"]
#Channels 	  =	["Mu", "Ele"]
Channels 	  =	["Mu"]
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
         "SignalSpin12_M800"    : [rt.kMagenta,  "m_{T} = 800"],
         "SignalSpin12_M1200"   : [rt.kCyan,     "m_{T} = 1200"],
         "SignalSpin12_M1500"   : [rt.kPink,     "m_{T} = 1500"],
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
         "data_obs"   : [rt.kBlack, "Data"]
         }
SampleWeight = ["TTGamma", "TTbar", "SignalSpin12_M800"]
SampleLumi = SampleBkg
#SampleLumi.update(SampleSignal)
SampleSyst = ["TTGamma", "OtherBkgs"] 
#SampleSyst = SampleBkg.keys()
Samples = {}
Samples.update(SampleSignal)
Samples.update(SampleBkg)
Samples.update(SampleData)

myCyan = rt.kCyan
myRed = rt.kRed
myBlue = rt.kBlue

