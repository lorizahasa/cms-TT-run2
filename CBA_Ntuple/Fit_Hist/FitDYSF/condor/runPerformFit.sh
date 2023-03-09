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
	tar -xf CMSSW_12_6_0.tar.gz 
    cd CMSSW_12_6_0/src
    scram b -r ProjectRename
    eval `scramv1 runtime -sh`
    mv ../../FitDYSF.tar.gz .
	tar --strip-components=1 -xf FitDYSF.tar.gz
fi

#Run for Base, Signal region
echo "All arguements: "$@
echo "Number of arguements: "$#

python3 performFit.py -y $1 -d $2 -c $3 -r $4 --isT2W --isImpact
printf "Done fitting at ";/bin/date
xrdcp -rf ./output/Fit_Hist root://cmseos.fnal.gov/$5
cd ../../
rm -rf CMSSW*
printf "Done ";/bin/date
