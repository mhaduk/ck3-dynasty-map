# T-005 — Research backlog review

Status: COMPLETE after independent substantive GUI review, 2026-10-23.
Parent [#27](https://github.com/mhaduk/ck3-dynasty-map/issues/27) is closed completed.
The cross-chat receipt conflict is resolved by accepted reconciliation
`T005-F001-RECONCILE-20261023-02`; original frozen evidence remains unchanged.

Reviewed exactly R-005/R-007/R-008/R-009/R-010/R-011/R-012/R-013. GitHub writes
were authorized only for #5/#7/#8/#9/#10/#11/#12/#13. No titles, labels, unrelated
issues, Git index/history, implementation, installed files or game state changed.
No tests, source rescan, new runtime capture or external technical research ran.

## Disposition matrix

| Task | Original purpose | Current evidence | Decision | Remaining owner/work | GitHub action |
|---|---|---|---|---|---|
| [R-005 / #5](https://github.com/mhaduk/ck3-dynasty-map/issues/5) | Resolve fresh local-player scopes, unavailable entry and context invalidation. | R-005 FINAL GUARDS A passed only the displayed observer path after RESET on 1.20.1.1. Direct NULL Execute failed before effect entry. R-016 on 1.20.1.2 supplies valid-context smoke, not atomic entry. R-013 failed to create a no-Dynasty player. | REDUCE | Narrow dispatch/context and no-Dynasty coverage decision; color cleanup belongs to #9. | Body updated; remains open |
| [R-007 / #7](https://github.com/mhaduk/ck3-dynasty-map/issues/7) | Verify liege traversal and government-specific runtime semantics. | Generated 1.20.1.1 triggers.log:1816–1819 documents seniors excluding self; R-016 rechecked the relevant entries on 1.20.1.2. R-016 ran the county classifier. F-001 later obtained 3,147 supported closed Realms records, including 31 wrong results at the self-liege/self-top Nasr terminal. That is a concrete classifier predicate defect, not evidence that senior traversal is unavailable. The fix is prepared/installed; corrected runtime acceptance is still pending. | CLOSE | F-001 classifier acceptance; later functional/government regression. | Body updated; one closure comment; closed completed |
| [R-008 / #8](https://github.com/mhaduk/ck3-dynasty-map/issues/8) | Verify county-first traversal and exclude non-barony descendants from color writes. | Generated effects.log:11422–11427 includes county self and descendants with continue separate from limit; the used contract was rechecked for 1.20.1.2. R-016 uses county-rooted every_in_de_jure_hierarchy, continue always=yes, limit tier_barony. Its static direct sample contains 3 counties/13 baronies; execution markers did not emit numeric coverage counters. The user reported all three counties and constituent baronies green, without enumerated 13-title coverage. World execution is bounded, not exhaustive projection proof. | CLOSE | F-001 projection acceptance; R-009 write safety. | Body updated; one closure comment; closed completed |
| [R-009 / #9](https://github.com/mhaduk/ck3-dynasty-map/issues/9) | Determine barony color side effects, isolation, restoration and save/removal safety. | R-009 observed shared native/custom barony RGB and explicit AFTER-save overrides on 1.20.1.1; known-definition reset did not capture arbitrary originals. R-016 executed a bounded direct-RGB pipeline on 1.20.1.2; no later persistence/removal or exact restoration acceptance exists. F-001 visual approval and installed scope-clear fixes are not title RGB cleanup. | REDUCE | Narrow current renderer lifecycle, arbitrary-original restore and persistence/removal feasibility. | Body updated; remains open |
| [R-010 / #10](https://github.com/mhaduk/ck3-dynasty-map/issues/10) | Find original minimal native-menu integration and a usable refresh route. | Probe 01 recursive same-name inheritance crashed and remains withdrawn. Primitive-based original narrow replacement in probe 02 loaded and placed DM inside Additional Modes; basic native switching and Faith smoke passed in the tested configuration. R-016 then loaded the Dynasty menu/panel and three named views on 1.20.1.2 with user-reported switching/explicit Refresh/native-return smoke. F-001 continues actual UI development; full parity is unverified. | CLOSE | F-001 interaction/parity acceptance; C-210 compatibility. | Body updated; one closure comment; closed completed |
| [R-011 / #11](https://github.com/mhaduk/ck3-dynasty-map/issues/11) | Capture a generic clean vanilla save/map-interaction noise baseline. | The 1.20.1.1 no-mod startup/API session had empty error.log, not representative loaded-save coverage. Later tutorial/court-scene errors demonstrate that startup emptiness cannot attribute in-game noise. T-001 provides finite log boundaries/completeness checks; it does not supply a matched vanilla control or establish causality. | CLOSE | F-001/T-113 targeted attribution when evidence requires it. | Body updated; one closure comment; closed not_planned |
| [R-012 / #12](https://github.com/mhaduk/ck3-dynasty-map/issues/12) | Install/configure Tiger and establish a validation command. | R-014 source hierarchy treats Tiger as an optional external validator that may lag the game and emit false positives. No Tiger installation or run is established. Target-build generated docs, installed-source evidence, mod preflight and user-run parser/startup gates already define the actual workflow; preflight is not syntax/API proof. | CLOSE | Optional, evidence-triggered tooling under T-113. | Body updated; one closure comment; closed not_planned |
| [R-013 / #13](https://github.com/mhaduk/ck3-dynasty-map/issues/13) | Find a real no-Dynasty local-player fixture and verify unavailable UI. | The single set_to_lowborn attempt was rejected for the player; Dynasty remained present. A courtier guard and observer UI are not the real local-player case. No supported fixture or accepted waiver exists; R-016 valid-context execution does not change that. | CLOSE | R-005 no-Dynasty coverage decision; F-001/T-115 later UI acceptance. | Body updated; one closure comment; closed not_planned |

Counts: **8 reviewed; 0 kept unchanged; 2 narrowed/updated; 3 closed completed;
3 closed not planned.** Start/end open-issue inventories contain no additional
R issues outside the frozen scope. Only R-005 and R-009 remain open research.
“Completed” closes a research-method question with bounded evidence, not all
feature acceptance. “Not planned” retires redundant or unjustified standalone
work without declaring its original technical coverage passed.

## Evidence and limits

- [ADR-001/008/009/010](../DECISIONS.md): county semantics, unavailable activation, map-native interfaces and three views remain unchanged.
- [Generated contracts](../RESEARCH.md#liege-traversal--r-007), [projection contracts](../RESEARCH.md#county-barony-and-dynastyhouse-iterators--r-008--rg-color-01), and [1.20.1.2 revalidation](../RESEARCH.md#r-016--12012-used-api-revalidation-2026-10-21): clean 1.20.1.1 baseline differs from later probe-enabled generated output; documented agreement is not unchanged engine behavior.
- [R-005](R-005-player-context.md), [FINAL GUARDS](../evidence/2026-10-20-r005-player-context/final-guards-result.md): bounded observer UI after RESET; NULL dispatch fails; real no-Dynasty player fixture never established.
- [R-009](R-009-barony-color-safety.md): shared RGB/serialization observed in old build; arbitrary original capture, isolation and removal remain unresolved.
- [R-010 probe 02](../evidence/2026-10-20-r010-native-menu-02/README.md): original scoped menu integration observed; failed self-inheritance route withdrawn; no general load-order or parity proof.
- [R-016](R-016-my-dynasty-pipeline.md#final-disposition--2026-10-21): bounded three-view pipeline on 1.20.1.2. Its sample has 3 counties/13 static barony targets; runtime counters were not emitted and enumerated 13-title coverage was not proven.
- [F-001](F-001-dynasty-map-ux.md#current-reconciled-evidence--2026-10-23): complete interval but incomplete batch: 4,703 roster, 3,368 closed Realms frames, 3,147 supported records, 31 Nasr-terminal mismatches. Bukhara defect confirmed; later Realms/parser/V2 fixes and scope-clear cleanup are source/install accepted, not corrected full-runtime acceptance. The latest combined log audit remains pending; user-supplied visual approval is narrower than semantic/safety acceptance.
- [F-003](F-003-dynasty-subview-definitions.md): accepted classifier/projection semantics; [F-002](F-002-dynasty-color-strategy.md): accent extraction/fallback only, not renderer storage.
- [T-001](T-001-agent-workflow-optimization.md): bounded log tooling does not create a vanilla causal control. [R-014 source map](../CK3_SOURCE_MAP.md): Tiger is a secondary validator, not target-build authority.

Existing issue bodies and comments were fetched in full. Read-only owner checks
confirmed #20/#21/#22 and their divisions of responsibility. #20’s remote body
is older than the frozen local F-001 record; local evidence determines current
technical status here. No unauthorized synchronization of #20/#21/#22/#27 was
performed. Issue updates disclose that latest local findings may await Git
publication; all earlier bodies/history and any cost tables were preserved
verbatim beneath an explicitly superseded-history boundary.

## Decisions against the eight questions

Each numbered answer below corresponds exactly to #27’s eight review questions.

### R-005 — REDUCE

1. Original uncertainty: Resolve fresh local-player scopes, unavailable entry and context invalidation.
2. New knowledge: R-005 FINAL GUARDS A passed only the displayed observer path after RESET on 1.20.1.1. Direct NULL Execute failed before effect entry. R-016 on 1.20.1.2 supplies valid-context smoke, not atomic entry. R-013 failed to create a no-Dynasty player.
3. Actual decision blocker: Can the exposed map/GUI lifecycle prevent stale or invalid player/Dynasty dispatch across context loss and transition races, and how can the real no-Dynasty player case be covered?
4. Research or testing: Engine-boundary research remains; ordinary UI regression belongs to F-001.
5. Correct owner: R-005 #5 owns the remaining dispatch/context contract and the merged R-013 fixture-or-coverage decision. R-009 #9 owns actual RGB restoration; F-001 #20 implements and accepts the resulting UI contract (F-104/T-115/T-117 planning).
6. Would research change the build? Yes: it determines whether normal one-action entry can satisfy ADR-008 or remains blocked. Valid-context smoke and an effect guard cannot waive this.
7. Cheapest decisive evidence: Reuse existing API and diagnostic evidence; trace only the actual normal entry and invalidation boundary. Identify a supported pre-dispatch guard/invalidation contract and one discriminating transition observation. For no-Dynasty coverage, first establish supported playable-state constraints from existing evidence; propose a real fixture only on concrete new evidence. No repeat NULL or rejected set_to_lowborn experiment.
8. If omitted: ADR-008 activation/context safety stays blocked; retain guards and disclose unverified coverage.

Stop/acceptance: Stop with an evidence-backed entry/invalidation contract, or a precise unsupported boundary and blocked implementation decision. Acceptance requires fresh P/D at dispatch, no classification/result writes on unavailable activation, no stale-context use, and a distinct no-Dynasty player result OR an explicitly accepted coverage decision; unsupported fixtures remain UNVERIFIED. A negative report is not a safety pass.

Dependencies: Reuse R-003/R-004/R-016 and ADR-008/010. R-009 supplies cleanup capability after invalidation. F-001 owns ordinary UI regression after this contract is resolved. R-013 is merged here, with no separate research gate.

### R-007 — CLOSE

1. Original uncertainty: Verify liege traversal and government-specific runtime semantics.
2. New knowledge: Generated 1.20.1.1 triggers.log:1816–1819 documents seniors excluding self; R-016 rechecked the relevant entries on 1.20.1.2. R-016 ran the county classifier. F-001 later obtained 3,147 supported closed Realms records, including 31 wrong results at the self-liege/self-top Nasr terminal. That is a concrete classifier predicate defect, not evidence that senior traversal is unavailable. The fix is prepared/installed; corrected runtime acceptance is still pending.
3. Actual decision blocker: No separate implementation-choice unknown remains in this research scope; deep/government cases remain untested acceptance coverage.
4. Research or testing: Ordinary classifier and government acceptance testing.
5. Correct owner: F-001 #20 owns current three-view classifier acceptance and the confirmed terminal defect; T-111/T-112 and E-204/E-205 retain later cadet, nested/no-Dynasty and government coverage. R-005 #5 owns player validity, not traversal.
6. Would research change the build? No: ADR-010/F-003 already fix ordinary de-facto seniors, holder precedence and player subtree semantics. More generic traversal research would duplicate concrete feature tests.
7. Cheapest decisive evidence: No new research. In F-001, compare current identity receipts with the independent F-003 oracle, including independent/self-top, nested dynastic senior and player-vassal/sibling cases; missing natural cases stay untested.
8. If omitted: No architecture loss from skipping duplicate research; feature tests must still catch hierarchy defects.

Stop/acceptance: Research closes on a documented usable traversal contract and bounded execution evidence. This does not pass the all-three-view oracle, corrected Realms runtime, government or full coverage tests.

Dependencies: R-004/R-006/R-016 evidence reused; F-003 #22 is the accepted semantic reference, not a new research owner.

### R-008 — CLOSE

1. Original uncertainty: Verify county-first traversal and exclude non-barony descendants from color writes.
2. New knowledge: Generated effects.log:11422–11427 includes county self and descendants with continue separate from limit; the used contract was rechecked for 1.20.1.2. R-016 uses county-rooted every_in_de_jure_hierarchy, continue always=yes, limit tier_barony. Its static direct sample contains 3 counties/13 baronies; execution markers did not emit numeric coverage counters. The user reported all three counties and constituent baronies green, without enumerated 13-title coverage. World execution is bounded, not exhaustive projection proof.
3. Actual decision blocker: No separate traversal-method decision remains; exact full-map coverage is still unverified.
4. Research or testing: Ordinary projection coverage and renderer acceptance testing.
5. Correct owner: F-001 #20 owns every-county/secondary-barony projection acceptance; F-107/T-114 retain implementation regression. R-009 #9 owns safety of the writes.
6. Would research change the build? No: county classification and constituent-barony projection are accepted in ADR-001/010 and F-003.
7. Cheapest decisive evidence: No new research. F-001 must compare reached barony membership/counts against county membership, include secondary/unbuilt targets and reject any higher-tier write; role-only read-only audit does not prove stored RGB or coverage.
8. If omitted: No architecture loss; omitting ordinary coverage tests could still hide skipped or mispainted baronies.

Stop/acceptance: Research closes on documented recursion/filtering plus bounded sample execution. Whole-map coverage, stored RGB and safe restoration remain separate unpassed acceptance gates.

Dependencies: Reuse R-004/R-006/R-016; F-003 #22 defines the county projection contract.

### R-009 — REDUCE

1. Original uncertainty: Determine barony color side effects, isolation, restoration and save/removal safety.
2. New knowledge: R-009 observed shared native/custom barony RGB and explicit AFTER-save overrides on 1.20.1.1; known-definition reset did not capture arbitrary originals. R-016 executed a bounded direct-RGB pipeline on 1.20.1.2; no later persistence/removal or exact restoration acceptance exists. F-001 visual approval and installed scope-clear fixes are not title RGB cleanup.
3. Actual decision blocker: Can the current map-native shared title-RGB route restore arbitrary prior live colors on exit/context loss and meet save/load/removal requirements, or is that route blocked without a supported view-specific input?
4. Research or testing: Architecture-critical engine/storage research remains; normal UI and palette tests have other owners.
5. Correct owner: R-009 #9 solely owns map color-state isolation, exact restore and persistence/removal contract. R-005 #5 owns detecting invalid context and preventing dispatch; F-001 #20 implements/tests normal UI; F-002 #21 owns accent extraction and palette fallback only.
6. Would research change the build? Yes: shared serialized mutations can invalidate production use even with correct categories and attractive visuals.
7. Cheapest decisive evidence: Reuse established serialization/leakage findings; first identify a concrete supported original-color capture/restore contract or map-native isolated input from already mapped evidence. If viable, propose a minimal fixed-target before/write/restore observation with native-map comparison and separately authorized save/reload/disabled-mod fresh-process evidence. Do not launch or prepare it in T-005.
8. If omitted: Production renderer safety remains blocked; bounded probe success must not become a release claim.

Stop/acceptance: Stop with a supported exact restoration/isolation contract plus bounded evidence and explicit remaining coverage, or a precise blocked renderer decision. Unknown arbitrary originals, shared-state leakage or removal behavior cannot be marked safe. v0.1 requires exit/context restoration; v1.0 requires safe removal or a proven harmless path. Documentation of unknown harm is not a pass.

Dependencies: R-002/R-004/R-014/R-016 are evidence, not unfinished prerequisites. Coordinate one boundary with R-005: it signals context loss, this issue owns RGB restoration. F-002 accent choice cannot solve storage isolation.

### R-010 — CLOSE

1. Original uncertainty: Find original minimal native-menu integration and a usable refresh route.
2. New knowledge: Probe 01 recursive same-name inheritance crashed and remains withdrawn. Primitive-based original narrow replacement in probe 02 loaded and placed DM inside Additional Modes; basic native switching and Faith smoke passed in the tested configuration. R-016 then loaded the Dynasty menu/panel and three named views on 1.20.1.2 with user-reported switching/explicit Refresh/native-return smoke. F-001 continues actual UI development; full parity is unverified.
3. Actual decision blocker: No separate integration-method choice blocks the current direction. Complete UI parity, refresh attribution and compatibility remain acceptance work.
4. Research or testing: Ordinary UI/compatibility acceptance testing.
5. Correct owner: F-001 #20 owns menu/panel, normal entry/subview/Refresh acceptance, mini-menu/DLC/UI-scale and raid/barter guard regression; C-210 owns later other-mod compatibility. R-005 #5 owns safe dispatch/context; R-009 #9 owns color restore.
6. Would research change the build? No: original scoped overrides plus explicit Refresh give a demonstrated path. A universal filename/load-order theorem is unnecessary and unproved.
7. Cheapest decisive evidence: No new integration research. F-001 verifies ordinary action receipts, selected-mode refresh, menu-open no scan, native round-trip and relevant native controls/UI scales. Request matched vanilla evidence only for a concrete attribution problem.
8. If omitted: No method-selection loss; untested compatibility and UI controls must remain visible in acceptance.

Stop/acceptance: Close the method-selection research, preserving failed-route history and bounded evidence. No production parity, atomic entry or restore acceptance is claimed.

Dependencies: ADR-006/009/010 remain; no copied vanilla/HUD fallback. R-005/R-009 retain only their distinct safety questions.

### R-011 — CLOSE

1. Original uncertainty: Capture a generic clean vanilla save/map-interaction noise baseline.
2. New knowledge: The 1.20.1.1 no-mod startup/API session had empty error.log, not representative loaded-save coverage. Later tutorial/court-scene errors demonstrate that startup emptiness cannot attribute in-game noise. T-001 provides finite log boundaries/completeness checks; it does not supply a matched vanilla control or establish causality.
3. Actual decision blocker: No universal reusable noise catalogue can settle errors across changed build/save/playset/actions. Specific attribution questions remain case dependent.
4. Research or testing: Targeted diagnostic/acceptance evidence, not standing research.
5. Correct owner: F-001 #20 owns attribution of its current observed errors; T-113 owns release log review and any necessary matched vanilla control. These are acceptance tasks, not another standing research gate.
6. Would research change the build? No: a speculative generic capture would not change the map architecture or replace a matched comparison.
7. Cheapest decisive evidence: No blanket run. When an error affects acceptance, use the same build, relevant DLC/playset, save/action boundary and explicit attribution hypothesis for a bounded user-run vanilla comparison. Until then, keep unattributed errors visible.
8. If omitted: No blanket baseline is lost; unresolved errors cannot be dismissed and may require a matched control later.

Stop/acceptance: Close as not planned because the standalone research task is retired, not because representative vanilla coverage passed. Preserve empty-startup evidence and the missing loaded-save control.

Dependencies: Reuse T-001 checkpoint tooling; a complete interval is not clean logs or causal proof. R-001 build provenance remains necessary.

### R-012 — CLOSE

1. Original uncertainty: Install/configure Tiger and establish a validation command.
2. New knowledge: R-014 source hierarchy treats Tiger as an optional external validator that may lag the game and emit false positives. No Tiger installation or run is established. Target-build generated docs, installed-source evidence, mod preflight and user-run parser/startup gates already define the actual workflow; preflight is not syntax/API proof.
3. Actual decision blocker: No product/architecture question requires installing a convenience tool now; useful target-build diagnostics would need a concrete evaluation trigger.
4. Research or testing: Optional tooling setup, not research.
5. Correct owner: T-113 owns any later justified validator evaluation/invocation in implementation acceptance. Source/API authority remains the installed target build and generated docs.
6. Would research change the build? No: merely installing Tiger cannot decide renderer isolation, context safety or classification semantics.
7. Cheapest decisive evidence: No install. Revisit under T-113 only for a concrete static diagnostic gap with supported target-build coverage; record exact version/invocation, actionable findings and false positives. Do not replace parser/runtime gates.
8. If omitted: Supported static checks may be forgone; mandatory source/preflight/parser/runtime evidence still applies.

Stop/acceptance: Close as not planned; no install, validation result or Tiger pass is claimed. T-113 no longer blocks on R-012 or mandatory Tiger setup.

Dependencies: R-014 source hierarchy retained. Any later local installation needs its own scoped task/authorization; T-005 installs nothing.

### R-013 — CLOSE

1. Original uncertainty: Find a real no-Dynasty local-player fixture and verify unavailable UI.
2. New knowledge: The single set_to_lowborn attempt was rejected for the player; Dynasty remained present. A courtier guard and observer UI are not the real local-player case. No supported fixture or accepted waiver exists; R-016 valid-context execution does not change that.
3. Actual decision blocker: The real local-player no-Dynasty coverage question remains unresolved and is retained once in #5.
4. Research or testing: Fixture/coverage boundary remains research in R-005; UI behavior thereafter is acceptance testing.
5. Correct owner: Merged into R-005 #5, which now explicitly owns the fixture-or-coverage decision. F-001 #20 implements unavailable UI; F-104/T-115/E-206 retain acceptance/regression. R-009 #9 owns RGB cleanup separately.
6. Would research change the build? A supported constraint/fixture finding could change safety coverage, but no separate research owner is needed.
7. Cheapest decisive evidence: No new fixture iteration. Under R-005 reuse the failed attempt and known playability constraints, seek concrete supported-state evidence before proposing a fixture, or request an explicit documented coverage decision.
8. If omitted: Skipping the duplicate loses nothing if #5 retains the unresolved case; skipping the safety requirement would violate ADR-008.

Stop/acceptance: Close duplicate issue as not planned after scope transfer to #5. This is not technical completion, a no-Dynasty UI pass or an ADR-008 waiver.

Dependencies: ADR-008 unchanged. No repeat set_to_lowborn, speculative Aepak/herder conversion, direct NULL or passed lifecycle cases.

## Remaining implementation-blocking research

R-005 must establish a supported fresh-context/dispatch/invalidation contract or
report the precise blocked boundary. The merged no-Dynasty question requires a
supported real player fixture or an explicitly accepted coverage decision; the
rejected mutation, courtier and observer cases cannot satisfy it. Ordinary UI
coverage is F-001/F-104/T-115/T-117 work after that contract, not a second R issue.

R-009 must establish exact arbitrary-original restoration or a supported isolated
map input and the save/removal contract, or report the renderer route blocked.
R-005 detects invalid context; R-009 owns RGB cleanup. F-002’s palette and F-001’s
local-scope cleanup cannot solve title-state persistence. Excluded gameplay
carriers, speculative dummy inertness and broad renderer rescans are not retained.

Classifier terminal correctness, full projection membership, UI parity/refresh,
government edge coverage and compatibility remain ordinary unpassed acceptance.
They do not justify duplicate R-007/R-008/R-010 research. Planned test IDs in
BACKLOG/TEST_PLAN preserve these obligations; they are not newly created issues
or an authorization to execute tests. Multiplayer/All Dynasties remain deferred
product boundaries, not additional active research selected here.

## Remote verification and local synchronization

Before each write, verified repository identity, exact issue URL/number and
current body/state. Verified all eight resulting bodies and states; six closure
comments occur once and closure reasons are COMPLETED for #7/#8/#10 and
NOT_PLANNED for #11/#12/#13. Local ignored task artifacts retain full before/after
snapshots, exact UTF-8 body/comment files and comment URL receipts. Start/end
inventories show no extra open R issue. No comments were blindly retried.

Local backlog/current-state/research/history, R-005/R-009 summaries and affected
architecture/risk/test/compatibility ownership were synchronized after the remote
decisions. Dated evidence remains historical; this review adds no architectural
decision or product implementation. F-001 stays incomplete; parent T-005 awaits
GUI inspection and acceptance.

## Self-healing and practical improvement

Observation: initial broad local listings/combined reads exceeded output budgets.
Cause: existing handoff/evidence volume. Recovery: exact per-ID discovery and
bounded section reads; no missing evidence was inferred from clipped output.
Outcome: frozen contract and decisive evidence recovered. Improvement: start
with per-ID task/status and cap each reference read rather than listing all
historical artifacts.

Observation: draft R-008 evidence overstated 13 runtime writes. Cause: static
sample cardinality was conflated with emitted counters. Recovery: reread the
sample execution/observation records before publication and qualify the body.
Outcome: published text states static 13 targets and no enumerated runtime
coverage. Improvement: tie every numeric coverage claim to its emitted receipt.

Observation: `gh issue close --reason not_planned` failed with exit 1 after the
#11 body/comment were saved. Cause: gh CLI uses `not planned`, while the API
state enum uses `NOT_PLANNED`. Recovery: reread #11, verify the exact body and
single comment, then close with the documented CLI spelling; continue #12/#13.
Outcome: all intended changes verified; no duplicate comment. Improvement: map
API enum names to CLI argument values explicitly and resume from receipts.

GUI next step: inspect actual issue bodies/comments/reasons and scoped baseline
diff, validate counts/ownership and evidence limits, consume the child result,
then finalize #27 only within the parent’s authorization. No further game action
is requested by this review.


## Final GUI acceptance — 2026-10-23

GUI independently checked all eleven output hashes and the CLI result hash,
all other immutable inputs, actual per-file changes against the preserved dirty
baseline, all 64 review answers, and live GitHub bodies/history/comments/states.
Only R-005/R-009 remain open research. The six closure reasons and single new
explanatory comments match the matrix. Scoped whitespace checks passed. Parent
#27 now contains the final review table, checked acceptance criteria and one
verified completion comment, and is closed completed. Local Git publication
remains separately unauthorized; no staging/commit/push was performed.

Concurrent F-001 work appended a separate GUI receipt: 14,109 emitted role/intended
RGB agreements and 4,703 unique emitted counties per view, with Bukhara corrected.
Strict audit is still INCOMPLETE because declared counters are zero; global census,
stored RGB, pixels and lifecycle safety remain unproven. This later receipt
strengthens R-007 method closure and does not change any disposition. The frozen
CLI review above describes its earlier evidence boundary; no new raw-evidence
analysis is claimed here. The remaining concrete counter/export diagnosis belongs
to F-001, not a reopened broad research issue.

Administrative recovery: helper validation returned exit 2, input fingerprint
changed. Exact baseline comparison isolated only the new F-001 GUI-review section;
all other immutable inputs and final outputs matched. GUI preserved both chats’
work and the original COMPLETED revision, recorded independent substantive
acceptance privately and did not force a CONSUMED transition. This administrative
limitation does not invalidate the verified backlog decisions or parent outcome.
Practical improvement: freeze minimal copied context for concurrent evidence work;
no agent configuration was changed. Successful broad reads also clipped output;
focused comparisons and bounded sections recovered the needed review evidence.


## Receipt reconciliation and scoped publication — 2026-10-23

The user requested resolution of the F-001 conflict and explicitly authorized
commit/push. A new bounded reconciliation froze copies of both original results,
reviews and current context. Original result/baseline hashes, all eleven archived
T-005 output hashes and the final F-001 report hash were verified. The documented
reference changes are compatible GUI receipt/current-state edits, not conflicting
source or runtime evidence. The new `T005-F001-RECONCILE-20261023-02` receipt was
validated, completed and consumed through the helper. It supersedes the pending
integration of both original results; their frozen COMPLETED statuses and evidence
remain historical. Earlier statements about an unresolved administrative limit
above describe the earlier receipt attempt, not a current blocker.

T-005 dispositions and F-001 runtime limitations remain unchanged. Publication is
limited to T-005/reconciliation documentation and a concise current F-001 evidence
checkpoint. Unrelated mod/source/tool changes and detailed unpublished F-001
history are preserved locally. Agent configuration, original fingerprints and
runtime acceptance criteria were not modified.
