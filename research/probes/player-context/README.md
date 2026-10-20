# R-005 player-context diagnostics

**Current status (2026-10-20): Partial; static entry-contract review recorded.**
Target CK3 1.20.1.1; existing local probe-only playset, Realm Ledger off.
[Consolidated findings](../../../docs/RESEARCH.md#r-005--consolidated-status-2026-10-20)
are authoritative for current conclusions; dated history below is retained.

## Current outcome

Passed: explicit fresh player/Dynasty roots, repeated requests, manual player
switches, succession notification and successor activation, controlled save/load
activation, observer hiding/return and independent GUI marker invalidation.
Shared effect guard rejects a real no-Dynasty courtier and accepts a dynastic
player. No-Dynasty local-player UI remains untested.

NULL direct Execute blocks the effect but logs a character-scope validation
error; the conditional exists-root correction did not fix that. Do not repeat
this variant. The [static entry-contract review](../../../docs/evidence/2026-10-20-r005-player-context/entry-contract-review.md)
found query precedents only; `GuiScope.End` is not a guaranteed empty-root
constructor. An [isolated entry-contract probe v1](../player-entry-contract/README.md)
is prepared as source only, separate from this suite; it is not installed or
requested for execution. Character-change notifications did not
cover tested observer/load transitions. GUI marker clear is not color cleanup;
reported in-process reload retained the marker and does not prove save storage.

## Installed diagnostic components

- Existing native submenu source contains inert DM, R5, R5N, ARM/status, NULL
  and SUCCESSION. Raid/barter settings remain temporarily omitted.
- R5 supplies current player; R5N tests the shared guard on at most one existing
  no-Dynasty courtier/guest. It does not make that courtier the local player.
- Additive child on_action logs new/previous player for tested switches/succession.
- Zero-size additive startup widget clears a GUI-local ARM flag on player loss.
- **SUCCESSION kills the current living non-AI ruler with a player heir.**
  Use only a disposable timeline after a separate pre-test save; current probe
  is not wholly logging-only. Avoid incidental NULL/SUCCESSION activation.

No classifier/title/color writes or recurring scans. Static brace/encoding,
source/install equality and startup checks were performed at recorded revisions;
no Tiger run. Current variant startup was clean; final NULL runtime was not.

Raw logs/saves stay ignored/local. Reviewed screenshots are in
[the evidence record](../../../docs/evidence/2026-10-20-r005-player-context/README.md).
To withdraw diagnostics, exit CK3 and disable the entire local probe playset;
this is a procedure, not a recovery test already performed. For a future menu-only
run, remove diagnostic files/controls together and validate startup separately.
Keep pre-test save; disabling does not undo a death in a saved test timeline.

## Current source fingerprints

These hashes identify repository sources only; installation equality was checked
at deployment checkpoints, not rechecked by this documentation consolidation.

- `research/probes/native-menu-alternative/gui/zz_dynmap_native_menu_probe_02.gui`: `b89d443abe1808e4974b8828a36c2ea2a485ec34f0d3dd654977fcbc8a3b59d0`
- `research/probes/player-context/common/on_action/dynmap_r005_player_change.txt`: `f73e2f4daddc3c56ea180bc3521e5b8cfe3fce8dbfa9d2b15c0e0bd294232355`
- `research/probes/player-context/common/scripted_effects/dynmap_r005_context_effects.txt`: `84a464aaf3ba131d5b6bb3c70fcc324670548f40840763572bb7bf2f926933a4`
- `research/probes/player-context/common/scripted_guis/dynmap_r005_context.txt`: `68bd16720575222f5795ce9765d09e9009fd2f56352ce3f619c671d6264daf6b`
- `research/probes/player-context/gui/dynmap_r005_watcher.gui`: `6769835478dfb6fdbdb86796ab60d565199057bfa08ce74e21435930608dcf4d`
- `research/probes/player-context/gui/scripted_widgets/dynmap_r005_watcher.txt`: `0fbcc1ed240b0dc605086b3357f30d25bb0279839cf6ddb5a9fbc4249e2c8a4f`

## Historical checkpoint journal

Statuses, hashes and next steps below refer to their dated revisions. Later
results and the current summary above supersede them.

## Startup checkpoint 01

GUI loaded and gui_warnings.log was empty. error.log contained only a 142-byte
UTF-8 BOM warning for the diagnostic scripted GUI. Source corrected to UTF-8
BOM; restart and a fresh log check required. No runtime click result yet.

## Startup checkpoint 02

After restart, the probe mod is enabled and the submenu GUI loads. error.log
and gui_warnings.log are both 0 bytes. Raw logs archived locally under
`local/evidence/r005-player-context/startup-02`. This confirms clean startup
after the BOM correction, not click/root/guard behavior. Next: one R5 click
in a paused disposable game.

## R-005 click checkpoint 01 — 2026-10-20

User reported one R5 click in a disposable game. Captured debug.log:4105–4117
contains exactly one EXECUTE_ENTER / VALID_DYNASTY / EXECUTE_EXIT sequence.
Root is Alexios Palaiologos, character internal ID 52979 (historical ID 34281);
the Dynasty scope is Palaiologos, internal ID 17 (key 48). This verifies explicit
player-root delivery and a valid Dynasty traversal for this case only. No claim
of absent-context safety, automatic Execute validation or lifecycle coverage.

gui_warnings.log is empty. error.log is 17,413 bytes with tutorial/court-scene
errors preceding the click; no direct diagnostic filename reference. Attribution
is unresolved without a matched vanilla scenario. Raw capture is ignored under
local/evidence/r005-player-context/click-01. Next: repeat one R5 click while
paused, verify a second execution with the same root, then player switching.

## R-005 repeat checkpoint 01 — 2026-10-20

User switched to Terrain and clicked R5 three times. Captured debug.log has
three additional complete ENTER / VALID_DYNASTY / EXIT sequences (four total),
all with character 52979 / Dynasty 17. Repeated execution of this diagnostic
button works in the tested context; this is not proof of re-click activation
for a future selected custom map mode. error.log is byte-identical to click-01
(17,413 bytes); gui_warnings.log remains empty. Raw logs archived locally under
local/evidence/r005-player-context/repeat-01. Next: switch to another dynastic
character in this disposable game and click R5 once; compare fresh context.

## R-005 player-switch checkpoint 01 — 2026-10-20

User selected Duke Stefan and clicked R5 once. Fifth complete diagnostic
execution in debug.log:4227–4239 has Stefan Nemanjić of d_rashka as root
(character 51736, historical ID 218500) and Nemanjić as Dynasty (85, key 184),
replacing the prior Alexios/Palaiologos context. Fresh root/Dynasty acquisition
after this manual character switch is VERIFIED; no hook was installed/tested.
error.log is byte-identical to repeat-01 (17,413 bytes); GUI warnings empty.
Raw logs archived locally under local/evidence/r005-player-context/player-switch-01.
Next gate: global observer/no-player UI availability and evaluation errors.
Succession, no-Dynasty character, direct invalid execution, reload and cleanup
remain unverified; R-005 stays Partial.

## R-005 observer checkpoint 01 — 2026-10-20

User entered global observer and supplied a screenshot showing R5 absent while
inert DM remains. Diagnostic execution count stays five: no additional effect
execution observed. GUI warnings remain empty. However error.log grew from
17,413 to 149,481 bytes, with repeated invalid-character can_raid errors at
common/scripted_rules/00_rules.txt:543. The original submenu replacement uses
GetPlayer.CanRaid for its raid-setting visibility, so it is a concrete suspect;
absence of a diagnostic filename in errors does not exclude our GUI as caller.
A matched vanilla observer/control-isolation check is needed before attribution.
Hidden R5 is positive visibility evidence, not a clean observer safety pass.
Raw logs: local/evidence/r005-player-context/observer-01. Reviewed screenshot:
docs/evidence/2026-10-20-r005-player-context/observer-r5-hidden.png.
Next: return to a playable character to stop exercising absent-player controls;
then isolate and guard the submenu player-dependent settings before retesting.

## R-005 observer-return checkpoint 01 — 2026-10-20

User returned from observer to Gavril and clicked R5. Sixth complete execution
uses Gavril Basarab of c_suceava (character 54609, historical ID
moldavian_count_1) and Basarab Dynasty (4964, key moldavian_placeholder_dynasty_1).
The tested observer-to-player return supplies fresh context; no stale Stefan
or Alexios scope is used. GUI warnings remain empty. error.log reached 655,011
bytes with 2,327 can_raid errors; last recorded error is 14:03:55, before the
14:04:01 diagnostic click (log timestamps). No continued-spam claim can be made
without a later sample. Raw logs: local/evidence/r005-player-context/observer-return-01.
Next: exit to launcher and prepare an isolation variant removing the two
player-dependent raid/barter visibility controls; restart and compare observer
logs before selecting a production guard. R5 remains a logging-only diagnostic.

## Observer isolation variant — prepared 2026-10-20

Temporarily omitted the raid and barter settings from the original submenu
source, removing GetPlayer.CanRaid and GetPlayer.HasBarterGoods evaluations.
Other controls and R5 remain unchanged. This is a diagnostic reduction, not a
production solution or proof that either control caused the errors.
GUI SHA-256: `24565d92445507734c6e4f56ed8b42729887c6e6db2e2c342af65c3e692dd60b`. Restart, inspect startup, then repeat global observer
with Additional Modes open. Compare errors and R5 visibility. Historical R-010
parity checks do not apply to this reduced variant.

## Isolation startup checkpoint — 2026-10-20

Installed reduced GUI loaded with the local probe enabled. error.log and
gui_warnings.log are both empty. Raw logs archived under ignored
local/evidence/r005-player-context/isolation-startup-01. Observer comparison
is pending; startup alone does not establish the source of earlier errors.

## R-005 isolation observer checkpoint — 2026-10-20

User clicked R5 as a player, switched to global observer, confirmed R5 hidden
and held Additional Modes open for approximately 10 seconds. Fresh logs show
one complete Gavril Basarab / Basarab execution, no extra execution in observer,
zero can_raid errors and empty gui_warnings.log. error.log is 17,300 bytes,
containing court-scene errors; no diagnostic reference. Raw logs archived under
local/evidence/r005-player-context/isolation-observer-01.

Removing both player-dependent settings eliminated the previously observed
can_raid spam in this test. This supports that GUI evaluation path as the cause;
it does not isolate each removed control independently or prove barter safety.
R5 visibility and explicit root delivery passed this observer transition in the
reduced variant. Do not equate this with clean overall error.log or completed
ADR-008 lifecycle/color restoration. Production guards for the omitted settings
remain undecided. Next: return to a player and click R5 once to verify recovery
in this reduced variant, then address the no-Dynasty/direct-execution gate.

## R-005 isolation return checkpoint — 2026-10-20

User selected Yaroslav and clicked R5 after returning from global observer.
The second execution in this session uses Yaroslav Rurikid of d_halych
(character 52141, historical ID 222500) and Rurikid Dynasty (1594, key 705),
not prior Gavril/Basarab. error.log remains byte-identical to the observer
checkpoint (17,300 bytes); zero can_raid errors and empty GUI warnings.
Fresh player context after observer return is VERIFIED for this reduced GUI
variant. Raw logs: local/evidence/r005-player-context/isolation-return-01.
Next: prepare a controlled no-Dynasty/direct-execution diagnostic; do not alter
the current player's Dynasty or claim invalid-context safety from valid cases.
Succession/reload/hooks and color cleanup remain separate open gates.

## No-Dynasty shared-guard variant — prepared 2026-10-20

R5 and new R5N now call one logging-only scripted effect. R5N is enabled when
the player's court/guests contain a character without a Dynasty. It selects at
most one matching character using ordered_courtier_or_guest, order_by = 0,
max = 1 (ties are intentionally irrelevant). The iterator may inspect the local
court/guest list, not the world; it runs only on request. No RNG, persistent
variables, character/Dynasty edits, title/color writes or recurring scans.

Evidence: clean effects.log:6363–6375 documents ordered iterator parameters
and character scopes; triggers.log:1579–1583 documents any_courtier_or_guest.
Expected: NO_DYNASTY_TEST_ENTER, GUARD_ENTER with current courtier and player
root, REJECT_NO_DYNASTY, GUARD_EXIT, NO_DYNASTY_TEST_EXIT. No VALID_DYNASTY
inside this execution. Root intentionally stays the player; this verifies
current-scope effect guarding, not direct ScriptedGui.Execute invalid-root
validation or no-Dynasty player UI. Disabled R5N means no candidate was found.
Restart/startup validation required. Earlier file hashes describe old revisions.

## R5N startup checkpoint — 2026-10-20

Local probe mounted; submenu GUI loaded. error.log and gui_warnings.log empty.
Source/install byte equality was checked during installation. Raw startup logs:
local/evidence/r005-player-context/no-dynasty-startup-01. No R5N click performed
yet; next checkpoint is one click if enabled in a paused disposable game.

## R-005 no-Dynasty guard checkpoint — 2026-10-20

User clicked R5N once. debug.log:4105–4114 records exactly one complete
NO_DYNASTY_TEST_ENTER / GUARD_ENTER / REJECT_NO_DYNASTY / GUARD_EXIT /
NO_DYNASTY_TEST_EXIT sequence. Current scope is Terentiy Lowborn (character
75862); root remains player Yaroslav Rurikid (52141). No VALID_DYNASTY branch
was executed in this test. The shared effect's current-scope exists = dynasty
guard rejects this real no-Dynasty character without attempting Dynasty scope
traversal. Root/current-scope distinction is confirmed by the diagnostic.

GUI warnings empty; error.log 17,300 bytes of court-scene errors, no can_raid
errors or direct dynmap reference. Raw logs archived under ignored
local/evidence/r005-player-context/no-dynasty-click-01. This does not verify
a no-Dynasty local-player button state, automatic Execute validation, absent
character roots or lifecycle hooks. Next: click ordinary R5 once to check the
valid branch after extracting the shared diagnostic effect, then lifecycle
hook/direct-execution research. R-005 remains Partial.

## R-005 shared valid-branch regression — 2026-10-20

After the R5N rejection test, user clicked ordinary R5 once. One complete
EXECUTE_ENTER / GUARD_ENTER / VALID_DYNASTY / GUARD_EXIT / EXECUTE_EXIT
sequence uses Yaroslav Rurikid (52141) as current/root and Rurikid Dynasty
(1594). Both branches of the extracted shared effect now have runtime evidence:
valid player traverses Dynasty; no-Dynasty courtier is rejected. error.log is
byte-identical to no-dynasty-click-01 (17,300 bytes); GUI warnings empty.
Raw logs: local/evidence/r005-player-context/shared-valid-01. No automatic
Execute validation, absent root, no-Dynasty player UI or lifecycle proof follows.
Next: logging-only on_player_character_change hook probe to resolve installed
comment/generated expected-scope discrepancy; no color work.

## Player-change hook variant — prepared 2026-10-20

Added original common/on_action/dynmap_r005_player_change.txt. Installed
common/on_action/_on_actions.info, MODDING INFO, explicitly documents appending
a custom child through on_actions while warning against a second effect block
on the native hook. This probe follows that documented additive pattern.
Native behavior remains defined by vanilla; no vanilla effect is replaced.
The child only logs scopes and checks previous_player_character existence.
No player/Dynasty edits, saved state, event scheduling, scans or color writes.

Expected markers: PLAYER_CHANGE_ENTER, scope dump, PREVIOUS_PLAYER_PRESENT
or PREVIOUS_PLAYER_ABSENT, PLAYER_CHANGE_EXIT. Delivery and scope semantics
remain runtime questions. First checkpoint: restart/startup log inspection.
Then, in a paused disposable game, note current player, switch to another
dynastic character once, report both names; no R5 click is required.
Observer/succession/load delivery is not established by a manual-switch pass.

## Hook startup checkpoint — 2026-10-20

Restart reached main menu with error.log and gui_warnings.log both empty.
Raw logs archived under local/evidence/r005-player-context/hook-startup-01.
No hook delivery claimed before character switching. User reported display
layout/resolution trouble; local settings show fullscreen, 1920x1080 and
render scale 1.0. Cause, including sleep/restore, unverified; no display settings
were changed by the diagnostic installation.

## Hook load observation — 2026-10-20

User reports loading the latest save after resolving the display issue. Capture
contains zero PLAYER_CHANGE_ENTER markers. This is a load observation, not
proof of a reliable load callback or complete save/load safety. error.log is
34,600 bytes with court-scene errors, no dynmap reference or can_raid errors;
GUI warnings empty. Raw logs: local/evidence/r005-player-context/hook-load-01.
Next: one manual character switch, report old/new names and inspect hook scopes.

## R-005 character-change hook checkpoint — 2026-10-20

User manually switched to Roman without an R5 click. Exactly one complete
PLAYER_CHANGE_ENTER / PREVIOUS_PLAYER_PRESENT / PLAYER_CHANGE_EXIT sequence
was captured. Root/current is Roman Vsevolodovich of d_volhynia (56052,
historical ID 222520); previous_player_character is Yaroslav Rurikid of
d_halych (52141, historical ID 222500). The child-hook registration and
new/previous-character scopes are VERIFIED for this manual switch. This
resolves the installed-comment/generated-Expected-Scope discrepancy for the
tested case in favor of the installed comment; metadata alone was insufficient.

error.log is byte-identical to hook-load-01 (34,600 bytes), no dynmap references;
GUI warnings empty. Raw logs: local/evidence/r005-player-context/hook-switch-01.
No proof of local-only execution, observer transition notification, succession
or reload notification follows. Next: observer transition and return without
R5 clicks, inspect hook delivery and missing scopes.

## R-005 observer hook delivery checkpoint — 2026-10-20

User reports Roman → global observer → King Kazimierz without R5 clicks.
Captured hook entry count remains one (the earlier Yaroslav → Roman switch).
No child-hook notification was observed for either reported observer transition.
This is negative evidence for relying solely on on_player_character_change
for ADR-008 context-loss safety; do not assume missing root callbacks.
error.log unchanged (34,600 bytes), zero can_raid/dynmap references, GUI warnings
empty. Raw logs: local/evidence/r005-player-context/hook-observer-return-01.
The hook works for the tested direct character switch but does not cover these
observer transitions. A separate local UI/context invalidation mechanism must
be researched; no recurring world scan is authorized.

Next checkpoint: ordinary R5 as Kazimierz, then a new disposable save/reload
and another R5 click to compare explicit fresh context across loading. This
checks activation after load, not automatic lifecycle/color restoration.

## R-005 controlled save/load activation — 2026-10-20

User performed R5 → new disposable test save → reload → R5. Two complete
executions at log times 17:21:12 and 17:22:06 both use Kazimierz Piast of
k_poland (52702, historical ID 221520) and Piast Dynasty (1592, key 699).
Save persistence entries occur between them. Explicit fresh activation after
this save/load passes. Hook count remains one, with no new notification from
loading. This does not establish automatic cleanup on load or active-map
persistence; no active map/classifier exists in the diagnostic.

error.log grew from 34,600 to 51,900 bytes, with court-scene invalid-character
locations; zero dynmap references/can_raid errors. GUI warnings empty. Court
error attribution remains unresolved. Raw logs:
local/evidence/r005-player-context/save-load-01. Save itself remains private
and untracked. Next: investigate local observer/load invalidation mechanisms
without recurring world scans; succession and direct-invalid execution remain
open. Do not repeat passed save/load activation without a regression reason.

## Batched lifecycle probe — prepared 2026-10-20

Added zero-size additive startup widget and separate ARM/status controls.
Installed _scripted_widgets.info documents startup registration; installed
multiplayer_lobby.gui:13–15 shows _hide/on_start UI cleanup. Candidate watcher
visibility depends solely on GetPlayer.IsValid and clears GUI-local
dynmap_r005_armed on hide. No scoped script is executed by this callback.
Registration, _hide delivery and VariableSystem behavior remain unverified.
See BATCH_TEST.md for one-session menu/direct-switch/observer/return/save-load
sequence. No world scans, gameplay state or color writes. No production
cleanup claim. Existing R5/R5N/hook diagnostics remain installed.

## Batch startup checkpoint — 2026-10-20

Watcher GUI asset loaded with probe mod enabled. error.log and
gui_warnings.log are empty. Raw logs archived under ignored
local/evidence/r005-player-context/batch-startup-01. This confirms clean
startup/asset parsing, not watcher instantiation or callback behavior.
Next: execute A–E from BATCH_TEST.md and record actual statuses.

## R-005 batch results — 2026-10-20

User reports B Roman/R5; C ARMED instead of CLEAR; D Kazimierz/R5, ARMED;
E ARMED after reload. A result was not explicitly reported. Three reviewed
screenshots show ARMED with R5 and ARM visible, inconsistent with the earlier
confirmed no-player global observer presentation. Clarification requested on
observer subtype. No claim that the watcher instantiated or its callback failed
in a verified absent-player context is warranted. Its mechanism is unproven.

Logs capture two R5 calls (Roman 56052; Kazimierz 52702) and two character-change
hook entries (Roman, then Kazimierz). A separate post-reload R5 execution is
not present in this capture; E is user-reported marker persistence only.
No save-file persistence conclusion follows from a GUI marker surviving
in-process reload. error.log 34,600 bytes, no dynmap/can_raid references; GUI
warnings empty. Raw logs: local/evidence/r005-player-context/batch-01.
Screenshots: docs/evidence/2026-10-20-r005-player-context/batch-armed-1.png
through -3.png. Court-scene errors remain outside task scope.

Next: resolve observer subtype, then verify watcher instantiation and callback
delivery with an independent positive control before repeating lifecycle tests.
Avoid another broad A–E cycle until the diagnostic itself is observable.

### R-005 confirmed watcher observer/return — 2026-10-20

User clarified that the first batch C had not actually entered global observer;
that attempt is invalid as a global-observer test, not a watcher failure. User
then repeated only C–D: ARM as player, close menu, global observer, reopen menu,
return to Kazimierz. Two screenshots confirm CLEAR with R5/R5N/ARM absent in
observer, then CLEAR with controls restored after returning. This supports
startup watcher instantiation and _hide-based GUI marker invalidation on
player-validity loss, including with the map menu closed. No extra R5/hook
execution: counts stay two each. error.log unchanged at 34,600 bytes, no
dynmap/can_raid references; GUI warnings empty. Court-scene errors excluded.
Raw capture: local/evidence/r005-player-context/watcher-observer-confirmed-01.
Reviewed images: docs/evidence/2026-10-20-r005-player-context/
watcher-observer-clear.png and watcher-return-clear.png.

The watcher hypothesis now has positive runtime evidence for this transition.
It clears a GUI-local flag only, not title colors or saved state. Earlier
reported ARMED after in-process reload remains a limitation: reloading need
not reset VariableSystem. Direct switches between valid players still use
separate hook/revalidation handling. No general lifecycle-safety claim.
Next: static inspection of guarded direct/no-root scripted-GUI execution and
prepare the smallest remaining invalid-context test; do not repeat C–D.
Succession and no-Dynasty local-player UI remain unverified.

### R-005 final diagnostic cycle prepared — 2026-10-20

NULL explicitly calls the existing character-scoped diagnostic Execute with
GetNullCharacter.MakeScope, bypassing IsValid. Generated data types expose
GetNullCharacter -> Character at data_types_uncategorized.txt:547–549. Outcome
(engine rejection, effect delivery or scope errors) is unknown; this deliberately
invalid call has no gameplay writes and must not become production behavior.

SUCCESSION is a separate, explicitly labeled disposable-timeline test that
uses death = natural on the current non-AI living ruler only if a player_heir
exists. Its activation intentionally changes gameplay; unlike earlier probes
this variant is NOT logging-only. Save to a new local slot before using it;
never overwrite a valued save and reload the pre-test slot afterward if desired.
Generated effects.log:4053 documents death = natural; event_targets.log:700
documents player_heir. The handler logs current character and expected heir
before death; runtime notification and successor context still require testing.
No classification/color writes. No-Dynasty local-player UI remains an explicit
untested case: the courtier effect guard is not a substitute.

One cycle: startup check; disposable save; ordinary R5, NULL once, SUCCESSION
once if enabled, acknowledge succession, pause and R5 as successor. Report
old/new ruler and any unexpected interface behavior. Do not re-arm or repeat
observer/load checks. If no heir or Game Over, record limitation and stop.

### Final-cycle startup checkpoint — 2026-10-20

Probe mod enabled; error.log and gui_warnings.log both empty. Raw logs:
local/evidence/r005-player-context/final-startup-01. NULL and succession
execution remain untested. Next: separate disposable save before any
SUCCESSION activation, then ordinary R5, NULL once, succession once and
successor R5. Stop on crash or Game Over.

### R-005 NULL direct Execute checkpoint — 2026-10-20

User clicked R5 then NULL. debug.log records one valid Kazimierz/Piast
execution, followed by a null-character error in dynmap_r005_context:is_valid
(line 4) at 17:42:50. No second EXECUTE_ENTER/GUARD_ENTER sequence occurred.
Thus direct Execute invokes validation in this tested case and rejected the
null root before effect execution, but the current is_valid = exists dynasty
condition is not safe on a missing character: it logs an invalid-scope error.
Do not call this a clean absent-root guard pass or general Execute contract.
Production entry must reject missing roots before character-scoped validation.

GUI warnings empty; error.log 17,602 bytes includes the intentional probe's
invalid-root error (distinct from excluded court errors). Raw logs:
local/evidence/r005-player-context/null-click-01. NULL's plain primitive button
looks like text but the log confirms click delivery. Do not repeat NULL in
this variant. Continue only the separately saved succession test; null guard
hardening remains open after this final cycle.

### R-005 succession checkpoint — 2026-10-20

SUCCESSION logged Kazimierz Piast (52702) and expected player heir Boleslaw
Piast (58578, historical ID 170096), then the hook fired automatically with
Boleslaw as root and previous_player_character Kazimierz. User's subsequent
R5 executed as Boleslaw / Piast Dynasty 1592. The tested player succession
notification and fresh successor activation pass. No new error.log bytes
after NULL (17,602 bytes total); GUI warnings empty. Raw evidence archived
under local/evidence/r005-player-context/succession-01. No further succession
repeat needed. Diagnostic timeline intentionally changed by ruler death; the
pre-test save permits recovery and remains outside Git.

Final cycle conclusion: succession passed; direct NULL exposed an invalid-root
validation error and requires correction/retest. No-Dynasty local-player UI
still lacks a verified fixture. R-005 remains Partial, not complete. Next single
task is absent-root guard hardening, followed by the smallest NULL/valid-root
regression. Do not repeat observer, load or succession. Color restoration is
still R-009 work, not part of this diagnostic outcome.

### R-005 absent-root guard correction prepared — 2026-10-20

Changed ordinary context is_valid to conditional trigger_if: exists = root
before testing dynasty; trigger_else always = no. Effect also explicitly
checks root before calling the shared character guard. Installed scripted GUI
00_empire_faith_gate_guis.txt:51–78 demonstrates conditional validation;
clean triggers.log documents exists as a null-target check. This is a
candidate fix, not runtime verified. It avoids assuming AND short-circuiting.
After restart/startup check, click NULL once then ordinary R5 once. Expected:
no missing-character error/effect from NULL, and one valid player execution.
No repeated succession, observer or save/load requested.

### Root-guard startup checkpoint — 2026-10-20

After restart, error.log and gui_warnings.log are empty. Raw logs archived
under local/evidence/r005-player-context/root-guard-startup-01. Conditional
root guard runtime result is pending; next sequence is NULL once then R5
once as a valid player. No succession repeat.

### R-005 conditional-root guard regression — 2026-10-20

User loaded the post-succession Boleslaw save and clicked NULL then R5. This
is a valid fixture for the ordinary-player regression. Exactly one complete
execution uses Boleslaw Piast (58578) / Piast (1592). NULL still logs an invalid
character error at dynmap_r005_context:is_valid line 4, despite the conditional
exists-root guard; no effect execution occurs for NULL. The attempted fix does
NOT make direct invalid-root execution clean. Failure points at validation
entry; engine character-scope requirements are a candidate explanation, not
an independently proven implementation detail.

error.log 17,602 bytes includes the known deliberate NULL error; GUI warnings
empty. Raw capture: local/evidence/r005-player-context/root-guard-click-01.
Do not repeat this variant. Production must avoid dispatching character-scoped
Execute with absent player, rather than assuming an internal trigger can make
such dispatch safe. A verified missing-player UI path already hides controls;
programmatic dispatch constraints need to be documented and reviewed before
selecting the entry architecture. No-Dynasty local-player fixture still missing.
Next: consolidate R-005 results and the invalid-dispatch limitation, then decide
whether a separate rootless entry is needed; no further user clicks requested.
