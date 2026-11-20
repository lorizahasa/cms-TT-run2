# Skim NanoAOD changes

## Clean Skim_NanoAOD production with RDataFrame

Changes relative to `79fb8d0`:

- Replace the manual event loop and reader with one RDataFrame skimmer,
  using four threads by default.
- Keep only the Table 9 muon/electron trigger ORs and their two flags.
  Remove expanded trigger tests, matching branches, and six trigger histograms.
- Use an explicit branch list, retaining the ntuple analysis inputs, PV/pileup
  information, both b-tag scores, and generator/systematic weights.
- Preserve `hEvents` and the pre-selection `hGenEventCount`/`hGenEventSumw`
  bookkeeping. Add input/schema checks, duplicate protection, empty-output
  handling, and safe output/failure handling.
- Update the build and launchers for CMSSW_14_1_0_pre4 and four RDF threads.
  Condor requests four CPUs and 9 GB; packaging includes only production inputs.
  Local bulk launching defaults to one concurrent skim.
- Fix input-file counting so repeated/trailing whitespace is not counted as
  additional files.

Validation: a fresh run on all 13 original files of the 2017 spin-1/2,
800 GeV signal sample processed 200,000 events in 5 min 13 s. All 170,274
Table 9 events, 127 retained branches, and generator counters matched the old
output; the 2,023 events passing only the expanded trigger OR were removed.
All 204,394,113 compared values matched. Test and validation artifacts remain
local and are excluded from this commit.

Compatibility: the current downstream ntuple reader still expects the removed
expanded flags and trigger histograms. It needs a separate compatibility update
before reading the new skims.
