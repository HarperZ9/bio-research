"""Synthetic-data checks for conn01.analyze (no participant data used)."""
import numpy as np
import pandas as pd
import pytest

import conn01_synth  # noqa: F401  (adds src/ to sys.path)
from conn01 import analyze as an

NUM = ["age", "mean_fd", "n_retained"]
CAT = ["sex", "site"]


def planted(n: int, r_partial: float, seed: int = 0, sites: int = 2) -> pd.DataFrame:
    """Data where x and y share covariate-driven variance plus a planted partial r."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "age": rng.uniform(18, 70, n), "mean_fd": rng.gamma(2, 0.05, n),
        "n_retained": rng.integers(800, 1900, n).astype(float),
        "sex": rng.choice(["F", "M"], n), "site": rng.choice(list("ABC"[:sites]), n),
    })
    z = an.covariate_matrix(df, NUM, CAT)
    z = (z - z.mean(0)) / z.std(0)
    e1 = rng.normal(size=n)
    e2 = r_partial * e1 + np.sqrt(1 - r_partial ** 2) * rng.normal(size=n)
    df["ctq_total"] = 50 + 8 * (z @ rng.normal(size=z.shape[1]) * 0.8 + e1)
    df["z_out"] = 0.3 + 0.1 * (z @ rng.normal(size=z.shape[1]) * 0.8 + e2)
    return df


def test_planted_partial_r_is_recovered():
    df = planted(20000, 0.25, seed=1)
    res = an.run_test(df, "ctq_total", "z_out", NUM, CAT, "t")
    assert abs(res.r - 0.25) < 0.02
    assert res.n == 20000 and res.k_covariates == 5  # 3 numeric + sex + 1 site dummy
    zero = an.run_test(planted(20000, 0.0, seed=2), "ctq_total", "z_out", NUM, CAT, "t")
    assert abs(zero.r) < 0.02


def test_partial_r_differs_from_raw_r_when_confounded():
    df = planted(5000, 0.0, seed=3)
    fd = (df["mean_fd"] - df["mean_fd"].mean()) / df["mean_fd"].std()
    df["ctq_total"] += 8 * fd   # both variables now share motion variance
    df["z_out"] += 0.1 * fd
    raw = np.corrcoef(df["ctq_total"], df["z_out"])[0, 1]
    part = an.run_test(df, "ctq_total", "z_out", NUM, CAT, "t").r
    assert abs(part) < 0.04 and abs(raw - part) > 0.05


def test_p_value_matches_ols_coefficient_t_test():
    df = planted(300, 0.2, seed=4)
    res = an.run_test(df, "ctq_total", "z_out", NUM, CAT, "t")
    z = an.covariate_matrix(df, NUM, CAT)
    x = np.column_stack([np.ones(len(df)), df["ctq_total"], z])
    y = df["z_out"].to_numpy()
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    resid = y - x @ beta
    dof = len(y) - x.shape[1]
    cov = np.linalg.inv(x.T @ x) * (resid @ resid) / dof
    t = beta[1] / np.sqrt(cov[1, 1])
    from scipy import stats
    assert res.p == pytest.approx(2 * stats.t.sf(abs(t), dof), rel=1e-6)


def test_single_site_adds_no_site_column():
    df = planted(200, 0.1, seed=5, sites=1)
    assert an.covariate_matrix(df, NUM, CAT).shape[1] == 4


def test_fisher_ci_formula():
    lo, hi = an.fisher_ci(0.3, 203, 5, 0.95)
    se = 1 / np.sqrt(203 - 3 - 5)
    assert lo == pytest.approx(np.tanh(np.arctanh(0.3) - 1.959964 * se), abs=1e-5)
    assert hi == pytest.approx(np.tanh(np.arctanh(0.3) + 1.959964 * se), abs=1e-5)
    lo90, hi90 = an.fisher_ci(0.3, 203, 5, 0.90)
    assert lo < lo90 < 0.3 < hi90 < hi


@pytest.mark.parametrize("r,ci95,ci90,expected", [
    (0.30, (0.15, 0.44), (0.17, 0.42), (an.ASSOCIATION, "meaningful")),
    (-0.20, (-0.33, -0.06), (-0.31, -0.08), (an.ASSOCIATION, "meaningful")),
    (0.12, (0.02, 0.22), (0.04, 0.20), (an.ASSOCIATION, "small")),
    (0.01, (-0.12, 0.14), (-0.10, 0.12), (an.NO_MEANINGFUL, "")),
    (0.05, (-0.15, 0.25), (-0.12, 0.22), (an.INCONCLUSIVE, "")),
    (0.00, (-0.25, 0.25), (-0.21, 0.21), (an.INCONCLUSIVE, "")),
])
def test_decision_rule_constructed_inputs(r, ci95, ci90, expected):
    assert an.decide(r, ci95, ci90) == expected


def test_decision_rule_end_to_end_three_outcomes():
    assoc = an.run_test(planted(2000, 0.35, seed=6), "ctq_total", "z_out", NUM, CAT, "a")
    null = an.run_test(planted(3000, 0.0, seed=7), "ctq_total", "z_out", NUM, CAT, "b")
    small_n = an.run_test(planted(40, 0.0, seed=8), "ctq_total", "z_out", NUM, CAT, "c")
    assert (assoc.decision, assoc.magnitude) == (an.ASSOCIATION, "meaningful")
    assert null.decision == an.NO_MEANINGFUL
    assert small_n.decision == an.INCONCLUSIVE


def test_holm_adjustment():
    assert an.holm([0.01, 0.04]) == pytest.approx([0.02, 0.04])
    assert an.holm([0.04, 0.01]) == pytest.approx([0.04, 0.02])
    assert an.holm([0.03, 0.02]) == pytest.approx([0.04, 0.04])  # monotone step-down
    assert an.holm([0.6, 0.7]) == pytest.approx([1.0, 1.0])


def test_primary_secondary_applies_holm_to_association_flag():
    df = planted(400, 0.12, seed=9)
    df["z_sec"] = df["z_out"]
    rows = an.primary_and_secondary(df, "z_out", "z_sec", NUM, CAT)
    assert [r["label"] for r in rows] == ["primary", "secondary"]
    for r in rows:
        assert r["p_holm"] == pytest.approx(min(1.0, 2 * r["p"]))
        assert r["association_survives_holm"] == (
            r["decision"] == an.ASSOCIATION and r["p_holm"] < 0.05)


def test_ctq_total_sums_and_excludes_missing():
    df = pd.DataFrame({c: [5, 10, 999] for c in an.CTQ_SUBSCALES})
    df.loc[1, "ctqscore_sa"] = np.nan
    total = an.ctq_total(df)
    assert total.iloc[0] == 25 and np.isnan(total.iloc[1]) and np.isnan(total.iloc[2])


def test_ctq_total_rejects_out_of_range_values():
    df = pd.DataFrame({c: [5] for c in an.CTQ_SUBSCALES})
    df.loc[0, "ctqscore_ea"] = 30
    with pytest.raises(ValueError):
        an.ctq_total(df)
