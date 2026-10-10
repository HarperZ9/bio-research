"""Run ModelDB 244414 (Williams et al. 2013 ChR2-H134R, NEURON) under voltage
clamp and write summary measures to data/opsin03/neuron_williams.json.

Runs in WSL with NEURON from pip. Usage:
  python scripts/opsin03_neuron_williams.py <compiled_mod_dir> <out_json>
The mod directory must hold ChR2H134R.mod compiled with nrnivmodl
(x86_64/libnrnmech.so). Model download: https://modeldb.science/download/244414
"""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from neuron import h

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from opsin03.metrics import summarize  # noqa: E402

IRRADIANCES = [0.5, 1.0, 2.0, 5.0, 10.0, 19.8]
PRE, DUR, POST, DT = 50.0, 500.0, 300.0, 0.01


def run_one(irr, v_hold, dur=DUR, celsius=22.0):
    """One square pulse; returns a Trace-like object with current in mA/cm2."""
    h.celsius = celsius
    soma = h.Section(name="soma")
    soma.L = soma.diam = 20.0
    soma.insert("ChR2")
    seg = soma(0.5)
    seg.light_delay_ChR2 = PRE
    seg.pulse_width_ChR2 = dur
    seg.light_intensity_ChR2 = irr
    clamp = h.SEClamp(seg)
    clamp.dur1, clamp.amp1, clamp.rs = 1e9, v_hold, 1e-3
    t_vec = h.Vector().record(h._ref_t)
    i_vec = h.Vector().record(seg._ref_i_ChR2)
    h.dt = DT
    h.finitialize(v_hold)
    h.continuerun(PRE + dur + POST)
    t = np.array(t_vec)
    cur = np.array(i_vec)
    return SimpleNamespace(t=t, current=cur, on=PRE, off=PRE + dur)


def density(m):
    """Rename current keys: this model reports mA/cm2, not nA."""
    return {k.replace("_nA", "_mA_cm2"): v for k, v in m.items()}


def main(mod_dir, out_json):
    h.nrn_load_dll(str(Path(mod_dir) / "x86_64" / "libnrnmech.so"))
    h.load_file("stdrun.hoc")
    out = {"model": "ModelDB 244414, ChR2H134R.mod", "celsius": 22.0,
           "pulse_ms": DUR, "units_current": "mA/cm2 (gmax 0.4 mS/cm2)",
           "runs": []}
    for v_hold in (-70.0, -80.0):
        for irr in IRRADIANCES:
            m = density(summarize(run_one(irr, v_hold)))
            out["runs"].append({"v_mV": v_hold, "irr_mW_mm2": irr, **m})
    short = density(summarize(run_one(19.8, -80.0, dur=10.0)))
    out["short_pulse_10ms_19.8"] = short
    off = run_one(0.0, -70.0)
    out["no_light_max_abs_current"] = float(np.max(np.abs(off.current)))
    Path(out_json).write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
