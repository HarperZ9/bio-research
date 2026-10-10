"""Regenerate the numbers quoted in project-docs/opsin03/STEP1.md.

Usage (Windows venv): H:/bio-data/venvs/opsin/Scripts/python
  scripts/opsin03_step1_numbers.py data/opsin03/step1_numbers.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opsin03 import reference as ref  # noqa: E402
from opsin03.chr2 import MODELS, simulate_pulse  # noqa: E402
from opsin03.metrics import peak, summarize  # noqa: E402
from opsin03.params import PROVENANCE  # noqa: E402

IRRS = ref.FIVE_IRRADIANCES + [ref.NORM_IRRADIANCE]


def peaks(prm):
    return [peak(simulate_pulse(prm, e, 50.0, post_ms=1.0)) for e in IRRS]


def lin_protocol(prm):
    long_ = summarize(simulate_pulse(prm, ref.NORM_IRRADIANCE, 500.0,
                                     v_mv=ref.V_LIN))
    short = summarize(simulate_pulse(prm, ref.NORM_IRRADIANCE, 10.0,
                                     v_mv=ref.V_LIN))
    return {"pulse_500ms": long_, "pulse_10ms": short}


def main(out):
    res = {"provenance": PROVENANCE, "irradiances_mW_mm2": IRRS,
           "lin2009_wt_ranges": ref.LIN2009_WT,
           "lin2009_h134r_ranges": ref.LIN2009_H134R, "models": {}}
    for name, prm in MODELS.items():
        p = peaks(prm)
        res["models"][name] = {
            "peak_nA_at_-70mV": p,
            "peak_normalised_to_19.8": [x / p[-1] for x in p],
            "lin_protocol_-80mV": lin_protocol(prm),
        }
    Path(out).write_text(json.dumps(res, indent=2) + "\n")
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
