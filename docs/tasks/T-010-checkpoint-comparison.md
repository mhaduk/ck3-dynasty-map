# T-010 — Finite checkpoint comparison

Status: **PLANNED — next area selected on 2026-10-23; not READY**.
Planning only; no implementation, live capture or GitHub issue is authorized.
Predecessors: [T-008](T-008-workflow-optimization.md) and
[T-009](T-009-structured-preflight.md).

## Why this area next

The earlier seven-candidate analysis rated finite log profiles/comparison as
potentially valuable, with substantial attribution risk. Historical audit and
counter-diagnosis receipts repeatedly assembled interval/reset gaps, pins,
observed messages and counts manually. T-008 now provides inventory integrity
and selected statuses; T-009 adds structured preflight evidence. The next useful
question is what changed between two explicitly named finite checkpoints.

Choose a narrow read-only comparison before broader profiles. Current
ck3_log_delta.py already reports interval/expectation/observation states,
checkpoint and baseline IDs, captured byte counts and error summaries. Reuse
those contracts rather than build another log parser. Actual maintenance cost,
frequency and savings remain unmeasured; this is a qualitative prioritization.
Full semantic stage-chain validation is deferred because deployment receipt
and payload identity contracts still need separate scope. Deployment/rollback
remains a distinct higher-risk permission class.

## Proposed minimal iteration

Compare exactly two explicitly pinned saved checkpoint manifests/reports.
Do not open or parse raw logs in the first iteration. Report each input's
original completeness, IDs and limits, then separate:

- newly captured byte ranges, only when boundaries/generation are comparable;
- observed message identity, only to the extent the existing summary preserves
  an adequate identity; matching counts alone do not establish identity;
- per-message or aggregate count differences with their scope/comparability;
- causal attribution, always UNPROVEN by this file comparison.

Missing fields, resets, partial lines, truncation, caps, optional gaps,
unsupported formats and uncertain generation/identity must stay visible. A
missing or filtered message is UNKNOWN, not proof of disappearance. Never
subtract unequal windows and call the result new errors, nor promote source
INCOMPLETE to a clean comparison. Prefer partial useful observations plus
explicit non-comparability over inventing a universal verdict.

## Preparation and tests to freeze before EXECUTE

Use one bounded CLI contract review over named current log helper/tests,
inventory guide and two copied small saved manifest examples. GUI chooses
exact supported fields, identity/comparability rules and the smallest output
contract from that evidence. If summaries lack a reliable field, mark it
UNKNOWN or return the gap; do not expand automatically into raw-log analysis,
normalization, live capture or a new profile framework.

Future synthetic cases must include comparable adjacent and overlapping
windows, unrelated baselines/generations, reset/truncation, complete versus
required/optional gaps, same message with changed count, different messages
with equal counts, absent/filtered identity, unknown schema, stale pins and
privacy sentinels. Exact expected non-claims and preservation of upstream
verdicts are acceptance criteria. Retain existing helper/report regressions;
public-only tests cannot depend on ignored historical artifacts.

## Routing, permissions and stop conditions

GUI owns scope, comparability semantics, trade-offs and acceptance. Recommend
Luna / Medium for bounded evidence collection and any subsequently approved
implementation; runtime selection must be confirmed separately. A future
EXECUTE needs a new frozen per-ID handoff with exact inputs, owned paths,
checks and GUI-supplied execution plan. No worker starts from this plan.

Offline named manifests only; no raw logs, save/dump, real game/app/process/UI,
new capture, install/rollback, repair/repin/migration, automatic discovery,
publication or external message. Do not copy raw message text or machine paths
into public output; freeze a sanitized allowlist. F-001 remains paused.
If identity/generation cannot be established from supplied metadata, stop the
dependent comparison and return UNKNOWN/evidence needed, without inventing a
fixture pass or requesting another game test. No completion/accounting claim.

## Evidence and recovery lesson

Basis: accepted T-008 candidate analysis and repeated reset/pin/count work in
its named historical examples, plus the current helper's explicit summary
fields. T-009 review also showed that passing happy-path tests missed combined
incomplete/defect and malformed-type cases. Include these negative combinations
at initial scope freeze. Short GUI planning avoids a redundant research cycle;
exact schema/comparability verification remains the next bounded CLI stage.
