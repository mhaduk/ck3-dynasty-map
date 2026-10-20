# Project Charter

## Problem

CK3's House map mode distinguishes individual Houses. Cadet branches therefore fragment a Dynasty into unrelated colors, making it difficult to visualize dynastic expansion. Players also lack a concise view showing the difference between land directly held by members of their Dynasty and land politically subordinate to dynastic rulers.

## Goals

### G1 — My Dynasty
Provide a map mode that classifies every landed county into three states relative to the local player:

1. `DIRECT`: county holder belongs to the player's Dynasty.
2. `CONTROLLED`: holder does not belong to the player's Dynasty, but one or more de-facto lieges do.
3. `OTHER`: no holder/liege in the de-facto chain belongs to the player's Dynasty.

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
