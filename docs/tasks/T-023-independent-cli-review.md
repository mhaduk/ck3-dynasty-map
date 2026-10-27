# T-023 — Independent CLI review and bounded corrections

Issue: [#49](https://github.com/mhaduk/ck3-dynasty-map/issues/49).
Status: COMPLETE — GUI implementation acceptance and saved-session cost
verification completed on 2026-10-25. Source implementation and workflow Wiki
guides are published; issue #49 is closed completed after this authorized
final GUI receipt. Shared future-task workflow is active.

## AI costs — GUI verified, finite cutoff

GUI verified saved response counters from ten sessions (two GUI and eight CLI,
including independent reviewers and closeout) through 2026-10-25T14:57:08Z.
All 1,344 response records in those frozen source prefixes are assigned to T-023
and deduplicated by response identity. Two initial issue-selected GUI turns
account for the ten records omitted by the preliminary CLI mapping.

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6.1-sol | 39,768,834 | 38,892,416 | 876,418 | 239,182 | 40,008,016 | $8.99014860 |
| gpt-6-luna | 142,395,549 | 140,796,416 | 1,599,133 | 435,654 | 142,831,203 | $1.78570446 |
| **Total** | **182,164,383** | **179,688,832** | **2,475,551** | **674,836** | **182,839,219** | **$10.77585306** |

Partial known-model Standard API-equivalent estimate, not subscription spending
or an invoice. Prices verified on 2026-10-25 against [official API pricing](https://developers.openai.com/api/docs/pricing),
[Sol model pricing](https://developers.openai.com/api/docs/models/gpt-6.1-sol) and
[Luna model pricing](https://developers.openai.com/api/docs/models/gpt-6-luna).
Each response uses its recorded input count: 22 Sol requests exceed 272K input
and use 2x input/cache and 1.5x output rates for the whole request. All remaining
requests use the documented short-context rates. Cache-write counters are zero
in the selected records. Cached input is a subset; reasoning is already included
in output. Actual processing tier, regional/tool/invoice adjustments and any
further unavailable usage are not inferred.

The GUI checked the complete-line source hashes, exact task/turn assignments,
helper recomputation, request-level pricing and Decimal sums. Five bounded saved
guardian-review metadata sources link to other parent sessions; no additional
T-023 review counters were found there. This is not a claim of zero unavailable
review usage. Subsequent publication and final GUI closeout are excluded by the
unchanged cutoff. Original CLI artifacts remain preserved; their provisional
short-only estimate is superseded by this verified result.

[Saved GUI-text estimate history](../telemetry/gui-context/T-023.jsonl) is separate from usage accounting.

## Final GUI closeout

The implementation remains exactly the accepted candidate: 154 independent
tests passed, 102 probes supported the final review, and all three residuals
were independently resolved. No new independent review or implementation change
was introduced for publication. Source publication: `ca6184ccf110d8a90e1ba4932364863df2388a04`;
Wiki guide publication: `d5f52ba63cf2726d01fc63cd297d2f68aa980de6`.
Final verified-cost Home publication: `fe8bf7447cc1b0a5a28e5795783defdb4c103f61`;
issue #49 is CLOSED/completed with `ai-cost-table-format` verified.

GUI preserved the preliminary CLI receipt, recorded CHANGES REQUIRED for its
limited accounting errors, and completed the two bounded corrections directly
during the authorized final cost check. The shared code, original cutoff and
historical task prices remain unchanged. Final issue/Home/source readbacks and
receipt evidence are retained privately. T-021 triage records the attribution/
pricing gap and recovered tooling failures as KEEP OBSERVING; no optimization
task or effectiveness claim follows.

The CLI Home preview used an earlier base. GUI applies the corrected cost section
to the actual published Home, preserving the new workflow links and unrelated
legacy navigation. Compact five-column summary/detail tables and the global
caveat remain. Runtime freshness/OS isolation and prospective savings remain
outside the proven boundary; historical ledgers are never silently migrated.

## Historical authorized cleanup scope — 2026-10-25

The user authorized scoped cleanup, cost accounting, documentation, repository
staging/commit/push and GitHub issue/Wiki publication, preferably in CLI without
independent review. `T023-CLOSEOUT-20261025-09` performs that bounded EXECUTE
work against the accepted code. This supersedes earlier no-publication notes
for this closeout only; old immutable receipts remain historical evidence.

The ordinary GUI receipt still verifies accounting against saved GUI/CLI/review
sessions before formal parent/issue closure, as required by the project cost
gate. CLI may publish source/docs and exact cost tables with pending GUI-check
status, update #49 while open, publish Wiki workflow guides, and prepare the
final Home cost rollup. GUI performs final cost verification/closure/Home rollup
at receipt; no independent reviewer or repeated permission request is required.
Live inventory and saved GUI-text history remain GUI-owned read-only publication
inputs, not CLI outputs. Accepted implementation semantics are unchanged.

Historical correction sequence: original
`T023-EXECUTE-20261025-01` receipt consumed with that verdict and preserved;
correction `T023-FIX-20261025-02` was also consumed CHANGES REQUIRED after
GUI verification. Correction 2 `T023-FIX-20261025-03` was consumed CHANGES
REQUIRED after independent `T023-VERIFY-20261025-04` found four material defects.
The VERIFY assessment itself was accepted and consumed; that does not accept
the implementation. Correction 3 `T023-FIX-20261025-05` was consumed CHANGES
REQUIRED after `T023-VERIFY-20261025-06`; GUI explicitly amended this bootstrap's
selected maximum from three to four for correction `T023-FIX-20261025-07`.
Prior rejected/partial/frozen evidence remains unchanged.

## GUI acceptance and local workflow activation — 2026-10-25

GUI verified all three reviewer outputs, exact receipts/provenance and binding
to 13 unchanged candidate outputs. Fresh independent review passed 154 tests
in 84.947 seconds (command timing only) and assessed 102 probe records. All
three review-06 residuals are independently RESOLVED, no material finding remains,
and A1–A8, issue/addendum, all 25 clarification sections and twelve review
dimensions have sufficient bounded evidence. GUI inspected decisive resolutions
and implicated source slices, then accepted and consumed both receipts without
another review or correction. T-021 self-reviews are explicitly triaged, including
two final KEEP OBSERVING observations; no measured effectiveness claim.

The accepted generic helpers, documentation and templates now govern future
local project work. GUI normally enables the loop for new substantial
implementation delegations, with explicit trivial/legacy exceptions. Each
enabled task freezes its own contracts/profiles/policy and receives the verified
single ten-row handoff; old handoffs keep their existing representation. The
executor persists, reviewers are fresh and read-only, ordinary repairs stay in
CLI, and GUI retains decisions/final acceptance. The bootstrap's four-round
amendment is historical authority for this task only, never a future default.

GUI integrated this acceptance into agent/workflow/state/history instructions
and corrected a nonmaterial inaccurate first-run historical sentence below.
Accepted implementation code is unchanged by GUI integration. Exact original
candidate and reviewer bytes remain preserved with hashes privately.

Runtime model/session identity and external freshness attestation remain
UNKNOWN; file tests do not establish OS isolation or prospective production
savings/effectiveness. Unsupported historical ledgers require an explicit GUI
migration decision, never fabricated backfill. Saved GUI/CLI/review accounting
with a frozen cutoff remains required before parent closeout. No cost totals
are invented, and no Git staging/commit/push, GitHub/Wiki write, parent/issue
closure or game/launcher operation is authorized or performed here.

Scope confirmation: this task changes the shared project workflow, tooling,
agent instructions and delegation templates for future work. It is not a
task-local experiment. Disposable simulations validate that shared capability;
they are not the delivered scope. Each applicable future delegation still
freezes its own execution/review contracts, profiles and continuation policy.
Trivial actions and legacy handoffs retain their approved exceptions. Local
shared use is accepted as recorded above; old bootstrap/historical ledgers are
not automatically migrated.

## Independent review of correction 3 and explicit GUI budget decision

GUI verified all three reviewer outputs, exact receipt/provenance and binding to
13 unchanged candidate outputs. Independent review passed 152 tests in 83.213
seconds (command timing only) and assessed 214 probes. Original four reproduction
families are corrected; V1-04 shared transition prerequisites are independently
resolved. Three residual normal-operation failures prevent acceptance:

- V1-01: after legitimate GUI executor recovery, a known former executor remains
  eligible for a later independent review and can enable readiness.
- V1-02: finite-budget escalation carries a previously independently resolved
  finding, overwriting its final disposition and evidence as ESCALATED.
- V1-03: rendering checks caller-supplied parent text but not actual registered
  delegation metadata, so nonexistent or unrelated handoffs are accepted.

GUI reviewed the three decisive probe records and implicated source slices,
accepted and consumed the completed VERIFY assessment, and consumed the source
CHANGES REQUIRED. Reviewer self-review explicitly triaged: two repeated
KEEP OBSERVING observations, no optimization or effectiveness claim. Original
receipts, outputs and source/profile limitations are preserved privately.

The selected three-correction policy was exhausted and returned to GUI. GUI
now explicitly freezes MAX_CYCLES=4 for this bootstrap's next preparation,
authorizing one additional narrow executor correction of these three residuals.
Reason: the reproduced failures remain inside existing approved invariants;
prior major failures are fixed and extensive policy/integration behavior works;
no new architecture, scope or permission is needed. Accepting known defects to
meet a budget would not satisfy the task. This is a prospective GUI decision,
not CLI permission to extend a loop or rewriting an old frozen three-round
contract. A fresh independent review follows correction 4; further material
failures return to GUI, with no automatic fifth correction. Runtime profile,
production effectiveness, rollout, costs and publication remain separate.

## Independent review of correction 2 — CHANGES REQUIRED

GUI verified three reviewer output hashes, receipt/provenance and binding to
all 13 unchanged source outputs. Independent review passed all 146 scoped tests
in 68.296 seconds (command timing only), assessed 41 probe records and exercised
17 open-ended corrections followed by R18 acceptance. The original G1 and
scalar-readiness G2 cases are fixed in normal lifecycle reads. Four remaining
bounded defects prevent acceptance:

- V1-01: initial executor identity/profile and self-review facts have no immutable
  initialization anchor; projection changes can enable self-review/replacement
  or fabricated known-zero metrics.
- V1-02: an unresolved finding can disappear from later required resolutions
  and permit ACCEPTED; the final historical disposition is also ambiguous.
- V1-03: normal ten-row rendering uses the parent ID for all four commands,
  while local operations require the distinct delegation ID.
- V1-04: a second review attempt can start before correction; the shared handoff
  correction bridge can reopen after blocked escalation without current valid
  authorization, despite the normal review API correctly rejecting it.

GUI checked decisive probe evidence and implicated source slices without
repeating the whole independent test run. Exact source/review bytes and decisions
are preserved privately. Reviewer self-review was explicitly triaged: two
KEEP OBSERVING observations for repeated validation coverage gaps and recovered
discovery/temporary-fixture path failures. No effectiveness claim or separate
optimization task. The next correction is round 3 of this bootstrap's explicitly
selected three; a fresh independent review is required afterward. Exhaustion
does not authorize an extra round without GUI decision.

## GUI review of initial implementation

All 15 actual output hashes and the receipt hash matched. The six named suites
independently passed 123 tests, but additional disposable reproductions showed
four missing safeguards: four corrections under a selected limit of one; GUI
receipt resolution using an unrelated accepted contract/result; mutable status
overriding the immutable review verdict; and acceptance after a BLOCKED
disposition without a required escalation/allowed-gap decision. Review also
identified missing integration of corrected outputs with the existing handoff
completion gates, compact final receipt, cycle triage and complete acceptance
evidence. These are required task corrections, not expanded optimization work.

Seven bounded findings and reproduction evidence are preserved privately under
`T023-GUI-REVIEW-20261025-01`. GUI explicitly triaged the executor self-review:
three observations, KEEP OBSERVING, including repeated stale-revision recovery;
no separate optimization task. Correction 1 of the GUI-selected three-round
budget follows the existing workflow; the new loop is not accepted for use.

## Correction 1 — implementation delivered; GUI requires two residual fixes

GUI verified all 16 actual output hashes and the receipt hash, independently
passed 135 tests in 52.665 seconds, then reproduced two residual integrity
failures: changing only the projected contract and its self-hash changes the
effective budget from 3 to 10 while the frozen GUI contract stays 3; setting
only the scalar escalation text reports Ready for GUI with no review or
immutable escalation event. Private `T023-GUI-REVIEW-20261025-02` preserves
the exact original outputs, reproductions and G1/G2 findings. GUI triaged two
repeated observations as KEEP OBSERVING; no separate optimization task.
The following executor implementation summary is historical delivery evidence;
its broad binding claims remain subject to those two required corrections.

`T023-FIX-20261025-02` now binds review evidence to the exact registered
handoff, immutable contract/inputs, current result and changed owned outputs.
Single-use corrections re-enter normal handoff completion with archived prior
bytes and reset progress; fresh review, explicit finding resolution, bounded
budget, continuity-break recovery, final receipt, cycle-report extraction and
all-cycle GUI triage are integrated. Frozen preparation binds plan/profile/
budget/rationale and the ten-row renderer derives its values from that contract.
All seven GUI findings have evidence-backed dispositions. The six required
affected suites pass 135 tests; first-pass and corrected existing-handoff flows,
including final T-021 ingestion, were simulated in disposable roots. The live
inventory and this active correction's lifecycle were not used as fixtures.
Actual model/runtime isolation and future savings remain explicitly unknown;
rollout to a real task awaits GUI acceptance. Evidence and simulation
matrices identify each criterion and its test. No task or issue closure is
claimed.

## Frozen direction — 2026-10-25

Extend the existing handoff lifecycle with paired frozen execution/review
contracts, a persistent executor, a fresh read-only reviewer for each review,
immutable correction packages and a compact final GUI receipt. Preserve
ownership, revision, progress, registry, privacy and GUI acceptance safeguards.
The normative issue comment requires a single ten-row handoff table and a
deterministic runtime status; legacy handoffs retain their current shape.

The latest supplemental clarification supersedes the earlier finite-only
interpretation and the issue's prohibition on open-ended loops. GUI explicitly
freezes either `MAX_CYCLES` with any positive task-specific correction maximum,
or `UNTIL_ACCEPTED_OR_ESCALATED` with no numeric maximum. Three is the normal
proposal, requiring explicit GUI selection. It is never a target review count.
At that preparation point the bootstrap retained its selected maximum of three
corrections; adding open-ended capability did not change it. The later explicit
GUI decision above prospectively amends the bootstrap maximum to four.

`ACCEPTED` and `ESCALATE TO GUI` stop the CLI loop immediately under either
policy. An accepted first review means one review, zero corrections and no
second review. Under `MAX_CYCLES=N`, N corrections permit a final fresh review
R(N+1); only another `CHANGES REQUIRED` exhausts the budget. Under the open-ended
policy, count alone never causes escalation. Ordinary bounded defects remain
between the persistent executor and fresh read-only reviewers; decisions and
demonstrably unproductive continuation escalate. Telemetry and T-021 GUI triage
are collected for the final return, without requiring GUI at every correction.

## GUI reassessment of the unstarted correction — 2026-10-25

Compared the live issue and its normative ten-row presentation comment with the
user's supplemental clarification and the actual source. The prior plan is
sound for G1/G2, but insufficient for the clarified task as a whole. The current
schema accepted only finite budgets 1–100; authorization, review submission,
correction and rendering assumed a numeric budget. Runtime status omitted explicit
policy and review count. Existing terminal-verdict guards and long-cycle tests
are useful evidence, but do not establish the requested stop/policy matrix.
The automatic escalation of a recurring unresolved finding/regression also
needs to distinguish ordinary bounded repair from a genuine decision or
unproductive continuation. These are observed implementation differences,
not a claim that all existing lifecycle behavior is defective.

GUI revised the same unclaimed `T023-FIX-20261025-03` preparation, preserving its
original READY contract/baseline and prior receipts. Its scope now includes G1/G2,
explicit finite/open-ended policies, immediate terminal behavior, truthful
status/receipt/telemetry and corresponding documentation and focused tests.
Eight frozen milestones replace the earlier five. The new capability still
does not review its own bootstrap handoff. A fresh independent CLI review of
the corrected candidate is required before final GUI acceptance; ordinary
subsequent corrections use the original executor. Synthetic actors are not
independent model review, and a passing test count alone is not acceptance.

## Execution boundary

Delegation: `T023-EXECUTE-20261025-01`, using the existing approved pickup and
receipt workflow while the new capability is being implemented. Source,
synthetic tests, disposable simulations and concise workflow documentation
only. No game/launcher action, publication, issue mutation, Git staging,
commit or push. The live optimization inventory stays GUI-owned and outside
CLI output ownership. Corrected implementation evidence, substantive acceptance
and saved-session cost accounting remain pending.

## Candidate correction 2 — independent review pending

The current `T023-FIX-20261025-03` implementation binds the full effective
paired contract to the exact registered frozen bytes on every lifecycle read,
validates authoritative event projections and derives readiness/escalation from
current immutable events. Paired contract v2 requires an explicit
`MAX_CYCLES` positive maximum or `UNTIL_ACCEPTED_OR_ESCALATED` with a null
maximum. Version 1 remains finite with its frozen selected maximum. A finite
maximum N permits N corrections and a final fresh R(N+1); open-ended loops have
no numeric exhaustion. Terminal ACCEPTED and ESCALATE verdicts stop immediately.
Repeated unresolved findings remain correctable CHANGES REQUIRED unless a
reviewer makes a reasoned escalation decision.

The fixed ten-row renderer shows the actual policy. Deterministic status and the
final receipt show policy, nullable maximum, separate review/correction counts,
current verdict/readiness, first-pass acceptance, finding recurrence, known
telemetry aggregates and GUI rejection signal. Missing measurements remain
UNKNOWN. The full criterion matrix and disposable lifecycle records are in the
local-only `evidence.json` and `simulation.json` beside this handoff; these are
candidate execution evidence, not GUI acceptance.

The required regression command completed with 146 tests passing. During work,
one initial progress command used the pre-claim revision and was rejected; the
claim had incremented STATUS to revision 3. A later progress attempt also used
a stale revision after a successful transition. Both were recovered by reading
persisted `STATUS.json` and retrying with its current revision; no failed
transition changed the milestone state. The first focused test run exposed an
overstrict event-order check and a misedited symlink assertion; both were
corrected, and the full suites then passed. Reusable instruction: reread the
persisted status revision before each progress command, and validate each new
event-order guard against both correction and interruption flows.

Actual model identities/session freshness, GUI acceptance, final T-021
inventory triage, parent cost accounting and prospective workflow effectiveness
remain UNKNOWN or pending. A fresh independent read-only CLI review is required
before GUI acceptance. No task/issue closure or publication is claimed.

## Candidate correction 3 — independent review pending

The current correction candidate addresses independent findings V1-01–V1-04:
immutable initial executor authority anchored to the original result/report;
continued outstanding findings through later reviews and final dispositions;
separate delegation and parent IDs in all rendered commands; and shared
correction-bridge checks before archive/status writes. Historical ledgers
without an initial snapshot fail closed for an explicit GUI migration decision.

Focused tests cover scalar identity/profile substitutions, a recomputed initial
report self-hash, retained original telemetry, dropped finding rejection plus
later independent resolution, distinct parent/delegation rendering for finite
and open policies, and no-write rejection of early review and post-escalation
bridge calls. The full required six-module regression command passed 152 tests
in 80.579 seconds. Disposable finite and open-policy corrected flows reached
normal handoff completion, T-021 cycle triage and consume. `git diff --check`
and JSON deliverable validation passed. Tool-failure recovery details are in
the correction's CLI result and self-review.

This is a candidate only: fresh independent review of these exact completed
bytes and GUI acceptance have not occurred. Actual model/session identity,
live T-021 triage, parent cost accounting, closure, publication and rollout
remain pending or UNKNOWN. Original receipts, prior candidate bytes, reviewer
evidence, GUI-owned inventory and other unowned state remain outside this
correction's outputs.

## Candidate correction 4 — T023-FIX-20261025-07; fresh review pending

GUI explicitly amended the bootstrap to `MAX_CYCLES=4`; this is correction 4/4
and authorizes no fifth correction. The candidate addresses only review-06
residuals V1-01 through V1-03. Reviewer exclusion now derives the initial
executor and every validated recovery identity at both review entry and
submission. Budget exhaustion carries only unresolved/regressed prior findings
and current findings, preserving resolved dispositions and evidence. The
normal enabled renderer resolves the registered delegation, validates its
frozen status and paired contract, and checks exact parent and contract
identity before formatting.

Evidence includes two GUI recovery transitions with original/intermediate/
current API and CLI rejection attempts, no-write assertions, a finite budget
boundary with resolved F1 and newly escalated F2, and real disposable registered
finite/open rendering fixtures with invalid binding negatives. The required
six-module validation initially exposed fixture mismatches, which were corrected.
After adding the two-recovery API/CLI coverage, the focused test passed and the
full suite passed 154 tests in 88.909 seconds. `git diff --check` passed.
At that delivery point the candidate remained pending a fresh
independent read-only review and GUI acceptance; no rollout or publication is
claimed. One malformed shell quote while reading task context was corrected by
quoting the path as a single shell argument; no project files were changed by
that failed read.

The existing A1–A8 and clarification decisions remain the governing GUI
authority. This correction changes only the three review-06 dispositions
above; it does not reopen prior findings marked fixed or alter frozen receipts.
Fresh review and GUI acceptance are still pending.

### A1–A8 preservation matrix for candidate 4

| Criterion | Candidate 4 disposition | Evidence in this correction |
|---|---|---|
| A1 authoritative frozen execution/review contracts | Preserved; registration verification strengthened at normal rendering | `registered-render-binding`; registered finite/open fixtures and exact contract negatives |
| A2 immutable authoritative lifecycle state and identity | Preserved; reviewer independence strengthened across recovery history | `executor-history-independence`; two-recovery API/CLI rejection and no-write assertions |
| A3 explicit finite/open correction policy | Preserved | Existing six-module regression suite; finite/open renderer fixtures |
| A4 immediate terminal verdict semantics | Preserved | Existing lifecycle and receipt regressions in the required suite |
| A5 correction-count boundary and escalation | Preserved; resolved prior dispositions now survive exhaustion | `escalation-dispositions`; MAX_CYCLES=1 F1/F2 boundary |
| A6 ordinary repair versus GUI escalation | Preserved; only outstanding prior findings are carried at automatic exhaustion | Explicit escalation and lifecycle regressions in the required suite |
| A7 ten-row registered handoff and policy display | Strengthened with delegation/parent/contract binding | `registered-render-binding`; four commands, ten rows, final plan row for finite/open |
| A8 criterion-to-evidence traceability | Updated for the three review-06 residuals; older accepted findings remain preserved | `dispositions.json`, `evidence.json`, `simulation.json`, and final CLI receipt |

The supplemental clarification and prior frozen source/reviewer records remain
authoritative inputs. This candidate does not claim independent acceptance,
runtime isolation, production effectiveness, or GUI closeout.
