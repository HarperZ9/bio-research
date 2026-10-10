"""Site-level statistics: limma-style moderated t, Hedges g, exact permutations.

Rows are sites, columns are samples; NaN marks a missing value. `groups` is a
boolean vector, True for the stress (or treated) group.
"""
from __future__ import annotations

from itertools import combinations

import numpy as np
from scipy import special


def trigamma_inverse(x: np.ndarray | float) -> np.ndarray:
    """Solve trigamma(y) = x by Newton iteration (Smyth 2004, limma)."""
    x = np.atleast_1d(np.asarray(x, dtype=float))
    y = 0.5 + 1.0 / x
    for _ in range(50):
        tri = special.polygamma(1, y)
        dif = tri * (1 - tri / x) / special.polygamma(2, y)
        y = y + dif
        if np.all(-dif / y < 1e-8):
            break
    return y


def fit_f_dist(s2: np.ndarray, df: np.ndarray) -> tuple[float, float]:
    """Method-of-moments prior (d0, s0^2) for residual variances."""
    ok = (df > 0) & np.isfinite(s2) & (s2 > 0)
    s2, df = s2[ok], df[ok]
    n = s2.size
    e = np.log(s2) - special.digamma(df / 2) + np.log(df / 2)
    emean = e.mean()
    evar = np.sum((e - emean) ** 2) / (n - 1) - np.mean(special.polygamma(1, df / 2))
    if evar > 0:
        d0 = float(2 * trigamma_inverse(evar)[0])
        s0sq = float(np.exp(emean + special.digamma(d0 / 2) - np.log(d0 / 2)))
    else:
        d0, s0sq = np.inf, float(np.exp(emean))
    return d0, s0sq


def group_moments(y: np.ndarray, groups: np.ndarray) -> dict:
    """Per-site group means, counts, pooled variance and residual df."""
    a, b = y[:, groups], y[:, ~groups]
    na, nb = np.sum(~np.isnan(a), 1), np.sum(~np.isnan(b), 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        ma, mb = np.nanmean(a, 1), np.nanmean(b, 1)
        ss = np.nansum((a - ma[:, None]) ** 2, 1) + np.nansum((b - mb[:, None]) ** 2, 1)
        df = (na + nb - 2).astype(float)
        s2 = np.where(df > 0, ss / np.where(df > 0, df, 1), np.nan)
    return {"ma": ma, "mb": mb, "na": na, "nb": nb, "s2": s2, "df": df}


def moderated_t(y: np.ndarray, groups: np.ndarray, prior=None) -> dict:
    """Moderated t for stress minus control; sites need >= 2 values per group."""
    m = group_moments(y, groups)
    valid = (m["na"] >= 2) & (m["nb"] >= 2)
    d0, s0sq = prior if prior is not None else fit_f_dist(m["s2"][valid], m["df"][valid])
    df = m["df"]
    if np.isinf(d0):
        post = np.full_like(m["s2"], s0sq)
    else:
        post = (d0 * s0sq + df * m["s2"]) / (d0 + df)
    lfc = m["ma"] - m["mb"]
    with np.errstate(invalid="ignore", divide="ignore"):
        t = lfc / np.sqrt(post * (1 / m["na"] + 1 / m["nb"]))
    t = np.where(valid, t, np.nan)
    p_up = special.stdtr(df + d0, -t) if np.isfinite(d0) else special.ndtr(-t)
    return {"t": t, "lfc": np.where(valid, lfc, np.nan), "p_up": p_up,
            "valid": valid, "d0": d0, "s0sq": s0sq}


def hedges_g(y: np.ndarray, groups: np.ndarray) -> np.ndarray:
    """Hedges g per site (pooled SD, small-sample correction)."""
    m = group_moments(y, groups)
    n = m["na"] + m["nb"]
    with np.errstate(invalid="ignore", divide="ignore"):
        d = (m["ma"] - m["mb"]) / np.sqrt(m["s2"])
        return d * (1 - 3 / (4 * n - 9))


def labelings(n: int, k: int, max_n: int = 5000, seed: int = 7) -> list[np.ndarray]:
    """All boolean labelings with k True of n, or max_n random ones (first = none)."""
    total = special.comb(n, k, exact=True)
    if total <= max_n:
        out = []
        for idx in combinations(range(n), k):
            g = np.zeros(n, bool)
            g[list(idx)] = True
            out.append(g)
        return out
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(max_n):
        g = np.zeros(n, bool)
        g[rng.choice(n, k, replace=False)] = True
        out.append(g)
    return out


def permutation_p_up(stat_fn, y: np.ndarray, groups: np.ndarray,
                     max_n: int = 5000, seed: int = 7) -> tuple[float, float, int]:
    """One-sided (UP) and two-sided permutation p for a scalar statistic.

    stat_fn(y, groups) -> float. The observed labeling is included in the
    reference set when all labelings are enumerated; with random labelings the
    observed value is added once.
    """
    obs = stat_fn(y, groups)
    labs = labelings(y.shape[1], int(groups.sum()), max_n, seed)
    exact = special.comb(y.shape[1], int(groups.sum()), exact=True) <= max_n
    ref = np.array([stat_fn(y, g) for g in labs])
    if not exact:
        ref = np.append(ref, obs)
    ref = ref[np.isfinite(ref)]
    tol = 1e-12
    p_up = float(np.mean(ref >= obs - tol))
    p_two = float(np.mean(np.abs(ref) >= abs(obs) - tol))
    return p_up, p_two, int(ref.size)
