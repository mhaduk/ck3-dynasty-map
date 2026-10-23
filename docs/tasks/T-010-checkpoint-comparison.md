# T-010 — Finite checkpoint comparison

Status: **CLOSED — GUI accepted the corrected implementation and the completed record was published with issue #36 on 2026-10-23.**
Research is accepted/consumed. Both original EXECUTE and CLI correction remain
consumed CHANGES REQUIRED with original bytes preserved; GUI accepted the final
small dependency-guard correction separately. The initial local checkpoint
preceded this separately authorized publication; no live capture or F-001
continuation occurred. Predecessors:
[T-008](T-008-workflow-optimization.md) and
[T-009](T-009-structured-preflight.md).

## Why this area next

The earlier seven-candidate analysis rated finite log profiles/comparison as
potentially valuable, with substantial attribution risk. Historical audit and
counter-diagnosis receipts repeatedly assembled interval/reset gaps, pins,
observed messages and counts manually. T-008 now provides inventory integrity
and selected statuses; T-009 adds structured preflight evidence. The next useful
question is what changed between two explicitly named finite checkpoints.

Choose a narrow read-only comparison before broader profiles. Current
ck3_log_delta.py already reports interval/expectation/observation states,
checkpoint and baseline IDs, captured byte counts and error summaries. Reuse
those contracts rather than build another log parser. Actual maintenance cost,
frequency and savings remain unmeasured; this is a qualitative prioritization.
Full semantic stage-chain validation is deferred because deployment receipt
and payload identity contracts still need separate scope. Deployment/rollback
remains a distinct higher-risk permission class.

## Proposed minimal iteration

Compare exactly two explicitly pinned saved checkpoint manifests/reports.
Do not open or parse raw logs in the first iteration. Report each input's
original completeness, IDs and limits, then separate:

- newly captured byte ranges, only when boundaries/generation are comparable;
- observed message identity, only to the extent the existing summary preserves
  an adequate identity; matching counts alone do not establish identity;
- per-message or aggregate count differences with their scope/comparability;
- causal attribution, always UNPROVEN by this file comparison.

Missing fields, resets, partial lines, truncation, caps, optional gaps,
unsupported formats and uncertain generation/identity must stay visible. A
missing or filtered message is UNKNOWN, not proof of disappearance. Never
subtract unequal windows and call the result new errors, nor promote source
INCOMPLETE to a clean comparison. Prefer partial useful observations plus
explicit non-comparability over inventing a universal verdict.

## Preparation and tests to freeze before EXECUTE

Use one bounded CLI contract review over named current log helper/tests,
inventory guide and two copied small saved manifest examples. GUI chooses
exact supported fields, identity/comparability rules and the smallest output
contract from that evidence. If summaries lack a reliable field, mark it
UNKNOWN or return the gap; do not expand automatically into raw-log analysis,
normalization, live capture or a new profile framework.

Future synthetic cases must include comparable adjacent and overlapping
windows, unrelated baselines/generations, reset/truncation, complete versus
required/optional gaps, same message with changed count, different messages
with equal counts, absent/filtered identity, unknown schema, stale pins and
privacy sentinels. Exact expected non-claims and preservation of upstream
verdicts are acceptance criteria. Retain existing helper/report regressions;
public-only tests cannot depend on ignored historical artifacts.

## Routing, permissions and stop conditions

GUI owns scope, comparability semantics, trade-offs and acceptance. Recommend
Luna / Medium for bounded evidence collection and any subsequently approved
implementation; runtime selection must be confirmed separately. A future
EXECUTE needs a new frozen per-ID handoff with exact inputs, owned paths,
checks and GUI-supplied execution plan. No worker starts from this plan.

Offline named manifests only; no raw logs, save/dump, real game/app/process/UI,
new capture, install/rollback, repair/repin/migration, automatic discovery,
publication or external message. Do not copy raw message text or machine paths
into public output; freeze a sanitized allowlist. F-001 remains paused.
If identity/generation cannot be established from supplied metadata, stop the
dependent comparison and return UNKNOWN/evidence needed, without inventing a
fixture pass or requesting another game test. No completion/accounting claim.

## Evidence and recovery lesson

Basis: accepted T-008 candidate analysis and repeated reset/pin/count work in
its named historical examples, plus the current helper's explicit summary
fields. T-009 review also showed that passing happy-path tests missed combined
incomplete/defect and malformed-type cases. Include these negative combinations
at initial scope freeze. Short GUI planning avoids a redundant research cycle;
exact schema/comparability verification remains the next bounded CLI stage.

## Initial CLI scope — 2026-10-23

Review the current log-delta producer/tests and accepted inventory adapter/guide
against exactly two copied historical format-1 manifests (startup append and
load delta). Copies and provenance stay private; no raw logs or live inputs.
Separate observed byte boundaries, possible content identity and count changes,
with an explicit matrix of support/unknowns. A historical example does not
prove a generation or authorize another F-001 action.

Return a compact field/claim map, minimum implementation recommendation,
proposed versioned input/output contract, acceptance tests and exact GUI
decisions needed. Include combined incomplete/defect cases and malformed
field types learned from T-009. No source edits, fixture implementation, helper
runs against real data, new checkpoint or public evidence copy. A separate
approved EXECUTE follows only after GUI selects the contract.

## GUI contract selection — 2026-10-23

Producer/source review confirms that format-1 deltas omit baseline file
identity/generation evidence. The copied startup manifest is INCOMPLETE with
required truncation; the load manifest is COMPLETE with 404 analyzed error
lines and 15 retained global fingerprints. Different baseline tokens and
labels/times do not establish continuity. Research is accepted; no earlier
gap is repaired by the later complete interval.

Select a private JSON-only comparison of exactly two explicitly pinned
format-1 manifests: literal source summaries, declared numeric range geometry
and digest-field equality, retained global fingerprint membership, side-by-side
counts and explicit coverage. Generation/continuity stay UNKNOWN; new-byte and
count-delta fields stay null; event identity/causality remain UNPROVEN. No caller
generation assertion, subtraction into new errors, raw-log reads, producer
change or new inventory adapter. A structurally complete metadata comparison
can contain an INCOMPLETE source; its exit/status never upgrades that source.

Separate EXECUTE freezes field/privacy allowlists, byte/count/schema limits,
path/pin/no-overwrite protections, negative/combined tests and public-only
portability. Initial implementation files are a small comparison CLI, tests
and guide, reusing unchanged inventory validation helpers. GUI reviews the
actual results before parent acceptance/accounting.

Research recovery: CLI initially ended after claim/start without doing the
analysis; the same owner/revision resumed without reset. Later admin/output
path confusion was corrected and provenance rechecked. Use exact STATUS owned
paths and continue through the complete gate before reporting completion.

## Bounded implementation — 2026-10-23

GUI-frozen EXECUTE scope is implemented in `scripts/ck3_log_compare.py` with
focused subprocess tests and the [usage guide](../CHECKPOINT_COMPARISON.md).
The CLI requires exactly two explicit byte/hash pins, uses the unchanged
`evidence_report.py` safe path/JSON helpers, reads only the two manifest files,
and writes deterministic reports exclusively below `.codex-sync/` with mode
0600. Captured log paths and message text are ignored. Declared offset geometry,
digest-field equality, side-by-side scoped counts and retained-summary
membership are reported separately; invalid summaries have unknown overlap.
Generation/continuity remain UNKNOWN, new-byte/count-delta fields null, and
event identity/causality UNPROVEN. No aggregate PASS is emitted.

The copied startup-append/load-delta smoke returned exit 0 with metadata
COMPLETE and no structural issues while preserving source statuses INCOMPLETE
and COMPLETE. Summary coverage is PARTIAL and COMPLETE respectively. The new
synthetic CLI suite covers range geometry and symmetry, empty ranges, source
gaps, combined source incompleteness and summary inconsistency, pin drift,
malformed types/duplicate keys/fingerprints, symlinks/outside paths, exclusive
output, privacy sentinels, input immutability, determinism, and a public-only
CLI run. Exact regression and isolated-tree results are in the private
implementation dossier. This is file-level structural metadata only; GUI
acceptance remains pending.

## Initial implementation review — changes required, 2026-10-23

GUI reran 19 focused tests and reproduced two frozen-contract failures. A
list-valued partial-line flag emits an issue but still permits range_valid,
IDENTICAL geometry and COMPLETE summary coverage. Correctly pinned malformed
source JSON exits 1 without a report instead of producing INCOMPLETE/exit 2.
Original outputs are preserved; initial EXECUTE is consumed CHANGES REQUIRED.
A separate correction `T010-FIX-20261023-03` must block clean dependent
observations on invalid flags and distinguish source-parse from envelope
errors while retaining the safe peer. No architecture/scope expansion.

Recovery lesson: combine invalid coverage flags with apparently equal ranges,
and test malformed source versus envelope at the actual CLI boundary.
Parent acceptance/accounting remain pending. No Git/runtime/publication action.

## Bounded correction execution — 2026-10-23

`T010-FIX-20261023-03` corrects the two frozen repros without changing the
comparison architecture. Invalid selected source-row or per-log analysis
fragment flags now leave dependent declared range/digest relations `UNKNOWN`
and summary coverage `UNKNOWN`; they are omitted from the safe projection.
Absent optional source-row flags keep their producer-defined false default,
and recognized true gaps remain `PARTIAL`. Missing/invalid selected state,
required, analysis, and source status metadata cannot produce clean summary
coverage. Correctly pinned source JSON decoding, finite-number, nesting and
bounded-collection failures now produce a finite `invalid_source_json` issue,
metadata `INCOMPLETE`, and exit 2 while retaining the independently valid
peer. Envelope failures remain exit 1 with no report. Detailed commands,
test evidence and recovered command/path errors are in the private correction
dossier; GUI review and parent acceptance/accounting remain pending.

## Final GUI acceptance — 2026-10-23

The private saved-manifest comparison is accepted locally. It checks explicit
pins and selected metadata, retains source statuses, compares declared numeric
ranges/hash fields and retained global fingerprints, and presents count
context. Generation/continuity remain UNKNOWN; new-byte/count-delta/new-error
fields remain null; event identity and causality remain UNPROVEN. No raw-log
read or source-helper change is required. Structural metadata COMPLETE never
upgrades an INCOMPLETE source or proves a clean run.

GUI independently reran 23 CLI-corrected tests. It then found the same
dependency gap when the entire per-log analysis collection/row was missing or
malformed. Three small range-invalidating guards and one regression matrix
covering both roles/five missing-or-invalid forms were applied directly under
the small-edit exception. All final 24 tests pass independently and in a fresh
public-only isolated tree. The two original flag/parser regressions are
covered; a correctly pinned malformed source writes INCOMPLETE/exit 2 while
invalid envelopes remain exit 1 without output. Valid peer metadata survives.
CLI evidence records 29 inventory and 15 log-delta regression tests passing,
plus saved-example and guide smokes. The helper bytes remain unchanged.

Original receipts and original/final accepted outputs are preserved privately.
The correction receipt is consumed CHANGES REQUIRED rather than rewriting its
output hashes to claim it delivered GUI fixes. The separate GUI acceptance
record pins final source/test bytes. Tool-path, dossier-placement, temporary
alias, revision and test-fixture failures were recovered as documented in CLI
records; premature pickup-only completion resumed with the original owner and
revision. Reusable lesson: test unavailable whole structures as well as invalid
scalars, and require known-clean dependencies before a positive comparison.
No new global instruction or framework was added.

## Saved-session accounting

One GUI session (five selected T-010 turns) and three CLI sessions (four turns,
including premature pickup and explicit resume) were checked. Runtime records
confirm Sol in GUI and Luna in CLI. Existing accounting helper and independent
response-ID sum agree on 215 responses and 22,167,566 total tokens. Private
frozen sources/hashes and exact assignments remain local. Six same-day review
sources were checked by parent/root-turn linkage; none matched selected turns.
The initial plan was mixed with the T-009 commit turn and remains unallocated.
Coverage is partial; later accounting, documentation integration and final
message are excluded by the finite cutoff, without recursive extension.

Known measured token cost is approximately **$1.76 API-equivalent**: Sol
$1.5259968 and Luna $0.2382361, sum $1.7642329 before rounding. This is not
subscription spending. Same-day verified Standard reference rates were reused:
Sol uncached/cached/output $2/$0.10/$10 per million and Luna $0.10/$0.01/$0.50.
Fourteen recorded requests exceed 272,000 input tokens; Sol long-context rates
(2x input/cache, 1.5x output) were applied per request, not to aggregate totals.
Maximum request input is 298,631 tokens; recorded cache-write input is zero.
Actual processing tier, regional charges, tool costs and unobserved usage are
not established. Sources: [official pricing](https://developers.openai.com/api/docs/pricing?latest-pricing-expanded=true)
and [Sol context pricing](https://developers.openai.com/api/docs/models/gpt-6.1-sol),
checked on 2026-10-23. Unknown usage is not zero.

<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| gpt-6-luna | 14933989 | 14526720 | 407269 | 104484 | 42687 | 15038473 | partial |
| gpt-6.1-sol | 7103557 | 7071232 | 32325 | 25536 | 6346 | 7129093 | partial |
| **Total** | 22037546 | 21597952 | 439594 | 130020 | 49033 | 22167566 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-23T19:06:57.266616+00:00. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
Partial measured coverage: five task-specific GUI turns in one session, four CLI turns in three sessions including premature pickup and resume. 215 own response IDs deduplicated; independent sum agrees. Preliminary mixed T-009 commit/planning turn unallocated; later accounting/integration/final response excluded. Six same-day linked review sources checked; no matching selected parent/root turn found. Missing usage is not zero.
<!-- ai-cost:end -->


## Publication and closure — 2026-10-23

Published completed record: [issue #36](https://github.com/mhaduk/ck3-dynasty-map/issues/36), closed after validation of the approved batch gates. Generation and continuity remain UNKNOWN, count/new-byte deltas remain null, and event causality remains UNPROVEN. Frozen measured usage is 22,167,566 tokens and $1.7642329 API-equivalent, partial coverage; long-context Sol pricing was applied request by request. Later shared closeout work is excluded. See the [Wiki AI-cost table](https://github.com/mhaduk/ck3-dynasty-map/wiki).
