# Current State

Updated 2026-10-21. Primary operational handoff; detailed findings remain in their canonical documents.

## Environment / Project Context

- Target baseline: CK3 1.20.1.1 (Crozier); current branch: `research/native-menu-alternative`.
- Milestone: M0 research/bootstrap. No production mod or classifier has been implemented.
- This checkpoint contains R-005 and R-010 research/probe work. Preserve unrelated local evidence and excluded materials; do not reset or overwrite them.

## Current Task

- **R-009 — Barony color side effects, map isolation and exit/restore** ([Issue #9](https://github.com/mhaduk/ck3-dynasty-map/issues/9)).
- **Status:** Partial / active; first user-run batch, native-color data trace and static Situation feasibility checkpoint consolidated in the [R-009 checkpoint](tasks/R-009-barony-color-safety.md). Native/custom barony writes share state and serialize title RGB. Situation county-key add/remove and independent region RGB have installed usage/contracts; renderer coverage, isolated view binding and safe lifecycle/removal remain unverified.
- **Next action:** review the prepared R-009 publication package, then execute R-014 / #14 in a separate chat. R-009 remains partial/open and resumes after R-014 with the source map as a guide to renderer leads. Do not prepare another Situation probe now. Persistent state is not categorically prohibited; the concern is repurposing unrelated titles/Situations as fragile map workarounds. No production strategy selected and no ADR rewritten. Publication preparation made no staging/commit/push or GitHub writes.
- **Scope:** first-launch batch completed and prior enabled selection restored; R009 remains installed but disabled. User authorized the reviewed single checkpoint commit, normal push to the existing research branch and #9 body replacement with the issue kept open. Publication is pending execution at this checkpoint. No other GitHub writes or new runtime stage; mod-disabled/fresh-process observation remains a separate future scope.
- **App state:** user reports CK3 closed and launcher reopened. GUI restored prior enabled selection and verified launcher UI plus enabled-mod manifest; no Codex game UI inspection/control. Saves and raw evidence preserved.

## Previous R-005 checkpoint

- **R-005 — Player context, validity guards, and context-loss handling** ([Issue #5](https://github.com/mhaduk/ck3-dynasty-map/issues/5)).
- **Goal:** establish safe local-player/Dynasty entry and context-loss behavior for ADR-008.
- **Status:** Partial / active.
- **Current checkpoint:** [FINAL GUARDS](evidence/2026-10-20-r005-player-context/final-guards-result.md) A passed for the tested displayed UI path into observer; B's one-shot `set_to_lowborn` fixture was rejected on the player character, so no-Dynasty local-player UI remains unverified and is deferred to [R-013 / #13](https://github.com/mhaduk/ck3-dynasty-map/issues/13). The consolidated [R-005 checkpoint](tasks/R-005-player-context.md) was reviewed and accepted as a partial checkpoint. Do not run more fixtures or repeat passed cases.
- **Handoff:** the R-005 publication is recorded locally; current branch history includes its checkpoint at `c14a06f`. No additional R-005 runtime tests are requested. R-009 has started in its own chat with context collection and batch preparation. R-010 remains separate for native-menu parity/refresh. The user closed CK3 and opened the launcher; Codex restored the prior selection in the existing Dynasty Map - GUI Probe playset (Native Menu Probe on, ENTRY diagnostic off), confirmed by launcher UI and enabled_mods. The diagnostic remains installed but disabled.
- **Blockers/open questions:** A is bounded external UI evidence, not direct invalid-root safety or proof against every transition race; no-Dynasty local-player UI is unverified. Do not invoke the known NULL diagnostic again. Do not repeat passed switch, succession, observer or activation-after-load cases.
- **Runtime state / permission:** final results are user-led; the final checkpoint includes fixture rejection in error.log. Earlier whole-run logs contain excluded court-scene errors. Do not claim clean overall logs. User reported game exit; prior playset selection was restored and verified. Diagnostic files remain installed but disabled; no files or saves were deleted. Preserve saves and evidence.
- **App ownership:** CLI runs ready file/code/install/log tasks without waiting for user actions. Codex GUI owns code coordination, launcher/mod configuration, instructions and log analysis; it must not inspect, screenshot or control the CK3 game UI. The user alone opens launcher/game through Steam and performs all in-game loading, saving, character/observer changes and diagnostic clicks. Reuse the existing test playset.
- **Fallback / GitHub permission:** the one-attempt fixture failed and the authorized follow-up R-013 / #13 was created and verified open. The user explicitly authorized the reviewed two-commit package, normal push to the existing research branch, replacement of the #5 body and a #10 status comment. #13 needs no additional write; no issue closure, merge to main or new runtime work is authorized by this publication. #5 remains open. A failed fixture is not a passed no-Dynasty UI test; A is bounded external UI guard evidence, not direct invalid-root safety. ADR-008 is unchanged.
- **Recommended model:** Sol / High if the entry-contract research requires difficult engine reasoning; otherwise Luna / Medium for bounded documentation/maintenance.

## Next Up

1. **R-014** — inventory CK3 documentation/source hierarchy and integrate the concise source map in a separate chat.
2. **R-009** — resume renderer-input and lifecycle research after R-014; no probe is prepared or authorized by this checkpoint.
3. **R-010** — complete native-menu parity, availability, refresh, and lifecycle checks.
4. **R-007 / R-008** — runtime-check liege traversal and county-to-de-jure-barony behavior.
5. **R-011 / R-012** — complete vanilla baseline and CK3 Tiger setup/validation prerequisites.

## Last Completed

- **R-006** — generated target-build scope links for county/barony, holder, Dynasty, and House verified; no runtime claim. See [task history](TASK_HISTORY.md) and [RESEARCH.md](RESEARCH.md).

## Relevant Verified Baseline

- Clean generated CK3 1.20.1.1 API docs verify key scope links and iterator/effect signatures; they do not prove runtime rendering or lifecycle safety.
- Runtime diagnostics verify fresh player/Dynasty context on tested activation, switch, succession, and observer return; the player-change hook did not cover tested observer/load transitions.
- The GUI observer watcher cleared its GUI-local marker on tested loss of player validity. It does not restore title colors or prove save/load reset behavior.
- Direct character-scoped Execute with a null root logged an invalid-character validation error before the effect ran, including after a conditional-root guard attempt.
- R-010 probe 02 has startup, native-menu placement, basic interaction, and Faith sub-mode smoke evidence. Full parity, availability, refresh, and cleanup remain open.

## Active Blockers

- R-005 / RG-PLAYER-01: no-Dynasty local-player UI deferred to R-013; safe direct invalid-root behavior remains unproven despite bounded external UI evidence for A.
- R-009 / RG-STATE-01: supported view-specific color input and safe exit/removal behavior.
- R-010 / RG-UI-01: complete native-menu behavior and dependable refresh.

## Relevant Unresolved Questions

- Does a supported rootless entry or UI guard prevent dispatch into character-scoped validation when there is no local player?
- Which target-build cleanup mechanism restores map visuals without a recurring scan or stale Dynasty context?
- Can the native submenu maintain required vanilla control visibility/behavior while providing unavailable state and refresh?

See [BACKLOG.md](BACKLOG.md) for all tasks and dependencies, [RESEARCH.md](RESEARCH.md) for technical evidence, and [CODEX_WORKFLOW.md](CODEX_WORKFLOW.md) for operating procedures.
