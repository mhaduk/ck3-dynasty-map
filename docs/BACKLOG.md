# Backlog

M0 tasks are tracked in [GitHub Issues](https://github.com/mhaduk/ck3-dynasty-map/issues).
This document preserves sequencing, dependencies and a status snapshot; keep it
synchronized with Issues. Later milestones remain planned here until migrated.
IDs such as R-002 are separate from GitHub issue numbers. Only verified GitHub issue titles allocate canonical IDs; older future-milestone IDs below are provisional unregistered planning references and must be registered/rekeyed before execution. See [verified registry](task-registry.json).

## Project tooling

T-005 is COMPLETE after substantive GUI review (2026-10-23); parent #27 is closed completed. Cross-chat receipt integration with F-001 is resolved by a new accepted reconciliation; original frozen evidence is preserved.
See [T-005 review](tasks/T-005-research-backlog-review.md) for eight dispositions, evidence and ownership.
Dated migration/checkpoint statements below retain their historical meaning.

| ID | Priority | Work item | Status |
|---|---|---|---|
| [T-007 / #31](tasks/T-007-task-registry.md) | P1 | Reconcile canonical task registry and enforce GitHub-first creation | Complete — canonical registry/guard and 88 tests accepted; T-003/#25 restored, frozen evidence retained, #31 closed and Wiki read back; partial cost $0.72286920; scoped repository commit/push subsequently authorized on 2026-10-25 |
| [T-023 / #49](tasks/T-023-independent-cli-review.md) | P1 | Add independent CLI review/correction loop before GUI acceptance | Complete — accepted shared workflow, 154 independent tests/102 probes; source and Wiki published; GUI-verified 182,839,219 tokens / $10.77585306 partial cost; #49 closed completed |
| [T-021 / #47](tasks/T-021-execution-review.md) | P2 | Add post-execution self-review and persistent GUI optimization triage | Complete — corrected implementation accepted; 70 independent tests; real inventory migration and report triage; partial cost $0.95229018; scoped publication authorized |
| [T-013 / #34](tasks/T-013-wiki-cost-table.md) | P2 | Simplify Wiki AI-cost summary and expose grand total | Complete — five columns, bold Total, unchanged historical accounting; six GUI tests; Wiki and closed issue readbacks pass; partial task cost $0.42056876 |
| [T-020 / #46](tasks/T-020-handoff-execution-plan.md) | P2 | Show intended CLI work in the existing handoff table | Complete — frozen 1–10-bullet summary, six-row planned table and legacy compatibility; 54 GUI tests; partial cost $0.36908640 verified |
| [T-012 / #33](tasks/T-012-gui-context-measurement.md) | P2 | Measure known GUI session text cheaply, calibrate CLI estimates, show plan count and standardize progress rendering | Complete — corrected implementation accepted; 82 GUI tests and real-schema smoke; prospective aggregate history, calibrated time/steps and canonical progress; partial saved GUI/CLI cost $0.79798050 verified; scoped publication authorized |
| [T-003 / #25](tasks/T-003-handoff-progress.md) | P1 | GUI-supplied execution plan and compact persistent CLI progress | Complete — independent GUI acceptance and consumed receipt on 2026-10-23; 36 handoff tests pass; supplied capped plans, persistent monotonic progress and gated CLI completion; #25 closed; canonical T-003 identity restored on 2026-10-25; Wiki guide/cost coverage published; scoped Git publication authorized; presentation follow-up accepted: standalone commentary and copyable-template/language guidance, no lifecycle change |
| [Historical Wiki](tasks/legacy-wiki-feasibility.md) | P1 | Assess GitHub Wiki capability and prepare three-section draft with grouped AI cost estimates | Complete — three-section Wiki Home published; 2026-10-23 Standard-rate verification confirms R $15.38 / T $4.17 for known priced models, partial coverage; F/B have no eligible tasks. Initial draft feasibility limits remain documented |
| [T-004 / #26](https://github.com/mhaduk/ck3-dynasty-map/issues/26) | P1 | Standardize issue title convention and reconcile/publish documentation and Wiki costs | Complete — canonical `<ID> — <title>` rule applied to instructions/templates; #26 closed after publication; Wiki AI-cost tables refreshed with 2026-10-23 Standard rates; T-004 measured usage unavailable, not zero |
| [T-002 / #24](https://github.com/mhaduk/ck3-dynasty-map/issues/24) | P1 | Per-model historical token accounting and close-time workflow proposal | Complete locally — [accepted result](tasks/T-002-task-ai-cost.md); 11 verified remote tables, 10 local mirrors, 27 offline tests; partial coverage. Configuration proposal unapplied; scoped Git publication authorized 2026-10-22; #24 now verified CLOSED; earlier accounting cutoff excluded its closure |
| [T-001 / #23](https://github.com/mhaduk/ck3-dynasty-map/issues/23) | P0 | Incrementally improve per-ID parallel CLI handoffs, context/routing, log analysis and feedback | Complete — [canonical record](tasks/T-001-agent-workflow-optimization.md); GUI accepted both corrected stages on 2026-10-22; 37 offline tooling tests passed. Scoped publication authorized; receipt in #23. Savings unmeasured; F-001 paused |
| [T-006 / #28](tasks/T-006-workflow-automation.md) | P1 | Establish GUI/Sol → CLI/Luna model-routing and evidence-driven delegation contract | Complete and published — GUI accepted corrected step 0 and session-backed accounting; 36 tests and corrected template lifecycle pass; #28 closed completed; Wiki synchronized; no helper/schema/model-config change |
| [T-008 / #32](tasks/T-008-workflow-optimization.md) | P2 | Reassess and select the next minimal workflow optimization after T-006 routing | Complete — corrected offline inventory accepted by GUI; 22 focused/isolated tests, 84 upstream regressions; #32 closed after publication; remaining candidates mapped to T-011 |
| [T-009](tasks/T-009-structured-preflight.md) | P2 | Add structured preflight evidence compatible with the T-008 inventory | Complete — corrected implementation accepted/consumed; 39 focused/isolated tests and 123 targeted regressions; #35 closed after publication; no live app action |
| [T-010](tasks/T-010-checkpoint-comparison.md) | P2 | Compare two finite pinned log checkpoints without causal inference | Complete — final GUI correction accepted; 24 focused/isolated tests, 29 inventory and 15 log-delta regressions; #36 closed after publication; source limits remain explicit |
| [T-015 / #41](tasks/T-015-diagnostic-escalation.md) | P2 | Opt-in diagnostic escalation and independent advisory review | Complete — corrected packet builder/import accepted; 161 independent tests and historical dry run; saved-session costs verified; issue/Wiki published; no external reviewer or CK3 operation required |
| [T-011 / #37](https://github.com/mhaduk/ck3-dynasty-map/issues/37) | P3 | Preserve undelivered T-008 optimization candidates for later prioritization | Deferred — OPEN; no implementation selected |

## M0 — Research & bootstrap

| ID | GitHub issue | Priority | Work item | Depends on | Status |
|---|---|---|---|---|---|
| R-001 | [#1](https://github.com/mhaduk/ck3-dynasty-map/issues/1) | P0 | Record installed CK3 version and DLC/playset baseline | — | Complete — environment inventory; see RESEARCH.md |
| R-002 | [#2](https://github.com/mhaduk/ck3-dynasty-map/issues/2) | P0 | Inspect current `gfx/map/map_modes/map_modes.txt` | R-001 | Complete — native definitions inspected; custom loading/runtime unverified |
| R-003 | [#3](https://github.com/mhaduk/ck3-dynasty-map/issues/3) | P0 | Inspect installed map-mode GUI, unavailable UI and activation/refresh/exit hooks | R-001 | Complete — static GUI/type inspection; runtime gates open |
| R-004 | [#4](https://github.com/mhaduk/ck3-dynasty-map/issues/4) | P0 | Generate `script_docs` and `dump_data_types` | R-001 | Complete — clean script_docs and dump_data_types generated |
| R-005 | [#5](https://github.com/mhaduk/ck3-dynasty-map/issues/5) | P0 | Verify local-player/Dynasty scopes, validity guards and active-context invalidation/restore hooks | R-003,R-004 | REDUCE — open: dispatch/context-loss contract and merged no-Dynasty fixture-or-coverage decision; RGB cleanup owned by R-009 |
| R-006 | [#6](https://github.com/mhaduk/ck3-dynasty-map/issues/6) | P0 | Verify county -> holder -> dynasty transitions | R-004 | Complete — clean generated scope links verified; no runtime claim |
| R-007 | [#7](https://github.com/mhaduk/ck3-dynasty-map/issues/7) | P0 | Verify `any_liege_or_above` in target build | R-004 | Closed completed — documented traversal plus bounded R-016/F-001 evidence; remaining classifier/government acceptance owned by F-001 and T-111/T-112/E-204/E-205 |
| R-008 | [#8](https://github.com/mhaduk/ck3-dynasty-map/issues/8) | P0 | Verify county -> de-jure baronies iterator | R-004 | Closed completed — county-rooted barony filtering and bounded sample demonstrated; full projection acceptance owned by F-001/F-107/T-114 |
| R-009 | [#9](https://github.com/mhaduk/ck3-dynasty-map/issues/9) | P0 | Verify barony color writes, dummy-title side effects and exit/restore behavior | R-002,R-004 | REDUCE — open: current shared title-RGB isolation, exact arbitrary-original restore and save/removal contract; excluded carriers and palette-source research removed |
| R-010 | [#10](https://github.com/mhaduk/ck3-dynasty-map/issues/10) | P1 | Confirm additive/minimal original GUI integration, unavailable UI and dependable refresh path | R-003 | Closed completed — original scoped native-menu integration and explicit Refresh demonstrated within bounded smoke; F-001 owns UI/parity/refresh acceptance, R-005/R-009 safety |
| R-011 | [#11](https://github.com/mhaduk/ck3-dynasty-map/issues/11) | P1 | Capture vanilla error-log baseline without mod | R-001 | Closed not planned — retire generic vanilla capture; F-001/T-113 request matched controls only for concrete attribution gaps; checkpoint completeness is not causality |
| R-012 | [#12](https://github.com/mhaduk/ck3-dynasty-map/issues/12) | P1 | Install/configure CK3 Tiger locally | R-001 | Closed not planned — Tiger setup is optional evidence-triggered tooling under T-113, not a research dependency; no install/run claimed |
| R-013 | [#13](https://github.com/mhaduk/ck3-dynasty-map/issues/13) | P2 | Establish a supported no-Dynasty local-player fixture and verify unavailable UI | R-005 | Closed not planned — merged unresolved fixture-or-coverage decision into R-005; no no-Dynasty UI pass or ADR-008 waiver |
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
| [F-001 / #20](https://github.com/mhaduk/ck3-dynasty-map/issues/20) | Dynasty entry, three subviews, legend and accepted grey-ground appearance; bounded cleanup closeout | R-016,R-005,R-009; completed R-010 method; ADR-008/009/010 | Complete for accepted bounded fresh-session UI/ordinary interaction; GUI independently verified saved-session costs and final publication scope. Cycle31 remains historically FAILED. Fresh-game error-channel controls did not reproduce the two earlier unnamed duplicate-title errors; cause/save impact UNKNOWN. F-005/#30 compatibility and F-004/#29 diagnostics remain open. See [canonical record](tasks/F-001-dynasty-map-ux.md) and [painting/test guide](F001_MAP_PAINTING.md) |
| [F-002 / #21](https://github.com/mhaduk/ck3-dynasty-map/issues/21) | Character-associated color approximation and exact fallback; bounded accepted behavior | R-009,R-016; ADR-010 | Complete for bounded user acceptance; partial finite-cutoff cost and limitations published, #21 closed after Issue/Wiki readback — [color strategy](tasks/F-002-dynasty-color-strategy.md) |
| [F-003 / #22](https://github.com/mhaduk/ck3-dynasty-map/issues/22) | Define Dynasty subview behavior and semantic category roles | R-016; ADR-010 | Complete — [behavior reference](tasks/F-003-dynasty-subview-definitions.md); defines selection, classification and Primary/Secondary/Neutral result roles; F-001 owns visual treatment and F-002 color-source/fallback |
| [F-004 / #29](https://github.com/mhaduk/ck3-dynasty-map/issues/29) | Dynasty Map diagnostics hardening | Accepted F-001 -27/-28 evidence; strict analyzer | Bounded diagnostic/interaction acceptance delivered 2026-10-24: native DIAG V3 values/samples and separate REALMS/HOLDINGS/MY_REALM AUDIT V4 passes against emitted rosters; stable rows accepted. Closed completed after independent GUI cost/evidence review and verified issue/Wiki publication. Historical truncations, partial latest sample interval and unattributed init/court errors remain visible; no census/stored-RGB/lifecycle/clean-log claim. See [diagnostic matrix](tasks/F-004-diagnostics-hardening.md) and [developer guide](F004_DIAGNOSTICS.md) |
| [F-005 / #30](https://github.com/mhaduk/ck3-dynasty-map/issues/30) | Dynasty Map functional follow-ups and deferred final icons | F-003; R-005 context/noDynasty; R-009 RGB lifecycle; R-017 fixtures | Open follow-up — [functional/UX matrix](tasks/F-005-functional-followups.md); owns unresolved old-session duplicate-title cause/persistence, residual compatibility and functional/UX acceptance after F-001's bounded fresh-session closeout. Former local F-004 [icon history](tasks/F-004-icon-preparation.md) preserved; no new artwork |

| [R-018 / #38](tasks/R-018-diagnostic-timing-research.md) | Research reliable elapsed timing and presentation boundaries | Reuse F-004 timing findings | Open/deferred research; timer excluded from F-004 |
| [F-006 / #39](tasks/F-006-diagnostic-timer.md) | Implement Shift diagnostic elapsed timer | R-018 and GUI design approval | Planned/blocked on research; independent of F-004 |

These plans are separate backlog records, not implementation or runtime
authorization. Existing F-101 through F-110 IDs remain stable; their older
holder-first wording is historical planning context and must be mapped to the
current ADR-010 views when a successor is scoped, never renumbered in place.

Current T-005 ownership: R-005 absorbs R-013’s unresolved no-Dynasty case; R-009 owns RGB safety. R-007/R-008/R-010 research is closed; F-001 owns their ordinary feature acceptance. The following FINAL GUARDS paragraph describes the earlier ownership checkpoint.

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
| F-104 | P0 | Resolve valid player Dynasty and implement ADR-008 unavailability/context-loss safety, including the unresolved no-Dynasty coverage decision in R-005 | R-005,R-009,F-101 |
| F-105 | P0 | Implement `DIRECT` county classifier | R-006,F-104 |
| F-106 | P0 | Implement `CONTROLLED` via verified liege traversal, including no-Dynasty holders | R-006,R-007,F-104 |
| F-107 | P0 | Propagate county class to baronies through the R-009-approved color strategy | R-008,F-102,F-105,F-106 |
| F-108 | P0 | Integrate map-mode button, unavailable state and exit/restore | R-003,R-009,R-010,F-103,F-104,F-107 |
| F-109 | P1 | Add English localization | F-108 |
| F-110 | P0 | Implement dependable refresh: verified re-click or minimal explicit mechanism | R-003,R-010,F-108 |
| T-111 | P0 | Validate direct holder and cadet House cases | F-105,F-107 |
| T-112 | P0 | Validate nested foreign and no-Dynasty holders under dynastic lieges | F-106,F-107 |
| T-113 | P0 | Review bounded error logs; obtain matched vanilla control for unresolved attribution; evaluate Tiger only for a concrete static-check gap | F-109,F-110,T-111,T-112,T-114,T-115,T-116,T-117 |
| T-114 | P0 | Validate valid activation and barony rendering, including dummy-title side effects | R-009,F-107,F-108,F-109 |
| T-115 | P0 | Validate unavailable activation: no player/no Dynasty, no classification/color writes, no all-neutral substitute; the no-Dynasty player case follows R-005 | F-104,F-108,R-005 |
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
| E-206 | P1 | Harden no-Dynasty player UX/regressions while preserving ADR-008 unavailability; fixture/coverage decision owned by R-005 | v0.1.0,R-005 |
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
