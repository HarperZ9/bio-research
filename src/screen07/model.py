"""Filtering, normalization and a limma-trend-like moderated t in numpy.

Empirical Bayes follows Smyth (2004), Stat Appl Genet Mol Biol 3:3,
with a single (not trended) prior variance.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import special, stats


def filter_and_log(values: pd.DataFrame, kind: str, k: int) -> pd.DataFrame:
    """Return log2 expression for genes passing the pre-registered filter."""
    if kind == "counts":
        lib = values.sum(axis=0)
        cpm = values / lib * 1e6
        keep = (cpm >= 1).sum(axis=1) >= k
        counts = values.loc[keep]
        sf = median_of_ratios(counts)
        eff_lib = sf * np.exp(np.log(lib).mean())
        return np.log2((counts + 0.5) / (eff_lib + 1.0) * 1e6)
    if kind == "logcpm":
        keep = (values >= 0).sum(axis=1) >= k
        return values.loc[keep]
    if kind == "rpkm":
        keep = (values >= 1).sum(axis=1) >= k
        return np.log2(values.loc[keep] + 1.0)
    raise ValueError(f"unknown kind {kind}")


def median_of_ratios(counts: pd.DataFrame) -> pd.Series:
    """DESeq-style size factors over genes with no zero count."""
    pos = counts[(counts > 0).all(axis=1)]
    if len(pos) < 100:
        raise ValueError(f"only {len(pos)} genes without zeros for size factors")
    logc = np.log(pos)
    ratios = logc.sub(logc.mean(axis=1), axis=0)
    return np.exp(ratios.median(axis=0))


def design_matrix(samples: pd.DataFrame, covariates: list[str]) -> np.ndarray:
    """Intercept + covariate dummies + condition (defeated = 1), last column."""
    cols = [np.ones(len(samples))]
    for cov in covariates:
        levels = sorted(samples[cov].unique())
        for lev in levels[1:]:
            cols.append((samples[cov] == lev).to_numpy(float))
    cols.append((samples["condition"] == "defeated").to_numpy(float))
    X = np.column_stack(cols)
    if np.linalg.matrix_rank(X) < X.shape[1]:
        raise ValueError("design matrix is rank deficient")
    return X


def trigamma_inverse(x: float) -> float:
    """Solve trigamma(y) = x by Newton iteration (limma's algorithm)."""
    y = 0.5 + 1.0 / x
    for _ in range(50):
        tri = special.polygamma(1, y)
        dif = tri * (1.0 - tri / x) / special.polygamma(2, y)
        y += dif
        if -dif / y < 1e-8:
            break
    return float(y)


def fit_prior(s2: np.ndarray, d: float) -> tuple[float, float]:
    """Moment estimate of prior df d0 and prior variance s0^2."""
    s2 = np.maximum(s2, 1e-12)
    e = np.log(s2) - special.digamma(d / 2) + np.log(d / 2)
    emean = e.mean()
    evar = e.var(ddof=1) - special.polygamma(1, d / 2)
    if evar <= 0:
        return np.inf, float(np.exp(emean))
    d0 = 2 * trigamma_inverse(evar)
    s0sq = np.exp(emean + special.digamma(d0 / 2) - np.log(d0 / 2))
    return float(d0), float(s0sq)


def moderated_t(logexpr: np.ndarray, X: np.ndarray) -> dict[str, np.ndarray]:
    """Moderated t for the last design column, for every gene (rows)."""
    n, p = X.shape
    d = n - p
    if d < 1:
        raise ValueError("no residual degrees of freedom")
    xtx_inv = np.linalg.inv(X.T @ X)
    beta = logexpr @ X @ xtx_inv
    resid = logexpr - beta @ X.T
    s2 = (resid ** 2).sum(axis=1) / d
    d0, s0sq = fit_prior(s2, d)
    if np.isinf(d0):
        post = np.full_like(s2, s0sq)
        df_tot = np.inf
    else:
        post = (d0 * s0sq + d * s2) / (d0 + d)
        df_tot = d0 + d
    se = np.sqrt(post * xtx_inv[-1, -1])
    t = beta[:, -1] / se
    df_eff = df_tot if np.isfinite(df_tot) else 1e6
    p_up = stats.t.sf(t, df_eff)
    return {"logfc": beta[:, -1], "t": t, "p_up": p_up,
            "p_two": 2 * np.minimum(p_up, 1 - p_up), "d0": d0, "df": df_eff}
