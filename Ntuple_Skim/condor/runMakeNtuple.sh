#!/bin/bash
#To be run on remote machine
#Take input arguments as an array
myArray=( "$@" )
#Array: Size=$#, an element=$1, all element = $@
year=$1
decay=$2
syst=$3
sample=$4
job=$5
nJobTotal=$6
outDir=$7

printf "Start Running Histogramming at ";/bin/date
printf "Worker node hostname ";/bin/hostname

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then 
    echo "Running Interactively" ; 
else
    echo "Running In Batch"
    echo ${_CONDOR_SCRATCH_DIR}
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    scramv1 project CMSSW CMSSW_10_2_14
    cd CMSSW_10_2_14/src
    eval `scramv1 runtime -sh`
    cd ../..
	tar --strip-components=1 -zxf Ntuple_Skim.tar.gz
fi

#Run for Base, Signal region
echo "All arguements: "$@
echo "Number of arguements: "$#
varname=${sample}_FileList_${year}
cd sample
source FilesSkim_cff.sh 
cd -
jobNum=" ${job}of${nJobTotal}"
echo "./makeNtuple ${decay} ${year} ${sample}__${syst} ${jobNum} . ${!varname}"
./makeNtuple ${decay} ${year} ${sample}__${syst} ${jobNum} . ${!varname}

printf "Done Histogramming at ";/bin/date
#---------------------------------------------
#Copy the ouput root files
#---------------------------------------------
if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then
    echo "Running Interactively" ;
else
    xrdcp -f ${sample}*.root root://cmseos.fnal.gov/${outDir}
    echo "Cleanup"
    rm -rf CMSSW_10_2_14
    rm *.root
fi
printf "Done ";/bin/date
