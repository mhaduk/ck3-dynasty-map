# Post-execution review and optimization inventory

New handoffs carry `Self-review contract: execution-review/v1`. The result has
one provenance JSON fence, then one structured review JSON fence inside
`## Result`. The helper checks all nine categories, at most five ranked
hotspots, public-safe evidence identifiers and finite nonnegative metrics.
Unknown measurements are `null`; older tasks without the marker keep their
existing completion contract.

The review object has this shape:

```json
{"type":"post_execution_self_review","version":1,"categories":{"errors_recovery":"NONE","execution_time":"NONE","token_context_hotspots":"NONE","rework":"NONE","automation_candidates":"NONE","discovery_overhead":"NONE","repeated_knowledge_acquisition":"NONE","validation_gaps":"NONE","scope_process_anomalies":"NONE"},"cost_hotspots":[],"metrics":{"elapsed_seconds":null,"tokens":null}}
```

## GUI triage and inventory

The inventory is GUI-owned mutable state. A delegated CLI task must never own,
edit, reset, or fingerprint it as a completed output. GUI reviews each report,
authors semantic keys and per-observation decisions, then invokes
`scripts/execution_review.py ingest`. Synthetic inventory fixtures belong in
temporary test roots. `handoff.py consume` checks the matching report hash in
the ledger before receipt; this gate remains separate from task acceptance.

The minimum item schema includes a stable `OPT-NNNN` display ID, category,
summary, first/last dates, occurrence count, affected parent/execution IDs,
metric coverage, trend/status, optional optimization link and per-occurrence
history. Every occurrence records its own decision, rationale, link/boundary
state when changed, and evidence. Empty reports still add a ledger row with
report-level rationale, evidence and decision. Duplicate semantic keys in one
report are rejected before writing. One attempt adds at most one occurrence per
key. Missing metrics become explicit `null` and increment unknown coverage;
report-wide totals are never copied onto each observation. Out-of-order
occurrences are rejected without changing inventory bytes.

`migrate` is an explicit GUI operation. It adds display and history fields
deterministically to the current version-1 inventory, while preserving ledger
IDs, content hashes, occurrence evidence, decisions and counts. Fields absent
from legacy data remain marked `unknown`; no category, summary, status,
decision, or execution provenance is inferred. Review migration on a copied
synthetic fixture before applying it to the live inventory. Do not use migration
to rewrite ledger identity or backfill reports.

Effectiveness (`IMPROVING` or `RESOLVED`) is compared to the already persisted
verified optimization link and implementation boundary. An observation cannot
replace either value. It also needs a recorded later `EXECUTE` provenance object
with task ID, delegation type, execution date and public evidence reference.
The evidence date must be after the persisted boundary. Ingestion date alone,
a task link alone, and evidence supplied only alongside the effectiveness
observation do not establish the later execution. Future occurrences continue
to be collected after an effectiveness claim.

Every public evidence reference uses the same bounded identifier validator.
URL-encoded or wrapped private paths, session identifiers and invalid
structures are rejected. Inventory reads validate schema, uniqueness,
chronology and ledger assumptions before returning data; malformed JSON or
invariants produce a controlled validation error. All components of controlled
paths are checked for symlinks. Only the canonical platform aliases `/tmp` to
`/private/tmp` and `/var` to `/private/var` are trusted; nested aliases are
rejected.

## Complete triage input example

The CLI is `python3 scripts/execution_review.py ingest INVENTORY TRIAGE_JSON`.
The GUI-created JSON must contain exactly the fields below. The report hash is
SHA-256 of canonical review JSON: sorted keys, compact separators, UTF-8. The
per-item fields can override the report-level decision and rationale.

```json
{
  "report": {"type":"post_execution_self_review","version":1,"categories":{"errors_recovery":"NONE","execution_time":"NONE","token_context_hotspots":"NONE","rework":"NONE","automation_candidates":"NONE","discovery_overhead":"NONE","repeated_knowledge_acquisition":"NONE","validation_gaps":"NONE","scope_process_anomalies":"NONE"},"cost_hotspots":[],"metrics":{"elapsed_seconds":null,"tokens":null}},
  "task_id": "T021-DOC-EXAMPLE-01",
  "attempt": 1,
  "report_sha256": "6cf9f14c5515d0a10ad47ad33573397f6d5e37875d57e1dc49c7516ed81de35f",
  "observations": [
    {"key":"handoff.docs-example","category":"discovery_overhead","summary":"Synthetic example observation","text":"This disposable example demonstrates the full triage payload.","trend":"NEW","metrics":{"time_seconds":null,"tokens":null,"rework_count":null,"manual_effort":null,"reliability_events":null},"decision":"KEEP OBSERVING","rationale":"Synthetic documentation example.","evidence":["handoff:T021-DOC-EXAMPLE-01"]}
  ],
  "decision": "KEEP OBSERVING",
  "rationale": "First observed execution; retain factual recurrence evidence.",
  "evidence": ["handoff:T021-DOC-EXAMPLE-01"]
}
```

Save the JSON object above to a temporary `triage.json`, then run:

```sh
python3 scripts/execution_review.py ingest /tmp/optimization-inventory.json /tmp/triage.json
```

For a clean temporary run, first copy `docs/telemetry/optimization-inventory.json`
to `/tmp/optimization-inventory.json`; this CLI command is an example only and
must never target the live inventory from a delegated CLI task.

When later evidence supports an effectiveness claim, include an earlier
occurrence whose `execution_provenance` is explicit, for example:

```json
{"task_id":"T021-EXECUTE-20261026-01","delegation_type":"EXECUTE","date":"2026-10-26","evidence":"handoff:T021-EXECUTE-20261026-01"}
```

This provenance belongs on the later execution observation. The eventual
`IMPROVING`/`RESOLVED` triage must retain the existing link and boundary.

## Minimal result placement

~~~~markdown
## Result
- Outcome: SUCCESS
- Acceptance: PASS

### QUESTION / SCOPE
Bounded work summary.

### FINDINGS
- Implemented and verified the assigned correction.

### OPTIONS
Not applicable.

### RECOMMENDATION
GUI review is pending.

### UNRESOLVED / UNKNOWN
- Human semantic classification remains GUI-owned.

### DECISION REQUIRED
None; GUI acceptance remains pending.

```json
{"id":"T021-EXAMPLE","parent_id":"T-021","attempt":1,"inputs":{},"outputs":{}}
```

```json
{"type":"post_execution_self_review","version":1,"categories":{"errors_recovery":"NONE","execution_time":"NONE","token_context_hotspots":"NONE","rework":"NONE","automation_candidates":"NONE","discovery_overhead":"NONE","repeated_knowledge_acquisition":"NONE","validation_gaps":"NONE","scope_process_anomalies":"NONE"},"cost_hotspots":[],"metrics":{"elapsed_seconds":null,"tokens":null}}
```
~~~~

The outer code fence above only presents this example. A real result contains
one provenance object followed by one review object, not a nested Markdown
fence around both. The receipt parser checks that ordering. The helper does no
GitHub action or optimization recommendation; only the GUI decides whether to
create a separate optimization task. One GUI inventory writer runs at a time.
