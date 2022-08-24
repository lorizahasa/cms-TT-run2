#-----------------------------------------------------------------
dirCBA  = "/store/user/rverma/Output/cms-TT-run2/CBA_Ntuple"
dirHist = "%s/Hist_Ntuple/HistMisIDSF"%dirCBA
dirFit  = "./output/Fit_Hist/FitMisIDSF"
dirFit_ = "/eos/uscms%s/Fit_Hist/FitMisIDSF"%dirCBA
dirTwiki= "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Twiki"
#-----------------------------------------------------------------
Year = []
Year.append("2016Pre")
Year.append("2016Post")
Year.append("2017")
Year.append("2018")
Year.append("2016Pre__2016Post__2017__2018")

Channel = []
Channel.append("Mu")
Channel.append("Ele")
Channel.append("Mu__Ele")

Decay 	      =	["Semilep"]
