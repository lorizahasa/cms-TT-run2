# Skim Condor production and incremental checks

Initialize the CMS/ROOT environment before checking ROOT files. Commands below
work from `Skim_NanoAOD`; the checker resolves its configuration paths from its
own location, independently of the current working directory.

## Creating a submission

Build `makeSkim` and generate the sample lists before creating a submission
package. `createJdlFiles.py` writes the package and JDLs in `condor/tmpSub`.
It refuses to replace an existing `tmpSub`, preserving previous logs and check
state. Keep the submission directory in place while any retry rounds remain.
For a new production, first preserve the previous submission directory and use
a fresh output location.

The checker never runs `createJdlFiles.py`, submits jobs, removes outputs, or
modifies the existing submission archive, wrapper, original logs, or JDLs.

## First check and later rounds

Inspect the expected production without network access or writes:

```bash
python3 condor/checkJobStatus.py --plan
```

Check the existing submission with eight independent ROOT worker processes:

```bash
python3 condor/checkJobStatus.py --production run2_skims --workers 8
```

Repeat that exact command after resubmitting. It rechecks unresolved jobs,
retains passed results, and writes a new round directory. Unchanged historical
logs are cached too. `--recheck-all` explicitly repeats every ROOT check.
Cached results are also reconsidered if an output disappears, its job is
currently active, or new logs establish that a cached output is partial.

The default initial log directories are `tmpSub/log` and `tmpSub/log_resub`.
Both are scanned recursively, including archived retries in `log_resub/old`.
Later rounds' `logs/` directories are discovered automatically. Extra log
directories can be supplied with repeated `--log-dir` options.

Useful options:

- `--submission-dir PATH`: use another saved submission.
- `--years 2017` and `--samples TTbarPowheg_Hadronic`: restrict a production.
- `--max-jobs 20`: bound the number of unresolved jobs checked in this round.
  Unchecked jobs stay unresolved.
- `--io-timeout 30`: timeout for infrastructure queries and XRootD requests.
- `--output-base PATH`: override the archived output location; local ROOT
  output directories are supported for tests.
- `--proxy PATH`: proxy path written to the prepared JDL; normally discovered
  from the environment or `voms-proxy-info`.
- `--input-event-counts FILE`: add verified per-file DAS counts from JSON
  `{"files": {"/store/...root": 123}}`. They are copied into the production's
  `input_event_counts.json` and reused automatically on later rounds. Existing
  cached counts cannot be silently changed. Jobs whose assigned files are all
  covered must match their summed DAS counts, even if their ROOT file opens
  and its own counters agree.
- `--queue-json FILE`: explicitly use a recorded `condor_q` JSON snapshot,
  primarily for offline tests. Use live queue queries for normal checks.

The saved manifest comes from `tmpSub/Skim_NanoAOD.tar.gz`, including the
submitted input list, exact file splitting, job counts, and cached DAS totals.
It records hashes of the archive and wrapper. Changing the production inputs,
output base, selected years/samples, or package requires a new production name.
The old metadata file-count field is not trusted for splitting; actual input
filenames are used.

## Files and manual resubmission

```text
condor/tmpSub/checks/run2_skims/
  manifest.json
  log_index.json
  check_state.json
  round_001/
    report.json
    failed_jobs.json
    resubmitJobs.jdl
    submit.sh
    logs/
  round_002/
    ...
```

A JDL and `submit.sh` are created only when failed jobs are safe to retry.
Inspect the report and JDL, then submit explicitly:

```bash
condor_submit condor/tmpSub/checks/run2_skims/round_001/resubmitJobs.jdl
```

The generated JDL uses absolute paths to the submission package and this
round's logs. Condor writes the resubmission's stdout, stderr, and event logs
into that round's `logs/` directory. Run the checker again after those jobs
finish; it prepares the next round with only remaining failures.

Idle, running, held, suspended, removing, and transferring jobs remain pending
and are not duplicated in retries. If the queue query fails, retry preparation
is withheld. An EOS listing failure stops the round instead of treating all
outputs as missing. Original submission/resubmission files are never overwritten.

To execute a prepared retry round locally, pass its `failed_jobs.json` to
`bash runJobsLocal.sh --failed-jobs FILE`. Add `--stage-out` to copy successful
outputs to their recorded EOS destinations and remove those local ROOT copies.
Without it, outputs stay local. The launcher uses the frozen submission
executable and input lists; it does not read the obsolete `localResubmitJobs.txt`.
See the parent README for examples, output paths, and concurrency options.

## Checks and counters

Each ROOT output must open without zombie/recovery errors and contain an
`Events` tree, integer Table 9 flags, and valid `hEvents` counters. The tree's
entry count must equal bin 4. MC also requires finite generator counters, with
positive `hGenEventCount`; a split job's signed sum may be zero or negative.
A legitimate zero-selected-event tree is accepted.

Historical input-loading logs are compared with the assigned file list.
Logs showing skipped inputs or a crashed attempt whose partial input count
matches the EOS file are flagged. Transient warning strings alone do not
invalidate an otherwise consistent output.

`hEvents` bin 2 counts input events, not selected events. Sample summaries
compare its aggregate with the DAS total cached in the submitted
`JobsNano_cff.py`; this is not a fresh DAS query. A remaining aggregate
difference is recorded as `needs_review`, rather than blindly retrying every
job or applying an event-count correction.

`check_state.json` retains per-job counts, signed generator sums, latest log
paths, status, and failure reasons. Only the parent writes it, using atomic
replacement and a production lock. Interrupted rounds keep their latest
checkpoint; the next invocation resumes unresolved jobs.

The checker's `normalization_ready` remains preliminary. Use the separate
finalizer below to publish the normalization inputs. Neither script modifies
`Ntuple_Skim`.

## Final normalization export

After all selected jobs pass, choose the eras from `Skim_NanoAOD`:

```bash
python3 condor/finalizeNormalization.py --years 2017 --workers 8
python3 condor/finalizeNormalization.py --years 2016Pre 2016Post --workers 8
python3 condor/finalizeNormalization.py --years all --workers 8
```

These write `normalization/2017_normalization.json`,
`normalization/2016Pre_2016Post_normalization.json`, or
`normalization/Run2_normalization.json`, respectively. One JSON contains the
selected eras, with separate full-sample denominators for each era and sample.
`--years all` means `2016Pre 2016Post 2017 2018`; it does not use the current
year selection in `SkimInputs.py`.

The script discovers saved production records at
`condor/*/checks/*/manifest.json`. It requires matching checker state and
complete coverage of the selected samples in the frozen job catalogs. Missing
eras or samples stop the export. Overlapping production records are rejected;
the script never chooses a production based only on its date or cached status.

Preview the chosen productions and output filename without network access or
new files:

```bash
python3 condor/finalizeNormalization.py --years all --plan
```

Override discovery with explicit production records when necessary. Repeat
`--production-dir` to combine separate productions:

```bash
python3 condor/finalizeNormalization.py --years all \
  --production-dir condor/tmpSub/checks/run2016_20261120 \
  --production-dir condor/tmpSub_2017_2018_20261121/checks/run2017_2018_20261121
```

The original single-production invocation remains supported:

```bash
python3 condor/finalizeNormalization.py \
  --production-dir condor/tmpSub/checks/run2_skims --workers 8
```

For every chosen production, the finalizer verifies the frozen submission package and checker state,
checks that no selected jobs are active, queries live DAS per-file event
counts, and independently rereads every selected EOS output with spawned
ROOT processes. It reads headers and histograms, without event loops. It
requires complete input coverage, matching processed counts, valid generator
totals, and agreement with the latest passed checker records. Discrepancies
produce a diagnostic report, never an automatic normalization correction.

A successful export is written outside the temporary directory. With the
original single-production invocation and no `--years`, the default remains:

```text
Skim_NanoAOD/normalization/run2_skims.json
```

Per-production reports and DAS snapshots are stored in the production's
`finalization/round_NNN/` directory. Year-based exports also retain an aggregate
report and source-export snapshots under `normalization/reports/`. The final
combined JSON is published only after every source passes and a final check
confirms that no relevant job is active and no source checker state changed.
Existing exports are never overwritten; use `--output` to choose a new filename.
Generated normalization files are ignored by Git.

Useful options:

- `--output FILE.json`: choose the persistent export filename.
- `--search-dir DIR`: discover `*/checks/*` production records under another
  submission parent instead of `Skim_NanoAOD/condor`.
- `--years 2017 --samples SignalSpin12_M800`: export only complete selected
  samples. The scope and years are recorded in the JSON; sample-restricted
  default filenames have a suffix to distinguish them from full-era exports.
- `--das-counts FILE.json`: explicitly use a saved per-file DAS snapshot
  instead of a live query. This choice and the snapshot hash are recorded.
- `--queue-json FILE.json`: explicitly use a queue snapshot for offline tests.

Year-based exports retain a `source_productions` list with the hashes,
validation reports, DAS sources, and recorded retry packages or replica
overrides. A separate merge command is not needed.

The exported `samples[year][sample]` records contain input/selected counts,
`genEventCount`, signed `genEventSumw`, and the exact skim file list. Every
split ntuple job must use the same full-sample totals. For MC the normalization
is `cross section * luminosity * Generator_weight / genEventSumw`; cross
sections and luminosities still come from the analysis configuration. The
selected-event count must not be used as the denominator. Data records use
`normalization_method: unit_weight` and null generator counters. A zero full
MC generator sum blocks export; zero/negative split-job sums are allowed.
The ntuple reader still needs its separate compatibility/JSON update.
