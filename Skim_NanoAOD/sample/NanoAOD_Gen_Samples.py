
#--------------------------
# 2016
#--------------------------
MCType16='RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1'
DataType16='Nano1June2019-v1'
DataType16_ver2='_ver2-Nano1June2019_ver2-v1'
sampleList_2016 = {
'TT_tytg_M700':  '/TstarTstarToTgammaTgluon_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM', 
'TT_tytg_M800':  '/TstarTstarToTgammaTgluon_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM', 
'TT_tytg_M900':  '/TstarTstarToTgammaTgluon_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM', 
'TT_tytg_M1000': '/TstarTstarToTgammaTgluon_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM', 
#'TT_tytg_M1100': '/TstarTstarToTgammaTgluon_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM', 
'TT_tytg_M1200': '/TstarTstarToTgammaTgluon_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM', 
'TT_tytg_M1300': '/TstarTstarToTgammaTgluon_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM', 
'TT_tytg_M1400': '/TstarTstarToTgammaTgluon_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM', 
'TT_tytg_M1500': '/TstarTstarToTgammaTgluon_M-1500_TuneCUETP8M1_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM', 
'TT_tytg_M1600': '/TstarTstarToTgammaTgluon_M-1600_TuneCUETP8M1_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM', 

'TTGamma_Dilepton'     : '/TTGamma_Dilept_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM',
'TTGamma_Hadronic'   : '/TTGamma_Hadronic_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM',
'TTGamma_SingleLept' : '/TTGamma_SingleLept_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM',

'TTbarPowheg_Dilepton' : '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType16+'/NANOAODSIM',
'TTbarPowheg_Hadronic' : '/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType16+'/NANOAODSIM',
'TTbarPowheg_Semilept' : '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType16+'/NANOAODSIM',
'TGJets' : '/TGJets_TuneCUETP8M1_13TeV_amcatnlo_madspin_pythia8/'+MCType16+'/NANOAODSIM',

'ST_s_channel' : '/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/'+MCType16+'/NANOAODSIM',
'ST_t_channel' : '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType16+'/NANOAODSIM',
'ST_tbar_channel' : '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType16+'/NANOAODSIM',
'ST_tW_channel' : '/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType16+'/NANOAODSIM',
'ST_tbarW_channel' : '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType16+'/NANOAODSIM',

'Data_SingleMu_b' : '/SingleMuon/Run2016B'+DataType16_ver2+'/NANOAOD',
'Data_SingleMu_c' : '/SingleMuon/Run2016C-'+DataType16+'/NANOAOD',
'Data_SingleMu_d' : '/SingleMuon/Run2016D-'+DataType16+'/NANOAOD',
'Data_SingleMu_e' : '/SingleMuon/Run2016E-'+DataType16+'/NANOAOD',
'Data_SingleMu_f' : '/SingleMuon/Run2016F-'+DataType16+'/NANOAOD',
'Data_SingleMu_g' : '/SingleMuon/Run2016G-'+DataType16+'/NANOAOD',
'Data_SingleMu_h' : '/SingleMuon/Run2016H-'+DataType16+'/NANOAOD',

'Data_SingleEle_b' : '/SingleElectron/Run2016B'+DataType16_ver2+'/NANOAOD',
'Data_SingleEle_c' : '/SingleElectron/Run2016C-'+DataType16+'/NANOAOD',
'Data_SingleEle_d' : '/SingleElectron/Run2016D-'+DataType16+'/NANOAOD',
'Data_SingleEle_e' : '/SingleElectron/Run2016E-'+DataType16+'/NANOAOD',
'Data_SingleEle_f' : '/SingleElectron/Run2016F-'+DataType16+'/NANOAOD',
'Data_SingleEle_g' : '/SingleElectron/Run2016G-'+DataType16+'/NANOAOD',
'Data_SingleEle_h' : '/SingleElectron/Run2016H-'+DataType16+'/NANOAOD',

}

#--------------------------
# 2017
#--------------------------
MCType17 = 'RunIIFall17NanoAODv6-PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1'
MCType17_pmx = MCType17.replace('102X','new_pmx_102X')
DataType17='Nano1June2019-v1'
sampleList_2017 = {
'TT_tytg_M700':  '/TstarTstarToTgluonTgamma_M-700_TuneCP5_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM', 
'TT_tytg_M800':  '/TstarTstarToTgluonTgamma_M-800_TuneCP5_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM', 
'TT_tytg_M900':  '/TstarTstarToTgluonTgamma_M-900_TuneCP5_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM', 
'TT_tytg_M1000': '/TstarTstarToTgluonTgamma_M-1000_TuneCP5_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM', 
#'TT_tytg_M1100': '/TstarTstarToTgluonTgamma_M-1100_TuneCP5_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM', 
'TT_tytg_M1200': '/TstarTstarToTgluonTgamma_M-1200_TuneCP5_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM', 
'TT_tytg_M1300': '/TstarTstarToTgluonTgamma_M-1300_TuneCP5_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM', 
'TT_tytg_M1400': '/TstarTstarToTgluonTgamma_M-1400_TuneCP5_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM', 
'TT_tytg_M1500': '/TstarTstarToTgluonTgamma_M-1500_TuneCP5_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM', 
'TT_tytg_M1600': '/TstarTstarToTgluonTgamma_M-1600_TuneCP5_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM', 

'TTGamma_Dilepton'     : '/TTGamma_Dilept_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM',
'TTGamma_Hadronic'   : '/TTGamma_Hadronic_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM',
'TTGamma_SingleLept' : '/TTGamma_SingleLept_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType17+'/NANOAODSIM',

'TTbarPowheg_Dilepton' : '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType17_pmx+'/NANOAODSIM',
'TTbarPowheg_Hadronic' : '/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType17_pmx+'/NANOAODSIM',
'TTbarPowheg_Semilept' : '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType17+'/NANOAODSIM',
'TGJets' : '/TGJets_TuneCP5_13TeV_amcatnlo_madspin_pythia8/'+MCType17+'/NANOAODSIM',

'ST_s_channel'     : '/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/'+MCType17_pmx+'/NANOAODSIM',
'ST_t_channel'     : '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType17+'/NANOAODSIM',
'ST_tbar_channel'  : '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType17+'/NANOAODSIM',
'ST_tW_channel'    : '/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType17_pmx+'/NANOAODSIM',
'ST_tbarW_channel' : '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType17+'/NANOAODSIM',

'Data_SingleMu_b' : '/SingleMuon/Run2017B-'+DataType17+'/NANOAOD',
'Data_SingleMu_c' : '/SingleMuon/Run2017C-'+DataType17+'/NANOAOD',
'Data_SingleMu_d' : '/SingleMuon/Run2017D-'+DataType17+'/NANOAOD',
'Data_SingleMu_e' : '/SingleMuon/Run2017E-'+DataType17+'/NANOAOD',
'Data_SingleMu_f' : '/SingleMuon/Run2017F-'+DataType17+'/NANOAOD',

'Data_SingleEle_b' : '/SingleElectron/Run2017B-'+DataType17+'/NANOAOD',
'Data_SingleEle_c' : '/SingleElectron/Run2017C-'+DataType17+'/NANOAOD',
'Data_SingleEle_d' : '/SingleElectron/Run2017D-'+DataType17+'/NANOAOD',
'Data_SingleEle_e' : '/SingleElectron/Run2017E-'+DataType17+'/NANOAOD',
'Data_SingleEle_f' : '/SingleElectron/Run2017F-'+DataType17+'/NANOAOD',
}

#--------------------------
# 2018
#--------------------------
MCType18='RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20-v1'
DataType18='Nano1June2019-v1'
MCType18_ext1 = MCType18.replace('-v1','_ext1-v1')
MCType18_v3 = MCType18.replace('-v1','-v3')
sampleList_2018 = {
'TT_tytg_M700':  '/TstarTstarToTgluonTgamma_M-700_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM', 
'TT_tytg_M800':  '/TstarTstarToTgluonTgamma_M-800_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM', 
'TT_tytg_M900':  '/TstarTstarToTgluonTgamma_M-900_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM', 
'TT_tytg_M1000': '/TstarTstarToTgluonTgamma_M-1000_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM', 
#'TT_tytg_M1100': '/TstarTstarToTgluonTgamma_M-1100_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM', 
'TT_tytg_M1200': '/TstarTstarToTgluonTgamma_M-1200_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM', 
'TT_tytg_M1300': '/TstarTstarToTgluonTgamma_M-1300_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM', 
'TT_tytg_M1400': '/TstarTstarToTgluonTgamma_M-1400_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM', 
'TT_tytg_M1500': '/TstarTstarToTgluonTgamma_M-1500_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM', 
'TT_tytg_M1600': '/TstarTstarToTgluonTgamma_M-1600_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM', 

'TTGamma_Dilepton'     : '/TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM',
'TTGamma_Hadronic'   : '/TTGamma_Hadronic_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM',
'TTGamma_SingleLept' : '/TTGamma_SingleLept_TuneCP5_13TeV-madgraph-pythia8/'+MCType18+'/NANOAODSIM',

'TTbarPowheg_Dilepton' : '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/'+MCType18+'/NANOAODSIM',
'TTbarPowheg_Hadronic' : '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/'+MCType18_v3+'/NANOAODSIM',
'TTbarPowheg_Semilept' : '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/'+MCType18+'/NANOAODSIM',
'TGJets' : '/TGJets_TuneCP5_13TeV_amcatnlo_madspin_pythia8/'+MCType18+'/NANOAODSIM',

'ST_s_channel'     : '/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/'+MCType18_ext1+'/NANOAODSIM',
'ST_t_channel'     : '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/'+MCType18+'/NANOAODSIM',
'ST_tbar_channel'  : '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/'+MCType18+'/NANOAODSIM',
'ST_tW_channel'    : '/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/'+MCType18_ext1+'/NANOAODSIM',
'ST_tbarW_channel' : '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/'+MCType18_ext1+'/NANOAODSIM',

'Data_SingleMu_a' : '/SingleMuon/Run2018A-'+DataType18+'/NANOAOD',
'Data_SingleMu_b' : '/SingleMuon/Run2018B-'+DataType18+'/NANOAOD',
'Data_SingleMu_c' : '/SingleMuon/Run2018C-'+DataType18+'/NANOAOD',
'Data_SingleMu_d' : '/SingleMuon/Run2018D-'+DataType18+'/NANOAOD',

'Data_SingleEle_a' : '/EGamma/Run2018A-'+DataType18+'/NANOAOD',
'Data_SingleEle_b' : '/EGamma/Run2018B-'+DataType18+'/NANOAOD',
'Data_SingleEle_c' : '/EGamma/Run2018C-'+DataType18+'/NANOAOD',
'Data_SingleEle_d' : '/EGamma/Run2018D-'+DataType18+'/NANOAOD',
}
