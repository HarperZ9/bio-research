"""Blocked two-factor design for 07c: log2 value ~ sex + stress, per site.

Rows are sites, columns are samples, NaN = missing. `sex` and `stress` are
boolean vectors. Each row is fitted by least squares on its observed samples,
vectorised over rows. The moderated t for the stress coefficient uses the
same empirical Bayes prior as the two-group code (stats.fit_f_dist).
"""
from __future__ import annotations

import numpy as np
from scipy import stats as sps

from .stats import fit_f_dist


def design(sex: np.ndarray, stress: np.ndarray) -> np.ndarray:
    """Columns [1, sex, stress]; the stress coefficient is last."""
    n = len(sex)
    return np.column_stack([np.ones(n), sex.astype(float), stress.astype(float)])


def cell_valid(y: np.ndarray, sex: np.ndarray, stress: np.ndarray, min_n: int = 2) -> np.ndarray:
    """Rows with at least min_n values in every sex x stress cell."""
    ok = np.ones(y.shape[0], bool)
    for s in (False, True):
        for g in (False, True):
            cols = (sex == s) & (stress == g)
            ok &= np.sum(~np.isnan(y[:, cols]), 1) >= min_n
    return ok


def lm_moderated_t(y: np.ndarray, x: np.ndarray, valid: np.ndarray, prior=None) -> dict:
    """Moderated t for the last coefficient of x, rows fitted on observed values."""
    w = ~np.isnan(y)
    y0 = np.where(w, y, 0.0)
    nr, p = y.shape[0], x.shape[1]
    beta = np.full((nr, p), np.nan)
    unscaled = np.full(nr, np.nan)
    s2 = np.full(nr, np.nan)
    df = np.sum(w, 1).astype(float) - p
    if np.any(valid):
        wv = w[valid].astype(float)
        xtx = np.einsum("rj,jp,jq->rpq", wv, x, x)
        inv = np.linalg.inv(xtx)
        xty = np.einsum("rj,jp->rp", y0[valid] * wv, x)
        b = np.einsum("rpq,rq->rp", inv, xty)
        resid = (y0[valid] - b @ x.T) * wv
        beta[valid] = b
        unscaled[valid] = inv[:, -1, -1]
        s2[valid] = np.sum(resid ** 2, 1) / df[valid]
    d0, s0sq = prior if prior is not None else fit_f_dist(s2[valid], df[valid])
    post = np.full(nr, s0sq) if np.isinf(d0) else (d0 * s0sq + df * s2) / (d0 + df)
    with np.errstate(invalid="ignore", divide="ignore"):
        t = beta[:, -1] / np.sqrt(post * unscaled)
    t = np.where(valid, t, np.nan)
    return {"t": t, "lfc": np.where(valid, beta[:, -1], np.nan), "valid": valid,
            "d0": d0, "s0sq": s0sq, "df": df}


def blocked_t(y: np.ndarray, sex: np.ndarray, stress: np.ndarray, prior=None) -> dict:
    """Moderated t for stress, sex-blocked, with cell eligibility."""
    return lm_moderated_t(y, design(sex, stress), cell_valid(y, sex, stress), prior)


def blocked_set_stat(y, sex, stress, idx) -> float:
    """Mean blocked moderated t over set rows (prior refitted on all rows)."""
    t = blocked_t(y, sex, stress)["t"][idx]
    return float(np.nanmean(t)) if np.any(np.isfinite(t)) else np.nan


def stratified_labelings(sex: np.ndarray, stress: np.ndarray, n: int = 2000,
                         seed: int = 7) -> list[np.ndarray]:
    """Random stress relabelings that keep the stress count within each sex."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        g = np.zeros(len(sex), bool)
        for s in (False, True):
            cols = np.flatnonzero(sex == s)
            k = int(stress[cols].sum())
            g[rng.choice(cols, k, replace=False)] = True
        out.append(g)
    return out


def stratified_perm_p(stat_fn, y, sex, stress, n: int = 2000, seed: int = 7) -> dict:
    """One-sided UP, DOWN and two-sided p; observed labeling added once."""
    obs = stat_fn(y, sex, stress)
    ref = np.array([stat_fn(y, sex, g) for g in stratified_labelings(sex, stress, n, seed)])
    ref = np.append(ref, obs)
    ref = ref[np.isfinite(ref)]
    tol = 1e-12
    return {"stat": obs, "p_up": float(np.mean(ref >= obs - tol)),
            "p_down": float(np.mean(ref <= obs + tol)),
            "p_two": float(np.mean(np.abs(ref) >= abs(obs) - tol)), "n": int(ref.size)}


def blocked_set_score_ci(y, sex, stress, idx) -> dict:
    """Set score (site-centred mean) regressed on [1, sex, stress]; 95% t interval."""
    sub = y[idx]
    score = np.nanmean(sub - np.nanmean(sub, 1, keepdims=True), 0)
    ok = np.isfinite(score)
    x = design(sex, stress)[ok]
    b, rss, *_ = np.linalg.lstsq(x, score[ok], rcond=None)
    df = int(ok.sum()) - x.shape[1]
    resid = score[ok] - x @ b
    s2 = float(resid @ resid) / df
    se = float(np.sqrt(s2 * np.linalg.inv(x.T @ x)[-1, -1]))
    h = sps.t.ppf(0.975, df) * se
    return {"diff": float(b[-1]), "lo": float(b[-1] - h), "hi": float(b[-1] + h),
            "se": se, "df": df, "scores": score.tolist()}
