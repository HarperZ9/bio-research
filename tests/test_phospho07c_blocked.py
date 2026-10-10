"""Synthetic-data checks for the 07c sex-blocked statistics."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from phospho07b.blocked import (  # noqa: E402
    blocked_set_score_ci, blocked_set_stat, blocked_t, cell_valid, design, lm_moderated_t,
    stratified_labelings, stratified_perm_p)
from phospho07b.settest import rotation_test_design  # noqa: E402
from phospho07b.stats import moderated_t  # noqa: E402

# 18 samples: 9 per sex; within each sex 3 control, 6 stress (the PXD057176 layout)
SEX = np.array([False] * 9 + [True] * 9)
STRESS = np.array(([False] * 3 + [True] * 6) * 2)


def _null(n_sites=500, seed=0, n=18):
    rng = np.random.default_rng(seed)
    return rng.normal(size=(n_sites, n)) * 0.3 + rng.normal(20, 2, size=(n_sites, 1))


def test_design_reduces_to_two_group_moderated_t():
    g = np.array([True] * 3 + [False] * 3)
    y = _null(seed=1, n=6)
    y[5, 0] = np.nan
    y[9, 4] = np.nan
    x = np.column_stack([np.ones(6), g.astype(float)])
    ref = moderated_t(y, g)
    got = lm_moderated_t(y, x, ref["valid"])
    assert np.allclose(got["t"][ref["valid"]], ref["t"][ref["valid"]])
    assert abs(got["d0"] - ref["d0"]) < 1e-9 if np.isfinite(ref["d0"]) else np.isinf(got["d0"])


def test_sex_effect_is_blocked_out():
    y = _null(seed=2)
    y[:, SEX] += 3.0  # large sex difference, no stress effect
    t = blocked_t(y, SEX, STRESS)["t"]
    assert abs(np.nanmean(t)) < 0.2
    assert np.mean(np.abs(t) > 3) < 0.02


def test_planted_stress_effect_recovered():
    y = _null(seed=3)
    idx = np.arange(6)
    y[np.ix_(idx, np.flatnonzero(STRESS))] += 1.0
    y[:, SEX] += 2.0
    bt = blocked_t(y, SEX, STRESS)
    assert np.allclose(bt["lfc"][idx], 1.0, atol=0.4)
    perm = stratified_perm_p(lambda m, s, g: blocked_set_stat(m, s, g, idx), y, SEX, STRESS, n=199)
    assert perm["p_up"] <= 0.01 and perm["n"] == 200
    ci = blocked_set_score_ci(y, SEX, STRESS, idx)
    # site-centred set score of a uniform planted shift equals the shift
    assert ci["lo"] < 1.0 < ci["hi"] and ci["lo"] > 0.5 and ci["df"] == 15


def test_cell_validity_needs_two_per_cell():
    y = _null(n_sites=3, seed=4)
    y[0, [0, 1]] = np.nan  # female control cell left with 1 value
    y[1, [0]] = np.nan  # 2 left: still valid
    assert cell_valid(y, SEX, STRESS).tolist() == [False, True, True]


def test_stratified_labelings_keep_counts_within_sex():
    for g in stratified_labelings(SEX, STRESS, n=50, seed=1):
        assert g[~SEX].sum() == 6 and g[SEX].sum() == 6


def test_rotation_design_observed_matches_blocked_t():
    y = _null(seed=5)
    idx = np.arange(10, 20)
    bt = blocked_t(y, SEX, STRESS)
    rot = rotation_test_design(y, design(SEX, STRESS), idx, (bt["d0"], bt["s0sq"]), n_rot=99)
    assert abs(rot["stat"] - np.mean(bt["t"][idx])) < 1e-9
    assert abs(rot["p_up"] + rot["p_down"] - 1) < 0.05


def test_rotation_design_calibrated_on_correlated_null_sets():
    calls = 0
    for s in range(100):
        y = _null(n_sites=300, seed=100 + s)
        idx = np.arange(8)
        rng = np.random.default_rng(500 + s)
        y[idx] += rng.normal(size=18) * 0.6  # co-regulated, no stress effect
        y[:, SEX] += 1.5
        bt = blocked_t(y, SEX, STRESS)
        rot = rotation_test_design(y, design(SEX, STRESS), idx, (bt["d0"], bt["s0sq"]),
                                   n_rot=499, seed=s)
        calls += rot["p_two"] < 0.05
    assert calls <= 12  # 5 expected; binomial upper tail margin
