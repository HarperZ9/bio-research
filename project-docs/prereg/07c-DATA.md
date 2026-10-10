# Project 07c data receipts

Downloaded 2026-10-09 (Pacific) after the pre-registration was committed
(commit bda508e, 07c-phospho-tau-hippocampus.md SHA-256
ae2a23f6ad0f4493ef46f23a6466d44b8464aae67871178b9a0d369a6f8befe7). Local root:
`H:\bio-data\proteomics`. Processed tables only; no raw files. Sizes in bytes.
Python environment: `H:\bio-data\venv07` (as 07b).

## Metadata read before the pre-registration (no data tables)

| Local path | URL | Bytes | SHA-256 |
|---|---|---|---|
| meta/PXD057176.json | https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD057176&outputMode=json | 6788 | cf2dac7aa286350190f00240f06fd35981edb4bada7347c5d7f69bb0a18ad989 |
| meta/PXD050750.json | https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD050750&outputMode=json | 6305 | ec5132b13973cf1bcf4fb4e5c654fac9c9272871eef4477a9f18046d566b45fa |
| meta/iprox_PXD057176.json | https://www.iprox.cn/proxi/datasets/PXD057176 | 6567 | de2732c6cc01414f1d36a46dd9ae5e25b81d5f970f2b3ff71c95db5c4f15d033 |
| meta/iprox_PXD050750.json | https://www.iprox.cn/proxi/datasets/PXD050750 | 5735 | 11c99d42e6bd105967787903d7d2cdc040000789dd418d6b61a055918d76528a |
| meta/springer_42322444.html | https://link.springer.com/article/10.1007/s11064-026-04819-2 | 549388 | 90feba12277e56de67182150e04e96172d97a377954d33bc45495722c9a549d3 |
| ref/rat_tau_P19332_iso.fasta | https://rest.uniprot.org/uniprotkb/stream?query=accession:P19332&includeIsoform=true&format=fasta | 5247 | 848ac92edc68806524881e07ba25bc223af0dff81a6693a7cc473af8edbc2887 |
| ref/human_tau_P10636_iso.fasta | https://rest.uniprot.org/uniprotkb/stream?query=accession:P10636&includeIsoform=true&format=fasta | 5261 | 5dc981d2afdaad6b862d6b5c13d186ed94284999e52ba0cfb3e8964e1f2809f8 |

Europe PMC records for PMID 42322444 and 38852542 were read through the REST
search API (both closed access). The ScienceDirect page for PMID 38852542
returned a bot challenge and was not read.

## PXD057176 (iProX IPX0010016000)

Licence: UNVERIFIED. Neither the ProteomeXchange record nor the iProX PROXI
record has a licence field. The paper is closed access (Springer). Use here
is analysis of a public deposit for private research.

| Local path | URL | Bytes | SHA-256 |
|---|---|---|---|
| PXD057176/Phospho_Report.zip | http://download.iprox.org/IPX0010016000/IPX0010016001/Phospho_Report.zip | 65595386 | 1d6300ea65a831e4091388091f303468d6f43bd1437ab6e95f381026a1735063 |

Byte count matches the HTTP HEAD size read before the pre-registration. iProX
publishes no checksums that were found. Archive contents (Spectronaut
reports, tab-separated text despite the .xls suffix), extracted to
`PXD057176/Phospho_Report/`:

| File | Bytes | SHA-256 | Used |
|---|---|---|---|
| Report_PTMSiteReport (Normal).xls | 21578442 | 871c1990ae6d5eded831237afb96e12c82657c41e4d2216cfc1fd4ebc2565807 | yes (format a) |
| Report_PTMSiteReport (Pivot).xls | 4219487 | a7514ca980db1769c7a2ad6f291d945e8ad31e35295dca9999f286a44700961e | no (no site probability column) |
| Report_BGS Factory Report (Normal).xls | 170293136 | 4c99eea73dbc19014b5483e50fc3e7c85810b4032b0049f0ab3cd9582f0f6946 | imputation flag check only |
| Report_Peptide Quant (Normal).xls | 46569770 | bdd5f20e87cfd3e774d7fd1c089f8fccd77fda4a697fd522fe8630223e863ef0 | no |
| Report_Peptide Quant (Pivot).xls | 4934132 | 0552af054b3ac9bf3ef6a728e003feec74fd0d638f520ba140214f59872e4a9c | no |
| Report_peptides (Pivot).xls | 15834277 | 943afeacc0910aaed9336b93911f88e74be3ee5df69c4df4e8cf09ec34eadc26 | no |

Run names: the 18 `R.FileName` values match the 18 raw-file names of the
ProteomeXchange record one to one. The report's `R.Condition` column reads
C_C, C_D, C_I, X_C, X_D, X_I, consistent with the pre-registered decoding.

Table facts: 45,636 phospho rows (site x multiplicity x run), 4,929 collapse
keys; every row with a numeric quantity already has site probability >= 0.75
(Spectronaut filtered at export), so the pre-registered filter removed nothing
further. `EG.IsImputed` in the BGS report is False on all 222,662 rows.

## PXD050750

Not downloaded. Design and n could not be decoded from metadata
(pre-registration section 2).

## Outputs

| File | SHA-256 (as written, LF) |
|---|---|
| project-docs/prereg/07c-results/primary-PXD057176.json | 62c167b48ae69e7939bcf9fed5f5479126045613efdfe5acaa8191faf98ef431 |
| project-docs/prereg/07c-results/posctl-PXD024829-rerun.json | b7a2a45d4f78ec9f94c7caad7557e31d3f62bf3c1be0fc2e6aaa68373e396c3d (byte-identical to the 07b positive-control output) |
