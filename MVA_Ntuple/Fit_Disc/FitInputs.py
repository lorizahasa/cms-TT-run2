import ROOT as rt
from collections import OrderedDict
#-----------------------------------------------------------------
condorOutDir  = "/store/user/rverma/Output/cms-TT-run2/MVA_Ntuple" 
dirFit = "/eos/uscms%s/Fit_Disc/FitMain"%condorOutDir
dirTwiki= "/eos/uscms/store/user/rverma/Output/cms-TT-run2/Twiki"
#-----------------------------------------------------------------
Year = []
Year.append("2016Pre")
#Year.append("2016Post")
#Year.append("2017")
#Year.append("2018")
#Year.append("2016Pre__2016Post__2017__2018")

Channel = []
Channel.append("Mu")
#Channel.append("Ele")
#Channel.append("Mu__Ele")

Decay 	  =	["Semilep"]

regionList = []
regionList.append("ttyg_Enriched_SR_Boosted")
regionList.append("ttyg_Enriched_SR_Resolved")
regionList.append("ttyg_Enriched_SR_Boosted__ttyg_Enriched_SR_Resolved")

histList = []
histList.append("Reco_mass_T")
histList.append("Reco_st")

xss = {}
xss["700.0"]   = 0.03*0.97*2*4.92
xss["800.0"]   = 0.03*0.97*2*1.68
xss["900.0"]   = 0.03*0.97*2*0.636
xss["1000.0"]  = 0.03*0.97*2*0.262
##xss["1100.0"]  = 0.03*0.97*2*0.116
xss["1200.0"]  = 0.03*0.97*2*0.0537
xss["1300.0"]  = 0.03*0.97*2*0.0261
xss["1400.0"]  = 0.03*0.97*2*0.0131
xss["1500.0"]  = 0.03*0.97*2*0.00677
xss["1600.0"]  = 0.03*0.97*2*0.00359

xss = OrderedDict(sorted(xss.items(), key=lambda t: t[1]))

regionDict = {}
#regionDict["ttyg_Enriched_SR"] = "Inclusive"
regionDict["ttyg_Enriched_SR_Boosted"] = "Boosted"
regionDict["ttyg_Enriched_SR_Resolved"]= "Resolved"
#regionDict["ttyg_Enriched_SR_Boosted__ttyg_Enriched_SR_Resolved"]="Boosted+Resolved"
