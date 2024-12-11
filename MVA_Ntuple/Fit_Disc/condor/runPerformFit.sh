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
	tar -xf CMSSW_14_1_0_pre4.tar.gz 
    #scramv1 project CMSSW CMSSW_14_1_0_pre4
    cd CMSSW_14_1_0_pre4/src
    scram b -r ProjectRename
    eval `scramv1 runtime -sh`
    mv ../../Fit_Disc.tar.gz .
	tar --strip-components=1 -xf Fit_Disc.tar.gz
    
fi

#Run for Base, Signal region
echo "All arguements: "$@
echo "Number of arguements: "$#
#python3 performFit.py -y $1 -d $2 -c $3 --mass $4 --method $5 -r $6 --hist $7 --isT2W --isImpact --isFD --isGOF
python3 performFit.py -y $1 -d $2 -p $3 -c $4 --mass $5 --method $6 -r $7 --hist $8 --isT2W --isImpact --isLimit
printf "Done fitting at ";/bin/date
xrdcp -rf ./output/Fit_Disc/ root://cmseos.fnal.gov/$9
rm -r ./output
cd ..
rm -rf CMSSW*
printf "Done ";/bin/date
