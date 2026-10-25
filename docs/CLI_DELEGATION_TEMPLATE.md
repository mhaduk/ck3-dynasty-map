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
Keep user-facing commentary in the language of the latest user request, including
readable stage descriptions; preserve exact commands, IDs and required receipt phrases.
After each successful meaningful progress transition, send one standalone agent
commentary based on persisted `STATUS.json.progress`, using the parent ID and
the current stage label (or “milestone boundary”):
`●  <parent ID> [<30-cell Unicode bar>] ~<percent>% — <stage>`. Never relay no-ops
or failed, rejected or stale commands; do not duplicate an unchanged state or
guess progress. At 100%, say
`CLI complete; GUI review pending`. Commentary contains no ANSI escapes. Terminal
output uses a green ANSI bullet when color is supported and the same glyph
uncolored otherwise. Keep ordinary command output as evidence; shell output
itself is not an agent commentary.

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

The GUI supplies a real 1–20 milestone plan as its final preparation step when
progress is useful; the example above is illustrative only. Follow the current
schema: CLI must not invent an initial plan. Justified in-scope amendments
use the existing `progress --amend` procedure; scope changes require a new handoff.

For a planned handoff, append one `Plan of execution` row after the five
standard receipt rows using `handoff.render_handoff_table`. GUI supplies up to
ten concise authored summary bullets, each mapped to ordered milestone IDs,
and freezes them with `create --plan-summary`. The helper binds the summary to
the plan fingerprint, rejects stale or incomplete mappings, and escapes table
cells. For more than ten milestones, GUI authors ordered meaningful groups.
Planless legacy handoffs retain the five-row table.

## Compact result example

Keep the exact top-level headings and required success/check/provenance grammar
below. Put the evidence dossier under `## Result`; omit optional detail that
does not apply, while retaining every dossier heading for clear unknowns.
For results with `Self-review contract: execution-review/v1`, append exactly
one fenced provenance JSON object in the result and exactly one fenced review
JSON object after it, both within `## Result`; no second provenance example or
identity fence is allowed. `handoff.py` rejects duplicate provenance objects.
It has `type: post_execution_self_review`, `version: 1`, all categories,
`cost_hotspots` (maximum five) and `metrics` (unknown is `null`). CLI records
observations only; GUI owns ingestion and decisions.

The live `docs/telemetry/optimization-inventory.json` is GUI-owned mutable
state. Do not declare it owned, edit it, reset/backfill it, or include it in
completed-output hashes. Use temporary synthetic inventory fixtures only.

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
