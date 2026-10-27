# R-002 — Installed map-mode definitions

Status: DONE

CK3 build: 1.20.1.1 (Crozier)

Completed: 2026-10-20

## Goal

Inspect the installed vanilla map-mode definitions relevant to a barony-color mode.

## Result

The native `baronies` map mode uses `color_mode = baronies`. This confirms the native definition structure inspected for this build, not custom file loading, custom selection, or safe temporary rendering.

## Verified findings

- The installed map-mode definitions include named map-mode objects and a native baronies renderer.
- Format documentation supports the inspected definition structure.
- Custom map-mode loading and runtime rendering remain unverified and are tracked by R-009/R-010.

## Unsupported / failed approaches

- No custom mode was validated by this static inspection.

## Unknowns

- Whether the proposed custom definition loads from a separate file and renders safely.

## Decision

Keep custom loading and renderer behavior behind the existing research gates; no architecture change resulted.

## Evidence

- [R-002 findings](../RESEARCH.md#verified--r-002-installed-map-mode-definitions-2026-10-20)
- Installed vanilla reference summarized there: `game/gfx/map/map_modes/map_modes.txt`, native `baronies` object.
- GitHub Issue #2.

## Impact

Informed the candidate map-mode definition in ARCHITECTURE.md; no implementation authorized.

## Full investigation

GitHub Issue #2 in the public repository.

<!-- ai-cost:start -->
## AI cost

| Model | Input total | Cached input (subset) | Uncached input | Output total | Reasoning output (subset) | Total tokens | Coverage |
|---|---:|---:|---:|---:|---:|---:|---|
| gpt-6.1-sol | 1170615 | 1142016 | 28599 | 4005 | 112 | 1174620 | partial |
| **Total** | 1170615 | 1142016 | 28599 | 4005 | 112 | 1174620 | partial |

Method: task-ai-cost/1; evidence cutoff: 2026-10-22T13:15:22Z. Measured response counters only; cached input and reasoning output are subsets, not addends. Uncached input = input minus cached input; total = input plus output where recorded.
Coverage is partial: only explicitly evidenced task turns and linked reviews are allocated; ambiguous usage and missing history are not estimated. Only the explicit definitions-investigation and closure turn is allocated; earlier shared research remains unallocated. This backfill job is assigned to T-002 and excluded from these historical totals. No currency or quota inference.
<!-- ai-cost:end -->