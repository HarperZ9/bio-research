"""Smoke test of the full analysis runner on synthetic participants and tables."""
import json

import numpy as np
import pandas as pd

import conn01_synth as syn
from conn01 import analyze as an, run_analysis as ra


def _participant(root, label, rng, coupling):
    d = root / f"sub-{label}"
    d.mkdir(parents=True)
    for k in (1, 2):
        conf, meta = syn.confounds(150, rng)
        stem = f"sub-{label}_task-restAP_run-{k:02d}"
        syn.regions(conf, rng, coupling).to_csv(d / f"{stem}_timeseries.tsv", sep="\t", index=False)
        conf.to_csv(d / f"{stem}_desc-confounds_timeseries.tsv", sep="\t", index=False)
        (d / f"{stem}_desc-confounds_timeseries.json").write_text(json.dumps(meta))
    qc = {"runs": [{"scanner": {"InstitutionName": "Synthetic Site"}}]}
    (d / f"sub-{label}_qc.json").write_text(json.dumps(qc))
    (d / "DONE").touch()


def test_runner_end_to_end_on_synthetic_inputs(tmp_path):
    rng = np.random.default_rng(0)
    n = 40
    ids = [f"SYN{i:03d}" for i in range(n)]
    sub = rng.integers(5, 26, size=(n, 5))
    for i, label in enumerate(ids):
        coupling = 0.1 + 0.6 * (sub[i].sum() - 25) / 100  # planted CTQ link
        _participant(tmp_path / "conn", label, rng, coupling)
    ctq = pd.DataFrame(sub, columns=an.CTQ_SUBSCALES)
    ctq.insert(0, "pid", ids)
    ctq["ctqscore_val"] = rng.integers(0, 4, n)
    ctq.loc[0, "ctqscore_ea"] = 999  # missing code: excluded
    ctq.to_csv(tmp_path / "ctq.tsv", sep="\t", index=False)
    pd.DataFrame({"pid": ids, "age": rng.integers(18, 70, n),
                  "sex": rng.choice(["F", "M"], n),
                  "grp": rng.choice(["patient", "control"], n)}
                 ).to_csv(tmp_path / "demos.tsv", sep="\t", index=False)
    out = tmp_path / "res.json"
    ra.main(["--conn-root", str(tmp_path / "conn"), "--ctq", str(tmp_path / "ctq.tsv"),
             "--demos", str(tmp_path / "demos.tsv"), "--out", str(out),
             "--id-col", "pid", "--age-col", "age", "--sex-col", "sex",
             "--group-col", "grp"])
    res = json.loads(out.read_text())
    prim, sec = res["registered"]
    assert prim["label"] == "primary" and sec["label"] == "secondary"
    assert prim["n"] == n - 1  # the 999 participant is out
    assert prim["k_covariates"] == 4  # age, mean_fd, n_retained, sex (one site)
    assert prim["r"] > 0.3 and prim["decision"] == an.ASSOCIATION
    names = {r["sensitivity"] for r in res["sensitivity"]}
    assert {"gsr", "amygdala_l", "amygdala_r", "exclude_max_minimization",
            "plus_diagnostic_group", "exclude_compcor_short", "fd_rule_unfiltered"} <= names
    assert all(r["status"] == "exploratory" for r in res["sensitivity"])
