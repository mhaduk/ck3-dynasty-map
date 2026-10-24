# T-015 — Diagnostic escalation and independent review

## Status

**COMPLETE — GUI accepted on 2026-10-24; [issue #41](https://github.com/mhaduk/ck3-dynasty-map/issues/41) closed completed.**
GUI independently inspected corrected source and adversarial tests, reran all
161 tests and verified the frozen saved-session cost account against the
original source prefixes. The original failed execution and accepted
administrative receipt repair remain preserved privately.

## Result summary

The implementation adds an opt-in, evidence-state escalation gate; a standard
library helper that consumes one explicit versioned manifest and named bounded
inputs; deterministic packet/prompt generation; private immutable snapshots;
hash validation; and explicit advisory response import. Reviewers cannot
change project files, Issues, game state or task status through this helper.
Coordinator synthesis remains manual. A historical dry run uses only the
already-recorded named F-004 documentation and preserves completed experiments
and their limits.

Import rejects dangling review-file symlinks and uses exclusive creation.
Manifest inputs are checked for type before use; identity JSON is schema-checked
and its review ID must match the manifest and output directory. Optional
absence is explicit, while unsafe optional paths fail closed. Source excerpts
and imported replies cannot escape their Markdown text blocks with literal
fences.

## Acceptance and limits

- Packet provenance records manifest, source and extracted-content hashes and
  selectors. Preview is no-write; repeated build refuses overwrite.
- Required missing inputs fail. Genuinely absent optional input and absent
  selected fields are marked `UNAVAILABLE`; unsafe optional paths and malformed
  inputs fail. Source evidence class and upstream text are not upgraded.
- Paths, symlinks, review IDs, identity metadata, source/excerpt sizes and
  common sensitive values are bounded/checked. The scanner is not proof of
  privacy; human review before transfer remains required.
- Responses are imported only by explicit path into separate private files,
  tagged with reviewer label and packet/response hashes. They remain untrusted
  advisory text. Multiple responses do not enter subsequent packet/prompt
  bytes.
- No new CK3 experiment, external reviewer invocation or API integration was
  needed. The user separately authorized documentation, issue/Wiki publication,
  scoped cleanup, commit and push; no measured savings are claimed.

## Checks

Exact commands, hashes, historical excerpt paths, saved-session mapping and
known limitations are recorded in the local handoff result and
`.codex-sync/T015-FIX-CLOSEOUT-PREP-20261024-03/validation.md`.

- `corrections`: PASS — adversarial symlink, null-schema, malformed identity,
  review directory/identity symlinks, review-ID mismatch, Markdown-fence and
  optional-path/type cases.
- `regressions`: PASS — 161 tests across seven required suites.
- `historical-packet`: PASS — original packet validates `VALID`; packet hash
  remains `21271a5306286f48796ce8105e6b8e8706e4e73ae404555b00c883374397fe83`.
- `accounting`: PASS — 118 mapped own responses from one GUI session and two
  CLI sessions; automatic-review usage is unavailable in inspected sources.
- local-ai-cost-table-format: PASS — local table and arithmetic verified.
- ai-cost-table-format: PASS — issue body table, arithmetic, limitations and
  label verified by remote readback; matching canonical table below.
- `documentation`: PASS — workflow and usage guide accepted; Wiki Home and
  Diagnostic-review published in `be80e03` and read back byte-for-byte.
- `privacy-scope`: PASS — exact public-file scan and whitespace check recorded
  locally; scoped publication follows staged-diff privacy review.
- `publication-plan`: PASS — branch, base, files and later readback gates are
  listed in the local handoff.

## AI cost

| Model | Input | Cached input (subset) | Uncached input | Output | Total tokens | Known-model API-equivalent cost |
|---|---:|---:|---:|---:|---:|---:|
| `gpt-6.1-sol` | 2,169,809 | 2,092,160 | 77,649 | 13,221 | 2,183,030 | $0.49672400 |
| `gpt-6-luna` | 6,636,876 | 6,427,776 | 209,100 | 52,820 | 6,689,696 | $0.11159776 |
| **Total** | **8,806,685** | **8,519,936** | **286,749** | **66,041** | **8,872,726** | **$0.60832176** |

Method: `task-ai-cost/1` plus independent per-response recomputation. Finite
cutoff: 2026-10-24T12:12:05Z. Coverage is partial: three GUI turns and two CLI
sessions produced 118 assigned response records. Later work is excluded.
Automatic-review counters were not present in the inspected session streams;
the separately checked review directory was absent, so this usage is
unavailable, not zero. Official OpenAI API Standard rates were checked on
2026-10-24; every request was below the 272,000 input-token long-context
threshold. Cache-write counters were present and zero for all 118 records.
This is API-equivalent pricing, not actual API spend or subscription cost.
Sources: [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol),
[GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna),
[API pricing](https://developers.openai.com/api/docs/pricing).

## Publication and recovery

[Wiki guide](https://github.com/mhaduk/ck3-dynasty-map/wiki/Diagnostic-review)
and the Wiki Home T-group totals are published and verified. The issue retains
its original scope and checked acceptance criteria, with the per-model cost
table and ai-cost-table-format label. Repository indexes reflect this closeout.

The original GUI handoff incorrectly owned a directory; a file-based receipt
repair preserved that FAILED attempt. Subsequent GUI adversarial review found
the dangling-output-link and null-input defects; the accepted correction adds
exclusive writes and typed validation with dedicated negative tests. During
publication, a trailing-newline difference initially stopped issue-hash
comparison; content comparison established unchanged remote scope. Future
handoffs should preflight output types and distinguish transport newline
normalization from substantive drift. Private packets, session snapshots,
baselines and failed results remain local for audit; no raw evidence is
published and no disposable T-015 workspace artifact was identified.
