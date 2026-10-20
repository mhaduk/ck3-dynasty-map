# R-010 probe 02 — original submenu replacement

Status: installed and enabled in the local probe-only playset. Startup,
native-menu placement/tooltip and user-reported basic/Faith sub-mode smoke checks
passed. Broader compatibility and lifecycle behavior remain unverified. Target CK3 1.20.1.1 (Crozier).
Branch `research/native-menu-alternative` starts at `13a82c0`, inheriting the
complete handoff and failed-probe history; the original branch is retained.

## Different hypothesis

Replace only the script-defined `flowcontainer_additional_mapmodes` type with
an original body deriving directly from the engine `flowcontainer` primitive.
It never derives from the replaced type. A uniquely named helper derives from
the existing native `icon_button_mapmode` type. This avoids the known direct
self-resolution cycle but does not guarantee that duplicate type registration,
load precedence or runtime UI behavior will work.

The source is authored independently; no vanilla GUI file/body was copied.
Installed observations supply the native mode keys, action names and DLC gates.
This is the architecture's existing minimal original scoped-override candidate,
not a change to ADR-006 or a selected production integration strategy.

## Scope and tradeoffs

- Replace the Additional Modes submenu only, not HUD, main map bar or banner.
- One disabled DM marker; it has no onclick or world/state effect.
- Reference all 16 observed native menu modes and their shortcuts, plus the four
  native additional-settings controls. Existing native controls may change
  modes/settings when the user intentionally uses them.
- Preserve the `mapmodes_insert_before` seam for native mini-mode overrides.
- Use original compact row layout and native controls/assets by reference.
  This is not an exact reproduction of vanilla layout/animations/tutorial IDs.
- No title/dummy title, custom map definition, classifier, scripting callbacks,
  recurring work, localization or standalone overlay is added.
- Replacement affects every native instance using this shared submenu type;
  mini-mode and UI-scale regression coverage are therefore needed later.
- Any other mod replacing the same type conflicts. Multiplayer unsupported.

`gui/zz_dynmap_native_menu_probe_02.gui` has an intentional prefix exception:
the prior debug log read the first root-level dynmap file before shared/mapmodes.
The zz filename originally tested later loading, but the actual run still
read it before shared/mapmodes. It remains the tested filename, not evidence of
a later-loading requirement or general replacement precedence. The existing overridden type/block identifiers
are integration seams; owned helper/widget identifiers use dynmap_.

Source/install SHA-256:
`6bb3dfce4d508989ffd2cf41345b6f56c71d81de725ea739f4c2629466ac2121`.

## Setup and test checkpoints

The launcher-generated `Dynasty Map - Native Menu Probe` mod (0.0.0, exact
supported build 1.20.1.1) is reused. Its previous GUI remains .gui.disabled.
The only active GUI file in that local mod is probe 02. It was mounted alone
in the tested launch; the failed first probe remains quarantined. The following
steps record the installation/test procedure, not outstanding setup work.

1. Exit the current vanilla game normally, saving first if desired. In CK3's
   launcher select `Dynasty Map - GUI Probe`. Only the local test mod may be
   enabled; keep Realm Ledger off and record mounted DLC from fresh logs.
2. Launch once and **stop at the main menu**. Inspect debug/error/gui-warning
   logs to confirm this file mounted and to catch load/type errors before play.
3. Only if startup is clean enough against the no-mod baseline, use a disposable
   test game. Open + / Additional Modes: exactly one disabled DM marker must be
   inside the native menu, alongside all DLC-appropriate native entries/settings.
4. Check tooltip, menu open/close, native mode selection and return to Realms;
   later test faith mini-mode menus and another UI scale before broader claims.
5. On crash/type errors/broken menu, archive raw evidence locally, select No mods
   and quarantine the new GUI; do not retry unchanged or copy vanilla.
6. On completion, disable the test and confirm vanilla startup recovery.

## Validation so far

Source review: balanced braces, unique helper base, no same-name inheritance,
16 mode references, one disabled marker with no onclick, no classifier/color
operations. Source and installed bytes match. Raw pre-test logs/config archived
under ignored local/evidence/native-menu-probe-02/before. Startup evidence (13:21 launch) now confirms the probe mounted and this GUI
file read; error.log and gui_warnings.log were empty at the startup checkpoint.
Subsequent visual and user-reported interaction results are recorded below.
General override precedence remains unknown. No CK3 Tiger run was performed. R-010 remains
open; player safety/manual refresh/color-state research gates remain open.

## Startup checkpoint — 2026-10-20

User confirmed startup. debug.log:134–140 identifies expected DLC and only the
local probe; :1027–1028 records reading gui/zz_dynmap_native_menu_probe_02.gui.
error.log and gui_warnings.log are both 0 bytes at inspection. Raw logs/config
archived in ignored local/evidence/native-menu-probe-02/startup-01.
This confirms file loading without the prior startup crash, not that our menu
type won registration or that DM is visible. Next: disposable game, open +,
inspect DM and existing native entries/settings, then menu open/close and logs.

## In-game visual checkpoint — 2026-10-20

User screenshot confirms DM appears inside Additional Modes, its tooltip is
shown and native icon rows/Disease Graphics remain visible. Source/install
hashes match. The actual root-level zz file was still read before shared/mapmodes
in this run, so earlier assumptions about filename-driven late loading were
not confirmed; the menu nevertheless takes effect. No universal precedence
rule follows. See [reviewed visual evidence](../../../docs/evidence/2026-10-20-r010-native-menu-02/README.md).

In-game gui_warnings.log is empty. error.log is 17,413 bytes with tutorial and
court-scene invalid-character errors; no direct probe filename reference was
found, but a matched vanilla scenario has not established attribution. Menu
interaction results followed below; expanded mini-menu, UI-scale and recovery
remain pending.

## Basic interaction checkpoint — 2026-10-20

After being asked to switch native modes/return to Realms and reopen the menu,
the user confirmed it works. They also reported DM clicking has no map-changing
effect, consistent with the disabled/actionless source. This is user-reported
smoke evidence, not an automated click trace or exhaustive UI parity test.
Fresh log capture has unchanged sizes/content: gui_warnings 0 bytes, error.log
17,413 bytes with no direct probe filename or ResolveTypes match. Raw capture
is local/ignored under native-menu-probe-02/interactions-01. Existing error
attribution, expanded mini-menu/UI-scale, refresh, unavailable state, lifecycle and
probe-02 disable/recovery tests remain pending; R-010 is not closed.

## Faith sub-mode smoke — 2026-10-20

User confirmed Faith sub-mode controls are visible and can be switched/returned
in the current configuration. Fresh error/gui-warning sizes are unchanged
(17,413 / 0 bytes); debug/game logs grew and were archived locally. This does
not verify every sub-mode/DLC, expanded mini-menu content, alternate UI scales
or the future Dynasty group. R-010 safety/refresh/lifecycle gates stay open.
