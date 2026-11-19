---
name: litfilter
description: "Screen and rank literature with explicit criteria: collect records from the supplied sources, deduplicate by DOI/title, apply the case's inclusion/exclusion/must-have/year criteria with a per-record reason, rank the survivors by transparent term-overlap scoring, and report the included set, the excluded set with reasons, and omissions. Trigger on: '文献筛选', '智能排序', '筛选与排序', 'screen and rank papers', 'inclusion exclusion criteria', '文献排序'. Not for: reading a single paper, writing, or drawing."
---

# litfilter — Literature Screening and Transparent Ranking

Deliver a screened, ranked candidate set where every keep/drop decision has a stated reason. The failure mode this skill exists to prevent: a ranked list with no screening rationale, silent exclusion of records, duplicates counted as separate papers, and a result set that does not match the stated scope.

**Method in one line:** collect → normalize → dedupe by DOI/title → apply the case's screening criteria with per-record reasons → rank the survivors by transparent scoring → report included + excluded + omissions.

## When to use

- Input: a case file (default `/input/case.json`) with the research question, sources/cached responses, and screening criteria (`screening.include` / `exclude` / `must_have` / `min_year` / `max_year`).
- Output: under `/app/output` — `candidates.json`, `search_log.json`, `result.json`.

## Pipeline

```bash
python3 scripts/search.py --case /input/case.json --work /app/work
python3 scripts/report.py --case /input/case.json --work /app/work
```

1. **Collect & normalize** — same multi-source loader as the retrieval skill (Crossref `message.items`, EuropePMC `resultList.result`, generic lists). Every record keeps `source_file` + `record_id`.
2. **Query plan** — verbatim / title+abstract / core-concepts / provided.
3. **Dedupe** — DOI first, then normalized title; the richer record wins.
4. **Screen** — each record gets `screening.decision` (`include`/`exclude`) and `screening.reasons`:
   - any `exclude` term in title/abstract/venue → `exclude` (reason names the term);
   - no `include` term hit → `exclude`;
   - missing a `must_have` item → `exclude`;
   - year outside `[min_year, max_year]` → `exclude`.
5. **Rank** — survivors scored by `(3·title_hits + 1·abstract_hits + 2·coverage + 0.5·doi + 0.3·abstract + recency) · source_weight`, with the rationale stored.
6. **Report** — `candidates` (included), `excluded` (with reasons), `screening_summary`, `omissions`.

## Rules that must hold

1. **Every decision has a reason.** A record is never dropped silently.
2. **Dedupe by identity.** DOI, then normalized title.
3. **Ranking is transparent.** Score formula + winning query stored per record.
4. **Omissions are stated.** Empty result, missing DOI, no recent records, unreachable sources.
5. **No fabricated metadata.** Missing fields stay empty.

## Exception handling

| Situation | Behaviour |
|-|-|
| No criteria supplied | all records kept, reason "无显式纳入词，保留" |
| Payload shape unknown | logged; records skipped |
| Live API unreachable | falls back to cached responses |
| No records | `status: partial`, omissions explains |

## Self-check

```bash
python3 -c "import json;c=json.load(open('/app/work/candidates.json'));print(c['screening_summary']);print(all('screening' in x for x in c['candidates']))"
python3 -c "import json;r=json.load(open('/app/work/result.json'));print(r['case_id'], r['status'], r['counts'])"
```
