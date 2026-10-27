# T-025 — Verify remaining Dynasty Map lifecycle and persistence gates

Issue: [#51](https://github.com/mhaduk/ck3-dynasty-map/issues/51)
Parent: [R-009 / #9](https://github.com/mhaduk/ck3-dynasty-map/issues/9)
Status: **PLANNED / not started** (registered 2026-10-27)

## Accepted baseline to reuse

R-009's user-accepted local checkpoint covers the corrected current-DEV observer
path on CK3 1.20.1.2: automatic return from the custom Dynasty view to native
Realms in observer mode, selection of native Cultures while still observing,
return to the original player without automatic Dynasty reentry, and ordinary
manual reentry. The final refresh save matched the corrected pre-observer title
identities and RGB for all 18,190 title records. The bounded error log was
unchanged; GUI and database-conflict logs were empty. These results are limited
to the observed path and do not establish beta safety or all-world-state
identity.

Reuse accepted source29/install30/startup31 and runtime32–36 evidence. Do not
repeat broad API research or the completed cardinalate-copy experiment.

## Remaining work

1. Reconcile the earlier repeat-cycle discrepancy: the saved checkpoint labelled
   Dynasty Realms matched first Holdings and differed from first Realms in 81
   baronies. Later controlled Realms entry maps agree. Cause remains unknown;
   do not attribute it to user action or code without evidence.
2. Verify the final painted-save/reload and fresh-process DEV-absent path for the
   corrected fixture-free candidate. Earlier absent-mod evidence used an older
   fixture-bearing payload and does not automatically pass this candidate.
3. Compare complete title keys/IDs, RGB fields and relevant noncolor owner,
   capital, liege, and context fields across corrected checkpoints. This is
   saved-title invariance evidence, not proof of all-world-state equality or
   native display behavior.
4. Record one explicit candidate lifecycle/persistence verdict and limitations
   for T-017's release-readiness decision.

## Boundaries

- Status remains **PLANNED**; no game test was performed as part of R-009 closeout.
- User alone starts/stops CK3 and performs all loads, saves, switching and tests.
- R-005 owns broader player/no-Dynasty dispatch and detection; T-014 owns
  production packaging; T-017 owns beta readiness.
- Preserve historical research and experimental saves. No migration, deletion,
  reset, alternative renderer, palette redesign or performance work is included.
- Gray-base palette quality is deferred.

## Acceptance

Resolve each remaining criterion with bounded evidence or state the exact
unavailable gate and its evidence limit. Explain the 81-barony discrepancy or
preserve its causal uncertainty. Verify corrected-candidate save/reload,
DEV-absent behavior and title invariants, or leave the gate explicitly open.
R-009 closure is not SAFE FOR BETA.
