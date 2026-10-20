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

1. Launch vanilla with `-debug_mode -develop`.
2. Capture baseline `error.log` noise before enabling the mod.
3. Enable only Dynasty Map for core validation.
4. Keep a separate compatibility playset for interaction tests.

## Milestone coverage

Documentation-only changes may mark game-runtime validation not applicable;
review textual consistency, links and diffs instead. Do not imply game tests ran.

v0.1 requires minimum smoke/regression coverage of safe activation,
classification, rendering, dependable refresh, exit/restore and unavailable-state
behavior. Run Tiger and compare error.log with the vanilla baseline. Record
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
| Activate with valid player and Dynasty | Correct DIRECT/CONTROLLED/OTHER county classification and barony rendering; no new mod-caused log errors |
| No valid local player | My Dynasty unavailable; activation performs no classification or color writes; no all-neutral substitute |
| Player has no valid Dynasty | Same unavailable behavior, verified independently from missing player |
| Manual refresh/re-activation after holder or liege change | Updated correct map through M0-verified re-click, or the smallest explicit refresh mechanism if re-click is unsupported |
| Repeat activation/refresh | Stable results, guarded scopes and no accumulating visual state |
| Player context becomes invalid while active | Stop using old Dynasty; clear/restore visual state as far as the verified API permits; record limitations and prove no stale-context classification |
| Switch to another valid player Dynasty | Stop old-context use; any subsequent classification uses the new valid context; test cleanup and re-activation |
| Exit to another map mode | Restore expected visuals with no leaked Dynasty colors; record the API-supported restoration mechanism |
| Render lowborn/no-Dynasty holder under qualifying dynastic liege | CONTROLLED, never automatically OTHER |

M0 must determine UI disabling/hiding and context-invalidation/restore hooks.
Unavailable activation must not classify or write colors; restoration cleanup on
loss of an active context is a separate operation and may need restore writes.
Use runtime/probe evidence sufficient to demonstrate those distinctions.

## My Dynasty functional matrix

| Case | Expected |
|---|---|
| Player directly holds county | DIRECT |
| Same Dynasty, different cadet House holds county | DIRECT |
| Foreign Count under same-Dynasty Duke | CONTROLLED |
| Foreign Count -> foreign Duke -> same-Dynasty King | CONTROLLED |
| Same-Dynasty Count under foreign Duke/King | DIRECT |
| Foreign holder with no same-Dynasty liege | OTHER |
| Independent same-Dynasty ruler | DIRECT for counties directly held by that Dynasty's counts/ruler; controlled semantics for foreign vassals beneath a dynastic liege |
| No-Dynasty/lowborn holder | OTHER unless a liege belongs to player Dynasty |
| Player without valid Dynasty | mode unavailable; no classification/color writes on activation; no all-neutral substitute |
| No valid local player | mode unavailable with the same no-work activation behavior |
| Cadet branch created while game running | correct after refresh |
| Succession changes holder Dynasty | correct after refresh |
| Vassal transfer changes liege chain | correct after refresh |

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
