# F-003 — Dynasty subview definitions and appearance

Status: COMPLETE — accepted-definition record, 2026-10-21. This document
consolidates ADR-010 and the user-approved menu structure; it is not a feature
implementation or a claim of complete runtime correctness. The confirmed third
name is **My Realm & Dynasty**, not Dynasty Holdings&Realms.

## Menu and interaction

| Element | Accepted definition | Appearance / behavior |
|---|---|---|
| Entry | One **Dynasty** entry in the map menu | Opens Dynasty Realms on initial entry and on return from a native mode |
| First subview | **Dynasty Realms** (default) | Selected state and its matching legend visible |
| Second subview | **Dynasty Holdings** | Direct selection recomputes its own categories |
| Third subview | **My Realm & Dynasty** | Direct selection recomputes its own categories |
| Refresh | Recompute the selected subview using fresh player/Dynasty context | Explicit action; no recurring world scan |
| Other menus | Opening/closing a menu while Dynasty stays active retains the selected subview | Menu opening alone must not compute |
| Return | Return to ordinary **Realms** | Custom panel leaves with Dynasty; native controls retain native behavior |
| Diagnostics | Development tools separate from the normal flow | Normal activation does not require CHECK/COMPUTE/DISPLAY |

F-001 owns final spacing, positioning, sizing, tooltips, supported scales and
visual acceptance. Current prototype layout is a tested research candidate,
not a frozen final layout. Desired behavior in this table is not a universal
runtime guarantee: R-016 established only bounded smoke evidence.

## Exact category definitions

P is the valid current player, D their valid Dynasty, H the county holder,
S all ordinary de-facto seniors above H (excluding H), and T the highest ruler.
An independent H is its own T. Evaluate dark first, then light, then grey.

| Subview / question | Dark category | Light category, only if not dark | Grey category |
|---|---|---|---|
| **Dynasty Realms** — where does the Dynasty rule independently or under others? | T belongs to D: the whole realm has a dynastic highest ruler | H or any senior in S belongs to D, under a foreign T | Neither condition matches, or county is unheld |
| **Dynasty Holdings** — where does the Dynasty hold counties directly versus through vassals? | H belongs to D | At least one senior in S belongs to D | Neither condition matches, or county is unheld |
| **My Realm & Dynasty** — my own realm versus the wider Dynasty | H is P, or P is in S: the player's own de-facto subtree | H or any senior in S belongs to D, outside that subtree | Neither condition matches, or county is unheld |

A player who is a vassal has a dark subtree in My Realm & Dynasty; sibling
vassals under the same top ruler are not automatically part of it. Cadet Houses
share Dynasty identity. Lowborn holders still require the senior-chain check.
The county is the semantic unit: every constituent barony inherits its category
irrespective of the baron's Dynasty. De-jure hierarchy is used only for that
projection. Occupation, claims and tributary/suzerain relations do not classify.
Invalid player or Dynasty means **unavailable with no classification/writes**,
not grey territory. Active-context loss/cleanup remains a separate safety gate.

## Examples

D means the player's Dynasty; all chains below are de facto.

| County holder → seniors | Realms | Holdings | My Realm & Dynasty |
|---|---|---|---|
| Foreign count → player king | Dark | Light | Dark |
| D count → player king | Dark | Dark | Dark |
| D count → foreign king, outside player's subtree | Light | Dark | Light |
| Foreign count → D duke (not player) → foreign king | Light | Light | Light |
| Foreign count → player duke → foreign king | Light | Light | Dark |
| Foreign sibling count under player's foreign king, no D senior | Grey | Grey | Grey |
| Foreign count → independent D relative king | Dark | Light | Light |
| Independent D count outside player's subtree | Dark | Dark | Light |
| Foreign-only chain outside player's subtree | Grey | Grey | Grey |

## Palette and legend contract

| Category | Current R-016 prototype RGB | Target appearance / legend |
|---|---|---|
| Dark | 25, 105, 50 | Strong category shade, distinct from light and neutral; meaning depends on active subview |
| Light | 145, 220, 150 | Lighter related shade with sufficient separation from dark and terrain |
| Grey | 65, 70, 80 | Clearly neutral nonmatching county land, including continental/world controls |
| Unavailable | No color write | Disabled/hidden actions and explicit unavailable behavior; never a neutral-map substitute |

The grey values in code did **not** produce satisfactory visible neutral ground
in R-016. This remains failed visual acceptance, not a proven palette-only or
shader-only cause. F-001 must diagnose classification/projection/display and
verify contrast at relevant zooms. Ocean and non-county impassable areas are not
automatically grey county results; F-001 defines their presentation separately.

F-002 owns whether a supported Dynasty/House/coat-of-arms source can supply the
accent. Fixed green remains the fallback, not a permanent brand-color decision.
Legend swatches and words must match the actual active palette; a hue change
must not change category semantics. Actual accessible Dynasty color is unproven.

## Ownership and limits

- [ADR-010](../DECISIONS.md#adr-010--three-dynasty-views-and-their-native-map-layout): accepted semantics and order.
- [R-016](R-016-my-dynasty-pipeline.md): completed research with bounded validation, known grey failure and safety/persistence limits.
- [R-017](R-017-test-scenario-selection.md): reproducible character/year and contrasting fixtures.
- [F-001](F-001-dynasty-map-ux.md): final UI and grey/contrast implementation specification.
- [F-002](F-002-dynasty-color-strategy.md): color-source/fallback strategy.

No new runtime, install, source change, All Dynasties implementation, background
scan or lifecycle waiver is part of F-003. Broader semantic coverage, no-Dynasty
UI, atomic entry, shared title-color restoration and save/removal safety remain
unverified under their existing owners.
