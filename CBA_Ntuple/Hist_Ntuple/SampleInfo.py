import sys
sys.dont_write_bytecode = True
from FilesNtuple_cff import * 

era16Pre  = ["b1_preVFP", "b2_preVFP", "c_preVFP", "d_preVFP", "e_preVFP", "f_preVFP"]
era16Post = ["f_postVFP", "g_postVFP", "h_postVFP"]
era17 = ["b", "c", "d", "e", "f"]
era18 = ["a", "b", "c", "d"]
data16MuPre = []
data16MuPost = []
data17Mu = []
data18Mu = []
data16ElePre = []
data16ElePost = []
data17Ele = []
data18Ele = []
for d in era16Pre:
    data16MuPre.append("Data_SingleMu_%s"%d)
    data16ElePre.append("Data_SingleEle_%s"%d)
for d in era16Post:
    data16MuPost.append("Data_SingleMu_%s"%d)
    data16ElePost.append("Data_SingleEle_%s"%d)
for d in era17:
    data17Mu.append("Data_SingleMu_%s"%d)
    data17Ele.append("Data_SingleEle_%s"%d)
for d in era18:
    data18Mu.append("Data_SingleMu_%s"%d)
    data18Ele.append("Data_SingleEle_%s"%d)
dataAllMu = {"2016PreVFP":data16MuPre, "2016PostVFP":data16MuPost, "2017":data17Mu, "2018":data18Mu}
dataAllEle = {"2016PreVFP":data16ElePre, "2016PostVFP":data16ElePost, "2017":data17Ele, "2018":data18Ele}
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
               "Signal_M700"  : gs(y, d, syst, ["Signal_M700"]),  
               "Signal_M800"  : gs(y, d, syst, ["Signal_M800"]),  
               "Signal_M900"  : gs(y, d, syst, ["Signal_M900"]),  
               "Signal_M1000" : gs(y, d, syst, ["Signal_M1000"]),  
               #"Signal_M1100" : gs(y, d, syst, ["Signal_M1100"]),  
               "Signal_M1200" : gs(y, d, syst, ["Signal_M1200"]),  
               "Signal_M1300" : gs(y, d, syst, ["Signal_M1300"]),  
               "Signal_M1400" : gs(y, d, syst, ["Signal_M1400"]),  
               "Signal_M1500" : gs(y, d, syst, ["Signal_M1500"]),  
               "Signal_M1600" : gs(y, d, syst, ["Signal_M1600"]),  
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
                   'ZGamma'
                   ]),
               "QCDEle"   : gs(y, d, syst, [
                   "QCD_Pt30To50_Ele",
                   "QCD_Pt50To80_Ele",
                   "QCD_Pt80To120_Ele",
                   "QCD_Pt120To170_Ele",
                   "QCD_Pt170To300_Ele",
                   "QCD_Pt300ToInf_Ele",
                   #'GJets_HT40To100',
                   #'GJets_HT100To200',
                   'GJets_HT200To400',
                   'GJets_HT400To600',
                   'GJets_HT600ToInf',
                   ]),
               "QCDMu"    : gs(y, d, syst, [
                   #"QCD_Pt20To30_Mu",
                   "QCD_Pt30To50_Mu",
                   "QCD_Pt50To80_Mu",
                   "QCD_Pt80To120_Mu",
                   "QCD_Pt120To170_Mu",
                   "QCD_Pt170To300_Mu",
                   "QCD_Pt300To470_Mu",
                   "QCD_Pt470To600_Mu",
                   "QCD_Pt600To800_Mu",
                   "QCD_Pt800To1000_Mu",
                   ##"QCD_Pt1000ToInf_Mu",
                   #"GJets_HT40To100",
                   #"GJets_HT100To200",
                   "GJets_HT200To400",
                   "GJets_HT400To600",
                   "GJets_HT600ToInf"
                             ]),
               "DataMu" : gs(y, d, syst, dataAllMu[y]),
               "DataEle" : gs(y, d, syst, dataAllEle[y])
               }
               
    Others_List= [
                'TTZtoQQ',
                'TTWtoQQ', 
                "TTWtoLNu",
                'TTZtoLL',
                'WW',
                'WZ',
                'ZZ'
                ]
    samples["Others"] = gs(y, d, syst, Others_List)
    return samples

if __name__ == '__main__':
    a = getSamples("2017", "Semilep", "JetBase")
    print a.keys()
