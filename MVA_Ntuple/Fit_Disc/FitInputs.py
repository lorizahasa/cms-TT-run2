import ROOT as rt
from collections import OrderedDict
#-----------------------------------------------------------------
condorOutDir  = "/store/user/lhasa/Output/cms-TT-run2/MVA_Ntuple" 
dirFit = "/eos/uscms%s/Fit_Disc/FitMain"%condorOutDir
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

Decay 	  =	["Semilep"]


histList = []
histList.append("Reco_mass_T")
histList.append("Reco_st")

xss = {}
xss["700.0"]   = 0.03*0.97*2*4.92
xss["800.0"]   = 0.03*0.97*2*1.68
xss["900.0"]   = 0.03*0.97*2*0.636
#xss["1000.0"]  = 0.03*0.97*2*0.262
xss["1100.0"]  = 0.03*0.97*2*0.116
xss["1200.0"]  = 0.03*0.97*2*0.0537
#xss["1300.0"]  = 0.03*0.97*2*0.0261
#xss["1400.0"]  = 0.03*0.97*2*0.0131
xss["1500.0"]  = 0.03*0.97*2*0.00677
#xss["1600.0"]  = 0.03*0.97*2*0.00359
xss["2750.0"]  = 0.03*0.97*2*0.0003746
xss = OrderedDict(sorted(xss.items(), key=lambda t: t[1]))

rDict = {}
#rDict["ttyg_Enriched_SR"] = "Inclusive"
rDict["ttyg_Enriched_SR_Boosted"] = "SR, Boosted"
rDict["ttyg_Enriched_SR_Resolved"]= "SR, Resolved"
rDict["ttyg_Enriched_SR_Boosted__ttyg_Enriched_SR_Resolved"]="SR, Boosted+Resolved"
rDict["ttyg_Enriched_CR_Boosted"] = "CR, Boosted"
rDict["ttyg_Enriched_CR_Resolved"]= "CR, Resolved"
rDict["ttyg_Enriched_CR_Boosted__ttyg_Enriched_CR_Resolved"]="CR, Boosted+Resolved"

dataType = {"SR": "Asimoy", "CR": "Real"}
toInject = {}
toInject["SR"] = " -t -1"
toInject["CR"] = " --expectSignal 0"


def getRegion(region):
    regShort = "SR"
    if "CR" in region:
        regShort = "CR"
    return regShort


def getLumiLabel(year):
    lumi = "35.9 fb^{-1}"
    if "16Pre" in year:
        lumi = "19.5 fb^{-1} (2016Pre)"
    if "16Post" in year:
        lumi = "16.8 fb^{-1} (2016Post)"
    if "17" in year:
        lumi = "41.5 fb^{-1} (2017)"
    if "18" in year:
        lumi = "59.8 fb^{-1} (2018)"
    if "__" in year:
        lumi = "138 fb^{-1} (Run2)"
    return lumi

def getChLabel(decay, channel):
    nDict   = {"Semilep": "1", "Dilep":2}
    chDict  = {"Mu": "#mu", "Ele": "e"}
    colDict = {"Mu": rt.kBlue, "Ele": rt.kRed}
    name = ""
    for ch in channel.split("__"):
        name += "%s#color[%i]{%s}"%(nDict[decay], colDict[ch], chDict[ch])
    return name
