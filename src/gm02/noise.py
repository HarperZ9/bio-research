"""Noise-floor statistics for a repeated within-person measurement."""
import numpy as np
from scipy import stats


def cv_pct(x):
    x = np.asarray(x, float)
    return float(100.0 * x.std(ddof=1) / x.mean())


def pooled_within_cv(x, groups, level=0.90):
    """Pooled within-group SD as percent of the grand mean, with a chi-square CI."""
    x, groups = np.asarray(x, float), np.asarray(groups)
    ss = sum(((x[groups == g] - x[groups == g].mean()) ** 2).sum() for g in np.unique(groups))
    df = len(x) - len(np.unique(groups))
    a = (1 - level) / 2
    m = x.mean()
    return {"cv": float(100 * np.sqrt(ss / df) / m),
            "cv_lo": float(100 * np.sqrt(ss / stats.chi2.ppf(1 - a, df)) / m),
            "cv_hi": float(100 * np.sqrt(ss / stats.chi2.ppf(a, df)) / m),
            "df": int(df)}


def robust_sd_pct(x):
    x = np.asarray(x, float)
    return float(100.0 * 1.4826 * np.median(np.abs(x - np.median(x))) / x.mean())


def _sorted(x, day):
    x, day = np.asarray(x, float), np.asarray(day)
    order = np.argsort(day)
    return x[order], day[order]


def consecutive_diffs(x, day):
    """Differences between rows whose day index differs by exactly 1."""
    x, day = _sorted(x, day)
    return np.diff(x)[np.diff(day) == 1]


def lag1_autocorr(x, day):
    x, day = _sorted(x, day)
    keep = np.diff(day) == 1
    xc = x - x.mean()
    return float(np.corrcoef(xc[:-1][keep], xc[1:][keep])[0, 1])


def summarize(x, study, day):
    """Noise-floor block for one measure: overall, per study, pooled, test-retest."""
    x, study, day = np.asarray(x, float), np.asarray(study), np.asarray(day)
    out = {"n": int(len(x)), "mean": float(x.mean()), "cv_all": cv_pct(x)}
    out.update({f"pooled_{k}": v for k, v in pooled_within_cv(x, study).items()})
    diffs, ac = [], []
    for s in np.unique(study):
        m = study == s
        out[f"study{s}_mean"] = float(x[m].mean())
        out[f"study{s}_cv"] = cv_pct(x[m])
        out[f"study{s}_robust_sd_pct"] = robust_sd_pct(x[m])
        diffs.append(consecutive_diffs(x[m], day[m]))
        ac.append(lag1_autocorr(x[m], day[m]))
    d = np.concatenate(diffs)
    out["typical_error_pct"] = float(100 * d.std(ddof=1) / np.sqrt(2) / x.mean())
    out["n_consecutive_pairs"] = int(len(d))
    out["te_over_within_sd"] = out["typical_error_pct"] / out["pooled_cv"]
    out["lag1_autocorr_by_study"] = ac
    return out


def welch_offset_pct(x, study, level=0.95):
    """Mean of study 2 minus study 1, as percent of the study-1 mean, Welch CI."""
    x, study = np.asarray(x, float), np.asarray(study)
    a, b = x[study == 1], x[study == 2]
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    se = np.sqrt(va + vb)
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    q = stats.t.ppf(0.5 + level / 2, df)
    diff, s = b.mean() - a.mean(), 100.0 / a.mean()
    return {"offset_pct": float(diff * s), "lo": float((diff - q * se) * s),
            "hi": float((diff + q * se) * s)}
