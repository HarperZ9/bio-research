"""Project 01: CTQ total vs amygdala-vmPFC resting connectivity (ds005237).

Governed by project-docs/prereg/01-amygdala-vmpfc-ctq.md (frozen). Modules:
atlas (region masks), extract (region time series and QC from fMRIPrep
outputs), denoise (pre-registered confound regression and censoring),
analyze (partial correlation, decision rule, Holm). AFNI fallback path
(prereg 01 deviation 4): afni_prep (helpers around afni_proc.py),
afni_confounds (fMRIPrep-format confounds), afni_qc (overlay, tSNR).
"""
