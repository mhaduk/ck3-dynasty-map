# R-005 — Missing-player entry contract review

Date: 2026-10-20. Status: static review complete; entry safety unresolved.
Target: the recorded CK3 1.20.1.1 baseline. This review used installed source
and existing generated documentation, with no new dump, game launch, probe
installation or runtime test. Previous successful cases were not repeated.

## New static evidence

| Source in installed game / generated docs | Finding | Limit |
|---|---|---|
| `common/scripted_guis/pam_scripted_guis.txt:2–28`; `gui/window_pam_christian_church.gui:52,115,191,196,1058,1093` | Great Schism query entries omit `scope`; callers use `IsShown(GuiScope.End)` without explicitly setting a root. | These are query calls, not `Execute`, and the surrounding window supplies data contexts. This does not prove empty-root execution or absent-player safety. |
| `common/scripted_guis/tgp_scripted_guis.txt:35–39`; `data_types_uncategorized.txt:20020–20023` | `HasAccessToMinistry` calls an entry without declared `scope`, adding named `owner` rather than setting a root; the entry uses optional named-scope traversal. | Supports a candidate named-input design for queries only. Does not establish a safe null input, an empty root or effect dispatch. |
| `data_types_gui.txt:15–18`; `data_types_script.txt:4279–4281` | `GuiScope` returns the GUI top Jomini scope; `TopScope.End` returns `TopScope`. | Omitting `SetRoot` does not itself establish that the resulting scope has no root. Do not describe `GuiScope.End` as a guaranteed empty-scope constructor. |
| `data_types_script.txt:3735–3737,3944–3970` | `Scope.IsSet` returns bool; `Execute` returns void; `IsShown` and `IsValid` return bool. | No argument-evaluation order or conditional dispatch guarantee is documented by these signatures. |
| `data_types_common.txt:98–101,1320–1408` | `And` and typed `Select_*` functions are exposed. | Return types and boolean descriptions do not document lazy argument evaluation. Wrapping a character-scoped query in `And` is not an established safety boundary. |
| `triggers.log:600–602` | `exists` checks a target against the null object and lists `Supported Scopes: none`. | This is trigger metadata, not documentation that a scripted-GUI declaration accepts `scope = none`, or that its validator can enter safely with a null character root. The earlier runtime failure still applies. |

A bounded inspection of the nine installed `game/common/scripted_guis/*.txt`
files found nine top-level entries without an explicit `scope`; none contained
an `effect` block. Searching installed `game/gui` call sites found no
`Execute(GuiScope.End)` or `Execute(GuiScope.AddScope(...))` example. These are
negative findings within that source set, not proof that such execution is
unsupported. No scripted-GUI schema documenting the omitted-scope default was
found in the inspected source.

## Working conclusion

Keep two separate hypotheses:

1. Prevent dispatch into a character-scoped entry when there is no player.
   Tested control hiding is useful evidence for ordinary interaction; it does
   not prove evaluation ordering of `enabled`, other bindings, or callbacks
   during context loss. Do not rely on assumed lazy GUI expressions.
2. Use an entry that does not require a character root, then validate a named
   player input before traversing Dynasty. Vanilla query patterns justify
   investigating this, but neither the omitted-scope default nor safe effect
   execution is established. Do not adopt it as production architecture yet.

The conditional root guard inside the existing character entry remains a
failed fix. Do not invoke the existing NULL control again. ADR-008 remains
unchanged; R-005 and RG-PLAYER-01 remain open. No-Dynasty local-player UI is a
separate unresolved case. R-009 owns color restoration.

## Smallest future probe, if runtime investigation is requested

This review originally proposed the scope below. A subsequent source-only
preparation is in [entry-contract probe v1](../../../research/probes/player-entry-contract/README.md).
It has not been installed or run; its actual behavior remains unverified.

- Isolate a new diagnostic from the existing NULL/SUCCESSION controls. Use an
  independent GUI context, an entry without declared character scope, and only
  fixed log markers plus scope inspection. No Dynasty traversal or gameplay
  writes in its first revision.
- First establish actual input scope and whether query/effect entry is accepted
  in a genuinely absent-player context. Do not infer an empty root from the
  spelling `GuiScope.End`, and do not reuse the failing character entry.
- Only after that boundary is established, separately evaluate the proposed
  named-player input and guard. An unset named input and a null Character
  converted with `MakeScope` are distinct cases; one must not stand in for the
  other. Guard acceptance alone does not prove safe `Execute` behavior.
- Treat a validation error, unexpected inherited root or missing effect marker
  as an unresolved/failed contract, not a pass. Stop rather than retrying the
  same diagnostic. Any later successful safe rejection still needs a valid
  input control for the new entry, not repeats of old switch/lifecycle tests.

No runtime cycle is requested now. Next is review of the prepared source before
a runtime decision; no-Dynasty player UI still needs a
verified playable fixture independently.
