# T-021 — Post-execution review and GUI optimization inventory

Status: complete, accepted by GUI on 2026-10-25 with saved-session cost
verification. Scoped repository publication and completion of issue #47 were
explicitly authorized by the user on 2026-10-25.

## Correction delivered

The independent review of `T021-EXECUTE-20261025-01` reproduced defects in
effectiveness checks, recurrence counts, unknown metric coverage, evidence/path
validation, per-observation history and the provenance example/parser. The
correction is limited to those findings and the original issue #47 scope.

- Effectiveness now checks the persisted verified optimization link and stored
  boundary. It rejects replacement boundaries and requires a matching later
  `EXECUTE` provenance record, execution date and evidence reference.
- Duplicate semantic keys are rejected before writes; chronological regression
  is rejected without changing bytes. All supported metrics are present in
  every occurrence as a number or explicit `null`; known and unknown counts are
  separate and report-level totals are not attributed to each observation.
- Inventory items retain stable `OPT-NNNN` IDs, category, summary, dates,
  occurrence count, affected tasks/executions, metric coverage, trend/status,
  optional link and boundary history, plus per-occurrence decisions,
  rationales and evidence. Empty reviews retain report-level ledger rationale,
  evidence and decision.
- Deterministic GUI migration preserves existing ledger identity/hashes,
  decisions, occurrence content and counts. Missing legacy fields remain
  explicitly unknown; the live inventory was not read for modification or
  migrated during this CLI task.
- Inventory reads validate structure and invariants with controlled errors.
  Controlled paths reject symlink components, except the two canonical macOS
  system aliases `/tmp` -> `/private/tmp` and `/var` -> `/private/var`. Shared
  evidence validation rejects encoded private paths and session identifiers.
- Result parsing accepts exactly one provenance object followed by exactly one
  structured review object. Documentation includes a complete executable
  synthetic triage payload and consistent result placement.

## Evidence

The required scoped command passed:

```text
python3 -m unittest tests.test_execution_review tests.test_handoff tests.test_gui_context
Ran 70 tests — OK
```

Focused tests cover all six independently reproduced GUI failure cases, valid report
hashes on downstream negative cases, unchanged bytes after rejection, distinct
per-item decisions/history, omitted metric coverage, empty ledger rationale,
legacy migration, chronology, symlink ancestors, full new-contract
complete/triage/consume, interruption/idempotent retry and preserved legacy,
planless and GUI-context suites. A disposable execution of the documented JSON
payload against a copied inventory succeeded (4 items, 2 ledger rows). The
reported test count includes all three scoped modules.

Evidence files: `tests/test_execution_review.py`, `tests/test_handoff.py`,
`scripts/execution_review.py`, `scripts/handoff.py`,
`docs/EXECUTION_REVIEW.md`, and
`.codex-sync/T021-FIX-20261025-02/evidence.json`.

## Boundaries and next step

CLI performed no production inventory mutation, historical backfill, publication,
Git staging, commit, push, GitHub write, game or launcher action. GUI independently
reran all 70 tests, verified frozen output hashes and checked copied migration for
ledger, count and evidence preservation and idempotence. GUI then migrated the live
inventory, ingested the correction report and consumed the corrected receipt as
ACCEPTED. The original receipt remains CHANGES REQUIRED.

Correction triage: three observations, one REPEATED and two NEW; two KEEP OBSERVING
and one NO ACTION. No separate optimization task was created. GUI directly
corrected the template's remaining provenance-placement example and the nested
Markdown example fence after preserving the accepted receipt. Human classification
quality and long-term trend/effectiveness remain unverified. The accounting receipt
was independently accepted after exact counter reconciliation. Repository and issue publication are now user-authorized; this authorization
does not add unrelated optimization work.

## AI costs

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6.1-sol | 2813075 | 2695296 | 117779 | 16943 | 2830018 | $0.67451760 |
| gpt-6-luna | 20322276 | 20035328 | 286948 | 97449 | 20419725 | $0.27777258 |
| unknown (linked review) | N/A | N/A | N/A | N/A | N/A | N/A |
| **Total** | 23135351 | 22730624 | 404727 | 114392 | 23249743 | $0.95229018 |

[GUI context history](https://github.com/mhaduk/ck3-dynasty-map/blob/research/native-menu-alternative/docs/telemetry/gui-context/T-021.jsonl)

Partial measured coverage: 253 unique response counters from one saved GUI session
and two CLI sessions, independently recomputed by GUI with exact per-model agreement.
The finite cutoff is 2026-10-25T07:44:59.893Z (08:44:59.893 Warsaw, after the
daylight-saving transition). This includes preparation, implementation, recovery,
correction and GUI review through the frozen snapshot. Later accounting and closeout
work are excluded. Private snapshots, turn mappings and source hashes remain local.

Linked review usage and model identity are unavailable. A bounded same-day search
examined ten metadata prefixes of at most 8 KiB each; all headers extended beyond
that limit, so absence of a parent link in those prefixes does not establish that
no review ran. The unknown component stays N/A; it contributes zero only to the
known-cost sum, without claiming its actual usage was zero. Both measured models
are priced; no recorded measured-model bucket is unpriced.

Standard API-equivalent prices checked 2026-10-25, per million uncached/cached/output
tokens: gpt-6.1-sol $2/$0.10/$10 and gpt-6-luna $0.10/$0.01/$0.50.
Sources: [official pricing](https://developers.openai.com/api/docs/pricing),
[Sol pricing and context threshold](https://developers.openai.com/api/docs/models/gpt-6.1-sol),
and [Luna pricing and context threshold](https://developers.openai.com/api/docs/models/gpt-6-luna).
All measured input counters were below 272K (maximum 151,993), so short-context
rates apply. Cached input is a subset; reasoning output is already included in
Output. Recorded cache-write counters sum to zero; no service-tier or regional
adjustment is inferred. This is a partial Standard API-equivalent estimate, not
subscription spending or an invoice.

The accounting self-review was triaged into three NEW / KEEP OBSERVING observations.
No optimization task was created. A minor report wording error was corrected by GUI:
24 responses exceed 128K input across both models (5 Sol and 19 Luna); the counters
and price calculation were unaffected. Recovered mapping, stale-revision, syntax
and bounded-metadata probe errors remain preserved in the private receipt.
