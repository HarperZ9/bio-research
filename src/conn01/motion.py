"""Filtered framewise displacement (prereg 01 deviations 5 and 5a).

All FD here is Power FD: the sum of absolute backward differences of the six
rigid-body parameters, rotations converted to mm on a 50 mm sphere, with
FD[0] = 0. The 24 motion regressors used in denoising are never filtered.

Low-pass (deviation 5a, the primary rule): each parameter is low-pass
filtered at 0.1 Hz with a first-order Butterworth filter, applied forward and
backward (scipy filtfilt, zero phase), after Gratton et al. 2020. Padding:
Gratton et al. zero-padded 100 frames. Here each end is padded with 100
mirrored frames (filtfilt padtype "even", fewer for runs shorter than 101
frames). On synthetic 0.35 Hz breathing at TR 0.8 s, odd (point-symmetric)
padding, the scipy default, left end-of-run FD up to 0.18 mm, above the
0.1 mm threshold; mirrored padding kept the end frames within 0.02 mm of the
interior (tests/test_conn01_motion.py). Gratton et al. validated the
low-pass on single-band data; here it is used on TR 0.8 s multiband data,
outside that setting.

Band-stop (deviation 5, now a sensitivity rule): 0.31 to 0.43 Hz, the ABCD
approach for TR 0.8 s multiband data (Fair et al. 2020); Butterworth design
order 4 (order 8 band-stop), second-order sections, sosfiltfilt. Known limit:
with a large breathing oscillation a few volumes at each run end exceed
0.2 mm (synthetic 0.4 mm breathing: 0 to 6 of 488 volumes, all within 10
volumes of an end). No edge rule is added.

Both filters are defined in Hz, so the digital cutoffs follow the run's TR.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, sosfiltfilt

MOTION_6 = ["trans_x", "trans_y", "trans_z", "rot_x", "rot_y", "rot_z"]
HEAD_RADIUS_MM = 50.0
RESP_BAND_HZ = (0.31, 0.43)
FILTER_ORDER = 4
LOWPASS_HZ = 0.1
LOWPASS_ORDER = 1
LOWPASS_PAD_FRAMES = 100
BANDSTOP_DESC = {
    "type": "butterworth_bandstop", "design_order": FILTER_ORDER,
    "band_hz": list(RESP_BAND_HZ), "zero_phase": "sosfiltfilt (forward-backward)",
    "fd": "Power, 50 mm head radius",
}
LOWPASS_DESC = {
    "type": "butterworth_lowpass", "order": LOWPASS_ORDER, "cutoff_hz": LOWPASS_HZ,
    "zero_phase": "filtfilt (forward-backward)",
    "padding": f"{LOWPASS_PAD_FRAMES} mirrored frames per end",
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
    (TR >= about 1.16 s for 0.31 to 0.43 Hz): the band-stop rule is then not
    defined for that run and must not silently fall back.
    """
    nyq = _nyquist(tr)
    lo, hi = band
    if not 0 < lo < hi < nyq:
        raise ValueError(f"band {band} Hz does not fit below Nyquist {nyq:.3f} Hz "
                         f"(TR {tr} s)")
    sos = butter(FILTER_ORDER, [lo / nyq, hi / nyq], btype="bandstop", output="sos")
    return sosfiltfilt(sos, np.asarray(params, float), axis=0)


def _nyquist(tr: float) -> float:
    if not tr or not np.isfinite(tr) or tr <= 0:
        raise ValueError(f"invalid repetition time: {tr!r}")
    return 0.5 / tr


def lowpass(params: np.ndarray, tr: float, cutoff: float = LOWPASS_HZ,
            pad: int = LOWPASS_PAD_FRAMES) -> np.ndarray:
    """Zero-phase first-order Butterworth low-pass with mirrored padding."""
    nyq = _nyquist(tr)
    if not 0 < cutoff < nyq:
        raise ValueError(f"cutoff {cutoff} Hz not below Nyquist {nyq:.3f} Hz (TR {tr} s)")
    x = np.asarray(params, float)
    b, a = butter(LOWPASS_ORDER, cutoff / nyq, btype="low")
    return filtfilt(b, a, x, axis=0, padtype="even", padlen=min(pad, len(x) - 1))


def motion_params(confounds: pd.DataFrame) -> np.ndarray:
    """The six base parameters; gaps are filled from the nearest value."""
    missing = [c for c in MOTION_6 if c not in confounds.columns]
    if missing:
        raise KeyError(f"confounds missing motion columns: {missing}")
    return confounds[MOTION_6].astype(float).ffill().bfill().to_numpy()


def bandstop_fd(confounds: pd.DataFrame, tr: float) -> np.ndarray:
    """Power FD of the band-stop filtered motion parameters; FD[0] = 0."""
    return power_fd(bandstop(motion_params(confounds), tr))


def lowpass_fd(confounds: pd.DataFrame, tr: float) -> np.ndarray:
    """Power FD of the 0.1 Hz low-pass filtered motion parameters; FD[0] = 0."""
    return power_fd(lowpass(motion_params(confounds), tr))


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
