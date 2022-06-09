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
    export SCRAM_ARCH=slc7_amd64_gcc700
    scramv1 project CMSSW CMSSW_10_6_10
    cd CMSSW_10_6_10/src
    eval `scramv1 runtime -sh`
	cd ../..
	tar --strip-components=1 -zxvf Disc_Ntuple.tar.gz
fi

#Run for Base, Signal region
echo "All arguements: "$@
echo "Number of arguements: "$#
python runReader.py -y $1 -d $2 -c $3 -s $4 --method $5 -r $6 --syst $7
printf "Done Histogramming at ";/bin/date

#---------------------------------------------
#Copy the ouput root files
#---------------------------------------------
printf "Copying output files ..."
xrdcp -rf discs/Read root://cmseos.fnal.gov/$8
rm -r discs
rm -r CMSSW_10_6_10
printf "Done ";/bin/date
