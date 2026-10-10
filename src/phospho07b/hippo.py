"""07c: tau phosphosites in PXD057176 mouse hippocampus, CRS vs Ctrl, sex-blocked."""
from __future__ import annotations

import json
import re

import numpy as np

from .blocked import (blocked_set_score_ci, blocked_set_stat, blocked_t, design,
                      stratified_perm_p)
from .hippo_checks import (combine_07b, decide_07c, decode_runs, reproduction,
                           sex_label_check, y_specific_windows)
from .loaders import load_spectronaut_ptm_sites, read_fasta_gz
from .primary import PRIMARY, SECONDARY, build_matrix, calibration_panel, set_tests, site_table
from .settest import (matched_independent_sets, matched_single_protein_sets, percentile,
                      rotation_test_design, set_score_ci)
from .stats import hedges_g, moderated_t

REPORT = "Phospho_Report/Report_PTMSiteReport (Normal).xls"
RUNS = ["Phos_DIA_20230422_C_C1_BE1_1_21276", "Phos_DIA_20230422_C_C2_BE2_1_21277",
        "Phos_DIA_20230422_C_C3_BE3_1_21278", "Phos_DIA_20230422_C_D1_BE4_1_21291",
        "Phos_DIA_20230422_C_D2_BE5_1_21292", "Phos_DIA_20230422_C_D3_BE6_1_21293",
        "Phos_DIA_20230422_C_I1_BE7_1_21296", "Phos_DIA_20230422_C_I2_BE8_1_21297",
        "Phos_DIA_20230422_C_I3_RD4_1_21298", "Phos_DIA_20230422_X_C1_RD5_1_21301",
        "Phos_DIA_20230422_X_C2_RD6_1_21302", "Phos_DIA_20230422_X_C3_RD7_1_21303",
        "Phos_DIA_20230422_X_D1_RD8_1_21306", "Phos_DIA_20230422_X_D2_RE1_1_21307",
        "Phos_DIA_20230422_X_D3_RE2_1_21308", "Phos_DIA_20230422_X_I1_RE3_1_21311",
        "Phos_DIA_20230422_X_I2_RE4_1_21312", "Phos_DIA_20230422_X_I3_RE5_1_21313"]
OTHERS = {"STMN1_S38": ("Stmn1", "SVPDFPLSPPKKKDL"), "PDHA1_S232": ("Pdha1", "NRYGMGTSVERAAAS")}
RIBO = re.compile(r"^(Rp[ls]\d+(a|al|l|l1|x)?|Rplp[012]|Rpsa)$")
TAU = [f"TAU_{n}" for n in PRIMARY]


def blocked_sites(y, sex, stress, names) -> list[dict]:
    """Per-site blocked lfc and t, pooled Hedges g, cell counts."""
    arr = y.to_numpy()
    bt, g = blocked_t(arr, sex, stress), hedges_g(arr, stress)
    out = []
    for n in names:
        if n not in y.index:
            out.append({"site": n, "quantified": False})
            continue
        i = y.index.get_loc(n)
        cells = {f"{'M' if s else 'F'}{'S' if t else 'C'}":
                 int(np.sum(~np.isnan(arr[i, (sex == s) & (stress == t)])))
                 for s in (False, True) for t in (False, True)}
        out.append({"site": n, "quantified": bool(bt["valid"][i]), "cells": cells,
                    "lfc": _f(bt["lfc"][i]), "t": _f(bt["t"][i]), "hedges_g": _f(g[i])})
    return out


def _f(x):
    return None if x is None or not np.isfinite(x) else round(float(x), 4)


def blocked_set_tests(arr, sex, stress, idx, prior, prots, exclude) -> dict:
    """Stratified permutation, rotation, single-protein and independent random sets."""
    perm = stratified_perm_p(lambda m, s, g: blocked_set_stat(m, s, g, idx), arr, sex, stress)
    rot = rotation_test_design(arr, design(sex, stress), idx, prior)
    bt = blocked_t(arr, sex, stress)
    t, eligible, inten = bt["t"], bt["valid"], np.nanmean(arr, 1)
    sp = matched_single_protein_sets(prots, inten, eligible, len(idx),
                                     float(np.nanmean(inten[idx])), exclude=exclude)
    ind = matched_independent_sets(inten, eligible, idx)
    stat = float(np.nanmean(t[idx]))
    return {"k": len(idx), "S": _f(stat), "perm_p_up": perm["p_up"],
            "perm_p_down": perm["p_down"], "perm_p_two": perm["p_two"], "n_labelings": perm["n"],
            "rot_p_up": rot["p_up"], "rot_p_down": rot["p_down"], "rot_p_two": rot["p_two"],
            "rot_sites": rot["n_sites"], "single_protein_sets": len(sp),
            "single_protein_pct": _f(percentile(stat, np.array([np.nanmean(t[s]) for s in sp])))
            if sp else None,
            "independent_pct": _f(percentile(stat, np.array([np.nanmean(t[s]) for s in ind])))}


def per_sex(y, sex, stress, covered, prots, exclude, names=("female", "male")) -> dict:
    """Secondary: 07b two-group statistics within each sex (6 stress vs 3 Ctrl).

    names: output keys for sex False and True (prefix labels if sex is unconfirmed).
    """
    out = {}
    for s in (False, True):
        cols = sex == s
        sub = y.loc[:, cols]
        arr, g = sub.to_numpy(), stress[cols]
        rows = site_table(sub, g, covered)
        idx = np.array([sub.index.get_loc(r["site"]) for r in rows if r.get("quantified")])
        res = {"sites": rows, "k": int(idx.size)}
        if idx.size:
            mt = moderated_t(arr, g)
            res["tests"] = set_tests(arr, g, idx, (mt["d0"], mt["s0sq"]), np.nanmean(arr, 1),
                                     mt["valid"], prots, exclude)
            res["set_score"] = set_score_ci(arr, g, idx)
        out[names[1] if s else names[0]] = res
    return out


def phenotype(y, sex, group, covered) -> dict:
    """Descriptive: AD-Sus vs Ctrl and Insus vs Ctrl, each sex-blocked."""
    out = {}
    for gname in ("D", "I"):
        cols = (group == "C") | (group == gname)
        sub = y.loc[:, cols]
        rows = blocked_sites(sub, sex[cols], group[cols] == gname, covered)
        idx = np.array([sub.index.get_loc(r["site"]) for r in rows if r.get("quantified")])
        bt = blocked_t(sub.to_numpy(), sex[cols], group[cols] == gname)
        res = {"sites": rows}
        if idx.size:
            res["S"] = _f(np.nanmean(bt["t"][idx]))
            x = design(sex[cols], group[cols] == gname)
            res["rotation"] = rotation_test_design(sub.to_numpy(), x, idx, (bt["d0"], bt["s0sq"]))
        out[{"D": "AD-Sus_vs_Ctrl", "I": "Insus_vs_Ctrl"}[gname]] = res
    return out


def run(data: str, fasta_gz: str, prior_07b_json: str) -> dict:
    """Run the 07c pre-registered analysis and return a result dict."""
    seqs, gmap = read_fasta_gz(fasta_gz)
    values, annot = load_spectronaut_ptm_sites(f"{data}/{REPORT}", RUNS, gmap)
    lab = decode_runs(RUNS)
    prefix, group = lab["prefix"], lab["group"]
    y, genes, prots, hits = build_matrix(values, annot, OTHERS)
    ywin = y_specific_windows(annot["window15"].tolist(), seqs, gmap)
    is_y = np.array([k in annot.index and annot.loc[k, "window15"] in ywin for k in y.index])
    res = {"runs": RUNS, "n_sites_table": int(values.shape[0]), "table_keys": hits}
    res["label_check"] = sex_label_check(y.to_numpy(), is_y, prefix)
    male = res["label_check"]["male_prefix"] or "X"
    sex, stress = prefix == male, group != "C"
    female_pf = [p for p in ("C", "X") if p != male] if res["label_check"]["male_prefix"] else ["C", "X"]
    srow = y.index.get_loc("STMN1_S38") if "STMN1_S38" in y.index else None
    arr = y.to_numpy()
    res["reproduction"] = reproduction(arr, srow, prefix, group, female_pf)
    prow = y.index.get_loc("PDHA1_S232") if "PDHA1_S232" in y.index else None
    res["pdha1_s232"] = (reproduction(arr, prow, prefix, group, female_pf)["contrasts"]
                         if prow is not None else "not in table")
    bt = blocked_t(arr, sex, stress)
    prior = (bt["d0"], bt["s0sq"])
    res.update({"n_sites": int(arr.shape[0]), "n_valid": int(bt["valid"].sum()),
                "prior_d0": bt["d0"], "prior_s0sq": bt["s0sq"],
                "primary_sites": blocked_sites(y, sex, stress, TAU),
                "secondary_sites": blocked_sites(y, sex, stress, [f"TAU_{n}" for n in SECONDARY])})
    covered = [s["site"] for s in res["primary_sites"] if s.get("quantified")]
    res["covered"], res["coverage_gate"] = covered, len(covered) >= 3
    if res["coverage_gate"]:
        _set_level(res, y, arr, sex, stress, group, prior, genes, prots, bt, covered)
    lfcs = [s["lfc"] for s in res["primary_sites"] if s.get("quantified")]
    per = [v.get("set_score", {}).get("diff") for v in res.get("per_sex", {}).values()] or [None]
    res["decision"] = decide_07c(res["coverage_gate"], res["reproduction"]["pass"],
                                 res.get("tau"), lfcs, res.get("ribosomal"),
                                 res.get("calibration"), res.get("set_score"), per)
    if "set_score" in res:
        with open(prior_07b_json, encoding="utf-8") as fh:
            res["combined_with_07b"] = combine_07b(json.load(fh)["set_score"], res["set_score"])
    return res


def _set_level(res, y, arr, sex, stress, group, prior, genes, prots, bt, covered):
    idx = np.array([y.index.get_loc(n) for n in covered])
    ribo_mask = np.array([bool(RIBO.match(g)) for g in genes]) & bt["valid"]
    excl = {"TAU", *OTHERS} | set(prots[ribo_mask])
    res["tau"] = blocked_set_tests(arr, sex, stress, idx, prior, prots, excl)
    res["set_score"] = blocked_set_score_ci(arr, sex, stress, idx)
    res["mean_lfc"] = float(np.mean([s["lfc"] for s in res["primary_sites"] if s.get("quantified")]))
    res["leave_one_out_S"] = [float(np.nanmean(bt["t"][np.delete(idx, j)])) for j in range(len(idx))]
    ridx = np.flatnonzero(ribo_mask)
    res["ribosomal_genes"] = sorted(set(genes[ridx]))
    res["ribosomal"] = blocked_set_tests(arr, sex, stress, ridx, prior, prots, excl)
    res["calibration"] = calibration_panel(arr, stress, prior, prots, bt["valid"], excl, len(idx),
                                           x=design(sex, stress))
    names = (("female", "male") if res["label_check"]["male_prefix"]
             else ("prefix_C_unconfirmed", "prefix_X_unconfirmed"))
    res["per_sex"] = per_sex(y, sex, stress, covered, prots, excl, names)
    res["phenotype"] = phenotype(y, sex, group, covered)
