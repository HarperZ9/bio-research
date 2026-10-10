"""Four- and six-state ChR2 kinetic models under voltage clamp.

Equations reproduce RhO_4states and RhO_6states in PyRhO pyrho/models.py
(commit dade008ad2f9d18cf7c3b26782b7063e1a597e40). Plain NumPy/SciPy, no
simulator dependency. Time in ms, irradiance in mW/mm^2, current in nA
(negative is inward), conductance g0 in pS.

State order, 4-state: C1, O1, O2, C2.
State order, 6-state: C1, I1, O1, O2, I2, C2.
"""
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from .params import CHR2_4STATE, CHR2_6STATE

H_PLANCK = 6.62607015e-34  # J s
C_LIGHT = 2.99792458e8  # m/s


def irradiance_to_flux(irr_mw_mm2, wavelength_nm=470.0):
    """Convert irradiance [mW/mm^2] to photon flux [photons mm^-2 s^-1].

    Same formula as PyRhO utilities.irrad2flux.
    """
    e_photon_mj = 1e12 * H_PLANCK * C_LIGHT / wavelength_nm
    return irr_mw_mm2 / e_photon_mj


def light_rates(prm, phi):
    """Light-dependent transition rates [ms^-1] for flux phi."""
    hp = phi ** prm["p"] / (phi ** prm["p"] + prm["phi_m"] ** prm["p"])
    hq = phi ** prm["q"] / (phi ** prm["q"] + prm["phi_m"] ** prm["q"])
    return {
        "Ga1": prm["k1"] * hp,
        "Ga2": prm["k2"] * hp,
        "Gf": prm["Gf0"] + prm["k_f"] * hq,
        "Gb": prm["Gb0"] + prm["k_b"] * hq,
    }


def rate_matrix(prm, phi):
    """Generator matrix A with ds/dt = A s for the given flux."""
    r = light_rates(prm, phi)
    gd1, gd2, gr0 = prm["Gd1"], prm["Gd2"], prm["Gr0"]
    ga1, ga2, gf, gb = r["Ga1"], r["Ga2"], r["Gf"], r["Gb"]
    if "Go1" not in prm:
        return np.array([
            [-ga1, gd1, 0.0, gr0],
            [ga1, -(gd1 + gf), gb, 0.0],
            [0.0, gf, -(gd2 + gb), ga2],
            [0.0, 0.0, gd2, -(ga2 + gr0)],
        ])
    go1, go2 = prm["Go1"], prm["Go2"]
    return np.array([
        [-ga1, 0.0, gd1, 0.0, 0.0, gr0],
        [ga1, -go1, 0.0, 0.0, 0.0, 0.0],
        [0.0, go1, -(gd1 + gf), gb, 0.0, 0.0],
        [0.0, 0.0, gf, -(gb + gd2), go2, 0.0],
        [0.0, 0.0, 0.0, 0.0, -go2, ga2],
        [0.0, 0.0, 0.0, gd2, 0.0, -(ga2 + gr0)],
    ])


def open_indices(prm):
    """Indices of O1 and O2 in the state vector."""
    return (2, 3) if "Go1" in prm else (1, 2)


def f_voltage(prm, v_mv):
    """Inward-rectification factor f(V); equals 1 near -70 mV."""
    dv = v_mv - prm["E"]
    if abs(dv) < 1e-9:
        return prm["v1"] / prm["v0"]
    return (prm["v1"] / dv) * (1.0 - np.exp(-dv / prm["v0"]))


def photocurrent(prm, states, v_mv):
    """Photocurrent [nA] from a (n_t, n_states) state array at clamp V."""
    i_o1, i_o2 = open_indices(prm)
    f_phi = states[:, i_o1] + prm["gam"] * states[:, i_o2]
    g_ps = prm["g0"] * f_phi * f_voltage(prm, v_mv)
    return g_ps * (v_mv - prm["E"]) * 1e-6


def steady_state(prm, phi):
    """Analytic steady state: null vector of the generator, normalised."""
    a = rate_matrix(prm, phi)
    n = a.shape[0]
    m = np.vstack([a, np.ones(n)])
    rhs = np.zeros(n + 1)
    rhs[-1] = 1.0
    sol, *_ = np.linalg.lstsq(m, rhs, rcond=None)
    return sol


@dataclass
class Trace:
    t: np.ndarray  # ms
    current: np.ndarray  # nA
    states: np.ndarray  # (n_t, n_states)
    on: float  # light onset, ms
    off: float  # light offset, ms


def _integrate(prm, phi, s0, t0, t1, dt):
    """Integrate the linear ODE over [t0, t1] with constant flux."""
    a = rate_matrix(prm, phi)
    n_pts = int(round((t1 - t0) / dt)) + 1
    t_eval = np.linspace(t0, t1, n_pts)
    sol = solve_ivp(lambda _t, s: a @ s, (t0, t1), s0, method="LSODA",
                    t_eval=t_eval, jac=lambda _t, _s: a,
                    rtol=1e-9, atol=1e-12, max_step=0.5)
    if not sol.success:
        raise RuntimeError(f"ODE integration failed: {sol.message}")
    return sol.t, sol.y.T


def simulate_pulse(prm, irr_mw_mm2, duration_ms, v_mv=-70.0, pre_ms=50.0,
                   post_ms=300.0, dt=0.01, wavelength_nm=470.0):
    """Voltage-clamp response to one square light pulse from dark."""
    n = rate_matrix(prm, 0.0).shape[0]
    s0 = np.zeros(n)
    s0[0] = 1.0
    phi = irradiance_to_flux(irr_mw_mm2, wavelength_nm)
    on, off, end = pre_ms, pre_ms + duration_ms, pre_ms + duration_ms + post_ms
    segs = [(0.0, on, 0.0), (on, off, phi), (off, end, 0.0)]
    ts, ss = [], []
    for k, (t0, t1, ph) in enumerate(segs):
        t, s = _integrate(prm, ph, s0, t0, t1, dt)
        s0 = s[-1]
        ts.append(t if k == 0 else t[1:])
        ss.append(s if k == 0 else s[1:])
    t = np.concatenate(ts)
    states = np.vstack(ss)
    return Trace(t, photocurrent(prm, states, v_mv), states, on, off)


MODELS = {"4state": CHR2_4STATE, "6state": CHR2_6STATE}
