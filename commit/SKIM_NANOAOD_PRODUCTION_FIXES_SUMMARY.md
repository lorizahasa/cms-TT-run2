# Skim NanoAOD production fixes and bookkeeping

Changes relative to `9fdae14`, following the RDataFrame cleanup.

## Production changes

- `Skim_NanoAOD/makeSkim.C`: handle mixed availability of Table 9 HLT
  branches across input files. Missing decisions are false; available decisions
  keep their original values. Group compatible inputs for ROOT 6.30 and merge
  their snapshots, preserving the trigger selections and combined bookkeeping.
  Incompatible selected physics schemas and invalid trigger types still fail.
- `Skim_NanoAOD/condor/createJdlFiles.py`: prevent automatic return of ROOT
  files to the submission directory with `transfer_output_files = ""`, retain
  stdout/stderr and Condor event logs, and refuse to delete an existing
  submission directory. Successful worker outputs are staged to EOS.
- `Skim_NanoAOD/condor/checkJobStatus.py`: replace repeated full scans with
  parallel checks and persistent per-job state. Later rounds reuse passed
  results and check unresolved or changed outputs. Validate ROOT trees,
  bookkeeping and available input-count evidence; prepare retry JDLs without
  submitting automatically. Preserve original submission inputs and logs,
  check the live queue, and withhold retries when queue status is unavailable.
- **New** `Skim_NanoAOD/condor/finalizeNormalization.py`: independently verify
  complete output coverage, live DAS input counts, and generator bookkeeping
  before exporting full-sample normalization JSON. Failed checks produce a
  diagnostic report instead of a usable export. Normalization uses the signed
  full-sample `genEventSumw`, not the number of selected events. Select eras
  with `--years` or use `--years all` for one Run 2 JSON. The script discovers
  production records, rejects overlapping or incomplete coverage, and validates
  every source before publishing the combined export. Keep the original
  single-production interface and record each source's provenance. No separate
  JSON merge script is needed.
- `Skim_NanoAOD/sample/getFiles.py`: obtain valid filenames and their event
  counts from checked DAS JSON queries. Validate and sort inputs, calculate
  job splitting from the actual file list, and preserve existing configuration
  on query or publication failure. Add timeouts, retries, locking, and CLI
  options; remove shell/eval-based query parsing and the NumPy dependency.
- `Skim_NanoAOD/runJobsLocal.sh` and **new** `runJobsLocal.py`: support direct
  sample runs and checker retry lists from any working directory. Add explicit
  concurrency, per-job logs, failure summaries, output protection, and optional
  EOS staging. Retries use the frozen production package and input splitting.
- Update both skim READMEs and `.gitignore` for the new workflow, temporary
  submission directories, normalization exports, and generated lock files.

## Measured optimization results

These measurements cover the RDF/branch cleanup and the production updates.

| Measurement | Before | After | Improvement |
| --- | ---: | ---: | --- |
| RDF runtime: one thread versus four | 20 min 49 s | 6 min 34 s | 3.17x speedup; 68.5% less wall time |
| Saved branches, 2017 signal example | 171 | 127 | 44 fewer branches; 25.7% reduction |

The timing measurements used the same 13 NanoAOD files and 200,000 events for
the 2017 spin-1/2, 800 GeV signal sample. The 3.17x result compares total wall
time with one and four RDF threads. The one- and four-thread runs matched in
retained event identities, trigger flags, generator weights, branch schema,
and bookkeeping. The original pre-RDF manual run took
approximately 19 minutes for its event loop; this is an approximate reference
with a different timing definition.

Full-production storage, comparing the same output filenames with the saved
old EOS inventories (decimal GB):

| Year | Files | Before [GB] | After [GB] | Saved [GB] | Reduction |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2017 | 737 | 649.5 | 348.3 | 301.1 | 46.4% |
| 2018 | 1,050 | 935.2 | 502.4 | 432.8 | 46.3% |
| Combined | 1,787 | 1,584.6 | 850.7 | 734.0 | 46.3% |

The storage reduction reflects the combined branch/trigger cleanup and output
implementation. All required available analysis fields and normalization
bookkeeping are retained.

The first `checkJobStatus.py` pass checked 1,787 jobs in approximately 41 seconds
using eight workers. This measures output/log/bookkeeping checks, not skim
production. Later rounds reuse passed results and check unresolved outputs.

For the initial Condor submissions, median successful-job runtimes were
29.3 minutes (2017) and 31.8 minutes (2018). Submission-to-last-termination
times were 7 h 43 min and 14 h 52 min, respectively, including queue waiting
and excluding the later 2017 retries.

## Production status

- Run 2 production is complete: 920 skim outputs for 2016 pre/post-VFP,
  737 for 2017, and 1,050 for 2018, totaling 2,707 outputs.
- The combined normalization JSON contains 428 sample/era records, keeping
  generator sums separate by sample and era.

The earlier cleanup summary is retained as the record of the RDF conversion:
[RDataFrame cleanup](SKIM_NANOAOD_RDF_CLEANUP_SUMMARY.md).
