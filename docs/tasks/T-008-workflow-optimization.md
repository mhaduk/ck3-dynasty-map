# T-008 — Workflow optimization after routing

Status: **PLANNED — OPEN as [GitHub issue #32](https://github.com/mhaduk/ck3-dynasty-map/issues/32), not READY, not started**. Begin in a new session only after
T-006 routing is accepted and closed. Use the Sol → Luna → Sol contract from
T-006. No implementation or additional GitHub issue is authorized by this planning note.

## Goal

Select and implement the smallest useful follow-up that reduces repeated
evidence assembly and review effort while preserving distinct upstream
verdicts, evidence limits, user-only CK3 operations, privacy and permission
boundaries. Start with a bounded read-only COLLECT / VERIFY / RESEARCH phase on
Luna, return findings/options/recommendation to GUI, and wait for GUI to choose
scope. Any EXECUTE phase requires a separate explicit handoff and permission.

## Candidate scope for fresh prioritization

1. Compact read-only evidence report over existing results, with explicit
   completeness/unknown fields and no synthesized green PASS.
2. Cross-stage link validation for payload → install receipt → checkpoint →
   marker/schema → analyzer, retaining upstream statuses and mismatches.
3. Log profiles and finite checkpoint comparisons, with careful separation of
   new bytes, known message identity, count changes and unproven causality.
4. Structured preflight result using a stable output contract rather than
   parsing free-form stdout.
5. Explicit manifests/pins for already named inputs; no broad discovery or
   automatic live fallback.
6. Append-only archive/compare and sanitized summaries without migrating old
   archives or publishing automatically.
7. Parametric deployment and verified file rollback, only under a separately
   approved install scope and user-declared safe app state.
8. Other T-006 recommendations that remain useful after routing, subject to
   evidence and fresh prioritization.

The analysis suggested a thin report/link-validation layer first, then log
profiles/comparison, with deployment as a higher-risk separate permission
class. This is historical qualitative advice, not a binding decision. Recheck
dependencies, qualitative value/effort, revalidation cost and exclusion risk
before selecting one minimal iteration.

## Exclusions and dependencies

- No game automation, engine safety verdicts, causal attribution, release
  stripping, broad scans, automatic repair, publication or unapproved writes.
- No AI-accounting ledger implementation; T-002's existing proposal remains
  deferred and requires its own authorization.
- Reuse `handoff.py`, log capture, classification analysis and preflight where
  relevant; do not duplicate their functions or change semantics implicitly.
- Preserve user-only launch/load/save/character switching/testing and existing
  ownership, provenance, privacy, compatibility and review guarantees.
- T-006 acceptance and accounting are prerequisites. Each selected
  implementation needs its own frozen inputs, owned paths, checks, permissions
  and GUI-supplied execution plan.

## Readiness criteria

T-008 can be scoped only when a new-session evidence review identifies a
specific repeated cost, a bounded candidate with named existing inputs,
acceptance cases that preserve upstream verdicts/unknowns, a privacy and
permission plan, and an explicit GUI choice of the first iteration. Keep
remaining candidates planned until separately selected.
