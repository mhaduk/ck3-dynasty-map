# R-010 native-menu probe checkpoint history

This dated record preserves probe preparation and user-reported runtime checkpoints. The reusable conclusion and current gate status remain in [RESEARCH.md](../../RESEARCH.md). Checkpoints are historical and later observations supersede earlier next steps.

### R-010 authorized menu-only probe prepared (2026-10-20)

After the concrete proposal, the user approved preparing the inert-button
native-menu test. Original source and procedure are in
[research/probes/native-menu](../../../research/probes/native-menu/README.md).
It tests same-name decoration of the additional-menu type and overrides only
the named insertion block with one disabled DM button. This is a hypothesis,
not verified type resolution. No onclick, classification, title/color write,
map definition, scripted-widget overlay or recurring work is present.

**Performed:** prepared original source, reviewed its limited scope and brace
structure; archived pre-probe debug/error/gui-warning/game logs and mod-load
configuration under ignored local/evidence. The active session's mod-load
configuration still lists zero mods. error.log now contains 97,878 bytes after
the user's test-game start (rather than the earlier empty startup observation);
errors predate loading this probe. A full clean test matrix/bookmark identity
is not established, so R-011 stays Partial. No raw logs are tracked.

**Not performed:** launcher-generated mod creation, install/enable, engine
loading, runtime layout/click verification, Tiger or game restart. The generic
launcher opened without CK3 game context. The next step requires the user to
open the CK3 launcher through Steam and create the local probe mod; descriptors
remain launcher-generated and machine-local under the bootstrap policy.
The procedure includes separate playset setup, failure-stop conditions and
restoring vanilla by disabling the probe. No integration strategy is selected
until runtime success. R-010 remains Partial/open; R-005 is deferred while this
user-requested menu probe is pending.

### R-010 probe installation completed (2026-10-20)

User opened the CK3-specific launcher through Steam. The agent used its local
Create a Mod flow (no upload) to generate `Dynasty Map - Native Menu Probe`,
version 0.0.0, exact supported build 1.20.1.1, directory
`dynmap_native_menu_probe`. With filesystem approval, the original GUI source
was copied to that local mod's gui directory; SHA-256 matches source:
`dc572d67794fa5d17bda7100c8f282f1ba31228991414111db84ce3221e277f0`.
Descriptors remain machine-local; vanilla and repository descriptor state are
unchanged.

A separate `Dynasty Map - GUI Probe` playset was created and explicitly selected
on launcher Home. Read-only database inspection confirms that it is active and
contains only the enabled probe; `dlc_load.json` confirms one enabled local mod
and no disabled DLC. The new playset has no explicit per-DLC rows, so actual
DLC mounting will be verified from the next runtime log rather than assumed.
Initial playset was not modified. No game launch, engine validation or GUI
runtime result yet; R-010 remains Partial/open. The immediate next task is to
launch the selected playset and open Additional Modes in a disposable test game.

### R-010 runtime failure and quarantine — 2026-10-20 13:00

**Observed:** a single launch with only `Dynasty Map - Native Menu Probe`
crashed at 13:00:31 Europe/Warsaw, about five seconds after launch, before the
main menu. `debug.log:134–140` confirms the probe enabled/mounted, and
`:612–613` confirms its GUI file was read. Fresh error.log, gui_warnings.log
and game.log were empty. An empty error log does not clear a startup crash.

The user-supplied macOS report explicitly states stack exhaustion due to
excessive recursion. Crashed thread 12 contains approximately 43,800 recursive
`CPdxGuiFactory::ResolveTypes` calls, followed by ResolveDesc/AddTypesToReload/
PostLoadAssets. **Inference, strongly supported:** this original same-name
script-defined type/base declaration resolves cyclically rather than decorating
the prior menu type in this tested configuration. This rejects this probe;
it does not prove every form of GUI extension impossible. No second run or
controlled engine-internal diagnosis was performed. The report also identifies
Hardware model details are not needed to reproduce this checkpoint and are omitted.

The additional launcher text shows successful Steam library loading and two
undefined log categories. It is not evidence that Steam connectivity caused the
crash; the recursion stack is the relevant diagnostic evidence.

**Containment verified:** raw crash report and launch logs archived in ignored
local/evidence/native-menu-probe/crash-01. Launcher Home switched to No mods;
mod-load JSON confirms zero enabled mods. The installed GUI was quarantined as
`.gui.disabled` with filesystem approval; matching original source moved to
[failed probe source](../../../research/probes/native-menu/failed/dynmap_native_menu_probe.gui.disabled).
No active .gui remains in the installed probe. Source SHA-256 remains
`dc572d67794fa5d17bda7100c8f282f1ba31228991414111db84ce3221e277f0`.
Vanilla files and external descriptors unchanged. The probe never loaded a save
or performed map/color/classification writes. No vanilla recovery rerun yet.

**Gate disposition:** R-010 remains open; RG-UI-01 is blocked for the tested
native-menu method. The broader no-copy integration question remains unresolved,
not proven impossible. Do not reuse this attempt or promote the separate-widget
fallback against the user's stated preference. No architecture policy is relaxed.
**Single next task:** verify a No mods launch reaches the main menu and inspect
fresh logs; only then research a materially different original integration
mechanism before proposing another probe. No automatic retry of the failed type.

### R-010 vanilla recovery and reviewed evidence record (2026-10-20)

User confirmed successful startup after No mods was selected. Fresh runtime
`debug.log` at 13:09:24 lists no mods and Garments of the Holy Roman Empire;
mod-load JSON has zero enabled mods and recovery error.log is 0 bytes at
inspection. This confirms startup recovery, not save/load or full removal safety.
Raw recovery logs were archived locally alongside the failed-launch evidence.

The user requested branch history with documentation, logs and screenshots.
[Earlier reviewed test evidence](../2026-10-20-r010-native-menu/README.md) contains
original test notes and selected diagnostic excerpts; its user-supplied images
are outside this package. Raw logs/reports, local paths
and account/incident identifiers are excluded from tracked evidence. Failed
original source stays disabled. R-010 remains open; the next task is research
into a materially different original native-menu integration method.

### R-010 alternative probe 02 prepared — 2026-10-20

On user request to continue with another menu test, branch
`research/native-menu-alternative` was created from `13a82c0`; the handoff branch
and its complete documentation/evidence remain intact.

Read-only inspection confirmed native `flowcontainer_additional_mapmodes` derives
from primitive `flowcontainer` (mapmodes.gui:483), is instantiated by the existing
menu at :419, and has 16 explicit mode references plus four settings controls.
The failed launch log read the original root-level probe before shared/mapmodes
(:612 versus :1590), so precedence cannot be assumed from a dynmap prefix alone.

A materially different **original scoped replacement** is now prepared:
[probe 02 procedure/source](../../../research/probes/native-menu-alternative/README.md).
It defines the menu type with primitive flowcontainer as its base, never the
menu type itself. An independently authored compact layout references native
modes/settings with their observed DLC gates and shortcuts and adds one inert
DM marker. The native mini-menu insertion block remains available. This is not
a copied vanilla body, adjacent overlay or whole-HUD replacement. Layout,
animation and tutorial-ID parity are not claimed; all shared instances and
other mods overriding this type are compatibility concerns.

Source uses an intentional loading-order filename exception
`gui/zz_dynmap_native_menu_probe_02.gui`; actual registration/replacement
precedence remains unverified. Its hash is
`6bb3dfce4d508989ffd2cf41345b6f56c71d81de725ea739f4c2629466ac2121`.
With filesystem approval, identical source was installed in the inactive
launcher-generated local probe mod. Failed probe 01 remains quarantined.
No vanilla/descriptors were changed. Pre-test raw logs are archived locally;
current mod-load JSON remains No mods. No game run or screenshot for probe 02.

Static source review checked brace balance, no same-name base/derived pair,
16 native-mode references, one disabled actionless marker and absence of
classifier/title/color operations. This is not engine validation; Tiger has not
been run. R-010 remains open/Partial, and no integration strategy or ADR changed.
**Single next task:** select the probe-only playset, launch once and stop at the
main menu; inspect fresh mount/type/error evidence before proceeding to any
in-game layout test. Do not automatically retry a failing launch.

### R-010 probe 02 startup checkpoint passed (2026-10-20)

User confirmed startup/main menu after the 13:21 launch. Fresh debug.log:134–140
lists only the local probe and Garments of the Holy Roman Empire;
:1027–1028 records loading gui/zz_dynmap_native_menu_probe_02.gui. At inspection,
error.log and gui_warnings.log are both 0 bytes. Raw launch logs and mod-load
config archived locally/ignored under native-menu-probe-02/startup-01.

**Verified:** this new source is mounted/read and the game starts without the
prior recursive GUI-resolution crash. **Not yet verified:** which duplicate
type definition is effective, whether the DM marker appears inside the native
menu, native entries/settings parity, close behavior, mini-menu and UI-scale
regressions. No classification/color effects performed. Next checkpoint is a
disposable test game and opening Additional Modes under +. R-010 stays open.

### R-010 probe 02 native-menu placement confirmed (2026-10-20)

The user-supplied screenshot shows a subdued DM control inside Additional Modes,
above the existing native icon rows, with the exact probe-02 tooltip. Disease
Graphics is still visible. This confirms a real native-menu layout integration
for the original primitive-based replacement in this tested configuration,
not an adjacent standalone widget. Source/install hashes match the prepared
probe. [Reviewed screenshot/test record](README.md).

Important correction to the load-order hypothesis: the captured startup log
reads root-level zz probe at :1027 **before** shared/mapmodes.gui at :1587.
The attempt works visually despite that order. Do not claim the zz prefix made
it load later or infer general namespace/first-wins/last-wins semantics.

At in-game capture, gui_warnings.log remains 0 bytes and error.log is 17,413
bytes. Observed entries concern an invalid tutorial lesson key and invalid
character/culture evaluation in gfx/court_scene/scene_cultures/00_default_cultures.txt.
No direct probe filename or GUI ResolveTypes error was found. Attribution is
unresolved without a matched-save vanilla comparison; this is not an error-free
runtime claim. Raw logs/config archived locally/ignored.

**Next checkpoint:** repeated menu open/close, native map switching/return to
Realms and fresh-log review. Native icon/settings functionality, faith mini-menu,
UI scales, player guards, manual refresh and lifecycle restoration remain
unverified. R-010 stays Partial/open; RG-UI-01 now has positive placement evidence,
not completion of its entire safety/UX gate. No classifier/color work performed.

### R-010 probe 02 basic interaction smoke confirmed (2026-10-20)

User reported DM clicks do not change the map, consistent with its disabled,
actionless source, and confirmed the requested native-mode switching/return and
menu open/close checks work. This is user-reported smoke evidence, not an
agent-operated click trace or complete regression matrix. Fresh log capture
has unchanged sizes/content: gui_warnings 0 bytes and error.log 17,413 bytes,
with no direct probe-name or ResolveTypes matches. Raw evidence is local/ignored
under native-menu-probe-02/interactions-01. Existing script-error attribution
remains unresolved. Reviewed record updated; no additional screenshot claimed.

The minimal original submenu replacement has positive placement, tooltip and
basic-interaction evidence for this build/configuration. R-010 remains open:
mini-mode/UI-scale compatibility, unavailable state, dependable refresh and
cleanup remain unverified. **Single next research task:** R-005 read-only
player/Dynasty guard and scripted-GUI execution-context investigation, before
adding any active My Dynasty control. Keep existing inert probe scope unchanged.

### R-010 probe 02 Faith sub-mode smoke (2026-10-20)

After selecting Faith, the user confirmed the sub-mode buttons are visible and
can be switched/returned in response to the requested smoke check. This is
positive user-reported evidence for the current 1.20-style native controls with
probe 02 enabled. No screenshot/exact sub-mode sequence was captured; do not
claim all sub-mode variants, expanded mini-menu content, DLC or UI-scale coverage,
or a working future Dynasty group. Fresh logs retain error.log 17,413 bytes and
gui_warnings.log 0 bytes; debug/game logs grew. Raw capture archived locally under
native-menu-probe-02/faith-submodes-01. Error attribution still unresolved.
Reviewed evidence record updated. R-010 stays open; next task remains R-005
read-only player/Dynasty guard and execution-context research.
