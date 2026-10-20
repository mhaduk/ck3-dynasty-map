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
| RK-09 | All Dynasties cannot access a native Dynasty/House color | Medium | High | Research native House mode; retain title-color and palette fallbacks |
| RK-10 | Dynasty color changes when dynasty head/title changes | Medium | Medium | Document chosen strategy; test succession/new cadet branches |
| RK-11 | Lowborn/no-Dynasty landed holders cause invalid scopes | Medium | Medium | Guard missing Dynasty scopes; still check lieges for CONTROLLED before assigning OTHER |
| RK-12 | Observer/no local player breaks My Dynasty | Medium | Low | Unavailable under ADR-008; no classification/color writes on activation; test active-context cleanup |
| RK-13 | Multiplayer desync/incorrect local player context | Unknown | High | Unsupported until deliberately tested |
| RK-14 | CK3 1.21 lands before implementation completes | High | Medium | Re-lock target on gaming Mac; never assume 1.20.1 files |
| RK-15 | Copying code from old mods creates licensing/attribution ambiguity | Medium | Medium | Reimplement from documented behavior where possible; track third-party provenance |
| RK-16 | Mod removal leaves persistent color/state changes in save | Unknown | High | Document v0.x limitations; require safe removal or a proven harmless path for v1.0 |
| RK-17 | Dynasty colors leak into other map modes or fail to restore | Unknown | High | M0 verifies color-state/restore API; v0.1 tests exit, repeated activation and context-loss cleanup |
| RK-18 | Dummy color titles cause unintended gameplay or UI effects | Unknown | High | Verify inert/non-creatable behavior in M0 and inspect runtime side effects in v0.1 rendering tests |
| RK-19 | Full refresh causes a visible hitch despite zero inactive scans | Unknown | Medium | Record v0.1 smoke observations; measure in v0.2 before optimizing; no persistent cache without evidence |
| RK-20 | Player switching or context loss leaves the active map using an old Dynasty | Unknown | High | Stop old-context use, clear/restore as far as API permits; verify lifecycle hooks in M0 and v0.1 regression tests |
| RK-21 | Ironman/achievement compatibility is unknown | Unknown | Medium | Make no support claim until explicitly tested against a recorded build and playset |
| RK-22 | Shades are inaccessible or neutral territory is confused with unavailable mode | Unknown | Medium | Review contrast/accessibility; unavailable mode must not render an all-neutral substitute; verify unavailable UI in M0 |
| RK-23 | GUI type extension resolves cyclically and crashes at startup | Observed in R-010 probe | High | Failed same-name probe quarantined; verify vanilla recovery; require different evidence-backed integration before another test |
