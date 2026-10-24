# F-004 — Dynasty Map diagnostics hardening

Issue: [#29](https://github.com/mhaduk/ck3-dynasty-map/issues/29).
Functional successor: [F-005 / #30](https://github.com/mhaduk/ck3-dynasty-map/issues/30).

## Bounded closeout result — 2026-10-24

**User-accepted scope:** the diagnostic and icon-interaction acceptance below
is complete for the fresh paused Ismail 867 fixture on CK3 1.20.1.2 / Steam
build 26046173. The user authorized issue closeout, documentation and cost
publication, safe local cleanup, and scoped Git publication. GUI independently
verified saved-session hashes, counters and exact cost arithmetic; all 55
focused parser tests pass. Issue #29 is closed completed with the canonical
cost table and `ai-cost-table-format` label verified by published-body readback.
Wiki publication `d5f08ac` and both published pages were read back and matched.
No further game test is requested.

| Accepted evidence | Result and limit |
|---|---|
| DIAG V3 native summary and samples | Native `debug_log_scopes` declarations supply real values across the twelve named counters. Holdings, Realms and My Realm samples remain within ten samples per role and twenty details; the observed role sample counts were Holdings 10/10/10, Realms 10/3/10 and My Realm 2/10/10. These are bounded samples, not a full-map audit. |
| AUDIT V4 REALMS | PASS: 4,703 declared/emitted counties/results, 1,854 actors; Primary 31, Secondary 3, Neutral 4,669; role and intended-RGB agreement; attempted writes 0. |
| AUDIT V4 HOLDINGS | PASS: 4,703 counties/results, 1,854 actors; Primary 16, Secondary 18, Neutral 4,669; role and intended-RGB agreement; attempted writes 0. |
| AUDIT V4 MY_REALM | PASS: 4,703 counties/results, 1,854 actors; Primary 2, Secondary 32, Neutral 4,669; role and intended-RGB agreement; attempted writes 0. |
| Stable modifier rows and hits | User accepts a fixed 130×40 host with two complete three-button rows at a shared origin, 5 px gaps, 40×40 controls and 26×26 transparent artwork. Holding/releasing Shift+Option leaves the host stationary and tested icon hits work. The engine's internal layout cause is not proven. See [interaction history](../F004_GUI_INTERACTION.md). |

Each V4 PASS is relative to the emitted roster for one selected view/build and
fixture. No independent world census, stored-RGB getter, pixel comparison,
save/removal, global coverage, or lifecycle safety is claimed. Earlier failed
and truncated audit captures remain preserved. The latest samples operation
has complete operation framing, but its file interval has an unrelated partial
boundary and the overall sample-only analysis remains INCOMPLETE. Initialization
and court-scene errors remain unattributed; this is not a clean-log claim.

Elapsed timing is excluded from F-004: [R-018 / #38](https://github.com/mhaduk/ck3-dynasty-map/issues/38)
retains open feasibility research and [F-006 / #39](https://github.com/mhaduk/ck3-dynasty-map/issues/39)
remains planned/blocked on that research and GUI design approval. F-005 / #30
retains residual old-save/functional/artwork questions; R-005 / #5 and R-009
/#9 retain context and exact RGB/save/removal ownership. The closeout
recommendation is **completed for the accepted bounded scope**, with those
limits explicit.

### Finite saved-session cost account

<!-- ai-cost:start -->
## AI cost

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| `gpt-6.1-sol` | 58,164,560 | 57,324,288 | 840,272 | 108,473 | 58,273,033 | $14.14955400 |
| `gpt-6-luna` | 81,577,903 | 80,017,792 | 1,560,111 | 387,093 | 81,964,996 | $1.14973552 |
| `codex-auto-review` | 45,779 | 27,648 | 18,131 | 220 | 45,999 | N/A — model rate unavailable |
| **Total** | **139,788,242** | **137,369,728** | **2,418,514** | **495,786** | **140,284,028** | **$15.29928952** |

Method: `task-ai-cost/1` with explicit response/turn mapping and an independent
per-response recomputation. Finite cutoff: 2026-10-24T11:20:00Z, the frozen
completion boundary for the selected saved source prefixes. Coverage is partial:
56 assigned GUI turns, all 10 identified F-004 CLI sessions in the allowed
2026-10-23/24 roots, and two linked review turns yielded 944 assigned response
records; four unrelated GUI responses remain unallocated. External advice
sessions had no separately accessible counter source, and responses after the
cutoff (including later closeout/report maintenance) are excluded. `codex-auto-review`
is measured but unpriced. N/A does not mean zero usage.

The official OpenAI API Standard prices fetched on 2026-10-24 apply the
per-request `input_tokens` tier: 126 `gpt-6.1-sol` responses exceed 272,000
input tokens; no `gpt-6-luna` response does. Cache-write counters were recorded
as zero. Cached input and reasoning output are subsets, not extra addends. This
is an API-equivalent estimate, not actual API billing or ChatGPT subscription
cost. Rates and sources: [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol),
[GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna), and
[API pricing](https://developers.openai.com/api/docs/pricing). GUI independently verified arithmetic from frozen saved sources; the published
issue table was read back and matched (`ai-cost-table-format`: PASS).
<!-- ai-cost:end -->

The full prior dated research journal is retained below. The accepted final
state does not erase earlier failures or upgrade their verdicts.

Status: OPEN follow-up, created 2026-10-23 from the bounded F-001 closeout.
This ID supersedes the former local icon-only use of F-004. That historical
record is preserved; outstanding artwork belongs to F-005. No diagnostic fix
or additional runtime experiment is implemented by this planning record.

## Accepted evidence and limits

User accepts the supplied native-like grey/green appearance of all three views.
Ordinary, Shift summary, Alt bounded samples and Alt+Shift read-only audit
callbacks were observed in the accepted F-001 batch. One complete emitted batch
has 4,703 counties per view and 14,109 role/intended-RGB agreements; Bukhara is
Primary and Darghan Neutral. These are emitted-record observations, not an
independent world census, stored-RGB getter or pixel verification.

Nine temporary controls found positive local counters and exported values while
localized numbers remained zero. The documented `SCOPE` → `TopScope.GetValue`
named accessor is legal; no cure is proven. A proposed `|0` formatting change
was not applied or tested. Strict analysis remains **INCOMPLETE**. Two audit
beginnings and one ending were observed; the second batch's interruption cause
and physical click count are unknown. Court-scene invalid-character errors
remain separately unattributed.

## Bounded work and acceptance

| Need and actual evidence | Impact | Minimum follow-up | Acceptance and stop condition |
|---|---|---|---|
| Numeric rendering/count contract: positive controls coexist with localized zero | Declared totals cannot certify completeness; summary numbers are unreliable | Isolate one documented export/localization boundary with a positive and zero control; review target-build contracts before changing it | Actual values render correctly and reconcile with independently counted records, including genuine zero; stop on the first unresolved boundary and record it, never substitute synthetic positive counts |
| Strict completeness: zero roster/view counters and an unfinished second batch | Formal full-world acceptance remains unavailable despite record agreement | Preserve batch boundaries, missing endings, count disagreement and provenance; compare one finite complete capture to the independent analyzer | Missing/duplicate records, partial lines, zero/contradictory declarations and interrupted batches remain INCOMPLETE; complete valid fixtures pass. No deduplication based on assumed clicks |
| Bounded readable output: actor/roster backend is useful, complete audit is large | Repeated full dumps burden diagnosis; callbacks are not counts | Retain one summary and bounded samples, measure actual output against existing 10-per-role plus 20-detail limits, keep full audit explicit | Useful counts/identities fit the documented bounds; full audit remains opt-in and suppresses paint/display/selection changes; stop if a proposed optimization weakens evidence |
| Observed sample text includes `ROLEprimary$` | Sample role formatting is ambiguous to readers/parsers | Capture and isolate one real formatted sample, preserving raw evidence; review substitution grammar without speculative store rewrites | Role text and identity are readable and correctly parsed for each role; malformed/unknown tokens cannot become acceptance evidence |
| Court-scene invalid-character errors, attribution unknown | Cannot claim clean runtime or harmlessness from unrelated channels | Request a matched control only if this error blocks a concrete feature gate; separate timing, source and context from map callbacks | Evidence either attributes the error and records recovery, or explicitly leaves attribution unknown and names blocked tests. Do not classify it harmless without proof |
| Automated runtime diagnostic verification | Offline parser/source checks cannot validate engine delivery or stored colors | Reuse bounded log capture and strict independent analysis over user-run checkpoints; preserve frozen input hashes, receipts and actual user action reports | One end-to-end checkpoint distinguishes callback observation, interval completeness, semantic agreement and acceptance; failures remain visible, with no skip/expectedFailure or invented data |

Stop after the scoped hypothesis/control batch. Further research requires a
concrete remaining question; do not resume an indefinite numeric-cure loop.
Temporary COUNTERPROBE/KEYPROBE scaffolding is retired after preserving its
accepted evidence. Runtime diagnostics, compact actor/roster audit grammar,
sample bounds, cleanup guards and the strict independent analyzer remain.

## Ownership

[F-001](F-001-dynasty-map-ux.md) / [#20](https://github.com/mhaduk/ck3-dynasty-map/issues/20)
owns the delivered menu/appearance and final cleanup smoke. F-005 owns residual
functional/UX acceptance; R-005 / [#5](https://github.com/mhaduk/ck3-dynasty-map/issues/5)
owns context/no-Dynasty research, and R-009 / [#9](https://github.com/mhaduk/ck3-dynasty-map/issues/9)
owns exact RGB restoration/save/removal. Diagnostics work grants no lifecycle
waiver. Target evidence is CK3 1.20.1.2 / Steam build 26046173; generated API
provenance retains its recorded build limits.

## Cycle30 verification — 2026-10-23

One finite five-log test interval is COMPLETE. Shift Realms produced one
SUMMARY receipt, Alt Holdings one SAMPLES receipt, and the combined modifier
one full audit with one beginning and one ending; no reject or retired
COUNTERPROBE/KEYPROBE markers occurred. Raw sample text remains malformed
(`ROLEprimary$`, `ROLEsecondary$`, `ROLEneutral$`): 10 samples per role and
20 Neutral detail records were observed, within the existing bounds. This is
an output-count observation, not a strict grammar pass.

The unchanged strict analyzer ran once on the exact contiguous full batch:
exit 2, INCOMPLETE. It parsed 4,703 roster counties, 1,854 actor definitions
and 14,109 view records (4,703 per view); declared roster/actor/view counts
remain zero. All emitted intended RGB values match the fixed role palette,
and all audit records say writes suppressed. Strict classification and RGB
verdicts remain UNVERIFIED; no new independent role-agreement, census,
stored-RGB or pixel claim follows. This batch ended; the historical second
unfinished batch and its unknown cause remain historical evidence.

At load, the error channel contains 57 invalid-character court trigger blocks
and one court culture-set failure, separately unattributed. New retired-helper
title-template/load errors block cleanup readiness and are tracked by F-005;
they are not explained away by the known numeric diagnostic gap.

## Cycle31 retained diagnostic limits — 2026-10-23

The final focused recovery check observed one full audit beginning and ending,
no rejection and no retired probe markers. The user confirmed the requested
paused icon/selection sequence worked as expected; this is a human report,
not a stored-color or selected-map-ID getter. Runtime bodies and the strict
analyzer/tests are unchanged; the known zero-count contract remains INCOMPLETE
without another redundant analyzer run. The loaded interval again contains
57 court invalid-character blocks plus one culture-set failure, separately
unattributed. Three missing helper-template errors disappeared after exact
declaration restoration, but two unnamed duplicate-title errors persist under
F-005 and continue to block F-001 closure. No numeric/court cure is claimed.

## F-001 bounded closeout ownership — 2026-10-23

The user accepts the delivered F-001 menu, appearance and ordinary interaction
on fresh 867 Ismail sessions and directs narrowed feature closure. Cycle34/35
complete error-channel lines did not reproduce the earlier two unnamed
duplicate-title errors; overall captures remain INCOMPLETE at a partial final
debug line. This disposition does not change F-004 ownership: numeric rendering,
strict framing/completeness, malformed sample labels, interrupted-batch
robustness and court-error attribution remain OPEN here. The user has not
accepted a clean diagnostic contract or a harmlessness attribution.

## F-004-DEBUG-PREP-20261023-01 — preparation attempt

The named READY handoff was picked up for local preparation. Static review
confirmed the target build as CK3 1.20.1.2 / Steam 26046173 and found that the
native `icon_button_mapmode` frame is 40×40 with a full-size button and
decorative child icon; this payload had reduced Additional Maps instances to
32×32. The mod's view slots already use 40×40 buttons with 26×26 transparent
icons and 4–5 px separation. The shared Additional Maps parent retains native
`filter_mouse = all`; no evidence justified changing its inheritance or
stacking. The 13 mod-created native-style Additional Maps icons now use 40×40.
This remains a static hit-area candidate; Dynasty/My Realms boundaries,
click-through and native icon interception require the user-run checks below.

The prior numeric diagnosis was reused. It ruled out an unsupported
`SCOPE.GetValue` overload claim: generated target docs say uppercase SCOPE is
TopScope. It isolated the unknown to localized evaluation/context. The
existing TOTAL field now has the documented native numeric `|0` formatting
candidate while the other eleven expressions and counter stores remain intact.
The sample-role marker removes the trailing `$` which appeared in the observed
`ROLEprimary$` text. Neither correction is runtime-verified; the nine-control
finding is not repeated or promoted to a PASS.

Timing feasibility review found only profiler frame/current-frame APIs in the
preserved generated GUI docs (`PdxProfilerGetFrameTimeMs` and
`PdxProfilerGetCurrentFrame`). They report profiler frame information and do
not expose a start/stop elapsed interval spanning the scripted-GUI dispatch,
cleanup, classification, projection and pre-selection callback. No supported
synchronous elapsed source or presentation-completion event was established;
timing remains NOT IMPLEMENTED / UNKNOWN and renderer completion UNKNOWN.

This attempt is incomplete. Top Dynasty now shares REALMS ordinary/Shift/Option
routes, but Shift timing is absent and Shift+Option still calls the historical
all-three V2 audit. Selected-view-only V3 framing/backend, strict V3 analyzer
and its negative fixtures were not implemented. Historical V1/V2 meanings
remain unchanged. No installation, app action, or game test is authorized by
this preparation. See private bounded evidence and the proposed user-run
checkpoint order in `.codex-sync/F004-PREP-20261023-01/`.


## F004-DEBUG-FIX-20261023-02 — selected-view correction preparation

The failed preparation candidate is superseded for current local review by this
scoped correction; its original status, evidence and GUI review remain
historical. Three Shift+Option entry points now dispatch explicit V3 selected
REALMS, HOLDINGS or MY_REALM backends. Each shares one actor/roster setup and
cleanup path and calls only its named classifier. The top Dynasty entry uses
REALMS. The V3 analyzer preserves V1 and V2 FULL meanings and independently
reconstructs F-003 role semantics from actor/roster relationships. It rejects
missing, extra, wrong-view, duplicate, malformed, contradictory, zero, rejected,
partial and interrupted evidence. A V3 PASS is limited to its named view; the
three views require three separate batches.

All 16 mod-created native Additional Maps instances remain 32×32, matching the
installed 1.20.1.2 native instances. The earlier preparation's count of 13 was
an undercount; direct review covered four rows. Its prior 40×40 enlargement was
reverted because it had no demonstrated value for custom Dynasty/My Realm
clicks. The custom Dynasty and three subview slots retain their existing 40×40 button
frames, 26×26 transparent artwork, fixed layout and current parent filtering.
Static source shows the native circle artwork and nested round button; actual
mask hit testing, overlays, parent/child interception and click-through remain
runtime checks.

Bounded samples now use literal lower-case role markers for Primary, Secondary
and Neutral. This removes the uncertain parameter interpolation from those
labels; engine log delivery remains unverified. The existing TOTAL `|0` format
remains a source-supported discriminating candidate from the accepted narrow
numeric diagnosis, not a demonstrated cure. Other counter expressions and
stores are unchanged. Shift elapsed timing is NOT IMPLEMENTED / UNKNOWN because
the reused target-build review found no documented synchronous elapsed source;
renderer completion remains UNKNOWN.

Offline classification tests: 41 passed. Target-version source preflight:
passed for 9 files. These checks do not establish CK3 parsing, runtime
compatibility, actual hit areas, numeric localization behavior, or renderer
completion. A minimized one-session user checkpoint plan is in the private
handoff. No installation/game action, staging, commit, publication or GitHub
write occurred. GUI review and any later installation/runtime authorization
remain required.


## User scope update and installation — 2026-10-23

Timer measurement is explicitly excluded from F-004 acceptance/tests. R-018 / #38 owns further feasibility analysis; F-006 / #39 owns later approved implementation. Existing negative timing findings are reused, not treated as proof of impossibility.

User declared CK3 closed and launcher open and authorized file replacement and testing. GUI preserved the prior payload/wrapper, startup logs and enabled-mod manifest privately, installed the accepted selected-V3 candidate, and passed source/installed equality preflight for all 9 files. Five payload files changed; wrapper and prior playset selections remain unchanged. GUI verified the existing test playset with R016 alone enabled. Startup/runtime gates remain pending; this is not a diagnostic pass or task closure.


## First selected-view runtime checkpoint — 2026-10-23

User reports ordinary/modifier behavior passes except the My Realm & Dynasty hover/hit boundary; other icons behave correctly. Supplied screenshot has no cursor, so exact obstruction remains unknown. Bounded complete file capture parses readable samples within 10-per-role/20-detail bounds for all three views. Numeric summaries and roster declarations remain zero: the TOTAL formatting candidate did not cure the boundary. One selected REALMS audit has an ending and 4703 emitted results, but contradictory declarations keep strict acceptance INCOMPLETE/UNVERIFIED. The available second HOLDINGS audit has no ending; no MY_REALM audit frame is observed before the saved cutoff. Cause remains UNKNOWN; normal user exit/final flush check is pending before any retest. Error-channel initialization/court messages remain unattributed. No full diagnostic pass or clean-runtime claim.

## Final-flush review and bounded runtime correction — 2026-10-23

After the user closed CK3 normally, the same frozen debug bytes were observed:
15,224,546 bytes, unchanged from the pre-exit capture. This shows that the
final-exit check added no bytes; it does not identify why the audit stopped.
The file interval is complete at its declared capture boundary, while strict
V3 analysis remains INCOMPLETE: the REALMS batch has 4703 emitted county
records and 1854 actor definitions but zero declarations, and a following
HOLDINGS frame ends mid-roster without its matched end. No MY_REALM frame is
present in the captured bytes. Initialization/court errors remain
unattributed. Do not infer a missed click, flush cause, or clean runtime.

The numeric source path was traced from script locals through
`save_scope_value_as` snapshots to localization on the player-root dispatch
and nested player-scope writers. Existing guards, setup order and cleanup do
not establish which saved-value table the localized `SCOPE.GetValue` reads.
The native `|0` TOTAL candidate already failed to change observed zeros.
No further source correction is supported. Keep analyzer zero/contradiction
rejection intact. A future GUI decision could authorize one existing
TOTAL-field comparison of the same positive saved key through dispatch-root
and nested-writer contexts; include a true-zero case only if available without
a new carrier or gameplay mutation. Keep declarations independent from emitted
records.

The hit-area comparison found the three custom slots share 40×40 slot and
round-button geometry, centered 26×26 transparent icons, and the same enabled,
modifier and callback structure. The third icon uses a different texture, but
the evidence does not show its loaded alpha mask or runtime hit-test shape.
Installed 1.20.1.2 sources show the native round frame and circle-mask artwork;
they do not document mask hit testing, sibling interception, clipping or
hover propagation. User observation is that the cursor hand appears before
highlight and highlight begins farther inward; the supplied screenshot has no
cursor. Cause remains UNKNOWN. No geometry or mouse-filter edit is supported.
A future minimal check should show the cursor at the failing outer edge and
one working sibling at the corresponding edge, with highlight state visible.

V3 logging emits actor definitions, every county identity/holder record and
selected-view results. Reviewed target API evidence does not document a
debug-log byte/rate cap. Reducing those records would remove evidence required
for independent actor graph, roster and selected-view checks; no safe
reduction or framing repair is justified. The HOLDINGS truncation and absent
MY_REALM frame remain UNKNOWN among logging limit, callback interruption and
actions performed. Keep interrupted batches INCOMPLETE. No source, analyzer or
test change was needed in this continuation; V1/V2/V3 and sample contracts
remain unchanged.

Future retest is limited to: (1) after GUI acceptance and a separately
authorized install, check the My Realm edge and matching working sibling edge;
(2) run the approved numeric receiver comparison with positive and true-zero
values; and (3) invoke only missing individual selected audit(s), each once,
then compare the final capture. User alone manages launcher/game and performs
all UI actions. Before any future file replacement, require CK3 and launcher
closed; user alone starts CK3 afterward. Do not repeat accepted icon behavior,
all nine controls, or a broad three-view run.

## F004-PROBE-PREP-20261023-05 — GUI-selected diagnostic candidate

The current local candidate makes one reversible fixed-slot position change:
the complete REALMS and MY_REALM 40×40 slot blocks exchange first/third
positions; HOLDINGS stays in the middle. A private byte-exact pre-change copy
is preserved in the per-ID handoff. A structural test checks the new order and
identities. This is a position control only; no hit-area enlargement, filter,
art, callback, guard or style change is intended. The result of a future paired
edge observation cannot by itself prove mask behavior versus overlap.

The REALMS Shift summary path now logs the same once-computed and exported
`dynmap_r016_out_total` through two adjacent diagnostic boundaries: inside the
saved player writer (`NESTED_WRITER`) and, after that scope block returns,
through the dispatch root (`DISPATCH_ROOT`). Top Dynasty already dispatches to
this same REALMS summary. Each line is labeled as a receiver experiment and
uses the existing `SCOPE.GetValue(...)|0` form. An unavailable player path emits
`UNAVAILABLE`; no value is substituted. A guaranteed zero saved control is not
available in this unchanged gameplay path, so zero-control comparison is
explicitly omitted. No new counter, persistent variable, gameplay mutation,
scan, carrier, or audit/schema change is introduced.

Pinned 1.20.1.2 generated docs describe uppercase SCOPE as TopScope,
`TopScope.GetValue(Arg0)` as the named numeric lookup, and `save_scope_value_as`
as an event-chain named numeric target. A shipped saved-value localization
example uses the same native `|0` form. These sources support the selected API
shape, not the unresolved question whether `debug_log` localization in both
caller contexts sees the same saved-value table or renders the correct value.
The candidate is therefore an experiment, not a numeric cure. The existing V3
count declarations, parser acceptance and zero/contradiction rejection remain
unchanged. Full audit output is still incomplete/truncated and no engine output
limit is established.

No installation or game/launcher action is part of this preparation. The
minimal future check is GUI review first, then separate install authorization;
with both apps closed before replacement, the user alone starts CK3 and checks
the main-menu log gate before loading a fresh paused fixture. Observe the paired
first/third hover boundary and run one REALMS Shift comparison through either
the top Dynasty entry or the REALMS subview; both share the same summary path.
Do not run broad audits here. If a later audit is approved, run HOLDINGS-only
before another full audit; keep MY_REALM as separate missing evidence. Capture
boundaries and output-limit cause remain unknown. F-004 stays open.


## Final native-style UI preparation — 2026-10-24

The GUI-approved banner candidate restores icon order to REALMS, HOLDINGS,
MY_REALM. It removes the old persistent three-category legend and lower Realms
button. Each view button now uses the native tooltip placement convention and
describes its own Dark, Light and Grey categories without modifier/debug
instructions. The native `MAP_MODE_SHOWING_HEADER` localization is displayed
above the active view name in a compact header using the shipped title texture,
`Font_Size_Medium` and `text_map_mode_header` style. A native `button_close`
returns to Realms and retains the shipped `close_window` shortcut. The separate
custom header is visible only for the three Dynasty modes; hover itself has no
scripted callback. Exact hover latency, visual layout, pointer coverage and
runtime refresh behavior remain unverified. The inspected native map icon uses
ordinary `tooltip` plus `tooltip_nw`; no per-control immediate-delay property
was established, so no global tooltip setting or custom polling was added.

The two-context receiver experiment was removed from the REALMS summary effect
and its localized records. Its last bounded runtime output recorded TOTAL 0 at
both `NESTED_WRITER` and `DISPATCH_ROOT`; it did not resolve the receiver
boundary. Ordinary DIAG V2 `UNAVAILABLE` output remains, and the analyzer's
strict zero/contradiction rejection is unchanged. Existing target-build source
evidence supports `SCOPE.GetValue(name)` as a documented named TopScope value
and supports the saved-scope numeric target shape, but does not establish which
saved-value context `debug_log` localization observes. No numeric cure or
weakened audit contract is claimed. Do not repeat the nondiagnostic zero/zero
comparison. GUI should decide whether to keep this as an open diagnostic gate
while reviewing the UI, or commission separate bounded source research into
the unresolved `debug_log` localization context.

Focused classification/source tests pass (45). Target-version file preflight
is recorded in the private handoff; these checks do not prove CK3 GUI parsing,
hover delay, visual acceptance, renderer safety or clean runtime. The scoped
verification recovered stale evidence/source paths, an initially malformed
test assertion, an append-context mismatch and one stale handoff revision; each
was resolved from the current file manifest or persisted status, then the full
focused suite passed. Suggested workflow improvement: resolve historical paths
with `rg --files`, inspect append context, and read persisted status before each
helper transition; rerun the scoped suite after changing test source.

No install, launcher/game action, new capture, staging, commit, publication or
GitHub write is part of this preparation. After GUI review and separate install
authorization, one consolidated user-run session should verify manifest/wrapper
and installed-file equality first, pass the startup main-menu gate, then check
the three tooltip cards, icon order/edge coverage, `Showing:`/selected name,
close action, configured native close-window shortcut and map parity. Stop before save loading or diagnostic
work if startup produces an attributed error or unexpected mount. Any later
numeric comparison or missing selected-view audit remains a separate GUI
decision. F-004 remains open; R-018/F-006 timer work is excluded.

## Native tooltip and hit-frame correction — 2026-10-24

The three child hover strings now use a native `#T ...#!` title, one concise
mode-description line, a blank paragraph, and separate bold Dark, Light and
Grey rows. Their category meanings remain those defined in F-003; the top-level
Dynasty tooltip remains an ordinary short description. The strings use escaped
`\n` sequences in one localization value, following installed map-mode
descriptions.

The six ordinary/audit child buttons now anchor at the top-left of their
40×40 wrapper and size to 100% of it. This makes each button frame use the full
wrapper bounds while preserving the centered 26×26 transparent artwork and
the three-slot row geometry. Installed `gui/shared/buttons.gui` defines
`button_round` as a `button_icon` subtype with a 40×40 default frame and shows
`icon_button_mapmode` sizing the nested `button_round` to 100% of its parent;
the native `gui/shared/mapmodes.gui` map-mode controls likewise use nested
100%-sized buttons. This supports the chosen frame normalization. Static source
cannot establish engine hit testing or prove that the third icon's right edge
now responds; that remains a minimal user-run runtime check.

Dispatch, map-mode selection, the selected-only V3 audit path, tooltip timing,
icons, header, close action and palette behavior are unchanged. Hover remains
inert; no legend, footer, callback, timer or debug hint was added. Source tests
cover the six full-slot button frames, tooltip structure and existing dispatch
invariants. Preflight and focused-test results are recorded in the private
handoff. The runtime hit correction and rendered tooltip layout remain pending
GUI review and separately authorized installation.


## User-approved public tooltip copy — 2026-10-24

User accepted public-facing Shows descriptions, Dark/Light/Grey definitions and explicit independent/highest-ruler explanations for all three views. Saved exact approved wording to the three tooltip localization entries with native title/paragraph formatting. No classifier, dispatch or palette change. Existing layout test now checks structure instead of freezing the retired description sentences. Not installed yet. User accepts latest layout/tooltip formatting; third/right half hit fault persists after frame normalization. Shift callback is observed complete, numerical output remains zero. Next source work must address the actual positional interception/bounds and numeric emission contracts, without repeating passed UI/Shift tests.

## Scope dump and direct-flow hit diagnostic candidate — 2026-10-24

Inserted one `debug_log_scopes = yes` after the REALMS summary snapshot and
immediately before its existing localized count line, in the same saved
diagnostic-player scope. Generated target-build `effects.log` pinned to CK3
1.20.1.2 / Steam 26046173 documents only that `yes` logs full scope info; it
does not say numeric saved values are included. Positive named numeric output
alongside SUMMARY zero would strengthen a logger/localization-context
hypothesis. Missing numeric entries remain inconclusive. The existing
same-name vanilla saved-value/localization pairs disprove a general
incompatibility claim; no documented explicit saved-value injection interface
for `debug_log` was found in the pinned generated effect contract.

Removed only the three intermediate slot widgets in the custom subview row.
The six normal/audit `button_round` controls are now direct children of the
horizontal `flowcontainer`, in REALMS, HOLDINGS, MY_REALM pairs, each explicitly
40×40 with `ignoreinvisible = yes` on the row. Existing mutually exclusive
visibility expressions and the former `GetPlayer.IsValid` slot guard keep one
control per logical position visible for ordinary, Shift-only and Alt-only
states versus combined Alt+Shift audit, while retaining hidden slots without a
valid player.
Target 1.20.1.2 vanilla `hud.gui` and `window_military.gui` show ordinary
button controls directly under flowcontainers with `ignoreinvisible`; this
supports syntax/composition, not this candidate's runtime geometry or hit
behavior. Callbacks, order, 5px spacing, 26×26 icon children, hover bindings,
selection state, header and close control are retained. The change tests
intermediate-boundary/interception as a candidate; it is not a proven fix.

Focused tests now assert direct button order, explicit frames, paired visibility
and the single scope-dump boundary. Localization bytes remain at the frozen
user-approved hash. The private restore manifest maps this task's original
owned source bytes to the immutable handoff baseline. Installation and runtime
remain pending GUI review; no numeric output, layout geometry or hit test is
accepted by this preparation.


## Full-scope experiment outcome — 2026-10-24

A single full scope dump immediately after REALMS snapshot and before localized SUMMARY contains all 12 named saved numeric targets, including TOTAL 4703, Primary 31, Secondary 3 and Neutral 4669; the immediately following localized SUMMARY reports all zeros. Expected current/root identity is observed. This strongly supports a logger/localization access-context gap rather than absent snapshot values or simple lifetime/formatting failure; exact engine implementation remains unknown. File interval is COMPLETE; this does not confer strict audit/classifier acceptance. User reports direct-row candidate fixes right MY_REALM but creates analogous left REALMS hit failure: no overall hit-area cure accepted. No further repeated clicks needed for this experiment.

## F004-COUNTERS-HIT-20261024-15 — combined preparation result

The active summary/sample callbacks now use DIAG V3 and pin source
`F004_NATIVE_14`, CK3 1.20.1.2 / Steam build 26046173. They compute once,
snapshot the existing twelve `dynmap_r016_out_*` counters once, and frame one
native `debug_log_scopes = yes` block. The localized zero SUMMARY is no longer
used as an authoritative declaration. Samples retain their 10-per-role and
20-detail limits.

The selected audit now uses AUDIT V4. It emits one native roster/actor block
with only `out_roster` and `out_actors`, then a separate selected-view block
with the twelve snapshotted counters. The analyzer accepts complete,
build-bound frames only; it checks current and Root identity, exact phase keys,
duplicate/injected namespace keys, fixed-point integer grammar, arithmetic,
roster/actor agreement and independent per-view records. Missing native values
remain INCOMPLETE; no row-count fallback exists. Historical V1/V2/V3
interpretations are preserved. The native format is debug output, not a stable
serialization API. The observed REALMS scope dump and operation markers were
about 1.3 KB / 20 lines; larger audit output remains unmeasured.

The icon hit-area hypothesis was checked against the actual source chain. The
outer `widget_map_mode_banner` is 100%×100% and already has
`allow_outside = yes`; the nested active vertical flow and child three-button
horizontal flow have no fixed width. Three visible 40×40 controls plus two
5 px gaps need 130×40. This evidence does not show a clipping ancestor. The
user-observed edge fault moved from right MY_REALM to left REALMS after
direct-row normalization, but no cursor coordinates or precise hit boundary
are available. No safe, source-supported anchor/host correction can be
justified; the GUI file is unchanged and hit behavior remains unresolved.

The focused suite passes 54 tests. Source preflight passes for 9 files at
1.20.1.2; Python compilation and `git diff --check` pass. Re-analysis of the
frozen post-exit checkpoint preserves its prior INCOMPLETE verdict. No install,
launcher/game operation, capture, staging, commit, publication or GitHub write
occurred. The private handoff contains the parser contract, hit-bounds
assessment, verification details and a bounded future retest plan.


## GUI review of native-counter preparation — 2026-10-24

Original F004-COUNTERS-HIT-20261024-15 consumed CHANGES REQUIRED after independent false-PASS repros: paired counter markers could name another view, and a V4 tag could carry a legacy no-build header. GUI preserved completed bytes and corrected those gates plus native END prefix parsing; added regression cases. All 55 focused tests and 9-file preflight pass. GUI-corrected counter candidate accepted for later runtime validation only; not installed. Native DIAG V3/AUDIT V4 source declares actual saved values, with no row-derived fallback and historical schemas preserved. Icon GUI is unchanged; no hit correction delivered or accepted, no repeated unchanged edge test requested. Source-based hit assessment remains an unresolved result, not a cure. No task closure or strict runtime pass.


## Native declaration first runtime check — 2026-10-24

One DIAG V3 REALMS summary has complete framing and all 12 native counters parsed, including total 4703, Primary 31, Secondary 3, Neutral 4669, held 3476, unheld 1227 and attempted writes 11297. Basic sums reconcile. New summary channel works in this bounded check; no other view/sample/audit is inferred. Global analyzer remains INCOMPLETE because this summary-only checkpoint contains no full semantic audit batch, not because native declarations failed. Separate selected REALMS audit is the next gate.


## First strict native REALMS audit — 2026-10-24

One bounded AUDIT V4 REALMS checkpoint passes independent analysis: complete framing, 4703 declared/emitted roster and result records, 1854 declared/emitted actors, role MATCH and intended-RGB MATCH; attempted writes 0. Counts reconcile (Primary 31, Secondary 3, Neutral 4669). This is acceptance relative to the emitted roster in the tested build/fixture, not an independent engine census, stored-color/pixel or lifecycle result. Other views remain unverified. Historical failed/truncated captures stay unchanged. Remaining views should use isolated fresh-start checkpoints to avoid repeating the prior second-audit truncation; its cause remains unknown.


## Strict native HOLDINGS audit — 2026-10-24

One isolated fresh-start AUDIT V4 HOLDINGS checkpoint passes: complete framing, 4703 declared/emitted counties/results and 1854 actors, independent role MATCH and intended-RGB MATCH, attempted writes 0. Primary 16, Secondary 18, Neutral 4669 reconcile total 4703. This covers emitted records for the tested view/build/fixture only. MY_REALM remains to be checked; no stored RGB/global census/lifecycle pass follows.


## Strict native MY_REALM audit and modifier-layout finding — 2026-10-24

Isolated selected MY_REALM AUDIT V4 passes: complete 4703 counties/results,1854 actors, role/intended-RGB MATCH, Primary2 Secondary32 Neutral4669, attempted writes0. All three views now have individual bounded emitted-record audit PASS; no census/stored RGB/lifecycle claim. User observes Shift+Option moves the icon row roughly one column left and makes all three hit areas work; releasing modifiers restores the problematic normal layout. Exact displacement unmeasured. Next correction isolates whole normal/audit rows at one fixed host origin; native counter work stays unchanged.


## Stable modifier rows — candidate prepared 2026-10-24

The user observed that holding Shift+Option moved the three-icon row by about
one column and restored all three hit areas; releasing the modifiers returned
the previous layout. The candidate replaces six interleaved controls with a
130×40 widget host and two complete horizontal rows, each containing the same
three 40×40 controls at a shared top-left origin with 5px spacing. Normal and
audit row visibility is mutually exclusive; button-level player validity,
guards, icons, tooltips, map selection, native counter/audit callbacks, header
and close control are retained. No audit callback changes the map mode.

Target-build GUI examples show fixed-size widgets, `parentanchor = top|left`,
`widgetanchor = top|left`, and native flowcontainers. The candidate's equal row
origins and widths follow from the explicit common anchors and
3×40+2×5=130 geometry; this is source-based coordinate reasoning, not proof
of engine-computed rectangles or runtime stability. The 55 focused tests pass
and the 9-file offline preflight passes for 1.20.1.2. GUI review, install and
user-run hover retest remain pending. No game, launcher, process, log or save
was inspected or operated.


## User acceptance of stable icon rows — 2026-10-24

User reports final layout works ideally after checking hold/release Shift+Option without clicking and icon hits. Fixed130x40 host and two complete3-button rows resolve the tested problem; exact internal engine cause remains unproven. Full symptom/failed-attempt/solution history: [GUI interaction resolution](../F004_GUI_INTERACTION.md). Native counter/three selected audits already passed before GUI-only change, whose data/actions remained immutable. Current non-diagnostic interaction interval has no diagnostic markers; a partial log boundary keeps its capture INCOMPLETE and does not replace the user observation. Initialization/court errors remain unattributed, no clean-log claim. One new-format bounded-sample delivery check and closeout accounting/documentation remain before closure.


## Final bounded-sample delivery check — 2026-10-24

One complete DIAG V3 SAMPLES HOLDINGS operation parses readable roles, 10 samples per role and 20 detail records, within limits. All 12 native counters delivered (total4703, Primary16, Secondary18, Neutral4669, attempted writes11297). No native framing/parse error. Summary/sample-only analyzer global status remains INCOMPLETE because no full semantic batch was requested; the entire file interval also retains an unrelated partial-boundary INCOMPLETE flag. The operation itself is fully framed; no stronger interval/census/stored-color claim follows. Together with the separate three-view V4 PASS checkpoints and user-accepted stable layout/hits, the scoped functional checklist is delivered. Formal cost verification/documentation and any authorized publication remain pending; F-004 not yet administratively closed.
