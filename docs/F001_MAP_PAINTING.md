# F-001 map painting and test history

This note explains the bounded implementation that was accepted for fresh
867 Ismail sessions and the evidence behind that acceptance. It does not claim
production lifecycle safety, complete diagnostic data, global coverage, stored
RGB readback, or safety for an existing save.

## Current painting path

The source is the research payload under
[`research/probes/my-dynasty-r016/mod`](../research/probes/my-dynasty-r016/mod).
The three custom map definitions in
[`dynmap_r016_modes.txt`](../research/probes/my-dynasty-r016/mod/gfx/map/map_modes/dynmap_r016_modes.txt)
all use `color_mode = baronies`, native barony names and selection, and five
native zoom profiles. They are three named selections of the same renderer and shared color data,
not separate color stores.

### The visual correction that made grey land readable

The decisive presentation comparison was between the custom Dynasty mode and
native Baronies **using the same already-computed colors**. Native Baronies
showed the desired grey/green presentation while the custom display remained
weak. Static comparison then found the custom definitions lacked native
Baronies' five explicit `gradient_parameters` profiles. The reviewed change
added their resolved numeric values to **each of the three existing custom
modes**: zoom steps **2, 9, 15, 20 and 21**, fifteen profiles in total. These
control fill/edge alpha, widths and lighting blends. The subsequent supplied
three-view screenshots were accepted. No new shader, independent overlay or
change to the classifier/palette was part of that presentation change.

We retained the three custom mode IDs because selecting native Baronies directly
would bypass the Dynasty selection predicates, subview controls, active labels
and legends. Early grey failure did not isolate a universal renderer cause;
this was a targeted configuration correction followed by bounded visual
acceptance. The highest-ruler classification fix below was a **separate**
correction: improved contrast alone could not fix the Bukhara role.

### Computation and projection

Each ordinary click starts from a fresh, guarded living player character P
with Dynasty D. The callback validates that character and Dynasty before
computation. For each county, the classifier follows the accepted F-003
semantics: Dynasty Realms tests the highest ruler T (with H itself as T when
the county holder H is independent), Holdings tests H and then its de-facto
seniors, and My Realm & Dynasty tests P/H membership and senior relationships.
Primary is evaluated before Secondary; Grey is the fallback, including an
unheld county. The Realms self-liege correction makes an independent ruler
count as the highest ruler rather than disappear from that comparison.

For each county role, the corresponding effect traverses
`every_in_de_jure_hierarchy`, filters `tier_barony`, then calls
`set_title_color` on each constituent barony. The fixed intended RGB values are
Primary `(25, 105, 50)`, Secondary `(145, 220, 150)`, and Neutral `(65, 70,
80)`. The map renderer then reads barony colors through the native baronies
map mode. The callbacks compute before selecting/displaying the requested map;
an active-map re-click refreshes it. Returning to a Dynasty view or manually
re-entering also recomputes. Shift adds a summary; Option/Alt adds bounded
samples; Shift+Option/Alt runs the explicit three-view read-only diagnostic
audit. Ctrl adds no separate operation. The map IDs are `dynmap_my_dynasty`,
`dynmap_dynasty_holdings` and `dynmap_my_realm_dynasty`.

All three views write the same mutable title RGB values. Selecting one view
repaints the shared colors, so the implementation does not keep independent
per-view textures or color storage. There is no automatic restoration on
native-map return, context loss, save/load, mod removal, or uninstall. The
Alt+Shift audit suppresses writers and selection; it reports intended/emitted
data, not a readback of stored RGB. No shader or overlay path is involved.

Source anchors: [`scripted_effects/dynmap_r016.txt`](../research/probes/my-dynasty-r016/mod/common/scripted_effects/dynmap_r016.txt)
contains the three role writers and county traversal; [`scripted_guis/dynmap_r016.txt`](../research/probes/my-dynasty-r016/mod/common/scripted_guis/dynmap_r016.txt)
contains guarded character dispatch; the map definitions above declare the
native barony renderer. Semantic precedence and view definitions are in
[`F-003`](tasks/F-003-dynasty-subview-definitions.md) and ADR-010 in
[`DECISIONS.md`](DECISIONS.md).

## Material approach changes

| Problem / approach | Observation and outcome | Why it changed or remains limited |
|---|---|---|
| Early grey map; palette, renderer and classification were all plausible causes | Same-data native/custom display comparison exposed missing native gradient profiles. Five resolved numeric profiles were added to each custom mode; user then accepted the supplied three-view grey/green appearance | This presentation correction preserved classifier, RGB assignments and custom mode IDs. It does not prove a universal shader defect or all zoom/scale coverage |
| Direct title-color writes versus a copy-only helper experiment | The bounded final path uses county classification and direct barony title-color writes. The copy-only helper path was later retired | The exact chronology and causal contribution of each experiment are not fully preserved in the distilled public record; do not assign a stronger cause |
| County classification projected to every barony in its de-jure hierarchy | Current source writes the role color to each filtered barony; a reviewed complete emitted batch had 4,703 counties per view | Emitted records are not an independent county census, stored-color readback, or pixel proof |
| Presentation and three-view interaction | User accepted the supplied grey/green appearance, labels and legends; ordinary and modifier callbacks were observed | Zoom, scale, relationship and transition coverage remains bounded |
| Independent highest-ruler/self-liege correction | Reviewed emitted records place Bukhara in Primary and Darghan in Neutral for the tested fixture | This corrects the observed classifier case; it does not prove every independent-ruler or government case |
| Ordinary route and modifier diagnostics | Fresh player roots, liveness/Dynasty guards, compute-before-display ordering and explicit summary/sample/audit routes remain in source | Broad context-loss and dispatch behavior is still open under R-005/F-005; numeric and framing gaps belong to F-004 |
| Diagnostic probes and retirement | Temporary counter/key probes, trace hooks and tester/baseline controls were removed after use; strict auditing was retained | Nine numeric controls exported positive values while localized summaries showed zero. No numeric cure was established; strict audit stays INCOMPLETE |
| Seven-file cleanup | Source/install equality and 33 existing tests passed, but a later load showed three missing retired-template errors plus two unnamed duplicate-title errors | Static reachability did not establish that saved references were absent. This cleanup was superseded by exact compatibility restoration |
| Nine-file compatibility restoration | Only the exact prior title/CoA declarations and six localization entries were restored; all nine installed files matched source | Three missing-template errors disappeared. Two duplicate-title errors persisted, with unknown cause and save/RGB impact |
| Old-save error disposition | The existing paused session retained two unnamed duplicate-title errors despite the focused icon/selection sequence working by user report | Their cause, affected titles and persistence impact remain UNKNOWN. The accepted bounded feature closeout does not claim old-save repair |
| Bounded source research and new-game controls | Exact helper-key/build/installed-source checks in cycle33 did not identify a duplicate or engine cause. Later new-game comparisons did not reproduce the two duplicate-title errors | This narrows the observed compatibility issue to the tested old-session path; it does not prove the old save is the cause or clean all diagnostics |
| Final two-file UI cleanup, installation and smoke | Diagnostics UI was removed; the installed package was rechecked and the user supplied a screenshot and reported the final ordinary sequence complete | This supports the accepted fresh-session menu/appearance/ordinary interaction scope only; source and install details are preserved in the cycle35 receipt |

Retained landed-title and CoA declarations, plus the six restored localization
names, are inert compatibility data for loaded references. They are not the
current color source or computation path.

## Test and evidence inventory

These are stages of one investigation, not independent incidents when the
same captured log was mirrored into another report.

| Stage / evidence | Expected and observed result | Verdict and limit |
|---|---|---|
| Supplied presentation screenshots and accepted three-view review | Grey/green appearance, labels and legends accepted by the user | PASS for supplied conditions; not every zoom, scale, relationship or pixel pipeline |
| 33 classification, parser and source-routing tests; independent GUI reruns | Existing cases passed, including role precedence, route guards and no-paint audit path | PASS for the tested source contract; not a CK3 parser or runtime guarantee |
| Bukhara/Darghan complete emitted batch | 4,703 counties per view and 14,109 role/intended-RGB records; Bukhara Primary, Darghan Neutral | Agreement observed; strict audit INCOMPLETE because declared counters/completeness were unresolved. Not global coverage, stored RGB or pixel proof |
| Modifier combinations and held-through-release checks | Ordinary, summary, samples and read-only audit paths observed; audit suppresses writes and selection | Bounded route evidence. Historical two audit beginnings and one ending remain; interruption cause and physical click count are unknown |
| Numeric controls, malformed labels and interrupted batch | Nine controls had positive local/exported counts while localized values remained zero; role labels included malformed `ROLEprimary$` forms; one batch was interrupted | Diagnostic acceptance FAIL/INCOMPLETE; no numeric fix, parser relaxation or passed strict audit |
| Package and installation integrity, cycles29/31 | BOM-preserving source preflight passed; seven-file then nine-file source/install equality was checked. The prior payload/log backup, wrapper, manifest and ordered R016-only playset selection were verified and preserved | PASS for those finite file/selection checks; not CK3 parsing, broad compatibility or safe color restoration |
| Cycle 29 cleanup checks | Seven-file source/install equality and 33 tests passed | Those checks did not predict the later saved-session template errors |
| Cycle 30 grouped smoke | Menu gate and ordinary/modifier/native-return callbacks observed; loaded session showed three missing retired-template errors and two unnamed duplicate-title errors | Closure not accepted. Append capture after log reset INCOMPLETE; separate byte-zero startup interval COMPLETE |
| Cycle 31 compatibility recovery | Exact declarations restored; nine-file equality and same 33 tests passed; three template errors absent, two duplicate-title errors remained | Partial compatibility recovery, historically FAILED for closure. No save edit or RGB persistence proof |
| Cycle 32 debug-UI cleanup and cycle 33 duplicate-title source research | The unused debug toggle/panel and three UI-only text keys were removed. Exact helper-key checks in installed title/CoA/localization sources and build metadata did not identify the cause of duplicate-title errors | No title fix was justified; retained helper declarations were not deleted speculatively. No new gameplay or diagnostic data-audit pass |
| Cycle 34 new-game control | Startup append interval INCOMPLETE after reset; separate byte-zero startup captured runtime 1.20.1.2, enabled/mounted mod and both GUI completions. New-game capture ended on a partial debug line | Startup bounded evidence COMPLETE; overall new-game capture INCOMPLETE. Complete error-channel lines contained zero duplicate-title entries and zero dynmap mentions; other errors remain unattributed |
| Cycle 35 final cleanup install and fresh-game smoke | User confirmed final smoke steps and supplied screenshot of removed diagnostics UI. Error channels 34/35 match after timestamp normalization | Fresh-game comparison did not reproduce the two duplicate-title errors; not a universal clean-log result. Overall smoke capture INCOMPLETE due to final partial debug line |

The menu checks for cycle34/35 were finite observations, not proof for every
campaign or save. No fresh runtime test, source bug fix, or diagnostic audit is
part of this closeout preparation.

## Earlier test sequence and failed approaches

The following dated ledger supplements the grouped inventory above. It is
reconstructed from the preserved pre-distillation F-001/README journals and
per-stage results. Each row is an observation or preparation/checkpoint, not
an additional independent runtime experiment. Original raw captures, failed
commands, exact hashes and lifecycle results remain private and preserved.

| Date / stage | Action, result and resulting decision |
|---|---|
| 2026-10-21: menu/icon preparation and install | One Dynasty parent and three native-style children retained; temporary repeated shield explicitly accepted. Source/installation checks did not themselves accept map output or runtime syntax |
| 2026-10-21: first startup failure and trace repair | Six error entries reported three trace/watch scope targets used but never set in reachable script. Their setters existed only in the future console recipe. Loaded diagnostic setup was corrected to capture the player and two nominated titles; guards and cleanup retained. Corrected startup subsequently passed its bounded gate |
| 2026-10-21: console invocation and nine-barony trace | First console recipe was rejected; a compact explicit title-rooted caller executed. Branch/write receipts and the Bukhara category discrepancy were retained. Issued writes were not stored-color or pixel readback |
| 2026-10-21–22: display isolation | User attributed weak display to custom Realms and good grey display to native Baronies. Crops/zoom differed, so exact matched-camera parity was not claimed. Follow-up static comparison isolated missing explicit gradient profiles; source preparation verified all fifteen profiles, then installed/startup/three-view visual checks accepted the bounded presentation |
| 2026-10-22: read-only classification audit | Eleven completed compute passes (Realms4/Holdings4/MyRealm3) lacked decisive per-county identity/RGB receipts; screenshots could not be tied to exact computations. Classification remained UNVERIFIED, prompting an explicit identity/roster audit |
| 2026-10-22: first full dump, incomplete | Roster4703; 3368 closed Realms records plus one open, no later views or batch ending. In3147 supported closed records,3116 matched and31 shared the Nasr-terminal discrepancy. Another221 frames exposed valid runtime Dynasty IDs with empty database keys. Neither incomplete stream nor parser fix was converted into a full pass |
| 2026-10-22: self-liege and parser/V2 fixes | Raw Nasr identity showed self-liege/self-top and independence. Replaced the two incorrect no-liege terminal assumptions with supported self-top logic; runtime-only Dynasty identity parsing and compact actor/roster grammar addressed the separate parser/output boundary. Writers and accepted presentation remained unchanged |
| 2026-10-22: modifier preparation rejected in part | Useful classifier/parser/backend corrections were retained, but an unproven Alt/combined dispatch or conditional void-selection API was not accepted. GUI selected mutually exclusive icon variants using documented Shift/Alt booleans and ordinary button actions, with audit-only combined route |
| 2026-10-22: side modifier tester and cleanup correction | Side tester was used to isolate physical modifier delivery before production bindings. Startup found references to retired legacy trace input targets; the scoped correction and subsequent installation preserved original negative evidence. Do not interpret source/test passes as runtime delivery proof |
| 2026-10-23: grouped runtime and diagnostic investigation | Ordinary and modifier callbacks plus a complete emitted three-view batch were observed. Nine numeric controls showed positive local/exported counters but zero localized totals. A second batch began without ending; actual click count and interruption cause remained unknown. No deduplication or invented ending was used |
| 2026-10-23: production modifier contract and bundle | Existing 33 source/parser/classifier tests and exact installation checks passed; held-through-release ordinary/Shift/Option/combined gestures were user-tested. Combined audit left the active view unchanged as intended. Formal numeric audit remained INCOMPLETE; sample bounds were observed despite malformed role labels |
| 2026-10-23: closeout29–31 | Cleanup, missing-template regression, exact inert compatibility restoration and two unresolved old-session duplicate messages are separately recorded above; cycle31 remains FAILED for its historical closure contract |
| 2026-10-23: closeout32–35 | Debug UI removed; bounded duplicate research yielded UNKNOWN; fresh-game control then final installed-cleanup smoke did not reproduce the two old-session duplicate errors. The user confirmed all requested ordinary view/legend/selection/native-return/re-entry actions, including default Realms on re-entry |

This ledger preserves the distinction between **presentation configuration**,
**semantic classification**, **runtime diagnostic plumbing**, and **loaded-state
compatibility**. Success in one did not establish the others. The final accepted
scope and unresolved owners are set out below.

## Residual owners and disposition

The accepted scope is the bounded menu, appearance and ordinary interaction on
fresh 867 Ismail sessions. F-004/#29 owns counter rendering, strict framing,
malformed sample labels, interrupted batches and court-error attribution.
F-005/#30 owns functional/UX follow-ups and the unresolved old-save error
disposition; R-005/#5 retains context/no-Dynasty research, and R-009/#9 retains
exact color restoration, save/load and removal research. Those issues remain
open. No lifecycle waiver, global census, automatic restoration or old-save
repair is claimed.
