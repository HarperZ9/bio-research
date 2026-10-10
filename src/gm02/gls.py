"""Generalized least squares with AR(1) errors inside blocks (no cross-block correlation).

Two rows in the same block correlate as rho ** |t_i - t_j|, where t is the day
index, so gaps from dropped days are handled. rho is chosen by maximum profile
likelihood over a grid, then refined with a bounded scalar search.
"""
from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from scipy import optimize, stats

DEFAULT_GRID = np.linspace(-0.95, 0.95, 39)


@dataclass
class GLSResult:
    beta: np.ndarray
    se: np.ndarray
    t: np.ndarray
    rho: float
    sigma2: float
    df: int
    names: tuple

    def ci(self, level=0.95):
        q = stats.t.ppf(0.5 + level / 2, self.df)
        return self.beta - q * self.se, self.beta + q * self.se

    def p(self):
        return 2 * stats.t.sf(np.abs(self.t), self.df)


@lru_cache(maxsize=8192)
def _whitener(blocks, times, rho):
    """Return (W, logdet_V) with W V W' = I for the block AR(1) covariance."""
    b = np.asarray(blocks)
    t = np.asarray(times, dtype=float)
    lag = np.abs(t[:, None] - t[None, :])
    same = b[:, None] == b[None, :]
    V = np.where(same, np.sign(rho) ** lag * np.abs(rho) ** lag, 0.0)
    V[np.diag_indices_from(V)] = 1.0
    L = np.linalg.cholesky(V)
    return np.linalg.inv(L), 2.0 * float(np.log(np.diag(L)).sum())


def _profile(y, X, blocks, times, rho):
    W, logdet = _whitener(blocks, times, float(rho))
    ys, Xs = W @ y, W @ X
    beta, *_ = np.linalg.lstsq(Xs, ys, rcond=None)
    rss = float(((ys - Xs @ beta) ** 2).sum())
    n = len(y)
    loglik = -0.5 * n * np.log(rss / n) - 0.5 * logdet
    return loglik, beta, rss, Xs


def _best_rho(y, X, blocks, times, grid, refine):
    lls = [_profile(y, X, blocks, times, r)[0] for r in grid]
    best = float(grid[int(np.argmax(lls))])
    if not refine:
        return best
    step = float(grid[1] - grid[0])
    lo, hi = max(-0.95, best - step), min(0.95, best + step)
    res = optimize.minimize_scalar(
        lambda r: -_profile(y, X, blocks, times, round(r, 4))[0],
        bounds=(lo, hi), method="bounded", options={"xatol": 1e-3})
    return round(float(res.x), 4)


def fit(y, X, blocks, times, names=None, grid=DEFAULT_GRID, refine=True):
    """Fit y = X beta + e with block AR(1) errors; return a GLSResult."""
    y = np.asarray(y, float)
    X = np.asarray(X, float)
    blocks = tuple(np.asarray(blocks).tolist())
    times = tuple(float(v) for v in np.asarray(times))
    rho = _best_rho(y, X, blocks, times, grid, refine)
    _, beta, rss, Xs = _profile(y, X, blocks, times, rho)
    n, k = X.shape
    df = n - k
    sigma2 = rss / df
    se = np.sqrt(np.diag(sigma2 * np.linalg.inv(Xs.T @ Xs)))
    names = tuple(names) if names is not None else tuple(f"x{i}" for i in range(k))
    return GLSResult(beta, se, beta / se, rho, sigma2, df, names)
