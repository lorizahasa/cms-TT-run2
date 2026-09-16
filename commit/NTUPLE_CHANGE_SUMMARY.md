# Ntuple update summary

This document summarizes the changes in `Ntuple_Skim` relative to commit
`fd52208` (`Skim NanoAOD trigger and normalization changes`).

## Suggested commit title

```text
Update Ntuple certification, cutflows, overlap removal, and PU inputs
```

## Implemented changes

### Run-2 data certification

- Added the recommended Run-2 certification JSON files:
  - `Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt`
  - `Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt`
  - `Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt`
- Updated the luminosity-mask mapping in `makeNtuple.C`:
  - 2016Pre and 2016Post use the Legacy 2016 certification.
  - 2017 uses the UL2017 Golden JSON.
  - 2018 uses the Legacy 2018 certification.
- Retained the older JSON files for reference.

### TTGamma overlap removal

- Corrected the overlap removal between inclusive and photon-`pT`-binned
  TTGamma samples.
- Inclusive TTGamma events are rejected when an LHE photon has
  `pT >= 100 GeV`.
- The LHE-particle loop now sets an event-level flag; the subsequent
  `continue` correctly skips the event loop instead of only advancing the
  LHE-particle loop.
- The overlap-rejection counter is filled once per rejected event.

### Signal cutflow information

- Kept the existing combined `hCutflow` histogram for all samples.
- Added `hCutflowEle` and `hCutflowMu` for Semilep signal samples only.
- The channel-specific cumulative cutflows contain:
  1. Input
  2. Overlap filter
  3. HEM veto
  4. Lumi mask
  5. Trigger + primary vertex
  6. Tight lepton
  7. Loose-lepton veto
  8. MET / Ntuple selected
- Electron and muon selections are counted independently after the common
  event-level filters.

### Vertex and pileup-validation inputs

- Added `PV_npvsGood` to store the number of reconstructed good primary
  vertices for data and MC.
- Added `Pileup_nTrueInt` to store the true pileup interaction count for MC.
- `Pileup_nTrueInt` remains at its initialized value of `-1` for data.
- Existing nominal and varied pileup weights remain available through
  `Weight_pu`, `Weight_puUp`, and `Weight_puDown`.

### Semileptonic muon thresholds

- Raised the loose-muon `pT` threshold from `15 GeV` to `30 GeV`.
- Raised the prompt-muon threshold from `pT > 30 GeV` to `pT >= 55 GeV`.

### Generated-output handling

- Added a local `.gitignore` so the comparison outputs under `oldCert/` and
  `newCert/` are not committed.

## Local validation

- Rebuilt `makeNtuple` successfully after the source changes.
- Verified that all three new JSON files are present and parse as JSON
  objects.
- Produced matching 2017 SingleMuon era-B Ntuples from the same 28 input
  skim files using the old and new certifications.
- Both ROOT files open successfully and contain `AnalysisTree`,
  `PV_npvsGood`, and `Pileup_nTrueInt`.

| 2017 SingleMuon era B | Selected events |
|---|---:|
| Old EOY2017 certification | 3,349,063 |
| New UL2017 Golden JSON | 3,355,405 |
| Difference | +6,342 (+0.1894%) |

The comparison ROOT files are retained locally but ignored by Git.

## Out-of-scope working-tree changes

The following modified files are outside `Ntuple_Skim` and are not described
by this Ntuple commit summary:

- `Skim_NanoAOD/condor/checkJobStatus.py`
- `Skim_NanoAOD/condor/createJdlFiles.py`
- `Skim_NanoAOD/condor/runMakeSkims.sh`
