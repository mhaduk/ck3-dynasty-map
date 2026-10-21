# F-001 — Dynasty map menu and visual contract

Status: PLANNED successor specification; no implementation authorized here.
The three-view semantics, labels, order and default are accepted in ADR-010.
This plan defines the review needed to turn the R-016 candidate UI into a
product contract while preserving unresolved feasibility and safety gates.

## Accepted product decisions

- One top-level Dynasty map entry; while active, associated subviews appear in
  this order: Dynasty Realms (default), Dynasty Holdings, My Realm & Dynasty.
- Each view uses ADR-010's county semantics and dark-over-light precedence.
- The selected subview and its legend are visible. English labels are approved.
- Fixed colors remain usable as a temporary palette interface; F-002 owns
  whether a Dynasty-derived accent is supportable.
- Grey nonmatching land is a P0 visual acceptance requirement. Poorly visible
  grey in R-016 is a known failed acceptance item, not a closed defect.

## Proposed interaction and layout contract

```text
Map mode bar: [Dynasty]
Active map banner: [Dynasty Realms] [Dynasty Holdings] [My Realm & Dynasty]
Legend:          [dark swatch + meaning] [light swatch + meaning] [grey swatch + meaning]
Actions:         [Refresh] [Return to Realms]
```

Treat this as a compact proposal, not a claim that current panel placement or
native overrides are final. Keep the active map and current selection clear;
make each subview a direct selection. Refresh recomputes the selected view from
fresh player/Dynasty context. Returning to Realms selects that view explicitly.
Opening an unrelated menu must not scan or silently change the selected view.
The accepted initial entry and family re-entry default is Dynasty Realms.
Opening or closing an unrelated menu while Dynasty remains active preserves
the selected alternative. Leaving for a native map and re-entering Dynasty
returns to Dynasty Realms; it does not restore the previous alternative.

Unavailable context must visibly disable or hide entry/actions and must not
dispatch a character-rooted classifier. On context loss while active, the
required unavailable/cleanup behavior remains an ADR-008 and R-005/R-009 gate;
do not imply that a grey repaint, GUI watcher, or launcher state solves it.
Final user flow must not depend on diagnostic controls. Keep diagnostics
collapsed/developer-only during development, then remove them from the normal
flow.

## Visual acceptance matrix

| Area | Acceptance |
|---|---|
| Classification and projection | Correct dark/light/grey semantics per ADR-010; all county baronies, including secondary baronies, receive the county result |
| Neutral ground | Nonmatching land has an unmistakable grey fill across relevant views; classification, projection and renderer behavior are investigated before changing only the palette |
| Boundaries | Specify ocean and impassable-land behavior explicitly. Current proposal: leave non-county ocean/impassable regions to native rendering; do not paint them grey unless a supported rule is established |
| Contrast | Check near and distant zoom, supported UI scales, selected versus unselected control, map terrain and color-vision-independent cues |
| Redundant cues | Show selected subview by both label/state treatment and shape/outline; category meaning must not rely on hue alone |
| Legend | Swatches and text match the actual active palette and semantics; no hard-coded green assumptions if F-002 changes the accent |
| Refresh and return | Refresh visibly targets the selected view; Return selects Realms; ordinary native round-trip and re-entry follow the reviewed persistence rule |
| Availability and safety | No invalid-root dispatch, stale-context display, or unsupported exit/removal claim; lifecycle behavior has explicit evidence and owner |

## Stages and dependencies

1. Review the compact layout proposal, labels, selection/default rules and
   acceptance matrix. Mark each point as accepted, proposed or unresolved.
2. Perform a narrow technical gap audit against R-016, R-010, R-005, R-009,
   ADR-008/009/010 and target-build evidence. Diagnose the grey failure across
   classification, county-to-barony projection and rendering; do not assume a
   shader/terrain-only cause. Reuse existing evidence; new source research or
   runtime requires its own bounded scope.
3. Prepare an implementation handoff only after the UX specification is
   reviewed. Keep safe normal activation separate from diagnostic execution.
4. Stage grouped visual and interaction acceptance, then address lifecycle,
   compatibility, privacy and release gates with their existing owners.

R-017's selected fixtures should inform later acceptance coverage. F-002 owns
color-source feasibility and does not block this task's initial grey diagnosis,
layout specification or use of explicit palette slots. R-005/R-009/R-010 and
R-013 dependencies remain visible; F-001 does not promise to solve every
historical lifecycle or compatibility issue. No ADR waiver, issue creation,
implementation, installation or test is included in this planning record.

Accepted category/appearance reference: [F-003](F-003-dynasty-subview-definitions.md).
