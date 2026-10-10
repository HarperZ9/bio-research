"""Pre-registered denoising, censoring and run exclusion (prereg 01).

Regressors: 24 motion parameters, aCompCor (top 5 white-matter plus top 5 CSF
components; per deviation 1 of 2026-10-09, the available components up to 5
per mask when fMRIPrep retains fewer), all cosine drift terms; no global
signal in the primary model.
Censoring: volumes with FD > 0.5 mm. A run is unusable if more than 20% of its
volumes are censored or its mean FD > 0.3 mm. A participant needs >= 2 usable
runs.

Denoising is applied to region-mean time series. Ordinary least squares
residualization is linear, so the mean of voxelwise residuals equals the
residual of the region mean; the result matches denoising voxels first.
Censored volumes are removed before the regression and the correlation.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

FD_CENSOR_MM = 0.5
MAX_CENSORED_FRACTION = 0.20
MAX_RUN_MEAN_FD_MM = 0.3
MIN_USABLE_RUNS = 2
N_COMPCOR_PER_MASK = 5

_MOTION_BASE = ["trans_x", "trans_y", "trans_z", "rot_x", "rot_y", "rot_z"]
MOTION_24 = [
    f"{b}{s}" for b in _MOTION_BASE
    for s in ("", "_derivative1", "_power2", "_derivative1_power2")
]




@dataclass
class RunQC:
    n_volumes: int
    n_censored: int
    mean_fd: float
    censored_fraction: float
    usable: bool
    reason: str


def fd_series(confounds: pd.DataFrame) -> np.ndarray:
    """Framewise displacement; the undefined first value is set to 0."""
    return confounds["framewise_displacement"].fillna(0.0).to_numpy(float)


def censor_mask(fd: np.ndarray, threshold: float = FD_CENSOR_MM) -> np.ndarray:
    """True for volumes kept; FD strictly above the threshold is censored."""
    return ~(np.asarray(fd) > threshold)


def run_qc(confounds: pd.DataFrame) -> RunQC:
    """Apply the pre-registered run exclusion rules to one run."""
    fd = fd_series(confounds)
    keep = censor_mask(fd)
    n = len(fd)
    n_cens = int((~keep).sum())
    frac = n_cens / n if n else 1.0
    # Mean FD over defined values (the first volume has no FD).
    raw = confounds["framewise_displacement"].to_numpy(float)
    mean_fd = float(np.nanmean(raw)) if np.isfinite(raw).any() else float("nan")
    reasons = []
    if frac > MAX_CENSORED_FRACTION:
        reasons.append("censored_fraction>0.20")
    if not mean_fd <= MAX_RUN_MEAN_FD_MM:
        reasons.append("mean_fd>0.3")
    return RunQC(n, n_cens, mean_fd, frac, not reasons, ";".join(reasons))


COMPCOR_PREFIXES = ("a_comp_cor_", "c_comp_cor_", "w_comp_cor_")


def compcor_columns(meta: dict, mask: str, n: int = N_COMPCOR_PER_MASK) -> list[str]:
    """Top retained aCompCor columns for one mask ("WM" or "CSF"), up to n.

    Components are ranked by singular value within the mask, using the
    confounds JSON. The mask is read from each entry's "Mask" field, so both
    naming schemes work: fMRIPrep >= 21 names WM and CSF components
    w_comp_cor_XX and c_comp_cor_XX (a_comp_cor_XX is the combined mask);
    older releases named all of them a_comp_cor_XX. Fewer than n are
    returned when fewer were retained (prereg 01 deviation 1); callers
    record the count.
    """
    rows = [
        (k, v.get("SingularValue", 0.0)) for k, v in meta.items()
        if k.startswith(COMPCOR_PREFIXES) and v.get("Mask") == mask
        and v.get("Retained", True)
    ]
    rows.sort(key=lambda kv: -kv[1])
    return [k for k, _ in rows[:n]]


def compcor_counts(meta: dict) -> dict[str, int]:
    """Number of aCompCor components used per mask (capped at 5)."""
    return {m: len(compcor_columns(meta, m)) for m in ("WM", "CSF")}


def design_matrix(confounds: pd.DataFrame, meta: dict, gsr: bool = False) -> np.ndarray:
    """Nuisance design: intercept + 24 motion + 5 WM + 5 CSF aCompCor + cosines."""
    cols = list(MOTION_24)
    cols += compcor_columns(meta, "WM")
    cols += compcor_columns(meta, "CSF")
    cols += sorted(c for c in confounds.columns if c.startswith("cosine"))
    if gsr:
        cols.append("global_signal")
    missing = [c for c in cols if c not in confounds.columns]
    if missing:
        raise KeyError(f"confounds missing columns: {missing}")
    x = confounds[cols].fillna(0.0).to_numpy(float)
    return np.column_stack([np.ones(len(x)), x])


def residualize(y: np.ndarray, x: np.ndarray) -> np.ndarray:
    """OLS residuals of y (t, k) on design x (t, p)."""
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    return y - x @ beta


def run_connectivity(ts: pd.DataFrame, confounds: pd.DataFrame, meta: dict,
                     pairs: list[tuple[str, str]], gsr: bool = False) -> dict[str, float]:
    """Fisher z of the Pearson r for each region pair in one run."""
    keep = censor_mask(fd_series(confounds))
    x = design_matrix(confounds, meta, gsr)[keep]
    if x.shape[0] <= x.shape[1] + 2:
        raise ValueError("too few retained volumes for the nuisance model")
    names = sorted({r for p in pairs for r in p})
    res = residualize(ts[names].to_numpy(float)[keep], x)
    idx = {n: i for i, n in enumerate(names)}
    out = {}
    for a, b in pairs:
        r = np.corrcoef(res[:, idx[a]], res[:, idx[b]])[0, 1]
        out[f"{a}__{b}"] = float(np.arctanh(r))
    return out
