"""Synthetic-data checks for 07b table parsing and the decision rule."""
import gzip
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from phospho07b.loaders import (  # noqa: E402
    find_sites, load_spectronaut, log2_median_centre, phospho_positions)
from phospho07b.posctl import bh  # noqa: E402
from phospho07b.primary import decide  # noqa: E402

PH = "Phospho_STY_NL_98 (STY)"
PROT = "MKAAAARPPASPSPQRQAGAPKLLLLR"


def test_phospho_positions_keeps_only_localized():
    mod = f"_ELEKPMQSKPQS[{PH}]PVIQATAGS[{PH}]PK_"
    loc = (f"_ELEKPMQS[{PH}: 0%]KPQS[{PH}: 100%]PVIQAT[{PH}: 0%]"
           f"AGS[{PH}: 60%]PK_")
    assert phospho_positions(mod, loc) == [11]


def test_phospho_positions_ignores_other_mods():
    mod = f"_[Acetyl (Protein N-term)]M[Oxidation (M)]AS[{PH}]K_"
    loc = f"_[Acetyl (Protein N-term)]M[Oxidation (M)]AS[{PH}: 99%]K_"
    assert phospho_positions(mod, loc) == [2]


def test_load_spectronaut_sums_precursors_and_places_site(tmp_path):
    fa = tmp_path / "ref.fasta.gz"
    with gzip.open(fa, "wt") as fh:
        fh.write(">sp|O88935|SYN1_MOUSE Synapsin-1 OS=Mus musculus GN=Syn1\n" + PROT + "\n")
    mod = f"_RPPASPS[{PH}]PQR_"
    loc = f"_RPPASPS[{PH}: 98%]PQR_"
    rows = []
    for f, q in (("a", 100.0), ("a", 50.0), ("b", 30.0)):
        rows.append({"R.FileName": f, "PG.ProteinAccessions": "O88935",
                     "EG.PTMLocalizationProbabilities": loc, "EG.ModifiedPeptide": mod,
                     "EG.StrippedSequence": "RPPASPSPQR", "FG.Quantity": q})
    path = tmp_path / "rep.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    values, annot = load_spectronaut(str(path), ["a", "b"], str(fa))
    key = "O88935_S13"  # centre of ARPPASPSPQRQAGA
    assert list(values.index) == [key]
    assert values.loc[key, "a"] == 150.0 and values.loc[key, "b"] == 30.0
    assert find_sites(annot, {"x": "ARPPASPSPQRQAGA"})["x"] == [key]


def test_median_centring_uses_complete_sites():
    v = pd.DataFrame({"s1": [2.0, 4.0, np.nan], "s2": [8.0, 16.0, 1.0]})
    y = log2_median_centre(v)
    assert np.allclose(y.iloc[:2].median(), 0.0)


def test_bh_matches_hand_values():
    p = np.array([0.01, 0.04, 0.03, np.nan])
    q = bh(p)
    assert np.allclose(q[:3], [0.03, 0.04, 0.04]) and np.isnan(q[3])


def _inputs(rot_up=0.01, pct=97.0, perm=0.05, lfc=(0.5, 0.4, 0.3), hi=1.0):
    tau = {"rot_p_up": rot_up, "single_protein_pct": pct, "perm_p_up": perm}
    sites = [{"quantified": True, "lfc": v} for v in lfc]
    ribo = {"rot_p_two": 0.5, "independent_pct": 50.0}
    calib = {"pass": True}
    return tau, sites, ribo, calib, {"hi": hi}


def test_decision_rule_branches():
    assert decide(False, True, *_inputs()) == "NOT MEASURABLE"
    assert decide(True, False, *_inputs()) == "UNINTERPRETABLE"
    assert decide(True, True, *_inputs()) == "SUGGESTIVE"
    assert decide(True, True, *_inputs(perm=0.10)).startswith("NULL, weak")
    assert decide(True, True, *_inputs(rot_up=0.2, hi=0.3)) == "NULL, excludes a 1.5-fold rise"
    tau, sites, ribo, calib, ci = _inputs()
    ribo = {"rot_p_two": 0.01, "independent_pct": 99.9}
    assert "controls flagged" in decide(True, True, tau, sites, ribo, calib, ci)
