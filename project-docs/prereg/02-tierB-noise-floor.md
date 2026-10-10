# Pre-registration 02 Tier B: within-person noise floor of hippocampal volume and a lagged stress association (ds002674)

Version 1, 2026-10-09 (Pacific). Written before any T1w image, and before any
value of perceived stress, mood, hormone or volume, was downloaded or opened.
Parent: brief 02 (project-docs/briefs/02-stress-grey-matter.md), sections 5
(Tier B), 6 and 7.

## 1. Question and decision

Question 1 (primary deliverable): how much does an automated hippocampal
volume estimate move from day to day in one healthy adult scanned 60 times on
one scanner, when nothing should change the tissue at a resolvable scale?

Question 2 (exploratory, low power): within this one person, does daily
Perceived Stress Scale (PSS) score on the scan day or the day before predict
hippocampal volume, in the direction the glucocorticoid cascade predicts
(higher stress, smaller volume)?

Decision informed: whether the Tier A UK Biobank test (brief section 5) can
resolve its -0.10 SD margin with single scans, or must rely on annualized
change over 2+ years with averaging, and so whether the application is worth
its cost (rule in section 7).

Verifier the model did not see: the 60 T1w images and the participants.tsv
values, opened only after this file is committed and hashed.

## 2. Metadata read before freezing (no data values opened)

Sources read on 2026-10-09: the public S3 listing of s3://openneuro.org/ds002674/
(728 objects), README, CHANGES, dataset_description.json, two T1w JSON
sidecars (ses-01, ses-31), and the header line only of participants.tsv
(row count 61 lines including the header; no value printed).

Observed:
- Licence CC0 (dataset_description.json). DatasetDOI
  10.18112/openneuro.ds002674.v1.0.5. One participant (sub-01), sessions
  ses-01 to ses-60. Each session has one T1w (MPRAGE 0.8 mm, Siemens 3T
  Prisma), one T2star, field maps and one resting BOLD. No sessions.tsv, no
  participants.json, no phenotype folder, no T2w hippocampal TSE file.
- participants.tsv columns: participant_id, session_id, poms_tension,
  poms_depression, poms_anger, poms_vigor, poms_fatigue, poms_confusion, psqi,
  state_anxiety, perceived_stress, total_calorie_intake.
- README: sessions 1 to 30 (2018) naturally cycling; sessions 31 to 60 (2019)
  on an oral hormonal contraceptive. 30 consecutive days per study.
  Questionnaires adapted to the past 24 hours, given each morning. Blood drawn
  at 10:00 (plus or minus 30 min) after 2 h without food or drink except
  water; no caffeine before sessions. A 3D-printed foam head case was used on
  days 8 to 30 of study 1 and all of study 2 (so sessions 1 to 7 had none).
  No physiological recordings during scanning.
- CHANGES 1.0.5: "data for ses-19 has been re-uploaded; scans were identical
  to ses-18".

Not available in this snapshot (observed by absence in the listing): serum
hormone values, cortisol, scan dates, scan clock times, motion estimates.
So the hormone covariate is the regime label only, and time of day cannot be
modeled (the protocol fixes it near 10:00 to 11:00, inferred from the README).

## 3. Data and exclusions

Download: the 60 `sub-01/ses-*/anat/sub-01_ses-*_T1w.nii.gz` files with their
JSON sidecars, participants.tsv, README, CHANGES, dataset_description.json, to
H:\bio-data\ds002674 (never C:). Sizes and SHA-256 go to
project-docs/prereg/02-DATA.md.

Exclusion rules, applied before any outcome value is examined:
1. If the ses-19 T1w is byte-identical (same SHA-256) to ses-18, ses-19 is
   excluded as a duplicate. Any other pair of byte-identical T1w files: the
   later session is excluded.
2. A session whose T1w fails to load or whose SynthSeg run fails is excluded
   and logged.
3. No exclusion on volume or QC value in the primary analysis. QC enters as
   a covariate.

## 4. Segmentation (fixed)

- Tool: SynthSeg 2.0, robust model, from github.com/BBillot/SynthSeg at
  commit 2a2aa3bbfccb83f8253a51ca8b329b9938a2646d. The author-hosted model
  folder link in the README returned HTTP 404 on 2026-10-09, so the model
  weights come from the FreeSurfer git-annex HTTP store, verified by the
  SHA-256 embedded in each annex key:
  - synthseg_robust_2.0.h5, 214,606,800 bytes, SHA-256
    7bc30bf5c3d204f20c4a6cb5a283aedbcab6af1de927cda783f59b67d19cb01c
  - synthseg_qc_2.0.h5, 49,878,004 bytes, SHA-256
    fb92e37daa0842bdd8a03bc06a3b36b0d38810e31c714659cedd09119c0abfb7
  - synthseg_parc_2.0.h5 (only if the code requires it to load), 53,090,840
    bytes, SHA-256 83bb1de76fb6f173c6dacacd433f81209fc6abb1dbc179a930ec06ecabbeb684
- Call: `SynthSeg_predict.py --i <T1w> --o <seg> --robust --vol <csv> --qc <csv>
  --threads <n>`, CPU, no --parc. No FreeSurfer licence is needed.
- Environment: Python 3.8 venv at /mnt/h/bio-data/venvs/synthseg (WSL Ubuntu
  24.04), tensorflow-cpu 2.2.x, keras 2.3.1, per the repository's Python 3.8
  requirements; exact versions logged in 02-DATA.md.
- FreeSurfer longitudinal (brief section 6 step 5) is not run: no licence yet.
  That is a planned deviation from the brief, recorded here before data.
- MRIQC (brief section 6 step 4) is not run. The quality covariate is the
  SynthSeg QC score (section 5). Planned deviation, recorded before data.

## 5. Variables

- Hippocampus, bilateral (primary): SynthSeg left-hippocampus plus
  right-hippocampus volume (labels 17 and 53), mm^3.
- Amygdala, bilateral (secondary): labels 18 and 54.
- TIV: the SynthSeg "total intracranial" volume column.
- Primary outcome Y = bilateral hippocampus / TIV, expressed as percent
  deviation from the mean over all retained sessions. Amygdala Y_amy is built
  the same way.
- Quality covariate Q: mean of all SynthSeg 2.0 QC scores for the session
  (every QC column except the subject name; column names logged at run time).
- Stress: perceived_stress, standardized to SD units over retained sessions.
  PSS lag 0 = the scan-day value. PSS lag 1 = the previous session's value
  within the same study (sessions are consecutive days); missing for the
  first session of each study and after any excluded or missing session.
- Regime: 0 for sessions 1 to 30 (natural cycle), 1 for 31 to 60 (oral
  contraceptive). Regime is confounded with study year and head-case use.
- Scan order: day index within study (1 to 30), centered.

## 6. Analyses (fixed)

### 6.1 Noise floor (primary deliverable)

For Y, raw bilateral hippocampus, left, right, amygdala and TIV:
- Mean, SD and coefficient of variation (CV, percent), over all retained
  sessions and within each study.
- Pooled within-study CV: sqrt of the mean of the two within-study variances,
  as percent of the grand mean. 90 percent CI from the chi-square
  distribution with (n - 2) degrees of freedom. This is the decision
  quantity, computed for Y.
- Robust SD: 1.4826 x MAD within study, percent.
- Session-to-session test-retest: differences between consecutive sessions
  within study; typical error = SD(differences) / sqrt(2), in percent; its
  ratio to the within-study SD; lag-1 autocorrelation of Y within study;
  correlation of left and right hippocampal series across sessions.
- Regime offset: mean Y difference (study 2 minus study 1) in percent, Welch
  95 percent CI. Descriptive only, confounded with year and head case.
- Pipeline sanity: if TIV within-study CV exceeds 1.5 percent, the noise
  floor is reported but flagged as limited by the pipeline, not the tissue.

### 6.2 Association model (exploratory)

Y_t = b0 + b1 PSS_t + b2 PSS_(t-1) + b3 Regime + b4 ScanOrder + b5 Q + e_t,
with e_t AR(1) within each study (common rho, no correlation across the
one-year gap), fit by generalized least squares with rho chosen by maximum
profile likelihood over (-0.95, 0.95). Sessions with lag-1 missing are
dropped (expected n about 57).

- Effect units: percent of mean hippocampal Y per 1 SD of PSS, with 95
  percent Wald CI from the GLS fit.
- Inference: block permutation. Within each study the daily PSS series is
  cut into 6 contiguous blocks of 5 days, blocks are shuffled within study,
  lag 1 is recomputed from the shuffled series, and the full model (rho
  re-estimated) is refit. 5000 permutations, seed 20261009. Two-sided p for
  each of b1 and b2 = (1 + count of |t_perm| >= |t_obs|) / 5001.
- Alpha: 0.025 per coefficient (two coefficients, Bonferroni, family 0.05).
- Secondary outcome: the same model for Y_amy. No prediction of sign
  (animal data suggest growth, brief section 5 Tier A).
- Sensitivity, reported regardless of result: (a) the model without Q; (b)
  raw bilateral volume (not TIV-normalized) as outcome with log TIV not
  included; (c) excluding sessions 1 to 7 (no head case); (d) excluding
  sessions whose Y lies more than 4 robust SD from the study median.
- Unit tests on synthetic data must pass before the real run: AR(1) GLS
  recovers a planted effect, and block permutation holds its error rate near
  nominal on autocorrelated null data.

### 6.3 Power, stated honestly

With about 57 usable sessions, 80 percent power, Fisher z: alpha 0.05 two-sided
detects |r| of about 0.35 or larger; at alpha 0.025 the threshold is about
|r| 0.40. Autocorrelation lowers the effective n and raises these thresholds.
A null here does not exclude a within-person association smaller than about
|r| 0.4, and says nothing about other people.

## 7. Decision rules (fixed)

Noise floor (thresholds from brief 02 section 6 step 9, the brief's own
inferred values, frozen here unchanged):
- Pooled within-study CV of Y at or below 0.5 percent: single-scan precision
  is good enough that the Tier A margin of 0.10 SD is realistic; the UK
  Biobank application is worth pursuing as designed.
- CV at or above 1.5 percent: single-scan changes of 1 to 2 percent are not
  resolvable; Tier A must use annualized change over 2+ years with averaging
  of repeated measures, and the application is worth pursuing only in that
  form.
- Between 0.5 and 1.5 percent: Tier A proceeds only with annualized change
  over 2+ years, and its margin is recomputed with the measured CV before any
  application text is written.
- If the 90 percent CI of the CV crosses a threshold, the call is labeled
  provisional.
- Transfer caveat: UK Biobank IDPs come from FSL FIRST, not SynthSeg, and from
  many people; this noise floor is one person, one scanner, one pipeline.

Association:
- Support for a within-person stress-to-volume association: b1 or b2
  negative with block-permutation p < 0.025, and the same sign in
  sensitivity analyses (a) and (b).
- Opposite sign with p < 0.025: reported as not supporting the cascade
  prediction.
- Otherwise: not detected. The report states the CI in percent per SD of PSS
  and what it excludes.
- No association result changes the noise-floor decision; Tier B was never
  powered to decide the stress question.

## 8. Does not prove

- One person, one scanner, one pipeline. Nothing here generalizes.
- Volume is net apparent tissue volume, not dendritic, synaptic, glial or
  neuronal change.
- Hydration (water allowed before sessions) and time-of-day effects can move
  apparent volume and are not measured; time of day is only fixed by
  protocol.
- PSS is self-report over 24 hours, not cortisol. No cortisol or hormone
  values are in the dataset.
- Regime is confounded with year and head-case use.
