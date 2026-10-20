# R-005 — ENTRY v3 rooted comparison

Date: 2026-10-20. Target: recorded CK3 1.20.1.1 baseline.
Result: **both logging entries executed once with the same explicit valid
player root**. This completes the v3 comparison, not R-005 / RG-PLAYER-01.

## Evidence

User supplied screenshots showing Paused/PLAYER and both WAITING labels before
and after RESET, followed by both RECEIVED labels after CONTROL then ROOTED.
RESET was used while already WAITING; this does not independently test clearing
set flags and no repeat is needed for the entry comparison.

Current-run debug.log contains exactly:

| Entry | Log lines | Effect markers | Current/root scope |
|---|---|---|---|
| CONTROL, declared `scope = character` | 4111–4117 | One CONTROL_ENTER and one CONTROL_EXIT | Kazimierz Piast, character 52702, historical ID 221520 |
| ROOTED, omitted `scope` | 4118–4124 | One ROOTED_ENTER and one ROOTED_EXIT | Same Kazimierz Piast, character 52702, historical ID 221520 |

Both use `GuiScope.SetRoot(GetPlayer.MakeScope).End`. Log order agrees with the
user-reported CONTROL then ROOTED sequence. This does not establish ordering of
the two callbacks within either button. No saved event targets were listed.
Both effects only log markers and scopes; they do not traverse Dynasty or
modify gameplay state.

Only the intended ENTRY probe is listed as enabled in startup logs. Captured
debug.log is 467,955 bytes; gui_warnings.log is empty; error.log is 17,300 bytes
with the previously excluded court-scene locations and no diagnostic reference.
This is a whole-run capture, not a matched pre/post-click error delta. Do not
claim the entire error log is clean. Raw logs remain in ignored local evidence.
No automated game inspection or interaction was performed for this observation.

## Conclusions and limits

- The positive control establishes this mod's Execute/logging path under the
  tested explicit valid root. The rooted omitted-scope entry also executed,
  so omitted `scope` alone does not prohibit effects in that context.
- An omitted declaration is not a rootless-execution contract: v3 explicitly
  supplies a character root. It does not resolve the absence of v1/v2 markers
  under NO PLAYER or prove the cause of that difference. Do not call that a
  safe rejection, a generally unsupported API or a lazy-evaluation guarantee.
- This supports retaining explicit fresh valid-player roots as the verified
  execution baseline. Missing-player dispatch must still be prevented by an
  established external boundary or use another separately verified entry.
- No new Dynasty, no-Dynasty player UI, lifecycle, locality, title/color or
  cleanup claims follow. ADR-008 remains unchanged. R-005 remains Partial.

Do not repeat v3 or old passed cases. Next review the explicit-valid-player
dispatch contract and its remaining guard boundary, then identify a justified
no-Dynasty local-player fixture. No further runtime cycle is requested by this
result. User owns all game actions; game exit and prior playset restoration
have not yet been reported for this run.
