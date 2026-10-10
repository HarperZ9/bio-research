"""Block permutation checks on autocorrelated synthetic data (project 02 Tier B)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gm02 import perm  # noqa: E402
from test_gm02_gls import ar1  # noqa: E402

N = 30
COARSE = np.linspace(-0.9, 0.9, 10)


def make_build(y_by_study):
    y_all = np.concatenate(y_by_study)
    blocks = np.repeat([1, 2], N)
    times = np.tile(np.arange(1, N + 1), 2)

    def build(lag0, lag_1):
        keep = ~np.isnan(lag_1)
        X = np.column_stack([np.ones(keep.sum()), lag0[keep], lag_1[keep],
                             (blocks[keep] == 2).astype(float)])
        return y_all[keep], X, blocks[keep], times[keep]
    return build


def test_block_shuffle_keeps_blocks_intact():
    rng = np.random.default_rng(0)
    s = np.arange(30)
    out = perm.block_shuffle(s, 5, rng)
    assert sorted(out) == list(s)
    chunks = out.reshape(6, 5)
    assert all((np.diff(c) == 1).all() for c in chunks)


def test_lag1_never_crosses_studies():
    lag0, lag_1 = perm.lags_from_daily([np.arange(3.0), np.arange(10.0, 13.0)])
    assert np.isnan(lag_1[0]) and np.isnan(lag_1[3])
    assert lag_1[4] == 10.0 and lag_1[1] == 0.0


def test_error_rate_on_autocorrelated_null():
    """X and Y both AR(1) with rho 0.7, independent: rejections near nominal."""
    rng = np.random.default_rng(20261009)
    n_sim, rejections = 120, 0
    for i in range(n_sim):
        x = [ar1(N, 0.7, rng), ar1(N, 0.7, rng)]
        y = [ar1(N, 0.7, rng), ar1(N, 0.7, rng)]
        _, p, _ = perm.permutation_test(x, make_build(y), [1], n_perm=59,
                                        seed=i, grid=COARSE, refine=False)
        rejections += p[0] < 0.05
    rate = rejections / n_sim
    assert rate <= 0.10, rate  # binomial 95% upper bound for 0.05 at n = 120 is about 0.09


def test_planted_lag0_effect_is_detected():
    rng = np.random.default_rng(5)
    x = [ar1(N, 0.5, rng), ar1(N, 0.5, rng)]
    y = [1.0 * x[k] + ar1(N, 0.5, rng, sd=0.6) for k in range(2)]
    obs, p, _ = perm.permutation_test(x, make_build(y), [1, 2], n_perm=199,
                                      seed=1, grid=COARSE, refine=False)
    assert p[0] <= 0.01
    assert obs.beta[1] > 0.6
