# Pre-registration 07c: stress-linked tau phosphosites in deposited hippocampal phospho tables

Version 1, 2026-10-09. Written before any data table named here was downloaded
or opened. Parent: pre-registration 07b (project-docs/prereg/07b-phospho-tau.md,
SHA-256 d9b5ce94...a573fc) and finding F-07b-1 (weak null in mouse mPFC,
PXD016302, 3 vs 3; positive control passed). Motivation: Rissman et al. 2012
saw tau phosphorylation rise after restraint in mouse hippocampus and not in
isocortex, so a cortex null leaves the hippocampal question open.

## 1. Question and decision

Question: in rodent hippocampus after chronic stress, are the tau phosphosites
that antibody studies reported as stress-increased higher in a deposited
phospho table?

Decision informed: whether the stress-to-tau step of project 07 has any support
in open rodent phosphoproteomes (continue toward raw-file reanalysis or new
tissue), or whether two independent deposited sets in two regions both fail to
show it (the deposited-table arm closes for tau; brief 07b section 6 routes
become the only way forward).

Verifier the model did not see: the deposited table (opened only after this
file is committed and hashed) and the paper's own reported phosphosite
(Stmn1 S38), used as a reproduction check.

## 2. Metadata decoding (no data table opened)

Sources read on 2026-10-09: ProteomeXchange records
(https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD057176&outputMode=json
and the same for PXD050750), the iProX PROXI records
(https://www.iprox.cn/proxi/datasets/PXD057176, .../PXD050750), Europe PMC and
PubMed records for PMID 42322444 and 38852542, and the Springer article page
for DOI 10.1007/s11064-026-04819-2 (abstract plus the supplementary-file
captions; the body text is paywalled and was not read).

### PXD057176: decoded, kept

Paper: "Sex-Specific Hippocampal Phosphoproteomic Features Associated with
Stress-Induced Phenotypes in Mice Exposed to Chronic Restraint Stress",
Neurochem Res 51(4), 2026, DOI 10.1007/s11064-026-04819-2, PMID 42322444. Not
open access. Instrument timsTOF Pro, 4D label-free DIA phospho. Processed file:
Phospho_Report.zip, 65,595,386 bytes (HTTP HEAD, 2026-10-09).

Raw files (18): `Phos_DIA_20230422_<S>_<G><r>_...d.zip` with S in {C, X},
G in {C, D, I}, r in {1, 2, 3}.

Supplementary captions on the Springer page (read 2026-10-09) state:
- Groups: anxiodepression-susceptible (AD-Sus), insusceptible (Insus), and
  "Ctrl, non-stressed control"; both sexes.
- Table S2 sample names: Female-AD-1..3, Male-AD-1..3, Female-I-1..3,
  Male-I-1..3, Female-C-1..3, Male-C-1..3. So 3 phospho samples per group per
  sex, 18 samples.
- Table S1: behavioural data of the CRS-exposed and non-stressed mice
  "ultimately selected for phosphoproteomic analysis (n = 6 per group per
  sex)". Six mice per group per sex feed three samples, so each sample may be
  a pool of two mice. Pooling is UNVERIFIED; the body text was not read.

Decoding:
- G: C = Ctrl (non-stressed), D = AD-Sus, I = Insus. Matches the paper's
  sample nomenclature (C, AD, I) and the 3 x 2 x 3 layout. Confidence: high.
- S: C = female, X = male. Inferred from pinyin initials (ci = female, xiong =
  male); no record states it. Confidence: moderate. Section 7 adds a data
  check (Y-linked phosphosites) that confirms or swaps this before any
  per-sex result is read. The primary test does not depend on which prefix is
  which sex.

Contrasts. Primary: chronic restraint stress (AD-Sus plus Insus, 12 samples)
vs Ctrl (6 samples), both sexes pooled, sex as a blocking factor. Secondary:
the same contrast within each sex (6 vs 3). Descriptive: AD-Sus vs Ctrl and
Insus vs Ctrl, each with sex as a block.

Sample columns in the report are assigned by matching the raw-file names
above. If the report's run names cannot be matched to these 18 names one to
one, the dataset is UNINTERPRETABLE.

### PXD050750: not decodable, dropped

Rat hippocampus, CUMS, Sun et al. 2024, J Psychiatr Res 176:119, DOI
10.1016/j.jpsychires.2024.06.004, PMID 38852542. Raw files are named
A1..A9 and 1..6 (15 files) and carry no group label. Two processed archives
(txt.rar, txt8064TQ.rar) are unlabeled. The ProteomeXchange record says "No
PTMs are included in the dataset" although the paper reports phosphoproteomics.
The paper is not open access (Europe PMC and Semantic Scholar: closed); the
publisher page returned a bot challenge, which was not bypassed. The abstract
gives no group sizes. Which files are phospho-enriched, which are proteome,
and which group each file belongs to cannot be decoded from metadata. Per the
run instruction, PXD050750 is dropped. Not analysed; not downloaded.

## 3. Tau site list and numbering

Same verified list as 07b (re-read from full text, 07b section 2). Primary set
T (human 2N4R numbering): S202, T205, T231, S396, S404, S409. Direction UP in
stress. Secondary, descriptive only: S262, S356.

Matching is by 15-mer sequence window, as in 07b; protein numbering in the
table is not trusted. Mouse windows (P10637-2 / P10637 canonical) are those of
07b section 3.

Rat mapping (recorded for completeness; PXD050750 is dropped, so it is not
applied). Rat tau UniProt P19332 isoforms fetched 2026-10-09 from
https://rest.uniprot.org/uniprotkb/stream?query=accession:P19332&includeIsoform=true&format=fasta
(SHA-256 848ac92edc68806524881e07ba25bc223af0dff81a6693a7cc473af8edbc2887;
human P10636 isoform file re-fetched with the same SHA-256 as 07b). Global
alignment of P10636-8 against P19332 canonical (752 aa) and P19332-5 (432 aa)
with `src/phospho07b/seqmap.py`:

| Human 2N4R | Rat P19332 canonical | Rat P19332-5 | Rat 15-mer window | Equals mouse window? |
|---|---|---|---|---|
| S202 | S513 | S193 | SGYSSPGSPGTPGSR | yes |
| T205 | T516 | T196 | SSPGSPGTPGSRSRT | yes |
| T231 | T542 | T222 | KKVAVVRTPPKSPSA | yes |
| S262 | S573 | S253 | NVRSKIGSTENLKHQ | yes |
| S356 | S667 | S347 | RVQSKIGSLDNITHV | yes |
| S396 | S707 | S387 | GAEIVYKSPVVSGDT | yes |
| S404 | S715 | S395 | PVVSGDTSPRHLSNV | yes |
| S409 | S720 | S400 | DTSPRHLSNVSSTGS | yes |

The PXD057176 abstract's "Mapt (T523)" is mouse canonical T523 = human T231,
a primary site. Its direction is not stated in any record read.

## 4. Processing (fixed before opening)

1. Report format. The archive's format is unknown. Rules by format:
   (a) Spectronaut PTM site report (one row per site or site multiplicity,
   with a site probability and a flanking window): keep rows with site
   localization probability >= 0.75; a site's value per run is the sum over
   its multiplicity rows; the window is the centre 15 residues of the
   flanking sequence.
   (b) Spectronaut precursor or peptide long report: the 07b rules and
   `load_spectronaut` (sum over precursors, localization >= 0.75, peptides
   placed on the mouse Swiss-Prot isoform FASTA used in 07b, SHA-256
   94b4f1e5...1671).
   (c) Any other layout: map onto the nearest of (a) or (b) and log the
   mapping as a deviation.
2. Zero or empty quantity is missing. log2. No imputation. Values imputed by
   the search software with no flag are used as deposited and logged as a
   deviation.
3. Per-sample median centring over sites quantified in all 18 samples.
4. Eligibility for the primary (blocked) analysis: at least 2 values in each
   of the four sex x stress cells. Per-sex analysis: at least 2 values in each
   group of that sex. Descriptive phenotype contrasts: at least 2 values in
   each sex x group cell used.
5. A tau target with several table rows (isoform or multiplicity duplicates)
   is the sum of linear intensities of those rows, as in 07b.
6. No total-tau adjustment: the deposit has no paired global proteome.

## 5. Statistics

Site level, primary: per-site linear model log2 value ~ sex + stress (stress =
1 for AD-Sus and Insus), fitted by least squares on the available samples.
Moderated t for the stress coefficient (limma-style empirical Bayes; prior d0,
s0^2 fitted by the method of moments on residual variances of eligible sites,
as in 07b). Effect size: the stress coefficient (log2 fold change adjusted for
sex) and Hedges g from the pooled two-group comparison.

Per-sex secondary: the 07b two-group moderated t (6 vs 3).

Coverage gate (step 0): primary T sites that pass section 4 step 4 for the
primary contrast. Fewer than 3 of 6: NOT MEASURABLE, stop. Sites are not
substituted after looking.

Primary test: S = mean moderated t of the stress coefficient over covered T
sites. Reference distribution: stress labels permuted within sex (stratified),
2,000 random relabelings (seed 7) with the observed labeling added once; prior
refitted for each relabeling. p_UP = share of relabelings with S >= observed.
With 12 vs 6 and strata of 9, the smallest attainable p is 1/2001.

Rotation test (ROAST-style, Wu et al. 2010) for the same S with the design
[1, sex, stress], rotating the stress effect and the residual space (n - 3 =
15 dimensions for complete sites), 9,999 rotations, prior fixed from the
observed fit, complete-case set rows. p_UP = (b + 1) / (R + 1).

Set effect size: per-sample set score = mean over covered T sites of the
site-centred log2 value; stress coefficient from score ~ sex + stress with a
t-based 95% interval (df = n - 3). Also the mean of site log2 fold changes and
the leave-one-site-out range of S.

Matched random single-protein site sets: as 07b (1,000 sets, one protein
each, mean intensity within 0.5 SD, seed 7, Mapt and ribosomal proteins
excluded), with S recomputed from the blocked moderated t. Rank = percentile
of the observed S.

Per-sex secondary: within each sex, 07b statistics on 6 vs 3: exact
permutation over all 84 labelings (smallest one-sided p 1/84), rotation test,
Welch 95% interval of the set score difference.

## 6. Controls and gate

Positive control, pipeline (as 07b): re-run the 07b positive control
(PXD024829, dHC, Syn1 pS553, swim 0 min vs home cage) with the code as it
stands after the 07c changes. Required: PASS under the 07b criterion. If it
fails, STOP.

In-dataset positive control: none is available from metadata. No site with a
known, independently validated chronic-restraint change in mouse hippocampus
was found in the records read. The gate for PXD057176 is therefore weaker
than 07b's: it rests on the label check, the reproduction check, the
calibration panel and the negative control below. This is stated in the
finding.

Label check (sex): Y-linked phosphosites are those whose 15-mer window occurs
in Ddx3y (Q62095), Eif2s3y (Q9Z0N2), Kdm5d (Q62240 isoforms) or Uty (P79457)
and in no other mouse Swiss-Prot sequence. Criterion: Y-linked sites are
quantified in at least 7 of 9 samples of one prefix and in at most 2 of 9 of
the other, for a majority of the Y-linked sites found. The prefix with values
is male. If this agrees with section 2, labels stand; if reversed, the per-sex
labels are swapped and logged; if no Y-linked site is found or the pattern is
mixed, per-sex results are reported as "prefix C" and "prefix X" with sex
unconfirmed. The primary test is unaffected in all three cases.

Reproduction check: the paper names Stmn1 S38 as a key phosphorylation target
in female AD-Sus and female Insus (direction not stated in any record read).
Mouse Stmn1 P54227 S38 window SVPDFPLSPPKKKDL. Criterion: the site is
quantified and |log2 fold change| >= log2(1.2) = 0.263 in at least one of
female AD-Sus vs female Ctrl or female Insus vs female Ctrl (two-group,
descriptive fold change). The 1.2-fold threshold is assumed (a common cut-off;
the paper's threshold was not read). If the female prefix is unconfirmed, the
criterion is met by either prefix. Failure: PXD057176 results are
UNINTERPRETABLE. Mapt T523 is not used for reproduction because it is a test
site. Pdha1 S232 (window NRYGMGTSVERAAAS) is reported descriptively.

Negative controls (PXD057176), as 07b:
- Ribosomal site set (Rpl*, Rps*, Rplp*, Rpsa; Rps6 excluded): permutation,
  rotation, and independent random-site test, all three calls recorded.
- Calibration panel: 200 single-protein k-site sets (seed 7), rotation test
  with the blocked design (999 rotations). Required: share with two-sided
  p < 0.05 at most 0.15.
- Miscalibration rule: calibration panel fails, or the ribosomal set is called
  at two-sided rotation p < 0.05 and lies outside the 2.5 to 97.5 percentile
  band of the independent random-site test: the rotation test is labeled
  miscalibrated and cannot carry a positive call.

## 7. Decision rule

PXD057176, primary (pooled, sex-blocked):
- STOP: pipeline positive control fails.
- UNINTERPRETABLE: run names cannot be matched to the 18 decoded samples, or
  the reproduction check fails.
- NOT MEASURABLE: coverage gate fails.
- SUGGESTIVE: all of (a) mean log2 fold change over covered T sites > 0 and at
  least 3 covered T sites with log2 fold change > 0; (b) rotation p_UP < 0.05,
  rotation test not miscalibrated; (c) matched single-protein percentile
  >= 95; (d) stratified permutation p_UP < 0.05.
- OPPOSITE: the mirror of (a) to (d) for DOWN (mean log2 fold change < 0 with
  at least 3 sites < 0, rotation p_DOWN < 0.05, percentile <= 5, permutation
  p_DOWN < 0.05). Reported as a null for the UP hypothesis with a signal in
  the other direction.
- NULL otherwise. Sub-label "excludes a 1.5-fold rise" if the upper bound of
  the set-score 95% interval is below log2(1.5) = 0.585, else "weak (a
  1.5-fold rise not excluded)".

Per-sex secondary results are descriptive. They cannot turn a primary NULL
into SUGGESTIVE.

Hippocampal SUPPORT for the 07 hypothesis requires: PXD057176 SUGGESTIVE, and
the per-sex set-score difference > 0 in both sexes. SUGGESTIVE without both
sexes positive is reported as "SUGGESTIVE, sex-dependent".

Combining 07b and 07c (fixed now, with 07b known and 07c unknown):
- 07c SUPPORT, 07b NULL: hippocampus-specific signal, consistent with Rissman
  2012 (hippocampus yes, isocortex no). Not a replication: different region,
  model (CRS vs CUMS), lab and platform. Next step: a second hippocampal
  dataset or raw-file reanalysis before any claim.
- 07c NULL, 07b NULL: null in two regions, two labs, two stress models. The
  deposited-table arm for tau closes; brief 07b section 6 routes 2 to 4 are
  what remains. Sub-labels from each dataset carried.
- 07c OPPOSITE: no support; reported as a discordant signal.
- 07c NOT MEASURABLE or UNINTERPRETABLE: UNINFORMATIVE for hippocampus; the
  combined state is F-07b-1 alone.
- Descriptive only: inverse-variance fixed-effect combination of the 07b
  set-score difference (-0.06, 95% CI -0.72 to +0.60) and the 07c primary
  stress coefficient, with its 95% interval. Different regions and models;
  not a decision input.

## 8. Does not prove

- MS single sites are not the antibody joint epitopes (AT8, PHF-1).
- Samples may be pools of two mice (Table S1 n = 6 per group per sex, 3
  samples); effective n may be lower than it looks, and pool membership is
  unknown.
- The CRS mice were split by behaviour into AD-Sus and Insus; pooling them
  estimates a stress effect averaged over phenotypes that the authors chose
  by selection ("ultimately selected"), not a random sample of stressed mice.
- No total-tau adjustment; no paired global proteome.
- The in-dataset gate is weaker than 07b's: no validated chronic-stress site
  exists in this deposit to show the table can detect a true chronic effect.
- Nothing here measures microtubule stability.
