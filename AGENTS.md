# Codex project instructions

## Project and source of truth

Dynasty Map is a pre-implementation Crusader Kings III mod project. Immediately
after this file, read [docs/CURRENT_STATE.md](docs/CURRENT_STATE.md). Keep it
synchronized whenever project state materially changes, including research
results, blockers and the single next task. It summarizes state; detailed
evidence and accepted decisions remain in their existing documents. Read
README.md, CONTRIBUTING.md, docs/PROJECT_CHARTER.md, docs/DECISIONS.md and
docs/ARCHITECTURE.md before proposing changes. Use docs/ROADMAP.md and
docs/BACKLOG.md for scope and sequencing, and docs/RESEARCH.md for open gates.
Preserve existing documentation and architecture decisions. Report conflicts
rather than silently choosing new semantics; record necessary architecture or
semantic changes in docs/DECISIONS.md.

The repository documentation governs product intent. For CK3 API details,
verify the actual installed target build and locally generated script_docs /
dump_data_types; historical examples and the documented research baseline are
not proof of current compatibility. Community documentation and archived repositories
are historical/reference evidence only. Claim target-build verification only with
installed vanilla, generated script_docs or runtime evidence recorded during M0.
Record original findings in docs/RESEARCH.md.

## Current scope

Repository bootstrap and research come first. Do not create CK3 implementation
files, descriptors, dummy titles, localization or GUI scaffolding until an
implementation task is explicitly requested and its research prerequisites
are satisfied. Follow docs/SECOND_MAC_BOOTSTRAP.md for future local research.
Do not claim game validation or tooling checks that were not performed.

## File ownership and provenance

- Do not copy or modify vanilla CK3 files. Inspect installed files read-only
  when authorized research requires it; keep game files out of Git.
- Keep generated API dumps, saves, logs, local paths and reference material
  in ignored local directories. Commit only original findings and selected,
  reviewed test evidence, never raw copyrighted dumps.
- Do not import third-party code without verified reuse terms and provenance
  recorded in THIRD_PARTY.md.
- A future need for a vanilla GUI copy must be resolved against ADR-006 and
  the current task restrictions before proceeding.
- External launcher .mod files are machine-local. A future repository-owned
  descriptor.mod may be tracked after review; do not create it during bootstrap.

## Required design invariants for future implementation

- Implement My Dynasty first; compare Dynasty identity, including cadet Houses.
- Classify each county by its legal holder: DIRECT if the holder shares the
  player's Dynasty; otherwise CONTROLLED if any de-facto liege shares it;
  otherwise OTHER. DIRECT takes precedence.
- Propagate the county classification to its de-jure baronies; write colors
  only to baronies. Occupations, tributaries and regents do not change semantics.
- Guard absent holders and Dynasty scopes. A holder without a Dynasty still
  requires the liege-chain check and may be CONTROLLED; only a holder sharing
  the player's Dynasty is DIRECT.
- Under ADR-008, My Dynasty is unavailable unless both the local player and
  player Dynasty are valid. Unavailable activation performs no classification or
  color writes; never substitute an all-neutral map. If context becomes invalid
  while active, stop using the old Dynasty and clear/restore visual state as far
  as the API permits. M0 must verify UI disabling/hiding and lifecycle cleanup.
- v0.1 requires dependable manual refresh: verified re-click activation or the
  smallest explicit refresh mechanism if re-click is unavailable.
- Refresh on activation/manual request for v0.1–v0.2. No daily/monthly scans,
  recurring inactive work or persistent graph/cache in the MVP. Profile before
  proposing optimizations; recurring global scans require profiler evidence
  and an ADR.
- Prefer additive UI integration and separate named modes over global state.
  Verify all UI, scope, iterator and color-effect research gates locally.
- Keep All Dynasties behind its documented color-strategy gate; document
  stability, collisions and save-state behavior before merging implementation.
- Use dynmap_* script/localization IDs, d_dynmap_* dummy titles and the dynmap
  event namespace. Prefix owned filenames with dynmap_ where loading rules allow.

## Workflow and validation

- Keep main releasable. Use short-lived feature/, fix/ or research/ branches
  for subsequent work. Follow the existing issue and PR templates.
- Keep changes focused. Update relevant docs/tests for behavior changes,
  ADRs for semantics/architecture, and CHANGELOG.md for user-visible changes.
- For documentation/bootstrap work, check diffs, links, ignore rules and staged
  content; CK3 execution is not required for documentation-only changes.
- Documentation-only changes may mark game-runtime validation not applicable.
- For implementation, use the milestone coverage in docs/TEST_PLAN.md: CK3 Tiger, error.log against a
  vanilla baseline, relevant functional/state tests and profiler evidence for
  iteration/rendering changes. Record build, DLC/playset and test limitations.
- Multiplayer and total conversions are unsupported unless deliberately tested.
- v0.1 requires lifecycle/classification smoke and regression coverage; v0.2 adds
  deeper hardening, profiling and compatibility tests. Removal limitations may
  be documented during v0.x; v1.0 requires safe removal or a proven harmless path.
- Follow docs/COMPATIBILITY.md and docs/VERSIONING.md for release work. Never
  bump supported_version solely to suppress launcher warnings.
- Do not commit, publish, create releases or upload to Workshop unless requested.
