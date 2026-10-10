"""Load deposited phospho tables into a site x sample matrix with annotations.

Output of both loaders: (values, annot). values is a DataFrame of linear
intensities (rows = site keys, columns = samples, NaN = missing). annot has
columns protein, gene, aa, pos, window15.
"""
from __future__ import annotations

import gzip
import re

import numpy as np
import pandas as pd

from .seqmap import window

TOKEN = re.compile(r"\[([^\]]*)\]|([A-Z])")
SPN_COLS = ["R.FileName", "PG.ProteinAccessions", "EG.PTMLocalizationProbabilities",
            "EG.ModifiedPeptide", "EG.StrippedSequence", "FG.Quantity"]


def read_fasta_gz(path: str) -> tuple[dict[str, str], dict[str, str]]:
    """UniProt FASTA (gz) -> ({accession: seq}, {accession: gene})."""
    seqs, genes, acc = {}, {}, None
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith(">"):
                acc = line[1:].split("|")[1]
                m = re.search(r" GN=(\S+)", line)
                genes[acc] = m.group(1) if m else ""
                seqs[acc] = []
            else:
                seqs[acc].append(line.strip())
    return {k: "".join(v) for k, v in seqs.items()}, genes


def phospho_positions(modpep: str, locstr: str, min_prob: float = 0.75) -> list[int]:
    """0-based peptide positions that carry phospho with localization >= min_prob."""
    carried, n = set(), -1
    for mod, aa in TOKEN.findall(modpep.strip("_")):
        if aa:
            n += 1
        elif "Phospho" in mod and n >= 0:
            carried.add(n)
    probs, n = {}, -1
    for mod, aa in TOKEN.findall(locstr.strip("_")):
        if aa:
            n += 1
        elif "Phospho" in mod and ":" in mod and n >= 0:
            probs[n] = float(mod.rsplit(":", 1)[1].strip().rstrip("%")) / 100
    return sorted(p for p in carried if probs.get(p, 0.0) >= min_prob)


def _place(stripped: str, accs: str, seqs: dict) -> tuple[str, int] | None:
    """First accession whose sequence contains the peptide, with 0-based offset."""
    for acc in accs.split(";"):
        s = seqs.get(acc)
        if s is not None:
            i = s.find(stripped)
            if i >= 0:
                return acc, i
    return None


def _peptide_sites(pep: pd.DataFrame, seqs: dict, genes: dict) -> pd.DataFrame:
    """One row per (peptide form, localized site) with protein coordinates."""
    rows = []
    for r in pep.itertuples(index=False):
        hit = _place(r.stripped, r.accs, seqs)
        if hit is None:
            continue
        acc, off = hit
        for p in phospho_positions(r.modpep, r.locstr):
            pos = off + p + 1
            rows.append((r.modpep, r.locstr, f"{acc}_{r.stripped[p]}{pos}", acc,
                         genes.get(acc, ""), r.stripped[p], pos, window(seqs[acc], pos)))
    return pd.DataFrame(rows, columns=["modpep", "locstr", "site", "protein", "gene",
                                       "aa", "pos", "window15"])


def load_spectronaut(path: str, files: list[str], fasta_gz: str):
    """Spectronaut long report -> site matrix (sum over precursors per file)."""
    seqs, genes = read_fasta_gz(fasta_gz)
    parts = []
    for chunk in pd.read_csv(path, usecols=SPN_COLS, chunksize=2_000_000, low_memory=False):
        chunk = chunk[chunk["R.FileName"].isin(files)]
        parts.append(chunk)
    df = pd.concat(parts, ignore_index=True)
    df.columns = ["file", "accs", "locstr", "modpep", "stripped", "q"]
    df = df[np.isfinite(df["q"]) & (df["q"] > 0)]
    per = df.groupby(["file", "modpep", "locstr", "stripped", "accs"], as_index=False)["q"].sum()
    forms = per[["modpep", "locstr", "stripped", "accs"]].drop_duplicates()
    sites = _peptide_sites(forms, seqs, genes)
    merged = per.merge(sites, on=["modpep", "locstr"])
    values = merged.pivot_table(index="site", columns="file", values="q", aggfunc="sum")
    values = values.reindex(columns=files)
    annot = sites.drop_duplicates("site").set_index("site").loc[values.index,
                                                                ["protein", "gene", "aa", "pos", "window15"]]
    return values, annot


def load_maxquant_sites(path: str, samples: list[str]):
    """MaxQuant Phospho (STY)Sites.txt -> site matrix from summed Intensity columns."""
    df = pd.read_csv(path, sep="\t", low_memory=False)
    for flag in ("Reverse", "Potential contaminant"):
        if flag in df:
            df = df[df[flag].astype(str) != "+"]
    df = df[df["Localization prob"] >= 0.75]
    prot = df["Protein"].astype(str)
    key = prot + "_" + df["Amino acid"].astype(str) + df["Position"].astype(str)
    values = df[[f"Intensity {s}" for s in samples]].astype(float).replace(0, np.nan)
    values.columns = samples
    values.index = key
    win = df["Sequence window"].astype(str).str.split(";").str[0].str[8:23]
    annot = pd.DataFrame({"protein": prot.values, "gene": df["Gene names"].astype(str).values,
                          "aa": df["Amino acid"].values, "pos": df["Position"].values,
                          "window15": win.values}, index=key)
    keep = ~values.index.duplicated()
    return values[keep], annot[keep]


def log2_median_centre(values: pd.DataFrame) -> pd.DataFrame:
    """log2, then subtract each sample's median over sites complete in all samples."""
    y = np.log2(values)
    complete = y.dropna()
    return y - complete.median(axis=0)


def find_sites(annot: pd.DataFrame, windows: dict[str, str]) -> dict[str, list[str]]:
    """Map target name -> table site keys whose 15-mer window matches."""
    return {name: annot.index[annot["window15"] == w].tolist() for name, w in windows.items()}
