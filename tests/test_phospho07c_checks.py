"""Synthetic checks for 07c decoding, label check, reproduction, decision and loader."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from phospho07b.hippo import RUNS  # noqa: E402
from phospho07b.hippo_checks import (  # noqa: E402
    combine_07b, decide_07c, decode_runs, reproduction, sex_label_check, y_specific_windows)
from phospho07b.loaders import load_spectronaut_ptm_sites  # noqa: E402

LAB = decode_runs(RUNS)
TAU_NULL = {"rot_p_up": 0.4, "rot_p_down": 0.6, "single_protein_pct": 50.0,
            "perm_p_up": 0.4, "perm_p_down": 0.6}
TAU_UP = {"rot_p_up": 0.01, "rot_p_down": 0.99, "single_protein_pct": 97.0,
          "perm_p_up": 0.01, "perm_p_down": 0.99}
RIBO_OK = {"rot_p_two": 0.5, "independent_pct": 50.0}
CAL_OK = {"pass": True}


def test_decode_runs_layout():
    assert (LAB["prefix"] == "C").sum() == 9 and (LAB["prefix"] == "X").sum() == 9
    for p in ("C", "X"):
        for g in ("C", "D", "I"):
            assert ((LAB["prefix"] == p) & (LAB["group"] == g)).sum() == 3


def test_sex_label_check_branches():
    pre = LAB["prefix"]
    raw = np.full((3, 18), np.nan)
    raw[:, pre == "X"] = 1.0
    assert sex_label_check(raw, np.ones(3, bool), pre)["verdict"] == "confirmed"
    raw2 = np.full((3, 18), np.nan)
    raw2[:, pre == "C"] = 1.0
    assert sex_label_check(raw2, np.ones(3, bool), pre)["verdict"] == "swapped"
    assert sex_label_check(np.ones((3, 18)), np.ones(3, bool), pre)["male_prefix"] is None
    assert sex_label_check(raw, np.zeros(3, bool), pre)["verdict"].startswith("unconfirmed")


def test_y_specific_windows_excludes_shared():
    seqs = {"Y1": "MAAAKKSPLSRDEEQWT", "X1": "MAAAKKSPLSRDEEQWA", "Y2": "MPPPGGTYRRSLLQNNV"}
    genes = {"Y1": "Ddx3y", "X1": "Ddx3x", "Y2": "Uty"}
    shared = "AAAKKSPLSRDEEQW"  # also in the X homolog
    unique = "PPPGGTYRRSLLQNN"
    assert y_specific_windows([shared, unique], seqs, genes) == {unique}


def test_reproduction_threshold():
    y = np.zeros((1, 18))
    pre, grp = LAB["prefix"], LAB["group"]
    rng = np.random.default_rng(0)
    y += rng.normal(scale=0.01, size=y.shape)
    assert not reproduction(y, 0, pre, grp, ["C"])["pass"]
    y[0, (pre == "C") & (grp == "I")] -= 0.4  # 0.4 > log2(1.2) = 0.263
    assert reproduction(y, 0, pre, grp, ["C"])["pass"]
    assert not reproduction(y, 0, pre, grp, ["X"])["pass"]
    assert reproduction(y, None, pre, grp, ["C"])["pass"] is False


def test_decide_branches():
    ci_tight, ci_wide = {"hi": 0.3}, {"hi": 0.9}
    up = [0.3, 0.2, 0.1, 0.4]
    assert decide_07c(True, False, TAU_NULL, up, RIBO_OK, CAL_OK, ci_tight, [1, 1])["primary"] \
        == "UNINTERPRETABLE"
    assert decide_07c(False, True, None, [], None, None, None, [None, None])["primary"] \
        == "NOT MEASURABLE"
    d = decide_07c(True, True, TAU_UP, up, RIBO_OK, CAL_OK, ci_wide, [0.2, 0.1])
    assert d == {"primary": "SUGGESTIVE", "hippocampal": "SUPPORT"}
    d = decide_07c(True, True, TAU_UP, up, RIBO_OK, CAL_OK, ci_wide, [0.2, -0.1])
    assert d["hippocampal"] == "SUGGESTIVE, sex-dependent"
    d = decide_07c(True, True, TAU_UP, up, RIBO_OK, {"pass": False}, ci_wide, [0.2, 0.1])
    assert d["primary"].startswith("NULL, weak") and "miscalibrated" in d["primary"]
    down = {"rot_p_up": 0.99, "rot_p_down": 0.01, "single_protein_pct": 2.0,
            "perm_p_up": 0.99, "perm_p_down": 0.01}
    assert decide_07c(True, True, down, [-v for v in up], RIBO_OK, CAL_OK, ci_tight,
                      [0, 0])["primary"] == "OPPOSITE"
    assert decide_07c(True, True, TAU_NULL, up, RIBO_OK, CAL_OK, ci_tight, [0, 0])["primary"] \
        == "NULL, excludes a 1.5-fold rise"


def test_combine_inverse_variance():
    b = {"diff": 0.0, "lo": -1.0, "hi": 1.0, "df": 1e6}
    c = {"diff": 1.0, "se": 1.0 / 1.959964}
    out = combine_07b(b, c)
    assert abs(out["est"] - 0.5) < 1e-3 and abs(out["se_07b"] - out["se_07c"]) < 1e-3


def test_ptm_site_loader(tmp_path):
    cols = ["R.FileName", "PTM.CollapseKey", "PTM.FlankingRegion", "PTM.ModificationTitle",
            "PTM.ProteinId", "PTM.Quantity", "PTM.SiteAA", "PTM.SiteLocation",
            "PTM.SiteProbability"]
    w = "SVPDFPLSPPKKKDL"
    rows = [
        ["r1", "P54227_S38_M1", w, "Phospho (STY)", "P54227", "100", "S", "38", "0.9"],
        ["r1", "P54227_S38_M2", w, "Phospho (STY)", "P54227", "50", "S", "38", "0.8"],
        ["r2", "P54227_S38_M1", w, "Phospho (STY)", "P54227", "200", "S", "38", "0.5"],
        ["r2", "P54227_S38_M2", w, "Phospho (STY)", "P54227", "Filtered", "S", "38", "0.9"],
        ["r1", "P54227_C10_M1", "XXXXXXXCXXXXXXX", "Carbamidomethyl (C)", "P54227", "9",
         "C", "10", "1"],
    ]
    path = tmp_path / "ptm.xls"
    path.write_text("\n".join("\t".join(r) for r in [cols, *rows]) + "\n", encoding="utf-8")
    values, annot = load_spectronaut_ptm_sites(str(path), ["r1", "r2"], {"P54227": "Stmn1"})
    assert values.index.tolist() == ["P54227_S38"]
    assert values.loc["P54227_S38", "r1"] == 150  # multiplicities summed
    assert np.isnan(values.loc["P54227_S38", "r2"])  # low probability and Filtered dropped
    assert annot.loc["P54227_S38", "gene"] == "Stmn1" and annot.loc["P54227_S38", "window15"] == w
