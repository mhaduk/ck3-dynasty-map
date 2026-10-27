# T-002 — Per-task AI token accounting

Selected by the user on 2026-10-22. Status: COMPLETE locally — historical
backfill, corrected helper, GUI review and automation proposal accepted.
Configuration activation and remote Issue #24 closure are outside this
completed stage. Scoped Git staging, commit and push were separately authorized
by the user on 2026-10-22.
Tracking: [T-002 / #24](https://github.com/mhaduk/ck3-dynasty-map/issues/24).

## Goal and routing

Append a consistent `AI cost` section to the end of closed task descriptions,
using locally recorded session usage and a breakdown by actual model. Backfill
the existing closed tasks first, then propose agent/workflow changes that would
maintain this section automatically at task closure. This stage proposes those
configuration changes; it does not activate them.

GUI owns scope, dispatch and review. CLI owns bounded log analysis, an offline
accounting helper, backfill and the automation proposal. Recommended profile:
Sol / Medium for attribution and accounting design; actual model must be
reported only when known. No CK3 app-state prerequisite or user game action.
Other chats retain their independently authorized scope. T-002 grants no
game, launcher, process, mod, installation or F-001 work.

## Frozen backfill inventory

Verified closed on GitHub on 2026-10-22 in `mhaduk/ck3-dynasty-map`:

| Issue | Task | Disposition |
|---|---|---|
| #1 | R-001 | Completed |
| #2 | R-002 | Completed |
| #3 | R-003 | Completed |
| #4 | R-004 | Completed |
| #6 | R-006 | Completed |
| #14 | R-014 | Completed |
| #15 | R-015 | Not planned; account for work actually performed |
| #16 | R-016 | Completed research with limits |
| #17 | Community standards/license chore; no stable planning ID | Completed |
| #19 | R-017 | Completed |
| #23 | T-001 | Completed |

F-003 / #22 is still OPEN remotely despite the accepted local specification;
report that discrepancy without changing its state or backfilling this batch.
T-002 itself is not yet closed and is outside this historical inventory.

## Required accounting contract

- Use measured local counters where available. Separate measured, partial,
  estimated and unavailable results; missing evidence is `N/A`, never zero.
  Estimates require a stated method/range and must not masquerade as counters.
- Attribute GUI, CLI, review, failed attempts, retries and child sessions when
  supported by evidence. A task ID mention alone is insufficient attribution.
  Split multi-task sessions by evidenced turn/event boundaries; do not charge
  a whole shared session to each task. Leave ambiguous usage unallocated and
  report it. Preserve actual model IDs, including unknown model buckets.
- Validate the actual installed log schema. Do not assume API field semantics
  exactly match Codex counters. Deduplicate repeated/cumulative usage events,
  forks and parent/child records; handle counter resets and model changes.
- Minimum table: model, input total, cached input (subset), uncached input
  (only if derivable), output total, reasoning output (subset if recorded),
  total tokens and evidence coverage. Add cache-write or other categories only
  when the logs support their semantics; expose unsupported categories as N/A.
  Do not add subsets again into totals. Include a reconciled total row.
- End each description with the same managed `## AI cost` fragment, a short
  method/version, evidence cutoff date and completeness/attribution limits.
  Use stable section markers so reruns replace the fragment exactly once.
  Public content contains aggregates only, never raw logs, prompt text, local
  paths, private session IDs, account identifiers or credentials.
- This is token accounting, not a currency invoice or a subscription/quota
  measurement. No monetary estimate or pricing lookup is required.

Official semantic references (local schema remains decisive):
[prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
and [reasoning usage](https://developers.openai.com/api/docs/guides/reasoning).

## Deliverables and acceptance

1. A bounded read-only discovery of relevant local session records and a
   private attribution manifest, with fixed byte/event cutoffs for live logs.
   Do not ingest unrelated project conversations or modify source logs/DBs.
2. A reusable offline helper with a preview mode, explicit task/session mapping,
   reproducible totals and synthetic regression tests for accounting traps.
3. A sanitized `AI cost` fragment at the end of each of the eleven closed issue
   descriptions; prepare mirrors for the ten existing canonical task records.
   Apply a mirror only where no active handoff depends on or owns that file;
   otherwise return an unapplied fragment for GUI integration after receipt.
   Issue #17 has no canonical task file; keep its mapping in the private report.
   Preserve all prior description text and task/issue dispositions.
4. A private receipt per remote write and a coverage report distinguishing
   complete, partial, ambiguous and missing evidence. No invented historical
   numbers. Missing historical counters can be a complete negative finding;
   failed publication must be reported as incomplete, not successful backfill.
5. A concrete, unapplied configuration/workflow proposal and patch explaining
   attribution capture, close-time preview/update, permissions, retries,
   idempotence and final-turn/review usage reconciliation. Include how its own
   accounting work and late-arriving usage would be handled without recursion.
6. GUI reviews actual changes, totals, limits and the proposal before parent
   completion. CLI completion does not close T-002 or enable automation.

## Permissions and parallel ownership

The user's request authorizes creation of this tracking task and the described
historical description updates. CLI GitHub writes are restricted to `AI cost`
fragments on the eleven enumerated closed issues, with repository/target/state
verification before each write and readback afterward. Do not alter titles,
comments, labels, other body text or issue state. No other GitHub writes.
At CLI dispatch, Git staging, commit and push were excluded. The user later
authorized scoped publication of the accepted T-002 files; see the publication
record below. Other scopes remain excluded.

The named handoff `.codex-sync/tasks/T-002/` freezes exact editable files,
initial dirty bytes, checks and immutable inputs. CLI is the sole writer for
its outputs; GUI does not edit them while it runs. Canonical historical records
are returned as unapplied fragments in this handoff to avoid changing inputs
of other concurrent chats. AGENTS/workflow changes are
proposal-only. Preserve unrelated F-001/F-004/probe work and earlier handoffs.

## Dispatch observation and recovery

The existing per-ID workflow supports this bounded background CLI job while
GUI can coordinate nonoverlapping work. Unknown: historical attribution and
counter coverage, to be resolved by CLI rather than repeated GUI log research.
Cheapest decisive check is one attributed task/event sample followed by the
frozen inventory. Stop dependent writes on ambiguous ownership/body drift;
finish independent coverage and proposal work.

Preparation recovered an invalid optional directory search, an oversized read,
a sandbox network failure and a connector argument-binding error by narrowing
reads and using the documented GitHub CLI with network access. A shared-state
patch was rejected because another chat concurrently resumed F-001; no shared
file was overwritten. T-002 therefore uses its named task/status as authority
and defers shared CURRENT_STATE/BACKLOG integration. Improvement: preflight
exact directories, request compact inventory fields and keep dispatch records
separate when another chat owns shared operational files.

## GUI review — 2026-10-22

GUI independently passed the 18 supplied tests, reproduced the accounting
result from all 3006 frozen records and verified all eleven current GitHub
descriptions against the exact previews and closed dispositions. The historical
subtotal is 136,940,642 measured tokens; coverage is partial for every target.
All ten canonical mirror source hashes match; mirrors remain unapplied.

GUI reproduced two missing regressions with disposable synthetic files:
cumulative mode discards known input/output/total deltas when optional cache
or reasoning details are absent, and an output hardlink to a source bypasses
alias protection and overwrites that source. No real source was damaged and
the historical response-mode figures are unaffected. The first receipt was
consumed with CHANGES REQUIRED; it does not accept the helper or close T-002.

T-002-FIX is the bounded CLI correction, recommended Sol / Medium. Preserve
published tables and earlier evidence, add regression coverage, and reproduce
unchanged historical totals before GUI acceptance. Shared operational files
remain with the concurrent F-001 coordinator. Automation remains an unapplied
proposal: an instruction-driven finite checkpoint, with attribution and
publication still manually coordinated; no runtime hook is implemented.

Self-healing: supplied passing tests missed missing-detail behavior in one
supported accounting mode and filesystem identity aliases. Test read-only
guarantees with real disposable files and optional-field loss in every mode.


## Final disposition — 2026-10-22

GUI accepted T-002-FIX after independently rerunning all 27 offline tests and
reviewing the actual correction. Direct, symlink and hardlink output aliases
are refused before writing. Known cumulative deltas survive absent optional
cache/reasoning fields; unknown details remain N/A. Conservative baseline,
reset and turn/model-boundary limits remain documented.

The full 3006-record, 72-source recomputation is byte-identical to the frozen
historical artifact. Eleven closed GitHub descriptions were independently
verified during the first receipt; correction work made no remote changes.
The 136,940,642-token historical subtotal is measured partial coverage, not a
full cost estimate. Ten exact mirror fragments were integrated after checking
source hashes and confirming no active handoff owns or depends on those files.
Issue #17 has no separate canonical planning record. F-003 / #22 remains
outside the historical batch. Both the rejected first result and corrected
acceptance receipt are preserved privately.

The proposal adds a private task/turn attribution ledger and a finite
accounting/preview/publication checkpoint to task finalization. It handles
late CLI/review turns and separates accounting maintenance to avoid recursive
updates. It is an instruction-driven checkpoint proposal, not an implemented
runtime hook. AGENTS and CODEX_WORKFLOW remain unchanged. Implementation and
review performed no automation activation, game/launcher work, Git publication
or #24 closure. Scoped Git publication was authorized afterward. Existing
F-001 work remains unchanged.

The table below is only the early frozen T-002 snapshot. It excludes subsequent
execution, correction, final CLI responses and GUI review/integration. No full
T-002 cost or savings is claimed. A later independently requested checkpoint
can reconcile completed work through a new explicit cutoff.

Self-healing: CLI recovered portable-filesystem-test and directory-precondition
errors; GUI independently verified the final result. Final documentation
preparation stopped before any writes because a broad key-pattern check
matched the method name, then recovered by inspecting the aggregate fragment
and narrowing the pattern. Retain targeted real-CLI alias/optional-counter
regressions and contextual privacy review; no extra global rule is needed.

## Scoped publication — 2026-10-22

The user authorized documentation, saving, staging, commit and push of this
accepted task. Publication includes the helper, tests, this canonical record,
ten historical table mirrors, T-002 tracking entries and the reusable
[accounting method and unapplied configuration proposal](../AI_COST_ACCOUNTING.md).
Shared tracking files are staged with only T-002 additions; unrelated F-001,
F-004 and probe changes stay in the working tree. Private manifests, session
records, original issue bodies and review receipts remain ignored.

Privacy and exact staged-diff review precede the commit. Publication uses the
existing branch with an ordinary push; no force push, configuration activation
or Issue #24 closure is included. The verified commit/ref receipt is retained
locally and reported after push; this record does not claim an unverified push.

<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| codex-auto-review | 130736 | 107136 | 23600 | 802 | 442 | 131538 | partial |
| gpt-6.1-sol | 1757068 | 1642368 | 114700 | 13680 | 2473 | 1770748 | partial |
| **Total** | 1887804 | 1749504 | 138300 | 14482 | 2915 | 1902286 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-22T13:15:22Z. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
Coverage is partial: early T-002 preparation/execution snapshot only. Later CLI work, T-002-FIX and GUI review/integration are outside this cutoff. No full-task total, currency cost or quota inference. Local table only; open issue #24 was not updated.
<!-- ai-cost:end -->
