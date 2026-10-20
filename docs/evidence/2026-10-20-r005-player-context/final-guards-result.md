# R-005 — FINAL GUARDS checkpoints

Date: 2026-10-20. Target: recorded CK3 1.20.1.1 baseline.
Checkpoint A: passed for the tested ordinary UI path/state transition.
Checkpoint B: fixture rejected by engine; no-Dynasty local-player UI remains
unverified and deferred to [R-013 / #13](https://github.com/mhaduk/ck3-dynasty-map/issues/13).
R-005 remains partial pending consolidation and cleanup; ADR-008 is unchanged.

## A — Missing-player dispatch boundary

User reported and supplied five screenshots: initial PLAYER/UNCHECKED with
disabled activation, CHECK gives READY, one MY DYNASTY TEST produces ACTIVATE
RECEIVED, RESET restores UNCHECKED/WAITING, then global observer shows NO PLAYER
and every action button is absent. The one-shot fixture remains unused.

Captured debug.log contains one CHECK_INSPECT_ENTER/CHECK_HAS_DYNASTY/
CHECK_INSPECT_EXIT sequence (lines 4148–4155), followed by one ACTIVATE_ENTER/
ACTIVATE_EXIT sequence (4156–4162). Both current/root scopes are Kazimierz Piast,
character 52702, historical ID 221520. No further activation/inspection sequence
and no LOWBORN_BEFORE marker occur in the capture after the reported observer
transition. error.log is 17,300 bytes with excluded court-scene locations, no
probe reference; gui_warnings.log is empty. Whole-run capture is retained locally
as checkpoint A and the baseline for B; no exact observer-entry log timestamp
is independently available. Do not claim a clean overall error log.

The positive control ran, and missing-player controls were not dispatchable
through the displayed UI in this tested transition, with no extra effects or
probe-attributed validation error. Accept this as bounded external UI guard
evidence. It does not make direct invalid-root Execute safe or prove atomic
behavior under every possible UI race, MP or programmatic caller.

RESET preceded observer and already cleared availability. This sequence does
not independently prove the nested player's _hide watcher cleared a live READY
cache; do not claim that additional result or repeat A merely to obtain it.
Earlier watcher evidence remains separately bounded. No classification/colors
exist in the logging diagnostic and no restoration claim follows.

## B — Controlled lowborn fixture

The user supplied screenshots showing PLAYER/UNCHECKED, then LOWBORN USED,
then PLAYER/READY after CHECK, and reported no Game Over. The captured log delta
confirms one fixture invocation at 20:13:45. The engine explicitly rejected
`set_to_lowborn` on the player character. LOWBORN_AFTER_HAS_DYNASTY and
LOWBORN_EXIT followed; fresh CHECK at 20:14:19 also reported CHECK_HAS_DYNASTY
with the same current/root character as checkpoint A. No no-Dynasty player
state was created. READY and enabled activation therefore match the retained
Dynasty; this is not evidence of an availability bug or a passed negative test.

Checkpoint B logs were captured as append-only deltas relative to A. error.log
grew by 367 bytes containing the fixture rejection; gui_warnings.log remained
empty. The known rejected fixture is the probe-attributed error for this stage.
Raw logs remain local and ignored. No further activation was observed after B.

Per the user's one-attempt limit, stop fixture experimentation. Follow-up
R-013 / #13 was created and verified open for a supported fixture and actual
no-Dynasty local-player UI evidence. Courtier rejection and NO PLAYER do not
substitute for that evidence. Do not repeat the lowborn fixture or passed cases.
No GitHub changes to R-005 / #5, staging, commit or push were performed.

After B the user confirmed CK3 closed and its launcher open. Codex restored
the original selection in the existing Dynasty Map - GUI Probe playset:
Native Menu Probe enabled, ENTRY diagnostic disabled. Launcher toggle states
and enabled_mods match the saved pre-test selection. Diagnostic files remain
installed but disabled; no save or mod files were deleted. This is launcher
configuration restoration, not evidence of in-game color restoration. All
in-game actions/screenshots are user-provided; Codex analyzed files/logs and
configured only the launcher.
