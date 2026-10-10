# Project 07 analysis log

Append-only. Times are local (Pacific), 2026-10-09.

| Step | Event | Commit | SHA-256 |
|---|---|---|---|
| 1 | Pre-registration v1 committed; no expression data downloaded or opened | 16b34fd | 07-microtubule-screen.md v1: 4ec33fd8b9f292b420d3dc55e6b194f091cdd952d658d1f833a8a075da4fef95 |
| 1 | Gene set M frozen (32 genes) | 16b34fd | 07-geneset-M.txt: 0dd7f70afee5b9a6d8d7a2c1b26069d6d2acc2104dc095a799fe24dbf4ad3a99 |
| 2 | Pre-registration v2 committed: held-out C = GSE72343 PFC (fallback GSE161726); no expression data downloaded | c936dd6 | 07-microtubule-screen.md v2: b21b3093bb94606b859e21ddf675fe3a0e4f1c62020c5ac54f429c2287fbd1ca |
| 3 | Downloads (processed files only) recorded in 07-DATA.md; GSE72343 had no per-sample values, fallback GSE161726 used | commit adding this row | see 07-DATA.md |
| 4 | Analysis run as pre-registered; result NULL in discovery (p DOWN 0.31), positive control failed in discovery; entry F-07-1 in FINDINGS.md | commit adding this row | 07-results/07-results.json: dfdf65d5dc5ca6b3f741585f3299b708462d6403f7706ef42ffb2b1989f566f9 |
