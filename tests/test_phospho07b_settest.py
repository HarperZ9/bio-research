"""Synthetic-data checks for the 07b set tests and controls."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from phospho07b.settest import (  # noqa: E402
    matched_independent_sets, matched_single_protein_sets, percentile, rotation_test,
    set_score_ci, set_stat)
from phospho07b.stats import moderated_t, permutation_p_up  # noqa: E402

G33 = np.array([True, True, True, False, False, False])


def _null(n_sites=600, seed=0):
    rng = np.random.default_rng(seed)
    return rng.normal(size=(n_sites, 6)) * 0.3 + rng.normal(20, 2, size=(n_sites, 1))


def _correlated_block(y, rows, seed):
    """Add a shared per-sample factor to rows: co-regulated, no group effect."""
    rng = np.random.default_rng(seed)
    y[rows] += rng.normal(size=6) * 0.6
    return y


def test_planted_effect_recovered():
    y = _null(seed=4)
    idx = np.arange(6)
    y[np.ix_(idx, np.flatnonzero(G33))] += 1.5
    p_up, _, n = permutation_p_up(lambda m, g: set_stat(m, g, idx), y, G33)
    assert n == 20 and p_up == 1 / 20
    prior = moderated_t(y, G33)
    rot = rotation_test(y, G33, idx, (prior["d0"], prior["s0sq"]), n_rot=1999)
    assert rot["p_up"] < 0.01
    ci = set_score_ci(y, G33, idx)
    assert ci["lo"] > 0.5 and ci["lo"] < 1.5 < ci["hi"] + 0.5


def test_rotation_observed_matches_moderated_t():
    y = _null(seed=5)
    idx = np.arange(10, 20)
    res = moderated_t(y, G33)
    rot = rotation_test(y, G33, idx, (res["d0"], res["s0sq"]), n_rot=99)
    assert abs(rot["stat"] - np.mean(res["t"][idx])) < 1e-9


def test_negative_control_rotation_calibrated_on_correlated_null_sets():
    calls = 0
    for s in range(100):
        y = _null(n_sites=300, seed=100 + s)
        idx = np.arange(8)
        y = _correlated_block(y, idx, seed=500 + s)
        res = moderated_t(y, G33)
        rot = rotation_test(y, G33, idx, (res["d0"], res["s0sq"]), n_rot=499, seed=s)
        calls += rot["p_two"] < 0.05
    assert calls <= 12  # 5 expected; binomial upper tail margin


def test_independent_random_sets_overcall_correlated_null_sets():
    """The F-07-1 lesson: an independence-assuming test overcalls co-regulated sets."""
    calls = 0
    for s in range(60):
        y = _null(n_sites=300, seed=200 + s)
        idx = np.arange(8)
        y = _correlated_block(y, idx, seed=700 + s)
        t = moderated_t(y, G33)["t"]
        inten = np.nanmean(y, 1)
        sets = matched_independent_sets(inten, np.isfinite(t), idx, n_sets=300, seed=s)
        ref = np.array([np.nanmean(t[r]) for r in sets])
        pc = percentile(np.nanmean(t[idx]), ref)
        calls += pc < 2.5 or pc > 97.5
    assert calls > 6  # well above the 5% (3 of 60) a calibrated test would give


def test_single_protein_sets_match_size_protein_and_intensity():
    rng = np.random.default_rng(8)
    prots = np.repeat(np.arange(100), 5).astype(str)
    inten = rng.normal(20, 2, 500)
    sets = matched_single_protein_sets(prots, inten, np.ones(500, bool), 3, 20.0,
                                       n_sets=200, exclude={"0"})
    assert len(sets) == 200
    tol = 0.5 * np.std(inten)
    for s in sets:
        assert len(s) == 3 and len(set(prots[s])) == 1 and prots[s[0]] != "0"
        assert abs(inten[s].mean() - 20.0) <= tol + 1e-12


def test_percentile_ties_and_extremes():
    ref = np.array([1.0, 2.0, 3.0, 4.0])
    assert percentile(5.0, ref) == 100.0
    assert percentile(0.0, ref) == 0.0
    assert percentile(2.0, ref) == 37.5
