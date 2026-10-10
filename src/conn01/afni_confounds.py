"""fMRIPrep-format confounds for the AFNI fallback path (prereg 01, deviation 4).

The AFNI path must feed extract.py and denoise.py unchanged, so this module
writes the same confounds table and JSON that fMRIPrep 25.2 writes, with the
same algorithms where denoise.py reads the column:

  * trans_x..rot_z (mm, rad) from the 3dvolreg parameters, plus the
    fMRIPrep expansion _derivative1, _power2, _derivative1_power2
    (first derivative row n/a), giving the 24 motion parameters;
  * framewise_displacement: Power FD, sum of absolute backward differences,
    rotations as arc length on a 50 mm sphere, first row n/a;
  * aCompCor as nipype's compute_noise_components: initial non-steady-state
    volumes dropped, DCT high-pass (128 s), column-wise variance
    normalisation, SVD, components retained up to 50% cumulative variance,
    separately for the CSF, WM and combined masks; named c_comp_cor_XX,
    w_comp_cor_XX and a_comp_cor_XX as in fMRIPrep >= 21;
  * cosineXX (non-constant DCT columns) and non_steady_state_outlierXX;
  * global_signal, csf, white_matter means and their expansions.

Ported from the fMRIPrep 25.2.6 container sources (fmriprep/interfaces/
confounds.py, nipype/algorithms/confounds.py); no code is imported from them.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

FD_RADIUS_MM = 50.0
HIGH_PASS_PERIOD_S = 128.0
VARIANCE_THRESHOLD = 0.5
MASK_PREFIX = {"CSF": "c_comp_cor_", "WM": "w_comp_cor_", "combined": "a_comp_cor_"}
MOTION_COLS = ["trans_x", "trans_y", "trans_z", "rot_x", "rot_y", "rot_z"]


def afni_motion_to_fmriprep(dfile: np.ndarray) -> pd.DataFrame:
    """3dvolreg -1Dfile columns (roll pitch yaw dS dL dP; deg, mm) to fMRIPrep.

    AFNI roll is about I-S, pitch about R-L, yaw about A-P. fMRIPrep rot_x is
    about the left-right axis, rot_y about anterior-posterior, rot_z about
    superior-inferior. Signs may differ between conventions; the 24-parameter
    regression and FD are invariant to sign.
    """
    d = np.asarray(dfile, float)
    if d.ndim != 2 or d.shape[1] != 6:
        raise ValueError(f"expected n x 6 volreg parameters, got {d.shape}")
    roll, pitch, yaw, d_s, d_l, d_p = d.T
    return pd.DataFrame({
        "trans_x": d_l, "trans_y": d_p, "trans_z": d_s,
        "rot_x": np.deg2rad(pitch), "rot_y": np.deg2rad(yaw), "rot_z": np.deg2rad(roll),
    })


def expand_dd1_squared(df: pd.DataFrame) -> pd.DataFrame:
    """fMRIPrep '(dd1(x))^^2': x, x_derivative1, x_power2, x_derivative1_power2."""
    out = {}
    for c in df.columns:
        x = df[c].astype(float)
        d1 = x.diff()  # first row NaN, as in fMRIPrep
        out[c] = x
        out[f"{c}_derivative1"] = d1
        out[f"{c}_power2"] = x ** 2
        out[f"{c}_derivative1_power2"] = d1 ** 2
    return pd.DataFrame(out)


def framewise_displacement(motion: pd.DataFrame, radius: float = FD_RADIUS_MM) -> np.ndarray:
    """Power FD as in fMRIPrep's FramewiseDisplacement interface."""
    diff = motion[MOTION_COLS].diff()
    diff[["rot_x", "rot_y", "rot_z"]] *= radius
    return diff.abs().sum(axis=1, skipna=False).to_numpy(float)


def cosine_drift(n: int, tr: float, period_cut: float = HIGH_PASS_PERIOD_S) -> np.ndarray:
    """nipype _cosine_drift: DCT-II columns with period >= period_cut, then a constant."""
    order = max(int(np.floor(2 * n * (1.0 / period_cut) * tr)), 1)
    x = np.zeros((n, order))
    t = np.arange(n)
    for k in range(1, order):
        x[:, k - 1] = np.sqrt(2.0 / n) * np.cos((np.pi / n) * (t + 0.5) * k)
    x[:, order - 1] = 1.0
    return x


def non_steady_state_count(global_signal: np.ndarray, thresh: float = 3.5) -> int:
    """nipype is_outlier on the first 50 volumes' whole-image mean."""
    g = np.asarray(global_signal, float)[:50]
    diff = np.abs(g - np.median(g))
    mad = np.median(diff)
    if mad == 0:
        return 0
    z = 0.6745 * diff / mad
    n = 0
    for value in z:
        if value <= thresh:
            break
        n += 1
    return n


def compcor(voxels: np.ndarray, tr: float, threshold: float = VARIANCE_THRESHOLD):
    """Components of a (voxels, time) matrix as nipype compute_noise_components.

    Returns (components (t, k), singular values, variance explained,
    cumulative variance, k). k is the smallest number reaching `threshold`.
    """
    v = np.array(voxels, dtype=np.float64)
    v[~np.isfinite(v.sum(axis=1))] = 0.0
    if v.shape[0] == 0:
        return np.zeros((v.shape[1], 0)), np.array([]), np.array([]), np.array([]), 0
    x = cosine_drift(v.shape[1], tr)
    beta = np.linalg.lstsq(x, v.T, rcond=None)[0]
    m = (v - (x @ beta).T).T  # time x voxels, filtered and demeaned
    sd = np.std(m, axis=0)
    sd[(sd == 0) | ~np.isfinite(sd)] = 1.0
    u, s, _ = np.linalg.svd(m / sd, full_matrices=False)
    var = s ** 2 / np.sum(s ** 2)
    cum = np.cumsum(var)
    k = int(np.searchsorted(cum, threshold) + 1)
    return u[:, :k], s, var, cum, k


def compcor_table(series: dict[str, np.ndarray], tr: float, skip: int,
                  n_vols: int) -> tuple[pd.DataFrame, dict]:
    """Retained components per mask, renamed and padded with zeros for skipped rows.

    series maps mask name ("CSF", "WM", "combined") to a (voxels, time) array.
    """
    cols, meta = {}, {}
    for mask in ("CSF", "WM", "combined"):
        comps, s, var, cum, k = compcor(series[mask][:, skip:], tr)
        for j in range(k):
            name = f"{MASK_PREFIX[mask]}{j:02d}"
            col = np.zeros(n_vols)
            col[skip:] = comps[:, j]
            cols[name] = col
            meta[name] = {"Method": "aCompCor", "Mask": mask, "Retained": True,
                          "SingularValue": float(s[j]),
                          "VarianceExplained": float(var[j]),
                          "CumulativeVarianceExplained": float(cum[j])}
    return pd.DataFrame(cols, index=range(n_vols)), meta


def cosine_and_nss(n_vols: int, tr: float, skip: int) -> pd.DataFrame:
    """cosineXX columns (zero on skipped rows) and one indicator per skipped volume."""
    basis = cosine_drift(n_vols - skip, tr)[:, :-1]
    out = {}
    for j in range(basis.shape[1]):
        col = np.zeros(n_vols)
        col[skip:] = basis[:, j]
        out[f"cosine{j:02d}"] = col
    for j in range(skip):
        col = np.zeros(n_vols)
        col[j] = 1.0
        out[f"non_steady_state_outlier{j:02d}"] = col
    return pd.DataFrame(out, index=range(n_vols))


def build_confounds(dfile: np.ndarray, series: dict[str, np.ndarray],
                    global_signal: np.ndarray, tr: float,
                    skip: int) -> tuple[pd.DataFrame, dict]:
    """Assemble the fMRIPrep-format confounds table and its JSON metadata."""
    motion = afni_motion_to_fmriprep(dfile)
    n = len(motion)
    if len(global_signal) != n or any(v.shape[1] != n for v in series.values()):
        raise ValueError("motion, signals and BOLD disagree on the number of volumes")
    signals = pd.DataFrame({
        "global_signal": global_signal,
        "csf": _masked_mean(series["CSF"]),
        "white_matter": _masked_mean(series["WM"]),
    })
    acc, meta = compcor_table(series, tr, skip, n)
    fd = pd.DataFrame({"framewise_displacement": framewise_displacement(motion)})
    table = pd.concat([expand_dd1_squared(signals), fd, expand_dd1_squared(motion),
                       acc, cosine_and_nss(n, tr, skip)], axis=1)
    meta.update({c: {"Method": "Mean"} for c in ("global_signal", "csf", "white_matter")})
    meta["framewise_displacement"] = {"Units": "mm"}
    meta["RepetitionTime"] = float(tr)  # read by the filtered FD rule (deviation 5)
    return table, meta


def _masked_mean(voxels: np.ndarray) -> np.ndarray:
    if voxels.shape[0] == 0:
        return np.full(voxels.shape[1], np.nan)
    return voxels.mean(axis=0)
