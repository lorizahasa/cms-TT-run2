## Signal generation and grid-pack prodcution for UL Run2

Clone the genproduction repo (do everyting outside of CMSSW)
* git clone https://github.com/cms-sw/genproductions.git

Copy the UFO and python script which will create MG cards
* cp top3decays_ufo.tgz genproductions/bin/MadGraph5_aMCatNLO/
* mkdir -p genproductions/bin/MadGraph5_aMCatNLO/cards/TpTp_production
* cp pairProduction_ttgaChannel.py genproductions/bin/MadGraph5_aMCatNLO/cards/TpTp_production
* cd genproductions/bin/MadGraph5_aMCatNLO/cards/TpTp_production
* python pairProduction_ttgaChannel.py
* ls

Now we can produce one grid-pack for one signal mass point
* cd ../../
* ./gridpack_generation.sh TpTp_M1000_ttga_channel cards/TpTp_production/TpTp_M1000_ttga_channel


In order to produce all grid-packs, we submit condor jobs
* cd ../../../
* cp gridpack_generation_LOCAL_CONDOR.sh genproductions/bin/MadGraph5_aMCatNLO/
Change the path in makeGridPacks.sh where the output grid-packs will be copied

* source tarCommand.sh
* condor_submit submitGridPacks.jdl

