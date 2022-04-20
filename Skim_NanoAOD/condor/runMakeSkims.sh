#!/bin/bash
#To be run on remote machine
#Take input arguments as an array
myArray=( "$@" )
#Array: Size=$#, an element=$1, all element = $@

printf "Start Running Histogramming at ";/bin/date
printf "Worker node hostname ";/bin/hostname

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then 
    echo "Running Interactively" ; 
else
    echo "Running In Batch"
    echo ${_CONDOR_SCRATCH_DIR}
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    scramv1 project CMSSW CMSSW_10_2_13
    cd CMSSW_10_2_13/src
    eval `scramv1 runtime -sh`
    cd ../..
	tar --strip-components=1 -zxvf Skim_NanoAOD.tar.gz
fi

#Run for Base, Signal region
echo "All arguements: "$@
echo "Number of arguements: "$#
outDir=$1
year=$2
sample=$3
job=$4
nJobTotal=$5
varname=${sample}_FileList_${year}
source sample/FilesNano_cff.sh
if [ -z $job ] ; then
    jobNum=""
else
    jobNum=" ${job}of${nJobTotal}"
fi
echo "./makeSkim ${year}${jobNum} ${sample}_Skim.root ${!varname}"
./makeSkim ${year}$jobNum ${sample}_Skim.root ${!varname}

printf "Done Histogramming at ";/bin/date
#---------------------------------------------
#Copy the ouput root files
#---------------------------------------------
if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then
    echo "Running Interactively" ;
else
    xrdcp -f ${sample}_Skim*.root root://cmseos.fnal.gov/${outDir}/${year}
    echo "Cleanup"
    rm -rf CMSSW_10_2_13
    rm *.root
fi
printf "Done ";/bin/date
