# F-007 — All Dynasties: parked API checkpoint

Issue: [#55](https://github.com/mhaduk/ck3-dynasty-map/issues/55).
Status: **OPEN / PARKED — blocked at the script-side CoA RGB gate**, 2026-10-28.
The user ended this iteration and requested publication of findings and a future
plan. No fourth view was implemented or installed. The original issue retains
the approved feature specification and unchecked acceptance criteria.

## Goal and unchanged architecture

All Dynasties should paint each independent realm with the existing dark shade
selected from its top ruler's Dynasty CoA. Local vassal/holder Dynasties and cadet
Houses must not override that color; no-Dynasty and unheld land stay neutral.
Reuse the current barony renderer, neutral base, independent-ruler/root-down
traversal and F-002 ordered-pair palette/fallback. Color collisions are accepted.
A new renderer, county mapping, Dynasty registry, persistent cache or adjacency
coloring is unnecessary for the known blocker and remains outside approved work.

The shared implementation could start at six RGB channels and the existing
selector. Existing three-view GUI acquisition may remain unchanged; a reusable
script-side Character helper is desirable only if its input accessor is proven.

## Confirmed findings — CK3 1.20.1.2

| Operation | Target-build evidence | Supported context / result |
|---|---|---|
| `dynasty` | `event_targets.log:550–552`; `event_scopes.log:136–141` | Script Character → Dynasty scope; effects and variables supported |
| `Character.GetDynasty` | `data_types_uncategorized.txt:34627–34629` | Data-function Character → Dynasty |
| `Dynasty.GetDynastyCoA` | `data_types_uncategorized.txt:60871–60873` | Data-function Dynasty → CoatOfArms; no effect-callable producer established |
| `CoatOfArms.GetColor(Arg0)` | `data_types_gui.txt:884–886` | GUI/data-function CoatOfArms → CVector4f; no script numeric RGB reader established |
| `generate_coa`, `reset_coa`, `set_coa` | `effects.log:14097–14113` | Script-callable mutations; no documented returned CoA RGB values |

The installed `common/script_values/_script_values.info` describes numeric
formulas, temporary scope/value storage and scope chaining, not arbitrary GUI
function calls or a CoA-channel producer. Searches covered the generated effect,
trigger, scope-target and scope-type catalogs and shipped script_values (122
text files) / scripted_effects (185 text files). No supported RGB reader was
established. No CoA/color-named event-target or scope type was listed.
`has_user_set_coa` and `has_coa_gfx` are predicates, not RGB getters.

**Missing boundary:** scripted Dynasty scope → readable CoA color1/color2 →
six numeric RGB channels accepted by F-002. Arbitrary-Character GUI access is
supported; it does not demonstrate that same access in effect/value evaluation.
`ScriptedGui.Execute` appearing in data_types_script does not supply a
script-side ScriptedGui producer; do not reopen that route without concrete new
evidence. Catalog absence is a bounded supported-API finding, not proof that
all undocumented engine mechanisms are impossible.

## Execution, recovery and cleanup

- `F007-IMPLEMENT-20261028-01` remains **FAILED**, not completed/accepted. Its
  generated candidate is only the unchanged eight-file current-dev baseline.
  No semantic implementation tests or runtime plan were produced.
- GUI verified all ten declared output hashes and triaged the factual
  self-review. No independent implementation review occurred because no
  implementation passed Step 0.
- GUI initially froze a retired installation path. Current wrapper and persisted
  configuration resolve DEV correctly; all eight installed files match the
  generated baseline. This preparation error is recovered, not an open blocker.
  Improvement: resolve current installation metadata before freezing paths.
- A generated catalog contained a non-UTF-8 byte. Byte-preserving bounded
  extraction recovered the relevant signatures without rewriting the source.
  Improvement: hash preserved raw bytes and avoid assuming full-log UTF-8.
- The broad diagnostic packet `F007-COA-BRIDGE-20261028-01` was prepared but never
  sent; it is superseded by the narrower script-accessor gate. It is historical
  evidence, not an active request to investigate GUI controllers.
- The narrow report `F007-SCRIPT-COA-CHECK-20261028-01`, original failed contract,
  candidate hashes, packet and receipts are retained privately for provenance.
  No destructive cleanup of frozen evidence or user/game files was needed.
  No live payload, playset or save changed; no game interaction occurred.

## Future iterations — plan only, no execution authorization

1. **Reopen the script accessor gate only on concrete new evidence.** Reuse the
   recorded negative search and fingerprints. Check a newly identified function,
   scope link, numeric value or supported caller in the target build; after a
   build update revalidate only the affected API. Require exact name, source,
   input context, return type and evidence of effect/value callability. Do not
   repeat broad completed scans or infer callability from a data-types filename.
2. **Optional independent advisory analysis.** Supply only this boundary,
   relevant signatures and current six-channel selector contract. Ask for one
   concrete accessor/caller to verify, with source/version and falsification
   criteria. Do not resend the superseded broad packet unchanged. External
   advice is a hypothesis until checked against the installed target build.
3. **NPC microprobe only after syntax is evidenced.** On one naturally available
   NPC other than the player, read its Dynasty CoA channels, feed the existing
   selector, and log RGB plus palette_id without painting the world. Compare
   with that NPC's GUI CoA using a distinct pair where convenient. Success must
   establish origin, expected selection and independence from GetPlayer; parser,
   scope/type or unavailable-value failures stop the probe. User alone runs CK3.
4. **If direct script access still has no supported route, make a separate GUI
   architecture decision before coding.** The smallest potential change is
   per-refresh GUI-side acquisition for each independent-ruler Character,
   followed by an existing-style scoped RGB/palette dispatch. The script helper
   remains responsible for palette/realm painting; renderer and color semantics
   remain unchanged. Supported enumeration, invocation context and ordering are
   unproven prerequisites, not available APIs asserted by this plan.
5. **Assess orchestration cost explicitly if step 4 is accepted.** A synchronous
   batch would need supported iteration/dispatch. If only multi-frame GUI work
   is possible, a transient per-refresh controller/worklist may be required:
   run identity, progress/completion, reentry/cancellation, ruler validity,
   context loss, cleanup and partial-map visibility would need a defined
   contract. Evaluate whether the user accepts this added state and delay.
   Temporary run state must not silently become a persistent Dynasty registry
   or cache. If complexity is unacceptable, leave F-007 parked.
6. **Implement the fourth view only after the data-source gate and any material
   architecture choice are accepted.** Keep the existing three paths stable;
   select a palette per ruler, then use the existing dark shade and traversal.
   Source/preflight and fresh independent review precede installation. Runtime
   acceptance then covers mixed-vassal realms, multiple colors, neutral cases,
   four-view switching, native/context-loss return, bounded errors and qualitative
   refresh delay. Full-world computation is not the first experiment.

No future stage starts automatically. Registry/caching frameworks, alternative
renderers, House-map reverse engineering and color-collision optimization are
not recommended fallback work. Any proposal beyond minimal acquisition/dispatch
needs a separate scope and user decision. No ADR or architecture contract was
changed by this checkpoint.

<!-- ai-cost:start -->
## AI cost — partial research checkpoint

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6-luna | 2169909 | 2072320 | 97589 | 16477 | 2186386 | $0.03872060 |
| gpt-6.1-sol | 6784835 | 6513280 | 271555 | 34055 | 6818890 | $1.5349880 |
| Automatic approval review — unavailable | N/A | N/A | N/A | N/A | N/A | N/A — unmeasured/unpriced |
| **Total** | 8954744 | 8585600 | 369144 | 50532 | 9005276 | **$1.57370860** |

Method: task-ai-cost/1; frozen evidence cutoff **2026-10-28T11:40:42+00:00**.
Measured response counters cover one F-007 GUI session (six task turns) and the
one failed CLI session (one task turn), including preparation, failed attempts,
recovery, packet preparation, narrow API verification and publication work saved
before cutoff. Response identities were deduplicated; no whole unrelated session
was charged. This is processed input/output across requests, largely cached,
not unique text or active-context size. Later accounting, publication, Git
approval reviews and final readback are excluded to avoid recursive accounting.
No independent implementation review or external diagnostic answer occurred.
Linked automatic approval-review counters were not identified in the selected
saved intervals; their coverage/cost remain unavailable, not zero.

Cached input is a subset; uncached = input minus cached; total tokens = input
plus output. Reasoning is included in output and is not added again. All 82
measured requests recorded zero cache-write tokens; none exceeded 272,000 input
tokens, so no long-context multiplier applies. Missing usage is N/A, not zero;
N/A contributes zero only to known-cost arithmetic. The USD total is partial.

Standard API-equivalent prices verified **2026-10-28**:
[GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
$2/$0.10/$10 and
[GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)
$0.10/$0.01/$0.50 per million uncached/cached/output tokens. The documented
long-context rule is 2× input/cache and 1.5× output above 272,000 input tokens.
Actual subscription charges, service tier, regional/tool charges and unavailable
reviewer billing are not inferred. This is not a bill or a full task-lifetime cost.
<!-- ai-cost:end -->
