# T-027 — Reconcile research branch into main and freeze v0.1.0-rc.1

Issue: [#53](https://github.com/mhaduk/ck3-dynasty-map/issues/53).
Classification: STANDARD / repository integration. Direct execution was explicitly requested; no delegated implementation or independent-review claim.

## Integration checkpoint — 2026-10-27

The normal merge preserves both histories. The checkpoint tag `v0.1.0-rc.1` identifies the verified resulting `main`; the final remote commit/tag readback is recorded in the issue receipt. This is a development checkpoint, not SAFE FOR BETA, a production package, a GitHub Release, Workshop publication, or satisfaction of T-014/T-017/T-025. T-026 may audit this baseline; no optimization work was performed here.

Fetched pre-merge heads:

- `main`: `3a01ac07021c2a6f5c758cab64b8815d3b100c07`.
- `research/native-menu-alternative`: `5a99b4925e3367e3d2d9fd0820c5527bf112b64e`.
- Divergence: 3 main-only / 56 research-only commits.

The preserved main-only commits are `a6489838e80acf580c7ff3c9303fdd06f497882e` (Contributor Covenant), `ae25ed9fb362e74f5af28987078780dffc9eb169` (MIT License), and `3a01ac07021c2a6f5c758cab64b8815d3b100c07` (community standards).

The sole conflict was README's release-plan tail. Resolution retained the entire current research README and appended the exact License section from main. LICENSE, THIRD_PARTY.md, CODE_OF_CONDUCT.md and SECURITY.md match pre-merge main byte for byte. No runtime source, descriptor, script, test or workflow contract was changed. Only integration records and the verified issue-registry mirror were added/updated beyond that merge. The registry also reflects already-published T-026 and the T-017 title; neither task was executed.

## Validation

- Both original heads must be ancestors of final main; tag must equal that exact final head, checked again after publication.
- Focused tests: 11 DEV preparation, 10 mod preflight, 18 registry and 44 handoff/workflow tests passed.
- Full suite: 368 tests, 4 failures and 2 errors, all in historical classification assertions. An isolated archive of the exact research head reproduces the same six failures across 55 classification tests. Those source/test files are unchanged; this is pre-existing test drift, not a green full-suite claim, and no out-of-scope repair was made.
- Reconstructed `current-dev` before/after: identical inventory, bytes and SHA-256 across eight files; preflight PASS for 1.20.1.2. The checker compares disposable build artifacts, not the live installation.
- Legal/community files: exact main-side bytes retained; research/scripts/tests and workflow files remain unchanged.
- No game, launcher, installation, runtime test or release publication was required or performed.
- Public-content and staged-diff privacy checks precede commit; remote main/tag readback precedes final receipt.

## Execution observations and self-review

Initial Git metadata writes were denied by filesystem permissions; scoped authorized retries succeeded. The offline registry initially lacked T-027; synchronization and explicit T-027/#53 verification resolved it before execution. A trial merge predicted the README conflict, then the real merge reproduced it; the bounded resolution is described above. An optional process diagnostic was blocked by host permissions and was abandoned; test completion is read from the original command instead. Use the exact scoped Git permission on the first metadata-writing command and check registry binding before merging. No workflow optimization was implemented.

## AI cost

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6.1-sol | 738,978 | 651,264 | 87,714 | 2,935 | 741,913 | N/A |
| **Total** | 738,978 | 651,264 | 87,714 | 2,935 | 741,913 | N/A |

Partial coverage through 2026-10-27T14:59:41.073Z: one saved GUI session, 13 deduplicated response records, no CLI sessions or linked independent-review sessions. Model identity is recorded verbatim; gpt-6.1-sol has no verified public API price in this account, so it remains explicitly unpriced (N/A, not zero spend). No model alias or price is inferred. Context-rate pricing is unavailable. Cached input is a subset; reasoning is included in output. Cache-write input counters are zero in all recorded responses. Later validation, documentation and publication are excluded by the frozen cutoff. Private source snapshot, exact turn mapping and response audit are preserved locally; no raw session data is published.
