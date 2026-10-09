# Brief 07: Neuronal microtubules, stress, activity and dendritic remodeling

Date: 2026-10-09. Register: research brief, internal. Verification key: [A] = DOI record and abstract opened and read (PubMed or Crossref); [M] = DOI record opened (Crossref metadata) but abstract not read, so content claims rest on title and prior knowledge; UNVERIFIED = could not open. Confidence labels: high / moderate / low / unknown.

## Result first

1. The best-supported chain is: chronic stress or glucocorticoids raise tau phosphorylation in rat and mouse hippocampus and prefrontal cortex (replicated in at least two independent labs), and tau deletion blocks stress-induced apical dendrite atrophy and spine loss in mouse PFC (one lab, one study). Confidence: moderate.
2. No source I opened shows that stress changes microtubule dynamics or stability directly in dendrites in vivo. The microtubule step in the chain is inferred from tau's known role, not measured. Confidence: moderate that this gap exists in what I found; I did not run an exhaustive search.
3. Microtubule-stabilizing drugs rescued tau-transgenic mice (epothilone D, BMS-241027) but the one large trial of a microtubule-targeting peptide in a tauopathy (davunetide, PSP, n=313) was null. A Phase 1 epothilone-class trial in mild AD (n=40) finished with no posted results. Confidence: high on the trial facts.
4. A mRNA-level test of a stress-microtubule link is possible on open rodent data (GSE109315 plus held-out GSE127812) but is underpowered and misses the post-translational mechanism. Treat it as a cheap first screen, not a test of the tau mechanism.
5. Orch-OR is not part of mainstream microtubule biology and is kept out of the analysis (section 5).

## 1. Question and the decision it informs

Question: does chronic stress or glucocorticoid exposure change neuronal microtubule stability, through tau and other MAPs, and does that explain dendritic retraction, spine loss and (by extension) regional grey matter reduction? Where does activity act on the same machinery?

Decision informed: whether to spend analysis effort on a microtubule-centered mechanism hypothesis in the Sapolsky frame (glucocorticoid cascade to structural loss), and which open dataset gives the cheapest first falsifiable check. Baseline: the prior working assumption is that dendritic remodeling is actin- and synapse-driven. Change trigger: if the pre-registered microtubule gene set (section 7) shows no consistent shift in independent stress datasets, deprioritize transcript-level work and move to protein or phospho-proteomic data.

## 2. Established biology

Dynamic instability. Microtubules switch stochastically between growth and shrinkage (catastrophe and rescue), driven by GTP-tubulin cap hydrolysis. Original description: Mitchison and Kirschner 1984 [M]; review: Desai and Mitchison 1997 [M]. Confidence: high.

Polarity. Axonal microtubules are uniformly plus-end-out; mammalian dendrites have mixed polarity in proximal regions (Baas et al. 1988, hippocampal neurons) [M]. Overview of neuronal microtubule organization: Kapitein and Hoogenraad 2015 [M]. Confidence: high. Dendritic orientation is often described as mixed in mammals, with a minus-end-out majority in some dendrites; details vary by neuron type (from memory, low confidence).

Tubulin code. Post-translational modifications tune microtubule properties and motor binding (Janke and Magiera 2020 [M]).
- Acetylation (alpha-tubulin K40) marks long-lived microtubules and promotes kinesin-1 binding and transport (Reed et al. 2006 [M]). HDAC6 inhibition raised acetylation and rescued transport in a Huntington model (Dompierre et al. 2007 [M]). Confidence: high on the cited findings.
- Detyrosination marks stable microtubules and affects motor and depolymerase engagement. Covered in Janke and Magiera 2020 [M]; I did not open a primary paper on neurons, so details are from the review title only.
- Polyglutamylation: excess causes neurodegeneration and disrupts transport in mice (Magiera et al. 2018 [M]); reviewed in Bodakuntla et al. 2021 [M]. Confidence: moderate.

MAPs. Tau is enriched in axons and also has a dendritic role in postsynaptic Fyn targeting (Ittner et al. 2010 [A]). Tau mislocalizes to spines in disease models and impairs synaptic function independent of neuron death (Hoover et al. 2010 [M]). MAP2 is required for dendrite elongation (Harada et al. 2002 [M]). MAP1B is a major developmental MAP; no primary source opened, so treat any specific MAP1B claim as unsupported here. General review: Bodakuntla et al. 2019 [M]. Tau physiology and pathology: Wang and Mandelkow 2016 [M]. Tau knockout mice are viable with mild phenotypes, attributed to MAP redundancy (from memory, low confidence); tau loss can cause iron-related parkinsonism with age (Lei et al. 2012 [M]).

Severing enzymes. Spastin and katanin sever microtubules and shape neuronal branching (Yu et al. 2008 [M]). Spastin structure: Roll-Mecak and Vale 2008 [M]. Tau protects axonal microtubules from katanin severing (Qiang et al. 2006 [M]); in vitro, tau forms distinct phases on the lattice that regulate severing enzymes and kinesin (Siahaan et al. 2019, preprint DOI [M]). Confidence: moderate-high.

Microtubule entry into spines. Dynamic microtubules transiently invade spines of mature neurons, more often and for longer with higher activity (Hu et al. 2008 [A]). Growing plus ends (EB3) enter spines and modulate spine shape through p140Cap and cortactin (Jaworski et al. 2009 [A]). NMDA receptor activation suppresses microtubule growth and spine entry (Kapitein et al. 2011 [M]); synaptic calcium, F-actin and drebrin regulate entry (Merriam et al. 2013 [M]). BDNF-induced PSD-95 increase in spines requires invasions (Hu et al. 2011 [M]). Models: cultured rodent neurons. In vivo evidence: none opened. Confidence: high in culture, unknown in vivo.

Axonal transport. Motor-driven transport depends on microtubule tracks and their modifications (Hirokawa et al. 2010 [M]); links to AD in Stokin and Goldstein 2006 [M]. Confidence: high.

## 3. Stress and activity links

Dendritic remodeling (the structural anchor, McEwen and Sapolsky lines):
- Chronic restraint stress shrinks CA3 apical dendrites (Watanabe et al. 1992 [M]; Magarinos et al. 1995, two papers: comparison of stress paradigms [M], involvement of glucocorticoids and excitatory amino acids [M]). The 1995 pair implicates adrenal steroids and excitatory amino acids. Mossy fiber terminal ultrastructure changes after 21 d of restraint, not after a single session (Magarinos et al. 1997 [A]).
- Hippocampus and amygdala diverge: CA3 retracts while basolateral amygdala neurons grow (Vyas et al. 2002 [M]).
- mPFC: apical dendritic reorganization (Radley et al. 2004 [M]); 21 d restraint reduced apical spine density by 16% and apical dendritic length by 20%, with an estimated third of axospinous synapses on apical dendrites lost (Radley et al. 2005 [A]); partial reversibility after recovery (Radley et al. 2005b [M]); corticosteroids alter PFC dendrites and PFC-dependent behavior (Cerqueira et al. 2005 [M]); dendritic changes predict attentional set-shifting deficits (Liston et al. 2006 [M]).
- Reviews: McEwen et al. 2015 [M]; Sapolsky 2000 on hippocampal atrophy in neuropsychiatric disorders [M]; the glucocorticoid cascade hypothesis (Sapolsky et al. 1986 [M]).
- Models: rat and mouse, histology (Golgi or intracellular fills), typically n of 5 to 10 animals per group (from memory, low confidence). Replication: the CA3 and mPFC findings have been reproduced across many groups (moderate confidence; I did not systematically audit failures).

Stress and tau (the microtubule-associated step):
- Glucocorticoids induce AD-like tau changes in rat neuronal cells expressing human tau (Sotiropoulos et al. 2008 [M]).
- In middle-aged wild-type rats, chronic stress and glucocorticoid induced abnormal tau hyperphosphorylation in hippocampus and PFC with impairments of hippocampus- and PFC-dependent behavior; prior stress aggravated glucocorticoid and Abeta effects (Sotiropoulos et al. 2011 [A]). Effect sizes were not extracted here: unknown.
- Repeated stress raised hippocampal tau phosphorylation in mice, sustained 24 h after the last stress, with a fraction shifted to detergent-soluble fractions and globular aggregates; the response depended on CRFR1, not CRFR2 (Rissman et al. 2012 [A]). Independent lab (UCSD/Salk) from Sotiropoulos (Minho/Munich), which is the main replication signal for the stress to tau-P step. Confidence: moderate-high.
- Causality test: stress produced apical dendrite atrophy, spine loss and working-memory deficits in wild-type mouse PFC, absent in Tau-KO; proteomics of PFC synaptosomes pointed to mitochondria (Lopes et al. 2017 [A]). One study, one lab, knockout (lifelong compensation possible). Confidence: moderate.
- Conference abstracts from the same group report HDAC6-dependent changes after stress (Sotiropoulos 2016 [M], abstract only); not evidence on its own.
- Human tissue: I found no opened paper showing stress- or cortisol-linked tau change in human brain. Unknown.

Activity: activity increases the number and duration of spine invasions in culture (Hu 2008 [A]); NMDAR activation suppresses microtubule growth and spine entry (Kapitein 2011 [M]). These two point in different directions on net effect of activity, depending on stimulus; the difference is not resolved here (moderate confidence that the literature is mixed).

Inference (labeled): glucocorticoid and CRF signaling raise tau phosphorylation (kinase effects), reducing tau binding to the lattice, shifting microtubule stability and dendritic transport, which with excitatory drive could favor retraction. Each link has support; the end-to-end microtubule stability measurement in stressed dendrites is missing. Confidence: low as a whole.

## 4. Disease links in proportion

- Tauopathies: tau hyperphosphorylation and loss of microtubule-stabilizing function are the rationale for stabilizers (Brunden et al. 2010 [A]).
- Epothilone D in PS19 mice, once weekly for 3 months at low dose, improved microtubule density, axonal integrity and cognition (Brunden 2010 [A]). BMS-241027 (an epothilone) restored in vivo microtubule dynamics in rTg4510 mice and improved water-maze deficits, tau pathology and neurodegeneration, at doses that only partly normalized dynamics (Barten et al. 2012 [A]). Mouse only.
- Human: NCT01492374, BMS-241027 in mild AD, Phase 1, n=40 actual, completed Oct 2013, no results posted on ClinicalTrials.gov (API checked today; hasResults false) [A]. Reason for halting development not found; Alzforum lists it as discontinued (search snippet only, UNVERIFIED page content).
- Davunetide in PSP: Phase 2/3, 313 randomized, 52 weeks, no difference in PSPRS (median 11.8 vs 11.8, p=0.41) or SEADL (p=0.92); conclusion "not an effective treatment" (Boxer et al. 2014 [A]). Confidence: high. Note the preclinical rationale that davunetide stabilizes microtubules was not confirmed as a target-engagement result in that trial (abstract does not report a microtubule biomarker).
- Take: stabilizers work in tau-transgenic mice and not (yet) in people. This weakens a strong "stabilize microtubules to protect from stress" translation. It does not test stress-induced dendritic loss, which differs in cause.

## 5. Side note: Orch-OR (separate from mainstream microtubule biology)

Claimed: Penrose and Hameroff propose that consciousness arises from orchestrated objective reduction, a gravity-related quantum collapse, in coherent states of neuronal microtubules (Hameroff and Penrose 2014 [M]).

Tests and critiques:
- Decoherence: Tegmark 2000 calculated decoherence times of about 1e-13 to 1e-20 s, far shorter than neural dynamics of 1e-3 to 1e-1 s, concluding brain cognition is classical [A].
- Thermal and coherence critiques of the Frohlich-condensation basis: Reimers et al. 2009 [M] and McKemmish et al. 2009 [M] (title: the proposal "is not biologically feasible").
- Supportive reports: UV superradiance in tryptophan networks in microtubule-like architectures (Babcock et al. 2024 [M]); energy migration in microtubules (Kalra et al. 2023, ACS Cent Sci, DOI 10.1021/acscentsci.2c01114 [M]); anesthetic effects on tubulin terahertz oscillations (Craddock et al. 2017 [M]); the epothilone B result below; and a MRI claim of non-classical brain function (Kerskens and Perez 2022 [M]). These show photophysics in vitro or indirect correlations, not quantum coherence driving cognition.
- Wiest group: epothilone B delayed loss of righting reflex under isoflurane by 69 s (Cohen's d 1.9) in male rats; authors say this fits Orch-OR (Khan et al. 2024 [A]). Alternative: taxane effects on neuronal transport or excitability would also shift anesthetic latency, so it does not discriminate Orch-OR. Confidence: high on that logic. Single-lab, small design.

Standing: not accepted by neuroscience or physics consensus; no experiment has shown functionally relevant quantum coherence in microtubules at body temperature (moderate confidence; based on the sources above plus general knowledge, no systematic survey). Nothing in sections 2 to 4 depends on Orch-OR.

## 6. Open data

Reachability was checked on 2026-10-09 with an HTTP request (200 = server responded; a 200 does not prove the data files are downloadable). Nothing downloaded.

| Resource | URL | Access terms | Reachable today |
|---|---|---|---|
| NCBI GEO (rodent stress sets) | https://www.ncbi.nlm.nih.gov/geo/ | Open, no account for download | Yes (200) |
| GSE109315, chronic social defeat, mPFC, vHPC, BNST, C57BL/6Crl and DBA/2Crl, ribo-depleted RNA-seq, 88 sample IDs, PMIDs 30073192, 31857655 | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE109315 | Open | Record read via GEO text API: yes |
| GSE127812, repeated social defeat, PFC, 6 samples, PMID 31032362 | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE127812 | Open | Record read: yes |
| GSE81587, CUMS, mPFC, n=2 vs 2, PMID 27427907 | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE81587 | Open | Record read: yes |
| GSE138670, chronic stress, sorted Sst and PV interneurons in mPFC, 30 samples, PMIDs 31712551, 31743111 | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE138670 | Open | Record read: yes |
| Allen Brain Map (human MTG, M1, ACC, V1, SEA-AD MTG; mouse cortex and hippocampus) | https://brain-map.org/atlases-and-data/rnaseq | Described as an Open Science resource; license text not read (Terms of Use page not opened): unknown | Yes (301 to brain-map.org, page read) |
| Allen Human Brain Atlas | https://human.brain-map.org/ | As above | Yes (200) |
| GTEx portal | https://gtexportal.org/home/downloads/adult-gtex/overview | Summary and expression files open; individual genotypes controlled via dbGaP; a data use agreement may apply to downloads (third-party report, UNVERIFIED) | Yes (200); page body is script-rendered, content not readable by my fetcher |
| PsychENCODE | https://psychencode.synapse.org/ (redirects to Synapse) | Registered Synapse account plus access request; search results say primary home moved to NIMH Data Archive (UNVERIFIED) | Redirect works (307). adult.psychencode.org did not respond (000) |
| CZ CELLxGENE Discover | https://cellxgene.cziscience.com/ | License per dataset; terms page not read: unknown | Yes (200); page reports 33M+ cells |
| Synapse (AD Knowledge Portal, SEA-AD, ROSMAP) | https://adknowledgeportal.synapse.org/ | Account and data use terms for some sets: unknown | Yes (200) |
| ProteomeXchange (proteomics) | https://www.proteomexchange.org/ | Open | Yes (200) |
| ENIGMA (grey matter meta-analysis) | https://enigma.ini.usc.edu/ | Summary statistics availability: unknown | Yes (200) |
| UK Biobank | https://www.ukbiobank.ac.uk/ | Application required | 403 to my request (bot block likely) |
| Human Proteome Map, PGC | humanproteomemap.org, pgc.unc.edu | n/a | No response (000) |

Notes: GTEx and Allen hold no stress exposure variable, so they are for expression context (which cell types express which MAP, tubulin isoform and modifying-enzyme genes), not for testing stress effects. I did not find a chronic-stress proteomic or phospho-tau dataset on open repositories; unknown, search not exhaustive. No human stress-cohort expression dataset was verified; do not assume one.

## 7. Verifier design

Hypothesis (pre-registered before looking): in rodent mPFC, chronic social stress shifts expression of a fixed microtubule-regulator gene set in a consistent direction relative to size-matched random gene sets; direction predicted DOWN (inferred from loss of dendritic arbor; confidence low).

Fixed gene set M (freeze and hash the list before any expression is opened; about 30 genes): Mapt, Map2, Map1a, Map1b, Map6, Mapre1, Mapre3, Stmn1-4, Dcx, Spast, Katna1, Katnb1, Kif5a-c, Hdac6, Atat1, Sirt2, Ttll1/6/7, Ccp1/5, Vash1/2, Tubb3, Tuba1a, Tubb2a. Use mouse symbols.

Design:
- Discovery: GSE109315, C57BL/6Crl mPFC, control (n=6) vs susceptible (n=6) vs resilient (n=6). Also vHPC as a second region (not tested for replication).
- Internal held-out: DBA/2Crl mPFC from the same series (different strain, n=6 control vs 8 susceptible).
- External held-out: GSE127812 (different lab and protocol, small n) and GSE138670 interneurons for direction only.
- Test: competitive gene-set test (limma camera or fgsea) of M against 10,000 random size-matched sets matched on mean expression.
- Controls: positive control Fkbp5 and Sgk1 up in stressed groups (expected from glucocorticoid biology, moderate confidence); negative control ribosomal gene set (no shift expected).

Support: discovery competitive p < 0.05 in the predicted direction, same sign in the DBA/2Crl held-out at p < 0.05 one-sided and same sign in GSE127812 (direction only, since n is small), and positive control passes.
Null: discovery p >= 0.05, or sign flips in held-out sets. Report as null for transcript-level screening; this does not rule out post-translational changes.
Ambiguous: discovery significant but one held-out set discordant; report as unreplicated.
False-success check: the gene set test must beat random sets matched on expression; confirm results are not driven by one gene (leave-one-out) or by batch/sequencer (GSE109315 used two platforms, GPL13112 and GPL19057; model platform as covariate).

## 8. First analysis plan (one workstation, 24 cores, WSL Ubuntu, R)

1. Freeze gene list M as a text file; record SHA-256 in the analysis log. Pre-state direction and thresholds from section 7.
2. In WSL, create an R environment (Bioconductor: GEOquery, limma, edgeR, fgsea, tximport) and a Python helper for plots.
3. Read each series record with GEOquery; inspect supplementary files. If processed count tables exist, use them. If only SRA runs exist, fetch FASTQ (fasterq-dump) and quantify with salmon against GRCm39 (24 threads, a few hours at this size); do this only after the dataset use is approved. Do not download until then.
4. QC: sample-level PCA by strain, region, platform, condition; remove nothing without a written reason.
5. Differential expression in limma-voom: model ~ platform + condition per region and strain.
6. Competitive gene-set test for M versus 10,000 random matched sets; record p, direction, and leave-one-gene-out range.
7. Positive and negative control sets; stop and debug if the positive control fails.
8. Repeat on DBA/2Crl, then GSE127812 (counts, direction only), then GSE138670 per cell type and sex.
9. Write a one-page result: support, null or ambiguous per section 7, with n, intervals and the does-not-prove line.
10. If null or ambiguous, next target is a protein-level source (phospho-proteomics from ProteomeXchange for stress models) rather than more mRNA sets.

## 9. Does not prove, and risks

- Transcript level is not tau phosphorylation or microtubule stability; a null here leaves the tau mechanism untouched, and a positive here does not show causation.
- Tau-KO rescue (Lopes 2017) shows tau is needed, not that microtubule destabilization is the mediator; tau also acts at synapses (Fyn, mitochondria transport).
- Rodent restraint and social defeat do not equal human trauma; grey matter change in humans (MRI) has no verified link to these microtubule steps in this brief.
- Small n (6 per group; 2 per group in GSE81587), single-lab model studies, and unmeasured sex effects (GSE138670 only has sex structure) limit inference. Forking-path risk is real; pre-registration in section 7 is the control.
- Effect sizes for most stress/tau and dendrite studies were not extracted. A DOI record opened is not the same as the full text read; [M] items may be mischaracterized beyond their title.
- Search coverage: Crossref and PubMed lookups, not a systematic review. The replication record is assessed by what I opened, not by an audit.
- Davunetide and epothilone D results do not show that microtubule stabilization fails to protect against stress; they were tested in tauopathy.
- Orch-OR must not be used to motivate hypotheses here.

## 10. References

DOIs resolve via https://doi.org/ (record opened through Crossref or PubMed on 2026-10-09 unless marked).

- Mitchison T, Kirschner M 1984. Nature. 10.1038/312237a0 [M]
- Desai A, Mitchison TJ 1997. Annu Rev Cell Dev Biol. 10.1146/annurev.cellbio.13.1.83 [M]
- Baas PW et al. 1988. PNAS. 10.1073/pnas.85.21.8335 [M]
- Janke C, Magiera MM 2020. Nat Rev Mol Cell Biol. 10.1038/s41580-020-0214-3 [M]
- Kapitein LC, Hoogenraad CC 2015. Neuron. 10.1016/j.neuron.2015.05.046 [M]
- Reed NA et al. 2006. Curr Biol. 10.1016/j.cub.2006.09.014 [M]
- Dompierre JP et al. 2007. J Neurosci. 10.1523/JNEUROSCI.0037-07.2007 [M]
- Magiera MM et al. 2018. EMBO J. 10.15252/embj.2018100440 [M]
- Bodakuntla S et al. 2021. Neurosci Lett. 10.1016/j.neulet.2021.135656 [M]
- Bodakuntla S et al. 2019. Trends Cell Biol. 10.1016/j.tcb.2019.07.004 [M]
- Ittner LM et al. 2010. Cell. 10.1016/j.cell.2010.06.036 [A]
- Hoover BR et al. 2010. Neuron. 10.1016/j.neuron.2010.11.030 [M]
- Harada A et al. 2002. J Cell Biol. 10.1083/jcb.200110134 [M]
- Wang Y, Mandelkow E 2016. Nat Rev Neurosci. 10.1038/nrn.2015.1 [M]
- Lei P et al. 2012. Nat Med. 10.1038/nm.2613 [M]
- Yu W et al. 2008. Mol Biol Cell. 10.1091/mbc.e07-09-0878 [M]
- Roll-Mecak A, Vale RD 2008. Nature. 10.1038/nature06482 [M]
- Qiang L et al. 2006. J Neurosci. 10.1523/JNEUROSCI.5392-05.2006 [M]
- Siahaan V et al. 2019 (bioRxiv preprint). 10.1101/424374 [M]
- Hu X et al. 2008. J Neurosci. 10.1523/JNEUROSCI.3074-08.2008 [A]
- Jaworski J et al. 2009. Neuron. 10.1016/j.neuron.2008.11.013 [A]
- Kapitein LC et al. 2011. J Neurosci. 10.1523/JNEUROSCI.6215-10.2011 [M]
- Merriam EB et al. 2013. J Neurosci. 10.1523/JNEUROSCI.0661-13.2013 [M]
- Hu X et al. 2011. J Neurosci. 10.1523/JNEUROSCI.2445-11.2011 [M]
- Hirokawa N et al. 2010. Neuron. 10.1016/j.neuron.2010.09.039 [M]
- Stokin GB, Goldstein LSB 2006. Annu Rev Biochem. 10.1146/annurev.biochem.75.103004.142637 [M]
- Watanabe Y, Gould E, McEwen BS 1992. Brain Res. 10.1016/0006-8993(92)91597-8 [M]
- Magarinos AM, McEwen BS 1995. Neuroscience. 10.1016/0306-4522(95)00256-i and 10.1016/0306-4522(95)00259-l [M]
- Magarinos AM et al. 1997. PNAS. 10.1073/pnas.94.25.14002 [A]
- Vyas A et al. 2002. J Neurosci. 10.1523/JNEUROSCI.22-15-06810.2002 [M]
- Radley JJ et al. 2004. Neuroscience. 10.1016/j.neuroscience.2004.01.006 [M]
- Radley JJ et al. 2005. Cereb Cortex. 10.1093/cercor/bhi104 [A]
- Radley JJ et al. 2005b. Exp Neurol. 10.1016/j.expneurol.2005.07.008 [M]
- Cerqueira JJ et al. 2005. J Neurosci. 10.1523/JNEUROSCI.1598-05.2005 [M]
- Liston C et al. 2006. J Neurosci. 10.1523/JNEUROSCI.1184-06.2006 [M]
- McEwen BS, Nasca C, Gray JD 2016. Neuropsychopharmacology. 10.1038/npp.2015.171 [M]
- Sapolsky RM 2000. Arch Gen Psychiatry. 10.1001/archpsyc.57.10.925 [M]
- Sapolsky RM, Krey LC, McEwen BS 1986. Endocr Rev. 10.1210/edrv-7-3-284 [M]
- Sotiropoulos I et al. 2008. J Neurochem. 10.1111/j.1471-4159.2008.05613.x [M]
- Sotiropoulos I et al. 2011. J Neurosci. 10.1523/JNEUROSCI.0730-11.2011 [A]
- Rissman RA et al. 2012. PNAS. 10.1073/pnas.1203140109 [A]
- Lopes S et al. 2017. Cereb Cortex. 10.1093/cercor/bhw057 [A]
- Brunden KR et al. 2010. J Neurosci. 10.1523/JNEUROSCI.3059-10.2010 [A]
- Barten DM et al. 2012. J Neurosci. 10.1523/JNEUROSCI.0188-12.2012 [A]
- Boxer AL et al. 2014. Lancet Neurol. 10.1016/S1474-4422(14)70088-2 [A]
- NCT01492374, BMS-241027 mild AD. https://clinicaltrials.gov/study/NCT01492374 [A, via API]
- Hameroff S, Penrose R 2014. Phys Life Rev. 10.1016/j.plrev.2013.08.002 [M]
- Tegmark M 2000. Phys Rev E. 10.1103/PhysRevE.61.4194 [A]
- Reimers JR et al. 2009. PNAS. 10.1073/pnas.0806273106 [M]
- McKemmish LK et al. 2009. Phys Rev E. 10.1103/PhysRevE.80.021912 [M]
- Craddock TJA et al. 2017. Sci Rep. 10.1038/s41598-017-09992-7 [M]
- Kalra AP et al. 2023. ACS Cent Sci. 10.1021/acscentsci.2c01114 [M]
- Babcock NS et al. 2024. J Phys Chem B. 10.1021/acs.jpcb.3c07936 [M]
- Kerskens CM, Perez DL 2022. J Phys Commun. 10.1088/2399-6528/ac94be [M]
- Khan S et al. 2024. eNeuro. 10.1523/ENEURO.0291-24.2024 [A]
- GEO series: GSE109315, GSE127812, GSE81587, GSE138670 (URLs in section 6) [records read]
- Sotiropoulos I et al. 2016 conference abstract. 10.1016/j.jalz.2016.06.2170 [M, abstract only]
- Alzforum BMS-241027 entry, https://alzforum.org/node/192066: UNVERIFIED (seen in search results only, not opened)
- Allen Brain Map Terms of Use, GTEx data use terms, PsychENCODE access page: UNVERIFIED (not opened)
