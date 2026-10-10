# Audit 04 codebook: does a citing sentence claim more than the cited study measured?

Version 1.0. Written 2026-10-09 before any citing sentence was retrieved or read.
Source for "what was measured": project-docs/briefs/04-mycorrhizal-network-audit.md
(sections 2, 3 and 8). The brief read both papers at abstract depth only, so the
measured lists below are abstract-level descriptions. Confidence that they are
complete: moderate.

## 1. Unit of coding

One unit is one citation context: the sentence (or sentence fragment) that
Semantic Scholar returns as the place where a citing paper cites the target paper.
Each unit has an id, the target paper (SIMARD1997 or BEILER2010) and the text.
Code the claim the sentence attaches to the target citation. Ignore everything you
know about the citing paper.

## 2. What each target study measured

### SIMARD1997
Simard SW, Perry DA, Jones MD, Myrold DD, Durall DM, Molina R (1997). Net transfer
of carbon between ectomycorrhizal tree species in the field. Nature 388:579-582.
doi:10.1038/41557 (DOI confirmed by Crossref title search on 2026-10-09).

Measured (per abstract, as summarized in the brief):
- Field study in British Columbia with tree seedlings, not mature trees.
- Reciprocal isotope labeling (13C and 14C) of paper birch (Betula papyrifera) and
  Douglas-fir (Pseudotsuga menziesii), both ectomycorrhizal (EcM).
- Carbon moved in both directions between birch and Douglas-fir.
- Net transfer was to Douglas-fir, averaging about 6% of the carbon isotope uptake
  by photosynthesis.
- Shading of Douglas-fir changed (increased) net transfer.
- Western redcedar (arbuscular mycorrhizal, not EcM) took up little isotope; the
  authors read this as evidence for a hyphal (EcM) route.
- The authors interpreted the transfer as moving through shared EcM fungi.

Not measured: seedling survival, growth or fitness effects; mature or "mother"
trees; kin or relatedness; defense or warning signals; network topology or genet
mapping; persistence of links; exclusion of the soil-solution pathway (Karst et
al. 2023 state the result is consistent with a soil pathway); any forest type
other than this mixed birch, Douglas-fir and redcedar seedling system.

### BEILER2010
Beiler KJ, Durall DM, Simard SW, Maxwell SA, Kretzer AM (2010). Architecture of the
wood-wide web: Rhizopogon spp. genets link multiple Douglas-fir cohorts. New
Phytologist 185:543-553. doi:10.1111/j.1469-8137.2009.03069.x (Crossref-confirmed
2026-10-09; online 2009, issue 2010).

Measured (per abstract, as summarized in the brief):
- Microsatellite genotyping of two Rhizopogon species (R. vesiculosus and
  R. vinicolor) on root tips and of interior Douglas-fir trees.
- One 30 x 30 m plot in an old-growth interior Douglas-fir stand in British Columbia.
- Each Rhizopogon species formed 13 to 14 genets; a single genet colonized up to 19
  trees.
- Genets linked trees of multiple age cohorts.
- The network had a scale-free, hub-dominated topology; large old trees were the
  most connected nodes.

Not measured: movement of carbon, nitrogen, water or any resource (no flow at
all); seedling survival or growth; kin or relatedness effects; signals; whether a
mapped link is functional or persistent; any forest type beyond the one plot.

## 3. Primary code (exactly one per unit)

Apply the decision order in section 5.

- ACCURATE. The claim attached to the citation is within what the study
  measured (section 2), including a fair description of its limits or a critique
  of it that describes it correctly.
- OVERREACH. The claim attached to the citation goes beyond what the study
  measured in at least one way listed in section 4. This includes claims stated as
  speculation (see the hedge rule).
- NEUTRAL. The citation is used for method, site, species, taxonomy, general
  mycorrhizal background, or as a pointer that a topic was studied, and the
  sentence makes no claim about networks, transfer or network effects.
- UNCLEAR. The text is too truncated or garbled to read, is not in English, or it
  is impossible to tell which claim the citation supports.

## 4. Overreach subtypes (one or more for every OVERREACH)

- O1 MAGNITUDE: transfer "in amounts that matter", "substantial", "large",
  "significant amounts", "enough to subsidize", "nourishes". The word
  "significant" alone, reading as a statistical result, is not O1.
- O2 BENEFIT: CMN or transfer improves seedling or tree survival, growth,
  establishment, facilitation or fitness.
- O3 KIN_MOTHER: kin preference, mother trees nurturing, feeding or recognizing
  offspring, altruism, parental care.
- O4 SIGNAL: warning, defense or stress signals, communication, information
  transfer, "talking" trees.
- O5 UBIQUITY: CMNs stated as general fact across forests or plants ("forest trees
  are interconnected", "all trees are linked", "most plants share networks")
  without a qualifier such as "can" or "in Douglas-fir forests".
- O6 CERTAINTY: "proved", "demonstrated conclusively", "established", "it is now
  known", or route stated as settled with the soil pathway ruled out.
- O7 FLOW_FROM_STRUCTURE: resource movement attributed to a study that mapped
  structure only (any transfer claim citing BEILER2010 alone as support).
- O8 SYSTEM_MISMATCH: wrong organisms, life stage or setting attributed to the
  study (for example SIMARD1997 cited for mature trees, mother trees, a
  greenhouse study, or for transfer to a non-EcM host).

## 5. Decision order

1. Can the sentence be read, and can you tell which claim the target citation
   supports? If no, UNCLEAR.
2. Does the sentence make any claim about mycorrhizal networks, shared fungi,
   transfer, or network effects that the citation supports? If no, NEUTRAL.
3. Compare each part of that claim with section 2. If any part goes beyond the
   "Measured" list, OVERREACH with every applicable subtype. Otherwise ACCURATE.

Specific rules:
- Hedge rule: a claim beyond the study stays OVERREACH even when hedged ("may",
  "might", "could", "has been suggested"), because the citation is offered as
  support for something the study did not test. Mark hedged = Y.
- SIMARD1997 route rule: "carbon transfer between trees through mycorrhizal
  networks / shared fungi" matches the authors' own reported interpretation and is
  ACCURATE. It becomes OVERREACH (O6) only with proof or certainty language, or
  when stated as having excluded the soil pathway.
- "Trees" for seedlings: "transfer between trees" citing SIMARD1997 is ACCURATE.
  "From large / mature / old / mother trees to seedlings" is O8 (and O3 if
  nurturing is implied).
- BEILER2010 hub rule: "large old trees are hubs / most connected" is ACCURATE.
  Hubs that "support", "nurse" or "supply" seedlings are O7 and O3 or O2.
- Multi-citation sentences: code the target against the whole claim the citation
  group supports. Mark multi_cite = Y when the sentence cites other sources for
  the same claim. Report shares with and without multi_cite units.

## 6. Recording format

One row per unit: id, code, subtypes (semicolon list, blank unless OVERREACH),
hedged (Y/N), multi_cite (Y/N), note (one short line, optional).

## 7. Two coders and disagreement rule (fixed before coding)

- Coder A (lead session) and coder B (a separate subagent given only this
  codebook and the units) code independently. Neither sees the other's codes.
- Both original code files are kept unchanged.
- Agreement: Cohen's kappa on the primary code (four categories), plus raw percent
  agreement.
- Resolution rule, applied mechanically:
  - Strict estimate: a unit counts as OVERREACH only when both coders coded it
    OVERREACH. This is the primary (lower-bound) estimate.
  - Lenient estimate: a unit counts as OVERREACH when either coder coded it
    OVERREACH. This is the upper bound.
  - Each coder's own share is also reported.
  - Subtype counts use units where both coders coded OVERREACH, counting a subtype
    when either coder listed it.

## 8. Analysis plan (fixed before retrieval)

- Sampling: one context per citing paper (chosen at random), then up to 100 citing
  papers per target, stratified by publication year bucket with proportional
  allocation. Seed 20261009.
- Year buckets: 1997-2009, 2010-2016, 2017-2022, 2023-2026 (2023 onward is after
  Karst et al. 2023).
- Shares: OVERREACH / all sampled units, and OVERREACH / (ACCURATE + OVERREACH).
- Intervals: Wilson 95% score interval.
- Citing papers with no year are kept in the sample frame under bucket "unknown"
  and reported separately.
