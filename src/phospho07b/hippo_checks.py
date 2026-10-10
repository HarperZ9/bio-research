"""07c checks: run-name decoding, sex label check, reproduction, decision, combination."""
from __future__ import annotations

import numpy as np
from scipy import stats as sps

from .stats import moderated_t

Y_GENES = ("Ddx3y", "Eif2s3y", "Kdm5d", "Uty")
LOG2_12 = float(np.log2(1.2))
LOG2_15 = float(np.log2(1.5))


def decode_runs(runs: list[str]) -> dict:
    """Phos_DIA_<date>_<S>_<G><r>_... -> prefix S (C or X) and group G (C, D, I)."""
    prefix, group = [], []
    for r in runs:
        parts = r.split("_")
        prefix.append(parts[3])
        group.append(parts[4][0])
    if set(prefix) != {"C", "X"} or set(group) != {"C", "D", "I"}:
        raise ValueError(f"run names do not decode: {sorted(set(prefix))} {sorted(set(group))}")
    return {"prefix": np.array(prefix), "group": np.array(group)}


def y_specific_windows(windows: list[str], seqs: dict[str, str], genes: dict[str, str]) -> set:
    """Table windows found in a Y-linked protein and in no other sequence."""
    ykeys = [a for a in seqs if genes.get(a) in Y_GENES]
    yseq = "|".join(seqs[a] for a in ykeys)
    other = "|".join(s for a, s in seqs.items() if genes.get(a) not in Y_GENES)
    out = set()
    for w in set(windows):
        core = w.strip("_")
        if len(core) >= 11 and core in yseq and core not in other:
            out.add(w)
    return out


def sex_label_check(raw: np.ndarray, is_y: np.ndarray, prefix: np.ndarray) -> dict:
    """Which prefix carries the Y-linked sites (section 6 criterion)."""
    rows = np.flatnonzero(is_y)
    res = {"n_y_sites": int(rows.size), "male_prefix": None, "per_site": []}
    if rows.size == 0:
        res["verdict"] = "unconfirmed (no Y-linked site)"
        return res
    votes = {"C": 0, "X": 0}
    for i in rows:
        cnt = {p: int(np.sum(~np.isnan(raw[i, prefix == p]))) for p in ("C", "X")}
        res["per_site"].append(cnt)
        for a, b in (("C", "X"), ("X", "C")):
            if cnt[a] >= 7 and cnt[b] <= 2:
                votes[a] += 1
    for p in ("C", "X"):
        if votes[p] > rows.size / 2:
            res["male_prefix"] = p
    res["votes"] = votes
    if res["male_prefix"] is None:
        res["verdict"] = "unconfirmed (mixed pattern)"
    else:
        res["verdict"] = "confirmed" if res["male_prefix"] == "X" else "swapped"
    return res


def two_group_lfc(y: np.ndarray, cols_a: np.ndarray, cols_b: np.ndarray, row: int) -> dict:
    """Moderated t of a minus b on the subset of columns, for one row."""
    sub = np.concatenate([y[:, cols_a], y[:, cols_b]], 1)
    g = np.array([True] * cols_a.sum() + [False] * cols_b.sum())
    mt = moderated_t(sub, g)
    return {"lfc": _f(mt["lfc"][row]), "t": _f(mt["t"][row]), "valid": bool(mt["valid"][row])}


def reproduction(y, row, prefix, group, female_prefixes) -> dict:
    """Stmn1 S38: |lfc| >= log2(1.2) in a female phenotype vs female Ctrl."""
    out = {"contrasts": {}, "pass": False}
    if row is None:
        out["note"] = "Stmn1 S38 not in table"
        return out
    for fp in female_prefixes:
        ctrl = (prefix == fp) & (group == "C")
        for gname in ("D", "I"):
            r = two_group_lfc(y, (prefix == fp) & (group == gname), ctrl, row)
            out["contrasts"][f"{fp}_{gname}_vs_{fp}_C"] = r
            if r["valid"] and r["lfc"] is not None and abs(r["lfc"]) >= LOG2_12:
                out["pass"] = True
    return out


def _f(x):
    return None if x is None or not np.isfinite(x) else round(float(x), 4)


def decide_07c(cov_ok, repro_ok, tau, lfcs, ribo, calib, ci, per_sex) -> dict:
    """Section 7 of the 07c pre-registration."""
    if not repro_ok:
        return {"primary": "UNINTERPRETABLE", "hippocampal": "UNINFORMATIVE"}
    if not cov_ok:
        return {"primary": "NOT MEASURABLE", "hippocampal": "UNINFORMATIVE"}
    ribo_flag = ribo["rot_p_two"] < 0.05 and not (2.5 <= ribo["independent_pct"] <= 97.5)
    rot_ok = calib["pass"] and not ribo_flag
    pct = tau["single_protein_pct"]
    up = (np.mean(lfcs) > 0 and sum(v > 0 for v in lfcs) >= 3 and rot_ok
          and tau["rot_p_up"] < 0.05 and pct is not None and pct >= 95
          and tau["perm_p_up"] < 0.05)
    down = (np.mean(lfcs) < 0 and sum(v < 0 for v in lfcs) >= 3 and rot_ok
            and tau["rot_p_down"] < 0.05 and pct is not None and pct <= 5
            and tau["perm_p_down"] < 0.05)
    tag = "" if rot_ok else " (controls flagged: rotation test miscalibrated)"
    if up:
        both = all(s is not None and s > 0 for s in per_sex)
        return {"primary": "SUGGESTIVE",
                "hippocampal": "SUPPORT" if both else "SUGGESTIVE, sex-dependent"}
    if down:
        return {"primary": "OPPOSITE" + tag, "hippocampal": "OPPOSITE"}
    sub = "excludes a 1.5-fold rise" if ci["hi"] < LOG2_15 else "weak (a 1.5-fold rise not excluded)"
    return {"primary": f"NULL, {sub}{tag}", "hippocampal": f"NULL, {sub}"}


def combine_07b(ci_07b: dict, ci_07c: dict) -> dict:
    """Inverse-variance fixed-effect combination of the two set-score effects."""
    se_b = (ci_07b["hi"] - ci_07b["lo"]) / (2 * sps.t.ppf(0.975, ci_07b["df"]))
    se_c = ci_07c["se"]
    w = np.array([1 / se_b ** 2, 1 / se_c ** 2])
    est = float(np.sum(w * np.array([ci_07b["diff"], ci_07c["diff"]])) / w.sum())
    se = float(np.sqrt(1 / w.sum()))
    return {"est": est, "lo": est - 1.96 * se, "hi": est + 1.96 * se, "se": se,
            "se_07b": float(se_b), "se_07c": float(se_c)}
