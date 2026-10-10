"""Checks for the 07b residue-number mapping by alignment."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from phospho07b.seqmap import align_map, map_sites, window  # noqa: E402

CORE = "MAEPRQEFEVMEDHAGTYGLGDRKDQGGYTMHQDQEGDTDAGLKESPLQTPTEDGSEEPGSETSDAKSTPTAE"


def test_identity_alignment_maps_each_position():
    pairs = align_map(CORE, CORE)
    assert all(pairs[i] == i for i in range(1, len(CORE) + 1))


def test_deletion_shifts_downstream_numbers():
    src = CORE[:10] + "ABCDEFGHIKL" + CORE[10:]  # 11-residue insert, like human vs mouse
    hits = map_sites(src, CORE, [f"S{src.index('SPLQ') + 1}"])
    assert hits[0]["dst_pos"] == CORE.index("SPLQ") + 1
    assert hits[0]["src_window"] == hits[0]["dst_window"]


def test_window_padding():
    assert window("ABCDE", 1, 2) == "__ABC"
    assert window("ABCDE", 5, 2) == "CDE__"
