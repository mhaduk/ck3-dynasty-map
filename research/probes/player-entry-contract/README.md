# R-005 — final-guards diagnostic

**Runtime attempt complete; no more R-005 fixture tests are pending.** Target CK3 1.20.1.1. The diagnostic remains installed in the existing ENTRY mod but is disabled in the restored test playset. R-005 / RG-PLAYER-01 remain partial/open; ADR-008 is unchanged.

## Final results

Checkpoint A passed for the tested ordinary displayed UI path: a healthy rooted CHECK and activation worked; after RESET and entering global observer, NO PLAYER appeared and all action buttons were absent. The bounded capture had no extra activation or probe-attributed validation error. This does not prove direct invalid-root Execute is safe, atomic behavior across all UI races, live READY clearing by the nested watcher (RESET came first), multiplayer locality or programmatic caller safety.

Checkpoint B did not create a no-Dynasty local player. The user invoked the one-shot, explicitly labelled LOWBORN TEST on the current test ruler. The engine rejected `set_to_lowborn` on the player character; the Dynasty remained, and a fresh CHECK returned READY. This is fixture failure, not a negative UI test. Do not repeat this fixture or try variants. R-013 / #13 owns future supported fixture and no-Dynasty player UI work.

See the authoritative [FINAL GUARDS result](../../../docs/evidence/2026-10-20-r005-player-context/final-guards-result.md) and [R-005 checkpoint](../../../docs/tasks/R-005-player-context.md). V1, V2 and V3 remain historical evidence: V1 was inconclusive, V2 confirmed a separate GUI receipt but no effect entry, and V3 ran two entries once with the same explicit valid player root. None established rootless execution. The earlier direct NULL call logged an invalid-character validation error before effect entry; never repeat it.

## Diagnostic scope and cleanup

The panel logs explicit-root CHECK, availability and activation observations. Only the intentionally clicked fixture entry calls `set_to_lowborn = yes`, on the current living human ruler after confirming a Dynasty; no classification, title or color writes are present. The diagnostic’s action controls use player-validity and GUI-local state. This is probe behavior, not production readiness.

After the test, the user closed CK3 and opened the launcher. The original selection in the existing Dynasty Map - GUI Probe playset was restored: Native Menu Probe on, ENTRY diagnostic off. Launcher controls and enabled_mods matched. The diagnostic files remain installed but disabled; no saves or mod files were deleted. This is configuration cleanup, not proof of in-game map-color restoration.

Do not run more R-005 trials. R-009 owns barony color side effects, map isolation and exit/restore; R-010 owns native-menu parity/refresh. All R-005 runtime actions were user performed; the final evidence has bounded limits and excluded court-scene log noise remains excluded, not evidence of globally clean logs.
