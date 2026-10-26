# R-009 — Validate current title-color renderer safety for beta

Status: **OPEN / P0 release-safety research**  
Target: **CK3 1.20.1.2, current `Dynasty Map [DEV]` runtime**  
Issue: [#9](https://github.com/mhaduk/ck3-dynasty-map/issues/9)  
Updated: **2026-10-26**

## Current disposition

The current accepted Dynasty Map renderer is the baseline for this task. It already renders all three Dynasty views by calling `set_title_color` on constituent baronies.

R-009 is no longer a search for a renderer. Its single purpose is to determine whether the current direct-title-RGB renderer can meet the lifecycle and persistence safety required for `0.1.0-beta.1`, and to make the smallest necessary correction if a supported mechanism exists.

Do **not** reopen broad renderer research unless the current renderer is first shown unable to satisfy the beta safety gate.

Historical R-009 investigations remain evidence in Git history and under `research/probes/barony-color-batch/`; they are not active next steps.

## Current baseline

The accepted implementation:

- runs on CK3 1.20.1.2;
- is installed as `Dynasty Map [DEV]` after T-019;
- renders Dynasty Realms, Dynasty Holdings and My Realm & Dynasty;
- directly mutates title RGB through `set_title_color` on tier-barony titles;
- has accepted semantics and visuals;
- has no demonstrated automatic restore of arbitrary pre-existing title RGB.

The current `operation_cleanup` clears saved scopes and diagnostic/audit state. It does **not** restore title RGB and must not be treated as renderer cleanup.

Do not recreate the removed local launcher entry `Dynasty Map - R009 Barony Color Batch`. Validation should use the current DEV path unless a tiny disposable fixture is strictly required to discriminate one engine behavior.

## Established evidence

Previous R-009 work already established the following for the tested title-color path:

- direct RGB, named-color and `set_color_from_title` writes visibly change tested baronies;
- native and tested custom barony views observe the changed shared title state;
- changing map mode did not automatically restore the original state;
- the tested observer transition did not automatically restore it;
- designated BEFORE/AFTER save comparison found explicit title RGB overrides in AFTER that were absent in BEFORE;
- known-definition reset restores a known static value but does not prove restoration of an arbitrary live original.

Therefore do not spend execution time reconfirming that `set_title_color` works or that title RGB can serialize.

## Single decision question

**Can the current direct-title-RGB renderer be made acceptably safe for `0.1.0-beta.1`, including exit/context loss, save/load and mod-disable/removal behavior, without reopening broad renderer research?**

Use this decision order and stop at the first supported answer:

1. **Native/default reset** — determine whether CK3 exposes a supported operation that returns a title to its normal/native color state without requiring the prior RGB value.
2. **Capture + restore** — if not, determine whether the actual current title color can be captured before the first Dynasty Map mutation and restored later with sufficient fidelity.
3. **Harmless persistence** — if exact restoration is unavailable, determine whether remaining persisted state is demonstrably harmless under the supported beta workflow.
4. **Renderer blocked** — if none of the above meets T-017, record the exact blocker and stop. Do not automatically start replacement-renderer research inside R-009.

## Lifecycle contract to establish

The final result must define what happens at each boundary:

| Boundary | Required answer |
|---|---|
| Native map -> Dynasty Map | When is original/native state captured or otherwise protected? |
| Switch among three Dynasty views | Can repainting accumulate stale or unrecoverable state? |
| Refresh/recompute | Is repeated execution idempotent with respect to restoration state? |
| Dynasty Map -> native/non-Dynasty map | What restores or neutralizes the temporary RGB? |
| Player/Dynasty context loss while active | What happens to already-painted RGB? |
| Save while Dynasty Map is painted | What RGB state is serialized? |
| Reload that save with mod enabled | Is the expected safe state recovered? |
| Reload with mod disabled/removed | Does any harmful/materially incorrect persistent state remain? |

R-005 owns detection of invalid player/Dynasty context and prevention of unsafe dispatch. R-009 owns restoration/cleanup of RGB that has already been mutated when such context is lost.

## Removal-safety constraint

If temporary Dynasty Map RGB is serialized and the mod is subsequently disabled or removed, the mod cannot rely on a later uninstall callback to repair the save because its code is no longer running.

Accordingly, the beta contract must not depend solely on cleanup that occurs only after a future Dynasty Map action. A save created while Dynasty Map is active must not leave temporary RGB as a known harmful state that becomes unrecoverable when the mod is absent.

## Minimum execution plan

1. Inspect only the already-mapped CK3 effect/data surface needed to decide whether native/default reset exists or current title color is readable/capturable.
2. Select the smallest supported restoration contract. Avoid broad source scans and alternate-renderer archaeology.
3. If a viable mechanism exists, implement the smallest bounded change in the current DEV renderer rather than a parallel architecture.
4. Validate representative known titles through `native -> Dynasty paint -> leave Dynasty Map -> native comparison`.
5. Validate repeated entry, switching and refresh for stale/cumulative state.
6. Validate the context-loss boundary against the R-005 contract.
7. Perform a bounded save/load test because title RGB serialization is already established.
8. Perform a fresh-process load with the mod disabled/removed if needed to decide whether persisted state is harmless or release-blocking.
9. Record exact observations and limits. Do not extrapolate a small fixed-target sample into unsupported universal claims.
10. Stop as soon as the current renderer is either **SAFE FOR BETA** or **CURRENT RENDERER BLOCKED**.

## Preferred production-path validation

Use `Dynasty Map [DEV]` rather than recreating the historical R-009 probe.

The minimum practical sequence should cover:

```text
native map state
-> enter Dynasty Realms
-> switch Dynasty Holdings
-> switch My Realm & Dynasty
-> refresh/recompute
-> return to native map
-> compare representative title state
-> save/load as required by the discovered contract
-> disabled/removed-mod fresh-process load if required for the release decision
```

A smaller fixed-target diagnostic is acceptable only when it directly answers one unresolved engine capability and avoids disturbing the current renderer unnecessarily.

## Acceptance criteria

R-009 may close **PASS** only when bounded evidence supports all release-critical points:

- [ ] the rendering state modified by Dynasty Map is explicitly identified;
- [ ] leaving Dynasty Map has a defined safe title-color outcome;
- [ ] repeated activation/switch/refresh does not create harmful cumulative or stale RGB state;
- [ ] context loss has a defined cleanup/restoration outcome compatible with R-005;
- [ ] save/load behavior is understood and tested sufficiently for the beta contract;
- [ ] disabling/removing the mod does not leave a known damaging or materially incorrect persistent state;
- [ ] any remaining persistence is demonstrated harmless rather than merely undocumented;
- [ ] validation uses the current DEV production path, not only a historical two-barony probe;
- [ ] no new project-attributable parser/GUI/log-spam failure is introduced during the bounded validation;
- [ ] evidence limits and untested coverage are stated explicitly.

## Blocked outcome

If the current renderer cannot meet the release gate, close/stop R-009 with:

**CURRENT RENDERER BLOCKED**

and record:

- the exact missing capability or harmful lifecycle behavior;
- the smallest observation that proves the blocker;
- why capture/reset/harmless-persistence routes are insufficient;
- the smallest architectural decision that must follow.

Do not continue automatically into Situations, dummy titles, Decisions, council selectors, generic shaders or another renderer family. A replacement-renderer investigation should be a separate explicitly authorized issue if needed.

## Release rule

For `0.1.0-beta.1`:

- safe exit/context-loss behavior is required;
- save/load behavior must be understood;
- disabling/removing the mod must not leave a known harmful persistent state;
- documentation of unknown harm is not a pass.

This aligns R-009 with the T-017 release gate. Safe removal is a beta concern, not something automatically deferred to `1.0`.

## Ownership

R-009 owns:

- title-RGB mutation isolation/restoration;
- lifecycle cleanup of already-painted state;
- persistence/save/load/removal safety of the renderer.

Related owners:

- R-005 — valid current player/Dynasty dispatch and context-loss detection;
- F-001/F-005 — normal UI/product behavior and release-minimum functional smoke;
- F-002 — Dynasty accent/palette selection;
- T-014 — production source/package/Workshop preparation;
- T-017 — final `0.1.0-beta.1` readiness decision.

## Non-goals

Unless the current renderer is first proven blocked, R-009 does not include:

- Situation architecture;
- Decisions/council/title-selector rendering;
- dummy-title carrier design;
- generic shader/provider exploration;
- All Dynasties;
- palette redesign;
- performance optimization;
- broad compatibility testing;
- recreation of historical probe launcher entries.

## Evidence references

- [Issue #9](https://github.com/mhaduk/ck3-dynasty-map/issues/9)
- [Historical R-009 probe](../../research/probes/barony-color-batch/README.md)
- [R-016 current renderer research](R-016-my-dynasty-pipeline.md)
- [T-019 local DEV cleanup](T-019-local-mod-variants.md)
- [T-017 release gate](https://github.com/mhaduk/ck3-dynasty-map/issues/43)

## Success criterion

R-009 ends in exactly one actionable state:

**SAFE FOR BETA** — the current renderer has a supported, boundedly validated lifecycle/persistence contract compatible with T-017.

or

**CURRENT RENDERER BLOCKED** — the precise safety gap is documented and the smallest follow-up architectural decision is identified.

Anything between those states remains a release blocker.