## Signal generation and grid-pack prodcution for UL Run2

Clone the genproduction repo (do everyting outside of CMSSW)
* git clone https://github.com/cms-sw/genproductions.git

Copy the UFO, create MG cards, and produce 1 grid-pack 
* source createCards.sh 
* Use MG_aMC_v2.6.5  with CMSSW_10_6_19 with slc7_amd64_gcc700 in gridpack_generation.sh
* Use MG_aMC_v2.7.3  with CMSSW_12_4_8 with slc7_amd64_gcc700 in gridpack_generation.sh
* ./gridpack_generation.sh TpTp_M1000_ttga_channel cards/TpTp_production/TpTp_M1000_ttga_channel


In order to produce all grid-packs, we submit condor jobs
* cd ../../../
* Change the path in makeGridPacks.sh where the output grid-packs will be copied
* source tarCommand.sh
* voms-proxy-init -voms cms
* mkdir log
* condor_submit submitGridPacks.jdl


## Archive 1
* MG cards used for B2G-16-025 for spin32:
* https://github.com/cms-sw/genproductions/blob/33032da0eba3466b92d9f139afd447ce6193b3b6/bin/MadGraph5_aMCatNLO/cards/production/13TeV/Top32
* And the coressponding UFO file:
* https://cms-project-generators.web.cern.ch/cms-project-generators/top32.tgz
* Please note that this UFO file (top32.tgz) is also used for the Run2UL spin 32 signal samples (AN-2021-151)
 

## Archive 2
* MG cards used for 2017-18 Rereco (EOY) samples for spin 32 
* https://github.com/cms-sw/genproductions/blob/master/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/Top32
* And the coressponding UFO file:
* https://cms-project-generators.web.cern.ch/cms-project-generators/Top32_UFO.tar.gz 
