"""Render the compact grouped AI-cost summary for the Wiki Home page."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import re
from typing import List, Optional


HEADERS = ("Type", "Closed tasks", "Total tokens", "Cached tokens", "API cost")
CAVEAT = (
    "Totals are approximate and based on measured usage; some historical tasks "
    "may have incomplete coverage."
)


@dataclass(frozen=True)
class Group:
    kind: str
    closed_tasks: int
    total_tokens: Optional[int]
    cached_tokens: Optional[int]
    known_usd: Optional[Decimal]


def _cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def render_table(groups: List[Group]) -> str:
    kinds = [group.kind for group in groups]
    if not kinds or len(set(kinds)) != len(kinds):
        raise ValueError("groups must be nonempty and unique")
    rows = [
        "| " + " | ".join(HEADERS) + " |",
        "|---|---:|---:|---:|---:|",
    ]
    for group in groups:
        rows.append("| " + " | ".join((
            _cell(group.kind),
            str(group.closed_tasks),
            _number(group.total_tokens),
            _number(group.cached_tokens),
            _money(group.known_usd),
        )) + " |")
    total = Group(
        "**Total**",
        sum(group.closed_tasks for group in groups),
        _known_sum([g.total_tokens for g in groups]),
        _known_sum([g.cached_tokens for g in groups]),
        sum((g.known_usd or Decimal(0) for g in groups), Decimal(0)),
    )
    rows.append("| " + " | ".join((
        total.kind,
        f"**{total.closed_tasks}**",
        f"**{_number(total.total_tokens)}**",
        f"**{_number(total.cached_tokens)}**",
        f"**{_money(total.known_usd)}**",
    )) + " |")
    return "\n".join(rows)


def _known_sum(values: List[Optional[int]]) -> Optional[int]:
    known = [value for value in values if value is not None]
    return sum(known) if known else None


def _number(value: Optional[int]) -> str:
    return "N/A" if value is None else f"{value:,}"


def _money(value: Optional[Decimal]) -> str:
    if value is None:
        return "N/A"
    rounded = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"${rounded:,.2f}"


def replace_summary(markdown: str, groups: List[Group]) -> str:
    """Replace only the summary block and its one-line caveat."""
    heading = "## AI cost estimates"
    if markdown.count(heading) != 1:
        raise ValueError("expected exactly one AI cost estimates section")
    start = markdown.index(heading) + len(heading)
    match = re.search(r"\n\n\| Group \| Task \|", markdown[start:])
    if not match:
        raise ValueError("detailed per-task table boundary not found")
    detail_start = start + match.start()
    return markdown[:start] + "\n\n" + render_table(groups) + "\n\n" + CAVEAT + markdown[detail_start:]
