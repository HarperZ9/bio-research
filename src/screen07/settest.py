"""Competitive gene-set tests: expression-matched random sets, leave-one-out,
and sample-label permutation."""
from __future__ import annotations

import numpy as np
import pandas as pd

from .model import moderated_t

N_BINS = 20


def expression_bins(mean_expr: pd.Series) -> pd.Series:
    """20 equal-count bins of mean log expression."""
    return pd.qcut(mean_expr.rank(method="first"), N_BINS, labels=False)


def random_set_null(bins: pd.Series, tstat: pd.Series, members: list[str],
                    n_sets: int, rng: np.random.Generator) -> np.ndarray:
    """Mean t of n_sets random sets, each member replaced by a same-bin non-member."""
    total = np.zeros(n_sets)
    member_bins = bins.loc[members].value_counts()
    nonmember = ~bins.index.isin(members)
    for b, m_b in member_bins.items():
        pool = tstat[(bins == b).to_numpy() & nonmember].to_numpy()
        if len(pool) < m_b:
            raise ValueError(f"bin {b} has too few non-member genes")
        keys = rng.random((n_sets, len(pool)))
        idx = np.argpartition(keys, m_b - 1, axis=1)[:, :m_b]
        total += pool[idx].sum(axis=1)
    return total / len(members)


def p_values(obs: float, null: np.ndarray) -> dict[str, float]:
    n = len(null)
    p_down = (1 + np.sum(null <= obs)) / (n + 1)
    p_up = (1 + np.sum(null >= obs)) / (n + 1)
    return {"p_down": float(p_down), "p_up": float(p_up),
            "p_two": float(min(1.0, 2 * min(p_down, p_up)))}


def random_set_test(bins: pd.Series, tstat: pd.Series, members: list[str],
                    n_sets: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    obs = float(tstat.loc[members].mean())
    null = random_set_null(bins, tstat, members, n_sets, rng)
    out = {"n_genes": len(members), "set_mean_t": obs,
           "null_mean": float(null.mean()), "null_sd": float(null.std(ddof=1))}
    out.update(p_values(obs, null))
    return out


def leave_one_out(bins: pd.Series, tstat: pd.Series, members: list[str],
                  n_sets: int, seed: int) -> pd.DataFrame:
    rows = []
    for g in members:
        rest = [m for m in members if m != g]
        res = random_set_test(bins, tstat, rest, n_sets, seed)
        rows.append({"dropped": g, "set_mean_t": res["set_mean_t"],
                     "p_down": res["p_down"], "p_two": res["p_two"]})
    return pd.DataFrame(rows)


def _permute_within(strata: np.ndarray, labels: np.ndarray,
                    rng: np.random.Generator) -> np.ndarray:
    out = labels.copy()
    for s in np.unique(strata):
        idx = np.flatnonzero(strata == s)
        out[idx] = rng.permutation(labels[idx])
    return out


def permutation_test(logexpr: pd.DataFrame, samples: pd.DataFrame,
                     covariates: list[str], members: list[str],
                     n_perm: int, seed: int) -> dict:
    """Competitive statistic mean t(M) - mean t(all genes); condition labels
    permuted within covariate strata. Keeps inter-gene correlation."""
    from .model import design_matrix
    rng = np.random.default_rng(seed)
    is_member = logexpr.index.isin(members)
    Y = logexpr.to_numpy()
    strata = (samples[covariates].astype(str).agg("|".join, axis=1).to_numpy()
              if covariates else np.zeros(len(samples), dtype=int))

    def stat(smp: pd.DataFrame) -> float:
        t = moderated_t(Y, design_matrix(smp, covariates))["t"]
        return float(t[is_member].mean() - t.mean())

    obs = stat(samples)
    labels = samples["condition"].to_numpy()
    null = np.empty(n_perm)
    for i in range(n_perm):
        smp = samples.copy()
        smp["condition"] = _permute_within(strata, labels, rng)
        null[i] = stat(smp)
    p_two = (1 + np.sum(np.abs(null) >= abs(obs))) / (n_perm + 1)
    p_down = (1 + np.sum(null <= obs)) / (n_perm + 1)
    return {"stat": obs, "p_two": float(p_two), "p_down": float(p_down),
            "n_perm": n_perm}
