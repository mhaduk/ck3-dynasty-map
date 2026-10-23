# T-011 — Deferred workflow optimization ideas

Status: **OPEN / DEFERRED** — tracked in [issue #37](https://github.com/mhaduk/ck3-dynasty-map/issues/37). This is an archive of candidates for later prioritization, not an implementation task. No priority override or implementation date is set.

## Delivered foundations and boundaries

- [T-008](T-008-workflow-optimization.md) delivers an explicit pinned inventory, independent upstream statuses and declared equality links. Full semantic validation across payload, installation, checkpoint, marker and analyzer remains deferred until stable identity and receipt contracts exist. It does not synthesize engine PASS.
- [T-009](T-009-structured-preflight.md) delivers opt-in structured preflight and a compatible inventory adapter with legacy parity, typed status and coverage. It does not prove CK3 syntax, API or runtime compatibility.
- [T-010](T-010-checkpoint-comparison.md) delivers private finite saved-manifest metadata, range-field and fingerprint comparison. Generation and continuity remain UNKNOWN; deltas are null and causality is UNPROVEN. Broader log profiles, trusted generation/identity and comparable-window analysis remain deferred.

## Candidate disposition

| Candidate | Delivered | Deferred remainder | Value, risk and dependency | Reopen when |
|---|---|---|---|---|
| 1. Thin report | T-008 bounded inventory | Broader projections | Less repeated assembly; keep upstream status and unknowns | A repeated evidence need is named |
| 2. Cross-stage links | Basic declared equality links | Full payload/install/checkpoint/marker/analyzer semantic chain | Useful consistency checks; depends on stable identity/receipt contracts | Those contracts and bounded fixtures exist |
| 3. Log profiles and comparisons | T-010 finite metadata comparison | Profiles, trusted generation/identity, comparable windows | Better change context; avoid causal claims | Named logs and comparable-window rules are accepted |
| 4. Structured preflight | T-009 contract and adapter | Additional producers only if needed | Stable machine-readable evidence; no syntax/API/runtime proof | A consumer has a concrete need |
| 5. Explicit manifests/pins | Bounded tools use named pins | Broader reusable named-input manifests and payload pins | Reproducibility; no broad discovery/live fallback | Repeated named-input duplication is shown |
| 6. Append-only archive/compare | Not implemented; scoped cleanup backup is not this feature | Reusable archive, comparison and sanitized summary tooling | Traceability with privacy and retention risks | A bounded retention need and policy are defined |
| 7. Parametric deployment/rollback | Not implemented | Separate deployment and verified rollback workflow | Higher operational risk; separate permission class required | Safe app state and rollback contract are explicitly approved |

The T-002 AI accounting ledger remains separately deferred and excluded. Automatic discovery/repair, engine claims and user-only game actions remain boundaries; they are not implied future backlog features. Every candidate needs fresh evidence, scope, acceptance criteria, permissions and GUI selection before implementation.
