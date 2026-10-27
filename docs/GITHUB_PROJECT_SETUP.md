# GitHub Project Setup

## Project

Name: `Dynasty Map`
Primary view: Board

Columns/status values:

1. Backlog
2. Ready
3. In progress
4. Review / Test
5. Done

## Milestones

- `M0 Research & Bootstrap`
- `v0.1.0 My Dynasty MVP`
- `v0.2.0 My Dynasty Beta`
- `v0.3.0 All Dynasties Experimental`
- `v0.4.0 Integrated Dynasty Map`
- `v1.0.0 Stable`

## Labels

### Type
- `type:feature`
- `type:bug`
- `type:research`
- `type:docs`
- `type:maintenance`

### Area
- `area:map-renderer`
- `area:gui`
- `area:script`
- `area:performance`
- `area:compatibility`
- `area:release`

### Priority
- `priority:P0`
- `priority:P1`
- `priority:P2`
- `priority:P3`

### Special
- `blocked`
- `needs-game-test`
- `needs-profiler`

## Workflow

- New research/feature starts in Backlog.
- Move to Ready only when dependencies are satisfied.
- One active P0 engineering task at a time during initial PoC work.
- PR moves item to Review / Test.
- Done after the task's acceptance criteria are met. For documentation-only work, game-runtime validation may be marked not applicable.

Use `docs/BACKLOG.md` as the initial source when creating issues so stable planning IDs remain traceable in issue descriptions. Title format is `<ID> — <concise title>` (R/F/T/B ID only; no redundant textual type prefix); see [CODEX_WORKFLOW.md](CODEX_WORKFLOW.md). Substantial work uses one Issue as its investigation journal; the distilled completed result belongs in one `docs/tasks/<ID>-<slug>.md` file and one concise row in `docs/TASK_HISTORY.md`. `docs/CURRENT_STATE.md` names the active task and immediate queue.

Use `gh` for authorized GitHub operations. Reads and writes are separate permissions; never write remotely unless the task explicitly authorizes GitHub writes. Before writing, inspect the exact repository/Issue/PR and verify the result. Do not include raw logs, local absolute paths, account identifiers, credentials, or unreviewed screenshots in Issues. See [CODEX_WORKFLOW.md](CODEX_WORKFLOW.md).
