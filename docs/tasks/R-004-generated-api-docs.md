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
