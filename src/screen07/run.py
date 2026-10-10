"""Run the pre-registered project 07 screen (project-docs/prereg/07-*.md).

Usage (from the src/ directory):
    python -m screen07.run --data H:/bio-data/screen07 --repo C:/dev/bio-research
"""
from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path

import numpy as np
import pandas as pd

from . import loaders
from .annot import gencode_symbols, read_gene_set
from .model import design_matrix, filter_and_log, moderated_t
from .plots import pca_plot
from .settest import (expression_bins, leave_one_out, permutation_test,
                      random_set_test)

log = logging.getLogger("screen07")
N_SETS, N_PERM, SEED = 10_000, 2_000, 7
RIBO = re.compile(r"^Rp[ls]\d+[a-z]?$")
POS_CONTROLS = ["Fkbp5", "Sgk1"]


def analyse(ds: loaders.Dataset, gene_set: list[str], out_dir: Path,
            label: str, run_perm: bool = True) -> dict:
    """Full pre-registered analysis of one contrast."""
    smp = ds.samples
    k = int(smp["condition"].value_counts().min())
    logexpr = filter_and_log(ds.values[smp.index.tolist()], ds.kind, k)
    X = design_matrix(smp, ds.covariates)
    fit = moderated_t(logexpr.to_numpy(), X)
    tstat = pd.Series(fit["t"], index=logexpr.index)
    bins = expression_bins(logexpr.mean(axis=1))
    present = [g for g in gene_set if g in logexpr.index]
    res = {"label": label, "dataset": ds.name, "kind": ds.kind,
           "n_control": int((smp["condition"] == "control").sum()),
           "n_defeated": int((smp["condition"] == "defeated").sum()),
           "subgroups": smp["subgroup"].value_counts().to_dict(),
           "covariates": ds.covariates, "filter_k": k,
           "n_genes_tested": int(len(logexpr)), "prior_df": fit["d0"],
           "notes": ds.notes, "M_missing": [g for g in gene_set if g not in present]}
    res["primary"] = random_set_test(bins, tstat, present, N_SETS, SEED)
    loo = leave_one_out(bins, tstat, present, N_SETS, SEED)
    res["loo"] = {"set_mean_t_min": float(loo.set_mean_t.min()),
                  "set_mean_t_max": float(loo.set_mean_t.max()),
                  "p_down_min": float(loo.p_down.min()),
                  "p_down_max": float(loo.p_down.max()),
                  "p_two_max": float(loo.p_two.max())}
    if run_perm:
        res["permutation"] = permutation_test(logexpr, smp, ds.covariates,
                                              present, N_PERM, SEED)
    res["positive_control"] = positive_control(fit, logexpr.index)
    ribo = [g for g in logexpr.index if RIBO.match(g)]
    res["negative_control_ribosomal"] = random_set_test(bins, tstat, ribo, N_SETS, SEED)
    genes = pd.DataFrame({"logfc": fit["logfc"], "t": fit["t"], "p_two": fit["p_two"]},
                         index=logexpr.index).loc[present]
    genes.to_csv(out_dir / f"{slug(label)}_M_genes.tsv", sep="\t")
    pca_plot(logexpr, smp, ds.covariates, out_dir / f"{slug(label)}_pca.png", label)
    return res


def positive_control(fit: dict, genes: pd.Index) -> dict:
    out = {}
    for g in POS_CONTROLS:
        if g not in genes:
            out[g] = None
            continue
        i = genes.get_loc(g)
        out[g] = {"logfc": float(fit["logfc"][i]), "t": float(fit["t"][i]),
                  "p_up": float(fit["p_up"][i])}
    hits = [v for v in out.values() if v is not None]
    out["pass"] = bool(len(hits) == 2 and all(v["logfc"] > 0 for v in hits)
                       and any(v["p_up"] < 0.05 for v in hits))
    return out


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")


def subset(ds: loaders.Dataset, keep_subgroups: list[str], name: str) -> loaders.Dataset:
    smp = ds.samples[ds.samples["subgroup"].isin(keep_subgroups)]
    covs = [c for c in ds.covariates if smp[c].nunique() > 1]
    return loaders.Dataset(name, ds.values, ds.kind, smp, covs, list(ds.notes))


def build_datasets(data: Path, raw: Path, meta: Path) -> list[tuple[str, loaders.Dataset, bool]]:
    ens2sym = gencode_symbols(data / "ref" / "gencode.vM17.annotation.gtf.gz")
    b6 = loaders.load_gse109315(raw, meta, ens2sym, "C57BL/6Crl")
    dba = loaders.load_gse109315(raw, meta, ens2sym, "DBA/2Crl")
    return [
        ("discovery: GSE109315 C57BL/6Crl mPFC, defeated vs control", b6, True),
        ("secondary: GSE109315 C57BL/6Crl susceptible vs control",
         subset(b6, ["control", "susceptible"], b6.name), False),
        ("secondary: GSE109315 C57BL/6Crl resilient vs control",
         subset(b6, ["control", "resilient"], b6.name), False),
        ("held-out A: GSE109315 DBA/2Crl mPFC", dba, True),
        ("held-out B: GSE127812 PFC", loaders.load_gse127812(raw, meta), True),
        ("held-out C: GSE161726 mPFC (fallback)", loaders.load_gse161726(raw, meta, ens2sym), True),
    ]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--repo", type=Path, required=True)
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    out_dir = a.data / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    gene_set = read_gene_set(a.repo / "project-docs" / "prereg" / "07-geneset-M.txt")
    results = []
    for label, ds, perm in build_datasets(a.data, a.data / "raw", a.data / "meta"):
        log.info("analysing %s", label)
        try:
            results.append(analyse(ds, gene_set, out_dir, label, perm))
        except Exception:
            log.exception("analysis failed for %s", label)
            raise
    text = json.dumps(results, indent=2, default=float)
    (out_dir / "07-results.json").write_text(text, encoding="utf8")
    log.info("wrote %s", out_dir / "07-results.json")


if __name__ == "__main__":
    main()
