# R-009 — Barony color batch

Status: first broad user-run batch completed; R-009 PARTIAL, 2026-10-20.
Target: CK3 1.20.1.1 (Crozier). Isolated research mod, not the Dynasty Map
implementation. Installed and byte-verified before the session; left installed
but disabled after GUI restored prior selection. No Tiger or independent review.

Direct/named/copy writes visibly worked; native and custom barony views share
changed title state. Mode exit and reported observer retained colors; same-process
AFTER reload did too. Subsequent read-only designated save inspection proves
explicit title RGB serialization, with different A/B values. Definition resets
made both red but did not capture/restore arbitrary originals. Fresh-process/
disabled-mod behavior and automatic cleanup remain unverified.

All four sources are search-visible with CoA errors; cyan lacks a capital (C04
skipped); two files lack BOM. Creatability is user-reported but unverified; no
title creation tested. Observer C09 has no new receipt, C10 skipped. Court-scene
errors remain, GUI warnings empty. No whole-run-clean/inertness claim.

[BATCH_TEST.md](BATCH_TEST.md) records actual execution, skips and open gates;
it is not an instruction to repeat the batch. The next research task is R-014's
documentation-source inventory in a separate chat. R-009 resumes afterward to
revisit renderer input and lifecycle questions using that source map. The
generic renderer connection remains unverified; Situation is a documented
specialized consumer, not an approved workaround. No new launch/repair requested.
See the [canonical R-009 checkpoint](../../../docs/tasks/R-009-barony-color-safety.md).
Multiplayer is unsupported.

## Boundaries and payload

- Only `b_london` (A, province 1527) and `b_southwark` (B, province 1526) receive
  color effects. `b_woxbrigge` (province 1528) and `c_middlesex` are controls.
- Four original, unheld duchy definitions supply magenta, cyan, yellow and the
  definition baseline. No holder/history/province, title creation/grant, Dynasty
  mutation, classifier, iterator, saved counter or startup effect is added.
- All fixture definitions set normal and partition creation guards to false. Cyan also uses
  `landless = yes` / `allow_domicile = no`; yellow/baseline use
  `no_automatic_claims = yes` / `de_jure_drift_disabled = yes`. These flags
  constrain definitions; they do not establish inertness. No title is hidden by
  an invented API. Search visibility is now confirmed;
  creation/partition restrictions and unexpected later holder behavior remain
  unverified.
  Different colors make the variants distinguishable, not a controlled test of
  each flag in isolation. Do not create or grant them to test their restrictions.
- The additive startup widget has no native-menu override or dependency on an
  existing probe. C00–C08/C11 use fresh explicit player roots, hidden/disabled
  without a valid player, and effect-level Dynasty guards. C09/C10 explicitly
  root a known title; they never dispatch into an absent character root.
- The panel is visible only under `IsInGame`; all color buttons are manual.
  C00 arms title-root buttons as a GUI receipt,
  not proof of script success. C09 must be confirmed in logs before C10. No
  automatic invalid-context effect, recurring watcher or color cleanup runs.
- M01 selects native `baronies`; M02 selects the original minimal custom
  `dynmap_r009_baronies`; A01 selects `dynmap_r009_baronies_filled`, a distinct
  original filled candidate loaded alongside it in the same launch. User-run
  observations support loading/selecting both custom definitions and their
  reported fill; broad schema/default behavior remains unverified. Renderer
  buttons never write colors. Native HUD controls remain
  available if the panel/custom mode fails. HIDE only hides the panel.
- English localization defines fixture names and the custom mode. Raw diagnostic
  labels are English. Other languages/UI scales have not been tested.

Installable source roots are `common/`, `gfx/`, `gui/`, `localization/` and
`descriptor.mod`. The first installation/run used the existing test playset,
preserved prior selection and archived logs locally.
Do not install `alternatives/` as an active source root. The first install was
byte-verified; no new installation or source repair is part of this research stage.

## Capability matrix

This table describes the payload capabilities originally prepared. Actual
executed/skipped/untested state is in [BATCH_TEST.md](BATCH_TEST.md); execution,
visual results and persistence are distinct evidence.

| ID | Coverage / writes | Dependency and failure isolation |
|---|---|---|
| C00 | Inspect eight fixed title keys, existence and holder presence; no writes | Valid player/Dynasty; missing target skips its dependent cases; held source skips that source |
| C01 | Direct RGB magenta `{ 240 25 200 }` to A | No dummy dependency |
| C02 | Named `dynmap_r009_magenta`, same RGB, to A | Named-color registration; compare to C01 at unchanged zoom |
| C03 | Copy standard magenta dummy to A; repeat the same button | Source must exist and be unheld; original plan three invocations; actual five |
| C04 | Copy landless cyan dummy to A | Independent cyan source guard |
| C05 | Copy guarded yellow dummy to A | Independent yellow source guard |
| C06 | Copy same magenta dummy separately to A and B | Per-target guards; observe equality/drift, not assumed identical RGB |
| C07 | Copy current A to B, a second copy in the chain after C03 | Both baronies exist; A remains unchanged; no copy into a duchy |
| C08 | Copy baseline dummy to A/B | Approximate definition reset, with documented copy drift; valid player/Dynasty |
| C09 | Title-root read-only dispatch receipt | New `scope = landed_title` / known-title root combination, grounded in exposed types; verify before C10 |
| C10 | Title-root direct `{ 230 5 5 }` to A/B | Manual definition reset; independent of player/Dynasty, not automatic or a captured-original restore |
| C11 | Same direct definition reset via fresh valid player/Dynasty | Fallback when C09/C10 fails; no title-root dependency |
| M01 | Native baronies / baseline observation | Available independently of M02 |
| M02 | Minimal original custom baronies definition | May fail registration or render unfilled; return to M01/Realms and continue color cases |
| L01 | Compare Realms, Counties, Houses, Faith; leave/re-enter and repeat activation | Manual observation; no restoration hook is installed |
| L02 | Context loss with a known color active; optional manual C09/C10 while observer | Tests only new color persistence/cleanup; no R-005 fixture or guard replay |
| S01 | Save active, reload in the same launch, inspect before clicking; then continue operation | Separate untouched BEFORE and mutated AFTER saves; distinguishes loading from disabling |
| D01 | Fixture search/title-window visibility, normal/partition creation restrictions and holder checks | No creation/grant/ownership changes; partition guard is static unless an independent safe observation exists |
| A01 | Independent original filled custom mode, loaded alongside M02 | Same-launch comparison observed; exact intensity unmeasured. Disabled alternative is reference only; never install a duplicate |
| S02 | Load mutated AFTER save with probe disabled | Separate later launch; never inferred from S01 |
| X01 | Exact live-original RGB capture and reset / automatic exit or context-loss color restore | Blocked: no supported capture/reset path identified; no guessed automatic writes |
| X02 | `reset_title_color`, using `reset_title_name` or `reset_coa` as color reset | Static-rejected: no documented color-reset signature; the latter effects reset names/arms, not color |
| X03 | Copy live original into a dummy duchy as a snapshot | Not shipped: copy drift prevents exact capture and would introduce higher-tier color writes contrary to the barony-only safety boundary |

C01→C02 compares the same intended value. C03→C06→C07 separates repeated
copy, shared source and one extra chain hop. C04/C05 have distinct colors for
source identification. Neither visible similarity nor `AFTER_EFFECT` measures
exact RGB; no getter was found for that purpose.

## Evidence and hypotheses

Existing evidence is reused from [RESEARCH.md](../../../docs/RESEARCH.md#title-color-effects--r-009--rg-state-01),
R-002/R-003/R-004 and R-005 FINAL GUARDS. New focused static inspection used
local generated output and installed vanilla; no external research or target
regeneration was needed. Paths below are relative to game or generated logs.

| Evidence | What it supports / limitation |
|---|---|
| `effects.log:12761–12767,12646–12649` | Landed-title RGB/named write and copying with slight shift; later visible write/save results recorded above |
| `effects.log:554–556`; `triggers.log:600–602` | Debug markers and existence guard; markers do not prove renderer success |
| `common/landed_titles/00_landed_titles.txt:2330–2373` | Target/control identity, provinces, both target definition colors `{ 230 5 5 }`; not live-original values |
| `common/landed_titles/_landed_titles.info:34–61,103–109,152–157,225–237` | Color/landless/domicile/claim/drift and separate partition creation fields; inertness remains unknown |
| `common/landed_titles/00_landed_titles.txt:78926–78956` | Native normal-creation false guards; not a guarantee against forced script granting |
| `common/named_colors/default_colors.txt:1–24`; `culture_colors.txt:1–15` | Named-color registry `colors` structure and RGB entries; combined with generated named-color support grounds C02 |
| `data_types_uncategorized.txt:673–675,113889–113891,114825–114827`; `data_types_script.txt:4147–4149` | GetTitleByKey → Title, Title.MakeScope → Scope, validity and SetRoot → TopScope. C09/C10 combined these in a new title-root path; C09 later received only with valid player, C10 skipped |
| `gui/window_title.gui:289`; `common/scripted_guis/pam_scripted_guis.txt:55–65` | Title-root GuiScope construction exists for a breakdown; scripted GUI supports non-character scopes. Neither example proves title-root Execute works |
| `gui/debug/window_component_library.gui:719–727` | Native `IsInGame` visibility gate; the panel uses it to exclude frontend operation, not to prove title-root safety |
| `localization/english/map/map_modes_l_english.yml:4–5` | Native mode name/description localization keys; the custom keys follow that observed shape |
| `data_types_common.txt:1949–1995` | GUI-local receipt/show-hide keys. They are not saved title state or a cleanup mechanism |
| `gfx/map/map_modes/map_modes.txt:1–6,109–201`; R-002 summary | Native barony mode/fields, near step 2 and filled mid step 9. Minimal custom omissions remain a hypothesis; A01 authors its own gradients |
| `research/probes/player-entry-contract/` | Tested additive widget registration, manual fresh player roots and no-player control hiding. The R009 package subsequently loaded in the first batch |

Focused searches of generated effects/event-targets and the exposed `Title`
type identified no title-color getter, exact snapshot or reset-color API. This
is a bounded negative finding, not proof that no engine solution exists.
`TitleCustomizationWindow.GetMapColor` is window state, not a demonstrated
arbitrary title-color capture/restore interface; it is not used here.

## Restoration limits

C08 resets toward a dummy initialized from the static definition and introduces
copy drift. C10/C11 directly set that definition RGB, avoiding copy drift for
that write, but cannot recover a customized or previously mutated live original.
No label says RESTORED. A visual match in the disposable baseline would only
support a bounded definition reset for these targets. No automatic mode-exit or
context-loss write is installed, because no supported exact-original capture path was established.

The original rollback proposal was loading untouched BEFORE or starting a fresh
disposable session. BEFORE was loaded after resets, so effective rollback from
marked state was not demonstrated; do not overwrite real saves or
claim disabling the mod reverses changes. Preserve the mutated AFTER save for
the separate S02 launch. ADR-008 and the production restoration gate stay open.

## Source review

Preparation includes delimiter/reference checks, target/write-boundary review,
API cross-check, documentation consistency and privacy inspection. These are
lightweight static checks, not CK3 parsing, Tiger, independent review or runtime
passes. Actual check results are in the R-009 checkpoint and local CLI result.

## GUI source review adjustment

The parent reviewed the actual package and moved A01 into the active mode file
under a distinct key, adding its own selector and localization. Both custom
variants were subsequently observed in the first launch. The disabled alternative is
reference only; it must not be installed as a second definition. That was static
source review; subsequent bounded runtime results are recorded above. S02 remains untested and would need a separately scoped launch.
