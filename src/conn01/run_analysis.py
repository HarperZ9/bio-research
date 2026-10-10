"""Run the registered analysis once on real data (lead session only).

  python -I -m conn01.run_analysis --conn-root /mnt/h/bio-data/ds005237/conn01 \
      --ctq PHENO/ctq01.tsv --demos PHENO/demos.tsv --out results01.json \
      --id-col <col> --age-col <col> --sex-col <col> [--site-col <col>] \
      [--group-col <col>] [--fd-rule lowpass|unfiltered|bandstop|lowpass_strict]

Column names in the phenotype tables were not read when this was written
(the hard rule kept phenotype contents unopened); they are arguments. If a
named column is missing the script stops and lists the available column
names, never values. Without --site-col the scanner InstitutionName from the
BIDS sidecars is used as site. The results JSON holds the primary and
secondary tests (Holm across both) and the exploratory sensitivity
analyses, labelled as exploratory.

FD rule (prereg 01 deviation 5a): censoring, run exclusion and the mean-FD
covariate use the 0.1 Hz low-pass rule by default. --fd-rule selects another
rule for the main table. The sensitivity list always holds every rule not
used for the main table ("fd_rule_<name>"), each with the sample it leaves
(n), which are the sensitivity analyses of deviation 5a.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

from . import analyze as an
from . import denoise as dn
from . import participant as pt

PRIMARY_Z = "z__amygdala_bilateral__vmpfc_fmc"
SECONDARY_Z = "z__amygdala_bilateral__subcallosal"


def read_table(path: Path, id_col: str, needed: list[str]) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", dtype=str)
    missing = [c for c in [id_col] + needed if c not in df.columns]
    if missing:
        raise KeyError(f"{path.name}: missing {missing}; columns are {list(df.columns)}")
    df = df[[id_col] + needed].rename(columns={id_col: "participant_id"})
    df["participant_id"] = df["participant_id"].str.strip().map(
        lambda s: s if s.startswith("sub-") else f"sub-{s}")
    if df["participant_id"].duplicated().any():
        raise ValueError(f"{path.name}: duplicate participant ids")
    return df


def scanner_site(conn_root: Path, pid: str) -> str | None:
    qc = Path(conn_root) / pid / f"{pid}_qc.json"
    if not qc.exists():
        return None
    runs = json.loads(qc.read_text()).get("runs", [])
    return (runs[0].get("scanner") or {}).get("InstitutionName") if runs else None


def assemble(a: argparse.Namespace, gsr: bool = False,
             rule: str | None = None) -> pd.DataFrame:
    """Merge outcomes, CTQ and demographics; keep included participants."""
    out = pt.build_outcome_table(a.conn_root, gsr=gsr, rule=rule or a.fd_rule)
    ctq = read_table(a.ctq, a.id_col, an.CTQ_SUBSCALES + ["ctqscore_val"])
    demo_cols = [a.age_col, a.sex_col] + [c for c in (a.site_col, a.group_col) if c]
    demos = read_table(a.demos, a.id_col, demo_cols)
    df = out.merge(ctq, on="participant_id", how="inner")
    df = df.merge(demos, on="participant_id", how="inner")
    df["ctq_total"] = an.ctq_total(df)
    df["age"] = pd.to_numeric(df[a.age_col], errors="coerce")
    df["sex"] = df[a.sex_col]
    df["site"] = (df[a.site_col] if a.site_col else
                  df["participant_id"].map(lambda p: scanner_site(a.conn_root, p)))
    if df["site"].isna().any():
        raise ValueError(f"site unknown for {int(df['site'].isna().sum())} "
                         "participants; pass --site-col or check the QC JSON")
    for sc in an.CTQ_SUBSCALES + ["ctqscore_val"]:
        df[sc] = pd.to_numeric(df[sc], errors="coerce").mask(
            lambda s: s.isin(an.MISSING_CODES))
    return df[df["included"].astype(bool)]


NUMERIC = ["age", "mean_fd", "n_retained"]
CATEGORICAL = ["sex", "site"]


def sensitivity(a: argparse.Namespace, df: pd.DataFrame) -> list[dict]:
    """The five prereg sensitivity analyses plus the deviation 1 aCompCor one
    and the deviation 5a FD rules (every rule not used for the main table)."""
    res = []
    for other in (r for r in dn.RULES if r != a.fd_rule):
        odf = assemble(a, rule=other)
        res += _tag(f"fd_rule_{other}", an.primary_and_secondary(
            odf, PRIMARY_Z, SECONDARY_Z, NUMERIC, CATEGORICAL))
    gdf = assemble(a, gsr=True)
    res += _tag("gsr", an.primary_and_secondary(gdf, PRIMARY_Z, SECONDARY_Z,
                                                NUMERIC, CATEGORICAL))
    for side in ("l", "r"):
        res += _tag(f"amygdala_{side}", an.primary_and_secondary(
            df, f"z__amygdala_{side}__vmpfc_fmc", f"z__amygdala_{side}__subcallosal",
            NUMERIC, CATEGORICAL))
    for sc in an.CTQ_SUBSCALES:
        res += _tag(f"subscale_{sc}", an.primary_and_secondary(
            df, PRIMARY_Z, SECONDARY_Z, NUMERIC, CATEGORICAL, exposure=sc))
    val_max = df["ctqscore_val"].max()
    kept = df[df["ctqscore_val"] < val_max]
    res += _tag("exclude_max_minimization", an.primary_and_secondary(
        kept, PRIMARY_Z, SECONDARY_Z, NUMERIC, CATEGORICAL))
    res += _tag("exclude_compcor_short", an.primary_and_secondary(
        an.exclude_compcor_short(df), PRIMARY_Z, SECONDARY_Z, NUMERIC, CATEGORICAL))
    if a.group_col:
        res += _tag("plus_diagnostic_group", an.primary_and_secondary(
            df, PRIMARY_Z, SECONDARY_Z, NUMERIC, CATEGORICAL + [a.group_col]))
    return res


def _tag(name: str, rows: list[dict]) -> list[dict]:
    for r in rows:
        r["sensitivity"] = name
        r["status"] = "exploratory"
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="prereg 01 analysis, run once")
    ap.add_argument("--conn-root", type=Path, required=True)
    ap.add_argument("--ctq", type=Path, required=True)
    ap.add_argument("--demos", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--id-col", required=True)
    ap.add_argument("--age-col", required=True)
    ap.add_argument("--sex-col", required=True)
    ap.add_argument("--site-col")
    ap.add_argument("--group-col")
    ap.add_argument("--fd-rule", choices=dn.RULES, default=dn.PRIMARY_RULE,
                    help="censoring/exclusion FD rule for the main table "
                         "(deviation 5a: lowpass is primary; unfiltered, "
                         "bandstop and lowpass_strict are sensitivity rules)")
    ap.add_argument("--compcor-full-only", action="store_true",
                    help="deviation 1 sensitivity as the main table: keep only "
                         "participants with 5 aCompCor components per mask")
    a = ap.parse_args(argv)
    df = assemble(a)
    if a.compcor_full_only:
        df = an.exclude_compcor_short(df)
    primary = an.primary_and_secondary(df, PRIMARY_Z, SECONDARY_Z, NUMERIC, CATEGORICAL)
    result = {"prereg_sha256": "4d4681b9f44188b37e60fd9c53d94a85e01cd1529f4d2be7228a42a3ff36f753",
              "n_after_merge": int(len(df)), "registered": primary,
              "sensitivity": sensitivity(a, df),
              "compcor_full_only": a.compcor_full_only, "fd_rule": a.fd_rule}
    a.out.write_text(json.dumps(result, indent=2, default=float))
    print(f"[run_analysis] wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
