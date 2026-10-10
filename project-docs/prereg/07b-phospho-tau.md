# Pre-registration 07b: stress-linked tau phosphosites in deposited mouse phospho tables

Version 1, 2026-10-09. Written before any data table named here was downloaded
or opened. Source brief: project-docs/briefs/07b-proteomics-pivot.md. Lessons
carried from F-07-1 (project-docs/FINDINGS.md): the positive control must match
the sample timing; a random-set test that treats features as independent is
anticonservative for co-regulated features and cannot be primary; the
statistics ship with unit tests on synthetic data.

## 1. Question and decision

Question: in mouse medial prefrontal cortex after chronic unpredictable mild
stress (CUMS), are the tau phosphosites that antibody studies reported as
stress-increased also higher in a deposited label-free phospho table?

Decision informed: whether the protein-level arm of project 07 continues on
deposited phospho tables (replication in PXD057176 and PXD050750), or moves to
raw-file reanalysis or new tissue (brief section 6). Change trigger: NOT
MEASURABLE moves the next step to brief section 6 routes 1 and 2; NULL or
SUGGESTIVE moves it to replication in a second deposited set before any claim.

Verifier the model did not see: the deposited tables themselves (opened only
after this file is committed and hashed), and the positive control site, which
the PXD024829 authors validated by western blot.

## 2. Tau site list, re-read from full text on 2026-10-09

Both papers were read as full text from their PMC article pages (HTML fetched
directly, then converted to text; no summarizing tool). Neither is open access
in Europe PMC, so the Europe PMC full-text XML was unavailable.

Sotiropoulos et al. 2011, J Neurosci, DOI 10.1523/JNEUROSCI.0730-11.2011,
https://pmc.ncbi.nlm.nih.gov/articles/PMC6633145/ (page SHA-256
1f28c4cf3525009b37c362e5b9fdfaac94c4c6a9b082e8fe75b439dfdea127e6).
- Animals: male Wistar rats, 14 months, subgroups n = 6 to 7, one month of
  chronic unpredictable stress.
- Western blot, hippocampus and PFC, normalized to total tau (Tau-5): stress
  increased pSer202 (CP-13), pThr231 (CP-9), pSer396/404 (PHF-1) and pSer409
  (PG5), "p <= 0.05 in all cases", both regions. Direction UP.
- Immunohistochemistry: CP-13 (pSer202) and 12E8 (pSer262/Ser356) staining shown
  for subiculum and PFC as confirmation. The Discussion names pThr231 and
  pSer262 as "upregulated by stress". The 12E8 result has no western blot and
  no site separation between Ser262 and Ser356.
- Glucocorticoid treatment of unstressed rats largely reproduced the stress
  effect.

Rissman et al. 2012, PNAS 109:6277, DOI 10.1073/pnas.1203140109,
https://pmc.ncbi.nlm.nih.gov/articles/PMC3341026/ (page SHA-256
a421acb3a756de63154ca2696220a6ab9a21cdbe1bb1814e015c33ea38db1f53).
- Animals: wild-type and CRFR-knockout mice; acute (one 30 min restraint) or
  repeated (14 daily) restraint; killed 20 min or 24 h after the last session.
- Western blot, hippocampus: AT8 (Ser202/Thr205) and PHF-1 (Ser396/404) rose
  after acute and repeated restraint; only the repeated-stress rise persisted at
  24 h. Direction UP.
- Isocortex and cerebellum from the same mice: "no significant change in tau-P
  at the PHF-1 or AT8 sites" (P > 0.05, ANOVA, Fig. S1). This is a prior reason
  to expect a weaker or absent effect in mouse cortex.
- PHF-1 immunohistochemistry (n = 4 or 5 per group): hilar and CA neurons;
  labeling weaker after repeated than after acute stress. Western blot n per
  group was not found in the text.

Correction to the brief: the brief listed S262 among the primary sites. S262
rests on immunohistochemistry only, with an epitope (12E8) that does not
separate S262 from S356. It moves to the secondary list.

Primary set T (western blot evidence, human 2N4R numbering): S202, T205, T231,
S396, S404, S409. Direction: UP in stress. Each antibody reads a joint epitope
(AT8 = S202+T205, PHF-1 = S396+S404); mass spectrometry reads single sites.
Secondary, descriptive only: S262, S356.

## 3. Numbering map (human 2N4R to mouse Mapt)

Sequences: UniProt P10636 (human tau, isoform P10636-8 = 2N4R, 441 aa) and
P10637 (mouse tau; canonical 733 aa; isoform P10637-2, 430 aa, is the mouse
2N4R form). Retrieved 2026-10-09 from rest.uniprot.org (stream query with
includeIsoform=true). File SHA-256 as fetched: P10636 isoforms
5dc981d2afdaad6b862d6b5c13d186ed94284999e52ba0cfb3e8964e1f2809f8, P10637
isoforms 23ad887891a597fe74692178273d38768a85f217a19d2103bc9a21e33384dd9d,
O88935 isoforms 242cd0fb4381af4dc098b2d670c32b826faef0e0b3cd24c9b24e89b24dd368cd.
The FASTA files are not kept in the repo (UniProt can revise them); the mapping
is re-derived by `src/phospho07b/seqmap.py` (global alignment, match +2,
mismatch -1, gap -3). Window = residues -7 to +7.

| Human 2N4R | Mouse P10637-2 (2N4R, 430 aa) | Mouse P10637 canonical (733 aa) | Mouse 15-mer window | Human window identical? |
|---|---|---|---|---|
| S202 | S191 | S494 | SGYSSPGSPGTPGSR | yes |
| T205 | T194 | T497 | SSPGSPGTPGSRSRT | yes |
| T231 | T220 | T523 | KKVAVVRTPPKSPSA | no (last residue S in human) |
| S262 | S251 | S554 | NVRSKIGSTENLKHQ | no (K to R at -4) |
| S356 | S345 | S648 | RVQSKIGSLDNITHV | yes |
| S396 | S385 | S688 | GAEIVYKSPVVSGDT | yes |
| S404 | S393 | S696 | PVVSGDTSPRHLSNV | yes |
| S409 | S398 | S701 | DTSPRHLSNVSSTGS | yes |

Mouse 2N4R is 11 residues shorter than human 2N4R before S202. Note: the
"Mapt T523" reported for PXD057176 (brief section 2) is mouse canonical T523,
which is human T231.

Matching rule in the tables: a table site counts as a target site when its
mouse 15-mer window (centre residue phosphorylated) equals the window above.
Protein numbering in the table is not trusted, because the search database
isoform is unknown. MaxQuant tables carry a 31-residue "Sequence window"; its
central 15 residues are compared. Peptide-level tables are matched by placing
the stripped peptide in the mouse sequence and reading the window at the
localized residue.

## 4. Datasets and contrasts

Positive control: PXD024829 (von Ziegler et al. 2022, Nat Commun, DOI
10.1038/s41467-022-29367-5, PMC8983670, CC BY; full text read 2026-10-09).
Contrast: dorsal hippocampus, mice killed directly after a 6 min swim ("0 min"
group) vs home-cage controls, Experiment 1. The paper reports 5 to 8 mice per
group, each mouse an independent sample. Site: Synapsin 1 pS553 (mouse O88935
numbering, S553 in all three isoforms; window ARPPASPSPQRQAGA). The paper
validated a roughly 3-fold rise of p-S553-SYN1 in dHC immediately after stress
by western blot (t(6) = 2.40, p = 0.037 one-tailed, N = 4 per group). Timing
matches: fast phosphorylation, tissue taken at the peak.

Primary: PXD016302 (Xiao et al. 2020, Front Cell Neurosci, DOI
10.3389/fncel.2020.00048, PMC7156020, CC BY). Contrast: mPFC control+saline (3)
vs CUMS+saline (3). The ketamine arm and NAc are not used. Tissue taken 1 h
after a saline injection in both arms. Replicate independence is UNVERIFIED:
the Methods say four mice per group, and the Results say "the brain tissues ...
in a group of four mice were then homogenized" and that fractions came from
"three biological replicates per group". The three replicates may be splits of
one pooled homogenate. Section 8 caps the call because of this.

Group labels come from the column names in the deposited table, checked against
the raw-file names in the ProteomeXchange record. If labels cannot be assigned
unambiguously, the dataset is UNINFORMATIVE.

## 5. Processing (fixed before opening)

1. MaxQuant `Phospho (STY)Sites.txt`: drop rows flagged Reverse or Potential
   contaminant; keep rows with Localization prob >= 0.75; per-sample values
   from the summed `Intensity <sample>` columns. Peptide-level tables:
   keep peptides with localization probability >= 0.75 where a column exists;
   a site value is the sum of intensities of all modified peptides whose
   localized sites include it.
2. Zero intensity is missing. Values are log2. No imputation. If the deposited
   table holds imputed values with no flag to separate them, they are used as
   deposited and logged as a deviation.
3. Per-sample median centering over sites quantified in every sample of the
   contrast.
4. A site enters the site-level analysis when it has at least 2 values in each
   group.
5. No protein-level normalization in the primary test. PXD016302 has no paired
   global proteome (its proteinGroups.txt comes from the enriched run), so Mapt
   abundance is reported as context only.

## 6. Statistics

Site level: moderated t (limma-style empirical Bayes: prior degrees of freedom
d0 and prior variance s0^2 fitted by the method of moments on log residual
variances across all sites, Smyth 2004), contrast stress minus control. Effect
sizes per site: log2 fold change (difference of group means) and Hedges g.

Coverage gate (step 0): count primary T sites that pass section 5 step 4 in
the PXD016302 contrast. Fewer than 3 of 6: the primary test is NOT MEASURABLE
and stops. Sites are not substituted after looking.

Primary test: set statistic S = mean moderated t over the covered T sites.
Reference distribution: exact sample-label permutation over all 20 distinct
3 vs 3 labelings; the moderated t (including the prior fit) is recomputed for
each labeling. One-sided p_UP = (number of labelings with S >= S_observed) / 20.
Honest limit: the smallest attainable one-sided p is 1/20 = 0.05 and the
smallest two-sided p is 2/20 = 0.10, so 3 vs 3 cannot reach p < 0.05. The
permutation result is read as a rank: does the observed labeling rank first
of 20?

Secondary test: rotation test (ROAST-style, Wu et al. 2010) for the same S,
9,999 random rotations of the residual space with the prior fixed from the
observed fit, one-sided p_UP = (b + 1) / (R + 1). It keeps inter-site
correlation but assumes normal errors and independent samples.

Set effect size: per-sample set score = mean over covered T sites of the
site-centred log2 value; difference of group means with Welch 95% interval;
mean log2 fold change over covered T sites; leave-one-site-out range of S.

Matched random site sets (rank criterion): 1,000 sets of k sites (k = number
of covered T sites), each drawn from one protein (not Mapt, not ribosomal)
with at least k eligible sites, so that the within-protein co-regulation of a
single-protein set is kept. A set is accepted when its mean log2 intensity is
within 0.5 SD (SD of site mean intensities) of the T-set mean. Random seed 7.
If fewer than 1,000 sets are accepted in 200,000 draws, the accepted sets are
used and the count is reported. Rank = percentile of S among the random-set S.

## 7. Controls

Positive control (pipeline): in PXD024829 dHC, Syn1 pS553 must show log2 fold
change > 0 and one-sided exact permutation p < 0.05 for its site-level
moderated t (all relabelings if their number is at most 5,000, else 5,000
random relabelings, seed 7). Descriptive: number of sites with BH q < 0.05.
If the site is absent or the criterion fails: STOP, report, do not interpret
PXD016302.

Reproduction check (PXD016302): the paper reports Rims1 phosphorylation
roughly halved by CUMS (Fig. 4B, text) and Map2 repressed. Criterion: at least
one quantified Rims1 site with log2 fold change <= -0.5. Map2 direction is
reported descriptively (the paper text does not name the Map2 site). If the
Rims1 criterion fails, PXD016302 results are labeled UNINTERPRETABLE.

Negative controls (PXD016302), both tests recorded on each:
- Ribosomal set: all covered sites on Rpl*, Rps*, Rplp* proteins except Rps6
  (an mTOR readout). Run the rotation test and the permutation test, and an
  intensity-matched random-site test that treats sites as independent (the
  F-07-1 style test), recording all three calls.
- Calibration panel: 200 single-protein site sets drawn as for the matched
  random sets (seed 7), each run through the rotation test (999 rotations).
  Required: the fraction with two-sided rotation p < 0.05 is at most 0.15
  (0.05 expected under the null; the margin allows true CUMS effects).
- Miscalibration rule: if the calibration panel fails, or the ribosomal set is
  called at two-sided p < 0.05 by the rotation test and also falls outside the
  2.5 to 97.5 percentile band of the independent random-site test, the
  rotation test is labeled miscalibrated and cannot carry a positive call.

## 8. Decision rule (PXD016302)

- STOP: positive control fails. Nothing below is interpreted.
- NOT MEASURABLE: coverage gate fails (fewer than 3 covered primary sites).
- UNINTERPRETABLE: reproduction check fails, or group labels are ambiguous.
- SUGGESTIVE: all of (a) mean log2 fold change over covered T sites > 0 and at
  least 3 covered T sites with log2 fold change > 0; (b) rotation p_UP < 0.05
  with the rotation test not miscalibrated; (c) matched random-set percentile
  >= 95; (d) observed labeling ranks first of 20 in the exact permutation.
  SUPPORT is not reachable in this run: replicate independence is unverified
  and the brief's support rule needs a same-sign result in PXD057176 or
  PXD050750, which this run does not test.
- NULL: gate passes, controls behave, SUGGESTIVE criteria not met. Sub-label:
  "NULL, excludes a 1.5-fold rise" if the upper bound of the set-score 95%
  interval is below log2(1.5) = 0.585; otherwise "NULL, weak (a 1.5-fold rise
  not excluded)".

## 9. Does not prove

- Antibody epitopes in rat (Sotiropoulos) and mouse hippocampus (Rissman) are
  not single-site MS measurements; a null in mouse mPFC does not contradict
  them. Rissman reported no isocortex change in mouse.
- A positive in a 3 vs 3 screen with possibly pooled replicates is a lead, not
  evidence of a stress effect on tau in animals.
- Phospho changes can reflect total tau changes; protein adjustment is not
  available here.
- Nothing here measures microtubule stability.
