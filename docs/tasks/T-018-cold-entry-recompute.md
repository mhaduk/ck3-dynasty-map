# T-018 — Reduce Dynasty Map cold-entry recomputation cost

Issue: [#44](https://github.com/mhaduk/ck3-dynasty-map/issues/44).

## Current checkpoint — 2026-10-25; issue remains in progress

**IN PROGRESS — experimental checkpoint.** The user paused further experiments
and accepts the observed roughly two-second entry for now. The current local
research candidate is corrected palette-hoist **B**; its effects source
SHA-256 is `3dcc3e171ceece48e80b1109f33d5507740d9e86dab88f5f76b71b771b24cdba`,
matching the accepted ten-file installed receipt. Do not infer production-wide
compatibility or feature completion from this local checkpoint.

The supplied GUI checkpoint reuses three complete existing B summary frames;
their emitted fields match A/R0. Each frame reports 4,703 counties, 3,476 held,
1,227 unheld and 12,247 attempted writes. REALMS reports 298 primary / 0
secondary / 4,405 neutral; HOLDINGS 38 / 260 / 4,405; MY_REALM 89 / 209 / 4,405.
The original diagnostic had 11,297 attempted writes. These are emitted
diagnostic counters, not an independent world census or proof of stored/rendered
RGB. Manual same-save timings were original 2.2s, R0 2.5s, A 2.3s and B 2.2s.
The differences are within manual timing uncertainty: **no demonstrated
speedup, percentage gain or causal conclusion**. Engineering preference is not
performance evidence.

Root-down A reorganized classification to visit independent roots and direct
vassals; it can visit more characters and title candidates than the earlier
county-by-county classifier. B moved the finite 76-literal palette dispatch
from projected baronies to exceptional counties, but duplicates literal
branch/traversal source. At fixed palette size the asymptotic source model
remains `O(R + V + E + T + C + B)`; practical costs add traversal nodes, title
candidates, dispatch checks and substantially more source. Final effects are
4,125 lines versus 2,152 in the preserved A baseline (+1,973 after restoration),
with 66 top-level declarations across 65 names. The duplicate declaration is
intentionally retained. This is a source-level model, not measured engine cost.

The final B source correction restored the exact A declaration that an earlier
reviewed candidate had removed; the original escalation remains historical.
The separate scope-repair handoff was independently accepted, B was installed
with an exact ten-file match, and the final GUI checkpoint verified its summary
frames. The final user timing report did not add explicit B visual/native-return
acceptance. Earlier A color/switch observations remain bounded evidence.
Earlier validation/review failures and corrections are preserved below; the
unchanged classification suite’s six GUI/localization source-shape failures
remain known.

Log evidence is finite and not atomic: some warnings appeared later due to
buffering. Old court errors, two intentional GUI overrides and a duplicate
effect warning remain in the recorded interval. No dynmap error-channel
mentions were found in the bounded evidence; this does not establish clean
global logs. Recursive depth/cycles, special-government behavior, atypical
roots, full population census, exact stored/rendered RGB and universal engine
compatibility remain unproven.

### Resume gate

No more profiling, palette/RGB work, runtime tests or optimization is authorized
in this checkpoint. Resume only after the user reopens T-018. The smallest
decisive next step would compare the frozen baseline and B on the same preserved
save/build using a verified existing timing method; R-018/F-006 own timer
research and must not be silently started here. If no existing method provides
comparable measurements, stop with manual observations marked inconclusive.
Future online source/forum analysis is an optional separate research stage, not
evidence that either algorithm is faster.

### AI cost — finite checkpoint

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| gpt-6-luna | 69,187,073 | 67,843,968 | 1,343,105 | 345,425 | 69,532,498 | $0.98546268 |
| gpt-6.1-sol | 39,035,458 | 38,201,856 | 833,602 | 146,955 | 39,182,413 | $8.99049880 |
| **Total** | **108,222,531** | **106,045,824** | **2,176,707** | **492,380** | **108,714,911** | **$9.97596148** |

[GUI context history](../telemetry/gui-context/T-018.jsonl)

Partial known-model Standard API-equivalent estimate through 2026-10-25
22:49:54 UTC; 932 attributable response records from 20 frozen session
sources. Pricing checked 2026-10-25 against the [official API pricing
page](https://developers.openai.com/api/docs/pricing), with documented
whole-request long-context rates for 51 Sol responses over 272,000 input
tokens. Exact service tier/region is unavailable; cache writes are not
separately priced. This is not invoice or subscription spend. Post-cutoff
checkpoint work and later GUI/publication work are excluded.

GUI independently verified the 932 saved-response records, required saved GUI
session, per-response pricing and fresh open-issue readback on 2026-10-26. The
documentation checkpoint is accepted; T-018 remains in progress and experiments
remain deferred by the user. On 2026-10-26 the user authorized scoped
repository publication of the accepted source/tests, checkpoint documentation
and reviewed aggregate telemetry.

## Prior accepted cold-entry stage — R0

The earlier bounded source change added a flat neutral barony initialization
before each valid Dynasty view recomputation, retained Primary/Secondary county
overrides, and removed one proven duplicate Holdings predicate. Neutral
counties remained in the classifier and diagnostics but no longer repainted
their de-jure baronies after the base pass. This stage made no performance or
runtime acceptance claim.

For **B** yielded baronies and **E** baronies under Primary/Secondary counties,
attempted RGB writes were **B + E**: one neutral base write per barony plus one
exception override. Offline evidence did not enumerate B or E; the write count
could exceed the previous total. The structural saving was removal of Neutral
county hierarchy traversals while retaining one flat base and one
`every_county` classification pass. Historical pre-change counts were
diagnostic values, not same-save before/after results.

R0 validation recorded 11 focused cold-entry tests passing; 49/55
classification tests passing with six GUI/localization source-shape failures;
two passes each for palette-context, quantized-palette and RGB-mix suites; and
CK3 1.20.1.2 source preflight passing for 10 files. The generated
`every_barony` API evidence retained 1.20.1.1 provenance and did not prove
1.20.1.2 runtime enumeration or color coverage.

## Historical status — A source candidate (superseded by current checkpoint)

**Implementation A source candidate prepared; independent source review and a
separate user-run runtime gate are pending.** The valid world repaint still
initializes one neutral barony base, then seeds each independent county-or-higher
landed ruler and recursively visits direct vassals. Each visited character
classifies its directly held county titles with a fixed inherited tuple:
`root_is_D`, `strict_ancestor_has_D`, and `inside_player_subtree`. A separate
county pass counts unheld counties as Neutral without reclassifying held
counties. The prior county classifiers remain in source as unused diagnostic
oracles; no world entry calls them.

Primary/Secondary precedence follows F-003 for all three views. The tuple is
encoded by 24 literal scripted-effect variants (eight state combinations for
each fixed view). A node checks its own Dynasty before entering its direct
vassals, so each child receives the parent's inclusive Dynasty result as its
strict-ancestor bit; child Dynasty and player identity select the child's next
variant. Siblings dispatch independently and no character/global/list
membership state is written. This is a source candidate only. Recursive custom
effect support, engine scope behavior, stack/cycle limits, atypical root
coverage, target-build iterator behavior and runtime performance remain
UNKNOWN. No installation, runtime, or speedup acceptance is claimed.

## Operation accounting

For **R** independent roots, **V** visited characters including intermediary,
baron-level and unlanded vassal nodes, **E** direct-vassal edges, **T** held-title
candidates examined by the tier-filtered iterators, **C** counties visited by
the unheld pass, and **B** baronies in neutral initialization/projection, the
source-level work is `O(R + V + E + T + C + B)` with one county projection for
each held county. On an ordinary forest, `E <= V - R`. Filter, iterator,
effect dispatch and recursive engine costs are undocumented. The previous
classifier modeled repeated senior checks as `O(C * H + B)` for maximum senior
chain depth **H**. A benefit is plausible when repeated walks dominate extra
vassal/title traversal; no measured improvement is established. Diagnostic
holder/senior/top counters retain their prior diagnostic-only queries and are
excluded from ordinary traversal timing claims.

The neutral base and Primary/Secondary county overrides retain attempted-write
accounting `B + E_counties`, where `E_counties` is the number of baronies below
Primary or Secondary counties. Current same-save counts are a later runtime
comparison, not an offline test expectation.

## Validation

- Root-down condition-aware source checker and forest-model tests: 6 passed.
  They bind guarded parent/child branch conditions to literal child variants,
  compare chain/star/player-vassal/missing-Dynasty/unheld fixtures with an
  independent F-003 oracle, and reject role, ancestor, sibling, skipped-root,
  duplicate-county, audit-write and neutral-counter mutations.
- Focused cold-entry source/synthetic tests: 11 passed, including base-write
  accounting and audit/no-write guards.
- Existing classification suite: 49/55 passed. The same six GUI/localization
  source-shape failures reproduce against the frozen R0 source: `test_child_modifier_dispatch_keeps_single_view_semantics`,
  `test_hover_copy_has_full_categories_without_debug_or_modifier_hints`,
  `test_numeric_total_candidate_and_sample_role_grammar_are_narrow`,
  `test_source_emitted_grammar_uses_tested_native_shapes`,
  `test_source_normal_paths_full_audit_and_bounded_cleanup_invariants`, and
  `test_top_dynasty_routes_reuse_realms_modifier_operations`. No unrelated
  assertion or file was widened to conceal them.
- Palette context, quantized palette, and RGB mixing suites: 2 passed each.
- Mod preflight: source-only check at CK3 version 1.20.1.2; it verifies file
  conventions/inventory, not parsing, API, recursion, coverage or runtime.
- `git diff --check`: result recorded in the private executor receipt.

The generated `every_barony` API evidence retains its 1.20.1.1 provenance and
does not prove 1.20.1.2 runtime enumeration or color coverage. User-run startup,
same-save classification/timing, all-view switching, native-map return and
post-action log review remain separate follow-up gates.

The private executor receipt preserves the detailed source mapping, validation
evidence, output hashes and GUI handoff limits.

## Palette dispatch hoist B — current installed implementation

B retains accepted A as its byte-exact comparison baseline and changes only the
Primary and Secondary county paint effects. Each now selects among the 76
literal palette branches (or its historical fallback) at county scope; the
selected branch then walks that county's de-jure baronies and writes the same
RGB once per barony. Palette ID comparisons therefore move from each projected
barony to each exceptional county and role. The hierarchy classifier and
neutral base are unchanged. Role diagnostics run once after projection;
county-write and attempted-write increments remain diagnostic-guarded and
occur once per written barony. Audit role logging remains write-free.

The two old mixed-palette effects remain byte-identical A definitions for
compatibility with existing source checks, but have no production call sites.
All other top-level A effects compare byte-for-byte. The preserved A baseline
has 2,152 lines; final B has 4,125 (+1,973) after the exact 74-line A occurrence
was restored. There are 66 top-level declarations across 65 names. This is
bounded source repetition; source tests establish structure and accounting,
not engine latency or a speedup.

Focused source evidence: six palette-hoist tests, six unchanged rootdown tests,
eleven cold-entry tests, two palette-context tests, two quantized-palette tests
and two RGB-mix tests pass. The unchanged classification suite remains 49/55:
the same six GUI/localization/modifier-source-shape tests listed above fail;
no such files or assertions were changed. Source preflight passes for ten files
at CK3 1.20.1.2. The checker does not establish parser, API, runtime, saved-game
or performance compatibility. Later source review accepted the restored scope,
the install receipt verified the ten-file match, and the current checkpoint
records existing summary frames and inconclusive manual timing; broad runtime
and performance acceptance remain pending.

### R1 correction — production-linked validation

Fresh reviewer R1 identified missing test evidence for counter-guard nesting and
production-linked mutation/fixture behavior. C-R1 fixes both findings without
changing the effects candidate. The palette-hoist tests now run a shared
candidate-accepting source validator against the real source and require it to
reject altered RGB, palette ID, role callback, dispatch moved into the barony
loop, missing/duplicate counters, counter increments moved outside the
per-barony diagnostic guard, audit writes, and reset/callback order changes.
The validated source structure drives a small projection fixture with multiple
Primary/Secondary baronies, a neutral county, an empty exceptional county,
diagnostic on/off, audit and rejected-context paths. The cold-entry source
checker also checks guard containment for base and every override branch and
rejects the counter-guard escape mutation. Effects file remains byte-identical
to the reviewed B candidate; rootdown and all other non-owned inputs remain
unchanged.

After correction, palette-hoist tests: 6 passed; cold-entry tests: 12 passed;
rootdown: 6 passed; palette-context, quantized-palette and RGB-mix: 2 passed
each. Classification remains 49/55 with the same four failures and two errors
on unchanged GUI/localization/modifier-source-shape tests. Source preflight
passes for 10 files at 1.20.1.2. These checks still do not establish CK3
parser/API/runtime compatibility or performance.

### R2 correction — fallback and callback structure

R2 found the source validator could accept the Primary callback nested inside
fallback and did not apply the numbered branch's hierarchy/filter/write checks
to fallback. C-R2 fixes the test validator only; effects remain byte-identical.
The validator now tracks balanced brace depth when selecting direct siblings,
requires the role callback to be a diagnostic-guarded sibling after the complete
fallback branch, and applies the same barony iterator, filter, single literal
write, dispatch exclusion and guarded accounting checks to all 76 numbered
branches and fallback. The source-derived projection first runs these invariants,
so it rejects the same broken candidates before modeling output.

The focused palette suite has 7 tests passing, including explicit rejection of
callback-in-fallback, removed fallback tier filter, fallback write outside the
loop and fallback dispatch inside the barony loop. Full frozen validation:
rootdown 6, cold-entry 12, palette-context 2, quantized-palette 2 and RGB-mix 2
passed; classification remains 49/55 with the same six unchanged
GUI/localization/modifier source-shape failures; ten-file source preflight and
diff check pass. No production effect changed. Runtime and speedup remain
unproven.

### R3 GUI-directed occurrence restoration — accepted bounded source correction

The prior implementation handoff ended in `ESCALATE TO GUI` after identifying
an out-of-scope deletion: A contains 66 top-level effect occurrences across 65
unique names, while escalated B contained 65 occurrences. GUI directed a new,
separate bounded repair to restore the exact first A occurrence of
`dynmap_r016_realms_county_effect` between `dynmap_r016_paint_mixed_secondary_effect`
and `dynmap_r016_select_palette_effect`. The later duplicate remains in place.
This does not rewrite the prior escalation or its evidence.

The repair copies the original A declaration and body verbatim. An occurrence
aware test helper walks balanced top-level declarations while respecting
comments and quoted strings; its regression rejects deletion of either
identical occurrence and ignores a nested column-zero `else` containing a
declaration-like line. The new test also preserves the prior R1/R2 guard,
callback, fallback and mutation checks. Palette-hoist tests now pass 8 tests;
rootdown 6, cold-entry 12, palette-context 2, quantized-palette 2, and RGB-mix
2 pass. Classification remains 49/55 with the same four failures and two
errors in unchanged GUI/localization/modifier source-shape checks. Ten-file
preflight at 1.20.1.2 and `git diff --check` pass. This is source evidence only:
the engine parser, runtime, installed equality and performance remain
unverified. The separate repair review accepted the restored occurrence; the
later ten-file install receipt and current experiment checkpoint establish the
installed hash and bounded emitted summaries.
