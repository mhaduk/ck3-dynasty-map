# R-017 — Test scenario and start selection

Issue: [#19](https://github.com/mhaduk/ck3-dynasty-map/issues/19).

Status: **COMPLETE — scenario-selection stage**. Three easy-to-select starts
are recorded below for subsequent user-run tests: Ismail Samani in the 867
Iranian Intermezzo, William the Bastard in the 1066 Fate of England, and
Murchad ua Briain in the 1066 Rags to Riches bookmark. The roster and static
locators are ready; runtime behavior, complete liege chains, and remaining
family/comparator cases are intentionally left for those later tests. No
runtime test was performed in this task. Harold 1066 remains the R-016
comparison baseline and is not counted as a new recommendation.

## Decision and evidence labels

Use **Ismail Samani, 867.1.1** as the primary future test start: the bookmark
selects `c_bukhara`, and explicitly labels Nasr (163099) both Ismail's liege
and brother. Target title history places Ismail in `c_bukhara` and Nasr in
`k_transoxiana` at the start. This is the strongest sourced natural player to
Dynastic senior case among the shortlist. Use **William the Bastard, 1066.9.15**
as an optional complement for a second, differently dated title-history case:
he holds `d_normandy` and `c_alencon`; the duchy's recorded liege changes from
`k_france` to `k_england` on 1066.10.14. Murchad 1066 remains an easy alternate
with a confirmed starting duchy and county holder, but his senior chain is not
established here.

Evidence labels: **VERIFIED-static** means an installed bookmark, character,
House/Dynasty or title-history field directly supports the claim. **LIKELY**
marks a start-date title-liege chain suggested by title history that still
needs live-game confirmation. **UNKNOWN** means do not count the case as
covered. Title-history `liege` fields and de-jure hierarchy are reported
separately from bookmark relationship labels; a de-jure parent alone is not
evidence of de-facto liegeage.

## Sourced start records

| Candidate | Start title and county evidence | Family / Dynasty identity | Chain and status | Use |
|---|---|---|---|---|
| **Ismail Samani (primary)** | Bookmark `bm_867_persia`, 867.1.1, key `bookmark_persia_ismail_samani`, ID 163157, title `c_bukhara`. `history/titles/k_transoxiana.txt`: `c_bukhara` holder 163157 from 864.1.1 and `liege = k_transoxiana`; `k_transoxiana` holder 163099 from 864.1.1. | `history/characters/tajik.txt`: Ismail 163157 and Nasr 163099 both `dynasty_house = house_samanid`; `common/dynasty_houses/00_dynasty_houses.txt` maps that House to Dynasty 1042070. Bookmark sidekick explicitly says `BOOKMARK_RELATION_LIEGE_AND_BROTHER`; Ismail history comment at 866.1.1 also calls Nasr his brother and liege. | **VERIFIED-static:** Ismail starts as a vassal under named same-Dynasty Nasr; the bookmark directly labels that relationship. Nasr holds `k_transoxiana` at start. **UNKNOWN:** whether Nasr has a senior above him in the live start; no complete runtime chain is claimed. | Best direct player → Dynasty senior fixture for My Realm & Dynasty and Holdings/Realms. Does not alone cover a Dynasty ruler outside the player's subtree or a neutral comparator. |
| **William the Bastard (complement)** | Bookmark `bm_1066_hastings`, 1066.9.15, key `bookmark_hastings_normandy`, ID 140, title `d_normandy`. `history/titles/k_france.txt`: `d_normandy` holder 140 from 1035.7.3; `c_alencon` holder 140 from 1037.1.1. | `history/characters/norman.txt`: William 140 has `dynasty = 752`; `common/dynasties/00_dynasties.txt` identifies 752 as Normandie. | **LIKELY:** title history records `d_normandy` liege as `k_france` from 911.1.1, changing to `k_england` on 1066.10.14, after the bookmark date. Treat this as a promising date-specific liege-chain fixture, not runtime proof. | Useful second start for a recorded liege transition and direct county/title holder. Relationship and live status still need a short observation. |
| **Murchad ua Briain (alternate)** | Bookmark `bm_1066_rags_to_riches`, 1066.9.15, key `bookmark_rags_to_riches_petty_king_murchad`, ID 83355, title `d_munster`. `history/titles/k_ireland.txt`: `d_munster` holder 83355 from 1063.7.1 and `c_thomond` holder 83355 from 1063.7.1. | `history/characters/irish.txt`: Murchad 83355, Brian 83357 and Bébinn 166126 use `house_british_isles_briain`; `common/dynasty_houses/00_dynasty_houses.txt` maps that House to Dynasty 100009. **Conflict:** the bookmark sidekick entries label Brian/Bébinn with `dynasty = 695`; `common/dynasties/00_dynasties.txt` defines Dynasty 695 as Briain, while the House record maps Briain to 100009. Do not treat the bookmark's numeric sidekick field as a confirmed character-Dynasty match. | **VERIFIED-static:** title holders and shared House are sourced. **UNKNOWN:** independence/vassal status and full de-facto chain. | Easy alternate with actual county/title holder evidence; use only after the Dynasty ID discrepancy and senior chain are checked in-game. |

The English bookmark localization identifies the routes as **The Iranian
Intermezzo**, **The Fate of England**, and **Rags to Riches**. These are
ordinary playable bookmarks without an explicit DLC gate in their entries;
this does not verify the user's ownership or enabled content.

## Coverage scorecard against ADR-010 / F-003

| Required case | Ismail 867 primary | William 1066 complement | Murchad 1066 alternate |
|---|---|---|---|
| Player's starting title and held county | **VERIFIED-static** — `c_bukhara`, holder Ismail (163157) | **VERIFIED-static** — `d_normandy`; `c_alencon`, holder William (140) | **VERIFIED-static** — `d_munster`; `c_thomond`, holder Murchad (83355) |
| Player independent or vassal | **VERIFIED-static vassal** — bookmark says Nasr (163099) is liege | **LIKELY vassal** — title-history `liege = k_france` on start date; runtime confirmation needed | **UNKNOWN** — do not infer from de-jure title placement |
| Natural Dynasty senior / county outside player's subtree | **VERIFIED-static** — Nasr is same-House/Dynasty named liege; separate outside-subtree county not located | **UNKNOWN** — no distinct Dynastic senior fixture verified | **UNKNOWN** — bookmark relative labels conflict on Dynasty ID; no senior chain verified |
| Foreign holder in player subtree vs sibling under same top ruler | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** |
| Independent Dynasty relative and/or their vassal | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** |
| Foreign-only neutral comparator | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** |
| Cadet House, lowborn holder with Dynastic senior, unheld county | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** |

The selection deliverable is complete: Ismail is the primary start for a
direct natural player-to-Dynastic-liege case, William is a second start with a
date-specific historical liege transition, and Murchad is an easy alternate.
The three starts are selected for observation, not claimed as a complete
coverage matrix. Outside-subtree, sibling, independent-relative, foreign-only,
cadet, lowborn and unheld cases remain to be explored during later testing.
Do not infer live de-facto chains from `common/landed_titles` hierarchy.
Bookmark's explicit Ismail–Nasr relation is direct static evidence; other
title-history `liege` chains remain **LIKELY** until a game-state observation.

## Shortest future observation if needed

No game action was part of this research task. In a later user-run check,
start the 867 **Iranian Intermezzo** as Ismail and pause before
using a subview. Record (1) Ismail's actual held county/title and displayed
liege; (2) Nasr's full senior chain through the top ruler; and (3) one nearby
county held by a non-Samanid under a Dynastic senior or, if immediately
available, a foreign-only comparator. Record each county, holder, House,
Dynasty and every senior. Leave the other scorecard rows UNKNOWN if they are
not immediately verifiable. Do not use names, borders, or de-jure placement as
substitutes for character House/Dynasty and actual liege details.

## Source provenance and limits

Target: installed CK3 1.20.1.2 (Crozier), Steam build 26046173, as recorded in
the current project state. Narrow source files inspected (paths relative to
installed `game/`):

- `common/bookmarks/bookmarks/00_bookmarks.txt` — `bm_867_persia`,
  `bm_1066_hastings`, `bm_1066_rags_to_riches`; start dates, character IDs,
  title keys, and Ismail's explicit liege/brother sidekick relation.
- `history/characters/tajik.txt`, `irish.txt`, `norman.txt` — IDs 163157,
  163099, 83355, 83357, 166126 and 140; House/Dynasty and family fields.
- `common/dynasty_houses/00_dynasty_houses.txt` and
  `common/dynasties/00_dynasties.txt` — House-to-Dynasty mappings, including
  the Briain numeric discrepancy.
- `history/titles/k_transoxiana.txt`, `k_ireland.txt`, and `k_france.txt` —
  dated holders and explicit title-liege transitions for the named titles.
- `common/landed_titles/00_landed_titles.txt` — county/title rank and
  de-jure nesting only; not used alone to claim de-facto liegeage.
- `localization/english/bookmark/bookmark_persia_867_l_english.yml`,
  `bookmark_hastings_1066_l_english.yml`, and
  `bookmark_rags_to_riches_1066_l_english.yml` — English bookmark/character
  labels.
- [ADR-010](../DECISIONS.md#adr-010--three-dynasty-views-and-their-native-map-layout),
  [F-003](F-003-dynasty-subview-definitions.md), and
  [R-016](R-016-my-dynasty-pipeline.md) — accepted meanings and Harold baseline.

No save, runtime state, DLC ownership, or launcher/game UI was inspected. No
raw installed data was copied into the repository, and no APIs or build
compatibility claims were revalidated.

<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| codex-auto-review | 75298 | 48896 | 26402 | 356 | 123 | 75654 | partial |
| gpt-6-luna | 15451215 | 15000960 | 450255 | 94071 | 44497 | 15545286 | partial |
| **Total** | 15526513 | 15049856 | 476657 | 94427 | 44620 | 15620940 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-22T13:15:22Z. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
Coverage is partial: only explicitly evidenced task turns and linked reviews are allocated; ambiguous usage and missing history are not estimated. Includes research, corrections, reviews, closure and the evidenced failed initial pickup. Shared advance planning with other tasks remains unallocated. This backfill job is assigned to T-002 and excluded from these historical totals. No currency or quota inference.
<!-- ai-cost:end -->