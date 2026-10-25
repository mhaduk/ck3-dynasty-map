# T-007 — Synchronize task registry and enforce GitHub-first creation

Canonical task: [#31](https://github.com/mhaduk/ck3-dynasty-map/issues/31).
Status: COMPLETE — implementation and bounded audit accepted on 2026-10-25;
GitHub #31 closed completed and published result/Wiki read back. Repository
source publication was subsequently authorized by the user on 2026-10-25.
The initial GitHub/Wiki authorization excluded repository staging, commit and
push; the later explicit commit/push instruction authorizes this scoped publication. Direct execution in this GUI chat was requested; no
worker handoff, game/launcher operation or product implementation was needed.

## Result

GitHub issue titles are the sole canonical task-ID allocator. The verified
[registry mirror](../task-registry.json) inventories all 47 issues: 46 canonical
R/F/T tasks and one unclassified historical chore. R has 18 IDs, F has 6, T has
22. Closed tasks reserve IDs. At the audit cutoff, the next numbers are R-019,
F-007 and T-023. Body mentions and local future-milestone labels allocate nothing.

The narrow [registry helper](../../scripts/task_registry.py) supports paginated
sync, offline verify/audit, read-only next-ID lookup and authorized reservation.
New handoff creation requires an explicit matching issue number and records its
number, URL and exact canonical title. Claim/progress/completion validate saved
identity offline. No live GitHub call is added to ordinary registered execution.
Network failure, missing registration, wrong repository, duplicate canonical
IDs, failed readback and detected concurrent allocation fail closed. GitHub
cannot enforce atomic unique titles: a detected collision preserves the remote
issues and permits no new local registration; reconcile/re-query before retry.
The mirror retains IDs removed from earlier snapshots. Historical deleted IDs
never observed by the mirror require durable recovery before allocation.

Ownership and manual/agent creation sequence are defined once in the
[workflow](../CODEX_WORKFLOW.md#github-first-task-registry), with a short agent
entry point. Local specifications, navigation, handoffs and Wiki are mirrors.
The helper is a coordination guard, not authentication or a replacement for
review of task meaning. A valid issue number alone cannot prove that arbitrary
free-text work matches its specification; GUI still owns scope and acceptance.

## Audit and reconciliations

| Class | Observed mismatch | Resolution |
|---|---|---|
| C | #25 and #31 both titled T-007 | Restored original progress identity T-003/#25; T-007 belongs solely to registry #31. #25 keeps CLOSED state and original body/counters under an explicit identity correction. |
| B/C | Wiki work used local T-003 without an issue | Preserved its complete original record as [unnumbered historical Wiki work](legacy-wiki-feasibility.md); it no longer allocates T-003. Further execution requires a fresh GitHub reservation. No duplicate retrospective issue or new implementation task created. |
| C | Frozen T007 progress/display handoffs pointed at local T-007 | Explicit historical aliases map those two consumed receipts to T-003/#25. Original task/status/result/baseline bytes remain unchanged; aliases cannot authorize fresh execution. |
| C | Old Wiki T-003 READY handoff could be picked up as progress | Registry quarantines it and the consumed Wiki retry; named pickup rejects, bare pickup excludes quarantined work. Frozen evidence remains intact. |
| D | F002 mapping candidate50 remained READY after later candidates and F-002 closure | Explicit supersession quarantine prevents accidental execution. Source52/installation53 and accepted feature lifecycle remain unchanged. |
| C | BACKLOG, history, workflow, T-012/T-020 and Wiki called progress T-007 | Active navigation/examples now use T-003; historical prose is explicitly superseded, original record retained, old paths become compatibility notices. |
| D | T-002 navigation implied #24 closure was excluded/currently pending | Annotated current verified CLOSED state while retaining the earlier accounting cutoff. No remote lifecycle change. |
| A | Some issues have no individual local specification file | Full verified registry supplies their local identity/state mirror and points to the existing issue specification. No invented result or duplicated task. |
| B | Later backlog milestone labels are not registered GitHub tasks | Clearly marked provisional planning references; handoff creation rejects unregistered parents. No historical milestone prose rewritten or ID silently reserved. |
| D | Wiki costs omitted newly closed T-021 | Added the existing accepted finite-cutoff T-021 aggregate without changing its counters or reopening its task. T-007 is added separately at this closeout. |

Root cause is documented in the preserved progress record and commit history:
the earlier Wiki task allocated T-003 locally without a GitHub issue. After
GitHub created progress #25 as T-003, local preparation treated Wiki as the ID
owner, chose T007-PROGRESS and later renamed #25 to T-007. That “repair”
collided with already registered #31. Local exclusive directory creation was
not a GitHub reservation. Public commit `6b5bdc1` records that progress implementation as T-007; `bd3b3f0` retains its later accounting under the same mistaken identity. The unregistered Wiki label never had authority over
#25. Neither progress implementation nor its costs are reassigned to #31.

F-003 remains OPEN on GitHub although its specification was accepted locally:
those are different lifecycle facts, explicitly retained. Existing R-005/R-009
open gates and closed/not-planned research dispositions remain unchanged.
No task is closed solely because a local file says its documentation is ready.
No legacy inbox exists; the checked per-ID directories are the applicable source.

### Complete canonical inventory at audit cutoff

| Task | GitHub | State at audit | Local mirror |
|---|---|---|---|
| F-001 | [#20](https://github.com/mhaduk/ck3-dynasty-map/issues/20) | CLOSED | F-001-resume.md, F-001-dynasty-map-ux.md |
| F-002 | [#21](https://github.com/mhaduk/ck3-dynasty-map/issues/21) | CLOSED | F-002-dynasty-color-strategy.md |
| F-003 | [#22](https://github.com/mhaduk/ck3-dynasty-map/issues/22) | OPEN | F-003-dynasty-subview-definitions.md |
| F-004 | [#29](https://github.com/mhaduk/ck3-dynasty-map/issues/29) | CLOSED | F-004-diagnostics-hardening.md, F-004-icon-preparation.md |
| F-005 | [#30](https://github.com/mhaduk/ck3-dynasty-map/issues/30) | OPEN | F-005-functional-followups.md |
| F-006 | [#39](https://github.com/mhaduk/ck3-dynasty-map/issues/39) | OPEN | F-006-diagnostic-timer.md |
| R-001 | [#1](https://github.com/mhaduk/ck3-dynasty-map/issues/1) | CLOSED | R-001-environment-baseline.md |
| R-002 | [#2](https://github.com/mhaduk/ck3-dynasty-map/issues/2) | CLOSED | R-002-map-mode-definitions.md |
| R-003 | [#3](https://github.com/mhaduk/ck3-dynasty-map/issues/3) | CLOSED | R-003-map-mode-gui-inspection.md |
| R-004 | [#4](https://github.com/mhaduk/ck3-dynasty-map/issues/4) | CLOSED | R-004-generated-api-docs.md |
| R-005 | [#5](https://github.com/mhaduk/ck3-dynasty-map/issues/5) | OPEN | R-005-player-context.md |
| R-006 | [#6](https://github.com/mhaduk/ck3-dynasty-map/issues/6) | CLOSED | R-006-scope-links.md |
| R-007 | [#7](https://github.com/mhaduk/ck3-dynasty-map/issues/7) | CLOSED | Verified registry entry; issue owns specification |
| R-008 | [#8](https://github.com/mhaduk/ck3-dynasty-map/issues/8) | CLOSED | Verified registry entry; issue owns specification |
| R-009 | [#9](https://github.com/mhaduk/ck3-dynasty-map/issues/9) | OPEN | R-009-barony-color-safety.md |
| R-010 | [#10](https://github.com/mhaduk/ck3-dynasty-map/issues/10) | CLOSED | Verified registry entry; issue owns specification |
| R-011 | [#11](https://github.com/mhaduk/ck3-dynasty-map/issues/11) | CLOSED | Verified registry entry; issue owns specification |
| R-012 | [#12](https://github.com/mhaduk/ck3-dynasty-map/issues/12) | CLOSED | Verified registry entry; issue owns specification |
| R-013 | [#13](https://github.com/mhaduk/ck3-dynasty-map/issues/13) | CLOSED | Verified registry entry; issue owns specification |
| R-014 | [#14](https://github.com/mhaduk/ck3-dynasty-map/issues/14) | CLOSED | R-014-source-map.md |
| R-015 | [#15](https://github.com/mhaduk/ck3-dynasty-map/issues/15) | CLOSED | R-015-clerical-regions.md |
| R-016 | [#16](https://github.com/mhaduk/ck3-dynasty-map/issues/16) | CLOSED | R-016-my-dynasty-pipeline.md |
| R-017 | [#19](https://github.com/mhaduk/ck3-dynasty-map/issues/19) | CLOSED | R-017-test-scenario-selection.md |
| R-018 | [#38](https://github.com/mhaduk/ck3-dynasty-map/issues/38) | OPEN | R-018-diagnostic-timing-research.md |
| T-001 | [#23](https://github.com/mhaduk/ck3-dynasty-map/issues/23) | CLOSED | T-001-agent-workflow-optimization.md |
| T-002 | [#24](https://github.com/mhaduk/ck3-dynasty-map/issues/24) | CLOSED | T-002-task-ai-cost.md |
| T-003 | [#25](https://github.com/mhaduk/ck3-dynasty-map/issues/25) | CLOSED | T-003-handoff-progress.md |
| T-004 | [#26](https://github.com/mhaduk/ck3-dynasty-map/issues/26) | CLOSED | T-004-issue-title-convention.md |
| T-005 | [#27](https://github.com/mhaduk/ck3-dynasty-map/issues/27) | CLOSED | T-005-research-backlog-review.md |
| T-006 | [#28](https://github.com/mhaduk/ck3-dynasty-map/issues/28) | CLOSED | T-006-workflow-automation.md |
| T-007 | [#31](https://github.com/mhaduk/ck3-dynasty-map/issues/31) | OPEN | T-007-task-registry.md |
| T-008 | [#32](https://github.com/mhaduk/ck3-dynasty-map/issues/32) | CLOSED | T-008-workflow-optimization.md |
| T-009 | [#35](https://github.com/mhaduk/ck3-dynasty-map/issues/35) | CLOSED | T-009-structured-preflight.md |
| T-010 | [#36](https://github.com/mhaduk/ck3-dynasty-map/issues/36) | CLOSED | T-010-checkpoint-comparison.md |
| T-011 | [#37](https://github.com/mhaduk/ck3-dynasty-map/issues/37) | OPEN | T-011-deferred-workflow-optimizations.md |
| T-012 | [#33](https://github.com/mhaduk/ck3-dynasty-map/issues/33) | CLOSED | T-012-gui-context-measurement.md |
| T-013 | [#34](https://github.com/mhaduk/ck3-dynasty-map/issues/34) | CLOSED | T-013-wiki-cost-table.md |
| T-014 | [#40](https://github.com/mhaduk/ck3-dynasty-map/issues/40) | OPEN | Verified registry entry; issue owns specification |
| T-015 | [#41](https://github.com/mhaduk/ck3-dynasty-map/issues/41) | CLOSED | T-015-diagnostic-escalation.md |
| T-016 | [#42](https://github.com/mhaduk/ck3-dynasty-map/issues/42) | OPEN | Verified registry entry; issue owns specification |
| T-017 | [#43](https://github.com/mhaduk/ck3-dynasty-map/issues/43) | OPEN | Verified registry entry; issue owns specification |
| T-018 | [#44](https://github.com/mhaduk/ck3-dynasty-map/issues/44) | OPEN | Verified registry entry; issue owns specification |
| T-019 | [#45](https://github.com/mhaduk/ck3-dynasty-map/issues/45) | OPEN | Verified registry entry; issue owns specification |
| T-020 | [#46](https://github.com/mhaduk/ck3-dynasty-map/issues/46) | CLOSED | T-020-handoff-execution-plan.md |
| T-021 | [#47](https://github.com/mhaduk/ck3-dynasty-map/issues/47) | CLOSED | T-021-execution-review.md |
| T-022 | [#48](https://github.com/mhaduk/ck3-dynasty-map/issues/48) | OPEN | Verified registry entry; issue owns specification |

The table is the pre-closeout audit snapshot; #31 closes only after final gates.
The JSON mirror records the subsequent verified state. Individual missing
specification files are not unregistered tasks: the issue remains their source.

## Verification

88 focused offline tests pass: 42 handoff lifecycle/progress tests, 18 registry
cases, 15 GUI-context tests and 13 execution-review tests. Registry fixtures
cover every requested automated case, pagination/PR exclusion, wrong repo,
readback failure, historical aliases/quarantine and actual successful creation
of a temporary local handoff after mocked GitHub-first reservation. Tests create
no public issues. Existing handoff ownership, frozen scope, accounting hooks,
progress, summary formatting and review contracts are retained.

The live read-only audit checks all persisted handoff statuses against the
registry; only the five explicitly documented historical dispositions remain.
Named old Wiki pickup rejects; bare pickup reports no eligible READY task.
Intentional negative checks are not claimed as operational failures. Stored
hashes confirm all five original task/status files remain byte-identical.
Whitespace, local links and scoped public-content privacy checks are required
before publication and passed; no repository staging, commit or push is performed.
Wiki commit `507d27b` published only Home, Handoff-progress and Task-registry.
A fresh remote clone matched all three files exactly; issue #25 identity/state,
#31 final body/state/label and canonical cost-table readbacks passed.
The grouped Wiki known cost is $94.71390072 before display rounding, from
T-013 baseline $93.03874134 plus unchanged T-021 $0.95229018 and T-007
$0.72286920. It now covers 33 closed tasks; no old task cost was reassigned.

- ai-cost-table-format: PASS

## Self-review and recovered failures

Observation: the first broad state/history read exceeded the output budget;
recovery used bounded relevant searches and reused those findings. An overly
broad fixture replacement inserted a block twice and produced IndentationError;
removed the duplicate and reran the complete handoff suite successfully.
A registry test initially compared raw lowercase REST state against normalized
uppercase fixture state; corrected the assertion to compare canonical inventory,
then all cases passed. No product behavior was weakened to satisfy the test.

One legacy-inbox search returned rg exit 2 because the optional inbox does not
exist; inspection established that absence, and the audit continued using
per-ID state. A later broad search of historical publication JSON emitted an
oversized result; the exact canonical T-013 record supplied the needed unrounded
amounts. Improvement: check optional exact paths before reading and compare
normalized API structures; scope edits and historical searches to one occurrence
or canonical source. No hidden game/process check or destructive recovery occurred.

Publication recovery: the first fetch could not write `.git/FETCH_HEAD` under
the restricted filesystem. The authorized elevated retry succeeded; the remote
and local branch matched before staging. Git metadata writes require the
appropriate execution permission even after user commit/push authorization.

The source was reviewed against the acceptance cases after implementation;
this is coordinator review, not an independent worker review. No optimization
report authorizes further implementation or changes to the live optimization
inventory.

## AI costs

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6.1-sol | 3396027 | 3297792 | 98235 | 19662 | 3415689 | $0.72286920 |
| **Total** | 3396027 | 3297792 | 98235 | 19662 | 3415689 | $0.72286920 |

Partial finite-cutoff coverage: 36 deduplicated response records from one saved
GUI session; no CLI session used. Existing accounting helper and independent
response-ID summation agree exactly. Frozen cutoff: 2026-10-25T08:07:33.096Z
(09:07:33 Warsaw). Later reporting, accounting and publication work is excluded.
Twelve same-day saved-session metadata files were checked; no linked automatic
review session/counters were found. Missing review usage is unavailable, not
zero. Source snapshot/hash, exact turn mapping and audit remain private.
No GUI context history was measured; no fabricated history link is added.

[Official Sol pricing](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
checked 2026-10-25: Standard API-equivalent rates per million uncached/cached/output
tokens are $2/$0.10/$10. Maximum observed request input is 137,422, below the
272K long-context threshold. All recorded models are priced. Cached input is
a subset; reasoning output is already included in Output. No nonzero cache-write
counter was observed. Processing tier, tool fees and regional adjustments are
not inferred. This is a rough estimate for measured usage, not subscription
spend or an invoice. Historical cost amounts remain unchanged.
