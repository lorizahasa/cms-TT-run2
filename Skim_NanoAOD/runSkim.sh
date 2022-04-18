#!/bin/bash
#./runSkim.sh -y 2017 -f 1of10 -o "outTest.root" -i "$Signal_M800_FileList_2017"
source sample/FilesNano_cff.sh
while getopts y:f:o:i: options;do
    case $options in
        y) year=$OPTARG;;
        f) fraction=$OPTARG;; 
        o) outFile=$OPTARG;; 
        i) inFiles=$OPTARG;; 
    esac
done
#echo Running for: $year, $fraction, $outFile, $inFiles
./makeSkim $year $fraction $outFile $inFiles 
