# Codex project rules

**CLI pickup precedence:** when the user invokes `pobierz zadanie`, treat the
command as a handoff pickup, not ordinary session startup. Read this file and
`.codex-sync/CLI_TASK.md` first. If its status is `READY`, its delegation ID
and parent task ID define the work; they take precedence over stale or
historical task status in `CURRENT_STATE.md` and `TASK_HISTORY.md`. Do not
select a different task or stop at a closed task listed in those documents.
Then read only the handoff's referenced context, mark it `IN_PROGRESS`, and
execute its scope. If the handoff is absent, not `READY`, or inconsistent,
report that exact condition instead of falling back to another task. For
ordinary GUI startup without a pickup command, follow the normal state/history
sequence below and honor the latest explicit user task selection over stale
state text.

Read [CURRENT_STATE.md](docs/CURRENT_STATE.md), then [TASK_HISTORY.md](docs/TASK_HISTORY.md). Read the active task and only the deeper project documents it needs. Reuse completed findings; do not repeat target-build research unless the build changes, evidence conflicts, or revalidation is requested.

Before opening or reading a path, establish the repository root and validate the exact path exists and is readable; validate directories before listing them and output paths before writing. For required inputs, report a missing/unreadable path before proceeding. For optional inputs, skip them explicitly. Use the full path from the repository root (including hidden parent directories such as `.codex-sync/`); use `List` only on directories and `Read` on exact file paths. Do not assume wildcard patterns match: discover candidates with `rg --files` or check the exact path first. ADRs are sections in `docs/DECISIONS.md`, not separate `docs/ADR-*.md` files. Handle expected no-match search results separately from actual command failures. For `rg`, exit 1 means no matches and exit 2 means a command/path/regex error; inspect stderr and correct the smallest failing step before continuing. Quote search patterns and paths, prefer literal `-F` searches for identifiers, and avoid chaining reads or searches with `&&` when an expected no-match can stop the chain.

**Self-healing and configuration feedback:** if an agent encounters an unexpected
tool, path, command, or workflow problem, it must report it in the task result,
including the sanitized operation, error/exit code, root cause if known,
recovery, and whether work continued. It may correct and retry its own step only
within the granted scope. The GUI reviews reported problems and updates agent
configuration when the instructions caused or failed to prevent a recurrence;
agents must not silently suppress problems or modify `AGENTS.md`/
`CODEX_WORKFLOW.md` unless that configuration edit is explicitly assigned.
Before marking a CLI handoff `COMPLETED`, verify `CLI_RESULT.md` contains the
required self-healing section; write `None` only after reviewing the run for
errors. An omitted section is a completion-gate failure, not an implicit
“nothing happened.”

For CK3 source discovery, start with the [source map](docs/CK3_SOURCE_MAP.md) and open only its recommended target-build sources before broad installation or web searches.

Before preparing or revising any probe/mod, and after game-build changes, read [MOD_AUTHORING_RULES.md](docs/MOD_AUTHORING_RULES.md). Run `python3 scripts/check_mod_preflight.py <payload-root> --expected-version <version>` before installation and repeat with `--installed <installed-root>` afterward. Every relevant CLI handoff must name these commands, roots and exact expected version. Complete the manual checklist and user-run startup/log gate; the checker does not validate CK3 syntax, APIs or runtime compatibility.

Keep one substantial backlog task per chat. Preserve stable task IDs and update the state/index when work materially changes. Use [CODEX_WORKFLOW.md](docs/CODEX_WORKFLOW.md) for GUI/CLI handoff, model choice, task finalization, GitHub permissions, and privacy gates. For a scoped delegated CLI task, use `.codex-sync/` and avoid overlapping edits.

Before substantial work, choose GUI or CLI explicitly. Default to CLI for bounded source preparation, documentation updates and mechanical work once the design and acceptance criteria are clear, even if GUI performed the preceding research. Prepare the handoff instead of doing the delegated work in GUI. Keep GUI for coordination, unresolved reasoning and result review; small direct edits are allowed when handoff overhead would exceed the work. State a concrete reason when retaining substantial CLI-suitable work in GUI. See the workflow routing rules.

Role split: CLI executes bounded code/file/install/log tasks without waiting for user actions. It MUST assume the declared game/launcher state is correct: no ps/pgrep, process enumeration, Activity Monitor, GUI inspection or state-confirmation gate. The user prepares that state before invoking CLI; GUI may check prerequisites before handoff without inspecting the game UI. Do not fail or escalate merely to verify declared app state. Report only actual task/tool failures. Codex GUI coordinates, reviews results/logs, configures the already open launcher and mod installations, and gives concise CK3 test instructions. Codex never opens, screenshots, inspects, clicks, controls, starts or stops the CK3 game UI. The user alone opens launcher/game through Steam and performs all in-game loading, saving, character switching, option selection and tests. Reuse the existing test playset by default and preserve its prior mod selection. Before each stage state required app state, Codex work and the user's exact next steps. See CODEX_WORKFLOW.md.

Launcher identification: multiple macOS launcher versions share the same name/bundle ID. On ambiguous binding or timeout, GUI follows the [running-launcher procedure](docs/CODEX_WORKFLOW.md#identify-the-already-running-launcher-on-macos): resolve the running main executable and bind its exact app path; never guess a version or infer absence from a timeout. This does not authorize CLI state checks or launcher/game launch.

Treat `dalej`, `ok`, `gotowe` and `tak` as authorization to continue the clearly described next step and its necessary substeps; do not ask the same permission again. If that step explicitly includes installation, launch or a new test, the acknowledgement authorizes those actions and supersedes an earlier restriction for that stated scope. Complete preparation, source review and documentation together. Preserve unrelated restrictions; ask only for genuinely missing information, an unresolved material ambiguity or an action outside the accepted scope. Current user instructions take precedence over older permission notes in project documents. See CODEX_WORKFLOW.md for handoff and permission details.

Use Luna / Medium for well-specified routine CLI work; Luna / Low for trivial mechanical work; Sol / High for difficult CK3 research/debugging; Sol / Medium for independent review. Model choice follows reasoning difficulty, not file count.

Treat all persistent repository and GitHub content as public. Run the privacy gate before staging and inspect staged content again before committing. Do not stage, commit, push, publish, or perform GitHub writes without explicit authorization. Never modify vanilla CK3 files. Keep generated dumps, raw logs, saves, local paths, and machine-specific references out of Git.

The project remains pre-implementation until research prerequisites and an implementation task are explicit. Preserve ADR semantics and verify CK3 APIs against the installed target build and generated documentation. Do not claim game or tooling validation that was not performed.
