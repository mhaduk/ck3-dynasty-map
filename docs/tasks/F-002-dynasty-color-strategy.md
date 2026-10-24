# F-002 — Dynasty color strategy

Issue: [#21](https://github.com/mhaduk/ck3-dynasty-map/issues/21).

Status: COMPLETE for bounded, user-accepted character-associated palette behavior. Source 52, installation 53, fresh startup 54, first-entry observation 55, and GUI review of native summaries 56 form the accepted working baseline. The GUI independently verified the finite-cutoff saved-session cost account. Issue #21 and the project Wiki were updated and read back; the issue was closed after publication gates passed. This is not a full-roster or lifecycle-safety claim.

## Accepted behavior

The current player’s CoA exposes two ordered RGB colors to the existing refresh callback. The selector compares all six byte channels against a frozen table of 76 complete ordered color pairs. Each channel has an inclusive ±5 tolerance; the 76 boxes are disjoint. The matched table row selects the precomputed category shades. Twelve roster entries have no second color, and unknown/unmatched pairs select the exact historical option-B green (dark 25/105/50, light 145/220/150). User observations support practical character-associated variation. This is an approximation, not a Dynasty-ID lookup or a promise that a Dynasty keeps one color across cadet Houses or succession.

Dark output preserves the 75/25 RGB mix, applying a maximum-channel floor of 40 only when the mix is darker; zero maps to 40/40/40. Light output moves dark 35% toward white. Byte outputs use floor(x+0.5). The Charles pair accepted at first entry produces dark 134/59/29 and light 176/128/108. The source word `red` is not treated as literal 255 RGB. Tolerance is an intentional classification allowance; it is not evidence that the engine rounds source RGB in a particular way.

Selection happens once in the normal current-character refresh script before the world paint. The selected ID feeds the existing writers. No automatic switch hook, timer, dynasty registry, or repeated scan is added. Observer mode hides the custom controls when there is no valid player. Existing classification and category meanings are unchanged. The existing native header, close/back control, three views, exact F-004 tooltip text and 130x40 host geometry are preserved.

## Evidence and limits


A separate transparent top-of-viewport diagnostic overlay remains in the accepted source. It exposes cached-ID/channel diagnostics and only the known Charles pair-2 and option-B swatch examples; it is not a 76-row palette legend. The screenshot evidence does not establish that this top overlay rendered or verify its placement. It was authorized and remains; this closeout does not remove it or claim visual acceptance for it.

The user reports that colors work across many characters, observer behavior is correct, and the requested behavior works. The first-entry screenshot documents the brown Charles map and Dynasty Realms tooltip; the second supplied screenshot documents a different palette in another session. These are bounded user observations, not a census of all 76 pairs, an independent RGB pixel audit, or proof of stored channel values. Runtime 56 independently verified the framing/arithmetic of three diagnostic summaries (4,703 rows each); it did not independently audit classification.

The accepted source is the exact ten-file payload from `F002-PALETTE-DIAG-FIX-20261024-52`, installed and hash-matched in 53. The initial source candidate needed a selector dataflow correction after 51; accepted source 52 writes all six fresh RGB variables before matching. The normal repository probe had drifted in six of ten files before consolidation; a private pre-consolidation snapshot is retained. The installed-payload equality/preflight evidence is in the private receipt for 53.

The table was generated from a named-color roster with source fingerprint `3142d65d5217c40cb015bc7c66275695ebb5c618dd243a13182aebc1de0e186c`. It contains 88 ordered textual pairs: 76 complete and 12 without color2. All 12 missing-color2 entries use option B. The source did not establish the engine’s absent-slot normalization, so no general alpha/zero interpretation is claimed. Aliases and sparse pair IDs are retained in matching; no nearest-color search is used. The generated public table omits raw Dynasty IDs and vanilla source dumps.

Known historic failures and corrections remain visible in the private task chain: direct dynamic `Color` assignment was rejected by the target parser; an earlier macro form exceeded the engine’s depth-20 limit; the initial palette candidate regressed accepted menu presentation because its baseline predated F-001 cleanup; and a later selector read stale diagnostic values until source 52 corrected its write-before-branch dataflow. Each failure was a bounded source/startup finding, not proof that the accepted path is impossible.

This acceptance does not establish full 76-pair runtime coverage, exact RGB storage/readback for every character, rendered-pixel accuracy, performance under a census, missing-slot normalization, saved-game compatibility, or safety after removing the mod. No fresh game test, save, character switch, or installation is part of closeout preparation. The user alone controls CK3.

## AI-cost accounting

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| `codex-auto-review` | 21,580 | 6,016 | 15,564 | 134 | 21,714 | N/A — unpriced model |
| `gpt-6-luna` | 169,742,951 | 165,842,560 | 3,900,391 | 1,024,175 | 170,767,126 | $2.56055220 |
| `gpt-6.1-sol` | 77,868,017 | 77,110,016 | 758,001 | 192,887 | 78,060,904 | $13.82554320 |
| **Total** | **247,632,548** | **242,958,592** | **4,673,956** | **1,217,196** | **248,849,744** | **$16.38609540** |

**Coverage:** partial finite cutoff 2026-10-24 21:27:16 UTC. The inventory includes 3 identified GUI session files, 31 identified Luna CLI session files, and one linked automatic-review session, with 140 attributed turns and 2,212 assigned response records. The mapping selects turns by explicit F-002 task IDs and unlabeled continuations bounded by F-002 turns. Forty-three response records in those mixed-task source files remain unassigned; one unlabeled Luna turn also remains excluded. Earlier unrelated sessions before the first F-002 activity were not assigned. The current closeout preparation after the frozen cutoff, GUI review, and publication are excluded.

**Pricing:** current official OpenAI Standard rates checked 2026-10-24. `gpt-6.1-sol` rates per million: short input $2.00, cached $0.10, output $10.00; long input $4.00, cached $0.20, output $15.00. `gpt-6-luna`: short $0.10, $0.01, $0.50; long $0.20, $0.02, $0.75. The long-context tier applies above 272,000 input tokens per request; 72 Sol requests qualified and no Luna request did. Cached input is a subset; uncached input is input minus cached. Reasoning tokens are already included in Output.

Pricing references: [OpenAI API pricing](https://developers.openai.com/api/docs/pricing), [gpt-6.1-sol model rates](https://developers.openai.com/api/docs/models/gpt-6.1-sol), and [gpt-6-luna model rates](https://developers.openai.com/api/docs/models/gpt-6-luna) (checked 2026-10-24).

The recorded `codex-auto-review` identifier is not priced in the official model tables and remains visibly unpriced. Cache-write counters and actual service tier/region are unavailable, so these are rough API-equivalent estimates for measured usage, not API spend or subscription cost. N/A model cost contributes $0 only to the known-dollar sum; missing usage is never treated as zero.

Private mapping, session-prefix hashes, response-level audit, and independent recomputation are in this handoff’s `cost-mapping.json`, `cost-inventory-private.json`, `cost-audit.json`, and `cost-account.json`.


The linked [F-002 GUI context history](../telemetry/gui-context/F-002.jsonl) contains aggregate saved-text estimates through handoff 48 only; it is not token-usage or cost evidence.

## Closeout assets and verification

- [First Dynasty entry and Dynasty Realms tooltip](../images/f002/first-entry-dynasty-realms-tooltip.png) — user-supplied screenshot 55, resized for display and converted to a generic sRGB profile; no gameplay identity beyond the reported Charles II 867 test is inferred.
- [Different character palette](../images/f002/multiple-character-colors.png) — user-supplied screenshot, resized and converted to generic sRGB.
- [Accepted map and unobscured compact menu](../images/f002/accepted-menu-unobscured.png) — user-supplied screenshot, resized and converted to sRGB. It documents the map/menu presentation only; it predates the final tooltip restoration and does not establish tooltip or first-entry behavior.
- The public record pins the accepted ten-file payload hashes in the closeout evidence.
- Source-table, generator, focused regression, preflight, screenshot metadata/privacy and publication preview checks are recorded in the F-002 closeout-preparation handoff.

The bounded task and authorized publication are complete. The frozen partial finite-cutoff cost remains $16.38609540 known-model API-equivalent usage; later preparation, review and publication work is excluded. See the published Issue #21 and Wiki record for the same cost table and remaining evidence limits.
