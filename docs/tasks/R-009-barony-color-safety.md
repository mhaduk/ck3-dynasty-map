# R-009 — Barony color side effects, isolation and restore

**Current disposition — 2026-10-23: REDUCE / open.** Keep only the current map-native renderer safety question: exact restoration of arbitrary live originals, shared title-RGB isolation and save/load/removal feasibility. R-016’s 1.20.1.2 bounded execution and F-001 visual approval do not establish these. First identify a concrete supported capture/restore or isolated input contract; stop with evidence or a precise blocked renderer decision. No repeat broad scans, excluded carriers, dummy-title inertness project or palette-source duplication; F-002 owns accent/fallback, R-005 dispatch/context loss, F-001 normal UI acceptance. Local/saved-scope cleanup is not title RGB restoration. See [T-005](T-005-research-backlog-review.md). Historical proposals below are superseded as next steps.


Status: PARTIAL / active. Target: CK3 1.20.1.1 (Crozier).
Updated: 2026-10-21. Issue: [#9](https://github.com/mhaduk/ck3-dynasty-map/issues/9).

## Current disposition — 2026-10-21

The highlight/selection and binary-view findings below are retained as static
research history. ADR-009 subsequently excluded Decisions, council selectors,
Situations and religious-object carriers from the product architecture. Their
historical proposed experiments are not current next steps. No binary product
scope reduction or carrier probe is approved. R-009 remains PARTIAL: shared
barony RGB writes and serialization are confirmed for the tested paths, while
acceptable persistence, broader visual effects and cleanup remain unresolved.
This checkpoint records existing findings only; no new source research,
runtime, installation or issue update is included.

## Result and architectural consequence

The first user-run [batch](../../research/probes/barony-color-batch/README.md)
confirmed visible direct RGB, named-color and copy writes on two fixed baronies.
Both native and custom barony views use the changed state. Mode changes and
reported observer transition retained it. Read-only inspection of designated
BEFORE/AFTER copies now confirms explicit title RGB overrides in AFTER that are
absent from BEFORE: these writes serialize into the save. A fresh-process load
with the mod disabled remains untested. This mechanism has not met temporary,
view-specific coloring and restoration requirements.

An independent barony -> DIRECT/CONTROLLED/OTHER -> palette model is conceptually
valid, but a supported connection to a view-specific renderer is **unverified**.
Focused native data-source research found engine-bound province color textures
and specialized Situation color inputs; no generic classification/table upload
hook was identified in the inspected sources. Do not implement the classifier,
add titles or optimize refresh before resolving that boundary. The project
remains M0 / pre-implementation; ADR semantics are unchanged.

## Native color data trace — static evidence

Paths below are game-relative; generated filenames refer to existing target-build
documentation. R-002/R-003 definition and GUI research is reused.

| Native mode / producer | Grouping and color evidence | Exposed input / unresolved boundary |
|---|---|---|
| `baronies` / `baronies` | Barony names/selection; title definitions supply map RGB; title effects modify it. User-run views and save inspection connect changed barony RGB to shared title state. | Mode presentation, title definitions and RGB/named/copy writes exposed. No independent per-view class palette identified. `gfx/map/map_modes/map_modes.txt:116–122`; `common/landed_titles/_landed_titles.info:34–36`; generated `effects.log:12646–12649,12761–12767`. |
| `realms` / `selected_character_realms` | Ruler/realm grouping with vassal exploration. Defines document liege/vassal zoom behavior, tributary/confederation mixing and a civil-war branch using primary-title color. | Presentation/global factors exposed; full ordinary realm color lookup and political-group-to-province algorithm remain engine behavior. No category callback identified. `map_modes.txt:276–281`; `common/defines/graphic/00_graphics.txt:225–226,435–438`. |
| `houses` / `houses` | County/explored-House names; tooltip follows title -> `GetHouseMapModeTitleHolder` -> House. Helper returns Character. Actual RGB origin and helper's holder/ancestor selection algorithm UNKNOWN. | House/Dynasty template `color` is documented as read but unused by game logic; no active map RGB or Dynasty-collapse callback demonstrated. Do not assume CoA/title/head color. `map_modes.txt:2961–2967`; `localization/english/gui/map_l_english.yml:104–105`; generated `data_types_uncategorized.txt:113829–113831`; `common/dynasty_houses/_dynasty_houses.info:39–42`; `common/dynasties/_dynasties.info:41–44`. |
| Faiths: `religions` / `religions` | Native description: county faith, selected-Faith rites at close zoom, stripes for county/top-liege faith mismatch. Tooltip reads county Rite and its Faith, separately holder/top-liege Rite. Faith/Rite definitions supply colors. | Religious definitions/colors exposed; county faith/rite changes mutate religion, not a separate category channel. Exact zoom/stripe/cache producer remains opaque. `map_modes.txt:1434–1441`; `localization/english/gui/ingame_main_l_english.yml:39`; `localization/english/gui/map_l_english.yml:116–121`; `common/religion/rite_types/_rite_types.info:27–40`, `faith_types/_faith_types.info:1–12`. |

The general Realms/Houses UI semantics above also have native description
support in `localization/english/gui/ingame_main_l_english.yml:28,53`. Those
strings describe intended native behavior; this task did not run those tests.

`gfx/FX/jomini/jomini_province_overlays.fxh:9–26,77–135` binds and samples
`JominiProvinceColorIndirection` / `JominiProvinceColor`, combining primary,
secondary and alternate channels with gradients/edges. `gfx/FX/bordercolor.fxh:55–75`
adds pattern, desaturation and lighting/flat-map blending. The shader is an
exposed consumer; the mode-specific producer populating those resources remains
opaque. Seeing shader text does not establish a dynamic script/GUI upload path.

Generated `MapMode` lists metadata/accessors, not color submission, provider
registration or invalidation (`data_types_uncategorized.txt:86117–86160`).
`SetMapMode` selects a key; return-to-Realms only selects another renderer
(`gui/shared/mapmodes.gui:1398–1407`). No exposed cache/update schedule,
automatic exit cleanup, transient local storage or synchronization contract was
identified in the reviewed map types/configuration/shaders. Variables/lists
alone do not establish consumption. Native House grouping is not Dynasty
classification; religious/political grouping is not interchangeable with it.

### Concrete alternative and recommendation

Situation is a documented specialized consumer: native `situation` selects
`color_mode = situation` (`map_modes.txt:5226–5231`). Situation schemas expose
sub-region/group `map_color`, geographical/title membership, character-validity
triggers and lifecycle hooks (`common/situation/situations/_situations.info:64–98,114–185`).
Generated `start_situation` accepts sub-region RGB; title membership operations
add/remove de-jure counties (`effects.log:2857–2876,18244–18256,18423–18435`).
This is positive extension evidence, not proof of a local temporary map layer.

At least one nonoverlapping sub-region and limits of 255 regions/groups apply;
three category regions do not automatically exceed that limit. County-key
membership now has installed add/remove usage evidence (below); character-group
projection into territory, independent view binding, saved/shared behavior and
cleanup remain unresolved.
Situation phase province effects are another real consumer, with effect-index
priority and primary/secondary collisions, but no demonstrated independent
barony-class upload or view-local lifecycle (`gfx/map/province_effects/_province_effects.info:5–16,24–38`;
Situation schema `:267–271`).

The bounded Situation trace below advances that investigation. Exact House RGB
origin is secondary until a reusable input exists; All Dynasties stays gated.

Direct/named writes avoid dummy sources but retain title mutation/serialization.
Copy writes add documented drift and fixture side effects. Neither is selected
as the production fallback. Shared shader recoloring lacks a classification
input and verified view gating. No final color strategy or ADR revision occurs.

### Two binary player views — static feasibility (2026-10-21)

The proposed separate DIRECT and exclusive INDIRECT views are a **viable runtime
hypothesis through a county title selector**, not a verified production route.
Reducing the requirement to one highlighted set removes the need for three
simultaneous class colors. The prior three-color negative result does not rule
this out. This is analysis of a product proposal; G1 and ADR semantics remain
unchanged. All Dynasties is a separate many-group problem.

With valid player Dynasty PD, DIRECT means a present holder whose Dynasty equals
PD. INDIRECT means NOT DIRECT, a present holder and a de-facto liege above that
holder with Dynasty PD. Lowborn holders still require the liege check; absent
holders match neither. Cadet Houses compare via Dynasty. Direct-view background
includes CONTROLLED and OTHER; indirect-view background includes DIRECT and
OTHER. Neither background means “no dynastic connection.” Invalid player/PD
means unavailable under ADR-008, not an empty result. A union of DIRECT and
CONTROLLED would be a different optional view, not exclusive INDIRECT.

`common/decisions/_decisions.info:286–310,376–404` documents one widget per
decision, title-root `title_valid`, decision-taker `scope:ruler` and world/realm
tier controllers. The shipped realm county selector's predicate checks holder
identity plus a vacant province without construction
(`common/decisions/00_holy_order_decisions.txt:648–663`;
`common/scripted_triggers/00_religious_triggers.txt:1122–1128`). The world
`select_county_title` controller is documented; the realm variant cannot cover
dynastic land across independent realms. Exact inclusion of unheld/nonstandard
counties remains unknown.

A newly traced Faith-window shortcut opens that exact decision with
`GetDecisionWithKey` and `OpenGameViewData('decision_detail', Decision.Self)`
(`gui/window_faith.gui:1489–1516`). Thus two authored decision identities can
carry two predicates through an exposed opening action. The widget then calls
`OnSelectTitle`; selector GUI consumes a list and one selected title
(`gui/decision_view_widgets/decision_view_generic_title_selector_widget.gui:15–30`;
`gui/window_title_selector.gui:23–25,34–55,74–96`). This is decision-carried
inspection, not a demonstrated independent map-mode extension. Opening the
decision and confirming its execution are distinct actions.

Native `select_county_title` uses filled gradients at near through flat zoom
(`gfx/map/map_modes/map_modes.txt:34–92,1991–2067`), supporting investigation of
area fill. No explicit predicate-to-renderer binding or assignment of valid/
invalid colors is exposed in that chain. A list/checkmark is not proof that all
matching counties are filled simultaneously. Global validity/default palettes
are not view-owned; overriding them may affect vanilla. Selected-title emphasis,
exact county-to-barony coverage and hidden universe filters remain unknown.
The standard picker button also requires `HasValidTitles`, so a legitimate
zero-match view needs separate handling; safe empty-context rendering is unproven.

Normal decision-list selection triggers `ResetCustomWidgetState` through an
animation (`gui/window_decisions.gui:354–355`;
`gui/window_decisions_detail.gui:28–38`). The shortcut does not explicitly do so.
This reset is not a verified map refresh/clear. Two contexts' replacement,
fresh PD binding, context loss, Close/map-switch cleanup, save/removal and native
evaluation cost remain unexamined. R-005's diagnostic guards do not validate
this controller. `SetMapMode` alone supplies neither predicate nor ruler.

Council predicates remain a weaker binary hypothesis: `county_target = all`
exists, but potential-task activation depends on council/position context.
The location UI exposes Close separately from Select
(`gui/window_council.gui:210–228,323–330,1054–1059,1099–1108`;
generated `data_types_uncategorized.txt:93915–93970`). That does not prove
side-effect-free preview or cleanup. A fake decision/task still couples the map
to unrelated gameplay machinery; persistence alone is not the objection.

Together, two consistent binary snapshots could recover all three original
categories, but lose simultaneous comparison and require precise legends.
Neither “has a Dynasty” nor inspecting one chosen Dynasty satisfies All
Dynasties; no new House-to-Dynasty renderer/palette input was found. GUI may
consider one future fixed-target world-selector experiment for simultaneous
fill, outside-realm/lowborn-holder controls, selected/empty states and context
replacement/clear. Only an outline was returned locally: no probe, classifier,
installation or runtime stage is prepared or authorized. R-009 remains partial.

### Native highlight and selection inputs — static checkpoint (2026-10-21)

No suitable independent three-category area-color input was found in the
bounded target-build highlight/selection pass. This does not prove global
engine impossibility. The conceptual classifier and ADR semantics are unchanged.

| Input family | Positive evidence | Missing link for this project |
|---|---|---|
| Title picker | `common/decisions/_decisions.info:305–310,388–404` documents title-root `title_valid` with `scope:ruler` and tier/world/realm controllers; `common/decisions/00_holy_order_decisions.txt:648–666` supplies a county predicate. GUI calls selection and Close/Confirm (`gui/decision_view_widgets/decision_view_generic_title_selector_widget.gui:15–30`; `gui/window_title_selector.gui:23–25,47–55,91–96`). | Script-fed eligibility is real; no three county-set/RGB channels or arbitrary layer clear. Native `select_county_title` exists (`gfx/map/map_modes/map_modes.txt:1991–2067`), but controller-to-renderer binding, barony fill, context cleanup and persistence are not documented by these callers. |
| Council target preview | County target enums, potential/valid predicates, own-realm tint and assignment hooks (`common/council_tasks/_council_tasks.info:3–14,35–60`); actual task-selection button (`gui/window_council.gui:1099–1108`). | Native task/validity/numeric palettes are not arbitrary dynasty categories; preview-to-renderer/exit behavior and barony coverage remain unknown. Assignment is gameplay; its cancellation hook is not a custom visual-layer callback. |
| Geographical regions | Definition county/province lists and visual-region RGB (`map_data/geographical_regions/_geographical_regions.info:3–32`); multiple selected database regions, Toggle/Clear/Close (`gui/window_geographical_regions.gui:45–81,111–127`; generated `data_types_uncategorized.txt:70321–70424`). | Authored geography is not runtime class membership. No membership writer or selected-region/category RGB binding identified; debug and visual-region consumers are distinct (`map_modes.txt:3863–3867,3942–3946`). Situation membership effects do not edit a geographical region. |
| Hover/highlight | Struggle object enter/leave border clear (`gui/hud.gui:5014–5022`); global holding/highlight alpha and native palettes (`common/defines/graphic/00_graphics.txt:209–219,399–433,926–928`). | Object/border input and global appearance knobs do not supply arbitrary area geometry or three view-owned colors. Icons/pins and editor painting are different interfaces. |

These are potential selection-based inspection interfaces, not a verified
DIRECT/CONTROLLED/OTHER map. Explicit UI Close/Clear actions do not establish
automatic cleanup on map/context changes, local execution or save/removal
safety. No new producer/binding justified repeating shader research.

The bounded external sample found no independent implementation:
[War Maps 3](https://steamcommunity.com/workshop/filedetails/?id=3450639748)
describes the known dummy-title/barony-copy family (updated 2025-07-11, 1.16
discussion); [Trade Maps DTR](https://steamcommunity.com/sharedfiles/filedetails/?id=2821874072)
declares War Maps ancestry (updated 2024-12-16), without an accessible original
implementation proving a different route; [More Mapmode Buttons](https://steamcommunity.com/sharedfiles/filedetails/?id=2223763531)
describes buttons/presentation (CK3 1.2, updated 2020-11-24). No original code
repository or reusable code license was located for these three; none was
installed or validated for 1.20.1.1. Descriptions do not prove internal APIs.

Next: GUI reviews the options and chooses whether a selection-based UX merits
later investigation or further map research requires a concrete new input
source. No candidate meets the independent three-category contract yet.
Persistent data remains acceptable in principle; fragile gameplay-system reuse
and safe lifecycle/removal are the concerns. No probe preparation, installation
or runtime stage is authorized by this pass. Full trace, comparison matrix and
negative-search register were returned in the local CLI result package.

### Situation feasibility — static checkpoint

**Blocked on named unknowns, not an approved architecture.** The first
`natural_disaster_earthquake` object in
`common/situation/situations/tgp_natural_disaster.txt:1–180` provides a compact
start/membership/phase/end trace. Its area starts empty; the spawn effect adds
the epicenter **county** and neighboring **counties** using
`add_dejure_title_to_sub_region`
(`common/scripted_effects/10_dlc_tgp_natural_disaster_scripted_effects.txt:73–133`).
Cleanup removes individual counties with the paired effect
(`events/situation_events/tgp_natural_disaster_events.txt:43–84`), and a separate
remaining-participant condition ends the Situation (`:87–110`). This resolves
county-key acceptance at installed-script level; exact runtime coverage and
cross-category movement remain untested.

The earthquake omits `map_mode`, so its documented default is participant-group
coloring. Region RGB alone does not establish its visible output. A bounded
second reference explicitly selects `map_mode = sub_regions` and independent
region RGB (`common/situation/situations/game_extra_nomads_sami.txt:1–24`);
the native consumer is `color_mode = situation`. This is a concrete region/color
input route without title RGB writes or extra titles, not a generic class upload.

| Requirement | Static result / unresolved behavior |
|---|---|
| Three disjoint dynamic county classes | County add/remove usage supported; three fits the 255-region limit. Reassignment, empty categories, unheld/nonstandard county and relevant barony coverage untested. Character groups are not a verified substitute for county classes. |
| Explicit RGB independent of title colors | Input contract supported by schema/start effect and region-mode example. Visible colors and rendering with zero participants untested. |
| Independent selection and simultaneous vanilla Situations | Blocked: list/pin selects a world object by ID; generic window selects a sub-region. No independent named-map-to-Situation binding or competing-view arbitration demonstrated. |
| ADR-008, refresh, context loss and clean exit without inactive scans | Blocked: on-demand membership/end effects exist; automatic renderer cleanup/context hooks and engine maintenance cost unverified. Close/map selection is not documented to end the object. |
| Suppress unnecessary gameplay/UI | Both automatic enrollment switches can be disabled and authored hooks/modifiers/migration omitted. Safe zero-participant rendering and complete UI/notification suppression unverified; hiding a shortcut does not hide the Situation. |
| Local ephemeral state, save/load and removal | Exposed route mutates a world Situation. No local-only/nonserialized storage contract identified. Exact Situation serialization, synchronization, post-end residue and disabled-mod load remain untested. |
| DLC/feature requirement | Sami creation explicitly requires MPO and a game rule; no generic Situation entitlement requirement established by schema/start API. File prefixes do not prove one. |

Selection uses `ToggleGameViewData(Situation.GetWindowName, Situation.GetID)`
(`gui/window_situation_list.gui:369–374`; map pin `gui/map_icon_layer.gui:6068–6086`).
The generic view reads/selects a sub-region
(`gui/window_situation.gui:70–114,738–744`); generated
`data_types_uncategorized.txt:108524–108532,108680–108682` confirms accessors,
not renderer arbitration or automatic Close cleanup. Other-tab Situation items
include nonparticipants (`window_situation_list.gui:261–272`). The visibility
toggle pins only shortcuts (`:512–550`;
`localization/english/situations/situation_list_window_l_english.yml:14–18`).

The schema explicitly permits disabling both ruler auto-add paths and exposes
authored hooks (`_situations.info:129–218`). Disaster events/modifiers/pulses are
therefore not mandatory generic behavior. Conversely, world uniqueness,
mutable membership, dated phases and explicit end effects establish simulation
usage, not local GUI storage. Temporary scope references do not make the object
temporary. Participant/group `on_leave` does not fire on Situation end
(`:170–175,200–208`), so cleanup cannot rely on it. No save was inspected for
Situation state; earlier title RGB serialization cannot establish that state.
Phase province overlays share this carrier and add effect-channel collisions;
they do not resolve locality, selection or lifecycle.

R-014 documentation-source inventory is complete. The subsequent highlight
input pass above used its source map. The user has not made
persistent state categorically unacceptable; the concern is whether reusing
unrelated title/Situation systems would be a fragile map workaround. Situation
remains a specialized, unapproved candidate with unresolved view binding,
coverage, lifecycle, save/removal and gameplay/UI effects. Any later runtime
scope needs a fresh design and explicit authorization. Do not repeat prior
passed batches. R-009 and RG-STATE-01 remain open.

## First user-run batch — actual evidence

Evidence combines user reports/supplied crops and preserved logs; Codex did not
inspect or control the CK3 game UI. Sources remain unchanged after installation.

| Cases | Observed result | Limit |
|---|---|---|
| C00; initial C09 | Targets/controls and four unheld fixtures exist; one valid-player title-root receipt | No observer title-root success inferred |
| C01=2, C02=1, C03=5, C05=2, C06=1, C07=2 | Complete log pairs and per-target effect markers; direct/named/copy visibly changed A/B; one C05 after reload | Actual counts exceeded plan. Similar appearance is not exact RGB equality or a per-copy drift measurement |
| C04; C10 | No invocations; skipped | Cyan setup error; observer C09 lacked a new receipt, so no C10 reset |
| M01/M02/A01 | Native and both original custom barony views reported rendering; minimal more terrain-blended, filled slightly lighter | Differing crops/zoom do not quantify intensity. This supports only tested custom definitions, not general registration/schema rules |
| L01 | Other comparison modes reportedly normal; native baronies shows mutations again after round-trip | Bounded mode/zoom coverage; shared barony state, not map-only isolation or restoration |
| S01 | AFTER reload in same process retained purple before writes; subsequent C05 worked | Serialization separately established below; fresh-process/disabled-mod rendering still untested |
| L02 / observer C09 | Reported NO PLAYER retained yellow/purple; no new C09 receipt beyond initial baseline | Reported clicks not verified; no dispatch cause inferred; no automatic cleanup installed |
| C08=1; C11=1 | Complete receipts for both targets; copied/direct definition resets made both red | Static definition reset only; not arbitrary live-original capture or automatic restore |
| BEFORE load | Reported red after loading, after manual resets had already made targets red | Not independent proof of rollback from marked state; no repeat requested |
| D01 | All four fixtures visible in Find Title; Magenta window says Not created yet | User-reported creatability unverified; no Create action/requirements established and no creation performed |

All four fixtures produced CoA generation errors; cyan also lacks a capital.
Two source files lack UTF-8 BOM. Court-scene errors occur in the run; GUI
warnings are empty. No whole-run-clean claim. Search visibility/setup errors
leave inertness unresolved; definition guards alone do not prove it. There are
four fixed sources, never one title per barony. They are historical diagnostic
fixtures, not an approved production palette.

## Supporting save inspection and restoration limits

Only designated disposable BEFORE/AFTER saves were opened and inspected on
ignored copies using existing ZIP/plain-text tooling. Original SHA-256 hashes
were equal before/after. AFTER contains explicit title-level RGB overrides for
London and Southwark; BEFORE has no explicit RGB override in those records.
The two AFTER values differ numerically. These fields are separate from CoA
references, demonstrating serialized title-color changes and bounded inequality,
not a per-invocation drift law. Absent/default fields are not a live-original
getter. All four fixture records occur in both saves; registration is not proof
of creation/ownership. No inference about Realms/Houses/Faith internal storage
or post-disable behavior follows.

C08 copies static-definition red with documented drift. C11 writes that RGB
directly; C10 was skipped. Neither captures customization/prior mutations.
Focused generated-effects/event-targets/Title searches have not identified an
arbitrary title RGB getter, exact snapshot or reset-color API. Customization
window state is not a demonstrated arbitrary-title capture interface. No
invented automatic reset or live-original-to-dummy snapshot is adopted.

## Operational checkpoint and checks

User reported CK3 closed and launcher reopened; GUI restored the previous
selection (Native Menu Probe on; Entry/R009 off) and verified it in launcher
and enabled-mod manifest. R009 remains installed but disabled. This CLI task
accepted that declared state, performed no app/process inspection and changed
no installation/playset/save/vanilla source. Existing raw evidence, chronology,
save copies and audit remain ignored locally.

This stage performed source-citation/diff self-review, relative-link checks,
public-content privacy review and `git diff --check`. It ran no new game test,
Tiger, engine parser, tool installation or independent review. No Git staging,
commit, push, fetch or GitHub operation. Full local trace and remaining
questions are returned through the delegated result; R-009 is not complete.
