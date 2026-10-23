# T-004 — Standardize issue title convention

Status: COMPLETE, 2026-10-23. Tracking: [T-004 / #26](https://github.com/mhaduk/ck3-dynasty-map/issues/26).

## Outcome

The canonical project issue title is `<ID> — <concise title>`, where IDs retain their R/F/T/B category prefix. Redundant textual categories such as `research:`, `feature:`, `feat:`, `task:`, `chore:` and `bug:` do not precede the ID. GitHub type labels remain useful metadata. CONTRIBUTING commit-message examples remain unchanged because they describe commits, not issue titles.

AGENTS.md points to the detailed workflow rule. CODEX_WORKFLOW.md defines the rule, and project setup plus research, feature and bug templates align with it using replaceable R-XXX, F-XXX and B-XXX placeholders. Inspection found no script or test that generated or parsed issue titles, so no automation or prose-only test was added. Existing issue titles, IDs, semantics and unrelated issue bodies were not mass-edited.

## Acceptance evidence

- Configuration and project setup specify `<ID> — <title>` and prohibit redundant category text.
- The three issue templates use the matching ID category and tell users to replace the placeholder with the next verified stable ID.
- Existing type labels remain intact; commit prefixes in CONTRIBUTING are unchanged.
- No title automation dependency was found. Static template, link, and acceptance checks are recorded in the publication receipt.
- Issue #26 was updated with the evidence and closed completed after the repository documentation and Wiki publication were verified. No GUI review is claimed by the CLI stage.

## Wiki AI-cost refresh and limits

The published Wiki Home retains its other two sections and its two-table AI-cost section. Inventory cutoff is the #26 completion on 2026-10-23. Closed issue counts are R=15, T=4, F=0, B=0; T includes #26. T-003 has no tracking issue and is not counted as an invented closed task. Open F-001 is excluded. T-004's measured total, cached tokens and API-equivalent estimate are N/A because no attributable usage counters for this CLI work were available at the finite cutoff; this is not zero.

Known-model estimates were recomputed from existing measured model counters using official Standard short-context prices checked 2026-10-23: gpt-6.1-sol $2 / $0.10 cached / $10 per million input / cached input / output; gpt-6-luna $0.10 / $0.01 / $0.50. The resulting known-model estimates are R $30.77 and T $8.34; unpriced model buckets remain excluded and visible in coverage notes. Historical token totals and cached-token counts are unchanged. Estimates describe measured usage only, are not subscription spend or lifetime task cost, and omit unavailable request-level context, cache-write, service-tier and missing-history details. Source: [official OpenAI API pricing](https://developers.openai.com/api/docs/pricing), checked 2026-10-23.

## Stage evidence

- Observation: #26 was OPEN with all acceptance boxes unchecked; local T-003 history described the published estimate as $15.38 R / $4.17 T and the backlog incorrectly said no publication / USD N/A.
- Cause: issue-template defaults retained textual prefixes, configuration omitted the stable title shape, and the backlog reflected the initial T-003 feasibility checkpoint rather than its later publication.
- Recovery: aligned instructions/templates, corrected the stale T-003 status, recalculated the Wiki at the current official Standard rates, and verified the issue and Wiki readbacks.
- Outcome: issue #26 closed completed after the repository commit and Wiki publication; the CLI publication receipt is retained in the private handoff record.
- Reusable improvement: inspect the exact named handoff before using older task journals, and refresh published price-derived values when the official rate tier changes.

## Scope limits

No issue title or unrelated issue body was changed. No automated title parser existed, so the criteria requiring parser changes and tests were not applicable. No game, mod, launcher, test playset, or runtime work was performed. The incomplete and paused F-001 status and all research gates remain unchanged.
