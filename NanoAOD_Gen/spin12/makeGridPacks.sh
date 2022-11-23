#!/bin/bash

sample=$1
mass=$2

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then 
    echo "Running Interactively" ; 
else
    echo "Running In Batch"
    cd ${_CONDOR_SCRATCH_DIR}
    echo ${_CONDOR_SCRATCH_DIR}
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    ls
#    xrdcp root://cmseos.fnal.gov//store/user/dnoonan/productionFiles.tgz .
    tar -zxf productionFiles.tgz
    ls
fi

cd genproductions/bin/MadGraph5_aMCatNLO

case $sample in 
    0)
        ./gridpack_generation_LOCAL_CONDOR.sh TpTp_M${mass}_ttga_channel cards/TpTp_production/TpTp_M${mass}_ttga_channel
        xrdcp -f TpTp_M${mass}_ttga_channel_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz root://cmseos.fnal.gov//store/user/lpctop/TPrimeMC/GridPacksNew
        ;;
    1) 
        ./gridpack_generation_LOCAL_CONDOR.sh TpTp_M${mass}_ttgg_channel cards/TpTp_production/TpTp_M${mass}_ttgg_channel
        xrdcp -f TpTp_M${mass}_ttgg_channel_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz root://cmseos.fnal.gov//store/user/lpctop/TPrimeMC/GridPacksNew
        ;;
    2)
        ./gridpack_generation_LOCAL_CONDOR.sh TpTp_M${mass}_ttaa_channel cards/TpTp_production/TpTp_M${mass}_ttaa_channel
        xrdcp -f TpTp_M${mass}_ttaa_channel_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz root://cmseos.fnal.gov//store/user/lpctop/TPrimeMC/GridPacksNew
        ;;
esac

cd -

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then
    echo "Running Interactively" ;
else
    echo "Running In Batch"
    rm TpTp*
fi
