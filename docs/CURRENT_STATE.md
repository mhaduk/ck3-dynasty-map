# Current project state

Updated 2026-10-20. Read after AGENTS.md; synchronize on material changes.

- **Build:** CK3 1.20.1.1 (Crozier), Steam build 25913294; Steam branch UNKNOWN.
  macOS 26.5.2 (25F84), arm64; supplied crash report identifies Mac16,10.
- **Milestone:** M0 research/bootstrap. One inert-menu GUI probe failed at
  startup and is quarantined. No production mod/classifier implemented.
- **Completed:** R-001 inventory, R-002 definitions, R-003 static GUI inspection,
  R-004 clean API generation, R-006 scope signatures. Five Issues closed;
  seven open. [BACKLOG.md](BACKLOG.md) maps planning IDs to GitHub.
- **VERIFIED baseline:** clean docs expose holder/Dynasty/House links,
  county/barony/de-jure iterators and liege traversal excluding self. Color-copy
  effects shift RGB slightly. Installed native baronies renderer exists.
  Signatures are not visual/lifecycle proof. Details: [RESEARCH.md](RESEARCH.md).
- **Failed route:** same-name decoration of the additional-menu type crashed
  in recursive GUI ResolveTypes at startup. Original/installed GUI quarantined
  as .gui.disabled. This attempt is withdrawn; not all integration is disproven.
- **Probe 01 recovery:** historical No mods run at 13:09 succeeded, with expected
  DLC and empty error.log. Current tested session runs only probe 02. No full
  save/removal or map-function test claimed.
- **Current blockers/questions:** full native-menu behavior/regressions, custom map
  loading, player/Dynasty guards, manual refresh, context-loss/exit restoration,
  map-only color isolation/persistence, runtime performance and Dynasty colors.
  R-011 remains Partial; vanilla test-game errors were archived before the probe.
- **Design:** My Dynasty first; county classification, barony-only writes;
  DIRECT before liege-based CONTROLLED, including no-Dynasty holders. ADR-008
  requires valid player/Dynasty. On-demand refresh; no persistent cache/scans.
  User requires native menu integration; no adjacent overlay selected.
- **Last task:** probe 02 placement/tooltip and basic interactions passed in
  user-reported smoke checks: DM inert, native mode switching/return and menu
  open/close work. Faith sub-mode visibility/switching/return also confirmed by
  user. GUI warnings remain empty; error.log contains
  17,413 bytes of errors with attribution unresolved. [Evidence](evidence/2026-10-20-r010-native-menu-02/README.md).
- **Single next task:** R-005 read-only player/Dynasty guard and scripted-GUI
  context research before adding any active My Dynasty control. R-010 remains
  Partial: expanded mini-menu/all-variant/UI-scale coverage, unavailable state,
  refresh and lifecycle pending.
  Existing probe stays inert; no classifier/color work or vanilla edits.
- **Git/privacy:** branch research/native-menu-alternative retains complete
  handoff/test history. Local history was privacy-scrubbed; prior branch bases
  and hashes changed. Sanitized handoff is 13a82c0, probe-02 record 3feefd5.
  Project-local public login/noreply identity configured; global config unchanged.
  [Privacy audit](PRIVACY_AUDIT.md) defines publication scope. User-authorized
  atomic push published sanitized main and both research branches on 2026-10-20.
  No feature merge into main. Old local backup/reflogs/checkpoints stay private;
  upstream caches/clones may retain earlier data. Inspect actual refs/status.
