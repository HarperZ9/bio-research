# Project 07b data receipts

Downloaded 2026-10-09 (Pacific) after the pre-registration was committed
(commit 05cb868, 07b-phospho-tau.md SHA-256
d9b5ce948da9aa49e91afb7c0173482c5beb65976153538a1fe0b919f7a573fc). Local root:
`H:\bio-data\proteomics` (WSL `/mnt/h/bio-data/proteomics`). Processed tables
only; no raw files. Sizes in bytes. Python environment: `H:\bio-data\venv07`
(Python 3.12.10, numpy, scipy, pandas as logged in 07-DATA.md; pytest 9.1.1
added for this run).

## Dataset records (ProteomeXchange)

| Local path | URL | Bytes | SHA-256 |
|---|---|---|---|
| meta/PXD024829.json | https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD024829&outputMode=json | 36780 | ffa16fa08c7d6057f273b69c8e354f8cf9b35dcb3e1568d4d371d20e7b82df66 |
| meta/PXD016302.json | https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD016302&outputMode=json | 6386 | a242350d32efb2d4848dbbbbb9e05565d0dddb303b4d6820fe797555a3cad9cd |

Hosting per the records: PXD024829 on PRIDE (ftp.pride.ebi.ac.uk, archive
2022/02); PXD016302 on iProX (download.iprox.org, IPX0001870000/IPX0001870001).

## PXD024829 (positive control), downloaded first

Licence: CC0 (PRIDE Archive API v3 project record, field `license`, read
2026-10-09).

| Local path | URL | Bytes | SHA-256 |
|---|---|---|---|
| PXD024829/20191031_174447_20191028_AllPhosphoData_Report.csv | https://ftp.pride.ebi.ac.uk/pride/data/archive/2022/02/PXD024829/20191031_174447_20191028_AllPhosphoData_Report.csv | 447498775 | 5ac3d8f1af4710ce8ab4685c7212090a6cc40c088986d75f7c9aae8522355237 |
| PXD024829/Metadata_Phosphos.csv | https://ftp.pride.ebi.ac.uk/pride/data/archive/2022/02/PXD024829/Metadata_Phosphos.csv | 9142 | 9eee098e65c72dcc5471a93b54bd701c0b852f76418f16a8dbff0e00b8e74855 |
| PXD024829/checksum.txt | https://ftp.pride.ebi.ac.uk/pride/data/archive/2022/02/PXD024829/checksum.txt | 23224 | 918a6ef9460a031106c4a4a846db997c04d3d3c98a0beca4feefa7d37a584d5a |

The deposited checksum.txt lists SHA-1 values. Both files match:
report ffb0c184c334e48b1c3e73b4d2363d9f535f2d1c, metadata
8a42024a3a4b97df39e26e778f5f09a62249f95c.

Design read from Metadata_Phosphos.csv: Experiment 1 (`ShortExp` Exp1), dHC,
`ShortCond` SW06 (killed directly after the 6 min swim; animals 13, 5, 9, 1, 7, 3)
vs CON (home cage; animals 14, 6, 10, 2, 8, 12, 4). 6 vs 7, one file per animal,
two processing blocks.

## Reference proteome (added; not named in the pre-registration)

| Local path | URL | Bytes | SHA-256 |
|---|---|---|---|
| ref/mouse_sprot_iso.fasta.gz | https://rest.uniprot.org/uniprotkb/stream?query=organism_id:10090+AND+reviewed:true&includeIsoform=true&format=fasta&compressed=true | 9004225 | 94b4f1e541fca31905d9583114bba4a2f024670545f80d14743b8619da661671 |

25,758 entries (Swiss-Prot mouse with isoforms). Used only to place Spectronaut
peptides on protein coordinates for the positive control. Licence: UniProt
CC BY 4.0 (from memory, moderate confidence).

## PXD016302 (primary)

Licence: UNVERIFIED. The ProteomeXchange record has no licence field; the iProX
PROXI endpoint returned an empty record; the iProX project page is
script-rendered. The paper is CC BY. Use here is analysis of a public deposit
for private research.

| Local path | URL | Bytes | SHA-256 |
|---|---|---|---|
| PXD016302/Phospho (STY)Sites.txt | http://download.iprox.org/IPX0001870000/IPX0001870001/Phospho%20(STY)Sites.txt | 48487463 | ae86672cdf4d0ff1e355a2c8c9774ae369f109351d96b6b99bca759f0ec50061 |
| PXD016302/proteinGroups.txt | http://download.iprox.org/IPX0001870000/IPX0001870001/proteinGroups.txt | 15106654 | baa0e52e109d602ac7b2402eac830895e5a2656e176e805156263f676d56d225 |

peptides.txt (20,428,658 bytes) was not downloaded; no step uses it. iProX
publishes no checksums that were found, so integrity rests on byte counts,
which match the brief's HTTP HEAD sizes.

Group labels: the site table has intensity columns A to R (17, no Q) and
XY-1 to XY-18 (18). Raw-file names in the ProteomeXchange record carry group
labels for letters A to R: A, B, C = "mPFC_control+saline_repeat_1..3";
D, E, F = "mPFC_CUMS+saline_repeat_1..3". The XY-n columns match no deposited
raw-file name and are not described anywhere read; they were not used.

## Outputs

| File | SHA-256 (as written, LF) |
|---|---|
| project-docs/prereg/07b-results/posctl-PXD024829.json | b7a2a45d4f78ec9f94c7caad7557e31d3f62bf3c1be0fc2e6aaa68373e396c3d |
| project-docs/prereg/07b-results/primary-PXD016302.json | 5355d27bf8f8e1b5dfa29da3fec5a9c49b21b1ea8115812cf41c5b64da3b28ad |
