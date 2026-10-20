# Publication privacy audit

Date: 2026-10-20. Scope: tracked files and reachable commit metadata on all
three local project branches, including historical versions of tracked content.
This is not an audit/removal of all private files on the workstation.

## Cleanup performed

- Rewrote four project commits to replace the private author/committer identity
  with public GitHub login `mhaduk` and
  `1523472+mhaduk@users.noreply.github.com`.
- Replaced the machine-specific CK3 user-data root with `${CK3_USER_DATA}` in
  historical documentation. Updated references to rewritten ancestor commits.
- Preserved branch relationships, original dates, research/test content and
  source/screenshot assets. No vanilla files were changed.
- Set project-local Git identity to the public login/noreply address for future
  commits. Global Git configuration is unchanged.
- Scanned every tracked blob and commit metadata reachable from local branches
  for the private identity and home-directory paths. No matches remain in that
  publication scope. Rechecked screenshot EXIF/XMP/ICC metadata: only technical
  image data and Screenshot comments observed, with no identifying/GPS tags.

## Deliberately private or unchanged state

A private, recoverable Git bundle and reference mapping were saved outside the
repository before rewriting. Raw logs/crash report remain under ignored local/.
Local reflogs, unreachable old objects and Codex-managed checkpoint refs were
not purged; they are private recovery/application state, not the publication
scope. No claims are made that these local recovery copies contain no identity.

No push was performed. GitHub and origin remote-tracking refs retain the
previous history, including its original identity/path disclosures. Rewriting
local branches alone does not erase published content. Replacing upstream
history requires a separate explicit publishing decision; even then, external
caches/clones may retain prior content. Ordinary shared log excerpts/screenshots
remain the reviewed evidence, never raw generated API dumps or crash reports.

## Continuation

Use the sanitized local branch history and inspect actual refs/status before any
publication. Keep commits on the project-local public identity. Operational next
task remains R-005 read-only player/Dynasty context and guard research; privacy
cleanup does not approve new mod behavior or a push.
