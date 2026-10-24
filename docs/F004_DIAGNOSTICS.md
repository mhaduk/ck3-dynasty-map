# F-004 diagnostics and interaction guide

This developer guide records the accepted CK3 1.20.1.2 / Steam build 26046173
diagnostic contract and user gestures. It does not claim that CK3's native
debug-scope output is a stable serialization API or that saved map colors are
restored safely.

## Native declaration channel

Earlier controls showed positive local counters and saved snapshots while the
localized summary printed zero. The current diagnostic channel reads the
captured named values from the native `debug_log_scopes = yes` output. The
localization mismatch is therefore not used as the audit's declared count.
The native text remains build-bound diagnostic evidence; do not assume its
format is a supported CK3 serialization interface.

DIAG V3 emits a framed summary or bounded sample operation. Its twelve native
counters include total, Primary, Secondary, Neutral, held/unheld, holder and
senior match counts, subtree and attempted writes. Samples are limited to ten
entries per role and twenty detail records. An operation with complete framing
establishes that operation's delivery and bounds; it does not establish a
full-map classifier PASS.

AUDIT V4 emits a separate native roster/actor declaration block and a selected
view counter block. The strict analyzer checks complete build-bound framing,
current and Root identity, phase keys, duplicate/injected keys, integer
grammar, arithmetic, roster/actor agreement and per-view emitted records.
Missing declarations stay INCOMPLETE; row counts are never substituted for
missing native declarations. A PASS is limited to that selected view and the
emitted roster in the tested fixture. REALMS, HOLDINGS and MY_REALM each need
their own selected-view batch.

Keep these verdicts separate in reports:

1. callback or operation observed;
2. operation framing and whole-file interval completeness;
3. declared-count and emitted-record agreement;
4. role and intended-RGB agreement;
5. user acceptance and any broader lifecycle claim.

For example, the latest bounded SAMPLES operation is fully framed and within
its limits while the containing file interval retains a partial unrelated
boundary and the sample-only global analysis stays INCOMPLETE. Neither label
overwrites the other.

## Modifier gestures

The three view buttons share a stable 130×40 host. A complete normal row and a
complete audit row occupy the same top-left origin; each row contains three
40×40 controls with 5 px gaps. The artwork is 26×26 and mouse-transparent.
Row-level visibility selects the alternative row. User testing in the fresh
Ismail 867 fixture found the host stationary and icon hits correct when
Shift+Option was held/released without clicking, then verified normal hits.
This confirms the accepted behavior in that build, not the engine's internal
anchor/layout mechanism.

| Gesture | Behavior |
|---|---|
| Ordinary click | Recompute and display the selected view. |
| Shift+click | Emit the compact DIAG V3 summary and display the view. |
| Option+click | Emit DIAG V3 bounded samples and display the view. |
| Shift+Option+click | Run one AUDIT V4 read-only batch for the clicked view; do not paint, change selection or display another view. Top-level Dynasty uses REALMS. |

Public hover copy contains the view name, legend and approved plain-language
description. Modifier mechanics belong in developer/test instructions; do not
add public debug hints to the tooltip.

The full UI investigation, failed layouts and resolution sequence are in
[F-004 GUI interaction history](F004_GUI_INTERACTION.md). A call that selects a
map mode or resets a definition is not proof that prior RGB values were
restored. Court-scene initialization errors remain unattributed; do not call
them harmless or claim a clean log. Context safety, independent global
coverage, stored RGB, pixel comparison, save/load/removal and lifecycle remain
separate open gates under F-005, R-005 and R-009.
