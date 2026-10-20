# R-005 player-context checkpoint history

This dated record preserves diagnostic setup and runtime checkpoints for the still-open R-005 task. The reusable conclusion and current next action are in [RESEARCH.md](../../RESEARCH.md#r-005--consolidated-status-2026-10-20) and [CURRENT_STATE.md](../../CURRENT_STATE.md). Checkpoints are historical; later observations supersede earlier hypotheses and next steps.

### R-005 diagnostic preparation (2026-10-20)

An explicitly authorized logging-only diagnostic is prepared in
`research/probes/player-context`, with a separate R5 button in the existing
original submenu source. Fresh player-root construction, visibility, IsValid
and effect-level Dynasty guard are hypotheses under test, not verified runtime
behavior. DM remains inert; no classifier/title/color writes. First checkpoint
is startup log inspection followed by a single paused-game click. Character
change hooks and invalid-context transitions remain subsequent gates.

### R-005 click checkpoint 01 — 2026-10-20

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

### R-005 repeat checkpoint 01 — 2026-10-20

User switched to Terrain and clicked R5 three times. Captured debug.log has
three additional complete ENTER / VALID_DYNASTY / EXIT sequences (four total),
all with character 52979 / Dynasty 17. Repeated execution of this diagnostic
button works in the tested context; this is not proof of re-click activation
for a future selected custom map mode. error.log is byte-identical to click-01
(17,413 bytes); gui_warnings.log remains empty. Raw logs archived locally under
local/evidence/r005-player-context/repeat-01. Next: switch to another dynastic
character in this disposable game and click R5 once; compare fresh context.

### R-005 player-switch checkpoint 01 — 2026-10-20

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

### R-005 observer checkpoint 01 — 2026-10-20

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

### R-005 observer-return checkpoint 01 — 2026-10-20

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

### R-005 isolation observer checkpoint — 2026-10-20

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

### R-005 isolation return checkpoint — 2026-10-20

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

### R-005 no-Dynasty shared-guard variant — prepared 2026-10-20

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

### R-005 no-Dynasty guard checkpoint — 2026-10-20

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

### R-005 shared valid-branch regression — 2026-10-20

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

### R-005 player-change hook variant — prepared 2026-10-20

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

### R-005 hook load observation — 2026-10-20

User reports loading the latest save after resolving the display issue. Capture
contains zero PLAYER_CHANGE_ENTER markers. This is a load observation, not
proof of a reliable load callback or complete save/load safety. error.log is
34,600 bytes with court-scene errors, no dynmap reference or can_raid errors;
GUI warnings empty. Raw logs: local/evidence/r005-player-context/hook-load-01.
Next: one manual character switch, report old/new names and inspect hook scopes.

### R-005 character-change hook checkpoint — 2026-10-20

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

### R-005 observer hook delivery checkpoint — 2026-10-20

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

### R-005 controlled save/load activation — 2026-10-20

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

### R-005 observer-invalidation candidate — 2026-10-20

Court-scene errors are excluded from further R-005 investigation at the user's
direction; keep prior captures but do not use them to delay this task.

Installed GUI shows lifecycle-state callbacks: settings/setting_types.gui:18–20
uses _hide/on_finish to clear a VariableSystem key; multiplayer_lobby.gui:13–15
uses _hide/on_start and on_finish for UI cleanup. hud.gui:28–51 already verifies
GetPlayer.IsValid as the observer visibility discriminator. These support a
new diagnostic hypothesis, not a verified context-loss handler.

Next probe: a zero-size additive startup widget whose visibility depends only
on GetPlayer.IsValid, independent of the map-menu ancestor; _hide clears a
GUI-local diagnostic flag. A separate arm/status control in the menu will show
whether that flag survives ordinary menu close/reopen but clears after global
observer/return with the menu closed. This avoids executing character-scoped
script after the player disappears, world scans and gameplay state. A successful
flag test would establish GUI notification only, not title-color restoration,
same-validity character switches, reload reset guarantees or multiplayer safety.
Installation/restart and runtime validation are still required.

### R-005 batched lifecycle probe — prepared 2026-10-20

Added zero-size additive startup widget and separate ARM/status controls.
Installed _scripted_widgets.info documents startup registration; installed
multiplayer_lobby.gui:13–15 shows _hide/on_start UI cleanup. Candidate watcher
visibility depends solely on GetPlayer.IsValid and clears GUI-local
dynmap_r005_armed on hide. No scoped script is executed by this callback.
Registration, _hide delivery and VariableSystem behavior remain unverified.
See BATCH_TEST.md for one-session menu/direct-switch/observer/return/save-load
sequence. No world scans, gameplay state or color writes. No production
cleanup claim. Existing R5/R5N/hook diagnostics remain installed.

### R-005 batch results — 2026-10-20

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

### R-005 interrupted entry-contract inspection — session handoff

Read-only inspection after consolidation found Scope.IsSet -> bool in clean
data_types/data_types_script.txt:3735–3737. Installed
common/scripted_guis/tgp_scripted_guis.txt contains entries without explicit
scope (including tgp_has_access_to_ministry_trigger_gui). These are candidates
only: omitted scope does not prove a rootless default or safe Execute, and
Scope.IsSet does not prove lazy GUI argument evaluation. No installed example
or runtime result establishing a safe replacement entry was obtained before
the user paused for workflow optimization. No further implementation/install
change or runtime test. Resume read-only contract review in the same checkout.

### R-005 entry-contract static review resumed — 2026-10-20

Reviewed the remaining dispatch question without repeating completed research
or runtime cases. New installed-source call sites show omitted-scope query
entries called with `GuiScope.End` and a named-input query without explicit
`SetRoot`. Generated docs identify `GuiScope` as the GUI top scope; no empty-root
guarantee follows. No effect-bearing omitted-scope entry or matching direct
Execute call was found in the inspected installed source set. Lazy argument
evaluation and safe absent-player effect dispatch remain unproven.

See [the review](entry-contract-review.md) for source references, evidence limits
and a minimal future probe proposal. No probe source/install changes, game
launches, runtime tests, staging, commits, pushes or GitHub writes. R-005 remains
Partial; no-Dynasty local-player UI is independently open. Next: decide on the
narrow proposal before any runtime work; do not repeat NULL or passed cases.

### R-005 isolated entry-contract v1 source prepared — 2026-10-20

User authorized preparation without installation or execution. Added the
independent [entry-contract probe](../../../research/probes/player-entry-contract/README.md):
unique scripted-GUI entry without declared scope, a startup widget with manual
ENTRY control, registration, descriptor and a bounded future procedure.
The effect logs ENTER/actual scopes/EXIT only. No named input or Dynasty
traversal; no gameplay writes, native menu replacement or hooks. The current
GUI scope might still supply a root; the probe does not assume otherwise.

Existing NULL/SUCCESSION and watcher sources are untouched. No installation,
game launch, runtime checks, Tiger run, staging, commits, pushes or GitHub writes.
Prepared source is unvalidated in game. R-005 remains Partial; next is review
of the payload and procedure before deciding on runtime work.

### R-005 entry-contract v1 source review — 2026-10-20

Reviewed payload, registration and bounded procedure in the preparing chat;
no independent reviewer or engine validation is claimed. No source-level
blocker identified for the logging diagnostic. Clarified that the GUI reads
player validity while the entry performs no character/Dynasty traversal.
An ambiguous scope dump cannot establish rootlessness; missing markers without
confirmed click delivery cannot establish unsupported execution. Both remain
inconclusive rather than justification for repeating the unchanged probe.

Source is ready for a runtime decision. No installation, game launch or test;
the user's no-tests constraint remains in force. Existing local changes and
old diagnostics preserved. R-005 remains Partial, with both safety gates open.

### R-005 entry installation verified; launcher automation boundary — 2026-10-20

CLI result used attempt 01 ID while the active retry had attempt 02 ID. GUI
reconciled explicitly through actual installation inspection: four-file payload
inventory exact, all source/install bytes equal, wrapper name/build/path correct,
three earlier log copies equal to originals at review. Original handoff records
and reconciliation note remain ignored/local; no repeat installation.

GUI created the separate `Dynasty Map - R005 Entry v1` playset, initially empty.
The launcher did not offer the newly installed mod in that session. After normal
exit/reopen, launcher showed its generic library view. Steam UI capture failed;
Finder automation was not approved. Minimum manual prerequisite: open the CK3
launcher from Steam; Codex retains mod selection and launch. No game launch,
startup validation, ENTRY click, old NULL or passed-case repetition occurred.

### R-005 existing playset configured; user owns app start — 2026-10-20

User corrected app ownership: they alone open/restart launcher and CK3 through
Steam. Codex inspected only the already running launcher in this step; it did
not launch either app or click PLAY/RESUME. The correct CK3-specific view now
offered the installed ENTRY mod. Codex reused `Dynasty Map - GUI Probe`, disabled
Native Menu Probe and added/enabled ENTRY v1 only; Realm Ledger is absent.
Visible launcher state and saved enabled-mod configuration agree. Installed
payload still matches source. Earlier logs and previous selection are retained
locally for restoration. No new playset, game launch or runtime test in this
step. Next: user starts CK3 through Steam, stops at main menu; Codex inspects
fresh startup logs before the single new absent-player observation.

### ENTRY v1 startup and reported click — 2026-10-20

Startup passed with only ENTRY mounted and empty error/GUI-warning logs.
User supplied Paused/NO PLAYER/ENTRY screenshot and reported one click after
the pre-click capture. Post-click logs still have zero ENTER/EXIT markers and
no scope dump; GUI warnings empty. New debug/error intervals match and contain
repeated can_raid errors without a diagnostic reference. No clean effect-entry
or rootless safety conclusion. See [the result](entry-v1-result.md).
Do not repeat unchanged v1. Next: prepare a GUI-only click indicator separately
from dispatch; user exits CK3 before any installation changes. Cleanup and
prior-selection restoration remain pending. All game interaction is user-owned.

### ENTRY v2 GUI receipt confirmed; no effect markers — 2026-10-20

Matched v2 CLI handoff completed and installed bytes were verified. User later
supplied four screenshots and reported load/observer/RESET/ENTRY actions.
Screens show Paused/NO PLAYER/Observing and WAITING-to-CLICK RECEIVED; receipt
callback confirmed. RESET started from WAITING, so no independent flag-clearing
pass follows. Current-run capture has zero V2 ENTER/EXIT markers, no associated
scope dump or diagnostic error reference; GUI warnings empty. Court-scene
errors remain excluded. See [v2 result](entry-v2-result.md).

Do not repeat unchanged v2. Review Execute/root/scope boundary before any new
probe, retaining uncertainty about the separate Execute callback. No further
runtime cycle requested; user has not reported game exit or configuration
restoration after this observation.

### ENTRY v3 rooted comparison passed — 2026-10-20

User supplied Paused/PLAYER/WAITING and subsequent ROOTED RECEIVED / CONTROL
RECEIVED screenshots. Current-run logs contain exactly one complete CONTROL
sequence followed by one ROOTED sequence, both current/root Kazimierz Piast
(52702, historical ID 221520). This verifies effects in both definitions with
the same explicitly supplied valid root; it does not prove rootless execution
or explain v1/v2 marker absence. GUI warnings empty; excluded court-scene
errors remain without diagnostic references. See [v3 result](entry-v3-result.md).

Do not repeat v3 or old passed cases. R-005 remains Partial for safe absent-player
dispatch and no-Dynasty local-player UI. Next consolidate the valid-root contract
and guard boundary before another probe. No further runtime cycle requested;
user has not reported game exit or prior-selection restoration for this run.
