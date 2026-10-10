"""Set-level tests: mean moderated t, rotation test, matched random site sets."""
from __future__ import annotations

import numpy as np
from scipy import stats as sps

from .stats import moderated_t


def set_stat(y: np.ndarray, groups: np.ndarray, idx: np.ndarray) -> float:
    """Mean moderated t over the set rows idx (prior refitted on all rows)."""
    t = moderated_t(y, groups)["t"][idx]
    return float(np.nanmean(t)) if np.any(np.isfinite(t)) else np.nan


def _effects(y: np.ndarray, groups: np.ndarray) -> tuple[np.ndarray, float]:
    """Rotate-able effects (rows x n-1) from a QR of [1, group]; and the sign."""
    n = y.shape[1]
    x = np.column_stack([np.ones(n), groups.astype(float)])
    q, r = np.linalg.qr(x, mode="complete")
    eff = y @ q  # rows x n
    sign = np.sign(r[1, 1])
    return eff[:, 1:], float(sign)


def rotation_test(y: np.ndarray, groups: np.ndarray, idx: np.ndarray, prior,
                  n_rot: int = 9999, seed: int = 7) -> dict:
    """ROAST-style one-sided (UP) and two-sided p for the mean moderated t.

    Uses complete-case rows of the set only. prior = (d0, s0sq) fixed.
    """
    sub = y[idx]
    sub = sub[~np.isnan(sub).any(1)]
    if sub.shape[0] == 0:
        return {"p_up": np.nan, "p_two": np.nan, "n_sites": 0, "stat": np.nan}
    n = y.shape[1]
    v, sign = _effects(sub, groups)
    norm2 = np.sum(v ** 2, 1)
    d = n - 2
    d0, s0sq = prior

    def stat(e1):
        s2 = (norm2 - e1 ** 2) / d
        post = s0sq if np.isinf(d0) else (d0 * s0sq + d * s2) / (d0 + d)
        # t = beta / se; beta = e1 / r11 and se = sqrt(post) / |r11|
        return np.mean(sign * e1 / np.sqrt(post))

    obs = stat(v[:, 0])
    rng = np.random.default_rng(seed)
    r = rng.standard_normal((n_rot, v.shape[1]))
    r /= np.linalg.norm(r, axis=1, keepdims=True)
    rot = np.array([stat(v @ ri) for ri in r])
    return {"p_up": (np.sum(rot >= obs) + 1) / (n_rot + 1),
            "p_two": (np.sum(np.abs(rot) >= abs(obs)) + 1) / (n_rot + 1),
            "n_sites": int(sub.shape[0]), "stat": float(obs)}


def set_score_ci(y: np.ndarray, groups: np.ndarray, idx: np.ndarray) -> dict:
    """Per-sample set score (site-centred mean) and Welch 95% CI of the difference."""
    sub = y[idx]
    centred = sub - np.nanmean(sub, 1, keepdims=True)
    score = np.nanmean(centred, 0)
    a, b = score[groups], score[~groups]
    a, b = a[np.isfinite(a)], b[np.isfinite(b)]
    diff = a.mean() - b.mean()
    va, vb = a.var(ddof=1) / a.size, b.var(ddof=1) / b.size
    se = np.sqrt(va + vb)
    dfw = (va + vb) ** 2 / (va ** 2 / (a.size - 1) + vb ** 2 / (b.size - 1))
    h = sps.t.ppf(0.975, dfw) * se
    return {"diff": float(diff), "lo": float(diff - h), "hi": float(diff + h),
            "df": float(dfw), "scores": score.tolist()}


def matched_single_protein_sets(proteins: np.ndarray, intensity: np.ndarray,
                                eligible: np.ndarray, k: int, target_mean: float,
                                n_sets: int = 1000, max_draws: int = 200000,
                                exclude=(), seed: int = 7) -> list[np.ndarray]:
    """Random k-site sets from one protein each, matched on mean intensity."""
    rng = np.random.default_rng(seed)
    tol = 0.5 * np.nanstd(intensity[eligible])
    by_prot: dict = {}
    for i in np.flatnonzero(eligible):
        if proteins[i] not in exclude:
            by_prot.setdefault(proteins[i], []).append(i)
    pool = [np.array(v) for v in by_prot.values() if len(v) >= k]
    out = []
    for _ in range(max_draws):
        if len(out) >= n_sets or not pool:
            break
        rows = pool[rng.integers(len(pool))]
        pick = rng.choice(rows, k, replace=False)
        if abs(np.nanmean(intensity[pick]) - target_mean) <= tol:
            out.append(pick)
    return out


def matched_independent_sets(intensity: np.ndarray, eligible: np.ndarray, idx: np.ndarray,
                             n_sets: int = 1000, n_bins: int = 20, seed: int = 7) -> list[np.ndarray]:
    """F-07-1 style random sets: sites drawn independently within intensity bins."""
    rng = np.random.default_rng(seed)
    elig = np.flatnonzero(eligible)
    edges = np.quantile(intensity[elig], np.linspace(0, 1, n_bins + 1))
    bins = np.clip(np.searchsorted(edges, intensity, side="right") - 1, 0, n_bins - 1)
    members = {b: elig[bins[elig] == b] for b in range(n_bins)}
    need = bins[idx]
    return [np.array([rng.choice(members[b]) for b in need]) for _ in range(n_sets)]


def percentile(obs: float, ref: np.ndarray) -> float:
    """Percent of reference values strictly below obs, plus half the ties."""
    ref = ref[np.isfinite(ref)]
    return float(100 * (np.sum(ref < obs) + 0.5 * np.sum(ref == obs)) / ref.size)
