# T-003 — GitHub Wiki feasibility and content preparation

Selected by the user on 2026-10-22. Status: COMPLETE — feasibility review,
three-section draft and live Wiki publication accepted by GUI on 2026-10-22.
Target: [mhaduk/ck3-dynasty-map Wiki](https://github.com/mhaduk/ck3-dynasty-map/wiki).
No GitHub issue was created. The user separately authorized Wiki publication
and repository commit/push on 2026-10-22.

## Goal

Determine whether a project wiki can be created and maintained at the target
repository, what repository/account permissions and setup it requires, and
prepare a reviewable draft for three requested sections:

1. **Assumptions and definitions** — explain the three map views/types using
   the accepted project definitions, clearly distinguishing settled semantics
   from research limits and future plans.
2. **Screenshots and guide** — mark the guide as TODO. Include a temporary
   screenshot candidate showing the green/grey map split from the
   user-supplied `user-comparison-3.png`; preserve provenance and review its
   suitability before any public upload.
3. **AI cost estimates** — summarize AI-cost sections for closed tasks, grouped
   by task prefix R, T, F and B. Put one four-row summary table first, then
   task-level details grouped in the same order. Report total tokens, cached
   input tokens, and estimated USD cost.

## Evidence and accounting rules

- Start from the T-002 accepted historical method, but refresh the closed-task
  inventory and verify current source descriptions/records before finalizing.
  Do not assume T-002's older issue inventory is still current.
- Include only tasks confirmed closed at the documented cutoff. Use stable
  planning task IDs and their leading type letter. Report closed work without a
  stable R/T/F/B task ID separately as unclassified; never force it into a
  group. Exclude open tasks, including F-003 if it remains open, and explain
  exclusions. A zero-row type means no eligible closed task was found, not a
  measured zero-cost task.
- Use `AI cost` entries as the evidence source for task totals and cached input.
  Preserve partial/unavailable coverage and unknown model buckets. Do not
  present measured partial usage as the complete lifetime cost of a task.
- Estimate USD from verified model-specific input, cached-input and output
  prices, using the correct units and a stated price effective date/source.
  Cached input is a subset of input: apply cached pricing only to that subset,
  and never add it to the total token count. Label the result an estimate for
  measured covered usage. Unknown model pricing remains N/A or a clearly
  bounded range; do not invent a price. State whether reasoning output is
  already included in output pricing. Do not infer subscription or quota cost.
- Keep the summary rows exactly R, T, F, B. Include columns for task count,
  measured total tokens, cached input tokens, estimated USD and coverage.
  The detail tables must also show task ID/title, total tokens, cached input,
  estimated USD and coverage; retain model detail where needed to make the
  estimate auditable.
- Use only sanitized aggregate data in proposed public pages. No raw session
  records, prompts, local paths, private IDs or credentials.

## Permissions and limits

The feasibility stage was read-only GitHub research plus local draft
preparation. A later user authorization permitted editing the existing Wiki
Home page. The guide remains TODO and the temporary screenshot candidate was
not uploaded. A subsequent user authorization permitted committing and
pushing the T-003 repository documentation changes. Do not access the CK3 game
UI.

## Deliverables

- A concise feasibility report: wiki enabled/disabled/unknown, evidence and
  access limitations, required permissions/setup, supported page workflow,
  and a clear recommendation for the next step.
- A local Markdown draft suitable for the wiki with the three requested
  sections, TODO guide text and temporary screenshot candidate.
- Reproducible aggregate and task-level token/cached-token/USD tables, with
  source cutoff, formulas, prices and limits.
- A short provenance/privacy check for screenshot and public aggregates.

## Acceptance

- `wiki-capability`: current repository wiki capability and observed access
  are evidenced; unknowns are not guessed.
- `definitions`: all three views and limits agree with canonical definitions.
- `screenshot-draft`: guide is marked TODO and the green/grey user screenshot
  is represented as a temporary candidate, not uploaded.
- `inventory-and-groups`: eligible closed tasks are current at cutoff and
  grouped R/T/F/B; unclassified closed work and exclusions are explicit.
- `cost-reconciliation`: total/cached tokens reconcile to source tables and
  USD estimates use cited dated prices with unknowns/partial coverage shown.
- `draft-privacy`: page draft contains no private session data or local path.
- `no-remote-writes`: no GitHub/wiki/repository mutation, staging, commit,
  push or publication occurred.

## Final disposition — 2026-10-22

Read-only repository metadata confirms `has_wiki=true`; authenticated
permission flags indicate admin/push. This does not establish that the Wiki
has been initialized or that pages already exist: the Wiki URL redirected to
the repository, and read-only `.wiki.git` lookup returned Repository not
found. Keep initialization as unknown until a separately authorized setup.

The three-section draft passed GUI review. It follows F-003 semantics, marks
the guide TODO and used the user-supplied green/grey comparison as a temporary
relative image candidate. The screenshot is appearance reference only; its
clipped UI and incomplete metadata review meant a cleaned/exported copy would
need review before upload. The published guide remains TODO and the image was
not uploaded.

At the 2026-10-22T16:38:31Z inventory cutoff, the categorized closed-task
subtotal was 134,866,114 measured tokens and 130,108,032 cached input tokens:

| Type | Closed tasks | Measured total tokens | Cached input tokens | USD estimate | Coverage |
|---|---:|---:|---:|---|---|
| R | 9 | 106,527,859 | 102,845,824 | N/A | Partial |
| T | 2 | 28,338,255 | 27,262,208 | N/A | Partial |
| F | 0 | N/A | N/A | N/A | No eligible closed tasks |
| B | 0 | N/A | N/A | N/A | No eligible closed tasks |

Unclassified closed chore #17 adds 3,976,814 measured tokens and 3,786,112
cached input tokens, for 138,842,928 total and 133,894,144 cached across all
12 closed issues. Every included AI-cost table has partial coverage and the
same earlier counter cutoff, 2026-10-22T13:15:22Z. At initial draft time USD
was N/A because no applicable Codex credit-to-USD billing basis was
established. After the user clarified that the desired metric was an
API-equivalent estimate, the then-current model rates were applied to known
model usage. On 2026-10-23 the official Standard short-context API rates were
rechecked (Sol: $2 input / $0.10 cached input / $10 output per million; Luna:
$0.10 / $0.01 / $0.50). Independent recomputation confirms the published
known-model estimates remain R $15.38 and T $4.17. F/B remain N/A (no eligible
closed tasks). The separate lower “All models” tier was not used. The per-task
table includes the unclassified #17 estimate of $0.06 as its own row; the
2026-10-23 Standard-rate check confirms it. These are rough API-equivalent estimates for
measured usage, not subscription cost or complete lifetime task cost; token
coverage remains partial. The user then requested that the AI-cost section
contain only the two tables. The published section now has a four-row R/T/F/B
summary table followed by a detailed per-task table, without method,
assumptions or explanatory prose. The other two Wiki sections remain intact.

The existing Home page was saved through the GitHub Wiki editor and the
published page was verified after save. The 2026-10-23 T-004 publication
rechecks the current closed-task inventory and official Standard rates; the prior R/T known-model totals remain
unchanged. T-004 itself has no attributable counters and is marked N/A.
Continue adding API-equivalent USD estimates when new AI-cost entries are
added, using their model and input/cached-input/output token counts.
