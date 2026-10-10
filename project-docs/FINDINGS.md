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

## F-07-1 (2026-10-09). Microtubule-regulator mRNA after chronic social defeat, mouse mPFC: null in discovery

Question. In mouse mPFC, does chronic social defeat shift mRNA of a fixed 32-gene
microtubule-regulator set (tubulins, MAPs, stathmins, severing enzymes, kinesin-1,
+TIPs, tubulin-modifying enzymes) DOWN, relative to random genes of matched
expression? Decision informed (brief 07, section 1): whether transcript-level
microtubule work is worth more effort, or the next step moves to protein and
phospho-proteomic data.

Receipts.
- Pre-registration: project-docs/prereg/07-microtubule-screen.md, v1 commit 16b34fd
  (SHA-256 4ec33fd8...4fef95), v2 commit c936dd6 (SHA-256 b21b3093...fbd1ca), both
  committed before any expression file was downloaded. Gene set:
  project-docs/prereg/07-geneset-M.txt (SHA-256 0dd7f70a...4ad3a99). Hash log:
  project-docs/prereg/07-LOG.md.
- Data receipts (URLs, bytes, SHA-256): project-docs/prereg/07-DATA.md. Data live under
  H:\bio-data\screen07, not in the repo.
- Code: src/screen07/ (Python 3.12, numpy/scipy/pandas). Run from src/:
  `python -m screen07.run --data H:/bio-data/screen07 --repo C:/dev/bio-research`.
  Output: project-docs/prereg/07-results/07-results.json, per-set M gene tables, PCA plots.
- Test: mean moderated t of M vs 10,000 expression-matched random sets (20 bins, seed 7);
  leave-one-gene-out; 2,000 within-strata label permutations of mean t(M) minus mean t(all).

Result per set (observed). "Null mean" is the mean of the 10,000 random-set statistics.

| Set | n ctrl / defeated | M genes | Set mean t | Null mean (SD) | p DOWN (random sets) | LOO p DOWN range | Permutation p two-sided | Pre-registered criterion |
|---|---|---|---|---|---|---|---|---|
| Discovery GSE109315 C57BL/6Crl mPFC | 6 / 12 | 31 | -0.18 | -0.09 (0.19) | 0.31 | 0.19 to 0.43 | 0.51 | p < 0.05: FAIL |
| Held-out A GSE109315 DBA/2Crl mPFC | 6 / 8 | 31 | -0.58 | -0.37 (0.16) | 0.095 | 0.046 to 0.17 | 0.046 | p < 0.05: FAIL |
| Held-out B GSE127812 PFC | 3 / 3 | 29 | +0.23 | +0.31 (0.27) | 0.40 | 0.20 to 0.55 | 0.95 | negative sign: FAIL |
| Held-out C GSE161726 mPFC (fallback) | 4 / 15 | 31 | -0.31 | +0.12 (0.18) | 0.0067 | 0.0023 to 0.019 | 0.42 | p < 0.05: PASS, labeled fragile |

Secondary contrasts in discovery (not decisive): susceptible vs control p DOWN 0.45;
resilient vs control p DOWN 0.10. No single M gene reached p < 0.01 in any set
(discovery minimum: Kif5b, t = -2.18, p = 0.043, uncorrected).

Verdict under the pre-registration: NULL. The discovery test failed (p = 0.31), so
the held-out sets cannot turn this into support. Confidence: high that the
pre-registered test is null on these data; the screen had low power for small
shifts (12 vs 6 animals), so "no shift" is not shown.

Positive control (Fkbp5 and Sgk1 up). Discovery: FAIL. Fkbp5 up (log2FC 0.21,
p = 0.034 one-sided); Sgk1 flat (log2FC -0.01, p = 0.54). Held-out A: fail (both
flat). Held-out B: Fkbp5 filtered out, Sgk1 up p = 0.026, fail by rule. Held-out C:
pass (Sgk1 p = 0.028, Fkbp5 positive). As pre-registered, sample labels were
rechecked first: matrix columns match GEO titles, and group sizes match the series
design (6/6/6 and 6/8). Per the rule, the discovery M result is also labeled
"uninterpretable" until the cause is found. Inferred cause, not tested: GSE109315
collected tissue 6 to 8 days after the last defeat, and Sgk1 is a fast
glucocorticoid-response gene, so the control was a poor choice for this timing
(confidence: moderate). Under either label the discovery set gives no support.

Negative control (ribosomal protein genes, 69 to 74 genes). It shifted in all four
primary sets (two-sided p <= 0.03; down in discovery, B and C, up in A). The
pre-registration flags this as possible composition bias. A second reading fits
too: ribosomal genes are tightly co-regulated, and a random-set test that treats
genes as independent overstates significance for any co-regulated set. Held-out C
supports this reading: the random-set test gave p = 0.0067 and the label
permutation, which keeps gene-gene correlation, gave p = 0.42 (inferred, moderate
confidence). Check-the-check lesson: the pre-registered primary test is
anticonservative for co-regulated sets. Its nulls are informative; its positives
need the permutation or a correlation-aware test (camera or rotation) to agree.

Deviations from the pre-registration (all logged, none changed a decision rule):
1. GSE72343 held only per-contrast DE tables, no per-sample values. The
   pre-specified fallback GSE161726 mPFC was used for held-out C.
2. GSE109315 deposited logCPM, not counts (anticipated in v2). Used as deposited;
   the CPM >= 1 filter became logCPM >= 0. All mPFC samples are on GPL19057, so no
   platform covariate was needed (brief section 7 concern does not apply to mPFC).
3. GSE127812 deposited transcript-level RPKM. Summed to gene symbol, then
   log2(RPKM + 1), filter RPKM >= 1 in 3 samples. The transcript-to-gene sum is a
   step the pre-registration did not name.
4. Ensembl IDs in GSE109315 and GSE161726 were mapped to symbols with the GENCODE
   vM17 GTF (an outside source; GSE161726 used M17, the GSE109315 annotation release
   is unknown). 64 and 86 IDs did not map.
5. The permutation statistic (mean t of M minus mean t of all genes) was fixed in
   code before the first run; the pre-registration did not spell out its form.
6. GSE161726 file paths name library pools ("Pool1"); pools are not in the GEO
   metadata, so they were not modeled, as the pre-registration requires.
7. Ttll6 failed the expression filter in every set; Vash2 and Svbp also failed in
   GSE127812. The set was not refilled.

Decision. The brief's change trigger fires: deprioritize transcript-level
microtubule screening in bulk tissue. Next step per brief section 8.10: a
protein-level source (phospho-proteomics in a stress model) rather than more
mRNA sets. If a later mRNA screen is run, use a correlation-aware primary test.

Does not prove.
- mRNA cannot see tau phosphorylation, tubulin modification state or microtubule
  stability. A null here leaves the stress-to-tau-to-microtubule chain untouched.
- Bulk tissue mixes neurons, glia and vessels; a neuron-specific or
  dendrite-local shift can be diluted below detection.
- Mouse chronic social defeat, males only, one tissue time point per set; not human
  trauma, not chronic restraint (the model behind the dendrite-atrophy findings).
- A null with 6 vs 12 animals does not exclude small effects; the held-out C
  signal is fragile and from low-input libraries with visible PCA outliers (no
  sample removed).

## F-07b-1 (2026-10-09). Stress-linked tau phosphosites, mouse mPFC after CUMS (PXD016302): weak null

Question. In mouse mPFC after chronic unpredictable mild stress, are the tau
sites that antibody studies reported as stress-increased (human 2N4R S202, T205,
T231, S396, S404, S409; Sotiropoulos 2011, Rissman 2012, both re-read from full
text) higher in the deposited label-free phospho table? Decision informed (brief
07b): whether the protein-level arm continues on deposited tables or moves to
raw-file reanalysis or new tissue.

Receipts.
- Pre-registration: project-docs/prereg/07b-phospho-tau.md, commit 05cb868,
  SHA-256 d9b5ce94...a573fc (HASHES.md), committed before any table was
  downloaded.
- Data receipts (URLs, bytes, SHA-256, licences): project-docs/prereg/07b-DATA.md.
  Data under H:\bio-data\proteomics. PXD024829 files match the deposited SHA-1.
- Code: src/phospho07b/ (Python 3.12, numpy/scipy/pandas). Run from src/:
  `python -m phospho07b.run posctl --data H:/bio-data/proteomics/PXD024829 --fasta H:/bio-data/proteomics/ref/mouse_sprot_iso.fasta.gz --out ...`
  and `python -m phospho07b.run primary --data H:/bio-data/proteomics/PXD016302 --control A B C --stress D E F --out ...`.
  Outputs: project-docs/prereg/07b-results/*.json.
- Tests: tests/test_phospho07b_{stats,settest,seqmap,loaders}.py, 22 passed
  (planted effect recovered; exact 3 vs 3 permutation p = 1/20 one-sided and
  2/20 two-sided at the floor; rotation test calibrated on correlated null sets,
  at most 12 of 100 calls; the independent random-set test overcalls the same
  correlated sets, the F-07-1 lesson; decision-rule branches).
- Numbering: mouse site = human 2N4R minus 11 in P10637-2; in canonical P10637,
  human S202/T205/T231/S396/S404/S409 = mouse S494/T497/T523/S688/S696/S701. The
  "Mapt T523" of PXD057176 is human T231.

Positive control (PXD024829, dHC, 6 min swim vs home cage, 6 vs 7 mice). PASS.
Syn1 pS553: log2FC +1.35 (about 2.5-fold; the paper's western gave about
3-fold), moderated t 6.12, Hedges g 3.47, exact permutation p_UP = 1/1716 (the
observed labeling ranks first of all 1,716). 643 of 7,781 tested sites at BH
q < 0.05 (the paper reported 847 modified peptides with its own pipeline).

Primary (PXD016302 mPFC, control+saline A-C vs CUMS+saline D-F, 3 vs 3).
Coverage gate passed: 5 of 6 primary sites quantified in all 6 samples; S409
absent. 12,230 sites after filters; 7,075 testable.

| Site (human / mouse canonical) | log2FC CUMS - control | Moderated t | Hedges g |
|---|---|---|---|
| S202 / S494 | +0.42 | 1.30 | 0.79 |
| T205 / T497 | +0.05 | 0.18 | 0.12 |
| T231 / T523 | -0.05 | -0.21 | -0.15 |
| S396 / S688 | +0.21 | 1.04 | 1.15 |
| S404 / S696 | -0.92 | -1.12 | -0.58 |
| S409 / S701 | not quantified | | |
| Secondary S262 / S554 | +0.06 | 0.19 | 0.12 |
| Secondary S356 / S648 | -0.68 | -2.52 | -1.71 |

Set level (5 sites): mean moderated t S = +0.24; mean log2FC -0.06; set-score
difference -0.06, Welch 95% CI -0.72 to +0.60. Exact permutation p_UP = 0.30
(observed labeling ranks 6th of 20; two-sided 0.60). Rotation p_UP = 0.28.
Percentile among 1,000 intensity-matched single-protein random sets: 66.8;
among independent random sets: 61.3. Leave-one-site-out S: -0.03 to +0.58.

Controls in PXD016302.
- Reproduction check: PASS (Rims1 S790 log2FC -1.12, t -4.04; criterion was any
  Rims1 site <= -0.5). Map2 sites ran both ways (descriptive).
- Ribosomal set (9 sites on Rpl12, Rpl14, Rpl23a, Rpl34, Rpl4, Rps10, Rps27, Rps28,
  Rps3): permutation two-sided 0.10 (the floor), rotation two-sided 0.38 (6
  complete sites), independent random-set percentile 8.7, single-protein
  percentile 11.1. Not flagged by the miscalibration rule.
- Calibration panel: 200 random single-protein 5-site sets, 7% at rotation
  two-sided p < 0.05 (limit 15%). PASS.
- Context only: Mapt protein groups in proteinGroups.txt (from the enriched
  run) log2FC +0.30 and +0.09.

Decision under the pre-registered rule: NULL, weak (a 1.5-fold rise not
excluded). No SUGGESTIVE criterion was met. The upper CI bound (+0.60) sits just
above log2(1.5) = 0.585, so a 1.5-fold rise is not excluded. Confidence: high
that the pre-registered test is null on this table; low power (3 vs 3, possibly
pooled) means "no rise" is not shown.

Deviations (none changed a decision rule):
1. A mouse Swiss-Prot reference FASTA was downloaded to place Spectronaut
   peptides (positive control); the pre-registration did not name it.
2. The rotation test uses complete-case set rows only (tau 5 of 5; ribosomal 6
   of 9); the calibration panel draws from complete-case sites. Not specified
   in the pre-registration.
3. Random-set eligibility = sites with at least 2 values per group (the site
   analysis filter); the pre-registration said "eligible" without definition.
4. The PXD016302 table holds 18 undescribed XY-1..XY-18 sample columns. Only
   letter columns A-F were used, which match labeled raw-file names. Labels
   judged unambiguous for A-F.
5. Tau rows in PXD016302 sit on TrEMBL A0A0A0MQC7, whose numbering equals
   P10637 canonical; matching was by 15-mer window as pre-registered.
6. Unquantified sites print a Hedges g in the JSON (computed from fewer than 2
   values per group); those values are not used anywhere.

Next step (change trigger): replication in a second deposited set
(PXD057176 hippocampus or PXD050750 rat hippocampus), with the same code and a
new pre-registration, before any claim; mPFC alone cannot settle the question.

Does not prove.
- A null in mouse mPFC does not contradict the antibody results: those were rat
  hippocampus and PFC (Sotiropoulos) and mouse hippocampus (Rissman, who saw
  no change in mouse isocortex).
- MS single sites are not the joint antibody epitopes (AT8, PHF-1).
- The three replicates per group may be splits of one pooled homogenate of four
  mice (paper text); if so, the effective n is one animal pool per group.
- Phospho change was not adjusted for total tau; no paired global proteome.
- Tissue was taken 1 h after an injection in both arms; acute injection stress
  may mask or mimic chronic effects.
- Nothing here measures microtubule stability. The positive control shows the
  pipeline detects a fast, large site change in 6 vs 7 animals, not that it
  would detect a small chronic one in 3 vs 3.

## F-07c-1 (2026-10-09). Stress-linked tau phosphosites, mouse hippocampus after chronic restraint (PXD057176): null, excludes a 1.5-fold rise

Question. In mouse hippocampus after chronic restraint stress, are the tau
sites that antibody studies reported as stress-increased (human 2N4R S202,
T205, T231, S396, S404, S409) higher in the deposited DIA phospho table?
Motivation: F-07b-1 was a weak null in mPFC, and Rissman 2012 saw the rise in
hippocampus only. Decision informed: whether the deposited-table arm for tau
continues or closes (pre-registration 07c section 1).

Receipts.
- Pre-registration: project-docs/prereg/07c-phospho-tau-hippocampus.md,
  commit bda508e, SHA-256 ae2a23f6...8befe7 (HASHES.md), committed before the
  table was downloaded.
- Data receipts: project-docs/prereg/07c-DATA.md (URLs, bytes, SHA-256,
  licence UNVERIFIED for iProX). Data under H:\bio-data\proteomics.
- Code: src/phospho07b/ extended (blocked.py: per-site sex + stress linear
  model with moderated t, stratified permutation, blocked set score;
  hippo.py and hippo_checks.py: 07c runner, run-name decoding, Y-linked label
  check, reproduction, decision, 07b combination; loaders.py: Spectronaut PTM
  site report; settest.py: rotation test generalized to a design matrix).
  Run from src/: `python -m phospho07b.run hippo --data H:/bio-data/proteomics/PXD057176 --fasta H:/bio-data/proteomics/ref/mouse_sprot_iso.fasta.gz --prior-07b ../project-docs/prereg/07b-results/primary-PXD016302.json --out ...`.
  Outputs: project-docs/prereg/07c-results/*.json.
- Tests: tests/test_phospho07c_{blocked,checks}.py (14 new) plus the 22 of
  07b, 36 passed. New checks: the blocked model reduces to the 07b two-group t;
  a large sex effect does not leak into the stress t; planted stress effect
  recovered (stratified permutation p <= 0.01, interval covers the plant);
  rotation test with the sex design calibrated on correlated null sets (at
  most 12 of 100 calls); label-check, reproduction and decision branches;
  loader drops low-probability and "Filtered" values and sums multiplicities.

Datasets (decoded from metadata only, before any table).
- PXD057176 kept. Supplementary captions on the Springer page give groups
  Ctrl (non-stressed), AD-Sus, Insus, 3 samples per group per sex. File-name
  letter 2 (C, D, I) = Ctrl, AD-Sus, Insus (high confidence). Letter 1
  (C, X) = female, male by pinyin inference (moderate). Table S1 says n = 6
  mice per group per sex for 3 samples, so samples may be two-mouse pools.
- PXD050750 dropped: raw files A1..A9 and 1..6 carry no group label, the
  record says "no PTMs", the paper is closed and its page returned a bot
  challenge. Design and n not decodable. Rat tau windows were mapped anyway
  (all 8 equal the mouse windows) and are recorded in the pre-registration.

Gate.
- Pipeline positive control (PXD024829 Syn1 pS553) re-run with the extended
  code: PASS, output byte-identical to the 07b result (log2FC +1.35, exact
  p_UP = 1/1716).
- In-dataset positive control: none available. The gate here is weaker than
  in 07b and rests on the checks below.
- Run names: the 18 report runs match the 18 decoded file names; the report's
  own R.Condition labels (C_C ... X_I) agree.
- Sex label check: no Y-linked (Ddx3y, Eif2s3y, Kdm5d, Uty) site in the
  table. Sex UNCONFIRMED; per-sex results are labeled by prefix.
- Reproduction (Stmn1 S38, |log2FC| >= 0.263 in a female phenotype vs female
  Ctrl): PASS on the 1.2-fold rule. Prefix C Insus vs Ctrl -0.66 (t -1.62),
  AD-Sus -0.20; prefix X AD-Sus -0.60, Insus +0.21. The passing contrast is
  not itself significant, so this check is weak.
- Calibration panel (200 single-protein 4-site sets, sex-blocked rotation):
  17% at two-sided p < 0.05, above the 15% limit. FAIL. The rotation test is
  labeled miscalibrated and cannot carry a positive call.
- Ribosomal set (4 eligible sites: Rpl12, Rpl18a, Rps2, Rps8): permutation
  two-sided 0.50, rotation two-sided 1.00 (2 complete sites), independent
  random-set percentile 26.4, single-protein percentile 2.9.

Primary (sex-blocked, CRS = AD-Sus + Insus, 12 vs 6). 4,819 sites after
filters; 1,673 eligible (at least 2 values in each sex x stress cell).
Coverage gate passed: 4 of 6 (T205 and S409 not in the table).

| Site (human / mouse canonical) | log2FC CRS - Ctrl (sex-adjusted) | Moderated t | Hedges g |
|---|---|---|---|
| S202 / S494 | +0.18 | 1.46 | 0.34 |
| T205 / T497 | not in table | | |
| T231 / T523 | -0.04 | -0.20 | -0.09 |
| S396 / S688 | +0.16 | 0.82 | 0.38 |
| S404 / S696 | +0.01 | 0.04 | -0.07 |
| S409 / S701 | not in table | | |
| Secondary S262, S356 | not in table | | |

Set level: S = +0.53; mean log2FC +0.08; set-score stress coefficient +0.04,
95% CI -0.25 to +0.33 (df 15). Stratified permutation p_UP = 0.21 (2,001
within-sex labelings). Rotation p_UP = 0.15 (3 complete sites; test flagged).
Single-protein random-set percentile 79.4; independent 76.9.
Leave-one-site-out S: +0.22 to +0.77.

Decision under the pre-registered rule: NULL, excludes a 1.5-fold rise (upper
bound +0.33 < 0.585), with controls flagged (rotation test miscalibrated).
The flag cannot change a null. Confidence: high that the pre-registered
pooled test is null on this table; moderate that it is informative, because
the in-dataset gate is weak.

Descriptive, not decision inputs (per-sex and phenotype looks are several
comparisons; none was pre-registered as a test).
- Prefix C (inferred female, 6 vs 3): S -0.74, permutation p_UP 0.94, set
  difference -0.19 (Welch 95% CI -0.44 to +0.05); T231 -0.57 (t -3.10).
- Prefix X (inferred male, 6 vs 3): S +1.61, exact p_UP 4/84 = 0.048,
  rotation p_UP 0.046 (flagged test), single-protein percentile 99.6; set
  difference +0.34 (Welch 95% CI -0.22 to +0.91); all 4 sites positive.
- The two prefixes point in opposite directions. A sex x stress interaction
  was not pre-registered and was not tested. The prefix X pattern is a lead
  only: one of two sex looks, sex unconfirmed, rotation test flagged, and its
  interval includes zero.
- AD-Sus vs Ctrl: S +0.38, rotation p_UP 0.33. Insus vs Ctrl: S +0.59,
  rotation p_UP 0.055.
- Mapt T523 (the paper's Insus target, human T231): pooled -0.04; Insus vs
  Ctrl -0.03. Not reproduced at the pooled level; prefixes C and X give -0.57
  and +0.50.

How 07b and 07c combine (rule fixed in the 07c pre-registration).
- 07b NULL (weak) in mPFC after CUMS, 07c NULL (excludes 1.5-fold) in
  hippocampus after CRS: null in two regions, two labs, two stress models,
  two platforms. Under the rule, the deposited-table arm for tau closes;
  brief 07b section 6 routes 2 to 4 (raw-file reanalysis, targeted antibody
  work, human cohorts) remain.
- Fixed-effect combination of the set-score effects (descriptive, different
  regions and models): +0.01, 95% CI -0.21 to +0.24 (SE 07b 0.22, 07c 0.14).
- The Rissman hippocampus-only pattern is not reproduced in pooled sexes.
  The prefix X (inferred male) look is the only place an UP pattern appears.
  The sex of Rissman's mice was not recorded in the 07b reading (UNVERIFIED).

Deviations (none changed a decision rule):
1. Format (a) used the long "PTMSiteReport (Normal)" file. The pivot version
   has no site probability, so it could not apply the 0.75 rule.
2. Spectronaut had already filtered at site probability 0.75, so the
   pre-registered filter removed nothing more. No imputation flag was set.
3. Gene names came from the mouse Swiss-Prot FASTA by accession (the report
   has no gene column); 11 of 4,819 sites have no gene name.
4. Per-sex output is keyed by prefix because sex was unconfirmed; the code
   still treats prefix X as "sex = 1" for blocking, which does not change the
   blocked test.
5. The rotation function gained a DOWN p-value and a design-matrix form; the
   07b positive control and the 07b primary both re-ran byte-identically
   (SHA-256 b7a2a45d...6c3d and 5355d27b...28ad).

Next step (change trigger met): no further deposited-table tau test without
a new dataset with decodable labels. A sex-specific hippocampal question
(prefix X lead) needs a confirmed-sex dataset or raw-file reanalysis with a
pre-registered interaction test.

Does not prove.
- MS single sites are not the antibody joint epitopes (AT8, PHF-1); T205 and
  S409 were not measured here.
- Samples may be two-mouse pools; effective n may be smaller than 18.
- Stress mice were selected by behaviour into two phenotypes; the pooled
  contrast averages over a selected sample, not a random one.
- The table could not show it detects a true chronic effect: there is no
  in-dataset positive control, the reproduction pass rests on a fold change
  without significance, and the calibration panel failed its limit.
- No total-tau adjustment; no paired global proteome.
- Sex labels are inferred, not confirmed.
- Nothing here measures microtubule stability.

## F-02-1 (2026-10-10). Day-to-day noise floor of hippocampal volume in one person (ds002674, 60 sessions): 0.77 percent; lagged stress association not detected

Question. In one healthy adult scanned on 60 days (30 naturally cycling, 2018;
30 on an oral contraceptive, 2019), how much does an automated hippocampal
volume move from day to day, and does same-day or prior-day Perceived Stress
Scale (PSS) predict it? Decision informed: whether a larger longitudinal test
can resolve the effect sizes in the literature with single scans
(pre-registration section 7).

Receipts.
- Pre-registration: project-docs/prereg/02-tierB-noise-floor.md, commit
  961bf36, SHA-256 7d4a0604...ffd50230 (HASHES.md), committed before any image
  or table value was downloaded.
- Data receipts: project-docs/prereg/02-DATA.md and
  02-results/ds002674-manifest.txt (124 files, 1,103,437,406 bytes, CC0). Data
  under H:\bio-data\ds002674; segmentations under
  H:\bio-data\ds002674-derivatives\synthseg.
- Segmentation: SynthSeg 2.0 robust (BBillot/SynthSeg 2a2aa3b, weights checked
  against FreeSurfer annex SHA-256), CPU, all 60 sessions, 0 failures.
- Code: src/gm02/ (gls.py block-AR(1) GLS with profile-likelihood rho;
  perm.py block permutation; noise.py; data.py; run.py). Run from src/:
  `python -m gm02.run H:/bio-data/ds002674-derivatives/synthseg H:/bio-data/ds002674/participants.tsv ../project-docs/prereg/02-results`.
  Outputs: 02-results/results.json, 02-results/sessions.csv.
- Tests: tests/test_gm02_{gls,perm,noise,run}.py, 13 passed. GLS recovers a
  planted slope (mean 0.6 over 200 runs, 95 percent CI coverage in 0.90 to
  0.99); block permutation on independent AR(1) (rho 0.7) X and Y rejected 2
  of 120 at alpha 0.05 (conservative); end-to-end run recovers a planted
  -1 percent per SD effect.
- Exclusions: none. No duplicate T1w (ses-18 and ses-19 differ by file and
  voxel hash). No session beyond 4 robust SD.

Noise floor (all 60 sessions; percent of the mean).

| Measure | Pooled within-study CV (90% CI) | Study 1 CV | Study 2 CV | Typical error (consecutive days) | Lag-1 autocorr (study 1, 2) |
|---|---|---|---|---|---|
| Hippocampus / TIV (decision quantity) | 0.77 (0.67 to 0.92) | 0.85 | 0.69 | 0.65 | 0.41, 0.10 |
| Hippocampus, raw bilateral (mean 8586 mm^3) | 0.78 (0.68 to 0.92) | 0.88 | 0.67 | 0.64 | 0.43, 0.11 |
| Left hippocampus | 1.09 (0.94 to 1.28) | 1.26 | 0.87 | 0.84 | 0.48, 0.21 |
| Right hippocampus | 0.92 (0.80 to 1.09) | 0.82 | 1.02 | 0.86 | 0.21, 0.08 |
| Amygdala / TIV | 1.21 (1.05 to 1.43) | 1.04 | 1.35 | 1.19 | 0.14, -0.13 |
| TIV (mean 1,499,193 mm^3) | 0.11 (0.10 to 0.13) | 0.11 | 0.11 | 0.11 | -0.23, 0.38 |

- Left and right hippocampal series correlate at r = 0.20 across sessions, so
  most of the day-to-day movement is not shared between hemispheres
  (inferred: mostly measurement noise, not whole-structure change).
- TIV is stable (0.11 percent), so the pipeline sanity flag is off; dividing
  by TIV changes the hippocampal CV very little.
- Regime offset (contraceptive minus natural cycle), hippocampus/TIV: +0.27
  percent, Welch 95% CI -0.13 to +0.67. TIV: -0.12 percent (-0.18 to -0.06).
  Descriptive only; confounded with year and head-case use.

Association (AR(1) GLS, n = 58, rho 0.11; effect in percent of mean
hippocampal volume per 1 SD of PSS; PSS mean 10.5, SD 6.0; block-permutation p,
5000 permutations, alpha 0.025 per term).

| Model | PSS lag 0 (95% CI), p_perm | PSS lag 1 (95% CI), p_perm |
|---|---|---|
| Primary (hippocampus/TIV, full covariates) | -0.24 (-0.47 to -0.01), 0.055 | -0.12 (-0.35 to +0.11), 0.30 |
| (a) no QC covariate | -0.23 (-0.46 to -0.01), 0.055 | -0.12 (-0.35 to +0.10), 0.28 |
| (b) raw volume | -0.25 (-0.47 to -0.02), 0.040 | -0.11 (-0.34 to +0.12), 0.34 |
| (c) sessions 1 to 7 dropped (n = 52) | -0.19 (-0.42 to +0.05), 0.097 | -0.13 (-0.36 to +0.10), 0.26 |
| (d) outliers dropped (none qualified) | same as primary | same as primary |
| Secondary: amygdala/TIV | -0.24 (-0.62 to +0.14), 0.24 | +0.22 (-0.17 to +0.60), 0.24 |

Decision under the pre-registered rules.
- Noise floor: pooled CV 0.77 percent falls in the 0.5 to 1.5 percent band,
  and its 90% CI (0.67 to 0.92) crosses neither threshold, so the call is not
  provisional. Two single scans resolve a change of about 1.8 percent or more
  (inferred: 1.96 x sqrt 2 x typical error 0.65); the 1 to 3
  percent effects in the literature sit at or below that. A larger study
  should use annualized change over 2+ years or several scans per time point,
  with its margin recomputed from this CV.
- Practical status: the pre-registered target, UK Biobank Tier A, is off
  because the operator declined fee-gated data on 2026-10-09. The rule still
  says what any free longitudinal set must offer: repeated scans per visit or
  multi-year intervals. Choosing that dataset is open.
- Association: NOT DETECTED. The lag-0 estimate is negative (higher stress,
  smaller volume), partial r about -0.27, with p_perm 0.055 against an alpha
  of 0.025. It meets neither the pre-registered alpha nor the 0.05 level in
  the primary model, and weakens when the no-head-case sessions are dropped.
  This is a lead to test elsewhere, not a finding. The CI excludes a drop
  larger than about 0.5 percent per SD of PSS on the scan day.

Deviations (all recorded here; none changes a decision).
- FreeSurfer longitudinal and MRIQC were not run (declared in the
  pre-registration before data); the quality covariate is the SynthSeg QC mean.
- The SynthSeg batch was killed by a session restart after 50 of 60 images;
  the remaining 10 ran in a second batch with the same code, weights and venv
  (scripts/gm02_synthseg_batch.sh, systemd transient unit).
- data.py first expected a "subject" column in the per-image CSVs; SynthSeg
  writes an unnamed index column. Fixed before any result was produced.
- Sensitivity (c) drops the outcome rows for sessions 1 to 7 but keeps their
  PSS values as lag-1 inputs for session 8, since the exclusion concerns scan
  quality, not the questionnaire.
- The brief's SIMON comparison (section 6 step 7) was not run.

Does not prove.
- One person, one scanner, one pipeline. The noise floor of FSL FIRST or of
  other people and scanners may differ.
- Volume is net apparent tissue volume, not dendritic, synaptic, glial or
  neuronal change.
- Hydration (water allowed before sessions) and time of day were not measured;
  the protocol only fixes sessions near 10:00. Either could produce a
  day-to-day signal of this size.
- PSS is 24-hour self-report, not cortisol; no hormone values are in the
  dataset. The regime term is confounded with year and head-case use.
- With 58 sessions, power is 80 percent only for |r| of about 0.40 at alpha
  0.025. A null does not exclude smaller within-person associations.

Confidence: high that the hippocampal day-to-day CV with SynthSeg on this
scanner is near 0.7 to 0.9 percent; moderate that it transfers to other
pipelines; low for any stress-to-volume inference.
