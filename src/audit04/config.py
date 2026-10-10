"""Shared constants for audit 04 (citation audit of CMN papers)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "audit04"
RAW = DATA / "raw"

TARGETS = {
    "SIMARD1997": "10.1038/41557",
    "BEILER2010": "10.1111/j.1469-8137.2009.03069.x",
}
SEED = 20261009
PER_TARGET = 100
BUCKETS = [(1997, 2009), (2010, 2016), (2017, 2022), (2023, 2026)]


def bucket(year):
    """Map a publication year to the pre-registered bucket label."""
    if year is None:
        return "unknown"
    for lo, hi in BUCKETS:
        if lo <= year <= hi:
            return f"{lo}-{hi}"
    return "unknown"
