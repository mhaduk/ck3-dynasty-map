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
- Done only after required in-game validation.

Use `docs/BACKLOG.md` as the initial source when creating issues so planning IDs remain traceable in issue descriptions.
