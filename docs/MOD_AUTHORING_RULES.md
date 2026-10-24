# Mod authoring and preflight rules

Mandatory for every new or revised probe/mod and after a game-build change.
Read this document before preparation. Run the checker before installation and
again against the installed payload. These rules supplement the role and
permission boundaries in [CODEX_WORKFLOW.md](CODEX_WORKFLOW.md).

## Evidence and project conventions

- **Observed engine diagnostic:** the R-016 startup on CK3 1.20.1.1 reported
  missing UTF-8 BOMs for scripts in `common/scripted_effects`,
  `common/scripted_guis`, `common/landed_titles` and `gfx/map/map_modes`.
  The engine said it would attempt reading anyway; reaching main menu was not
  a clean startup pass. See the [checkpoint](tasks/R-016-my-dynasty-pipeline.md#first-startup--encoding-correction--2026-10-21).
- **Mandatory project convention:** all `.txt` scripts under `common/` and
  `gfx/`, including helper CoA definitions, and all localization `.yml` use
  strict UTF-8 with exactly one leading BOM (`EF BB BF`). This conservative
  convention extends beyond the four observed directories; no universal
  engine requirement is inferred from those errors. Localization also follows
  the existing project BOM convention.
- GUI `.gui` and `descriptor.mod` must be strict UTF-8. No BOM requirement for
  these categories has been observed. Do not add BOMs to arbitrary documents
  or binary assets.
- Normalize only reviewed text categories: decode strict UTF-8, remove leading
  BOM characters, prepend one BOM, and compare the remaining bytes with the
  original body. Preserve line endings and text; do not silently rewrite an
  unknown encoding. Keep original bytes in ignored local evidence.
- **Installed source evidence:** helper CoA objects belong under
  `common/coat_of_arms/coat_of_arms/`, keyed by the title identifier. Check the
  relevant installed `.info` and nearby shipped example for each subsystem;
  an old folder proposal is not authoritative. R-016 rechecked this layout and
  title fields on 1.20.1.2; successful object resolution remains a runtime gate.
- `supported_version` is a compatibility declaration. Use the exact reviewed
  build version for diagnostics; changing it never establishes compatibility.

## Required manual source review

1. Record installed version/build from launcher metadata and Steam manifest;
   identify source and generated-document provenance using the
   [source map](CK3_SOURCE_MAP.md). After updates, recheck affected dependencies
   against installed sources. Compare hashes/old bytes only when preserved;
   do not assert unchanged files from matching API names or line numbers.
2. Use original bodies and project identifiers. List every intentional native
   identifier override and its conflict/selection implications. Verify folder
   placement, schema, references, assets, helper keys and localization keys,
   including `l_<language>:` header, matching folder and filename. The checker
   does not resolve CK3 objects or check duplicate keys and script semantics.
   Every added helper landed title also needs a distinct localized title name
   and adjective; non-creatable color sources are not exempt from this review.
3. Review fresh roots, validity guards, scope transitions, traversal, write
   order and stop conditions. Exclude old NULL/SUCCESSION/LOWBORN diagnostic
   callbacks and gameplay fixture mutations unless explicitly scoped. Follow
   ADR-008/009: no decision/council/Situation/religious carriers, automatic
   world scans or unrelated alternatives. Explicitly staged manual world
   computation is distinct from automatic scanning. Never modify vanilla;
   do not package copied vanilla bodies/replacement files.
4. Preserve generated docs and previous passes with their actual build labels.
   An update requires targeted revalidation, not automatic rejection of every
   old finding or a broad repeat of completed research. Newly missing API
   contracts require fresh user-generated `script_docs`/`dump_data_types` and
   targeted review before dependent computation; CLI does not operate console
   or imply regeneration. Static source agreement is candidate readiness only.

## Required checks and installation sequence

From the repository root, replacing angle-bracket placeholders with explicit
paths and the exact reviewed version:

```sh
python3 scripts/check_mod_preflight.py <payload-root> --expected-version <version>
python3 scripts/check_mod_preflight.py <payload-root> --expected-version <version> --installed <installed-root>
```

The standard-library checker is read-only. It checks the declared text
categories, leading BOMs, UTF-8, localization header/folder/filename, required
descriptor metadata, misplaced top-level CoA folder and incidental research
files. With `--installed`, it checks the complete file inventory, exact bytes
and SHA-256 equality. Symlinks are rejected. It is not a CK3 parser, Tiger,
reference resolver, privacy scanner or API/runtime validator; unknown file
categories and engine loading precedence need manual review.

For a pinned machine-readable result, add `--json` to either command. JSON is
opt-in; the default human-readable output and exit behavior stay the same. The
versioned `mod-preflight-result/1` schema reports literal `PASS`, `FAIL`, or
`INCOMPLETE`, coverage, version/comparison states and finite finding counts. It
uses `descriptor_unavailable` when an incomplete inventory cannot establish
whether the required descriptor is present; default output retains the
historical missing-descriptor message. It contains no payload paths, descriptor contents, expected-version text or raw
errors. A complete file check still does not establish syntax, references,
engine API, load/save, RGB or user acceptance. See
[EVIDENCE_REPORT.md](EVIDENCE_REPORT.md) for the schema, adapter behavior and a
copyable pinned-report example.

1. Complete source self-review and pass offline preflight **before install**.
   Every relevant CLI handoff must name both commands, payload roots and exact
   expected version; no hidden normalization or installation in the checker.
2. Obtain the scoped installation authorization. Assume the user's declared
   game/launcher state in CLI. Preserve the exact existing probe/wrapper,
   current startup logs and enabled-mod manifest in ignored local evidence
   before mutations. Preserve prior playset selection for restoration.
3. Install only the reviewed isolated payload and wrapper; compare wrapper
   name/version/supported_version/path separately. Run post-install preflight
   and keep a per-file hash/BOM receipt. Resolve any mismatch before startup.
   CLI checks `dlc_load.json` enabled mods and resolved wrappers/payloads against
   the intended set; use bounded read-only playset/configuration evidence only
   when needed. GUI reviews the receipt without routine visual launcher checks.
   GUI configures the already open launcher only for a proven mismatch or
   unresolved ambiguity, then persisted configuration is read back. See the
   file-first verification procedure in CODEX_WORKFLOW. Startup logs below
   independently establish what the engine actually mounted.
4. User alone starts CK3 through Steam and stops at main menu. Capture a fresh
   bounded log interval and verify actual mounted mod, build, GUI warnings,
   errors and database conflicts before play, save loading or classification.
   Empty logs cover only actions actually performed. A metadata bump and a
   preflight pass never replace this startup checkpoint.
5. Stop progression on preflight failure, attributed startup errors, crash,
   unexpected helpers, wrong category/coverage, missing/reject markers or
   harmful side effects. Preserve evidence and name the unresolved gate.
   Further computation/save/load tests need their own authorized scope and
   current API review; no silent continuation from startup to classification.
6. Roll back only the scoped probe from its backup when appropriate and
   authorized, with CK3 declared closed. GUI restores prior mod selection;
   restored files/selection do not restore saved RGB or prove safe removal.
   Preserve saves. Raw logs, generated/vanilla material, machine paths and
   private identifiers stay ignored. Apply the workflow privacy gate to
   public changes; staging/commit/push/GitHub writes need explicit permission.
