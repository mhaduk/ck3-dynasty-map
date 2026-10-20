# Roadmap

The mod uses Semantic Versioning. Versions below `1.0.0` are intentionally experimental; minor versions may change implementation details while preserving the stated product direction.

## M0 — Research & local bootstrap (no release)

**Purpose:** lock implementation to the actual installed CK3 build.

Exit criteria:

- exact CK3 version recorded;
- current vanilla map-mode definitions inspected;
- current map-mode GUI/sub-mode mechanism understood;
- `script_docs` and `dump_data_types` generated locally;
- My Dynasty PoC path confirmed;
- GUI integration strategy selected, including unavailable UI, context invalidation/restore and verified re-click or minimal explicit refresh;
- no copyrighted vanilla game files committed to Git.

## v0.1.0 — My Dynasty MVP

Scope:

- custom My Dynasty map mode;
- county-level semantics;
- `DIRECT`, `CONTROLLED`, `OTHER` rendering;
- static refresh on activation;
- unavailable without a valid local player or valid player Dynasty; no classification/color writes on unavailable activation and no all-neutral substitute (ADR-008);
- stop old-Dynasty use on active-context invalidation and clear/restore visuals as far as the API permits;
- dependable manual refresh: M0-verified re-click or the smallest explicit refresh mechanism needed;
- English localization;
- minimal icon/UI integration using the least invasive mechanism supported by the target CK3 build;
- basic `error.log` cleanliness.

Explicitly deferred:

- live refresh;
- All Dynasties;
- multiplayer support;
- total conversion compatibility.

Release gate:

- direct/cadet-branch county tests pass;
- nested liege test passes;
- minimum smoke/regression coverage proves safe activation, three-state classification (including no-Dynasty holders under dynastic lieges), rendering, refresh/re-activation, exit/restore and unavailable-state behavior per TEST_PLAN.md;
- absent local-player/Dynasty activation does no classification/color writes; active-context loss stops old-context use with API-supported visual cleanup;
- no recurring scan when inactive;
- no mod-caused script errors in core test save.

## v0.2.0 — My Dynasty beta / hardening

Scope:

- tooltip/legend explaining shades;
- optional Polish localization;
- observer/no-dynasty UX hardening and regression coverage beyond the v0.1 safety guards;
- save/load and add/remove-mid-save tests;
- administrative/clan/tribal edge-case coverage;
- Script Profiler baseline;
- color/contrast tuning;
- compatibility documentation for map-UI mods;
- refine the dependable refresh UX already required in v0.1.

Release gate:

- performance results documented;
- no known P0/P1 correctness bug;
- compatibility behavior reproducible;
- known pre-1.0 removal limitations documented; safe removal remains desirable.

## v0.3.0 — All Dynasties experimental

Scope:

- implementation of a selected dynasty color strategy;
- cadet Houses collapse to one Dynasty identity;
- no-Dynasty/lowborn fallback;
- static refresh;
- experimental label if color stability is not yet guaranteed.

Research gate before implementation:

- inspect native House map internals;
- determine whether native House colors can be grouped/reused;
- otherwise benchmark dynasty-head-title and palette alternatives.

Release gate:

- a Dynasty keeps one color across all its cadet Houses within one refresh;
- color assignment behavior is documented and predictable;
- no persistent registry unless approved by ADR.

## v0.4.0 — Integrated Dynasty Map

Scope:

- coherent `Dynasty` UI with `All Dynasties` and `My Dynasty` as sub-modes if CK3 API supports it;
- consistent tooltips/legend;
- manual refresh UX;
- final compatibility strategy for vanilla map-menu changes;
- regression suite for both modes.

## v1.0.0 — Stable public release

Scope:

- both map modes production-ready;
- README installation/user documentation;
- Workshop-ready metadata and image assets;
- clean release checklist;
- safe removal or a clearly proven harmless removal path;
- compatibility matrix for current CK3 minor release;
- documented upgrade path after CK3 patches.

## Post-1.0 candidates

Not committed:

- select/click a Dynasty and isolate its lands;
- optional realm-vs-direct shade schemes;
- event-driven refresh while visible;
- extra dynasty relationships (tributaries, ceremonial/subject mechanics);
- total-conversion compatibility packs.
