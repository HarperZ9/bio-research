"""Block permutation of a daily exposure series, refitting the block-AR(1) GLS model."""
import numpy as np

from . import gls


def block_shuffle(series, block_len, rng):
    """Shuffle contiguous blocks of a 1-D array; a short final block stays a block."""
    series = np.asarray(series)
    blocks = [series[s:s + block_len] for s in range(0, len(series), block_len)]
    order = rng.permutation(len(blocks))
    return np.concatenate([blocks[i] for i in order])


def lag1(daily):
    """Previous-day value within one study series (NaN on day 1)."""
    daily = np.asarray(daily, float)
    out = np.full(len(daily), np.nan)
    out[1:] = daily[:-1]
    return out


def lags_from_daily(daily_by_study):
    """Concatenate lag-0 and lag-1 series across studies (lag never crosses studies)."""
    lag0 = np.concatenate([np.asarray(d, float) for d in daily_by_study])
    lag_1 = np.concatenate([lag1(d) for d in daily_by_study])
    return lag0, lag_1


def permutation_test(daily_by_study, build, coef_idx, n_perm, seed,
                     block_len=5, grid=gls.DEFAULT_GRID, refine=True):
    """Two-sided block-permutation p-values for the coefficients in coef_idx.

    daily_by_study: list of 1-D arrays, one value per study day (NaN = unavailable).
    build(lag0, lag1) -> (y, X, blocks, times), rows already filtered.
    Returns (observed GLSResult, p array, permutation t matrix).
    """
    rng = np.random.default_rng(seed)
    obs = gls.fit(*build(*lags_from_daily(daily_by_study)), grid=grid, refine=refine)
    t_obs = np.abs(obs.t[coef_idx])
    t_perm = np.empty((n_perm, len(coef_idx)))
    for i in range(n_perm):
        shuffled = [block_shuffle(d, block_len, rng) for d in daily_by_study]
        res = gls.fit(*build(*lags_from_daily(shuffled)), grid=grid, refine=refine)
        t_perm[i] = res.t[coef_idx]
    p = (1 + (np.abs(t_perm) >= t_obs).sum(axis=0)) / (n_perm + 1)
    return obs, p, t_perm
