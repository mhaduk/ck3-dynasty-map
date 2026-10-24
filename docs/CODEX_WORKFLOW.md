# Codex Workflow

This document is the detailed operating procedure. Keep [AGENTS.md](../AGENTS.md) short. The repository and all GitHub content are public; local machine state is not project documentation.

## Session startup and task scope

### CLI handoff pickup precedence

`pobierz zadanie [ID]` selects a READY handoff, before consulting operational
state/history. Read `AGENTS.md`, then use `resolve [ID]`. A named ID inspects
`.codex-sync/tasks/<ID>/CLI_TASK.md` and `STATUS.json` first; it does not require
or read the legacy inbox when that task exists. Only when the named directory
is absent may the resolver match that exact ID in the controlled legacy inbox.
An existing ineligible or inconsistent named task must not fall through.

Bare pickup uses `resolve` across READY per-ID and active legacy candidates;
exactly one is required, including when both formats coexist. Zero or multiple
candidates require a discrepancy report, never a guess or a product-task
fallback. Read only the resolved handoff's referenced context, validate its
contract, then claim/mark it IN_PROGRESS. Its ID and parent override stale
state/history entries. Receipt resolution is separate: `resolve [ID] --receipt`
selects COMPLETED results for `gotowe [ID]`, with the same uniqueness rule for
a bare receipt. READY tasks are not pending receipt candidates.

For ordinary GUI startup, read the state and history as below, but the latest
explicit user selection in the conversation takes precedence over stale
operational text. Before dispatching a handoff, GUI should synchronize the
selected task in `CURRENT_STATE.md`; the handoff remains an additional explicit
source of task identity for CLI pickup.

1. Read `AGENTS.md`, `docs/CURRENT_STATE.md`, then `docs/TASK_HISTORY.md`; identify the stable task ID and read only relevant task sections/evidence.
2. Reuse reviewed findings while their input fingerprints, build and evidence remain current. Invalidate only the affected conclusions when one changes. Do not reread full history/workflow on every receipt.
3. Check Git status before editing and preserve unrelated changes. Keep one substantial backlog task in a chat.
4. For CK3 research, start at [CK3_SOURCE_MAP.md](CK3_SOURCE_MAP.md), then inspect only recommended target-build sources. Repeat research only for changed build, conflicting evidence or requested revalidation.

### File and command preflight

Before opening/reading a file, check that the exact path exists and is
readable; before listing a directory, check that it exists and is a directory.
Before writing, verify the intended parent directory exists and the target is
the expected file. For required inputs, report a missing/unreadable path and
stop the dependent step; for optional references, skip them and record that
they were unavailable. Never use an assumed wildcard such as `docs/ADR-010*`
as a file path. Discover names with `rg --files` or check an exact path first;
ADR records live in `docs/DECISIONS.md`. Establish the repository root before
using relative paths. Include hidden directories in exact references, such as
`.codex-sync/CLI_TASK.md`; use `List` for a directory and `Read` for a file,
not `List` on a filename. Do not chain reads of unchecked paths with `&&`,
since one missing path can abort the whole batch. For searches, quote both the
pattern and path. Prefer `rg -n -F` with exact identifiers before regular
expressions; if using a regex, check quoting and syntax. Treat `rg` exit 1 as
“no matches” and exit 2 as a command, regex, or path error: inspect stderr,
correct the smallest failing operation, and do not proceed as though it was a
successful search. Avoid putting expected no-match searches inside an `&&`
chain. A preflight check is a guard against predictable failures, not a
substitute for reporting genuine unexpected tool errors.

## Model choice

GUI / Sol is the orchestrator and decision maker: it owns the problem, scope,
acceptance criteria, architecture, material alternatives and trade-offs,
direction, final acceptance and next step. CLI / Luna is the default worker for
bounded evidence collection, verification, research, comparison, analysis and
execution of an approved plan. Recommend Luna / Medium for ordinary bounded
work and Luna / Low for trivial mechanical work. Difficulty calls for more
bounded evidence, a recommendation or escalation to GUI; it does not trigger an
automatic architecture choice or model upgrade. GUI may explicitly select a
stronger worker or reviewer when warranted. Profiles are recommendations unless
the runtime confirms the selected model. When supported by the installed CLI,
an individual session may be started with `--model gpt-6-luna -c
model_reasoning_effort='"medium"'`; this is an optional invocation example,
not a shared default or a claim that every account/session can select it. Do
not claim measured cost or quality savings from this routing.

## Required GUI/CLI routing decision

Before substantial source edits, documentation maintenance or investigation,
choose where the work belongs. Reassess when uncertain research becomes a
bounded implementation/preparation task; the preceding GUI work is not a
reason to keep all subsequent work there.

| Work | Default route |
|---|---|
| User coordination, scope/architecture decisions, material alternatives/trade-offs, direction and unresolved decisions | GUI / Sol |
| COLLECT, VERIFY, RESEARCH and approved EXECUTE work within frozen scope | CLI / Luna / Medium by default; Luna / Low for trivial mechanical work |
| Difficult bounded reasoning or conflicting evidence | CLI gathers and presents bounded evidence/recommendations; GUI decides whether to direct further work or explicitly choose a stronger worker/reviewer |
| Documentation, consistency and mechanical edits | CLI / Luna / Medium; Luna / Low when trivial |
| Independent review | GUI / Sol owns acceptance; it may explicitly choose a separate reviewer/session when useful |
| Inspecting a CLI result and integrating its conclusions | GUI |
| All CK3 game UI interaction, including start/exit, loading, saving, observation and tests | User only; no Codex game-window inspection or control |
| Verify installed payload and persisted enabled-mod/playset configuration | CLI, read-only file evidence first; no routine launcher UI inspection |
| Correct an incorrect or unresolved launcher/playset configuration | Codex GUI, already open launcher only; reuse the test playset |
| A small direct edit where the handoff would cost more than the edit, such as a short workflow clarification | GUI allowed |

Before expensive or uncertain work, briefly state: user requirement, mechanism, decisive evidence, blocking unknown, cheapest test and stop/reopen condition. GUI should reach a decision or dispatch a bounded handoff after brief reconnaissance; this is a direction, not a hard timeout. Keep small edits in GUI when handoff overhead exceeds the work.

For bounded, separable work, CLI is the default action, not an optional
suggestion after the GUI has already completed it. Prepare `CLI_TASK.md` and
give the user the launch instruction. Do not duplicate its assigned work while
waiting. Before retaining substantial CLI-suitable work in GUI, state one
concrete reason, such as an explicit user request for direct execution or
edits that cannot safely be separated. Convenience or already having read the
files is not sufficient. Do not delegate tiny edits merely to satisfy a quota.

Example: GUI resolves the R-005 research question enough to specify a probe;
CLI then prepares the isolated payload and documentation in one task; GUI
reviews the actual result. Source preparation, self-review and documentation
belong to that authorized preparation stage. A self-review must not be called
independent review.

## Delegation classes, evidence and escalation

For difficult unresolved problems, GUI may opt into an independent diagnostic
review when evidence leaves competing hypotheses, cross-layer contradictions,
weakly documented behavior, a costly next experiment, repeated rediscovery, or
a material assumption challenge. A simple reproducible defect, one likely
decisive check, mechanical work, missing decisive user evidence, or token count
alone is not a trigger. GUI / Coordinator remains the decision and acceptance
authority; any external reviewer is read-only and advisory. Use the bounded
manual packet workflow, immutable-input rules and privacy limits in
[Diagnostic Review](DIAGNOSTIC_REVIEW.md). Do not claim savings or treat
unavailable external usage as zero. Match the output directory name to the
manifest review ID; optional evidence may be unavailable only when it is
genuinely absent. Treat symlinks and malformed identity data as errors.

Every new `CLI_TASK.md` names one primary delegation type: `COLLECT` (gather
facts/evidence), `VERIFY` (check a stated claim or contract), `RESEARCH` (bound
analysis of a question and alternatives), or `EXECUTE` (carry out an approved,
bounded plan). Secondary activities may be stated in prose. `DECIDE` is
reserved for GUI and is never a CLI delegation type. Each task states
`Decision authority: GUI`; these are semantic instructions, not a new enforced
STATUS schema.

CLI may interpret evidence and recommend options with reasons, benefits, risks
and scope impact. It should complete useful safe work within the delegation
before escalating minor uncertainty: gather another bounded source, test
hypotheses, compare options or state uncertainty where authorized. Escalate
architecture, scope, direction, material trade-offs, consequential evidence
conflicts, work outside the contract, or decisions not safely derived from it.
Continue independent authorized work while an unrelated question is pending;
never cross permission, ownership or decision boundaries.

Return a compact, decision-oriented dossier inside `## Result` in the existing
`CLI_RESULT.md`: `### QUESTION / SCOPE`, `### FINDINGS`, `### EVIDENCE`,
`### OPTIONS` (when applicable), `### RECOMMENDATION` (optional),
`### UNRESOLVED / UNKNOWN`, and `### DECISION REQUIRED`. Map critical claims to
precise paths/lines and snapshot hashes, test invocations/results, or receipt,
checkpoint and commit IDs as applicable. Mark claims as observed, inferred or
recommended; distinguish historical evidence from fresh checks, preserve
upstream completeness/verdicts, and say UNKNOWN when evidence does not decide.
Do not include private chain-of-thought or raw dumps. GUI reviews the dossier,
opens selected decisive evidence, and inspects the actual scoped diff/checks;
it does not repeat the full context by default. Widen review only for mismatch,
missing provenance, changed inputs or material risk. CLI self-review is not
independent review; a recommendation is not acceptance.

## Roles, prerequisites and CK3 test cycle

- CLI executes ready, bounded code/file/install/log tasks and returns results.
  It assumes the declared game/launcher state is correct because the user
  prepares it before invoking CLI. Do not verify it with ps/pgrep, process
  enumeration, Activity Monitor, app inventories, UI access or another method.
  Do not request escalation/confirmation for a process check, wait for user
  actions, or mark FAILED because app state was not independently verified.
  CLI reports actual code/file/tool failures, not a manufactured state gate.
- Codex GUI coordinates the work, prepares handoffs, reviews actual changes,
  reviews CLI installation/configuration receipts and logs. It configures the
  already open CK3 launcher/playset only for a documented mismatch or unresolved
  configuration that cannot be settled from file evidence. It gives the user concise in-game test instructions and
  analyzes logs afterward. It may perform mod file operations or delegate them
  to CLI according to the routing rules.
- The user opens/restarts launcher and game through Steam and performs every
  interaction inside CK3: loading, saving, menus/options, character changes,
  observer setup, diagnostic clicks, interface testing and normal game exit.

Codex must not bind to, inspect, screenshot, activate, click, control, launch
or close the CK3 game window, even when automation is technically available.
A failed in-game automation call is not a reason to try another method. Do not
spend tokens exploring the game UI. Analyze logs and user-reported observations;
distinguish those evidence sources. When a visual comparison is needed, ask the
user for an observation or screenshot. The user captures it; Codex may inspect
only images supplied by the user. Never capture/read the running game screen,
use game-screen OCR or pixel sampling, or try alternative vision/UI methods to
compare it autonomously. Do not spend time/tokens probing graphical access.
This applies to every delegated agent as well as GUI coordination. Launcher
configuration is separate and grants no access to the CK3 game screen.
Do not launch/relaunch the launcher either; configure it only after the user
has opened the CK3-specific launcher through Steam. Do not click PLAY/RESUME.
If useful, the parent GUI may check prerequisites before dispatch using a
bounded read-only process check or launcher observation, never the game UI.
The user's declared state is sufficient; do not repeat a check in CLI. Do not
turn process inspection into a required gate. Preserve saves and never modify
vanilla. This rule supersedes older handoffs requiring CLI process checks.

Reuse the existing test playset. A new probe/revision or separate mod payload
does not require another playset: isolation means only intended mods are enabled
for the run. Preserve prior selection locally and restore it after the user
exits the game. Create another playset only for a concrete need to preserve
parallel configurations or an explicit user request.

### File-first installation and activation verification

CLI verifies installation without routinely opening or inspecting the launcher:

1. Before replacement preserve the payload, external wrapper, bounded prior
   logs and enabled-mod/playset configuration in private local evidence. Run
   source preflight, then installed inventory/byte/hash equality preflight.
   Compare external wrapper name, version, supported_version and resolved path
   separately; matching metadata alone is not an installed-file check.
2. Read `dlc_load.json` and compare its `enabled_mods` with the exact intended
   set, including preserved prior selections. Resolve each enabled wrapper and
   payload; detect missing/duplicate/conflicting entries and unintended active
   probes. Do not silently disable an unrelated mod. Keep disabled-DLC state.
3. If the manifest is missing, malformed, ambiguous, inconsistent with expected
   selection, or has concrete evidence of staleness, use bounded read-only
   launcher configuration/playset data (such as its SQLite database) as needed.
   Use read-only access and handle locks or unavailable schema as evidence gaps;
   do not modify launcher databases/manifests or infer current playset identity
   from the mod list alone. No routine process or UI check is introduced.
4. Return exact file checks and persisted selection verdict separately, with
   private hashes/source provenance and explicit unknowns. Coherent sufficient
   file evidence means GUI reviews the receipt; it does not repeat the check
   visually or ask the user to open the launcher solely for verification.
5. GUI uses the already open launcher only to correct a proven configuration
   mismatch or resolve a material ambiguity that file checks cannot settle.
   If needed the user opens it through Steam. Preserve the existing playset
   and selections; after UI changes re-read persisted configuration. The user
   alone starts the game. Fresh bounded startup logs remain the authority for
   the mod/build actually mounted; a manifest is configuration evidence, not
   runtime proof. A previously passed selection check may be reused until its
   inputs or intended set change.

These checks add no game/process/UI permission or direct launcher-file editing
permission. They apply to installation, restoration and subsequent revisions;
only unresolved or changed evidence warrants broader checking. Token savings
are an intended reduction of duplicate GUI work, not measured savings.

### Identify the already running launcher on macOS

This is GUI-only troubleshooting when launcher binding is ambiguous or times
out, never a CLI prerequisite or a check of the user's declared game state.
Multiple installed launcher versions can share the display name `Paradox
Launcher` and bundle ID `com.paradoxinteractive.launcher`. App-inventory order,
the first path in an ambiguity error and the highest installed version do not
identify the running instance. A timeout does not mean the launcher is closed.

1. Use the supported computer-use app inventory. If name/bundle-ID binding is
   ambiguous or times out, resolve the main running launcher executable with
   a bounded read-only lookup limited to that launcher (or an exact PID supplied
   by the user). Exclude Helper/Renderer processes. A sandbox-denied lookup is
   not evidence that no launcher exists; use authorized read-only escalation
   when appropriate. Do not enumerate or inspect CK3.
2. Derive the enclosing `Paradox Launcher.app` path from that executable and
   bind with `cua.getApp(fullAppPath)`. Do not guess a versioned directory:
   selecting an inactive copy may launch it. Do not restart either app.
3. Verify the returned launcher window identifies **Crusader Kings III** before
   configuring its playset. Use fresh accessibility state for subsequent UI
   actions. Use only APIs present in the current tool documentation; if window
   listing is unavailable, do not invent it or retry it as an alternative.
4. Keep resolved paths, PIDs and version-specific hints in ignored local notes;
   rediscover after launcher updates/restarts. Persist this portable procedure,
   not one machine's path/PID. Distinguish a successful bind from verified mod
   discovery/selection, and verify the enabled-mod manifest after UI changes.

### User app-state shorthand

The user may declare `GZ` = gra zamknięta (CK3 closed), `LO` = launcher
otwarty (launcher open), or both as `GZ, LO`. Treat these as explicit user
state declarations with the same meaning as the full phrases, without process
or UI verification. The shorthand alone reports state; it does not authorize
unrelated work. During an already described installation/test stage it satisfies
that stage's corresponding state prerequisite. Do not infer unreported states.

### User-operated CK3 console

The user confirmed **Shift + Alt + C** opens the console in the tested macOS
setup (2026-10-21). Prefer that observed shortcut when giving this user console
instructions; do not assume the backtick/section-sign key works on their layout.
Other layouts may differ. The user alone opens the console and enters commands;
Codex never operates or inspects the game window. After a user restart, use fresh
logs/version/mod evidence and output timestamps to establish generation provenance.

Use this cycle:

1. State required app state and the user's necessary preparation (for example,
   close CK3; open its launcher through Steam only if configuration requires
   GUI correction). CLI first verifies the persisted configuration as above. Accept the user's confirmation that prerequisites are ready;
   tell CLI to assume that state and execute without rechecking.
2. CLI performs its assigned work/checks and returns installation, persisted
   selection and prior-log preservation receipts. GUI reviews the decisive
   evidence; it inspects/configures the launcher only for the exceptions above.
3. GUI reports readiness and gives a short numbered set of user actions with
   expected visible result and a clear stop point. Group practical steps into
   one checkpoint; do not ask for another approval between routine substeps.
   The user starts CK3, loads/creates the disposable session and performs the
   specified actions. Never repeat passed cases without a concrete reason.
4. After the user reports completion, inspect/capture the relevant log interval,
   correlate it with their report and record findings with precise limits.
   Keep raw logs/saves/local paths ignored. If evidence is missing, request only
   the missing observation; do not operate the game or repeat the whole cycle.
5. Tell the user when game exit is required; after they exit, Codex handles
   authorized mod restoration and verifies files/persisted configuration first;
   launcher UI is needed only for unresolved or incorrect configuration.

These are role assignments, not extra approval checkpoints. Existing scope,
permissions, sandbox requirements and the acknowledgement rules still apply.

### Bounded log checkpoints

Use `scripts/ck3_log_delta.py` for a finite, per-file interval. Put baselines,
manifests and captured bytes under ignored `.codex-sync/`; choose a new path for
each run. Named logs are optional unless listed with `--required-name`;
explicit `--file` inputs are required. Missing optional logs remain visible as
gaps in the report. A required gap, changed boundary, partial line/read or byte
cap yields an incomplete interval for a required input. Baselines record whether
the cursor splits a line; initial and final fragments stay in the byte artifact
but are excluded from marker/error analysis. Fingerprints sample the first and
last 256 baseline bytes, so arbitrary same-size rewrites elsewhere may go undetected.

Example, with the user's CK3 log directory supplied explicitly:

```sh
python3 scripts/ck3_log_delta.py baseline \
  --log-dir "/path/to/CK3/logs" --name debug.log --name error.log \
  --required-name debug.log --required-name error.log \
  --payload-label "probe label" --build-label "build label" \
  --output .codex-sync/baseline-run-01.json
# User performs the already-authorized CK3 actions.
python3 scripts/ck3_log_delta.py delta \
  --baseline .codex-sync/baseline-run-01.json \
  --output-dir .codex-sync/checkpoint-run-01
```

Reports separate `interval_status` (`COMPLETE`, `COMPLETE_WITH_OPTIONAL_GAPS`
or `INCOMPLETE`), `observation_status` and marker/chain `expectation_status`
(`MET`, `UNMET` or `UNVERIFIED_INCOMPLETE_EVIDENCE`). Exit 0 means the command
produced its report; neither exit success nor interval completeness establishes
clean logs or CK3 test acceptance. `error.log` counts every nonempty complete
line as an error-channel observation; other logs use a labelled English severity
keyword heuristic. Full normalized message hashes distinguish repeated messages
from different messages with the same clipped snippet; summaries are bounded.

The CLI captures only bytes through each file's frozen end size; later appends
belong to a future checkpoint. Each log has its own capture interval, so the
set is not an atomic snapshot. An optional JSON `--spec` may define literal
`markers` (`name`, `literal`, optional `expected` and `log`) and ordered
`chains` (`name`, `begin`, `end`, optional `reject` and `log`). Every chain
occurrence is evaluated in text position order, including on one line; overlapping chain literal spans are refused as ambiguous. Counts and
ordered pairs are evidence of observed text only; equal counts do not prove
event identity. A missing marker means execution was unobserved. A
`WRITE_RETURNED` marker supports an execution receipt, not stored RGB,
classification correctness or visual acceptance. Keep the short CLI report
with the private artifacts, then let GUI review the receipt alongside user
observations. CLI finishes on current files and never waits for another game
action.

## Authorization and stage completion

### Batch preparation and user test instructions

Prepare related hypotheses, controls, expected observations and log checks
together before another user test launch. Prefer the existing installed payload
and complete ordinary view switches/observations in one paused session, with
one report per meaningful checkpoint rather than an acknowledgement per click.
Reuse passed cases unless a changed build/payload or comparison baseline gives
a concrete reason to repeat them. Keep necessary execution/attribution gates,
but do not split preparation, self-review and documentation into extra approvals.
An unresolved earlier error is not automatically a blocker for every independent
observation; identify its suspected effect and which dependent tests it blocks.
Do not label it harmless without evidence. Batch all justified source fixes for
the next revision; avoid speculative single-field edit/restart loops. Save/load,
disabled-mod and fresh-process checks retain their distinct state prerequisites.

- Carry out all necessary substeps of an authorized stage without asking for
  separate approval for planning, preparation, self-review and documentation.
  Include appropriate checks within the accepted scope. Do not end each
  substep with a new offer to continue.
- Treat `dalej`, `ok`, `gotowe` and `tak` (including natural variants such as
  `ok, to dalej`) as authorization to continue the clearly described next step
  and its necessary substeps. Act rather than asking whether the user really
  meant to continue. An additional formal permission phrase is not required.
- Acknowledgement of a proposal explicitly including installation, game launch
  or a specified new test authorizes that proposal, even when an earlier stage
  excluded tests. It supersedes the earlier restriction for that stated scope;
  it does not authorize repeating passed tests or unrelated actions. Approval
  of preparation alone still does not authorize an unmentioned runtime cycle.
- Example: after "Next: install the isolated ENTRY v1 probe and perform one
  absent-player observation", `dalej` authorizes that installation and single
  observation. Do not ask the user separately to revoke an older no-tests
  instruction. After "Next: prepare source only", `ok` authorizes preparation.
- Ask only if required information is missing, multiple materially different
  next actions remain unresolved, or the action lies outside the accepted
  scope. State ordinary implementation assumptions and proceed. A restriction
  already superseded by acceptance of the concrete next step is not a blocker.
  Complete unaffected authorized work before asking about a real blocker.
- Current user messages take precedence over historical permission notes in
  CURRENT_STATE.md, probe procedures and handoff records. Update the current
  operational state when permissions change; preserve dated history as history.
  Do not invent another review-only approval stage or an acknowledgement loop.
- Authorization must still identify the action through context. A bare
  acknowledgement of unrelated work does not grant Git staging/commit/push,
  publishing or GitHub writes. If those exact actions were clearly proposed,
  the user's affirmative acknowledgement counts as explicit authorization.
- A CLI handoff carries the parent's permissions and exclusions verbatim in
  substance. Delegation grants no extra Git, GitHub, install or runtime rights.

## GUI to CLI handoff

GUI / Sol owns task selection, problem and scope, acceptance criteria,
architecture, material choices, user coordination and review. CLI / Luna owns
only the bounded work, files and checks listed in its delegation; it may
interpret evidence and recommend, while decision authority remains GUI. Give
every task a stable delegation ID and parent ID, primary type and
`Decision authority: GUI`, model profile, frozen scope, minimal exact context,
allowed discovery/input roots and limits, mutable-state policy or snapshots,
owned output paths, exclusions, safety/permissions, checks and GUI next step.
Record hashes of actual dirty input bytes; Git HEAD alone is not a baseline.
One integrator edits shared source/docs. Parallel tasks write separate
artifacts. Do not repeat GUI research in CLI. Installations and tests against
one live game remain sequential. A worktree is optional and must receive the
correct input snapshot. Use [CLI_DELEGATION_TEMPLATE.md](CLI_DELEGATION_TEMPLATE.md)
for the compatible task and result shape; it does not replace the lifecycle
helper.

Route bounded collection, verification, research, comparisons, documentation,
analysis and approved execution to CLI / Luna / Medium; trivial mechanical work
may use Luna / Low. GUI retains decisions and product coordination. More
difficult work remains bounded and is returned with evidence or an escalation
request; do not auto-upgrade the model or transfer decision authority. GUI may
explicitly select a stronger worker/reviewer. These are recommendations, not
availability or cost claims; report actual model only when known. Preserve the
small direct-edit exception when delegation overhead exceeds the work.

For probes/mods, read [MOD_AUTHORING_RULES.md](MOD_AUTHORING_RULES.md), name exact payload/install roots and expected version, run the preflight before installation and again with `--installed` afterward, and include the manual and user-run startup/log gates. This does not apply to tooling that does not touch a mod.

For authorized recurring installs, a machine-local trusted-project
`.codex/config.toml` may add only the exact diagnostic mod directory to
`sandbox_workspace_write.writable_roots`, keeping `workspace-write` and the
existing approval policy. Keep that configuration ignored by Git. Start a new
CLI session to load the setting; host-managed session permissions may override
local configuration. Try ordinary sandbox execution within that allowed root;
do not request escalation preemptively on every installer retry. Escalate only
for an actual denied operation outside the effective policy. Do not grant the
whole CK3 user-data/game directory or disable the sandbox. Permissions do not
replace scoped install authorization, backups, preflight or the game-closed
prerequisite. Self-review installer evidence-directory handling before execution,
and use no-write syntax inspection to avoid unrelated cache permissions.

### Per-ID lifecycle helper

New handoffs live under `.codex-sync/tasks/<ID>/` with `CLI_TASK.md`,
`STATUS.json`, `CLI_RESULT.md`, `GUI_REVIEW.md` and optional `artifacts/`.
`STATUS.json` alone controls lifecycle. Scope is frozen at READY; a different
scope needs a new ID. The helper coordinates cooperating workers, not an OS
sandbox. All administrative paths, including hidden parents, archives, claims,
locks and review/result paths, must remain regular files/directories without
symlinks. This prevents accidental path escape, not hostile concurrent path
replacement or hard-link attacks.

Run `python3 scripts/handoff.py --root . <operation> ...` from the repository:

- Create: `create <ID> --parent <PARENT> --task-file <path> [--input <path> ...]
  [--owned <path> ...] [--check <name> ...]`. Paths are normalized and relative
  to the repository. `--input` declares an immutable dependency. `--owned`
  explicitly declares an editable input/output, including an existing dirty
  source/doc or a new file; if also supplied as `--input`, it is editable but
  must initially exist. Other new owned files have an initial fingerprint of
  JSON `null`. All initial fingerprints remain in `inputs`, and the actual
  initial bytes and manifest remain in `baseline/` across attempts. Do not omit
  editable source from the baseline. Handoff administration is not an assigned
  input/output; local context outside `tasks/` may be an input.
- Resolve pickup: `resolve [ID]` selects the named READY handoff or the sole
  READY candidate, considering controlled legacy compatibility as above.
  `claim <ID> --owner <session-label> --revision <N>` checks the frozen scope
  and **all** initial fingerprints before claim side effects, then moves READY
  to IN_PROGRESS. An interrupted claim is preserved; no age-based takeover.
- Inspect: `list` shows per-ID states/revisions; `validate <ID>` checks frozen
  scope and preserved baseline. READY validation checks all initial inputs;
  during work it checks immutable dependencies while allowing declared edits.
  Completed/consumed validation also checks recorded final output hashes.
  Validate before work and completion. Hashes cannot identify who edited an
  owned file: one writer per owned path and the integrator's baseline/diff
  review remain necessary; edits to undeclared files are not OS-enforced.
- Finish: write `CLI_RESULT.md` with nonempty sections Identity, Result, Files,
  Checks, Self-healing / agent-instruction findings, Permissions / Git state,
  and GUI next step. Include a fenced `json` provenance object with `id`,
  `parent_id`, `attempt`, the exact initial `inputs` map from STATUS, and an
  `outputs` map of every owned path to its final SHA-256 (or `null` if absent;
  `{}` when no paths are owned). Result must contain the exact lines
  `- Outcome: SUCCESS` and `- Acceptance: PASS`; Checks must contain an exact
  `- <check-name>: PASS` line for each requested check. Annotations belong on
  separate lines. `complete <ID> --owner <owner> --revision <N>` checks this
  real grammar, frozen scope, immutable dependencies and final provenance,
  then records outputs/result hashes and moves to COMPLETED. It permits
  assigned edits and retains the original inputs. Structural validation does
  not prove truth or substantive acceptance. A complete negative finding is
  successful only if it satisfies its investigation's criteria.
- Failure/recovery: `fail <ID> --owner <owner> --revision <N> --reason <text>`
  records FAILED even if scope or input drift caused the failure.
  `recover <ID> --revision <N> --reason <text>` records a READY claim interrupted
  before its status update, preserving claim evidence for coordinator review.
- Retry: `retry <ID> --revision <N>` is an explicit coordinator action for FAILED
  or confirmed interrupted IN_PROGRESS. Scope and **all initial** inputs,
  including owned files, must still match. Changed inputs require a new
  delegation with a new baseline; the helper never restores or discards edits.
  Retry archives previous status, result, review and claim owner in
  `attempts/<attempt>/`, preserves baseline evidence and reopens the same
  scope with a new attempt. It never silently rebases fingerprints.
- Receipt: `resolve [ID] --receipt` resolves COMPLETED results, not READY work.
  After inspecting actual changes/evidence, `consume <ID> --revision <N>
  --review <text>` verifies unchanged result, immutable inputs and final
  outputs, records the review and moves COMPLETED to CONSUMED.
  CONSUMED records GUI review as ACCEPTED or CHANGES REQUIRED; only acceptance
  advances the parent stage.

Every mutating transition holds a per-task OS file lock from the revision,
state and owner checks through its evidence changes and status replacement.
Creation reserves a new ID exclusively; separate IDs have separate locks.
Stale commands cannot change claims, archives or reviews. Do not acquire a
second lock inside a transition. Status writes use atomic replacement.

Retry and consume write `.transition.json` before changing attempt/review
evidence. If interrupted, repeat the **same command with the original
revision and review text** to finish idempotently, even when status was already
written. Other transitions are blocked while the journal remains. Archives
are copied completely before active evidence is removed; the journal retains
the original evidence until status is committed. Conflicting preserved bytes
require coordinator inspection; do not remove the journal or steal a claim.
This is local interruption recovery, not a power-loss durability guarantee.

### GUI execution plan and CLI progress

As the **last preparation step**, after settling scope, permissions, owned
paths and checks, GUI derives 1–20 meaningful major milestones for a handoff
where progress reporting is useful. Prefer fewer broad stages; never list shell
commands or add stages merely to smooth the display. Include validation,
review, cleanup, authorized publication and final handoff when materially
required. A publication milestone grants no permission. Freeze the plan before
READY using `create --execution-plan '<plan JSON>'`, which appends one fenced
`json` object `{"execution_plan": <plan>}` to `CLI_TASK.md`. Alternatively put
that single block directly in the task description. Do not supply both.

The plan has exactly `total_steps` and `steps`, where `total_steps` is an integer
matching the list length, and each step has exactly `id` and `label`. IDs are
unique lowercase identifiers matching `[a-z][a-z0-9_-]{0,39}`. Labels are
nonempty, single-line text up to 160 characters without control characters.
Malformed or duplicate plans are refused before task creation. CLI receives
the GUI's initial plan and chooses concrete commands within each stage; it
must not reconstruct initial milestones from prose. Existing planless per-ID
tasks and controlled legacy handoffs remain compatible without migration or
invented progress. `progress` refuses a planless task.

For a planned handoff, show the actual `execution_plan.total_steps` beside the
time range in the GUI-to-CLI receipt table. Keep a compact calibration record
with original estimate ranges and claim-to-complete elapsed minutes. Pair only
comparable, single-attempt completed work; exclude failed, retried, interrupted,
or otherwise incomparable tasks and do not count user waiting as compute.
When there are enough comparable pairs, use the median actual/estimated midpoint
ratio as a simple robust multiplier, apply it to both range endpoints, and round
outward to whole minutes. Preserve source pairs and describe the small-sample
uncertainty. If fewer than three comparable pairs exist, use the user-observed
2–3× overestimate only as a prior: divide the low endpoint by 3 and the high
endpoint by 2, round outward, and label the result as prior-based rather than
measured. A planless handoff retains the ordinary uncalibrated estimate and
shows `no plan`. Save newly available estimate/elapsed pairs during normal task
closeout; progress transitions do not measure or display time.
The standard library helper can retain a candidate pair during that same
closeout with `python3 scripts/gui_context.py --repo . --timing-task-id <ID>`;
it reads only the named per-ID `CLI_TASK.md` and `STATUS.json`, appends
idempotently to `.codex-sync/gui-context-calibration.json`, separate from the
frozen T-012 evidence snapshot, and marks whether a frozen
range was present. GUI explicitly marks a reviewed comparable candidate with
`--timing-eligible <ID> --review-note '<reason>'`. To prepare a range, use
`python3 scripts/gui_context.py --repo . --estimate-min <low> --estimate-max <high> --steps <plan-count>`;
the output includes the calibrated range, basis, pair count and uncertainty.
GUI still decides comparability before using a pair. Keep the raw baseline in `Estimated CLI time: <low>–<high> minutes` in the frozen task and calibrated time/steps separately, to avoid applying calibration twice. See [GUI context guide](GUI_CONTEXT.md) for retry, history integrity, session boundaries and published-ref handling.

An optional GUI context measurement is prepared during the same handoff
preparation, with no extra model call or GUI turn. Run
`python3 scripts/gui_context.py --session <explicit-saved-session-file> --task <parent-ID> --handoff <delegation-ID> --repository-ref <published-ref> --identity <stable-private-session-key> --preview <private-preview.json>`
and pass that preview to normal `handoff.py create --context-preview`.
The helper reads only the named bounded JSONL input (16 MiB maximum), counts
deduplicated user/assistant text from known message events, and labels
`ceil(UTF-8 bytes / 4)` as an estimate. It does not inspect a GUI or infer active
model context from request usage. It writes aggregate JSONL under
`docs/telemetry/gui-context/<parent-ID>.jsonl`; raw text, session key, path,
hash and byte cursor stay private in `.codex-sync/gui-context-private.json`.
Changed identity, method, compaction or reset makes the delta unknown. No
measurement means no history file and no history link. The optional preview is
diagnostic only, at most two short lines, and never changes scope or plan.

Example in a disposable repository (owner `worker`, no assigned outputs):

```sh
python3 scripts/handoff.py --root . create T-007-EXAMPLE --parent T-007 \
  --task 'Prepare bounded change, verify it and finalize evidence.' \
  --check offline-tests \
  --execution-plan '{"total_steps":3,"steps":[{"id":"prepare","label":"Prepare bounded change"},{"id":"verify","label":"Validate and review change"},{"id":"handoff","label":"Finalize evidence and CLI handoff"}]}'
python3 scripts/handoff.py --root . claim T-007-EXAMPLE --owner worker --revision 1
python3 scripts/handoff.py --root . progress T-007-EXAMPLE --owner worker --revision 2 --start prepare
# Execute concrete preparation commands; keep ordinary output readable.
python3 scripts/handoff.py --root . progress T-007-EXAMPLE --owner worker --revision 3 --done prepare
```

Continue with `--start verify`, `--done verify`, `--start handoff`, `--done
handoff`, each with the current revision from `STATUS.json`. Write the exact
result grammar and hashes, then run `validate` and `complete` as above. Use
`progress <ID> --owner <owner> --revision <N> --start <id>` at a stage's start
and `--done <id>` after its actual work passes. Only one milestone may be
current; finish it before starting another. All supplied milestones are
required; their IDs may be visited in an order appropriate to dependencies.
Only the final `complete` operation can emit 100%, after all milestones,
result checks, frozen input/scope and final provenance checks pass. Its output
explicitly says `CLI complete; GUI review pending`. Later receipt/acceptance
remains the coordinator's separate decision; 100% does not complete a parent.

Each successful meaningful transition emits one compact diagnostic line on
command stdout. The renderer uses a 30-cell Unicode bar with
`percent * 30 // 100` filled cells, the parent ID (delegation ID only when the
parent is unavailable), and the persisted plan's readable label. Its shape is
`●  T-007 [██████████████████░░░░░░░░░░] ~60% — Validate changes`. A green ANSI
sequence colors the bullet only when stdout is a TTY and `NO_COLOR` is absent;
otherwise the same bullet is uncolored. At 100%, the label is exactly
`CLI complete; GUI review pending`. This is ordinary tool output; it does not
create an agent message and the client may collapse it. After the command
succeeds, CLI reads persisted `STATUS.json.progress` and sends one standalone
plain-text agent commentary with the same readable structure, without ANSI
escapes. Translate readable stage/boundary text into the language of the latest
user request; preserve commands, IDs and required receipt phrases. Never
reconstruct or guess a percentage from the command text. Do not relay a failed,
rejected, stale or no-op command, and do not repeat a commentary for an unchanged
state. At 100%, explicitly say
`CLI complete; GUI review pending`. No timer, ETA, elapsed-time display,
sub-progress or repeated checklist is added. Normal command logs remain. While
a long stage runs, leave the displayed percentage unchanged. The integer is
`max(previous_display, min(99, completed_count * 100 // total_steps))`;
only gated CLI completion sets 100. This is a coarse milestone orientation,
not measured time, CPU, tokens or remaining workload. One-stage tasks remain
at 0 until that stage ends, then 99 until completion gates pass.

For genuinely necessary major work **within the same scope**, use
`progress <ID> --owner <owner> --revision <N> --amend '<replacement plan JSON>'
--reason '<justification>'`. Adapt labels only when original intent remains;
retain every existing ID and its order, optionally appending major stages.
No deletions, renames or reordering; the cap stays 20 steps and there may be
at most 20 amendments per task. Reasons must be nonempty and at most 1000
characters. Semantics and necessity require review; the helper validates
structure, not whether a justification is true. A changed scope or permission
still requires a new handoff. The frozen original plan/scope remain unchanged;
status preserves each replacement plan, reason, owner, revision and timestamp.
Replaying this evidence must reproduce the active plan. Adding stages clamps
the displayed high-water mark until the completed fraction catches up; it
does not create artificial progress.

`STATUS.json.progress` persists the active plan, current ID, completed IDs,
displayed integer and amendment evidence. Restart with the same owner and
current revision; do not reclaim or steal a claim. Repeating a current `start`
or already completed `done` with the **current** revision is a silent no-op,
without a revision increment; a stale revision is still rejected. Validation
does not emit a bar or advance progress. Status persistence and terminal
printing are not an atomic transaction: interruption after persistence but
before output can omit a line; restarting must not invent or replay work.

Failure preserves the last progress as evidence and never emits 100. FAILED
tasks reject progress changes. Explicit coordinator retry keeps the original
scope/input rules and archives the prior status with its progress. The new
attempt retains amendments and displayed high-water mark but clears current
and completed IDs, so every milestone must be executed again. Its retained
percentage is historical orientation, not a remaining-work estimate. An
interrupted IN_PROGRESS attempt uses the same explicit retry safeguards.
COMPLETED and CONSUMED tasks reject progress writes; receipt keeps the
100% CLI-execution value even if GUI requests changes. Corrective work needs
a separate handoff. Planless tasks keep the original lifecycle behavior.

Progress uses the same per-task lock, owner, revision, pending-journal,
symlink/path, baseline and frozen-contract guards as lifecycle transitions.
Only one atomic status replacement follows all checks. No progress command
changes task text, baseline, claims, outputs, result grammar or publication
permissions. See [T-007](tasks/T-007-handoff-progress.md) for acceptance and
offline evidence; GUI still reviews the actual diff and evidence before receipt.

### Legacy pickup and GUI receipt

The controlled T-001-T1-FIX correction continues in `.codex-sync/CLI_TASK.md`
until GUI accepts the foundation. Its Status line remains the legacy authority;
mark it IN_PROGRESS and write `.codex-sync/CLI_RESULT.md`. Do not use the helper
to claim/complete that correction or migrate it midway. Preserve archives.
Named new-format tasks work without the legacy inbox. Bare pickup/receipt must
first use the shared resolver so it cannot silently prefer legacy.

A legacy result still includes identity, actual checks, limits, permissions/Git
state, GUI next step and self-healing. Before marking COMPLETED, inspect every
assigned gate and the actual result. Terminal text is exactly
`COMPLETED: STATUS SUCCESS!` on success or `COMPLETED: STATUS FAILURE!` on
failure; success requires all assigned acceptance criteria.

`gotowe <ID>` means review and consume that completed result. Bare `gotowe`
requires a sole eligible COMPLETED candidate across both formats. Confirm
identity, inspect actual diff/evidence and self-healing, update the parent
record/state/index where materially changed, then consume the named result
(or record legacy review). Preserve failed evidence. Child completion never
completes its parent.

Every material stage records in its own result: observation, cause or unknown, recovery, outcome, and a small reusable instruction/tool suggestion. Report recovered errors with sanitized operation, diagnostic/exit code and recovery. One coordinator promotes verified reusable lessons; repeated violations of an existing rule call for execution/tool fixes, not automatic rule growth. No background monitor or report per chat message.

## GitHub issue title convention

Use the stable task identifier as the only textual category prefix in new
project issue titles: `<ID> — <concise title>`, where `<ID>` begins with R-,
F-, T- or B- and uses the next verified stable identifier. Do not prepend
`research:`, `feature:`, `feat:`, `task:`, `chore:`, `bug:` or equivalent
category words. Keep useful GitHub type labels as metadata. Templates should
show the appropriate ID prefix and explain that the placeholder must be
replaced; examples should retain ordinary title text after the ID. Commit
message prefixes in CONTRIBUTING.md are separate and remain valid. Do not
change historical issue bodies or task identifiers merely to match this rule.

## GitHub and permissions

Use `gh` for GitHub operations when available. Read-only examples include `gh auth status`, `gh repo view`, `gh issue list`, and `gh issue view <number>`. Authentication is local state: do not reauthenticate automatically or record credentials/account identity. GitHub reads and writes are separate permissions. A task must explicitly authorize GitHub writes before creating/editing/commenting on/closing Issues or PRs or changing labels/milestones. Before each write, verify the repository, exact target, and current remote state; make only the requested change and verify the result. Never guess an Issue number or create a duplicate. GitHub-write authorization does not grant Git staging, commit, or push permission.

For substantial work, use the stable planning ID (R/F/T/B-xxx) in the Issue title/body. The Issue is the detailed investigation journal; comments may record hypotheses, tests and concise sanitized evidence. Do not paste full logs. At completion, put the distilled result in one canonical `docs/tasks/<ID>-<slug>.md`, update reusable technical knowledge in `RESEARCH.md`, and finalize the Issue only if writes are authorized. Do not close an Issue before its acceptance criteria are met.

### Wiki AI-cost estimates

Before closing any task, the GUI coordinator verifies its cost accounting
against saved sessions. Every task must have at least one identified GUI
session and zero or more identified CLI sessions; GUI-only tasks need no CLI
session. Include all attributable GUI preparation/review/publication, CLI
execution and linked automatic-review response counters through the frozen
cutoff. Record the session inventory and exact task/turn mapping privately.
If the required GUI session cannot be found, report the evidence gap and the
search performed; never invent a session or silently skip the GUI check.
Map task-specific turns and deduplicate response IDs with the existing
accounting helper; do not use aggregate session totals for mixed-task chats.
Keep source snapshots, hashes and assignments private.
A missing table in CLI_RESULT is not a reason to declare N/A. Use N/A only
for a specifically checked missing/unattributable counter, and record the
source check and reason. Unknown model prices remain unpriced even when
usage is measured. Freeze a finite completion cutoff and state later excluded
work; do not repeatedly extend accounting to count its own publication.

When publishing or updating the project Wiki's AI-cost section, estimate the
API-equivalent USD cost for every newly added eligible task using its recorded
per-model input, cached-input and output token counts. Apply current official
API prices for each recorded model and state the price lookup date and source.
Cached input is a subset of input; price uncached and cached input separately,
and do not count reasoning tokens again when already included in output. Do
not equate subscription usage with API spend. Keep unknown model/pricing
buckets visible as unpriced; do not guess model mappings. Note when
request-level context lengths, cache writes or other metering details are
unavailable, and label the result as a rough estimate for measured usage.
Recheck official API prices when refreshing the Wiki, since rates can change.
Preserve the existing R/T/F/B summary and matching per-task detail groups.

For **total cost** arithmetic at every aggregation level (model, task, task
type and overall), an N/A cost component contributes $0 to the sum. It must
not propagate N/A over known dollar amounts. Whenever at least one component
has a numeric USD cost greater than zero, display the total in USD, never
N/A. Sum unrounded known amounts before formatting the displayed total.
For example, `$1.24 + N/A = $1.24`, and `$1.24 + $0.53 + N/A = $1.77`.
This convention applies only to cost aggregation: keep individual unavailable
costs as N/A and unknown model prices visibly unpriced. Do not replace missing
token counters with zero or claim missing usage actually cost nothing. Label
such totals as partial known/priced cost and preserve coverage limitations.

### Required AI-cost table in task reports

Every AI-cost update or task-closeout publication must include a GFM table in
the GitHub Issue/PR body and matching canonical task record. A prose total or
link alone does not satisfy this requirement. Keep prose for context below
the table. Use exactly these columns, one row per recorded model, and a bold
Total row:

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| <recorded model> | <input> | <cached subset> | <input minus cached> | <output> | <input plus output> | <$USD or N/A> |
| **Total** | <sum> | <sum> | <sum> | <sum> | <sum> | <sum of known unrounded USD> |

State partial/missing coverage, finite cutoff, excluded work, price date/source,
context-rate handling and unpriced models below the table. Keep unavailable
counters N/A and unknown prices explicitly unpriced; do not hide their rows or
invent model aliases. Cached input is a subset; reasoning is already included
in Output. Sum known unrounded USD with N/A contributing zero only to cost
arithmetic; a positive known sum must display USD. The token-only fragment
from task_ai_cost.py is not the final priced publication table: combine its
verified counters with verified per-model pricing without changing attribution.

For any handoff updating/publishing costs, GUI must assign the named check
`ai-cost-table-format`. CLI must verify the exact header, per-model rows, Total
row, arithmetic and limitations in every scoped Issue/PR body and canonical
record, then read back the published body and verify the same table again.
Report the exact standalone `- ai-cost-table-format: PASS` only after those
checks. Missing tables or prose-only reports are CHANGES REQUIRED even when
the numeric prose total is correct. This is a semantic review/check convention,
not a new handoff.py schema or permission. Preserve the Wiki's separate grouped
R/T/F/B summary and per-task layout; it need not use this per-model schema.

## Task finalization

GUI must perform the saved-session cost check above before closing each task,
including GUI-only tasks; CLI completion alone does not satisfy that check.

Before marking a substantial task done, update the canonical task summary, reusable research if needed, decisions if semantics/architecture changed, backlog, task history, current state, and affected risk/test/architecture docs. Update CHANGELOG only for user-visible changes. Run relevant consistency checks and privacy review. Preserve partial status when gates remain open; do not turn an unfinished task into a historical completion row.

## Public-content privacy gates

Before staging, inspect every candidate change for identifying absolute paths, usernames, emails, credentials/tokens/cookies, account or device IDs, private URLs, raw logs/dumps/saves, and generated or copyrighted vanilla material. Sanitize or stop on suspicious content. Before commit, inspect the exact staged diff again, run `git diff --cached --check`, and check for unexpected generated/binary files. A later cleanup does not remove secrets from Git history. Do not stage/commit/push unless separately authorized. Existing historical privacy audit is recorded in `PRIVACY_AUDIT.md`; this workflow applies controls to new and modified content.

No custom scanner is added yet: simple pattern matching can miss context in screenshots/logs and produce false alarms, while mandatory human review remains necessary. Reconsider a small helper if repeated manual checks become error-prone; any helper supplements, rather than replaces, review of the exact diff.

## Local handoff files

`.codex-sync/` is local-only and ignored by Git. Keep `CLI_TASK.md` and `CLI_RESULT.md` concise; do not use them to store credentials, raw logs, or private machine details.
