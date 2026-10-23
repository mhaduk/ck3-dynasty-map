# T-007 — Handoff execution plan and CLI progress

## 2026-10-23 presentation correction — accepted

The GUI identified that progress bars printed in shell output may be hidden in
collapsed tool-result cards and are not standalone agent messages. The helper's
stdout remains useful diagnostic evidence, but it cannot guarantee user-facing
presentation or native text color. Instructions now require CLI to relay one
standalone commentary after each successful meaningful transition, formatting
only the persisted progress state with the parent ID, a compact ten-cell bar,
approximate percentage and readable stage. No-op, rejected, stale or failed
commands produce no relay; unchanged states are not repeated. At 100%, the
message says CLI completion is gated and GUI review remains pending. No lifecycle
or progress calculation behavior changes. A disposable fixture demonstrates the
state and relay contract; offline helper checks cannot prove client styling or
reliable model instruction-following. Historical acceptance, evidence and cost
cutoff below remain unchanged.

Independent GUI review accepted and consumed `T007-DISPLAY-20261023-02` on
2026-10-23. All 36 existing handoff tests passed again. The saved worker session
confirms `gpt-6-luna / medium`; the worker had reported this as unknown because
it had not inspected runtime evidence. Helper and test source remain unchanged.
GUI moved the progress instructions inside the template's copyable task example
so copied handoffs retain them, and added a short language rule after the user
reported an unintended Finnish commentary. Commentary follows the latest user
request's language; commands, IDs and required receipt phrases remain exact.
This reduces ambiguity without guaranteeing perfect model adherence.

Self-healing: the worker recovered from a rejected exact-text patch by rereading
live lines; a broad listing was narrowed after noisy output. GUI found the relay
paragraph outside the template's copyable example and moved it inside. Review
copyable artifacts as copied, rather than relying on surrounding guidance.
No executable behavior changed and no additional implementation tests are needed.

### Correction-only accounting

The original T-007 table below is unchanged. This separate follow-up uses one
saved GUI session (preparation and review turns) and one saved CLI session,
with frozen source snapshots and explicit per-turn assignments retained privately.
The existing accounting helper and independent response-ID sum agree on 46
records through 2026-10-23T14:10:07.257077Z. No linked automatic-review counters
were found in these two selected sessions or the bounded task-ID session search;
no zero-cost claim is made for missing/unattributed review usage. Later record
integration, language/template refinements, accounting publication and Git work
are excluded from this finite cutoff. Coverage is partial.

| Model | Input | Cached input (subset) | Output | Total tokens | API-equivalent USD |
|---|---:|---:|---:|---:|---:|
| gpt-6.1-sol | 1315194 | 1231616 | 7180 | 1322374 | $0.362118 |
| gpt-6-luna | 1438576 | 1373056 | 10033 | 1448609 | $0.025299 |
| **Total** | **2753770** | **2604672** | **17213** | **2770983** | **$0.387417** |

Standard short-context rates checked on 2026-10-23 at
[official API pricing](https://developers.openai.com/api/docs/pricing): per
million uncached/cached/output tokens, Sol $2/$0.10/$10 and Luna $0.10/$0.01/$0.50.
Observed request inputs remain below 272K; cache-write counters are zero.
Reasoning is included in output, not counted again. This is a rough estimate for
measured usage, not subscription spend or a claim of billed processing tier.
The correction does not refresh the closed-task Wiki or historical issue totals.

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

Correction on 2026-10-23: the initial N/A was an accounting omission, not
missing session evidence. The coordinator stopped at the CLI report instead
of reading the saved sessions. Task-specific preparation, CLI implementation,
GUI review/publication and linked automatic reviews were recovered from
response-level records through the original completion at 2026-10-23T11:52:07.855Z.
A frozen private attribution manifest preserves exact source bytes, hashes,
turn assignments and response IDs. The existing accounting helper and an
independent direct sum agree on all 56 response records. This later correction
is outside that finite cutoff; no ongoing/full-future-task claim is made.

Measured usage totals 4,675,197 tokens, including 4,400,128 cached input tokens.
The known-model Standard API-equivalent estimate is $1.2434732 (about $1.24).
It uses gpt-6.1-sol rates of $2 uncached input, $0.10 cached input and $10 output
per million tokens, checked on 2026-10-23 at
[OpenAI API pricing](https://developers.openai.com/api/docs/pricing).
All priced requests are below the long-context threshold; cache-write counters
are zero. Standard is an estimate, not a claim about actual subscription spend
or processing-tier billing. Reasoning output is already included in output.
The measured codex-auto-review bucket has no established public model price
and remains unpriced; it is included in token totals, excluded from USD totals.

Recovery: replace the N/A row with measured per-model usage and update Wiki
rollups. Reusable improvement: closing a task must inspect saved session
counters and exact task/turn attribution before declaring N/A; missing counters
in a CLI report alone are insufficient. Freeze a completion cutoff to avoid
recursively counting the accounting/publication work forever.

The user authorized scoped documentation/Wiki cleanup, commit and push after
successful review. Public content contains no private task artifacts, raw logs,
saves, generated dumps or machine paths. Issue #25 is verified CLOSED/completed
with all 13 acceptance items checked and its collision corrected to T-007. Wiki commit `4f1f66c` publishes the
[handoff progress guide](https://github.com/mhaduk/ck3-dynasty-map/wiki/Handoff-progress)
and initially added T-007 as N/A. The subsequent session-backed correction
updates coverage to T: 5 closed, 3 measured, with 33,013,452 measured tokens,
31,662,336 cached-input tokens and a $5.41 known-model estimate (unrounded
sum $5.4123779). The original historical amounts remain unchanged.
The repository publication contains only the reviewed helper/tests and related
instructions/records; no game or implementation follow-up is started.

<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| codex-auto-review | 41930 | 26496 | 15434 | 292 | 175 | 42222 | partial |
| gpt-6.1-sol | 4597047 | 4373632 | 223415 | 35928 | 5178 | 4632975 | partial |
| **Total** | 4638977 | 4400128 | 238849 | 36220 | 5353 | 4675197 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-23T11:52:07.855Z. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
Coverage: measured preparation, CLI implementation, GUI review/publication and linked automatic reviews through original completion. This later correction is excluded. Response IDs deduplicated; independent direct sum agrees. codex-auto-review is measured but unpriced; no invented model mapping. Standard short-context API estimate; no subscription-spend claim.
<!-- ai-cost:end -->
