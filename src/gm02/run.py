"""Run the frozen Tier B analysis (pre-registration 02-tierB-noise-floor.md, v1).

Usage: python -m gm02.run <synthseg_root> <participants.tsv> <out_dir> [--excluded 19,...]
"""
import argparse
import json
from pathlib import Path

import numpy as np

from . import data, noise, perm

N_PERM = 5000
SEED = 20261009
ALPHA = 0.025
NAMES = ("intercept", "pss_lag0", "pss_lag1", "regime_oc", "scan_order", "qc_mean")


def noise_floor(t):
    k = t[~t["excluded"]]
    st, day = k["study"].values, k["day"].values
    out = {m: noise.summarize(k[m].values, st, day)
           for m in ("hipp_ratio", "hipp", "hipp_l", "hipp_r", "amy_ratio", "amy", "tiv")}
    out["left_right_hipp_r"] = float(np.corrcoef(k["hipp_l"], k["hipp_r"])[0, 1])
    out["regime_offset_hipp_ratio"] = noise.welch_offset_pct(k["hipp_ratio"].values, st)
    out["regime_offset_tiv"] = noise.welch_offset_pct(k["tiv"].values, st)
    return out


def daily_pss(t):
    """Standardized PSS, one array of 30 days per study (NaN if missing or excluded)."""
    p = t["pss"].where(~t["excluded"])
    z = (p - p.mean()) / p.std(ddof=1)
    return [z[t["study"] == s].values.astype(float) for s in (1, 2)], float(p.mean()), float(p.std(ddof=1))


def make_build(t, y, use_q=True):
    """Return build(lag0, lag1) that drops rows with any missing input."""
    regime = (t["study"].values == 2).astype(float)
    order = t["day"].values - 15.5
    q = t["qc_mean"].values.astype(float)
    blocks, times = t["study"].values, t["day"].values

    def build(lag0, lag_1):
        cols = [np.ones(len(y)), lag0, lag_1, regime, order] + ([q] if use_q else [])
        X = np.column_stack(cols)
        keep = ~np.isnan(y) & ~np.isnan(X).any(axis=1)
        return y[keep], X[keep], blocks[keep], times[keep]
    return build


def run_model(t, y, label, use_q=True, n_perm=None):
    daily, _, _ = daily_pss(t)
    n_perm = N_PERM if n_perm is None else n_perm
    obs, p, _ = perm.permutation_test(daily, make_build(t, y, use_q), [1, 2], n_perm, SEED)
    lo, hi = obs.ci()
    names = NAMES if use_q else NAMES[:-1]
    coefs = {n: {"beta": float(obs.beta[i]), "se": float(obs.se[i]), "lo": float(lo[i]),
                 "hi": float(hi[i]), "p_wald": float(obs.p()[i])} for i, n in enumerate(names)}
    coefs["pss_lag0"]["p_perm"] = float(p[0])
    coefs["pss_lag1"]["p_perm"] = float(p[1])
    n_rows = int(len(make_build(t, y, use_q)(*perm.lags_from_daily(daily))[0]))
    return {"label": label, "n": n_rows, "rho": obs.rho, "df": obs.df, "coefs": coefs}


def robust_outliers(t, col):
    k = ~t["excluded"]
    flag = np.zeros(len(t), bool)
    for s in (1, 2):
        m = (k & (t["study"] == s)).values
        x = t[col].values[m]
        mad = 1.4826 * np.median(np.abs(x - np.median(x)))
        flag[np.where(m)[0]] = np.abs(x - np.median(x)) > 4 * mad
    return flag


def association(t):
    keep = (~t["excluded"]).values
    y = data.pct_dev(t["hipp_ratio"], keep)
    no_headcase = keep & (t.index.values > 7)
    out_flag = robust_outliers(t, "hipp_ratio")
    return {
        "primary": run_model(t, y, "hippocampus/TIV, full model"),
        "amygdala": run_model(t, data.pct_dev(t["amy_ratio"], keep), "amygdala/TIV, full model"),
        "sens_a_no_qc": run_model(t, y, "hippocampus/TIV, no QC covariate", use_q=False),
        "sens_b_raw": run_model(t, data.pct_dev(t["hipp"], keep), "raw bilateral hippocampus"),
        "sens_c_headcase": run_model(t, np.where(no_headcase, y, np.nan),
                                     "hippocampus/TIV, sessions 1-7 dropped"),
        "sens_d_outliers": run_model(t, np.where(out_flag, np.nan, y),
                                     "hippocampus/TIV, >4 robust SD rows dropped"),
        "n_outliers_dropped_d": int(out_flag.sum()),
    }


def decide(nf, assoc):
    cv = nf["hipp_ratio"]
    c, lo, hi = cv["pooled_cv"], cv["pooled_cv_lo"], cv["pooled_cv_hi"]
    if c <= 0.5:
        rule = "<=0.5%: single-scan precision adequate; Tier A as designed"
    elif c >= 1.5:
        rule = ">=1.5%: Tier A only with annualized change over 2+ years and averaging"
    else:
        rule = "0.5-1.5%: Tier A only with annualized change over 2+ years; margin recomputed"
    provisional = (lo <= 0.5 <= hi) or (lo <= 1.5 <= hi)
    pr = assoc["primary"]["coefs"]
    support = [k for k in ("pss_lag0", "pss_lag1") if pr[k]["beta"] < 0 and pr[k]["p_perm"] < ALPHA
               and assoc["sens_a_no_qc"]["coefs"][k]["beta"] < 0
               and assoc["sens_b_raw"]["coefs"][k]["beta"] < 0]
    opposite = [k for k in ("pss_lag0", "pss_lag1") if pr[k]["beta"] > 0 and pr[k]["p_perm"] < ALPHA]
    verdict = "support" if support else ("opposite sign" if opposite else "not detected")
    return {"noise_rule": rule, "provisional": bool(provisional),
            "tiv_flag": nf["tiv"]["pooled_cv"] > 1.5, "association": verdict,
            "support_terms": support, "opposite_terms": opposite}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("synthseg_root")
    ap.add_argument("participants")
    ap.add_argument("out_dir")
    ap.add_argument("--excluded", default="")
    a = ap.parse_args(argv)
    excl = [int(s) for s in a.excluded.split(",") if s]
    t, qc_names = data.build_table(a.synthseg_root, a.participants, excl)
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    t.to_csv(out / "sessions.csv")
    nf = noise_floor(t)
    assoc = association(t)
    _, pmean, psd = daily_pss(t)
    res = {"qc_columns": qc_names, "excluded": excl, "n_failed": int(t["failed"].sum()),
           "pss_mean": pmean, "pss_sd": psd, "noise_floor": nf, "association": assoc,
           "decision": decide(nf, assoc), "n_perm": N_PERM, "seed": SEED}
    (out / "results.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res["decision"], indent=2))


if __name__ == "__main__":
    main()
