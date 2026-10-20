# Contributing

## Development rules

1. Prefix new CK3 identifiers with `dynmap_`.
2. Keep `main` releasable; use short-lived branches.
3. Do not commit vanilla CK3 game files or generated `script_docs` output.
4. Add/update tests and documentation for behavior changes.
5. Run CK3 Tiger and inspect `error.log` before release-oriented PRs.
6. Do not introduce recurring global scans without profiler evidence and an ADR.
7. Any change to My Dynasty semantics requires an ADR update.
8. Any All Dynasties color-strategy change requires an ADR update and stability test.
9. Treat repository and GitHub content as public; sanitize paths, identities, logs, screenshots and credentials before staging or sharing.

See [CODEX_WORKFLOW.md](docs/CODEX_WORKFLOW.md) for task IDs, handoffs, GitHub permissions and the required pre-stage / pre-commit privacy gates.

## Commit examples

- `feat: add direct dynasty county classifier`
- `fix: guard holders without dynasty`
- `perf: classify once per county before barony coloring`
- `docs: record CK3 1.21 compatibility test`
- `research: document current sub-map-mode GUI`
