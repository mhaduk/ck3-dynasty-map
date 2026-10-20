# Research Findings

**Research date:** 2026-10-20
**Reported public CK3 release at research time (reference baseline, not installed-build verification):** 1.20.1 "Crozier" (2026-10-13). Paradox stated that subsequent changes were being targeted at the forthcoming 1.21 update, so the implementation target must be re-checked on the gaming Mac before coding.

## Evidence policy and target-build status

Community documentation, Workshop descriptions and archived repositories are
historical/reference evidence only. They suggest research probes; they do not
verify API behavior for the target CK3 build. No target-build API verification
has been recorded yet. M0 must confirm behavior from installed vanilla files,
generated script_docs or runtime testing before implementation relies on it.

For each verified finding, record the exact CK3 build, date, probe/backlog ID,
local file/API entry or runtime procedure, observed result and limitations.
Keep raw generated dumps local; record original findings here. Distinguish
reference claims, design assumptions and target-build observations.

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

Historical script references describe `any_liege_or_above` as iterating lieges above a character while skipping the character itself. M0 must inspect installed vanilla/generated script_docs and test the required scopes; current target-build use has not been verified.

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
