"""Harvard-Oxford region masks, 50% threshold, MNI152NLin2009cAsym 2 mm.

Source: TemplateFlow images tpl-MNI152NLin2009cAsym_res-02_atlas-{HOSPA,HOCPA}
_desc-th50_dseg.nii.gz (Harvard-Oxford maximum-probability labels, voxels
below 50% probability set to background).

Label values were checked on 2026-10-09: the TemplateFlow MNI152NLin6Asym
th50 images match nilearn's FSL "sub/cort-maxprob-thr50-2mm" images voxel for
voxel, and in that scheme Left Amygdala = 10, Right Amygdala = 20 (subcortical),
Frontal Medial Cortex = 25, Subcallosal Cortex = 27 (cortical). The same label
scheme is used by the MNI152NLin2009cAsym resampling of the atlas.
"""
from __future__ import annotations

import os

import numpy as np

SUBCORTICAL = "HOSPA"
CORTICAL = "HOCPA"

# region name -> (atlas, label values)
REGIONS: dict[str, tuple[str, tuple[int, ...]]] = {
    "amygdala_l": (SUBCORTICAL, (10,)),
    "amygdala_r": (SUBCORTICAL, (20,)),
    "amygdala_bilateral": (SUBCORTICAL, (10, 20)),
    "vmpfc_fmc": (CORTICAL, (25,)),
    "subcallosal": (CORTICAL, (27,)),
}

TEMPLATE = "MNI152NLin2009cAsym"
DEFAULT_TF_HOME = "/mnt/h/bio-data/templateflow"


def atlas_path(atlas: str) -> str:
    """Fetch (or reuse) the 2 mm th50 label image for one atlas."""
    os.environ.setdefault("TEMPLATEFLOW_HOME", DEFAULT_TF_HOME)
    from templateflow import api as tf

    path = tf.get(TEMPLATE, resolution=2, atlas=atlas, desc="th50",
                  suffix="dseg", extension=".nii.gz")
    if not path:
        raise FileNotFoundError(f"TemplateFlow returned nothing for {atlas}")
    return str(path)


def masks_from_labels(labels: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Build boolean masks for every region from atlas label arrays."""
    out = {}
    for name, (atlas, values) in REGIONS.items():
        mask = np.isin(labels[atlas], values)
        if not mask.any():
            raise ValueError(f"region {name} is empty in atlas {atlas}")
        out[name] = mask
    return out


def load_masks(reference_img=None):
    """Return (masks, affine) on the atlas grid, or on reference_img's grid.

    If a reference image is given and its grid differs from the atlas grid,
    the label image is resampled with nearest-neighbour interpolation.
    """
    import nibabel as nib

    labels, affine = {}, None
    for atlas in (SUBCORTICAL, CORTICAL):
        img = nib.load(atlas_path(atlas))
        if reference_img is not None and not _same_grid(img, reference_img):
            from nilearn.image import resample_to_img

            img = resample_to_img(img, reference_img, interpolation="nearest",
                                  force_resample=True, copy_header=True)
        labels[atlas] = np.asarray(img.dataobj).astype(int)
        affine = img.affine
    return masks_from_labels(labels), affine


def _same_grid(a, b) -> bool:
    return a.shape[:3] == b.shape[:3] and np.allclose(a.affine, b.affine, atol=1e-3)


def region_means(data: np.ndarray, masks: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Mean time series per region from a 4D array (x, y, z, t)."""
    if data.ndim != 4:
        raise ValueError(f"expected 4D BOLD data, got shape {data.shape}")
    out = {}
    for name, mask in masks.items():
        if mask.shape != data.shape[:3]:
            raise ValueError(f"mask {name} shape {mask.shape} != BOLD {data.shape[:3]}")
        out[name] = data[mask].mean(axis=0)
    return out
