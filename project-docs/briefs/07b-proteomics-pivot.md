# Brief 07b: Protein-level pivot for project 07 (tau phosphosites, tubulin modifications, MAP levels)

Date: 2026-10-09. Register: research brief, internal. Follows F-07-1 (mRNA gene-set screen null, positive control failed, random-set test too lenient). Nothing was downloaded. No commit.

Opened-today key. PRIDE = PRIDE Archive API record read today. PX = ProteomeXchange PROXI API record read today. HEAD = file size read today by HTTP HEAD, no body downloaded. EPMC = abstract or open full text read today via Europe PMC. WEB = PMC page read today through a summarizing fetch tool (paraphrase risk, moderate confidence). UNVERIFIED = not opened.

## 1. Result first

1. Open, processed, site-level phospho tables for rodent chronic stress DO exist. Three candidates have search-engine tables beside the raw files (section 3, ranks 1 to 3). Confidence: high that the files are listed; unknown whether tau sites appear in them, because no table was opened.
2. Best for a pre-registered tau-site test: PXD016302 (mouse mPFC, chronic unpredictable mild stress, phospho-enriched, MaxQuant site table 48.5 MB). Its limit is n=3 per group, so only large effects are detectable.
3. Tubulin acetylation and detyrosination cannot be tested from any deposited table I found. All searches I saw list phospho only. A test needs raw-file reanalysis with acetyl-K as a variable modification (hundreds of GB) or antibody work. Detyrosination is a C-terminal change that tryptic MS covers poorly (from memory, low confidence).
4. No open human PFC or hippocampus dataset with a stress or glucocorticoid exposure variable was found. Human data below is a proxy only.
5. MassIVE and jPOST: keyword sweeps through the ProteomeXchange index found no rodent or human brain stress dataset. Not exhaustive; MassIVE-only (MSV) accessions are not in that index and were not queried.

## 2. Stress-linked tau sites (what the primary papers reported)

Source details were read through WEB for both PMC pages. Re-read the full text before freezing the list.

- Sotiropoulos et al. 2011, J Neurosci, DOI 10.1523/JNEUROSCI.0730-11.2011, PMC6633145 [WEB]. Male Wistar rats, 14 months, subgroups n=6 to 7, one month of chronic unpredictable stress, plus corticosterone and Abeta arms. Reported stress-increased sites, hippocampus and PFC: pSer202 (CP13), pThr231 (CP-9), pSer396/404 (PHF-1), pSer409 (PG5). pSer262/356 (12E8) is ambiguous: Results tie it to Abeta plus corticosterone in PFC, the Discussion says stress raised pSer262. Total tau also rose (qualitative scoring).
- Rissman et al. 2012, PNAS, DOI 10.1073/pnas.1203140109, PMC3341026 [WEB]. Mouse hippocampus. AT8 (Ser202/Thr205) and PHF-1 (Ser396/404) rose after acute and repeated restraint. Isocortex and cerebellum showed no change. Western blot n per group not found in the text read.
- Both studies used antibodies. Antibody epitopes are not single-site MS measurements, and numbering follows human 2N4R tau. Mouse and rat Mapt isoform numbering differs; the mapping must be done by sequence alignment and logged.
- Reported in a deposited-data paper: PXD057176 paper lists Mapt T523 and Stmn1 S38 as key phosphorylation targets in Insus groups (Neurochem Res 2026, PMID 42322444, [EPMC] abstract only). Mouse numbering for T523 is UNVERIFIED. Direction is not stated in the abstract.

## 3. Ranked candidates

Fields: accession; URL; species, region, model; n; data type; processed tables; sizes; license; verification.

### Rank 1. PXD016302 (iProX IPX0001870000)
- URL (record read via API): https://proteomecentral.proteomexchange.org/api/proxi/v0.1/datasets/PXD016302 ; iProX page http://www.iprox.org/page/project.html?id=IPX0001870000 is script-rendered and showed no fields.
- Mouse C57BL/6J, mPFC (NAc also present), chronic unpredictable mild stress, with saline or ketamine arms. Xiao et al. 2020, Front Cell Neurosci, PMID 32317933, CC BY paper [EPMC].
- n: control+saline 3, CUMS+saline 3, CUMS+ketamine 3 mPFC raw files (file names). Paper: four mice per group, three biological replicates per group. Whether replicates are pooled animals is unknown. Tissue taken 1 h after an injection (injection stress is shared by both saline arms).
- Data: label-free, phospho-enriched, Q Exactive HF. Paper reports 3,988 quantified mPFC sites. Tau coverage UNVERIFIED.
- Processed: MaxQuant Phospho (STY)Sites.txt 48,487,463 bytes; peptides.txt 20,428,658; proteinGroups.txt 15,106,654 [HEAD]. 18 raw files.
- License: repository license UNVERIFIED. Paper is CC BY.
- Opened today: PX record, file sizes, paper.
- Fit: the only chronic-stress, PFC, phospho-enriched set with a site table. The mPFC contrast of interest is control vs CUMS+saline.

### Rank 2. PXD057176 (iProX IPX0010016000)
- Mouse, hippocampus, chronic restraint stress, females and males, anxiodepression-susceptible vs insusceptible. Paper: Neurochem Res 2026, PMID 42322444 [EPMC].
- n: 18 raw .d.zip files, file-name codes C, D, I and C/X (probably 3 groups x 2 sexes x 3). Meaning of the letters UNVERIFIED. Whether a no-stress control group exists is unclear from the abstract.
- Data: 4D label-free DIA phospho (timsTOF Pro). Tau enrichment of sites reported (Mapt T523).
- Processed: Phospho_Report.zip 65,595,386 bytes [HEAD].
- License UNVERIFIED. Opened today: PX record, sizes, abstract.
- Fit: hippocampus, chronic restraint (the model behind the dendrite-atrophy work), sex as a factor. Contrast design is stress-phenotype, not stress vs naive, until the letters are decoded.

### Rank 3. PXD050750 (iProX IPX0008407000)
- Rat, hippocampus, chronic unpredictable mild stress, proteome plus phospho. Sun et al. 2024, J Psychiatr Res, PMID 38852542 [EPMC abstract]. NMT2 inhibition is a separate arm.
- n: 15 raw files; group sizes UNVERIFIED. PX metadata says "no PTMs" although the paper reports phosphoproteomics (metadata inconsistency).
- Processed: txt8064TQ.rar 160,652,169 bytes; txt.rar 83,352,441 bytes [HEAD]. Whether phospho is enriched UNVERIFIED.
- License UNVERIFIED. Fit: second species and region, same exposure family as Sotiropoulos 2011 (rat CUS). Use after ranks 1 and 2.

### Rank 4. PXD073765 (PRIDE)
- Mouse, mPFC synaptosomes, learned helplessness (inescapable stress), both sexes. Abdulla et al., eNeuro 2026, PMID 41980822, CC BY [EPMC].
- n: 4 mice per sex per condition (paper). Conditions include baseline, no-shock, escapable and inescapable shock.
- Data: label-free; TiO2 phospho-enriched plus global proteome (paper methods). 48 raw files.
- Processed on PRIDE: 11 search XML files (810 MB total), 11 peak files (7.5 GB), no protein or site tables [PRIDE]. Extended-data tables in the paper UNVERIFIED.
- License: CC0 [PRIDE]. Fit: best n and sex balance, but synaptosome fraction, acute-ish paradigm, and PRIDE has no site table. Needs search-output parsing.

### Rank 5. PXD024829 and PXD029903 (PRIDE), positive-control set
- Mouse hippocampus (dorsal and ventral), acute swim stress, phospho-enriched, DIA, 5 to 8 mice per group, time course 0 to 45 min. Nat Commun 2022, PMID 35383160, CC BY [EPMC].
- Processed CSV reports present (names seen; sizes UNVERIFIED). Raw 190.8 GB and 20.1 GB. License CC0 [PRIDE].
- Not chronic. Use only to check that the pipeline detects known rapid phospho-changes and to see tau-site coverage. Paper validated Syn1 pS553 by western.

### Protein-level MAP and tubulin abundance only (no PTM sites)
| Accession | Model | Region | n | Notes |
|---|---|---|---|---|
| PXD037878 (iProX) | CSDS mouse | dmPFC | control, resilient, susceptible, roughly 5/4/? per file names; UNVERIFIED | MaxQuant txt 13.6 and 18.1 MB [HEAD]; Yao 2023 PMID 36759610 CC BY |
| PXD054244 (PRIDE) | chronic restraint mouse | mPFC | UNVERIFIED | TMT; CC0; no processed table listed |
| PXD007573 (PRIDE) | CSDS mouse | PFC | 8 vs 8, pooled | iTRAQ; EBI terms of use; msf and prot.xml |
| PXD047159 (PRIDE) | chronic social isolation rat | PFC synaptosomes | 7 per group | mzTab result file; CC0 |
| PXD074187 (PRIDE) | psychosocial stress x Western diet mouse | frontal cortex, hippocampus | UNVERIFIED | CC0; per-run CSV outputs |
| PXD074547 (PRIDE) | female social defeat mouse | hippocampus | pooled tissue, n UNVERIFIED | LFQ; mzTab per run; CC0 |
| PXD029845 (PRIDE) | human suicide completers vs sudden death controls | PFC BA9/10 | 23 vs 13 | TMT; protein list txt; CC0; not a stress exposure, proxy only |

Checked and excluded: PXD013146 (serum plus brain TMT, nonspecific to MAPs; not opened in detail), PXD034382 (NRBF2 knockout, not stress contrast), PXD076837 (tau IP phospho in fear-conditioned hippocampus; useful for tau-site detectability, not stress).

## 4. Best dataset for the pre-registered test

Primary: PXD016302, mPFC, control vs CUMS+saline, tau and MAP phosphosites. Replication direction check: PXD057176 hippocampus (after decoding groups) and PXD050750 rat hippocampus. Rationale: only chronic-stress PFC set with a site table; two independent labs and two species give a direction check; sites 202/205/231/396/404/409 are the ones Sotiropoulos and Rissman reported.

Hard limits to state before any look:
- n=3 per group. Detectable effect is large (Cohen's d above roughly 2 for 80% power at alpha 0.05, standard two-sample approximation, from memory). A null is weak evidence.
- Site coverage is unknown. Tau is low abundance; if S202/T205/T231/S396/S404 are absent from the table, the primary test is "not measurable", not null.
- Phospho changes can reflect total protein changes. Total tau and protein-level data come from the same run only where a global proteome exists (PXD016302: proteinGroups.txt is the enriched run, UNVERIFIED which).

## 5. Test design (pre-register before opening any table)

Freeze, hash and log before opening data: (a) site list T, human 2N4R numbering S202, T205, T231, S262, S396, S404, S409, mapped to mouse or rat Mapt by alignment with the mapping table committed; (b) direction UP in stress (inferred from antibody studies; confidence moderate); (c) MAP set for protein level: Mapt, Map1a, Map1b, Map2, Map6, Stmn1, Stmn2, Dcx; (d) tubulin PTM readouts are excluded from this dataset round (section 1 item 3).

Step 0, coverage gate. Count how many T sites are quantified in at least 2 of 3 samples per group. If fewer than 3 sites, stop and report "not measurable in PXD016302". Do not substitute sites after looking.

Primary test (correlation-aware):
- Site-level moderated t (limma) on log intensity, localization probability at least 0.75, contrast stress vs control.
- Set-level statistic: mean signed t over T. Reference distribution from sample-label permutation of the full site matrix (all permutations of 6 samples = 20 distinct splits; report the exact minimum achievable p, which is 0.1 two-sided for a 3 vs 3 split, so the primary p cannot go below it). Because 3 vs 3 cannot reach 0.05, the primary decision is effect size with interval plus rank among permutations, and replication across sets, not a p threshold. Add a rotation test (ROAST or camera with estimated inter-site correlation) as secondary. Where permutation and random-set tests disagree, trust permutation (F-07-1 lesson: held-out C gave p 0.0067 by random sets and 0.42 by permutation).
- Never use the independent-gene random-set test as primary.

Controls:
- Negative control, calibrates the test: ribosomal-protein phosphosites (excluding Rps6, an mTOR readout), plus 1,000 random site sets matched on mean intensity AND on number of sites per protein. Required result: permutation p not extreme in more than about 5% of control sets. If the ribosomal set again comes out "significant" under both tests, treat the test as miscalibrated and stop. Record both tests' calls on each control, as F-07-1 should have.
- Positive control, pipeline sensitivity: in PXD024829, acute swim at 0 min vs home cage should show Syn1 pS553 up (paper's western-validated site). If it fails, fix quantification before touching chronic sets.
- Positive control, reproduction: re-derive a headline result stated in each dataset's paper (Map2-related change, PXD016302, per its Figure 4B; Stmn1 S38 and Mapt T523, PXD057176). If the deposited table does not reproduce the paper, label all results from that table "uninterpretable", as F-07-1 did for failed controls.
- Avoid repeating the Sgk1/Fkbp5 timing error: choose controls whose timing matches the sample collection (acute set for fast phosphorylation; chronic sets for sustained changes only).
- Leave-one-site-out range reported. Normalize phospho sites to protein level where a paired global run exists; otherwise report raw phospho only and say protein adjustment was unavailable.

Support: direction UP for at least 3 of the T sites in PXD016302 with permutation rank in the top 5% of control-set statistics, AND same sign in at least one of PXD057176 or PXD050750 after normalization. Null: coverage gate passed and set statistic indistinguishable from matched control sets in all datasets. Not measurable: coverage gate failed.

## 6. Next-best routes if site coverage fails

1. Download the PRIDE search XML for PXD073765 and parse tau sites (810 MB, approval needed).
2. Reanalyze raw files with a tau-focused search (FragPipe or MaxQuant with acetyl-K) for PXD016302 (18 files) or PXD024829. Approval and disk plan needed.
3. Targeted work: pS202/T205 and tubulin K40ac/detyrosination by antibody western on new tissue is outside open-data scope.
4. Human: query AMP-AD (ROSMAP DLPFC proteomics with psychosocial measures) via Synapse. UNVERIFIED that such variables and tau-site data exist; access terms not read.

## 7. Does not prove

- Open candidate tables exist; this brief does not show they contain tau sites, adequate power or a clean stress contrast. No table was opened.
- n=3 per group is a screen. A null leaves the stress-to-tau step untouched; a positive in mouse CUMS does not show microtubule destabilization (that step is inferred, not measured).
- Antibody-defined epitopes in the 2011 and 2012 papers (rat, mouse) are not the same measurement as MS site intensities.
- Different models (CUMS, restraint, defeat, learned helplessness) and regions (mPFC, hippocampus) are pooled only for direction checks.
- Sotiropoulos and Rissman site lists come from a summarizing fetch of PMC pages; verify against full text before freezing.
- Repository licenses for iProX sets were not found (page script-rendered; web search found no iProX license text). PRIDE sets are CC0 per the API. Reuse terms for iProX data UNVERIFIED.
- Search was keyword-based on PRIDE API, the ProteomeXchange index and Europe PMC; absence of a dataset is not shown. MassIVE-only and jPOST-only deposits outside the index were not checked.
- Human proxy (suicide PFC) has no stress or cortisol variable.
