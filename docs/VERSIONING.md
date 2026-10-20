# Versioning and Release Process

## Scheme

Use Semantic Versioning: `MAJOR.MINOR.PATCH`.

Before 1.0:

- `0.MINOR.0` = meaningful feature milestone or architecture change;
- `0.MINOR.PATCH` = bug fix / compatibility validation / documentation fix without new major functionality.

After 1.0:

- `MAJOR` = incompatible behavior/configuration change;
- `MINOR` = backward-compatible feature;
- `PATCH` = backward-compatible fix.

## Version sources that must agree

For a release, these values must match:

1. `descriptor.mod` -> `version="X.Y.Z"`
2. Git tag -> `vX.Y.Z`
3. `CHANGELOG.md` release heading
4. GitHub Release title
5. Workshop changelog/version text when published

The CK3 game compatibility version is separate:

`descriptor.mod -> supported_version="1.xx.*"`

## Branching

Keep the process simple:

- `main` must remain releasable;
- use short-lived `feature/...`, `fix/...`, `research/...` branches;
- merge through PR once GitHub workflow is established;
- no permanent `develop` branch for a project this size.

## CK3 patch maintenance procedure

When Paradox ships a new CK3 minor/major patch:

1. Do **not** immediately bump `supported_version`.
2. Record the new CK3 version in `docs/COMPATIBILITY.md`.
3. Diff locally the vanilla files our mod integrates with, especially map modes and GUI.
4. Regenerate `script_docs` and `dump_data_types`.
5. Run CK3 Tiger against the new vanilla install.
6. Run the full core functional test matrix.
7. Inspect `error.log` against a vanilla baseline.
8. Re-run Script Profiler smoke test.
9. Update compatibility documentation.
10. Only then update `supported_version` and release a patch/minor version.

## Changelog policy

Use a Keep-a-Changelog style:

- Added
- Changed
- Fixed
- Performance
- Compatibility
- Known issues

Every user-visible behavior change belongs in `CHANGELOG.md` before release.

## Milestone validation policy

- Documentation-only changes may mark game-runtime validation not applicable;
  perform textual consistency/link/diff checks and do not claim runtime testing.
- v0.1 requires Tiger/error.log review and minimum smoke/regression coverage of
  safe activation, classification, rendering, dependable refresh/re-activation,
  exit/restore and unavailable behavior. Record active-context loss handling and
  visible hitch observations. Verify re-click in M0 or supply the smallest
  explicit refresh mechanism needed.
- v0.2 adds deeper hardening, profiler baselines, state/save/load/removal tests and
  compatibility coverage. Apply the relevant regression checks to later patches;
  measure again when iteration/rendering or the game build changes.
- Safe removal is desirable during v0.x; known limitations may be documented.
  For v1.0, safe removal or a clearly proven harmless removal path is required.
  A documented harmful or unknown removal outcome does not satisfy that gate.

## Release checklist

Apply checks at the depth required by the milestone above. Record each deferred
pre-1.0 check and limitation explicitly; do not waive v0.1 lifecycle acceptance
or the v1.0 removal-safety gate.

- [ ] Target CK3 version recorded
- [ ] All milestone P0/P1 issues closed or explicitly waived
- [ ] Tiger run reviewed
- [ ] `error.log` compared to vanilla baseline
- [ ] Milestone smoke/regression matrix passed, including activation, unavailable state, refresh and exit/restore
- [ ] Save/load coverage passed at milestone depth; pre-1.0 limitations or untested cases documented
- [ ] v0.x removal findings/limitations documented; v1.0 safe removal or proven harmless path demonstrated
- [ ] v0.1 visible-hitch smoke observations recorded; v0.2+ profiling baseline/regression evidence captured as applicable
- [ ] `supported_version` validated
- [ ] README/docs updated
- [ ] CHANGELOG finalized
- [ ] descriptor, tag, changelog versions match
- [ ] Git tag `vX.Y.Z` created
- [ ] GitHub release created
- [ ] Workshop update only after local release artifact passes smoke test
