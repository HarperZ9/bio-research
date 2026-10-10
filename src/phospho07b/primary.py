"""Primary test in PXD016302 mPFC: tau set, controls, decision rule."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .loaders import find_sites, log2_median_centre
from .posctl import combine_target
from .settest import (matched_independent_sets, matched_single_protein_sets, percentile,
                      rotation_test, rotation_test_design, set_score_ci, set_stat)
from .stats import hedges_g, moderated_t, permutation_p_up

PRIMARY = {"S202": "SGYSSPGSPGTPGSR", "T205": "SSPGSPGTPGSRSRT", "T231": "KKVAVVRTPPKSPSA",
           "S396": "GAEIVYKSPVVSGDT", "S404": "PVVSGDTSPRHLSNV", "S409": "DTSPRHLSNVSSTGS"}
SECONDARY = {"S262": "NVRSKIGSTENLKHQ", "S356": "RVQSKIGSLDNITHV"}
LOG2_15 = float(np.log2(1.5))


def build_matrix(values: pd.DataFrame, annot: pd.DataFrame, others: dict | None = None):
    """Collapse each tau target to one row; return y, row names, genes, targets.

    others: optional {row name: (gene, 15-mer window)} for non-tau sites that
    are collapsed the same way (07c reproduction sites).
    """
    hits = find_sites(annot, {**PRIMARY, **SECONDARY})
    ohits = find_sites(annot, {k: w for k, (_, w) in (others or {}).items()})
    used = sorted({k for v in [*hits.values(), *ohits.values()] for k in v})
    rest = values.drop(index=used)
    extra = {f"TAU_{n}": combine_target(values, k) for n, k in hits.items() if k}
    oextra = {n: combine_target(values, k) for n, k in ohits.items() if k}
    tau = pd.DataFrame({**extra, **oextra}, index=values.columns).T
    allv = pd.concat([rest, tau])
    genes = (list(annot.loc[rest.index, "gene"].str.split(";").str[0]) + ["Mapt"] * len(extra)
             + [others[n][0] for n in oextra])
    prots = list(annot.loc[rest.index, "protein"]) + ["TAU"] * len(extra) + list(oextra)
    y = log2_median_centre(allv)
    if others is not None:
        hits = {**hits, **ohits}
    return y, np.array(genes), np.array(prots), hits


def site_table(y: pd.DataFrame, groups: np.ndarray, names: list[str]) -> list[dict]:
    """Per-site effect sizes for the named rows."""
    arr = y.to_numpy()
    mt, g = moderated_t(arr, groups), hedges_g(arr, groups)
    out = []
    for n in names:
        if n not in y.index:
            out.append({"site": n, "quantified": False})
            continue
        i = y.index.get_loc(n)
        out.append({"site": n, "quantified": bool(mt["valid"][i]),
                    "n_stress": int(np.sum(~np.isnan(arr[i, groups]))),
                    "n_control": int(np.sum(~np.isnan(arr[i, ~groups]))),
                    "lfc": _f(mt["lfc"][i]), "t": _f(mt["t"][i]), "hedges_g": _f(g[i])})
    return out


def _f(x) -> float | None:
    return None if x is None or not np.isfinite(x) else round(float(x), 4)


def set_tests(arr, groups, idx, prior, intensity, eligible, prots, exclude) -> dict:
    """Permutation, rotation, single-protein and independent random-set tests."""
    stat = set_stat(arr, groups, idx)
    p_up, p_two, n = permutation_p_up(lambda m, g: set_stat(m, g, idx), arr, groups)
    rot = rotation_test(arr, groups, idx, prior)
    t = moderated_t(arr, groups)["t"]
    k = len(idx)
    sp = matched_single_protein_sets(prots, intensity, eligible, k,
                                     float(np.nanmean(intensity[idx])), exclude=exclude)
    ind = matched_independent_sets(intensity, eligible, idx)
    sp_ref = np.array([np.nanmean(t[s]) for s in sp])
    ind_ref = np.array([np.nanmean(t[s]) for s in ind])
    return {"k": k, "S": _f(stat), "perm_p_up": p_up, "perm_p_two": p_two, "n_labelings": n,
            "rot_p_up": rot["p_up"], "rot_p_two": rot["p_two"], "rot_sites": rot["n_sites"],
            "single_protein_sets": len(sp),
            "single_protein_pct": _f(percentile(stat, sp_ref)) if len(sp) else None,
            "independent_pct": _f(percentile(stat, ind_ref))}


def calibration_panel(arr, groups, prior, prots, eligible, exclude, k, n_sets=200, seed=7,
                      x=None):
    """Rotation test on random single-protein sets: fraction two-sided p < 0.05.

    x: optional design matrix (last column tested); default is [1, groups].
    """
    if x is None:
        x = np.column_stack([np.ones(arr.shape[1]), groups.astype(float)])
    rng = np.random.default_rng(seed)
    by = {}
    for i in np.flatnonzero(eligible & ~np.isnan(arr).any(1)):
        if prots[i] not in exclude:
            by.setdefault(prots[i], []).append(i)
    pool = [np.array(v) for v in by.values() if len(v) >= k]
    ps = []
    for j in range(n_sets):
        rows = pool[rng.integers(len(pool))]
        pick = rng.choice(rows, k, replace=False)
        ps.append(rotation_test_design(arr, x, pick, prior, n_rot=999, seed=j)["p_two"])
    ps = np.array(ps)
    return {"n_sets": n_sets, "k": k, "frac_p_two_lt_005": float(np.mean(ps < 0.05)),
            "pass": bool(np.mean(ps < 0.05) <= 0.15)}


def decide(cov_ok, repro_ok, tau, sites, ribo, calib, ci) -> str:
    """Apply section 8 of the pre-registration."""
    if not cov_ok:
        return "NOT MEASURABLE"
    if not repro_ok:
        return "UNINTERPRETABLE"
    ribo_flag = ribo["rot_p_two"] < 0.05 and not (2.5 <= ribo["independent_pct"] <= 97.5)
    rot_ok = calib["pass"] and not ribo_flag
    lfcs = [s["lfc"] for s in sites if s.get("quantified")]
    a = np.mean(lfcs) > 0 and sum(v > 0 for v in lfcs) >= 3
    b = rot_ok and tau["rot_p_up"] < 0.05
    c = tau["single_protein_pct"] is not None and tau["single_protein_pct"] >= 95
    d = tau["perm_p_up"] <= 1 / 20 + 1e-12
    if a and b and c and d:
        return "SUGGESTIVE"
    tag = "" if rot_ok else " (controls flagged: rotation test miscalibrated)"
    if ci["hi"] < LOG2_15:
        return "NULL, excludes a 1.5-fold rise" + tag
    return "NULL, weak (a 1.5-fold rise not excluded)" + tag
