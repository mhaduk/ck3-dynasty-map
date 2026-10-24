# GUI context estimate

The next ordinary GUI-to-CLI handoff can include a small estimate of the known
saved session text. It does not read the live GUI, request another model call,
interpret the measurement, recommend a rollover, or estimate actual active
model context or billing usage.

## Prepare a handoff

The coordinator supplies one explicit saved-session JSONL path and a stable
opaque identity for that local session. The identity is private and must be
reused only for that same session. During normal handoff preparation, run:

```sh
python3 scripts/gui_context.py \
  --session <explicit-saved-session-file> \
  --task T-012 \
  --handoff <public-delegation-ID> \
  --repository-ref <published-branch-or-commit> \
  --identity <stable-private-session-key> \
  --preview .codex-sync/gui-context-preview.json
```

Then pass the generated JSON to the ordinary `scripts/handoff.py create`
command as `--context-preview .codex-sync/gui-context-preview.json`. This adds
two diagnostic lines and a link to the task description before its frozen plan.
It does not add scope, alter the number of plan steps, or create another model
turn. In the user-facing handoff, show the measured values in the combined table
row, directly below `Estimated CLI time / steps`: `szacowane tokeny/wiadomości`
with value `<N> tokenów; <M> wiadomości`. Use `niedostępne` when unavailable.
This describes saved GUI-session text, not the full active model context. Omit the option if no explicit saved session is available.

The parser recognizes `response_item` message events with `user` or `assistant`
roles and text content blocks. It deduplicates repeated message IDs, ignores
tool calls, usage counters and other metadata as text, and reads at most 16 MiB.
It reports message count, characters, UTF-8 bytes, the latest recognized model
and reasoning level (`effort`, with `reasoning_effort` compatibility), and the source event timestamp when available. Missing
metadata is `null` / unknown.

The token figure is `ceil(known UTF-8 text bytes / 4)`, explicitly estimated.
It does not include everything that may have entered a model request: system
instructions, tool payloads, hidden input, truncation, compaction and other
runtime transformations may change active context. No error bound is claimed.
Per-request input counters remain usage telemetry and are never substituted for
active context size.

For planned receipts, append a sixth `Plan of execution` row after the five
standard rows with `handoff.render_handoff_table(rows, plan, summary)`. Author
the concise summary during the existing preparation pass; store its canonical
plan fingerprint and ordered milestone-ID groups with `create --plan-summary`.
Use at most ten bullets and group plans above ten milestones explicitly. A
fingerprint mismatch or incomplete/reordered IDs fails closed. Planless older
receipts continue to render their original five rows.

## History and privacy

One aggregate JSONL history is created at
`docs/telemetry/gui-context/<parent-ID>.jsonl` only after an actual measurement.
It contains the task ID, handoff ID and sequence, measurement timestamp and heuristic provenance, aggregate counts,
estimated token count, delta state/reason, recognized model/reasoning metadata,
source timestamp and a provenance label. It contains no message text, session
identity, source path or source hash. A repository link is added below the
canonical AI-cost table in an offline Issue-body preview only when the history
contains a real measurement. Publication and readback remain a later, separately
authorized closeout action.

`.codex-sync/gui-context-private.json` keeps the hashed session identity, source
path/hash, byte cursor, prefix hash and prior aggregate needed to decide whether
a delta is safe. Keep this file private and out of Git. A delta is unknown after
a session identity or method change, a file reset, or a rewrite/compaction before
the prior cursor. Repeating an unchanged measurement for the same handoff is idempotent and regenerates its preview. Distinct handoffs with unchanged text record zero growth. Deltas follow the same saved session across parent tasks; unrelated sessions remain unknown. Run one coordinator writer at a time. Public history is hash-checked against private provenance; interrupted cross-file writes fail closed for coordinator recovery. A changed
history file, unsafe symlink, malformed JSON, or oversized input fails closed.

## Time estimate and progress display

For planned work, show the frozen milestone count in the handoff table. Use
comparable single-attempt estimate/claim-to-complete pairs when at least three
exist: take the median actual-to-estimate midpoint ratio, apply it to both range
endpoints, and round outward. Retain each pair and its source privately. With
fewer than three pairs, the user's 2–3× overestimate observation is only a prior;
divide the low estimate by 3 and the high estimate by 2, round outward, and say
that the result is prior-based. User waiting is not compute. Failed, retried,
interrupted and incomparable attempts are excluded. Planless handoffs retain the
ordinary uncalibrated range and say `no plan`.
At ordinary closeout, retain a candidate from the frozen estimate and
claim/completion timestamps with
`python3 scripts/gui_context.py --repo . --timing-task-id <ID>`. This operation
is idempotent and reads only that handoff's `CLI_TASK.md` and `STATUS.json`;
the recorded elapsed value is wall time and may include pauses, so GUI reviews
comparability before counting it.
Future candidates are retained in private
`.codex-sync/gui-context-calibration.json`, separate from the frozen T-012
sample snapshot.
After the coordinator marks at least three candidate pairs comparable, produce
a new handoff range with
`python3 scripts/gui_context.py --repo . --estimate-min <low> --estimate-max <high> --steps <plan-count>`.
The helper uses the median actual/estimate-midpoint ratio and reports the
observed ratio spread alongside the planned-step count. With fewer than three
reviewed pairs, it applies only the prior formula above.

Terminal progress uses a 30-cell Unicode bar, parent task ID, approximate
percentage and persisted human-readable stage. The bullet is green ANSI only
when stdout supports color and `NO_COLOR` is absent. Commentary uses the same
structure without ANSI. Progress remains milestone-based; it does not measure
elapsed time.

## Activation and validation

GUI review confirmed the current saved-session message schema and runtime `effort`
field using one explicitly identified GUI session. A private temporary-tree smoke
read 1,156,507 JSONL bytes in about 3.08 ms; it counted 11 known messages,
20,550 UTF-8 text bytes and about 5,138 estimated tokens. These are validation
figures, not a production history row or actual active model context. Temporary
history was removed. The first production row belongs to the next ordinary
handoff after activation; there is no historical context backfill.

Keep the raw uncalibrated range in `Estimated CLI time: <low>–<high> minutes`
in the frozen task, and the displayed calibrated time/steps separately. This
prevents recalibrating an already calibrated estimate. The T-012 execution
provides the first reviewed candidate: raw 15–25 minutes, 17 minutes 29 seconds
wall elapsed, five milestones. One pair cannot establish a measured factor.
Never represent the prior-adjusted 5–13 minute range as T-012's original estimate.

For history links pass the same published repository ref to measurement
`--repository-ref` and AI-cost preview `--repository-ref`. The default is `main`;
use the actual published branch when the history has not reached the default
branch. At closeout, no measurement means no fabricated link or history row.
