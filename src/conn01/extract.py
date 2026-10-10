"""Extract region-mean BOLD time series and QC numbers from fMRIPrep outputs.

Usage (inside the conn01 venv, run with python -I):
  python -I -m conn01.extract --fmriprep-dir DERIV --bids-dir BIDS \
      --participant NDARINV... --out OUTROOT
  python -I -m conn01.extract --requalify --participant NDARINV... --out OUTROOT

--requalify recomputes the motion QC (FD rules of prereg 01 deviation 5)
from the confounds copies already in OUTROOT/sub-<label>/, with the TR stored
in the existing QC JSON, after the fMRIPrep derivatives were cleaned up. It
reads no time series and keeps the other QC fields as they were.

For each resting-state run it writes, under OUTROOT/sub-<label>/:
  <run>_timeseries.tsv                       region means, one column per region
  <run>_desc-confounds_timeseries.tsv/.json  copied from fMRIPrep
  sub-<label>_qc.json                        per-run QC and provenance
Per run the QC holds motion QC under the filtered (primary) and unfiltered
(original) FD rules and "roi_signal": tSNR and coverage per region on the
minimally processed BOLD (record only, conn01.roi_signal).
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
from . import motion
from . import roi_signal as rs

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
    return extract_run(bold)[0]


def brain_mask_path(bold: Path) -> Path:
    """fMRIPrep's brain mask for the run, same space as the BOLD."""
    return bold.with_name(bold.name.replace("_desc-preproc_bold", "_desc-brain_mask"))


def extract_run(bold: Path) -> tuple[pd.DataFrame, dict]:
    """Region means per volume plus the roi_signal QC, in one chunked pass."""
    import nibabel as nib

    img = nib.load(str(bold))
    ref = nib.Nifti1Image(np.zeros(img.shape[:3], np.int8), img.affine)
    masks, _ = atlas.load_masks(reference_img=ref)
    n_t = img.shape[3]
    cols = {name: np.empty(n_t) for name in masks}
    acc = rs.SignalAccumulator(img.shape[:3])
    for t0 in range(0, n_t, CHUNK):
        t1 = min(n_t, t0 + CHUNK)
        block = np.asarray(img.dataobj[..., t0:t1], dtype=np.float32)
        acc.add(block)
        for name, series in atlas.region_means(block, masks).items():
            cols[name][t0:t1] = series
    mpath = brain_mask_path(bold)
    if mpath.exists():
        brain, source = np.asarray(nib.load(str(mpath)).dataobj) > 0, mpath.name
    else:
        brain, source = acc.mean_sd()[0] > 0, "nonzero_temporal_mean (no brain mask file)"
    return pd.DataFrame(cols), rs.summarize(acc, masks, brain, source)


def bids_metadata(bids_dir: Path, label: str, stem: str) -> dict:
    """Scanner fields from the raw BOLD sidecar (site information)."""
    side = Path(bids_dir) / f"sub-{label}" / "func" / f"{stem}_bold.json"
    if not side.exists():
        return {}
    meta = json.loads(side.read_text())
    keep = ("InstitutionName", "StationName", "ManufacturersModelName",
            "RepetitionTime")
    return {k: meta.get(k) for k in keep}


def run_record(stem: str, conf: pd.DataFrame, meta: dict, n_ts: int | None,
               tr: float) -> dict:
    """QC numbers for one run; no connectivity values.

    Motion QC is recorded under both FD rules; the unprefixed fields
    (n_censored, mean_fd, usable, reason) are the primary filtered rule.
    n_ts None skips the row check (requalify, time series not read).
    """
    if n_ts is not None and len(conf) != n_ts:
        raise ValueError(f"{stem}: confounds rows {len(conf)} != volumes {n_ts}")
    n_wm = len(dn.compcor_columns(meta, "WM", n=10**6))
    n_csf = len(dn.compcor_columns(meta, "CSF", n=10**6))
    used = dn.compcor_counts(meta)
    nss = [c for c in conf.columns if c.startswith("non_steady_state")]
    return {"run": stem, **dn.run_qc_both(conf, tr), "n_acompcor_wm_retained": n_wm,
            "n_acompcor_csf_retained": n_csf, "n_acompcor_wm_used": used["WM"],
            "n_acompcor_csf_used": used["CSF"], "n_non_steady_state": len(nss)}


def process_participant(fmriprep_dir: Path, bids_dir: Path, label: str,
                        out_root: Path, sdc_receipt: Path | None = None) -> Path:
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
        ts, signal = extract_run(bold)
        ts.to_csv(out / f"{stem}_timeseries.tsv", sep="\t", index=False)
        conf = pd.read_csv(conf_src, sep="\t")
        meta = json.loads(conf_src.with_suffix(".json").read_text())
        scanner = bids_metadata(bids_dir, label, stem)
        tr = motion.repetition_time(meta, scanner)
        rec = run_record(stem, conf, meta, len(ts), tr)
        rec["scanner"] = scanner
        rec["roi_signal"] = signal
        records.append(rec)
    sdc = json.loads(sdc_receipt.read_text()) if sdc_receipt else None
    write_qc(out, label, records, fmriprep_dir, sdc)
    return out


def write_qc(out: Path, label: str, records: list[dict], fmriprep_dir: Path,
             sdc: dict | None = None) -> None:
    desc = Path(fmriprep_dir) / "dataset_description.json"
    generated = json.loads(desc.read_text()).get("GeneratedBy") if desc.exists() else None
    write_qc_json(out, label, records, generated, sdc)


def write_qc_json(out: Path, label: str, records: list[dict], generated,
                  sdc: dict | None) -> None:
    usable = sum(r["usable"] for r in records)
    usable_u = sum(r["usable_unfiltered"] for r in records)
    qc = {"participant": f"sub-{label}", "fmriprep_generated_by": generated,
          "n_runs": len(records), "fd_rule": dn.RULE_FILTERED,
          "n_usable_runs": usable,
          "meets_min_usable_runs": usable >= dn.MIN_USABLE_RUNS,
          "n_usable_runs_unfiltered": usable_u,
          "meets_min_usable_runs_unfiltered": usable_u >= dn.MIN_USABLE_RUNS,
          "acompcor_min_used": {
              "WM": min((r["n_acompcor_wm_used"] for r in records), default=0),
              "CSF": min((r["n_acompcor_csf_used"] for r in records), default=0)},
          "sdc": sdc,
          "regions": {k: list(v[1]) for k, v in atlas.REGIONS.items()},
          "runs": records}
    (out / f"sub-{label}_qc.json").write_text(json.dumps(qc, indent=2))


def requalify(out_root: Path, label: str) -> Path:
    """Recompute motion QC from kept confounds; other QC fields are kept.

    The TR comes from the existing QC JSON (tr_s, else the BOLD sidecar
    fields stored under scanner), else the confounds JSON. roi_signal is kept
    if present, else recorded as unavailable because the BOLD is gone.
    """
    out = Path(out_root) / f"sub-{label}"
    qc_path = out / f"sub-{label}_qc.json"
    old = json.loads(qc_path.read_text())
    records = []
    for prev in old["runs"]:
        stem = prev["run"]
        conf_path = out / f"{stem}_desc-confounds_timeseries.tsv"
        conf = pd.read_csv(conf_path, sep="\t")
        meta = json.loads(conf_path.with_suffix(".json").read_text())
        scanner = prev.get("scanner") or {}
        tr = prev.get("tr_s") or motion.repetition_time(meta, scanner)
        rec = run_record(stem, conf, meta, None, float(tr))
        if rec["n_volumes"] != prev["n_volumes"]:
            raise ValueError(f"{stem}: {rec['n_volumes']} confounds rows, QC had "
                             f"{prev['n_volumes']} volumes")
        rec["scanner"] = scanner
        rec["roi_signal"] = prev.get("roi_signal") or {
            "unavailable": "preprocessed BOLD removed at cleanup; requalified "
                           "from confounds only"}
        records.append(rec)
    write_qc_json(out, label, records, old.get("fmriprep_generated_by"), old.get("sdc"))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fmriprep-dir", type=Path)
    ap.add_argument("--bids-dir", type=Path)
    ap.add_argument("--requalify", action="store_true",
                    help="recompute motion QC from the confounds kept in --out")
    ap.add_argument("--participant", required=True, help="label without sub-")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--sdc-receipt", type=Path,
                    help="fmaplink receipt: field maps or field-map-less SyN")
    a = ap.parse_args(argv)
    label = a.participant.removeprefix("sub-")
    if a.requalify:
        out = requalify(a.out, label)
        print(f"[extract] requalified {out}")
        return 0
    if a.fmriprep_dir is None or a.bids_dir is None:
        ap.error("--fmriprep-dir and --bids-dir are required unless --requalify")
    out = process_participant(a.fmriprep_dir, a.bids_dir, label, a.out,
                              a.sdc_receipt)
    print(f"[extract] wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
