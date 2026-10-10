"""Extract region-mean BOLD time series and QC numbers from fMRIPrep outputs.

Usage (inside the conn01 venv, run with python -I):
  python -I -m conn01.extract --fmriprep-dir DERIV --bids-dir BIDS \
      --participant NDARINV... --out OUTROOT

For each resting-state run it writes, under OUTROOT/sub-<label>/:
  <run>_timeseries.tsv                       region means, one column per region
  <run>_desc-confounds_timeseries.tsv/.json  copied from fMRIPrep
  sub-<label>_qc.json                        per-run QC and provenance
No connectivity value is computed or printed here.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from . import atlas
from . import denoise as dn

SPACE = "space-MNI152NLin2009cAsym_res-2"
CHUNK = 64  # volumes read at a time, keeps memory near 0.3 GB per chunk


def find_runs(fmriprep_dir: Path, label: str) -> list[Path]:
    func = Path(fmriprep_dir) / f"sub-{label}" / "func"
    pattern = f"sub-{label}_task-rest*_{SPACE}_desc-preproc_bold.nii.gz"
    return sorted(func.glob(pattern))


def run_stem(bold: Path) -> str:
    """sub-X_task-restAP_run-01 from the preprocessed BOLD file name."""
    return bold.name.split(f"_{SPACE}")[0]


def extract_timeseries(bold: Path) -> pd.DataFrame:
    """Region means per volume, read in chunks to bound memory."""
    import nibabel as nib

    img = nib.load(str(bold))
    ref = nib.Nifti1Image(np.zeros(img.shape[:3], np.int8), img.affine)
    masks, _ = atlas.load_masks(reference_img=ref)
    n_t = img.shape[3]
    cols = {name: np.empty(n_t) for name in masks}
    for t0 in range(0, n_t, CHUNK):
        t1 = min(n_t, t0 + CHUNK)
        block = np.asarray(img.dataobj[..., t0:t1], dtype=np.float32)
        for name, series in atlas.region_means(block, masks).items():
            cols[name][t0:t1] = series
    return pd.DataFrame(cols)


def bids_metadata(bids_dir: Path, label: str, stem: str) -> dict:
    """Scanner fields from the raw BOLD sidecar (site information)."""
    side = Path(bids_dir) / f"sub-{label}" / "func" / f"{stem}_bold.json"
    if not side.exists():
        return {}
    meta = json.loads(side.read_text())
    keep = ("InstitutionName", "StationName", "ManufacturersModelName",
            "RepetitionTime")
    return {k: meta.get(k) for k in keep}


def run_record(stem: str, conf: pd.DataFrame, meta: dict, n_ts: int) -> dict:
    """QC numbers for one run; no connectivity values."""
    if len(conf) != n_ts:
        raise ValueError(f"{stem}: confounds rows {len(conf)} != volumes {n_ts}")
    qc = dn.run_qc(conf)
    n_wm = len(dn.compcor_columns(meta, "WM", n=10**6, allow_fewer=True))
    n_csf = len(dn.compcor_columns(meta, "CSF", n=10**6, allow_fewer=True))
    nss = [c for c in conf.columns if c.startswith("non_steady_state")]
    return {"run": stem, **vars(qc), "n_acompcor_wm_retained": n_wm,
            "n_acompcor_csf_retained": n_csf, "n_non_steady_state": len(nss)}


def process_participant(fmriprep_dir: Path, bids_dir: Path, label: str,
                        out_root: Path) -> Path:
    runs = find_runs(fmriprep_dir, label)
    if not runs:
        raise FileNotFoundError(f"no {SPACE} rest BOLD for sub-{label}")
    out = Path(out_root) / f"sub-{label}"
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for bold in runs:
        stem = run_stem(bold)
        conf_src = bold.parent / f"{stem}_desc-confounds_timeseries.tsv"
        shutil.copy2(conf_src, out / conf_src.name)
        shutil.copy2(conf_src.with_suffix(".json"), out / f"{conf_src.stem}.json")
        ts = extract_timeseries(bold)
        ts.to_csv(out / f"{stem}_timeseries.tsv", sep="\t", index=False)
        conf = pd.read_csv(conf_src, sep="\t")
        meta = json.loads(conf_src.with_suffix(".json").read_text())
        rec = run_record(stem, conf, meta, len(ts))
        rec["scanner"] = bids_metadata(bids_dir, label, stem)
        records.append(rec)
    write_qc(out, label, records, fmriprep_dir)
    return out


def write_qc(out: Path, label: str, records: list[dict], fmriprep_dir: Path) -> None:
    desc = Path(fmriprep_dir) / "dataset_description.json"
    generated = json.loads(desc.read_text()).get("GeneratedBy") if desc.exists() else None
    usable = sum(r["usable"] for r in records)
    qc = {"participant": f"sub-{label}", "fmriprep_generated_by": generated,
          "n_runs": len(records), "n_usable_runs": usable,
          "meets_min_usable_runs": usable >= dn.MIN_USABLE_RUNS,
          "regions": {k: list(v[1]) for k, v in atlas.REGIONS.items()},
          "runs": records}
    (out / f"sub-{label}_qc.json").write_text(json.dumps(qc, indent=2))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fmriprep-dir", type=Path, required=True)
    ap.add_argument("--bids-dir", type=Path, required=True)
    ap.add_argument("--participant", required=True, help="label without sub-")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    label = a.participant.removeprefix("sub-")
    out = process_participant(a.fmriprep_dir, a.bids_dir, label, a.out)
    print(f"[extract] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
