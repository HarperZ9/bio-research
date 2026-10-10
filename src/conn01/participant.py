"""Participant-level outcome: Fisher z averaged over usable runs, plus QC.

Reads the per-run files that extract.py writes:
  <sub>_<run>_timeseries.tsv          region-mean BOLD (undenoised)
  <sub>_<run>_desc-confounds_timeseries.tsv / .json   fMRIPrep confounds
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import denoise as dn

PRIMARY = ("amygdala_bilateral", "vmpfc_fmc")
SECONDARY = ("amygdala_bilateral", "subcallosal")
LATERAL = [("amygdala_l", "vmpfc_fmc"), ("amygdala_r", "vmpfc_fmc"),
           ("amygdala_l", "subcallosal"), ("amygdala_r", "subcallosal")]
ALL_PAIRS = [PRIMARY, SECONDARY] + LATERAL


def summarize_runs(runs: list[tuple[pd.DataFrame, pd.DataFrame, dict]],
                   gsr: bool = False, allow_fewer_compcor: bool = False) -> dict:
    """Combine runs given as (timeseries, confounds, confounds_json) tuples.

    Returns a dict with per-pair mean z over usable runs, mean FD over usable
    runs (all defined FD values pooled), retained volume count (uncensored
    volumes in usable runs), run counts and an inclusion flag.
    """
    qcs = [dn.run_qc(c) for _, c, _ in runs]
    usable = [i for i, q in enumerate(qcs) if q.usable]
    out = {"n_runs": len(runs), "n_usable_runs": len(usable),
           "included": len(usable) >= dn.MIN_USABLE_RUNS,
           "runs": [vars(q) for q in qcs]}
    if not usable:
        out.update(mean_fd=float("nan"), n_retained=0)
        return out
    fds = np.concatenate([
        runs[i][1]["framewise_displacement"].to_numpy(float) for i in usable
    ])
    out["mean_fd"] = float(np.nanmean(fds))
    out["n_retained"] = int(sum(qcs[i].n_volumes - qcs[i].n_censored for i in usable))
    per_run = [
        dn.run_connectivity(runs[i][0], runs[i][1], runs[i][2], ALL_PAIRS,
                            gsr=gsr, allow_fewer_compcor=allow_fewer_compcor)
        for i in usable
    ]
    for key in per_run[0]:
        out[f"z__{key}"] = float(np.mean([r[key] for r in per_run]))
    return out


def load_subject_runs(sub_dir: Path) -> list[tuple[pd.DataFrame, pd.DataFrame, dict]]:
    """Load every rest run that extract.py wrote for one participant."""
    runs = []
    for ts_path in sorted(Path(sub_dir).glob("*_timeseries.tsv")):
        if "desc-confounds" in ts_path.name:
            continue
        stem = ts_path.name[: -len("_timeseries.tsv")]
        conf = Path(sub_dir) / f"{stem}_desc-confounds_timeseries.tsv"
        meta = conf.with_suffix(".json")
        runs.append((pd.read_csv(ts_path, sep="\t"),
                     pd.read_csv(conf, sep="\t"),
                     json.loads(meta.read_text())))
    return runs


def build_outcome_table(root: Path, gsr: bool = False,
                        allow_fewer_compcor: bool = False) -> pd.DataFrame:
    """One row per participant directory under root that has a DONE marker."""
    rows = []
    for sub_dir in sorted(Path(root).glob("sub-*")):
        if not (sub_dir / "DONE").exists():
            continue
        try:
            summary = summarize_runs(load_subject_runs(sub_dir), gsr,
                                     allow_fewer_compcor)
            summary.pop("runs")
            summary["error"] = ""
        except (dn.CompCorShortfall, KeyError, ValueError) as exc:
            # Recorded, not swallowed: the row is excluded and the reason kept.
            print(f"[conn01] {sub_dir.name}: excluded, {type(exc).__name__}: {exc}")
            summary = {"included": False, "error": f"{type(exc).__name__}: {exc}"}
        summary["participant_id"] = sub_dir.name
        rows.append(summary)
    return pd.DataFrame(rows)
