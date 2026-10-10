"""Summary measures of a voltage-clamp photocurrent trace.

Definitions (fixed before comparison with any reference value):
- peak: largest inward magnitude during the light pulse, nA (positive number).
- plateau: inward magnitude at the last sample of the light pulse.
- ratio: plateau / peak.
- tau_off: single-exponential fit A*exp(-t/tau) to the decay after light
  offset, over the window from offset until the magnitude first falls below
  10% of its value at offset. Lin et al. 2009 report a single closing time
  constant; their exact fit window is not stated in the text I read.
- t_1e: model-free time from offset to the first sample below 1/e of the
  offset magnitude.
"""
import numpy as np
from scipy.optimize import curve_fit


def _mask(trace, start, stop):
    return (trace.t >= start) & (trace.t <= stop)


def peak(trace):
    m = _mask(trace, trace.on, trace.off)
    return float(np.max(-trace.current[m]))


def plateau(trace):
    m = _mask(trace, trace.on, trace.off)
    return float(-trace.current[m][-1])


def ss_peak_ratio(trace):
    return plateau(trace) / peak(trace)


def _decay(trace):
    m = trace.t >= trace.off
    t = trace.t[m] - trace.off
    y = -trace.current[m]
    return t, y


def t_one_over_e(trace):
    t, y = _decay(trace)
    below = np.nonzero(y < y[0] / np.e)[0]
    return float(t[below[0]]) if below.size else float("nan")


def tau_off(trace):
    t, y = _decay(trace)
    below = np.nonzero(y < 0.1 * y[0])[0]
    stop = below[0] if below.size else len(t)
    tt, yy = t[:stop], y[:stop]
    guess = max(t_one_over_e(trace), 1.0)
    (a, tau), _ = curve_fit(lambda x, a, k: a * np.exp(-x / k), tt, yy,
                            p0=(yy[0], guess), maxfev=20000)
    return float(tau)


def summarize(trace):
    return {
        "peak_nA": peak(trace),
        "plateau_nA": plateau(trace),
        "ratio": ss_peak_ratio(trace),
        "tau_off_ms": tau_off(trace),
        "t_1e_ms": t_one_over_e(trace),
    }
