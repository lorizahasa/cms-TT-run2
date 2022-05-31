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
	tar -zxf CMSSW_10_2_13.tar.gz 
    #scramv1 project CMSSW CMSSW_10_2_14
    cd CMSSW_10_2_13/src
    scram b -r ProjectRename
    eval `scramv1 runtime -sh`
    mv ../../FitDYSF.tar.gz .
	tar --strip-components=1 -zxf FitDYSF.tar.gz
fi

#Run for Base, Signal region
echo "All arguements: "$@
echo "Number of arguements: "$#

python performFit.py -y $1 -d $2 -c $3 -r $4 --isT2W --isImpact
printf "Done fitting at ";/bin/date
xrdcp -rf ./output/ root://cmseos.fnal.gov/$5
rm -r ./output
printf "Done ";/bin/date
