"""Command line: python -m phospho07b.run posctl|primary|hippo --data DIR --fasta GZ --out JSON."""
from __future__ import annotations

import argparse
import json
import re

import numpy as np

from . import hippo, posctl
from .loaders import load_maxquant_sites
from .primary import (PRIMARY, SECONDARY, build_matrix, calibration_panel, decide,
                      set_tests, site_table)
from .settest import set_score_ci
from .stats import moderated_t

RIBO = re.compile(r"^(Rp[ls]\d+(a|al|l|l1|x)?|Rplp[012]|Rpsa)$")
SITES_FILE = "Phospho (STY)Sites.txt"


def run_primary(data: str, control: list[str], stress: list[str]) -> dict:
    samples = control + stress
    groups = np.array([False] * len(control) + [True] * len(stress))
    values, annot = load_maxquant_sites(f"{data}/{SITES_FILE}", samples)
    y, genes, prots, hits = build_matrix(values, annot)
    arr = y.to_numpy()
    mt = moderated_t(arr, groups)
    prior = (mt["d0"], mt["s0sq"])
    names = [f"TAU_{n}" for n in PRIMARY]
    sites = site_table(y, groups, names)
    covered = [s["site"] for s in sites if s.get("quantified")]
    res = {"samples": {"control": control, "stress": stress}, "n_sites": int(arr.shape[0]),
           "n_valid": int(mt["valid"].sum()), "prior_d0": mt["d0"], "prior_s0sq": mt["s0sq"],
           "tau_table_keys": hits, "primary_sites": sites,
           "secondary_sites": site_table(y, groups, [f"TAU_{n}" for n in SECONDARY]),
           "covered": covered, "coverage_gate": len(covered) >= 3}
    res["mapt_rows_any"] = [k for k in y.index if "TAU_" in k]
    res["reproduction"] = _reproduction(y, groups, genes)
    if not res["coverage_gate"]:
        res["decision"] = "NOT MEASURABLE"
        return res
    _set_level(res, y, arr, groups, prior, genes, prots, covered)
    res["decision"] = decide(True, res["reproduction"]["pass"], res["tau"], sites,
                             res["ribosomal"], res["calibration"], res["set_score"])
    return res


def _reproduction(y, groups, genes) -> dict:
    rows = [y.index[i] for i in np.flatnonzero(np.isin(genes, ["Rims1", "Map2"]))]
    tab = site_table(y, groups, rows)
    for t, r in zip(tab, rows):
        t["gene"] = genes[y.index.get_loc(r)]
    rims = [t for t in tab if t["gene"] == "Rims1" and t.get("quantified")]
    ok = any(t["lfc"] <= -0.5 for t in rims)
    return {"pass": ok, "sites": tab}


def _set_level(res, y, arr, groups, prior, genes, prots, covered):
    idx = np.array([y.index.get_loc(n) for n in covered])
    inten = np.nanmean(arr, 1)
    eligible = moderated_t(arr, groups)["valid"]
    ribo_mask = np.array([bool(RIBO.match(g)) for g in genes]) & eligible
    excl = {"TAU"} | set(prots[ribo_mask])
    res["tau"] = set_tests(arr, groups, idx, prior, inten, eligible, prots, excl)
    res["set_score"] = set_score_ci(arr, groups, idx)
    res["mean_lfc"] = float(np.mean([s["lfc"] for s in res["primary_sites"] if s.get("quantified")]))
    res["leave_one_out_S"] = [float(np.nanmean(moderated_t(arr, groups)["t"][np.delete(idx, j)]))
                              for j in range(len(idx))]
    ridx = np.flatnonzero(ribo_mask)
    res["ribosomal_genes"] = sorted(set(genes[ridx]))
    res["ribosomal"] = set_tests(arr, groups, ridx, prior, inten, eligible, prots, excl)
    res["calibration"] = calibration_panel(arr, groups, prior, prots, eligible, excl, len(idx))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["posctl", "primary", "hippo"])
    ap.add_argument("--data", required=True)
    ap.add_argument("--fasta")
    ap.add_argument("--control", nargs="*")
    ap.add_argument("--stress", nargs="*")
    ap.add_argument("--prior-07b", help="07b primary JSON (hippo mode)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.mode == "posctl":
        res = posctl.run(a.data, a.fasta)
    elif a.mode == "hippo":
        res = hippo.run(a.data, a.fasta, a.prior_07b)
    else:
        res = run_primary(a.data, a.control, a.stress)
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print(json.dumps({k: res[k] for k in res if k in ("verdict", "decision", "lfc", "perm_p_up",
                                                        "coverage_gate", "covered")}, default=str))


if __name__ == "__main__":
    main()
