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
branches are reported and treated as false in each input file where they are
absent. Missing required event controls or generator metadata, or incompatible
physics branch schemas, cause a nonzero exit.

## Generating input lists

```bash
python3 sample/getFiles.py
```

This uses `Years` from `SkimInputs.py`. `--years 2017 2018` can override the
selection without editing that file. It works from any directory and writes
`sample/FilesNano_cff.sh` and `sample/JobsNano_cff.py` by default.

One DAS JSON query per distinct dataset provides the valid ROOT filenames and
their individual event counts. The stored event total is their sum, so it
corresponds to the exact inputs rather than a separate dataset-summary query.
The default job target remains five million events, capped by the number of
input files. Filenames are sorted for reproducible splitting.

Queries have a 120-second timeout and one retry by default; use `--timeout`
and `--retries` to adjust them. Failed, empty, duplicate, or malformed results
stop generation. Both files are staged only after every selected sample
passes; replacement errors trigger rollback. Unselected eras have empty job
dictionaries, preserving existing Condor imports without adding jobs.

`--dry-run` performs the metadata queries and validation without changing the
configuration. `--output-dir` selects another destination. Catalog entries must
be DAS NanoAOD dataset names; bare private EOS paths are rejected because
their independent event-count metadata is unavailable through this query.

## Trigger selections

| Era | Muon OR | Electron OR |
| --- | --- | --- |
| 2016Pre, 2016Post | `HLT_Mu50`, `HLT_TkMu50` | `HLT_Ele27_WPTight_Gsf`, `HLT_Ele115_CaloIdVT_GsfTrkIdT`, `HLT_Photon175` |
| 2017 | `HLT_Mu50`, `HLT_TkMu100`, `HLT_OldMu100` | `HLT_Ele35_WPTight_Gsf`, `HLT_Ele115_CaloIdVT_GsfTrkIdT`, `HLT_Photon200` |
| 2018 | `HLT_Mu50`, `HLT_TkMu100`, `HLT_OldMu100` | `HLT_Ele32_WPTight_Gsf`, `HLT_Ele115_CaloIdVT_GsfTrkIdT`, `HLT_Photon200` |

The saved integer flags are `passTrigMuTable9` and `passTrigEleTable9`. Only
Table 9 raw HLT decisions present in any assigned input are saved, with false
values for files lacking that path. A path absent from every assigned input
contributes false to the OR without adding a raw output branch. Expanded trigger ORs,
2017 trigger-object matching tests, and their extra branches are removed.
The explicit retained branch list is in `interface/SkimBranchConfig.h`.
It preserves the PV/pileup inputs, generator weights, systematic inputs, and
both `Jet_btagDeepB` and `Jet_btagDeepFlavB`.

For ROOT 6.30, mixed HLT availability is handled by processing groups of files
with the same available paths and merging their snapshots into one job output.
Each input event is processed once, and bookkeeping sums over every group.
Uniform inputs keep the original single-group execution. Physics branch types
and availability must still agree across the assigned files.

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
refuses to replace an existing `tmpSub`, preserving its submission and checking
history. Use a fresh directory for a new production.

`runJobsLocal.sh` uses `runJobsLocal.py` to run an explicitly selected sample
or a retry list from the checker. It works from any directory. Initialize the
CMS/ROOT environment and build `makeSkim` first. Preview a local run with:

```bash
bash runJobsLocal.sh 2017 SignalSpin12_M800 --dry-run
```

Run that sample, or just one file split, with:

```bash
bash runJobsLocal.sh 2017 SignalSpin12_M800 --output-dir local_runs/signal_2017
bash runJobsLocal.sh 2017 SignalSpin12_M800 1 3 --output-dir local_runs/signal_split
```

The optional `JOB TOTAL` arguments use the same contiguous input-file splitting
as Condor. Without them, the selected sample's full input list is processed.
Outputs go to `OUTPUT_DIR/YEAR/`, keeping eras separate. Each job has stdout
and stderr files in `OUTPUT_DIR/YEAR/logs/`; `run_summary.json` records results.
Without `--output-dir`, a new directory is created under `local_runs/`.
Existing ROOT outputs are never overwritten. Missing configuration and failed
skims return a nonzero exit status.

The defaults are one concurrent skim and four threads per skim. Use `--parallel`
and `--threads`, or the environment variables `SKIM_MAX_PARALLEL` and
`SKIM_THREADS`, to change these. Total requested concurrency is their product.
`--dry-run` validates and prints the plan without processing or creating files.

When a checker round produces `failed_jobs.json`, retry it locally with:

```bash
bash runJobsLocal.sh --failed-jobs condor/tmpSub/checks/run2_skims/round_001/failed_jobs.json --dry-run
bash runJobsLocal.sh --failed-jobs condor/tmpSub/checks/run2_skims/round_001/failed_jobs.json --stage-out
```

Retries use the frozen executable and file lists from the original submission
archive, checked against the production manifest. Keep that archive until the
retries finish. Use `--years` and `--samples` to restrict the retry list.
Without `--stage-out`, outputs stay local. With it, the launcher checks that
the selected jobs are absent from the active Condor queue, copies successful
outputs to their recorded EOS destinations, and removes each local ROOT copy
only after its copy succeeds. A failed copy leaves its ROOT file and logs
locally. Remaining failures are written to a new `failed_jobs.json` alongside
the copied manifest, so that list can be used for another local retry.
The old `localResubmitJobs.txt` shell-command format is no longer used.

The [incremental job checker](condor/README.md) stores per-job status and
prepares separate retry rounds, checking only unresolved outputs on later
runs. It uses multiprocessing and never submits jobs automatically.

## Compatibility

The current `Ntuple_Skim` reader still expects the removed expanded trigger
flags and six trigger histograms. It must be adapted before using these new
skim files for ntuple production. Existing skim ROOT files are unchanged.

This directory tracks production code and documentation. Tests, studies,
archives, and generated local outputs are kept locally and excluded from Git.
The separate `condor/finalizeNormalization.py` exports verified normalization
metadata into `normalization/` after checks pass; see the Condor README for
usage. Use `--years 2017`, `--years 2016Pre 2016Post`, or `--years all` to
discover matching production records and generate one JSON for those eras.
`--plan` previews the selection; explicit `--production-dir` overrides remain
available. Exports are kept outside `tmpSub` and excluded from Git.
See the [production-fix summary](../commit/SKIM_NANOAOD_PRODUCTION_FIXES_SUMMARY.md)
for the latest changes and validation, and the
[RDataFrame cleanup summary](../commit/SKIM_NANOAOD_RDF_CLEANUP_SUMMARY.md)
for the earlier conversion.
