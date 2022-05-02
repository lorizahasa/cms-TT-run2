import sys
sys.dont_write_bytecode = True
def sampleDict(year):
    # MCv1
    mcTypes = {}
    mcTypes["2016PreVFP"]  = 'RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1'
    mcTypes["2016PostVFP"] = 'RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1'
    mcTypes["2017"] = 'RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1'
    mcTypes["2018"] = 'RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1'
    # MCv2
    mcTypes2 = {}
    for key in mcTypes.keys(): 
        mcTypes2[key] = mcTypes[key].replace("-v1", "-v2")
    # MC old UL
    mcTypes3 = {} # These are used for GJets only as 20UL samples are not available
    mcTypes3["2016PreVFP"]  = 'RunIISummer19UL16NanoAODAPVv2-106X_mcRun2_asymptotic_preVFP_v9-v1'
    mcTypes3["2016PostVFP"] = 'RunIISummer19UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1'
    mcTypes3['2017'] = 'RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1'
    mcTypes3['2018'] = 'RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1'

    #Data 2016
    DataType16              ='UL2016_MiniAODv2_NanoAODv9-v1'
    DataType16_hipm         ='HIPM_UL2016_MiniAODv2_NanoAODv9-v2'
    DataType16_hipm_ver1    ='ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v2'
    DataType16_hipm_ver2    ='ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v2'
    #Data 2017
    DataType17 = 'UL2017_MiniAODv2_NanoAODv9-v1'
    #Data 2018
    DataType18       = 'UL2018_MiniAODv2_NanoAODv9-v1'
    DataType18_v2    = DataType18.replace('-v1','-v2')
    DataType18_v3    = DataType18.replace('-v1','-v3')

    #Using legacy signal samples for now, switch to UL later
    leg = {}
    leg['2016'] = ['TgammaTgluon', 'TuneCUETP8M1','RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1'] 
    if '2016' in year:
        leg[year] = ['TgammaTgluon', 'TuneCUETP8M1','RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1'] 
    leg['2017'] = ['TgluonTgamma', 'TuneCP5' ,'RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1']
    leg['2018'] = ['TgluonTgamma', 'TuneCP5' ,'RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1']
    #--------------------------
    # Signal samples
    #--------------------------
    sigSamp = {
    'Signal_M700':  '/TstarTstarTo'+leg[year][0]+'_M-700_'+leg[year][1]+'_13TeV-madgraph-pythia8/'+leg[year][2]+'/NANOAODSIM', 
    'Signal_M800':  '/TstarTstarTo'+leg[year][0]+'_M-800_'+leg[year][1]+'_13TeV-madgraph-pythia8/'+leg[year][2]+'/NANOAODSIM', 
    'Signal_M900':  '/TstarTstarTo'+leg[year][0]+'_M-900_'+leg[year][1]+'_13TeV-madgraph-pythia8/'+leg[year][2]+'/NANOAODSIM', 
    'Signal_M1000': '/TstarTstarTo'+leg[year][0]+'_M-1000_'+leg[year][1]+'_13TeV-madgraph-pythia8/'+leg[year][2]+'/NANOAODSIM', 
    #'Signal_M1100': '/TstarTstarTo'+leg[year][0]+'_M-1100_'+leg[year][1]+'_13TeV-madgraph-pythia8/'+leg[year][2]+'/NANOAODSIM', 
    'Signal_M1200': '/TstarTstarTo'+leg[year][0]+'_M-1200_'+leg[year][1]+'_13TeV-madgraph-pythia8/'+leg[year][2]+'/NANOAODSIM', 
    'Signal_M1300': '/TstarTstarTo'+leg[year][0]+'_M-1300_'+leg[year][1]+'_13TeV-madgraph-pythia8/'+leg[year][2]+'/NANOAODSIM', 
    'Signal_M1400': '/TstarTstarTo'+leg[year][0]+'_M-1400_'+leg[year][1]+'_13TeV-madgraph-pythia8/'+leg[year][2]+'/NANOAODSIM', 
    'Signal_M1500': '/TstarTstarTo'+leg[year][0]+'_M-1500_'+leg[year][1]+'_13TeV-madgraph-pythia8/'+leg[year][2]+'/NANOAODSIM', 
    'Signal_M1600': '/TstarTstarTo'+leg[year][0]+'_M-1600_'+leg[year][1]+'_13TeV-madgraph-pythia8/'+leg[year][2]+'/NANOAODSIM',  
    }

    #--------------------------
    # tty samples
    #--------------------------
    TTGamma17 = {
    'TTGamma_Hadronic_Pt200' : '/TTGamma_Hadronic_ptGamma200inf_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+leg[year][2]+'/NANOAODSIM', 
    'TTGamma_Dilepton_Pt100'  : '/TTGamma_Dilept_ptGamma100-200_TuneCP5_13TeV-madgraph-pythia8/'+mcTypes2[year].replace('v2', 'v3')+'/NANOAODSIM',
    'TTGamma_SingleLept_TuneDown' : '/TTGamma_SingleLept_TuneCP5Down_13TeV-madgraph-pythia8/'+mcTypes2[year].replace('v2', 'v3')+'/NANOAODSIM',
    }
    commonSamp = {
    #Inclusive
    'TTGamma_Hadronic'   : '/TTGamma_Hadronic_TuneCP5_13TeV-madgraph-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'TTGamma_SingleLept' : '/TTGamma_SingleLept_TuneCP5_13TeV-madgraph-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'TTGamma_Dilepton'     : '/TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    #pT binned 
    'TTGamma_Hadronic_Pt100' : '/TTGamma_Hadronic_ptGamma100-200_TuneCP5_13TeV-madgraph-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'TTGamma_Hadronic_Pt200' : '/TTGamma_Hadronic_ptGamma200inf_TuneCP5_13TeV-madgraph-pythia8/'+mcTypes2[year]+'/NANOAODSIM', #UL not avial for 2017
    'TTGamma_SingleLept_Pt100' : '/TTGamma_SingleLept_ptGamma100-200_TuneCP5_13TeV-madgraph-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'TTGamma_SingleLept_Pt200' : '/TTGamma_SingleLept_ptGamma200inf_TuneCP5_13TeV-madgraph-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'TTGamma_Dilepton_Pt100'  : '/TTGamma_Dilept_ptGamma100-200_TuneCP5_13TeV-madgraph-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'TTGamma_Dilepton_Pt200' : '/TTGamma_Dilept_ptGamma200inf_TuneCP5_13TeV-madgraph-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    #Inclusive 1lep syst 
    'TTGamma_SingleLept_TuneDown' : '/TTGamma_SingleLept_TuneCP5Down_13TeV-madgraph-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'TTGamma_SingleLept_TuneUp'   : '/TTGamma_SingleLept_TuneCP5Up_13TeV-madgraph-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    #Inclusive 2lep syst
    'TTGamma_Dilepton_TuneDown' : '/TTGamma_Dilept_TuneCP5Down_13TeV-madgraph-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'TTGamma_Dilepton_TuneUp'   : '/TTGamma_Dilept_TuneCP5Up_13TeV-madgraph-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    #--------------------------
    # tt samples
    #--------------------------
    'TTbarPowheg_Hadronic' : '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'TTbarPowheg_Semilept' : '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'TTbarPowheg_Dilepton' : '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    #--------------------------
    # single t 
    #--------------------------
    'ST_s_channel' : '/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'ST_t_channel' : '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'ST_tbar_channel' : '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'ST_tW_channel' : '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'ST_tbarW_channel' : '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'TGJets' : '/TGJets_TuneCP5_13TeV-amcatnlo-madspin-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    #--------------------------
    # y+jets
    #--------------------------
    'GJets_HT200To400'      : '/GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes3[year]+'/NANOAODSIM',
    'GJets_HT400To600'      : '/GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes3[year]+'/NANOAODSIM',
    'GJets_HT600ToInf'      : '/GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes3[year]+'/NANOAODSIM',
    #--------------------------
    # DY+jets
    #--------------------------
    'DYjetsM50'     : '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'DYjetsM10to50' : '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    #--------------------------
    # W + jets samples
    #--------------------------
    'W1jets'      : '/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'W2jets'      : '/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'W3jets'      : '/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'W4jets'      : '/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    #--------------------------
    #QCD mu
    #--------------------------
    'QCD_Pt30To50_Mu'         : '/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt50To80_Mu'         : '/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt80To120_Mu'        : '/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt120To170_Mu'       : '/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt170To300_Mu'       : '/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt300To470_Mu'       : '/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt470To600_Mu'       : '/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt600To800_Mu'       : '/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt800To1000_Mu'      : '/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt1000ToInf_Mu'      : '/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    #--------------------------
    #QCD ele
    #--------------------------
    'QCD_Pt30to50_Ele'        : '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt50to80_Ele'        : '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt80to120_Ele'       : '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt120to170_Ele'      : '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt170to300_Ele'      : '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'QCD_Pt300toInf_Ele'      : '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    #--------------------------
    # W/Z + y
    #--------------------------
    'WGamma' : '/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'ZGamma' : '/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    #--------------------------
    # VV 
    #--------------------------
    'WW'      : '/WW_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'WZ'      : '/WZ_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'ZZ'      : '/ZZ_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    #--------------------------
    # ttV 
    #--------------------------
    'TTZtoQQ' : '/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'TTWtoQQ' : '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'TTWtoLNu' : '/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'TTZtoLL' : '/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    }

    preSamp = {
    'W1jets'      : '/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'W2jets'      : '/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'W3jets'      : '/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'ST_tW_channel' : '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'ST_tbarW_channel' : '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'TGJets' : '/TGJets_TuneCP5_13TeV-amcatnlo-madspin-pythia8/'+mcTypes[year].replace("-v1", '_ext1-v1')+'/NANOAODSIM',
    'TTWtoQQ' : '/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    'TTWtoLNu' : '/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/'+mcTypes2[year]+'/NANOAODSIM',
    }
    postSamp = {
    'QCD_Pt30To50_Mu'         : '/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'QCD_Pt50To80_Mu'         : '/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'QCD_Pt80To120_Mu'        : '/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'QCD_Pt120To170_Mu'       : '/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'QCD_Pt170To300_Mu'       : '/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'QCD_Pt300To470_Mu'       : '/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'QCD_Pt470To600_Mu'       : '/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'QCD_Pt600To800_Mu'       : '/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'QCD_Pt800To1000_Mu'      : '/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    'QCD_Pt1000ToInf_Mu'      : '/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/'+mcTypes[year]+'/NANOAODSIM',
    }
    #--------------------------
    # Data 
    #--------------------------
    dataSamp16Pre = {
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

    dataSamp16Post = {
    # muon
    'Data_SingleMu_f_postVFP' : '/SingleMuon/Run2016F-'+DataType16+'/NANOAOD',
    'Data_SingleMu_g_postVFP' : '/SingleMuon/Run2016G-'+DataType16+'/NANOAOD',
    'Data_SingleMu_h_postVFP' : '/SingleMuon/Run2016H-'+DataType16+'/NANOAOD',
    # electron
    'Data_SingleEle_f_postVFP' : '/SingleElectron/Run2016F-'+DataType16+'/NANOAOD',
    'Data_SingleEle_g_postVFP' : '/SingleElectron/Run2016G-'+DataType16+'/NANOAOD',
    'Data_SingleEle_h_postVFP' : '/SingleElectron/Run2016H-'+DataType16+'/NANOAOD',
    }

    dataSamp17 = {
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

    dataSamp18 = {
    # muon
    'Data_SingleMu_a' : '/SingleMuon/Run2018A-'+DataType18_v2+'/NANOAOD',
    'Data_SingleMu_b' : '/SingleMuon/Run2018B-'+DataType18_v2+'/NANOAOD',
    'Data_SingleMu_c' : '/SingleMuon/Run2018C-'+DataType18_v2+'/NANOAOD',
    'Data_SingleMu_d' : '/SingleMuon/Run2018D-'+DataType18+'/NANOAOD',
    # electron
    'Data_SingleEle_a' : '/EGamma/Run2018A-'+DataType18+'/NANOAOD',
    'Data_SingleEle_b' : '/EGamma/Run2018B-'+DataType18+'/NANOAOD',
    'Data_SingleEle_c' : '/EGamma/Run2018C-'+DataType18+'/NANOAOD',
    'Data_SingleEle_d' : '/EGamma/Run2018D-'+DataType18_v3+'/NANOAOD',
    }
    allSamples = {}
    if '2016' in year:
        allSamples.update(commonSamp)
        allSamples.update(sigSamp)
        if "Pre" in year:
            allSamples.update(preSamp)
            allSamples.update(dataSamp16Pre)
        if "Post" in year:
            allSamples.update(postSamp)
            allSamples.update(dataSamp16Post)
    if '2017' in year:
        allSamples.update(commonSamp)
        allSamples.update(TTGamma17)
        allSamples.update(sigSamp)
        allSamples.update(dataSamp17)
    if '2018' in year:
        allSamples.update(commonSamp)
        allSamples.update(sigSamp)
        allSamples.update(dataSamp18)

    return allSamples

if __name__=="__main__":
    samp = sampleDict('2016PreVFP')
    #samp = sampleDict('2016PostVFP')
    #samp = sampleDict('2017')
    #samp = sampleDict('2018')
    print(samp)

