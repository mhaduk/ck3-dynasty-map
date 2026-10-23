# F-001 — paused-session resume checkpoint

Updated 2026-10-23. **OPEN / PARTIAL; paused explicitly by the user.** Work on
other tasks may proceed. Do not automatically resume F-001, create a new CLI
handoff, repeat game tests or mark it complete.

## Minimal startup for a future session

Read AGENTS.md, CURRENT_STATE and TASK_HISTORY, then this checkpoint and the
[current canonical result](F-001-dynasty-map-ux.md). Read only the relevant
follow-up section, rather than reconstructing the full experiment history.
Resume only when the user explicitly selects F-001 again.

## Published and verified

- Partial implementation: [263eb2a](https://github.com/mhaduk/ck3-dynasty-map/commit/263eb2a8f880ae39b4edd5fa8292fc846ec5d958), branch `research/native-menu-alternative`.
- One Dynasty parent, three native-style subviews, selected icons/legends and
  accepted grey/green appearance. F-003 semantics remain fixed.
- Click computes/displays; Shift adds summary; Option/Alt adds bounded samples;
  Shift+Option audits all three without changing the active map. Ctrl adds no
  separate action. Callback receipts and user-visible operation were observed.
- Retired tracing/tester/experimental paths stay removed. Two inert compatibility
  definition files and six names were restored; the package has nine files.
- 33 tests and complete source/installed equality passed in the final CLI and
  independent GUI receipt. Main-menu mount/version/GUI gate passed on 1.20.1.2.
- CLI cycle31 published an honest partial result. Its lifecycle is FAILED for
  unmet closure, reviewed by GUI; do not attempt a successful consume or rebase.

## What actually blocks closure

Two unnamed `Duplicate landed title name` errors persist when loading the
reviewed session. Three earlier named missing-template errors no longer occur.
Cause, affected titles, save-history relationship and persistence/RGB impact
remain unknown. User-visible success does not establish safe compatibility.

The next substantive decision, when resumed, is a bounded disposition of those
**two remaining load errors**, coordinated with F-005/R-009. Do not blindly
restore old diagnostic execution, edit saves, or assume the cause. Request new
runtime evidence only when a precise missing observation justifies it and the
user authorizes the stage. Last observed app state was a user-loaded paused
session; current app state must not be inferred or checked through processes/UI.

## Remaining owners and nonblocking historical limits

- [F-005 / #30](https://github.com/mhaduk/ck3-dynasty-map/issues/30): the load
  blocker, functional/UX coverage, unmeasured roughly one-second click latency,
  final icons and compatibility acceptance. [Local matrix](F-005-functional-followups.md).
- [F-004 / #29](https://github.com/mhaduk/ck3-dynasty-map/issues/29): positive
  counters exported but localized summaries zero, strict audit INCOMPLETE,
  sample-label formatting, interrupted-batch robustness and concrete court-error
  attribution. No numeric cure has been proven. [Local matrix](F-004-diagnostics-hardening.md).
- R-005/#5 owns context/no-Dynasty research; R-009/#9 owns exact restoration,
  isolation, save/removal. Do not duplicate or silently complete these owners.
- Historical agreement for 14,109 emitted role/intended-RGB records is not a
  global census, stored-color readback, pixel or lifecycle guarantee.

## Accounting and evidence

Measured partial costs and cutoff are preserved in the canonical F-001 record
and #20. Wiki closed-task totals exclude open F-001; do not add it until closure.
No recursive cost refresh is needed merely to read this handoff.

Raw logs, prior journals, exact user replies, original baselines, backups and
publication/accounting receipts are preserved in ignored local handoff storage.
The local GUI_HANDOFF points to exact cycle31 files; never publish that private
material or ask the user to recreate screenshots already retained. #20 contains
this pause disposition and the repair-owner links.
