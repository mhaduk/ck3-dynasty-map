# Architecture

## Status

This document defines the intended architecture before access to the target machine's CK3 installation. Anything marked **Research Gate** must be confirmed against the installed CK3 version before implementation. All API names and file paths below are candidates from historical/reference evidence until M0 verifies them from installed vanilla files, generated script_docs or runtime tests.

## Logical components

```mermaid
flowchart LR
    UI[Map mode UI] --> SG[Scripted GUI entry point]
    SG --> C[County classifier]
    C --> R[Barony color renderer]
    P[Local player Dynasty] --> C
    H[County holder + liege hierarchy] --> C
    COL[Dummy color titles / color strategy] --> R
```

### 1. Map mode definition

Expected location:

`gfx/map/map_modes/dynmap_map_modes.txt`

The proposed custom map uses `color_mode = baronies`, following historical community examples; M0 must verify the target-build rendering mechanism.

### 2. Scripted GUI / execution logic

Expected location:

`common/scripted_guis/dynmap_map_modes.txt`

Responsibilities:

- determine the current local player's Dynasty;
- execute a static refresh on valid activation/manual request;
- classify counties;
- apply colors to the county's baronies;
- fail safely if no local player or no Dynasty exists, starting in v0.1; v0.2 adds UX hardening and regression coverage.

Under ADR-008, My Dynasty is unavailable if there is no valid local player or the local player has no valid Dynasty. Activation in that state must perform no classification or color writes. An all-neutral map is not a substitute for unavailability.

If context becomes invalid while the mode is active, stop using the old Dynasty context and clear/restore visual state as far as the CK3 map-mode API permits. M0 must determine how to disable/hide the UI and detect context invalidation safely, including what cleanup/restore the API supports. Cleanup is distinct from unavailable activation and may require restoration writes; it must not classify against stale context.

### 3. Color sources

Expected location:

`common/landed_titles/dynmap_colors.txt`

For My Dynasty, use a small set of non-creatable dummy landed titles as color sources:

- `d_dynmap_direct`
- `d_dynmap_controlled`
- `d_dynmap_other`

Exact RGB values are intentionally deferred until in-game testing because lighting/terrain blending affects perceived contrast.

### 4. GUI integration

**Research Gate RG-UI-01**: inspect CK3 1.20.x/1.21.x vanilla `map_modes.txt` and the current map-mode GUI. The public custom-map-mode guide was last verified against a very old CK3 version, while the recorded patch references report sub-map-mode display changes in CK3 1.20. Verify the installed behavior during M0, including unavailable UI, re-click/manual refresh and exit/restore hooks.

Preferred order:

1. data-driven/additive integration without replacing a large vanilla GUI file;
2. minimal scoped GUI override;
3. if neither approach is viable, record RG-UI-01 as blocked and document the evidence before revisiting the design.

ADR-006 prohibits vanilla files in Git. A full `mapmodes.gui` copy is therefore not an authorized fallback. Do not copy or modify vanilla files; inspect them read-only. Any future proposal to change this policy requires an explicit ADR revision and authorization before proceeding.

## Domain model

### Entity relationships relevant to My Dynasty

```mermaid
flowchart BT
    B[Barony] --> C[County]
    C --> H[County holder]
    H --> D[Holder Dynasty]
    H --> L1[Liege]
    L1 --> L2[Liege above]
    L2 --> TL[Top liege]
```

The design models the ordinary de-facto political hierarchy as a rooted forest with one liege per ruler. M0 must confirm the applicable scopes and government behavior. Historical references describe `any_liege_or_above`; prefer verified engine traversal over materializing a graph.

## My Dynasty classification

Let `PD` be the valid local player's Dynasty and `H` the county holder. This is conceptual pseudocode, not verified CK3 syntax.

```text
if local player or PD is invalid:
    mode unavailable; return without classification or color writes
else if H exists and H has a valid Dynasty and H.dynasty == PD:
    DIRECT
else if H exists and a qualifying de-facto liege has dynasty == PD:
    CONTROLLED
else:
    OTHER
```

Important semantics:

- cadet Houses automatically collapse because comparison is on `dynasty`;
- county holder controls classification, not barony holder;
- a holder without a Dynasty cannot be DIRECT, but can be CONTROLLED through a qualifying liege; check the chain before assigning OTHER;
- occupations do not change classification in v1.0;
- tributary/suzerain relations do not count as lieges in v1.0;
- regents/co-rulers do not replace the legal title holder for classification.

## State management

### Principle: avoid persistent state in MVP

Older custom map-mode examples multiplex one renderer using global variables. That creates save-state, observer-mode and multiplayer concerns. For the first implementation, prefer one named map-mode definition per logical mode and derive button state from `IsMapMode(...)` if CK3 1.20+ allows it.

Do not introduce persistent cache variables unless profiling demonstrates a measurable need.

## Refresh model

### v0.1–v0.2: static/on-demand

- valid activation executes a full classification/color pass;
- v0.1 requires a dependable refresh path: re-click only if verified by M0; otherwise use the smallest explicit refresh mechanism needed;
- revalidate local player/Dynasty on activation and refresh; never reuse stale context;
- invalid context while active stops old-context use and triggers API-supported clear/restore; verify lifecycle hooks during M0 without recurring world scans;
- no daily/monthly pulse or title-change listeners for world recomputation; minimal context-safety lifecycle handling is required;
- exiting restores normal map visuals as supported and verified against the target API.

### Post-0.2 options

Only after profiling and correctness testing:

- event-driven invalidation/refresh on title-holder or vassal-hierarchy changes;
- limited periodic refresh while the mode is visible.

Incremental caching is deliberately postponed because invalidation is harder than recomputation for a shallow hierarchy.

## All Dynasties architecture

All Dynasties remains behind a research gate.

Desired logical key:

`territorial ruler -> House -> Dynasty -> shared color`

Candidate color strategies, in preferred research order:

1. **Reuse native House-map internals** if CK3 exposes a grouping/color hook.
2. **Dynasty-head primary-title color** as a stable-enough source for all counties of the Dynasty.
3. **Main/founding House-derived color** if exposed by current GUI/script APIs.
4. **Deterministic palette allocation** only if a stable Dynasty identity can be mapped without persistent save-state.
5. Persistent color registry as a last resort.

No All Dynasties implementation should be merged until the color strategy has explicit stability, collision and save-state behavior documented.

## Naming conventions

- All custom script IDs: `dynmap_*`
- All localization keys: `dynmap_*`
- All dummy titles: `d_dynmap_*`
- Future event namespace: `dynmap`
- Files owned by this project should start with `dynmap_` where CK3 loading rules permit it.
