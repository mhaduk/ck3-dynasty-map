# Codex Workflow

This document is the detailed operating procedure. Keep [AGENTS.md](../AGENTS.md) short. The repository and all GitHub content are public; local machine state is not project documentation.

## Session startup and task scope

1. Read `AGENTS.md`, `docs/CURRENT_STATE.md`, and `docs/TASK_HISTORY.md`.
2. Identify the active stable task ID. Read its issue/definition only if needed, then load only the relevant sections of deeper docs and evidence.
3. Check Git status before editing. Preserve unrelated user changes. One substantial backlog task belongs in one chat; keep iterations of that task in the same chat.
4. For CK3 research, identify the subsystem, consult [CK3_SOURCE_MAP.md](CK3_SOURCE_MAP.md), then inspect only the recommended target-build/generated/vanilla sources. Escalate to separately authorized runtime work or bounded community discovery only when static sources leave the question unresolved. Reuse completed findings; repeat target-build research only when the build changes, evidence conflicts, or revalidation is requested.

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

Read `AGENTS.md` and `.codex-sync/CLI_TASK.md`; require `Status: READY`, then load only referenced context. Warn before starting if the active model is reliably known to differ from the recommendation. Mark the task `IN_PROGRESS`, execute only the permitted work, run requested checks, write `.codex-sync/CLI_RESULT.md`, then mark the task `COMPLETED`. If blocked or failed, record `FAILED` and preserve both files for GUI inspection.

`CLI_RESULT.md` should report the delegation and parent IDs, result, changed files, checks, new findings, decisions needed, blockers, Git staged/committed/pushed state, GitHub operations and verification, and recommended next action. Be concise.

## GUI command: “gotowe”

When a CLI handoff is pending, `gotowe` means consume its result and continue
the authorized workflow; do not ask whether to read it. Outside that context,
it follows the acknowledgement rule above. The word itself is not evidence
that checks passed or that CLI produced a result.

Read the result and confirm its delegation ID matches the task. Inspect the actual working tree for relevant changes; do not rely on the result text alone. Incorporate findings, decide whether the handoff succeeded, update the parent task as needed, mark the task `CONSUMED`, and clean the sync files only after safely preserving the result. Keep failed handoffs until reviewed.

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
