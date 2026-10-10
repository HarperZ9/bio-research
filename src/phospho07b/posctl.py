"""Positive control: Syn1 pS553 in PXD024829 dHC, swim (6 min) vs home cage."""
from __future__ import annotations

import csv

import numpy as np
import pandas as pd

from .loaders import find_sites, load_spectronaut, log2_median_centre
from .stats import hedges_g, moderated_t, permutation_p_up

SYN1_S553 = "ARPPASPSPQRQAGA"
REPORT = "20191031_174447_20191028_AllPhosphoData_Report.csv"


def dhc_exp1_design(meta_csv: str) -> tuple[list[str], np.ndarray, list[dict]]:
    """Exp1 dHC files and labels (True = swim) from the deposited metadata."""
    with open(meta_csv, encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh, delimiter=";"))
    keep = [r for r in rows if r["ShortExp"] == "Exp1" and r["Region"] == "dHC"
            and r["ShortCond"] in ("CON", "SW06")]
    files = [r["FileName"] for r in keep]
    groups = np.array([r["ShortCond"] == "SW06" for r in keep])
    return files, groups, keep


def combine_target(values: pd.DataFrame, keys: list[str]) -> np.ndarray:
    """Sum linear intensities of all table keys for one physical site."""
    sub = values.loc[keys]
    total = sub.sum(axis=0, min_count=1)
    return total.to_numpy(dtype=float)


def bh(p: np.ndarray) -> np.ndarray:
    """Benjamini-Hochberg adjusted p (NaN kept)."""
    out = np.full_like(p, np.nan)
    ok = np.isfinite(p)
    pv = p[ok]
    order = np.argsort(pv)
    ranked = pv[order] * pv.size / (np.arange(pv.size) + 1)
    ranked = np.minimum.accumulate(ranked[::-1])[::-1]
    adj = np.empty_like(pv)
    adj[order] = np.minimum(ranked, 1)
    out[ok] = adj
    return out


def run(data_dir: str, fasta_gz: str) -> dict:
    """Run the pre-registered positive control and return a result dict."""
    files, groups, meta = dhc_exp1_design(f"{data_dir}/Metadata_Phosphos.csv")
    values, annot = load_spectronaut(f"{data_dir}/{REPORT}", files, fasta_gz)
    keys = find_sites(annot, {"Syn1_S553": SYN1_S553})["Syn1_S553"]
    res = {"n_swim": int(groups.sum()), "n_control": int((~groups).sum()),
           "animals": [r["Animal"] for r in meta], "n_sites_table": int(values.shape[0]),
           "syn1_keys": keys}
    if not keys:
        res["verdict"] = "FAIL (site not in table)"
        return res
    target = combine_target(values, keys)
    others = values.drop(index=keys)
    allv = pd.concat([others, pd.DataFrame([target], columns=values.columns, index=["SYN1_S553"])])
    y = log2_median_centre(allv).to_numpy()
    row = y.shape[0] - 1
    mt = moderated_t(y, groups)
    p_up, p_two, n_lab = permutation_p_up(lambda m, g: moderated_t(m, g)["t"][row], y, groups)
    q = bh(2 * np.minimum(mt["p_up"], 1 - mt["p_up"]))
    res.update({
        "syn1_values_log2": [None if np.isnan(v) else round(float(v), 4) for v in y[row]],
        "lfc": float(mt["lfc"][row]), "t": float(mt["t"][row]),
        "hedges_g": float(hedges_g(y, groups)[row]),
        "perm_p_up": p_up, "perm_p_two": p_two, "n_labelings": n_lab,
        "d0": mt["d0"], "s0sq": mt["s0sq"],
        "n_sites_tested": int(np.sum(mt["valid"])),
        "n_bh_q_lt_005": int(np.nansum(q < 0.05)),
    })
    passed = res["lfc"] > 0 and p_up < 0.05
    res["verdict"] = "PASS" if passed else "FAIL"
    return res
