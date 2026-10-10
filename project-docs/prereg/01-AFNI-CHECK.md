# Prereg 01, deviation 4: AFNI fallback path

**Status: not used: license obtained 2026-10-10.** The FreeSurfer license is
now in place, so under deviation 4 the whole sample runs through fMRIPrep.
No participant was preprocessed with AFNI. The code below stays in the repo,
unused.

## What was built
- AFNI AFNI_26.3.02 ('Philip the Arab'), afni_proc.py 8.11, installed in
  WSL Ubuntu-24.04 from the official Ubuntu 24 instructions. The binaries
  live on H: (`/mnt/h/bio-data/afni/abin`, 958 files, 273 MB by `du`). The
  apt dependencies follow the official admin script, minus the desktop apps
  (gedit, evince, eog, gnome-terminal, nautilus, firefox, gnome-tweaks). The
  R packages (`rPkgsInstall`) were not installed; only group-level R
  programs such as 3dMVM need them.
- `scripts/run_afni_one.sh`: @SSwarper, then FSL FAST from the fMRIPrep
  container with sMRIPrep's flags, then one afni_proc.py call per rest run.
  Each run gets slice timing, blip-up/down correction when fmaplink accepts
  the field maps, motion correction and a warp to the TemplateFlow
  MNI152NLin2009cAsym 2 mm grid. No smoothing. The run then writes
  fMRIPrep-format confounds and calls the unchanged extract.py.
- `src/conn01/afni_confounds.py`, `afni_prep.py`, `afni_qc.py`, ported from
  the fMRIPrep 25.2.6 container sources: 24 motion parameters, Power FD,
  aCompCor with the 50% variance rule, cosine and non-steady-state columns.
- `scripts/pipeline_guard.sh`. `run_all.sh` takes `PIPELINE=afni|fmriprep`
  and refuses to mix pipelines in one output directory. The guard also runs
  in `run_fmriprep_one.sh`.
- Tests: `tests/test_conn01_afni.py`. The full conn01 suite passed, 61 tests.

## Fix that applies to the fMRIPrep path
fMRIPrep 25.2.6 (checked in the container source, `RenameACompCor`) names the
WM components `w_comp_cor_XX` and the CSF components `c_comp_cor_XX`.
`a_comp_cor_XX` holds only the combined mask. `denoise.compcor_columns` used
to read only `a_comp_cor_*` with Mask WM or CSF. On real 25.2 output it would
have found zero WM and zero CSF components, and the model would have run
without aCompCor, recording a count of 0 and raising no error. It now selects
by the JSON "Mask" field across all three prefixes. A regression test covers
this. No participant had been preprocessed when the fix was made.

## End-to-end check
Stopped. One participant (sub-NDARINVAG023WG3) was fetched. The blip plan
paired the field maps for all 4 runs. @SSwarper ran for about 80 minutes and
was still in the nonlinear warp (3dQwarp) when it was stopped. No afni_proc
run, confounds, time series, QC image or connectivity value was produced. The
partial files were deleted. Runtime, memory, registration quality, censored
fraction and tSNR are unknown for this path.

Does not prove: the synthetic tests show format compatibility with
extract.py and denoise.py. They do not show that AFNI preprocessing matches
fMRIPrep on real data.
