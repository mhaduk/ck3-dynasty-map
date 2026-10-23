# F-005 — Dynasty Map functional follow-ups

Issue: [#30](https://github.com/mhaduk/ck3-dynasty-map/issues/30).
Diagnostic successor: [F-004 / #29](https://github.com/mhaduk/ck3-dynasty-map/issues/29).

Status: OPEN follow-up, created 2026-10-23 from the bounded F-001 closeout.
This record tracks unverified acceptance and deferred UX. It does not assert
new defects, replace research owners or promise release safety. No new feature,
icon, runtime test or lifecycle waiver is implemented here.

## Evidence and residual acceptance

Accepted: one Dynasty parent and three native-style children, selected-view
labels/legends, supplied grey/green appearance, observed ordinary/modifier
callbacks, and 14,109 emitted role/intended-RGB agreements across 4,703 emitted
counties per view in the complete batch. Bukhara is Primary and Darghan Neutral
in reviewed current records. F-003 semantics and fixed palette remain unchanged.
Formal audit is INCOMPLETE: localized declarations are zero and another batch
is unfinished. F-004 owns those diagnostic gaps; record agreement alone proves
neither global coverage nor stored RGB, screen output or lifecycle safety.

| Unverified requirement | Existing evidence / gap | Owner and minimum follow-up | Acceptance / stop |
|---|---|---|---|
| Current-player availability, invalid root, context loss and no Dynasty | Ordinary routes use fresh player roots and guards; no universal dispatch/transition-race or no-Dynasty integration acceptance | R-005 / [#5](https://github.com/mhaduk/ck3-dynasty-map/issues/5) owns remaining API/context and fixture-or-coverage decision; F-005 later integrates the established contract | Valid/invalid and context-loss paths have explicit bounded evidence and no writes on unavailable context; stop dependent tests on an unresolved unsafe dispatch, never equate unavailable with Neutral |
| Exact original RGB restoration, isolation, save/load and removal | Current views share mutable title RGB; write attempts/intended RGB do not prove storage or restoration | R-009 / [#9](https://github.com/mhaduk/ck3-dynasty-map/issues/9) owns safety research; F-005 tracks dependent feature acceptance, including removal of retired helper definitions | Exact supported lifecycle behavior and limits are verified before release claims; stop on persistent unintended changes, preserve saves, never promise a file rollback restores RGB |
| County-to-all-barony projection and independent global coverage | County-rooted barony filtering and bounded historical sample exist; 4,703 emitted counties are not an independent census | F-005, using existing F-107/T-114 plans and completed R-008 method; choose one independent coverage/projection oracle | Every expected county and constituent barony is accounted for, including secondary/unheld/edge cases, without deriving the expected set from the same emitted stream; unexplained gaps stop global acceptance |
| F-003 roles across governments and edge relationships | Synthetic examples and bounded current record agreement; special governments, missing Dynasty, vassal/sibling/cadet fixtures lack complete runtime coverage | F-005 with R-017 fixtures and existing T-111/T-112/E-204/E-205 plans; do not reopen completed traversal research without conflicting evidence | A bounded natural fixture matrix agrees with F-003; unexpected classification stops that feature case, not an unrelated diagnostic-cure loop |
| Zoom, UI scale, contrast, ocean/impassable boundaries and redundant cues | User accepts supplied views/zoom; other scales/contexts remain unverified; three definitions retain native zoom profiles | F-005: agree a small supported visual matrix, retain labels/down frames and native non-county rendering | Active view/legend and neutral land remain clear at supported scales/zooms, boundaries documented; do not infer all-scale acceptance from supplied captures |
| Native round-trip, refresh, unrelated-menu persistence and compatibility | Historical ordinary smoke appeared to work; shared menu/banner override seams remain, raid/barter parity omitted | F-005: one grouped native-return/re-entry/active-reclick/unrelated-menu smoke, then targeted compatibility/parity cases only where required | Re-entry defaults to Realms, active re-click refreshes, unrelated menus preserve selection without computation, native controls meet declared parity; stop on unsafe regression or conflicting override |
| Performance and normal-flow usability | No accepted world-compute timing or responsiveness budget; diagnostics are opt-in | F-005: measure one declared representative normal refresh and bounded diagnostic operation, agree a budget before claiming performance | Report actual latency/output limits and supported environment; stop a runaway operation through user coordination, never silently expand scans/background work |

Existing [F-002](F-002-dynasty-color-strategy.md) / #21 remains the separate
Dynasty-derived color-source/fallback owner. This task preserves F-003 / #22
semantics and does not reopen or duplicate the closed R-007/R-008/R-010 research.

## Deferred final icons

Transferred from the historical local [F-004 icon record](F-004-icon-preparation.md),
whose content/history remains intact. Accepted symbol direction: Dynasty parent
shield, Dynasty Realms crown, Dynasty Holdings castle, My Realm & Dynasty shield
with crown. The last combined symbol was not established in the bounded CK3
asset inspection; reuse those findings instead of repeating the search.

The user permits the same shield for the parent and My Realm & Dynasty during
tests. Labels/tooltips, selected state and active-view name distinguish them;
temporary duplication is not final artwork acceptance. When selected later,
agree any changed visual direction first; choose/provide the final symbols,
verify provenance/permitted use, native-size/UI-scale legibility and normal,
hover and selected states. Reference native assets instead of copying vanilla
artwork into the public repository. Update only icon mapping/references without
changing F-003 semantics or menu behavior. No asset search, image generation,
composite or redesign is assigned in the current cleanup cycle.

## F-001 bounded closeout update — 2026-10-23

The user accepts the delivered F-001 menu, appearance and ordinary interaction
on fresh 867 Ismail sessions and directs narrowed feature closure. Cycle34/35
complete error-channel lines did not reproduce the two unnamed duplicate-title
errors from the earlier existing-session load. The cause and save persistence
impact remain UNKNOWN; overall captures are INCOMPLETE at a partial final debug
line, and other initialization/court errors remain unattributed. F-005 continues
to own old-session compatibility, functional/UX coverage and deferred icons.
This does not claim the old save is repaired or establish lifecycle safety.

## Completion boundary

F-001's accepted bounded scope does not complete F-005, F-004, R-005 or R-009.
Each residual item needs its own evidence or explicit supported coverage
decision; genuine unsafe regressions remain blockers for the affected scope.

## Cycle30 verification and cleanup blocker — 2026-10-23

Main-menu startup passed for the narrowed smoke: runtime 1.20.1.2, enabled and
mounted R016, both cleaned GUI loads complete, empty error/GUI/conflict
channels at that checkpoint. The original append capture detected reset logs
and was retained INCOMPLETE; one byte-zero fresh-generation recovery was
COMPLETE. Startup does not prove loaded-session compatibility.

The user reports the ordinary three-view sequence and modifier steps done,
with approximately one second of delay after clicking and an uncertain
impression that recalculation became slower. This is a user estimate, not a
measured performance regression or agreed budget. Native return/re-entry was
done and returned to Dynasty Realms, which is the expected default. Specific
visual subchecks and Holdings retention after the combined gesture must not
be inferred solely from completion or audit markers; retain any missing
explicit observation as unverified. The finite test capture contains one
summary, one sample operation and one complete framed full audit; strict
numeric acceptance remains INCOMPLETE under F-004.

**Cleanup compatibility blocker:** before those diagnostic operations, the
loaded session reported invalid templates for `d_dynmap_r016_direct`,
`d_dynmap_r016_controlled` and `d_dynmap_r016_other`, plus two duplicate-title
name errors with no name supplied. These are concrete R016 retired-helper
reference errors in the cleaned package session. Their origin, save-history
relationship, duplication cause and persistence/RGB impact are unknown: no
save was read, and no control or repair was performed. Do not attribute the
duplicate entries to particular titles without evidence. This prevents a
clean cleanup/lifecycle verdict and narrowed F-001 closure readiness despite
the successful menu gate and observed callbacks.

Preserve this evidence and stop further dependent writes/tests. F-005 owns
the cleanup compatibility disposition with R-009 / #9 retaining exact
restoration/save/removal research ownership; R-005 / #5 is unchanged. GUI
should review one focused compatibility recovery decision within the final
cycle budget, not start another numeric probe or assume restoring files
repairs saved RGB. No automatic rollback, save editing, fresh fixture test,
new launch or source/install change is authorized by this verification.

## Cycle31 partial compatibility recovery — 2026-10-23

Restored only the exact prior landed-title/CoA files and six original
name/adjective localization entries, with original BOMs. These are inert
compatibility declarations; retired copy/trace/probe/baseline execution paths
stay removed. All other runtime bodies are unchanged. The same 33 existing
tests and source/installed nine-file equality passed; wrapper, manifest and
actual ordered R016-only selection were preserved after verified backup.

User-only startup passed through menu. The existing paused session then loaded,
and the user confirmed the requested icon/Holdings/combined-audit interaction
worked as expected. The complete finite load interval has **zero missing-title
template errors but two remaining unnamed duplicate-title errors**. Three
specific retired-template diagnostics are absent after restoration; this does
not establish the duplication cause or repair stored RGB/save state. No title
name is supplied by the remaining errors, so no title attribution is invented.
The same 57 invalid court-character trigger blocks plus one culture-set failure
remain separately unattributed. One full audit is framed; strict numeric
acceptance stays INCOMPLETE and was not retested or weakened.

**F-001 remains OPEN / NOT READY for closure.** F-005 owns the precise remaining
compatibility blocker; R-009 retains restoration/save/removal and R-005 context
ownership. No new test/fixture/save research, installation or cycle32 is started.
The approximately one-second click delay remains an unmeasured prior report.
A later disposition must account for the two actual duplicate-title errors
before accepting compatibility; correct visible behavior alone is insufficient.
