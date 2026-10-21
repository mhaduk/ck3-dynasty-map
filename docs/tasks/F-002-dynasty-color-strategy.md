# F-002 — Dynasty color-source strategy

Issue: [#21](https://github.com/mhaduk/ck3-dynasty-map/issues/21).

Status: PLANNED successor research; no source/API investigation or palette
implementation performed in this planning stage. Fixed colors remain the
current fallback. This task is separate from F-001's menu and grey-ground work.

## Goal and candidates

Determine whether a usable Dynasty-identity accent can be obtained safely and
consistently, and choose a source/fallback contract. Compare these candidates
without treating them as equivalent:

1. An actual accessible Dynasty color, only if a supported target-build field
   or API is demonstrated for the relevant Dynasty object.
2. A House or coat-of-arms-derived hue. House identity is not Dynasty identity;
   multiple heraldic colors, complexity and cadet-House continuity may make
   this only an explicitly approximate visual cue.
3. A documented primary-title color fallback. This represents a title, not
   necessarily the Dynasty's own color; record its approximation and succession
   behavior rather than calling it a Dynasty color.

R-009 found a template color read that was unused and did not demonstrate an
active native House/Dynasty palette getter. Do not promote either into an API
claim. Never promise that every Dynasty has a usable exposed color.

## Evaluation criteria

- Stability for the same Dynasty across cadet Houses, succession and changes in
  primary title; clearly label any source that does not meet this criterion.
- Contrast against the required grey neutral ground, terrain and the second
  shade used by the three-category legend.
- A deterministic missing/invalid-color fallback and two distinguishable
  category shades derived from the chosen accent.
- Legend readability and accurate swatches when palette selection is dynamic.
- Supported target-build access, safe scope/context handling and save-state
  implications, including whether any persistent mapping is required.
- CoA complexity/multiple colors and whether extracting a color would require
  unsupported asset parsing or rendering inspection.

## Research deliverables

- A candidate comparison with evidence labels: verified field/API, documented
  behavior, approximation, or unresolved hypothesis.
- A proposed source/fallback decision and exact supported extraction contract;
  if no actual Dynasty color source is demonstrated, say so and retain the
  fixed-palette fallback pending an explicit product decision.
- A bounded evidence plan and acceptance matrix for same-Dynasty cadet Houses,
  succession/primary-title changes, missing colors, contrast and legend output.

Out of scope: asset parsing or pixel/color extraction from CoA rendering,
inventing an engine/API field, persistent color registry, implementing the
palette, expanding to All Dynasties, or changing ADR-010 category semantics.
F-001 may proceed with fixed palette values behind explicit palette/legend
slots; it must not hard-code green as a permanent product assumption. R-017
fixtures may guide later validation. F-002 begins only when separately selected
as the active backlog task.

Accepted category/appearance reference: [F-003](F-003-dynasty-subview-definitions.md).
