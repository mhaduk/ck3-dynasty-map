# R-005 selected visual evidence — 2026-10-20

User-supplied cropped screenshot of Additional Modes in global observer:
R5 is absent; inert DM and native controls remain visible. Reviewed image
contains game UI only, no local paths/account information. Target CK3 1.20.1.1,
local native-menu probe plus R-005 diagnostic; Realm Ledger disabled.

This proves visibility in the captured state, not safe evaluation of hidden
controls or lifecycle cleanup. Observer error.log grew with invalid-character
can_raid errors; attribution requires isolation (see RESEARCH.md).

Three additional user-provided crops, batch-armed-1.png through -3.png, show
ARMED with R5/R5N/ARM still visible. User supplied them in B–E test reporting
order; exact individual step mapping not independently established. All contain
only game UI. Observer subtype is unresolved; do not call this a verified
global-observer callback failure.

Confirmed follow-up: watcher-observer-clear.png shows CLEAR and no R5/R5N/ARM
in global observer; watcher-return-clear.png shows those controls restored and
CLEAR after returning to Kazimierz. User corrected the earlier batch: its first
C attempt had not entered global observer. These two game-UI-only crops are
reviewed evidence for the corrected C–D, not proof of color cleanup.

## Consolidated interpretation

The corrected observer/return pair is the positive watcher evidence. Earlier
batch ARMED images are historical: user clarified they had not entered global
observer in first C. That supersedes the earlier unresolved-subtype note; do
not count those images as watcher failure. Screenshots show GUI only; scope,
succession and NULL results derive from locally archived logs and original
findings in RESEARCH.md. No raw dumps/logs/saves are published here.

## FINAL GUARDS and cleanup

The [final result](final-guards-result.md) records two independent outcomes.
A passed for the tested displayed path: after a healthy rooted positive control
and RESET, observer showed NO PLAYER with action buttons absent; the bounded log
capture had no extra activation or probe-attributed validation error. This does
not establish direct invalid-root safety, every transition race, or live READY
clearing by the nested watcher because RESET came first.

B did not create a no-Dynasty player. The engine rejected the one permitted
`set_to_lowborn` call on the player character; Dynasty remained and fresh CHECK
returned READY. This is fixture failure, not a no-Dynasty UI pass. Further
fixture work and actual no-Dynasty local-player UI are deferred to
[R-013 / #13](https://github.com/mhaduk/ck3-dynasty-map/issues/13). Do not repeat
this mutation or try variants. The diagnostic remains installed but disabled;
the original playset selection was restored and verified. This records launcher
cleanup, not map-color restoration. No further R-005 runtime test is pending.
