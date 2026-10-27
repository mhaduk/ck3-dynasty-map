# F-006 — Implement Dynasty Map diagnostic timer

Status: PLANNED / BLOCKED on R-018 research and GUI design approval; created 2026-10-23 at user request. Timer is outside F-004 / #29.

## Desired behavior
Shift+click logs reliable elapsed execution time alongside the compact summary for the clicked Dynasty view. Top-level Dynasty uses the exact same REALMS implementation as Dynasty Realms. Ordinary click should not gain diagnostic overhead. No debug panel.

## Dependencies and acceptance
- R-018 must establish a feasible real-time source and explicit boundaries, units, precision and overhead; GUI accepts the design before implementation.
- Measure dispatch/computation/paint preparation only where supported. Claim rendering completion only with documented completion evidence; otherwise label it unmeasured.
- Share the implementation across top Dynasty and REALMS; cover all three view backends without additional computation passes solely for timing.
- Preserve Option bounded samples, Shift+Option selected-view read-only audit, guards and cleanup. No selection or color side effects from measurement.
- Meaningful offline checks plus one minimal user-run validation after separate preparation/install approval. No fabricated timings, game-time substitution or profiler-frame values presented as callback duration.

This record grants no immediate implementation, installation or game action. F-004 diagnostics acceptance does not depend on this feature.

Issue: [#39](https://github.com/mhaduk/ck3-dynasty-map/issues/39).
