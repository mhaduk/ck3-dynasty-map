# Architecture Decision Records

## ADR-001 — County is the semantic unit

**Status:** Accepted
**Decision:** classify dynastic control at county level and propagate the result to baronies.

**Why:** barony holders include mayors, clergy and other local holding types that would visually fragment political dynastic control. The feature is intended to answer who rules the county and under whose dynastic realm it sits.

## ADR-002 — Controlled means any de-facto liege in the chain

**Status:** Accepted
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

**Boundary:** a county holder without a Dynasty still requires the de-facto
liege-chain check and can be CONTROLLED. DIRECT requires the county holder to
belong to the valid player's Dynasty.

**Validation:** v0.1 must cover valid activation, unavailable activation with no
classification/color writes, manual refresh/re-activation, active-context loss
and API-supported exit/restore. See TEST_PLAN.md.
