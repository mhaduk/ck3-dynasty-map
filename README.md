# Dynasty Map for Crusader Kings III

**Status:** research prototype; R-016 complete with limits, no production release
**Target:** CK3 1.20.1.2 "Crozier" / Steam build 26046173 (2026-10-21; bounded prototype startup/runtime smoke). Clean original API baseline: 1.20.1.1.
**Repository intent:** source code, design documentation, test evidence, and release history for a CK3 mod adding dynasty-focused map modes.

## Product goal

CK3 exposes a House map mode but does not provide a world map that groups cadet Houses by their parent Dynasty. Dynasty Map aims to add two complementary views:

1. **My Dynasty** — shows where the player's dynasty directly holds counties and where it politically controls counties through the de-facto liege hierarchy.
2. **All Dynasties** — groups landed rulers by Dynasty so cadet Houses of the same Dynasty share one map identity/color.

The project deliberately starts with **My Dynasty** because it avoids the hardest unresolved problem: assigning stable, distinct colors to every Dynasty.

## Accepted My Dynasty subviews

One **Dynasty** map entry offers three subviews. Dark wins over light;
nonmatching county land should be grey.

| Subview | Dark | Otherwise light |
|---|---|---|
| **Dynasty Realms** (default) | Highest de-facto ruler is in the player's Dynasty | Holder or any senior is in that Dynasty |
| **Dynasty Holdings** | County holder is in the player's Dynasty | Any de-facto senior is in that Dynasty |
| **My Realm & Dynasty** | Player holds the county or is a senior in its chain | Holder or any senior is in the player's Dynasty |

The county is the semantic unit; constituent baronies inherit its category.
Cadet Houses share Dynasty identity. Invalid player/Dynasty means unavailable
with no writes. See [F-003](docs/tasks/F-003-dynasty-subview-definitions.md) for
the exact definitions, appearance, examples and legend contract.

R-016 demonstrated the pipeline and bounded UI smoke, not release readiness.
Grey neutral ground failed visual acceptance. Complete semantic coverage,
context safety, shared title-color restoration and save/removal remain open.
R-017 plans better test fixtures; F-001 owns final UI/grey/contrast; F-002 owns
color-source feasibility. All Dynasties remains deferred.

## Engineering principles

- No compiler or native plugin dependency for the initial implementation; use CK3/Jomini scripting and GUI files.
- No recurring global scan in the MVP. Recompute only when the user activates/refreshes the map mode.
- Avoid persistent caches until profiling proves they are necessary.
- Avoid copying vanilla CK3 files into the public repository.
- Prefix all mod identifiers with `dynmap_` to reduce conflicts.
- Treat current installed CK3 files and generated `script_docs` as the source of truth.
- Do not bump `supported_version` merely to silence launcher warnings; validate first.

## Documentation

- [Current state / Codex session handoff](docs/CURRENT_STATE.md)
- [Completed task history](docs/TASK_HISTORY.md)
- [Subview definitions and appearance (F-003)](docs/tasks/F-003-dynasty-subview-definitions.md)
- [Codex workflow](docs/CODEX_WORKFLOW.md)
- [Implementation review](docs/IMPLEMENTATION_REVIEW.md)

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
