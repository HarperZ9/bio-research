"""Synthetic-data checks for the block AR(1) GLS fit (project 02 Tier B)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gm02 import gls  # noqa: E402


def ar1(n, rho, rng, sd=1.0):
    e = np.empty(n)
    e[0] = rng.normal(0, sd / np.sqrt(1 - rho ** 2))
    for i in range(1, n):
        e[i] = rho * e[i - 1] + rng.normal(0, sd)
    return e


def two_studies(rng, beta, rho, n=30):
    x = rng.normal(size=2 * n)
    e = np.concatenate([ar1(n, rho, rng), ar1(n, rho, rng)])
    blocks = np.repeat([1, 2], n)
    times = np.tile(np.arange(1, n + 1), 2)
    X = np.column_stack([np.ones(2 * n), x, (blocks == 2).astype(float)])
    y = X @ np.array([0.0, beta, 0.5]) + e
    return y, X, blocks, times


def test_whitener_inverts_covariance():
    W, _ = gls._whitener((1, 1, 1, 2, 2), (1.0, 2.0, 4.0, 1.0, 2.0), 0.6)
    t = np.array([1, 2, 4, 1, 2.0])
    b = np.array([1, 1, 1, 2, 2])
    V = np.where(b[:, None] == b[None, :], 0.6 ** np.abs(t[:, None] - t[None, :]), 0)
    assert np.allclose(W @ V @ W.T, np.eye(5), atol=1e-10)


def test_recovers_planted_effect_and_rho():
    rng = np.random.default_rng(1)
    betas, rhos, covered = [], [], 0
    for _ in range(200):
        y, X, b, t = two_studies(rng, beta=0.6, rho=0.6)
        r = gls.fit(y, X, b, t, refine=False)
        betas.append(r.beta[1])
        rhos.append(r.rho)
        lo, hi = r.ci()
        covered += lo[1] <= 0.6 <= hi[1]
    assert abs(np.mean(betas) - 0.6) < 0.03
    assert 0.45 < np.mean(rhos) < 0.65  # ML rho is biased slightly low at n = 30
    assert 0.90 <= covered / 200 <= 0.99


def test_planted_effect_is_detected_and_null_is_not():
    rng = np.random.default_rng(2)
    y, X, b, t = two_studies(rng, beta=1.0, rho=0.5)
    assert gls.fit(y, X, b, t).p()[1] < 0.001
    y, X, b, t = two_studies(rng, beta=0.0, rho=0.5)
    assert gls.fit(y, X, b, t).p()[1] > 0.001


def test_gls_beats_ols_on_autocorrelated_errors():
    """Under strong AR(1) errors, GLS slope estimates vary less than OLS ones."""
    rng = np.random.default_rng(3)
    g, o = [], []
    for _ in range(150):
        n = 30
        x = np.concatenate([ar1(n, 0.8, rng), ar1(n, 0.8, rng)])
        e = np.concatenate([ar1(n, 0.8, rng), ar1(n, 0.8, rng)])
        X = np.column_stack([np.ones(2 * n), x])
        y = 0.3 * x + e
        g.append(gls.fit(y, X, np.repeat([1, 2], n), np.tile(np.arange(n), 2), refine=False).beta[1])
        o.append(np.linalg.lstsq(X, y, rcond=None)[0][1])
    assert np.std(g) < np.std(o)
