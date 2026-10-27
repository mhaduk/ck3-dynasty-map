# Changelog

All notable changes to Dynasty Map will be documented here.

## [Unreleased]

### Verified
- R-009's corrected current-DEV GUI fallback passes the bounded observer
  return, native Culture selection and manual reentry path on CK3 1.20.1.2.
  The reproducible `current-dev` builder emits the fixture-free eight-file
  candidate with that reviewed correction. Remaining persistence and lifecycle
  checks transfer to T-025; no beta-safety claim is made.
- F-004 bounded diagnostics: native DIAG V3 values and samples are delivered;
  separate REALMS, HOLDINGS and MY_REALM AUDIT V4 captures pass against their
  emitted rosters. The user accepts the fixed-row interaction in CK3
  1.20.1.2 / Steam 26046173. Historical failures, partial sample interval,
  unattributed initialization/court errors and lifecycle limits remain explicit.
- Added developer documentation for the native declaration channel, parser
  verdict boundaries, modifier gestures and fixed-row interaction.

### Research and design
- R-016 historical pipeline and three-view prototype research closed with bounded validation on CK3 1.20.1.2; neutral-grey rendering and production safety remain unresolved.
- Accepted Dynasty Realms, Dynasty Holdings and My Realm & Dynasty definitions consolidated in F-003.
- R-017 test-scenario, F-001 UI/contrast and F-002 color-source plans recorded.
- Reusable mod encoding/preflight rules and read-only file checker added.

### Added
- Local `Dynasty Map [DEV]` identity and preparation helper; obsolete installed
  probe entries retired while historical sources remain preserved. Production
  creation is deferred to T-014; no runtime behavior change.
- Player-first GitHub Wiki with supplied Before/After and three-view illustrations, grouped navigation, dedicated usage/compatibility pages and separate AI-cost documentation.
- Accepted shared CLI execution-review workflow with persistent executors, fresh read-only reviewers, per-task correction policies and registered handoff commands; formal T-023 cost closeout is pending GUI verification.
- T-013 Wiki: compact five-column AI-cost summary with a bold grand total;
  detailed accounting provenance remains separate and historical values are preserved.
- T-020 developer workflow: planned GUI-to-CLI tables append a concise execution
  summary bound to the frozen milestones, preserving existing telemetry and progress.
- T-012 developer workflow: local GUI session text estimates, aggregate history,
  context-history links in cost previews, calibrated CLI ranges with plan counts,
  and a consistent 30-cell Unicode progress line. No session-management decisions.
- T-010 private checkpoint metadata comparison: explicit saved-manifest pins,
  declared ranges, retained fingerprints and count context with source gaps
  preserved; no inferred continuity, new-event counts or causality.
- T-009 structured preflight: optional `--json` and a typed evidence inventory
  adapter preserve file-check findings, incomplete coverage and separate
  source/inventory verdicts; checked legacy text and exit behavior retained.
- T-008 offline evidence inventory: explicit file/hash pins, selected upstream
  statuses and declared equality links produce a private deterministic report
  with visible unknowns and gaps, without an aggregate runtime PASS.
- Project architecture and release plan.
- Research baseline for CK3 1.20.1.
- My Dynasty semantics and performance strategy.
- T-007 progress presentation: CLI handoffs relay successful persisted
  milestone transitions as concise standalone agent commentary, including the
  parent task, approximate percentage and readable stage. No-op/failure
  suppression and the GUI-review-pending completion cue are explicit.

## Planned [0.1.0]

### Added
- My Dynasty map mode.
- Direct / controlled / other county classification.
- Manual/static refresh.

## Planned [0.2.0]

### Added
- My Dynasty UI hardening, tooltips and profiling.

## Planned [0.3.0]

### Added
- Experimental All Dynasties mode.

## Planned [0.4.0]

### Changed
- F-001 closeout removes the unused diagnostics toggle, informational panel
  and three UI-only localization entries; modifier hints remain on each view.
  This records the actual two-file UI cleanup from cycle32, later installed in
  cycle35; it does not claim diagnostic-backend removal or a clean log.
- Integrated Dynasty map-mode UX with both modes.

## Planned [1.0.0]

### Added
- Stable public release of My Dynasty + All Dynasties.
