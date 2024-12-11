#!/bin/bash
#To be run on remote machine
#Take input arguments as an array
myArray=( "$@" )
#Array: Size=$#, an element=$1, all element = $@

printf "Start Running Histogramming at"; /bin/date
printf "Worker node hostname "; /bin/hostname

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then 
    echo "Running Interactively" ; 
else
    echo "Running In Batch"
    echo ${_CONDOR_SCRATCH_DIR}
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    #export SCRAM_ARCH=slc7_amd64_gcc700
    scramv1 project CMSSW CMSSW_14_1_0
    cd CMSSW_14_1_0/src
    eval `scramv1 runtime -sh`
	cd ../..
	tar --strip-components=1 -xvf Disc_Ntuple.tar.gz
fi

#Run for Base, Signal region
echo "All arguements: "$@
echo "Number of arguements: "$#
if [ $# -eq 7 ] 
then
    python3 runClass.py -y $1 -d $2 -p $3 -c $4 --method $5 -r $6
    outDir=$7
elif [ $# -eq 9 ] 
then
    python3 runClass.py -y $1 -d $2 -p $3 -c $4 --method $5 -r $6 --syst $7 --level $8 
    outDir=$9

#For over/under flow of arguments
else
    echo "The number of command line areguments should be 7 or 9" 
fi
printf "Done Histogramming at "; /bin/date

#---------------------------------------------
#Copy the ouput root files
#---------------------------------------------
printf "Copying output files ..."
xrdcp -rf discs/Class/Classification root://cmseos.fnal.gov/$outDir
rm -r discs
printf "Done ";/bin/date
