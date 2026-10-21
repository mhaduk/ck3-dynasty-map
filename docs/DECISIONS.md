# Architecture Decision Records

## ADR-001 — County is the semantic unit

**Status:** Accepted
**Decision:** classify dynastic control at county level and propagate the result to baronies.

**Why:** barony holders include mayors, clergy and other local holding types that would visually fragment political dynastic control. The feature is intended to answer who rules the county and under whose dynastic realm it sits.

## ADR-002 — Controlled means any de-facto liege in the chain

**Status:** Accepted

**Scope clarification (ADR-010, 2026-10-21):** this holder-first rule is
Dynasty Holdings; it is not the universal rule for all Dynasty views.

**Decision:** a county is `CONTROLLED` when its holder is not in the player's Dynasty but at least one de-facto liege above the holder is.

**Example:** Count Wettin -> Duke Piast -> King Přemyslid yields `CONTROLLED` for a Přemyslid player Dynasty.

**Excluded:** tributary/suzerain relations are not treated as lieges for v1.0.

## ADR-003 — No persistent graph/cache for MVP

**Status:** Accepted
**Decision:** recompute on demand using engine scopes/iterators.

**Why:** the ordinary hierarchy is expected to be shallow and historical references describe `any_liege_or_above`; target-build behavior must be verified during M0. A cache creates more invalidation paths than useful performance value until profiling proves otherwise.

## ADR-004 — Static refresh first

**Status:** Accepted
**Decision:** v0.1 and v0.2 refresh only on map activation/manual refresh.

**Why:** prior map mods successfully used static modes; this avoids monthly global scans, global mode variables and event-invalidation complexity.

## ADR-005 — Avoid global variables where possible

**Status:** Accepted for v0.1 design; verify during implementation.
**Decision:** prefer separate named map-mode definitions and `IsMapMode(...)` UI state rather than multiplexing modes through a saved global variable.

**Why:** reduces save pollution and known observer/multiplayer concerns in older custom map implementations.

## ADR-006 — Do not copy vanilla files into Git

**Status:** Accepted
**Decision:** vanilla references remain local and gitignored. Only original mod files and documentation are committed.

**Why:** copyright hygiene and easier review of what the mod actually changes.

## ADR-007 — All Dynasties is gated by color strategy

**Status:** Accepted
**Decision:** do not commit to a persistent palette registry before checking native House-map behavior and simpler title-derived strategies.

**Why:** persistent mapping adds save-state, invalidation and maintenance complexity.

## ADR-008 — My Dynasty requires a valid player Dynasty in v0.1

**Status:** Accepted

**Decision:** My Dynasty is unavailable without a valid local player or valid
player Dynasty. Unavailable activation performs no classification or color
writes. Do not substitute an all-neutral map.

If player context becomes invalid while My Dynasty is active, stop using the old
Dynasty context and clear/restore visual state as far as the CK3 map-mode API
permits. Restoration cleanup is distinct from unavailable activation. The exact
UI disabling/hiding mechanism and context-invalidation/restore hooks are M0
research questions, not verified target-build APIs. This safety handling must
not introduce recurring world scans.

**Why:** neutral territory means a valid comparison found no dynastic control;
an unavailable comparison must not imply that territorial result or retain stale
Dynasty context.

**Boundary (Holdings; see ADR-010 for the other views):** a county holder without a Dynasty still requires the de-facto
liege-chain check and can be CONTROLLED. DIRECT requires the county holder to
belong to the valid player's Dynasty.

**Validation:** v0.1 must cover valid activation, unavailable activation with no
classification/color writes, manual refresh/re-activation, active-context loss
and API-supported exit/restore. See TEST_PLAN.md.

## ADR-009 — Custom maps use map-system interfaces

**Status:** Accepted — explicit user direction, 2026-10-21.

**Decision:** Dynasty Map must use the map subsystem's exposed configuration,
data inputs and view lifecycle. Decisions, council-task selectors, Situations
and synthetic or mutated religious regions are not accepted carriers for the
feature. Opening such a carrier from a map-menu button does not satisfy this
requirement. Normal GUI/script glue is acceptable only when it drives an actual
map-system interface rather than an unrelated gameplay subsystem.

**Consequence:** the R-009 decision-carried binary-selector hypothesis is
excluded from the product direction; do not prepare its proposed experiment.
R-015's independent map-provider question remains relevant, but religious-object
mutation is outside the accepted architecture. Prior technical findings remain
valid as bounded research history, not implementation recommendations.

At the ADR-009 decision checkpoint, no suitable independent classification
input had been demonstrated. R-016 later demonstrated the bounded native
baronies/title-RGB pipeline, with isolation/restore safety still unresolved.
Further work must identify a concrete map-native input and lifecycle contract
or report that the inspected target-build interfaces do not establish one.
Do not substitute another gameplay carrier or reduce product semantics to fit
one. Original G1/G2 requirements and ADR-001 through ADR-008 remain unchanged.

## ADR-010 — Three Dynasty views and their native map layout

**Status:** Accepted — explicit user direction, 2026-10-21.

**Decision:** one top-level **Dynasty** entry in the existing map menu. Its
active map panel offers **Dynasty Realms** first/default, **Dynasty Holdings**
second and **My Realm & Dynasty** third. Show the selected subview, its legend
and manual refresh. Native House/Dynasties modes remain native. All Dynasties
is deferred within R-016, without changing the wider goal.

For fresh valid player P, Dynasty D and county holder H, let S be all ordinary
de-facto seniors of H and T the highest ruler (H itself when independent):

| View | Dark green | Light green, only if not dark | Grey |
|---|---|---|---|
| Dynasty Realms | T belongs to D | H or any member of S belongs to D | Neither match, or unheld |
| Dynasty Holdings | H belongs to D | Any member of S belongs to D | Neither match, or unheld |
| My Realm & Dynasty | H = P or P is in S | H or any member of S belongs to D | Neither match, or unheld |

Dark takes precedence. The player's subtree includes vassals when P is itself
a vassal; siblings under P's top ruler are outside it. Cadet Houses compare
Dynasty identity. A lowborn holder still requires senior checks. County results
project to every constituent barony. De-jure claims, occupation and tributary/
suzerain relations do not enter classification; de-jure hierarchy is used only
for county-to-barony projection. Invalid P/D means unavailable and no work.

**Relationship to prior decisions:** ADR-002 and ADR-008's DIRECT/CONTROLLED
boundary define Holdings, not all three views. Their dated evidence and
ADR-008's unavailable/context-loss requirements remain intact. This decision
does not waive lifecycle, isolation, persistence/removal or atomic-entry gates.

**Refresh/layout candidate:** selecting Dynasty enters/recomputes Realms;
selecting a subview or Refresh recomputes its own result with fresh P/D.
Opening Additional Modes alone does not scan or reset the current alternative.
Separate named map definitions express selection, but share mutable barony RGB;
there are no three stored datasets or saved selection cache. The research
payload prepares ordinary activation plus explicit compute/display diagnostics.
Void Execute followed by SetMapMode has no success receipt: runtime wiring,
transition safety and final one-action UX remain unverified. Diagnostics alone
cannot satisfy the target UX. Direct colors are 25/105/50, 145/220/150 and
65/70/80; historical Holdings sample/copy colors remain separate diagnostics.

F-003 consolidates the accepted ADR-010 subview behavior and semantic
category-role definitions in one
[reference](tasks/F-003-dynasty-subview-definitions.md); it changes no rule or
English label. F-001 owns visual treatment; F-002 owns color-source/fallback.
In particular, the third view remains My Realm & Dynasty.
