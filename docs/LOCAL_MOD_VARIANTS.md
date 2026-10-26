# Local Dynasty Map variants

The intended local identities are `Dynasty Map [DEV]` for ordinary development
and `Dynasty Map` for a reviewed production/release candidate. Display names
contain neither versions nor task IDs. Version and compatibility remain
descriptor metadata, governed by [VERSIONING.md](VERSIONING.md).

During normal development enable **Dynasty Map [DEV] only**. Enable
**Dynasty Map** only for an explicit production/release-candidate smoke test,
with DEV disabled. Preserve unrelated playset selections.

## Current development source and preparation

The current source remains `research/probes/my-dynasty-r016/mod` for provenance.
Its historical descriptor and internal identifiers are preserved. Prepare the
local DEV identity in a fresh ignored directory:

```sh
python3 scripts/prepare_dev_mod.py --output .codex-sync/dev-build/dynasty_map_dev
python3 scripts/check_mod_preflight.py .codex-sync/dev-build/dynasty_map_dev --expected-version 1.20.1.2
```

Use a new output directory for subsequent builds; the helper refuses overwrites
and changes only the descriptor name. It does not install files or operate the
launcher. Review the target version before future use; this command retains the
existing 1.20.1.2 declaration and establishes no broader compatibility.

The local install target is `<CK3-user-data>/mod/dynasty_map_dev`, with external
wrapper `<CK3-user-data>/mod/dynasty_map_dev.mod`. Copy the prepared descriptor
into that external wrapper and append one `path="<absolute-installed-DEV-root>"`
declaration. The payload descriptor remains portable, without `path` or a guessed
`remote_file_id`. Never commit the generated external wrapper.

With the game and launcher declared closed, preserve the prior install, wrapper,
selection and logs, install the reviewed payload, and run:

```sh
python3 scripts/check_mod_preflight.py .codex-sync/dev-build/dynasty_map_dev --expected-version 1.20.1.2 --installed '<absolute-installed-DEV-root>'
```

Verify the external wrapper and persisted enabled-mod configuration separately.
Existing machine-local write permissions for the retired R-016 install path do
not cover the new DEV target; use scoped authorization when required. Future
install instructions must target DEV rather than recreate a research-named
launcher entry. Follow [mod authoring rules](MOD_AUTHORING_RULES.md) for payload
changes and their startup/runtime gates.

## Production dependency

The reserved identity is `Dynasty Map`, with distinct intended install/wrapper
names `dynasty_map` and `dynasty_map.mod`. Production may only be populated from
the canonical reviewed package process owned by
[T-014 / #40](https://github.com/mhaduk/ck3-dynasty-map/issues/40).
Do not copy the current diagnostics into production or create a descriptor-only
placeholder to imply readiness. On 2026-10-26 the user explicitly deferred this
variant until T-014. There is currently **one installed canonical variant: DEV**;
production acceptance and two-installed-variant verification transfer to T-014.
T-019 is complete in the user-approved DEV/cleanup scope.

## Launcher check after T-019 cleanup

The user opens only the launcher through Steam, leaving the game closed:

1. Confirm `Dynasty Map [DEV]` appears in All installed mods.
2. Confirm Native Menu Probe, R005 Entry Contract Probe, R009 Barony Color Batch
   and R016 My Dynasty Diagnostic no longer appear as installed usable mods.
3. In the existing test playset, replace any missing retired entry with DEV and
   enable DEV only; preserve unrelated selections.
4. Report any stale entries or missing DEV registration before proceeding.

The launcher database is inspected read-only; deleting files and updating
`dlc_load.json` alone does not prove that cached registrations or playset links
have reconciled. User confirmation plus a fresh persisted configuration readback
is required. No gameplay regression is needed for this metadata-only migration.
Production selection/smoke remains deferred until T-014 supplies its package.
