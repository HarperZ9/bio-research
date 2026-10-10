"""GEO sample metadata and GENCODE gene-symbol mapping for screen07."""
from __future__ import annotations

import gzip
import logging
import re
import urllib.request
from pathlib import Path

import pandas as pd

log = logging.getLogger("screen07")
GEO_GSM_URL = ("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?"
               "acc={acc}&targ=gsm&form=text&view=brief")


def fetch_gsm_text(acc: str, cache_dir: Path) -> Path:
    """Download GEO sample metadata (no expression values) once and cache it."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    out = cache_dir / f"{acc}_gsm.txt"
    if not out.exists():
        url = GEO_GSM_URL.format(acc=acc)
        log.info("fetching sample metadata %s", url)
        with urllib.request.urlopen(url, timeout=120) as resp:
            out.write_bytes(resp.read())
    return out


def parse_gsm_text(path: Path) -> pd.DataFrame:
    """Parse GEO brief text into one row per sample."""
    rows: list[dict] = []
    cur: dict | None = None
    for line in path.read_text(encoding="utf8").splitlines():
        if line.startswith("^SAMPLE"):
            cur = {"gsm": line.split("=", 1)[1].strip()}
            rows.append(cur)
            continue
        if cur is None or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key, val = key.strip(), val.strip()
        if key == "!Sample_characteristics_ch1" and ":" in val:
            k, v = val.split(":", 1)
            cur[k.strip().lower()] = v.strip()
        elif key in ("!Sample_title", "!Sample_description",
                     "!Sample_platform_id", "!Sample_supplementary_file_1"):
            cur[key.replace("!Sample_", "")] = val
    return pd.DataFrame(rows)


_GTF_GENE = re.compile(r'gene_id "([^"]+)";.*?gene_name "([^"]+)";')


def gencode_symbols(gtf_gz: Path) -> dict[str, str]:
    """Map unversioned Ensembl gene ID to gene symbol from a GENCODE GTF."""
    mapping: dict[str, str] = {}
    with gzip.open(gtf_gz, "rt") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            parts = line.split("\t", 8)
            if len(parts) < 9 or parts[2] != "gene":
                continue
            m = _GTF_GENE.search(parts[8])
            if m:
                mapping[m.group(1).split(".")[0]] = m.group(2)
    if not mapping:
        raise ValueError(f"no gene records parsed from {gtf_gz}")
    return mapping


def read_gene_set(path: Path) -> list[str]:
    """Read a frozen gene list, ignoring comments and blank lines."""
    genes = [g.strip() for g in path.read_text(encoding="utf8").splitlines()]
    return [g for g in genes if g and not g.startswith("#")]
