
from Ntuple_Skim_FileLists_cff_danny import *
era16 = ["b", "c", "d", "e", "f", "g", "h"]
era17 = ["b", "c", "d", "e", "f"]
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
def gs(y, d, syst, s_array):
    sample = []
    for s in s_array:
        if "Data" in s and not "Base" in syst:
            sample += eval("%s_%s__%s_FileList_%s"%(d, "JetBase", s, y))
        else:
            sample += eval("%s_%s__%s_FileList_%s"%(d, syst, s, y))
    return sample

def getSamples(y, d, syst):
    samples = {
               "TT_tytg_M700"  : gs(y, d, syst, ["TstarTstarToTgammaTgluon_M700"]),  
               "TT_tytg_M800"  : gs(y, d, syst, ["TstarTstarToTgammaTgluon_M800"]),  
               "TT_tytg_M900"  : gs(y, d, syst, ["TstarTstarToTgammaTgluon_M900"]),  
               "TT_tytg_M1000" : gs(y, d, syst, ["TstarTstarToTgammaTgluon_M1000"]),  
               #"TT_tytg_M1100" : gs(y, d, syst, ["TstarTstarToTgammaTgluon_M1100"]),  
               "TT_tytg_M1200" : gs(y, d, syst, ["TstarTstarToTgammaTgluon_M1200"]),  
               "TT_tytg_M1300" : gs(y, d, syst, ["TstarTstarToTgammaTgluon_M1300"]),  
               "TT_tytg_M1400" : gs(y, d, syst, ["TstarTstarToTgammaTgluon_M1400"]),  
               "TT_tytg_M1500" : gs(y, d, syst, ["TstarTstarToTgammaTgluon_M1500"]),  
               "TT_tytg_M1600" : gs(y, d, syst, ["TstarTstarToTgammaTgluon_M1600"]),  
               "TTbar" : gs(y, d, syst, [
                   "TTbarPowheg_Hadronic" , 
                   "TTbarPowheg_Dilepton" , 
                   "TTbarPowheg_Semilept",
                   "ST_tbarW_channel" , 
                   "ST_s_channel", 
                   "ST_t_channel" , 
                   "ST_tbar_channel", 
                   "ST_tW_channel",
                   "TGJets"
                   ]),
               "TTGamma": gs(y, d, syst, [
                   'TTGamma_Dilepton', 
                   'TTGamma_Hadronic', 
                   'TTGamma_SingleLept',
                   'TTGamma_Dilepton_Pt100', 
                   'TTGamma_Hadronic_Pt100', 
                   'TTGamma_SingleLept_Pt100',
                   'TTGamma_Dilepton_Pt200', 
                   'TTGamma_Hadronic_Pt200', 
                   'TTGamma_SingleLept_Pt200'
                   ]),
               "WJets": gs(y, d, syst, [
                   'W1jets', 
                   'W2jets', 
                   'W3jets', 
                   'W4jets', 
                   ]),
               "DYJets": gs(y, d, syst, [
                   'DYjetsM10to50',
                   'DYjetsM50',
                   ]),
               "WGamma": gs(y, d, syst, [
                   'WGamma', 
                   ]),
               "ZGamma": gs(y, d, syst, [
                   'ZGamma_01J_5f_lowMass'
                   ]),
               "QCDEle"   : gs(y, d, syst, [
                   "QCD_Pt20to30_Ele",
                   "QCD_Pt30to50_Ele",
                   "QCD_Pt50to80_Ele",
                   "QCD_Pt80to120_Ele",
                   "QCD_Pt120to170_Ele",
                   "QCD_Pt170to300_Ele",
                   "QCD_Pt300toInf_Ele",
                   "QCD_Pt20to30_bcToE",  
                   "QCD_Pt30to80_bcToE",  
                   "QCD_Pt80to170_bcToE", 
                   "QCD_Pt170to250_bcToE",
                   "QCD_Pt250toInf_bcToE",
                   'GJets_HT40To100',
                   'GJets_HT100To200',
                   'GJets_HT200To400',
                   'GJets_HT400To600',
                   'GJets_HT600ToInf',
                   ]),
               "QCDMu"    : gs(y, d, syst, [
                   "QCD_Pt20to30_Mu",
                   "QCD_Pt30to50_Mu",
                   "QCD_Pt50to80_Mu",
                   "QCD_Pt80to120_Mu",
                   "QCD_Pt120to170_Mu",
                   "QCD_Pt170to300_Mu",
                   "QCD_Pt300to470_Mu",
                   "QCD_Pt470to600_Mu",
                   "QCD_Pt600to800_Mu",
                   "QCD_Pt800to1000_Mu",
                   "QCD_Pt1000toInf_Mu",
                   "QCD_Pt20to30_bcToE",  
                   "QCD_Pt30to80_bcToE",  
                   "QCD_Pt80to170_bcToE", 
                   "QCD_Pt170to250_bcToE",
                   "QCD_Pt250toInf_bcToE",
                   "GJets_HT40To100",
                   "GJets_HT100To200",
                   "GJets_HT200To400",
                   "GJets_HT400To600",
                   "GJets_HT600ToInf"
                             ]),
               "DataMu" : gs(y, d, syst, dataAllMu[y]),
               "DataEle" : gs(y, d, syst, dataAllEle[y])
               }
               
    Others_List= [
                'TTWtoQQ', 
                "TTWtoLNu",
                'TTZtoQQ',
                'TTZtoLL',
                'TTZtoLL_M1to10',
                'WWToLNuQQ_powheg',
                'WWTo4Q_powheg',
                'WZTo1L3Nu_amcatnlo',
                'WZTo1L1Nu2Q_amcatnlo',
                'WZTo2L2Q_amcatnlo',
                'WZTo3LNu_powheg',
                'ZZTo4L_powheg',
                'ZZTo2Q2Nu_amcatnlo',
                'VVTo2L2Nu_amcatnlo'
                ]
    if y =="2016":
        Others_List.append("ZZTo2L2Q_powheg")
    else:
        Others_List.append("ZZTo2L2Q_amcatnlo")
    samples["Others"] = gs(y, d, syst, Others_List)
    return samples

if __name__ == '__main__':
    a = getSamples("2016", "Semilep", "JetBase")
    print a.keys()
