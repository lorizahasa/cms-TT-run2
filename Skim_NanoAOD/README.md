# NanoAOD skim production

`makeSkim.C` is the production RDataFrame implementation. It reads NanoAOD,
applies the existing multiplicity protection and event filters, and saves events
passing the muon OR **or** electron OR from Table 9 of the analysis note.
The default is four threads; use `--threads 1` for serial execution.

## Build and run

From the CMSSW `src` directory:

```bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval "$(scram runtime -sh)"
cd cms-TT-run2/Skim_NanoAOD
make
./makeSkim --threads 4 --mc 2017 1of1 Signal_Skim.root local /path/to/NanoAOD.root
```

This writes `Signal_Skim_1of1.root` in the current directory. Supply `--data`
for data. The supported eras are `2016Pre`, `2016Post`, `2017`, and `2018`.
For remote input, replace `local` with `xrootd` and supply LFNs or complete
`root://` URLs. A valid proxy is needed for remote reads.

The positional arguments remain `YEAR JOBofTOTAL OUTPUT.root local|xrootd
INPUT.root [...]`. Splitting is by contiguous groups of input files, including
remainders. Existing output files are never overwritten. Missing Table 9 HLT
branches are reported and treated as false; missing required event controls or
generator metadata cause a nonzero exit.

## Trigger selections

| Era | Muon OR | Electron OR |
| --- | --- | --- |
| 2016Pre, 2016Post | `HLT_Mu50`, `HLT_TkMu50` | `HLT_Ele27_WPTight_Gsf`, `HLT_Ele115_CaloIdVT_GsfTrkIdT`, `HLT_Photon175` |
| 2017 | `HLT_Mu50`, `HLT_TkMu100`, `HLT_OldMu100` | `HLT_Ele35_WPTight_Gsf`, `HLT_Ele115_CaloIdVT_GsfTrkIdT`, `HLT_Photon200` |
| 2018 | `HLT_Mu50`, `HLT_TkMu100`, `HLT_OldMu100` | `HLT_Ele32_WPTight_Gsf`, `HLT_Ele115_CaloIdVT_GsfTrkIdT`, `HLT_Photon200` |

The saved integer flags are `passTrigMuTable9` and `passTrigEleTable9`. Only
Table 9 raw HLT decisions present in the input are saved. Expanded trigger ORs,
2017 trigger-object matching tests, and their extra branches are removed.
The explicit retained branch list is in `interface/SkimBranchConfig.h`.
It preserves the PV/pileup inputs, generator weights, systematic inputs, and
both `Jet_btagDeepB` and `Jet_btagDeepFlavB`.

## Output bookkeeping

The output has four objects:

- `Events`: selected events and the two Table 9 flags.
- `hEvents`: unweighted input, post-filter, and post-trigger counts. The latter
  two counts include the existing multiplicity protection.
- `hGenEventCount`: sum of the input `Runs/genEventCount`, before selections.
- `hGenEventSumw`: signed sum of the input `Runs/genEventSumw`, before selections.

The generator histograms are double precision and contain totals for the input
files assigned to this job. Data files have zero generator counters. The six
old `hAll_*` / `hPass_*` trigger-test histograms are no longer produced.
No event weights are applied during skimming.

## Batch and local launchers

`condor/runMakeSkims.sh` keeps its five arguments: `YEAR SAMPLE JOB TOTAL OUTDIR`.
It uses four RDF threads, propagates processing failures, and stages out only
a successful output. `SKIM_THREADS` overrides the thread count. New Condor
descriptions request four CPUs. If overriding the thread count in batch, match
the requested CPUs to that value.

The submission generator packages only production code, the executable, and
sample configuration. It excludes local ROOT files, studies, and archives.
Existing `condor/tmpSub` archives and submitted jobs are unchanged. Generate a
fresh submission package when ready to deploy this version; the generator also
replaces `tmpSub`, so preserve any historical submission logs first.

`runJobsLocal.sh` defaults to one concurrent skim (four threads).
`SKIM_MAX_PARALLEL` can increase concurrency on a sufficiently large machine.

## Compatibility

The current `Ntuple_Skim` reader still expects the removed expanded trigger
flags and six trigger histograms. It must be adapted before using these new
skim files for ntuple production. Existing skim ROOT files are unchanged.

This directory tracks production code and documentation. Tests, studies,
archives, and generated local outputs are kept locally and excluded from Git.
See [CHANGELOG.md](CHANGELOG.md) for the summary and validation result.
