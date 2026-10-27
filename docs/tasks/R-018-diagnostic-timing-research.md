# R-018 — Research reliable elapsed timing for Dynasty Map

Status: OPEN / deferred research, requested 2026-10-23. Timer measurement is explicitly removed from F-004 / #29 and does not block its diagnostics tests.

## Question and reused evidence
Can the installed target build provide a reliable real-time interval from a map-icon callback through relationship computation and color preparation? Can presentation completion be measured separately?
F-004 bounded review found profiler/frame values but no documented paired synchronous monotonic clock or presentation-completion event. This is a bounded negative finding, not proof that no solution exists. Reuse those findings rather than repeat broad searches.

## Bounded analysis and acceptance
- Inspect narrowly documented target-build APIs, shipped profiler usage and supported instrumentation alternatives; record build and generated-document provenance.
- Distinguish dispatch, computation, paint preparation, selection and actual presentation; state units, resolution, overhead and scope boundaries.
- Never substitute game time, frame duration, coarse log timestamps or file-arrival delay for precise callback elapsed time.
- Return a source-grounded feasible design with a minimal validation plan, or a justified unsupported/unknown disposition and a concrete remaining question. GUI owns architecture and trade-offs.
- No implementation, installation or game test is authorized by this planning record; user alone operates CK3. No automatic scans, gameplay changes or lifecycle waiver.

## Successor
F-006 will implement only a GUI-approved feasible result. F-004 continues independently without a timer requirement.

Issue: [#38](https://github.com/mhaduk/ck3-dynasty-map/issues/38).
