## Basic setups 
* cmsrel CMSSW_12_6_0
* cd CMSSW_12_6_0/src
* cmsenv
* git clone git@github.com:ravindkv/cms-TT-run2.git


## To produce one skim file from NanoAOD
* cd Skim_NanoAOD
* make clean
* make
* voms-proxy-init -voms cms
* cd sample
* python getFiles.py
* cd ..
* source sample/FilesNano_cff.sh
* ./makeNtuple Semilep 2017 SignalSpin12_M800__JEC_SubTotalRelative_up 1of1 . $SignalSpin12_M800_FileList_2017

### to produce many skim files using the condor setup
* cd condor
* python createJdlFiles.py
* cd tmpSub
* source condorSubmit.sh

Monitor the conodr jobs on linux terminal
* condor_q 
* condor_q -better-analyze 75671743.5
* condor_release rverma -name lpcschedd3.fnal.gov
* condor_qedit rverma RequestMemory 3072 -name lpcschedd3.fnal.gov

Once all condor jobs are finished, check the output Skim directories to collect
failed or corrupted jobs
* python checkJobStatus.py

Resubmit the failed jobs again using
* condor_submit resubmitJobs.jdl

If the jobs are failing multiple times, run them locally
* source condor/tmpSub/localResubmitJobs.sh


## To produce Ntuple from Skim files 
* cd Ntuple_Skim 
* make clean
* make
* cd sample
* python getFiles.py
* cd ..
* source sample/FilesSkim_cff.sh
* ./makeNtuple Semilep 2017 DYjetsM50__JetBase 1of10 . $DYjetsM50_FileList_2017

POG json: /cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG
* correction summary weight/JME/2018_UL/jmar.json

### To produce multiple Ntuple from Skim files
* cd condor 
* voms-proxy-init -voms cms
Follow the same instruction as we have for producing multiple skim files


## Cutbased analysis on the Ntuple
* cd CBA_Ntuple/Hist_Ntuple/
* cd HistMain
* cd sample
* python getFiles.py
* cd ..
* makeHists.py -s TTbar -y 2017 -r ttyg_Enriched_CR_Resolved --hist Reco_mass_T

### To produce multiple hists from Ntuple
Submit the condor jobs as before




## Gitlab link for the AN
https://gitlab.cern.ch/tdr/notes/AN-21-151
## Gitlab link for the PAS, Paper, Thesis, etc
