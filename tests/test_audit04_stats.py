"""Checks for the audit 04 statistics against hand-computed values."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "audit04"))

from stats import cohen_kappa, wilson  # noqa: E402
from sample import allocate  # noqa: E402


def test_wilson_matches_reference_values():
    lo, hi = wilson(5, 10)
    assert abs(lo - 0.2366) < 1e-4 and abs(hi - 0.7634) < 1e-4
    lo, hi = wilson(0, 10)
    assert lo == 0.0 and abs(hi - 0.2775) < 1e-4


def test_kappa_perfect_and_chance():
    assert cohen_kappa(list("aabb"), list("aabb"))[0] == 1.0
    assert cohen_kappa(list("abab"), list("aabb"))[0] == 0.0


def test_kappa_textbook_example():
    # 2x2 table a=20,b=5,c=10,d=15: po=0.7, pe=0.5, kappa=0.4
    a = ["y"] * 25 + ["n"] * 25
    b = ["y"] * 20 + ["n"] * 5 + ["y"] * 10 + ["n"] * 15
    k, po = cohen_kappa(a, b)
    assert abs(po - 0.7) < 1e-9 and abs(k - 0.4) < 1e-9


def test_allocate_sums_to_n_and_respects_small_frames():
    alloc = allocate({"x": 144, "y": 70, "z": 66, "w": 48, "u": 6}, 100)
    assert sum(alloc.values()) == 100
    assert allocate({"x": 3, "y": 4}, 100) == {"x": 3, "y": 4}
