# Prereg 01: proposed deviations and open interpretation points

Written 2026-10-09 while building the pipeline (src/conn01, scripts/). The
frozen pre-registration (sha256 4d4681b9...f753) is unchanged. Nothing below
is applied. Each item needs a decision by the operator and lead session
before the real run. Where the code had to pick something, it picks the most
literal reading and says so. No phenotype values or participant
connectivity values were opened to write this.

## A. Problems the prereg text cannot settle as written

1. **aCompCor component count.** The prereg fixes 5 white-matter plus 5 CSF
   components. fMRIPrep keeps only the components that explain 50% of the
   variance in each mask, so a run can have fewer than 5 retained for a mask.
   Current code: raises `CompCorShortfall`, and `build_outcome_table`
   excludes that participant and records the reason. The flag
   `--allow-fewer-compcor` uses whatever is available instead. Options: (a)
   exclude, as now; (b) use what is available and report counts; (c) rerun
   fMRIPrep with a fixed component count. `n_acompcor_wm_retained` and
   `n_acompcor_csf_retained` per run are in each QC JSON, so the scale of the
   problem is visible before deciding.
2. **Holm versus the CI decision rule.** The prereg sets the decision rule on
   the unadjusted 95% and 90% CIs and also asks for Holm across the primary
   and secondary tests. It does not say whether "association" requires the
   Holm-adjusted p < 0.05. Current code reports both: `decision` from the
   unadjusted CIs and `association_survives_holm`. Proposal: an association
   is claimed only when both hold.
3. **Field maps not linked.** In the participant inspected, the spin-echo
   field maps carry `B0FieldIdentifier: SpinEchoFieldMap_fmap`, but the rest
   BOLD sidecars carry neither `B0FieldSource` nor `IntendedFor`. fMRIPrep
   will then most likely skip distortion correction (moderate confidence;
   confirm in the first participant's fMRIPrep log or report). The prereg
   does not mention distortion correction. Options: (a) run as is, no
   correction; (b) add `B0FieldSource` to local copies of the BOLD sidecars;
   (c) `--use-syn-sdc`. The fetch script downloads the field maps either way.

## B. Underspecified details: what the code does now

4. **Non-steady-state volumes.** Not covered by the prereg. Code keeps all
   volumes and only adds the listed regressors; the count of flagged volumes
   per run is in the QC JSON.
5. **Mean FD.** Run exclusion uses the mean of the defined FD values in the
   run (the first volume has none). The participant covariate pools the
   defined FD values of all usable runs, censored volumes included.
   "Retained volumes" is the sum of uncensored volumes over usable runs.
6. **Bilateral amygdala.** One mask, the union of left and right labels; the
   series is the mean over all its voxels (not the average of the left and
   right series).
7. **Censoring in the regression.** Censored volumes are dropped before the
   nuisance regression and the correlation. Denoising runs on region means,
   which equals voxelwise denoising then averaging (checked in a test).
8. **Site.** Taken from a phenotype column if the lead passes `--site-col`,
   otherwise from the scanner `InstitutionName` in the BIDS sidecar. Added
   as a covariate only if more than one level is present, as registered.
9. **CTQ missing codes.** 999, -999, 777 and -777 count as missing; any other
   subscale value outside 5 to 25 stops the run. The README says missing
   values are coded 999; the other codes are guesses and harmless if absent.
10. **Sensitivity 4.** "ctqscore_val at its maximum" is read as the maximum
    observed in the analysed sample. If it means the scale maximum, pass
    that value instead (one-line change in run_analysis.py).
11. **Complete cases.** Participants missing any covariate are dropped from
    the model, in addition to the registered CTQ exclusion. The n is
    reported.

## C. Facts checked during the build

- ds005237 has 241 participant folders on S3; the inspected participant has
  four rest runs (restAP run-01/02, restPA run-01/02), matching the prereg
  ("four resting-state runs"). The brief said six; the prereg is right for
  this participant.
- Planned download per participant (T1w, four rest BOLD with sidecars, field
  maps): 2.48 GB for sub-NDARINVAG023WG3, from the S3 listing.
- fMRIPrep docs (stable page, v25.2.5) describe `--fs-no-reconall` as
  "Disable FreeSurfer surface preprocessing" and say FreeSurfer tools need a
  license; they do not say the license is optional with that flag. The
  scripts require it.
