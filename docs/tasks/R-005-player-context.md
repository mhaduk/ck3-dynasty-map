# R-005 — Player context and unavailable-state checkpoint

**Status: Partial / open.** Target: CK3 1.20.1.1 (Crozier), Steam build 25913294. This checkpoint consolidates evidence for R-005 / GitHub #5; it does not close the issue, waive ADR-008 or establish production readiness. See the [R-005 evidence index](../evidence/2026-10-20-r005-player-context/README.md) and [consolidated research](../RESEARCH.md#r-005--consolidated-status-2026-10-20).

## Result by gate

### RG-PLAYER-01 A — absent-player UI path

**Passed for the tested displayed path/state transition.** The FINAL GUARDS diagnostic first passed a healthy-player CHECK and activation positive control. After RESET, the user entered global observer. The panel showed NO PLAYER and all action buttons were absent. The captured interval had no further activation and no probe-attributed validation error. The detailed evidence is in [FINAL GUARDS checkpoints](../evidence/2026-10-20-r005-player-context/final-guards-result.md).

This is bounded external UI evidence. It does not show that direct invalid-root Execute is safe, that the UI guard is atomic across every transition race, or that a programmatic caller cannot dispatch. Earlier direct character-scoped NULL Execute failed validation before effect entry and logged an invalid-character error even with a conditional root guard; never repeat that diagnostic. V1's missing markers were inconclusive, V2 showed a separate GUI receipt without effect markers, and V3 showed both entry definitions running once with the same explicit valid player root. Those observations do not create a rootless contract.

The FINAL GUARDS run used RESET before observer. It therefore does not establish that the nested watcher cleared a still-live READY value. Earlier watcher evidence demonstrated GUI-local marker clearing in its own tested case, not context or color restoration.

### RG-PLAYER-01 B — local player without a Dynasty

**Unresolved; no no-Dynasty local player was created.** In the single accepted attempt, the explicitly labelled LOWBORN TEST fixture invoked `set_to_lowborn` on the current test ruler. The engine rejected the mutation on the player character. The player and Dynasty remained; a fresh CHECK returned READY. This is fixture failure, not an unavailable-UI failure or pass. The shared no-Dynasty guard passing on Terentiy, an existing courtier under a distinct player root, and observer NO PLAYER are not substitutes for a local player whose Dynasty is absent.

Per the one-attempt limit, no fixture variants should be tried in this task. The supported-fixture search and actual no-Dynasty local-player UI check are deferred to [R-013 / GitHub #13](https://github.com/mhaduk/ck3-dynasty-map/issues/13), which was created and verified open. No additional GitHub writes are authorized by this checkpoint.

## Established supporting evidence and limits

- Fresh explicit player roots have delivered a valid player/Dynasty context across tested activation, manual character switches, succession, observer return and controlled save/load. The tested character-change hook did not cover global-observer or load transitions; multiplayer locality is unknown.
- The shared effect guard correctly rejected a real no-Dynasty courtier without traversing a Dynasty from that current scope. This does not validate player UI with no Dynasty.
- A corrected GUI watcher cleared a GUI-local marker after observed player loss. GUI state reset on reload is not guaranteed; map colors were not written or restored in these R-005 diagnostics.
- Logs in earlier runs contained excluded court-scene errors; the deliberate NULL call logged an error. Do not describe whole-run error logs as clean.
- ADR-008 remains in force: My Dynasty is unavailable without a valid local player or valid player Dynasty; unavailable activation performs no classification/color writes and is not replaced by an all-neutral map. Active-context cleanup and restoration remain separate, open work.

## Cleanup and current setup

After FINAL GUARDS, the user closed CK3 and opened the launcher. The original selection in the existing Dynasty Map - GUI Probe playset was restored: Native Menu Probe on, ENTRY diagnostic off. Launcher controls and enabled_mods agreed with the saved original. The ENTRY diagnostic remains installed but disabled. No save/mod files were deleted. This confirms launcher configuration cleanup only; it does not prove in-game visual restoration.

## Stop decision and next work

Do not repeat V1–V3, direct NULL, the passed lifecycle cases or the rejected LOWBORN fixture. No further R-005 runtime session is pending. R-013 owns the deferred no-Dynasty local-player fixture/UI evidence. **R-009 is the next project task, not started here**, for barony color side effects, map isolation and exit/restore. R-010 separately owns native-menu parity and refresh. R-005 remains partial until its deferred evidence and remaining implementation/test gates are resolved.

## Evidence

- [FINAL GUARDS result](../evidence/2026-10-20-r005-player-context/final-guards-result.md)
- [V1 result](../evidence/2026-10-20-r005-player-context/entry-v1-result.md)
- [V2 result](../evidence/2026-10-20-r005-player-context/entry-v2-result.md)
- [V3 result](../evidence/2026-10-20-r005-player-context/entry-v3-result.md)
- [Selected screenshots and interpretation](../evidence/2026-10-20-r005-player-context/README.md)
- [Chronological checkpoint history](../evidence/2026-10-20-r005-player-context/checkpoint-history.md)
