# R-005 — ENTRY v1 runtime observation

Date: 2026-10-20. Target: recorded CK3 1.20.1.1 baseline.
Result: **inconclusive; effect entry not confirmed**. R-005 / RG-PLAYER-01 remain open.

## Evidence

- User started CK3 through Steam. Startup debug log lists only ENTRY Contract
  Probe as enabled and records its GUI asset loading. Startup error.log and
  gui_warnings.log were empty; this is startup parsing evidence only.
- User reported loading a test game and selecting observer. Their supplied
  screenshot shows Paused, R-005 ENTRY v1, NO PLAYER and the ENTRY control.
  The control is a separate top-center overlay, not in Additional Modes.
- A pre-click log capture contained zero ENTER and zero EXIT markers. After
  instruction to click once, the user reported the click. Post-click logs
  still contain zero of both `DYNMAP_R005_ENTRY_V1` effect markers.
- All captured logs retained their earlier content as a prefix. The new
  debug/error intervals are identical: 275,096 bytes, containing 1,004 repeated
  `can_raid` invalid-character errors at `common/scripted_rules/00_rules.txt:543`.
  No new diagnostic-entry reference was found. GUI warnings remained empty.
  This is not a clean overall error-log result. Caller attribution is not
  established; do not attribute these errors to the new entry or vanilla alone.
- Raw startup, pre-click and post-click logs and byte deltas are ignored/local.
  No scope dump or successful effect execution was obtained.

## Interpretation and next step

User-reported clicking and a visible control do not independently prove that
the GUI action reached ScriptedGui.Execute. The absence of effect markers
cannot distinguish missed GUI delivery, failed dispatch or silent validation
rejection. No rootless/absent-player safety pass or engine limitation is proven.

Do not repeat unchanged v1, old NULL, succession or passed lifecycle tests.
Next preparation should add an observable GUI-only click indicator and separate
dispatch action, so click receipt can be distinguished from effect entry.
Prepare source separately through CLI; do not install while CK3 is running.
The user owns all game interactions and exit. Preserve this observation before
changing instrumentation; do not expand into raid-control investigation here.

Cleanup/previous mod-selection restoration has not yet been performed. Ask the
user to exit CK3 without overwriting a valued save before installation changes.

## Static preparation follow-up

The first v2 CLI attempt backed up files only. Its search did not establish
expression chaining; parent review instead found the native repeated-property
pattern: `game/gui/window_message_settings.gui:77–86` places two separate
onclick properties in one button (VariableSystem Set/Clear), and
`game/gui/window_council.gui:62–66` combines a window action with VariableSystem
Clear in one button. This supports preparing two independent receipt/dispatch
callbacks. It does not prove their order or runtime effect delivery. Retry
handoff supplies these references; no repeated broad research is needed.
CLI assumes the user's prepared application state without process checks.
