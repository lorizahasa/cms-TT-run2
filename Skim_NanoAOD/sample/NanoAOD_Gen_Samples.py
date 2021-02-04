
#--------------------------
# 2016
#--------------------------
#MCType16='RunIISummer16NanoAODv5-PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1'
MCType16='RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1'
MCType16_ext1=MCType16.replace('-v1','_ext1-v1')
MCType16_ext2=MCType16.replace('-v1','_ext2-v1')
MCType16_ext3=MCType16.replace('-v1','_ext3-v1')
MCType16_noPULabel = MCType16.replace('PUMoriond17_','')

MCType16_v2 = MCType16.replace('-v1','-v2')

DataType16='Nano1June2019-v1'
DataType16_ver2='_ver2-Nano1June2019_ver2-v1'
sampleList_2016 = {
'TT_tyty_M800': '/TstarTstarToTgammaTgamma_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM',
'TT_tytg_M800': '/TstarTstarToTgammaTgluon_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM',
'TT_tgtg_M800': '/TstarTstarToTgluonTgluon_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', 
'TT_tyty_M1200': '/TstarTstarToTgammaTgamma_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM',
'TT_tytg_M1200': '/TstarTstarToTgammaTgluon_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM',
'TT_tgtg_M1200': '/TstarTstarToTgluonTgluon_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16NanoAODv6-PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/NANOAODSIM', 
'TTGamma_Dilepton'     : '/TTGamma_Dilept_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM',
'TTGamma_Hadronic'   : '/TTGamma_Hadronic_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM',
'TTGamma_SingleLept' : '/TTGamma_SingleLept_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM',

'TTGamma_Dilepton_Pt100'  : '/TTGamma_Dilept_ptGamma100-200_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM',
'TTGamma_Dilepton_Pt200' : '/TTGamma_Dilept_ptGamma200inf_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM',

'TTGamma_SingleLept_Pt100' : '/TTGamma_SingleLept_ptGamma100-200_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM',
'TTGamma_SingleLept_Pt200' : '/TTGamma_SingleLept_ptGamma200inf_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM',

'TTGamma_Hadronic_Pt100' : '/TTGamma_Hadronic_ptGamma100-200_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM',
'TTGamma_Hadronic_Pt200' : '/TTGamma_Hadronic_ptGamma200inf_TuneCP5_PSweights_13TeV-madgraph-pythia8/'+MCType16+'/NANOAODSIM',

'TTbarPowheg_Dilepton' : '/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType16+'/NANOAODSIM',
'TTbarPowheg_Hadronic' : '/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType16+'/NANOAODSIM',
'TTbarPowheg_Semilept' : '/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/'+MCType16+'/NANOAODSIM',
}
sampleList_2017 = sampleList_2016
sampleList_2018 = sampleList_2016
