# T-020 — Visible GUI-to-CLI execution plan

Complete — GUI accepted the implementation and its documentation correction on
2026-10-25. Tracking: [issue #46](https://github.com/mhaduk/ck3-dynasty-map/issues/46).

## Delivered behavior

Planned GUI → CLI handoffs retain the five established table rows and append one
`Plan of execution` row with 1–10 concise bullets in its value cell. The combined
T-012 tokens/messages row and time/step presentation remain intact. GUI authors
the summary during existing preparation and freezes it with the task; no extra
model turn, CLI execution cycle or mandatory confirmation is introduced.

The additive formatter uses the existing execution plan. Summary text maps to
ordered milestone IDs and an exact canonical-plan fingerprint; every milestone
is covered once in order. Plans above ten milestones require meaningful authored
grouping. Changed plans reject stale summaries. Planless legacy handoffs remain
valid. CLI authority, T-003 progress state, amendments and completion gates are
unchanged. Structural checks do not establish semantic quality; GUI reviews it.

## Validation and review

GUI independently reran 54 handoff/context tests successfully. Synthetic examples
cover one, five and twelve grouped milestones, legacy five-row rendering, stale
summary rejection, ordered coverage, the ten-bullet limit and cell escaping.
Whitespace and actual non-null output hashes were verified. No CK3 test or
product change was required.

The original CLI receipt is preserved as CONSUMED / CHANGES REQUIRED: AGENTS.md
still mandated five rows, and telemetry instructions called that row last. GUI
corrected both directly, reviewed the final bytes and separately accepted them.
CLI also recovered an omitted claim revision and an unwritable compiler-cache
path; it retried using the persisted revision and an approved temporary cache.
Reusable instruction: review active top-level instructions together with templates,
and preserve exact result grammar and file-hash checks during workflow edits.

CLI claim-to-complete wall time was 3.57 minutes against a displayed prior-based
10–30-minute estimate (raw 30–60). This candidate remains subject to comparability
review; one observation is not a new calibration or a compute-time claim.

## Publication scope

The user authorized scoped documentation, issue/Wiki updates, commit and push.
Private handoffs, raw accounting evidence and snapshots stay outside Git.
Aggregate-only T-012 history is included. No game/launcher action, mod change,
or unrelated classification repair is part of this task.

## AI costs

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6.1-sol | 1533611 | 1473408 | 60203 | 5379 | 1538990 | $0.32153680 |
| gpt-6-luna | 3194146 | 3123200 | 70946 | 18446 | 3212592 | $0.04754960 |
| **Total** | 4727757 | 4596608 | 131149 | 23825 | 4751582 | $0.36908640 |

[GUI context history](https://github.com/mhaduk/ck3-dynasty-map/blob/research/native-menu-alternative/docs/telemetry/gui-context/T-020.jsonl)

Partial measured coverage: 78 deduplicated response counters from one saved GUI session
and one CLI session, independently recomputed with exact agreement. Frozen cutoff:
2026-10-24T22:37:32.937Z (2026-10-25 00:37:32 Warsaw). Includes initial T-020
planning, delegation, implementation and GUI review/correction. Excludes intervening
repository reconciliation turns and this later accounting/documentation/publication.
Same-day metadata inventory found one GUI-linked guardian session solely for the
excluded reconciliation; no T-020-linked guardian source was found. Missing review
usage is N/A, not zero. Raw sessions, turn assignments and hashes remain private.

Standard API-equivalent prices checked 2026-10-25: per million uncached/cached/output
tokens, gpt-6.1-sol $2/$0.10/$10 and gpt-6-luna $0.10/$0.01/$0.50, from
[official OpenAI API pricing](https://developers.openai.com/api/docs/pricing).
All measured requests were below 272K input (maximum 105,123); short-context rates
apply. Cached input is a subset; reasoning is already included in Output. No
nonzero cache-write counter was observed; service-tier adjustments are not inferred.
Both measured models are priced. This is partial known API-equivalent cost,
not subscription spending or an invoice.
