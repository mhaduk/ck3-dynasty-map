# CK3 source map

Navigation index for Dynasty Map research. Assessed 2026-10-21 against the
installed CK3 1.20.1.1 (Crozier) baseline. This index points to sources; it does
not reproduce their contents or authorize runtime probes. Use portable roots:
`<game>/` is the installed `game/` directory and `<user-data>/` is CK3 user data.

## Evidence order

1. **Target-build static evidence:** generated `script_docs` and
   `dump_data_types` from a clean installed build; shipped `<game>/**/*.info`;
   then narrowly selected installed vanilla scripts, GUI and definitions.
   Generated docs establish documented APIs; `.info` describes supported
   structures; vanilla files show shipped usage. None alone proves engine
   rendering, timing, save behavior or lifecycle semantics.
2. **Target-build runtime evidence:** controlled user-run probes and the
   corresponding bounded logs. Runtime observations can resolve static
   ambiguity, but apply only to the tested build, path and conditions. Record
   setup, positive controls, exact observations and limits.
3. **Maintained explanatory and tool references:** CK3 Paradox Wiki, its
   searchable mirror, and tool documentation for that tool's own behavior.
   Reconcile all API claims against target-build sources.
4. **Discovery only:** community indexes/discussions, historical archives,
   derived datasets and other Clausewitz/Jomini games. Treat findings as
   hypotheses until checked against CK3 target-build evidence.

When sources conflict, prefer the narrowest direct evidence for the claim. A
reproducible 1.20.1.1 observation can override a static interpretation for its
tested case; it does not rewrite the API contract generally. A newer patch
requires renewed target-build checks. Static absence in a searched subset is
not proof that no engine path exists.

Evidence labels used in project notes:

- **VERIFIED** — evidence supports the stated claim; always name whether static
  target-build or bounded runtime evidence.
- **LIKELY** — converging but incomplete evidence; do not treat as a contract.
- **HISTORICAL** — useful prior-build material, not checked against the target.
- **COMMUNITY** — discovery/context from non-authoritative community material.
- **UNKNOWN** — not established by the inspected evidence.

## Quick lookup

| Question | Start here | Then inspect | Runtime? / limit |
|---|---|---|---|
| Effect or trigger signature, valid scope | `<user-data>/logs/effects.log`, `triggers.log` | Search the narrow vanilla call site and its scope setup | Only if semantics or execution are unclear |
| Scope transition / event target | `event_targets.log`; `event_scopes.log` | Find vanilla caller and follow each transition | Often for edge-case resolution; listed target is not proof of runtime result |
| Modifiers and on-actions | `modifiers.log`, `on_actions.log` | `common/modifier*`, `common/on_action`, nearby event/effect files | Needed for ordering, firing conditions and lifecycle not stated in docs |
| GUI function / type / return type | `<user-data>/logs/data_types/` (`data_types_gui.txt`, `data_types_script.txt`, `data_types_uncategorized.txt`) | Search vanilla `.gui` caller; check case and scope construction | Usually for execution ordering, invalid context, refresh and visibility behavior |
| GUI layout / native integration | `<game>/gui/` | Relevant `mapmodes.gui`, HUD/window and registration `.info` | Usually; composition and engine-managed behavior are not API signatures |
| Scripted GUI | `data_types_script.txt` and `data_types_gui.txt` | `common/scripted_guis/`, `gui/` invocation; search `ScriptedGui.Execute` | For root, availability, re-click and lifecycle semantics |
| Map mode / barony colors | `<game>/gfx/map/map_modes/map_modes.txt`; `common/landed_titles/` | Native map-mode GUI, color effects, shaders and the exact consumer | Yes for renderer input/isolation/restore. R-009 renderer input and lifecycle remain **UNKNOWN** |
| Area selection / geographical-region inputs | Generated `TitleSelectorWindow`, `GeographicalRegionsWindow`, `GuiPotentialCouncilTask`; `<game>/map_data/geographical_regions/_geographical_regions.info` | `common/decisions/_decisions.info` title controllers, `common/council_tasks/_council_tasks.info`, matching selector/window GUI | R-009 static trace found predicates and database identities, not a dynamic three-set/RGB layer. Region definition RGB is for visual regions; selection binding/cleanup needs separate evidence |
| County / barony / title traversal | `event_targets.log`, `effects.log`, `triggers.log` | `common/landed_titles/`, map/title effects and a focused iterator example | Runtime for unusual de-jure/holder cases; generated signatures do not prove intended coverage |
| Character / House / Dynasty and lieges | `event_targets.log`, `triggers.log` | `common/dynasty_houses/`, `common/dynasties/`, relevant decisions/effects | Runtime for succession, missing Dynasty, special governments or null behavior |
| Lifecycle hooks | `on_actions.log`, `event_scopes.log` | `common/on_action/` plus the vanilla caller/effect chain | Yes when hook timing, ordering or coverage matters |
| Localization | `<game>/localization/english/` and mod localization | Matching GUI/script use; wiki Localization page; Tiger as a check | Normally static; dynamic GUI localization may require data-type lookup |
| File format / override question | Nearby shipped `*.info` | One or two native examples in the same folder; wiki for concepts | Probe only if parser/loading behavior remains uncertain; `.info` may be incomplete |
| Mod loading / conflicts | `descriptor.mod`, launcher-generated mod metadata, `debug.log`, `database_conflicts.log` | Wiki Mod structure / troubleshooting; actual loaded file paths | Runtime log evidence needed for actual load order and conflict outcome |
| Debugging / validator finding | `error.log`, `debug.log`, `game.log`, `database_conflicts.log` | Source around the reported object; Tiger output and configuration | Logs are runtime/build evidence with a bounded interval; Tiger is not engine validation |

## Generated target-build documentation

R-004 generated both command families from clean CK3 1.20.1.1 on 2026-10-20;
no output was regenerated for R-014. Raw outputs are local under
`<user-data>/logs/` and are not repository artifacts. `script_docs` outputs
include at least:

| Output | What it indexes | Limits |
|---|---|---|
| `effects.log` | Effects, accepted arguments, supported scopes/targets, examples where emitted | A listed effect does not establish when it fires or all side effects |
| `triggers.log` | Triggers, scope/target contracts and documented forms | Does not prove control-flow, short-circuit or live result semantics |
| `event_targets.log` | Named target links and input/output scopes | Documents a route, not that a particular game state produces the expected object |
| `event_scopes.log` | Scope types and capabilities (trigger/effect evaluation, scope changes and variable storage) | Must follow caller context in vanilla; runtime cases may differ |
| `modifiers.log` | Modifier names and relevant typed/reference details | Does not establish where or how long a modifier is applied |
| `on_actions.log` | Registered on-action names, expected scope and whether called from code | Does not prove exact firing order, frequency or coverage |
| `custom_localization.log` | Customizable localization inputs where generated | Check installed output availability; it is not a complete localization-format guide |

The target-build outputs also include additional generated script reference logs;
consult the actual directory index rather than assuming a filename or that every
subsystem is represented. `dump_data_types` refreshed five nonempty text files
under `<user-data>/logs/data_types/`: `data_types_common.txt`,
`data_types_gui.txt`, `data_types_internalclausewitzgui.txt`,
`data_types_script.txt` and `data_types_uncategorized.txt`. These files document
exposed GUI/script types, functions, return
types, and some argument/type information. They are especially useful for GUI
bindings and scope APIs, but can omit arguments or side effects and do not
register a script API, guarantee safe null access, establish UI lifecycle, or
describe the map renderer's producer. Both command families are build-specific
and primary evidence for their documented signatures, not complete engine
specifications.

For this project, reusable verified examples include `holder`, `dynasty`,
`house`, `county`, and `barony` links in `event_targets.log`; liege traversal in
`triggers.log`; title RGB effects and county/barony iterators in `effects.log`;
and GUI `MapMode`/`ScriptedGui` functions in `data_types_*.txt`. See [RESEARCH.md](RESEARCH.md)
and the [R-009 checkpoint](tasks/R-009-barony-color-safety.md) for claims and
their precise target-build evidence limits.

## Installed game sources

### Shipped `.info`

Search the relevant folder for `_<category>.info` and sibling `.info` files,
then read only the section for the object being studied. They are installed
schema/format documentation, often with field descriptions, accepted values,
scope requirements and lifecycle hooks. They outrank a wiki for the installed
build's documented file shape. They can be incomplete, silent about defaults,
loading precedence, engine internals and runtime consequences. Verify syntax
against a nearby shipped definition; verify behavior separately.

Focused Dynasty Map examples already inspected:

- `common/landed_titles/_landed_titles.info` — title fields and RGB;
- `common/dynasty_houses/_dynasty_houses.info`, `common/dynasties/_dynasties.info` —
  House/Dynasty schema and documented color-field limits;
- `common/situation/situations/_situations.info` and
  `gfx/map/province_effects/_province_effects.info` — specialized map-color,
  membership and province-effect contracts;
- `gui/scripted_widgets/_scripted_widgets.info` — widget registration
  description. Its existence does not prove a project's widget placement or
  runtime lifecycle.

No matching map-mode `.info` was found beside `gfx/map/map_modes/map_modes.txt`
or directly in `gfx/map`; do not infer a complete map-mode schema from the
neighboring `.info` files.

### Vanilla usage examples

Treat installed vanilla files as a distinct target-build evidence class: they
show how Paradox actually composes a feature using exposed APIs. Search by
definition key, function/effect name, and caller in a narrow subsystem. Follow
includes, scope setup and effects only as far as the question requires.

| Topic | Search first |
|---|---|
| Map-mode definition, color mode and presentation | `gfx/map/map_modes/map_modes.txt`; graphic defines; native map UI under `gui/shared/` |
| GUI composition, map controls and visibility | `gui/shared/mapmodes.gui`; relevant `gui/hud_*.gui` or window file |
| Scripted GUI invocation / explicit root | `common/scripted_guis/`; `gui/` search for `ScriptedGui.Execute` and `GuiScope.SetRoot` |
| County, barony, holder and title scope patterns | `common/` script call site; `common/landed_titles/`; generated `event_targets.log` |
| Character, House and Dynasty patterns | `common/dynasties/`, `common/dynasty_houses/`, targeted character interactions/decisions and generated scope docs |
| Liege traversal | `common/` searches for `any_liege_or_above` / `every_liege_or_above`, checked against `triggers.log` |
| Effects, triggers and reusable script | `common/scripted_effects/`, `common/scripted_triggers/` and one caller |
| on_actions and lifecycle | `common/on_action/`, then follow the event/effect chain; confirm API in `on_actions.log` |
| Localization and dynamic text | matching `localization/<language>/` entry and the GUI/script that consumes it |
| Mod paths and file loading | shipped folder layout, `.info`, mod descriptor examples; compare the actual session's `debug.log` |

Generated docs answer “is this API documented and for which scopes?” Vanilla
answers “how is it used in shipped content?” Neither automatically answers
“what will this state do in a live game?” That remains a bounded runtime
question. Do not copy or modify vanilla files as a research shortcut.

## Runtime and debugging sources

- `-debug_mode` exposes the developer console and debug information; `-develop`
  enables development conveniences described by CK3 modding references. Check
  current installed behavior before relying on hot reload; it is not a
  correctness validator.
- The in-game developer console can invoke `script_docs` and `dump_data_types`
  and is useful for controlled user-led observations. It does not make a
  console response proof of later rendering or save behavior.
- GUI debug/editor facilities can help inspect widgets and live GUI state.
  Confirm availability and relevant commands in the installed build; editor
  visibility is not evidence that an engine callback or renderer input exists.
- Registered Data Types / GUI data-type explorers, when exposed in the current
  build, are interactive discovery aids. Prefer the generated
  `dump_data_types` output for reproducible static citations; the explorer was
  not separately validated for this task.
- `<user-data>/logs/error.log` records errors; `debug.log` helps establish
  session startup, loaded mods and debug context; `game.log` records game
  events; `database_conflicts.log` helps find duplicate/conflicting database
  objects. Preserve a bounded interval and compare with a vanilla baseline
  where relevant. Empty logs cover only the actions that occurred.
- Errorhoof or another log viewer is a presentation/search aid over logs, not
  an independent source of engine semantics. Do not assume availability unless
  installed and confirmed.
- [Tiger](https://github.com/amtep/tiger) is an external validator for script
  syntax, missing objects/localization, scope consistency and other supported
  checks. Its README calls it mature but notes false positives and that updates
  can trail game patches by days or weeks; visible releases include CK3 1.19.0.
  Use Tiger output as a lead to inspect, not as the API authority or runtime
  proof. R-012 owns local setup; Tiger was not installed or run here.

## External references (assessed 2026-10-21)

| Source | Status / useful for | Limits and evidence rule |
|---|---|---|
| [CK3 Paradox Wiki modding category](https://ck3.paradoxwikis.com/Category:Modding), including [Modding overview](https://ck3.paradoxwikis.com/Modding), [Scripting](https://ck3.paradoxwikis.com/Scripting), [Scopes](https://ck3.paradoxwikis.com/Scopes), [Triggers](https://ck3.paradoxwikis.com/Triggers), [Effects](https://ck3.paradoxwikis.com/Effects), [Interface](https://ck3.paradoxwikis.com/Interface), [Mod structure](https://ck3.paradoxwikis.com/Mod_structure), [Localization](https://ck3.paradoxwikis.com/Localization), [Mod troubleshooting](https://ck3.paradoxwikis.com/Mod_troubleshooting), [Console commands](https://ck3.paradoxwikis.com/Console_commands), [Map modding](https://ck3.paradoxwikis.com/Map_modding) | Canonical CK3 wiki; explanatory pages, concepts, console/debug guidance and navigation. | Direct pages returned 401 to the research fetcher. Page-specific current status is not implied by mirror commits: its mirror records `Scopes` verified for version 1.1 and `Localization` for 1.4; version notices vary or may be absent. Check each canonical page's own notice. Strong secondary reference; old verification cannot override 1.20.1.1 sources. |
| [jesec/ck3-modding-wiki](https://github.com/jesec/ck3-modding-wiki), [contents index](https://github.com/jesec/ck3-modding-wiki/blob/master/TABLE_OF_CONTENTS.md) | Community-maintained Markdown mirror/archive of modding-related Paradox Wiki pages; easy local/GitHub search. README claims daily GitHub Actions updates and links the canonical wiki. | A mirror, not official authority. The update cadence is a repository claim, not a guarantee that each page is current or target-build verified. Its mirrored Mod structure page explicitly shows version 1.1 verification. Use it to find pages, then reconcile. |
| [my-mods/awesome-ck3](https://github.com/my-mods/awesome-ck3) | Community resource index covering docs, guides, communities and tools; README points to CK3 User Mods and CK3 Modding Discord. | Discovery index; current maintenance was not established in this assessment. Links/guides may be stale and are not API authority. |
| [CK3 Modding Discord](https://discord.com/invite/apEvxDZ), [Paradox CK3 User Mods forum](https://forum.paradoxplaza.com/forum/forums/crusader-kings-iii.1046/) | Community troubleshooting, current practice and finding maintainers/examples. Linked by the Wiki mirror/resource index. | Informal and version-dependent. No Discord content was accessed. A bounded sample of Reddit threads ([learning resources](https://www.reddit.com/r/CrusaderKings/comments/1hvwxan/what_are_the_best_places_to_learn_to_mod_ck3/), [Wiki coverage](https://www.reddit.com/r/CrusaderKings/comments/1jng1eb/is_there_a_comprehensive_modding_wiki/)) recommends reading vanilla beside the Wiki and reports documentation gaps. Treat these anecdotes as leads only. |
| [CK3-Modding/Documentation](https://github.com/CK3-Modding/Documentation) | Archived community documentation; searchable concept explanations and older examples. | GitHub marks the repository archived on 2023-06-21; HISTORICAL only. Recheck all claims against current installed sources. |
| [nonniks/CK3_Documentation](https://github.com/nonniks/CK3_Documentation) | Derived AI-oriented package claiming extracted `.info` files and generated logs; useful for discovery/search when a local corpus is unavailable. | README reports build date 2025-11-24 and its own extraction/regeneration process. It is derived, not the installed target build; provenance does not establish exact 1.20.1.1 coverage. Do not import it into this project. |
| [Tiger README and releases](https://github.com/amtep/tiger) | Documentation for validator capability, configuration and known limitations. | Tool documentation is authoritative only for Tiger's behavior; validator version may lag CK3. No install/run in R-014 (R-012 owns setup). |
| [Paradox CK3 User Mods forum](https://forum.paradoxplaza.com/forum/forums/crusader-kings-iii.1046/) and bounded [Reddit discussion sample](https://www.reddit.com/r/CrusaderKings/comments/1hvwxan/) | Community troubleshooting and discovery. The sampled threads recommend reading vanilla with the Wiki and report gaps in public documentation. A 2024 [CK3 modding discussion](https://www.strategium.ru/forum/topic/94386-%D0%B2%D0%BE%D0%BF%D1%80%D0%BE%D1%81%D1%8B-%D0%BF%D0%BE-%D0%BC%D0%BE%D0%B4%D0%B4%D0%B8%D0%BD%D0%B3%D1%83-crusader-kings-3/page/50) demonstrates users navigating generated GUI data types and vanilla callers. | Informal and version-dependent; sample is not a survey or technical proof. No Discord content was accessed. Do not promote forum/Reddit/Discord consensus over generated docs, `.info`, vanilla or reproducible runtime evidence. |

External checks used primary project pages/READMEs where possible. The mirror's
daily-sync statement and the derived repository's build date are recorded as
claims visible in those repositories, not independently verified coverage.
No external documentation was copied into this repository.

## Research playbook

1. Name the subsystem and the claim to establish; consult this map's quick
   lookup row.
2. For API signatures/scopes, search the installed build's generated output.
   For file shape, inspect the relevant shipped `.info`.
3. For practical wiring, inspect one or two narrow installed vanilla examples
   and their caller/context.
4. Label the result as documented API, shipped usage or bounded runtime
   evidence. If static sources do not establish the behavior, define the
   smallest user-led runtime check in its own authorized task. Do not infer
   proof from absence in a searched subset.
5. Use Wiki/mirror for explanation and navigation; use Tiger to catch supported
   static errors; use community search only to generate leads. Revalidate each
   lead against target-build evidence.
6. Keep raw dumps/logs/save data local. Record concise findings, source build,
   exact locations and limitations in the canonical task summary.

For the current renderer boundary, R-009 remains **PARTIAL**: no supported
independent view-specific barony color input or safe cleanup lifecycle has
been established. This map is a navigation aid, not a resolution of those
unknowns.
