# Findings

Append-only. Each entry: question, receipts, result with intervals, does not prove.

## F-04-1 (2026-10-09). Citing sentences for two CMN papers: how often do they claim more than the study measured?

Question. When papers cite Simard et al. 1997 (Nature, doi:10.1038/41557, isotope
transfer between birch and Douglas-fir seedlings) or Beiler et al. 2010 (New
Phytologist, doi:10.1111/j.1469-8137.2009.03069.x, Rhizopogon genet mapping in one
plot), how often does the citing sentence claim more than the study measured?
Decision informed: which citation patterns need correcting in public and management
writing (brief 04, section 6), and whether Karst et al. 2023 overcitation rates hold
on an independent sample. Both DOIs were checked in Crossref (high confidence).

Receipts.
- Codebook, fixed before retrieval: project-docs/audit04/CODEBOOK.md
  (SHA-256 cc3d13ca9ca74d7d3bf9fff089339ae9265829304a2ebc28e925600e9875299f, commit fa145a9).
- Log: project-docs/audit04/LOG.md. Code: src/audit04/ (fetch, sample, stats,
  analyze); tests/test_audit04_stats.py.
- Data: data/audit04/coverage.json, sample.csv, units_blind.csv, codes_A.csv,
  codes_B.csv, merged.csv, results.md. Raw S2 JSON in data/audit04/raw/ (not committed;
  rerun src/audit04/fetch.py).

Coverage (observed). Semantic Scholar returned 891 citing records for Simard 1997 and
226 for Beiler 2010. Only 334 (37%) and 105 (46%) carried any citation context. The
sample is 100 citing papers per target, one context each, seed 20261009, stratified by
year bucket.

Agreement. Two coders (coder A, the lead session; coder B, a separate subagent given
only the codebook and the blind units). Cohen's kappa 0.893 over four codes, raw
agreement 92.5% (Simard 0.929, Beiler 0.855). 15 of 200 units disagreed; both code
files are kept unchanged.

Result. Strict estimate counts a unit as OVERREACH only when both coders said so;
lenient counts either coder. Wilson 95% intervals.

| Target | Strict, all units | Lenient, all units | Strict, of units both coded ACCURATE or OVERREACH |
|---|---|---|---|
| Simard 1997 | 37/100 = 37.0% [28.2, 46.8] | 40.0% [30.9, 49.8] | 37/70 = 52.9% [41.3, 64.1] |
| Beiler 2010 | 25/100 = 25.0% [17.5, 34.3] | 29.0% [21.0, 38.5] | 25/65 = 38.5% [27.6, 50.6] |

By year bucket, strict share of all units:
- Simard 1997: 1997-2009 16/43 = 37.2% [24.4, 52.1]; 2010-2016 10/21 = 47.6% [28.3, 67.6];
  2017-2022 6/20 = 30.0% [14.5, 51.9]; 2023-2026 4/14 = 28.6% [11.7, 54.6].
- Beiler 2010: 2010-2016 8/45 = 17.8% [9.3, 31.3]; 2017-2022 8/29 = 27.6% [14.7, 45.7];
  2023-2026 9/23 = 39.1% [22.2, 59.2].
The intervals overlap in every bucket. No trend is claimed for either paper. The
rising Beiler point estimates after 2023 are a hypothesis for a larger sample, not
a finding.

Dominant overreach types among strict OVERREACH units (a unit can carry several):
- Simard 1997 (n 37): O8 system mismatch 21, O2 seedling or tree benefit 17, O5 ubiquity 6,
  O1 magnitude 5. From coder notes, the O8 units split into two kinds. About 10 attribute
  the transfer to mature, canopy or "larger" trees, though the study used seedlings. About
  9 extend carbon to water, nitrogen, phosphorus or "nutrients". Kin (1) and signal (3)
  claims are rare.
- Beiler 2010 (n 25): O7 resource flow claimed from a structure-only study 10, O5 ubiquity 8,
  O3 kin or mother tree 6, O2 benefit 6, O4 signals or communication 5.

Sensitivity. Simard 1997 drops to 15/63 = 23.8% [15.0, 35.6] when hedged sentences
("may", "could") are excluded. Beiler 2010 drops to 20/89 = 22.5% [15.0, 32.2]. Restricted
to single-citation sentences, the shares are 34.0% [22.4, 47.8] for Simard 1997 and
22.0% [12.0, 36.7] for Beiler 2010.

Comparison (inferred, low to moderate confidence). Karst et al. 2023 report about 25%
unsupported citations for structure papers and nearly 50% for function papers. The
substantive-denominator shares here (38.5% for Beiler 2010, a structure paper; 52.9%
for Simard 1997, a function paper) are in the same range. The rubrics differ, so this
is not a replication of their numbers.

Does not prove.
- S2 context coverage is partial (37% and 46% of citing records). Papers without
  extractable contexts, often paywalled or older ones, may cite differently.
- A citing sentence may rely on other sources too. Multi-citation sentences were
  coded against the whole claim. The single-citation subset is smaller and has wider
  intervals.
- "What was measured" comes from abstract-level reading in brief 04. Full texts of
  both papers were not opened, so some ACCURATE or OVERREACH calls could change with
  the full text (for example "most trees linked" or the 37 and 47 tree link counts).
- Both coders are language models working from the same codebook. High kappa shows
  the rubric is applied consistently. It does not show that a human ecologist would
  code the same way. Coder B ran in a session that could reach coder A's scratch
  files and reported not opening them. That was self-reported, not enforced.
- Some S2 contexts are misattributed (no matching citation marker) or cite
  "Simard 1997a/b", which may be a different 1997 paper. These were coded UNCLEAR or
  by content.
- OVERREACH means the sentence claims more than this one study measured. It does not
  mean the claim is false. Other studies may support it.
