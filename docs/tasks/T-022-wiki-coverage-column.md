# T-022 — Remove coverage/source cutoff from Wiki AI-cost tables

Issue: [#48](https://github.com/mhaduk/ck3-dynasty-map/issues/48).

## Accepted result — 2026-10-25

Removed the public per-task `Coverage / source cutoff` column from Wiki Home and deleted its row-only prose. The five numeric/identity columns, all values, the existing five-column aggregate summary, Total row, global caveat, and all content outside the affected per-task table remain unchanged. Coverage, cutoff, and provenance remain in canonical task/accounting records.

The summary renderer in `scripts/wiki_cost_summary.py` already emits the accepted five-column aggregate table and does not generate the per-task table. The latter is maintained directly in Wiki Home; no template or generator was found that could reintroduce the removed column.

## Validation and publication

- Structural inspection confirmed each per-task row now has five cells and its original Type, Task, token, cached-token, and USD values.
- Search confirmed no `Coverage / source cutoff`, `Source cutoff`, or coverage column remains in the public Home table.
- Wiki commit `71ad14e77ddb4215fef089b007efedb57230b261` was pushed to `master`; independent remote readback confirmed the commit and the absence of coverage/source-cutoff text in the public tables.
- The repository's own `scripts/wiki_cost_summary.py` remains unchanged because it already generates only the five-column aggregate summary.

## AI costs

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6.1-sol | 1,715,406 | 1,656,064 | 59,342 | 8,309 | 1,723,715 | $0.36738040 |
| **Total** | **1,715,406** | **1,656,064** | **59,342** | **8,309** | **1,723,715** | **$0.36738040** |

Partial measured usage from one saved GUI session, using the cumulative token counters through the frozen cutoff `2026-10-25T08:18:24.289Z`. Work after that cutoff, including publication and closeout, is excluded. Cached input is a subset; reasoning is included in Output. No CLI session or linked automatic-review counters were assigned. This is a partial API-equivalent estimate, not subscription spending or an invoice.

Standard API-equivalent prices checked 2026-10-25: gpt-6.1-sol per million uncached/cached/output tokens at $2/$0.10/$10. Short-context rates apply; request-level context-length details and cache writes are unavailable. [Official model pricing](https://developers.openai.com/api/docs/models/gpt-6.1-sol).

No CK3 or mod files were changed.
