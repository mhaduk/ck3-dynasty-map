# T-024 — Execution classification and reasoning-cost guardrails

**Status:** COMPLETE — GUI accepted, receipt consumed; scoped publication authorized and completed on 2026-10-25.
**Issue:** #50 — `T-024 — Add lightweight execution classification and reasoning-cost guardrails`.

R1 correction: F1–F3 addressed in one correction cycle; fresh R2 independently returned ACCEPTED.

## Implementation

Extended the existing paired T-023 contract with an optional frozen `routing`
object. The contract validator accepts four classes, routes, concise reasons,
explicit High reasons, and concrete targeted-review triggers. It rejects
automatic XHigh/Max, disallows ordinary review loops for `NONE` and
`DIAGNOSTIC`, and preserves contracts without routing for legacy handoffs.

The existing handoff renderer shows the routing decision in one compact row;
MECHANICAL handoffs can state that independent review is absent. The final
receipt repeats the frozen decision. Workflow, implementation-review, and
handoff-template guidance document the cheapest-sufficient route, operational
closeout, installation, deterministic logs, diagnostic escalation, and
unchanged validation requirements.

## Evidence and limits

Focused synthetic tests cover MECHANICAL without independent review, direct
disabled-route completion/receipt resolution, STANDARD with Sol/Medium,
COMPLEX remaining at Medium, explicit High reasons visible in handoff and
receipt, XHigh/Max rejection, diagnostic routing, targeted-review triggers,
operational closeout/install/log scenarios, ambiguous evidence, retained
validation, and legacy compatibility. The four frozen check commands and
`git diff --check` are listed in the task's `CLI_RESULT.md` and `evidence.json`.

This is a GUI-authored routing decision stored in the existing paired contract;
it does not add an automated classifier call. Existing handoffs without the
optional object remain readable and were not migrated. Runtime model selection
remains a recommendation unless the runtime confirms it. R2 independent review and final GUI acceptance are complete. Scoped publication is authorized; no game or launcher action was performed.

## GUI acceptance — 2026-10-25

R2 returned ACCEPTED after one correction, resolving three bounded findings:
route-specific return wording for disabled review, visible High reason, and
required synthetic operational/install/log-validation scenarios. R2 evidenced
125 passing tests (44 handoff, 46 implementation review, 15 GUI context,
20 diagnostics), plus `git diff --check`. GUI verified the current result hash
and all ten declared output hashes, exact review/result revision, scope,
permissions, resolved findings and absence of required manual/runtime work.
Existing validation was not repeated after the accepted unchanged revision.

The immutable receipt left runtime identity/profile null. Targeted GUI checking
of saved metadata confirmed Luna/Medium executor continuity and distinct
Sol/Medium R1 and R2 sessions. Original null ledger values were preserved;
this supplemental provenance is not proof of OS isolation. All five cycle
reports and the current executor report were explicitly ingested and triaged
through T-021 before receipt consumption. Observations remain under observation;
no new optimization task or effectiveness claim was created.

The initial GUI receipt resolve correctly blocked on missing cycle triage;
explicit GUI ingestion and recording recovered the gate. Two attempted reads
of historical closeout filenames failed because those files did not exist;
file discovery located the actual `verified-summary.json` instead. Use exact
discovered paths and distinguish historic evidence from current provenance.
Private accepted-output snapshots, GUI decision and accounting audit remain
outside Git. The user subsequently authorized scoped source commit/push, issue update/closure
and Wiki publication in this GUI session.

## AI costs — GUI verified, finite cutoff

GUI verified saved response counters from one GUI session, the persistent CLI
executor (initial work and correction), and two independent review sessions.
All 198 attributable response records are deduplicated by response identity.
Frozen cutoff: 2026-10-25T17:51:58.290Z; later receipt/accounting/documentation and publication
work excluded. The rejected shortened pickup in the R2 session is task-attributable.

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6.1-sol | 3,789,827 | 3,575,808 | 214,019 | 16,957 | 3,806,784 | $0.95518880 |
| gpt-6-luna | 15,757,084 | 15,562,496 | 194,588 | 51,374 | 15,808,458 | $0.20077076 |
| **Total** | **19,546,911** | **19,138,304** | **408,607** | **68,331** | **19,615,242** | **$1.15595956** |

[GUI context history](https://github.com/mhaduk/ck3-dynasty-map/blob/research/native-menu-alternative/docs/telemetry/gui-context/T-024.jsonl)

Partial known-model Standard API-equivalent estimate; not subscription spending
or an invoice. Uses the project pricing evidence verified on 2026-10-25 against
[official API pricing](https://developers.openai.com/api/docs/pricing), preserved
in the accepted T-023 GUI accounting and rechecked against the official pricing
page during this publication (2026-10-25). Sol rates per million: $2 input / $0.10
cached / $10 output; Luna: $0.10 / $0.01 / $0.50. No selected request exceeds 272K input; short-context rates apply.
Reasoning output is already included in output. Processing tier, regional/tool
adjustments and unavailable usage are not inferred. No dedicated linked
automatic-review metadata/counter source was found in the bounded local source
search; this is a coverage gap, not zero usage. Private source snapshots, exact
turn assignments, hashes and per-response pricing audit are retained locally.

## Publication — 2026-10-25

The user authorized scoped cleanup, documentation, commit/push and GitHub/Wiki
closeout in the existing GUI. Issue #50 is CLOSED / completed; all acceptance
checkboxes, the canonical per-model/Total/USD table and the
`ai-cost-table-format` label were read back. Wiki commit `afb76ef` publishes
routing guidance and adds T-024 once to the cost detail/rollup; fetched remote
bytes match. Source publication uses `research/native-menu-alternative`.
The 125-test accepted code remains unchanged. Privacy gates cover the exact
source and staged changes. Later publication is outside the frozen cost cutoff.

- ai-cost-table-format: PASS
