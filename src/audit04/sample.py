"""Build the per-target frame and a seeded, year-stratified sample.

Frame: citing papers with at least one non-empty context. One context per
citing paper is chosen at random (seeded). Up to PER_TARGET papers per target,
proportional allocation across year buckets (largest-remainder rounding).
Writes data/audit04/coverage.csv, sample.csv and units_blind.csv.
"""
import csv
import json
import random

from config import DATA, PER_TARGET, RAW, SEED, TARGETS, bucket


def load_records(target):
    recs = []
    for path in sorted((RAW / target).glob("page_*.json")):
        recs.extend(json.loads(path.read_text(encoding="utf-8")).get("data", []))
    return recs


def allocate(sizes, n):
    """Proportional allocation with largest-remainder rounding, capped by size."""
    total = sum(sizes.values())
    if total <= n:
        return dict(sizes)
    quotas = {k: n * v / total for k, v in sizes.items()}
    alloc = {k: int(q) for k, q in quotas.items()}
    order = sorted(quotas, key=lambda k: quotas[k] - alloc[k], reverse=True)
    for k in order[: n - sum(alloc.values())]:
        alloc[k] += 1
    return alloc


def build(target, rng):
    recs = load_records(target)
    frame, seen = [], set()
    for r in recs:
        paper = r.get("citingPaper") or {}
        pid = paper.get("paperId")
        ctxs = [c.strip() for c in (r.get("contexts") or []) if c and c.strip()]
        if not pid or pid in seen or not ctxs:
            continue
        seen.add(pid)
        k = rng.randrange(len(ctxs))
        frame.append({
            "target": target, "citing_paper_id": pid,
            "title": paper.get("title") or "", "year": paper.get("year"),
            "bucket": bucket(paper.get("year")), "n_contexts": len(ctxs),
            "context_index": k, "context": ctxs[k],
            "intents": ";".join(sorted({i for i in (r.get("intents") or []) if i})),
        })
    by_bucket = {}
    for row in frame:
        by_bucket.setdefault(row["bucket"], []).append(row)
    alloc = allocate({b: len(v) for b, v in by_bucket.items()}, PER_TARGET)
    chosen = []
    for b in sorted(by_bucket):
        chosen.extend(rng.sample(by_bucket[b], alloc[b]))
    cov = {"target": target, "citing_records": len(recs),
           "with_context": len(frame),
           "frame_by_bucket": {b: len(v) for b, v in sorted(by_bucket.items())},
           "sampled_by_bucket": {b: alloc[b] for b in sorted(alloc)}}
    return chosen, cov


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main():
    rng = random.Random(SEED)
    sample, coverage = [], []
    for target in TARGETS:
        chosen, cov = build(target, rng)
        sample.extend(chosen)
        coverage.append(cov)
        print(json.dumps(cov))
    order = list(range(len(sample)))
    rng.shuffle(order)  # blind file is shuffled across targets and years
    for uid, i in enumerate(order, start=1):
        sample[i]["id"] = f"U{uid:03d}"
    sample.sort(key=lambda r: r["id"])
    fields = ["id", "target", "citing_paper_id", "title", "year", "bucket",
              "n_contexts", "context_index", "intents", "context"]
    write_csv(DATA / "sample.csv", sample, fields)
    write_csv(DATA / "units_blind.csv", sample, ["id", "target", "context"])
    (DATA / "coverage.json").write_text(json.dumps(coverage, indent=2),
                                        encoding="utf-8")


if __name__ == "__main__":
    main()
