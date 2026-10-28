# CLI delegation template

Copy the content inside the `~~~markdown` example into the GUI-prepared per-ID
`CLI_TASK.md` (omit the example's outer fence) and replace every placeholder.
The GUI freezes the task before READY. This template adds semantic
instructions only; `handoff.py` remains the lifecycle, ownership, revision and
provenance authority. Keep discovery bounded to named roots and exact inputs.
Declare substantive owned outputs outside `.codex-sync/tasks/`, which is
reserved for handoff administration. Check that every required deliverable
exists; a provenance value of `null` is not evidence that it was delivered.

~~~markdown
# <short task title>

Parent: <registered stable parent ID>
GitHub issue: <verified issue number and URL; --issue must match the saved registry>
Delegation type: <COLLECT | VERIFY | RESEARCH | EXECUTE>
Decision authority: GUI
Model recommendation: Luna / Medium (recommendation unless runtime confirms)
Estimated CLI time: <raw-low>–<raw-high> minutes (uncalibrated baseline for future comparable pairs)
Estimated CLI time / steps: <low>–<high> minutes / <exact frozen plan count> steps (<calibration basis; no plan when absent>)

## Question / scope
<Question, intended result and frozen boundaries>

## Acceptance
- <observable criterion>

## Discovery and inputs
- Allowed roots: <exact repository-relative or approved private roots>
- Inputs/snapshots: <exact files, snapshot/hash/manifest IDs>
- Limits: <depth, size, records, time, or explicit no-broad-scan rule>
- Mutable state: <frozen snapshot or named read policy and relevant cutoff>

## Owned paths
- <every output path; one writer per shared path>

## Exclusions
- <work and decisions not authorized>

## Safety / permissions
- <app state assumptions and user-only actions>
- <Git/GitHub/network/write permissions and privacy rules>

## Checks
- <check-name>: <method and pass condition>
- For AI-cost/closeout publication scopes, GUI must add `ai-cost-table-format`:
  every scoped Issue/PR body and canonical record contains the exact workflow
  per-model cost table (including Total and USD), arithmetic/coverage notes
  verified, then the published body is read back. Prose or a link is insufficient.
  The token-only helper fragment is not the final priced table.

## Progress and communication
Use the latest user's language; preserve exact commands, IDs and receipt phrases.
Follow `docs/CODEX_WORKFLOW.md`, section "GUI execution plan and CLI progress"
(repository-root path): use supplied milestones/current revision and relay only
successful meaningful persisted transitions. Never invent progress or an initial
legacy plan. At 100% preserve `CLI complete; GUI review pending`.

## Escalation
Complete useful safe bounded analysis first. Escalate scope, architecture,
direction, material trade-offs, consequential evidence conflicts, permission
boundaries, or a decision not derivable from this task. Continue independent
authorized work. Recommendations are advice; GUI acceptance is separate.

## GUI next step
<Specific review/decision requested; identify decisive evidence to inspect>

```json
{"execution_plan":{"total_steps":2,"steps":[{"id":"work","label":"Perform the bounded assigned work"},{"id":"handoff","label":"Validate outputs and prepare evidence for GUI review"}]}}
```
~~~

The sample plan is illustrative; GUI supplies and freezes the actual milestones
as the last preparation step. Use the canonical
[plan/progress procedure](CODEX_WORKFLOW.md#gui-execution-plan-and-cli-progress)
and [table presentation](CODEX_WORKFLOW.md#handoff-table-presentation), including
summary binding/grouping, saved-session estimate and conditional Routing row.
Do not reconstruct initial plans for legacy handoffs.

For substantial implementation, follow
[frozen independent-review preparation](IMPLEMENTATION_REVIEW.md#frozen-preparation)
and the [review/correction lifecycle](IMPLEMENTATION_REVIEW.md#lifecycle-evidence).
The paired contract and routing are frozen before READY; the original executor
handles corrections and every reviewer is fresh/read-only. Use the delegation
ID, actual selected finite/open policy and registered renderer inputs. For
classification and GUI finalization, use the
[routing procedure](CODEX_WORKFLOW.md#delegation-classes-evidence-and-escalation).
No template or classification grants permissions or removes required checks.

## Compact result example

For an existing registered delegation, run
`python3 scripts/handoff.py --root . preview <ID>` for the next applicable
command, or add `--mode result` for a current `CLI_RESULT.md` scaffold on
stdout. Preview does not claim, lock, initialize review or write a result file.
Replace the explicit owner placeholder before claiming; milestone completion
and task completion still require actual work and evidence. Refresh after
every transition and regenerate the scaffold after implementation: output
hashes describe the files at preview time, while input hashes retain the
registered baseline. JSON null marks a missing output, not a delivered file.
Fill outcome, acceptance, checks, dossier and self-review placeholders from
actual evidence; the unedited scaffold cannot complete. Preview grants no
permissions, invents no runtime profile or reviewer identity, and does not
bypass independent review, correction dispositions or GUI acceptance. It is a
cooperative snapshot, not an atomic transaction against concurrent writers.
Legacy inbox IDs are unsupported; use the explicitly registered per-ID task.

Keep the exact top-level headings and required success/check/provenance grammar
below. Put the evidence dossier under `## Result`; omit optional detail that
does not apply, while retaining every dossier heading for clear unknowns.
For marked tasks, follow the canonical
[self-review schema and placement](EXECUTION_REVIEW.md) and
[GUI triage procedure](EXECUTION_REVIEW.md#gui-triage-and-inventory): exactly one
provenance fence followed by one review fence within `## Result`. Legacy tasks
without the marker retain their contract. The live inventory is GUI-owned;
CLI supplies observations only, using disposable inventory fixtures for tests.

~~~markdown
## Identity
- ID: <ID>; parent: <PARENT>; attempt: <N>; owner/revision: <owner>/<N>
- Delegation type: <type>; Decision authority: GUI
- Model: <actual if runtime confirmed, otherwise unknown; recommendation is not confirmation>

## Result
- Outcome: SUCCESS
- Acceptance: PASS

### QUESTION / SCOPE
<What was checked and the bounded scope.>

### FINDINGS
- Observed: <decisive result>
- Inferred: <inference and basis, if any>

### EVIDENCE
- <claim> — `<path>:<line>`; snapshot/hash `<id>`; <test command/result or receipt/checkpoint/commit ID>.
- Distinguish fresh checks from historical records; identify upstream verdicts and completeness.

### OPTIONS
- <option, benefits, risks and scope impact; or “Not applicable.”>

### RECOMMENDATION
- <advice and reason; optional, not a GUI decision.>

### UNRESOLVED / UNKNOWN
- <remaining unknowns; use “None within this bounded check” only when supported.>

### DECISION REQUIRED
- <specific GUI decision; or “None; GUI acceptance remains pending.”>

```json
{"id":"<ID>","parent_id":"<PARENT>","attempt":1,"inputs":{},"outputs":{}}
```

For a marked task, insert its structured post-execution review JSON fence here,
after the actual provenance above. Replace the illustrative values with the
exact frozen inputs and actual output hashes; do not append another provenance.

## Files
- <changed or created owned path and purpose>

## Checks
- <check-name>: PASS

## Self-healing / agent-instruction findings
- Observation: <tool/path/result>
- Cause or unknown: <why it happened or what remains unknown>
- Recovery/outcome: <recovery and result, including recovered errors>
- Improvement: <small reusable instruction/tool suggestion>

## Permissions / Git state
- <actual permission boundary, operations performed/omitted, and concise Git state>

## GUI next step
- <selected evidence to review, outstanding decision, and acceptance status>

~~~

For an AI-cost/closeout publication result, keep the canonical table specified
in CODEX_WORKFLOW in each scoped Issue/PR body and canonical task record. In
`## Checks`, include the exact standalone `- ai-cost-table-format: PASS` only
after validating the table and published-body readback. A prose-only cost
summary is CHANGES REQUIRED. Do not change the generic result grammar or
add this check to unrelated tasks.

Never place chain-of-thought, credentials, private machine paths, raw logs,
saves or dumps in the dossier. Keep sensitive evidence private and cite its
bounded artifact identifier/hash rather than reproducing it. `handoff.py`
checks lifecycle grammar and hashes; it does not verify that claims are true.
CLI self-review is not independent GUI review, and a recommendation is not
acceptance.
