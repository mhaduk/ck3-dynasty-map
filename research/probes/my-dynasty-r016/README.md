# R-016 — Three Dynasty views, source candidate

## Current package — F-001 compatibility recovery, 2026-10-23

Research prototype for CK3 **1.20.1.2 / Steam build 26046173**, not a production
release. User accepts the supplied grey/green three-view appearance. The reviewed
cleanup passed its seven-file installation and main-menu gate, but loading the
existing test session reported three missing retired helper-title templates and
two unnamed duplicate-title errors. The final recovery candidate restores the
exact two prior title/CoA files and six original name/adjective entries, bringing
the package back to **nine files** without restoring retired execution paths.
All 33 existing classifier/parser/source-routing tests and the nine-file source
preflight pass. Recovery installation passed with complete nine-file equality,
unchanged wrapper/manifest/ordered R016-only playset selection and verified
backup of the prior payload and five ordinary logs. User-only startup and the
focused paused-session interaction check passed.
The three missing-template errors are absent after restoration, but two unnamed
duplicate-title errors persist at load. **F-001 remains OPEN / closure blocked**;
visible operation and file equality do not clear that remaining condition.

| Retained entry | Operation |
|---|---|
| Dynasty parent | Fresh guarded `dynmap_r016_compute_realms`, then select `dynmap_my_dynasty` |
| Three child icons, ordinary click | Fresh guarded computation, then select the matching existing map ID; active re-click is refresh |
| Shift+click on a child | One summary pass and matching display |
| Alt/Option+click on a child | Summary plus at most 10 samples per role and 20 additional detail counties, then matching display |
| Alt/Option+Shift+click on a child | One explicit all-three-view V2 audit; no painting or map/selection change |
| Ctrl with any gesture | Same operation; Ctrl is ignored |
| Collapsed Dynasty Map debugging | Shortcut hints; no separate Test modifiers control |

Keep modifiers held through mouse release. Fresh `GetPlayer.MakeScope` roots,
character liveness/Dynasty/CanChangeMapMode guards, accepted F-003 predicates,
three map IDs, five native zoom profiles per mode, RGB **25/105/50**,
**145/220/150**, **65/70/80**, labels/legends/down states and native controls
are preserved. Local optional state is cleared before/after diagnostic
operations; full audit still suppresses every writer. Actor/roster/county
records, current V2 grammar, sample bounds and strict independent analyzer remain.

Retired: nine completed COUNTERPROBE insertions, eight side KEYPROBE SG/effect
pairs and key readout, old two-county trace/console wrappers and hooks, old
fixed-county direct/copy palette experiments, baseline map/banner and orphaned
comparison/check/refresh labels. The old copy-only helper landed-title and CoA
files are retained only as inert compatibility declarations for loaded-state
references. Their original comments describe the retired experiment; no current
compute/copy path uses them. This retention does not establish save safety or
the cause of the two duplicate-title errors. There are no new assets or copied
vanilla bodies. The internal `dynmap_r016_check` availability SG is retained and is not the retired
CHECK button. Shared player/Dynasty scope cleanup remains explicit.

Accepted prior batch: 4,703 emitted counties/view and 14,109 role/intended-RGB
agreements, Bukhara Primary/Darghan Neutral. Local/export controls were positive
while localized counts remained zero; the numeric localization is unchanged,
no formatting cure is applied, and formal analysis remains **INCOMPLETE**.
Another batch is unfinished for unknown reasons, physical click count is not
established and court-scene errors are separately unattributed.

[F-004 diagnostics / #29](https://github.com/mhaduk/ck3-dynasty-map/issues/29)
owns these diagnostic gaps. [F-005 functional/UX / #30](https://github.com/mhaduk/ck3-dynasty-map/issues/30)
owns remaining acceptance and deferred final icons; R-005/#5 retains context/
no-Dynasty research, R-009/#9 exact RGB restoration/save/removal, and F-002 color
strategy. Repeated shield imagery remains approved temporarily. Emitted-record
agreement does not prove independent global coverage, stored RGB, pixels,
universal context safety or safe removal. A file backup cannot restore RGB.

Cycle 29 used the user's CK3-closed declaration and verified a full prior
payload/wrapper/manifest/five-log backup plus a consistent read-only SQLite
snapshot of actual ordered selection. R016-only GUI Probe selection, wrapper
and manifest stayed unchanged. A fresh five-log prelaunch baseline is local.
Cycle 30 observed startup and normal/modifier callbacks, but the load errors
block closure. Cycle 31 uses a fresh CK3-closed declaration for this minimal
recovery, then user-only menu and paused-session load checkpoints in the same
task. The user confirmed the requested Holdings/combined-audit sequence worked
as expected; one complete audit frame was observed. Strict numeric acceptance
remains INCOMPLETE. Two persistent unnamed duplicate-title errors prevent
F-001/#20 closure. Only truthful partial source/evidence publication proceeds;
F-001 remains excluded from the closed-task Wiki cost inventory.

## Evidence and historical limits

The earlier local preparation journal was privately archived before this
summary was distilled. Historical trace, fixed-county palette experiments,
KEYPROBE/COUNTERPROBE and baseline commands are retired. Do not use old probe
instructions to repeat passed tests or modify a live installation.

[Current F-001 record](../../../docs/tasks/F-001-dynasty-map-ux.md) records the
accepted appearance, Realms self-liege correction, source/parser checks,
three-cycle closeout and remaining load blocker.
[F-003](../../../docs/tasks/F-003-dynasty-subview-definitions.md) defines the
unchanged role predicates; [R-016](../../../docs/tasks/R-016-my-dynasty-pipeline.md)
retains the historical pipeline's bounded feasibility evidence.

This source package references shipped textures and native map controls; it
does not package vanilla artwork, generated shaders, logs, saves or dumps.
Before a separately authorized installation, follow
[mod authoring rules](../../../docs/MOD_AUTHORING_RULES.md), preflight the exact
target version, preserve the existing playset and back up the current payload.
User alone starts/loads/tests/exits CK3. File preflight/equality is distinct
from engine parsing, live compatibility and safe RGB restoration/removal.

## Offline audit interface

The independent analyzer consumes explicit frozen debug-log captures, in order:

```sh
python3 scripts/analyze_dynmap_classification.py <frozen-capture> --output-dir .codex-sync/audit-review-new
```

Use a new ignored output directory. The default aggregate input cap is 512 MiB;
partial lines, missing framing, identity conflicts and contradictory/zero
declarations remain INCOMPLETE. V2 frames use `BATCH_BEGIN SOURCE F001_FIX_12
TARGET 1.20.1.2 SCOPE FULL` through `BATCH_END`; actor definitions/references,
county roster, REALMS/HOLDINGS/MY_REALM records and declared counts must agree.
V1 historical captures are supported separately; diagnostic summary/sample
operations cannot certify a full audit. Exit 0 is complete emitted-evidence
agreement, exit 1 a semantic/intended-RGB mismatch, exit 2 incomplete/unverified
evidence or input/output error. None verifies stored RGB, pixels or independent
global coverage. Keep reports, county records and raw captures private.
