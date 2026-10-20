# Algorithms and Performance

## Key conclusion

Do **not** build a persistent graph for My Dynasty in the MVP.

The design models the ordinary vassal hierarchy as a rooted forest. CK3 1.20.1.1 script_docs verifies `any_liege_or_above` with character input/targets, traversing all lieges above the character and excluding self (`triggers.log:1816–1819`; see RESEARCH.md). Government-specific runtime behavior and shallow hierarchy depth remain assumptions to test/measure. A persistent graph would require difficult invalidation on succession, conquest, title revocation, vassal transfer, realm split, government mechanics and scripted effects.

## Notation and required safety guards

All pseudocode is conceptual, not verified CK3 API syntax. In particular,
`capital_county(B)` means the containing county of barony B; it is not a claim
that a CK3 function with that name exists. The documented containing-county link
is `county`, accepting `landed_title` or `province` and returning `landed_title`.
RESEARCH.md records verified scope, iterator and color-effect signatures for
1.20.1.1; the pseudocode as a whole is not executable CK3 syntax. Guard context,
rendering lifecycle and profiler integration still need validation.

Before either algorithm, validate the local player and player Dynasty. If either
is invalid, My Dynasty is unavailable: return without classification or color
writes, never render an all-neutral substitute (ADR-008). If context becomes
invalid while active, stop using the old Dynasty and clear/restore visuals as far
as the API permits. Restoration cleanup is distinct from unavailable activation.
Missing-scope guards are correctness requirements, not micro-optimizations.

## Algorithm A — naive barony scan

Pseudo-code:

```text
for each barony B:
    C = capital_county(B)
    H = holder(C)
    classify H against player dynasty
    color B
```

Complexity:

`O(B * H)`

where:

- `B` = number of baronies;
- `H` = liege-chain depth.

This is simple but repeats the same county classification for every barony in that county.

## Algorithm B — county classify, barony propagate (preferred)

Pseudo-code:

```text
PD = local_player.dynasty

for each county C:
    H = C.holder

    if H exists and H has a valid Dynasty and H.dynasty == PD:
        color = DIRECT
    else if H exists and a qualifying de-facto liege has dynasty == PD:
        color = CONTROLLED
    else:
        color = OTHER

    for each de-jure barony below C:
        set barony color = color
```

A holder without a Dynasty must still have its liege chain checked; it is CONTROLLED if a qualifying liege shares PD, otherwise OTHER. DIRECT requires a valid matching holder Dynasty. An absent holder is guarded and classified OTHER.

CK3 1.20.1.1 script_docs verifies `every_county` and `every_barony`, both yielding `landed_title` targets, and `every_in_de_jure_hierarchy` with `landed_title` input/targets. The hierarchy iterator includes the starting title itself; recursion (`continue`) is separate from result filtering (`limit`). County-to-barony filtering and visual behavior still need validation. See RESEARCH.md for exact log locations.

Because `any_liege_or_above` excludes the holder, the separate DIRECT check is required before CONTROLLED traversal, not just an optimization. The documented chain is county title -> `holder` -> character -> `dynasty`; character -> `house` -> `house_dynasty` also exposes Dynasty identity.

The color effects accept `landed_title`: `set_title_color` supports named/RGB values; `set_color_from_title` accepts a title target but deliberately shifts the copied color slightly. One shared source therefore does not guarantee identical RGB values. Persistence, restoration, map-only isolation, performance and color leakage remain UNKNOWN; no color-strategy change is selected here.

Complexity:

`O(C * H + B)`

This computes the expensive dynasty/liege predicate once per county, then performs one color write per barony.

## Why this is better than graph caching

A cached graph needs update rules for at least:

- title holder changed;
- liege changed;
- realm split/merge;
- succession;
- conquest/peace resolution;
- title destruction/creation;
- special administrative/government transitions;
- player character/dynasty changed.

Missing one invalidation event creates a silently wrong map. The static recompute algorithm is deterministic and self-healing on every refresh.

## Update strategy

### Phase 1: recompute on demand

Hard requirement: **zero recurring world scan while the map is inactive**.

A full refresh is allowed only when the user requests the map/refresh. This makes total cost proportional to user interaction rather than game time.

### Phase 2: measure before optimizing

After M0 verifies the profiler entry point (historically `Script.Profiling.Gui`), use it to measure:

- total refresh duration;
- call counts for `any_liege_or_above`;
- time spent in county iteration;
- time spent in `set_color_from_title`;
- difference between Algorithm A and B if both are easy to prototype.

Do not add caching until the profiler shows the static refresh is materially slow.

## Execution constraints and potential micro-optimizations

1. Check `holder.dynasty == player_dynasty` separately before traversing lieges; the verified traversal excludes the holder itself.
2. Use M0-verified missing-scope guards (historical candidates: `exists` / `?=`); these remain mandatory for correctness.
3. Save repeatedly-used scopes temporarily inside one execution if supported cleanly.
4. Avoid `every_living_character` entirely.
5. Avoid daily/monthly on-actions.
6. Color only baronies; community experience reports incorrect/blue rendering when applying the color-copy effect to higher title tiers.

## All Dynasties complexity

If All Dynasties can derive a color directly from each holder's Dynasty without building a registry, it has the same desirable form:

`O(C + B)` plus color lookup.

A dynamic palette registry can become significantly more complex because it needs:

- unique Dynasty discovery;
- stable Dynasty-to-color mapping;
- collision handling;
- persistence or deterministic hashing;
- cleanup for extinct/new dynasties.

That is why color strategy is a release gate for v0.3.0.
