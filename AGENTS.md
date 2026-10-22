# Codex project rules

## Startup and handoffs

- For ordinary GUI startup, read [CURRENT_STATE.md](docs/CURRENT_STATE.md), then [TASK_HISTORY.md](docs/TASK_HISTORY.md), then only the active task's relevant context. Reuse findings until inputs, build, evidence or user instructions change.
- `pobierz zadanie [ID]` picks up a READY handoff; `gotowe [ID]` reviews a completed result. For a named ID, inspect its per-ID task/status first, independently of the legacy inbox. Bare commands require a sole eligible candidate across per-ID and active legacy handoffs. Follow [CODEX_WORKFLOW.md](docs/CODEX_WORKFLOW.md); missing, inconsistent or ineligible handoffs never fall back to product tasks.
- Before substantial work, choose GUI or CLI using the workflow routing table. Bounded research, documentation and file work default to CLI. GUI coordinates, decides and reviews. Keep one substantial backlog task per chat; do not repeat GUI research in CLI.
- For each material stage, report observation, cause or unknown, recovery, outcome and a useful instruction/tool improvement. Report recovered command/path/tool failures; do not hide them. See the self-healing section in CODEX_WORKFLOW.

## Project and source rules

- CK3 source discovery starts at [CK3_SOURCE_MAP.md](docs/CK3_SOURCE_MAP.md). Reuse completed target-build research unless the build changes, evidence conflicts or revalidation is requested. Verify APIs against the installed target build and generated docs.
- Before preparing/revising a probe or mod, and after build changes, read [MOD_AUTHORING_RULES.md](docs/MOD_AUTHORING_RULES.md). Run `python3 scripts/check_mod_preflight.py <payload-root> --expected-version <version>` before installation and repeat with `--installed <installed-root>` afterward. A file checker does not prove syntax, API or runtime compatibility.
- The project remains pre-implementation until research gates and an implementation task are explicit. Preserve ADR semantics. Never modify vanilla CK3 files.

## Safety and permissions

- The user alone opens the launcher/game through Steam and performs all game loading, saving, character switching and tests. Codex never opens, captures, reads or controls the CK3 game UI, or starts/stops the game. CLI assumes declared app state and never checks processes. Use source, files, logs and user observations; inspect only screenshots supplied by the user. Launcher work stays separate from the game.
- Reuse the existing test playset and preserve its prior selections. Installations and tests sharing one live game are sequential. Before each stage, state required app state, Codex work and the user's exact next action.
- Treat repository and GitHub content as public. Keep credentials, private paths, raw logs, saves, generated dumps and machine-specific details out of Git. Run the privacy gate before staging and inspect staged content again before commit.
- Do not stage, commit, push, publish or write to GitHub without explicit authorization. Git and GitHub permissions are separate. Do not send external messages unless explicitly instructed.
- `dalej`, `ok`, `gotowe` and `tak` authorize the clearly described next step and its necessary substeps; do not ask again. Current user instructions override old permission notes. Preserve unrelated restrictions and ask only about missing information or materially unresolved choices.
- On ambiguous macOS launcher binding, follow the running-launcher procedure in CODEX_WORKFLOW; never guess a version or infer absence from timeout.

## File handling

Establish the repository root and validate each exact path before reading or writing. Use `rg --files` to discover names; ADRs are sections in `docs/DECISIONS.md`. For `rg`, exit 1 means no matches; exit 2 means fix the command/path and report the failure. Preserve unrelated dirty work. For scoped handoffs, use `.codex-sync/`, honor per-task output ownership and stop on actual overlapping edits.
