# Risk Register

| ID | Risk | Probability | Impact | Mitigation / decision |
|---|---|---:|---:|---|
| RK-01 | Old custom-map tutorials no longer match CK3 1.20+/1.21 UI | High | High | Inspect installed vanilla files before writing UI code |
| RK-02 | Full `mapmodes.gui` replacement conflicts with other UI/map mods | High if required | High | Use additive/minimal original integration; if a vanilla copy is required, block RG-UI-01 under ADR-006 |
| RK-03 | `set_color_from_title` used on wrong tier breaks rendering | Medium | High | Apply only to baronies; test minimal PoC first |
| RK-04 | Color effect creates error-log spam on current patch | Medium | Medium | Reproduce with one barony; inspect generated effect docs and log |
| RK-05 | Static map becomes stale after succession/conquest | Certain | Low | Explicit manual refresh in v0.x; tooltip documents behavior |
| RK-06 | Dynamic/event refresh introduces constant performance cost | Medium | High | No dynamic refresh before profiler evidence |
| RK-07 | Persistent graph/cache becomes stale after edge-case hierarchy changes | High | High | No persistent graph in MVP |
| RK-08 | Global variables pollute saves / complicate observer or multiplayer | Medium | Medium/High | Avoid global variables unless current UI forces multiplexing |
| RK-09 | Native Dynasty/House color getter is unavailable; approximate current-CoA palette may miss pairs | Medium | Medium | 76 complete ordered pairs with exact option-B fallback are accepted; universal getter and full-roster runtime remain unproven |
| RK-10 | Approximate palette may vary across cadet Houses/succession because it follows current CoA channels | Medium | Medium | User selected practical current-character association; Dynasty-wide continuity is not promised or proven |
| RK-11 | Lowborn/no-Dynasty landed holders cause invalid scopes | Medium | Medium | Guard missing Dynasty scopes; still check lieges for CONTROLLED before assigning OTHER |
| RK-12 | Observer/no local player breaks My Dynasty | Medium | Low | Unavailable under ADR-008; no classification/color writes on activation; test active-context cleanup |
| RK-13 | Multiplayer desync/incorrect local player context | Unknown | High | Unsupported until deliberately tested |
| RK-14 | CK3 1.21 lands before implementation completes | High | Medium | Re-lock target on gaming Mac; never assume 1.20.1 files |
| RK-15 | Copying code from old mods creates licensing/attribution ambiguity | Medium | Medium | Reimplement from documented behavior where possible; track third-party provenance |
| RK-16 | Mod removal leaves persistent color/state changes in save | Title RGB serialization observed; removal behavior unknown | High | R-009 AFTER contains explicit A/B overrides. Fresh-process/disabled-mod load untested; require safe removal or a proven harmless path for v1.0 |
| RK-17 | Dynasty colors leak into other map modes or fail to restore | Shared native/custom barony state and retained colors observed | High | R-009 mode exit/observer did not clear mutations; definition reset is not exact restoration. Resolve independent renderer input or exact cleanup before implementation |
| RK-18 | Dummy color titles cause unintended gameplay or UI effects | Search visibility/setup errors observed; creatability unverified | High | Four R-009 fixtures are visible with CoA/cyan-capital errors. No title creation tested. Historical candidate only; no extra titles before strategy decision |
| RK-19 | Full refresh causes a visible hitch despite zero inactive scans | Unknown | Medium | Record v0.1 smoke observations; measure in v0.2 before optimizing; no persistent cache without evidence |
| RK-20 | Player switching or context loss leaves the active map using an old Dynasty | Unknown | High | Stop old-context use, clear/restore as far as API permits; verify lifecycle hooks in M0 and v0.1 regression tests |
| RK-21 | Ironman/achievement compatibility is unknown | Unknown | Medium | Make no support claim until explicitly tested against a recorded build and playset |
| RK-22 | Shades are inaccessible or neutral territory is confused with unavailable mode | Unknown | Medium | Review contrast/accessibility; unavailable mode must not render an all-neutral substitute; verify unavailable UI in M0 |
| RK-23 | GUI type extension resolves cyclically and crashes at startup | Observed in R-010 probe | High | Failed same-name probe quarantined; verify vanilla recovery; require different evidence-backed integration before another test |
| RK-24 | Independent classification may lack a supported view-specific renderer input | Unresolved engine boundary | High | R-009 owns shared title-RGB isolation/exact restore/save/removal; no independent input demonstrated. ADR-009 excludes Situation/carrier alternatives; no new broad scan. R-016 bounded execution is not a lifecycle-safe production route |

R-016 closeout (2026-10-21): bounded three-view pipeline/UI smoke does not
resolve RK-16/17/20/24. RK-22 is now an observed visual acceptance failure: unrelated
continental county land is not clearly grey; F-001 owns diagnosis and contrast.
F-002 now has user-accepted approximate character-associated palette behavior with option-B fallback. Dynasty-ID stability, exact stored/rendered RGB, missing-slot normalization, removal safety and full-roster runtime coverage remain unproven. R-017 supplies natural fixtures.

T-005 ownership update (2026-10-23): RK-12/20 and no-Dynasty coverage belong to R-005 (R-013 merged); RK-16/17/24 to R-009. F-001 owns remaining ordinary menu/parity, hierarchy and projection acceptance after R-007/R-008/R-010 research closure. Later F-001 visuals are user-accepted for the supplied views; the older RK-22 failure above is historical, not a new requested redesign. Full classification/lifecycle acceptance remains open.

F-001 closeout update (2026-10-23): the user accepts the bounded menu,
appearance and ordinary interaction on fresh 867 Ismail sessions. Cycle34/35
fresh-game error-channel lines did not reproduce the two unnamed duplicate-title
errors seen in the earlier existing-session load; cause and persistence impact
remain UNKNOWN. The bounded acceptance does not reduce RK-16/17/20/24, strict
diagnostic, context, RGB restoration or removal risks. Overall new-game/smoke
captures remain INCOMPLETE at a partial final debug line.

F-004 bounded closeout update (2026-10-24): native declarations now support
the accepted DIAG V3 summary/samples and three independent selected-view V4
passes against emitted rosters; the fixed-row interaction is user-accepted.
This does not lower RK-16/17/20/24 or remove the strict sample-interval,
context, RGB restoration, save/removal, global coverage or lifecycle limits.
Initialization and court-scene errors remain unattributed; no clean-log or
harmlessness claim is made. Timing is owned by R-018/F-006, independent of
F-004. GUI cost/accounting review and publication readback passed; #29 is closed
completed for its bounded scope.
