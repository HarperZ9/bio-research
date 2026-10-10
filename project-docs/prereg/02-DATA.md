# Project 02 Tier B data receipts

Downloaded 2026-10-09 (Pacific) after the pre-registration was committed
(commit 961bf36, 02-tierB-noise-floor.md SHA-256
7d4a0604ee6878616ac7dc0c7c2bd47cef9e5edd12050d0d709aa294ffd50230). Local root:
`H:\bio-data\ds002674`. Source: public bucket s3://openneuro.org/ds002674/
(anonymous `aws s3 sync --no-sign-request` with include filters). Licence CC0
(dataset_description.json). Dataset DOI 10.18112/openneuro.ds002674.v1.0.5.

## Metadata read before the pre-registration

S3 object listing (728 objects), README, CHANGES, dataset_description.json, the
ses-01 and ses-31 T1w JSON sidecars, and the header line of participants.tsv.
No value of any table or image was printed or opened before the freeze.

## Files downloaded

124 files, 1,103,437,406 bytes:

| Item | Count | Bytes |
|---|---|---|
| `sub-01/ses-XX/anat/sub-01_ses-XX_T1w.nii.gz`, XX = 01 to 60 | 60 | 1,103,400,907 |
| `sub-01/ses-XX/anat/sub-01_ses-XX_T1w.json` | 60 | 475 each |
| participants.tsv | 1 | 2540 |
| README, CHANGES, dataset_description.json | 3 | 3910, 472, 1077 |

Per-file SHA-256 and sizes: `project-docs/prereg/02-results/ds002674-manifest.txt`
(format: sha256, bytes, path relative to the local root).

Selected hashes:

| File | SHA-256 |
|---|---|
| participants.tsv | b76f0fc1f516a079b27fb4ebb88e23ac27dd32d747dba1d369a6efab305d2f90 |
| dataset_description.json | caf1eb2ae0f84fc71700995ef6c05b9ff840e9dd113962a4b3be597b61c56499 |
| sub-01_ses-18_T1w.nii.gz | 294cdb6d8d1236bf631af1fe30047761199ad0c09b9171d2fb3924dc638093a8 |
| sub-01_ses-19_T1w.nii.gz | e50781d3a090925bb173f456d87b7f482e88271cb847f43ac219b2ae1298ae2a |

Exclusion rule 1 (duplicate T1w): no two T1w files share a SHA-256. The
decompressed voxel arrays of ses-17, ses-18 and ses-19 also differ (array
SHA-256 prefixes f82ed57a5109f037, 9b806892e2d1f1b7, 697494c28dea79b9). So
ses-19 is kept. All 60 images: 208 x 320 x 320 voxels, 0.8 x 0.797 x 0.797 mm.

Not in the dataset: hormone values, cortisol, scan dates and times, motion
estimates (see pre-registration section 2).

## Segmentation environment

- Code: github.com/BBillot/SynthSeg at commit
  2a2aa3bbfccb83f8253a51ca8b329b9938a2646d, cloned to
  `H:\bio-data\synthseg\SynthSeg`.
- Model weights: the README's author-hosted folder link returned HTTP 404 on
  2026-10-09. Weights fetched from the FreeSurfer git-annex HTTP store
  (https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/repo/annex.git,
  object path from the annex key) and checked against the SHA-256 in each key:

| Model | Bytes | SHA-256 | Check |
|---|---|---|---|
| synthseg_robust_2.0.h5 | 214,606,800 | 7bc30bf5c3d204f20c4a6cb5a283aedbcab6af1de927cda783f59b67d19cb01c | match |
| synthseg_qc_2.0.h5 | 49,878,004 | fb92e37daa0842bdd8a03bc06a3b36b0d38810e31c714659cedd09119c0abfb7 | match |
| synthseg_parc_2.0.h5 | 53,090,840 | 83bb1de76fb6f173c6dacacd433f81209fc6abb1dbc179a930ec06ecabbeb684 | match (not used) |

- Venv: `/mnt/h/bio-data/venvs/synthseg` (WSL Ubuntu 24.04), CPython 3.8.20
  from uv; tensorflow-cpu 2.2.0, keras 2.3.1, numpy 1.23.5, nibabel 5.0.1,
  h5py 2.10.0, protobuf 3.20.3, scipy 1.4.1.
- Call: `SynthSeg_predict.py --i in.txt --o out.txt --robust --vol vol.txt
  --qc qc.txt --threads 24`, CPU, one batch over all 60 images. Outputs in
  `H:\bio-data\ds002674-derivatives\synthseg\{seg,vol,qc}`. About 1 min 45 s
  per image on 24 cores, peak RSS about 8 GB.
- No FreeSurfer licence was used or needed.
