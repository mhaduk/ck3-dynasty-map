# Compatibility Policy

## Supported game versions

The installed M0 research target is CK3 1.20.1.1 (Crozier), Steam build 25913294,
confirmed on 2026-10-20. This is not a runtime compatibility declaration: the
initial logs/script_docs came from a session with NUI:Realm Ledger enabled.
Clean vanilla API docs were regenerated and rechecked on 2026-10-20; startup
error.log is empty. Save/map-mode baseline coverage and runtime probes remain
pending (see RESEARCH.md, clean follow-up). Reconfirm
the installed build after updates. `supported_version` is updated only after
the release checklist passes.

Prefer a minor-series wildcard only after validation, for example:

`supported_version="1.20.*"`

Do not change this field merely to remove launcher warnings. Treat it as a support declaration, not proof of compatibility; record the exact builds actually tested.

## Save compatibility

Target for v1.0:

- safe to add to an existing save;
- safe to update between patch releases of the mod;
- safe to remove, or a clearly proven harmless removal path.

During v0.x, safe removal is desirable; known removal limitations may be documented
for pre-1.0 releases. Record affected builds, observed state and any tested removal
procedure. Do not claim removal safety without evidence. For v1.0, safe removal or
a clearly proven harmless removal path is mandatory; documenting a harmful or
unknown outcome alone does not pass the gate. Color-state persistence and effects
on other map modes must be tested.

v0.1 requires minimum smoke/regression coverage for activation, classification,
rendering, dependable refresh, exit/restore and unavailable-state behavior.
v0.2 adds deeper save/load, removal, profiling and compatibility coverage.
See TEST_PLAN.md and VERSIONING.md for milestone gates.

Ironman/achievement compatibility remains unknown until verified; do not advertise
support based solely on the mod's intended visual scope.

## Other mods

### Expected low-risk overlap

- mods that do not touch map-mode definitions or map-mode GUI;
- character/event/content mods unrelated to map rendering.

### Expected conflict hotspots

- `gfx/map/map_modes/map_modes.txt` or equivalent definitions;
- current CK3 map-mode GUI files;
- mods that replace the same named map-mode object;
- map-mode button/menu overhauls.

If CK3 permits additive files for map definitions, use unique `dynmap_*` IDs to minimize conflicts. Use original mod files for any minimal scoped GUI override. If research finds that GUI insertion requires copying a vanilla file, treat RG-UI-01 as blocked under ADR-006 and document the limitation; a copy is not an authorized fallback. Consider compatibility patches only after 1.0.

## Total conversions

Not supported by default for 1.0. They may replace map dimensions, landed-title structures, GUI, map-mode definitions or government semantics. Compatibility packs should be separate deliverables.

## Multiplayer

Unsupported until tested. Old custom map mods report observer/global-variable and multiplayer uncertainty. Multiplayer support requires a dedicated test with identical mods/load order on all clients and explicit desync checks.
