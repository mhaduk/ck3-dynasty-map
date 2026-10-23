# T-008 — Workflow optimization after routing

Status: **CLOSED — GUI accepted the bounded offline evidence inventory on 2026-10-23; published with issue #32.** The original planned scope below is retained as dated history. Remaining candidates are mapped to [T-011](T-011-deferred-workflow-optimizations.md).

This record preserves the original plan and intermediate checkpoints. Current status: CLOSED after publication and closure of [issue #32](https://github.com/mhaduk/ck3-dynasty-map/issues/32); accepted implementation and its limitations are recorded below. Remaining optimization candidates stay deferred in [T-011](T-011-deferred-workflow-optimizations.md).

## Goal

Select and implement the smallest useful follow-up that reduces repeated
evidence assembly and review effort while preserving distinct upstream
verdicts, evidence limits, user-only CK3 operations, privacy and permission
boundaries. Start with a bounded read-only COLLECT / VERIFY / RESEARCH phase on
Luna, return findings/options/recommendation to GUI, and wait for GUI to choose
scope. Any EXECUTE phase requires a separate explicit handoff and permission.

## Candidate scope for fresh prioritization

1. Compact read-only evidence report over existing results, with explicit
   completeness/unknown fields and no synthesized green PASS.
2. Cross-stage link validation for payload → install receipt → checkpoint →
   marker/schema → analyzer, retaining upstream statuses and mismatches.
3. Log profiles and finite checkpoint comparisons, with careful separation of
   new bytes, known message identity, count changes and unproven causality.
4. Structured preflight result using a stable output contract rather than
   parsing free-form stdout.
5. Explicit manifests/pins for already named inputs; no broad discovery or
   automatic live fallback.
6. Append-only archive/compare and sanitized summaries without migrating old
   archives or publishing automatically.
7. Parametric deployment and verified file rollback, only under a separately
   approved install scope and user-declared safe app state.
8. Other T-006 recommendations that remain useful after routing, subject to
   evidence and fresh prioritization.

The analysis suggested a thin report/link-validation layer first, then log
profiles/comparison, with deployment as a higher-risk separate permission
class. This is historical qualitative advice, not a binding decision. Recheck
dependencies, qualitative value/effort, revalidation cost and exclusion risk
before selecting one minimal iteration.

## Exclusions and dependencies

- No game automation, engine safety verdicts, causal attribution, release
  stripping, broad scans, automatic repair, publication or unapproved writes.
- No AI-accounting ledger implementation; T-002's existing proposal remains
  deferred and requires its own authorization.
- Reuse `handoff.py`, log capture, classification analysis and preflight where
  relevant; do not duplicate their functions or change semantics implicitly.
- Preserve user-only launch/load/save/character switching/testing and existing
  ownership, provenance, privacy, compatibility and review guarantees.
- T-006 acceptance and accounting are prerequisites. Each selected
  implementation needs its own frozen inputs, owned paths, checks, permissions
  and GUI-supplied execution plan.

## Readiness criteria

T-008 can be scoped only when a new-session evidence review identifies a
specific repeated cost, a bounded candidate with named existing inputs,
acceptance cases that preserve upstream verdicts/unknowns, a privacy and
permission plan, and an explicit GUI choice of the first iteration. Keep
remaining candidates planned until separately selected.

## Initial GUI selection — 2026-10-23

The three named historical examples support repeated manual pin/status/gap
assembly. GUI independently checked decisive receipt/review excerpts and the
current log-delta/classifier producer contracts. No measured savings follow.
Select candidate 1 with only explicit integrity checks from candidate 2:
a finite manifest over named private files, deterministic JSON inventory,
limited projections of existing handoff/log-delta/classification statuses,
unknowns and mismatches preserved. No aggregate PASS, raw-log processing,
semantic chain validation, migration, deployment or auto-repair. Remaining
candidates stay deferred. A complete inventory can contain an upstream
FAILED/INCOMPLETE result; it never establishes runtime acceptance.

Research recovery: hidden-path discovery and oversized displays were replaced
with exact paths/bounded reads; a copied hash was mechanically corrected.
GUI verified preserved fingerprints and the substantive dossier. Use exact
paths and derive hashes mechanically. Research acceptance is separate from
implementation acceptance and parent closure/accounting.

## Selected implementation — offline evidence inventory

GUI selected the frozen `GUI_SPEC.md` in `T008-EXECUTE-20261023-02` on
2026-10-23. The CLI adds `scripts/evidence_report.py`, its focused tests and
usage guide. It accepts a finite manifest, reads only listed local regular
files, checks byte/hash pins, and projects a strict allowlist of current
handoff, log-delta and classification fields. It preserves literal upstream
statuses and compares only caller-declared supported fields or observed
hashes. It reports deterministic inventory completeness, including unknowns,
optional gaps and pin/link failures. Output is exclusive and private under
`.codex-sync/`; inputs are read-only. Limits, path rules, projections and
non-claims are documented in [EVIDENCE_REPORT.md](../EVIDENCE_REPORT.md).

Focused verification passes 15 tests, including the copied small
handoff and log-delta examples and a CLI smoke with source INCOMPLETE while
inventory exit remains 0. Upstream suites passed once: handoff 36, log-delta
15, classification 33. GUI review and saved-session accounting are pending;
the parent remains OPEN. No runtime, installation, savings or publication
claim is made. The substantive implementation dossier and final provenance
are in the local handoff result.

## GUI implementation review — corrections required, 2026-10-23

The initial EXECUTE receipt is consumed CHANGES REQUIRED, with original
outputs preserved privately. All 15 focused tests pass independently, but
GUI reproduced a valid optional-gap producer status being rejected, unsafe
identity strings being exported, numeric overflow accepted as infinity and
a symlink package root being accepted. Review also found private-fixture
test dependencies, failed-read budget accounting gaps and an invalid guide
example. These are contract defects, not CK3 findings. A separate bounded
correction `T008-FIX-20261023-03` retains the selected architecture and scope.
Parent remains OPEN; offline implementation acceptance/accounting is pending.

Recovery instruction: verify adapter enums against producer branches, test
privacy at every projected string, charge or conservatively stop uncertain
reads, and prove public tests run without ignored task artifacts.

## Bounded correction — T008-FIX-20261023-03

The correction preserves the selected inventory architecture and upstream
verdicts. The adapter now accepts the producer's literal
`COMPLETE_WITH_OPTIONAL_GAPS`; projected handoff and log checkpoint identities
must match the bounded portable token grammar. JSON parsing rejects floating
overflow anywhere in the document. Package roots and existing ancestors are
checked for symlinks before canonicalization; paths containing `..` are
rejected. Artifact reads reserve their declared-size ceiling plus one byte
before access, keep the reservation after failed/drifting reads, and stop
later reads when the total budget cannot cover them. A total-budget issue is
always inventory `INCOMPLETE`.

Public focused tests use synthetic producer-shaped fixtures and pass in an
isolated tree containing only the script, test, and package scaffold. Frozen
private examples were smoked separately and remain unchanged. The user-guide
example now creates both linked inputs and exact pins; its run returned
inventory `COMPLETE` and link `MATCH`. Detailed commands, recovery events,
hashes, and limits of this evidence are recorded in the local correction
dossier; GUI review and parent acceptance/accounting remain pending.

## Final GUI acceptance — 2026-10-23

The selected iteration is accepted: deterministic offline inventory over an
explicit finite manifest, byte/hash pins, caller-declared equality links and
allowlisted upstream fields. Missing, unsupported and mismatched evidence stays
visible. COMPLETE inventory can contain source FAILED/INCOMPLETE; it is not
runtime acceptance. No measured time/token savings are claimed. Other
optimization candidates are deferred, without expanding T-008 into deployment
or semantic chain validation.

GUI independently inspected corrected code, producer contracts, decisive
regression tests and guide. All 22 focused tests pass, also in a fresh isolated
public-only tree. Original optional-gap, privacy and numeric-overflow
reproductions are corrected. Root/ancestor symlink, conservative failed-read
budget and link-trust assertions were reviewed. The unchanged upstream suites
have 84 passing tests in the CLI correction evidence; a possible duplicate run
is disclosed. Both frozen small examples and the exact guide example passed
CLI smoke. Source/helper schemas, existing verdicts and F-001 pause remain
unchanged. Full hostile filesystem race protection and atomic multi-file
snapshots are outside the claim.

Initial defects and failed receipt remain historical evidence; original and
accepted outputs are preserved privately. Recovered tool/path/grammar errors
and possible repeated tests are disclosed in the correction dossier. GUI
accounting output was initially oversized; narrow field projections recovered
the session/turn evidence without publishing metadata. Reusable improvement:
compare enums with producer branches, exercise every exported string, test
public portability, and use bounded evidence projections and exact lifecycle
commands. No extra global instruction or helper duplication was introduced.

## Saved-session accounting

One saved GUI session and three CLI sessions cover preparation, research,
initial implementation, corrections and GUI review through the frozen cutoff.
The runtime records identify Sol in GUI and Luna in all three CLI sessions.
The existing accounting helper and an independent response-ID sum agree on
220 responses and 17,172,634 total tokens. Private snapshots, hashes and exact
turn assignments are retained locally. Four same-day review sources were
checked by linked parent/turn identity; none matched. Coverage remains partial
rather than claiming zero unobserved review usage.

At the 2026-10-23 Standard short-context reference rates, measured token usage
is approximately **$0.99 API-equivalent**: Sol $0.7801712 and Luna $0.2095182
(known total $0.9896894 before rounding). This is not subscription spending.
Maximum recorded request input is 153,348 tokens and recorded cache-write input
is zero. Actual service tier, regional processing, tool charges and missing
usage are not established. Later accounting, documentation integration and
the final response are excluded; the cutoff is not recursively extended.
[Official pricing](https://developers.openai.com/api/docs/pricing?latest-pricing-expanded=true)
was checked on 2026-10-23: uncached/cached/output per million are
$2/$0.10/$10 for GPT-6.1 Sol and $0.10/$0.01/$0.50 for GPT-6 Luna.

## Local commit and planned successor — 2026-10-23 (historical checkpoint)

The user authorized a local commit of accepted T-008 and the short successor
plan, explicitly excluding push. GitHub/Wiki updates and issue closure remain
outside that authority. The original finite accounting cutoff stays fixed;
this later commit/planning work is excluded.

[T-009](T-009-structured-preflight.md) is planned as the next small iteration:
versioned structured preflight evidence and one compatible inventory adapter.
This follows the earlier analysis's conditional recommendation because the
current checker emits only text and T-008 cannot project its result. Schema
and compatibility preparation precede any separate EXECUTE. No next-task
implementation, installation or game action begins here.

<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| gpt-6-luna | 13733273 | 13418240 | 315033 | 87665 | 25334 | 13820938 | partial |
| gpt-6.1-sol | 3330761 | 3205632 | 125129 | 20935 | 3908 | 3351696 | partial |
| **Total** | 17064034 | 16623872 | 440162 | 108600 | 29242 | 17172634 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-23T17:39:01.530464+00:00. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
One saved GUI session and three CLI sessions; 220 deduplicated own response IDs; independent sum agrees. Coverage partial; later accounting/integration/final response excluded. No matching linked automatic-review source in four same-day review sessions; not fabricated as zero usage.
<!-- ai-cost:end -->


## Publication and closure — 2026-10-23

Published to the approved branch and Wiki; [issue #32](https://github.com/mhaduk/ck3-dynasty-map/issues/32) was updated with the accepted result and closed completed after the batch gates. The initial PLANNED body is preserved above as dated scope history. T-008 measured 17,172,634 tokens and $0.9896894 API-equivalent at the frozen partial cutoff; later shared closeout work was excluded. Current rates and coverage notes are in the [Wiki AI-cost table](https://github.com/mhaduk/ck3-dynasty-map/wiki).
