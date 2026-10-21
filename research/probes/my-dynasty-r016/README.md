# R-016 — Three Dynasty views, source candidate

Research prototype for CK3 **1.20.1.2 / Steam build 26046173**, prepared,
installed and exercised on 2026-10-21. **R-016 research is closed with limits;
this is not a production release.** Fresh startup and first-execution log gates
passed; user reported ordinary switching/refresh/native-return smoke appears to
work. Grey nonmatching land failed visual acceptance. Full category coverage,
atomic context safety, shared title-color restoration and save/removal remain
unverified. Historical Holdings/sample/copy results retain their old palette
and evidence scope. Accepted definitions: [F-003](../../../docs/tasks/F-003-dynasty-subview-definitions.md).

## View definitions

One **Dynasty** entry in Additional Map Modes; while active, a separate map
banner offers exactly **Dynasty Realms**, **Dynasty Holdings**, **My Realm &
Dynasty**, in that order, with selected state, legend and manual Refresh.
Dynasty entry initially selects/recomputes Realms. A selected alternative stays
active until changed; merely reopening Additional Modes does not scan/reset it.
Each explicit subview click recomputes its own output, including return to Realms.
No CHECK/COMPUTE/DISPLAY controls are needed on the proposed ordinary path.

For fresh valid player P, Dynasty D, county holder H and all de-facto seniors S:

| View | Dark green | Otherwise light green |
|---|---|---|
| Dynasty Realms | Highest de-facto ruler has D; independent H is its own highest | H or any senior has D |
| Dynasty Holdings | H has D | Any senior has D |
| My Realm & Dynasty | H is P or P is in S | H or any senior has D |

Otherwise grey; unheld/invalid holder is grey. Invalid P/D means unavailable,
without classification/color writes. Dark has precedence. Cadet Houses compare
Dynasty. Lowborn holders still require senior checks. All constituent baronies
receive the county result, irrespective of their own baron. Occupation, de-jure
claims and tributary/suzerain links do not classify; de-jure traversal is used
only to find baronies. A player-vassal's dark subtree does not include sibling
vassals or the rest of their top ruler's realm. See
[ADR-010](../../../docs/DECISIONS.md#adr-010--three-dynasty-views-and-their-native-map-layout)
and the [independent truth table](../../../docs/TEST_PLAN.md#my-dynasty-functional-matrix).

New direct RGB: **25/105/50 dark**, **145/220/150 light**, **65/70/80 grey**.
Terrain/lighting may alter perceived colors; the legend uses matching swatches.

## Payload and entry limitations

`mod/` has nine original files. Three named mode definitions use the same native
baronies producer; these are selections, not independently stored color datasets.
The fourth, diagnostic-only mode displays the retained historical Holdings
sample palette. No native House/Dynasties definition is replaced.

Intentional native GUI type overrides: `flowcontainer_additional_mapmodes`
(existing primitive seam) and `widget_map_mode_banner` (new narrow primitive
composition). Native mode/setting rows remain; native banner headers and Faith
controls are references to native types. The custom active panel sits outside
the submode block replaced by `hud_bottom.gui`; native instance block seams are
preserved. Raid/barter omissions remain. No vanilla body/HUD file is packaged.
The overrides can conflict with other UI mods; bounded current layout/click/native-return smoke was user-reported; full
loading precedence, native parity and scale compatibility remain unverified. Prior R010
Faith smoke supports only the tested old integration, not this changed banner.

Normal entry/subview/Refresh uses fresh-root `ScriptedGui.Execute`, followed by
`SetMapMode`. Visibility checks player validity, availability queries fresh
Dynasty validity and CanChangeMapMode; effects check Dynasty again before a
world iterator/write. These are **candidate** controls. Execute returns void;
its next GUI action is not a success receipt. No success-aware atomic binding
was established, and a context race/failure can leave a stale selected output.
Character-scoped validation can run before an effect guard. No-Dynasty UI,
active-context loss/restore and transition races remain research gates. Do not
claim complete safe normal UX from staged diagnostics or static source checks.

Manual passes emit `DYNMAP_R016 WORLD_REALMS`, `WORLD_HOLDINGS` or
`WORLD_MY_REALM`, each with BEGIN/END and REJECT_NO_DYNASTY when applicable.
One root-scope dump per pass supports context review without promising counters.
Captured P/D scopes are cleared in the same call chain. There is no per-county
log flood, new-view counter claim, delayed/background pass or saved selection
cache. Shared native Baronies RGB, save serialization, exact repaint timing,
coverage and exit/removal safety remain unresolved. ADR-008/009 are unchanged;
All Dynasties is deferred within R016. This is not a production implementation.

## Separate optional diagnostics

**R016 diagnostics** toggles an explicitly labeled area in Additional Modes.
It exposes CHECK (availability hint only), COMPUTE/DISPLAY for each new view,
and retained direct/copy sample controls. COMPUTE then stop for log review before
DISPLAY provides a first-write gate with native Realms still selected; it does
not complete the ordinary UX requirement. DISPLAY never recomputes, and can
show another view's last RGB if misused. Use only the matching reviewed output.

The sample effect bodies, helper title and CoA definitions are unchanged:
Middlesex/Kent/Surrey, historical Holdings DIRECT/CONTROLLED/OTHER semantics,
green 40/190/80, orange 225/150/35, grey 65/70/80. Their separate baseline display
has the correct old legend and is never a fourth normal subview. Copy retains
existence/unheld guards and documented slight color shift. New direct views do
not depend on the copy/helper path. Three earlier empty-name load errors did
not recur in a fresh new game; neither causality nor safe persistence is proven.
No speculative helper change is included.

## Checks and recorded user-run batch

Source and installed preflight passed nine files; exact inventory/bytes/SHA-256
matched. Manual source review covered encoding/BOM, references, scope guards,
traversal and control wiring. No engine parser, Tiger or independent review was
performed. Fresh startup loaded both GUI files without error/GUI/conflict entries.
The paused-session baseline contained unrelated-attribution history/court errors;
subsequent tested compute intervals added no error/GUI/conflict bytes.

All three first-execution gates passed. User screenshots show ordered subviews,
selected state and matching legends; the user reports ordinary selection,
Refresh and native return appear to work. Five final complete execution pairs
support repeated dispatch, not exact per-control action attribution or complete
semantic coverage. Neutral continental land was not clearly grey: failed visual
acceptance. No profiler result, active-context safety or removal/restore proof.

Read-only preflight commands for a future separately scoped revision:

```sh
python3 scripts/check_mod_preflight.py research/probes/my-dynasty-r016/mod --expected-version 1.20.1.2
python3 scripts/check_mod_preflight.py research/probes/my-dynasty-r016/mod --expected-version 1.20.1.2 --installed <installed-r016-root>
```

These are file checks, not CK3 syntax/API/runtime validation. Future installs
must preserve payload/wrapper/logs/prior selection, verify wrapper metadata and
pass a user-run fresh startup gate under MOD_AUTHORING_RULES. No new launch or
save test is requested by this closed research record. Codex never operates or
inspects the game UI; user supplies observations. R-017 selects better fixtures;
F-001 owns grey/contrast/final UI and F-002 color-source strategy. See the
[R-016 final disposition](../../../docs/tasks/R-016-my-dynasty-pipeline.md#final-disposition--2026-10-21).
