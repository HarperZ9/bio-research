"""Synthetic fMRIPrep-like confounds and region signals for conn01 tests."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from conn01 import denoise as dn  # noqa: E402

REGIONS = ["amygdala_l", "amygdala_r", "amygdala_bilateral", "vmpfc_fmc",
           "subcallosal"]


def confounds(t: int, rng: np.random.Generator, fd: np.ndarray | None = None,
              n_wm: int = 7, n_csf: int = 7) -> tuple[pd.DataFrame, dict]:
    """Confounds table and JSON metadata shaped like fMRIPrep output."""
    cols = {c: rng.normal(size=t) for c in dn.MOTION_24}
    for c in dn.MOTION_24:
        if "derivative1" in c:
            cols[c][0] = np.nan
    meta = {}
    idx = 0
    for mask, n in (("CSF", n_csf), ("WM", n_wm), ("combined", 3)):
        for j in range(n):
            name = f"a_comp_cor_{idx:02d}"
            cols[name] = rng.normal(size=t)
            meta[name] = {"Mask": mask, "Retained": True,
                          "SingularValue": float(100 - j)}
            idx += 1
    tt = np.arange(t)
    for j in range(4):
        cols[f"cosine{j:02d}"] = np.cos(np.pi * (j + 1) * (tt + 0.5) / t)
    cols["global_signal"] = rng.normal(size=t)
    if fd is None:
        fd = np.abs(rng.normal(0.1, 0.03, size=t))
    fd = np.array(fd, float)
    fd[0] = np.nan
    cols["framewise_displacement"] = fd
    return pd.DataFrame(cols), meta


def regions(conf: pd.DataFrame, rng: np.random.Generator, coupling: float,
            nuisance_scale: float = 3.0) -> pd.DataFrame:
    """Region signals: shared neural signal plus large confound-driven noise.

    Each region is shared * sqrt(c) + own * sqrt(1 - c) with unit-variance
    parts, so after the nuisance regressors are removed any two regions
    correlate at c = coupling in expectation.
    """
    t = len(conf)
    nuis = conf[["trans_x", "rot_y", "a_comp_cor_07", "a_comp_cor_00",
                 "cosine00"]].fillna(0).to_numpy()
    shared = rng.normal(size=t)
    out = {}
    for name in REGIONS:
        own = rng.normal(size=t)
        sig = np.sqrt(coupling) * shared + np.sqrt(1 - coupling) * own
        w = rng.normal(size=nuis.shape[1]) * nuisance_scale
        out[name] = 100 + sig + nuis @ w
    return pd.DataFrame(out)
