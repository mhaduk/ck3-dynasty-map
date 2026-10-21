# F-003 — Dynasty subview behavior and category roles

Issue: [#22](https://github.com/mhaduk/ck3-dynasty-map/issues/22).

Status: COMPLETE — accepted behavior and semantic category-role reference,
updated 2026-10-21. This document defines what each subview means, how the
subviews are selected, and what result role a county receives. It does not
specify colors, palette values, color sources, layout, or visual acceptance.

## Menu and selection behavior

| Menu item | Role | Selection behavior |
|---|---|---|
| **Dynasty** | One top-level entry in the map menu | Opens the default **Dynasty Realms** subview |
| **Dynasty Realms** | First/default subview | Direct selection recomputes this view's result |
| **Dynasty Holdings** | Second subview | Direct selection recomputes this view's result |
| **My Realm & Dynasty** | Third subview | Direct selection recomputes this view's result |
| **Refresh** | Explicit recomputation action | Recomputes the currently selected subview from fresh player/Dynasty context |
| **Active indicator and legend** | Identifies the selected subview and its result-role meanings | The legend follows the active subview; F-001 owns its presentation |
| Native map mode | Ordinary native mode | Leaving Dynasty returns to native map behavior; re-entering Dynasty starts at Dynasty Realms |

Opening or closing an unrelated menu while Dynasty remains active preserves the
selected subview and does not itself trigger computation. The selected subview
must be identifiable in the interface. Native House/Dynasties modes keep their
native behavior. Diagnostic actions are not part of normal use.

## Shared classification terms

For a valid current player **P**, their Dynasty **D**, and county holder **H**:

- **S** is the set of all ordinary de-facto seniors above H, excluding H.
- **T** is the highest ruler in H's de-facto chain; when H is independent, H
  itself is T.
- A county is classified once. Its result applies to every constituent
  barony, regardless of each baron's Dynasty. De-jure hierarchy is used only
  for that county-to-barony projection.
- Cadet Houses match through shared Dynasty identity. If H has no Dynasty,
  senior checks still apply.
- De-jure claims, occupation, and tributary/suzerain relations do not classify
  a county.

## Subview meaning and result roles

Each subview assigns one semantic result role to a county. The roles describe
category behavior; they do not choose a color:

| Result role | Informal display vocabulary | Meaning |
|---|---|---|
| **Primary** | dark / main | Strongest positive match for the selected subview |
| **Secondary** | light / secondary | Related positive match when the primary condition does not match |
| **Neutral** | grey / nonmatching | Neither positive condition matches, or the county is unheld |

Evaluate **Primary** first, then **Secondary**, then **Neutral**. Thus a county
that meets both positive conditions receives Primary.

| Subview and question | Primary condition | Secondary condition, only if not Primary | Neutral condition |
|---|---|---|---|
| **Dynasty Realms** — where does the Dynasty rule independently or under others? | T belongs to D | H or any senior in S belongs to D | Neither condition matches, or county is unheld |
| **Dynasty Holdings** — where does the Dynasty hold counties directly versus through vassals? | H belongs to D | At least one senior in S belongs to D | Neither condition matches, or county is unheld |
| **My Realm & Dynasty** — where is the player's own de-facto subtree versus the wider Dynasty? | H is P, or P is in S | H or any senior in S belongs to D, outside the player's subtree | Neither condition matches, or county is unheld |

In **My Realm & Dynasty**, a player's subtree includes vassals below P even
when P is a vassal. Sibling vassals under the same highest ruler are outside
that subtree. A county in the player's subtree is Primary even if it also
matches the wider Dynasty condition.

## Examples

All liege chains are de facto. **D** means the current player's Dynasty.

| County holder → seniors | Dynasty Realms | Dynasty Holdings | My Realm & Dynasty |
|---|---|---|---|
| Foreign count → player king | Primary | Secondary | Primary |
| D count → player king | Primary | Primary | Primary |
| D count → foreign king, outside player's subtree | Secondary | Primary | Secondary |
| Foreign count → D duke (not player) → foreign king | Secondary | Secondary | Secondary |
| Foreign count → player duke → foreign king | Secondary | Secondary | Primary |
| Foreign sibling count under player's foreign king, no D senior | Neutral | Neutral | Neutral |
| Foreign count → independent D relative king | Primary | Secondary | Secondary |
| Independent D count outside player's subtree | Primary | Primary | Secondary |
| Foreign-only chain outside player's subtree | Neutral | Neutral | Neutral |

## Availability and boundaries

Invalid player or Dynasty means **unavailable**, with no classification or
map-result writes; it does not mean Neutral. Active-context loss, safe cleanup,
and restoration remain separate safety requirements under ADR-008 and the
existing R-005/R-009 work.

This contract does not define the subview panel's placement or sizing, the
rendered colors for Primary/Secondary/Neutral, legend styling, contrast, ocean
or impassable-land treatment, or visual acceptance. F-001 owns final UI and
visual behavior. F-002 owns whether a Dynasty/House/title-derived accent can be
used and its fallback strategy. The implementation must preserve these
semantic roles if the visual treatment changes.

## Ownership and source of truth

- [ADR-010](../DECISIONS.md#adr-010--three-dynasty-views-and-their-native-map-layout) is the accepted product decision for the three views and core classification semantics.
- [R-016](R-016-my-dynasty-pipeline.md) records bounded research evidence and its limits; it is not full runtime acceptance.
- [F-001](F-001-dynasty-map-ux.md) owns layout, interaction presentation, legend and visual acceptance, including neutral-ground visibility.
- [F-002](F-002-dynasty-color-strategy.md) owns color-source and fallback research.
- [R-017](R-017-test-scenario-selection.md) owns reproducible test scenarios.

This is a documentation-only contract. It does not authorize implementation,
installation, runtime tests, All Dynasties, background scans, or lifecycle
waivers.
