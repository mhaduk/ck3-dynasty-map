# Second-Mac Bootstrap Checklist

This is the first session checklist for the Mac that actually has CK3 installed.
For current progress, read [CURRENT_STATE.md](CURRENT_STATE.md) and
[TASK_HISTORY.md](TASK_HISTORY.md) first. R-001 is
complete for 1.20.1.1 as of 2026-10-20; clean vanilla API generation is complete;
save/map-mode baseline coverage is still pending (R-011). This checklist is not authorization to create a mod skeleton
before an implementation task and its research prerequisites are approved.

## 1. Confirm the target

Record:

- CK3 exact version/build;
- Steam branch (normal/beta);
- macOS version;
- DLC enabled;
- whether CK3 1.21 has replaced the current 1.20.1 research baseline.

## 2. Development launch options

Use:

`-debug_mode -develop`

The modding guide recommends these options for console access and hot reload where supported.

## 3. Deferred until implementation authorization: create the local mod

Create `Dynasty Map` in the launcher so CK3 generates correct local descriptors for that machine.

Then reconcile the generated folder with this repository. The machine-specific external `.mod` file must **not** be committed; `descriptor.mod` inside the repository can be committed after review.

## 4. Inspect local references read-only

Inspect the installed vanilla files in place. Do not copy or modify them.
Use a gitignored directory such as `local/` for original research notes and
machine-local paths; commit only reviewed findings in the project documentation.

Inspect locally at minimum:

- `game/gfx/map/map_modes/map_modes.txt`
- current map-mode GUI files under `game/gui/`, including unavailable UI and activation/refresh/exit hooks
- relevant `_*.info` files near map modes/scripted GUI if present

## 5. Generate current API documentation

From CK3 console run:

- `script_docs`
- `dump_data_types`

Keep generated logs local/gitignored. Extract only project-relevant findings into `docs/RESEARCH.md`.

## 6. Capture a vanilla log baseline

Run CK3 with no mods, open a save, interact with map modes, then archive locally:

- `logs/error.log`
- relevant debug logs

This lets us distinguish our errors from vanilla noise.

## 7. Install developer tooling

Recommended:

- VS Code
- CK3/Paradox language extension of choice
- CK3 Tiger (local validator)
- Git

Do not make CI depend on copyrighted vanilla CK3 files stored in the repository.

## 8. Run the nine M0 research probes

Work through `R-002` through `R-010` in `BACKLOG.md` before writing final implementation.

The first executable PoC should do only this:

1. enter a custom barony-color map mode;
2. color one known test barony safely;
3. return to normal map modes;
4. produce no new error-log spam.

Also verify unavailable activation does no classification/color writes, active-context loss stops old-Dynasty use with API-supported cleanup, and re-click works as refresh. If re-click is unsupported, select the smallest explicit refresh mechanism. Record evidence under RG-UI-01, RG-PLAYER-01 and RG-STATE-01.

Only after the relevant research gates succeed should My Dynasty world scanning be added.

## 9. First My Dynasty PoC

Implement the simplest correct three-state classifier, refresh only on click, and profile it before considering caching or live updates.
