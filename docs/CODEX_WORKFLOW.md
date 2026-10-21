# Codex Workflow

This document is the detailed operating procedure. Keep [AGENTS.md](../AGENTS.md) short. The repository and all GitHub content are public; local machine state is not project documentation.

## Session startup and task scope

### CLI handoff pickup precedence

When the user invokes `pobierz zadanie`, this is a handoff pickup. Read
`AGENTS.md` and `.codex-sync/CLI_TASK.md` before selecting any task from the
operational state/history. A `READY` handoff's delegation ID and parent task ID
are the active work for that invocation and override stale or historical
`CURRENT_STATE.md` / `TASK_HISTORY.md` entries. Read only the handoff's
referenced context, mark it `IN_PROGRESS`, and proceed within its scope. Do not
announce or select a different task because a completed task remains in the
state file. If the handoff is missing, not `READY`, or its IDs/status conflict,
report the discrepancy and stop; never silently fall back to another task.

For ordinary GUI startup, read the state and history as below, but the latest
explicit user selection in the conversation takes precedence over stale
operational text. Before dispatching a handoff, GUI should synchronize the
selected task in `CURRENT_STATE.md`; the handoff remains an additional explicit
source of task identity for CLI pickup.

1. Read `AGENTS.md`, `docs/CURRENT_STATE.md`, and `docs/TASK_HISTORY.md`.
2. Identify the active stable task ID. Read its issue/definition only if needed, then load only the relevant sections of deeper docs and evidence.
3. Check Git status before editing. Preserve unrelated user changes. One substantial backlog task belongs in one chat; keep iterations of that task in the same chat.
4. For CK3 research, identify the subsystem, consult [CK3_SOURCE_MAP.md](CK3_SOURCE_MAP.md), then inspect only the recommended target-build/generated/vanilla sources. Escalate to separately authorized runtime work or bounded community discovery only when static sources leave the question unresolved. Reuse completed findings; repeat target-build research only when the build changes, evidence conflicts, or revalidation is requested.

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

The GUI coordinates with the user and uses Sol / Medium as the default reasoning profile. CLI defaults to Luna / Medium for scoped routine work, Luna / Low for trivial mechanical work, Sol / High for unknown CK3 behavior or difficult debugging, and Sol / Medium (or High when warranted) for independent review. Choose by reasoning difficulty, not task size. Do not claim a model switch unless the runtime confirms it.

## Required GUI/CLI routing decision

Before substantial source edits, documentation maintenance or investigation,
choose where the work belongs. Reassess when uncertain research becomes a
bounded implementation/preparation task; the preceding GUI work is not a
reason to keep all subsequent work there.

| Work | Default route |
|---|---|
| User coordination, scope/architecture decisions, unresolved engine reasoning | GUI; delegate a bounded specialist question when useful |
| Probe/source preparation with a settled design and clear acceptance criteria | CLI, usually Luna / Medium |
| Bounded documentation updates, consistency work, mechanical edits | CLI, usually Luna / Medium; Luna / Low for trivial work |
| Genuinely independent review | A separate reviewer/session, usually Sol / Medium; GUI assesses the returned result |
| Inspecting a CLI result and integrating its conclusions | GUI |
| All CK3 game UI interaction, including start/exit, loading, saving, observation and tests | User only; no Codex game-window inspection or control |
| Configuring an already open launcher, playset selection and mod toggles | Codex GUI; reuse the test playset by default |
| A small direct edit where the handoff would cost more than the edit, such as a short workflow clarification | GUI allowed |

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

## Roles, prerequisites and CK3 test cycle

- CLI executes ready, bounded code/file/install/log tasks and returns results.
  It assumes the declared game/launcher state is correct because the user
  prepares it before invoking CLI. Do not verify it with ps/pgrep, process
  enumeration, Activity Monitor, app inventories, UI access or another method.
  Do not request escalation/confirmation for a process check, wait for user
  actions, or mark FAILED because app state was not independently verified.
  CLI reports actual code/file/tool failures, not a manufactured state gate.
- Codex GUI coordinates the work, prepares handoffs, reviews actual changes,
  inspects logs and installed mod files, and configures the already open CK3
  launcher/playset. It gives the user concise in-game test instructions and
  analyzes logs afterward. It may perform mod file operations or delegate them
  to CLI according to the routing rules.
- The user opens/restarts launcher and game through Steam and performs every
  interaction inside CK3: loading, saving, menus/options, character changes,
  observer setup, diagnostic clicks, interface testing and normal game exit.

Codex must not bind to, inspect, screenshot, activate, click, control, launch
or close the CK3 game window, even when automation is technically available.
A failed in-game automation call is not a reason to try another method. Do not
spend tokens exploring the game UI. Analyze logs and user-reported observations;
distinguish those evidence sources. The user may supply screenshots if useful.
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

### User-operated CK3 console

The user confirmed **Shift + Alt + C** opens the console in the tested macOS
setup (2026-10-21). Prefer that observed shortcut when giving this user console
instructions; do not assume the backtick/section-sign key works on their layout.
Other layouts may differ. The user alone opens the console and enters commands;
Codex never operates or inspects the game window. After a user restart, use fresh
logs/version/mod evidence and output timestamps to establish generation provenance.

Use this cycle:

1. State required app state and the user's necessary preparation (for example,
   close CK3, or open its launcher through Steam). Codex configures the launcher
   when available. Accept the user's confirmation that prerequisites are ready;
   tell CLI to assume that state and execute without rechecking.
2. CLI performs its assigned work/checks and returns; GUI verifies the result,
   installed payload, intended mod selection and preservation of prior logs.
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
   launcher/mod restoration and verifies the resulting configuration.

These are role assignments, not extra approval checkpoints. Existing scope,
permissions, sandbox requirements and the acknowledgement rules still apply.

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

For every probe/mod preparation, revision or game-build change, read and apply
[MOD_AUTHORING_RULES.md](MOD_AUTHORING_RULES.md). The handoff must name the
explicit source/installed payload roots, exact expected version, and commands
`python3 scripts/check_mod_preflight.py <payload-root> --expected-version <version>`
before installation and the same command with `--installed <installed-root>`
afterward. Include manual source/schema/guard review, private backups, wrapper
metadata verification and the fresh user-run startup/log checkpoint before
loading, saving or classification. A file check or metadata declaration is not
engine/API/runtime validation. Build changes require targeted revalidation and
generated-document provenance; retain prior findings under their actual build.

Use one active delegation at a time. Write `.codex-sync/CLI_TASK.md` with a unique delegation ID, parent task ID, model/reasoning recommendation, goal, reason, minimal context references, requested work, expected files, exclusions, explicit permissions, completion criteria, and result path. The task file owns its listed files while the delegation is active; the GUI avoids those files and CLI avoids unrelated files. If unexpected overlapping edits appear, stop and report the conflict.

Tell the user briefly which model to use and to start CLI with `pobierz zadanie`. Do not duplicate the task body in chat. For specialist investigation, prefer repository edits disabled and return findings through `CLI_RESULT.md`.

Bundle related source preparation, its self-review, permitted checks and the
necessary documentation into one bounded handoff rather than separate approval
rounds. Include pre-existing local changes and how to preserve them. Preparing
the handoff is not executing it: do not claim CLI ran or the recommended model
was used until there is an actual result. If the user must start CLI manually,
stop at the handoff boundary and await that result.

Include a GUI-before / CLI-work / GUI-after / user-action split, including
declared launcher/game state as an assumption, not a CLI check. Complete
permitted launcher/file prerequisites and obtain necessary user preparation
before dispatch; CLI must not wait for
user actions. After the result arrives, launcher configuration, logs and
readiness remain Codex responsibilities; all in-game work belongs to the user.
A result's "GUI next steps" are for Codex configuration, not a click checklist
to forward to the human. Launch permissions in an older handoff do not override
the user's standing instruction that they alone start launcher and game.

## CLI command: “pobierz zadanie”

Read `AGENTS.md` and `.codex-sync/CLI_TASK.md` before choosing a task from
`CURRENT_STATE.md` or `TASK_HISTORY.md`. Require `Status: READY`, and use its
delegation and parent IDs as the active assignment even if the state/history
still describes the previous task. Load only referenced context. If the
handoff is missing, not ready, or inconsistent, report that and stop rather
than selecting fallback work. Warn before starting if the active model is
reliably known to differ from the recommendation. Mark the task `IN_PROGRESS`,
execute only the permitted work, run requested checks, write
`.codex-sync/CLI_RESULT.md`, then mark the task `COMPLETED`. If blocked or
failed, record `FAILED` and preserve both files for GUI inspection.

For every file referenced by the handoff, validate the exact path before
reading it. First confirm the repository root; use the full repository-relative
path, including `.codex-sync/` for handoff files. Use `List` only to inspect a
directory and `Read` for its exact file. Separate required and optional
references; do not issue a batch of assumed paths or globs and let the shell
fail on the first missing match. A search that returns no matches is not by
itself a task failure: check the search scope/source map and report the
coverage limit. For `rg`, exit 1 is no matches; exit 2 is a real invocation,
regex, or path error. On exit 2, inspect stderr and fix the command/path before
continuing; do not count that attempt as evidence. Record actual tool or file
errors accurately.

If a read/list/search tool call fails, do not repeat it unchanged or continue
dependent work. Capture the exact path, operation, exit code, and diagnostic;
then validate the path or syntax and retry only the smallest read-only step. If
the exact required file is genuinely absent/unreadable, stop and report the
blocker. This makes predictable setup mistakes avoidable while keeping genuine
unexpected errors visible.

### Self-healing and configuration feedback

Agents should recover from a correctable in-scope problem, then report it so
the workflow can improve. Every CLI result must include a
**Self-healing / agent-instruction findings** section. If no problem occurred,
write `None`. If a problem occurred, even when recovered, record the sanitized
operation and target, exact exit code/error summary, cause if known, corrective
step, whether retry succeeded, any work skipped, and whether the issue suggests
a reusable instruction gap. Do not include credentials, private paths, raw logs, or
unnecessary personal data. Distinguish genuine command/tool failures from
expected no-match or optional-file conditions; never disguise one as the other.

The GUI reviews that section and the actual changes when consuming the result.
If the problem exposes a repeatable instruction/configuration gap, update and
validate `AGENTS.md` and/or `CODEX_WORKFLOW.md`, and preserve the task's result
and scope. If the error is isolated or the instructions already cover it,
record why no configuration change is needed. CLI may fix its own command or
path and continue within scope, but must not edit agent configuration unless
the handoff explicitly includes that work. Do not create an automatic loop
that changes configuration for every harmless no-match; changes must address
an identified, reusable failure mode.

Before marking a handoff `COMPLETED`, inspect the actual `CLI_RESULT.md` and
confirm the self-healing section exists and accurately accounts for the run.
Write `None` only after reviewing the tool/command results. If a problem
occurred but its cause or recovery is unknown, say so explicitly rather than
implying it was fixed. A missing section blocks `COMPLETED` until the result is
amended; do not emit the success line while this gate is open.

At the end of the user-facing CLI response, print one status line with ANSI
color when the terminal supports it: on genuine success, green
`COMPLETED: STATUS SUCCESS!`; on a failed/blocked task, red
`COMPLETED: STATUS FAILURE!`. Use ANSI SGR green (`\033[32m`) and red
(`\033[31m`), then reset (`\033[0m`). If color is unavailable, print the same
exact text plainly; never expose raw escape codes. Keep `CLI_RESULT.md`
machine-readable and uncolored: its lifecycle field remains `COMPLETED` only
for success and `FAILED` for failure/blocking, regardless of the requested
human-readable completion label. Do not print SUCCESS for partial work or
failed acceptance criteria.

`CLI_RESULT.md` should report the delegation and parent IDs, result, changed files, checks, new findings, the required self-healing/configuration-feedback section, decisions needed, blockers, Git staged/committed/pushed state, GitHub operations and verification, and recommended next action. Be concise.

## GUI command: “gotowe”

When a CLI handoff is pending, `gotowe` means consume its result and continue
the authorized workflow; do not ask whether to read it. Outside that context,
it follows the acknowledgement rule above. The word itself is not evidence
that checks passed or that CLI produced a result.

Read the result and confirm its delegation ID matches the task. Inspect the actual working tree for relevant changes; do not rely on the result text alone. Incorporate findings, decide whether the handoff succeeded, update the parent task as needed, mark the task `CONSUMED`, and clean the sync files only after safely preserving the result. Keep failed handoffs until reviewed.

As part of consuming a CLI result, review its self-healing section. If the
section is missing, do not consume the handoff as-is: use observed evidence to
append a clearly labeled GUI audit addendum, or request a CLI amendment when no
reliable evidence is available. Do not invent a cause or recovery. When the
section
identifies a reusable gap in agent instructions, correct the relevant
configuration and run the appropriate documentation checks before completing
consumption. Do not modify configuration for expected no-match cases or
isolated errors already covered by current rules; record that assessment in the
GUI response.

Lifecycle: `READY -> IN_PROGRESS -> COMPLETED -> CONSUMED -> cleanup`; failure: `READY -> IN_PROGRESS -> FAILED`.

## GitHub and permissions

Use `gh` for GitHub operations when available. Read-only examples include `gh auth status`, `gh repo view`, `gh issue list`, and `gh issue view <number>`. Authentication is local state: do not reauthenticate automatically or record credentials/account identity. GitHub reads and writes are separate permissions. A task must explicitly authorize GitHub writes before creating/editing/commenting on/closing Issues or PRs or changing labels/milestones. Before each write, verify the repository, exact target, and current remote state; make only the requested change and verify the result. Never guess an Issue number or create a duplicate. GitHub-write authorization does not grant Git staging, commit, or push permission.

For substantial work, use the stable planning ID (R/F/T/B-xxx) in the Issue title/body. The Issue is the detailed investigation journal; comments may record hypotheses, tests and concise sanitized evidence. Do not paste full logs. At completion, put the distilled result in one canonical `docs/tasks/<ID>-<slug>.md`, update reusable technical knowledge in `RESEARCH.md`, and finalize the Issue only if writes are authorized. Do not close an Issue before its acceptance criteria are met.

## Task finalization

Before marking a substantial task done, update the canonical task summary, reusable research if needed, decisions if semantics/architecture changed, backlog, task history, current state, and affected risk/test/architecture docs. Update CHANGELOG only for user-visible changes. Run relevant consistency checks and privacy review. Preserve partial status when gates remain open; do not turn an unfinished task into a historical completion row.

## Public-content privacy gates

Before staging, inspect every candidate change for identifying absolute paths, usernames, emails, credentials/tokens/cookies, account or device IDs, private URLs, raw logs/dumps/saves, and generated or copyrighted vanilla material. Sanitize or stop on suspicious content. Before commit, inspect the exact staged diff again, run `git diff --cached --check`, and check for unexpected generated/binary files. A later cleanup does not remove secrets from Git history. Do not stage/commit/push unless separately authorized. Existing historical privacy audit is recorded in `PRIVACY_AUDIT.md`; this workflow applies controls to new and modified content.

No custom scanner is added yet: simple pattern matching can miss context in screenshots/logs and produce false alarms, while mandatory human review remains necessary. Reconsider a small helper if repeated manual checks become error-prone; any helper supplements, rather than replaces, review of the exact diff.

## Local handoff files

`.codex-sync/` is local-only and ignored by Git. Keep `CLI_TASK.md` and `CLI_RESULT.md` concise; do not use them to store credentials, raw logs, or private machine details.
