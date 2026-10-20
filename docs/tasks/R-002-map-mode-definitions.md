# R-002 — Installed map-mode definitions

Status: DONE

CK3 build: 1.20.1.1 (Crozier)

Completed: 2026-10-20

## Goal

Inspect the installed vanilla map-mode definitions relevant to a barony-color mode.

## Result

The native `baronies` map mode uses `color_mode = baronies`. This confirms the native definition structure inspected for this build, not custom file loading, custom selection, or safe temporary rendering.

## Verified findings

- The installed map-mode definitions include named map-mode objects and a native baronies renderer.
- Format documentation supports the inspected definition structure.
- Custom map-mode loading and runtime rendering remain unverified and are tracked by R-009/R-010.

## Unsupported / failed approaches

- No custom mode was validated by this static inspection.

## Unknowns

- Whether the proposed custom definition loads from a separate file and renders safely.

## Decision

Keep custom loading and renderer behavior behind the existing research gates; no architecture change resulted.

## Evidence

- [R-002 findings](../RESEARCH.md#verified--r-002-installed-map-mode-definitions-2026-10-20)
- Installed vanilla reference summarized there: `game/gfx/map/map_modes/map_modes.txt`, native `baronies` object.
- GitHub Issue #2.

## Impact

Informed the candidate map-mode definition in ARCHITECTURE.md; no implementation authorized.

## Full investigation

GitHub Issue #2 in the public repository.
