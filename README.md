## Basic setups 
* cmsrel CMSSW_10_2_13
* cd CMSSW_10_2_13/src
* cmsenv
* git clone git@github.com:ravindkv/cms-TT-run2.git

## To produce skim files from NanoAOD
* cd Skim_NanoAOD
* make clean
* make
* voms-proxy-init -voms cms
* source sample/FilesNano_cff.sh
* ./runSkim.sh -y 2017 -f 1of22 -o "out.root" -i "$Signal_M800_FileList_2017" 

## Gitlab link for the AN
https://gitlab.cern.ch/tdr/notes/AN-21-151
## Gitlab link for the PAS, Paper, Thesis, etc
