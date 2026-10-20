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
- **Recovery:** No mods selected, empty mod-load config and fresh 13:09 runtime
  logs verified; user confirmed successful startup. Expected DLC mounted;
  recovery error.log empty. No full save/removal or map-function test claimed.
- **Current blockers/questions:** compliant native-menu insertion, custom map
  loading, player/Dynasty guards, manual refresh, context-loss/exit restoration,
  map-only color isolation/persistence, runtime performance and Dynasty colors.
  R-011 remains Partial; vanilla test-game errors were archived before the probe.
- **Design:** My Dynasty first; county classification, barony-only writes;
  DIRECT before liege-based CONTROLLED, including no-Dynasty holders. ADR-008
  requires valid player/Dynasty. On-demand refresh; no persistent cache/scans.
  User requires native menu integration; no adjacent overlay selected.
- **Last task:** preserved probe source/history and reviewed failure/recovery
  evidence. [Test record](evidence/2026-10-20-r010-native-menu/README.md).
  Raw evidence stays ignored; do not reinstall the failed source.
- **Single next task:** R-010 research into a materially different original
  native-menu integration mechanism before proposing another probe. No vanilla
  GUI copy/policy relaxation, classifier or color work authorized.
- **Git:** branch research/codex-gui-handoff, based on 5b0efc0 (API findings).
  This snapshot records accumulated handoff/research and the failed probe;
  inspect actual status/history each session. User authorized local commits
  for this record; no push authorized.
