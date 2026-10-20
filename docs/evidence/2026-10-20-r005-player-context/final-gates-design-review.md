# R-005 — Combined final-gate design review

Date: 2026-10-20. Read-only analysis; no probe/install/game changes.
Result: one combined session is a goal, but a runnable plan is not ready.

## Guard proposal

Use a fresh explicit player root for the candidate Execute action. Bind the
clickable control's visible/enabled properties directly to GetPlayer.IsValid;
avoid automatic character-scoped queries in properties evaluated without a
player. Installed hud.gui:30–51 and the earlier watcher support the GUI validity
discriminator; v3 establishes logging effects with explicit valid roots.

This is a candidate external UI boundary, not atomic dispatch proof. Any new
probe must verify the changed control's availability and bounded log behavior,
separately from callback receipt. Do not repeat known NULL validation failures,
assume lazy And/Select evaluation, or treat hidden UI alone as universal safety.
No color/classification work belongs here. Source review is still required for
the no-Dynasty availability binding, including its absent-player evaluation.

## Natural fixture: why Aepak is not ready for a user test

CLI found fictional_cumans_3 (Aepak), alive at the 867 start, without a Dynasty
assignment in his character history; title history assigns c_chumkar_kia and
herder_government. Parent verified those source references, then found material
counterevidence not covered by the proposed playability inference:

| Installed source | Evidence / limit |
|---|---|
| history/characters/cuman.txt:4463–4473; history/titles/k_cuman.txt:61–66 | Aepak's history and title/government assignment; no runtime local-player proof. |
| common/governments/00_government_types.txt:738–746 | Herders have rulers_should_have_dynasty = no. |
| localization/english/government_l_english.yml:285 | Herder government is described as unplayable. This contradicts treating a county-tier scripted trigger as sufficient playability evidence; it is not an independent engine trace. |
| common/on_action/game_start.txt:459–488 | Without Khans of the Steppe DLC, startup converts herder/nomad holdings and relevant capital holders to tribal. The recorded test baseline has only Garments DLC mounted. |
| common/governments/00_government_types.txt:187–190,634–638; _governments.info:26–29 | Tribal/nomad rules request ruler Dynasties; generated state may differ from history. Exact Aepak runtime outcome is not proven. |
| common/on_action/yearly_on_actions.txt:1605–1623 | Player herders are converted to nomads by a yearly action; no general stable-player fixture follows from source history. |

Do not instruct the user to start as Aepak as if a playable no-Dynasty fixture
were established. The CLI analysis remains useful research, with this parent
correction retained. No natural local-player fixture is verified.

## Controlled fixture proposal — user accepted, not yet implemented/executed

Generated target-build effects.log:10714–10715 documents set_to_lowborn for a
character. A possible controlled setup is a clearly labelled, one-shot fixture
action affecting ONLY the current test ruler in a newly created disposable
timeline while paused. It would log the current player and Dynasty state before
and after setting that test character lowborn. It must not touch vanilla files,
valued saves, unrelated characters, titles or map colors. No automatic execution.

This intentionally changes a test character; the previous logging-only probe
scope does not cover executing it. Its exact permitted fixture scope must be
accepted before a user-run test. The user subsequently explicitly accepted this
scope for a new disposable timeline and one bounded combined attempt. Runtime
must independently confirm GetPlayer
valid, Dynasty absent and no Game Over; stop on mismatch, automatic Dynasty
creation or player loss. Never count NO PLAYER as a no-Dynasty player pass.
Source metadata alone does not establish fixture stability, even while paused.

If that scope is accepted, prepare one probe and one conditional session:

1. Healthy-player control for the new guarded entry, then absent-player
   availability/dispatch checkpoint with bounded markers/errors. This concerns
   the new boundary, not repeated old lifecycle tests.
2. Return to the same disposable test ruler; invoke the explicitly labelled
   lowborn fixture once. Only if the fixture checks pass, verify unavailable
   no-Dynasty local-player UI and no activation/classification/color writes.

Independent outcome criteria are required for both checkpoints; a fixture
failure leaves the second gate open. Do not promise that one session closes
R-005. If character mutation is outside the user's chosen scope, keep the
no-Dynasty gate open and continue natural-fixture research separately.

## Accepted fallback and preparation

User instructed that if this bounded attempt fails, record the unresolved
no-Dynasty edge case and create a GitHub follow-up to return to later, rather
than iterate indefinitely. Parent has conditional GitHub-write authorization
for that follow-up only and must check existing issues first; no issue exists
from this instruction yet. This does not convert failure into a pass or waive
ADR-008. Missing-player and fixture outcomes remain independent.

CLI preparation specifies manual CHECK for Dynasty availability, so no
character-scoped query is automatically evaluated under NO PLAYER. Automatic
control properties read only player validity and GUI-local status, with a
GUI-only player-loss invalidation watcher. LOWBORN TEST is one-shot and explicit;
no classification/colors or unrelated character changes. Source review and
runtime validation are still pending; the test plan is not a verified API.

## Prepared probe review

CLI implemented the combined probe; parent verified the exact four-file payload
and source/install equality, unchanged saved ENTRY-only selection, and matching
handoff IDs. Prior logs were preserved with zero FINAL markers. Automatic GUI
properties read only GetPlayer.IsValid or GUI-local keys. CHECK alone performs
the rooted availability query and logs an independent player/Dynasty inspection;
activation is guarded by player validity plus cached READY. Player loss clears
availability through a GUI-only nested watcher. LOWBORN validates the ruler and
Dynasty in both validation/effect, performs one set_to_lowborn statement, and
uses a GUI lock that RESET cannot clear. No other gameplay mutation was found.

These are source/install findings, not runtime acceptance. Callback order,
nested watcher behavior, availability and fixture outcome remain unverified.
Run checkpoint A and capture/report its result before the one-shot fixture in
B, within the same session. User alone performs all CK3 actions.
