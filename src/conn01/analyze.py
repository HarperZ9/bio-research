"""Primary and secondary tests of prereg 01, decision rule and Holm correction.

Model: partial Pearson correlation between CTQ total and the Fisher-z
amygdala-region connectivity, adjusting for age, sex, site (only if more than
one site is present), mean FD over usable runs and retained volume count.

CIs use the Fisher transform with standard error 1/sqrt(n - 3 - k), where k
is the number of covariate columns. The p value uses the t test of the
partial correlation with n - 2 - k degrees of freedom.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd
from scipy import stats

CTQ_SUBSCALES = ["ctqscore_ea", "ctqscore_en", "ctqscore_pa", "ctqscore_pn",
                 "ctqscore_sa"]
SUBSCALE_RANGE = (5, 25)
MISSING_CODES = (999, -999, 777, -777)
BOUND = 0.20
ALPHA = 0.05

ASSOCIATION = "association"
NO_MEANINGFUL = "no_meaningful_association"
INCONCLUSIVE = "inconclusive"


@dataclass
class TestResult:
    label: str
    n: int
    k_covariates: int
    r: float
    p: float
    ci95: tuple[float, float]
    ci90: tuple[float, float]
    decision: str
    magnitude: str
    p_holm: float = float("nan")
    association_survives_holm: bool = False


def ctq_total(df: pd.DataFrame) -> pd.Series:
    """Sum of the five CTQ subscales; NaN if any is missing.

    Codes in MISSING_CODES count as missing. Any other value outside 5 to 25
    raises, because it means the column is not what the prereg assumes.
    """
    sub = df[CTQ_SUBSCALES].apply(pd.to_numeric, errors="coerce")
    sub = sub.mask(sub.isin(MISSING_CODES))
    lo, hi = SUBSCALE_RANGE
    bad = sub.notna() & ((sub < lo) | (sub > hi))
    if bad.to_numpy().any():
        raise ValueError(f"{int(bad.to_numpy().sum())} CTQ subscale values "
                         f"outside {lo} to {hi} that are not missing codes")
    return sub.sum(axis=1, min_count=len(CTQ_SUBSCALES)).where(sub.notna().all(axis=1))


def covariate_matrix(df: pd.DataFrame, numeric: list[str],
                     categorical: list[str]) -> np.ndarray:
    """Numeric columns plus treatment-coded dummies for categorical columns.

    A categorical column with a single level (for example one site) adds no
    columns, which implements "site, if more than one site is recorded".
    """
    parts = [df[numeric].astype(float)]
    for col in categorical:
        levels = df[col].astype(str)
        if levels.nunique() > 1:
            parts.append(pd.get_dummies(levels, prefix=col, drop_first=True,
                                        dtype=float))
    return pd.concat(parts, axis=1).to_numpy(float)


def partial_corr(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> tuple[float, float, int, int]:
    """Partial r of x and y given covariates z; returns (r, p, n, k)."""
    n, k = len(x), z.shape[1]
    design = np.column_stack([np.ones(n), z])
    rx = x - design @ np.linalg.lstsq(design, x, rcond=None)[0]
    ry = y - design @ np.linalg.lstsq(design, y, rcond=None)[0]
    r = float(np.corrcoef(rx, ry)[0, 1])
    dof = n - 2 - k
    if dof < 1:
        raise ValueError(f"not enough participants: n={n}, k={k}")
    t = r * np.sqrt(dof / max(1e-300, 1 - r * r))
    p = float(2 * stats.t.sf(abs(t), dof))
    return r, p, n, k


def fisher_ci(r: float, n: int, k: int, level: float) -> tuple[float, float]:
    se = 1.0 / np.sqrt(n - 3 - k)
    crit = stats.norm.ppf(0.5 + level / 2)
    z = np.arctanh(r)
    return float(np.tanh(z - crit * se)), float(np.tanh(z + crit * se))


def decide(r: float, ci95: tuple[float, float], ci90: tuple[float, float],
           bound: float = BOUND) -> tuple[str, str]:
    """Pre-registered three-way rule. Returns (decision, magnitude).

    Association is checked first: the 95% CI excludes 0. Its magnitude is
    "meaningful" if |r| >= bound, else "small". Otherwise, "no meaningful
    association" if the 90% CI lies inside (-bound, bound). Else inconclusive.
    """
    if ci95[0] > 0 or ci95[1] < 0:
        return ASSOCIATION, ("meaningful" if abs(r) >= bound else "small")
    if ci90[0] > -bound and ci90[1] < bound:
        return NO_MEANINGFUL, ""
    return INCONCLUSIVE, ""


def holm(pvals: list[float]) -> list[float]:
    """Holm step-down adjusted p values, in the input order."""
    p = np.asarray(pvals, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * p[i])
        adj[i] = min(1.0, running)
    return adj.tolist()


def run_test(df: pd.DataFrame, exposure: str, outcome: str, numeric: list[str],
             categorical: list[str], label: str) -> TestResult:
    """Complete-case partial correlation test with the decision rule."""
    cols = [exposure, outcome] + numeric + categorical
    d = df.dropna(subset=cols)
    z = covariate_matrix(d, numeric, categorical)
    r, p, n, k = partial_corr(d[exposure].to_numpy(float),
                              d[outcome].to_numpy(float), z)
    ci95, ci90 = fisher_ci(r, n, k, 0.95), fisher_ci(r, n, k, 0.90)
    decision, magnitude = decide(r, ci95, ci90)
    return TestResult(label, n, k, r, p, ci95, ci90, decision, magnitude)


def primary_and_secondary(df: pd.DataFrame, primary_outcome: str,
                          secondary_outcome: str, numeric: list[str],
                          categorical: list[str],
                          exposure: str = "ctq_total") -> list[dict]:
    """Run both registered tests and apply Holm across the pair."""
    res = [run_test(df, exposure, primary_outcome, numeric, categorical, "primary"),
           run_test(df, exposure, secondary_outcome, numeric, categorical, "secondary")]
    for t, ph in zip(res, holm([t.p for t in res])):
        t.p_holm = ph
        t.association_survives_holm = bool(t.decision == ASSOCIATION and ph < ALPHA)
    return [asdict(t) for t in res]
