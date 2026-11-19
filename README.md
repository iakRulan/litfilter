# litfilter — 文献筛选与智能排序 Skill

在检索基础上加入**显式筛选**：每条文献的保留/剔除都有理由，幸存者按透明规则排序。

## 解决什么问题
普通检索只给排序结果，不说明剔除依据；重复文献被当成两篇；结果集与检索范围不符。

## 依赖
- Python 3.9+，仅标准库；离线使用缓存响应。

## 用法
```bash
python3 scripts/search.py --case /input/case.json --work /app/work
python3 scripts/report.py --case /input/case.json --work /app/work
```

输入示例：
```json
{
  "case_id": "demo",
  "question": "attention for machine translation",
  "responses": ["cr.json"],
  "screening": {"include": ["attention"], "exclude": ["gardening"], "min_year": 2015}
}
```
> 示意示例，不是正式案例结果。

## 输出
| 文件 | 内容 |
|-|-|
| `candidates.json` | 纳入集（含 relevance 与筛选理由）、剔除集、筛选汇总、遗漏 |
| `search_log.json` | 来源/查询记录数与错误 |
| `result.json` | `case_id` / `status` / counts / screening_summary / top_candidates |

## 筛选规则
- 命中 `exclude` → 剔除（给出命中词）
- 未命中任何 `include` → 剔除
- 缺少 `must_have` → 剔除
- 年份超出 `[min_year, max_year]` → 剔除
- 无纳入词时保留并注明

## 关键设计
- 决策有理由；去重按 DOI/标题；排序透明可复算；遗漏显式；元数据不臆造。

## 局限
- 词面匹配不识别同义词；筛选词需案例或模型提供。

## 版本
litfilter 1.0.0，纯 Python 标准库。
