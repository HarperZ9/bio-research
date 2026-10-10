"""Load each pre-registered dataset into a gene-symbol by sample table."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from .annot import fetch_gsm_text, parse_gsm_text

log = logging.getLogger("screen07")


@dataclass
class Dataset:
    name: str
    values: pd.DataFrame          # genes (symbols) x samples
    kind: str                     # "counts", "logcpm" or "rpkm"
    samples: pd.DataFrame         # index = column names; has "condition"
    covariates: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _symbolize(df: pd.DataFrame, ens2sym: dict[str, str], how: str,
               notes: list[str]) -> pd.DataFrame:
    """Replace Ensembl row IDs with symbols; collapse duplicate symbols."""
    ids = df.index.str.split(".").str[0]
    sym = pd.Series([ens2sym.get(x) for x in ids], index=df.index)
    n_unmapped = int(sym.isna().sum())
    out = df.loc[sym.notna().to_numpy()].copy()
    out.index = pd.Index(sym[sym.notna()].to_numpy())
    n_dup = int(out.index.duplicated(keep=False).sum())
    if how == "sum":
        out = out.groupby(level=0).sum()
    else:  # keep the most highly expressed row per symbol
        order = out.mean(axis=1).sort_values(ascending=False).index
        out = out.loc[order]
        out = out[~out.index.duplicated(keep="first")]
    notes.append(f"symbol mapping: {n_unmapped} IDs unmapped, {n_dup} rows "
                 f"in duplicated symbols collapsed by {how}")
    return out


def load_gse109315(raw: Path, meta: Path, ens2sym: dict[str, str],
                   strain: str) -> Dataset:
    """GSE109315 mPFC logCPM file, one strain."""
    vals = pd.read_csv(raw / "GSE109315" / "GSE109315_mPFC_counts_logCPM.txt.gz",
                       sep="\t", index_col=0)
    md = parse_gsm_text(fetch_gsm_text("GSE109315", meta))
    md = md[md["title"].str.endswith("_mPFC")].copy()
    md["col"] = md["title"].str.replace("_mPFC", "", regex=False).str.split("_").str[0]
    md = md[md["strain"] == strain].set_index("col")
    md["subgroup"] = md["csds phenotype"]
    md["condition"] = (md["subgroup"] != "control").map({True: "defeated", False: "control"})
    md["platform"] = md["platform_id"]
    missing = set(md.index) - set(vals.columns)
    if missing:
        raise ValueError(f"metadata samples missing from matrix: {missing}")
    notes = ["input is logCPM as deposited (not raw counts); used without renormalization"]
    vals = _symbolize(vals[md.index.tolist()], ens2sym, "max", notes)
    covs = ["platform"] if md["platform"].nunique() > 1 else []
    return Dataset(f"GSE109315 {strain} mPFC", vals, "logcpm", md, covs, notes)


def load_gse127812(raw: Path, meta: Path) -> Dataset:
    """GSE127812 PFC, transcript-level RPKM summed to gene symbol."""
    x = pd.read_excel(raw / "GSE127812" / "GSE127812_mRNAs-expression.xlsx")
    md = parse_gsm_text(fetch_gsm_text("GSE127812", meta))
    md["col_raw"] = md["description"]
    md["condition"] = md["title"].str.contains("without RSD").map(
        {True: "control", False: "defeated"})
    md["subgroup"] = md["condition"]
    colmap = {c: c.split("|")[1] for c in x.columns if "|" in c}
    x = x.rename(columns=colmap)
    md = md.set_index("col_raw")
    vals = x.dropna(subset=["symbol"]).groupby("symbol")[md.index.tolist()].sum()
    notes = ["input is transcript-level RPKM; summed per gene symbol; "
             "log2(RPKM + 1) used, filter RPKM >= 1"]
    return Dataset("GSE127812 PFC", vals, "rpkm", md, [], notes)


def load_gse161726(raw: Path, meta: Path, ens2sym: dict[str, str]) -> Dataset:
    """GSE161726 mPFC featureCounts per-sample files."""
    md = parse_gsm_text(fetch_gsm_text("GSE161726", meta))
    md = md[md["title"].str.contains("mPFC")].set_index("gsm")
    cols = {}
    for gsm in md.index:
        files = list((raw / "GSE161726").glob(f"{gsm}_*.tsv.gz"))
        if len(files) != 1:
            raise FileNotFoundError(f"expected one file for {gsm}, got {files}")
        t = pd.read_csv(files[0], sep="\t", comment="#", index_col=0)
        cols[gsm] = t.iloc[:, -1]
    vals = pd.DataFrame(cols)
    md["subgroup"] = md["behavioural phenotype"]
    md["condition"] = (md["subgroup"] != "Control").map({True: "defeated", False: "control"})
    notes = ["input is raw featureCounts (GENCODE M17 gene IDs)"]
    vals = _symbolize(vals, ens2sym, "sum", notes)
    return Dataset("GSE161726 mPFC", vals, "counts", md, [], notes)
