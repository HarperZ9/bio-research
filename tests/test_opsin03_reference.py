"""Step 1 comparisons: 4-state vs 6-state, Lin et al. 2009, ModelDB 244414.

Acceptance rules and sources live in src/opsin03/reference.py.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from opsin03 import reference as ref  # noqa: E402
from opsin03.chr2 import MODELS, simulate_pulse  # noqa: E402
from opsin03.metrics import peak, ss_peak_ratio, tau_off  # noqa: E402

NEURON_JSON = ROOT / "data" / "opsin03" / "neuron_williams.json"


def _peaks(prm, irrs, v=-70.0):
    return np.array([peak(simulate_pulse(prm, e, 50.0, v_mv=v, post_ms=1.0))
                     for e in irrs])


@pytest.mark.xfail(strict=True, reason=(
    "Observed 2026-10-09: 6-state peak is 77-79% below 4-state at "
    "0.5-10 mW/mm2 (g0 2.52e4 vs 1.14e5 pS). Brief criterion not met."))
def test_4state_and_6state_peak_within_10pct():
    p4 = _peaks(MODELS["4state"], ref.FIVE_IRRADIANCES)
    p6 = _peaks(MODELS["6state"], ref.FIVE_IRRADIANCES)
    rel = np.abs(p4 - p6) / p4
    assert np.all(rel <= ref.PEAK_TOLERANCE), f"4s {p4} 6s {p6} rel {rel}"


def test_4state_and_6state_normalised_shape_within_10pct():
    irrs = ref.FIVE_IRRADIANCES + [ref.NORM_IRRADIANCE]
    p4 = _peaks(MODELS["4state"], irrs)
    p6 = _peaks(MODELS["6state"], irrs)
    n4, n6 = p4[:-1] / p4[-1], p6[:-1] / p6[-1]
    rel = np.abs(n4 - n6) / n4
    assert np.all(rel <= ref.PEAK_TOLERANCE), f"4s {n4} 6s {n6} rel {rel}"


@pytest.fixture(scope="module")
def lin_traces():
    out = {}
    for name, prm in MODELS.items():
        long_ = simulate_pulse(prm, ref.NORM_IRRADIANCE, 500.0, v_mv=ref.V_LIN)
        short = simulate_pulse(prm, ref.NORM_IRRADIANCE, 10.0, v_mv=ref.V_LIN)
        out[name] = (long_, short)
    return out


def _inside(value, bounds):
    return bounds[0] <= value <= bounds[1]


@pytest.mark.xfail(strict=True, reason=(
    "Observed 2026-10-09: ratio 0.380 (4s), 0.366 (6s) at 19.8 mW/mm2; "
    "Lin 2009 WT range 0.093-0.337. Inside the H134R range instead."))
@pytest.mark.parametrize("name", list(MODELS))
def test_ss_peak_ratio_in_lin2009_wt_range(name, lin_traces):
    r = ss_peak_ratio(lin_traces[name][0])
    assert _inside(r, ref.LIN2009_WT["ratio"]), (r, ref.LIN2009_WT["ratio"])


@pytest.mark.parametrize("name", list(MODELS))
def test_tau_off_500ms_in_lin2009_wt_range(name, lin_traces):
    tau = tau_off(lin_traces[name][0])
    bounds = ref.LIN2009_WT["tau_off_500ms"]
    assert _inside(tau, bounds), (tau, bounds)


@pytest.mark.parametrize("name", list(MODELS))
def test_tau_off_10ms_in_lin2009_wt_range(name, lin_traces):
    tau = tau_off(lin_traces[name][1])
    bounds = ref.LIN2009_WT["tau_off_10ms"]
    assert _inside(tau, bounds), (tau, bounds)


@pytest.mark.xfail(strict=True, reason=(
    "Observed 2026-10-09: tau_off 10 ms / 500 ms = 0.49 (4s), 0.48 (6s); "
    "Lin 2009 reports duration-independent closure (0.99)."))
@pytest.mark.parametrize("name", list(MODELS))
def test_tau_off_independent_of_duration(name, lin_traces):
    ratio = tau_off(lin_traces[name][1]) / tau_off(lin_traces[name][0])
    assert _inside(ratio, ref.DURATION_INDEPENDENCE), ratio


def _neuron():
    if not NEURON_JSON.exists():
        pytest.skip("run scripts/opsin03_neuron_williams.py in WSL first")
    return json.loads(NEURON_JSON.read_text())


def test_neuron_williams_no_light_is_zero():
    assert _neuron()["no_light_max_abs_current"] == 0.0


@pytest.mark.xfail(strict=True, reason=(
    "Observed 2026-10-09: 4-state normalised peaks differ from ModelDB "
    "244414 by 25, 22, 18, 10, 4% at 0.5, 1, 2, 5, 10 mW/mm2."))
def test_4state_normalised_peaks_within_10pct_of_neuron_williams():
    """Shape only: the NEURON model reports mA/cm2, PyRhO reports nA."""
    runs = [r for r in _neuron()["runs"] if r["v_mV"] == -70.0]
    by_irr = {r["irr_mW_mm2"]: r["peak_mA_cm2"] for r in runs}
    nrn = np.array([by_irr[e] for e in ref.FIVE_IRRADIANCES])
    nrn = nrn / by_irr[ref.NORM_IRRADIANCE]
    p4 = _peaks(MODELS["4state"], ref.FIVE_IRRADIANCES + [ref.NORM_IRRADIANCE])
    n4 = p4[:-1] / p4[-1]
    rel = np.abs(n4 - nrn) / nrn
    assert np.all(rel <= ref.PEAK_TOLERANCE), f"4s {n4} nrn {nrn} rel {rel}"
