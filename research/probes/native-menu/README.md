# R-010 native-menu probe — FAILED / WITHDRAWN

Do not install or enable this attempt. It crashed CK3 1.20.1.1 on startup on
2026-10-20 at 13:00:31 Europe/Warsaw, before reaching the main menu.

## Result

The original narrow type-decoration hypothesis was tested once. The source used
`flowcontainer_additional_mapmodes` as both the newly declared type and base,
with an override of the native menu insertion block and one disabled DM button.
The crash report identifies stack exhaustion and tens of thousands of recursive
`CPdxGuiFactory::ResolveTypes` calls during GUI factory post-load. This strongly
supports a cyclic type-resolution cause in this probe; exact engine internals
and all alternative type/namespace strategies are not established by one test.

The user-supplied Steam output reports successful Steam library loading and
logging-category warnings; it does not explain this GUI recursion failure.
Empty error.log/gui_warnings.log at crash do not imply a successful GUI load.
Debug output confirms the probe was mounted and its GUI file was read first.

## Quarantine and recovery

- Failed original source is retained for provenance only at
  `failed/dynmap_native_menu_probe.gui.disabled`. There is no active probe GUI
  source under gui/ in this package.
- The matching machine-local installed GUI was renamed to `.gui.disabled` with
  approval. No vanilla files or launcher descriptors were changed.
- Launcher Home was switched to No mods; mod-load JSON confirms zero enabled
  mods and no disabled DLC. Recovery subsequently succeeded (user-confirmed startup and fresh no-mod logs).
- Raw crash report and launch logs are archived in ignored local/evidence;
  source SHA-256 is
  `dc572d67794fa5d17bda7100c8f282f1ba31228991414111db84ce3221e277f0`.
- The separate test playset still exists; do not use it for further runs of this
  attempt. Recovery should use No mods and confirm main-menu reachability.

No classification, map effects, title writes, world scans or new saves were
performed by the probe. No save was loaded in this failed launch. Vanilla startup recovery is now observed; full save/removal behavior remains untested.

## Gate disposition

R-010 stays open. The tested native-menu extension method failed; native-menu
integration under ADR-006 has no verified working path. Do not substitute a
vanilla GUI copy, a standalone overlay against the user's preference, or another
same-name recursion attempt. Vanilla startup recovery was confirmed; next
research a materially different original integration mechanism before any next
probe. Player guards, refresh and color-state gates remain open independently.

Only source/brace review was performed before launch; CK3 Tiger was unavailable
and not run. Such static review did not catch the engine's cyclic resolution.

Reviewed evidence: [failure and recovery record](../../../docs/evidence/2026-10-20-r010-native-menu/README.md).
