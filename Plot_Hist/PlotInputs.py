import ROOT as rt
#-----------------------------------------------------------------
condorHistDir  = "/eos/uscms/store/user/rverma/Output/cms-TT-run2"
#-----------------------------------------------------------------
Year 	      =	["2016", "2017", "2018"]
#Year 	      =	["2016"]
Channel 	  =	["Mu", "Ele"]
#Channel 	  =	["Mu"]
#Decay 	  =	["Semilep", "Dilep"]
Decay 	  =	["Semilep"]
Systematics   =	["PU","MuEff", "BTagSF_b","BTagSF_l","PhoEff","Q2","Pdf"]
SystLevel     = ["Up", "Down"]
PhaseSpace = ['Boosted_SR', 'Boosted_CR', 'Resolved_SR', 'Resolved_CR']

SampleSignal = {
         "TT_tytg_M800"    : [rt.kMagenta,   "10x m_{T} = 800"],
         "TT_tytg_M1200"   : [rt.kCyan,     "10x m_{T} = 1200"],
         "TT_tytg_M1600"   : [rt.kPink,     "10x m_{T} = 1600"],
         }

SampleBkg = {
         "TTGamma"   : [rt.kGreen, "t#bar{t}#gamma"],
         "TTbar"     : [rt.kRed, "t#bar{t}"],
         "SingleTop" : [rt.kOrange, "t"],
         "QCD"       : [rt.kBlack, "QCD"],
         "Others"    : [rt.kBlue, "Others"]
         }
SampleData = {
         "Data"   : [rt.kBlack, "Data"]
         }
SampleWeight = ["TTGamma", "TTbar", "TT_tytg_M800"]
SampleLumi = SampleBkg
SampleLumi.update(SampleSignal)
SampleSyst = SampleBkg.keys()
Samples = SampleSignal.keys() + SampleBkg.keys() + SampleData.keys()
plotList = ["Muon_pt"]
