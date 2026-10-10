# Audit 04 log

Append-only. Times are local, 2026-10-09.

1. DOI checks (Crossref, 2026-10-09). Title search "Net transfer of carbon between
   ectomycorrhizal tree species in the field" returned 10.1038/41557 as the top hit:
   Nature 388:579-582, 1997, authors Simard, Perry, Jones, Myrold, Durall, Molina.
   10.1111/j.1469-8137.2009.03069.x resolved to Beiler, Durall, Simard, Maxwell,
   Kretzer, New Phytologist 185:543-553 (Crossref issued date 2009-10-29).
   Semantic Scholar lookups: SIMARD1997 paperId e3047f087b1d859a1d900f37572ad51847789171
   (citationCount 891); BEILER2010 paperId 86f42d827b004e3662e664b0aae230bd99fe2767
   (citationCount 226). Confidence high.
2. Codebook v1.0 written before any citing sentence was retrieved.
   project-docs/audit04/CODEBOOK.md SHA-256: cc3d13ca9ca74d7d3bf9fff089339ae9265829304a2ebc28e925600e9875299f
3. Retrieval (src/audit04/fetch.py), 2026-10-09. Semantic Scholar Graph API
   /paper/DOI:<doi>/citations, fields contexts,intents,title,year,externalIds,
   limit 100, 3.5 s pause, no key, no rate-limit errors seen. Raw pages saved
   under data/audit04/raw/ (gitignored). SIMARD1997: 891 citing records, 334
   citing papers with at least one context (37%). BEILER2010: 226 citing records,
   105 with a context (46%). Coverage is partial; the rest had empty contexts.
4. Sample (src/audit04/sample.py), seed 20261009. One context per citing paper,
   proportional allocation by year bucket. SIMARD1997: 100 of 334 (1997-2009 43,
   2010-2016 21, 2017-2022 20, 2023-2026 14, unknown 2). BEILER2010: 100 of 105,
   2010-2016 45, 2017-2022 29, 2023-2026 23,
   unknown 3. Files: data/audit04/sample.csv (with year and title),
   data/audit04/units_blind.csv (id, target, context only, shuffled ids).
5. Coder B (separate subagent) launched with only CODEBOOK.md and
   units_blind.csv, before coder A began coding.
6. Coder A coded all 200 units from units_blind.csv (no year or title shown),
   wrote codes to a scratch file outside the repo until coder B finished.
   codes_A.csv SHA-256 at completion, before reading any coder B output:
   3fb69752c79d3ccb24a950fd77c92af22339f046ba4c7813700a412c96b5d606
   Coder A observations made while coding: S2 attaches some contexts to the
   target that show no matching citation marker (for example a sentence about
   ITSX software); several contexts cite "Simard et al. 1997a/b", which may be
   a different 1997 Simard paper that S2 merged; 5 contexts are not in English.
   These were coded UNCLEAR or by content as the codebook directs.
7. Coder B finished. data/audit04/codes_B.csv SHA-256
   d5deeb32db4161707816a05afbea20c44703b05b645b39afdd321000c5430335. Coder B
   reported it opened only the codebook and units file. It also noted that the
   shared scratchpad held coder A's files, which weakens blinding. Not enforced;
   recorded as a limit. Coder B's comment that the codebook lacks a
   resource-mismatch subtype (water, N, P cited to a carbon study) is noted for
   codebook v1.1. In v1.0 both coders used O8 for it.
8. codes_A.csv copied unchanged into data/audit04/ (hash matches entry 6).
   src/audit04/analyze.py computed kappa 0.893 (raw agreement 92.5%) and the shares
   in data/audit04/results.md. Disagreements resolved only by the pre-written
   strict and lenient rule; no code was changed. Finding appended as F-04-1 in
   project-docs/FINDINGS.md.
