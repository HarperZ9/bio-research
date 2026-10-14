# Project 02 next dataset: data readiness (ds004856, Dallas Lifespan Brain Study)

Date: 2026-10-14 (Pacific). Register: data receipt, flavored. Follows brief 02b
(project-docs/briefs/02b-free-longitudinal-data.md), "Alternative path if the
DUA is closed". Pre-registration draft: 02c-dlbs-stress-hippocampus.md (DRAFT,
not frozen).

## Result first

1. The 02b lead, OpenNeuro ds007026 ("stressrisk_openNeuro"), does not fit
   project 02. It is a two-session risk-task fMRI set. The T1w exists only at
   ses-1 (52 files); ses-2 holds functional runs and events only. It ships no
   README and no participants.tsv, so no stress variable is on file. Observed
   from the S3 listing (3155 objects, 64.6 GB) and dataset_description.json
   (CC0, DOI 10.18112/openneuro.ds007026.v1.0.0, version 1.0.0, 2025-12-03).
2. Among the 02b rank-3 sets, one fits: ds004856, the Dallas Lifespan Brain
   Study (DLBS). It is CC0, needs no account, has T1w at three waves about 4 to
   5 years apart, and carries the NIH Toolbox Perceived Stress survey at waves
   2 and 3. It is the first free, individual-accessible dataset found that has
   both repeated T1w at a 2+ year interval and a numeric stress measure.
3. The usable core for a prospective stress test is small: 162 participants
   have perceived stress at wave 2 and a T1w at waves 2 and 3 (median interval
   5.0 years). At that n the test has about 70 percent power for a partial
   |r| of 0.20 (calculation in the pre-registration draft).
4. Wave 1 has no perceived-stress score. It has NEO-PI-R neuroticism (a trait
   proxy for stress reactivity, not stress) and CES-D, with 300 participants
   holding T1w at waves 1 and 2.
5. Nothing that a pre-registration should lock has been opened: no stress,
   mood, neuroticism or volume value was printed or summarized. Only column
   names and counts of non-missing cells were read (details below).

## Candidates checked today

All from the public bucket s3://openneuro.org/ (anonymous list-objects-v2) and
each dataset's own dataset_description.json, README, CHANGES,
participants.json and the header line of participants.tsv.

| Dataset | Licence (own file) | Size | T1w by session (from listing) | Stress-relevant variable on file | Verdict |
|---|---|---|---|---|---|
| ds007026 stressrisk_openNeuro | CC0 | 64.6 GB | ses-1: 52; ses-2: none | none (no participants.tsv, no phenotype) | Not usable: one T1w per person |
| ds004856 DLBS | CC0 (dataset_description.json and README) | 242.6 GB total; T1w + sidecars 6.97 GB | wave1 465, wave2 301, wave3 201 (run-1 957, run-2 10) | NIH Toolbox Perceived Stress FF (waves 2, 3); CES-D, GDS (all waves); NEO-PI-R (wave 1) | Selected |
| ds004169 QTIM | CC0 | 148.0 GB | ses-01 1202, ses-02 140 | none open; phenotype needs a data transfer agreement and institutional ethics approval (README) | Not usable: retest interval about 3.5 months; phenotype closed to an individual |
| ds003592 neurocognitive aging | CC0 | 111.0 GB | ses-1 301 only | none in participants.tsv | Not usable: one T1w per person |
| ds005752 NIMH Healthy Research Volunteer | CC0 (DOI in its file points to ds004215 v2.0.1) | 715.4 GB | ses-01 493, ses-02 6 | ACE, BTQ, BAI, BDI, PHQ-9 indicators in participants.tsv | Not usable for change: 6 repeat T1w. A cross-sectional trauma set, noted for project 01 |
| ds007522 Precision Aging Network | CC0 | 526.5 GB | ses-01 944, ses-02 36, ses-03 1, follow01 67, follow02 12 | none on OpenNeuro; phenotype via the PAN data portal (request) | Not usable now: about 79 follow-ups, phenotype behind a portal request |
| ds005112 NIMH structural | CC0 | 7.3 GB | ses-01 568, ses-02 223, ses-03 94, ses-04 14, ses-05 2, ses-06 11 | age, sex, handedness only | Not usable: no stress variable; median age 16 |

## DLBS facts read from its own files

- Licence: "This dataset is licensed under the Creative Commons Zero (CC0)
  v1.0 License" (README). dataset_description.json: License CC0, DatasetDOI
  10.18112/openneuro.ds004856.v1.3.0. CHANGES top entry 1.3.0, 2025-07-10.
- Design (README; KTTK document, revised 2025-06-18): wave 1 collected
  2008 to 2014 (464 people), wave 2 2012 to 2017 (338 returned), wave 3 2018
  to 2022 (224 returned); wave 3 intervals are "somewhat less standardized due
  to interference from COVID-19 restrictions". Ages 20 to 89 at wave 1.
- Surveys at waves 2 and 3 were given online, "typically within a week of
  cognitive testing" (README). The MRI visit date relative to the survey is
  given only as intervals between MRI scans, so the survey-to-scan gap is
  UNVERIFIED.
- NIH Toolbox Perceived Stress Survey (KTTK p. 122): fixed form, assesses "how
  unpredictable, uncontrollable and overloaded respondents find their lives",
  5-point scale from "never" to "very often". Columns NIHPerStressFfRaw49,
  NIHPerStressFfTheta49, NIHPerStressFfT49 (T-score against the NIH Toolbox
  normative sample, mean 50, SD 10), NIHPerStressFfSE49, sheet
  derivatives/surveys/Template10_Psychosocial.xlsx, one sheet per wave.
- Structural derivatives: derivatives/brainsummary/Template_Structural_MRI.xlsx,
  FreeSurfer 5.3 run cross-sectionally per wave with manual edits and a second
  QC review (README). Columns include LhHippocampusVol, RhHippocampusVol,
  LhAmygdalaVol, RhAmygdalaVol, thalamus and putamen volumes, and
  TotalIntracranialVol.
- MRI sidecars (sub-1003, three waves): Manufacturer Philips; ProtocolName
  "MPRAGE2100SENSE" at wave 1 and "WIPMPRAGE2100SENSE" at waves 2 and 3;
  TR 8.37, 8.18, 8.25 ms; TE 3.89, 3.75, 3.78 ms. Model, field strength and
  software version are absent from the sidecars, so a scanner or software
  change between waves is UNVERIFIED. The protocol name changed between wave 1
  and wave 2 and not between waves 2 and 3 (observed for one participant; the
  full audit runs after freeze, see the pre-registration draft).
- Second MPRAGE runs exist for 10 scans, acquired "due to motion artifacts in
  their first scan" (README).
- Amyloid PET global SUVR: about 298 rows at wave 1 and 299 at wave 2
  (Template17_Amyloid.xlsx sheet dimensions).

## Availability counts (no values opened)

Counts of non-missing cells (empty, NA and xx counted missing; README: "xx"
marks a wave not returned). Pairs are participants with a T1w at both waves in
the S3 listing. Intervals and ages come from participants.tsv, which holds no
exposure or outcome.

| Item | Wave 1 | Wave 2 | Wave 3 |
|---|---|---|---|
| Perceived Stress FF raw | 0 | 296 | 201 |
| CES-D total | 460 | 289 | 147 |
| NEO-PI-R neuroticism total | 463 | 0 | 0 |
| FreeSurfer LhHippocampusVol | 464 | 295 | 190 |

| Pair | Both T1w | Interval (y), median [min, max] | Baseline age, median [min, max] | With exposure |
|---|---|---|---|---|
| W1 to W2 | 300 | 4.0 [2.51, 5.58] | 61 [21, 89]; 80 under 50 | NEO-N W1: 300; CES-D W1: 297 |
| W2 to W3 | 179 | 5.0 [2.89, 6.27] | 62 [26, 92]; 45 under 50 | PSS W2: 162; PSS W3: 165; both: 149; CES-D W2: 158 |
| W1 to W3 | 193 | 9.0 [6.06, 10.59] | 57 [21, 88] | NEO-N W1: 193 |

T1w wave patterns: all three waves 179, W1 only 150, W1 and W2 121, W1 and W3 14.

What was read from the outcome and exposure files, in full: sheet names,
sheet dimensions, header rows, and the non-missing counts above (computed by a
script that prints counts only). The FreeSurfer count used the
LhHippocampusVol column for presence only.

## Files on disk

Local root `H:\bio-data\ds004856` (WSL `/mnt/h/bio-data/ds004856`), never C:.
Download 2026-10-14 by anonymous HTTPS from s3://openneuro.org/ds004856/.

- Top level and derivatives, 26 files: README, CHANGES, .bidsignore,
  dataset_description.json, participants.json, participants.tsv, three
  task-*_events.json and task-Words_events.tsv, "DLBS KTTK.pdf", and the
  derivatives spreadsheets (brainsummary, cognition, surveys, genotyping).
  Excluded: code/pet_scripts and eprime files.
- T1w: every `sub-*/ses-wave*/anat/*_acq-MPRAGE_run-*_T1w.nii.gz` and its
  JSON sidecar. Other modalities (FLAIR, DWI, BOLD, ASL, PET) not fetched.
- Per-file SHA-256 and sizes: `02c-results/ds004856-manifest.txt` (format:
  sha256, bytes, path relative to the local root). Totals are in the section
  below.

Totals: 1960 files, 6,979,331,806 bytes (967 T1w NIfTI, 967 JSON sidecars,
26 top-level and derivative files). Every file size matches the S3 listing; no
file missing; 0 failed fetches. Manifest file SHA-256
d6eac10d9b645db89612c514069ecf98d0f9419325ad6bd8df520b8f2b1c5ce6.

Selected hashes:

| File | SHA-256 |
|---|---|
| participants.tsv | d739c81d5728d2f2968f30dfcaeef1320f1f3d435f2c42ea26be2286ca239c75 |
| dataset_description.json | 9f876cd42d97aece654c40b5ee55a4ea6aae56c605dececb11491968bc9f5d63 |
| README | c48a1c5be7804ec57dd8f2747100fd12b84688d13b832ecf9fd633f81454ffab |
| derivatives/surveys/Template10_Psychosocial.xlsx | 2ef162534468acef64cfa9ae7a1933e6d435bc69bdaf7c8bd3327b5ad8fa3155 |
| derivatives/brainsummary/Template_Structural_MRI.xlsx | 4de326963652a08a8b0ca5c2d9c2828b464ac10d6b279941faeee30a53b1b94f |
| DLBS KTTK.pdf | 69fb005e99ad6b8ad2d1867ca70b5e4dca6fb3acb1ae8432f4d70229df26b5b1 |

No image was opened or segmented. The images were downloaded before the
pre-registration is frozen, which differs from the Tier B order (freeze, then
download). The manifest hashes let the freeze commit show the files have not
changed since download.

## Disk

H: had 96 GiB free at the start of this step (the fMRIPrep batch for project 01
is writing to H: and keeps priority). This step used 7.0 GB, under the 15 GB cap
set for it. H: showed 70 GiB free at 12:38 PDT, about 25 minutes later. The
other 19 GiB went elsewhere; the project 01 work dir held 30 GB at that time,
and it grows and shrinks per participant, so no rate is claimed. Any further
download for project 02 should first check that H: keeps room for the batch.

## Not done, and why

- NKI-RS reply (eligibility question sent 2026-10-10): not checked here. Mail
  is the author's.
- Segmentation: not run. It waits for the freeze, and CPU is shared with the
  MMBU training and the project 01 batch.
- Scanner audit across all sidecars: deferred to after freeze; it reads only
  metadata, but the exclusion rule that uses it must be fixed first.

## Does not prove

- That DLBS perceived stress measures the glucocorticoid exposure in brief 02.
  It is self-report over the past month, with no cortisol.
- That the 162 core participants are representative. Returners are likely
  healthier than dropouts (inferred), and wave 2 and 3 cut-offs allowed some
  cognitive decline.
- That the listing counts equal usable images. QC, motion and protocol
  changes are not yet checked.
- That no better free set exists. The OpenNeuro search in 02b was partial.
