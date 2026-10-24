# T-012 — GUI context measurement, time estimates and progress

Status: COMPLETE — corrected implementation accepted by GUI, 2026-10-24.
User authorized scoped cleanup, issue/Wiki publication, closure, commit and push.

Source: [issue #33](https://github.com/mhaduk/ck3-dynasty-map/issues/33).
Guide: [GUI context](../GUI_CONTEXT.md).

## Accepted result

T-012 is accepted after independent GUI review and bounded local corrections.
The local helper estimates known saved user/assistant text as ceil(UTF-8 bytes / 4),
never active model context or billing input. Exact response usage remains separate.
Aggregate history is created only for subsequent normal handoffs, under
`docs/telemetry/gui-context/<parent>.jsonl`; source identity, paths, hashes and
cursors remain private. There is no context backfill, threshold or restart logic.

Normal handoff creation accepts two diagnostic lines without changing scope.
History records have handoff identity/sequence, heuristic provenance, timestamps,
counts and safe session deltas. Repeats regenerate previews; cross-task deltas
follow the same session. Tampered/incomplete history fails closed. One coordinator
writes at a time; interrupted cross-file writes require coordinator recovery.
The offline Issue preview places available history immediately below the AI-cost
Total row. The published ref is explicit. T-012 has no production history because
collection starts with the next normal handoff; no empty history link is invented.

Eight bounded historical timing candidates lacked original frozen ranges, so no
historical measured factor was inferred. The user-observed 2–3× prior is explicit;
future estimates use a median ratio only after three GUI-reviewed comparable
pairs. Raw and calibrated ranges are retained separately to avoid double
calibration. T-012 is the first reviewed pair: 15–25 minutes estimated,
17 minutes 29 seconds claim-to-complete, five steps. Its prior-adjusted 5–13
minute example was never the original estimate and is not a measured prediction.
Planless handoffs retain their uncalibrated range.

Terminal progress uses a green ANSI bullet for color-capable TTY output and the
same plain glyph otherwise, compact parent ID, proportional 30-cell Unicode bar,
approximate percentage and readable stage. T-007 semantics and completion gates,
T-006 decision authority and upstream evidence contracts remain intact.

```text
GUI session estimate: ~5,138 estimated tokens
GUI session: 11 messages / 20,550 UTF-8 bytes
Estimated CLI time / steps: 5–13 minutes / 5 steps (user-observation prior)
●  T-012 [███████████████░░░░░░░░░░░░░░░] ~50% — Weryfikacja zmian
```

The example matches the required layout; fill remains proportional to persisted
percentage. ANSI-disabled output uses the same line. Hidden/system input, tools,
truncation and compaction are excluded from saved text; no token error bound is
claimed. Sixteen MiB is the explicit session-read bound; larger sources fail
with an error rather than a truncated measurement. No token savings are claimed.

GUI independently reran 82 tests covering measurement, history/privacy, handoff,
Issue preview, time calibration, ANSI/fallback and existing lifecycle behavior.
A temporary-tree smoke confirmed the actual saved GUI schema, including runtime
`effort`: 1,156,507 bytes parsed in about 3.08 ms on one run. Temporary aggregates
were removed; production collection remains prospective. Zero additional model
calls/turns is a design property of the local mechanism.

The initial CLI result is preserved and consumed CHANGES REQUIRED; the GUI
separately accepted corrected bytes. Corrections added the actual effort field,
retry preview generation, history integrity, cross-parent deltas, cycle identity,
input alias protection, explicit published refs and planless estimate parity.
CLI runtime confirms gpt-6-luna / medium. No second CLI session was required.

Self-healing: CLI recovered a missing zsh glob, stopped an overbroad archive
search and narrowed timing reads to eight exact metadata pairs; temporary-root
path tests were corrected. GUI found the synthetic-only schema gap and exercised
one exact real source without adding production history. Future work should use
sanitized runtime schema fixtures, preserve raw estimate ranges at preparation,
and verify copied templates and real session fields before claiming integration.

## AI costs

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6-luna | 22860124 | 22621440 | 238684 | 90597 | 22950721 | $0.29538130 |
| gpt-6.1-sol | 1761477 | 1643392 | 118085 | 10209 | 1771686 | $0.5025992 |
| **Total** | 24621601 | 24264832 | 356769 | 100806 | 24722407 | $0.79798050 |

No production GUI-context history exists for T-012; collection starts at the next normal handoff.

Partial measured coverage through 2026-10-24T13:00:08.440Z: 178 deduplicated responses from one
saved GUI session (preparation and review) and one CLI session. The existing
accounting helper and an independent per-response sum match exactly. Later
review corrections, documentation, accounting/publication and Git work are
excluded from this frozen cutoff. Private source inventory, hashes, explicit
turn assignments and review-link checks are retained locally.

No parent-linked review source was found in the bounded same-day metadata
inventory (15 sessions, including three guardian sources); the exact separate
reviews directory was absent. Missing automatic-review counters are N/A, not
zero. Both observed models are priced; no unknown model mapping is invented.
All observed request inputs were below 272K (maximum 222,634); Standard short
rates apply. Cached input is a subset and reasoning is already included in
output; no nonzero cache-write counter was observed. Known-model total is
$0.79798050 API-equivalent, not subscription spending or actual invoiced API use.
Rates checked 2026-10-24: per million uncached/cached/output tokens, Sol
$2/$0.10/$10 and Luna $0.10/$0.01/$0.50, from
[official OpenAI API pricing](https://developers.openai.com/api/docs/pricing).
