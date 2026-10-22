# R-004 — Generated API documentation

Status: DONE

CK3 build: 1.20.1.1 (Crozier)

Completed: 2026-10-20

## Goal

Generate `script_docs` and `dump_data_types` from the installed target build so research can use current API evidence.

## Result

Clean generated API documentation was produced for CK3 1.20.1.1 and used to verify relevant script signatures and scope links. The generated dumps remain local; only concise original findings are kept in the repository.

## Verified findings

- The clean generated docs support the scope and iterator signatures referenced by R-006 through R-009.
- Generated signatures do not prove runtime visual, lifecycle, or state behavior.

## Unsupported / failed approaches

- Historical or community examples are not substitutes for the generated target-build docs.

## Unknowns

- Runtime behavior is tracked by the dependent research tasks.

## Decision

Keep generated dumps out of Git and record only reviewed, concise findings in RESEARCH.md.

## Evidence

- [R-004 and generated API findings](../RESEARCH.md#verified--ck3-12011-crozier-generated-script_docs)
- GitHub Issue #4.

## Impact

Unblocked target-build API research. R-006/R-007/R-008/R-009 remain distinct in their evidence and completion status.

## Full investigation

GitHub Issue #4 in the public repository.

<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| gpt-6.1-sol | 456581 | 450176 | 6405 | 2239 | 22 | 458820 | partial |
| **Total** | 456581 | 450176 | 6405 | 2239 | 22 | 458820 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-22T13:15:22Z. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
Coverage is partial: only explicitly evidenced task turns and linked reviews are allocated; ambiguous usage and missing history are not estimated. Only the clean generated-document verification turn is allocated; earlier API research overlaps multiple tasks and remains unallocated. This backfill job is assigned to T-002 and excluded from these historical totals. No currency or quota inference.
<!-- ai-cost:end -->