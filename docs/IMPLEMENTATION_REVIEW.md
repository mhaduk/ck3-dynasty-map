# Independent implementation review loop

`scripts/implementation_review.py` provides a cooperative local state guard for
tasks that explicitly opt into independent implementation review. It is not an
OS sandbox and cannot verify that a reviewer actually used a fresh runtime or
that a model/profile claim is true. Runtime identities and actual profiles are
stored separately and remain `null` unless bounded runtime metadata supplies
them.

## Frozen preparation

Before a task is made READY, GUI freezes one paired contract containing the
execution scope, acceptance and permission boundary, exact human-readable plan
and canonical summary hash, selected executor and reviewer profiles,
validation, all twelve named review dimensions, and escalation rules. Version 2
requires an explicit `correction_policy`: `MAX_CYCLES` accepts any positive
integer maximum, while `UNTIL_ACCEPTED_OR_ESCALATED` requires a null maximum.
Both require rationale. Immutable version 1 contracts remain finite with their
original selected maximum. Handoff validation compares the complete effective
contract to the exact registered frozen bytes and compares its plan with the
frozen `execution_plan` and `plan_summary`. The renderer accepts the frozen
contract as its only source for profiles, policy, budget, rationale and plan.
Legacy forms and classified disabled-contract forms follow the existing
[conditional table presentation](CODEX_WORKFLOW.md#handoff-table-presentation).
The executor remains the same
session across corrections; every reviewer is a new, read-only session. These
identity checks are cooperative guards, not proof of runtime isolation.

New classifications may include the optional `routing` object; legacy contracts
without it remain valid. GUI freezes `execution_class`, `review_route`,
`gui_finalization`, `reason`, nullable `high_reason` and `targeted_trigger`.
Use the canonical [classification and finalization procedure](CODEX_WORKFLOW.md#delegation-classes-evidence-and-escalation)
for allowed routes and effort. Schema validation in `validate_contract` remains
authoritative; classification changes effort only, never permissions or required
checks. A selected maximum of three is a normal proposal requiring GUI selection,
not a semantic constant or target correction count.

The normal `handoff.render_handoff_table` renderer requires an explicit
repository root. It resolves the delegation folder, validates its registered
status and frozen paired contract, then derives the parent from that status.
Caller-supplied contract and parent must match those registered values.
`render_enabled_handoff` remains a pure formatting helper and does not verify
registration. Reviewer independence excludes the initial executor and every
identity in the validated GUI recovery chain. Automatic budget escalation
carries only unresolved or regressed findings, preserving independent
reviewer dispositions and evidence for resolved findings in the final receipt.

## Lifecycle evidence

GUI passes the paired JSON contract to `handoff.py create --review-contract`
before READY. The helper fingerprints it alongside the frozen execution
description. Use the **delegation ID** (the `.codex-sync/tasks/<ID>` folder)
for every local command; the parent issue ID is not a substitute.
`wykonaj <ID>` means validate and claim that exact handoff, then execute it in the
persistent executor session. `sprawdź <ID>` means start a fresh read-only
reviewer session and inspect the frozen task/contract, current `CLI_RESULT.md`
and exact changed owned paths. On the first review only, initialize from those
exact artifacts with `implementation_review.py initialize <ID> @<frozen-contract> <CLI_RESULT.md> --changed <owned-path> [--executor-identity <known-opaque-id>]`;
the helper rejects a different contract, result or changed-file set. Then
persist a `begin-review` attempt and submit one bounded `review` receipt. An interrupted attempt remains immutable;
`fail-review` records its outcome and a retry needs a new review ID and fresh
reviewer identity. `initialize` is first setup only and refuses an existing
ledger.

`popraw <ID> R<n>` names the immutable review ID, not a parent ID or guessed
result file. First call `authorize-correction`; it checks the selected budget,
archives prior result/output bytes, and reopens the same handoff under its
existing owner, attempt and scope. Continue in the original executor session,
rerun the frozen plan and checks, write new provenance and `CLI_RESULT.md`, and
use ordinary `handoff.py complete` with the current revision. Then persist the
correction receipt with `correct`; a fresh reviewer must assess the new result.
If that executor session is genuinely lost, only GUI may use
`authorize-executor-recovery` with the exact correction ID, distinct
replacement identity and reason. Its immutable record marks the continuity
break; this is never a silent identity change.

`gotowe <ID>` resolves the exact delegation ID. If it differs from its parent,
return to the parent GUI task only after that delegation is current `ACCEPTED`
or explicitly escalated. GUI ingests each cycle through T-021's existing
inventory, including the ordinary current executor report required by the
handoff receipt, then records GUI triage for every cycle. Each triage checks the
exact report hash and stable `task:attempt:cycle` identity; incomplete coverage
blocks receipt consumption. Never infer which artifact a bare parent ID means.

Every mutation takes the existing handoff lock before the review lock.
Immutable cycle artifacts and their mutable projection use a pending transition
journal. If interrupted between writes, reads fail closed until
`recover-transition` verifies the exact pre/post projection hash and finishes
the journaled artifact bytes. The deterministic `status` projection cannot
replace the final receipt. `gui-reject` records a GUI quality signal. Reviewers
must attest that implementation files remained read-only. Stale result/path,
alternate contract, replayed IDs, tampered artifacts, symlink ancestors,
self-review, reused reviewer identity, missing dimensions or unproven finding
dispositions are rejected.

The only verdicts are `ACCEPTED`, `CHANGES REQUIRED`, and `ESCALATE TO GUI`.
Only `CHANGES REQUIRED` carries findings. Every finding needs one evidenced
executor disposition (`FIXED`, `NOT APPLICABLE`, `CANNOT FIX WITHIN SCOPE`, or
`BLOCKED`) before a fresh review. Material scope, architecture, permission, or
invariant conflicts should escalate immediately. `MAX_CYCLES=N` permits N
corrections and one final fresh review R(N+1); only CHANGES REQUIRED at that
review exhausts the budget. The open-ended policy has no count-based stop.
Review count and correction count are separate, and ACCEPTED or ESCALATE stops
immediately under either policy.

Initialization also stores an immutable `INITIAL` executor snapshot in the
existing lifecycle artifact tree. It binds initial identity, requested and
actual profile, exact completed result hash and parsed self-review report/hash.
The mutable projection must agree with that artifact on every read; later
executor identity changes require the explicit GUI recovery chain. The original
report stays anchored after corrected CLI results replace the current result.
Ledgers created before this anchor are rejected with a GUI migration-decision
message; the helper does not invent historical authority.

At each fresh review, every finding resolved as unresolved or regressed must
remain in the next `CHANGES REQUIRED` package until a reviewer resolves it or
explicit escalation carries it. `ACCEPTED` checks the complete outstanding
set. The final receipt preserves cycle history and adds one final disposition
per finding; executor claims alone do not resolve findings.

The renderer receives the exact delegation ID separately from the frozen
contract's parent issue ID. GUI binds `review_loop.task_id` to the registered
handoff folder and `review_loop.parent_id` to its registered parent; all four
commands use the delegation ID. The shared correction bridge revalidates the
exact current authorization, frozen contract, current result and nonterminal
state before writing an archive or changing handoff status.

`status()` derives readiness from validated immutable events. Every read checks
the complete effective contract against the registered handoff's frozen bytes
and hashes. Missing, reordered, fabricated or unindexed events fail closed.
Executor completion alone never enables GUI return; only the current result's
accepted review or an escalation tied to its immutable event does. A later
changed result invalidates readiness until reviewed.
GUI remains the final acceptance authority and can reject reviewer acceptance.

## User handoff

Use the registered `handoff.render_handoff_table` entry point and the canonical
[Handoff table presentation](CODEX_WORKFLOW.md#handoff-table-presentation).
The existing `render_enabled_handoff` supplies the conditional Routing row and
explicit disabled values where applicable; do not hard-code a universal row
count or remove these fields. Preserve the frozen presentation across
cycles; live status is separate. The original executor handles corrections,
and each independent reviewer uses a fresh session. No telemetry rows are added.

The workflow reuses T-021 for cycle observations and explicit GUI triage. Each
cycle may link a validated factual observation, known metrics and existing
usage/cost references; unknown metrics are null. Temporary synthetic inventory
fixtures are used for tests. No CLI cycle may edit the live inventory, change
routing, create optimization work, publish, or store conversations or hidden
reasoning. T-015 diagnostic review remains available for its separate purpose.

## Acceptance boundary

The ledger binds to the registered handoff ID, parent, attempt, owner, frozen
scope and paired-contract hashes, current completed result, and exact changed
owned outputs. Correction authorization is single-use and budget checked, then
re-enters the same normal completion path. Every correction needs a fresh
review; findings need evidenced executor dispositions and reviewer resolutions.
Repeated unresolved findings and regressions preserve findings and escalation
reasons. GUI rejection clears readiness. The deterministic final receipt
includes current provenance, findings/dispositions, profiles, counts,
validation gaps and T-021 triage coverage.

## Verification boundary

Unit tests and disposable simulations establish file-level contract behavior
only. They do not prove OS isolation, fresh model sessions, selected model
identity, or that GUI accepts the result. The GUI reviews exact changed bytes,
negative checks and cycle evidence, triages T-021 observations, then makes the
acceptance decision.
