
from Ntuple_Skim_FileLists_cff_danny import *
#-----------------------------------------
#INPUT AnalysisNtuples Directory
#----------------------------------------
dirBase = "root://cmseos.fnal.gov//store/user/rverma/Output/cms-TT-run2/Ntuple_Skim" 
dirBaseCR = dirBase
dirSyst = dirBase
dirSystCR = dirBase
dirBaseDilep = dirBase
dirSystDilep = dirBase

era16 = ["b", "c", "d", "e", "f", "g", "h"]
#era17 = ["b", "c", "d", "e", "f"]
era17 = ["b", "c", "d", "e"]
era18 = ["a", "b", "c", "d"]
data16Mu = []
data17Mu = []
data18Mu = []
data16Ele = []
data17Ele = []
data18Ele = []
for d in era16:
    data16Mu.append("Data_SingleMu_%s"%d)
    data16Ele.append("Data_SingleEle_%s"%d)
for d in era17:
    data17Mu.append("Data_SingleMu_%s"%d)
    data17Ele.append("Data_SingleEle_%s"%d)
for d in era18:
    data18Mu.append("Data_SingleMu_%s"%d)
    data18Ele.append("Data_SingleEle_%s"%d)
dataAllMu = {"2016":data16Mu, "2017":data17Mu, "2018":data18Mu}
dataAllEle = {"2016":data16Ele, "2017":data17Ele, "2018":data18Ele}
def gs(year, s_array):
    sample = []
    for s in s_array:
        sample += eval("%s_FileList_%s"%(s, year))
    return sample

def getSamples(y):
    samples = {
               "TT_tytg_M700"  : gs(y, ["TstarTstarToTgammaTgluon_M700"]),  
               "TT_tytg_M800"  : gs(y, ["TstarTstarToTgammaTgluon_M800"]),  
               "TT_tytg_M900"  : gs(y, ["TstarTstarToTgammaTgluon_M900"]),  
               "TT_tytg_M1000" : gs(y, ["TstarTstarToTgammaTgluon_M1000"]),  
               #"TT_tytg_M1100" : gs(y, ["TstarTstarToTgammaTgluon_M1100"]),  
               "TT_tytg_M1200" : gs(y, ["TstarTstarToTgammaTgluon_M1200"]),  
               "TT_tytg_M1300" : gs(y, ["TstarTstarToTgammaTgluon_M1300"]),  
               "TT_tytg_M1400" : gs(y, ["TstarTstarToTgammaTgluon_M1400"]),  
               "TT_tytg_M1500" : gs(y, ["TstarTstarToTgammaTgluon_M1500"]),  
               "TT_tytg_M1600" : gs(y, ["TstarTstarToTgammaTgluon_M1600"]),  
               "SingleTop" : gs(y, ["ST_tbarW_channel" , 
                   "ST_s_channel", 
                   "ST_t_channel" , 
                   "ST_tbar_channel", 
                   "ST_tW_channel"]),  
               "TTbar" : gs(y, ["TTbarPowheg_Hadronic" , 
                   "TTbarPowheg_Dilepton" , 
                   "TTbarPowheg_Semilept"]),
               "TTGamma": gs(y, ['TTGamma_Dilepton', 'TTGamma_Hadronic', 'TTGamma_SingleLept']),
               "Others": gs(y, ['W1jets', 'W2jets', 'W3jets', 'W4jets', 'TTWtoQQ', 'TTZtoQQ', 'WW', 'WZ', 'ZZ']),
               #TGJets
               "QCDEle"   : gs(y, ["QCD_Pt20to30_Ele",
                               "QCD_Pt30to50_Ele",
                               "QCD_Pt50to80_Ele",
                               "QCD_Pt80to120_Ele",
                               "QCD_Pt120to170_Ele",
                               "QCD_Pt170to300_Ele",
                               "QCD_Pt300toInf_Ele"]),
               "QCDMu"    : gs(y, ["QCD_Pt20to30_Mu",
                              "QCD_Pt30to50_Mu",
                              "QCD_Pt50to80_Mu",
                              "QCD_Pt80to120_Mu",
                              "QCD_Pt120to170_Mu",
                              "QCD_Pt170to300_Mu",
                              "QCD_Pt300to470_Mu",
                              "QCD_Pt470to600_Mu",
                              "QCD_Pt600to800_Mu",
                              "QCD_Pt800to1000_Mu",
                              "QCD_Pt1000toInf_Mu"
                             ]),
               "DataMu" : gs(y, dataAllMu[y]),
               "DataEle" : gs(y, dataAllEle[y])
               }
    return samples

a = getSamples("2016")
#print a
#print a.keys()
'''
    samples = {
               "TT_tytg_M700"  : gs(y, ["TstarTstarToTgammaTgluon_M700"]),  
               "TT_tytg_M800"  : gs(y, ["TstarTstarToTgammaTgluon_M800"]),  
               "TT_tytg_M900"  : gs(y, ["TstarTstarToTgammaTgluon_M900"]),  
               "TT_tytg_M1000" : gs(y, ["TstarTstarToTgammaTgluon_M1000"]),  
               "TT_tytg_M1100" : gs(y, ["TstarTstarToTgammaTgluon_M1100"]),  
               "TT_tytg_M1200" : gs(y, ["TstarTstarToTgammaTgluon_M1200"]),  
               "TT_tytg_M1300" : gs(y, ["TstarTstarToTgammaTgluon_M1300"]),  
               "TT_tytg_M1400" : gs(y, ["TstarTstarToTgammaTgluon_M1400"]),  
               "TT_tytg_M1500" : gs(y, ["TstarTstarToTgammaTgluon_M1500"]),  
               "TT_tytg_M1600" : gs(y, ["TstarTstarToTgammaTgluon_M1500"]),  
               "SingleTop" : gs(y, ["ST_tbarW_channel" , 
                   "ST_s_channel", 
                   "ST_t_channel" , 
                   "ST_tbar_channel", 
                   "ST_tW_channel"]),  
               "TTbar" : gs(y, ["TTbarPowheg_Hadronic" , 
                   "TTbarPowheg_Dilepton" , 
                   "TTbarPowheg_Semilept"]),
               "TTGamma": gs(y, ['TTGamma_Dilepton', 'TTGamma_Hadronic', 'TTGamma_SingleLept']),
               "TGJets": gs(y, ['TGJets']),
               "Wjets" : gs(y, ["W1jets" , 
                   "W2jets" , 
                   "W3jets" , 
                   "W4jets"]),  
               #"ZJets" : gs(y, ["DYjetsM50", 
               #    "DYjetsM10to50"]),  
               "TTV" : gs(y, ["TTWtoQQ" , 
                   "TTZtoQQ"]), 
                   #"TTWtoLNu",
                   #"TTZtoLL_M1to10", 
                   #"TTZtoLL"]),  
               "QCDEle"   : gs(y, ["QCD_Pt20to30_Ele",
                               "QCD_Pt30to50_Ele",
                               "QCD_Pt50to80_Ele",
                               "QCD_Pt80to120_Ele",
                               "QCD_Pt120to170_Ele",
                               "QCD_Pt170to300_Ele",
                               "QCD_Pt300toInf_Ele"]),
               "QCDMu"    : gs(y, ["QCD_Pt20to30_Mu",
                              "QCD_Pt30to50_Mu",
                              "QCD_Pt50to80_Mu",
                              "QCD_Pt80to120_Mu",
                              "QCD_Pt120to170_Mu",
                              "QCD_Pt170to300_Mu",
                              "QCD_Pt300to470_Mu",
                              "QCD_Pt470to600_Mu",
                              "QCD_Pt600to800_Mu",
                              "QCD_Pt800to1000_Mu",
                              "QCD_Pt1000toInf_Mu"
                             ]),
               "Diboson" : gs(y, ["WW" , "WZ" , "ZZ"]),  

               "DataMu" : gs(y, dataAllMu[y]),
               "DataEle" : gs(y, dataAllEle[y])
               }
    return samples
'''
