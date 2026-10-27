# R-009 barony color lifecycle and support contract

**Status: PROVISIONAL — current-build runtime verification pending.** This
contract records the bounded candidate boundary and the evidence needed for a
future GUI release decision. It does not declare the current renderer safe for
beta.

## State and observed effects

The renderer writes literal RGB values to the landed-title map-color field of
barony title records with `set_title_color`. Accepted save comparisons found
11,297 baronies gaining explicit RGB; the same values persisted across exit,
reload, and fresh-process loads without the DEV mod. Existing cleanup clears
transient script scopes, audit variables, and diagnostics. It does not restore
an arbitrary original title color. No supported arbitrary live-color read and
restore contract has been established in the bounded current-build sources.

The accepted cardinalate experiment also observed the unchanged vanilla effect
copying the selected temple barony's saved RGB to a new landless title, with
small channel shifts, in two constructed runs. Both runs contained a Papal
primary-title tier error. This establishes color-data propagation in those
runs; it does not establish visibility in ordinary map modes, gameplay impact,
or material harm. No normal barony color-picker was observed in the tested
holding customization surface; that bounded observation is not an exhaustive
consumer audit.

On exit, context loss, reload, or mod absence, already-painted RGB may remain.
The contract does not call transient `operation_cleanup` a color reset and does
not promise restoration. Persistence by itself is not evidence of harmlessness.
Any future run must compare existing painted RGB and native display state at
the named lifecycle checkpoints. A stale custom display after context loss is
a material unresolved outcome even if no new RGB write occurs. A new write in
an invalid context, or a neutral repaint caused by missing context, is a
failure. Existing RGB remaining unchanged is a different observation from
proving that the display is harmless.

## Supported candidate boundary

The opt-in `current-dev` DEV candidate is limited to fresh games and saves
demonstrably free of the three obsolete title fixtures:
`d_dynmap_r016_direct`, `d_dynmap_r016_controlled`, and
`d_dynmap_r016_other`. Old experimental saves remain preserved and outside this
candidate's compatibility promise; they are not migrated or repaired. Old RGB
overrides alone do not exclude a save. The candidate removes only the two
definition files for these fixtures, after exact-byte and retained-reference
checks. The historical ten-file source and default legacy builder behavior stay
unchanged.

The bounded absent-DEV experiment on older fixture-bearing saves produced
missing-template and duplicate-title diagnostics and removed the three named
fixture keys from the saved title map. That is a legacy-save compatibility
failure, not evidence that RGB itself caused the errors. External references
were not exhaustively searched. The `current-dev` candidate does not claim to
resolve this legacy debt. The older `r009-clean` profile retains its prior
eight-file output without the observer fallback.

## Accepted bounded observer result and remaining gates

On CK3 1.20.1.2, the corrected candidate automatically returned from the active
custom Dynasty view to native Realms in observer mode. The observer could then
select native Cultures; returning to the original player did not automatically
reenter Dynasty, and ordinary manual reentry worked. The final refresh save
matched the corrected pre-observer title identities and colors for all 18,190
records; bounded logs showed no new attributable error. This accepts the tested
observer path only. It does not establish all-world equality, safe removal,
harmless persistence, broad R-005 dispatch coverage, or beta readiness.

The earlier 81-barony repeated-cycle mismatch remains unexplained. T-025 / #51
owns that discrepancy, final corrected-candidate save/reload and fresh-process
DEV-absent checks, and full saved-title invariant comparisons. No new game tests
were performed as part of this closeout.

## Release gates still pending

The single planned two-start user sequence must verify current DEV startup,
three normal Dynasty views and repeated entry/reclick/refresh, native exit,
observer transition and return to the saved original character, painted-state
save/reload before any Dynasty click, and a fresh process with DEV absent loading
that designated save. The final comparison must reconcile canonical title key
and ID maps, all RGB fields, standard title colors/ownership/context, bounded
logs, and user-observed native views against the recorded baseline. Unsupported
view modes must be named as unavailable. No third start or exhaustive-map claim
is implied.

The real no-Dynasty fixture remains absent, so observer behavior does not close
R-005 context-loss coverage. No NULL/LOWBORN diagnostic calls are permitted by
this protocol. R-005 detection/guard work remains open and unimplemented here.
If stale display, invalid-context write, material state drift, or an attributable
startup/runtime failure remains, GUI must record **CURRENT RENDERER BLOCKED**
and identify that evidence. Missing errors or untested paths do not establish
harmlessness. Production packaging (T-014), R-005 closure, beta decision, and
publication are separate gates.
