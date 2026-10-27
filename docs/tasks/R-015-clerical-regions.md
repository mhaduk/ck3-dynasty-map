# R-015 — Clerical Regions renderer and scripting feasibility

Status: CLOSED — not planned, 2026-10-21. Architecture direction parked by
explicit user authorization; GitHub closure verified. Technical findings remain
partial: independent ownership/binding and runtime lifecycle unestablished.
Intended Rite-mismatch stripes officially documented. No probe was prepared.
Target: CK3 1.20.1.1 (Crozier); revalidate narrowly if the target build changes.
Priority: P1. Dependencies: R-001, R-004; reuse R-002/R-003 and R-009 findings.
Issue: [#15](https://github.com/mhaduk/ck3-dynasty-map/issues/15).

## Subsequent user direction — 2026-10-21

ADR-009 requires map-system interfaces. Synthetic/actual religious-region
carriers are excluded from the product architecture; the earlier conditional
religious-mutation experiment below is no longer a proposed next step.
Independent map-provider discovery remains relevant, but no such input was
identified by Stage A. Preserve the research as evidence, not a carrier plan.

## Goal

Determine whether the Clerical Regions mechanism exposes a reusable way to
render custom, dynamically assigned county groups, colors and stripes for
Dynasty Map, independently of the actual religious geography. Establish the
supported input and lifecycle contract, or document exactly which missing
interfaces or constraints prevent reuse. Visual similarity is a hypothesis,
not proof of a generic renderer API.

Evaluate three routes separately: an independent custom data provider using
the renderer; isolated synthetic region objects that coexist with vanilla;
and changes to actual clerical regions. The third is a comparison case, not an
approved architecture. Persistent state is not categorically forbidden, but
its gameplay, save, compatibility and removal costs must be explicit.

## Existing evidence and boundaries

- R-009 already confirms tested barony RGB writes, custom barony rendering and
  title-color serialization. Do not repeat those experiments. Its independent
  color input and safe lifecycle questions remain open.
- Preliminary local inspection found `clerical_regions` with
  `color_mode = clerical_regions`, county small names, clerical-region large
  names and selection in `gfx/map/map_modes/map_modes.txt:6054–6060`.
  `gui/shared/mapmodes.gui` exposes the native mode and Faith submenu.
- Existing generated `effects.log` describes `create_clerical_region` as
  taking free counties in the capital's de-jure kingdom reachable by land;
  `expand_clerical_region` takes adjacent counties outside existing regions.
  `split_clerical_region` and `transfer_to_new_clerical_region` also exist.
  These descriptions are static API evidence, not tested coverage or a
  complete inventory of available operations.
- Striped rendering is a lead from external research. Its exact meaning,
  triggering conditions and script accessibility are not yet verified here.
- Current ADRs remain unchanged: county semantics, DIRECT/CONTROLLED/OTHER,
  valid-player-Dynasty guards and activation/manual refresh first. All
  Dynasties requires grouping by Dynasty, including cadet Houses together.

## Investigation questions

1. **Trace the complete input chain.** Follow native definition, selection,
   GUI types, region/title identities, membership, color source and renderer
   consumer. Identify which parts are script/configurable and which appear
   engine-controlled. Distinguish authored definition keys from native
   `color_mode` values. A copied definition must not be mistaken for a new
   provider or independent storage.
2. **Membership and geometry.** Inventory creation, add/remove, reassignment,
   split, merge and destruction/reset interfaces and their scopes. Can one
   group contain disconnected counties across de-jure kingdoms, realms and
   faiths? Can an already assigned county move? Are overlaps, empty groups,
   unheld counties, water-separated land and all baronies of a county covered?
   Separate enforced constraints from defaults that another supported API
   could bypass. Determine group/object limits and DLC/feature requirements.
3. **Colors and stripes.** Locate actual color ownership and selection,
   primary/secondary channels and stripe conditions. Can a script supply
   independent fixed RGB or named colors without changing title RGB, faith,
   rite or religious authority? Are stripes arbitrary two-group display,
   overlap, or a hardcoded religious mismatch? Check zoom and selection
   overrides. Trace shader use only as needed to find a concrete input binding.
4. **Isolation and gameplay.** Can a separately named mode use its own region
   dataset while native Clerical Regions and other views continue to work?
   Would synthetic objects enter religious hierarchy, elections, succession,
   title ownership, AI, notifications, lists, modifiers or on-actions? Can those
   effects actually be omitted? Hiding UI alone is not isolation. Determine
   collision and load-order implications without replacing vanilla files.
5. **Lifecycle and persistence.** Identify documented refresh/invalidation,
   entry/exit, context replacement and deletion paths. Assess activation and
   manual refresh, loss of player/Dynasty, observer/load transitions,
   serialization, multiplayer locality/synchronization, and mod-disabled load.
   Distinguish hiding a view, clearing membership and destroying its objects.
   Do not infer restoration from a Close button or variable lifetime. Assess
   engine maintenance and update cost without inventing recurring world scans.
6. **Fit to the product.** Evaluate simultaneous three-category My Dynasty,
   the separately proposed binary views and many-group All Dynasties
   independently. An eligibility mask, one selected region, or existing
   religious grouping does not establish the required classification input.

## Stage A — Static research first

Start with `docs/CK3_SOURCE_MAP.md`, this task and the R-009 checkpoint. Reuse
existing clean generated docs: effects, triggers, event targets/scopes,
on-actions and GUI/script data types. Open relevant installed `.info`, then
follow narrowly selected vanilla religion, title, effect, event, GUI,
localization and graphics callers. Broaden only when the trace requires it.
No fresh documentation generation, installation or game launch is needed.

Return a capability matrix with exact game-relative file/line references,
evidence labels (static VERIFIED, LIKELY, UNKNOWN, or bounded runtime VERIFIED),
supported signatures, constraints and a bounded negative-search register.
Identify conflicting or outdated external claims. Static absence in a subset
must not become a claim of engine impossibility.

GUI owns scope and interpretation. Use CLI Sol / High for a bounded specialist
investigation through `.codex-sync/`, with precise file ownership and no
overlapping edits. Use Luna / Medium for later settled probe preparation.
Recommendations are not claims that a model was actually selected.

## Stage B — Conditional runtime experiment design

Design a minimal, isolated probe only if Stage A identifies a concrete exposed
input or a specific ambiguity that runtime can resolve. If no such path is
found, return the blocker and stop; do not create religious objects merely to
produce a similar screenshot. Preparing/installing/running a probe needs a
later explicit scope; this issue creation authorizes none of those actions.

The proposed test matrix should include:

- a native positive control and a custom view of the same input, followed by
  evidence that independent custom membership can actually be supplied;
- three fixed county groups, including disconnected and water-separated
  examples, an already assigned county and an unheld/empty holding control;
- move one county between groups, then empty a group; check stale fill,
  selection and updates while active and after re-entry;
- distinct colors and, only if an input exists, a controlled stripe case;
- native Clerical Regions plus Realms/Faith/Culture comparisons at fixed zoom;
- disposable before/after saves, fresh-process load, mod-disabled load and
  checks for religious/title gameplay residue, staged only when justified.

Define expected outcomes, receipts/log markers, controls and stop conditions.
Use the existing test playset and preserve prior selection, logs and saves.
CLI assumes the user-declared app state and performs file/log work without
process or GUI checks. Codex GUI configures only an already open launcher.
The user alone launches/exits CK3 and performs every in-game action and visual
observation; Codex never inspects or controls the game window.

## Deliverables and acceptance

- [ ] Evidence-backed input-to-renderer trace, including stripe semantics.
- [x] Capability/constraint matrix for membership, geometry, colors, isolation,
  lifecycle, persistence, compatibility, cost and DLC requirements.
- [x] Separate verdicts for independent provider, synthetic objects and actual
  religious-region mutation, with missing links named explicitly.
- [x] Product-fit verdict for three-category, binary and All Dynasties views.
- [x] Smallest discriminating runtime plan with exact original files needed,
  or a reasoned stop decision if no useful test is supported.
- [x] Canonical task summary and reusable findings updated, with backlog and
  current state synchronized. Mark any runtime-dependent claims unresolved.

Completion means answering feasibility at the evidenced level and recording
remaining gates; a positive result does not mean production readiness or that
R-009/R-010 are complete. No full classifier, palette registry, automatic
refresh system, ADR change, vanilla modification or unrelated research.

## Stage A checkpoint — 2026-10-21

**STOP before Dynasty Map probe preparation on current evidence.** The exposed
mechanisms operate on real clerical geography. Authored history supplies county
sets and real titles supply color inputs, but no independent provider or
arbitrary runtime county-membership writer was identified. A copied mode or
title-color screenshot would not answer that missing contract. This is a
bounded negative result, not proof of engine impossibility. No production route
or ADR change was selected. Self-review only; no runtime or independent review.

Evidence labels below: **VERIFIED** means target-build static API/shipped
usage; **LIKELY** is inference; **UNKNOWN** is unresolved. Paths are game-relative;
generated filenames refer to the existing clean R-004 corpus.

### Input trace and colors

`gui/shared/mapmodes.gui:45–49,1194–1205` and `gui/hud.gui:6231–6233` select
the native key. `gfx/map/map_modes/map_modes.txt:6054–6060` binds native
`color_mode`/`selection = clerical_regions`, county small names and region large
names. **VERIFIED:** configuration/selection, not a new data provider.

**VERIFIED:** real title history binds named geographical regions
(`history/titles/ce3/00_ecclesiastical_titles.txt:682–688,939–944`), with authored
county lists (`map_data/geographical_regions/geographical_region.txt:5922–5926,6011–6015`).
Historical `clerical_region = none` also occurs (`00_ecclesiastical_titles.txt:868–887`);
it is not a documented runtime clear effect.
`map_data/geographical_regions/_geographical_regions.info:3–18` documents
authored lists; its RGB at `:25–27` is for visual-regions mode.
Generated `event_targets.log:890–892` links county/barony title to region title;
`effects.log:11306–11309` iterates member county titles, and
`triggers.log:9977–9980` iterates region titles of a faith.

**VERIFIED:** region-title RGB definitions and shipped copy-color setup
(`common/landed_titles/07_pam_ecclesiastical_titles.txt:563–573,709–719`;
`common/scripted_effects/pam_effects.txt:7071–7088,7992–8004`). Generated
`effects.log:12646–12649,12761–12767` supports title copy and named/RGB writes.
**LIKELY:** title RGB is the ordinary region fill source. **UNKNOWN:** exact
primary/secondary binding, unheld fallback, selection override and invalidation.
This is title mutation, not an independent palette.

The province tooltip follows county -> region -> holder, comparing county Rite
with holder Rite (`common/customizable_localization/pam_custom_loc.txt:413–449`;
`localization/english/gui/map_l_english.yml:125–130`). **VERIFIED:** divergent
tooltip branch; **UNKNOWN:** whether that difference drives stripes. Faith's
county/top-liege Faith stripe description must not be transferred to this mode.
The external stripe premise has no supplied versioned source; this stage did
not fetch external material or establish that premise as current or outdated.

**VERIFIED:** shared graphics consume native province-color textures, with
primary gradients, secondary diagonal stripes and alternate solid overlay
(`gfx/FX/jomini/jomini_province_overlays.fxh:9–26,77–113,122–135`). **UNKNOWN:**
clerical producer conditions/colors and any script upload binding. Seeing the
consumer does not supply a writer. Mode gradient zoom setup is exposed
(`map_modes.txt:6061–6144`), but exact county/barony coverage and selected-region
overrides are untested. Elector/conversion icon zoom defines
(`common/defines/graphic/00_graphics.txt:692–693`) do not define area stripes.

### Capability and constraint matrix

| Capability | Static result and limit |
|---|---|
| Create | **VERIFIED:** province-root `create_clerical_region` block: domicile type, name, optional adj/pre/article, save scope; `effects.log:15316–15336`. Free counties in capital's de-jure kingdom reachable by land; no list/predicate/provider argument documented. |
| Add | **VERIFIED:** title-root `expand_clerical_region = <title>`, `effects.log:11573–11580`: adjacent unassigned target de-jure counties. Cannot steal assigned counties through this effect. Same-kingdom restriction is not stated for expansion. |
| Split / move | **VERIFIED:** character-root `split_clerical_region` with name, optional domicile/adj/pre/article, save scope; `effects.log:10775–10796`. Attempts ruler's realm portion of existing region around capital; not arbitrary selected counties. |
| Merge | **VERIFIED:** title-root `grow_clerical_region_from = <region-title>` takes all counties from adjacent source; `effects.log:11584–11590`. Not per-county reassignment; source-object cleanup details **UNKNOWN**. |
| Transfer | **VERIFIED:** character-root `transfer_to_new_clerical_region = <title>` transfers target title and destroys holder's old region; requires valid target/existing region holder; `effects.log:10940–10947`. |
| Remove / destroy / reset | **VERIFIED:** character-root `destroy_title = <title>` (`effects.log:4093–4095`), used on clerical titles in `events/dlc/pam/pam_clergy_events.txt:751–781,816–825`. No arbitrary per-county remove, empty constructor, independent clear or undo found; exact membership/render cleanup **UNKNOWN**. |
| Read / preflight | **VERIFIED:** size/existence/adjacency (`triggers.log:8447–8452,8551–8557,8650–8658`), create-size (`:10954–10959`). Split-size prose/example says province but Supported Scopes says character (`:7395–7400`); shipped character call at `common/scripted_triggers/pam_scripted_triggers.txt:3327–3332` resolves intended pattern. |
| Geometry / ownership | **VERIFIED:** creation constraints above and authored history lists. Native concept describes cross-realm jurisdiction (`localization/english/dlc/pam/pam_game_concepts_l_english.yml:119`). Arbitrary dynamic disconnected/water-separated groups, cross-faith retention and default bypass **UNKNOWN**; do not generalize creation constraints to all history/operations. |
| Overlap / empty / unheld | Free-only create/add and singular county link verified. Tooltip permits unheld region/no region. Overlap precedence, independent datasets, empty objects, unheld county/empty holding inclusion and all-barony fill **UNKNOWN**; unheld region is not unheld county evidence. |
| Limits | Native concept at `pam_game_concepts_l_english.yml:119` and `common/character_interactions/pam_interactions.txt:10801–10806` describe one region per ruler. Total cap/practical group limit **UNKNOWN**; no borrowing Situation's 255 limit. |
| DLC / religion | Christian doctrine supplies `has_clerical_regions` (`common/religion/doctrine_types/40_doctrines_special.txt:1–9`); request UI has doctrine/PAM gates (`common/character_interactions/01_puppet_interactions.txt:432–439,485–489`); PAM maps to `by_god_alone` (`common/scripted_triggers/00_has_dlc_scripted_triggers.txt:95–97`). Renderer/data/direct-effect availability without DLC **UNKNOWN**; mode definition/sub-button has no separate inspected DLC condition. |
| Refresh / exit / context | Generated MapMode members are metadata/accessors (`data_types_uncategorized.txt:86117–86160`). No provider replacement/invalidate/exit clear contract identified. Fresh PD, player/Dynasty loss, observer/load and manual refresh **UNKNOWN**. Selecting another mode does not undo world state. |
| Persistence / multiplayer | **LIKELY:** title/membership gameplay state is saved/shared. Exact clerical serialization, disabled-mod cleanup and multiplayer locality/sync **UNKNOWN**. R-009 barony RGB serialization is not clerical runtime verification. |
| Cost / compatibility | Shipped split-size/adjacency performance cautions (`pam_scripted_triggers.txt:3292,3327–3332,3513–3518`); timings/native update schedule **UNKNOWN**. Separate names avoid key collision only; shared native dataset, GUI keys, defines/shaders and load behavior need isolation evidence. No recurring scan proposed. |

### Isolation and route/product verdicts

**VERIFIED:** creation wrapper couples the new title to council assignment,
holder changes, Church Situation, fervor, government, opinions and notifications
(`common/scripted_effects/pam_effects.txt:7005–7117`). Those wrapper operations
can be omitted by not calling the wrapper; they are not all proven intrinsic
to `create_clerical_region`. However, holder-change hook can alter capital Rite
and Situation membership (`common/on_action/title_on_actions.txt:3170–3193`),
and mismatch is code-driven (`on_actions.log:3275–3277`;
`common/on_action/dlc/pam/pam_on_actions.txt:529–544`). Native jurisdiction and
clerical appointment candidate sources also exist
(`common/succession_appointment/clerical_christian.txt:1–12`). **UNKNOWN:** all
effects of unheld/custom-domicile objects and whether religious hierarchy,
AI/elections/succession/lists/notifications can be fully omitted. Hidden UI is
insufficient evidence of isolation.

| Route | Verdict |
|---|---|
| Independent provider | **UNKNOWN:** no county-set/palette/provider binding found. New definition key and shared shader do not establish independent storage. |
| Synthetic regions | Creation/history/title RGB exposed; arbitrary dynamic membership and private parallel geography **UNKNOWN**. Real county clerical link/native geography would be involved; no isolated coexistence demonstrated. |
| Actual religious-region mutation | **VERIFIED** as constrained gameplay operations; not selected as architecture. No accepted gameplay/save/compatibility tradeoff. |

Simultaneous DIRECT/CONTROLLED/OTHER, proposed DIRECT/exclusive INDIRECT binary
views, and All Dynasties each lack an established clerical classification input.
Selected region/eligibility is not arbitrary group assignment. Religious
many-group display does not collapse cadet Houses into Dynasties. This does not
invalidate R-009's separate county-selector binary hypothesis; R-009/R-010 remain
partial. No classifier, palette registry or product/ADR change.

### Search limits and next decision

Bounded clerical-token/operation/color searches covered generated effects,
triggers, targets/scopes, on-actions and all five data-type files; relevant
religion/title/geographical/domicile `.info`; native mode/GUI and narrow clerical
creation/split/merge/mismatch callers. Shared shader was checked only at the
known consumer boundary. English stripe descriptions did not reveal an explicit
clerical rule. No arbitrary runtime membership/palette/clear writer found;
absence in this subset does not rule out undocumented/unrelated-name APIs.
Situation add/remove-clerical-realm effects change Situation sub-regions, not
clerical membership. Local report retains the detailed negative-search register.

**STOP:** no useful independent-input experiment is currently specified.
Reopen only on a concrete writer/provider lead or a separately scoped decision
to investigate real religious mutation. If that gate changes, native positive
control plus copied view must precede independent three-set assignment; include
disconnected/water/assigned/unheld controls, county move and empty group, colors,
supported stripe input, active replacement/refresh/re-entry and native-view
comparison. Stop on refusal, shared native mutation, stale fill or gameplay
residue. Only after basic input/isolation passes should disposable save/load,
mod-disabled load, context loss and multiplayer tests be scoped. Reference
originals start with `gfx/map/map_modes/map_modes.txt`, `gui/shared/mapmodes.gui`
and the title/history/geographical/tooltip callers cited above; the essential
new writer is still missing, so an exact runnable payload cannot be specified.
No probe files, installation, runtime, Git staging/commit/push or GitHub writes.

## New-chat entry point

Read AGENTS.md, CURRENT_STATE.md, TASK_HISTORY.md, this issue/task and the
source map. Stage A checkpoint above supersedes the original start instruction;
GUI accepted the matching local R015-CLERICAL-STATIC-20261021-01 checkpoint
after reviewing its report, incremental changes and key source citations.
Keep the STOP decision until a concrete new input lead or separately scoped
religious-mutation investigation exists.
Research stays in the R-015 chat; R-009 remains separate and partial.
No Git staging, commit, push, further GitHub writes,
installation or runtime authorization transfers from creating this issue.

## Official-source follow-up — 2026-10-21

User supplied official-source leads after Stage A review. The official Steam
announcement feed was checked directly: [Dev Diary #8 and 1.20.0 release notes](https://store.steampowered.com/oldnews/?appgroupname=Crusader+Kings+III&appids=1158310&enddate=1793516400&feed=steam_community_announcements). Dev Diary #2 also describes the generic title layer:
[Ecclesiastical Power & Rites](https://store.steampowered.com/news/posts/?appids=1158310&enddate=1778587105&feed=steam_community_announcements).

- **VERIFIED official documentation:** Dev Diary #8 explicitly anticipates
  nonreligious reuse and advertises adding/removing counties plus region
  creation, splitting and merging. This establishes intended moddability,
  not the exact shipped operation signatures or arbitrary disconnected sets.
- **VERIFIED official documentation:** the 1.20.0 release notes describe stripes
  when county Rite differs from region Rite. Stage A's stripe UNKNOWN is now
  narrowed: the intended native rule is documented; exact producer/channel
  binding, script customization and installed-build runtime behavior remain
  unverified. The complete input/stripe acceptance item stays unresolved.
- **Evidence discrepancy:** installed generated effects inspected in Stage A
  expose constrained create/expand/split/merge; no arbitrary county writer was
  identified. The announcement warrants a focused reconciliation of which
  shipped add/remove operation it refers to, not a repeated broad source scan.
- Generic region reuse does not establish a parallel dataset coexisting with
  vanilla, a new provider bound to a custom mode, or arbitrary color/stripe
  callbacks. `color_mode = clerical_regions` was already found by Stage A.
- ADR-009 remains in force. Discovering genuinely generic map/region interfaces
  is relevant; mutation of native religious geography is not approved. No
  carrier probe, implementation, installation or runtime scope is added.

Potential next static question: reconcile the advertised county add/remove
capability with exact target-build interfaces, then determine whether an
independent dataset can reach the native renderer without altering religious
geography. If those links remain absent, document the precise limits. This
follow-up does not establish feasibility or authorize another gameplay carrier.

## Focused API reconciliation — 2026-10-21

Delegation `R015-REGION-API-RECONCILE-20261021-02` completed its bounded static
research; GUI reviewed and accepted the bounded checkpoint. Existing installed 1.20.1.1 sources/generated
APIs reused. No fresh runtime evidence, probe or architecture change.

**Verdict: advertised operation unresolved in corpus.** World-region primitives
exist, but no complete arbitrary county add/remove pair, independent family or
custom-mode dataset binding was identified. Official generic/nonreligious reuse
is positive design evidence; vanilla religious usage alone does not disprove
it. The missing supported ownership/binding links prevent a suitable ADR-009
route, even if the membership discrepancy is subsequently resolved.

| Chain link | Evidence / remaining gap |
|---|---|
| County writer | **VERIFIED static:** `expand_clerical_region = <title>`, region-title root and landed-title target (`effects.log:11573–11580`). Adjacency/unassigned restrictions are in the primitive's documentation. **LIKELY:** a county title can target a single eligible county; type accepts it, but county-tier self-inclusion is untested. **UNKNOWN:** arbitrary remove/reassign or disconnected addition. |
| Coarse membership changes | **VERIFIED static:** realm-portion split, adjacent whole-region merge, holder transfer/old-region destruction (`effects.log:10775–10796,11584–11590,10940–10947`). These do not specify an arbitrary single-county removal API. |
| Independent ownership | **VERIFIED static:** county/barony -> clerical title (`event_targets.log:890–892`), region -> counties (`effects.log:11306–11309`), faith -> region titles (`effects.log:14211–14214`). **LIKELY:** shared native clerical relationship. **UNKNOWN:** independent family for the same county. New title names/domicile parameters do not demonstrate separate storage. |
| Mode binding | **VERIFIED static, reused:** native enums (`gfx/map/map_modes/map_modes.txt:6054–6060`) and MapMode metadata (`data_types_uncategorized.txt:86117–86160`). **UNKNOWN:** independent dataset/provider/context selection. Copying a definition retains the native enum. |
| Colors / lifecycle | **VERIFIED static, reused:** real title RGB/copy writes (`effects.log:12646–12649,12761–12767`). **LIKELY:** ordinary region fill uses title RGB. **UNKNOWN:** exact producer/secondary channel, private palette, replace/refresh/clear and runtime cleanup. |
| Stripes | **VERIFIED official documentation:** county/region Rite mismatch, per the official-source follow-up above. Installed runtime, secondary color source and script-customizable condition remain **UNKNOWN**. No new concrete binding warranted further stripe/shader research. |

The expansion caller uses a duchy target
(`common/scripted_effects/pam_effects.txt:7840–7864,7884–7888`;
`common/character_interactions/01_puppet_interactions.txt:1094–1099`). Wrapper
conditions do not account for all restrictions: adjacency/free-only are already
in the generated effect description. Split is invoked on a secular ruler
(`pam_effects.txt:7933–7955`); merge transfers a whole adjacent region
(`pam_effects.txt:8119–8128`). No supported bypass was identified. Eligible
single-county expansion is a type-compatible candidate, not an arbitrary
membership contract or proof of a successful runtime call.

Generic-looking add/remove operations were checked by root/target:
`add_clerical_realm_to_sub_region`, `add_dejure_title_to_sub_region` and their
remove counterparts operate on `situation_sub_region`, targeting titles
(`effects.log:18236–18248,18415–18427`). Likewise `add_geographical_region` and
`remove_geographical_region` target authored regions from Situation scope
(`effects.log:18252–18256,18431–18435`). They do not write the clerical link.
History assignment remains initialization; geographical-region scope cannot
execute effects/store variables (`event_scopes.log:402–407`). No independent
family declaration was found in the inspected title/geographical-region info.

The bounded search extended Stage A beyond clerical effect names: all generated
effect descriptions for region/jurisdiction/membership and county/province
add/remove/set/assign/reassign/transfer/attach/detach/clear; target/scope docs;
all five data-type files for alternate region writers; relevant title/region
info and narrow expansion/split/merge callers. Remaining generic matches were
Situation membership or unrelated modifiers/capital/faith/location operations.
The ignored reconciliation report retains exact signatures and search limits.
Absence in inspected text is not engine impossibility.

G1 three simultaneous categories and G2 simultaneous Dynasty groups including
cadet Houses remain unsupported by an identified independent input. No binary
reduction or religious carrier is proposed. **STOP before probe preparation.**
Reopen on concrete supported membership, independent-family and mode-binding
interfaces; a county writer alone would not settle the latter two. No new
fixed-county experiment can yet meet those prerequisites. R-009/R-010 remain
partial; no installation, runtime, Git staging/commit/push or GitHub operation.

## Closure assessment after supplied external synthesis — 2026-10-21

**Recommendation: close the investigation direction as not planned, preserving
its partial evidence status; do not claim every original acceptance item passed.**
The issue remains open remotely until closure is explicitly authorized. Current
remote state was checked during this assessment. No implementation or further
task planning is included.

The user supplied an external synthesis of local findings, secondary research
and historical barony-map code. Its Clerical Regions discussion agrees with the
bounded local result: no supported independent dataset or map-to-dataset binding
has been demonstrated. It supplies no exact new county remove/reassign API,
parallel-family declaration or provider binding resolving the remaining gates.
The alleged recent community confirmation of non-overlap has no direct source
in the supplied synthesis; engine-singleton/C++ assertions remain unverified.
Do not promote them into VERIFIED findings.

Historical custom barony-map material concerns a separate architecture, not
proof about Clerical Regions. Public immutable source links supplied include
[historical map definitions](https://github.com/SebastianDanielFrenz/CK3-infrastructure/blob/20252db3e22d621c594a0aa77c8d238531d84f23/gfx/map/map_modes/map_modes.txt)
and [GUI activation](https://github.com/SebastianDanielFrenz/CK3-infrastructure/blob/20252db3e22d621c594a0aa77c8d238531d84f23/gui/shared/mod_gui.txt).
These pages could not be retrieved by the web tool in this assessment and remain
unverified source leads here. Existing project historical findings are reused;
no classifier recovery, alternative implementation or new task is planned.

Closure rationale: Stage A and the focused reconciliation have reached a
reasoned STOP under ADR-009. Further research has no concrete new independent-
input lead. Independent provider remains unestablished; synthetic religious
objects lack demonstrated isolation; actual religious mutations are outside the
accepted architecture. Product input for G1/G2 remains unproven. Intended native
Rite-mismatch stripes are documented, but exact producer/customization,
independent lifecycle and advertised arbitrary add/remove remain unresolved.
The first acceptance checkbox stays open, and runtime was deliberately not run.

This is a scope disposition, not engine impossibility, failed game validation
or proof that an alternative is production-ready. Persistent barony RGB does
not by itself establish save corruption, harmlessness or mandatory restoration;
R-009/R-010 remain partial. Original product goals/ADRs are unchanged. Do not
adopt the attachment's proposed scope reductions or follow-on task instructions.
Reopen only on concrete new API/provider/coexistence evidence. No Git staging,
commit, push, GitHub write, probe, installation or game work was performed.

## Final disposition — 2026-10-21

The user authorized publication, closure as not planned, a scoped commit and
normal push to the existing research branch. Issue #15's body now contains the
distilled findings and its closed/not_planned state was verified. This final
disposition supersedes earlier open/pending-authorization notes in this record.
The first acceptance item remains unresolved; closure is not full technical
completion or proof of engine impossibility. No runtime, new implementation,
product scope reduction or follow-on task was authorized. R-009/R-010 retain
their partial status. Reopen only on concrete independent-input evidence.

<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| codex-auto-review | 110792 | 86912 | 23880 | 494 | 236 | 111286 | partial |
| gpt-6.1-sol | 12569443 | 12106240 | 463203 | 68908 | 6824 | 12638351 | partial |
| **Total** | 12680235 | 12193152 | 487083 | 69402 | 7060 | 12749637 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-22T13:15:22Z. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
Coverage is partial: only explicitly evidenced task turns and linked reviews are allocated; ambiguous usage and missing history are not estimated. Includes attributed research, follow-ups, rejected approaches and closure review. Subsequent R-009 publication is excluded. Not-planned disposition is preserved. This backfill job is assigned to T-002 and excluded from these historical totals. No currency or quota inference.
<!-- ai-cost:end -->