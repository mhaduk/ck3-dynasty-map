# T-006 — Model routing and delegation contract

Parent issue: [#28](https://github.com/mhaduk/ck3-dynasty-map/issues/28). Status: **COMPLETE — GUI accepted step 0 on 2026-10-23 after corrections and saved-session cost verification; GitHub/Wiki publication completed 2026-10-23**.

## Goal and accepted scope

T-006's earlier CLI analysis found existing lifecycle, snapshot, ownership,
revision, provenance and bounded log/classification helpers worth reusing. Its
recommendations did not authorize blanket implementation. GUI selected only
step 0: make responsibility and model routing explicit for GUI / Sol and CLI /
Luna, add compact evidence-driven delegation/result guidance, and prepare
remaining worthwhile workflow work as planned T-008. The earlier analysis-only
restriction is superseded only for this routing/documentation scope.

The contract keeps `handoff.py`, its state and compatibility behavior intact.
Delegation type is semantic task prose; no STATUS schema, dispatcher, global
model switch, AI accounting change or new runtime framework is introduced.

## Routing contract

- GUI / Sol owns problem and scope, acceptance criteria, architecture, material
  alternatives/trade-offs, project direction, final review/acceptance and next
  step.
- CLI / Luna defaults to bounded COLLECT, VERIFY, RESEARCH and previously
  approved EXECUTE work. DECIDE is reserved for GUI. The task states
  `Decision authority: GUI`.
- CLI may interpret evidence and recommend options. It completes useful safe
  bounded work before escalating; material scope, architecture, direction,
  trade-off, consequential evidence conflict or permission-boundary questions
  return to GUI.
- Return a compact dossier with exact evidence provenance. GUI checks decisive
  evidence and the scoped diff, widening review only when risk, drift or
  missing provenance warrants it. Preserve unknowns and upstream verdicts.
- Profiles remain recommendations unless runtime confirms them. No model
  availability, cost or quality savings are claimed.

## Changes and acceptance mapping

| Acceptance area | Implementation |
|---|---|
| Responsibility, authority, work types and escalation | `AGENTS.md`; routing and delegation sections in `docs/CODEX_WORKFLOW.md` |
| Compact evidence-driven result without replacing lifecycle guarantees | `docs/CLI_DELEGATION_TEMPLATE.md`; existing `scripts/handoff.py` result/provenance grammar retained |
| Reusable task and result shape | `docs/CLI_DELEGATION_TEMPLATE.md` |
| Remaining recommendations deferred without implementation | [T-008 / #32 plan](T-008-workflow-optimization.md) |
| Backlog traceability | T-006 and T-008 rows in `docs/BACKLOG.md` |

The report evidence is from the accepted local analysis snapshot; it established
the value of reusing current handoff protections and the need to preserve
upstream statuses and uncertainty. This documentation task did not re-run its
historical research or claim engine/runtime evidence.

## Validation, boundaries and limitations

The CLI receipt for this preparation records the exact handoff suite,
synthetic-template lifecycle, routing consistency, acceptance matrix and
privacy checks. Those checks validate documents/helper compatibility only;
they do not create runtime model switching or prove that prose fields are
truthfully followed. `handoff.py` hashes support integrity, not truth or
independent review.

The routing preparation changed only the declared routing documents and plan
records. GUI separately corrected the small template issue described below.
Helper/test code, model/global configuration, decisions, product source and
live CK3 state remain unchanged. The publication updated and closed #28 as
completed while preserving its original analysis-only request verbatim. T-008
/ #32 remains open and planned for a new-session evidence review; no
implementation began. The Wiki now links the routing guide and lists T-006
once in its T cost detail and aggregate. Repository and Wiki commit IDs are
recorded in the private publication receipt.

## GUI disposition

GUI independently reviewed the routing diff, reusable template, T-008 limits
and acceptance mapping. All 13 requested criteria are satisfied after two
small corrections. The original CLI receipt remains historical CHANGES
REQUIRED: its substantive dossier was in the administrative directory rather
than the owned output path, and one template sentence disallowed supported
plan amendments. GUI preserved the original result and outputs, copied the
dossier to its declared path, clarified the existing amendment procedure and
added a required-deliverable path/existence reminder. No original receipt was
rewritten or force-rebased. Corrected source is accepted through a separate
GUI review record.

Fresh GUI validation: all 36 existing handoff tests passed; the corrected
result template passed create/claim/progress/complete/consume/validate in a
disposable fixture. Scoped diff whitespace, local links, privacy and unchanged
helper/test hashes were checked. Self-review remains separate from GUI
acceptance; legacy frozen tasks and planless compatibility remain intact.

Recovery lesson: nullable output provenance is not proof that a required
artifact exists; derive output paths and revisions from STATUS, and inspect
required deliverables. Model routing is an instruction contract, not runtime
enforcement. Saved execution evidence confirms the routing preparation used
Luna; no blanket cost/quality improvement is inferred.

## Saved-session cost verification

GUI inspected one saved GUI session and two CLI sessions, mapped their exact
turns and deduplicated 108 own response IDs. Existing accounting tooling and
an independent direct sum agree. The interrupted attachment mislabeled T-007
was preparatory work for this same corrected scope, is identified separately
in the private turn mapping and is not charged to completed T-007. A bounded
linked-parent review-session search found no matching automatic-review session;
an unrelated guardian session was excluded. Coverage remains partial rather
than inventing review usage.

The finite evidence cutoff is 2026-10-23T13:35:00.379783+00:00; later accounting, documentation
integration and publication are excluded. Maximum recorded request input was
187,645 tokens; aggregate cache-write input was zero. Request-level context
distribution and service-tier detail are unavailable. At 2026-10-23
Standard short-context rates, measured API-equivalent token cost is about
**$1.74**: Sol $1.69, Luna $0.06. This is a reference estimate,
not actual subscription spend or a claim about processing-tier billing.
[Official pricing](https://developers.openai.com/api/docs/pricing?latest-pricing-expanded=true)
provides per-million uncached/cached/output rates of $2/$0.10/$10 for
GPT-6.1 Sol and $0.10/$0.01/$0.50 for GPT-6 Luna. Unknown future or missing
usage is not zero; no unavailable component overrides a known USD total.
Publication did not recursively extend the accounting cutoff.


<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| gpt-6-luna | 3649643 | 3541632 | 108011 | 24041 | 6602 | 3673684 | partial |
| gpt-6.1-sol | 6566510 | 6210048 | 356462 | 35164 | 4497 | 6601674 | partial |
| **Total** | 10216153 | 9751680 | 464473 | 59205 | 11099 | 10275358 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-23T13:35:00.379783+00:00. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
Partial measured saved GUI/CLI responses through the frozen cutoff; later accounting/integration excluded. Cached input and reasoning output are subsets. No matching linked automatic-review session found in bounded parent search; no fabricated N/A or model mapping.
<!-- ai-cost:end -->
