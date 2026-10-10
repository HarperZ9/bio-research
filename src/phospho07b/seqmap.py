"""Map residue numbers between protein sequences by global alignment.

Used to carry human 2N4R tau site numbers (UniProt P10636-8) onto mouse tau
(UniProt P10637 isoforms) and to build flanking windows for matching sites in
deposited tables whose protein numbering is unknown.
"""
from __future__ import annotations

import numpy as np

MATCH, MISMATCH, GAP = 2, -1, -3


def read_fasta(path: str) -> dict[str, str]:
    """Return {accession: sequence}; accession is the second '|' field."""
    seqs: dict[str, str] = {}
    name = None
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">"):
                head = line[1:].split()[0]
                name = head.split("|")[1] if "|" in head else head
                seqs[name] = ""
            elif name is not None:
                seqs[name] += line
    return seqs


def _score_matrix(a: str, b: str) -> np.ndarray:
    """Needleman-Wunsch score matrix with linear gap penalty."""
    n, m = len(a), len(b)
    s = np.zeros((n + 1, m + 1), dtype=np.int64)
    s[:, 0] = GAP * np.arange(n + 1)
    s[0, :] = GAP * np.arange(m + 1)
    bb = np.frombuffer(b.encode(), dtype=np.uint8)
    for i in range(1, n + 1):
        sub = np.where(bb == ord(a[i - 1]), MATCH, MISMATCH)
        diag = s[i - 1, :-1] + sub
        up = s[i - 1, 1:] + GAP
        row = np.maximum(diag, up)
        cur = np.empty(m + 1, dtype=np.int64)
        cur[0] = s[i, 0]
        for j in range(1, m + 1):
            cur[j] = max(row[j - 1], cur[j - 1] + GAP)
        s[i] = cur
    return s


def align_map(a: str, b: str) -> dict[int, int]:
    """Map 1-based positions of a onto 1-based positions of b (aligned pairs only)."""
    s = _score_matrix(a, b)
    i, j, pairs = len(a), len(b), {}
    while i > 0 and j > 0:
        sub = MATCH if a[i - 1] == b[j - 1] else MISMATCH
        if s[i, j] == s[i - 1, j - 1] + sub:
            pairs[i] = j
            i, j = i - 1, j - 1
        elif s[i, j] == s[i - 1, j] + GAP:
            i -= 1
        else:
            j -= 1
    return pairs


def window(seq: str, pos: int, half: int = 7) -> str:
    """Flanking window of 2*half+1 residues centred on 1-based pos, '_' padded."""
    padded = "_" * half + seq + "_" * half
    return padded[pos - 1: pos - 1 + 2 * half + 1]


def map_sites(src: str, dst: str, sites: list[str]) -> list[dict]:
    """Map sites like 'S202' from src to dst; report residue and window agreement."""
    pairs = align_map(src, dst)
    out = []
    for site in sites:
        aa, pos = site[0], int(site[1:])
        if src[pos - 1] != aa:
            raise ValueError(f"{site}: source residue is {src[pos - 1]}")
        tgt = pairs.get(pos)
        out.append({
            "site": site,
            "dst_pos": tgt,
            "dst_aa": dst[tgt - 1] if tgt else None,
            "src_window": window(src, pos),
            "dst_window": window(dst, tgt) if tgt else None,
        })
    return out
