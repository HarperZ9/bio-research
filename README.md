# bio-research

Preregistered empirical studies and reproducible Python pipelines in neurobiology (trauma connectivity, longitudinal hippocampal MRI, opsin kinetics, neuronal microtubule/tau stability) and Pacific Northwest forest pathology and mycology.

Every study separates observed results, inferences, proposals, and unknowns, cites checked primary DOIs, ships an explicit "does not prove" boundary, and keeps null results intact.

## Shipped Modules (`src/` and `tests/`)

- `src/audit04/`: Common mycorrhizal network (CMN) overcitation audit on citing sentences for Simard et al. 1997 and Beiler et al. 2010 (`200` double-coded units, Cohen's kappa `0.893`).
- `src/conn01/`: Amygdala-vmPFC functional connectivity extraction, denoising, motion QC, and replication utilities.
- `src/gm02/`: Longitudinal grey-matter and hippocampal volume noise-floor analysis (OpenNeuro `ds002674` 60-session single-subject dataset, GLS and permutation controls).
- `src/opsin03/`: Channelrhodopsin-2 (`ChR2`) kinetic modeling and reference checks against published NEURON models (`ModelDB 244414`).
- `src/phospho07b/`: Stress-linked tau phosphosite proteomics loaders, sequence mapping, set tests, and blocked analyses (`PXD024829`, `PXD016302`, `PXD057176`).
- `src/screen07/`: Microtubule-regulator mRNA transcriptomics screen across mouse chronic social defeat datasets (`GSE109315`, `GSE127812`, `GSE161726`).

## Published Empirical Findings (`project-docs/FINDINGS.md`)

1. **F-04-1 (CMN citation overreach):** Strict double-coded overreach rates of `37.0%` (Simard 1997) and `25.0%` (Beiler 2010) across `100` citing contexts per paper (`project-docs/audit04/CODEBOOK.md`).
2. **F-07-1 (Microtubule-regulator mRNA after chronic social defeat):** Null in discovery (`GSE109315`), evaluated across held-out cohorts (`GSE127812`, `GSE161726`).
3. **F-07b-1 (Stress-linked tau phosphosites, mouse mPFC after CUMS, `PXD016302`):** Weak null, verified with positive-control calibration (`PXD024829`).
4. **F-07c-1 (Stress-linked tau phosphosites, mouse hippocampus after chronic restraint, `PXD057176`):** Null, excluding a `1.5`-fold rise under the preregistered protocol.
5. **F-02-1 (Day-to-day hippocampal volume noise floor, `ds002674`, 60 sessions):** Measured `0.77%` day-to-day noise floor; lagged stress association not detected.

## Running Tests

```bash
PYTHONPATH=src pytest tests/
```

Raw external genomics, proteomics, and MRI datasets are kept out of git and downloaded from their public repositories (`GEO`, `PRIDE`, `OpenNeuro`, `ModelDB`) using the checksums and manifest files documented under `project-docs/prereg/`.

## Scope and Safety Policy

- Pathogen and forest-ecology modules cover detection, ecology, and management only; never virulence, host-range expansion, or spread enhancement.
- Human neuroimaging studies use public datasets whose terms permit reuse, with zero re-identification attempts.
