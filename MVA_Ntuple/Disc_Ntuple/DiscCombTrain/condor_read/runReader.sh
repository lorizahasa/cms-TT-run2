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
    scramv1 project CMSSW CMSSW_10_2_14
    cd CMSSW_10_2_14/src
    eval `scramv1 runtime -sh`
	cd ../..
	tar --strip-components=1 -zxvf DiscCombTrain.tar.gz
fi

#Run for Base, Signal region
echo "All arguements: "$@
echo "Number of arguements: "$#
if [ $# -eq 6 ] 
then
    python runReader.py -y $1 -d $2 -c $3 -s $4 --method $5
    outDir=$6
elif [ $# -eq 8 ] 
then
    python runReader.py -y $1 -d $2 -c $3 -s $4 --method $5  --syst $6 --level $7 
    outDir=$8

#For over/under flow of arguments
else
    echo "The number of command line areguments should be 6 or 8" 
fi
printf "Done Histogramming at ";/bin/date

#---------------------------------------------
#Copy the ouput root files
#---------------------------------------------
printf "Copying output files ..."
xrdcp -rf discs/Read root://cmseos.fnal.gov/$outDir
rm -r discs
printf "Done ";/bin/date
