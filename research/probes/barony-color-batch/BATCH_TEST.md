# R-009 batch record — first launch completed, task partial

Target: CK3 1.20.1.1 (Crozier), 2026-10-20. This records the executed first
user-run batch and its coverage limits. It is not a request to repeat cases.
Sources and installation were left unchanged; after user exit GUI restored the
prior enabled selection. R009 remains installed but disabled. No new launch,
repair or mod-disabled test is authorized in the current documentation stage.

Codex used logs and user reports/supplied screenshots; all CK3 operation was
performed by the user. See [README](README.md) for payload boundaries and the
[canonical checkpoint](../../../docs/tasks/R-009-barony-color-safety.md) for
interpretation and native-color research. Raw logs/saves/chronology stay ignored.

## Executed / skipped / untested coverage

Counts below are complete BEGIN/END receipt pairs in the preserved final log;
effect markers distinguish execution from user-reported visuals. The original
plan allowed three C03 invocations; actual C03=5, C01=2 and C07=2. Do not record
the planned schedule as the actual experiment.

| ID | Actual state | Evidence and limit |
|---|---|---|
| C00 | Executed once | A/B, county/control and all four fixtures exist; A/B/county held, control/fixtures unheld. No writes |
| C01 | Executed twice | Direct RGB visibly purple on A; complete effect receipts |
| C02 | Executed once | Named-color write; visually unchanged from purple. Not numerical equality proof |
| C03 | Executed five times | Magenta-source copy, no obvious visual difference across repeats. Exact per-copy drift unmeasured |
| C04 | Skipped | Cyan landless source missing-capital setup error; no invocation |
| C05 | Executed twice | Yellow on A; second invocation after AFTER reload, while B stayed purple |
| C06 | Executed once, two targets | Same magenta source to A/B; visible purple. Shared source does not guarantee exact RGB |
| C07 | Executed twice | A -> B chained copy, no obvious extra shade difference. AFTER contains unequal A/B RGB, not a measured per-invocation drift law |
| C08 | Executed once, two targets | Copied definition-baseline source made both red; documented copy drift remains |
| C09 | Executed once with valid player; observer delivery unverified | Initial title-root receipt only. Reported observer clicks produced no new BEGIN/END/receipt; no engine cause inferred |
| C10 | Skipped | No new observer C09 receipt; no title-root reset invoked |
| C11 | Executed once, two targets | Direct definition RGB kept both red; arbitrary original/customized colors not captured |
| M01/M02/A01 | User-reported native/minimal/filled rendering | Native/filled area color stronger than minimal; differing crops/zoom preclude exact intensity comparison. Both custom keys available in same launch |
| L01 | Partial visual coverage; cleanup not met | Other modes reportedly normal, returning to native/custom baronies retains changes. Exact individual mode/zoom coverage bounded; no map-only isolation |
| S01 | Executed in same process with probe enabled | BEFORE and marked AFTER saved; AFTER reload initially Realms normal, baronies purple before effects; subsequent C05 worked. Fresh process/disabled mod not tested |
| L02 | Color retention observed after reported observer transition | NO PLAYER user-reported; colors unchanged. No automatic cleanup installed; not a new R-005 guard pass |
| D01 | Visibility confirmed; creation untested | Four sources in Find Title; Magenta says Not created yet. Reported creatability unverified, no Create action/requirements proven, no creation/grant performed |
| BEFORE rollback | Inconclusive as rollback experiment | Loaded only after C08/C11 had made both targets red. Reported red result does not prove loading reversed an active mutation; no repeat requested |
| S02 | Untested; separate future scope | Fresh-process/disabled-mod AFTER load, fixture residue and harmless removal remain open |
| X01 | Blocked | Exact live-original getter/capture/reset and automatic exit/context-loss cleanup not established |
| X02 | Rejected statically | No documented `reset_title_color`; name/CoA resets do not document map-color reset |
| X03 | Not shipped/tested | Snapshot into dummy title adds copy drift/higher-tier writes; not an exact-original solution |

## Setup errors and evidence limits

Startup mounted the installed batch and loaded the diagnostic GUI. Two source
files lack BOM; cyan reports a missing capital; all four fixtures produce CoA
generation errors. Court-scene errors also occur. GUI warnings empty; no
whole-run-clean or inertness claim. Bounded fixture failure led to C04 skip,
with independent cases retained; no source/encoding repair or restart occurred.

Direct/named/copy effects changed shared barony title state. Other-mode normal
appearance, Esc/Realms return, GUI receipt reset or restoring launcher selection
are not color restoration. C08/C11 use known definition red, not captured
originals. No automatic cleanup or classifier exists in this payload.

## Supporting serialization inspection — after the runtime batch

Only designated disposable BEFORE/AFTER originals were copied and inspected
read-only with existing ZIP/plain tooling; original hashes unchanged. AFTER
contains explicit title RGB overrides for A/B, absent in those BEFORE records;
the two AFTER values differ and are separate from CoA references. Four fixture
records occur in both saves, without proving creation/ownership. This establishes
serialization, independently of the same-process visual observation. It does
not establish disabled-mod/fresh-process rendering or a per-copy drift law.
No save was changed/deleted; no new game test occurred during analysis.

## Remaining gates and future-stage boundary

The separate class/palette model has no verified generic connection to a
view-specific renderer. Focused static work found engine-bound province textures
and documented Situation color/membership consumers; county precision, independent
view selection, saved/shared state and lifecycle need feasibility research
before another probe. Existing RGB/named writes remain state-mutating fallbacks,
not an approved production strategy. Do not add extra dummy titles.

If future runtime work is justified and explicitly scoped, combine independent
checks into one broad package with disposable saves and a clear stop point.
S02 requires a separately authorized launch: the user opens launcher/game via
Steam and performs all game actions; GUI owns configuration and log review.
Preserve existing saves/evidence, installed payload and prior selection. Do not
repeat passed R-005 fixtures, known NULL/lowborn diagnostics or these completed
copy/renderer cases merely to restate their results. No active user steps remain
in this historical checklist.
