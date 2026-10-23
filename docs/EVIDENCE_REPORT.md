# Offline evidence inventory

For side-by-side comparison of two explicitly pinned format-1 CK3 log-delta
metadata manifests, see [Saved checkpoint metadata comparison](CHECKPOINT_COMPARISON.md).
That report compares declared fields only; it cannot establish generation,
byte continuity, event identity, count deltas or causality.

`scripts/evidence_report.py` creates a deterministic inventory from one explicit
local manifest. It reads only the manifest and its listed files, never searches
for evidence, follows symlinks, contacts a service, or invokes another helper.
Use private package directories and place the new report under `.codex-sync/`.

```sh
python3 scripts/evidence_report.py \
  --root /path/to/private-package \
  --manifest manifest.json \
  --output .codex-sync/reports/example.json
```

The root must already exist as a real absolute path. Resolve it before calling
the tool when a platform exposes temporary or volume paths through symlink
aliases (for example, macOS `/tmp`). The root and every existing ancestor are
checked for symlinks before canonicalization. The manifest and all input paths
are portable, normalized paths relative to that root. Every parent must exist
and be a real directory. Inputs must be regular files; symlink components are rejected. The
output parent must already exist under `.codex-sync/`, and output creation is
exclusive: an existing path is left untouched and reported as an invocation
error. The report is written with private file permissions. Inputs are never
modified.

## Input schema

The manifest is UTF-8 JSON with exactly these top-level and entry keys:

This copyable example generates two deterministic synthetic inputs and computes
their exact pins, so every link endpoint is declared:

```sh
demo_root="$(mktemp -d)"
mkdir -p "$demo_root/.codex-sync" "$demo_root/receipts"
DEMO_ROOT="$demo_root" python3 - <<'PY'
import hashlib, json, os
from pathlib import Path
root = Path(os.environ['DEMO_ROOT']).resolve()
items = [
    ('receipt', 'receipts/child.json', 'handoff-status',
     {'id':'child-1','parent_id':'T-008','attempt':1,'revision':1,'status':'COMPLETED'}),
    ('parent', 'receipts/parent.json', 'handoff-status',
     {'id':'parent-1','parent_id':'T-008','attempt':1,'revision':1,'status':'COMPLETED'}),
]
artifacts = []
for ident, rel, kind, value in items:
    data = (json.dumps(value, separators=(',', ':')) + '\n').encode()
    (root / rel).write_bytes(data)
    artifacts.append({'id':ident,'path':rel,'required':True,'kind':kind,
                      'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
manifest = {'schema':'evidence-inventory-input/1','task_id':'T-008',
            'artifacts':artifacts,
            'links':[{'id':'same-parent','from':{'artifact':'receipt','field':'parent_id'},
                      'to':{'artifact':'parent','field':'parent_id'}}]}
(root / 'manifest.json').write_text(json.dumps(manifest, separators=(',', ':')) + '\n')
PY
python3 scripts/evidence_report.py --root "$(cd "$demo_root" && pwd -P)" \
  --manifest manifest.json --output .codex-sync/report.json
```

Artifact IDs and link IDs are bounded portable tokens. `task_id` is only a label and does
not establish artifact identity. Artifact kinds are `opaque`, `handoff-status`,
`log-delta`, `classification`, and `mod-preflight`. Each artifact requires its expected byte
length and lowercase SHA-256 digest. Duplicate IDs/paths and unknown fields
are rejected. A link compares two explicitly selected fields by exact value
and type; `sha256` selects the observed file digest. Supported fields are
limited to handoff identity/lifecycle fields, the five selected log-delta
fields, selected classification and mod-preflight status fields, or `sha256`.
List-valued findings are never link endpoints.
Links do not infer stage order, causality, identity repair, or semantic
equivalence. In particular, comparing lifecycle and domain status fields
does not make their meanings equivalent.

## Limits and projections

The manifest is capped at 256 KiB, 32 artifacts, 64 links, 64 MiB per file,
128 MiB total declared artifact bytes and attempted artifact-read budget, JSON
nesting depth 64, and 1000 classification batches. Before each artifact read,
the tool reserves the declared-size read ceiling plus one byte for growth
detection. A failed or drifting read keeps its reservation; once the remaining
budget cannot cover another read, later files stay UNKNOWN and inventory is
INCOMPLETE. A single bounded read supplies both the observed size/hash and JSON
projection. File metadata is checked around the read for detected changes; the tool does not
claim an atomic multi-file snapshot or protection against a hostile race.

`opaque` files are pinned without decoding. Do not list raw logs, saves, dumps,
or source files as evidence for this tool. `handoff-status` selects only
`id`, `parent_id`, `attempt`, `revision`, and `status` from the current
unversioned helper shape. `log-delta` accepts producer `format: 1` and selects
checkpoint/baseline IDs plus literal interval, expectation, and observation
statuses, including `COMPLETE_WITH_OPTIONAL_GAPS`. `classification` accepts
producer `schema: 2` and selects its top status, exit code, capture
completeness, and per-batch sequence, availability,
record completeness, classification match, and intended RGB mapping. No
records, names, errors, paths, diagnostics, owners, session values, or
arbitrary source text are exported. These are partial projections, not
exhaustive validation of producer contracts.

### Structured mod preflight

Use the checker's opt-in `--json` mode when the result will be pinned in an
evidence manifest. Default text output remains for people and is not an input
format. The producer writes one versioned object with these top-level fields:

| Field | Allowed values / meaning |
|---|---|
| `schema` | `mod-preflight-result/1` |
| `status` | `PASS`, `FAIL`, `INCOMPLETE`; literal producer verdict |
| `exit_code` | integer `0` or `1`; `PASS` is `0`, the others are `1` |
| `source_coverage` | `COMPLETE` or `INCOMPLETE` file traversal/read coverage |
| `source_files` | nonnegative count of successfully read regular source files |
| `source_version_check` | `NOT_REQUESTED`, `MATCH`, `MISMATCH`, `UNVERIFIED` |
| `installed_requested` | exact boolean; true only when `--installed` was supplied |
| `installed_coverage` | `NOT_REQUESTED`, `COMPLETE`, `INCOMPLETE` |
| `installed_files` | `null` if unrequested; otherwise a nonnegative successfully read file count |
| `installed_version_check` | `NOT_REQUESTED`, `MATCH`, `MISMATCH`, `UNVERIFIED` |
| `comparison` | `NOT_REQUESTED`, `MATCH`, `MISMATCH`, `UNVERIFIED` |
| `findings` | sorted rows `{scope, code, count}`; count is positive |
| `limits` | fixed producer limitation string; never trusted as arbitrary evidence text |

Finding scopes are `source`, `installed`, and `comparison`. The finite producer
codes are `invalid_root`, `misplaced_coa`, `symlink`, `incidental_file`,
`read_error`, `missing_bom`, `duplicate_bom`, `invalid_utf8`,
`bad_loc_header`, `loc_folder_mismatch`, `loc_filename_mismatch`,
`missing_descriptor`, `descriptor_unavailable`, `descriptor_declaration`, `version_mismatch`,
`inventory_missing`, `inventory_extra`, `bytes_mismatch`, and
`traversal_error`. Counts group repeated findings; legacy text still prints
each message in its original order. No payload or machine path, descriptor
content, requested version, or raw error is included in JSON.

`descriptor_unavailable` preserves the legacy missing-descriptor diagnostic
when an incomplete inventory cannot establish whether the descriptor is
present. Invalid roots retain their early diagnostic without a descriptor
finding. `INCOMPLETE` means the checker could not inspect a requested tree
completely, including a missing/non-directory/symlink root, skipped symlink,
or failed traversal/read. Observed policy findings remain present. A fully inspected tree
with a missing descriptor, bad encoding, or version mismatch is `FAIL` with
`COMPLETE` coverage. Without `--expected-version`, the version check is
`NOT_REQUESTED`; missing or malformed `supported_version` when a check was
requested is `UNVERIFIED`. A requested comparison is `UNVERIFIED` if either
tree is incomplete, while observed missing/extra/different entries remain in
the findings. These are file-check facts only.

The adapter projects typed status, exit, coverage, version, comparison,
file-count fields and recognized finding codes/counts. It rejects unsupported
schemas, malformed types/enums, incoherent status/exit pairs, invalid install
combinations, duplicate or unknown finding rows and oversized counts. Safe
recognized fields may remain visible with finite adapter issues; unknown text
is omitted. A bad pin makes all projections untrusted. Declared links compare
selected scalar values by exact type and value. `null` installed counts cannot
resolve a link. The report always adds its own static limitations; it does not
copy the producer's `limits` field. A `COMPLETE` inventory may faithfully
contain preflight `FAIL` or `INCOMPLETE`; inventory exit `0` is not a preflight
pass and never upgrades the source verdict.

This copyable example writes a synthetic payload, captures JSON, pins it, and
builds an inventory without invoking the checker during report consumption:

```sh
demo_root="$(mktemp -d)"
mkdir -p "$demo_root/.codex-sync" "$demo_root/evidence" "$demo_root/payload/gfx"
DEMO_ROOT="$demo_root" python3 - <<'PY'
import os
from pathlib import Path
root = Path(os.environ['DEMO_ROOT']).resolve()
(root/'payload/descriptor.mod').write_text('name = "Demo"\nversion = "1"\nsupported_version = "1.20.1.2"\n')
(root/'payload/gfx/mode.txt').write_bytes(b'\xef\xbb\xbfmode = { }\n')
PY
python3 scripts/check_mod_preflight.py "$demo_root/payload" \
  --expected-version 1.20.1.2 --json > "$demo_root/evidence/preflight.json"
DEMO_ROOT="$demo_root" python3 - <<'PY'
import hashlib, json, os
from pathlib import Path
root = Path(os.environ['DEMO_ROOT']).resolve()
rel = 'evidence/preflight.json'; data = (root/rel).read_bytes()
manifest = {'schema':'evidence-inventory-input/1','task_id':'DEMO',
  'artifacts':[{'id':'preflight','path':rel,'required':True,'kind':'mod-preflight',
    'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}], 'links':[]}
(root/'manifest.json').write_text(json.dumps(manifest, separators=(',', ':'))+'\n')
PY
python3 scripts/evidence_report.py --root "$(cd "$demo_root" && pwd -P)" \
  --manifest manifest.json --output .codex-sync/preflight-report.json
```

## Report meaning and exits

The JSON report has schema `evidence-inventory-report/1`, stable ordering, no
timestamp, and a final newline. It includes pins, selected fields, declared
links, missing/unsupported inputs, review findings, and static limitations.
Hash/size mismatches never contribute trusted upstream fields. Optional
missing or unsupported inputs are visible as gaps. A total attempted-read
budget failure is always `INCOMPLETE`, even for an optional file. Required
unknowns, mismatches, malformed present inputs, detected drift, and mismatched or
unknown declared links prevent inventory completeness.

- `COMPLETE`: all required pins/adapters and declared links resolved.
- `COMPLETE_WITH_OPTIONAL_GAPS`: required inventory resolved; optional inputs
  remain visibly unknown or unsupported.
- `INCOMPLETE`: at least one required uncertainty, input mismatch/defect, or
  failed/unknown declared link remains.

These labels describe inventory integrity only. A complete report may contain
literal upstream `FAILED`, `FAIL`, `INCOMPLETE`, `UNVERIFIED`, or `PASS`
values. There is no aggregate PASS, engine/runtime/storage/RGB/census/causal
verdict, or user acceptance. Exit `0` means report inventory is complete (with
or without optional gaps); exit `2` means an `INCOMPLETE` report was written;
exit `1` means invocation, manifest, or output failure. Exit codes never
reinterpret upstream verdicts.
