# F-001 — Dynasty map menu and visual contract

Issue: [#20](https://github.com/mhaduk/ck3-dynasty-map/issues/20).

Status: **OPEN / PARTIAL — closure blocked**, 2026-10-23. The user accepts the
shown menu, three-view grey/green appearance and focused interactions. The
final compatibility recovery removed three missing-template diagnostics, but
two unnamed duplicate-title errors persist on loading the existing session.
The agreed final-cycle stop condition therefore prevents narrowed F-001 closure.
This prototype is not a production, strict-audit or lifecycle acceptance claim.

## User pause checkpoint — 2026-10-23

Cycle31 has been reviewed as an honest published partial result. Its FAILED
closure status remains historical; no further CLI delegation, code change or
game test is requested. F-001 stays open while the user works on other tasks.
Resume only on explicit selection, using [the focused handoff](F-001-resume.md).
Two unnamed duplicate-title load errors remain; F-005/#30 owns their disposition.
F-004/#29 retains diagnostic gaps. Raw evidence and original journals are local
and preserved. Existing finite cost cutoff remains unchanged.

## Delivered scope and usage

One Dynasty parent in Additional Map Modes opens Dynasty Realms by default.
Three native-style child icons select Dynasty Realms, Dynasty Holdings and
My Realm & Dynasty; labels, legends, hover/selected frames and the accepted
appearance distinguish them. The temporary repeated shield remains approved;
final icons belong to [F-005](F-005-functional-followups.md#deferred-final-icons).
[F-003](F-003-dynasty-subview-definitions.md) defines the unchanged semantic
roles and precedence; F-002 owns a later Dynasty-derived color strategy.

| Child-icon gesture | Delivered operation |
|---|---|
| Ordinary click | Fresh guarded computation, then matching display; active re-click refreshes |
| Shift+click | Matching computation/display plus one summary |
| Option/Alt+click | Matching computation/display plus summary and bounded samples |
| Shift+Option/Alt+click | One explicit full three-view audit, without painting or selecting another map |
| Ctrl with any gesture | Same operation; Ctrl adds no action |

Hold modifiers through mouse release. The debugging area remains collapsed
and supplies shortcut hints. Native return/re-entry defaults to Dynasty Realms.
Opening unrelated menus, unavailable contexts and transition races retain
unverified coverage; do not infer their acceptance from ordinary clicks.

All three map IDs, five native zoom profiles per view and the fixed palette
25/105/50, 145/220/150, 65/70/80 are preserved. Ordinary routes retain fresh
player roots, liveness/Dynasty/CanChangeMapMode guards and compute-before-display
ordering. Exact context/dispatch safety remains R-005 research.

## Evidence retained from implementation and review

- Accepted supplied three-view screenshots establish the shown grey/green
  appearance; they do not certify every zoom, UI scale or relationship case.
- The Realms highest-ruler/self-liege defect was corrected before the accepted
  complete batch. Reviewed emitted records put Bukhara in Primary and Darghan
  in Neutral. One complete batch contained 4,703 emitted counties per view and
  14,109 role/intended-RGB agreements against the independent F-003 oracle.
  Emitted identities remain the input: this is not an independent world census,
  stored-RGB getter or pixel check.
- Nine temporary numeric controls showed positive locals/exports while
  localized counters rendered zero. SCOPE to TopScope.GetValue is documented;
  no numeric cure was proved or applied. Strict audit remains INCOMPLETE.
- Earlier two audit beginnings/one ending remain historical evidence; physical
  click count and the second interruption's cause are unknown. Current complete
  callbacks do not erase that finding or establish universal dispatch behavior.
- Source-derived checks cover the three slots and eight modifier combinations,
  guards, single dispatch, ordering and the combined no-paint/no-selection route.
  The independent parser still rejects missing/zero/contradictory declarations;
  no skip, expectedFailure or weakened acceptance was introduced.

The complete earlier local preparation/runtime journal was privately archived
before this public summary was distilled. Cross-chat T-005 reconciliation stays
accepted; no T-005 work is reopened or included in this feature's publication.

## Three-cycle closeout and final recovery

| Cycle | Actual result |
|---|---|
| 29 | Retired completed COUNTERPROBE/KEYPROBE scaffolding, side controls, trace/copy experiments and baseline mode. Seven-file source/install equality and 33 existing tests passed. F-004/#29 and F-005/#30 were created; F-001 stayed open |
| 30 | User-only menu and grouped normal/modifier/native-return smoke. Summary, samples and one full audit observed. Load reported three missing retired title templates and two unnamed duplicate-title errors; closure rejected. Approximate one-second click delay was user-reported, unmeasured and not a proved regression |
| 31 | Exact prior title/CoA declarations and six original localization entries restored; all other runtime bodies unchanged. Nine-file equality and the same 33 tests passed. User-only menu and focused paused-session load/selection check completed. Three missing-template errors absent, two duplicate-title errors persist; F-001 remains open |

The two restored files are inert compatibility declarations for loaded-state
references, with exact prior bytes/BOMs. Their original comments describe the
retired copy experiment; no old execution roots, trace hooks, side tester,
baseline profile, generated shader or vanilla artwork were restored. Static
reachability alone had been insufficient grounds to retire loaded references.

With CK3 declared closed, installation changed only those two additions and
localization. Verified backup covered the prior seven files, wrapper, enabled
manifest, five ordinary logs and a consistent read-only SQLite selection
snapshot. Actual ordered R016-only test selection, wrapper and manifest stayed
unchanged. All nine installed/source files match by inventory, bytes and SHA-256.
After user launch no installed files were written again.

The user explicitly reported main menu, then confirmed the existing session
was loaded and everything worked as requested. This contextually affirms the
focused icon/Holdings/combined-audit sequence; no independent UI observation or
literal selected-map ID was captured. One current full audit beginning/ending,
no rejection and no retired probe markers were observed. Strict numeric
analysis was not rerun against an unchanged known-failing contract.

The original startup append interval reset and remains INCOMPLETE. A separate
byte-zero current-generation capture was COMPLETE, confirming enabled/mounted
R016, both GUI completions and runtime 1.20.1.2. Error/GUI/conflict channels were
empty through menu; three bookmark and nine holy-order warnings remained
separately unattributed. The finite pre-load-to-test interval was COMPLETE:
error-channel diagnostics are two unnamed duplicate-title errors, 57 invalid
court-character trigger blocks and one court culture-set failure. Mirrored
channels are not additional incidents. GUI/conflict channels remained empty.

**Remaining blocker:** two `Duplicate landed title name` errors still occur on
load, without title names. Their cause, save-history relationship and persistence
or RGB impact are UNKNOWN. Removing the missing-template errors does not clear
this separate condition. No save was read/edited, no new fixture/control or
court/numeric root-cause investigation was started, and the final-cycle limit
was not converted into a passing verdict. The reviewed partial source and
findings may be published; the feature is not closed or represented as ready.

## Remaining owners and stop conditions

| Requirement | Owner and limit |
|---|---|
| Persistent unnamed duplicate-title load errors | [F-005 / #30](https://github.com/mhaduk/ck3-dynasty-map/issues/30); blocks F-001 closure pending explicit evidence/disposition, with R-009 retaining save/restoration research |
| Numeric zero declarations, strict framing/completeness, malformed role labels, readable bounds and automated verification | [F-004 / #29](https://github.com/mhaduk/ck3-dynasty-map/issues/29); strict status stays INCOMPLETE |
| Court-scene errors | F-004/F-005; attribution remains unknown and harmlessness is not established |
| Fresh/invalid context and real no-Dynasty coverage | [R-005 / #5](https://github.com/mhaduk/ck3-dynasty-map/issues/5), integrated later by F-005; unavailable is not Neutral |
| Exact original RGB restoration/isolation, save/load/removal | [R-009 / #9](https://github.com/mhaduk/ck3-dynasty-map/issues/9); a file backup cannot restore stored RGB |
| Independent global/projection/government coverage, UI-scale/zoom/parity/compatibility, performance and final icons | F-005; retain unmeasured approximately one-second click delay and existing fixture plans, without reopening completed research |

No automatic world scans, religious/Situation/decision carriers, lifecycle
waiver or ADR semantic change is introduced. No further game action or extra
microtask is requested by this result. The user alone starts/loads/tests/exits
CK3; Codex used files, logs and human reports, never game UI/process access.

## Verification and publication boundary

The 33 existing classification/parser/source-routing tests passed. Source and
installed preflights passed for nine files on target 1.20.1.2 / installed Steam
build 26046173. These are bounded checks, not a CK3 parser or universal API and
runtime guarantee. Compatibility recovery has a negative final acceptance
result because of the persistent duplicate-title errors.

Publication covers only the reviewed F-001 payload/analyzer/tests/README and
necessary F-001/F-004/F-005/state/backlog/history records. Unrelated workflow,
ignore/configuration and tooling changes remain excluded. The issue remains
OPEN; the closed-task Wiki must exclude F-001 even when measured partial costs
are recorded below. No completed-task history row is added.

<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| codex-auto-review | 137702 | 90624 | 47078 | 914 | 656 | 138616 | partial |
| gpt-6-luna | 18360165 | 17403264 | 956901 | 167261 | 44376 | 18527426 | partial |
| gpt-6.1-sol | 126810031 | 123501440 | 3308591 | 732531 | 175655 | 127542562 | partial |
| unknown | 344635 | 22784 | 321851 | 4501 | 0 | 349136 | partial |
| **Total** | 145652533 | 141018112 | 4634421 | 905207 | 220687 | 146557740 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-23T10:22:41.410082+00:00. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
Coverage is partial: explicitly mapped F-001 GUI/CLI/review work, failed attempts/retries and metadata-linked guardian reviews through the finite cutoff; prior R-016 work and shared T-005 work are excluded. Ambiguous or missing history is unallocated/N/A. Later accounting/publication and GUI receipt are excluded to avoid recursive accounting; this is not a full lifetime task cost or subscription/quota bill.

| Recorded model | Covered Standard API-equivalent USD |
|---|---:|
| codex-auto-review | N/A — unpriced |
| gpt-6-luna | $0.353353 |
| gpt-6.1-sol | $31.475997 |
| unknown | N/A — unpriced |
| **Known-model subtotal** | **$31.829350** |
| **Full total** | **N/A — unknown/review model buckets unpriced** |

Prices checked 2026-10-23: [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol), [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna). Per million uncached/cached/output tokens: $2/$0.10/$10 and $0.10/$0.01/$0.50. The 103 measured responses above 272,000 input tokens use the documented 2x input/cache and 1.5x output multiplier. Standard rates are an explicit API-equivalent comparison basis; actual service-tier, regional, cache-write, image/tool and other billing details are unavailable or excluded. Reasoning and cached tokens are subsets and are never added again.
<!-- ai-cost:end -->
