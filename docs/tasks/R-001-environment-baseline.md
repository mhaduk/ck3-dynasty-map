# R-001 — Environment baseline

Status: DONE

CK3 build: 1.20.1.1 (Crozier)

Completed: 2026-10-20

## Goal

Record the installed CK3 version and establish the environment baseline for M0 research.

## Result

The project recorded CK3 1.20.1.1 as its target research baseline. The finding establishes which installed files and generated API documentation the subsequent M0 research refers to. It does not establish compatibility with later builds or complete vanilla runtime cleanliness.

## Verified findings

- The recorded target build is CK3 1.20.1.1 (Crozier).
- Clean API documentation was later generated for this baseline under R-004.
- A clean startup-only vanilla observation does not complete the save/map interaction baseline; R-011 remains partial.

## Unsupported / failed approaches

- None recorded as part of the completed inventory.

## Unknowns

- Compatibility with newer CK3 builds must be researched when the target changes.
- Full vanilla save/map-mode log baseline remains R-011.

## Decision

Use the installed target build and generated API documentation as evidence; do not treat historical examples as target-build verification.

## Evidence

- [Research baseline and clean vanilla follow-up](../RESEARCH.md#r-001--environment-inventory-complete-2026-10-20)
- [Backlog R-001 / Issue #1](../BACKLOG.md)

## Impact

Unblocked target-build-specific inspection and API generation. R-011 remains a separate runtime-baseline task.

## Full investigation

GitHub Issue #1 in the public repository; its investigation history is authoritative for intermediate updates.
