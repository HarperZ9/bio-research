"""Synthetic-data checks for the 07b site-level statistics."""
import sys
from pathlib import Path

import numpy as np
from scipy import special, stats as sps

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from phospho07b.stats import (  # noqa: E402
    fit_f_dist, hedges_g, labelings, moderated_t, permutation_p_up, trigamma_inverse)

G33 = np.array([True, True, True, False, False, False])


def test_trigamma_inverse_round_trip():
    for y in (0.3, 1.0, 5.0, 40.0):
        x = special.polygamma(1, y)
        assert abs(trigamma_inverse(x)[0] - y) / y < 1e-6


def test_fit_f_dist_recovers_prior():
    rng = np.random.default_rng(1)
    d0, s0sq, df = 4.0, 0.5, 4
    sigma2 = s0sq * d0 / rng.chisquare(d0, 20000)
    s2 = sigma2 * rng.chisquare(df, 20000) / df
    est_d0, est_s0 = fit_f_dist(s2, np.full(20000, float(df)))
    assert abs(est_d0 - d0) / d0 < 0.2
    assert abs(est_s0 - s0sq) / s0sq < 0.1


def test_zero_prior_df_gives_student_t():
    rng = np.random.default_rng(2)
    y = rng.normal(size=(5, 6))
    res = moderated_t(y, G33, prior=(0.0, 1.0))
    ref = sps.ttest_ind(y[:, G33], y[:, ~G33], axis=1).statistic
    assert np.allclose(res["t"], ref)


def test_sites_with_too_few_values_are_excluded():
    y = np.ones((2, 6)) + np.arange(6) * 0.1
    y[1, :2] = np.nan  # only one value left in the stress group
    res = moderated_t(y, G33, prior=(3.0, 0.1))
    assert np.isfinite(res["t"][0]) and np.isnan(res["t"][1])
    assert not res["valid"][1]


def test_labelings_exact_counts():
    assert len(labelings(6, 3)) == 20
    assert len(labelings(8, 4)) == 70
    assert len(labelings(30, 15, max_n=100)) == 100


def test_permutation_p_exact_for_3_vs_3():
    rng = np.random.default_rng(3)
    y = rng.normal(size=(1, 6))
    y[0, G33] += 10.0  # perfect separation

    def mean_diff(m, g):
        return float(m[0, g].mean() - m[0, ~g].mean())

    p_up, p_two, n = permutation_p_up(mean_diff, y, G33)
    assert n == 20
    assert p_up == 1 / 20  # minimum attainable one-sided p
    assert p_two == 2 / 20  # minimum attainable two-sided p


def test_hedges_g_sign_and_size():
    y = np.array([[2.0, 2.1, 1.9, 0.0, 0.1, -0.1]])
    g = hedges_g(y, G33)[0]
    assert g > 10  # 2 units apart with SD 0.1, corrected down by 1 - 3/15
