# Task History

Compact index of completed substantial tasks. Investigation detail belongs in the linked summary and, where available, the GitHub Issue.

| Task | Goal | Result | Issue journal | Canonical summary |
|---|---|---|---|---|
| T-005 | Rationalize eight open research issues against current architecture/evidence | GUI accepted substantive result: 2 narrowed; 3 closed completed; 3 closed not planned. Only R-005/R-009 remain research. Parent closed; cross-chat F-001 integration resolved by accepted reconciliation. | [#27](https://github.com/mhaduk/ck3-dynasty-map/issues/27) | [T-005](tasks/T-005-research-backlog-review.md) |
| T-003 | Assess GitHub Wiki feasibility and prepare/publish three-section Wiki with grouped AI-cost summary | Published Wiki Home on 2026-10-22. AI-cost section has only R/T/F/B summary and per-task tables; API-equivalent estimates: R $15.38, T $4.17, F/B no eligible tasks. Partial measured token coverage; temporary screenshot not uploaded. | — | [T-003](tasks/T-003-wiki-feasibility.md) |
| T-002 | Backfill per-model token usage and propose close-time accounting | Corrected helper accepted on 2026-10-22; 27 offline tests; 3006-record recomputation unchanged; 11 remote tables and 10 local mirrors, partial coverage. Automation proposal unapplied; scoped Git publication authorized 2026-10-22; #24 closure excluded. | [#24](https://github.com/mhaduk/ck3-dynasty-map/issues/24) | [T-002](tasks/T-002-task-ai-cost.md) |
| T-001 | Incrementally optimize agent coordination, context and log analysis | Per-ID handoffs, explicit ownership/provenance, concise routing/context, direction/self-healing feedback and bounded log checkpoints accepted by GUI on 2026-10-22; 37 offline tests passed. Scoped publication tracked in #23; no measured savings or CK3 runtime validation. | [#23](https://github.com/mhaduk/ck3-dynasty-map/issues/23) | [T-001](tasks/T-001-agent-workflow-optimization.md) |
| R-001 | Record the installed CK3 baseline | Build 1.20.1.1 (Crozier) and the local research baseline recorded; not a full runtime compatibility claim. | [#1](https://github.com/mhaduk/ck3-dynasty-map/issues/1) | [R-001](tasks/R-001-environment-baseline.md) |
| R-002 | Inspect installed map-mode definitions | Native map-mode structure and baronies renderer inspected; custom loading/rendering remains unverified. | [#2](https://github.com/mhaduk/ck3-dynasty-map/issues/2) | [R-002](tasks/R-002-map-mode-definitions.md) |
| R-003 | Inspect installed map-mode GUI/API bindings | Static GUI/type inspection recorded; runtime integration and lifecycle gates remain open. | [#3](https://github.com/mhaduk/ck3-dynasty-map/issues/3) | [R-003](tasks/R-003-map-mode-gui-inspection.md) |
| R-004 | Generate current API documentation | Clean `script_docs` and `dump_data_types` generated for the recorded target build. | [#4](https://github.com/mhaduk/ck3-dynasty-map/issues/4) | [R-004](tasks/R-004-generated-api-docs.md) |
| R-006 | Verify formal scope links | County/barony and holder/Dynasty/House scope links verified in generated docs; no runtime claim. | [#6](https://github.com/mhaduk/ck3-dynasty-map/issues/6) | [R-006](tasks/R-006-scope-links.md) |
| R-014 | Inventory CK3 modding documentation and source hierarchy | Concise target-build source map created and integrated into agent/workflow instructions; runtime questions remain separate. | [#14](https://github.com/mhaduk/ck3-dynasty-map/issues/14) | [R-014](tasks/R-014-source-map.md) |
| R-017 | Select reproducible test starts and relationship fixtures | Scenario-selection stage complete: Ismail 867, William 1066, and Murchad 1066 are recorded as easy bookmark starts with static locators. Runtime liege chains and additional family/comparator coverage are deferred to later tests. | [#19](https://github.com/mhaduk/ck3-dynasty-map/issues/19) | [R-017](tasks/R-017-test-scenario-selection.md) |

Before the 2026-10-23 T-005 review, R-005, R-009 and R-010 were partial and not listed as completed. Current dispositions are recorded in the T-005 section below. R-014's
source map and agent/workflow integration are complete.
The [R-009 checkpoint](tasks/R-009-barony-color-safety.md) records first-batch
runtime results, title-color serialization and the unresolved independent renderer input.
The [R-005 partial checkpoint](tasks/R-005-player-context.md) consolidates its final gates; see [CURRENT_STATE.md](CURRENT_STATE.md) for the current next action and [RESEARCH.md](RESEARCH.md) for reusable findings.

## T-005 accepted research dispositions — 2026-10-23

[T-005 review](tasks/T-005-research-backlog-review.md) records verified remote dispositions: R-007/R-008/R-010 closed completed with bounded evidence; R-011/R-012/R-013 closed not planned. R-005/R-009 remain open and narrowed. R-013’s unresolved no-Dynasty coverage moved to R-005; remaining ordinary traversal/projection/menu acceptance belongs to F-001. Earlier partial statuses above describe their dated checkpoints. GUI independently accepted the substantive result and closed #27 completed; cross-chat integration is now resolved by accepted/consumed `T005-F001-RECONCILE-20261023-02`. Original frozen lifecycles and both chats’ evidence are preserved.

## Research closeouts with limits

| Task | Result | Remaining limits | Canonical summary |
|---|---|---|---|
| R-016 | Three-view historical pipeline feasibility demonstrated in bounded 1.20.1.2 startup/runtime smoke; user reports normal switching/refresh/native-return operations appear to work. Research closed with bounded validation. | Grey nonmatching land failed visual acceptance; full semantic coverage, performance, context/atomicity safety and persistence/removal remain open. No production-readiness claim; #16 closed as completed research and checkpoint published. | [R-016](tasks/R-016-my-dynasty-pipeline.md#final-disposition--2026-10-21) |

R-017 / [#19](https://github.com/mhaduk/ck3-dynasty-map/issues/19) is closed
as completed scenario selection: three starts are ready for later tests;
runtime chains and additional family/comparator coverage remain deferred.
F-002 remains planned/unselected. F-001's intervening preparation, accepted
shown appearance, Realms self-liege correction and modifier/parser checks are
distilled in its [canonical record](tasks/F-001-dynasty-map-ux.md). Its current
status is the incomplete checkpoint below; earlier category/display failures
are historical observations, not the current accepted result.

## F-001 incomplete closeout checkpoint — 2026-10-23

GUI reviewed cycle31 as a published partial result, then the user explicitly
paused F-001 to work on other tasks. It is not a completed-history entry.
[Future-session checkpoint](tasks/F-001-resume.md) records the two remaining
load errors and retained evidence; no new CLI cycle is pending.

This is an incomplete-task checkpoint, not a completed-task row. Final cycle31
restored the exact prior inert helper declarations/CoA and six original names,
without reviving retired execution paths. Nine-file source/install equality,
33 unchanged tests and user-only menu/focused interaction checks passed. The
three missing-template errors are absent; two unnamed duplicate-title load
errors persist, so F-001 / #20 remains OPEN / NOT READY. F-005/#30 owns that
compatibility blocker; F-004/#29 retains diagnostic gaps, and R-005/#5/R-009/#9
retain their safety research. No further test cycle, save research or false
feature closure is started. [Current canonical record](tasks/F-001-dynasty-map-ux.md).

## Closed research directions

These are administrative scope dispositions, not completed technical validations.

| Task | Disposition | Remaining limits | Canonical record |
|---|---|---|---|
| R-015 / [#15](https://github.com/mhaduk/ck3-dynasty-map/issues/15) | Closed as not planned, 2026-10-21; Clerical Regions direction parked | Independent membership/provider binding and lifecycle unproven; no runtime. Reopen only on concrete new evidence. | [R-015](tasks/R-015-clerical-regions.md#final-disposition--2026-10-21) |

## Accepted specification records

| Task | Result | Limits | Canonical summary |
|---|---|---|---|
| F-003 / [#22](https://github.com/mhaduk/ck3-dynasty-map/issues/22) | Accepted three-subview behavior, classification and Primary/Secondary/Neutral category roles documented; palette and visual treatment excluded, 2026-10-21 | Documentation only; layout/visual acceptance belongs to F-001, color-source/fallback to F-002, and lifecycle safety remains with its existing owners | [F-003](tasks/F-003-dynasty-subview-definitions.md) |
