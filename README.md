# Dynasty Map for Crusader Kings III

**Status:** planning / pre-implementation
**Research baseline:** CK3 1.20.1 "Crozier" (2026-10-20)
**Repository intent:** source code, design documentation, test evidence, and release history for a CK3 mod adding dynasty-focused map modes.

## Product goal

CK3 exposes a House map mode but does not provide a world map that groups cadet Houses by their parent Dynasty. Dynasty Map aims to add two complementary views:

1. **My Dynasty** — shows where the player's dynasty directly holds counties and where it politically controls counties through the de-facto liege hierarchy.
2. **All Dynasties** — groups landed rulers by Dynasty so cadet Houses of the same Dynasty share one map identity/color.

The project deliberately starts with **My Dynasty** because it avoids the hardest unresolved problem: assigning stable, distinct colors to every Dynasty.

## Planned semantics: My Dynasty

- **Direct / dark shade**: the county holder belongs to the player's Dynasty.
- **Controlled / light shade**: the county holder is not in the player's Dynasty, but at least one de-facto liege above that holder is.
- **Other / neutral**: neither the county holder nor any liege above them belongs to the player's Dynasty.

The county is the semantic unit. Baronies, cities and temples inherit the classification of their county so local holding types do not fragment the view.

## Engineering principles

- No compiler or native plugin dependency for the initial implementation; use CK3/Jomini scripting and GUI files.
- No recurring global scan in the MVP. Recompute only when the user activates/refreshes the map mode.
- Avoid persistent caches until profiling proves they are necessary.
- Avoid copying vanilla CK3 files into the public repository.
- Prefix all mod identifiers with `dynmap_` to reduce conflicts.
- Treat current installed CK3 files and generated `script_docs` as the source of truth.
- Do not bump `supported_version` merely to silence launcher warnings; validate first.

## Documentation

- [Project charter](docs/PROJECT_CHARTER.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Algorithms and performance](docs/ALGORITHMS.md)
- [Roadmap](docs/ROADMAP.md)
- [Backlog](docs/BACKLOG.md)
- [Architecture decisions](docs/DECISIONS.md)
- [Research findings](docs/RESEARCH.md)
- [Risk register](docs/RISK_REGISTER.md)
- [Test plan](docs/TEST_PLAN.md)
- [Compatibility policy](docs/COMPATIBILITY.md)
- [Versioning and release process](docs/VERSIONING.md)
- [Second-Mac bootstrap checklist](docs/SECOND_MAC_BOOTSTRAP.md)

## Current release plan

| Version | Theme | Exit criterion |
|---|---|---|
| `0.1.0` | My Dynasty MVP | Correct 3-state county classification and manual refresh |
| `0.2.0` | My Dynasty beta | UI polish, tooltips, profiling, edge-case coverage |
| `0.3.0` | All Dynasties experimental | Cadet Houses grouped by Dynasty with a viable color strategy |
| `0.4.0` | Integrated Dynasty Map | Both modes integrated coherently with CK3 map-mode UI |
| `1.0.0` | Stable public release | Both modes tested, documented, maintainable and release-ready |

See [ROADMAP.md](docs/ROADMAP.md) for details.
