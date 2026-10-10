"""ChR2 kinetic parameter sets copied from PyRhO.

Source: https://github.com/ProjectPyRhO/PyRhO, file pyrho/parameters.py at
commit dade008ad2f9d18cf7c3b26782b7063e1a597e40 (master on 2026-10-09, commit
date 2023-07-24). sha256 of the fetched file:
b7ae6fb552d683f386d7477e774a9e6d0b29b88f55b6691967994304ef219acc
Lines 179-196 (modelFits['4']['ChR2']) and 199-218 (modelFits['6']['ChR2']).
PyRhO is BSD-3-Clause. The file does not name the dataset these sets were fitted
to. Equations follow pyrho/models.py at the same commit (RhO_4states,
RhO_6states).

Units: rates in ms^-1, phi_m in photons mm^-2 s^-1, g0 in pS, voltages in mV.
"""

CHR2_4STATE = {
    "g0": 1.14e5, "gam": 0.00742, "phi_m": 2.33e17,
    "k1": 4.15, "k2": 0.868, "p": 0.833,
    "Gf0": 0.0373, "k_f": 0.0581, "Gb0": 0.0161, "k_b": 0.063, "q": 1.94,
    "Gd1": 0.105, "Gd2": 0.0138, "Gr0": 0.00033,
    "E": 0.0, "v0": 43.0, "v1": 17.1,
}

CHR2_6STATE = {
    "g0": 2.52e4, "gam": 0.0161, "phi_m": 3.54e17,
    "k1": 13.4, "k2": 2.71, "p": 0.985,
    "Gf0": 0.0389, "k_f": 0.103, "Gb0": 0.0198, "k_b": 0.139, "q": 1.58,
    "Go1": 2.0, "Go2": 0.0567,
    "Gd1": 0.112, "Gd2": 0.0185, "Gr0": 0.00033,
    "E": 0.0, "v0": 43.0, "v1": 17.1,
}

PROVENANCE = {
    "repo": "https://github.com/ProjectPyRhO/PyRhO",
    "file": "pyrho/parameters.py",
    "commit": "dade008ad2f9d18cf7c3b26782b7063e1a597e40",
    "sha256": "b7ae6fb552d683f386d7477e774a9e6d0b29b88f55b6691967994304ef219acc",
}
