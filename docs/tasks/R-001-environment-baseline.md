# R-001 — Environment baseline

Status: DONE

CK3 build: 1.20.1.1 (Crozier)

Completed: 2026-10-20

## Goal

Record the installed CK3 version and establish the environment baseline for M0 research.

## Result

The project recorded CK3 1.20.1.1 as its target research baseline. The finding establishes which installed files and generated API documentation the subsequent M0 research refers to. It does not establish compatibility with later builds or complete vanilla runtime cleanliness.

## Verified findings

- The recorded target build is CK3 1.20.1.1 (Crozier).
- Clean API documentation was later generated for this baseline under R-004.
- A clean startup-only vanilla observation does not complete the save/map interaction baseline; R-011 remains partial.

## Unsupported / failed approaches

- None recorded as part of the completed inventory.

## Unknowns

- Compatibility with newer CK3 builds must be researched when the target changes.
- Full vanilla save/map-mode log baseline remains R-011.

## Decision

Use the installed target build and generated API documentation as evidence; do not treat historical examples as target-build verification.

## Evidence

- [Research baseline and clean vanilla follow-up](../RESEARCH.md#r-001--environment-inventory-complete-2026-10-20)
- [Backlog R-001 / Issue #1](../BACKLOG.md)

## Impact

Unblocked target-build-specific inspection and API generation. R-011 remains a separate runtime-baseline task.

## Full investigation

GitHub Issue #1 in the public repository; its investigation history is authoritative for intermediate updates.

<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| gpt-6.1-sol | 289846 | 280320 | 9526 | 2121 | 27 | 291967 | partial |
| **Total** | 289846 | 280320 | 9526 | 2121 | 27 | 291967 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-22T13:15:22Z. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
Coverage is partial: only explicitly evidenced task turns and linked reviews are allocated; ambiguous usage and missing history are not estimated. Only the explicit environment-inventory turn is allocated; shared bootstrap and documentation work remains unallocated. This backfill job is assigned to T-002 and excluded from these historical totals. No currency or quota inference.
<!-- ai-cost:end -->