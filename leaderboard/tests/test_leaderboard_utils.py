import os
import unittest

from leaderboard.leaderboard_utils import (
    filter_by_period,
    filter_by_query,
    load_leaderboard,
    sort_rows,
)


class LeaderboardUtilsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        cls.csv_path = os.path.join(root, "leaderboard", "leaderboard.csv")
        with open(cls.csv_path, "r") as f:
            cls.header_line = f.readline().strip()
        cls.rows = load_leaderboard(cls.csv_path)

    def test_header(self):
        self.assertEqual(self.header_line.split(","), ["team", "accuracy", "submitted_at"])

    def test_sort_accuracy_desc(self):
        if not self.rows:
            self.skipTest("Leaderboard vide")
        sorted_rows = sort_rows(self.rows, key="accuracy", descending=True)
        max_accuracy = max(row["accuracy"] for row in self.rows)
        self.assertEqual(sorted_rows[0]["accuracy"], max_accuracy)

    def test_filter_query(self):
        if not self.rows:
            self.skipTest("Leaderboard vide")
        sample = self.rows[0]["team"]
        result = filter_by_query(self.rows, sample[:1])
        self.assertGreaterEqual(len(result), 1)

    def test_filter_period_all(self):
        result = filter_by_period(self.rows, "all")
        self.assertEqual(len(result), len(self.rows))


if __name__ == "__main__":
    unittest.main()
