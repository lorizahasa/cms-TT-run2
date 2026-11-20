#!/bin/bash
# Same five arguments for local and Condor execution.
set -eo pipefail
if [[ $# -ne 5 ]]; then
    echo "Usage: $0 YEAR SAMPLE JOB TOTAL OUTDIR" >&2
    exit 2
fi
year=$1
sample=$2
job=$3
nJobTotal=$4
outDir=$5
skim_threads=${SKIM_THREADS:-4}
if [[ ! $skim_threads =~ ^[1-9][0-9]*$ ]]; then
    echo "SKIM_THREADS must be a positive integer" >&2
    exit 2
fi
printf 'Start skimming at '
/bin/date
printf 'Worker node hostname '
/bin/hostname
# Retain this log marker for the existing job-status parser.
echo "All arguements: $*"
if [[ -n ${_CONDOR_SCRATCH_DIR:-} ]]; then
    cd "$_CONDOR_SCRATCH_DIR"
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    scramv1 project CMSSW CMSSW_14_1_0_pre4
    cd CMSSW_14_1_0_pre4/src
    eval "$(scramv1 runtime -sh)"
    cd "$_CONDOR_SCRATCH_DIR"
    tar --strip-components=1 -zxf Skim_NanoAOD.tar.gz
else
    cd "$(dirname "$(readlink -f "$0")")/.."
    if ! command -v root-config >/dev/null 2>&1; then
        echo "Initialize the CMS/ROOT environment before running locally." >&2
        exit 2
    fi
fi
source sample/FilesNano_cff.sh
varname=${sample}_FileList_${year}
if [[ ! $varname =~ ^[A-Za-z_][A-Za-z0-9_]*$ || -z ${!varname} ]]; then
    echo "No input list for $sample in $year" >&2
    exit 2
fi
read -r -a skim_inputs <<< "${!varname}"
sample_mode=--mc
[[ $sample != *Data* ]] || sample_mode=--data
jobNum="${job}of${nJobTotal}"
./makeSkim --threads "$skim_threads" "$sample_mode" "$year" "$jobNum" "${sample}_Skim.root" "${skim_inputs[@]}"
skim_output="${sample}_Skim_${jobNum}.root"
test -s "$skim_output"
if [[ -n ${_CONDOR_SCRATCH_DIR:-} ]]; then
    xrdcp -f "$skim_output" "root://cmseos.fnal.gov/${outDir%/}/$skim_output"
fi
printf 'Done skimming at '
/bin/date
