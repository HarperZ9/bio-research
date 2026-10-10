"""Visual and numeric QC for the AFNI path: registration overlay and tSNR.

  python -I -m conn01.afni_qc overlay --template T.nii.gz --t1w T1_in_MNI.nii.gz \
      --epi BOLD_mean.nii.gz --out sub-X_desc-afnireg.png
  python -I -m conn01.afni_qc tsnr --bold B --mask M --tr 0.8 --skip 0

tSNR is the voxel mean over time divided by the standard deviation of the
residual after the DCT drift basis (128 s) is removed, using the volumes
after any non-steady-state volumes. It reports the median over the brain
mask and over each study region. These are signal-quality numbers; no
correlation between regions is computed here.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from . import afni_confounds as ac

CHUNK = 64


def tsnr_map(data: np.ndarray, tr: float) -> np.ndarray:
    """tSNR per row of a (voxels, time) array."""
    x = ac.cosine_drift(data.shape[1], tr)
    beta = np.linalg.lstsq(x, data.T.astype(np.float64), rcond=None)[0]
    resid = data - (x @ beta).T
    sd = resid.std(axis=1)
    mean = data.mean(axis=1)
    out = np.zeros(len(sd))
    ok = sd > 0
    out[ok] = mean[ok] / sd[ok]
    return out


def tsnr_summary(bold: Path, mask: Path, tr: float, skip: int,
                 regions: dict[str, np.ndarray] | None = None) -> dict:
    """Median tSNR in the brain mask and, if given, in each region mask."""
    import nibabel as nib

    img = nib.load(str(bold))
    brain = np.asarray(nib.load(str(mask)).dataobj) > 0
    n_t = img.shape[3]
    vox = np.empty((int(brain.sum()), n_t - skip), np.float32)
    for t0 in range(skip, n_t, CHUNK):
        t1 = min(n_t, t0 + CHUNK)
        vox[:, t0 - skip:t1 - skip] = np.asarray(img.dataobj[..., t0:t1], np.float32)[brain]
    tmap = np.zeros(brain.shape)
    tmap[brain] = tsnr_map(vox, tr)
    out = {"brain_median": float(np.median(tmap[brain]))}
    for name, m in (regions or {}).items():
        sel = m & brain
        out[f"{name}_median"] = float(np.median(tmap[sel])) if sel.any() else float("nan")
        out[f"{name}_in_mask_fraction"] = float(sel.sum() / max(int(m.sum()), 1))
    return out


def _edges(vol: np.ndarray) -> np.ndarray:
    """Boolean edge map of a thresholded volume (a thin outline)."""
    from scipy.ndimage import binary_erosion

    pos = vol[vol > 0]
    if pos.size == 0:
        return np.zeros(vol.shape, bool)
    m = vol > np.percentile(pos, 40)
    return m & ~binary_erosion(m)


def overlay_png(template: Path, t1w: Path, epi: Path, out: Path) -> None:
    """3 x 3 panel: template with warped-T1 edges, mean EPI with template edges."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import nibabel as nib
    from nilearn.image import resample_to_img

    tpl = nib.load(str(template))
    vols = [np.asarray(resample_to_img(nib.load(str(p)), tpl, force_resample=True,
                                       copy_header=True).dataobj, float)
            for p in (t1w, epi)]
    t = np.asarray(tpl.dataobj, float)
    tpl_e = _edges(t)
    rows = [("template + warped T1 edges", t, _edges(vols[0])),
            ("warped T1 + template edges", vols[0], tpl_e),
            ("mean EPI + template edges", vols[1], tpl_e)]
    c = [s // 2 for s in t.shape]
    c[2] = int(t.shape[2] * 0.4)  # axial through amygdala / orbitofrontal level
    fig, axes = plt.subplots(3, 3, figsize=(10, 10))
    for r, (title, bg, edge) in enumerate(rows):
        for k in range(3):
            sl = [slice(None)] * 3
            sl[k] = c[k]
            ax = axes[r, k]
            ax.imshow(np.rot90(bg[tuple(sl)]), cmap="gray")
            ov = np.ma.masked_where(~np.rot90(edge[tuple(sl)]), np.rot90(edge[tuple(sl)]))
            ax.imshow(ov, cmap="autumn", alpha=0.9, interpolation="none")
            ax.set_axis_off()
        axes[r, 0].set_title(title, loc="left", fontsize=9)
    fig.tight_layout()
    fig.savefig(str(out), dpi=90)
    plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="AFNI-path QC")
    sp = ap.add_subparsers(dest="cmd", required=True)
    o = sp.add_parser("overlay")
    for k in ("template", "t1w", "epi", "out"):
        o.add_argument(f"--{k}", type=Path, required=True)
    t = sp.add_parser("tsnr")
    t.add_argument("--bold", type=Path, required=True)
    t.add_argument("--mask", type=Path, required=True)
    t.add_argument("--tr", type=float, required=True)
    t.add_argument("--skip", type=int, default=0)
    a = ap.parse_args(argv)
    if a.cmd == "overlay":
        overlay_png(a.template, a.t1w, a.epi, a.out)
        print(f"[afni_qc] wrote {a.out}")
        return 0
    import nibabel as nib

    from . import atlas

    ref = nib.load(str(a.mask))
    masks, _ = atlas.load_masks(reference_img=ref)
    keep = {k: masks[k] for k in ("amygdala_bilateral", "vmpfc_fmc", "subcallosal")}
    print(json.dumps(tsnr_summary(a.bold, a.mask, a.tr, a.skip, keep)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
