# AI token accounting

T-002 provides an offline helper and historical per-model `AI cost` tables.
Usage is measured in tokens, not currency, subscription usage or quota.
Historical tables have partial coverage: ambiguous work stays unallocated and
missing counters are `N/A`, not zero. This document preserves the accepted
method and the proposed close-time workflow. Agent instructions are unchanged.

## Current helper

`scripts/task_ai_cost.py` has two commands:

```sh
python3 scripts/task_ai_cost.py account \
  --mapping .codex-sync/task-usage-mapping.json \
  --output .codex-sync/task-usage-result.json

python3 scripts/task_ai_cost.py preview \
  --body .codex-sync/issue-body.txt \
  --fragment .codex-sync/ai-cost-fragment.md \
  --expected-sha256 "<SHA-256 of the exact UTF-8 issue body>" \
  --output .codex-sync/issue-preview.txt
```

Inputs and generated evidence stay private under ignored `.codex-sync/`.
The helper does not discover sessions, establish task ownership, generate a
mapping automatically or publish to GitHub. Output must be distinct from
every input, including through symlinks and hardlinks. Existing distinct output
files may be replaced. There is no hostile concurrent-path-replacement defense.

The private mapping has `version: 1`, a `cutoff` label, `sources` and
`assignments`. Each source declares its local `path`, owning `thread`, frozen
`size_bytes`, prefix `sha256` and optional `mode` (`responses` by default or
`cumulative`). Each assignment declares the zero-based `source` index, exact
`turn` and `tasks` array. Only a single-task assignment is allocated. Keep
identifiers, source paths and assignment evidence out of public documents.
All frozen source intervals must end on a complete JSONL line; later appends
are excluded. The supplied cutoff label must honestly describe those intervals.

## Counting and table semantics

- Prefer own `token_usage_record` response counters. Deduplicate response IDs
  across sources, omit inherited parent records in child files, reject
  conflicting duplicate usage and preserve unknown model context explicitly.
  Do not add cumulative or last-event counters to response totals.
- In explicit cumulative fallback mode, the first reading is a baseline.
  Difference each available field independently. A core counter decrease starts
  a fresh baseline; missing or reset optional details remain unknown. Deltas
  across turn/model boundaries are recorded without allocating them to a task.
  Hidden resets cannot always be detected. Missing totals are not inferred.
- Cached input and reasoning output are subsets where recorded, not extra
  addends. Uncached input is input minus cached input only when both are known.
  Total is input plus output where all are recorded and reconcile. Unknown
  component coverage remains unknown when records are aggregated.
- The table contains actual model IDs, input, cached/uncached input, output,
  reasoning output, a reconciled total and coverage. Additional cache-write or
  other categories need recorded counters and established semantics.

The current fragment renderer labels measured historical values `partial`.
It does not prove complete historical coverage. With no measured models it
renders unavailable values rather than zeros. Source IDs and audit records in
the accounting result are private; only aggregate fragments may be published.

## Managed description suffix

The `AI cost` fragment is the final managed section, bounded by
`<!-- ai-cost:start -->` and `<!-- ai-cost:end -->`. Preserve existing body bytes
outside that suffix. Preview verifies the expected body hash, appends the
section once or replaces only its previous suffix, and refuses malformed,
duplicate or non-final markers. Repeating an identical update is idempotent.

Before an authorized GitHub update, verify repository, exact issue, current
state and current body; compare again immediately before writing and read back
the exact expected body and unchanged disposition afterward. Keep private
original-body hashes and receipts. Read back uncertain writes before retrying.
An intervening remote race remains possible without atomic compare-and-swap.
Publication permission and Git staging/commit/push permission are separate.

## Proposed close-time agent configuration — unapplied

The proposed instruction is:

> At task finalization, run a finite AI-cost checkpoint using a private
> task/turn ledger, frozen source intervals, an aggregate-only preview and
> authorized publication. State incomplete final-turn coverage. Accounting
> maintenance does not trigger recursive updates.

The coordinator would maintain the private ledger from pickup, recording the
task, handoff, turn boundaries, actual model context and GUI/CLI/review roles,
including failed attempts and retries. A task-ID mention is insufficient to
assign a whole shared session. Linked child reviews use their own response
counters rather than parent totals or inherited history.

After substantive work and review, the coordinator would invoke the helper,
inspect coverage and privacy, preview the managed suffix and publish it under
the existing target-specific authorization. Mirror it to the canonical task
only when no active handoff owns or depends on that file.

A CLI's last response is measurable after it finishes. The next independent
GUI receipt can include that completed response and completed review turns
through a new explicit cutoff. Later accounting/publication overhead belongs
to a maintenance bucket, avoiding an endless cycle of recalculations. New
substantive work is reconciled at a later independent checkpoint. Never claim
an absolute final total when work after the cutoff is still missing.

This proposal is an instruction-driven checkpoint. Source discovery,
attribution, invocation, privacy review and publication remain coordinated
manually. No runtime close hook, watcher or automatic publication is installed.

## Validation and historical result

The accepted helper passes 27 offline tests, including real CLI checks for
cumulative missing fields, resets and model/turn boundaries; duplicate/fork
accounting; suffix preservation/idempotence; and direct, symlink and hardlink
input-alias rejection. Tests use disposable synthetic inputs.

GUI independently recomputed all 3006 historical records from 72 frozen source
intervals with exact equality to the earlier result. Eleven closed issue
descriptions were verified and ten canonical task mirrors integrated. The
historical subtotal is 136,940,642 measured tokens, with partial coverage for
every task. T-002's own table is an earlier partial snapshot, excluding later
execution, corrections and review; it is not a full-task cost.
