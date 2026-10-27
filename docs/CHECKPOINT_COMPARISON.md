# Saved checkpoint metadata comparison

`scripts/ck3_log_compare.py` compares exactly two explicitly pinned JSON
manifests emitted by `scripts/ck3_log_delta.py`. It reads the two manifest
files only. It never follows their embedded paths or opens captured log bytes.
The comparison is a private summary: retained message fingerprints may enable
correlation and must stay under `.codex-sync/`.

The envelope has schema `checkpoint-comparison-input/1`; each side pins one
repository-relative path, exact byte length and lowercase SHA-256:

```json
{
  "schema": "checkpoint-comparison-input/1",
  "left": {"path": "evidence/left.json", "bytes": 123, "sha256": "<64 lowercase hex characters>"},
  "right": {"path": "evidence/right.json", "bytes": 456, "sha256": "<64 lowercase hex characters>"}
}
```

Replace the example lengths and hashes with the exact pins for the two files.
Both paths are relative to the explicit root. Reusing one path on both sides is
allowed for an identical-input check. Do not generate pins by discovering
nearby files or by reading paths embedded in a report.

```sh
python3 scripts/ck3_log_compare.py --root /path/to/evidence-root \
  --manifest comparison-input.json \
  --output .codex-sync/checkpoint-comparison.json
```

The output parent must already exist below `.codex-sync/`; the destination is
created exclusively with mode `0600`. Existing outputs and symlinks are
refused. Inputs are immutable. Envelope and source JSON sizes are bounded at
64 KiB and 1 MiB respectively; at most 16 log entries and 250 retained
fingerprints per input are projected. The unchanged
`scripts/evidence_report.py` supplies root/path, regular-file, bounded JSON,
duplicate-key and nesting checks; it is an implementation dependency only and
is not run as a command. Public-only use therefore requires both scripts.

## Reading the result

The output schema is `checkpoint-comparison-result/1`. `metadata_status` is
`COMPLETE` when both pins and selected fields are structurally usable. It does
not mean that the upstream interval was complete or that semantic comparisons
are possible. Input pin mismatches, unsupported selected fields, malformed
counts, invalid ranges, duplicate fingerprints and inconsistent summary sums
produce an `INCOMPLETE` report with finite issue codes. Safe valid fields may
remain visible. A valid upstream `interval_status: INCOMPLETE` is preserved
literally and is not reclassified as invalid metadata.

Coverage flags are trusted only when they have the expected boolean type. A
malformed or unavailable selected flag makes summary coverage `UNKNOWN` and
dependent range/digest relations `UNKNOWN`; it is never treated as a clean
false flag. Missing optional source-row flags retain the producer's false
default, while a well-typed `true` flag makes coverage `PARTIAL`. Missing or
malformed required per-log analysis fragment metadata also prevents clean
coverage. Correctly pinned source bytes with invalid JSON produce an
`INCOMPLETE` report and exit `2`; the verified peer remains available and no
parser diagnostic or source path is copied into the report.

For a matching standard log name, `declared_range_relation` describes only
the reported half-open numeric coordinates. `declared_digest_equality`
compares SHA-256 fields declared by the reports. Neither field proves that the
captures came from the same file generation or that their bytes can be
combined. Gaps, partial rows and inconsistent captures make dependent range
and digest observations `UNKNOWN`. Per-log analyzed-line counts and the global
analyzed-line total retain explicit scope and reported/summary coverage. Counts
remain side-by-side; the tool never subtracts them. Global retained fingerprint rows describe membership in the
two retained summaries, not appearance, disappearance, event identity, or
per-log attribution. An unavailable or invalid fingerprint summary yields
`null` overlap rather than an empty set.

`generation_relation` and `byte_continuity` are always `UNKNOWN`; `new_bytes`,
`count_delta`, and `new_error_count` are always `null`; `event_identity` and
`causality` are always `UNPROVEN`. Equal IDs, offsets, digests, counts or
fingerprints do not change these fixed non-claims. The report also carries
fixed limits about sampled boundaries, non-atomic per-log capture, missing
engine/storage/RGB/census evidence, ordinary drift checks (which do not rule
out hostile concurrent replacement) and the private nature of fingerprint
summaries. No aggregate PASS is emitted.

Exit `0` means a structurally usable report was written, even if the source
manifest itself says `INCOMPLETE`. Exit `2` means an incomplete metadata report
was written. Exit `1` means invocation, envelope, path or output failure and
no report is retained. Standard output contains only a short write receipt;
errors do not echo source text or paths.

The frozen examples `startup-append.json` and `load-delta.json` remain private
handoff inputs and are not reproduced here. Their smoke command and result are
recorded in the local implementation dossier.
