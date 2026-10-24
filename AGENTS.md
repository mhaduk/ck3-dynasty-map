# Codex project rules

## Startup and handoffs

- Keep user-facing commentary in the language of the latest user request, including progress stage descriptions; preserve exact command names, identifiers and required receipt phrases.
- For ordinary GUI startup, read [CURRENT_STATE.md](docs/CURRENT_STATE.md), then [TASK_HISTORY.md](docs/TASK_HISTORY.md), then only the active task's relevant context. Reuse findings until inputs, build, evidence or user instructions change.
- `pobierz zadanie [ID]` picks up a READY handoff; `gotowe [ID]` reviews a completed result. For a named ID, inspect its per-ID task/status first, independently of the legacy inbox. Bare commands require a sole eligible candidate across per-ID and active legacy handoffs. Follow [CODEX_WORKFLOW.md](docs/CODEX_WORKFLOW.md); missing, inconsistent or ineligible handoffs never fall back to product tasks.
- Every GUI-to-CLI handoff message to the user must end with this five-row Markdown table, with all values filled in:

  | | Command / value |
  |---|---|
  | CLI pickup | `pobierz zadanie <ID>` |
  | GUI receipt | `gotowe <ID>` |
  | Model / reasoning level | `<recommended model> / <level>` |
  | Estimated CLI time / steps | `<calibrated range in minutes; <N> planned steps, or no plan>` |
  | szacowane tokeny/wiadomości | `<N> tokenów; <M> wiadomości` |

  Choose the model from the workflow routing guidance, state that it is a recommendation unless runtime confirms it, and estimate time from the bounded scope and known unknowns. For a successful CLI-to-GUI handoff, the user-facing completion message must contain only `SUCCESS` and `gotowe <ID>`; keep details in `CLI_RESULT.md`. Report failures or blocked work truthfully and separately.
- Before substantial work, choose GUI or CLI using the workflow routing table. Bounded research, documentation and file work default to CLI. GUI coordinates, decides and reviews. Keep one substantial backlog task per chat; do not repeat GUI research in CLI. New GitHub issue titles use `<ID> — <concise title>`; see [CODEX_WORKFLOW.md](docs/CODEX_WORKFLOW.md).
- Routing contract: GUI / Sol owns scope, criteria, architecture, material trade-offs, direction, final acceptance and next step. CLI / Luna defaults to bounded COLLECT, VERIFY, RESEARCH or approved EXECUTE work; DECIDE belongs to GUI. CLI may recommend options, completes useful authorized analysis before escalation, and returns compact evidence with provenance for targeted GUI review. Model profiles are recommendations unless the runtime confirms selection.
- As the final preparation step for useful long-running handoffs, GUI supplies a structured `execution_plan` with 1–20 major milestones before READY. Show its actual step count with the calibrated time range. Use comparable estimate/claim-to-complete pairs when available; with insufficient pairs, apply the explicitly labeled 2–3× user-observation prior and preserve uncertainty. CLI uses supplied IDs with `handoff.py progress` on meaningful starts/completions; justified amendments preserve frozen scope. After each successful meaningful transition, relay one standalone plain-text commentary from persisted `STATUS.json.progress`: `●  <parent ID> [<30-cell Unicode bar>] ~<percent>% — <human-readable stage or milestone boundary>`. Terminal output uses a green ANSI bullet when color is supported; otherwise use the same glyph uncolored. Use the parent ID, not the long execution ID. Do not relay no-ops or failed/rejected/stale commands, repeat an identical state, or guess progress; keep the last percentage during long stages. At 100%, state `CLI complete; GUI review pending`. Never invent a plan for old planless handoffs. See the workflow for commands and retry behavior.
- During normal GUI-to-CLI preparation, use the local saved-session estimate described in [GUI_CONTEXT.md](docs/GUI_CONTEXT.md). In the user-facing GUI-to-CLI handoff table, always put the saved GUI-session text estimate in the last row, immediately below `Estimated CLI time / steps`: label `szacowane tokeny/wiadomości`, value `<N> tokenów; <M> wiadomości` (example: `3709 tokenów; 12 wiadomości`). Do not show a separate estimate line above the table. Including this estimate only in CLI_TASK.md or tool output is insufficient. If saved-session measurement is unavailable, use `niedostępne` in that table cell without inventing values. Keep session text estimates separate from active context and billing. No extra model turn, context backfill, thresholds or restart recommendations. Preserve private provenance and aggregate-only per-task history; link available history below the AI-cost table at authorized closeout.
- Before closing any task, GUI verifies its cost accounting against at least one saved GUI session and zero or more CLI sessions, plus linked review counters, using a frozen completion cutoff. A CLI report without counters is not evidence for N/A; report any missing GUI-session evidence instead of inventing it. For total-cost arithmetic, N/A contributes $0; if any component has a positive USD cost, show the total in USD, never N/A. Keep component N/A values, incomplete coverage and unpriced models explicit; see CODEX_WORKFLOW.
- AI-cost updates and closeout publications must show the canonical per-model Markdown cost table in each scoped GitHub Issue/PR body and canonical task record, with a Total row and USD cost column; prose or a link alone is insufficient. Assign and verify `ai-cost-table-format`, including published-body readback; see CODEX_WORKFLOW for the exact schema and limits.
- For each material stage, report observation, cause or unknown, recovery, outcome and a useful instruction/tool improvement. Report recovered command/path/tool failures; do not hide them. See the self-healing section in CODEX_WORKFLOW.

## Project and source rules

- CK3 source discovery starts at [CK3_SOURCE_MAP.md](docs/CK3_SOURCE_MAP.md). Reuse completed target-build research unless the build changes, evidence conflicts or revalidation is requested. Verify APIs against the installed target build and generated docs.
- Before preparing/revising a probe or mod, and after build changes, read [MOD_AUTHORING_RULES.md](docs/MOD_AUTHORING_RULES.md). Run `python3 scripts/check_mod_preflight.py <payload-root> --expected-version <version>` before installation and repeat with `--installed <installed-root>` afterward. A file checker does not prove syntax, API or runtime compatibility.
- The project remains pre-implementation until research gates and an implementation task are explicit. Preserve ADR semantics. Never modify vanilla CK3 files.

## Safety and permissions

- The user alone opens the launcher/game through Steam and performs all game loading, saving, character switching and tests. Codex never opens, captures, reads or controls the CK3 game UI, or starts/stops the game. CLI assumes declared app state and never checks processes. Use source, files, logs and user observations; inspect only screenshots supplied by the user. Launcher work stays separate from the game.
- CLI verifies installed-file equality, wrapper metadata and persisted enabled-mod configuration (`dlc_load.json`; bounded read-only playset data if necessary). GUI reviews the receipt and configures the already open launcher only for an incorrect or unresolved configuration; no routine visual verification. Fresh startup logs still verify actual mounted mods/build. See CODEX_WORKFLOW.
- Reuse the existing test playset and preserve its prior selections. Installations and tests sharing one live game are sequential. Before each stage, state required app state, Codex work and the user's exact next action.
- Treat repository and GitHub content as public. Keep credentials, private paths, raw logs, saves, generated dumps and machine-specific details out of Git. Run the privacy gate before staging and inspect staged content again before commit.
- Do not stage, commit, push, publish or write to GitHub without explicit authorization. Git and GitHub permissions are separate. Do not send external messages unless explicitly instructed.
- `dalej`, `ok`, `gotowe` and `tak` authorize the clearly described next step and its necessary substeps; do not ask again. Current user instructions override old permission notes. Preserve unrelated restrictions and ask only about missing information or materially unresolved choices.
- On ambiguous macOS launcher binding, follow the running-launcher procedure in CODEX_WORKFLOW; never guess a version or infer absence from timeout.

## File handling

Establish the repository root and validate each exact path before reading or writing. Use `rg --files` to discover names; ADRs are sections in `docs/DECISIONS.md`. For `rg`, exit 1 means no matches; exit 2 means fix the command/path and report the failure. Preserve unrelated dirty work. For scoped handoffs, use `.codex-sync/`, honor per-task output ownership and stop on actual overlapping edits.
