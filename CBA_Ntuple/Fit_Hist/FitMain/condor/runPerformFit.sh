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
	tar -zxvf CMSSW_10_2_13.tar.gz 
    #scramv1 project CMSSW CMSSW_10_2_14
    cd CMSSW_10_2_13/src
    scram b ProjectRename
    eval `scramv1 runtime -sh`
    mv ../../FitMain.tar.gz .
	tar --strip-components=1 -zxvf FitMain.tar.gz
fi

#Run for Base, Signal region
echo "All arguements: "$@
echo "Number of arguements: "$#

python performFit.py -y $1 -d $2 -c $3 --mass $4 --hist $5 -r $6 $7 --isT2W --isLimit --isImpact
printf "Done Histogramming at ";/bin/date

#---------------------------------------------
#Copy the ouput root files
#---------------------------------------------
printf "Copying output files ..."
condorOutDir=/store/user/rverma/Output/cms-TT-run2/Fit_Hist/FitMain/forMain
eos root://cmseos.fnal.gov mkdir -p $condorOutDir/$1/$2/$3/$4/$5/$6
xrdcp -rf output/* root://cmseos.fnal.gov/$condorOutDir/$1/$2/$3/$4/$5/$6 
printf "Done ";/bin/date
