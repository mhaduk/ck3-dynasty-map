# Wiki content ownership

The [public Wiki](https://github.com/mhaduk/ck3-dynasty-map/wiki) is maintained in its separate Git repository. It explains and links canonical facts; it does not allocate tasks or define competing product semantics. No generator is required.

| Fact | Canonical owner | Wiki destination |
|---|---|---|
| Three-view names and classification | [F-003](tasks/F-003-dynasty-subview-definitions.md), ADR-010 in [DECISIONS](DECISIONS.md) | Map Views |
| Accepted menu and recomputation behavior | [F-001](tasks/F-001-dynasty-map-ux.md), [rendering guide](F001_MAP_PAINTING.md), current accepted source | Installation & Usage |
| Tested versus supported CK3 version | [Compatibility policy](COMPATIBILITY.md) and bounded runtime evidence | Compatibility & Known Issues |
| Actual release/version/distribution | [T-014/#40](https://github.com/mhaduk/ck3-dynasty-map/issues/40), [versioning](VERSIONING.md), [changelog](../CHANGELOG.md) | Home, Installation & Usage, Releases |
| Known limitations | [F-005](tasks/F-005-functional-followups.md), [R-005](tasks/R-005-player-context.md), [R-009](tasks/R-009-barony-color-safety.md) | Compatibility & Known Issues |
| Architecture and rendering | [Architecture](ARCHITECTURE.md), [rendering guide](F001_MAP_PAINTING.md) | How It Works, Map Rendering |
| Accounting | Saved response evidence and canonical task cost tables; accepted T-013 presentation | AI Cost |
| Accepted AI workflow | [Codex workflow](CODEX_WORKFLOW.md) and linked accepted guides | Development pages |

Home opens with the user-selected Before/After comparison. Map Views starts with native Houses and presents the three Dynasty views with readable illustrations and text. New image links use the explicit raw Wiki image URL. Remove superseded public embeds while preserving historical evidence; keep `F001-Map-Painting` as a compatibility alias to Map Rendering outside primary navigation.

For changes, inventory incoming links, preserve legacy destinations, verify canonical facts, review image privacy and third-party attribution, and validate links plus actual GitHub rendering. Publish only under user authorization, then fetch and compare the remote result. Preserve partial accounting coverage and finite cutoffs; count each newly closed task once and retain historical values unless a separately evidenced correction is authorized. Do not substitute task completion for a release.
