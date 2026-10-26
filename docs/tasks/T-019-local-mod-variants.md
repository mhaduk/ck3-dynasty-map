# T-019 — Consolidate local mod variants

Issue: [#45](https://github.com/mhaduk/ck3-dynasty-map/issues/45), identity verified
against the live issue and canonical registry on 2026-10-26.

Status: **COMPLETE in the user-approved DEV/cleanup scope, 2026-10-26.**
Production creation and two-installed-variant verification are explicitly moved
to T-014; this is not a claim that two variants are currently installed.

## Scope and disposition

The user requested direct execution and declared game and launcher closed.
After the missing production-package dependency was identified, the user chose
cleanup plus DEV. On 2026-10-26 the user confirmed production remains deferred
and authorized closeout, cost accounting, Wiki/issue updates, commit and push.
Production criteria transfer to T-014 rather than remaining silently incomplete.
No production source migration, version bump or gameplay change was included.

| Old launcher entry | Local descriptor/install stem | Disposition |
|---|---|---|
| Dynasty Map - Native Menu Probe | `dynmap_native_menu_probe` | Installed directory and external wrapper removed after backup |
| Dynasty Map - R005 Entry Contract Probe | `dynmap_r005_entry_contract_v1` | Installed directory and external wrapper removed after backup |
| Dynasty Map - R009 Barony Color Batch | `dynmap_r009_barony_color_batch` | Installed directory and external wrapper removed after backup |
| Dynasty Map - R016 My Dynasty Diagnostic | `dynmap_r016_my_dynasty` | Installed directory and external wrapper removed; current payload migrated to DEV |
| Dynasty Map [DEV] | `dynasty_map_dev` | Installed; version `0.0.0`, supported version `1.20.1.2` retained |
| Dynasty Map | `dynasty_map` | Reserved intended identity only; no directory, wrapper or package created |

All four old wrappers pointed to disposable local installed copies, not repository
research directories. The prior R-016 install matched the ten-file current source
exactly, including accepted T-018 palette-hoist B. Private backups preserve all
eight removed artifacts, prior manifest, a consistent launcher-database snapshot,
and available startup logs. Historical repository sources/records remain intact.

## Delivered and verified

- `prepare_dev_mod.py` prepares the DEV identity from the current source without
  rewriting its historical descriptor. Five focused tests pass, covering byte
  preservation, existing outputs, symlinks, recursive output and private metadata.
- Prepared and installed ten-file preflight both PASS. Fresh installed comparison
  confirms all nine non-descriptor files are identical to the previous payload.
  Only descriptor `name` changes; no semantic/runtime compatibility claim follows.
- External DEV wrapper matches the payload metadata and points to the distinct
  DEV install. `dlc_load.json` replaces the enabled R-016 wrapper with DEV while
  preserving other fields. Fresh file inventory finds DEV only and none of the
  four obsolete directories/wrappers.
- Launcher database was read-only throughout. Its old registrations/playset links
  were subsequently reconciled through launcher UI; see the verification below.
- [Local variant guide](../LOCAL_MOD_VARIANTS.md) establishes future DEV preparation,
  install identity, separate production ownership and activation rule.
- No vanilla files, saves, repository history or historical probe sources were
  edited or removed. No game UI/process inspection or game start/stop occurred.

## Recovery and self-review

Initial discovery referenced an absent optional directory and unmatched filename
glob. Discovery was narrowed to existing paths; no mutation occurred. A mistaken
related-issue lookup was corrected using canonical registry bindings (#40/#43).
Future related-issue reads should use registry bindings first.

Initial installation failed while creating the new DEV directory because existing
write permissions covered the retired install only. No install mutation preceded
that failure. A scoped elevated retry was approved and completed, with before/after
preflight and byte equality. Keep exact installation targets in future permissions;
do not recreate R-016 merely to reuse its old permission.

This was direct GUI execution with self-review, not an independent CLI review.
No optimization effectiveness or speedup is claimed. Saved-session usage and
partial known API-equivalent cost are independently verified below.

## Scope acceptance and deferred work

Launcher correction and fresh persisted playset readback PASS on 2026-10-26.
Production package creation, installation and separate selection are deferred to
T-014; T-017 owns release readiness. The user-approved DEV/cleanup scope is
accepted and complete, including launcher and persisted configuration checks.

Private machine-specific inventory, hashes, backup and installation receipt are
in ignored `.codex-sync/T019-CLEANUP-20261026/`.

## Launcher correction — 2026-10-26

The user supplied a screenshot of the four obsolete entries in the existing test
playset. Fresh read-only file evidence found DEV already registered as ready, while
the launcher had rewritten the enabled manifest to the missing R-016 entry. The
previous direct manifest edit was insufficient and should not be repeated: the
launcher owns persisted selection; use its UI for configuration changes.

Bound to the actual running launcher after a launcher-only executable lookup;
the ordinary lookup failed because process-list access was unavailable, and a
scoped elevated retry succeeded. No game process or window was inspected.
The CK3 identity was verified before interaction. Through launcher UI, added
DEV to the same playset and removed the four missing entries using Remove from
Playset. No unrelated selection or DLC was changed, and the playset name was
preserved. The library visibly contains DEV and the preserved unrelated mod,
without the four obsolete Dynasty entries. Final playset visibly has one enabled
mod, Dynasty Map [DEV].

Fresh read-only SQLite/manifest verification confirms DEV alone in the active
playset, DEV alone in enabled_mods, and zero old probe references across playsets.
The local launcher-verification receipt preserves the bounded result. No direct
database edit was made. No game launch or gameplay test was needed. Production
remains deferred to T-014; finite-cutoff task accounting is recorded below.

## Publication scope and validation

User-authorized closeout includes the source helper/tests, local variant guide,
current state/backlog/history/changelog, issue #45 and Wiki. The AI-Cost page now
focuses on Historical task accounting, sorts task rows by descending known cost,
and removes the unrelated T-013 introduction and T-016-specific accounting
section; their canonical records remain unchanged. No new task ID is allocated.

Checks: five focused DEV-preparation tests PASS; ten-file installed preflight
and byte equality PASS; launcher library, active playset and persisted manifest
PASS. Production installation/smoke is explicitly outside accepted scope.
Public-content privacy scan and documentation/diff checks precede staging;
exact staged content is reviewed before commit. Raw logs, screenshots, saves,
backup payloads, launcher databases and session records remain ignored.

## AI costs — verified finite cutoff

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6.1-sol | 6,513,883 | 6,349,312 | 164,571 | 18,326 | 6,532,209 | $1.14733320 |
| codex-auto-review | 43,349 | 12,032 | 31,317 | 397 | 43,746 | N/A — unpriced |
| **Total** | **6,557,232** | **6,361,344** | **195,888** | **18,723** | **6,575,955** | **$1.14733320** |

Partial measured coverage: 60 deduplicated responses from one saved GUI
session and two linked automatic-approval-review sessions; no delegated CLI
session. Independent raw-record summation agrees with the accounting helper.
Frozen cutoff: 2026-10-26T12:16:20.992Z. Later accounting, documentation, Wiki/issue
publication and commit/push are excluded. Private snapshots, source hashes and
turn assignments stay local. Automatic review is measured but codex-auto-review
has no verified public price and remains explicitly unpriced.

Standard API-equivalent pricing checked 2026-10-26: gpt-6.1-sol per million
uncached/cached/output tokens is $2/$0.10/$10, from the
[official model pricing](https://developers.openai.com/api/docs/models/gpt-6.1-sol).
Maximum measured request input is 174,238, below 272K; short-context rates
apply. Cached input is a subset of input; reasoning is included in Output.
No nonzero cache-write usage was observed. Actual service tier, regional/tool
fees and other invoice adjustments are not inferred. The total includes known
priced usage only; an unpriced component contributes no fabricated cost.
This is an approximate API equivalent, not subscription spending or an invoice.

## Publication verification — 2026-10-26

Wiki commit `cdebfec` is published; a fresh remote clone confirms all four
changed pages byte-for-byte, including the cleaned/sorted AI-Cost page.
Issue #45 is closed completed under the explicitly narrowed scope; its full
body was read back and matched exactly, including the canonical per-model
cost table. The `ai-cost-table-format` label is present. Historical task
figures remain unchanged; the registered closed-task rollup now counts 37
tasks, 1,064,778,231 measured tokens and $110.02328552 known cost ($110.02
displayed), with incomplete and unpriced coverage still explicit.

Closeout discovery encountered absent guessed accounting/wiki filenames; exact
file discovery recovered the canonical mapping and page names. No data changed
during those failed reads. Future closeouts should discover names before access.
Scoped repository commit/push is authorized; private snapshots/backup receipts
remain ignored. No game operation was part of publication.

- ai-cost-table-format: PASS
