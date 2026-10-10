# Pre-registration 07: microtubule-regulator gene-set screen after chronic social defeat

Version 2, 2026-10-09 (version 1 committed as 16b34fd). Version 1 was written 2026-10-09 before any expression data, count matrix or
supplementary file of any dataset named here was downloaded or opened. Source
brief: project-docs/briefs/07-neuronal-microtubules.md, sections 7 and 8.
The frozen gene list is the sibling file `07-geneset-M.txt`; its SHA-256 and
this file's SHA-256 are recorded in `07-LOG.md` before any download.

## Question and decision

Question: in mouse medial prefrontal cortex, does chronic social defeat stress
shift mRNA levels of a fixed set of microtubule regulators, relative to random
genes of similar expression level?

Decision informed: whether transcript-level microtubule work is worth more
effort. Change trigger (from the brief): a null or unreplicated result moves
the next step to protein or phospho-proteomic data.

## Gene set M (32 genes, frozen)

| Gene | Reason for inclusion |
|---|---|
| Tuba1a | Main neuronal alpha-tubulin isotype; the polymer subunit itself. |
| Tubb2a | Neuron-enriched beta-tubulin isotype. |
| Tubb3 | Neuron-specific beta-tubulin isotype, a marker of neuronal microtubules. |
| Mapt | Tau; the MAP in the stress-to-dendrite chain (brief section 3). |
| Map2 | Dendritic MAP required for dendrite elongation. |
| Map1a | Major dendritic MAP in mature neurons. |
| Map1b | Major MAP in developing and remodeling neurites. |
| Map6 | STOP protein; stabilizes neuronal microtubules against cold and drugs. |
| Dcx | Doublecortin; microtubule-binding stabilizer in immature neurons. |
| Mapre1 | EB1; plus-end tracking protein, marks growing ends. |
| Mapre3 | EB3; neuronal +TIP that drives microtubule entry into spines. |
| Stmn1 | Stathmin; tubulin-sequestering destabilizer. |
| Stmn2 | SCG10; neuronal stathmin, regulates dynamics in neurites. |
| Stmn3 | SCLIP; neuronal stathmin family member. |
| Stmn4 | RB3; neuronal stathmin family member. |
| Spast | Spastin; microtubule-severing enzyme that shapes branching. |
| Katna1 | Katanin p60; catalytic microtubule-severing subunit. |
| Katnb1 | Katanin p80; regulatory subunit of katanin. |
| Kif5a | Kinesin-1 heavy chain, neuron-specific; transport on acetylated tracks. |
| Kif5b | Kinesin-1 heavy chain, ubiquitous isoform. |
| Kif5c | Kinesin-1 heavy chain, neuron-enriched isoform. |
| Atat1 | Alpha-tubulin K40 acetyltransferase; marks long-lived microtubules. |
| Hdac6 | Main alpha-tubulin deacetylase; stress-linked in the Sotiropoulos abstracts. |
| Sirt2 | Second alpha-tubulin deacetylase. |
| Ttll1 | Polyglutamylase, main neuronal glutamylase complex subunit. |
| Ttll6 | Polyglutamylase (elongase). |
| Ttll7 | Polyglutamylase abundant in neurons. |
| Agtpbp1 | CCP1, deglutamylase; loss causes neurodegeneration in mice. |
| Agbl5 | CCP5, deglutamylase removing branch-point glutamates. |
| Vash1 | Vasohibin-1, tubulin detyrosinase. |
| Vash2 | Vasohibin-2, tubulin detyrosinase. |
| Svbp | Small vasohibin-binding protein; required partner of Vash1/2. |

Changes from the brief's draft list: "Ccp1/5" written as the mouse symbols
Agtpbp1 and Agbl5; Svbp added because the vasohibins need it to act. No other
change. Genes absent from a dataset after filtering are dropped from that
dataset's test and listed in the result; the set is not refilled.

## Prediction

Direction: DOWN. The mean gene-level statistic of M in defeated mice is lower
than in controls, relative to expression-matched random sets. Basis: inferred
from apical dendrite loss in stressed mPFC (brief section 3). Confidence in the
prediction: low.

## Data sets and roles

1. Discovery: GSE109315, C57BL/6Crl, mPFC. Primary contrast: all defeated mice
   (susceptible plus resilient pooled) versus controls. Secondary contrasts,
   reported but not used for the decision: susceptible vs control, resilient vs
   control.
2. Held-out A (same series, different strain): GSE109315, DBA/2Crl, mPFC,
   defeated vs control.
3. Held-out B (different lab, small n): GSE127812, PFC, defeated vs control.
   Direction only.
4. Held-out C (different lab, larger n): GSE72343 (Bagot et al., Nestler lab,
   PMID 27181059, C57BL/6J males, GPL13112). Named in version 2, see below.
5. Deferred, not part of this first analysis: GSE138670 (sorted interneurons),
   GSE81587 (n = 2 per group), vHPC and BNST in GSE109315.

Sample labels (strain, region, condition, platform) are taken from GEO sample
metadata. Reading metadata is allowed before analysis; reading expression
values is not.

## Method (fixed)

Implementation: Python 3.12, numpy, scipy, pandas. R and limma are not
installed on this workstation, so the brief's limma-voom step is replaced by a
limma-trend-like procedure written in Python. This is a declared change from
the brief, made before data.

1. Input: raw gene-level counts from GEO supplementary files. If only
   normalized values exist, the deviation is logged and the values are used on
   a log scale without renormalization.
2. Gene IDs mapped to mouse gene symbols (from the file, or from Ensembl IDs
   via the file's own annotation; any other mapping source is logged).
3. Filter: keep genes with CPM >= 1 in at least k samples, k = size of the
   smallest group in the contrast.
4. Normalization: median-of-ratios size factors; log2 CPM with prior count 0.5.
5. Per-gene linear model: ~ condition (+ platform when the subset spans both
   GPL13112 and GPL19057, + other batch fields named in the metadata, each
   logged). Empirical Bayes variance moderation with a single prior (Smyth
   2004 moment estimator). Gene-level statistic: moderated t for the
   condition coefficient.
6. Primary test: competitive random-set test. Set statistic = mean moderated t
   over the M genes present. Null = 10,000 random gene sets of the same size,
   each M gene replaced by a random non-M gene from the same expression bin
   (20 equal-count bins of mean log2 CPM). One-sided p for DOWN =
   (1 + number of random sets with statistic <= observed) / 10,001. Two-sided
   p also reported. Random seed 7.
7. Robustness (reported, not decisive): (a) leave-one-gene-out range of the set
   statistic and its p; (b) sample-label permutation test, 2,000 permutations
   of condition labels within platform strata, which keeps inter-gene
   correlation that the random-set test ignores. If (b) gives two-sided
   p >= 0.05 where the primary test gave p < 0.05, the result is labeled
   "fragile".
8. Positive control: Fkbp5 and Sgk1, gene-level. Pass = both have positive
   log fold change in defeated vs control and at least one has one-sided
   moderated p < 0.05. If it fails in discovery, sample labels are rechecked
   first; the M test is reported as "uninterpretable" until the cause is found.
9. Negative control: ribosomal protein genes (symbols matching ^Rp[ls]\d+[a-z]?$,
   excluding mitochondrial Mrp genes), same random-set test. A shift with
   two-sided p < 0.05 is flagged as possible composition bias.
10. QC: PCA of the subset, colored by condition and platform, written to the
    results folder. No sample is removed without a written reason in the
    deviations section of the result.

## Decision criteria

Support: discovery one-sided p < 0.05 for DOWN; held-out A one-sided p < 0.05
DOWN; held-out B same sign (negative set statistic); held-out C one-sided
p < 0.05 DOWN; positive control passes in discovery.

Null: discovery one-sided p >= 0.05, or discovery significant in the opposite
direction (two-sided p < 0.05, statistic positive). Reported as a null for
transcript-level screening; this does not rule out post-translational change.

Ambiguous / unreplicated: discovery passes but one or more held-out sets
fail its criterion. Each held-out result is reported separately.

## What changes after data is seen

Nothing above. Any change after the first download is written to the
"Deviations" section of the result and of FINDINGS.md, with the reason.

## Version 2 addendum: held-out C (added before any expression value was opened)

Search: NCBI E-utilities esearch on db=gds, term `("social defeat") AND
(prefrontal OR mPFC OR PFC) AND "Mus musculus"[orgn] AND gse[entry_type]`,
2026-10-09, 31 series returned. Candidates were screened on GEO record text and
sample metadata only (titles, characteristics, supplementary file names and
sizes). No supplementary file was downloaded at this step.

Chosen: GSE72343, "Circuit-wide transcriptional profiling reveals region
specific gene co-expression networks regulating depression susceptibility".
140 samples over 4 regions and 3 time points. Lab: Nestler (Mount Sinai);
GSE109315 is from a different lab (Helsinki; C57BL/6Crl and DBA/2Crl).
Verified from sample metadata, region "adult prefrontal cortex":

| Time point | Control | Susceptible | Resilient |
|---|---|---|---|
| 48h post CSDS | 3 | 3 | 3 |
| 28d post CSDS | 4 | 3 | 5 |
| 28d +1h stress post CSDS | 4 | 4 | 4 |

Held-out C contrast: PFC samples at 48h and 28d (control n = 7, defeated
n = 14), model ~ timepoint + condition, defeated = susceptible + resilient.
The "28d +1h stress" group is excluded because it adds an acute stressor on
the day of tissue collection, a different exposure from the discovery set
(GSE109315 collected tissue 6 to 8 days after the last defeat, per its record).
Criterion: one-sided p < 0.05 for DOWN in the primary random-set test.

Pre-specified fallback, decided now: GSE72343 has one supplementary file,
GSE72343_processed_data_files.tar.gz (2.2 MB per the GEO directory listing,
small for 140 samples). If it holds no per-sample PFC expression values, held-out
C becomes GSE161726 (Kalisch and Mueller labs, Mainz, PMID 37068238): mPFC,
control n = 4, defeated n = 15 (non-avoiders 5, indiscriminate avoiders 6,
discriminating avoiders 4), SMART-Seq v4 low input, contrast defeated vs control,
same criterion. Whether the fallback is used is decided from file names and
column headers only, and is logged.

Known before data, from the GSE109315 record: its processed files are named
`*_counts_logCPM.txt.gz`, so they may hold logCPM rather than raw counts.
Method step 1 already covers this case.

Other candidates considered and not chosen: GSE161726 (smaller control group,
low-input libraries; kept as fallback), GSE146845 (PFC, 4 to 5 per group with
a drug arm; smaller), GSE81672 (same lab as GSE72343, 3 to 5 per group),
GSE325386 (2026, social hierarchy design; region mix not checked), array-based
series (different platform type).
