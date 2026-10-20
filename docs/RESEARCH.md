# Research Findings

**Research date:** 2026-10-20
**Reported public CK3 release at research time (reference baseline, not installed-build verification):** 1.20.1 "Crozier" (2026-10-13). Paradox stated that subsequent changes were being targeted at the forthcoming 1.21 update, so the implementation target must be re-checked on the gaming Mac before coding.

## Evidence policy and target-build status

Community documentation, Workshop descriptions and archived repositories are
historical/reference evidence only. They suggest research probes; they do not
verify API behavior for the target CK3 build. The generated script_docs findings
below document APIs exposed by installed CK3 1.20.1.1 (Crozier). Initially
generated with NUI:Realm Ledger enabled, the listed entries were reconfirmed
in clean vanilla output on 2026-10-20 (see follow-up below).
They verify documented signatures and semantics, not runtime rendering behavior.
Other API assumptions still require installed-file, generated-doc or runtime
evidence before implementation relies on them.

For each verified finding, record the exact CK3 build, date, probe/backlog ID,
local file/API entry or runtime procedure, observed result and limitations.
Keep raw generated dumps local; record original findings here. Distinguish
reference claims, design assumptions and target-build observations.

## R-001 — Environment inventory complete (2026-10-20)

Read-only local inspection established the following baseline. This completes
R-001 as an inventory, not a clean vanilla runtime validation. Machine-local
paths and raw evidence stay outside Git under the existing provenance policy.

| Item | VERIFIED observation / evidence |
|---|---|
| Installed CK3 | 1.20.1.1 (Crozier), installed `launcher/launcher-settings.json` |
| Steam build | 25913294, `appmanifest_1158310.acf` |
| Clausewitz | `titus/release/1.20.1`; revision `af5c758c2072fbb444bab748c2b6dbb41faaa4b3`, installed branch/revision files |
| Titus | `release/1.20.1`; revision `32d8931eb5e04726c52574cce34a51147a3e4fd7`, installed branch/revision files |
| macOS / CPU | 26.5.2, build 25F84 (`sw_vers`); arm64 / Apple Silicon (`uname -m`) |
| Active playset | Initial playset, ID `64eafa44-4e66-4cba-b6af-ffdd77567ada`, read-only launcher database query |
| Enabled mod | NUI:Realm Ledger, Workshop ID 2995323766; launcher database, `dlc_load.json`, descriptor and runtime `debug.log` agree |
| DLC installed | Garments of the Holy Roman Empire (`dlc001_preorder`); package files and Steam depot present; no other packages found in inspected DLC directory |
| DLC enabled | `ck3_dlc001_preorder` enabled in active playset and mounted in `debug.log`; `disabled_dlcs` empty |
| Launch flags | `-debug_mode -develop` configured in Steam user `config/localconfig.vdf`, CK3 `LaunchOptions`; current process arguments not checked |
| Tools | Git 2.50.1 (Apple Git-155); Codex CLI 0.163.0; VS Code app and `code` command available |
| API output | script_docs generated successfully; effects, triggers, event targets and related logs timestamped 2026-10-20 approximately 11:55 Europe/Warsaw |

**UNKNOWN:** Steam branch selection (not explicitly present in inspected app
metadata); Mac model (system query denied); broader account DLC ownership;
At inventory time, `dump_data_types` completion/output was unknown; it is now
confirmed below. Internal source branch names do not prove
Steam branch selection.

**Initial baseline limitation (superseded by clean follow-up below):** NUI:Realm Ledger was enabled and mounted in the session
that produced the current runtime logs and script_docs. These are **not clean
vanilla evidence**. Preserve the documented API observations, but reconfirm them
after clean generation. No target rendering or lifecycle probes have run.

### Clean vanilla follow-up — R-004 complete; R-011 partial

On 2026-10-20 the user disabled Realm Ledger, restarted CK3 and executed
`script_docs` and `dump_data_types`. Read-only inspection confirms:

- `dlc_load.json`: no enabled mods and no disabled DLC.
- `debug.log:134–139`: empty Mod list; Garments of the Holy Roman Empire mounted;
  session startup at 12:16:54 Europe/Warsaw.
- Console history records both generation commands. Script-doc files refreshed
  at approximately 12:17:46; all five nonempty `logs/data_types/data_types_*.txt`
  files refreshed at approximately 12:17:53 (Europe/Warsaw).
- Every scope, iterator and color-effect entry cited below was rechecked at the
  same line locations in clean output; no discrepancies found.
- `error.log` is empty (0 bytes) at inspection after generation. This is a startup
  and API-generation observation only: save/bookmark and map-mode interaction
  coverage have not been established, and no archived vanilla log baseline has
  been captured. R-011 remains partial under TEST_PLAN.md.

Raw output remains in the game's local logs directory, outside Git. No game
files were modified by the agent, and no rendering/lifecycle probes were run.
That follow-up led to R-002, now complete below. The next task at that point was R-003 (now completed below);
UI and runtime research remain gated separately.

## VERIFIED — CK3 1.20.1.1 (Crozier) generated script_docs

**Evidence recorded:** 2026-10-20, static inspection of generated logs from the
installed build. Sources are local files under
`${CK3_USER_DATA}/logs/`.
Raw logs remain outside the repository. The clean follow-up above reconfirms these entries. No rendering/runtime probes were run.
These findings address API portions of R-006, R-007, R-008 and R-009; they do not
close the UI, runtime rendering or state-safety research gates.

### Liege traversal — R-007

`triggers.log:1816–1819` documents:

```text
any_liege_or_above = { <count=num/all> / <percent=fixed_point> <triggers> }
Supported Scopes: character
Supported Targets: character
```

The entry specifies all lieges above the scoped character, excluding the
character itself. Therefore the DIRECT holder-Dynasty check must happen
separately before CONTROLLED traversal. A holder without a Dynasty still needs
its liege chain checked. Special-government runtime behavior remains untested.

### Formal scope links — R-006 / R-008

| Link | Input scope | Output scope | Generated evidence |
|---|---|---|---|
| `holder` | `landed_title` | `character` | `event_targets.log:920–922` |
| `dynasty` | `character` | `dynasty` | `event_targets.log:550–552` |
| `house` | `character` | `dynasty_house` | `event_targets.log:610–612` |
| `house_dynasty` | `dynasty_house` | `dynasty` | `event_targets.log:1145–1147` |
| `county` | `landed_title` or `province` | `landed_title` (de-jure county) | `event_targets.log:1548–1550` |
| `barony` | `landed_title` or `province` | `landed_title` (de-jure barony) | `event_targets.log:1536–1538` |

The documented containing-county link is `county`. Conceptual notation such as
`capital_county(B)` in algorithm discussions is not a verified CK3 API call.

### County, barony and Dynasty/House iterators — R-008 / RG-COLOR-01

| Iterator | Listed input scope | Iterated target | Generated evidence |
|---|---|---|---|
| `every_county` | `none` | `landed_title` | `effects.log:773–776` |
| `every_barony` | `none` | `landed_title` | `effects.log:731–734` |
| `every_dynasty_house` | `dynasty` | `dynasty_house` | `effects.log:16177–16180` |
| `any_dynasty_house` | `dynasty` | `dynasty_house` | `triggers.log:11638–11641` |

The effect iterators document `limit = { <triggers> }` and an effects body.
The any-trigger documents the count/percent form used by `any_liege_or_above`.
House enumeration exposes identity/membership; it does not expose colors or a
renderer grouping callback.

`effects.log:11422–11427` also documents `every_in_de_jure_hierarchy` with
`landed_title` input and targets. It includes the starting title itself and all
de-jure descendants. `continue` controls recursion separately from `limit`.
The proposed county-to-barony filtering and rendering still need validation.

### Title-color effects — R-009 / RG-STATE-01

| Effect | Documented input and value/target | Generated evidence |
|---|---|---|
| `set_title_color` | `landed_title`; named colors or RGB, with example `set_title_color = { 255 0 0 }` | `effects.log:12761–12767` |
| `set_color_from_title` | `landed_title`; `set_color_from_title = <some title>`, target `landed_title` | `effects.log:12646–12649` |

`set_color_from_title` intentionally shifts the copied color slightly to avoid
an identical value. Do not assume identical RGB values across titles using the
same source. No replacement color strategy is selected by this finding.

Barony iteration yields the `landed_title` scope accepted by these effects;
this verifies scope compatibility, not safe temporary rendering. Persistence,
restoration and map-only isolation are UNKNOWN.

### Still UNKNOWN

- temporary map-only coloring and save persistence;
- safe restoration on exit, context loss or mod removal;
- refresh/recompute lifecycle and dependable activation/re-click behavior;
- custom grouping/classification callback for the native renderer;
- native House map color source and direct House/Dynasty color access;
- runtime performance and color leakage into other map modes.

These remain open M0 questions. Generated script_docs signatures do not by
themselves verify visual results, local-only execution or lifecycle safety.

## VERIFIED — R-002 installed map-mode definitions (2026-10-20)

**Target:** CK3 1.20.1.1 (Crozier), reconfirmed in installed launcher metadata.
Read-only inspection of `game/gfx/map/map_modes/map_modes.txt` (6,239 lines;
SHA-256 `feb28bbd29604cda4aeae2ac31e99f44fa4092b2de163f765b219a8e7775b115`).
No files were copied from vanilla or modified, and no runtime probe was run.
R-002 / [#2](https://github.com/mhaduk/ck3-dynasty-map/issues/2) is complete
as static definition research; custom loading and rendering are not verified.

### Definition structure and relevant native objects

The file contains 79 top-level named objects plus shared `@` constants. Each
object selects native renderer/naming/selection modes; a definition name need
not equal its `color_mode`. This is observed file syntax, not an exhaustive
schema of accepted engine fields or values.

| Installed evidence (game-relative file above) | Original finding |
|---|---|
| Lines 1–106 | Shared constants govern zoom thresholds and gradient/edge presentation. A separate original definition cannot assume these constants are visible across files. |
| Lines 109–114 | `debug_terrain` selects `terrain` coloring, `realms` map names and `holding` selection; not every native object contains gradient blocks. This does not prove those blocks are optional for a custom barony renderer. |
| Lines 116–195 | `baronies` uses `color_mode = baronies`, barony names/selection, `fill_in_impassable = no`, and repeated gradient blocks. This confirms the native barony renderer token exists in this target build. |
| Lines 196–201 | `counties` uses county coloring, names and selection. County semantics and barony rendering remain distinct choices. |
| Lines 276–281 | `realms` uses `selected_character_realms` coloring and different small/large naming modes; IDs are not interchangeable with renderer values. |
| Lines 2961–2967 | `houses` selects native House coloring, `county_houses` / `explored_houses` names, House selection, impassable fill and a tooltip key. No Dynasty grouping/color callback is exposed in this object. |
| Lines 5399–5406 | A native `dynastic_cycle` object exists; its name alone does not establish the county/Dynasty semantics required by this project or a reusable grouping API. |

Across the inspected file, observed immediate object fields are `color_mode`,
`small_map_names`, `large_map_names`, `selection`, `fill_in_impassable`,
`gradient_parameters`, `barony_description`, `selection_description` and
`select_holdings_on_close_zoom`. These are presentation/selection/description
settings, not evidence of an arbitrary scripted classification callback.
No sub-mode declaration, scripted-GUI invocation or activation/exit callback
was found in this definition file. Absence here does not prove engine absence.

### Format documentation and extension boundary

The map_modes directory contains only `map_modes.txt`; no adjacent `.info`
exists there or directly in `gfx/map`. A search of installed `gfx/**/*.info`
found a map-mode mention in `gfx/map/province_effects/_province_effects.info:16`,
but no map-mode definition schema. This is a bounded search, not a claim that
no other engine documentation exists.

The smallest candidate remains an **original**, uniquely named object in
`gfx/map/map_modes/dynmap_map_modes.txt`, selecting the verified native
`baronies` color mode. Separate-file discovery/merge behavior, required fields,
constant visibility, selectable custom names and actual visual results are
still UNKNOWN until an authorized minimal probe. Do not copy the vanilla file
or advertise additive loading as verified. GUI exposure is separate research:
the installed candidate is `game/gui/shared/mapmodes.gui` (R-003 / #3).

**Decision:** retain the existing architecture and candidate path; no ADR change
is needed. The historical barony renderer token is now confirmed locally, but
its temporary color-write safety remains R-009 / RG-STATE-01. Native House
internals and All Dynasties color access remain gated. No contradiction with
accepted project semantics was found. **Next task at R-002 completion:** R-003, inspect the
installed GUI and generated GUI types for insertion, unavailable state and
activation/manual-refresh/exit/context-loss hooks, distinguishing static
bindings from runtime behavior. R-010 chooses the integration strategy later.

## VERIFIED — R-003 installed GUI bindings (2026-10-20)

**Target:** installed CK3 1.20.1.1; static read-only GUI inspection and clean
12:17 generated data types. R-003 / [#3](https://github.com/mhaduk/ck3-dynasty-map/issues/3)
completes inspection only. RG-UI-01, RG-PLAYER-01 and RG-STATE-01 remain open;
no custom GUI, rendering or lifecycle runtime probe has been executed.

### UI structure and extension candidates

Sources below are relative to installed `game/`:

| Evidence | Original finding |
|---|---|
| `gui/hud.gui:2542–2554` | The live HUD instantiates the shared `map_modes` type; defining a new derived type alone does not establish that HUD will instantiate it. |
| `gui/shared/buttons.gui:1116–1170` | `icon_button_mapmode` has `mm_datacontext`, `mm_button` and `mm_icon` blocks. Its round button calls SetMapMode using MapMode.GetKey, derives down/glow state from IsMapMode and gets tooltip/icon through MapMode. |
| `gui/shared/mapmodes.gui:426–480` | Text and small round selectors call SetMapMode; both set alwaystransparent when already active. They cannot be assumed to provide re-click refresh. The main icon button uses down state instead; actual event delivery and recomputation remain untested. |
| `gui/shared/mapmodes.gui:483–526,1114–1158` | Additional-mode container has an empty `mapmodes_insert_before` block, overridden by the native mini-mode instance to insert controls. This proves local type/instance composition, not cross-file injection into the existing HUD. |
| `gui/shared/mapmodes.gui:1165–1214` | Faith sub-modes are explicitly enumerated as buttons for religions, holy_orders and clerical_regions, visible for those mode keys. This is not an automatic list of all mode definitions. |
| `gui/shared/mapmodes.gui:1255–1395` | Header labels enumerate known modes with IsMapMode visibility; custom key/header discovery is not established. |
| `gui/shared/mapmodes.gui:1398–1407` | Back-to-realms button calls SetMapMode('realms') and has a close-window shortcut. No custom color-restoration call is present there. Switching renderer is not proof of restoring changed title state. |
| `gui/shared/mapmodes.gui:1559–1600` | Banner offers named visibility/background/sub-mode blocks and _show/_hide animation states. The animations alone do not establish safe classification/cleanup hooks. |
| `gui/hud_bottom.gui:286–307` | Actual in-game banner instance overrides sub-mode content and adjusts faith controls. Patching only the shared default may not affect the instantiated content. |

No map-mode datamodel that automatically enumerates arbitrary custom modes was
found in the inspected shared file. Named blocks are promising seams for
**original** integration, but a safe way to reach the existing instance from a
separate mod file remains UNKNOWN. Do not treat a block name as a global patch
API, copy vanilla files, or select an override strategy before R-010.

### Generated GUI APIs and player context

All references below are in local `logs/data_types/`:

| Evidence | Verified exposed API |
|---|---|
| `data_types_uncategorized.txt:523–525,1399–1401,2743–2745,3187–3189` | GetMapMode returns MapMode; CanChangeMapMode and IsMapMode return bool; SetMapMode returns void. Argument types/side effects are not fully documented by these entries. |
| `data_types_uncategorized.txt:86122–86160` | MapMode exposes GetDesc, GetIcon, GetKey, GetName, HasIcon and self access. No lifecycle callback appears in this inspected type section. |
| `data_types_uncategorized.txt:571–573,34627–34629,40963–40965,61153–61155` | GetPlayer returns Character; Character.GetDynasty returns Dynasty; Character.IsValid and Dynasty.IsValid return bool. This does not prove chained null access is safe or boolean evaluation short-circuits. |
| `data_types_gui.txt:1–4,15–18` | GetScriptedGui returns ScriptedGui; GuiScope returns TopScope. |
| `data_types_script.txt:3944–3976` | ScriptedGui.Execute takes an argument and returns void; IsShown/IsValid return bool, with tooltip variants. Execution guards/locality must still be verified. |
| `gui/activity_window_widgets/funeral_deceased_selection_button.gui:27–28` (installed game) | A vanilla button explicitly constructs GuiScope.SetRoot(GetPlayer.MakeScope).End for scripted-GUI execution and has a second onclick. This is a target-build syntax example, not proof of absent-player safety or map refresh ordering. |

The map-mode buttons inspected do not invoke a scripted GUI and do not supply a
verified implicit character root. A future original button must explicitly
establish and revalidate its context. Native visible bindings (for example
mapmodes.gui:103,539,598) show conditional visibility is used; CanChangeMapMode
alone is not a valid-player/Dynasty guard. Exact ADR-008 UI guards, hidden versus
disabled behavior, attempted unavailable activation and context-loss cleanup
remain R-005/R-010 runtime questions. ScriptedGui.IsValid exposure alone does
not establish that Execute enforces the same guard.

### Gate disposition and next step

Re-click refresh, execution ordering/locality, switching-player/observer cleanup,
exit restoration and safe GUI injection remain UNKNOWN. No generic map exit or
player-context invalidation callback was identified in the inspected files;
this is a bounded negative result, not proof that no such API exists elsewhere.

**R-003 inspection is complete; no integration strategy is approved.** R-005
(player safety) and R-010 (integration feasibility) are now Ready for research,
not implementation. R-009 runtime work still awaits an authorized minimal probe
and its prerequisites. **Single next task: R-010**, read-only investigation of
original additive/minimal integration feasibility under ADR-006, tracing the
observed blocks to the live HUD. If no compliant insertion mechanism can be
established, report RG-UI-01 blocked rather than copying vanilla or relaxing policy.

## VERIFIED — R-010 additive widget registration documentation (2026-10-20)

**Target:** installed CK3 1.20.1.1. Read-only inspection; no implementation,
launcher changes or runtime probes. R-010 / [#10](https://github.com/mhaduk/ck3-dynasty-map/issues/10)
is **Partial**, not complete. Its visibility, refresh and lifecycle acceptance
still require runtime evidence after relevant prerequisites and authorization.

### Newly found documented entry point

Installed `game/gui/scripted_widgets/_scripted_widgets.info` (9 lines;
SHA-256 `c5e1e671c0328e37a11aa56004033f4609ed8709b56128b8ac4de2394b8ff3ad`)
documents a registration mechanism:

- Lines 1–5: registration entries pair a GUI file path with a widget name;
  the engine creates the referenced widget at startup without a code reference.
- Line 7: each registration creates an instance; duplicate registration creates
  overlapping instances at their scripted location. Use one registration and
  unique dynmap-prefixed paths/names.
- Line 9: all registration files are loaded, allowing multiple mods to provide
  widgets without sharing paths. This is installed documentation of additive
  registration, not a runtime test of this project.

The installed registration directory contains only this `.info`; no native
registration example establishes placement or lifecycle beyond the description.
Existing `gui/hud_bottom.gui:1–6` shows a top-level widget, default-GUI visibility
and a layer declaration; these are syntax references, not proof of which layer,
input behavior or anchor a registered custom widget should use.

### Feasibility result and scope boundary

A candidate needing no vanilla copy is a single original registered widget,
with a unique registration file under `gui/scripted_widgets/` and a separate
original GUI file under `gui/`. Both owned filenames/IDs should use dynmap_
prefixes where allowed. Do not create these files during read-only research.
The registration file extension/parser behavior and cross-file lookup still
need a minimal probe; the `.info` does not specify a complete file schema.

This supports investigating a **separate additive control**, positioned near
the native map UI if safe. It does not prove insertion into the existing map
menu, a new native sub-mode group, or cross-file replacement of shared blocks.
A new type by itself remains insufficient to alter the live HUD instance.
Separate-widget native-feeling placement must be reviewed and tested before
selecting a final integration strategy; no architecture/semantic ADR is changed.

A candidate control would use already exposed SetMapMode/IsMapMode bindings
and an explicitly constructed, revalidated player scope for scripted execution.
Do not use the active-state-transparent text selector as assumed refresh UX.
A smallest explicit refresh control remains an option if re-click cannot be
verified, but neither its event ordering nor safe execution is verified here.

RG-UI-01 is **open with a documented candidate**, not policy-blocked: no evidence
currently establishes that copying vanilla is necessary. Runtime widget loading,
menu/observer visibility, absent-player/Dynasty guards, duplicate instances,
UI scale/overlap/input, refresh/re-activation, player-context loss and cleanup
remain unverified. RG-PLAYER-01 and RG-STATE-01 remain open. No title colors were
written and no recurring work was added.

**Next single task:** R-005, read-only inspection of local-player/Dynasty guard
syntax, scripted-GUI execution context/guard behavior and available invalidation
hooks. Record which checks are static evidence and which require a future
explicitly authorized minimal probe. Do not treat that next task as permission
to create GUI/scaffolding or claim safety from method names alone.

### R-010 follow-up — native menu requested (2026-10-20)

The user explicitly prefers placement inside the existing map-mode menu;
a standalone adjacent widget is not the selected integration strategy.
This clarifies UI preference without changing classification semantics or ADR-006.

**VERIFIED static attachment chain:** `game/gui/hud.gui:2542–2554` instantiates
`map_modes`; `game/gui/shared/mapmodes.gui:419–423` instantiates
`flowcontainer_additional_mapmodes`; that type is defined at 483 and contains
`mapmodes_insert_before` at 526–529 inside the vertical menu content. A native
mini-mode instance overrides that block at 1120. Therefore this block is a
concrete candidate for an actual menu child, rather than a separate overlay.
The existing main icon rows around lines 278–406 have explicit button lists;
no automatic custom-mode enumeration was identified.

**Additional static evidence:** `game/gui/preload/defaults.gui:102,294–302`,
`game/gui/shared/lines.gui:4` and `clausewitz/gui/toolstypes.gui:875–878` use
same-name base/derived type spelling (for example built-in widget/flowcontainer
or engine tool types). This suggests a type-decoration avenue to investigate,
but does NOT prove that re-declaring the script-defined additional-menu type
preserves its old body, resolves the intended base, or affects existing HUD
instances. Cross-file resolution, namespace behavior and load order are UNKNOWN.
Do not publish a self-inheritance recipe as verified mod syntax.

A bounded scan of 416 game, 49 Clausewitz and 91 Jomini `.gui` files found no
working explicit inject/reparent/child-append mechanism under the searched
keywords (one comment-only parentwidget hit). A targeted scan of generated
data types likewise found no matching runtime parent/child mutation API.
This does not establish impossibility or exclude APIs under other names.

**Result:** native-menu integration is a concrete candidate, not proven possible
or impossible under the current no-copy policy. Scripted-widget registration
alone does not attach a widget to that menu. RG-UI-01 / R-010 remain open.

**Concrete next evidence needed for this question:** an explicitly authorized,
isolated menu-only GUI probe using original files to test the narrow menu-type
extension/block override. Success means one inert, uniquely named test button
is a real child in Additional map modes, follows native layout/open/close, and
preserves existing entries without duplicate widgets or new GUI errors. No map
mode definition, title/dummy title, color effect or world scan is needed for
that test. Verify load order/type resolution; stop on failure rather than
copying vanilla. This report creates no probe/scaffolding and does not authorize
it. R-005 read-only safety research remains independently available.

### R-010 authorized menu-only probe prepared (2026-10-20)

After the concrete proposal, the user approved preparing the inert-button
native-menu test. Original source and procedure are in
[research/probes/native-menu](../research/probes/native-menu/README.md).
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
Mac model `Mac16,10`, previously UNKNOWN during the R-001 system query.

The additional launcher text shows successful Steam library loading and two
undefined log categories. It is not evidence that Steam connectivity caused the
crash; the recursion stack is the relevant diagnostic evidence.

**Containment verified:** raw crash report and launch logs archived in ignored
local/evidence/native-menu-probe/crash-01. Launcher Home switched to No mods;
mod-load JSON confirms zero enabled mods. The installed GUI was quarantined as
`.gui.disabled` with filesystem approval; matching original source moved to
[failed probe source](../research/probes/native-menu/failed/dynmap_native_menu_probe.gui.disabled).
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
[Reviewed test evidence](evidence/2026-10-20-r010-native-menu/README.md) contains
original test notes, selected diagnostic excerpts and two user-supplied images
(target menu before the probe and crash dialogs). Raw logs/reports, local paths
and account/incident identifiers are excluded from tracked evidence. Failed
original source stays disabled. R-010 remains open; the next task is research
into a materially different original native-menu integration method.

## Historical/reference findings pending M0 verification

### Custom map modes are possible but historically not a first-class stable mod API

The CK3 modding guide documents a custom map-mode approach based on:

- `gfx/map/map_modes/`
- `common/scripted_guis/`
- map-mode GUI integration
- barony color changes via `set_color_from_title`

The same guide explicitly warns that custom map modes are cumbersome, maintenance-heavy and prone to compatibility issues.

### Color writes should target baronies

A later War Maps fork documents a hard-earned implementation rule: copy map colors to **baronies**, not higher title tiers, or the map can render incorrectly/blue. This aligns with the public guide's `color_mode = baronies` approach.

### Static refresh has historical precedent

War Maps and Family Matters used static custom maps that update when the user clicks the mode again. War Maps also had a dynamic monthly mode, but static maps were the default for more complex relationship views.

### A Dynasty/My Dynasty map has precedent

Silk Road advertised a `My dynasty` map mode. Family Matters credits Silk Road for Dynasty Map Mode code, and War Maps credits/adapts the same lineage. This demonstrates that dynasty-related territory coloring is technically feasible, even though those implementations are old and not directly portable to CK3 1.20+.

### Candidate hierarchy trigger

The historical candidate is now VERIFIED at the generated-API level for CK3 1.20.1.1: character input/targets, all lieges above the character, self excluded. See the generated evidence above; runtime government-specific behavior remains untested.

### CK3 provides profiling and generated API docs

- Reference documentation describes `script_docs` and `dump_data_types` as API documentation generators; verify their output on the installed build.
- Reference documentation describes an in-game Script Profiler in dev/debug mode; verify its entry point and measurements during M0.
- The recorded patch reference reports expanded `.info` documentation in 1.20.1; inspect what the installed build actually provides.

### Static validation tooling exists

`ck3-tiger` checks syntax, missing items, localization and scope consistency against vanilla + mod files. It can be run locally and has VS Code integration. This should complement, not replace, in-game `error.log` testing.

## Important CK3 1.20 change

The recorded CK3 1.20 patch reference reports a map-mode UI change: map modes with sub-map modes now show round sub-mode buttons above the map-mode name. Old tutorials that instruct copying and editing a specific block in `mapmodes.gui` cannot be assumed correct for 1.20+.

This is a **hard research gate** before implementing UI.

## Community-reported failure modes relevant to this project

1. **Map GUI conflicts.** Mods that replace/edit map-mode GUI files often conflict by load order.
2. **Patch breakage.** Older map-mode mods broke after UI/map-mode changes (community reports around 1.18 and later).
3. **Wrong title tier for color effect.** Community fork notes that using `set_color_from_title` on non-baronies can produce a broken/blue map.
4. **Error-log spam.** War Maps had a dedicated discussion about `set_color_from_title` log spam; exact root cause must be reproduced/avoided on current CK3.
5. **Observer/global-variable issues.** War Maps' author reported difficulty making multiple map modes work in Observer mode and suspected global-variable interactions.
6. **Multiplayer uncertainty.** Family Matters explicitly treated global-variable-based updates as incompatible with multiplayer; War Maps did not claim verified multiplayer support.
7. **Stale static maps.** Static maps need a re-click/refresh after title changes.
8. **Full GUI copy maintenance.** Map mods that copy vanilla GUI/map-mode files become fragile when Paradox adds or restructures modes.

## Open research gates

### RG-UI-01 — Current UI insertion method
Can the installed build add custom modes without replacing the full vanilla map-mode GUI? Determine UI disabling/hiding for unavailable My Dynasty (ADR-008), valid activation, a dependable refresh path and exit/restore. Verify re-click before using it; otherwise select the smallest explicit refresh mechanism needed for v0.1.

### RG-PLAYER-01 — Local player scope
What exact root/context is provided to the scripted GUI invoked from the installed map-mode button? Prefer a local-player-aware scope rather than global player iteration. Verify valid-player/Dynasty checks and safe invalidation on player switching, succession, observer transitions and reload; stop old-context use and clear/restore visuals as far as the API permits without recurring world scans.

### RG-COLOR-01 — All Dynasties color source
Does the native House map expose any reusable House/Dynasty color data or grouping hook?

### RG-STATE-01 — Save persistence
Does the chosen color mechanism affect other map modes or persist in saves? Verify restoration on exit/context loss and what remains after disabling the mod. Record any pre-1.0 removal limitations; v1.0 requires safe removal or a proven harmless removal path.

### RG-MP-01 — Multiplayer
Are map-color effects/UI execution local-only, synchronized, or desync-prone? Multiplayer remains unsupported until deliberately tested.

## Reference sources (not target-build verification)

- CK3 Modding Wiki / Git mirror — Map modding: https://github.com/jesec/ck3-modding-wiki/blob/master/wiki_pages/Map_modding.md
- CK3 Modding Wiki / Git mirror — Modding/debug workflow: https://github.com/jesec/ck3-modding-wiki/blob/master/wiki_pages/Modding.md
- Archived CK3 script effects reference (repository archived in 2023): https://github.com/CK3-Modding/Documentation/blob/master/docs/scripting/effects.md
- CK3 trigger reference (`any_liege_or_above`): https://github.com/jesec/ck3-modding-wiki/blob/master/wiki_pages/Triggers_list.md
- CK3 Tiger: https://github.com/amtep/tiger
- Silk Road Workshop page: https://steamcommunity.com/sharedfiles/filedetails/?id=2493459927
- Family Matters Workshop page: https://steamcommunity.com/sharedfiles/filedetails/?id=2624459127
- War Maps Workshop page: https://steamcommunity.com/sharedfiles/filedetails/?id=2624748092
- War Maps 3 note on barony coloring: https://steamcommunity.com/sharedfiles/filedetails/?id=3450639748
- CK3 1.20.0 changelog / sub-map-mode UI: https://steamdb.info/patchnotes/25588574/
- CK3 1.20.1 changelog: https://steamdb.info/patchnotes/25870654/
