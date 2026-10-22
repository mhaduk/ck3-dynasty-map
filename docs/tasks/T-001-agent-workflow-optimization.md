# T-001 — Incremental agent workflow optimization

Selected and implementation authorized by the user on 2026-10-22. Status:
COMPLETE — both corrected stages accepted by GUI on 2026-10-22.
Tracking: [T-001 / #23](https://github.com/mhaduk/ck3-dynasty-map/issues/23).
This is tooling/configuration work; F-001
remains paused and no CK3 work is authorized by this task.

## Goal and accepted boundaries

Reduce GUI latency, repeated context reads and total GUI+CLI effort while
preserving the existing GUI coordinator / manually invoked CLI / user-operated
game workflow. Improve it incrementally rather than replacing the framework.

Preserve all game-screen restrictions, launcher ownership, privacy controls,
separate Git/GitHub permissions, mod preflight/runtime gates and architectural
decisions. Never modify vanilla, installed mods, game state or launcher settings
for this tooling task. Preserve unrelated uncommitted project work.

## Accepted implementation

1. Per-delegation directories under `.codex-sync/tasks/<ID>/`, retaining
   `CLI_TASK.md`, `CLI_RESULT.md` and `GUI_REVIEW.md`; `STATUS.json` is the sole
   lifecycle authority. Named pickup/receipt commands use an explicit ID.
2. A small local helper validates IDs/paths, claims work atomically, controls
   lifecycle transitions, checks result identity/attempt/input provenance and
   lists tasks. Concurrent pickup of one ID must have one owner. Preserve
   interrupted/failed attempts and reject stale results. No daemon/server.
3. Parallel tasks own separate outputs. Shared source/docs integration has
   one writer; overlapping installations and one live test session remain
   sequential. Fingerprint actual dirty-tree inputs, not only Git HEAD.
4. Route bounded conceptual research and log analysis to CLI. Retain project
   profiles: Luna/Low for trivial mechanical work, Luna/Medium for routine
   bounded work, Sol/Medium for conceptual analysis/review and Sol/High for
   difficult CK3 reasoning. Never claim an unverified model switch.
5. Shorten operational context and remove duplicated procedure text while
   retaining recoverable historical findings and all material restrictions.
   CLI reads only assigned context; GUI reviews decisive evidence rather than
   repeating the investigation. Full task history is read when needed.
6. Standardize baseline/snapshot/log-delta analysis in a small helper. Detect
   truncation/rotation, incomplete marker chains and missing baselines; retain
   repeated new errors and private evidence. A CLI checkpoint finishes without
   waiting for user actions. Logs alone never prove visual acceptance.
7. Add a short direction check before expensive work: requirement, mechanism,
   decisive evidence, blocking unknown, cheapest test and stop/reopen condition.
8. Extend self-healing to GUI and time/token waste. Consolidate evidence-based
   lessons through one owner; avoid adding another rule for every isolated
   error. Recurrence despite an existing rule calls for execution/tool changes.

## Stages and acceptance

- **T-001-T1 — handoff foundations and instructions.** Luna / Medium. Implement
  the per-ID helper, lifecycle checks, meaningful concurrency/recovery tests,
  concise instruction changes and operational-context maintenance. Preserve
  access to earlier checkpoints before removing repeated state text.
- **T-001-T2 — bounded log analysis helper.** Luna / Medium for implementation;
  Luna / Low for routine use. Prepare after T1 review, using frozen local or
  synthetic evidence; no new game run. Test append, repeated errors, missing
  markers, incomplete pairs, rotation/truncation and missing baseline.
- **GUI review/integration.** Check actual changes and evidence, record limits,
  and consume each result. A completed child does not close T-001. Both stages
  and their reviews are required before the parent is complete.

Measure the next 3–5 delegations for GUI dispatch/review time, repeated reads,
context size, rework and avoidable game launches. Token/cost figures are
reported only when available; otherwise record unavailable, not an estimate
presented as measured usage. This observation window is not an automatic
background monitor.

## Foundation implementation and review

GUI review of T-001-T1 on 2026-10-22 reproduced four defects despite seven
passing tests: assigned edits blocked completion, scope drift could finish,
retry could overwrite newer status, and an attempt-directory symlink escaped
the root. The first implementation was not accepted; its evidence is retained.

T-001-T1-FIX delivered these corrections, accepted by GUI on 2026-10-22:

- Explicit `--owned` paths distinguish editable inputs/outputs from immutable
  `--input` dependencies. Initial dirty bytes/hashes remain in `baseline/` and
  `inputs`; completed results record final `outputs` hashes. Claim checks every
  initial input; completion permits assigned edits and checks immutable inputs.
- Claim, validation, retry and completion enforce frozen scope. Every mutating
  transition serializes checks, evidence changes and status writes per ID.
  Retry/receipt journals support explicit idempotent recovery after interruption.
- Administrative paths and hidden parents reject symlinks. Named pickup needs
  no legacy inbox; bare pickup and receipt each require a sole eligible result
  across the controlled legacy/new formats. Result check lines use one exact
  grammar, exercised through the real helper and an assigned-edit lifecycle.
- Regressions retain prior meaningful checks and cover deterministic stale
  revision ordering, independent IDs, interrupted archive/receipt phases and
  path escapes. Detailed results and incremental baseline/diff stay private in
  the correction evidence directory; these checks are self-review.

The helper coordinates cooperating writers. Hashes cannot attribute changes
inside an owned file, and it is not an OS sandbox or a power-loss recovery
system. A retry requires unchanged scope and all initial inputs, including
owned paths; changed inputs need a new delegation rather than silent rebase.

GUI reran all 22 tests successfully and verified returned initial/final hashes
against preserved baseline and actual files. The legacy task/result and GUI
acceptance receipt are archived privately. This accepts the foundation, not
the parent. New work uses the named interface.

## T-001-T2 — bounded log checkpoint helper

Delivered `scripts/ck3_log_delta.py`, synthetic tests and a concise workflow
example. The helper records an explicit per-log baseline, freezes each file's
end size for one capture, writes private delta bytes and a short report, and
counts repeated new error messages. Literal marker expectations and ordered
begin/end/reject chains are supported without assuming CK3 APIs. Required gaps
make the interval incomplete; optional missing logs remain explicit and produce
an optional-gap interval status. Appends after the frozen boundary are left for the next
run. The helper refuses symlinks, overwrites and source/output overlap.

Limits: baseline fingerprints sample the first and last 256 bytes; arbitrary
same-size rewrites outside those samples may be missed. Per-log captures are
not an atomic multi-file snapshot. Markers show observed text, not event
identity; `WRITE_RETURNED` does not prove stored RGB, classification or visual
acceptance. All automated coverage and the representative command flow use
disposable synthetic logs. No live CK3 logs, new game run, installation,
launcher operation or process check was used.

GUI reran all 33 tests successfully on 2026-10-22, then reproduced three
uncovered cases with the real script: a new error.log entry without English
severity words was missed; a baseline inside a line produced an unflagged
continuation; END before BEGIN on one line was counted as a valid pair. The
generic PASS label also needed to distinguish interval completeness from error
observations. That first T2 result was reviewed/consumed with CHANGES REQUIRED.

T-001-T2-FIX delivered the bounded correction, accepted by GUI. Error-channel
observations count nonempty complete error.log lines regardless of severity
keywords; other-log detection is explicitly heuristic. Message identities use
full normalized hashes with bounded snippets/counts. The baseline records line
boundaries, and partial initial/final fragments remain preserved but unparsed.
All chain occurrences follow text position order; overlapping literal spans
are refused explicitly. Reports separate interval completeness, error/rejection
observations and marker/chain expectations; exit success is not CK3 acceptance.
The full tooling suite passes 37 tests (15 log-helper and 22 handoff), including
new error-channel, initial-fragment and same-line order regressions. Actual-script
synthetic examples cover complete, error-observed and incomplete intervals with
source/baseline preservation. Receipt semantics now explicitly distinguish GUI
review from acceptance; the handoff helper and lifecycle remain unchanged.

## Final disposition — 2026-10-22

GUI accepted T-001-T2-FIX after rerunning all 37 tooling tests successfully
(15 log checkpoint and 22 handoff tests), checking actual code/provenance and
four representative real-script synthetic flows. The accepted result was
consumed before these final parent tracking edits. Prior rejected candidates,
their review findings and accepted output snapshots remain preserved locally.
T1 and T2 are complete; no required implementation or review remains.

The existing workflow skeleton is retained. Per-ID pickup/receipt, atomic
ownership and revision checks, explicit dirty-input/output provenance and one
shared-file integrator enable scoped parallel work. Short operational context,
CLI routing/model profiles, a direction check and material-stage self-healing
reduce repeated discovery. The log helper provides finite private byte
intervals and separates completeness, observations and expectations.

Validation is offline and synthetic; it establishes no new CK3 behavior. No
game/launcher/process, live-log/save, mod/installation or vanilla operation
occurred during implementation and validation. Publication was authorized
separately on 2026-10-22: a scoped T-001 commit/push and tracking Issue #23.
The issue records the verified publication receipt. Unrelated dirty work
remains preserved. F-001 remains paused with no new task
or runtime stage selected. No product/ADR semantics changed.

Actual token, cost and latency improvements are unmeasured. Observe ordinary
future delegations using the existing small measurement criteria; this is not
a background monitor or a remaining implementation gate. Keep boundary-sampling,
heuristic detection, literal-marker and cooperative-worker limits explicit.

Self-healing review: recovered CLI command/output/test issues and both rounds
of GUI-detected defects are retained in local results/reviews. Final GUI review
recovered one oversized read through a narrow follow-up. The resulting durable
improvements are specific editing/concurrency/path and log-semantic regressions;
no extra generic instruction was added for errors already covered by the rules.
