"""Noise-floor statistics on synthetic series with known spread (project 02 Tier B)."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gm02 import noise  # noqa: E402


def test_pooled_cv_removes_study_offset_and_ci_brackets():
    rng = np.random.default_rng(0)
    x = np.concatenate([rng.normal(1000, 10, 3000), rng.normal(1100, 10, 3000)])
    g = np.repeat([1, 2], 3000)
    r = noise.pooled_within_cv(x, g)
    assert abs(r["cv"] - 100 * 10 / 1050) < 0.03
    assert r["cv_lo"] < r["cv"] < r["cv_hi"]
    assert noise.cv_pct(x) > 4 * r["cv"]


def test_typical_error_matches_white_noise_sd():
    rng = np.random.default_rng(1)
    x = rng.normal(500, 5, 4000)
    s = noise.summarize(x, np.repeat([1, 2], 2000), np.tile(np.arange(2000), 2))
    assert abs(s["typical_error_pct"] - 1.0) < 0.05
    assert abs(s["te_over_within_sd"] - 1.0) < 0.05
    assert all(abs(a) < 0.06 for a in s["lag1_autocorr_by_study"])


def test_consecutive_diffs_skip_gaps():
    d = noise.consecutive_diffs([1.0, 2.0, 4.0, 8.0], [1, 2, 4, 5])
    assert list(d) == [1.0, 4.0]


def test_welch_offset_percent():
    x = np.array([100, 102, 98, 100, 110, 112, 108, 110.0])
    r = noise.welch_offset_pct(x, np.array([1, 1, 1, 1, 2, 2, 2, 2]))
    assert abs(r["offset_pct"] - 10.0) < 1e-9
    assert r["lo"] < 10 < r["hi"]
