# Pre-registration 01: childhood trauma and amygdala-vmPFC resting connectivity

Frozen before any phenotype value or image from the dataset was downloaded or
viewed. Only file names, `dataset_description.json` and
`phenotype/ctq01_definitions.tsv` were read. Operator choices of 2026-10-09:
anatomical vmPFC, full sample, smallest effect of interest |r| = 0.20.

## Data
OpenNeuro ds005237, Transdiagnostic Connectome Project, snapshot 1.1.3, CC0,
DOI 10.18112/openneuro.ds005237.v1.1.3. Transdiagnostic adult sample with
four resting-state runs per participant (per `dataset_description.json`).

## Variables
- **Exposure:** CTQ total = sum of `ctqscore_ea`, `ctqscore_en`, `ctqscore_pa`,
  `ctqscore_pn`, `ctqscore_sa` (range 25 to 125). Participants missing any of
  the five are excluded from the primary test.
- **Outcome:** bilateral amygdala to vmPFC resting-state functional
  connectivity: Pearson correlation of the mean denoised BOLD time series of
  the two regions, Fisher z transformed, averaged over usable runs.
- **Covariates:** age, sex, site (if more than one site is recorded), mean
  framewise displacement (FD) over usable runs, number of retained volumes.

## Regions (anatomical, Harvard-Oxford probabilistic atlas, 50% threshold, MNI152NLin2009cAsym 2 mm)
- Amygdala: left plus right amygdala (subcortical atlas).
- vmPFC, primary: "Frontal Medial Cortex" (cortical atlas).
- Subgenual cingulate, pre-declared secondary: "Subcallosal Cortex" (cortical
  atlas), the anatomical label closest to BA25.

## Preprocessing
fMRIPrep (exact version recorded in the receipt), output space
MNI152NLin2009cAsym. Denoising: 24 motion parameters, aCompCor (5 white matter
plus 5 CSF components), cosine drift terms, no global signal regression in the
primary analysis. Volumes with FD > 0.5 mm are censored. A run is unusable if
more than 20% of volumes are censored or mean FD > 0.3 mm. A participant needs
at least 2 usable runs.

## Primary test
Partial correlation between CTQ total and the outcome, adjusting for the
covariates. Two-sided, alpha 0.05. Report the partial r, its 95% CI and the
90% CI.

Decision rule, set before data:
- **Association:** 95% CI excludes 0. Magnitude is read against 0.20: an
  estimate at or beyond |0.20| is a meaningful association; below it is a
  real but small one.
- **No meaningful association:** 90% CI lies entirely within -0.20 to 0.20
  (two one-sided tests at alpha 0.05).
- **Inconclusive:** neither of the above.

The smallest effect of interest, |r| = 0.20, is about 4% shared variance. At
the expected n (about 200 to 240 after exclusions) this is near the smallest
effect the sample can confirm or exclude. Effects between 0.10 and 0.20 can
be missed; any write-up must say so.

## Secondary test
Same model with the subcallosal region in place of vmPFC. Holm correction
across the primary and secondary tests.

## Sensitivity analyses (exploratory, reported as such)
1. With global signal regression.
2. Left and right amygdala separately.
3. Each CTQ subscale separately.
4. Excluding participants with a high minimization/denial score
   (`ctqscore_val` at its maximum).
5. Adding diagnostic group as a covariate.

## Not tested here
PTSD diagnosis (no PTSD-specific scale in this dataset), causal direction,
task-evoked regulation. Rest connectivity is not emotion regulation.

## Deviations
Any change after this file is committed is logged below with date and reason.

2026-10-09, decided before any participant was preprocessed and before any
phenotype or connectivity value was opened (raised in
`01-DEVIATIONS-PROPOSED.md`):

1. aCompCor: use the available components up to 5 per mask (WM, CSF) and
   record the count per participant. Sensitivity analysis: exclude
   participants with fewer than 5 in either mask. Reason: the original text
   did not say what to do when fMRIPrep keeps fewer; exclusion would drop
   data on a technicality.
2. Holm: an "association" call for either test requires both the 95% CI
   excluding 0 and a Holm-adjusted p < 0.05 across the two tests. Reason:
   the original text named Holm without saying whether it gates the call;
   this is the stricter reading.
3. Susceptibility distortion correction (not specified originally): link each
   session's field maps to that session's rest runs with `IntendedFor` in
   local copies of the sidecars, so fMRIPrep uses the acquired field maps.
   If a session's field maps do not match its runs (phase-encoding or
   geometry), that participant falls back to fMRIPrep's field-map-less SyN
   correction, recorded in the QC receipt. Reason: vmPFC sits in the region
   most affected by susceptibility distortion and dropout.

2026-10-10, before any participant was preprocessed:

4. Preprocessing fallback. fMRIPrep requires a FreeSurfer license even with
   `--fs-no-reconall`, and the operator does not hold one yet. If the license
   is not in place when the AFNI path below passes its synthetic and
   one-participant checks, preprocess with AFNI `afni_proc.py` instead:
   same output space (MNI152NLin2009cAsym, 2 mm), the same 24 motion
   parameters, aCompCor (5 WM + 5 CSF from eroded masks, computed the same
   way as in the fMRIPrep path), cosine drift terms, the same censoring and
   run-exclusion rules, and reverse-phase-encoding distortion correction
   (`-blip_reverse_dset`) where the field maps allow it. The whole sample
   uses one pipeline; no participant mixes the two. Whichever pipeline is
   used is named in the result. Reason: avoid an indefinite block on a
   licensing step, without changing the analysis.

The pre-registration body above is unchanged; its frozen hash in HASHES.md
refers to the version before this section was filled in.
