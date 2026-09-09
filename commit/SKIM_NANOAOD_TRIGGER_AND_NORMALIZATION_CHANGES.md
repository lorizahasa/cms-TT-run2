# Skim NanoAOD trigger and normalization changes

## Suggested commit title

Propagate Table 9 triggers and generator normalization through skimming

## Summary

This update extends the NanoAOD skim with a second, analysis-specific set of trigger decisions and preserves the generator metadata needed for full-sample MC normalization. `Ntuple_Skim` consumes both additions: its preselection now uses the Table 9 trigger ORs, while its event weights retain the magnitude of the nominal generator weight instead of reducing it to its sign. The changes also improve ROOT file validation/cleanup and correct two Run 2 details (`HLT_OldMu100` and the 2018 HEM weight factor).

## `Skim_NanoAOD` changes

### Preserve pre-skim MC normalization metadata

- Read `genEventCount` and `genEventSumw` from the `Runs` tree of every NanoAOD input assigned to the current skim job.
- Resolve local paths and FNAL XRootD paths consistently when opening the input files for metadata.
- Fail the skim job if an MC input cannot be opened, has no `Runs` tree, lacks either required branch, or contains invalid metadata.
- Store each job's totals in one-bin `TH1D` histograms named `hGenEventCount` and `hGenEventSumw` in the skim output. Because the totals cover the input files before event filtering, downstream jobs can sum them across all skim files to recover the full-sample normalization.

### Add Table 9 trigger decisions

- Keep the existing expanded trigger decisions in `passTrigMu` and `passTrigEle` for validation and backward comparison.
- Enable and bind `HLT_Ele35_WPTight_Gsf` in the 2017 skim reader so it is available to the Table 9 electron OR.
- Add `passTrigMuTable9` and `passTrigEleTable9` branches with the following year-dependent ORs:

| Year | Muon Table 9 OR | Electron Table 9 OR |
| --- | --- | --- |
| 2016 | `HLT_Mu50` or `HLT_TkMu50` | `HLT_Ele27_WPTight_Gsf`, `HLT_Ele115_CaloIdVT_GsfTrkIdT`, or `HLT_Photon175` |
| 2017 | `HLT_Mu50`, `HLT_TkMu100`, or `HLT_OldMu100` | `HLT_Ele35_WPTight_Gsf`, `HLT_Ele115_CaloIdVT_GsfTrkIdT`, or `HLT_Photon200` |
| 2018 | `HLT_Mu50`, `HLT_TkMu100`, or `HLT_OldMu100` | `HLT_Ele32_WPTight_Gsf`, `HLT_Ele115_CaloIdVT_GsfTrkIdT`, or `HLT_Photon200` |

- Retain an event in the skim if it passes the MET filters and either the expanded trigger OR or the Table 9 trigger OR. This ensures that downstream validation can compare both definitions without losing events at skim time.
- Replace the nonexistent/incorrect `HLT_Mu100` name with the NanoAOD path `HLT_OldMu100` for 2017 and 2018, and align trigger-flow bin ordering with the evaluated OR order.

### Improve input and ROOT object handling

- Validate local and remote files when adding them to the `TChain`; report local failures and throw on a validated remote file that still cannot be added.
- Delete temporary input `TFile` objects after inspection so ROOT closes and unregisters them cleanly.
- Explicitly delete the output file and event-tree wrapper after writing the skim.

## Downstream `Ntuple_Skim` changes

### Consume Table 9 trigger branches

- Add readers for `passTrigMuTable9` and `passTrigEleTable9`.
- Add `EventPick::useTable9Triggers` so preselection can switch between the new Table 9 decisions and the original expanded decisions.
- Enable that switch in `makeNtuple`, making the Table 9 ORs the active trigger requirement for the muon and electron ntuple cutflows. The primary-vertex requirement remains part of the same first cutflow stage.
- Update the downstream raw trigger reader to use `HLT_OldMu100` consistently.

### Normalize MC using the full generator-weight sum

- For normal MC samples, read `hGenEventCount` and `hGenEventSumw` from every skim file passed on the command line, including files outside the current split ntuple job. This gives every split job the same full-sample denominator.
- Abort ntuple production cleanly when a skim file is unreadable, either metadata histogram is missing, the generated-event count is non-positive, or the summed generator weight is non-finite/effectively zero.
- Create the output ROOT file and initialize its tree only after normalization metadata passes validation, preventing failed normalization checks from leaving an empty or partial ntuple.
- Compute the luminosity factor as

  ```text
  cross section * integrated luminosity / genEventCount
  ```

  and normalize each event's nominal generator weight by the full-sample average,

  ```text
  normalized genWeight = event genWeight / (genEventSumw / genEventCount)
  ```

  so their product is equivalent to `cross section * luminosity * event genWeight / genEventSumw`.
- This replaces the previous sign-only `genWeight / abs(genWeight)` treatment and therefore preserves variations in the nominal generator-weight magnitude.
- Keep unit normalization for data and the `Test`, `TestAll`, and `TestFull` modes; explicitly initialize the data generator weight to one.
- Rename the event-weight helper argument and diagnostics from the ambiguous `nEvents_MC` to `genEventCount`.

### Correct 2018 HEM weighting

- Change the MC HEM-region factor from `1 - 0.3518` to `0.3518`, matching the intended affected-luminosity fraction. The data HEM veto logic is unchanged.

## Other repository changes

- Ignore generated validation outputs, skim CSV files, and old/validation scratch paths in `.gitignore`.

## Review notes before committing

- **Input-format compatibility:** `Ntuple_Skim` now requires the two Table 9 branches in the skim tree and, for non-test MC, both generator-metadata histograms. Older skim files do not contain these objects and must be regenerated or handled with an explicit compatibility fallback.

## Suggested validation

- Run one MC skim job per year and confirm that `hGenEventCount` and `hGenEventSumw` match direct sums from the input NanoAOD `Runs` trees.
- Verify the four trigger-decision branches event by event, especially `HLT_Ele35_WPTight_Gsf` in 2017 and `HLT_OldMu100` in 2017/2018.
- Run split and unsplit ntuple production over the same MC sample and confirm identical normalization and summed event yield.
- Run representative data and test-mode samples to confirm unit event weights and expected behavior when generator metadata is not required.
