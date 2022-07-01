#!/bin/bash
#To be run on remote machine
#Take input arguments as an array
myArray=( "$@" )
#Array: Size=$#, an element=$1, all element = $@

printf "Start skimming at ";/bin/date
printf "Worker node hostname ";/bin/hostname

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then 
    echo "Running Interactively" ; 
else
    echo "Running In Batch"
    echo ${_CONDOR_SCRATCH_DIR}
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    export SCRAM_ARCH=slc7_amd64_gcc700
    scramv1 project CMSSW CMSSW_10_6_10
    cd CMSSW_10_6_10/src
    eval `scramv1 runtime -sh`
    cd ../..
	tar --strip-components=1 -zxf Skim_NanoAOD.tar.gz
fi

#Run for Base, Signal region
echo "All arguements: "$@
echo "Number of arguements: "$#
year=$1
sample=$2
job=$3
nJobTotal=$4
outDir=$5
varname=${sample}_FileList_${year}
source sample/FilesNano_cff.sh
jobNum="${job}of${nJobTotal}"
echo "./makeSkim ${year} ${jobNum} ${sample}_Skim.root ${!varname}"
./makeSkim ${year} $jobNum ${sample}_Skim.root ${!varname}

printf "Done skimming at ";/bin/date
#---------------------------------------------
#Copy the ouput root files
#---------------------------------------------
if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then
    echo "Running Interactively" ;
else
    xrdcp -f ${sample}_Skim_${jobNum}.root root://cmseos.fnal.gov/${outDir}
    echo "Cleanup"
    rm -rf CMSSW*
    rm *.root 
fi
printf "Done ";/bin/date
