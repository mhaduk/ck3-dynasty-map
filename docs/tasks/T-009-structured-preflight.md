# T-009 — Structured preflight evidence

Status: **PLANNED — local follow-up selected on 2026-10-23; not READY**.
Planning only; no implementation or GitHub issue creation is authorized by
this record. Predecessor: [T-008](T-008-workflow-optimization.md).

## Problem and selected next step

T-008 provides a bounded inventory with selected upstream statuses, but its
current adapters cannot consume the preflight checker's result as structured
evidence. `scripts/check_mod_preflight.py` currently prints human-readable
success/failure and returns 0/1; it has no versioned JSON result. Operators
must preserve and interpret that prose separately. This is a concrete format
gap, not a measured cost or savings claim.

The accepted T-008 research ranked structured preflight as a small, lower-risk
candidate only when it helps the report. That condition now applies. Select
one additive JSON result contract and one matching T-008 adapter, rather than
starting full cross-stage semantic validation, log profiles or deployment.

## Proposed bounded scope

- Add an explicit JSON mode to the existing checker; keep default text output,
  existing checks and current success/failure exit meanings compatible. Build
  text and JSON from the same findings, never by parsing stdout.
- Freeze a versioned schema before EXECUTE: offline-file-check status, exit
  code, source/optional comparison coverage, finite finding codes and counts,
  expected-version check, and explicit syntax/API/runtime-unverified limits.
  Missing, unreadable or incomplete inputs must stay distinct from a complete
  clean file check. Exact operational-error handling needs a GUI decision
  after the bounded compatibility inventory, without silently changing exits.
- Extend `scripts/evidence_report.py` with one allowlisted adapter for that
  schema. Project only bounded typed status/coverage/count fields; retain
  upstream findings and uncertainty without converting inventory COMPLETE
  into preflight acceptance. Do not export raw diagnostics, absolute paths,
  payload names or source text. Existing manifest/report behavior stays intact.
- Use synthetic temporary payloads and installed-tree copies only. No live
  package installation, real CK3 scans, launcher/game/process action or
  modification of vanilla files. Reuse the existing checker implementation.

## Acceptance cases for the future frozen handoff

1. Current default text and 0/1 success/failure behavior remain compatible for
   representative valid, invalid and comparison cases.
2. Text and JSON agree on the same findings; repeated JSON output is stable.
   File checks never claim CK3 syntax, API, runtime, stored RGB or user acceptance.
3. Missing descriptor, malformed encoding, version mismatch, unreadable input,
   missing/extra/different comparison files and unsupported schema retain
   distinct observable findings/coverage; no synthesized success.
4. Complete inventory can contain failed/incomplete preflight. Pin mismatch,
   unknown schema and missing required fields prevent trusted links/projection
   just as for existing T-008 adapters; no verdict precedence or repair.
5. Privacy sentinels never appear in projected output. Public tests run without
   ignored local artifacts; existing checker/report callers and relevant
   regression suites pass. Inputs remain unchanged.

## Preparation, routing and stop conditions

GUI owns schema, compatibility decisions and final acceptance. Next prepare a
bounded CLI compatibility inventory over the named checker/report/guide and
synthetic acceptance cases; reuse T-008 findings, with no broad rediscovery.
Return any genuine error/coverage ambiguity to GUI before freezing EXECUTE.
Then create a separate per-ID handoff with exact inputs, owned paths, checks,
permissions and GUI-supplied execution plan. Recommend Luna / Medium; selection
is not runtime confirmation. No handoff is READY and no worker starts now.

Keep changes limited to checker, report adapter, relevant tests and guides.
Read MOD_AUTHORING_RULES before any future payload preparation. Preserve
existing preflight semantics; if additive structured reporting cannot do so,
stop for a GUI decision rather than expanding scope. No migrations, auto-pins,
repairs, lifecycle/schema changes in handoff.py, AI ledger, deployment/rollback,
publication or GitHub writes. F-001 remains paused.

## Planning provenance and limits

Basis: T-008's seven-candidate comparison and accepted report contracts; a
bounded inspection of the current checker's output branch confirms the format
gap. No new broad research or implementation was needed for this short GUI
planning edit. Earlier oversized context output was recovered with targeted
sections; use exact symbols/line ranges for subsequent preparation. Frequency,
maintenance cost and actual savings remain unmeasured. Other candidates stay
deferred; T-009 completion and accounting are not claimed.
