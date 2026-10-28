# T-026 — Astra audit and workflow optimization

Issue: [#52](https://github.com/mhaduk/ck3-dynasty-map/issues/52). Local implementation accepted; frozen GUI cost gate passed, Wiki/Issue publication and readback completed, and #52 closed COMPLETED on 2026-10-28. The scoped branch commit/tag/push remains pending.

## Baseline and scope

T-026 started from `main` / `v0.1.0-rc.1` at `3f670481bf11da10811b47cc7ea5aefa4ab3ee37`, on isolated branch `codex/t-026-astra-workflow-audit`. Local and remote `main` still point to that commit; the RC tag peels to it. The exact later tag `v0.1.0-rc.1-Astra` is absent locally/remotely at this checkpoint. No merge or main mutation is authorized by this closeout.

Phase A audit `T026-AUDIT-20261027-01` was accepted as a bounded decision input. Its selected sample covered nine parent tasks and ten delegation bundles (T-018, T-020, T-021, T-023, T-024, T-019, R-009 closeout, T-004, and R-017), with no more than two bundles per parent. The sample was heterogeneous, selected and not population-level. It found repeated hand-authored lifecycle/receipt work and duplicated policy text as the best-supported simplification opportunities. Audit recommendation #1 and #2 were then explicitly selected for Phase B, with #4 limited to governing later validation. The audit remains qualitative: it did not demonstrate causal cost reduction or closed-loop optimization effectiveness.

## Delivered work

**#1 — accepted locally.** Added read-only `handoff.py preview` for the registered task's applicable command and a current `CLI_RESULT.md` scaffold, plus a read-only implementation-review projection. The preview preserves existing lifecycle guards and emits no PASS/verdict/authorization. Historical validation and accepted source hashes are retained locally for GUI review; the public record summarizes the accepted behavior and evidence limits.

**#2 — accepted locally.** Consolidated repeated workflow directions into canonical procedures and short references; removed duplicated diagnostic prompt text by reading the canonical prompt; retained lifecycle, permissions, provenance and CK3 boundaries. The accepted local review record retains the detailed rule/source matrix and bounded regression evidence.

**#4 — limited procedure delivered.** Added a later-real-task observation procedure and use of existing inventory link/boundary/provenance fields. CLI did not own or edit the live optimization inventory. No later independent real-task validation of #1/#2 is proven yet; effectiveness remains unproven.

Both implementation delegations received independent R1 `ACCEPTED` with zero corrections. The scaffold stage's 140 focused tests and policy stage's 157 focused tests are historical receipts, not rerun here. No full suite, CK3 test, install, launcher action, or runtime test is part of this closeout.

The first real use of preview/receipt generation occurred during the selected policy handoff and required no reported ID, revision, path, or grammar repair. This is an initial-use observation within the same workflow intervention, not an independent effectiveness comparison and not a causal cost claim.

## Deferred audit recommendations

See [T026 deferred optimization snapshot](../T026_DEFERRED_OPTIMIZATIONS.md), dated 2026-10-27. #3 priced cost renderer remains unimplemented; #4 later independent validation is unproven; #5 broader compact-receipt formatter is unimplemented; #6 broad risk-test recommendations remain conditional; #7 CK3 Skill is deferred; #8 generic rewrite/framework/daemon/autonomous optimization is rejected. Re-evaluate any future selection using then-current evidence; this snapshot creates no new task, automatic priority or implementation authority.

## Partial finite-cutoff AI cost

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6-astra | 12,737,983 | 12,389,888 | 348,095 | 79,244 | 12,817,227 | $19.83303800 |
| gpt-6-luna | 213,903 | 187,392 | 26,511 | 1,035 | 214,938 | $0.00504252 |
| gpt-6.1-sol | 8,901,718 | 8,418,176 | 483,542 | 42,693 | 8,944,411 | $2.23583160 |
| **Total** | 21,853,604 | 20,995,456 | 858,148 | 122,972 | 21,976,576 | **$22.07391212** |

Partial finite-cutoff known-model API-equivalent estimate, not subscription spending or an invoice. Cutoff: 2026-10-27T20:14:44Z, complete-line source prefixes captured at closeout-preparation pickup. Eight source snapshots supplied 217 deduplicated assigned responses across exact GUI, executor, linked review and independent-review turns. The current GUI session prefix ends at the exact claim boundary; all later turns are excluded. [Aggregate GUI context history](https://github.com/mhaduk/ck3-dynasty-map/blob/codex/t-026-astra-workflow-audit/docs/telemetry/gui-context/T-026.jsonl). Full source sizes, hashes, turn assignments and response-level audit remain in private local accounting evidence; no session paths or raw session data are published. The finite source search found no additional T026-linked session on 2026-10-27, but coverage outside those identified sources is partial and any unavailable counters remain UNKNOWN, not zero. Accounting/publication work after the cutoff is excluded.

Standard short-context rates per million input/cached/output tokens checked 2026-10-27: Astra $10/$1/$50, Sol 6.1 $2/$0.10/$10, Luna $0.10/$0.01/$0.50. No mapped request exceeded 272K input; all recorded cache-write counters were zero. Official sources: [API pricing](https://developers.openai.com/api/docs/pricing), [Astra model page](https://developers.openai.com/api/docs/models/gpt-6-astra), [Sol 6.1 model page](https://developers.openai.com/api/docs/models/gpt-6.1-sol), [Luna model page](https://developers.openai.com/api/docs/models/gpt-6-luna). Reasoning output is a subset of output. No mapped model is unpriced; unknown coverage outside the mapping is not represented by N/A rows or treated as zero.

## Closeout and publication state

The GUI independently accepted the frozen finite-cutoff cost gate before publication. Six prepared Wiki pages were published as commit `2a8694d46626ddd59913057ee4c12d6b6c417139`; the remote `master` ref reads back that commit, whose six changed page blobs match all six prepared preview hashes. Issue #52 body read back byte-for-byte with SHA-256 `8c68f96a54a48e700f934de9dbdff17058d1d30c1aa4a5b61a26806122e570d6`; its canonical per-model table, `$22.07391212` total and cutoff/coverage limits passed `ai-cost-table-format`. Issue #52 is CLOSED / COMPLETED (closed 2026-10-28). The registry was synchronized and verifies T-026/#52.

The inspected Wiki checkout is archived and verified in the private publication handoff; only that checkout was removed. The archive contains the Git metadata and all 28 tracked files and frees approximately 292 KiB net. The next steps are the exact privacy/staged-diff review, scoped commit on `codex/t-026-astra-workflow-audit`, annotated `v0.1.0-rc.1-Astra` on that commit **before** pushing the current branch and exact tag, then remote-ref readback and confirmation that `main` and `v0.1.0-rc.1` remain unchanged. Registry synchronization also read back newly present open issue #55 / F-007 and the completed state of #53; no ID was created or additional issue acted on by this handoff. No GitHub Release, beta/Workshop readiness, or completion of T-014/T-017/T-025 is claimed.
