# Project Charter

## Problem

CK3's House map mode distinguishes individual Houses. Cadet branches therefore fragment a Dynasty into unrelated colors, making it difficult to visualize dynastic expansion. Players also lack a concise view showing the difference between land directly held by members of their Dynasty and land politically subordinate to dynastic rulers.

## Goals

### G1 — My Dynasty
Provide one Dynasty map family with **Dynasty Realms** (default), **Dynasty
Holdings** and **My Realm & Dynasty**. Each classifies counties into dark,
light and neutral categories under ADR-010. Holdings retains the original
DIRECT/CONTROLLED/OTHER rule; the other views distinguish dynastic highest
rulers and the player's own subtree. Exact definitions and appearance are in
[F-003](tasks/F-003-dynasty-subview-definitions.md). Research feasibility is
bounded; production safety and visual acceptance remain release requirements.

### G2 — All Dynasties
Provide a world map that preserves the useful territorial semantics of the House map while grouping cadet Houses by their parent Dynasty.

### G3 — Native-feeling UX
Integrate with CK3's existing map-mode UI. On CK3 1.20+, prefer the new sub-map-mode model if it is accessible to mods without fragile GUI replacement.

### G4 — Low runtime cost
The mod must have zero or negligible steady-state script cost when the map is not being refreshed. Expensive work must be user-driven unless later profiling justifies event-driven refresh.

### G5 — Maintainability
A CK3 patch must be reviewable through a documented compatibility checklist rather than trial-and-error edits.

## Non-goals for 1.0

- Replacing CK3's physical/province map.
- Modeling baron-level dynastic control as a separate semantic layer.
- Occupation overlays during war.
- Tributary/suzerain relationships as dynasty control.
- Multiplayer support unless explicitly validated.
- Compatibility patches for total conversions such as AGOT.
- Persistent dynasty color databases unless unavoidable.

## Success criteria for 1.0

- Both map modes are accessible from the standard map-mode UI.
- Cadet Houses compare by Dynasty identity, not House identity.
- My Dynasty semantics are correct across tested feudal, clan, tribal and administrative hierarchies.
- No recurring global scans while the map is inactive.
- No mod-caused errors in `error.log` during the test matrix.
- Performance measured with CK3 Script Profiler and documented.
- Safe behavior is documented for existing saves and mod removal.
- Compatibility limits with other map-UI mods are explicit.
