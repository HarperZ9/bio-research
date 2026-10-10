"""Link spin-echo field maps to rest BOLD runs (prereg 01, deviation 3).

Runs on the participant's LOCAL BIDS copy before fMRIPrep. For each session
(or the subject folder when there are no sessions) it checks that

  * the field maps form an opposite phase-encoding pair on one axis
    (for example j and j-), each with TotalReadoutTime;
  * every rest BOLD run in that session encodes along the same axis;
  * field maps and BOLD share image geometry (shape, voxel size, affine).

If every session passes, it writes IntendedFor (subject-relative paths) into
the field map sidecars and, so that both BIDS linking mechanisms agree,
B0FieldSource into the BOLD sidecars when the field maps carry a
B0FieldIdentifier. Originals are copied to a backup folder first. If any
session fails, nothing is edited and the participant uses fMRIPrep's
field-map-less SyN correction. The decision is written to a JSON receipt.

  python -I -m conn01.fmaplink --sub-dir BIDS/sub-X --receipt OUT.json \
      --backup-dir WORK/sidecars-orig
Prints "fieldmaps" or "syn" on the last line.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

import numpy as np

AFFINE_TOL_MM = 0.01


def session_of(path: Path) -> str:
    m = re.search(r"_(ses-[A-Za-z0-9]+)_", path.name)
    return m.group(1) if m else ""


def pe_axis(direction: str) -> str:
    return direction.rstrip("-")


def default_geometry(nifti: Path) -> tuple:
    """(shape[:3], zooms[:3], affine) from the NIfTI header only."""
    import nibabel as nib

    img = nib.load(str(nifti))
    return (tuple(img.shape[:3]), tuple(round(float(z), 4) for z in img.header.get_zooms()[:3]),
            np.asarray(img.affine))


def same_geometry(a: tuple, b: tuple) -> bool:
    return a[0] == b[0] and np.allclose(a[1], b[1], atol=1e-3) and \
        np.allclose(a[2], b[2], atol=AFFINE_TOL_MM)


def _sidecar(nifti: Path) -> Path:
    return nifti.with_name(nifti.name.replace(".nii.gz", ".json"))


def check_session(fmaps: list[Path], bolds: list[Path], geometry) -> str:
    """Empty string if compatible, else the reason it is not."""
    if not fmaps or not bolds:
        return "no field maps" if not fmaps else "no rest BOLD"
    meta = {f: json.loads(_sidecar(f).read_text()) for f in fmaps}
    dirs = [m.get("PhaseEncodingDirection", "") for m in meta.values()]
    if any(not d for d in dirs) or len({pe_axis(d) for d in dirs}) != 1:
        return f"field map phase encoding not on one axis: {dirs}"
    if len(set(dirs)) != 2:
        return f"field maps lack an opposite phase-encoding pair: {dirs}"
    if any("TotalReadoutTime" not in m for m in meta.values()):
        return "field map without TotalReadoutTime"
    fgeo = geometry(fmaps[0])
    if not all(same_geometry(fgeo, geometry(f)) for f in fmaps[1:]):
        return "field maps differ in geometry"
    for b in bolds:
        d = json.loads(_sidecar(b).read_text()).get("PhaseEncodingDirection", "")
        if pe_axis(d) != pe_axis(dirs[0]):
            return f"{b.name}: phase-encoding axis {d!r} differs from field maps"
        if not same_geometry(fgeo, geometry(b)):
            return f"{b.name}: geometry differs from field maps"
    return ""


def plan(sub_dir: Path, geometry=default_geometry) -> dict:
    """Decide the correction path for one participant; edits nothing."""
    fmaps = sorted((sub_dir).glob("**/fmap/*_epi.nii.gz"))
    bolds = sorted((sub_dir).glob("**/func/*task-rest*_bold.nii.gz"))
    sessions = sorted({session_of(p) for p in fmaps + bolds})
    receipt = {"sdc_path": "fieldmaps", "sessions": {}, "reason": ""}
    for ses in sessions:
        f = [p for p in fmaps if session_of(p) == ses]
        b = [p for p in bolds if session_of(p) == ses]
        why = check_session(f, b, geometry)
        receipt["sessions"][ses or "nosession"] = {
            "fieldmaps": [p.name for p in f], "bold": [p.name for p in b],
            "compatible": not why, "reason": why}
        if why and receipt["sdc_path"] == "fieldmaps":
            receipt.update(sdc_path="syn", reason=f"{ses or 'nosession'}: {why}")
    if not sessions:
        receipt.update(sdc_path="syn", reason="no field maps or rest BOLD found")
    return receipt


def apply_links(sub_dir: Path, receipt: dict, backup_dir: Path) -> None:
    """Write IntendedFor / B0FieldSource into the local sidecars."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    for info in receipt["sessions"].values():
        fmaps = [next(sub_dir.glob(f"**/fmap/{n}")) for n in info["fieldmaps"]]
        bolds = [next(sub_dir.glob(f"**/func/{n}")) for n in info["bold"]]
        intended = sorted(str(b.relative_to(sub_dir)).replace("\\", "/") for b in bolds)
        ids = set()
        for f in fmaps:
            side = _sidecar(f)
            shutil.copy2(side, backup_dir / side.name)
            meta = json.loads(side.read_text())
            meta["IntendedFor"] = intended
            if meta.get("B0FieldIdentifier"):
                ids.add(meta["B0FieldIdentifier"])
            side.write_text(json.dumps(meta, indent=2))
        source = next(iter(ids)) if len(ids) == 1 else None
        if source:
            for b in bolds:
                side = _sidecar(b)
                shutil.copy2(side, backup_dir / side.name)
                meta = json.loads(side.read_text())
                meta["B0FieldSource"] = source
                side.write_text(json.dumps(meta, indent=2))
        info["intended_for"] = intended
        info["b0_field_source"] = source


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="link field maps or fall back to SyN")
    ap.add_argument("--sub-dir", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    ap.add_argument("--backup-dir", type=Path, required=True)
    a = ap.parse_args(argv)
    receipt = plan(a.sub_dir)
    if receipt["sdc_path"] == "fieldmaps":
        apply_links(a.sub_dir, receipt, a.backup_dir)
    a.receipt.parent.mkdir(parents=True, exist_ok=True)
    a.receipt.write_text(json.dumps(receipt, indent=2))
    print(receipt["sdc_path"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
