# T-009 — Structured preflight evidence

Status: **CLOSED — GUI accepted the corrected implementation and the completed record was published with issue #35 on 2026-10-23.**
`T009-FIX-20261023-02` is accepted/consumed; initial EXECUTE remains consumed
CHANGES REQUIRED, with original evidence preserved. The user authorized scoped publication and closure in the 2026-10-23 batch handoff. No CK3 runtime or
installation work was performed. Predecessor: [T-008](T-008-workflow-optimization.md).

## Original problem and selected direction

T-008 provides a bounded inventory with selected upstream statuses, but its
initial adapters could not consume the preflight checker's result as
structured evidence. Before T-009, `scripts/check_mod_preflight.py` printed
human-readable success/failure and returned 0/1 without versioned JSON.
Operators had to preserve and interpret that prose separately. This is a concrete format
gap, not a measured cost or savings claim.

The accepted T-008 research ranked structured preflight as a small, lower-risk
candidate only when it helps the report. That condition now applies. Select
one additive JSON result contract and one matching T-008 adapter, rather than
starting full cross-stage semantic validation, log profiles or deployment.

## Proposed bounded scope

- Add an explicit JSON mode to the existing checker; keep default text output,
  existing checks and current success/failure exit meanings compatible. Build
  text and JSON from the same findings, never by parsing stdout.
- Freeze a versioned schema before EXECUTE: offline-file-check status, exit
  code, source/optional comparison coverage, finite finding codes and counts,
  expected-version check, and explicit syntax/API/runtime-unverified limits.
  Missing, unreadable or incomplete inputs must stay distinct from a complete
  clean file check. Exact operational-error handling needs a GUI decision
  after the bounded compatibility inventory, without silently changing exits.
- Extend `scripts/evidence_report.py` with one allowlisted adapter for that
  schema. Project only bounded typed status/coverage/count fields; retain
  upstream findings and uncertainty without converting inventory COMPLETE
  into preflight acceptance. Do not export raw diagnostics, absolute paths,
  payload names or source text. Existing manifest/report behavior stays intact.
- Use synthetic temporary payloads and installed-tree copies only. No live
  package installation, real CK3 scans, launcher/game/process action or
  modification of vanilla files. Reuse the existing checker implementation.

## Acceptance cases for the future frozen handoff

1. Current default text and 0/1 success/failure behavior remain compatible for
   representative valid, invalid and comparison cases.
2. Text and JSON agree on the same findings; repeated JSON output is stable.
   File checks never claim CK3 syntax, API, runtime, stored RGB or user acceptance.
3. Missing descriptor, malformed encoding, version mismatch, unreadable input,
   missing/extra/different comparison files and unsupported schema retain
   distinct observable findings/coverage; no synthesized success.
4. Complete inventory can contain failed/incomplete preflight. Pin mismatch,
   unknown schema and missing required fields prevent trusted links/projection
   just as for existing T-008 adapters; no verdict precedence or repair.
5. Privacy sentinels never appear in projected output. Public tests run without
   ignored local artifacts; existing checker/report callers and relevant
   regression suites pass. Inputs remain unchanged.

## Preparation, routing and stop conditions

GUI owns schema, compatibility decisions and final acceptance. The current
checker was inspected in a bounded GUI review; its existing checks, messages
and exits are explicit. GUI froze coverage/status/version/comparison meanings
in the local handoff specification, so compatibility verification and approved
implementation can proceed in one EXECUTE without another research cycle.
CLI first records representative legacy behavior, then implements and tests
the additive mode/adapter. New PASS/FAIL/INCOMPLETE statuses never change the
legacy 0/1 success/failure meaning. Test only synthetic files.

The task has exact inputs/owned outputs, a required compatibility matrix,
privacy and portability cases, end-to-end checker-to-inventory tests and
existing regression gates. A GUI-supplied execution plan controls progress.
Recommend Luna / Medium; selection is not runtime confirmation. Any material
conflict with the frozen compatibility/schema returns to GUI. Implementation
receipt does not complete the parent; independent GUI review/accounting follow.

Keep changes limited to checker, report adapter, relevant tests and guides.
Read MOD_AUTHORING_RULES before any future payload preparation. Preserve
existing preflight semantics; if additive structured reporting cannot do so,
stop for a GUI decision rather than expanding scope. No migrations, auto-pins,
repairs, lifecycle/schema changes in handoff.py, AI ledger, deployment/rollback,
publication or GitHub writes. F-001 remains paused.

## Planning provenance and limits

Basis: T-008's seven-candidate comparison and accepted report contracts; a
bounded inspection of the current checker's output branch confirms the format
gap. No new broad research or implementation was needed for this short GUI
planning edit. Earlier oversized context output was recovered with targeted
sections; use exact symbols/line ranges for subsequent preparation. Frequency,
maintenance cost and actual savings remain unmeasured. Other candidates stay
deferred; T-009 completion and accounting are not claimed.

## Current prioritization and acceptance — 2026-10-23

Near-term selection is a qualitative GUI judgment: the existing report can
consume handoff/log/classification results but not preflight prose. Structured
preflight fills a known gap with smaller scope/revalidation cost than full
semantic chain validation or log profiles; deployment is a separate higher-risk
permission class. The wider candidates may have larger eventual savings, but
current evidence does not measure or establish that ranking.

The frozen stage includes shared structured findings, opt-in JSON, strict
allowlisted adapter, exact legacy CLI comparison, success/failure/incomplete
coverage cases, malformed/unknown/pin mismatch and privacy checks, public-only
portability and existing regressions. No live game/application state or user
game action is needed. CLI returns code, tests, guide and a concise evidence
dossier; GUI reviews decisive cases and the diff. No new issue is created.

## CLI implementation result — 2026-10-23

Status: **implementation complete; GUI acceptance and saved-session cost
accounting pending**. The checker now has shared typed findings for the
unchanged default text renderer and opt-in `--json` schema
`mod-preflight-result/1`. Read/traversal gaps and symlinks produce
`INCOMPLETE`; complete policy violations remain `FAIL`. Comparison retains
observed differences with `UNVERIFIED` when either requested tree is
incomplete. `inspect(root, label, expected_version, errors)` remains available.

The report accepts exactly one additive `mod-preflight` kind. It pins the
result before projecting bounded typed scalars and allowlisted finding codes.
It does not invoke the checker, copy `limits` or arbitrary text, expose paths,
or promote inventory completeness to a preflight verdict. Existing manifest
and adapter behavior remains covered by the existing inventory suite.

Evidence and checks:

- Original checker bytes are preserved at the task-local compatibility
  artifact; SHA-256 is
  `5fd6c9d8bfb82a8f504567bd3cf312e51e253ca6dc60a7576295449f59563c1d`.
- Before/after CLI parity was byte-identical for exit/stdout/stderr on four
  synthetic cases: pass, missing BOM, source plus installed mismatch, and
  matching installed payload. Captures are private task-local artifacts.
- `python3 -m unittest tests.test_mod_preflight tests.test_evidence_report
  tests.test_handoff tests.test_ck3_log_delta
  tests.test_dynmap_classification`: **118 passed**. This includes all 22
  existing inventory assertions and new producer/adapter integration cases.
- A disposable public-only copy containing only the two focused scripts/tests
  and `tests/__init__.py` passed **34 tests**, without handoff artifacts.
- The documented example smoke returned inventory `COMPLETE`; `git diff
  --check` passed for the owned source, test and guide paths.
- Tests use synthetic files only. No install, launcher/game interaction,
  network, Git staging, commit, push or publication occurred.

The accepted scope and data model were respected. No material schema or
permission conflict remains unresolved. CLI self-review is not GUI acceptance;
GUI should inspect checker legacy parity, producer privacy, malformed/pinned
adapter cases and its diff, then complete independent saved-session cost
accounting. Model recommendation remains Luna / Medium; runtime selection was
not confirmed.

## Initial GUI review — changes required, 2026-10-23

GUI reran all 34 focused tests successfully and independently reproduced two
contract defects. In an ordinary tree with a symlink and no descriptor, the
default output loses the historical missing-descriptor finding and changes
the summary count. A pinned structured finding with a list-valued scope raises
an unhandled TypeError instead of yielding a finite adapter issue. Code enum
membership has the same unchecked-type pattern. Original outputs and receipt
are preserved; initial EXECUTE is consumed CHANGES REQUIRED.

A separate bounded correction `T009-FIX-20261023-02` must retain legacy
diagnostics while preserving new incomplete coverage semantics, guard finding
field types before enum membership, and extend negative compatibility/CLI
tests. Public tests passing alone do not prove the contract. Parent remains
OPEN; saved-session accounting and independent acceptance are pending. No
installation, runtime, Git or external publication authority is added.

Recovery instruction: test combined incomplete/known-defect cases against the
preserved original checker, and validate scalar types before set membership.

## CLI correction result — 2026-10-23

Correction implementation and checks are complete; GUI review and independent
saved-session accounting remain pending. The default checker again emits the
historical missing-descriptor diagnostic when an incomplete inventory cannot
establish descriptor availability. JSON uses finite `descriptor_unavailable`
while retaining `INCOMPLETE`; invalid roots retain their original early
diagnostic without an invented descriptor finding. The compatibility
`inspect(...)` wrapper also retains the prior error-list shape. The adapter
checks exact string types for `scope` and `code` before enum membership, so
malformed JSON produces finite `unsupported_finding` issues and cannot leak raw
values or resolve dependent links.

- Byte-pinned original checker: `.codex-sync/T009-FIX-20261023-02/original-checker.py`, SHA-256 `5fd6c9d8bfb82a8f504567bd3cf312e51e253ca6dc60a7576295449f59563c1d`. Frozen GUI specification and findings remain at their original input hashes in task status.
- Exact default stdout/stderr/exit parity with the baseline was rechecked for valid input, missing BOM, installed extra-file comparison, and the combined dangling-symlink plus absent-descriptor case. Private byte captures and hashes are in `.codex-sync/T009-FIX-20261023-02/artifacts/legacy-parity.json`.
- Deterministic read-denial mocks assert historical CLI and `inspect(...)` messages for an unreadable descriptor; invalid-root tests assert the early-return diagnostic. JSON coverage remains `INCOMPLETE` and excludes raw paths/errors.
- Malformed finding tests cover list, dict, null, bool and integer `scope`/`code` values. End-to-end report CLI tests cover required and optional malformed findings with dependent links (`UNKNOWN`, report written, exit 2, `INCOMPLETE`), plus the optional-gap policy without a link (`COMPLETE_WITH_OPTIONAL_GAPS`, exit 0). Boolean, float, negative and overflow counts remain rejected.
- Focused producer/adapter suite: **39 passed**, also in a disposable public-only tree. Final targeted regression suite: **123 passed** across preflight, report, handoff, log-delta and classification tests. `git diff --check` passed. All fixtures were synthetic; no installation, app/game action, network, Git staging or publication occurred.
- The first public-only copy attempt named a nonexistent `tests/__init__.py`; after checking `rg --files tests`, the retry copied only present files and passed all 39 tests. The first capture write found no `artifacts/` directory; exact-path inspection and creation of that allowed task-local directory let the parity capture complete. One milestone update used a stale revision after a successful progress write; persisted status supplied the next revision. A handoff `list` call with an unsupported positional ID and two patch attempts with stale context were corrected by consulting command help/current source before retrying.
- Initial completion checks identified that `CLI_RESULT.md` belongs under `.codex-sync/tasks/<ID>/`, requires fenced provenance, all required sections, exact success/check lines, and all planned milestones. The report was moved to the canonical handoff path, its provenance and exact lines were added, and the final milestone remains to be recorded before completion.

Self-review finds no remaining correction-scope conflict. This receipt does not
accept or complete parent T-009; GUI review must inspect the compatibility
artifact, malformed CLI cases, scoped diff, and saved-session accounting.

## Final GUI acceptance — 2026-10-23

The corrected checker and inventory adapter are accepted locally. The checker
now offers optional `--json` using `mod-preflight-result/1`; default text and
0/1 success/failure exits remain compatible for the checked representative
and combined negative cases. Shared findings retain independent coverage,
version/comparison and PASS/FAIL/INCOMPLETE meanings. The `mod-preflight`
inventory adapter projects bounded typed evidence without running the checker.
Complete inventory can contain failed/incomplete preflight; offline file PASS
never establishes CK3 syntax/API/runtime acceptance.

GUI inspected the exact fixes and independently reran 39 focused tests, plus
the same 39 tests in a public-only isolated tree. The original symlink plus
missing-descriptor reproduction now matches original stdout/stderr/exit
byte-for-byte, while JSON remains INCOMPLETE. List/dict/null/bool/integer
findings are controlled unsupported issues, with no exception. CLI evidence
records four parity captures, a guide smoke and 123 targeted regression tests
passing. No live package/game tests or measured savings follow.

Original EXECUTE remains CHANGES REQUIRED; accepted outputs and original
receipts are preserved privately. Earlier revision/path/patch-anchor/artifact
and test-package assumptions were recovered as recorded in the correction
dossier. GUI bounded oversized displays to exact sections. Reusable lesson:
combine known defects with incomplete coverage in compatibility tests, verify
scalar types before set membership, and discover exact artifact/test paths
before writes. No global workflow change was introduced.

## Saved-session cost verification

GUI checked one saved GUI session with three selected T-009 turns and both
CLI sessions. Runtime records confirm Sol in GUI and Luna in CLI. The existing
accounting helper and an independent response-ID sum agree: 212 responses,
21,427,689 tokens. Private frozen source copies, hashes and exact assignments
remain local. Six same-day automatic-review sources were checked by exact
parent/root-turn link; none matched selected turns. Coverage stays partial.
The preliminary T-009 plan was part of a mixed T-008 commit turn and remains
unallocated; no entire mixed-session total was assigned. Later accounting,
integration and the final message are excluded by the finite cutoff below.

Same-day officially verified Standard short-context token reference rates give
about **$0.83 API-equivalent** for measured usage: Sol $0.5725512 and Luna
$0.2543031, sum $0.8268543 before rounding. Maximum recorded request input is
229,568 tokens; recorded cache-write input is zero. This is not subscription
spending; actual tier, regional processing, tool charges and unobserved usage
are not established. No missing component is asserted to have cost zero.
[Official pricing](https://developers.openai.com/api/docs/pricing?latest-pricing-expanded=true),
verified on 2026-10-23 and reused from the same-day evidence, gives per-million
uncached/cached/output rates of $2/$0.10/$10 for GPT-6.1 Sol and
$0.10/$0.01/$0.50 for GPT-6 Luna. The accounting cutoff is not extended to count
its own documentation.

## Local commit and successor selection — 2026-10-23 (historical checkpoint)

The accepted T-009 implementation, records and short successor plan are
user-authorized for a local commit only; no push or external publication.
The saved-session accounting cutoff above remains frozen and excludes this
later commit/planning work.

[T-010](T-010-checkpoint-comparison.md) is the next planned area: compare two
explicit finite saved checkpoint reports, distinguishing byte intervals,
message identity, counts and unproven causality. This follows the earlier
analysis after the report/preflight foundations. Exact comparability and
privacy rules require bounded contract review before any separate EXECUTE;
no raw-log parsing, capture or implementation starts here.

<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| gpt-6-luna | 17954686 | 17651200 | 303486 | 94885 | 33283 | 18049571 | partial |
| gpt-6.1-sol | 3359797 | 3331712 | 28085 | 18321 | 4593 | 3378118 | partial |
| **Total** | 21314483 | 20982912 | 331571 | 113206 | 37876 | 21427689 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-23T18:16:57.841333+00:00. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
Partial measured coverage: one GUI session (three selected T-009 turns) and two CLI sessions; 212 deduplicated own responses. Independent sum agrees. Preliminary T-009 plan in mixed T-008 commit turn remains unallocated; later accounting/integration/final response excluded. Six same-day review sources checked; no exact selected parent/root-turn match. Unobserved usage is not zero.
<!-- ai-cost:end -->


## Publication and closure — 2026-10-23

Published completed record: [issue #35](https://github.com/mhaduk/ck3-dynasty-map/issues/35), closed after validation of the approved batch gates. The accepted implementation remains subject to its documented limits: structured preflight evidence does not establish CK3 syntax, API or runtime compatibility. Frozen measured usage is 21,427,689 tokens and $0.8268543 API-equivalent, partial coverage; later shared closeout work is excluded. See the [Wiki AI-cost table](https://github.com/mhaduk/ck3-dynasty-map/wiki).
