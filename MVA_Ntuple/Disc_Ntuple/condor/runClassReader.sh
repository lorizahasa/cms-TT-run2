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
	tar --strip-components=1 -zxvf Disc_Ntuple.tar.gz
fi

#Run for Base, Signal region
echo "All arguements: "$@
echo "Number of arguements: "$#
if [ $# -eq 5 ] 
then
    python Classification.py -y $1 -d $2 -c $3 --mass $4 --method $5
    python Reader.py -y $1 -d $2 -c $3 --mass $4 --method $5
elif [ $# -eq 7 ] 
then
    python Classification.py -y $1 -d $2 -c $3 --mass $4 --method $5  --syst $5 --level $6 
    python Reader.py -y $1 -d $2 -c $3 --mass $4 --method $5 --syst $5 --level $6 

#For over/under flow of arguments
else
    echo "The number of command line areguments should be 5 or 7" 
fi
printf "Done Histogramming at ";/bin/date

#---------------------------------------------
#Copy the ouput root files
#---------------------------------------------
printf "Copying output files ..."
condorOutDir=/store/user/rverma/Output/cms-TT-run2/MVA_Ntuple/Disc_Ntuple
eos root://cmseos.fnal.gov mkdir -p $condorOutDir/$1/$2/$3/$4/$5
xrdcp -rf *.root root://cmseos.fnal.gov/$condorOutDir/$1/$2/$3/$4/$5
rm *.root
printf "Done ";/bin/date
