# Project 07 data receipts

Downloaded 2026-10-09 over HTTPS from NCBI GEO and EBI (GENCODE). Local root:
`H:\bio-data\screen07` (WSL `/mnt/h/bio-data/screen07`). Processed files only;
no FASTQ. Sizes in bytes. Python environment: `H:\bio-data\venv07`
(Python 3.12.10, numpy 2.5.3, scipy 1.18.1, pandas 3.0.6, openpyxl 3.1.5,
matplotlib 3.11.2).

## Series-level files

| Local path | URL | Bytes | SHA-256 |
|---|---|---|---|
| raw/GSE109315/GSE109315_mPFC_counts_logCPM.txt.gz | https://ftp.ncbi.nlm.nih.gov/geo/series/GSE109nnn/GSE109315/suppl/GSE109315_mPFC_counts_logCPM.txt.gz | 4958620 | 4059b15ed332c5fe2b74f811bda00240d1f14909e0d755057225231b45d2957f |
| raw/GSE127812/GSE127812_mRNAs-expression.xlsx | https://ftp.ncbi.nlm.nih.gov/geo/series/GSE127nnn/GSE127812/suppl/GSE127812_mRNAs-expression.xlsx | 5324380 | 0cddca350a8369274e51cf8550f667d254aa9df56e52c4c2d71ded921d9e19a0 |
| raw/GSE72343/GSE72343_processed_data_files.tar.gz | https://ftp.ncbi.nlm.nih.gov/geo/series/GSE72nnn/GSE72343/suppl/GSE72343_processed_data_files.tar.gz | 2354028 | 89f2c32d0e34cee12d3d6f519ca6d83588e239e9067a5447c895cb0aa070beab |
| raw/GSE161726/filelist.txt | https://ftp.ncbi.nlm.nih.gov/geo/series/GSE161nnn/GSE161726/suppl/filelist.txt | 4445 | c1179e1ae9b7a7e9f2b5d32f4037e68d3a0d2a076cdcbb91b4f7e8cce797abb9 |
| ref/gencode.vM17.annotation.gtf.gz | https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M17/gencode.vM17.annotation.gtf.gz | 26087924 | 9a55407f2f193f6c74f202522d1a7bac5c928398dc667f4c51acbe837f81ce3c |

GSE72343 outcome: the archive lists only per-contrast differential-expression
tables (cuffdiff and diff_list files), no per-sample PFC values. Decided from the
`tar tzvf` file listing only. The pre-registered fallback GSE161726 was used
for held-out C. GSE72343 values were not analysed.

## GSE161726 mPFC per-sample files (19 of 66 samples; featureCounts, GENCODE M17)

URL pattern: `https://ftp.ncbi.nlm.nih.gov/geo/samples/GSM4913nnn/<GSM>/suppl/<file>`.
Sample-to-title map: raw/GSE161726/mpfc_samples.tsv (3067 bytes,
SHA-256 69aeebdf12e36714bb82e644af0b8cb04cb885149548ddb41b6591da4d800e09),
built from the GEO sample metadata.

| File | Bytes | SHA-256 |
|---|---|---|
| GSM4913341_C6_PFC_S49.tsv.gz | 3782383 | 715bdea533d3aeb78f9d858b8b1e48727177640f02153600af76864a1f1c2a55 |
| GSM4913342_C3_PFC_S52.tsv.gz | 3778490 | a38f1e50dbfc46447b822c4dce0499410821117b9c1cef7fa1b009c8b91d8a49 |
| GSM4913343_C1_PFC_S97.tsv.gz | 3784971 | d59a5217fa5148e640b73169aa1b8680b24eacf2b995fc3dc6bf593cb7a538cb |
| GSM4913344_C5_PFC_S103.tsv.gz | 3778980 | 312926489b6edab2800c8cf58f0f274d31c44aa90551258aacab17cf790e77d0 |
| GSM4913358_D9_PFC_S34.tsv.gz | 3783789 | 49ac7d4c8fcc7d9e3fe23dad8243bf23dae2d4ceb0fa7d26a175010c8dc159a0 |
| GSM4913359_D23_PFC_S40.tsv.gz | 3783739 | c085b121cee4cf210e23f04d6da3cd3173d32f6e8f878d89a0547d7888005acc |
| GSM4913360_D9_PFC_S85.tsv.gz | 3780041 | d306bd52bcbd15fefe8e49e9971099a5762788156b41a8f9a265e07395bb415a |
| GSM4913361_D10_PFC_S88.tsv.gz | 3776378 | 8db5da29aee3c084ac10bf5b150eb52dd1f4e746a56cd7171890cea78c7ef9c2 |
| GSM4913362_D18_PFC_S91.tsv.gz | 3785763 | 590cec92f28c7e164bb0f4e314c9b1e2cac7b4e3145e9c38bf2776ef492f8165 |
| GSM4913363_D27_PFC_S94.tsv.gz | 3783843 | b70864c9bad453c543a317342b39f22b2960077adb32b8dbb1195e7313dad31f |
| GSM4913375_D22_PFC_S22.tsv.gz | 3782194 | 73dd33f87489f126ad713a023d5f6d5351667200d250e02456cda8dcea3c563a |
| GSM4913376_D1_PFC_S64.tsv.gz | 3779169 | 925652a9e8a203731d9bbbb4a1fdb8babb966aea8e4ed577ebe8a190f7886652 |
| GSM4913377_D16_PFC_S67.tsv.gz | 3779217 | f96fa37d7243b652522ea0d89462571b6dd8a6aaafa9e91e8aa110185251acf8 |
| GSM4913378_D35_PFC_S70.tsv.gz | 3783928 | 13c32a828f9c4026d9b5949c5293eb3532b322ad255e06c3f8e4d35b233b5cc0 |
| GSM4913391_D16_PFC_S25.tsv.gz | 3773639 | 68377d3867f299a79ff9005f7e4ea579405cba6d657bb2497f65eb8c5c3d75e0 |
| GSM4913392_D18_PFC_S28.tsv.gz | 3768889 | 1ba13a735405276454e0234597d5842a20bdbc0212c54982455b916e8ec04fb5 |
| GSM4913393_D14_PFC_S31.tsv.gz | 3777564 | 349aaf3690022d84159b0aba80a9124ef883b384bf572792ae2e49d9995a2936 |
| GSM4913394_D2_PFC_S73.tsv.gz | 3783195 | e47deca8e3468fcef10e35c89c92495ec72a85d7915ee75917eaa6d546b7da8f |
| GSM4913395_D33_PFC_S82.tsv.gz | 3784478 | edcd12efb3f970bc2f6c1485bc2e917ecca0efc9deb816f30f86860b5c4a8723 |

## GEO sample metadata (no expression values)

Fetched by `src/screen07/annot.py` from
`https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=<GSE>&targ=gsm&form=text&view=brief`.

| Local path | SHA-256 |
|---|---|
| meta/GSE109315_gsm.txt | d51f3d694ce3e898a78318a08d62dc60cdf0251be19c4ab5e3f8671d9221a522 |
| meta/GSE127812_gsm.txt | 00b306a792de717b2a1a4567c9d630acc4bb12893846978bd0327ae289a68099 |
| meta/GSE161726_gsm.txt | 1d953381d4bbd7ab273a31301e2694e4f4373ffd8214dfa61b745cb800fb29ac |
