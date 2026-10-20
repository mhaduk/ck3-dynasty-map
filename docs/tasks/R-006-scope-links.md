# R-006 — County, holder, Dynasty, and House scope links

Status: DONE

CK3 build: 1.20.1.1 (Crozier)

Completed: 2026-10-20

## Goal

Verify the formal generated scope transitions needed to compare a county holder with the player's Dynasty.

## Result

Clean generated documentation verifies the relevant title/character/Dynasty/House links. This is a static API result only; it does not verify runtime classification or rendering.

## Verified findings

- `landed_title.holder` transitions to `character`.
- `character.dynasty` transitions to `dynasty`.
- `character.house` transitions to `dynasty_house`, and `dynasty_house.house_dynasty` transitions to `dynasty`.
- County/barony links accept `landed_title` or `province` and return `landed_title`.
- Comparing Dynasty identity supports the accepted cadet-House semantics; runtime classification remains future implementation/test work.

## Unsupported / failed approaches

- Scope signatures do not prove behavior for missing holders, missing Dynasties, or runtime iteration.

## Unknowns

- Runtime classification and edge cases remain gated by R-005/R-007/R-008 and implementation tests.

## Decision

No semantic change. Preserve ADR-001/ADR-002: county is the semantic unit, and compare Dynasty identity before liege traversal.

## Evidence

- [Generated scope links](../RESEARCH.md#formal-scope-links--r-006--r-008)
- GitHub Issue #6.

## Impact

Confirmed the static scope chain used by the architecture; no implementation was authorized.

## Full investigation

GitHub Issue #6 in the public repository.
