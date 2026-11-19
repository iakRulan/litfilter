# 输出字段字典

## `candidates.json`
- `case_id` / `question`
- `screening_criteria{}`：include / exclude / must_have / min_year / max_year
- `screening_summary{}`：included / excluded
- `queries[]`：检索查询计划
- `candidates[]`：纳入记录（含 `relevance{score,rationale,coverage,query}` 与 `screening{decision,reasons}`）
- `excluded[]`：剔除记录（含 `screening.reasons`）
- `omissions[]`

## `result.json`
`case_id` / `task` / `status` / `counts{sources,raw_records,unique_records,candidates,with_doi,with_abstract}` / `screening_summary` / `top_candidates` / `omissions` / `uncertainty` / `sources` / `changes`
