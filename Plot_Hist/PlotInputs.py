import ROOT as rt
#-----------------------------------------------------------------
condorHistDir  = "/eos/uscms/store/user/rverma/Output/cms-hcs-run2/CBA_RecoNtuple/Hist_Ntuple"
#-----------------------------------------------------------------
Year 	      =	["2016", "2017", "2018"]
#Year 	      =	["2016"]
Channel 	  =	["Mu", "Ele"]
#Channel 	  =	["Mu"]
#Decay 	  =	["Semilep", "Dilep"]
Decay 	  =	["Semilep"]
Systematics   =	["PU","MuEff","BTagSF_b","BTagSF_l","EleEff","Q2","Pdf","isr","fsr"]
#Systematics   =	["JER", "JECTotal"]
#Systematics   =	["PU","Q2"]
SystLevel     = ["Up", "Down"]
ControlRegion = []
#ControlRegion=["tight_a4j_a1b", "veryTight_a4j_a2b", "tight_a4j_e0b", "looseCR_a2j_e1b", "looseCR_a2j_a0b", "looseCR_a2j_e0b", "looseCR_e3j_a2b", "looseCR_e3j_e0b", "looseCR_e2j_e1b", "looseCR_e2j_e0j", "looseCR_e2j_e2b", "looseCR_e3j_e1b"]
isMC = True
isData = True
SamplesSyst = ['Diboson', 'TTV', 'Wjets', 'TTbar', 'ZJets', 'SingleTop', 'QCD']

Signal = {"HplusM100"   : [[""],
                          rt.kOrange,
                          "mH+ = 100 GeV",
                          isMC
                          ]
                          }
Samples = {"TTbar"     : [[""],
                          rt.kRed+1,
                          "t#bar{t}",
                          isMC
                          ],
           "Wjets"     : [[""],
                          rt.kCyan-3,
                          "W + jets",
                          isMC
                          ],
           "ZJets"     : [[""],
                          rt.kCyan-5,
                          "Z + jets",
                          isMC
                          ],
           "Diboson"   : [[""],
                          rt.kCyan-7,
                          "VV",
                          isMC
                          ],
           "SingleTop" : [[""],
                          rt.kOrange-3,
                          "Single t",
                          isMC
                          ],
           "TTV"       : [[""],
                          rt.kRed-7,
                          "ttV",
                          isMC
                          ],
           "QCD"    : [[""],
                          rt.kGreen,
                          "QCD MC",
                          isMC
                          ],
           "Data"   : [[""],
                          rt.kBlack,
                          "Data",
                          isData
                          ],
           }
