"""Participant-level outcome: Fisher z averaged over usable runs, plus QC.

Reads the per-run files that extract.py writes:
  <sub>_<run>_timeseries.tsv          region-mean BOLD (undenoised)
  <sub>_<run>_desc-confounds_timeseries.tsv / .json   fMRIPrep confounds
  <sub>_qc.json                       per-run TR (tr_s, or scanner.RepetitionTime)

Censoring and run exclusion follow the FD rule passed in: "filtered" (prereg
01 deviation 5, the primary rule) or "unfiltered" (the original rule, the
pre-registered sensitivity analysis). The mean FD covariate stays fMRIPrep's
unfiltered framewise_displacement over usable runs under both rules.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import denoise as dn
from . import motion

PRIMARY = ("amygdala_bilateral", "vmpfc_fmc")
SECONDARY = ("amygdala_bilateral", "subcallosal")
LATERAL = [("amygdala_l", "vmpfc_fmc"), ("amygdala_r", "vmpfc_fmc"),
           ("amygdala_l", "subcallosal"), ("amygdala_r", "subcallosal")]
ALL_PAIRS = [PRIMARY, SECONDARY] + LATERAL


def summarize_runs(runs: list[tuple[pd.DataFrame, pd.DataFrame, dict]],
                   gsr: bool = False, rule: str = dn.RULE_FILTERED) -> dict:
    """Combine runs given as (timeseries, confounds, confounds_json) tuples.

    Returns a dict with per-pair mean z over usable runs, mean FD over usable
    runs (all defined FD values pooled), retained volume count (uncensored
    volumes in usable runs), run counts, an inclusion flag, and the smallest
    aCompCor count used per mask over usable runs (deviation 1).
    """
    trs = [motion.repetition_time(m) if rule == dn.RULE_FILTERED else None
           for _, _, m in runs]
    qcs = [dn.run_qc(c, tr, rule) for (_, c, _), tr in zip(runs, trs)]
    usable = [i for i, q in enumerate(qcs) if q.usable]
    out = {"n_runs": len(runs), "n_usable_runs": len(usable),
           "included": len(usable) >= dn.MIN_USABLE_RUNS,
           "fd_rule": rule, "runs": [vars(q) for q in qcs]}
    if not usable:
        out.update(mean_fd=float("nan"), n_retained=0)
        return out
    fds = np.concatenate([
        runs[i][1]["framewise_displacement"].to_numpy(float) for i in usable
    ])
    out["mean_fd"] = float(np.nanmean(fds))
    out["n_retained"] = int(sum(qcs[i].n_volumes - qcs[i].n_censored for i in usable))
    counts = [dn.compcor_counts(runs[i][2]) for i in usable]
    out["n_compcor_wm_min"] = min(c["WM"] for c in counts)
    out["n_compcor_csf_min"] = min(c["CSF"] for c in counts)
    per_run = [
        dn.run_connectivity(runs[i][0], runs[i][1], runs[i][2], ALL_PAIRS, gsr=gsr,
                            rule=rule)
        for i in usable
    ]
    for key in per_run[0]:
        out[f"z__{key}"] = float(np.mean([r[key] for r in per_run]))
    return out


def load_subject_runs(sub_dir: Path) -> list[tuple[pd.DataFrame, pd.DataFrame, dict]]:
    """Load every rest run that extract.py wrote for one participant.

    When a confounds JSON has no RepetitionTime, the run's TR from the QC JSON
    is added to the in-memory metadata (files are not changed).
    """
    trs = qc_repetition_times(sub_dir)
    runs = []
    for ts_path in sorted(Path(sub_dir).glob("*_timeseries.tsv")):
        if "desc-confounds" in ts_path.name:
            continue
        stem = ts_path.name[: -len("_timeseries.tsv")]
        conf = Path(sub_dir) / f"{stem}_desc-confounds_timeseries.tsv"
        meta = conf.with_suffix(".json")
        m = json.loads(meta.read_text())
        if "RepetitionTime" not in m and trs.get(stem) is not None:
            m["RepetitionTime"] = trs[stem]
        runs.append((pd.read_csv(ts_path, sep="\t"),
                     pd.read_csv(conf, sep="\t"), m))
    return runs


def qc_repetition_times(sub_dir: Path) -> dict[str, float]:
    """Run stem to TR from the participant's QC JSON, if present."""
    out = {}
    for qc in Path(sub_dir).glob("sub-*_qc.json"):
        for r in json.loads(qc.read_text()).get("runs", []):
            tr = r.get("tr_s", (r.get("scanner") or {}).get("RepetitionTime"))
            if r.get("run") and tr is not None:
                out[r["run"]] = float(tr)
    return out


def build_outcome_table(root: Path, gsr: bool = False,
                        rule: str = dn.RULE_FILTERED) -> pd.DataFrame:
    """One row per participant directory under root that has a DONE marker."""
    rows = []
    for sub_dir in sorted(Path(root).glob("sub-*")):
        if not (sub_dir / "DONE").exists():
            continue
        try:
            summary = summarize_runs(load_subject_runs(sub_dir), gsr, rule)
            summary.pop("runs")
            summary["error"] = ""
        except (KeyError, ValueError) as exc:
            # Recorded, not swallowed: the row is excluded and the reason kept.
            print(f"[conn01] {sub_dir.name}: excluded, {type(exc).__name__}: {exc}")
            summary = {"included": False, "error": f"{type(exc).__name__}: {exc}"}
        summary["participant_id"] = sub_dir.name
        rows.append(summary)
    return pd.DataFrame(rows)
