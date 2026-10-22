# Backlog

M0 tasks are tracked in [GitHub Issues](https://github.com/mhaduk/ck3-dynasty-map/issues).
This document preserves sequencing, dependencies and a status snapshot; keep it
synchronized with Issues. Later milestones remain planned here until migrated.
IDs such as R-002 are stable planning IDs, separate from GitHub issue numbers.

## Project tooling

| ID | Priority | Work item | Status |
|---|---|---|---|
| [T-002 / #24](https://github.com/mhaduk/ck3-dynasty-map/issues/24) | P1 | Per-model historical token accounting and close-time workflow proposal | Complete locally — [accepted result](tasks/T-002-task-ai-cost.md); 11 verified remote tables, 10 local mirrors, 27 offline tests; partial coverage. Configuration proposal unapplied; scoped Git publication authorized 2026-10-22; #24 closure excluded |
| [T-001 / #23](https://github.com/mhaduk/ck3-dynasty-map/issues/23) | P0 | Incrementally improve per-ID parallel CLI handoffs, context/routing, log analysis and feedback | Complete — [canonical record](tasks/T-001-agent-workflow-optimization.md); GUI accepted both corrected stages on 2026-10-22; 37 offline tooling tests passed. Scoped publication authorized; receipt in #23. Savings unmeasured; F-001 paused |

## M0 — Research & bootstrap

| ID | GitHub issue | Priority | Work item | Depends on | Status |
|---|---|---|---|---|---|
| R-001 | [#1](https://github.com/mhaduk/ck3-dynasty-map/issues/1) | P0 | Record installed CK3 version and DLC/playset baseline | — | Complete — environment inventory; see RESEARCH.md |
| R-002 | [#2](https://github.com/mhaduk/ck3-dynasty-map/issues/2) | P0 | Inspect current `gfx/map/map_modes/map_modes.txt` | R-001 | Complete — native definitions inspected; custom loading/runtime unverified |
| R-003 | [#3](https://github.com/mhaduk/ck3-dynasty-map/issues/3) | P0 | Inspect installed map-mode GUI, unavailable UI and activation/refresh/exit hooks | R-001 | Complete — static GUI/type inspection; runtime gates open |
| R-004 | [#4](https://github.com/mhaduk/ck3-dynasty-map/issues/4) | P0 | Generate `script_docs` and `dump_data_types` | R-001 | Complete — clean script_docs and dump_data_types generated |
| R-005 | [#5](https://github.com/mhaduk/ck3-dynasty-map/issues/5) | P0 | Verify local-player/Dynasty scopes, validity guards and active-context invalidation/restore hooks | R-003,R-004 | Partial — FINAL GUARDS A passed for tested observer UI path; direct invalid-root safety and restore remain open; no-Dynasty player UI deferred to R-013 |
| R-006 | [#6](https://github.com/mhaduk/ck3-dynasty-map/issues/6) | P0 | Verify county -> holder -> dynasty transitions | R-004 | Complete — clean generated scope links verified; no runtime claim |
| R-007 | [#7](https://github.com/mhaduk/ck3-dynasty-map/issues/7) | P0 | Verify `any_liege_or_above` in target build | R-004 | Partial — clean documented traversal verified; runtime pending |
| R-008 | [#8](https://github.com/mhaduk/ck3-dynasty-map/issues/8) | P0 | Verify county -> de-jure baronies iterator | R-004 | Partial — iterator signatures verified; filtering/runtime pending |
| R-009 | [#9](https://github.com/mhaduk/ck3-dynasty-map/issues/9) | P0 | Verify barony color writes, dummy-title side effects and exit/restore behavior | R-002,R-004 | Partial — title RGB serialization/restore gaps remain. Binary follow-up supports a county-selector hypothesis with two decision-carried predicates; simultaneous area fill, empty state, coverage and context/clear unverified. Three-category and All Dynasties input gaps remain; ADR-009 excludes decision/council carrier route; no probe/runtime stage |
| R-010 | [#10](https://github.com/mhaduk/ck3-dynasty-map/issues/10) | P1 | Confirm additive/minimal original GUI integration, unavailable UI and dependable refresh path | R-003 | Partial — placement/basic/Faith smoke and R-005 watcher evidence; raid/barter guards, full parity/refresh/restore open |
| R-011 | [#11](https://github.com/mhaduk/ck3-dynasty-map/issues/11) | P1 | Capture vanilla error-log baseline without mod | R-001 | Partial — clean startup log empty; save/map interaction and archive pending |
| R-012 | [#12](https://github.com/mhaduk/ck3-dynasty-map/issues/12) | P1 | Install/configure CK3 Tiger locally | R-001 | Ready |
| R-013 | [#13](https://github.com/mhaduk/ck3-dynasty-map/issues/13) | P2 | Establish a supported no-Dynasty local-player fixture and verify unavailable UI | R-005 | Deferred — engine rejects the one-attempt player lowborn fixture; no further fixture iteration now |
| R-014 | [#14](https://github.com/mhaduk/ck3-dynasty-map/issues/14) | P1 | Inventory CK3 modding documentation and source hierarchy; create and integrate a concise source map | R-001,R-004 | Complete — [source map](CK3_SOURCE_MAP.md) and agent/workflow integration |
| R-015 | [#15](https://github.com/mhaduk/ck3-dynasty-map/issues/15) | P1 | Investigate Clerical Regions renderer, custom membership/colors/stripes and isolation | R-001,R-004 | Closed — not planned (2026-10-21); [final disposition](tasks/R-015-clerical-regions.md#final-disposition--2026-10-21). Independent provider not demonstrated; technical evidence partial; no probe/runtime |
| R-016 | [#16](https://github.com/mhaduk/ck3-dynasty-map/issues/16) | P0 | Validate historical My Dynasty pipeline with county semantics, fixed barony colors and manual refresh | R-002,R-004,R-005,R-009,R-010,R-014; reuse R-006/007/008 | Closed research with limits — 1.20.1.2 startup and three-view execution gates passed; user reports ordinary switching/refresh/native-return smoke appears to work. Grey nonmatching land failed visual acceptance; semantic coverage, performance, atomicity/context safety and persistence/removal remain open. [Canonical closeout](tasks/R-016-my-dynasty-pipeline.md#final-disposition--2026-10-21); published and #16 closed as completed research |

Initial migration verified 2026-10-20, before adding R-013: R-001 / #1, R-002 / #2, R-003 / #3, R-004 / #4 and R-006 / #6 are
closed as completed; the other seven M0 issues remain open. Ready/Partial/Blocked
are progress descriptions in issue bodies, not claims of native GitHub states.
Subsequent disposition: R-015 / #15 closed as not planned on 2026-10-21; its
technical findings remain partial.

### Successor definitions and plans

| ID | Work item | Depends on | Status |
|---|---|---|---|
| [R-017 / #19](https://github.com/mhaduk/ck3-dynasty-map/issues/19) | Select reproducible test character/start year and natural relationship fixtures for all three views | R-016; ADR-010 | Complete — scenario-selection stage: three bookmark starts selected (Ismail 867, William 1066, Murchad 1066). Runtime chains and remaining family/comparator coverage are for later tests; see [roster and locators](tasks/R-017-test-scenario-selection.md) |
| [F-001 / #20](https://github.com/mhaduk/ck3-dynasty-map/issues/20) | Specify Dynasty entry, active subviews, selection, legend, contrast and grey-ground visual/interaction contract | R-016,R-005,R-009,R-010,R-013; ADR-008/009/010 | Planned — [UX plan](tasks/F-001-dynasty-map-ux.md); grey visibility is P0 acceptance |
| [F-002 / #21](https://github.com/mhaduk/ck3-dynasty-map/issues/21) | Evaluate Dynasty/House/CoA/title color sources and fallback contract | R-009,R-016; ADR-010 | Planned — [color strategy](tasks/F-002-dynasty-color-strategy.md); fixed palette remains fallback and work is independent of F-001 layout/grey diagnosis |
| [F-003 / #22](https://github.com/mhaduk/ck3-dynasty-map/issues/22) | Define Dynasty subview behavior and semantic category roles | R-016; ADR-010 | Complete — [behavior reference](tasks/F-003-dynasty-subview-definitions.md); defines selection, classification and Primary/Secondary/Neutral result roles; F-001 owns visual treatment and F-002 color-source/fallback |

These plans are separate backlog records, not implementation or runtime
authorization. Existing F-101 through F-110 IDs remain stable; their older
holder-first wording is historical planning context and must be mapped to the
current ADR-010 views when a successor is scoped, never renumbered in place.

Latest [FINAL GUARDS result](evidence/2026-10-20-r005-player-context/final-guards-result.md)
and [canonical R-005 checkpoint](tasks/R-005-player-context.md) supersede older
next-test instructions in this section and in dated evidence. A passed the
bounded displayed UI path into observer after RESET; it does not establish
direct invalid-root safety or universal transition-race safety. B's one-shot
`set_to_lowborn` fixture was rejected on the player character and Dynasty
remained present. R-013 owns the deferred local-player/no-Dynasty UI case; do
not iterate on fixtures or repeat V1–V3 or passed lifecycle cases. R-005 remains
partial. R-009 owns color restoration; R-010 owns native-menu parity/refresh.
The no-Dynasty courtier guard and observer UI are not proof of a local player
without a Dynasty.

## v0.1.0 — My Dynasty MVP

| ID | Priority | Work item | Depends on |
|---|---|---|---|
| F-101 | P0 | Create launcher-generated local mod skeleton | R-001 |
| F-102 | P0 | Historical dummy color-source candidate; hold pending R-009 color-input decision | R-009,F-101 |
| F-103 | P0 | Add custom barony-color map definition | R-002,F-101 |
| F-104 | P0 | Resolve valid player Dynasty and implement ADR-008 unavailability/context-loss safety, including the deferred no-Dynasty player prerequisite in [R-013 / #13](https://github.com/mhaduk/ck3-dynasty-map/issues/13) | R-005,R-009,R-013,F-101 |
| F-105 | P0 | Implement `DIRECT` county classifier | R-006,F-104 |
| F-106 | P0 | Implement `CONTROLLED` via verified liege traversal, including no-Dynasty holders | R-006,R-007,F-104 |
| F-107 | P0 | Propagate county class to baronies through the R-009-approved color strategy | R-008,F-102,F-105,F-106 |
| F-108 | P0 | Integrate map-mode button, unavailable state and exit/restore | R-003,R-009,R-010,F-103,F-104,F-107 |
| F-109 | P1 | Add English localization | F-108 |
| F-110 | P0 | Implement dependable refresh: verified re-click or minimal explicit mechanism | R-003,R-010,F-108 |
| T-111 | P0 | Validate direct holder and cadet House cases | F-105,F-107 |
| T-112 | P0 | Validate nested foreign and no-Dynasty holders under dynastic lieges | F-106,F-107 |
| T-113 | P0 | Run Tiger and compare `error.log` with vanilla baseline | R-011,R-012,F-109,F-110,T-111,T-112,T-114,T-115,T-116,T-117 |
| T-114 | P0 | Validate valid activation and barony rendering, including dummy-title side effects | R-009,F-107,F-108,F-109 |
| T-115 | P0 | Validate unavailable activation: no player/no Dynasty, no classification/color writes, no all-neutral substitute; the no-Dynasty player case follows [R-013 / #13](https://github.com/mhaduk/ck3-dynasty-map/issues/13) | F-104,F-108,R-013 |
| T-116 | P0 | Validate manual refresh/re-activation after holder/liege changes | F-110,T-111,T-112 |
| T-117 | P0 | Validate active-context loss/player switching and exit/restore without color leaks | R-005,R-009,F-104,F-108 |

## v0.2.0 — Hardening

| ID | Priority | Work item | Depends on |
|---|---|---|---|
| U-201 | P1 | Add legend/tooltips for Direct/Controlled/Other | v0.1.0 |
| P-202 | P0 | Profile refresh with Script Profiler | v0.1.0 |
| P-203 | P1 | Compare naive barony scan vs county-first algorithm if needed | P-202 |
| E-204 | P0 | Test administrative government | v0.1.0 |
| E-205 | P1 | Test clan/tribal/theocratic/republic edge cases | v0.1.0 |
| E-206 | P1 | Harden no-Dynasty player UX/regressions while preserving ADR-008 unavailability; fixture/UI prerequisite follows [R-013 / #13](https://github.com/mhaduk/ck3-dynasty-map/issues/13) | v0.1.0,R-013 |
| E-207 | P1 | Harden observer/no-local-player UX and regression coverage beyond MVP guards | v0.1.0 |
| C-208 | P0 | Test save/load with map active | v0.1.0 |
| C-209 | P0 | Test adding/removing mod from existing save | v0.1.0 |
| C-210 | P1 | Document conflicts with map UI mods | v0.1.0 |
| L-211 | P2 | Add Polish localization | U-201 |

## v0.3.0 — All Dynasties

| ID | Priority | Work item | Depends on |
|---|---|---|---|
| A-301 | P0 | Reverse-engineer native House map semantics/color source | M0 |
| A-302 | P0 | Evaluate native grouping/reuse strategy | A-301 |
| A-303 | P0 | Prototype dynasty-head primary-title color fallback | A-301 |
| A-304 | P1 | Evaluate deterministic palette strategy | A-301 |
| A-305 | P0 | Select color strategy and record ADR | A-302,A-303,A-304 |
| A-306 | P0 | Implement All Dynasties classifier | A-305 |
| A-307 | P0 | Handle no-Dynasty holders | A-306 |
| A-308 | P0 | Test cadet Houses across independent/vassal realms | A-306 |
| A-309 | P1 | Test color stability after succession/new cadet branch | A-306 |

## v0.4.0 / v1.0.0

| ID | Priority | Work item |
|---|---|---|
| I-401 | P0 | Integrate both modes using current CK3 sub-mode UX if available |
| I-402 | P1 | Final icon/visual polish |
| I-403 | P0 | Full regression matrix |
| I-404 | P0 | Release compatibility checklist against current CK3 version |
| I-405 | P1 | Workshop metadata/screenshots |
| I-406 | P0 | Tag and publish `v1.0.0` |
