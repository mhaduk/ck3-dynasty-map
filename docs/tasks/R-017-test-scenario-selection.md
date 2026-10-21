# R-017 — Test scenario and start selection plan

Issue: [#19](https://github.com/mhaduk/ck3-dynasty-map/issues/19).

Status: PLANNED. No character/year recommendation has been researched or
verified. R-016 retains Harold 1066 as the historical baseline; it is not
presumed to be the best broad-coverage fixture.

## Goal

Choose one reproducible legal start and, only if needed, one complementary
start that exposes useful natural Dynasty relationships for the three ADR-010
views. Prefer a landed family and a broad Dynasty so territorial differences
are visible, while judging fixture quality by actual relationship coverage,
not Dynasty size alone. This task selects scenarios; it does not mutate a save,
force family relationships, or require a broad runtime matrix before R-016
research closeout.

## Selection method and evidence

1. List candidate characters, start dates, installed DLC requirements and
   available legal bookmark/start routes. Record source and build/date for each
   fact; do not present a remembered or inferred historical candidate as
   confirmed.
2. Score candidates against natural, inspectable county fixtures and the
   relationship cases below. Prefer a single start that covers the most
   discriminating cases; add at most one complementary start for important
   missing cases.
3. Record a reproducible setup: bookmark/date, character, game rules and DLC
   prerequisites, pause point, and how to locate each county/holder chain
   without editing the save.
4. Keep Harold 1066 results as the comparison baseline. Any new candidate is
   additional evidence with its own provenance, not a replacement for the
   existing report.

## Fixture expectations

P = player, D = player's Dynasty. Dark takes precedence; each senior below
is in the actual de-facto chain, not merely an immediate liege. Other-Dynasty
rulers are foreign for this comparison.

| County holder / de-facto chain | Realms | Holdings | My Realm & Dynasty | Why it matters |
|---|---|---|---|---|
| P's held county, P independent | Dark | Dark | Dark | Direct/independent baseline |
| D count → foreign king, outside P subtree | Light | Dark | Light | Dynastic subordinate |
| Foreign count → D duke (not P) → foreign king | Light | Light | Light | Intermediate senior counts |
| Foreign count → P duke → foreign king | Light | Light | Dark | Player-vassal subtree |
| Foreign sibling count → same foreign king as P duke, no D senior | Grey | Grey | Grey | Sibling excluded from player subtree |
| Independent D relative holding county | Dark | Dark | Light | Independent family member outside P subtree |
| Foreign count → independent D relative ruler | Dark | Light | Light | Relative's foreign vassal |
| Foreign count → independent P ruler | Dark | Light | Dark | Player's foreign vassal |
| Foreign holder/foreign-only chain, outside P subtree | Grey | Grey | Grey | Neutral comparison |
| Lowborn holder → independent D senior outside P subtree | Dark | Light | Light | Missing holder Dynasty still checks seniors |
| Cadet-House D count → foreign king, outside P subtree | Light | Dark | Light | Dynasty identity across Houses |
| Unheld county | Grey | Grey | Grey | Holder guard and projection |

The table describes expected county categories; every barony in each selected
county must show that county's category. Missing natural cases are explicitly
untested. Do not manufacture a result by assuming a family tie from names or
House labels; verify the relevant Dynasty and liege chain from game state.

## Deliverables and stop conditions

- A sourced recommendation for one primary start and no more than one
  complement, plus a scorecard of coverage and missing cases.
- A reproducible setup and fixture locator table tied to the three-view
  expectations above, including native-view reference and manual-refresh/state
  change requirements for later validation.
- Explicit DLC/accessibility and uncertainty notes. If no candidate has
  adequate evidence, return the missing evidence question rather than claiming
  an ideal fixture.

Out of scope: R-016 reruns, save mutation, forced family fixtures, broad
runtime testing as a closeout prerequisite, implementation, and changing
ADR-010 semantics. R-017 does not begin until separately selected as the active
backlog task.

Accepted behavior/category-role reference: [F-003](F-003-dynasty-subview-definitions.md).
