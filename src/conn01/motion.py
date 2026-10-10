"""Respiration-filtered framewise displacement (prereg 01 deviation 5).

FD for censoring and run exclusion is Power FD (sum of absolute backward
differences of the six rigid-body parameters, rotations converted to mm on a
50 mm sphere) computed after a zero-phase band-stop filter of the six
parameters at 0.31 to 0.43 Hz, the respiration band removed in the ABCD
approach for TR 0.8 s multiband data (Fair et al. 2020). The 24 motion
regressors used in denoising are not filtered.

Filter: Butterworth band-stop, design order 4 (order 8 band-stop), in
second-order sections, applied forward and backward (scipy sosfiltfilt, the
zero-phase filtfilt method), so the magnitude response is squared and there
is no phase shift. The band is defined in Hz, so the digital edges depend on
the run's repetition time.

Known limit: a forward-backward IIR filter has an edge transient. With a
large breathing oscillation, a few volumes at each end of a run can exceed
0.2 mm filtered FD and are censored (synthetic 0.4 mm breathing at TR 0.8 s:
0 to 6 volumes of 488, all within 10 volumes of a run end). No edge rule is
added; the counts are in the QC JSON.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt

MOTION_6 = ["trans_x", "trans_y", "trans_z", "rot_x", "rot_y", "rot_z"]
HEAD_RADIUS_MM = 50.0
RESP_BAND_HZ = (0.31, 0.43)
FILTER_ORDER = 4
FILTER_DESC = {
    "type": "butterworth_bandstop", "design_order": FILTER_ORDER,
    "band_hz": list(RESP_BAND_HZ), "zero_phase": "sosfiltfilt (forward-backward)",
    "fd": "Power, 50 mm head radius",
}


def power_fd(params: np.ndarray, radius: float = HEAD_RADIUS_MM) -> np.ndarray:
    """Power FD from a (t, 6) array of trans (mm) and rot (rad); FD[0] = 0."""
    p = np.asarray(params, float)
    d = np.abs(np.diff(p, axis=0))
    d[:, 3:] *= radius
    return np.concatenate([[0.0], d.sum(axis=1)])


def bandstop(params: np.ndarray, tr: float,
             band: tuple[float, float] = RESP_BAND_HZ) -> np.ndarray:
    """Zero-phase band-stop of each column of a (t, k) array sampled at TR s.

    Raises ValueError when the band does not fit below the Nyquist frequency
    (TR >= about 1.16 s for 0.31 to 0.43 Hz): the filtered rule is then not
    defined for that run and must not silently fall back.
    """
    if not tr or not np.isfinite(tr) or tr <= 0:
        raise ValueError(f"invalid repetition time: {tr!r}")
    nyq = 0.5 / tr
    lo, hi = band
    if not 0 < lo < hi < nyq:
        raise ValueError(f"band {band} Hz does not fit below Nyquist {nyq:.3f} Hz "
                         f"(TR {tr} s)")
    sos = butter(FILTER_ORDER, [lo / nyq, hi / nyq], btype="bandstop", output="sos")
    return sosfiltfilt(sos, np.asarray(params, float), axis=0)


def motion_params(confounds: pd.DataFrame) -> np.ndarray:
    """The six base parameters; gaps are filled from the nearest value."""
    missing = [c for c in MOTION_6 if c not in confounds.columns]
    if missing:
        raise KeyError(f"confounds missing motion columns: {missing}")
    return confounds[MOTION_6].astype(float).ffill().bfill().to_numpy()


def filtered_fd(confounds: pd.DataFrame, tr: float) -> np.ndarray:
    """Power FD of the band-stop filtered motion parameters; FD[0] = 0."""
    return power_fd(bandstop(motion_params(confounds), tr))


def raw_fd(confounds: pd.DataFrame) -> np.ndarray:
    """Power FD of the unfiltered parameters (check against fMRIPrep's column)."""
    return power_fd(motion_params(confounds))


def repetition_time(meta: dict | None, sidecar: dict | None = None) -> float:
    """TR in seconds from the BOLD sidecar, else from the confounds JSON."""
    for src in (sidecar or {}, meta or {}):
        tr = src.get("RepetitionTime")
        if tr is not None:
            return float(tr)
    raise KeyError("RepetitionTime not found in the BOLD sidecar or confounds JSON")
