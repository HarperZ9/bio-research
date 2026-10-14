# Pre-registration 02C (DRAFT): perceived stress and hippocampal volume change over five years (ds004856, Dallas Lifespan Brain Study)

DRAFT, version 0.1, 2026-10-14 (Pacific). NOT FROZEN. It enters
project-docs/prereg/HASHES.md only when the author approves it and it is
committed as version 1. Written before any stress, mood, personality or volume
value, and before any T1w image, was opened. The T1w files and the derivative
spreadsheets are already on disk, unopened, with SHA-256 receipts in 02c-DATA.md;
that order differs from Tier B and is disclosed here.

Parents: brief 02 (sections 5 to 7), brief 02b, finding F-02-1 (noise floor),
data readiness note 02c-DATA.md.

## 1. Question and decision

Question (primary): in community adults, does higher self-reported perceived
stress at one visit predict a faster loss of hippocampal volume over the next
five years, after age, sex, interval and baseline volume?

Decision informed: whether project 02 continues on free data alone. If DLBS
shows support (section 7), the next step is a replication plan on a second
free cohort. If it is a null with an equivalence result, project 02 records
that a small effect in community adults is excluded at this n and moves its
effort to the dense-sampling and noise-floor track. If it is inconclusive, the
project needs a larger cohort, which today means a data agreement (NKI-RS
phenotype or another), and the author decides whether to pursue one.

Verifier the model did not see: the DLBS perceived-stress scores and the
T1w-derived volumes, opened only after this file is frozen and hashed.

## 2. Data

ds004856 v1.3.0, CC0, local root H:\bio-data\ds004856. Facts and counts are in
02c-DATA.md. Waves are about 4 to 5 years apart; perceived stress exists at
waves 2 and 3 only.

## 3. Samples and exclusions (fixed before outcome)

Primary sample P: participants with a T1w at wave 2 and wave 3 and a
non-missing NIHPerStressFfT49 at wave 2. Expected n 162 before exclusions.

Secondary sample S: participants with a T1w at waves 1 and 2 and a
non-missing NEONeurTot46 at wave 1. Expected n 300.

Image choice: where a session has run-2, use run-2 (README: the second MPRAGE
was taken because of motion in the first). Otherwise run-1.

Exclusions, applied in this order and logged with counts:
1. A T1w that fails to load or whose segmentation fails.
2. Per-structure QC, as in Billot et al. 2023: a scan is dropped from an
   outcome when the SynthSeg QC score of the region that outcome uses is
   below 0.65. Hippocampal outcomes use the "hippocampus+amygdala" column,
   thalamus uses "thalamus", putamen uses "putamen+pallidum". A participant
   is dropped from an outcome if either scan of the pair fails. TIV has no QC
   column and is not filtered. Source and limits: section 10, item 2.
3. A participant whose two scans are byte-identical (same SHA-256).
4. No exclusion on any volume, change or stress value.

Protocol audit (metadata only, run after freeze and before the outcome is
opened): tabulate ProtocolName, TR and TE per wave from every sidecar. A
participant whose two scans differ in ProtocolName within the pair is flagged;
the flag enters as a covariate, not an exclusion.

## 4. Segmentation (fixed)

Same pipeline as F-02-1, so the noise floor transfers: SynthSeg 2.0 robust,
BBillot/SynthSeg commit 2a2aa3bbfccb83f8253a51ca8b329b9938a2646d, weights with
the SHA-256 values in 02-DATA.md, CPU, venv /mnt/h/bio-data/venvs/synthseg,
call `SynthSeg_predict.py --i <list> --o <list> --robust --vol <list> --qc
<list> --threads <n>`. Each wave is segmented cross-sectionally with the same
settings. No GPU. The run is resumable (skip images whose outputs exist) and
runs at below-normal priority with a thread cap so the project 01 batch and
other jobs keep their CPU.

Secondary pipeline: the DLBS-provided FreeSurfer 5.3 values
(Template_Structural_MRI.xlsx, SubcorticalVolume and GlobalVariables sheets).
Used only for the pipeline-sensitivity analysis in 6.4.

## 5. Variables

- H_w: bilateral hippocampus at wave w = SynthSeg left plus right hippocampus
  (labels 17 and 53), divided by SynthSeg total intracranial volume.
- Outcome Y (primary): annualized percent change,
  Y = 100 x (H_3 - H_2) / H_2 / interval, interval = MRIW2toW3 in years.
- Y_S (sample S): the same from wave 1 to wave 2, interval MRIW1toW2.
- Negative-control outcomes: thalamus (labels 10, 49) and putamen (12, 51),
  built the same way.
- Secondary outcome: amygdala (18, 54), no predicted sign.
- Exposure E (primary): NIHPerStressFfT49 at wave 2, standardized over sample P.
- Exposure E_S (secondary): NEONeurTot46 at wave 1, standardized over sample S.
- Covariates: baseline age (AgeMRI at the first wave of the pair), age squared
  (centered), sex, interval, baseline H (standardized), mean SynthSeg QC of
  the two scans, protocol-change flag (section 3).
- Exploratory covariates (sensitivity only): CES-D total at the baseline wave;
  amyloid global SUVR at the baseline wave where present.

## 6. Analyses (fixed)

### 6.1 Positive control (run first; gates the test)

In sample P (and separately S), regress Y on baseline age with sex. Expected:
older baseline age, more negative Y. If the age slope is not negative with a
95 percent CI that excludes 0, the pipeline is not measuring change and the
stress test is reported as void. Also reported: mean Y and its SD by age band
(under 50, 50 to 69, 70 and over).

### 6.2 Primary test (H1)

Ordinary least squares: Y ~ E + age + age^2 + sex + interval + baseline H + QC
+ protocol flag. HC3 robust standard errors.

- Effect unit: standardized beta of E (Y standardized over P), and the same
  as percent per year per 10 T-score points.
- H1 prediction: beta of E is negative.
- Test: two-sided, alpha 0.05. Partial r from the t statistic is reported.
- Equivalence: smallest effect of interest |beta| = 0.20 SD of Y per SD of E
  (my choice, matching the project 01 margin of |r| 0.20 set by the author on
  2026-10-09; the author may change it before freezing). TOST at alpha 0.05,
  that is, the 90 percent CI against plus or minus 0.20.

### 6.3 Secondary test (H2, sample S)

The same model with Y_S and E_S. Prediction: negative. Two-sided alpha 0.05.
Reported as secondary; neuroticism is a trait proxy, not a stress measure.

### 6.4 Sensitivity (reported regardless of result)

(a) without the QC and protocol covariates; (b) FreeSurfer 5.3 provided
values in place of SynthSeg; (c) adding CES-D at the baseline wave;
(d) adding amyloid global SUVR (subset where present); (e) excluding
participants with MMSE below 26 at either wave of the pair; (f) wave 3
perceived stress in place of wave 2 (retrospective; it measures the month
before wave 3 and cannot order cause); (g) negative-control outcomes thalamus
and putamen in place of H; (h) QC cut at 0.75 instead of 0.65 (section 10,
item 2).

### 6.5 Reverse direction (exploratory)

Baseline H at wave 2 predicting E at wave 3, with age, sex and E at wave 2.
Supports a vulnerability account if the beta of H is negative with a 95
percent CI that excludes 0.

### 6.6 Code and tests before the real run

Code goes in src/gm02c/ with synthetic tests: the model recovers a planted
beta of -0.3 on simulated data with the real sample size, and TOST classifies
a planted beta of 0 as equivalent at n 162 in 50 to 70 percent of runs (the
expected rate is about 59 percent from section 8; this checks the code, not
the data).

## 7. Decision rules (fixed)

- Void: positive control fails (6.1).
- Support for H1: beta of E negative, p < 0.05, same sign in sensitivity
  (a) and (b), and the negative-control outcomes (6.4 g) show an absolute
  beta under half the hippocampal beta.
- Opposite: beta of E positive with p < 0.05. Reported as not supporting the
  glucocorticoid-cascade prediction.
- Null with equivalence: the 90 percent CI lies inside plus or minus 0.20.
- Otherwise: inconclusive. The report states the CI and what it excludes.
- H2 never overrides H1. If H2 shows support while H1 is inconclusive, the
  report says so and labels it a trait association.

## 8. Power, stated honestly

Fisher z approximation, two-sided alpha 0.05, 8 covariates (hand calculation,
inferred):
- n 162: power 0.70 at |r| 0.20, 0.46 at 0.15, 0.88 at 0.25; 80 percent power
  needs |r| about 0.22.
- n 150 (after exclusions, assumed): power 0.67 at 0.20.
- Sample S, n 300: power 0.93 at 0.20, 0.73 at 0.15.
- Measurement noise: F-02-1 gives a within-person hippocampal CV of 0.77
  percent on one scanner and one day-scale. Over a 5-year interval that is
  about 1.09 / 5 = 0.22 percent per year of noise in Y (inferred; scanner and
  protocol drift across years will add to it). Typical hippocampal loss in
  older adults is about 1 percent per year (from memory, low confidence), so
  noise alone does not swamp the age effect.
- Equivalence at plus or minus 0.20: at n 162 the SE of beta is about
  1 / sqrt(153) = 0.081 and the 90 percent CI half-width about 0.13, so
  equivalence needs an estimate within about 0.067 of 0. With a true beta of
  0 that happens in about 59 percent of samples.

## 9. Does not prove

- Perceived stress is self-report over the past month. It is not cortisol and
  not life events, and one month need not represent five years.
- Observational: a link could come from a common cause (health, income,
  sleep, early neurodegeneration). The reverse-direction test and the
  covariates address only part of this.
- Volume is net apparent tissue volume, not dendritic, synaptic, glial or
  neuronal change.
- Returners at wave 3 are a selected group (48 percent of wave 1). A null may
  reflect range restriction.
- A null does not refute the cascade hypothesis for severe or prolonged
  stress, which this community sample may not contain.

## 10. Open items before freezing (author)

1. Confirm or change the margin of 0.20 SD.
2. QC threshold, checked 2026-10-14. Value 0.65 verified; author confirms
   its use given the limits below.
   - Source opened: Billot et al., "Robust machine learning segmentation for
     large-scale analysis of heterogeneous clinical brain MRI datasets",
     arXiv 2209.02032v2 (compiled 2023-01-04), https://arxiv.org/abs/2209.02032 ;
     published as PNAS 2023, DOI 10.1073/pnas.2216399120 (the PNAS page itself
     was not opened; the arXiv v2 text was). PDF SHA-256
     55496dd05adf44105be7cd4e8571b9f992ba9fb3cce3eed5243c2f9659bd11b1.
   - Methods, automated QC module: "The segmentation of a region is then
     classified as failed if it obtains a predicted Dice score lower than
     0.65 (a value chosen based on the validation set)." The scores are
     regressed Dice values, clipped to 0 to 1 in the released code
     (SynthSeg/predict_synthseg.py, np.clip(..., 0, 1)).
   - Two uses in the paper: whole-scan rejection if any region scores below
     0.65 (594 clinical scans, against visual QC), and a per-structure rule
     in the aging analysis, keeping "only ... regions with a QC score above
     0.65". This draft uses the per-structure rule.
   - Threshold sensitivity, Fig. S9b: accuracy "only varies by 0.01 for
     thresholds between 0.55 and 0.75". Hence sensitivity (h) at 0.75.
   - Applies to the robust model: the repo names the robust model
     "SynthSeg-robust", tutorial 7-synthseg+.py "show[s] how the robust
     version of SynthSeg was trained", and the README asks users of the
     robust version and automated QC to cite this paper. So the paper's
     SynthSeg+ is the --robust path used here (observed in the repo at commit
     2a2aa3b).
   - Limits: (1) the paper's QC regressor scores 10 regions; the released
     2.0 QC model writes 8 grouped columns (for example
     "hippocampus+amygdala"). Whether 0.65 was re-validated for the grouped
     2.0 model is UNVERIFIED; the repo README and code state no threshold.
     (2) The 0.65 cut was validated on heterogeneous clinical scans; on 1 mm
     research MPRAGE it is expected to catch only gross failures (inferred).
     (3) The FreeSurfer SynthSeg wiki page timed out twice on 2026-10-14 and
     was not read. (4) The repo README's "arxiv" link points to 2203.01969,
     a different (MICCAI 2022) paper; 2209.02032 is the matching preprint.
3. Confirm wave 2 stress as primary (prospective) over wave 3 (larger n by 3,
   but retrospective).
4. Approve the freeze; the commit hash and file SHA-256 then go to HASHES.md.
