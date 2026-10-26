# Dynasty Map for Crusader Kings III

**Status:** development build; no public beta has been released
**Target:** CK3 1.20.1.2 "Crozier" / Steam build 26046173 (2026-10-21; bounded prototype startup/runtime smoke). Clean original API baseline: 1.20.1.1.
**Repository intent:** source code, design documentation, test evidence, and release history for a CK3 mod adding dynasty-focused map modes.

## Product goal

CK3 provides a native House map view. Dynasty Map adds three Dynasty-focused views and groups cadet Houses through shared Dynasty identity:

1. **Dynasty Realms** — where the Dynasty rules independently or through the de-facto hierarchy.
2. **Dynasty Holdings** — counties held by Dynasty members directly, and foreign counties held by someone below a Dynasty member in the de-facto liege chain.
3. **My Realm & Dynasty** — the player's de-facto subtree and the wider Dynasty.

The county is the semantic unit and its baronies inherit the result. See [F-003](docs/tasks/F-003-dynasty-subview-definitions.md) for exact definitions.

The bounded target is CK3 1.20.1.2 / Steam build 26046173; this is not a broad support claim. No public beta or Workshop release is available. Shared color restoration, save/removal behavior, context safety and complete compatibility remain unresolved.

Player documentation: [GitHub Wiki](https://github.com/mhaduk/ck3-dynasty-map/wiki).

## Engineering principles

- No compiler or native plugin dependency for the initial implementation; use CK3/Jomini scripting and GUI files.
- No recurring global scan in the MVP. Recompute on activation or when the user clicks the active view button again; do not run a recurring global scan.
- Avoid persistent caches until profiling proves they are necessary.
- Avoid copying vanilla CK3 files into the public repository.
- Prefix all mod identifiers with `dynmap_` to reduce conflicts.
- Treat current installed CK3 files and generated `script_docs` as the source of truth.
- Do not bump `supported_version` merely to silence launcher warnings; validate first.

## Documentation

- [Current state / Codex session handoff](docs/CURRENT_STATE.md)
- [Completed task history](docs/TASK_HISTORY.md)
- [Subview definitions and semantics (F-003)](docs/tasks/F-003-dynasty-subview-definitions.md)
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
- [Local DEV and production variants](docs/LOCAL_MOD_VARIANTS.md)

## Release status

No public beta has been released. Release readiness and supported-version declarations follow [VERSIONING.md](docs/VERSIONING.md) and the current release-gate owner; the historical milestone roadmap remains internal planning context.
