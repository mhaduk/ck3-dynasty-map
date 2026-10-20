# Algorithms and Performance

## Key conclusion

Do **not** build a persistent graph for My Dynasty in the MVP.

The design models the ordinary vassal hierarchy as a rooted forest. Historical references describe `any_liege_or_above` as checking lieges above a character. M0 must verify target-build traversal and government behavior; shallow hierarchy depth is an assumption to measure. A persistent graph would require difficult invalidation on succession, conquest, title revocation, vassal transfer, realm split, government mechanics and scripted effects.

## Notation and required safety guards

All pseudocode is conceptual, not verified CK3 API syntax. In particular,
`capital_county(B)` means the containing county of barony B; it is not a claim
that a CK3 function with that name exists. All scope, iterator, guard, color and
profiler API candidates require M0 verification.

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

Historical references suggest global county and hierarchy iteration, including `every_in_de_jure_hierarchy` restricted to baronies. M0 must verify these operations in the installed target build before final code.

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

1. Check `holder.dynasty == player_dynasty` before traversing lieges.
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
