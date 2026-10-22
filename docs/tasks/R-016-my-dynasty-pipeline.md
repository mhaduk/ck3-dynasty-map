# R-016 — Historical My Dynasty pipeline validation plan

Status: CLOSED — RESEARCH COMPLETE WITH LIMITS — three approved views and target layout
prepared, installed and exercised in bounded 1.20.1.2 startup/runtime smoke,
2026-10-21. The pipeline executes and the user reports normal switching/refresh/
native-return operations appear to work. Visual acceptance failed for the grey
nonmatching background; full semantics, coverage, performance, context safety,
and persistence/removal remain open. This is research closeout, not production
acceptance. Three earlier empty-name load diagnostics did not recur in a fresh
new game; cause/helper persistence remain unresolved. Preserve dated evidence.
Issue: [#16](https://github.com/mhaduk/ck3-dynasty-map/issues/16).
Current target: CK3 1.20.1.2 (Crozier), Steam build 26046173. Original
research/API baseline and first startup: 1.20.1.1 / 25913294.

## Goal and current scope

[ADR-010](../DECISIONS.md#adr-010--three-dynasty-views-and-their-native-map-layout)
defines one Dynasty map entry with Dynasty Realms first/default, Dynasty Holdings
second and My Realm & Dynasty third as active-map subviews. Each computes fresh
county categories and projects dark green, light green or grey to constituent
baronies. Holdings preserves historical DIRECT/CONTROLLED/OTHER. Realms uses the
highest de-facto ruler for dark; My Realm uses only the player's own subtree,
including when the player is a vassal. All three check the full senior chain for
light where applicable, retain cadet identity and lowborn-holder senior checks,
and reject invalid P/D before any pass. Read the current truth table in
[TEST_PLAN](../TEST_PLAN.md#my-dynasty-functional-matrix).

All Dynasties remains deferred. No excluded gameplay carrier, background scans,
saved selection cache, production-readiness claim or lifecycle waiver. Target
layout is part of this research revision; ordinary activation is a candidate,
not a proven atomic success boundary. R-015 stays closed. Source preparation, installation and bounded runtime smoke are complete;
remaining production gaps are recorded in the closeout.

The original Stage A design and dated checkpoints below are historical Holdings
work and retain their original labels/builds. They do not prove new predicates.

## Inputs and corrections to the supplied handoff

The issue and supplied technical handoff define the research candidate, not a
target-build feasibility result. Historical source claims need source review;
secondary engine, corruption and performance claims are hypotheses.

Reuse rather than rediscover:

- [Source hierarchy](../CK3_SOURCE_MAP.md), [R-002](R-002-map-mode-definitions.md)
  and [R-006](R-006-scope-links.md).
- [R-007/R-008 signatures](../RESEARCH.md#liege-traversal--r-007):
  `any_liege_or_above` excludes the starting character; `every_county` is a
  world iterator; `every_in_de_jure_hierarchy` includes the starting title and
  needs barony filtering. Runtime behavior/coverage remain open.
- [R-005](R-005-player-context.md): explicit fresh player root and bounded
  unavailable-UI evidence. Do not revive NULL or rejected LOWBORN diagnostics.
- [R-009](R-009-barony-color-safety.md): direct/named/copy writes, shared native
  Baronies state and serialization already demonstrated. The
  [architecture record](../ARCHITECTURE.md) also records bounded loading and
  selection of separate custom definitions. Test the new integrated pipeline,
  not basic mutation or generic custom-mode loading again.
- [R-010 probe record](../../research/probes/native-menu-alternative/README.md):
  reuse the original primitive-based submenu approach. Current files contain
  R-005 diagnostics and reduced settings; do not mount them blindly as an inert
  baseline or reintroduce unsafe controls. General UI parity stays with R-010.

Persistent RGB does not establish corruption. Equally, normal Realms/Faith
appearance would not establish full isolation: native Baronies changes are
already known. Record effects separately from whether they are acceptable.
Do not implement restoration before evidence requires it; a no-restore product
choice must explicitly reconcile the observed effects with existing lifecycle
requirements. This plan does not waive them or select a production architecture.

## Stage A — bounded static research and exact design

Route: GUI owns scope/review; CLI uses Sol / High for unresolved CK3 reasoning.
No game/launcher state prerequisite, app/process/UI checks or user actions during
CLI execution. On proceeding, prepare one scoped `.codex-sync/CLI_TASK.md`;
do not execute Stage A under this planning-only checkpoint.

1. Review the four pinned historical source files linked in #16. Trace
   `line_dynasty_map`, `line_mapping_dynasty*` and `d_line_map_dynasty*` through
   relevant history/forks and the named Silk Road/Family Matters/War Maps
   sources only. Record searched sources/revisions and distinguish retained
   code from inferred behavior. Stop after this bounded search; failure to
   recover the old classifier does not block our own classifier.
2. Start from the existing R-006/007/008 evidence and source-map pointers.
   Resolve only missing syntax/context details: player Dynasty comparison,
   liege-chain predicate, world county iteration and county-to-barony filtering.
   Prefer county-first evaluation. Do not assume nesting a world `every_barony`
   iterator makes it county-local. Check scope preservation and invalid-holder,
   lowborn-holder and independent-holder branches. Document government limits.
3. Specify the smallest original map definition, guarded scripted GUI entry,
   effect helpers and adaptation of the R-010 menu. Establish activation/write
   order and what prevents unavailable entry from dispatching an invalid root
   or displaying stale colors. No payload yet.
4. Specify both fixed-color paths: direct `set_title_color` literals and copy
   from three non-creatable helper titles. Use existing R-009 evidence for
   supported writes; identify only remaining syntax, shift and helper side
   effects. No dynamic RGB or large helper-title palette.
5. Define natural/disposable fixture candidates, runtime observations, bounded
   log markers/counters and failure stop points for the matrix below.

Stage A deliverable: a concise source-cited report with historical classifier
recovered YES/NO; exact liege predicate; county-first YES/NO with reason; minimal
map definition; both color syntaxes; complete minimal file list; runtime-only
unknowns and evidence labels. Proposed file categories are `gfx/map/map_modes/`,
`common/scripted_guis/`, optional `common/scripted_effects/`, original GUI and
localization; `common/landed_titles/` only for the helper comparison.

Gate: GUI reviews actual evidence and design. If a required static link is
missing, identify it and stop probe preparation; absence in inspected text is
not engine-impossibility proof. Do not regenerate docs, broadly rescan the
installation or reopen excluded carriers.

## Stage B — isolated diagnostic preparation

After the Stage A design is reviewed and this stage is authorized, CLI prepares
the minimal My Dynasty Test source, self-review, available static checks and
documentation together. Use Luna / Medium for settled mechanical preparation;
unresolved engine reasoning remains Sol / High. No production implementation.
No app-state prerequisite for source-only work. Installation is separately
stated in the next stage; CLI never waits for user actions.

Reuse the R-010 integration seam with only safe required controls. Ensure the
payload does not activate old NULL/SUCCESSION/LOWBORN actions. Provide three
obvious diagnostic colors, guarded fresh context, one manual refresh pass and
bounded execution/count markers. Avoid persistent instrumentation where possible.
Use a small selected area for the two color-path comparison; do not repaint the
world twice merely to compare colors. Record static checks honestly: parser or
Tiger success must not be claimed unless actually run; tooling setup stays R-012.

Gate: GUI reviews the actual payload, files, guards and test instructions before
installation. No speculative backup/restore infrastructure or automatic updater.

## Stage C — user-run validation in practical batches

Prerequisite: explicitly staged installation/test scope, CK3 closed for payload
changes and launcher opened by the user through Steam when configuration is
needed. CLI assumes the declared state. Codex preserves existing logs and prior
selection in the existing test playset, installs/configures the intended probe
and verifies files/selection. User alone launches, observes and controls CK3.
Use a disposable timeline and copies; preserve the primary campaign.

| Batch | User actions / evidence | Pass or decision |
|---|---|---|
| C1: startup and local comparison | Start/load disposable session; compare direct/copy colors on the selected area at matching zoom; inspect county capital and secondary baronies | New payload loads; categories remain legible and county-consistent; helper/UI effects recorded; choose color path |
| C2: integrated world refresh | Activate My Dynasty; inspect known semantic cases; switch to Realms/Faith/Culture/relevant De Jure and back | Three categories coexist; complete county-to-barony projection; per-view changes recorded against pre-color observations |
| C3: refresh and performance | Re-click active mode; leave/re-enter; after a relevant natural ownership/liege change request refresh | Bounded markers distinguish execution from visual refresh; new classes replace old ones; record world counts, approximate delay and user-observed hitch |
| C4: persistence and removal | Save a disposable copy; user exits/restarts and loads it; check critical views; then, only if safe and explicitly staged, repeat with probe disabled | Load results, shared-state appearance and bounded log differences recorded; no untested removal-safety claim |

Required semantic cases: DIRECT including cadet-House identity; CONTROLLED via
immediate liege; CONTROLLED via a deeper dynastic senior below a foreign top
liege; OTHER; independent foreign and independent dynastic holder. Include a
lowborn holder under a dynastic senior when available. Prefer natural fixtures;
do not mutate gameplay to manufacture them without a concrete accepted fixture
scope. Missing cases remain limitations, not passes. Do not infer arbitrary
depth merely from one two-level runtime example; combine documented traversal
semantics with the discriminating fixture.

Re-click failure permits testing leave/re-enter as the manual-refresh contract.
Do not create a dedicated updater before that result. Assess performance from
measurement and user experience; do not invent a numerical success threshold.
If unacceptable, first review duplicate work in county/barony traversal.

Reuse R-005 guards without repeating passed lifecycle cases. Assess the new
pipeline's stale-context/visual-state limits separately; lack of a no-Dynasty
local-player fixture stays with R-013. GUI-marker clearing is not RGB cleanup.

At each batch, Codex gives exact short actions and a stop point, then correlates
the user report with the bounded log interval and baseline. Stop on crashes,
probe-attributed errors, incorrect coverage or harmful side effects; preserve
evidence instead of continuing. Before fresh-process/disabled-mod stages, state
the required exit/launcher state. After final user exit restore prior playset
selection; launcher restoration is not proof of in-game visual restoration.

## Exit decision and documentation

- Feasible candidate: identify classifier, color path, actual refresh contract,
  observed persistence/removal behavior, performance and remaining limits.
  Explicitly surface the known native Baronies effect; accepting that product
  compromise is a decision, not a technical test result.
- Restoration needed: name the reproduced affected view/state and return the
  smallest unresolved restoration question to R-009; do not build recovery
  infrastructure inside this feasibility task.
- Not feasible or partial: name the failed/unproven link (scope, projection,
  activation, rendering, refresh, leakage or performance). Distinguish a
  reproduced failure from missing evidence and from unfinished production gates.

Keep this canonical task, CURRENT_STATE and BACKLOG synchronized as stages
advance. Add reusable findings to RESEARCH only when established; record ADR
changes only after an explicit decision. TASK_HISTORY gains no completion row
until task completion. No staging, commit, push or GitHub writes are authorized
by planning; public notes exclude raw logs, saves, generated docs, copied vanilla
bodies and machine-specific/private data.


## Stage A checkpoint — 2026-10-21

Delegation `R016-STAGE-A-20261021-01` completed static research and self-review.
At that checkpoint, GUI review of the source report and entry/display gate was
next; Stage B had not yet been authorized. No payload, installation,
game/launcher operation, new dumps or tool setup had occurred then. The later
GUI disposition and Stage B checkpoint below supersede that next-action note.

### Historical result

**Classifier recovered: NO**, within the bounded search. At pinned revision
`20252db3e22d621c594a0aa77c8d238531d84f23` of CK3-infrastructure:

- [Map definition](https://github.com/SebastianDanielFrenz/CK3-infrastructure/blob/20252db3e22d621c594a0aa77c8d238531d84f23/gfx/map/map_modes/map_modes.txt#L2613-L2619)
  names the object `line_dynasty` and selects `color_mode = baronies`.
- [GUI](https://github.com/SebastianDanielFrenz/CK3-infrastructure/blob/20252db3e22d621c594a0aa77c8d238531d84f23/gui/shared/mod_gui.txt#L865-L879)
  selects that object and invokes `line_dynasty_map` with an explicit player root.
- [Palette](https://github.com/SebastianDanielFrenz/CK3-infrastructure/blob/20252db3e22d621c594a0aa77c8d238531d84f23/common/landed_titles/wm_map_color_title.txt#L1-L81)
  credits Silk Road and retains fixed Dynasty-family helper colors.
- The retained [infrastructure scripted GUI](https://github.com/SebastianDanielFrenz/CK3-infrastructure/blob/20252db3e22d621c594a0aa77c8d238531d84f23/common/scripted_guis/infra_map_mode_gui.txt#L1-L5)
  calls an [effect](https://github.com/SebastianDanielFrenz/CK3-infrastructure/blob/20252db3e22d621c594a0aa77c8d238531d84f23/common/scripted_effects/infra_map_color_effect.txt#L143-L178)
  which classifies world baronies and copies helper colors. This supports the
  generic pipeline, not the missing Dynasty classifier or historical runtime.

The five listed default-history revision trees and unique relevant file versions
were inspected; the public forks response was empty. Two discovery passes used
`line_dynasty_map`, `line_mapping_dynasty*`, `d_line_map_dynasty*` and the named
Silk Road/Family Matters/War Maps sources. No classifier source was recovered.
The four named Workshop descriptions were read; no package download, account
change or broader mod search followed. Family Matters credits Silk Road's
Dynasty map; War Maps describes re-click refresh. These are author descriptions,
not target-build API or runtime validation. Web blob reads failed with cache
misses; public raw/API fetches succeeded. Full search/revision register and
original design snippets remain in the local Stage A handoff report.

### Exact candidate and static evidence

**County-first: YES, for the diagnostic design.** Capture the fresh valid player
Dynasty once with `save_scope_as`; use `every_county`, guard holder existence,
then test holder Dynasty for DIRECT. Otherwise evaluate in holder scope:

```text
any_liege_or_above = {
    trigger_if = {
        limit = { exists = dynasty }
        dynasty = scope:dynmap_r016_player_dynasty
    }
    trigger_else = { always = no }
}
```

A lowborn holder still reaches this traversal. Each senior without Dynasty is
a nonmatch; independent foreign holders have no matching senior. DIRECT wins;
cadet Houses share Dynasty identity; unheld counties are OTHER. No top-liege
shortcut, recursion emulation, persistent Dynasty cache or county-local claim
for a nested world `every_barony` is used. Each category helper starts back in
county scope and projects through `every_in_de_jure_hierarchy`, explicitly
`continue = { always = yes }`, with `limit = { tier = tier_barony }`. The county
itself fails the limit without stopping recursion. Secondary/unbuilt baronies
are not excluded by holder/holding filters.

This composes existing R-006/007/008 contracts. Additional narrow sources:
`effects.log:2675–2677` supports saved scope identity across an unbroken chain;
`common/scripted_triggers/00_elective_triggers.txt:111–114` shows Dynasty identity
equality; `common/scripted_effects/00_title_effects.txt:53–57` shows hierarchy/tier
filtering. Government-specific de-facto edges and province coverage remain
runtime-only. Operation-count savings from classifying once per county are not
measured performance.

The minimal original `dynmap_my_dynasty` object uses `color_mode = baronies`,
barony small/large names and selection, `fill_in_impassable = no`. This reuses
R-009's bounded separate-definition mechanism. Direct writes use three literals
(e.g. `{ 40 190 80 }`, `{ 225 150 35 }`, `{ 65 70 80 }`); the comparison path uses
`set_color_from_title = title:d_dynmap_r016_direct` and two corresponding fixed
helpers. Both normal and partition creation guards are false. Three original
CoA objects avoid repeating the known missing-CoA setup; helper visibility,
capital/CoA resolution and inertness remain unproven. No numeric copy-drift law
or visual uniformity is inferred from the documented slight shift.

The proposed minimal file categories are descriptor, separate map definition,
scripted GUI, scripted effects, original primitive-based R-010 menu adaptation
and localization. Only the copy comparison adds landed-title and original CoA
files. No production files were created. Current R-010 diagnostic callbacks and
unsafe controls must not be mounted as a baseline.

### Entry/display gate and remaining tests

The intended order is fresh valid entry → capture → classify/project → completion
→ map selection. The effect guards Dynasty existence before any scan/write.
R-005's external player-validity path is reused; no automatic character-scoped
polling, null-root call or rejected LOWBORN fixture is proposed. A manual
CHECK/READY diagnostic followed by guarded fresh-root activation is a candidate,
not an accepted final one-click availability contract.

**Missing contract:** `ScriptedGui.Execute` returns void
(`data_types_script.txt:3944–3946`); a fresh `IsValid` recheck after Execute proves
availability, not successful completion. Multiple onclick ordering, renderer
refresh and atomic protection against player loss are not established by the
reviewed signatures. Do not select the custom map unconditionally after a
possibly rejected call. GUI must resolve this gate or explicitly scope a
bounded valid-context diagnostic before Stage B. Absence of that contract in the
inspected surface is not engine-impossibility proof. GUI READY clearing is not
RGB cleanup; active-context stale visuals and ADR-008 lifecycle remain open.

The report specifies C1 small-area direct/copy comparison, C2 integrated world
classification/coverage and pre/post normal views, C3 re-click or leave/re-enter
refresh plus natural ownership change/performance, and C4 separately staged
fresh-process/disabled-probe persistence observations. Candidate multi-barony
sample: Middlesex, optionally Kent/Surrey; no live holder/class fixture was
verified. Deep CONTROLLED requires a dynastic intermediate senior below a foreign
top liege. Missing natural cadet/lowborn/unheld cases remain limitations.

Use bounded BEGIN/END/REJECT and GUI receipts, local counters rather than saved
per-title instrumentation, no world log flood or extra counting world scan.
Counter output/helper lifetime must be checked before claiming numeric coverage.
Stop on crash, attributed errors, wrong classification/coverage or harmful side
effects. Known native Baronies sharing remains explicit. Persistence is not
corruption; accepting shared persistent RGB requires a product/lifecycle decision.
No restoration system, ADR waiver or production architecture was selected.

Self-review and documentation checks only; no engine parser, Tiger, new runtime
or independent-review claim. No staging, commit, push or GitHub writes.

## GUI review disposition — 2026-10-21

Accepted Stage A as a bounded static checkpoint. The matching delegation/result,
actual incremental changes and preserved historical files were reviewed. Key
target-build citations were spot-checked directly: liege traversal, hierarchy
recursion/filtering, scope capture/clear, Dynasty equality, native mode fields,
partition creation guard and Execute's void signature. No runtime or genuinely
independent review was performed. Historical classifier recovery remains NO.

The entry/display gap limits a production one-click contract; it does not
establish that classification or rendering is unavailable. Proposed next scope:
source-only preparation of a valid-context diagnostic, with separate COMPUTE
and DISPLAY actions. On a paused disposable session with an unchanged valid
player/Dynasty, user requests computation; Codex verifies the bounded END/no
REJECT/error interval before instructing the first display. DISPLAY performs
no classification and is not presented as proof that Execute succeeded. A later
runtime handoff must define the exact controls, fresh availability checks and
stop on any context change. This is a diagnostic procedure, not a final UX or
an atomic invalid-player guarantee; reuse R-005 protection and preserve ADR-008.

Source preparation must not implement the report's speculative combined
Execute/Select_CString chain as a proven gate. Full one-click refresh, stale-view
handling, player transitions and unavailable entry remain explicitly open.
No installation/test cycle or gameplay fixture mutation is included in this
proposed Stage B. The later Stage B checkpoint records the authorized
source-only preparation and its current GUI review gate.

## Stage B checkpoint — 2026-10-21

Delegation `R016-STAGE-B-PREP-20261021-02` completed source preparation and
self-review. The isolated diagnostic is in
[`research/probes/my-dynasty-r016/`](../../research/probes/my-dynasty-r016/).
It provides separate CHECK, COMPUTE WORLD, COMPUTE SAMPLE (direct/copy) and
DISPLAY controls; the effect rechecks Dynasty before any county pass/write and
uses county-first classification plus barony-tier projection. The fixed sample
uses Middlesex, Kent and Surrey without assuming their current classes. The
copy path checks that all three helper titles exist and remain unheld before
writing; missing sample counties and rejected copy helpers have bounded log
markers. The original target-build CoA format was checked against narrow
shipped examples at
`<game>/common/coat_of_arms/coat_of_arms/01_landed_titles.txt:7–18,3863–3872`:
objects are keyed by landed-title key and use pattern/color fields. The
diagnostic uses matching title-keyed objects; this confirms syntax shape only,
not startup resolution.

The procedure preserves the accepted valid-context boundary: on an unchanged,
paused disposable session, the user requests computation; GUI reviews matching
BEGIN/END, absence of REJECT and new probe-attributed errors before authorizing
the first DISPLAY. READY is a fresh availability hint, not a success receipt.
No one-click completion, atomic context protection or lifecycle safety is
claimed. Local counters and their `debug_log_scopes` output need runtime
confirmation; inability to read emitted values leaves coverage unproven.

Self-review found no copied vanilla body or NULL/SUCCESSION/LOWBORN callback.
Only bounded offline source checks were run. CK3 parsing, Tiger, game/runtime,
launcher, installation, save or playset changes were not performed. No new
tooling/dumps, Git staging/commit/push or GitHub write occurred. Next: GUI review
of the actual payload, guards, menu integration and documented stop procedure;
installation/test readiness is a separate explicit stage.

### Stage B GUI review and correction — 2026-10-21

Matched `R016-STAGE-B-PREP-20261021-02` and reviewed actual callbacks, effects,
GUI, metadata, helpers, localization and procedure. Accepted for a bounded
installation/startup checkpoint after correcting one source-layout defect:
helper CoA definitions were initially at `mod/coat_of_arms/coat_of_arms/`;
moved the original file to `mod/common/coat_of_arms/coat_of_arms/`, matching the
installed `common/coat_of_arms/coat_of_arms/01_landed_titles.txt`. This also
corrects the earlier Stage A proposed tree. Pattern asset and named CoA colors
were checked in the installed build; actual object resolution remains untested.

Fresh compute roots, Dynasty guards before iteration/writes, county-first
DIRECT precedence/full senior traversal, county-to-barony filtering and separate
display action match the diagnostic design. READY is cached availability only;
no atomic context/entry protection is claimed. END also appears after rejection,
so log review must require no REJECT, no missing sample target and no attributed
error, not END alone. Local counter output is not validated. No dangerous R-005
fixture callbacks are present. General UI parity and helper invisibility remain
unverified. Source review is not engine/parser/runtime validation or genuinely
independent review.

Next proposed stage: user closes CK3 and opens its launcher through Steam,
then confirms readiness. That continuation authorizes isolated installation
and a user-run startup-to-main-menu checkpoint only. Codex preserves logs and
prior selection in the existing test playset; conflicting probe menu mods are
disabled for the run. CLI performs bounded install/file checks under declared
app state without process/UI checks; GUI configures the already open launcher.
User alone launches CK3 and stops at main menu. Review startup logs before
loading or requesting any classification; no world/sample writes, save/load
or mod-removal test is included in that first checkpoint. Installation has not
occurred; Git staging/commit/push and GitHub writes remain unauthorized.

### Installation checkpoint — 2026-10-21

Delegation `R016-INSTALL-20261021-03` completed under the declared app state.
The eight reviewed payload files were installed as a separate local user mod;
the installed inventory exactly matches the source inventory and every file
passed SHA-256 and byte comparison. The wrapper points to the installed mod
directory and retains `supported_version = 1.20.1.1`. The helper CoA file is at
`common/coat_of_arms/coat_of_arms/dynmap_r016_colors.txt`. Pre-install
`debug.log`, `error.log`, `gui_warnings.log`, `dlc_load.json` and a launcher
database snapshot were preserved in ignored local evidence. Log and DLC
manifest hashes remained unchanged; the launcher database file differed at the
post-install read, so prior playset selection is not established by this
checkpoint. The saved database copy passes SQLite integrity check. CLI did not
write launcher or playset configuration, and the source payload was not changed.

No CK3 startup, parser, Tiger, map loading, classification, save/load or runtime
validation occurred. Next, GUI configures the existing test playset, preserves
the prior selection and checks the resulting enabled-mod manifest. The user
then starts CK3 and stops at the main menu; startup logs are reviewed before any
save is loaded or classification is requested. Git staging/commit/push and
GitHub writes remain unauthorized. See the matching ignored CLI result for the
local installation and evidence paths.

### Installation review / launcher access — 2026-10-21

Consumed `R016-INSTALL-20261021-03`; independently re-read all eight installed
files and confirmed inventory/hash equality with the reviewed source. Wrapper
exists; runtime has not run. Native launcher UI access timed out twice;
selection by bundle ID was ambiguous across two launcher versions. No launcher
settings/database writes were performed. Read-only active-playset/selection and
manifest snapshots plus a consistent SQLite backup are preserved locally.
The existing `Dynasty Map - GUI Probe` playset still enables Native Menu Probe;
R005/R009 are disabled and R016 is not registered in the launcher database yet.
User fallback: refresh installed mods (reopen launcher through Steam if needed),
add the installed R016 diagnostic to the same playset, enable only it and report
readiness. Codex verifies the resulting manifest before giving launch steps.
The previous selection is retained for restoration; no save/classification step
is included in the authorized startup-to-main-menu checkpoint.

### Launcher identity resolved / startup ready — 2026-10-21

The user supplied launcher/process screenshots and requested correcting agent
identification guidance. A launcher-only executable lookup showed the earlier
versioned app path was stale; multiple installed versions share one bundle ID.
Binding the confirmed running app path successfully returned the CK3 launcher
accessibility tree. No launcher/game restart was performed. AGENTS and workflow
now direct GUI to resolve the running main executable rather than guess a
version; CLI's declared-state rule is unchanged. Exact local identity is kept
only in ignored evidence, not as a portable configuration constant.

Within the already authorized setup, GUI used Mod library's Reload installed
mods with optional server-cache clearing unchecked. R016 was discovered and
added to the existing Dynasty Map - GUI Probe playset. Only R016 is enabled;
Native Menu Probe, R005 and R009 are disabled. Accessibility state and the
re-read enabled-mod manifest agree. Prior selection and prelaunch logs remain
preserved locally. Ready for user launch to main menu only; no save, classifier,
color write or runtime validation has occurred. No Git/GitHub publication.

### First startup / encoding correction — 2026-10-21

User reported reaching main menu. Captured startup `debug.log:137–140` confirms
R016 mounted; `:1030–1031` records its GUI file loading; `:3773` records target
version 1.20.1.1. `error.log` contains four probe-attributed missing UTF-8 BOM
messages for scripted effects, scripted GUIs, map modes and helper landed titles.
The messages say the engine will try reading them anyway; this is not a clean
startup pass or evidence of executed classification. `gui_warnings.log` and
`database_conflicts.log` were empty. No COMPUTE action was requested or observed;
no save was loaded in this checkpoint. Raw evidence remains ignored locally.

Prepared the small source correction directly in GUI: prepend BOM to exactly
those four files. Checked that the remaining bytes are identical to preserved
pre-fix sources. Installed files were not changed while CK3 remained open, so
source/install equality from the previous receipt no longer describes current
source. Next: user exits CK3 normally and opens launcher through Steam; on ready
acknowledgement CLI installs the four encoding fixes and byte-verifies the full
payload, then GUI gives one startup recheck to main menu. No new classification,
save/load or production UI/lifecycle scope. Existing R016-only selection and
prior-selection restoration record remain in place.


### Build update / mandatory preflight / reinstall — 2026-10-21

Delegation `R016-UPDATE-PREFLIGHT-20261021-04` completed targeted static review,
portable authoring rules/checker, source correction, scoped reinstall and
self-review. CLI assumed the user-declared game closed / launcher open state;
no process/app/UI checks occurred. Launcher metadata confirms 1.20.1.2 Crozier;
Steam manifest confirms build/TargetBuildID 26046173 and completed staged/download
bytes. Patch contents were not inferred. Generated API documents remain from
1.20.1.1; no generation or game launch occurred.

Current installed-source checks (all **static 1.20.1.2 evidence**, not runtime
compatibility):

| Dependency | Inspected source / result |
|---|---|
| Native Baronies fields | `<game>/gfx/map/map_modes/map_modes.txt:116–121` retains the candidate field shape. All 16 native modes referenced by this menu are defined. |
| R-010 integration seam | `gui/shared/mapmodes.gui:483–548,940–997` has the primitive submenu, insertion block, native mode instances and epidemic/legend callbacks. `gui/shared/buttons.gui:1116–1165` has the base map button and its three override blocks. Replacement order, composition and parity remain untested on this build. |
| Explicit fresh-root callback | `gui/activity_window_widgets/funeral_deceased_selection_button.gui:27` uses `Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )`. It does not establish completion/atomic validity. |
| County / senior traversal / equality | `common/scripted_effects/00_history_effects.txt:13–20`; `common/scripted_guis/00_religion.txt:32–40`; `common/scripted_triggers/00_elective_triggers.txt:111–114` contain the respective forms. `common/scripted_effects/00_title_effects.txt:53–57` uses hierarchy traversal plus a tier filter; exact recursion/continue semantics still need current generated docs. |
| Direct and copied title colors | `common/scripted_effects/00_major_decisions_scripted_effects.txt:251–255` and `common/scripted_effects/01_dlc_fp1_scripted_effects.txt:100–104` contain the RGB and title-copy forms. Prior barony runtime evidence remains old-build evidence. |
| Local diagnostics | `common/scripted_effects/07_dlc_ep3_scripted_effects.txt:2818–2834` uses set/change local variables. Nested lifetime and emitted counter values remain unknown. |
| Helper schema / CoA / sample | `common/landed_titles/_landed_titles.info:34–36,103–108,152–156,225–237` documents used fields/creation guards. `common/coat_of_arms/coat_of_arms/01_landed_titles.txt:7–18,3863–3872` supplies matching keyed format. `common/named_colors/default_colors.txt`, the solid pattern asset and fixed sample county/barony keys are present. Object resolution/inertness remains untested. |

No preserved old vanilla bytes were used for an old/new whole-file equality
claim. Matching source forms are renewed static observations, not proof of
unchanged engine behavior. No historical-classifier search was repeated.

[MOD_AUTHORING_RULES.md](../MOD_AUTHORING_RULES.md) now defines mandatory
preparation, manual source review, encoding, build provenance, install identity
and fresh startup gates. AGENTS/workflow and probe README require the standard
library checker before installation and again against installed payloads.
Missing-BOM and misplaced top-level CoA disposable regressions were rejected;
the corrected fixture and actual eight-file source passed. The checker is
read-only and does not parse CK3 or resolve APIs/objects.

Incremental source payload changes were only one leading BOM on the helper CoA
file and exact `supported_version` 1.20.1.1 → 1.20.1.2. The four earlier BOM
corrections were preserved. No classifier or GUI text changed. Relative to the
previous installed copy, five script files gained BOMs, with body bytes
unchanged, and descriptor/wrapper metadata changed. All eight installed files
passed complete inventory, exact byte and SHA-256 equality; six script or
localization files each have one leading BOM. Wrapper path/metadata were
verified separately. An initial receipt assertion expected a final wrapper
newline; a read-only recheck confirmed the intended version-only edit preserving
its original format. This was a receipt-check correction, not a CK3 failure.

The prior installed probe/wrapper, current logs, enabled-mod manifest and a
consistent read-only launcher database snapshot were preserved locally before
installation. Captured log/manifest bytes remained unchanged afterward. CLI did
not write launcher/playset configuration or inspect its UI; GUI must recheck
R016-only selection and retain the existing prior-selection restoration record.
No saves or vanilla files were touched. Public-content/links/whitespace checks
and unchanged-index checks were performed; no staging/commit/push/GitHub write.

**Verdict: startup candidate ready for GUI review; compatibility pending.**
Only the next user-run startup to main menu is authorized. GUI verifies the
installed payload/selection, then gives launch and stop instructions. Review a
fresh 1.20.1.2 startup interval for mount/build, attributed BOM/parser/GUI/helper
errors and database conflicts before any session loading or classification.
Stop if errors appear; main menu alone is not a pass.

After a clean startup, the smallest proposed further scope is user-only
`script_docs` and `dump_data_types` generation in a separately staged disposable
session, without COMPUTE/DISPLAY or fixture mutations. Verify new-build
provenance and review used holder/Dynasty links, senior/world/hierarchy traversal
(including continue/filter semantics), saved scopes, local counters, color
scopes and ScriptedGui/GuiScope/map/variable-system GUI signatures before
classification. These are pending gates, not commands run by CLI or an already
authorized classification stage. Startup success would still leave coverage,
colors/copy appearance, counters, refresh, performance, helper effects, active
context safety and persistence/removal unresolved. ADR-008/009 are unchanged.

### Build-update GUI review / startup recheck ready — 2026-10-21

Consumed matching `R016-UPDATE-PREFLIGHT-20261021-04`. Reviewed rules/checker,
agent/workflow integration, current-build report/citations, regression receipts
and incremental changes; reran read-only source/installed preflight successfully
for all eight files with expected version 1.20.1.2. Wrapper metadata separately
verified. Nonowned RESEARCH matches its dispatch snapshot. No parser/runtime or
independent-review claim follows.

Resolved the running launcher app path with a launcher-only read-only lookup;
launcher identifies CK3 1.20.1.2. Existing Dynasty Map - GUI Probe selection
shows Native Menu/R005/R009 disabled and R016 enabled; manifest agrees. No
selection change or app launch was needed. Prior restoration record preserved.
Ready for the already authorized user startup recheck to main menu only. Capture
fresh logs before loading, API generation or computation; new-build compatibility
and generated APIs remain pending. No staging/commit/push/GitHub writes.

### New-build startup passed / API refresh next — 2026-10-21

User reported arrival at main menu in the new process. Fresh captured logs
confirm only R016 enabled/mounted (`debug.log:137–140`), its GUI load
(`:1030–1031`) and version 1.20.1.2 (`:3773`), with checksum completion at :3776.
`error.log`, `gui_warnings.log` and `database_conflicts.log` are all 0 bytes.
The missing-BOM errors from the previous run are absent. This is a startup-only
pass with user-reported menu arrival; no map/classifier, helper visibility,
refresh or save/removal validation follows. No COMPUTE markers were found.

Preserved existing generated script/type documents with hashes/timestamps in
ignored local evidence before requesting user regeneration. Proposed next
bounded step: execute `script_docs` and `dump_data_types` via the user-controlled
console in the current main-menu session, without loading or computation.
If the console/commands are unavailable there, report that fact before staging
any disposable session. Successful output must be verified as freshly generated
on 1.20.1.2 with R016 enabled; it is not clean vanilla evidence. Keep the old
1.20.1.1 baseline intact and review only the APIs used by R016. No generation
has been performed by Codex or yet confirmed by the user.

### User console / generation receipt — 2026-10-21

User reported restarting and opening the console with Shift + Alt + C. Workflow
now records the shortcut verified for that setup. The new startup identifies
1.20.1.2 with only R016 mounted; error, GUI-warning and database-conflict logs
remain empty. All 12 script/type outputs preserved before regeneration are
now nonempty with newer mtimes, and console history contains both requested
commands. Current/old files and hash/timestamp manifests are preserved in ignored
local evidence. This is R016-enabled generation, not clean vanilla evidence.
No classifier or color writes were requested/observed. No further restart or
regeneration is needed for the scoped used-API review. That review is delegated
as `R016-API-REVIEW-12012-20261021-05` before any sample computation stage.


### Used-API review / small-sample readiness — 2026-10-21

Delegation `R016-API-REVIEW-12012-20261021-05` completed a bounded CLI review and
self-review. **No static blocker found for a later paused valid-context SMALL
SAMPLE direct/copy diagnostic.** GUI must review the actual result and stage
that runtime scope; this review performs and authorizes no loading, CHECK,
computation, DISPLAY, world pass or save. No payload changes or reinstall.

Both preserved snapshot manifests verify sizes/hashes. All 12 current outputs
are nonempty with matching snapshot/manifest mtimes, newer than the old baseline
and after the captured 1.20.1.2 startup/checksum. Current `debug.log:136–140`
identifies only R016 enabled/mounted, `:1030–1031` loads its GUI, and `:3773,3776`
records version/checksum completion. The enabled-mod manifest agrees; captured
error/GUI-warning/database-conflict logs are empty, with no COMPUTE markers.
Build 26046173 remains grounded by the preceding update/preflight receipt, not
an embedded API-dump build ID. The parent's console-command receipt is reused;
console history was not included in the supplied snapshots for independent
recheck. This is **R016-enabled generation, not clean vanilla**. No restart or
regeneration is needed. Empty startup/generation logs do not validate a classifier.

Compared 41 relevant generated contract entries against the preserved 1.20.1.1
entries: exact entry bytes agree. This renews the documented surface for the
current provenance; it does not establish unchanged engine behavior. Current
citations below use `<generated>/` for the preserved 1.20.1.2 snapshot:

| Contract | Fresh generated evidence / result |
|---|---|
| Holder / Dynasty / House | `event_targets.log:920–922,550–552,610–612,1145–1147`; title → holder → Dynasty, distinct House identity; cadet membership uses Dynasty. |
| Seniors and world counties | `triggers.log:1816–1819` excludes self and visits seniors; `effects.log:773–776` is global counties even from player context. |
| County/barony projection | `event_targets.log:1536–1538,1548–1550`; `effects.log:11422–11427` includes self, with recursion controlled independently of limit; `triggers.log:8959–8961` documents tier comparison. County-rooted traversal plus barony filter excludes county self without pruning descendants. |
| Capture and clear | `effects.log:2675–2677,243–245`: unbroken-chain scopes, cleared from top scope; not persistent Dynasty storage. |
| Direct and copy colors | `effects.log:12761–12767,12646–12649`: landed-title RGB and title-copy contracts; copy explicitly shifts slightly, with no exact drift guarantee. |
| Local diagnostics | `effects.log:139–144,2769–2776,554–555,564–565`: local set/change and scope logging exist; generated examples use generic variable names. Nested-helper counter lifetime/emission remains unproven. |
| GUI root / dispatch | `data_types_gui.txt:1–4,15–18`; `data_types_script.txt:2422–2425,3944–3946,3968–3970,4147–4149,4279–4281`: typed lookup, scope construction, Execute → void and IsValid → bool. No success/atomicity contract. |
| Player / selection / UI hint | `data_types_uncategorized.txt:571–573,35083–35085,40963–40965,3187–3189`; `data_types_common.txt:7–10,1326–1328,1949–1951,1961–1963,1973–1975,1985–1987`: Character promotion/validity, void selection, string choice and UI variable methods. Duplicate GetPlayer `:2197–2199` is unregistered; use the typed promotion evidence. |

Reused current-build vanilla receipts corroborate Dynasty equality
(`common/scripted_triggers/00_elective_triggers.txt:111–114`), hierarchy/tier
composition (`common/scripted_effects/00_title_effects.txt:53–57`), fresh-root
Execute (`gui/activity_window_widgets/funeral_deceased_selection_button.gui:27`)
and actual local-variable forms
(`common/scripted_effects/07_dlc_ep3_scripted_effects.txt:2818–2834`). No broad
source scan or historical-classifier rediscovery was performed.

Actual payload trace confirms fresh player roots on each manual computation,
internal Dynasty guard before capture/color writes, DIRECT precedence, and
senior traversal even when a county holder lacks Dynasty. Independent foreign
and holderless counties fall through to OTHER. World uses global county
iteration; both sample paths explicitly name only Middlesex/Kent/Surrey and
use the same county classifier/de-jure barony projection. Copy checks all three
source helpers exist and are unheld before painting. Saved player/Dynasty
scopes are cleared in the same call chain, including copy-helper rejection;
no delayed event or persistent Dynasty cache is introduced.

CHECK's READY string remains a potentially stale UI hint. Character-rooted
Execute validation precedes the effect guard; production null/transition
safety is not established. Separate DISPLAY selects the mode without proving
successful computation. The paused unchanged-context diagnostic restriction
remains essential; no new one-click or atomicity requirement is imposed on
this accepted diagnostic. If custom mode remains selected during copy, writes
may already be visible before another DISPLAY click.

Counter setup/increments refer back to the captured player root, but sample
increments cross scripted-effect helper boundaries. Fresh docs do not settle
that lifetime or whether full scope output includes local values. Treat absent
counter output as a limitation; attributed counter errors stop the probe.
END also follows rejects/target-missing branches: require matching BEGIN/END
plus no REJECT/TARGET_MISSING/errors. If recoverable, category totals must sum
to visited counties (three only when every sample target is reached); barony
coverage needs independent fixture observation. No concrete payload defect
requiring a correction was demonstrated in this static review.

**Proposed next user checkpoint, after GUI review/staging:** load/create a
disposable paused session with a valid player/Dynasty and keep context fixed.
Known sample keys are `c_middlesex`, `c_kent`, `c_surrey`; Middlesex includes
`b_london`, `b_southwark`, `b_woxbrigge` in the accepted current-build title
receipt. Current holders/classes and natural semantic fixtures remain unknown.
CHECK → READY → COMPUTE SAMPLE (direct RGB) once → stop before DISPLAY for Codex
log review. After clean corresponding markers/error review, DISPLAY and observe
county/barony coverage at a fixed zoom. Then COMPUTE SAMPLE (title copy) once →
stop for the same log review → DISPLAY/re-enter as needed and compare the same
area/zoom. Stop on context change, crash, reject/missing marker, attributed
error, wrong category/coverage or unexpected helper/visual effects. No WORLD,
unpause, gameplay fixture mutation or save in this proposed checkpoint.

Rendering/copy appearance, counters, semantic cases, refresh, helper effects,
performance, active-context lifecycle, persistence/removal and known shared
native Baronies state remain unresolved. Missing natural fixtures are limits,
not automatic blockers to the sample. No production path, persistence
acceptance or ADR-008/009 change follows. No app/process/UI check, runtime,
parser/Tiger, independent review, installation, Git staging/commit/push or
GitHub operation occurred. Input evidence and unrelated changes were preserved;
only owned reports and narrowly scoped R016 documentation were edited.

### Used-API GUI review / first sample instructions — 2026-10-21

Consumed matching `R016-API-REVIEW-12012-20261021-05`. Reviewed the source trace,
provenance/comparison receipts and incremental documentation; directly checked
fresh senior/hierarchy/color/Execute contract entries. Accepted no-static-blocker
verdict for the bounded valid-context sample, not runtime classification or
production safety. No further restart, generation or unchanged-payload checks.

Proposed first user action batch: load a disposable test session (or create a
new test game), pause with a valid dynastic player and keep context unchanged;
open Additional Modes, CHECK requiring READY, then COMPUTE SAMPLE (direct RGB)
once. Stop before DISPLAY and report readiness plus any menu/READY problem.
The three named county roots are Middlesex/Kent/Surrey. Do not COMPUTE WORLD,
unpause, switch character, save or request the copy path yet. Codex reviews
matching BEGIN/END with no REJECT/TARGET_MISSING/errors before requesting display.
User performance of this explicitly described batch supplies its runtime scope;
no sample action or result has yet been reported at this checkpoint.

### First direct sample execution — 2026-10-21

User reported clicking the instructed action with no visible change. Preserved
logs show exactly one SAMPLE_DIRECT BEGIN/END pair at 14:59:47, with valid
character root; no REJECT/TARGET_MISSING or errors at/after that execution.
Captured `debug.log:4122–4129` records entry, root scope and exit. Local counter
values are not emitted in that scope dump; totals/coverage are not verified.
User's no-change observation precedes requested DISPLAY selection, so it does
not establish failed coloring/rendering. Next bounded action is DISPLAY only,
observe the three sample counties and report colors/coverage; no new writes.

The overall session is not error-free: at 14:58:39 there are three duplicate
landed-title-name diagnostics with empty names, attribution unresolved, followed
by court-scene invalid-character diagnostics at 14:58:44 (before computation).
No probe filename appears in the captured error log. Do not label all of these
vanilla noise or infer causation from their timing alone. GUI/conflict logs are
empty. Preserve these issues for focused follow-up before expanding copy/world
write tests; no helper/title/source changes while the current game is running.
Raw evidence is local/ignored. No save or game UI inspection/control by Codex.

### First sample display — 2026-10-21

After the requested DISPLAY, user reported green and supplied a map screenshot
showing green-tinted area fill among differently colored surrounding baronies.
Together with the accepted direct sample execution, this supports visible
sample output through the selected view on 1.20.1.2. The image has no county
labels or holder/Dynasty information: do not infer complete Middlesex/Kent/Surrey
coverage, correct DIRECT semantics or simultaneous three-class success from it.
No copy/world computation is included. All five captured runtime logs are
byte-identical to the post-compute capture; DISPLAY added no recorded error.
Earlier load diagnostics remain unresolved, not erased by this positive result.
Screenshot and logs are preserved in ignored local evidence. Next user observation
is read-only county/color/secondary-barony inspection while paused, without
recomputation or saving. No game UI inspection/control by Codex occurred.

### Empty title-name follow-up — 2026-10-21

User clarified all sample areas visible in their image are green; no repeated
observation is requested. Focused source inspection found three helper title
keys have no corresponding localized title names/adjectives, unlike the installed
vanilla county-name/key convention. This is a confirmed omission and a plausible
cause of the three empty duplicate-name diagnostics; counts/timing do not prove
causation. No engine-source assertion or runtime fix claim is made.

Prepared a small source-only correction directly: six localization entries for
the three helper names/adjectives, unique names across helpers. Preserved old
bytes locally and retained UTF-8 BOM; source preflight passes. Added explicit
helper-title localization review to MOD_AUTHORING_RULES. No script/GUI/classifier
change or installed-file mutation while game is running. Existing installed
localization now differs from source intentionally until the scoped correction
is installed after user exit. Proposed next stage is one-file install plus
load-time diagnostic recheck; no world computation or saving. No additional
visual observation or repeated direct computation is needed in this current run.

### Helper-name correction installed — 2026-10-21

User confirmed the described closed-game/open-launcher state, authorizing the
one-file correction and targeted recheck. Per the small-edit exception, GUI
performed the single reviewed localization replacement directly; a CLI handoff
would cost more than this isolated operation. Preserved the old installed file,
logs and manifest first, then source preflight, scoped one-file install and
full source/installed preflight all passed: eight-file inventory/bytes/hashes
match. No classifier/GUI/descriptor or other installed file changed. Read-only
active-playset record and unchanged enabled-mod manifest retain only R016.
Prior restoration evidence remains. No process/game-UI check or launcher config
write was used; user declaration was accepted.

Next user startup stops at main menu for log review, followed by a separately
instructed disposable-session load to test the earlier load-time diagnostics.
Main menu alone cannot prove their disappearance. No new computation, world
scan, save or runtime fix claim; no Git/GitHub writes. Ignored local receipt
retains exact before/after file and configuration evidence.

### Post-name-fix startup — 2026-10-21

User reports menu arrival. Fresh logs confirm 1.20.1.2 at debug.log:3773,
R016 enabled/mounted and menu file loaded (:137,1030); error, GUI-warning and
database-conflict logs are empty. No compute markers. Startup passed for this
interval; it does not settle the earlier load-time empty-name error attribution.
Next user step is load/recreate the same disposable Harold test session and stay
paused, without CHECK/COMPUTE/DISPLAY/save, then report for load-log comparison.
No game UI was inspected/controlled. Raw startup logs preserved locally.

### Helper-name load recheck — localization hypothesis unresolved — 2026-10-21

User reported loading/recreating the instructed paused session. Fresh capture
still contains exactly three empty-name `Duplicate landed title name:` entries
at 15:11:23, then court-scene errors at 15:11:28. GUI/conflict logs remain empty;
there are no R016 execution markers. Thus adding helper localized names did
not remove the diagnostic: missing localization was a completeness defect,
not a demonstrated cause/remedy. Do not conflate display-name localization
with the engine's internal identity diagnostic or claim attribution from counts.
No further field edit, installation or user restart is proposed without review.

Prepared `R016-TITLE-DIAGNOSTIC-20261021-06` for read-only CLI source/log analysis:
reuse targeted current schema, analogous shipped/historical helper shapes and
prior R009 evidence, then return concrete mismatch or competing hypotheses plus
one minimal discriminating experiment. Current user session stays paused;
new compute/copy/world/save actions are on hold. Earlier direct green-render
result and all evidence are retained. No Git/GitHub publication.

### User steering — consolidate test iterations — 2026-10-21

User requested status and preparation of several tests together. Current result
is corrected startup/current API review plus bounded direct-sample execution
and visible green fill; CONTROLLED/OTHER, whole-world coverage, copy path,
refresh/performance and persistence/removal remain unverified. The localization
hypothesis failed to remove three load diagnostics; their attribution remains
open and does not erase the positive sample or automatically prove harm.

Amended the still-READY title-diagnostic handoff to deliver diagnosis and a
consolidated executable test plan together. Prefer existing controls/payload:
A sample color/direct-copy and native-view observations; B one world pass with
semantics/coverage/manual refresh/hitch; C separately staged disposable save,
fresh-process and disabled-mod observations. Actual runtime scope is staged
by GUI after reviewing the result. Preserve needed execution/log stop points,
but group ordinary actions and do not ask the user to confirm every click.
No speculative source fix/restart loop. Workflow now records this batching rule.

### Title diagnostic and consolidated test preparation — 2026-10-21

`R016-TITLE-DIAGNOSTIC-20261021-06` completed the scoped CLI read-only
investigation and prepared a concrete A/B/C plan for GUI review. No structural
defect or evidence-based field correction was demonstrated. The helper landed
title, CoA, localization and descriptor files match their installed counterparts;
the three title keys and matching CoA keys are individually unique, with no
definition collision in the checked current vanilla landed-title/static-CoA
directories. Six localized helper entries are installed correctly. Both prior
and corrected load error bodies agree after timestamp normalization: missing
localization was a completeness defect, not the established cause/remedy.

Current `common/landed_titles/_landed_titles.info:7–20,53–63,143–156,225–237,256–287`
documents tier-prefixed database definitions, landless default no, preferred
capital county and creation predicates. Dynamic-template `key` is explicitly
excluded from database definitions; no required static `name` field is supplied.
Shipped landless examples have capitals, while titular examples vary
(`00_landed_titles.txt:56–78,130–155,78927–78947`). These are not evidence that
R016's non-landless unheld helper needs an invented capital or another field
fix. Title-keyed pre-scripted CoA shape agrees with shipped examples
(`common/coat_of_arms/coat_of_arms/01_landed_titles.txt:7–19,3863–3875`). Static
shape does not prove runtime identity, RGB resolution, visibility or inertness.

Retained R009 startup/final first-run logs have no matching empty-name diagnostic;
they contain the known BOM, explicit landless-cyan capital and four CoA errors.
R009 used a different build/payload/session and is not a clean current helper-off
control. Both R016 error bursts follow the logged `Load Save` transition and
precede `InitPostRead`, without computation. This engine label alone does not
identify whether the user's input was an existing save or new-game setup;
R009's bookmark sequence also reaches that transition. No save was read here.
Possible helper/session registration, input-history/full-payload interaction
and independent baseline causes remain competing hypotheses. Three errors
matching three helpers do not identify the offending objects or establish harm.
Court-scene errors remain unattributed; no whole-session-clean claim.

Existing candidate can support bounded direct/native observations and a guarded
copy comparison, without reinstall/restart. Direct paths do not read helpers;
copy checks three objects exist and are unheld before writing, but those guards
do not prove distinct identity or correct source color. New execution errors,
rejects, missing targets, wrong classes/coverage or held/unexpected helper effects
stop dependent work. Copy-only rejection need not block separately reviewed
direct-world scope if there is no shared-state instability. Unresolved baseline
errors prevent clean helper/persistence/removal acceptance, not every independent
direct-render observation. No runtime scope is granted by this review.

The prepared plan groups: A, one current-session paired direct baseline only
because the new run has no compute, then copy and ordinary native-view/coverage
observations; B, one direct world pass with natural semantic fixtures, approximate
hitch and manual re-entry; C, separately staged disposable save, enabled fresh
process and disabled-mod observations. First execution of each write path keeps
its real marker/error gate, while ordinary observations are grouped. Prior
direct execution/green fill remain accepted. No ownership/Dynasty change is
manufactured to claim refresh, and missing fixtures/counters stay limits.

Current shipped sample structure is 3 counties and 13 baronies: Middlesex has
London, Southwark, Woxbrigge, Gore and Brentford (:2330–2384); Kent has Dover,
Canterbury, Rochester and Tonbridge (:3352–3375); Surrey has Chertsey, Guildford,
Kingston and Tandbridge (:3376–3399). This supplies an independent structural
coverage expectation, conditional on unchanged live membership, not a runtime
counter/coverage pass. All three sample classes may still be the same.

Smallest proposed attribution control needs no file change: explicitly create
the same fresh disposable bookmark session with the current payload, without
computation/save, and compare session-entry errors against the retained input
load. It can join a later staged session-replacement interval, not force another
restart now. If causal helper isolation is required, one designed helper-on/off
pair keeps identical original descriptor/CoA/localization and differs only in
the three helper definitions; no classifier/GUI in either variant. Neither
experiment was prepared as a payload, installed or run. A changed-payload stage
would require full authoring/manual/preflight/startup gates with exact 1.20.1.2.

Deliverables and private receipts remain in ignored handoff/evidence storage.
Only the owned reports, R016 checkpoint/status and backlog row changed. No full
unchanged preflight rerun, parser/Tiger/independent review, app/process/UI access,
game launch/exit, computation, save access, payload/install/config mutation,
Git staging/commit/push or GitHub operation occurred. GUI review/staging is next;
user's current session remains paused with no new action requested by CLI.

### Consolidated plan GUI review / Batch A staged — 2026-10-21

Consumed `R016-TITLE-DIAGNOSTIC-20261021-06`. Reviewed diagnostic hypotheses,
actual evidence limitations, current-source/reference trace, R009 comparison
and complete A/B/C plan. Accepted existing-payload diagnostic readiness; no new
structural fix, restart or reinstall is justified. The three load diagnostics
remain unattributed and cannot be declared harmless, but do not by themselves
invalidate independent direct observations. No speculative helper edit follows.

Next user batch A first block: unchanged paused dynastic context, grouped native
reference views at the sample area/zoom, return Realms, CHECK requiring READY,
then SAMPLE_DIRECT once and stop before DISPLAY for log delta. The current run
had no compute, so one direct pass supplies the paired baseline for later copy;
prior green result is retained. Snapshot baseline preserved locally. Later
visual/native/helper observations are grouped; copy has one first-execution
gate, world/save scopes remain separately staged. No acknowledgement per click,
new payload or runtime action by Codex. No Git/GitHub writes.

### Fresh-new-game control / menu baseline — 2026-10-21

User chose a fresh session to distinguish current new-game setup from earlier
input history after the update. Before starting it, user reported menu arrival
and asked for log review. Capture confirms 1.20.1.2 (:3773), only R016 mounted
and GUI loaded (:137,1030); error/GUI/conflict logs all empty, no execution
markers. Proposed next action is explicitly NEW Harold 1066 game, pause, report
for session-entry log comparison; no save loading, CHECK, COMPUTE, DISPLAY or
saving yet. This zero-file-change control was already designed in the accepted
diagnostic; it does not assume update corruption or resolve helper attribution.
Raw evidence preserved locally; no game UI or app control by Codex.

### Fresh-new-game control result — 2026-10-21

User reported creating the instructed fresh Harold test game. Preserved session
logs contain ZERO duplicate-title-name diagnostics, versus three in the earlier
session-entry capture using the same current payload. This supports input or
session-history dependence; it does not identify a particular save defect,
prove the update caused corruption, or establish helper persistence/removal
safety. Fresh game setup still logged history/employer, game-start/succession
and court-scene errors from installed-content locations; no R016 filename or
execution marker appears. Do not call the whole session clean or assign all
errors to vanilla without a matched control. GUI/conflict logs are empty.

The user-declared session remains paused. Resume consolidated Batch A without
restart/source changes: native reference views, Realms, CHECK requiring READY,
one paired direct sample baseline then bounded log review before DISPLAY.
No copy/world/save requested yet. Fresh captured files provide the execution
error baseline for this specific session. No game UI inspection/control.

### Batch A1 direct baseline accepted — 2026-10-21

Current fresh-session SAMPLE_DIRECT ran once at 15:42:20 with the expected
valid Harold root, BEGIN/END and no REJECT/TARGET_MISSING. Captured error,
GUI-warning and database-conflict deltas relative to session entry are zero;
no duplicate-title error appeared. Earlier game-setup errors remain unchanged
as baseline. No numeric counters are emitted, so coverage is not established.
Proceed with one grouped user observation block: DISPLAY, inspect the three
county areas and secondary baronies plus holder Dynasties, native-view
round-trip and return DISPLAY; report once. No copy/world/save or additional
compute, restart, installation or repeated baseline request. Raw logs preserved
locally; no game UI inspection/control by Codex.

### Batch A direct observations accepted — 2026-10-21

User reports all three sample counties and their baronies green; county holders
are the player or members of the same Dynasty. This supports correct DIRECT
for the reported fixtures, not CONTROLLED/OTHER or separately enumerated
13-title coverage. User reports ordinary map switches work normally and green
returns only after selecting My Dynasty. This is bounded native-view/re-entry
evidence, not full isolation, automatic refresh or persistence safety.

Captured observation delta adds no error/GUI/conflict entries and no extra
compute markers. Next first-copy gate: unchanged paused context, return Realms,
CHECK READY, one COMPUTE SAMPLE (title copy), then stop before DISPLAY for log
review. No extra direct pass, world scan, restart, install or save. Prior helper
identity uncertainty remains, though fresh-game duplicate diagnostics are absent.

### Batch A2 copy execution accepted / grouped A-to-B transition — 2026-10-21

User reported copy click with no visible change while the instructions kept
Realms selected. Captured one SAMPLE_COPY BEGIN/END at 15:47:16 with valid
Harold root, no REJECT/TARGET_MISSING and zero new error/GUI/conflict entries.
The existence/unheld guard did not reject; this is not proof of distinct helper
identity, exact RGB, full coverage or emitted counters. No color comparison has
yet been reported for the copied output in My Dynasty.

To reduce round trips, next user block groups DISPLAY copy/barony/native-view
comparison and, only if no wrong class/coverage/side effect is observed, the
already prepared one direct-world request: Realms, CHECK READY, COMPUTE WORLD
once, note approximate hitch, stop before DISPLAY for first-world log gate.
A visible issue stops that conditional progression and must be reported. No
save, unpause, player switch or restart; no runtime action performed by Codex.

### Batch B1 first world execution — 2026-10-21

User reported completion of the grouped copy-observation/world-request block
without specific visual or hitch details. Logs establish one WORLD_DIRECT
BEGIN/END at 15:49:43 with valid Harold root, no REJECT/missing markers and no
new error/GUI/conflict entries. Both markers share a timestamp second; this
is not a measured subsecond duration or proof of no visible hitch. Numeric
world counters were not emitted; exhaustive county/barony coverage is unknown.
No second world pass is requested. Copy visual/native observations and perceived
activation delay remain awaiting the user report.

Next grouped user block: DISPLAY full map, independently inspect natural
holder/Dynasty/senior fixtures for DIRECT/CONTROLLED/OTHER, constituent baronies
and areas outside original sample; native-mode round-trip and return. Report
actual observed cases and missing fixtures, plus outstanding copy/hitch details.
No unpause, additional compute, fixture mutation or save. No game UI control
by Codex; raw world execution capture retained locally.

### World visual report / proposed semantics clarification — 2026-10-21

User supplied a native House-view screenshot and a My Dynasty world screenshot,
reporting positive differentiated territorial coloring. Captured observation
logs have no new error/GUI/conflict entries and no additional compute markers.
The images/report support visible world-output differentiation; they do not
prove exhaustive coverage, every category or a deep-chain fixture. The current
probe palette is green DIRECT and orange CONTROLLED, blended with terrain;
perceived light/dark green does not alter which predicate ran. Explicit copy
appearance difference and perceived world hitch are still unreported.

User suggested a different product meaning: a dynastic superior should color
its whole realm dark green, while a dynastic subordinate under foreign control
should be light green, remainder grey. This differs from accepted county-holder
DIRECT precedence/any-senior CONTROLLED. Clarification requested: dark = top
de-facto ruler (including independent holder) has player Dynasty; light =
otherwise holder OR any senior has player Dynasty; grey = no match. A foreign
count under dynastic duke under foreign king would then be light. No acceptance
is inferred from tentative wording. Keep ADRs/code unchanged pending answer;
no new computation/save stage or loss of the existing bounded renderer result.

### Three-view product decision / preparation handoff — 2026-10-21

After comparing three alternatives, user explicitly approved all three English
names: Dynasty Realms as default, Dynasty Holdings second and My Realm & Dynasty
third in the Dynasty submenu. Realms distinguishes dynastic highest de-facto
rulers from dynastic territory under foreign highest rulers; Holdings retains
the historical holder-first rule; My Realm distinguishes the player's own
de-facto subtree from other dynastically controlled territory. Dark/light green
and grey express each view's categories; not three simultaneous datasets.
All Dynasties remains deferred. This supersedes the pending semantic question
above, without retroactively changing observed old-classifier results.

Prepared source-only CLI handoff R016-THREE-VIEWS-PREP-20261021-07 (Sol/High) for
all three classifiers, menu/default/legends, targeted new API review, source
preflight, coherent ADR/docs and a batched test plan. No installation or game
action in this stage; game may stay running. CLI will reconcile canonical
definitions; current installed candidate remains unchanged. No production,
lifecycle, runtime correctness or Git publication claim.

User further clarified the required layout before CLI execution: one top-level
Dynasty map mode with three associated subviews while active, Realms initially
default, selected subview and legend visible. This iteration must prepare that
target layout, not three sibling Additional Modes entries. Diagnostic controls
may remain in a separate area but cannot be the normal activation path. READY
handoff updated in place; no implementation/runtime validation claimed.

### Three-view source preparation — 2026-10-21

`R016-THREE-VIEWS-PREP-20261021-07` completed bounded CLI source preparation and
self-review, with no installation/runtime/independent-review claim. ADR-010 records
the accepted semantics, exact names/order/default and dark precedence. The new
source has three county classifiers and common barony RGB projection: dark
25/105/50, light 145/220/150, grey 65/70/80. Each manual world call captures fresh
player/Dynasty scopes, checks Dynasty before iteration, clears captured scopes
on completion, and emits bounded WORLD_REALMS, WORLD_HOLDINGS or WORLD_MY_REALM
BEGIN/END/REJECT_NO_DYNASTY markers. One root-scope dump per pass supports context review; new views do not claim
emitted counters.

Realms tests holder-with-no-liege explicitly, or a no-liege senior in the complete
senior iterator. It does not assume top_liege returns self for independents.
My Realm compares the holder and each senior directly with the captured player,
not the player's top liege; sibling vassals stay outside the dark subtree.
All light checks include the full holder/senior chain with per-character Dynasty
guards. Unheld counties project grey. De-jure traversal is projection only.

Reused the existing 41-contract .2 review. Newly used `liege` is documented as
character → character in `event_targets.log:664–666`; senior iteration excludes
self (`triggers.log:1816–1819`). Shipped
`common/scripted_triggers/00_elective_triggers.txt:167–175` combines senior
`this` equality and explicit liege existence; :111–114 grounds Dynasty equality.
No new top_liege/self or suzerain API assumption was introduced. Current .2
GUI contracts confirm IsMapMode, CanChangeMapMode, fresh-root IsValid/Execute and
void SetMapMode; shipped funeral selection :27–28 chains Execute and another
onclick. That is composition evidence, not success/atomicity or repaint proof.

One Dynasty menu entry computes/selects Realms. The active-map banner offers
exactly three ordered subviews, selected down state, view-specific legend and
Refresh. Additional menu opening does not compute or reset the alternative;
normal subview selection and refresh recompute their own output before selection.
Native mode/setting rows and prior raid/barter omissions are preserved. Intentional
native identifier overrides are `flowcontainer_additional_mapmodes` and the
new narrow `widget_map_mode_banner` primitive composition. Native headers/Faith
controls remain native references; the custom panel is outside the HUD-overridden
`map_mode_banner_sub_modes` block (`hud_bottom.gui:286–338`). No HUD or vanilla
body is packaged; actual replacement precedence/layout/clicks require testing.

Normal activation uses fresh guarded Execute then SetMapMode; Execute returns
void. No documented success-aware/atomic compute-display binding was established.
A context race or effect failure can still select stale shared RGB, so ordinary
UX remains a candidate, not complete production behavior. Separate per-view
COMPUTE then log-gated DISPLAY controls support safe paused diagnostic staging;
these controls do not satisfy the normal UX requirement by themselves. Active
context-loss, no-Dynasty UI, shared native Baronies effects, restoration and
save/removal gates remain open. No recurring watcher/scan or persistent selection
cache was added. Realms re-entry intentionally recomputes; the three modes do
not hold separate datasets.

Original sample direct/copy bodies and helper title/CoA definitions are retained
unchanged. They are clearly labeled historical Holdings baseline, with their
old green/orange/grey palette and a separate diagnostic display/legend, not a
fourth normal subview. New direct views do not depend on helper-copy acceptance.
Previous empty-name diagnosis and fresh-game/world evidence remain unchanged.

Offline preflight passed nine source files at exact expected version 1.20.1.2.
Manual source review covered folder/schema shape, unique keys/references,
localization and BOMs, guards/traversal/precedence, shared RGB and control wiring.
Whitespace, incremental diff/public privacy and unchanged empty-index checks were
performed. These are source checks, not a CK3 parser, Tiger, engine execution or
runtime API compatibility validation. Detailed receipts and consolidated test
plan remain ignored/local; the public batched plan is in TEST_PLAN and probe README.

Next: GUI review, then separately authorized closed-game installation with private
payload/wrapper/log/selection backups, source and installed exact-version preflight,
wrapper checks and fresh user-run menu/startup log gate. One paused session then
compares all new views, initial/default/selection/legends, natural hierarchy
fixtures (including player-vassal/subtree), baronies and native round trips, with
one first-execution gate per new classifier. Missing fixtures remain untested.
No save/fresh-process/disabled-mod batch, API regeneration, tooling installation,
app/process/game UI access, Git staging/commit/push or GitHub operations occurred.

### GUI review of three-view source — 2026-10-21

Matched delegation 07 completed result and actual source. Reviewed county
predicates, wrappers, callbacks, Dynasty entry and native-banner composition
against narrow installed banner/HUD override sources. Re-ran nine-file source
preflight at 1.20.1.2 and whitespace check: passed. Accepted research candidate
for controlled paused-context testing after installation; layout/precedence/
clicks and atomic context safety remain unverified. Known void Execute/display
gap is explicit, not solved by staged diagnostics. No installation by review.
Prepared delegation 08 for backed-up isolated install/byte verification only;
user closes CK3 and opens launcher before invoking CLI. No saves or publication.

### Three-view installation — 2026-10-21

Delegation `R016-THREE-VIEWS-INSTALL-20261021-08` completed after the user's
declared closed-game/open-launcher prerequisite. The source preflight passed
before copying, and the installed preflight passed afterward for exact version
1.20.1.2. Both report nine files; installed inventory, bytes and SHA-256 match
source. The wrapper's name, version, supported version and payload path match
the source descriptor and expected target. The original eight-file payload and
wrapper were backed up before the nine-file copy. No unexpected installed files
were present. Source hashes remained captured for comparison.

The five optional startup logs (`debug.log`, `error.log`, `game.log`,
`gui_warnings.log`, `database_conflicts.log`) were absent at install time;
`dlc_load.json` was present and backed up. Its read-only enabled-mod manifest
currently names the R-016 wrapper; this does not establish actual launcher
playset selection or a mounted payload. The install receipt and private backups
are local/ignored. No launcher configuration, logs, saves, source, vanilla,
Git staging/commit/push or GitHub content was changed. No startup/runtime or
CK3 compatibility claim follows from these file checks.

Next: GUI inspects the already-open launcher, reuses the existing test playset,
and verifies/configures its intended mod selection while retaining the prior
selection restoration receipt. The user then starts CK3 through Steam and stops
at the main menu for fresh build, mount, error, GUI-warning and conflict review.
Do not load or classify before that gate passes. Known execute/display ordering
and shared barony-RGB lifecycle limits remain open.

### Installed three-view candidate / launcher review — 2026-10-21

Installation 08 consumed. GUI re-ran installed preflight: nine-file exact
inventory/bytes/SHA-256 match. Wrapper and enabled manifest verified. Already
open CK3 launcher shows existing Dynasty Map - GUI Probe with R016 enabled and
Native/R005/R009 disabled; no selection changes needed. Prior backup/restore
records preserved. Next user PLAY to main menu, then fresh log/build/mount gate
before session/classification. No game UI inspection/control, startup/runtime
pass, save or publication.

### Three-view fresh startup gate — 2026-10-21

User reported main menu. Captured fresh startup logs: actual 1.20.1.2, R016
mounted, both original menu and new views GUI asset files loaded. error.log,
gui_warnings.log and database_conflicts.log each zero bytes. No classifier
execution markers. Startup gate passed for this candidate; this does not prove
in-session banner/layout, classification or context safety. User next creates
fresh disposable Harold1066, pauses and checks menu entry without activation;
session-entry baseline precedes first write. Raw logs remain ignored locally.

### Three-view session-entry baseline — 2026-10-21

User reports loaded session, Dynasty entry visible, not activated. Entry logs
have no DYNMAP_R016 compute markers, zero GUI/conflict bytes and no duplicate
landed-title-name diagnostic. error.log is 28155 bytes of history/employer,
succession/game-start and court-scene diagnostics before any compute, retained
as session baseline; no new classifier attribution inferred. Next first-write
gate is staged COMPUTE Dynasty Realms while native Realms remains active, then
log review before DISPLAY/alternative computation. No normal-path UX pass yet.

### Three-view first Realms compute gate — 2026-10-21

User reported staged compute. Logs contain one WORLD_REALMS BEGIN/END at
19:34:53, valid Harold/current Dynasty captures, no REJECT, and zero appended
error/GUI-warning/conflict bytes versus session baseline. First Realms execution
gate passed; no visible coverage/classification/layout or duration claim.
Next grouped observation: DISPLAY Dynasty Realms, inspect England/default
selection/three controls/legend; if correct return native Realms and staged
COMPUTE Dynasty Holdings once, then stop before its DISPLAY for first-write gate.
Stop/report a visual/layout issue instead of progressing through it. No save.

### First three-view visual report — 2026-10-21

User supplied cropped map image and reported roughly one-second click delay;
exact clicked control awaiting clarification. England is visibly differentiated
with a pale tint; screenshot excludes panel/legend and does not establish exact
RGB, dark-category correctness or target layout. New log delta contains no
classifier markers and zero appended error/GUI/conflict bytes. Thus no staged
Holdings execution is evidenced yet. Preserve screenshot/logs privately. Hold
new computations; request full game-window user screenshot including bottom
map/subview panel and clarify action before diagnosing a layout/palette defect.
No agent game UI access and no runtime layout pass.

### Realms panel and two-zoom user evidence — 2026-10-21

User clarified the preceding action was DISPLAY Dynasty Realms; the reported
roughly one-second delay refers to display, not measured world computation.
Two further user screenshots at different zooms, with no intervening view
clicks, show all three ordered subview controls, Realms highlighted, localized
Realms legend, Refresh and return-to-Realms controls. This supports visible
panel integration at those zooms only, not alternative click behavior or other
UI scales. England tint is pale/terrain-dominated and its expected dark fill is
not visually established. Preserve as comparison baseline; do not infer wrong
predicate or shader cause solely from screenshots. Next staged Holdings compute
from native Realms, log gate before display. No new source/install or save.

### Three-view first Holdings compute gate — 2026-10-21

One WORLD_HOLDINGS BEGIN/END at 19:39:20 with current Harold/Dynasty captures,
no rejection or additional new-view pass, zero new error/GUI/conflict bytes.
First Holdings execution gate passed; no coverage/correct-color claim. Next
group DISPLAY Holdings and same-zoom comparison to Realms; if no visible issue,
return native Realms and COMPUTE My Realm & Dynasty once, stop before DISPLAY
for final changed-classifier first-write review. User screenshots for comparison
are useful; no agent game UI access.

### Holdings visual feedback / next-revision priorities — 2026-10-21

User supplied Holdings screenshots showing selected Holdings and corresponding
legend, with differentiated green areas, then a wider continental view. User
positively assesses direction but reports unrelated continental land is not
visibly grey; neutral-background/contrast acceptance is NOT met. Cause remains
unresolved (classification/projection/rendering), not asserted terrain blending
only. User requests grey/contrast in next revision and suggests deriving the
accent from Dynasty identity. Reuse R009 findings: template color read-but-unused
and no demonstrated active native House/Dynasty palette access; do not assume
every dynasty provides a usable map RGB. Proposed accent research is distinct
from All Dynasties and does not authorize palette registry or bypass grey fix.
No new classifier execution inferred from screenshot/report; My Realm staged
compute remains unconfirmed. Hold further runtime progression while next source
revision scope is coordinated. No source/install/Git/GitHub writes by this note.

### User-directed research closeout boundary — 2026-10-21

User requests completion of remaining tests for this revision, then R016 research
closeout and planning F001 for target menu/submenu and visual definitions. No
further prototype/grey/palette implementation in R016. Read-only log audit
still shows only Realms and Holdings execution pairs, unchanged 28155 error
bytes and empty GUI/conflicts; My Realm execution not yet observed. Remaining
bounded runtime stage: staged My Realm first-write gate, then associated normal
selection/Refresh/native round-trip smoke with known grey defect retained as
failure/next-task requirement. No fixture expansion/persistence/save tests.
Prepared documentation-only successor planning handoff 09; final research
disposition must distinguish passed, failed and untested, and must not claim
GitHub closure/publication or production completion.

### Three-view first My Realm compute gate — 2026-10-21

User reported staged computation. One WORLD_MY_REALM BEGIN/END at 19:50:12
with valid Harold/current Dynasty captures, no rejection or extra new-view
compute markers and zero appended error/GUI/conflict bytes. Third changed
classifier execution gate passed, not proof of full semantic coverage.
Final grouped user smoke now authorized: display My Realm, ordinary subview
Holdings -> Realms -> My Realm, Refresh once, reopen/close Additional without
selection reset, native Realms/Faith/subview/Culture/De Jure round trip and
ordinary Dynasty entry returning default Realms. Remain paused/same character;
no save/fixtures/restart. Known grey defect remains recorded, not a reason to
expand R016 implementation; stop on new failure and report last action.

### Final three-view smoke and user closeout scope — 2026-10-21

User reports all requested operations appear to work, with poor grey background
limiting visual assessment. Final captured interval has five complete new-view
execution pairs in observed order MY_REALM, REALMS, HOLDINGS, MY_REALM, REALMS
at 19:51:29–19:52:11, no REJECT, zero new error/GUI/conflict bytes and unchanged
game.log. User's precise action order was not separately enumerated, so markers
are bounded evidence of repeated dispatch, not exact per-control attribution or
a proof that menu-only operations never scan. User visual report supports
ordinary switching/refresh/native return smoke; exhaustive classes, perf and
context/lifecycle safety remain unproven. No further user test requested in R016.

User explicitly split successors: R017 selects test character/year with family
and broad Dynasty; F001 specifies target menu/subviews/legend/contrast/grey;
F002 owns Dynasty/CoA/House color strategy. Plan only, no implementation or new
runtime/source discovery. Prepared docs handoff updated to these three tasks.
R016 is locally closed as research complete with partial technical validation
and a known visual defect, not all checks passed or production-ready. GitHub
#16 remains unchanged; no issue closure/publication was performed.

## Final disposition — 2026-10-21

**Closed as completed research with bounded/partial technical validation**, at
explicit user direction. The basic historical pipeline and original prototype
work on the tested target/context sufficiently to move from R&D into separately
scoped feature work. This is not a claim that every original acceptance item
passed or that the technique is safe for production saves.

| Question | Outcome / limit |
|---|---|
| Historical precedent | Pipeline reconstructed; exact historical classifier not recovered in bounded search |
| Current target | 1.20.1.2 / 26046173; original 1.20.1.1 evidence retained; 41 selected used contracts reviewed and new three-view contracts inspected |
| Packaging/startup | Nine-file source/install equivalence; fresh build/mod/GUI loading verified, startup error/GUI/conflict logs empty |
| Three classifiers | Each executed once through its changed-code first-write gate with valid player/Dynasty and zero new error/GUI/conflict bytes |
| Visible UI/interaction | User screenshots show ordered subviews/selected state/legends; user reports ordinary switching/Refresh/native return appear to work |
| Final runtime evidence | Five complete execution pairs in the last smoke interval, no rejects/new error deltas; exact per-control attribution not independently established |
| Neutral world / contrast | Failed visual acceptance: unrelated continental land not clearly grey; cause unresolved, transferred to F-001 |
| Classification/coverage | Positive bounded visuals, not exhaustive world/barony/deep-liege/cadet/lowborn/player-vassal correctness |
| Copy/direct comparison | Historical sample copy/direct execution accepted; exact visual drift comparison remains incomplete; new views use fixed direct RGB |
| Performance | No profiler measurement; user roughly-one-second report concerned DISPLAY, not measured world refresh |
| Context/atomicity | Void Execute is no success receipt; invalid-context UI and active-context safety remain unproven |
| Shared RGB/persistence | Known title RGB serialization/native Baronies sharing; fresh-process/disabled-mod removal and exact restore unresolved; no new save test |
| Helper load diagnostics | Earlier three empty-name errors did not recur in fresh newgame; localization hypothesis failed; source/cause/inertness not established |

All raw screenshots/logs/generated references/saves remain excluded from public
content. No vanilla files were edited or copied into the payload. Older dated
permissions and checkpoints above describe their stages, not current scope.

Successors: [R-017](R-017-test-scenario-selection.md) selects test fixtures;
[F-001](F-001-dynasty-map-ux.md) defines final UI and fixes grey/contrast;
[F-002](F-002-dynasty-color-strategy.md) selects a supported accent strategy.
[F-003](F-003-dynasty-subview-definitions.md) is the completed summary of accepted
definitions and appearance; the third name remains **My Realm & Dynasty**.
Existing R-005/R-009/R-010/R-013 safety owners and ADR-008/009 requirements stay
open. No successor implementation or additional R-016 runtime was started.
User authorized scoped commit/push and updating/closing #16; publication receipts
are retained locally after verification, not predicted in this document.

### Publication verified — 2026-10-21

User-authorized scoped research/source/docs checkpoint pushed to the existing
research branch. GitHub #16 title/body updated to the final 1.20.1.2 findings
and verified CLOSED with reason COMPLETED. Definition record F-003 is complete;
R-017/F-001/F-002 remain planned without new issues or implementation. Grey and
safety/coverage/persistence limits remain explicit. Publication/privacy receipts
are retained locally; no private evidence entered the commit.

<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| codex-auto-review | 269453 | 158336 | 111117 | 1508 | 1020 | 270961 | partial |
| gpt-6-luna | 9087490 | 8811648 | 275842 | 68902 | 29043 | 9156392 | partial |
| gpt-6.1-sol | 57594042 | 56097920 | 1496122 | 230252 | 44649 | 57824294 | partial |
| unknown | 400382 | 398848 | 1534 | 4351 | 0 | 404733 | partial |
| **Total** | 67351367 | 65466752 | 1884615 | 305013 | 74712 | 67656380 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-22T13:15:22Z. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
Coverage is partial: only explicitly evidenced task turns and linked reviews are allocated; ambiguous usage and missing history are not estimated. Includes attributed probe work, tests, retries and linked automatic reviews. Mixed finalization/planning turns and shared documentation work remain unallocated. The unknown-model bucket contains measured counters without a matching model context. This backfill job is assigned to T-002 and excluded from these historical totals. No currency or quota inference.
<!-- ai-cost:end -->