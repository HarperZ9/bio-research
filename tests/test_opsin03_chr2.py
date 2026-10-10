"""Step 1 checks on the ChR2 4-state and 6-state models: controls and scaling.

Run with the opsin venv: H:/bio-data/venvs/opsin/Scripts/python -m pytest
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opsin03.chr2 import (MODELS, irradiance_to_flux, simulate_pulse,  # noqa: E402
                          steady_state)
from opsin03.metrics import peak  # noqa: E402

SWEEP = [0.01, 0.1, 1.0, 10.0, 100.0, 1e3, 1e4, 1e5]  # mW/mm^2


@pytest.mark.parametrize("name", list(MODELS))
def test_no_light_gives_zero_current(name):
    tr = simulate_pulse(MODELS[name], 0.0, 500.0)
    assert np.max(np.abs(tr.current)) == 0.0
    assert np.allclose(tr.states[:, 0], 1.0)


@pytest.mark.parametrize("name", list(MODELS))
def test_state_occupancy_is_conserved(name):
    tr = simulate_pulse(MODELS[name], 10.0, 500.0)
    total = tr.states.sum(axis=1)
    assert np.max(np.abs(total - 1.0)) < 1e-6
    assert tr.states.min() > -1e-9


@pytest.mark.parametrize("name", list(MODELS))
def test_long_light_reaches_analytic_steady_state(name):
    """10 s of light: integrated states match the null vector of the generator."""
    prm = MODELS[name]
    tr = simulate_pulse(prm, 5.0, 10000.0, post_ms=1.0, dt=1.0)
    ss = steady_state(prm, irradiance_to_flux(5.0))
    end_light = np.searchsorted(tr.t, tr.off)
    assert np.max(np.abs(tr.states[end_light] - ss)) < 1e-4


def test_irradiance_conversion_matches_photon_energy():
    # 1 mW/mm^2 at 470 nm: E_photon = hc/lambda = 4.2265e-19 J
    assert irradiance_to_flux(1.0) == pytest.approx(2.366e15, rel=1e-3)


@pytest.fixture(scope="module")
def peak_sweep():
    return {n: [peak(simulate_pulse(p, e, 50.0, post_ms=1.0)) for e in SWEEP]
            for n, p in MODELS.items()}


@pytest.mark.parametrize("name", [
    "4state",
    pytest.param("6state", marks=pytest.mark.xfail(strict=True, reason=(
        "Observed 2026-10-09: 6-state peak falls from 1.463 nA at 100 to "
        "1.392 nA at 1e4 mW/mm2; dt-independent, a property of the set."))),
])
def test_peak_increases_monotonically_with_irradiance(name, peak_sweep):
    peaks = np.array(peak_sweep[name])
    assert peaks[0] > 0.0
    assert np.all(np.diff(peaks) > 0.0), peaks


@pytest.mark.parametrize("name", list(MODELS))
def test_peak_saturates_at_high_irradiance(name, peak_sweep):
    """Gain per decade falls, and the top decade adds less than 5%."""
    peaks = np.array(peak_sweep[name])
    gain = peaks[1:] / peaks[:-1]
    assert gain[-1] < 1.05, gain
    assert gain[-1] < gain[2] < gain[0], gain


@pytest.mark.parametrize("name", list(MODELS))
def test_peak_monotonic_within_experimental_range(name):
    """Added after the full-sweep result: 0.01 to 19.8 mW/mm^2 only, the
    range Lin et al. 2009 used (max 19.8). Narrower claim, labeled post hoc."""
    irrs = [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 19.8]
    peaks = np.array([peak(simulate_pulse(MODELS[name], e, 50.0, post_ms=1.0))
                      for e in irrs])
    assert np.all(np.diff(peaks) > 0.0), peaks
