import json as js
import sys
import os

sys.path.insert(0, os.getcwd().replace("sample",""))
from DiscInputs import Years, JME_dic
from SampleInfo import dataAllMu, dataAllEle

fileName = js.load(open("FilesNtuple_cff.json", "r"))

groupDic = {
    "TTbar" :  [
    "TTbarPowheg_Hadronic" , 
    "TTbarPowheg_Dilepton" , 
    "TTbarPowheg_Semilept",
    "ST_tbarW_channel" , 
    "ST_s_channel", 
    "ST_t_channel" , 
    "ST_tbar_channel", 
    "ST_tW_channel",
    "TGJets"
    ],
"TTGamma":[
    'TTGamma_Dilepton', 
    'TTGamma_Hadronic', 
    'TTGamma_SingleLept',
    'TTGamma_Dilepton_Pt100', 
    'TTGamma_Hadronic_Pt100', 
    'TTGamma_SingleLept_Pt100',
    'TTGamma_Dilepton_Pt200', 
    'TTGamma_Hadronic_Pt200', 
    'TTGamma_SingleLept_Pt200'
    ],
"TTGamma_TuneUp": [
    'TTGamma_Dilepton_TuneUp', 
    'TTGamma_SingleLept_TuneUp',
    ],
"TTGamma_TuneDown": [
    'TTGamma_Dilepton_TuneDown', 
    'TTGamma_SingleLept_TuneDown',
    ],
"WJets": [
    'W1Jets', 
    'W2Jets', 
    'W3Jets', 
    'W4Jets', 
    ],
"DYJets": [
    'DYJetsM10to50',
    'DYJetsM50',
    ],
"WGamma":  [
    'WGamma', 
    ],
"ZGamma": [
    'ZGamma'
    ],
"QCDEle"   :  [
    "QCD_Pt15To20_Ele",
    "QCD_Pt20To30_Ele",
    "QCD_Pt30To50_Ele",
    "QCD_Pt50To80_Ele",
    "QCD_Pt80To120_Ele",
    "QCD_Pt120To170_Ele",
    "QCD_Pt170To300_Ele",
    "QCD_Pt300ToInf_Ele",
    'GJets_HT40To100',
    'GJets_HT100To200',
    'GJets_HT200To400',
    'GJets_HT400To600',
    'GJets_HT600ToInf',
    ],
"QCDMu"    :[
    "QCD_Pt15To20_Mu",
    "QCD_Pt20To30_Mu",
    "QCD_Pt30To50_Mu",
    "QCD_Pt50To80_Mu",
    "QCD_Pt80To120_Mu",
    "QCD_Pt120To170_Mu",
    "QCD_Pt170To300_Mu",
    "QCD_Pt300To470_Mu",
    "QCD_Pt470To600_Mu",
    "QCD_Pt600To800_Mu",
    "QCD_Pt800To1000_Mu",
    "QCD_Pt1000ToInf_Mu",
    "GJets_HT40To100",
    "GJets_HT100To200",
    "GJets_HT200To400",
    "GJets_HT400To600",
    "GJets_HT600ToInf"
              ],
 "Others" : [
     'TTZtoQQ',
     'TTWtoQQ',
     "TTWtoLNu",
     'TTZtoLL',
     'WW',
     'WZ',
     'ZZ'
     ]}

def getDataSamp(year):
    dicData={}
    dicData["data_obsMu"]=dataAllMu[year]
    dicData["data_obsEle"]=dataAllEle[year]
    return dicData

fileList ={}
Years = ["2016Pre", "2016Post", "2017", "2018"]
JETS = ["JetBase", "JER_up"]

def groupSample(y,j):
    if "JetBase" in j:
        groupDic.update(getDataSamp(y))
    for gkey, gvalue in groupDic.items():
        new_gkey = "Semilep_%s__%s_FileList_%s"%(j,gkey,y)
        fileList[new_gkey]=[]
        for gval in gvalue:
            new_gval = "Semilep_%s__%s_FileList_%s"%(j,gval,y)
            for key, value in fileName.items():
                if new_gval in key:
                    fileList[new_gkey].extend(value)
                    #print(new_gval,key)
                else:
                    if not "Signal" in key: continue
                    #print(new_gval,key)
                    if not y in key: continue
                    if not j in key: continue
                    fileList[key]=value
                    #fileList[key].extend(value)

#print(fileList)
for year in Years:
    print(year)
    groupSample(year, "JetBase")
    for jets in JME_dic[year]:
        for l in ["_up", "_down"]:
            groupSample(year,"%s%s"%(jets,l))
fileNtuple = open("FilesNtuple_Grouped_cff.json","w")
js.dump(fileList, fileNtuple, indent=4)
