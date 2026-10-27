# R-005 — ENTRY v2 observation

Date: 2026-10-20. Target: recorded CK3 1.20.1.1 baseline.
Result: **GUI receipt confirmed; scripted effect entry unconfirmed**.
R-005 / RG-PLAYER-01 remain open.

## Evidence

User supplied four screenshots and described loading a save, selecting observer,
clicking RESET while already showing WAITING, then clicking ENTRY. The final
screen shows Paused, NO PLAYER and CLICK RECEIVED; an earlier screen shows
Paused/NO PLAYER/WAITING. The full supplied map view also shows Observing.
The loaded save may already have had no player; no player-to-observer transition
or lifecycle callback is claimed. RESET keeping an already-WAITING display
does not independently prove clearing a set flag. No repeat is requested.

Current-run log capture:

- debug.log: 467,713 bytes; zero `DYNMAP_R005_ENTRY_V2 ENTER` and zero EXIT.
- Intended ENTRY probe mounted; its GUI asset load is recorded. No effect scope
  dump associated with the probe was obtained.
- gui_warnings.log: empty.
- error.log: 17,300 bytes, court-scene locations already excluded from further
  R-005 investigation; no diagnostic/scripted-GUI reference found. This is not
  a clean overall error-log claim. The earlier v1 can_raid outcome must not be
  attributed or generalized from this different run.

This is a current-run capture after the user's report, not a matched v2
pre/post-click delta. Raw logs stay in ignored local evidence. Screenshots are
user-supplied observations, not automated game inspection.

## Interpretation

The visible WAITING-to-CLICK RECEIVED transition confirms the ENTRY button's
VariableSystem receipt callback. It rules out the narrow hypothesis that none
of that button's callbacks received the reported interaction. It does not prove
the separate Execute callback ran, its order, successful entry lookup, validator
acceptance or effect delivery. Absence of markers cannot establish safe
rootless rejection or an unsupported API.

Two separate onclick properties have installed-source precedent. That static
finding is not a runtime guarantee that the two particular v2 callbacks both
ran successfully. Do not mark dispatch or absent-player safety passed.

Next research: inspect the Execute/root/scope entry boundary and design one
discriminating query/positive control if needed, reusing the existing evidence.
Do not keep changing click cosmetics or repeat v1/v2 unchanged. Do not repeat
passed switch/succession/observer/load cases or investigate excluded court
errors. No new runtime cycle is requested by this result.

User still owns game interactions and exit; no exit or launcher restoration
has been reported for this run. Preserve current evidence before install edits.

## Focused static follow-up and proposed control

Installed `game/gui/interaction_menu_window.gui:370–374` supplies an explicit
player root to Execute; `common/scripted_guis/00_character.txt:1–4` declares
character scope for that entry. Likewise,
`gui/activity_window_widgets/funeral_deceased_selection_button.gui:24–28`
supplies a player root and has two onclick properties; its
`common/scripted_guis/ce1_funeral_scripted_guis.txt:9–12` entry declares character.
These are specific source precedents, not proof that Execute always needs a
character root. No alternate invocation wrapper is justified by these examples.

Proposed v3 compares two logging-only entries with the same explicit valid
player root: existing omitted-scope entry versus a character-scoped positive
control in the same mod. Each gets independent receipt and effect markers.
This tests a changed input/definition, not old lifecycle behavior. It avoids
another unrooted/observer invocation. A scoped control is needed before
attributing absent v2 markers to omitted-scope execution. Runtime outcome
remains unknown; no absent-player safety conclusion follows even if both pass.
