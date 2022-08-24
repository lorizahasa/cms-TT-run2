import sys
sys.dont_write_bytecode = True

Runs = {}
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVRun2LegacyAnalysis
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/XsdbTutorialSep
Runs["2016Pre"]  = 'RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11'
Runs["2016Post"] = 'RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17'
Runs["2017"] = 'RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9'
Runs["2018"] = 'RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1'

#--------------------------
# t*t* signal
#--------------------------
def getSignal(year, ch):
    vs = {'2016Pre': 'v1', '2016Post': 'v1', '2017': 'v1', '2018': 'v1'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict = {
    'Signal_M700':   '/TstarTstarTo%s_M-700_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    'Signal_M800':   '/TstarTstarTo%s_M-800_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M900':   '/TstarTstarTo%s_M-900_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M1000':  '/TstarTstarTo%s_M-1000_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M1100':  '/TstarTstarTo%s_M-1100_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    'Signal_M1200':  '/TstarTstarTo%s_M-1200_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    'Signal_M1300':  '/TstarTstarTo%s_M-1300_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M1400':  '/TstarTstarTo%s_M-1400_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    'Signal_M1500':  '/TstarTstarTo%s_M-1500_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M1600':  '/TstarTstarTo%s_M-1600_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M1700':  '/TstarTstarTo%s_M-1700_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M1800':  '/TstarTstarTo%s_M-1800_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M1900':  '/TstarTstarTo%s_M-1900_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M2000':  '/TstarTstarTo%s_M-2000_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M2250':  '/TstarTstarTo%s_M-2250_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M2500':  '/TstarTstarTo%s_M-2500_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M2750':  '/TstarTstarTo%s_M-2750_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    #'Signal_M3000':  '/TstarTstarTo%s_M-3000_TuneCP5_13TeV-madgraph-pythia8/'%ch+runV+'/NANOAODSIM',
    }
    return sampDict

#--------------------------
#TTGamma
#--------------------------
def getTTGamma(year):
    vs = {'2016Pre': 'v1', '2016Post': 'v1', '2017': 'v1', '2018': 'v1'}
    runV = "%s-%s"%(Runs[year], vs[year])
    #Inclusive
    sampDict1 = {
    'TTGamma_Hadronic'   : '/TTGamma_Hadronic_TuneCP5_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM',
    'TTGamma_SingleLept' : '/TTGamma_SingleLept_TuneCP5_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM',
    'TTGamma_Dilepton'   : '/TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM',
    }
    #pT binned and sys 
    vs = {'2016Pre': 'v2', '2016Post': 'v2', '2017': 'v2', '2018': 'v2'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict2 = {
    'TTGamma_Hadronic_Pt100' : '/TTGamma_Hadronic_ptGamma100-200_TuneCP5_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM',
    'TTGamma_SingleLept_Pt100' : '/TTGamma_SingleLept_ptGamma100-200_TuneCP5_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM',
    'TTGamma_SingleLept_Pt200' : '/TTGamma_SingleLept_ptGamma200inf_TuneCP5_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM',
    'TTGamma_Dilepton_Pt200' : '/TTGamma_Dilept_ptGamma200inf_TuneCP5_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM',
    'TTGamma_SingleLept_TuneUp'   : '/TTGamma_SingleLept_TuneCP5Up_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM',
    'TTGamma_Dilepton_TuneDown' : '/TTGamma_Dilept_TuneCP5Down_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM',
    'TTGamma_Dilepton_TuneUp'   : '/TTGamma_Dilept_TuneCP5Up_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM',
    }
    #pT binned and sys 
    vs = {'2016Pre': 'v2', '2016Post': 'v2', '2017': 'v3', '2018': 'v2'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict3 = {
    'TTGamma_Dilepton_Pt100'  : '/TTGamma_Dilept_ptGamma100-200_TuneCP5_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM',
    'TTGamma_SingleLept_TuneDown' : '/TTGamma_SingleLept_TuneCP5Down_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM',
    'TTGamma_Hadronic_Pt200' : '/TTGamma_Hadronic_ptGamma200inf_TuneCP5_13TeV-madgraph-pythia8/'+runV+'/NANOAODSIM', 
    }
    sampDict = {}
    sampDict.update(sampDict1)
    sampDict.update(sampDict2)
    sampDict.update(sampDict3)
    return sampDict

#--------------------------
# TTbar
#--------------------------
def getTTbar(year):
    vs = {'2016Pre': 'v1', '2016Post': 'v1', '2017': 'v1', '2018': 'v1'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict = {
    'TTbarPowheg_Hadronic' : '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/'+runV+'/NANOAODSIM',
    'TTbarPowheg_Semilept' : '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/'+runV+'/NANOAODSIM',
    'TTbarPowheg_Dilepton' : '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/'+runV+'/NANOAODSIM',
    }
    return sampDict

#--------------------------
# single t 
#--------------------------
def getST(year):
    vs = {'2016Pre': 'v1', '2016Post': 'v1', '2017': 'v1', '2018': 'v1'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict1 = {
    'TGJets' : '/TGJets_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/'+runV+'/NANOAODSIM',
    'ST_t_channel' : '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/'+runV+'/NANOAODSIM',
    'ST_tbar_channel' : '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/'+runV+'/NANOAODSIM',
    'ST_s_channel' : '/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/'+runV+'/NANOAODSIM',
    }
    vs = {'2016Pre': 'v1', '2016Post': 'v2', '2017': 'v2', '2018': 'v2'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict2 = {
    'ST_tW_channel' : '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/'+runV+'/NANOAODSIM',
    'ST_tbarW_channel' : '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/'+runV+'/NANOAODSIM',
    }
    sampDict = {}
    sampDict.update(sampDict1)
    sampDict.update(sampDict2)
    return sampDict

#--------------------------
# y+jets
#--------------------------
def getGJets(year):
    vs = {'2016Pre': 'v2', '2016Post': 'v2', '2017': 'v1', '2018': 'v1'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict = {
    #'GJets_HT40To100'       : '/GJets_DR-0p4_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8/'+runV+'/NANOAODSIM',#NA
    'GJets_HT100To200'      : '/GJets_DR-0p4_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/'+runV+'/NANOAODSIM',
    'GJets_HT200To400'      : '/GJets_DR-0p4_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/'+runV+'/NANOAODSIM',
    'GJets_HT400To600'      : '/GJets_DR-0p4_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/'+runV+'/NANOAODSIM',
    'GJets_HT600ToInf'      : '/GJets_DR-0p4_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/'+runV+'/NANOAODSIM',
    }
    return sampDict

#--------------------------
# DYJets
#--------------------------
def getDYJets(year):
    vs = {'2016Pre': 'v1', '2016Post': 'v1', '2017': 'v1', '2018': 'v1'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict = {
    'DYJetsM10to50' : '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/'+runV+'/NANOAODSIM',
    'DYJetsM50'     : '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/'+runV+'/NANOAODSIM',
    }
    return sampDict

#--------------------------
# WJets
#--------------------------
def getWJets(year):
    vs = {'2016Pre': 'v2', '2016Post': 'v1', '2017': 'v1', '2018': 'v1'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict1 = {
    'W1Jets'      : '/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/'+runV+'/NANOAODSIM',
    'W2Jets'      : '/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/'+runV+'/NANOAODSIM',
    'W3Jets'      : '/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/'+runV+'/NANOAODSIM',
    }
    vs = {'2016Pre': 'v2', '2016Post': 'v2', '2017': 'v2', '2018': 'v2'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict2 = {
    'W4Jets'      : '/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/'+runV+'/NANOAODSIM',
    }
    sampDict = {}
    sampDict.update(sampDict1)
    sampDict.update(sampDict2)
    return sampDict

#--------------------------
# W/Z + y
#--------------------------
def getWZGamma(year):
    vs = {'2016Pre': 'v1', '2016Post': 'v1', '2017': 'v1', '2018': 'v1'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict = {
    'WGamma' : '/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/'+runV+'/NANOAODSIM',
    'ZGamma' : '/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/'+runV+'/NANOAODSIM',
    }
    return sampDict

#--------------------------
# VV 
#--------------------------
def getVV(year):
    vs = {'2016Pre': 'v1', '2016Post': 'v1', '2017': 'v1', '2018': 'v1'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict = {
    'WW'      : '/WW_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'WZ'      : '/WZ_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'ZZ'      : '/ZZ_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    }
    return sampDict

#--------------------------
# TTV 
#--------------------------
def getTTV(year):
    vs = {'2016Pre': 'v1', '2016Post': 'v1', '2017': 'v1', '2018': 'v1'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict1 = {
    'TTZtoQQ' : '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/'+runV+'/NANOAODSIM',
    'TTZtoLL' : '/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/'+runV+'/NANOAODSIM',
    }
    vs = {'2016Pre': 'v2', '2016Post': 'v1', '2017': 'v1', '2018': 'v1'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict2 = {
    'TTWtoQQ' : '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/'+runV+'/NANOAODSIM',
    'TTWtoLNu' : '/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/'+runV+'/NANOAODSIM',
    }
    sampDict = {}
    sampDict.update(sampDict1)
    sampDict.update(sampDict2)
    return sampDict

#--------------------------
#QCD mu
#--------------------------
def getQCDMu(year):
    vs = {'2016Pre': 'v2', '2016Post': 'v1', '2017': 'v2', '2018': 'v2'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict1 = {
    'QCD_Pt20To30_Mu'         : '/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt30To50_Mu'         : '/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt50To80_Mu'         : '/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt80To120_Mu'        : '/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt120To170_Mu'       : '/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt170To300_Mu'       : '/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt300To470_Mu'       : '/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt470To600_Mu'       : '/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt600To800_Mu'       : '/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt800To1000_Mu'      : '/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt1000ToInf_Mu'      : '/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    }
    vs = {'2016Pre': 'v2', '2016Post': 'v2', '2017': 'v2', '2018': 'v2'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict2 = {
    'QCD_Pt15To20_Mu'         : '/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    }
    sampDict = {}
    sampDict.update(sampDict1)
    sampDict.update(sampDict2)
    return sampDict

#--------------------------
#QCD ele
#--------------------------
def getQCDEle(year):
    vs = {'2016Pre': 'v2', '2016Post': 'v2', '2017': 'v2', '2018': 'v2'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict1 = {
    'QCD_Pt30To50_Ele'        : '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt50To80_Ele'        : '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt80To120_Ele'       : '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt120To170_Ele'      : '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt170To300_Ele'      : '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    'QCD_Pt300ToInf_Ele'      : '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    }
    #### 15To20 #####
    vs = {'2016Pre': 'v1', '2016Post': 'v1', '2017': 'v2', '2018': 'v2'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict2 = {
    'QCD_Pt15To20_Ele'        : '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    }
    if 'Pre' in year:#FIXME
        sampDict2['QCD_Pt15To20_Ele'] = sampDict2['QCD_Pt15To20_Ele'].replace('APVv9', 'APVv2')
        sampDict2['QCD_Pt15To20_Ele'] = sampDict2['QCD_Pt15To20_Ele'].replace('v11', 'v9')
    #### 20To30 #####
    vs = {'2016Pre': 'v1', '2016Post': 'v2', '2017': 'v2', '2018': 'v1'}
    runV = "%s-%s"%(Runs[year], vs[year])
    sampDict3 = {
    'QCD_Pt20To30_Ele'        : '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/'+runV+'/NANOAODSIM',
    }
    if 'Pre' in year:#FIXME
        sampDict3['QCD_Pt20To30_Ele'] = sampDict3['QCD_Pt20To30_Ele'].replace('APVv9', 'APVv2')
        sampDict3['QCD_Pt20To30_Ele'] = sampDict3['QCD_Pt20To30_Ele'].replace('v11', 'v9')
    sampDict = {}
    sampDict.update(sampDict1)
    sampDict.update(sampDict2)
    sampDict.update(sampDict3)
    return sampDict

#--------------------------
# Data
#--------------------------
def getData(year):
    #2016 Pre
    DataType16_hipm         ='HIPM_UL2016_MiniAODv2_NanoAODv9-v2'
    DataType16_hipm_ver1    ='ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v2'
    DataType16_hipm_ver2    ='ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v2'
    sampDict16Pre = {
    # muon
    'Data_SingleMu_b1_preVFP' : '/SingleMuon/Run2016B-'+DataType16_hipm_ver1+'/NANOAOD',
    'Data_SingleMu_b2_preVFP' : '/SingleMuon/Run2016B-'+DataType16_hipm_ver2+'/NANOAOD',
    'Data_SingleMu_c_preVFP' : '/SingleMuon/Run2016C-'+DataType16_hipm+'/NANOAOD',
    'Data_SingleMu_d_preVFP' : '/SingleMuon/Run2016D-'+DataType16_hipm+'/NANOAOD',
    'Data_SingleMu_e_preVFP' : '/SingleMuon/Run2016E-'+DataType16_hipm+'/NANOAOD',
    'Data_SingleMu_f_preVFP' : '/SingleMuon/Run2016F-'+DataType16_hipm+'/NANOAOD',
    # electron
    'Data_SingleEle_b1_preVFP' : '/SingleElectron/Run2016B-'+DataType16_hipm_ver1+'/NANOAOD',
    'Data_SingleEle_b2_preVFP' : '/SingleElectron/Run2016B-'+DataType16_hipm_ver2+'/NANOAOD',
    'Data_SingleEle_c_preVFP' : '/SingleElectron/Run2016C-'+DataType16_hipm+'/NANOAOD',
    'Data_SingleEle_d_preVFP' : '/SingleElectron/Run2016D-'+DataType16_hipm+'/NANOAOD',
    'Data_SingleEle_e_preVFP' : '/SingleElectron/Run2016E-'+DataType16_hipm+'/NANOAOD',
    'Data_SingleEle_f_preVFP' : '/SingleElectron/Run2016F-'+DataType16_hipm+'/NANOAOD',
    }

    #2016 Post 
    DataType16              ='UL2016_MiniAODv2_NanoAODv9-v1'
    sampDict16Post = {
    # muon
    'Data_SingleMu_f_postVFP' : '/SingleMuon/Run2016F-'+DataType16+'/NANOAOD',
    'Data_SingleMu_g_postVFP' : '/SingleMuon/Run2016G-'+DataType16+'/NANOAOD',
    'Data_SingleMu_h_postVFP' : '/SingleMuon/Run2016H-'+DataType16+'/NANOAOD',
    # electron
    'Data_SingleEle_f_postVFP' : '/SingleElectron/Run2016F-'+DataType16+'/NANOAOD',
    'Data_SingleEle_g_postVFP' : '/SingleElectron/Run2016G-'+DataType16+'/NANOAOD',
    'Data_SingleEle_h_postVFP' : '/SingleElectron/Run2016H-'+DataType16+'/NANOAOD',
    }
    
    #2017
    DataType17 = 'UL2017_MiniAODv2_NanoAODv9-v1'
    sampDict17 = {
    # muon
    'Data_SingleMu_b' : '/SingleMuon/Run2017B-'+DataType17+'/NANOAOD',
    'Data_SingleMu_c' : '/SingleMuon/Run2017C-'+DataType17+'/NANOAOD',
    'Data_SingleMu_d' : '/SingleMuon/Run2017D-'+DataType17+'/NANOAOD',
    'Data_SingleMu_e' : '/SingleMuon/Run2017E-'+DataType17+'/NANOAOD',
    'Data_SingleMu_f' : '/SingleMuon/Run2017F-'+DataType17+'/NANOAOD',
    # electron
    'Data_SingleEle_b' : '/SingleElectron/Run2017B-'+DataType17+'/NANOAOD',
    'Data_SingleEle_c' : '/SingleElectron/Run2017C-'+DataType17+'/NANOAOD',
    'Data_SingleEle_d' : '/SingleElectron/Run2017D-'+DataType17+'/NANOAOD',
    'Data_SingleEle_e' : '/SingleElectron/Run2017E-'+DataType17+'/NANOAOD',
    'Data_SingleEle_f' : '/SingleElectron/Run2017F-'+DataType17+'/NANOAOD',
    }
    
    #2018
    DataType18_GT       = 'UL2018_MiniAODv2_NanoAODv9_GT36-v1'
    DataType18       = 'UL2018_MiniAODv2_NanoAODv9-v1'
    DataType18_v3    = DataType18.replace('-v1','-v3')
    sampDict18 = {
    # muon
    'Data_SingleMu_a' : '/SingleMuon/Run2018A-'+DataType18_GT+'/NANOAOD',
    'Data_SingleMu_b' : '/SingleMuon/Run2018B-'+DataType18_GT+'/NANOAOD',
    'Data_SingleMu_c' : '/SingleMuon/Run2018C-'+DataType18_GT+'/NANOAOD',
    'Data_SingleMu_d' : '/SingleMuon/Run2018D-'+DataType18_GT+'/NANOAOD',
    # electron
    'Data_SingleEle_a' : '/EGamma/Run2018A-'+DataType18+'/NANOAOD',
    'Data_SingleEle_b' : '/EGamma/Run2018B-'+DataType18+'/NANOAOD',
    'Data_SingleEle_c' : '/EGamma/Run2018C-'+DataType18+'/NANOAOD',
    'Data_SingleEle_d' : '/EGamma/Run2018D-'+DataType18_v3+'/NANOAOD',
    }
    sampDict = {}
    sampDict['2016Pre']     = sampDict16Pre
    sampDict['2016Post']    = sampDict16Post
    sampDict['2017']        = sampDict17
    sampDict['2018']        = sampDict18
    return sampDict[year]

def getMC(year):
    sampDict = {}
    #signal
    #sampDict.update(getSignal(year, "TgluonTgluon"))
    #sampDict.update(getSignal(year, "TgammaTgamma"))
    sampDict.update(getSignal(year, "TgluonTgamma"))
    #bkgs
    sampDict.update(getTTGamma(year))
    sampDict.update(getTTbar(year))
    sampDict.update(getST(year))
    sampDict.update(getGJets(year))
    sampDict.update(getDYJets(year))
    sampDict.update(getWJets(year))
    sampDict.update(getWZGamma(year))
    sampDict.update(getVV(year))
    sampDict.update(getTTV(year))
    sampDict.update(getQCDMu(year))
    sampDict.update(getQCDEle(year))
    return sampDict

def sampleDict(year):
    allSamples = {}
    allSamples.update(getData(year))
    allSamples.update(getMC(year))
    return allSamples

if __name__=="__main__":
    samp = sampleDict('2016Pre')
    #samp = sampleDict('2016Post')
    #samp = sampleDict('2017')
    #samp = sampleDict('2018')
    print(samp)

