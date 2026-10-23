# T-007 — Handoff execution plan and CLI progress

Status: COMPLETE — independent GUI acceptance and consumed receipt, 2026-10-23.
Scoped documentation/Wiki publication, commit and push authorized by the user.

Source: [issue #25](https://github.com/mhaduk/ck3-dynasty-map/issues/25), whose
original title/body used T-003. T-003 already identifies the completed Wiki
task. T-007 is the reserved local identity for this work; historical records
are not renumbered; the final task is T-007 to resolve that collision.
The bounded worker
is `T007-PROGRESS-20261023-01`; its frozen contract/baseline and private result
remain local. F-001 stays paused; app state is arbitrary and the user has no
game or launcher action for this task.

## Result and contract

The existing `scripts/handoff.py` handles supplied plans and progress; there is
no second lifecycle mechanism or extra module. GUI derives the final plan
after settling scope, permissions, outputs and validation, before READY.
`create --execution-plan '<JSON>'` appends the plan as a fenced JSON object to
the frozen task. Directly supplying that single block is also supported.
Plans have `total_steps` and `steps[{id,label}]`, 1–20 major milestones,
matching integer length, unique IDs and bounded readable labels. Existing
planless tasks, including frozen legacy handoffs, require no migration.

CLI executes concrete commands and uses supplied IDs with
`progress <ID> --owner <owner> --revision <N> --start <milestone>` and
`--done <milestone>`. One current ID, completed IDs, active plan, approximate
integer percentage and amendments persist in status. The compact task-ID bar
appears on meaningful transitions; normal logs remain between bars. Repeated
current starts/completed finishes with the current revision are silent no-ops.
There is no automatic clock, fake intra-stage progress, ETA, elapsed-time
display, checklist repetition or background monitoring.

Display uses `max(previous, min(99, completed * 100 // total))`. All milestones
and existing result/provenance/check gates must pass before `complete` writes
and emits 100%, explicitly labelled CLI completion with GUI review pending.
GUI review/parent acceptance remain separate. The signal describes coarse
milestone progress, not measured duration, resource use or remaining effort.

`--amend '<replacement plan JSON>' --reason '<justification>'` permits intent
adaptation in labels and genuinely necessary additional major stages within
scope. Existing IDs/order stay; there are no deletions or renames. Both the
20-step cap and a 20-amendment cap apply. Original frozen text and baseline
remain intact; each amendment records plan, reason, owner, revision and time.
The helper replays that evidence against the original plan. Structural checks
cannot prove necessity or preserved intent; those remain review obligations.
A changed scope/permission requires a new handoff. Clamping may temporarily
overstate the current fraction after an addition; the display waits until the
fraction catches up rather than manufacturing progress.

Failure retains progress below 100. An interrupted worker resumes with the
same owner/current revision, without reclaiming. Explicit retry still requires
all initial fingerprints and archives the previous attempt. It clears completed
and current IDs but retains amendments and the display high-water mark; every
milestone must pass again. Completed/consumed tasks reject progress mutations.
Receipt preserves the CLI's 100% even when GUI requires changes. A crash
between atomic status persistence and terminal printing can omit a bar; it
does not justify replaying work or advancing progress. Planless lifecycle is
unchanged. See [workflow commands and examples](../CODEX_WORKFLOW.md#gui-execution-plan-and-cli-progress).

## Issue acceptance self-review

GUI independently accepted the implementation and this coverage after inspecting
the source/test diff and rerunning all 36 tests. The table maps every
acceptance item in #25; the canonical offline suite is
`python3 -m unittest discover -s tests -p test_handoff.py`.

| #25 acceptance item | Implementation and evidence |
|---|---|
| GUI supplies structured plan when useful | AGENTS and workflow require it as final preparation step; create freezes JSON before READY; inline bootstrap is tested |
| Major logical milestones | GUI granularity rule and meaningful-stage examples; semantics require coordinator review |
| At most 20 milestones | Validation rejects 0, 21, mismatched length, bool totals, invalid IDs/labels and duplicates; 20 passes |
| CLI uses supplied initial plan | Reads only frozen block; planless progress refuses to invent stages; old completion remains compatible |
| Current/completed association | Start/done use known IDs; one active stage; completion requires a real start; state survives subprocess restart |
| Compact task ID and approximate percentage | One-line bar on claim/start/done/amend/complete; temporary-root end-to-end transcript |
| Readable logs, bounded noise | Ordinary logs interleaved in demo; no-op transitions emit nothing and leave revision unchanged |
| No ETA/elapsed prediction | No timer or prediction code; validate/repeated starts leave long-stage state unchanged |
| Display never decreases | Completed fraction clamped to retained high-water; amendment and retry regression cases |
| 100 only after final required stage | All milestones plus existing completion grammar/checks/output provenance; negative gate tests leave 99 |
| Unexpected major work | Bounded justified amendments preserve IDs/order, original task and evidence; monotonic demo |
| T-001 safeguards retained | Same locks/revisions/owner/state/path/journal/contract guards; prior lifecycle suite plus progress-specific negatives and concurrency |
| Documentation/tests updated | AGENTS, workflow, state, backlog, canonical record, history and offline helper tests; GUI integrated completion after acceptance |

## Validation and limits

Offline tests include malformed/duplicate/capped plans, planless compatibility,
inline bootstrap, restart/noise/long-stage invariance, unknown IDs, revision and
owner rejection, frozen scope/input/baseline drift, plan-evidence tampering,
amendments, failure/retry, early completion, separate receipt, unsafe paths and
pending journals. Existing lifecycle tests retain race, interruption recovery,
output provenance, safe paths and owned/immutable input coverage. New tests
also exercise progress locking, concurrent stale transitions and interrupted
status writes. All test tasks live in disposable temporary roots; no other
existing task administration is edited.

All 36 handoff tests pass, including the 22 pre-existing lifecycle tests and
14 progress-focused tests. No extra broad test run is needed for unrelated
mod code. Whitespace/diff and local documentation-link checks pass; the public
diff was inspected for identifying paths, secrets, raw logs and generated
material. The CLI worker performed no staging or publication; GUI publication
is separately authorized.

The suite's real subprocess demonstration creates/claims a temporary task,
records progress and a justified amendment, emits normal log lines, completes
with real result provenance, and consumes only that fixture. The private
handoff artifacts preserve the test output/transcript and checks. The live
T-007 bootstrap reuses its GUI-frozen six-step plan only after isolated tests
pass; its original scope and baseline stay intact. Previously completed manual
milestones are recorded as bootstrap catch-up without displaying older bars.

No runtime model switch, token savings, latency reduction or monetary savings
is claimed. The CLI worker had no publication or Git-write authority. The user
subsequently authorized scoped GUI publication, commit and push. No CK3,
launcher, process inspection, live-log access, saves or installation is
part of this work.

## Self-healing and independent GUI receipt

Observation: GUI preparation and the first CLI file discovery returned an
overly broad listing. Cause: recursive discovery mixed task and historical
paths. Recovery: exact task/helper/test paths were selected; no command failed.
Outcome: investigation stayed within bounded tooling context. Improvement:
discover only the named task directory and known helper/test files on pickup.
Initial working-tree state differed from the handoff's prose claim of a clean
tree: current state already contained task selection. Its bytes matched the
frozen fingerprint, so it was preserved rather than treated as an overlap.
Self-review also identified empty plan arguments and unclosed inline plan
fences as validation gaps before finalization. Explicit rejection and targeted
negative cases close both gaps; no actual command failure was hidden.

GUI independently inspected the actual helper/test diff, demonstration, frozen
plan/amendment rules, safeguards and all 13 acceptance rows. The independent
36-test rerun passed, including the 22 original lifecycle tests. No code
correction was necessary. The receipt was consumed as ACCEPTED before
coordinator documentation integration. Frozen task/baseline/result and copies
of all accepted outputs remain local; cleanup retains that evidence and leaves
unrelated task archives untouched. Publication uses the existing branch and
includes only T-007 source, tests and documentation.

## AI cost and publication scope

T-007 has no attributable response-counter report in the supplied evidence.
Input, cached-input, output and cost are N/A, not zero; no model mapping or
full-task total is inferred. Wiki retains the prior measured amounts and adds
this task as unmeasured. Official Standard rates were checked on 2026-10-23
at [OpenAI API pricing](https://developers.openai.com/api/docs/pricing).
Any future measured estimate must price uncached input, cached input and output
separately; cached input and reasoning output remain subsets. Unknown models
stay unpriced, and request-level context/cache-write/tier gaps remain explicit.
This is API-equivalent estimation, not subscription spending.

The user authorized scoped documentation/Wiki cleanup, commit and push after
successful review. Public content contains no private task artifacts, raw logs,
saves, generated dumps or machine paths. Issue #25 is verified CLOSED/completed
with all 13 acceptance items checked and its collision corrected to T-007. Wiki commit `4f1f66c` publishes the
[handoff progress guide](https://github.com/mhaduk/ck3-dynasty-map/wiki/Handoff-progress)
and updates closed-task cost coverage to T: 5 closed, 2 measured; measured
totals and the $4.17 known-model estimate remain unchanged. Standard rate
verification agrees with the existing historical estimate. T-007 remains N/A.
The repository publication contains only the reviewed helper/tests and related
instructions/records; no game or implementation follow-up is started.
