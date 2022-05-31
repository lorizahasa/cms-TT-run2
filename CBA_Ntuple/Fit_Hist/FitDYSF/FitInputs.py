#-----------------------------------------------------------------
dirCBA  = "/store/user/rverma/Output/cms-TT-run2/CBA_Ntuple"
dirHist = "%s/Hist_Ntuple/HistDYSF"%dirCBA
dirFit  = "./output/Fit_Hist/FitDYSF"
dirFit_ = "/eos/uscms%s/Fit_Hist/FitDYSF"%dirCBA
dirTwiki= "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Twiki"
#-----------------------------------------------------------------
Year = []
Year.append("2016PreVFP")
Year.append("2016PostVFP")
Year.append("2017")
Year.append("2018")
Year.append("2016PreVFP__2016PostVFP__2017__2018")

Channel = []
Channel.append("Mu")
Channel.append("Ele")
Channel.append("Mu__Ele")

Decay 	      =	["Dilep"]
