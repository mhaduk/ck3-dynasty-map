# Task History

Compact index of completed substantial tasks. Investigation detail belongs in the linked summary and, where available, the GitHub Issue.

| Task | Goal | Result | Issue journal | Canonical summary |
|---|---|---|---|---|
| R-001 | Record the installed CK3 baseline | Build 1.20.1.1 (Crozier) and the local research baseline recorded; not a full runtime compatibility claim. | [#1](https://github.com/mhaduk/ck3-dynasty-map/issues/1) | [R-001](tasks/R-001-environment-baseline.md) |
| R-002 | Inspect installed map-mode definitions | Native map-mode structure and baronies renderer inspected; custom loading/rendering remains unverified. | [#2](https://github.com/mhaduk/ck3-dynasty-map/issues/2) | [R-002](tasks/R-002-map-mode-definitions.md) |
| R-003 | Inspect installed map-mode GUI/API bindings | Static GUI/type inspection recorded; runtime integration and lifecycle gates remain open. | [#3](https://github.com/mhaduk/ck3-dynasty-map/issues/3) | [R-003](tasks/R-003-map-mode-gui-inspection.md) |
| R-004 | Generate current API documentation | Clean `script_docs` and `dump_data_types` generated for the recorded target build. | [#4](https://github.com/mhaduk/ck3-dynasty-map/issues/4) | [R-004](tasks/R-004-generated-api-docs.md) |
| R-006 | Verify formal scope links | County/barony and holder/Dynasty/House scope links verified in generated docs; no runtime claim. | [#6](https://github.com/mhaduk/ck3-dynasty-map/issues/6) | [R-006](tasks/R-006-scope-links.md) |
| R-014 | Inventory CK3 modding documentation and source hierarchy | Concise target-build source map created and integrated into agent/workflow instructions; runtime questions remain separate. | [#14](https://github.com/mhaduk/ck3-dynasty-map/issues/14) | [R-014](tasks/R-014-source-map.md) |
| R-017 | Select reproducible test starts and relationship fixtures | Scenario-selection stage complete: Ismail 867, William 1066, and Murchad 1066 are recorded as easy bookmark starts with static locators. Runtime liege chains and additional family/comparator coverage are deferred to later tests. | [#19](https://github.com/mhaduk/ck3-dynasty-map/issues/19) | [R-017](tasks/R-017-test-scenario-selection.md) |

R-005, R-009 and R-010 remain partial and are not listed as completed. R-014's
source map and agent/workflow integration are complete.
The [R-009 checkpoint](tasks/R-009-barony-color-safety.md) records first-batch
runtime results, title-color serialization and the unresolved independent renderer input.
The [R-005 partial checkpoint](tasks/R-005-player-context.md) consolidates its final gates; see [CURRENT_STATE.md](CURRENT_STATE.md) for the current next action and [RESEARCH.md](RESEARCH.md) for reusable findings.

## Research closeouts with limits

| Task | Result | Remaining limits | Canonical summary |
|---|---|---|---|
| R-016 | Three-view historical pipeline feasibility demonstrated in bounded 1.20.1.2 startup/runtime smoke; user reports normal switching/refresh/native-return operations appear to work. Research closed with bounded validation. | Grey nonmatching land failed visual acceptance; full semantic coverage, performance, context/atomicity safety and persistence/removal remain open. No production-readiness claim; #16 closed as completed research and checkpoint published. | [R-016](tasks/R-016-my-dynasty-pipeline.md#final-disposition--2026-10-21) |

R-017 / [#19](https://github.com/mhaduk/ck3-dynasty-map/issues/19) is closed as completed scenario selection: three bookmark starts are ready for later tests, while runtime chains and additional family/comparator coverage remain observations for that testing. Planned successors: [F-001](tasks/F-001-dynasty-map-ux.md) and [F-002](tasks/F-002-dynasty-color-strategy.md); neither is selected.

## Closed research directions

These are administrative scope dispositions, not completed technical validations.

| Task | Disposition | Remaining limits | Canonical record |
|---|---|---|---|
| R-015 / [#15](https://github.com/mhaduk/ck3-dynasty-map/issues/15) | Closed as not planned, 2026-10-21; Clerical Regions direction parked | Independent membership/provider binding and lifecycle unproven; no runtime. Reopen only on concrete new evidence. | [R-015](tasks/R-015-clerical-regions.md#final-disposition--2026-10-21) |

## Accepted specification records

| Task | Result | Limits | Canonical summary |
|---|---|---|---|
| F-003 / [#22](https://github.com/mhaduk/ck3-dynasty-map/issues/22) | Accepted three-subview behavior, classification and Primary/Secondary/Neutral category roles documented; palette and visual treatment excluded, 2026-10-21 | Documentation only; layout/visual acceptance belongs to F-001, color-source/fallback to F-002, and lifecycle safety remains with its existing owners | [F-003](tasks/F-003-dynasty-subview-definitions.md) |
