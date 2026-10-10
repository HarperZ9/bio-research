"""End-to-end wiring check of gm02.run on synthetic SynthSeg outputs (project 02 Tier B)."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gm02 import run  # noqa: E402

QC = ["general white matter", "general grey matter", "hippocampus+amygdala"]


def write_fake(root, beta_pct, rng):
    (root / "vol").mkdir(parents=True)
    (root / "qc").mkdir()
    pss = rng.normal(15, 5, 60)
    z = (pss - pss.mean()) / pss.std(ddof=1)
    for s in range(1, 61):
        tiv = 1.4e6 * (1 + rng.normal(0, 0.002))
        hipp = 8000 * (1 + beta_pct / 100 * z[s - 1] + rng.normal(0, 0.004))
        vol = {"subject": f"s{s}", "total intracranial": tiv,
               "left hippocampus": hipp / 2 * tiv / 1.4e6, "right hippocampus": hipp / 2 * tiv / 1.4e6,
               "left amygdala": 1500 + rng.normal(0, 15), "right amygdala": 1500 + rng.normal(0, 15)}
        pd.DataFrame([vol]).to_csv(root / "vol" / f"ses-{s:02d}_vol.csv", index=False)
        qc = {"subject": f"s{s}", **{k: 0.9 + rng.normal(0, 0.01) for k in QC}}
        pd.DataFrame([qc]).to_csv(root / "qc" / f"ses-{s:02d}_qc.csv", index=False)
    part = pd.DataFrame({"participant_id": "sub-01",
                         "session_id": [f"ses-{s:02d}" for s in range(1, 61)],
                         "perceived_stress": pss})
    part.to_csv(root / "participants.tsv", sep="\t", index=False)


def test_pipeline_recovers_planted_negative_effect(tmp_path, monkeypatch):
    monkeypatch.setattr(run, "N_PERM", 99)
    write_fake(tmp_path, beta_pct=-1.0, rng=np.random.default_rng(7))
    run.main([str(tmp_path), str(tmp_path / "participants.tsv"), str(tmp_path / "out")])
    res = json.loads((tmp_path / "out" / "results.json").read_text())
    lag0 = res["association"]["primary"]["coefs"]["pss_lag0"]
    assert lag0["lo"] < -1.0 < lag0["hi"]
    assert lag0["p_perm"] <= 0.02
    assert res["association"]["primary"]["n"] == 58
    assert res["decision"]["association"] == "support"
    assert res["qc_columns"] == QC
    assert res["noise_floor"]["tiv"]["pooled_cv"] < 0.5
