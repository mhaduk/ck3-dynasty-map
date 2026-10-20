# R-003 — Map-mode GUI inspection

Status: DONE

CK3 build: 1.20.1.1 (Crozier)

Completed: 2026-10-20

## Goal

Inspect installed map-mode GUI structure and generated GUI/API bindings for activation, availability, refresh, and exit research.

## Result

Static inspection identified native map-mode menu structures and candidate UI bindings. It did not establish that a mod can add a control safely, that a mode can be hidden/disabled for an unavailable player, or that activation/exit lifecycle behavior is supported.

## Verified findings

- Installed GUI contains native named map-mode blocks and explicit Faith sub-mode buttons.
- Generated GUI type documentation exposes relevant map-mode/player APIs, but API presence alone does not prove a safe player/Dynasty guard.
- The research gates for integration, availability, refresh, and cleanup remained open after this static task.

## Unsupported / failed approaches

- Static bindings alone cannot be treated as runtime integration or lifecycle proof.

## Unknowns

- Additive insertion and complete native-menu behavior; unavailable UI; refresh and cleanup.

## Decision

No integration strategy was selected by R-003. R-010 owns runtime integration research.

## Evidence

- [R-003 findings](../RESEARCH.md#verified--r-003-installed-gui-bindings-2026-10-20)
- Installed GUI and generated type references are summarized in RESEARCH.md; vanilla sources remain local and are not copied here.
- GitHub Issue #3.

## Impact

Defined candidate extension points and handed unresolved runtime gates to R-005/R-010.

## Full investigation

GitHub Issue #3 in the public repository.
