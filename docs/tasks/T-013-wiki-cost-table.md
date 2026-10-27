# T-013 — Simplify the Wiki AI-cost summary

Issue: [#34](https://github.com/mhaduk/ck3-dynasty-map/issues/34).

## Accepted result — 2026-10-25

The main Wiki AI-cost table has exactly five columns, a bold Total row and one short global caveat. Coverage and methodological headers are absent from this summary. Existing group order, accounting rules, historical values, detail rows and links are preserved. Authorized closeout adds T-013 as a new task to T; this separate addition explains the increase over the unchanged-baseline presentation preview ($92.62).

| Type | Closed tasks | Total tokens | Cached tokens | API cost |
|---|---:|---:|---:|---:|
| R | 15 | 106,527,859 | 102,845,824 | $15.38 |
| T | 13 | 145,843,895 | 141,268,224 | $12.93 |
| F | 3 | 545,740,537 | 531,023,616 | $64.72 |
| B | 0 | N/A | N/A | N/A |
| **Total** | **31** | **798,112,291** | **775,137,664** | **$93.04** |

Totals are approximate and based on measured usage; some historical tasks may have incomplete coverage.

The unchanged baseline known-cost sum was $92.61817258 (R $15.38251664, T $12.51234988, F $64.72330606). Adding T-013 $0.42056876 produces $93.03874134 before display rounding. Original group coverage/provenance remains in historical task records and the detailed Wiki table. B counters remain N/A; only known costs contribute to USD sums.

## Implementation and validation

- `scripts/wiki_cost_summary.py` renders supplied groups in their existing order and replaces only the main summary block. Decimal addition precedes rounding; wholly missing token totals remain N/A.
- `tests/test_wiki_cost_summary.py`: six focused tests pass, covering five columns, totals, N/A, extra groups/order, unique-group validation and detail preservation.
- GUI verified seven original output hashes, unrounded source amounts, exact unchanged group values and byte-identical content outside the summary. Current Wiki baseline: `c88955bafc2c21fd875d81803ab32871aa14518b`.
- Original CLI receipt consumed CHANGES REQUIRED; GUI independently accepted bounded corrections for additional groups, wholly missing counters and full Total emphasis. Original evidence retained privately; no historical evidence overwritten.
- User authorized scoped cleanup, issue/Wiki publication, commit and push. No CK3 changes or application operations.

## Recovery and reusable findings

CLI recovered an absent shell glob, incompatible type annotations, two rejected progress transitions and an incorrect ad hoc delimiter assertion; corrected searches, compatible annotations, persisted revisions and row-aware checks passed. GUI corrected an inaccurate F aggregate source reference: $64.72330606 is recorded directly in the frozen Wiki baseline; the F-002 canonical record contains its own task cost, not that aggregate. Use source-specific provenance and exercise extra-group/all-missing fixtures rather than only the current table. No additional project-wide rule is needed.

## AI costs

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6.1-sol | 1554067 | 1477120 | 76947 | 8716 | 1562783 | $0.38876600 |
| gpt-6-luna | 1864646 | 1790976 | 73670 | 13052 | 1877698 | $0.03180276 |
| **Total** | 3418713 | 3268096 | 150617 | 21768 | 3440481 | $0.42056876 |

[GUI context history](https://github.com/mhaduk/ck3-dynasty-map/blob/research/native-menu-alternative/docs/telemetry/gui-context/T-013.jsonl)

Partial measured coverage: 51 deduplicated responses from one saved GUI session and one CLI session; independently recomputed with exact agreement. Frozen cutoff: 2026-10-24T22:48:14.638Z (2026-10-25 Warsaw). Includes preparation, execution, GUI correction/review and initial closeout work; later accounting, documentation and publication are excluded. Same-day session-metadata search found no linked automatic-review session; missing review usage is N/A, not zero. Session inventory, snapshots, hashes and turn assignments remain private.

Standard API-equivalent prices checked 2026-10-25: per million uncached/cached/output tokens, gpt-6.1-sol $2/$0.10/$10 and gpt-6-luna $0.10/$0.01/$0.50; see [Sol pricing](https://developers.openai.com/api/docs/models/gpt-6.1-sol) and [Luna pricing](https://developers.openai.com/api/docs/models/gpt-6-luna). Maximum request input: 104,256, below 272K; short-context rates apply. Cached input is a subset; reasoning is included in Output. No nonzero cache-write counter was observed; service-tier, regional, tool and other invoice adjustments are not inferred. Both recorded models are priced; historical Wiki unpriced buckets remain unchanged. This is partial known API-equivalent cost, not subscription spending or an invoice.

## Publication receipt

Wiki commit `a835bda` publishes the compact Home summary and separate per-model cost page. Independent remote-clone readback matched both prepared pages. Issue #34 body and `ai-cost-table-format` label were read back and verified; issue closed completed. Canonical per-model table, arithmetic and limitations match the published body.

- ai-cost-table-format: PASS

Scoped repository publication is user-authorized. Private handoff evidence and accounting sources remain local; no unrelated changes are included.
