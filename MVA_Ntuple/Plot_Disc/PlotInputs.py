import ROOT as rt
#-----------------------------------------------------------------
dirCBA  = "/eos/uscms/store/user/lhasa/Output/cms-TT-run2/MVA_Ntuple/C"
dirDisc = "%s/Disc_Ntuple/DiscMain"%dirCBA
dirPlot = "%s/Plot_Disc/PlotMain"%dirCBA
dirTwiki= "/eos/uscms/store/user/lhasa/Output/cms-TT-run2/Twiki"
#-----------------------------------------------------------------
#Years 	      =	["2016Pre", "2016Post", "2017", "2018"]
Years 	      =	["2017"]
#Channels 	  =	["Mu", "Ele"]
Channels 	  =	["Mu"]
Decays 	      =	["Semilep"]

#Years and channels to be commbined
Years_         = ["2016Pre__2016Post__2017__2018"]
#Channels_      = ["Mu", "Ele", "Mu__Ele"]
Channels_      = ["Mu__Ele"]
#Channels_      = ["Mu__Ele"]

JME_dic = {}
JME_dic["2016Pre"] = ["JEC_Total", "JEC_Absolute","JEC_Absolute_2016","JEC_BBEC1", "JEC_BBEC1_2016","JEC_EC2","JEC_EC2_2016","JEC_HF","JEC_HF_2016","JEC_RelativeSample_2016","JEC_RelativeBal","JEC_FlavorQCD","JER"]
#JME_dic["2016Pre"] = ["JEC_Total", "JEC_Absolute","JEC_Absolute_2016Post","JEC_BBEC1", "JEC_BBEC1_2016Post","JEC_EC2","JEC_EC2_2016Post","JEC_HF","JEC_HF_2016Post","JEC_RelativeSample_2016Post","JEC_RelativeBal","JEC_FlavorQCD","JER_2016Post"]
JME_dic["2016Post"] = JME_dic["2016Pre"]
JME_dic["2017"] =  ["JEC_Total", "JEC_Absolute","JEC_Absolute_2017","JEC_BBEC1", "JEC_BBEC1_2017","JEC_EC2","JEC_EC2_2017","JEC_HF","JEC_HF_2017","JEC_RelativeSample_2017","JEC_RelativeBal","JEC_FlavorQCD","JER_2017"]
JME_dic["2018"]= ["JEC_Total", "JEC_Absolute","JEC_Absolute_2018","JEC_BBEC1", "JEC_BBEC1_2018","JEC_EC2","JEC_EC2_2018","JEC_HF","JEC_HF_2018","JEC_RelativeSample_2018","JEC_RelativeBal","JEC_FlavorQCD","JER"]

SystList_by_year = {year: [] for year in Years}


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
Systematics.append("Weight_ttag")


#Systematics.append("Weight_btag_b")

for year in Years:
    SystList_by_year[year] = Systematics + JME_dic[year]
    #SystList_by_year[year] = Systematics 

#print(SystList_by_year)


SystLevels = []
SystLevels.append("Up")
SystLevels.append("Down")

SampleSignal = {
         "SignalSpin32_M800"    : [rt.kMagenta,  "m_{T} = 800"],
         "SignalSpin32_M1200"   : [rt.kCyan,     "m_{T} = 1200"],
         "SignalSpin32_M1500"   : [rt.kPink,     "m_{T} = 1500"],
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
SampleWeight = ["TTGamma", "TTbar", "SignalSpin32_M800"]
SampleLumi = SampleBkg
#SampleLumi.update(SampleSignal)
SampleSyst = ["TTGamma", "OtherBkgs"] 
#SampleSyst = ["TTGamma"] 
#SampleSyst = SampleBkg.keys()
Samples = {}
Samples.update(SampleSignal)
Samples.update(SampleBkg)
Samples.update(SampleData)

myCyan = rt.kCyan
myRed = rt.kRed
myBlue = rt.kBlue

