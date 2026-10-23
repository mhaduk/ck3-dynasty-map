# Test Plan

## Test philosophy

Correctness first, then performance. A map that is fast but semantically wrong after succession or vassal transfer is worse than a static map that the user refreshes manually.

## Environments

Record for every test run:

- CK3 version/build;
- macOS version and Mac model;
- DLC set;
- enabled mod playset and load order;
- Dynasty Map version/commit;
- save/bookmark used.

## Baseline procedure

T-005 retires a blanket R-011 capture and mandatory R-012 setup. For a concrete
attribution gap, F-001/T-113 owns a matched vanilla control using recorded build,
DLC/playset, save and action boundaries. Reuse accepted evidence first; complete
T-001 intervals do not prove causality or clean logs. Preserve unresolved errors.
Core feature checks use the existing test playset; any additional game actions
require separately scoped user-led execution. Tiger is optional under T-113 only
when a supported static-check gap justifies evaluation; it is not an API authority
or replacement for source/preflight/parser/runtime gates.

## Milestone coverage

Documentation-only changes may mark game-runtime validation not applicable;
review textual consistency, links and diffs instead. Do not imply game tests ran.

v0.1 requires minimum smoke/regression coverage of safe activation,
classification, rendering, dependable refresh, exit/restore and unavailable-state
behavior. Review bounded error evidence and obtain a matched vanilla control
when attribution requires it; evaluate Tiger only for a concrete static-check gap. Record
visible refresh hitch observations; a deep profiling baseline is added in v0.2.

v0.2 adds deeper government/state regression, save/load and add/remove testing,
profiling and other-mod compatibility coverage. Before v1.0, complete the broader
matrix and demonstrate safe removal or a clearly proven harmless removal path.
Known removal limitations may be documented during v0.x; they do not waive v1.0
removal safety. Any v0.1 claim about saves/removal must have evidence; disclose
untested behavior and known limitations.

## v0.1 activation and lifecycle acceptance

| Case | Required result |
|---|---|
| Activate with valid player and Dynasty | Correct selected ADR-010 dark/light/grey county classification and barony rendering; no new mod-caused log errors |
| No valid local player | My Dynasty unavailable; activation performs no classification or color writes; no all-neutral substitute |
| Player has no valid Dynasty | Same unavailable behavior, verified independently from missing player; unresolved fixture-or-coverage decision now owned by R-005 (R-013 merged) |
| Manual refresh/re-activation after holder or liege change | Updated correct map through M0-verified re-click, or the smallest explicit refresh mechanism if re-click is unsupported |
| Repeat activation/refresh | Stable results, guarded scopes and no accumulating visual state |
| Player context becomes invalid while active | Stop using old Dynasty; clear/restore visual state as far as the verified API permits; record limitations and prove no stale-context classification |
| Switch to another valid player Dynasty | Stop old-context use; any subsequent classification uses the new valid context; test cleanup and re-activation |
| Exit to another map mode | Restore expected visuals with no leaked Dynasty colors; record the API-supported restoration mechanism |
| Render lowborn/no-Dynasty holder under qualifying dynastic liege | Evaluate all seniors using the selected ADR-010 view; never automatically grey |

M0 must determine UI disabling/hiding and player-context invalidation under
R-005, with ordinary UI acceptance in F-001; R-009 separately owns title-color exit/context-loss restoration.
Clearing a GUI marker or restoring launcher selection does not restore colors.
Unavailable activation must not classify or write colors; restoration cleanup on
loss of an active context is a separate operation and may need restore writes.
Use runtime/probe evidence sufficient to demonstrate those distinctions.

Ownership checkpoint after T-005 (2026-10-23): F-001 then owned hierarchy/projection/UI acceptance from closed R-007/R-008/R-010, including deep/government cases, exact barony coverage, selected-view Refresh receipts and native/DLC/UI-scale parity. R-005 owns dispatch/context and merged no-Dynasty coverage; R-009 exact RGB restore/save/removal. The dated snapshots below retain earlier issue references as history, not parallel live owners. No test was run in T-005.

F-001 closeout update, 2026-10-23: the user accepts the bounded menu,
appearance and ordinary interaction on fresh 867 Ismail sessions. This does
not mark strict diagnostics, global coverage, stored RGB, context-loss cleanup,
save/load/removal or broad UI parity as passed. F-004/#29 owns diagnostics;
F-005/#30 owns remaining functional/UI compatibility; R-005/#5 and R-009/#9
retain context and RGB/save/removal gaps. Refer to
[F-001 test history](F001_MAP_PAINTING.md); no new game test was run during this
documentation preparation.

## M0 R-005 diagnostic coverage snapshot — 2026-10-20

Passed diagnostic cases: explicit player/Dynasty context, repeated requests,
manual switches, succession hook/new-player context, activation after controlled
save/load, observer hiding/return and GUI-local marker clear with menu closed.
These are not production classification/rendering or full T-115/T-117 passes.

The later [FINAL GUARDS checkpoint](evidence/2026-10-20-r005-player-context/final-guards-result.md)
passed A for the displayed observer path after RESET: controls were absent and
no extra activation or probe-attributed validation error appeared in the
bounded capture. It did not exercise the watcher clearing a live READY value,
prove direct invalid-root safety or establish safety for every transition race.
The one-shot player `set_to_lowborn` fixture for B was rejected; Dynasty
remained present, so no-Dynasty local-player UI remains untested and is deferred
to [R-013 / #13](https://github.com/mhaduk/ck3-dynasty-map/issues/13). The
courtier effect guard and observer case do not substitute for that player case.
These diagnostics are not production classification/rendering or full T-115/
T-117 passes. Do not repeat passed cases or attempt another fixture in R-005.
Court-scene issues remain excluded from this research; the deliberate NULL
validation error must remain distinguishable from that noise. Color restoration,
active-map persistence and cleanup stay in R-009 and future implementation
tests. The SUCCESSION diagnostic kills a ruler: do not rerun it as routine
documentation work.

## M0 R-009 evidence snapshot — 2026-10-20

The isolated [batch](../research/probes/barony-color-batch/README.md) was installed
and user-run; its [checklist](../research/probes/barony-color-batch/BATCH_TEST.md)
now records executed/skipped/untested coverage. No repeat or new launch is
requested. R009 remains installed but disabled; prior playset selection was
restored by GUI after the user exited.

| Area | Evidence / remaining gate |
|---|---|
| Fixed-target RGB/named/copy writes | Visible success plus receipts; counts differed from planned repeats. Exact per-copy drift is unmeasured; AFTER contains distinct A/B RGB values |
| Native/minimal/filled custom baronies | Reported rendering; shared mutated state also visible in native baronies. Differing crops/zoom do not measure intensity |
| Exit/comparison/context loss | Other modes reportedly normal within bounded coverage; returning to baronies and reported observer retained colors. No automatic cleanup |
| Save/reload | Same-process enabled-mod reload retained colors before writes; read-only designated save copies separately prove title RGB serialization. Fresh-process/disabled-mod load remains untested |
| Definition resets / BEFORE | C08/C11 made targets red, not exact arbitrary-original restoration. BEFORE loaded after resets, so rollback from marked state is unproven |
| Title-root C09/C10 | C09 received once with valid player. Reported observer clicks had no new receipt; C10 skipped. Do not infer dispatch cause |
| Fixtures / errors | Four sources visible in Find Title with CoA errors; cyan missing capital, C04 skipped; two files lack BOM. Actual creation untested; user-reported creatability unverified. Court-scene errors remain, GUI warnings empty |

No production classifier, local-only color storage, exact live-original getter,
automatic restore or removal safety has been established. R-009's new static
trace found no generic table-to-renderer input in the reviewed surface; Situation
colors/membership provide a documented specialized consumer with unresolved
view binding, coverage, lifecycle and save/removal behavior. R-014's source
inventory is next in a separate chat; resume R-009 afterward with its source map
before deciding what further evidence is useful. Persistent state is not
categorically rejected; the concern is a fragile workaround built from unrelated
game systems. Any runtime scope needs a fresh design and explicit authorization.
See the [canonical partial checkpoint](tasks/R-009-barony-color-safety.md).

## My Dynasty functional matrix

ADR-010 supplies the current three-view expectations below. These are a design
review/truth table, **not CK3 execution results**. Historical DIRECT/CONTROLLED/
OTHER rows apply to Holdings. Player is P; all chains are ordinary de-facto,
without occupation, claims or tributary/suzerain links. Dark takes precedence.

| County / de-facto chain (D = player's Dynasty) | Realms | Holdings | My Realm & Dynasty |
|---|---|---|---|
| Foreign count → player king | Dark | Light | Dark |
| D count → player king | Dark | Dark | Dark |
| D count → foreign king, outside P subtree | Light | Dark | Light |
| Foreign count → D duke (not player) → foreign king | Light | Light | Light |
| Foreign count → independent D brother king | Dark | Light | Light |
| Independent D count outside P subtree | Dark | Dark | Light |
| Entirely foreign chain outside P subtree | Grey | Grey | Grey |
| Foreign count → player duke → foreign king | Light | Light | Dark |
| Foreign sibling count → same foreign king as player duke, no D senior | Grey | Grey | Grey |
| Lowborn holder → independent D senior outside P subtree | Dark | Light | Light |
| Cadet-House D count → foreign king, outside P subtree | Light | Dark | Light |
| Unheld/invalid county holder | Grey | Grey | Grey |
| No valid P or no valid D | Unavailable/no work | Unavailable/no work | Unavailable/no work |

Every barony in a county must receive its county result, including secondary
and empty holdings. Independents are their own highest ruler. A missing holder
Dynasty never skips dynastic seniors. Cadet creation, succession or vassal
transfer must produce the new result after a fresh manual recompute; use a
natural fixture only when available in a separately staged runtime scope.

### R016 three-view batch — execution record and limits, 2026-10-21

The planned startup and grouped runtime smoke were subsequently performed; see
the dated R-016 checkpoints for evidence. The five final execution pairs do not
map one-to-one to user actions. The numbered procedure below is retained as the
historical test design, not a pending R-016 run. Retain accepted old Holdings
direct/sample/copy/world evidence under
its original palette/semantics; it does not validate changed classifiers/UI.

1. With CK3 declared closed, later installer preserves installed payload/wrapper,
   logs and prior selection, runs exact-version 1.20.1.2 preflight, installs the
   reviewed source, verifies wrapper and installed equivalence. GUI reuses the
   existing test playset and intended selection. User starts CK3 via Steam,
   stops at menu; GUI checks fresh build/mount/error/GUI/conflict logs before play.
2. In one paused disposable valid P/D session, collect natural county/holder/
   senior fixtures and native references at fixed zoom. Open Additional Modes
   without clicking Dynasty; require no WORLD markers. Use diagnostic COMPUTE
   Realms once while native Realms is selected; stop before DISPLAY for its
   first-execution log gate. Repeat that gate once per new view before dependent
   display/next write. Matching BEGIN/END, no REJECT/new attributed errors are
   required; END is not complete coverage. No counter output is assumed.
3. After the relevant gates, group observations across all three outputs: exact
   labels/order, one top-level Dynasty entry, initial Realms, active subview
   controls and down state, matching legend/palette, meaningful contrasting
   counties, constituent baronies, native-view round trip and returning Realms
   output. The normal Dynasty/subview/Refresh path must execute its own classifier
   and select its mode without CHECK/COMPUTE/DISPLAY. Diagnostics are a separate
   area. Capture markers for normal clicks too; an ordinary menu opening or
   unrelated menu must not scan. Repeated normal clicks are justified here by
   the changed UI wiring, not a repeat of basic renderer/API smoke.
4. Explicitly retain player-vassal/subtree versus sibling-under-same-foreign-king,
   intermediate dynastic senior under foreign top, independent relative, cadet,
   lowborn and unheld fixtures in the report; missing natural cases are untested.
   No fixture mutation, console script, unpause or player switch is requested.
   Report a normal-UX/atomicity gap if the composed action fails; do not accept
   staged diagnostics as completion. Compare re-entry/recompute versus repaint
   timing and note approximate hitch without claiming measured duration.

Stop on wrong class/projection, missing/reject markers, new attributed error,
crash, context change or harmful helper/native effects; preserve partial evidence.
An unrelated baseline error needs attribution, not automatic erasure or a claim
of harmlessness. Legacy sample/copy controls are optional retained diagnostics,
not prerequisites for direct views. No save/load, fresh-process or disabled-mod
persistence batch is authorized here. ADR-008/009 safety gates remain open.

## Government / mechanics matrix

At minimum before 1.0:

- feudal;
- clan;
- tribal;
- administrative;
- theocratic/republic county holder edge case if naturally reachable;
- landless player with landed Dynasty relatives if current CK3 rules allow it;
- observer/no local player.

## State tests

- enter/exit map mode repeatedly;
- dependable manual refresh after title transfer (verified re-click or minimal explicit mechanism);
- save with map mode active, reload;
- enable mod on existing save;
- disable mod after save created with mod enabled; document v0.x limitations and prove safe removal or a harmless removal path for v1.0;
- verify dummy color titles have no unintended gameplay or UI effects;
- switch character if debug tools permit;
- game-over/succession transitions.

## UI tests

- button appears in intended location;
- active/down state correct;
- close/return-to-realms works;
- 1.20+ sub-mode buttons do not overlap other controls;
- tooltip/legend readable at 100% and common UI scales when included in the milestone;
- color accessibility reviewed; neutral territory remains distinct from unavailable mode behavior;
- no missing localization keys.

## Compatibility tests

- vanilla only;
- one representative mod that changes `map_modes.txt`;
- one representative mod that changes map-mode GUI;
- large content mod without map UI changes;
- total conversion only if explicitly targeted later;
- Ironman/achievement behavior remains unknown until explicitly verified and recorded.

## Performance tests

Use `Script.Profiling.Gui` or profiling console commands.

Measure:

- one My Dynasty refresh;
- repeated refresh 10x in the same save;
- profiler cost while map inactive (must be effectively zero from this feature);
- compare county-first and direct-barony implementations only if PoC indicates visible hitching.

Do not set a hard millisecond budget before measuring the reference Mac. Record a baseline first, then set a regression threshold for future releases.

## Release blocker severity

- **P0:** crash, save corruption, desync evidence, map globally broken, cannot exit mode.
- **P1:** wrong dynasty classification, large persistent performance regression, pervasive log errors.
- **P2:** stale tooltip, minor visual overlap, imperfect shade/contrast.
- **P3:** cosmetic/documentation issue.

## R-016 closeout coverage and successor tests

R-016 research is closed; its prepared procedures above are historical scope,
not requests to rerun the session. Fresh startup, three initial execution gates
and user-reported normal switching/Refresh/native-return smoke passed within
their bounded context. Grey nonmatching land failed visual acceptance. Numeric
coverage, exact per-control attribution, deep/cadet/lowborn/player-vassal cases,
changed-state freshness, profiling, context loss and save/removal remain unproven.
R-017 will select useful fixtures; F-001 tests final UI/neutral grey/contrast;
F-002 tests source/fallback colors. Use the accepted
[F-003 tables](tasks/F-003-dynasty-subview-definitions.md) for expectations.
