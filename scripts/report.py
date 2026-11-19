#!/usr/bin/env python3
"""report — finalize a literature search into result.json.

Usage:
    python3 report.py --case /input/case.json --work /app/work
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save(path: Path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True)
    ap.add_argument("--work", required=True)
    args = ap.parse_args(argv)

    case = load(Path(args.case))
    work = Path(args.work)
    cand = load(work / "candidates.json")
    log = load(work / "search_log.json")

    candidates = cand.get("candidates", [])
    result = {
        "case_id": cand.get("case_id") or case.get("case_id") or case.get("id") or Path(args.case).stem,
        "task": "literature-screening-and-ranking",
        "status": "complete" if candidates else "partial",
        "deliverables": {
            "candidates": "candidates.json",
            "search_log": "search_log.json",
        },
        "question": cand.get("question"),
        "screening_criteria": cand.get("screening_criteria"),
        "screening_summary": cand.get("screening_summary"),
        "queries": cand.get("queries"),
        "counts": {
            "sources": cand.get("source_count"),
            "raw_records": cand.get("raw_records"),
            "unique_records": cand.get("unique_records"),
            "candidates": len(candidates),
            "with_doi": sum(1 for c in candidates if c.get("doi")),
            "with_abstract": sum(1 for c in candidates if c.get("abstract")),
        },
        "top_candidates": candidates[:20],
        "omissions": cand.get("omissions", []),
        "uncertainty": cand.get("omissions", []),
        "sources": [c.get("source_file") for c in candidates[:20]],
        "changes": [
            {"step": "collect", "detail": f"{cand.get('raw_records')} raw records from {cand.get('source_count')} sources"},
            {"step": "dedupe", "detail": f"{cand.get('unique_records')} unique after DOI/title dedup"},
            {"step": "rank", "detail": cand.get("method")},
        ],
    }
    save(work / "result.json", result)
    print(f"report: {len(candidates)} candidates, status={result['status']}")
    return result


if __name__ == "__main__":
    main()
