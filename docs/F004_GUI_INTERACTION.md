# F-004 — icon hit-area and modifier-row resolution

Accepted by user on 2026-10-24 in CK3 1.20.1.2 / build 26046173, fresh paused Ismail 867 fixture. This records a bounded interaction result, not engine implementation proof or general compatibility.

## Symptom and investigation

Three custom40x40 icon controls initially rendered fully, but the third/right icon responded only over part of its visible area. Transparent26x26 artwork was already used. The user later observed that holding Shift+Option shifted the row roughly one icon column left and made all icons responsive; release restored the faulty normal state. Exact pixel displacement was not measured.

| Step | Change or observation | Result |
|---|---|---|
| Definition review | Same dimensions, guards, artwork transparency and modifier paths for three icons | No cause established from matching definitions |
| Position control | Exchanged complete first REALMS and third MY_REALM slot blocks | Fault stayed third/right, not with icon identity |
| Final appearance | Removed permanent legend/footer, added native Showing/name/X and hover legends | Appearance accepted; partial right hit remained |
| Slot-frame normalization | Child buttons top-left,100% of40x40 slot | Right hit still failed |
| Direct interleaved row | Removed slot wrappers; six alternating normal/audit buttons in one auto flow | Right became ideal, analogous fault appeared left |
| Modifier observation | Shift+Option changed row position and all hits worked in that state | Isolated state-dependent composition as material clue |
| Final fixed-host composition | One130x40 host, two complete three-button rows sharing top-left parent/widget origin,5px gaps; mutually exclusive visibility at ROW level | User confirms stationary row and correct icon response in tested normal/held/released states |

## Accepted construction

The shared footprint is3*40+2*5=130 logical pixels wide and40 high. Normal row contains REALMS,HOLDINGS,MY_REALM; alternate audit row contains the same three positions. Each child is40x40; decorative icons remain26x26 and mouse-transparent. Two complete flows share an origin within a fixed host. Row-level visibility selects normal versus Shift+Option, rather than interleaved per-button visibility driving the same flow. Existing enabled/player guards and tooltips remain.

Normal controls preserve ordinary computation/display, Shift summary/display and Option bounded samples/display. Audit controls preserve selected-view-only read-only AUDIT V4 without paint or selection callback. The GUI correction does not change native-counter data, classifier semantics, palette, header/X or accepted public tooltip text.

## What this establishes

Controlled observation establishes position/state dependence and confirms the final composition works in the tested build/fixture. It does not prove exactly how the engine combines anchors, autosizing, invisible children, clipping or mouse dispatch. Earlier assertions that a particular texture, precise parent width or invisible overlay caused the bug remain unsupported. The final repair is an explicit layout invariant, not an arbitrary wider hit rectangle or blanket mouse filter.

## Reusable authoring guidance

For mutually exclusive control sets that must occupy identical screen positions, use a stable explicit host and complete alternative rows with coincident origins. Verify press AND release without clicking, then both outer control edges. Treat rendered geometry and hit geometry separately; same-looking definitions alone do not prove alignment. Do not repeat classifier/audit tests when only row composition changes and immutable action/data contracts are verified.

Private installation, hash receipts, original experiments and user-run evidence are preserved under the F-004 local handoffs. Raw screenshots/logs remain private. No save/color restoration, world census, clean-log or broader lifecycle pass follows from this UI acceptance.
