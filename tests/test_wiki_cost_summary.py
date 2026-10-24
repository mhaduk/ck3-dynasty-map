import unittest
from decimal import Decimal

from scripts.wiki_cost_summary import Group, render_table, replace_summary


GROUPS = [
    Group("R", 15, 106_527_859, 102_845_824, Decimal("15.38251664")),
    Group("T", 12, 142_403_414, 138_000_128, Decimal("12.51234988")),
    Group("F", 3, 545_740_537, 531_023_616, Decimal("64.72330606")),
    Group("B", 0, None, None, None),
]


class WikiCostSummaryTests(unittest.TestCase):
    def test_five_columns_and_derived_total(self):
        table = render_table(GROUPS)
        lines = table.splitlines()
        self.assertEqual(lines[0], "| Type | Closed tasks | Total tokens | Cached tokens | API cost |")
        self.assertTrue(all(line.count("|") == 6 for line in lines))
        self.assertEqual(
            lines[-1],
            "| **Total** | **30** | **794,671,810** | **771,869,568** | **$92.62** |",
        )

    def test_missing_values_do_not_become_zero_rows(self):
        table = render_table(GROUPS)
        self.assertIn("| B | 0 | N/A | N/A | N/A |", table)
        self.assertIn("| **Total** | **30** |", table)

    def test_summary_replacement_preserves_details_and_other_sections(self):
        page = "# Home\n\n## Intro\n\nKeep me.\n\n## AI cost estimates\n\nold table\n\n| Group | Task |\n|---|---|\n| R | details |\n"
        result = replace_summary(page, GROUPS)
        self.assertIn("Keep me.", result)
        self.assertIn("| Group | Task |", result)
        self.assertIn("| R | details |", result)
        self.assertEqual(result.count("Totals are approximate"), 1)
        self.assertNotIn("old table", result)

    def test_preserves_order_and_aggregates_extra_group(self):
        groups = GROUPS[::-1] + [Group("X", 1, 10, 4, Decimal("0.005"))]
        lines = render_table(groups).splitlines()
        self.assertTrue(lines[2].startswith("| B |"))
        self.assertTrue(lines[-2].startswith("| X |"))
        self.assertEqual(lines[-1], "| **Total** | **31** | **794,671,820** | **771,869,572** | **$92.62** |")

    def test_wholly_unavailable_tokens_remain_unavailable(self):
        table = render_table([Group("X", 1, None, None, None)])
        self.assertIn("| **Total** | **1** | **N/A** | **N/A** | **$0.00** |", table)

    def test_rejects_empty_or_duplicate_groups(self):
        for groups in ([], [GROUPS[0], GROUPS[0]]):
            with self.assertRaises(ValueError):
                render_table(groups)


if __name__ == "__main__":
    unittest.main()
