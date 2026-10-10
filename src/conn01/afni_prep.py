"""Helpers that scripts/run_afni_one.sh calls around afni_proc.py (deviation 4).

  python -I -m conn01.afni_prep blip-plan --sub-dir BIDS/sub-X --receipt R.json
      one line per rest run: BOLD<TAB>FORWARD<TAB>REVERSE (or none none)
  python -I -m conn01.afni_prep slice-times --bold-json J --out F.1D
  python -I -m conn01.afni_prep nss --bold B.nii.gz
  python -I -m conn01.afni_prep acompcor-masks --gm G --wm W --csf C --out-dir D
  python -I -m conn01.afni_prep confounds --bold B --mask M --pv-dir D \
      --dfile motion.1D --tr 0.8 --skip 0 --out-tsv X_desc-confounds_timeseries.tsv

blip-plan reuses fmaplink's compatibility check (opposite phase-encoding
pair on the BOLD axis, same geometry). For each run the forward field map is
the one whose PhaseEncodingDirection equals the run's; the reverse is the
other. If fmaplink rejects the participant, no distortion correction is
applied in the AFNI path (AFNI has no field-map-less SyN equivalent), and the
receipt says so.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from . import afni_confounds as ac
from . import fmaplink

CHUNK = 64
PV_THRESHOLD = 0.99  # fMRIPrep Binarize(thresh_low=0.99) after the brain mask


def _pe(nifti: Path) -> str:
    side = nifti.with_name(nifti.name.replace(".nii.gz", ".json"))
    return json.loads(side.read_text()).get("PhaseEncodingDirection", "")


def blip_plan(sub_dir: Path, geometry=fmaplink.default_geometry) -> dict:
    """fmaplink decision plus a forward/reverse field map per rest run."""
    receipt = fmaplink.plan(sub_dir, geometry)
    runs = {}
    for info in receipt["sessions"].values():
        fmaps = [next(sub_dir.glob(f"**/fmap/{n}")) for n in info["fieldmaps"]]
        for name in info["bold"]:
            bold = next(sub_dir.glob(f"**/func/{name}"))
            pair = {"forward": None, "reverse": None}
            if receipt["sdc_path"] == "fieldmaps":
                pe = _pe(bold)
                pair["forward"] = next(str(f) for f in fmaps if _pe(f) == pe)
                pair["reverse"] = next(str(f) for f in fmaps if _pe(f) != pe)
            runs[str(bold)] = pair
    receipt["afni_sdc"] = "blip_reverse" if receipt["sdc_path"] == "fieldmaps" else "none"
    receipt["runs"] = runs
    return receipt


def slice_times(bold_json: Path) -> list[float]:
    meta = json.loads(Path(bold_json).read_text())
    times = meta.get("SliceTiming")
    if not times:
        raise KeyError(f"{bold_json}: no SliceTiming")
    return [float(t) for t in times]


def volume_means(bold: Path, n: int | None = None) -> np.ndarray:
    """Whole-image mean per volume (nipype NonSteadyStateDetector input)."""
    import nibabel as nib

    img = nib.load(str(bold))
    n_t = img.shape[3] if n is None else min(n, img.shape[3])
    return np.asarray(img.dataobj[..., :n_t], dtype=np.float32).mean(axis=(0, 1, 2))


def acompcor_pv_masks(gm: np.ndarray, wm: np.ndarray, csf: np.ndarray) -> dict:
    """fMRIPrep acompcor_masks (partial-volume route) on anatomical-space arrays.

    GM > 0.05, dilated by a radius-3 ball, is removed from WM and from the
    combined CSF+WM map; the CSF map is passed through, as in fMRIPrep.
    """
    from scipy.ndimage import binary_dilation

    r = 3
    z, y, x = np.mgrid[-r:r + 1, -r:r + 1, -r:r + 1]
    ball = (x ** 2 + y ** 2 + z ** 2) <= r * r
    gm_d = binary_dilation(gm > 0.05, structure=ball)
    wm = np.array(wm, dtype=np.float32)
    wm[gm_d] = 0
    comb = np.array(csf, dtype=np.float32) + wm
    comb[gm_d] = 0
    return {"CSF": np.array(csf, dtype=np.float32), "WM": wm, "combined": comb}


def masked_series(bold: Path, masks: dict[str, np.ndarray],
                  brain: np.ndarray) -> tuple[dict, np.ndarray]:
    """(voxels, time) arrays per mask and the brain-mask mean, read in chunks."""
    import nibabel as nib

    img = nib.load(str(bold))
    n_t = img.shape[3]
    out = {k: np.empty((int(m.sum()), n_t), np.float32) for k, m in masks.items()}
    gs = np.empty(n_t)
    for t0 in range(0, n_t, CHUNK):
        t1 = min(n_t, t0 + CHUNK)
        block = np.asarray(img.dataobj[..., t0:t1], dtype=np.float32)
        for k, m in masks.items():
            out[k][:, t0:t1] = block[m]
        gs[t0:t1] = block[brain].mean(axis=0)
    return out, gs


def write_confounds(bold: Path, mask: Path, pv_dir: Path, dfile: Path, tr: float,
                    skip: int, out_tsv: Path) -> dict:
    """Binarize the warped PV maps inside the brain mask, then build confounds."""
    import nibabel as nib

    brain = np.asarray(nib.load(str(mask)).dataobj) > 0
    masks = {}
    for k in ("CSF", "WM", "combined"):
        pv = np.asarray(nib.load(str(pv_dir / f"acompcor_{k}.nii.gz")).dataobj, float)
        masks[k] = (pv * brain) > PV_THRESHOLD
    series, gs = masked_series(bold, masks, brain)
    table, meta = ac.build_confounds(np.loadtxt(dfile, ndmin=2), series, gs, tr, skip)
    table.to_csv(out_tsv, sep="\t", index=False, na_rep="n/a")
    out_tsv.with_suffix(".json").write_text(json.dumps(meta, indent=2))
    return {k: int(m.sum()) for k, m in masks.items()}


def _cmd_blip(a) -> int:
    receipt = blip_plan(a.sub_dir)
    a.receipt.parent.mkdir(parents=True, exist_ok=True)
    a.receipt.write_text(json.dumps(receipt, indent=2))
    for bold, pair in receipt["runs"].items():
        print(f"{bold}\t{pair['forward'] or 'none'}\t{pair['reverse'] or 'none'}")
    return 0


def _cmd_masks(a) -> int:
    import nibabel as nib

    imgs = [nib.load(str(p)) for p in (a.gm, a.wm, a.csf)]
    gm, wm, csf = (np.asarray(i.dataobj, float) for i in imgs)
    a.out_dir.mkdir(parents=True, exist_ok=True)
    for k, arr in acompcor_pv_masks(gm, wm, csf).items():
        nib.Nifti1Image(arr, imgs[0].affine).to_filename(str(a.out_dir / f"acompcor_{k}.nii.gz"))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="AFNI-path helpers (prereg 01 deviation 4)")
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("blip-plan")
    b.add_argument("--sub-dir", type=Path, required=True)
    b.add_argument("--receipt", type=Path, required=True)
    s = sp.add_parser("slice-times")
    s.add_argument("--bold-json", type=Path, required=True)
    s.add_argument("--out", type=Path, required=True)
    n = sp.add_parser("nss")
    n.add_argument("--bold", type=Path, required=True)
    m = sp.add_parser("acompcor-masks")
    for k in ("gm", "wm", "csf", "out_dir"):
        m.add_argument(f"--{k.replace('_', '-')}", dest=k, type=Path, required=True)
    c = sp.add_parser("confounds")
    for k in ("bold", "mask", "pv_dir", "dfile", "out_tsv"):
        c.add_argument(f"--{k.replace('_', '-')}", dest=k, type=Path, required=True)
    c.add_argument("--tr", type=float, required=True)
    c.add_argument("--skip", type=int, required=True)
    a = ap.parse_args(argv)
    if a.cmd == "blip-plan":
        return _cmd_blip(a)
    if a.cmd == "slice-times":
        a.out.write_text(" ".join(f"{t:.6f}" for t in slice_times(a.bold_json)) + "\n")
        return 0
    if a.cmd == "nss":
        print(ac.non_steady_state_count(volume_means(a.bold, 50)))
        return 0
    if a.cmd == "acompcor-masks":
        return _cmd_masks(a)
    counts = write_confounds(a.bold, a.mask, a.pv_dir, a.dfile, a.tr, a.skip, a.out_tsv)
    print(json.dumps({"mask_voxels": counts}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
