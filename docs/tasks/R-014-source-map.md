# R-014 — CK3 source map and research order

Status: COMPLETE
Target: CK3 1.20.1.1 (Crozier)
Completed: 2026-10-21
Issue: [#14](https://github.com/mhaduk/ck3-dynasty-map/issues/14)

## Result

Created the concise searchable [CK3 source map](../CK3_SOURCE_MAP.md), then
integrated its lookup order in [AGENTS.md](../../AGENTS.md) and
[CODEX_WORKFLOW.md](../CODEX_WORKFLOW.md). The map distinguishes generated API
contracts, shipped schema, vanilla usage, bounded runtime evidence and
secondary discovery material. It covers project-specific scopes, map modes,
GUI, lifecycle, localization, loading, debugging and tooling.

## Target-build inventory

Reused R-004's clean generation from 2026-10-20; no output was regenerated.
Actual `script_docs` outputs include `effects.log`, `triggers.log`,
`event_targets.log`, `event_scopes.log`, `modifiers.log`, `on_actions.log`,
`custom_localization.log` and additional logs. The actual data-types directory
contains five nonempty text outputs: `data_types_common.txt`,
`data_types_gui.txt`, `data_types_internalclausewitzgui.txt`,
`data_types_script.txt` and `data_types_uncategorized.txt`. Both output families
are build-specific static references. They document signatures, scope/type
links and exposed functions, but are not complete semantic specifications and
do not prove engine rendering or lifecycle behavior. Raw output remains local.

Shipped `.info` files are documented as target-build schema/reference files;
the map points to focused title, Dynasty/House, Situation, province-effect and
scripted-widget examples. Vanilla definitions/scripts/GUI are treated
separately as evidence of shipped composition and caller context. R-009's
renderer input, view isolation and cleanup remain **UNKNOWN** and **PARTIAL**.

## External-source assessment

- The canonical CK3 Paradox Wiki and its scripting, scope, trigger, effect,
  interface, mod-structure, localization, troubleshooting, console and map
  pages are indexed. Direct page reads returned 401 in the research fetcher;
  accessible mirror pages identify old verification notices for Scopes (1.1),
  Mod structure (1.1) and Localization (1.4). Per-page status varies and should
  be checked on the canonical page when accessible.
- `jesec/ck3-modding-wiki` is a searchable Markdown mirror. Its README claims
  daily synchronization; this was recorded as a repository claim, not
  independently verified coverage or build currency.
- `my-mods/awesome-ck3`, Wiki-linked Discord and Paradox User Mods forums are
  classified as community discovery. A bounded discussion sample recommends
  reading vanilla with the Wiki and reports gaps in public documentation; it
  is not technical authority. No Discord content was accessed.
- `CK3-Modding/Documentation` is archived (GitHub archive date 2023-06-21) and
  historical. `nonniks/CK3_Documentation` is an optional derived discovery
  corpus with a visible README build date of 2025-11-24, not target-build
  authority.
- Tiger is classified as an external validator, not API documentation or
  runtime proof. Its README notes false positives and patch lag; R-012 owns
  local setup and no Tiger run occurred.

## Validation and limits

- Source map: 222 lines; local Markdown links resolved (2/2).
- Public-content review of the new and changed text found no private paths,
  emails, credentials or identifiers. Existing unrelated SHA-256/revision
  strings in `RESEARCH.md` were unchanged. No generated dumps, raw logs, saves,
  external document copies or binary files were added.
- `git diff --check` passed. Static consistency and link checks only; no game,
  parser, Tiger or runtime validation was performed.
- Inventory and review performed no publication operations. The user subsequently
  authorized staging, commit, push to the existing research branch, and updating
  and closing #14 after publication verification.

## Next

R-009 remains partial/open. The local R-009 checkpoint commit is already present; remote publication status
was not revalidated here. Resume renderer-input and lifecycle research in its
existing chat using the source map. No R-009 probe or architecture change is
authorized by this result.
