import pathlib
import sys
import unittest


PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

# Импорт идёт после добавления папки проекта в sys.path.
from progress_tracker import (  # noqa: E402
    average_gain_per_week,
    completed_rate,
    weight_gain,
    weight_gain_from_history,
)


class ProgressTrackerTests(unittest.TestCase):
    def test_weight_gain(self):
        self.assertEqual(weight_gain(61, 70), 9)
        self.assertEqual(weight_gain(70, 68.5), -1.5)

    def test_average_gain_per_week(self):
        self.assertAlmostEqual(average_gain_per_week(61, 70, 10), 0.9)

    def test_average_gain_rejects_non_positive_weeks(self):
        with self.assertRaises(ValueError):
            average_gain_per_week(61, 70, 0)

    def test_completed_rate(self):
        self.assertEqual(completed_rate([True, True, False, True]), 75.0)

    def test_completed_rate_for_empty_list(self):
        self.assertEqual(completed_rate([]), 0.0)

    def test_weight_gain_from_history(self):
        self.assertEqual(
            weight_gain_from_history([61, 64, 67, 70]),
            9,
        )
    def test_weight_history_rejects_too_few_measurements(self):
        with self.assertRaises(ValueError):
            weight_gain_from_history([])

        with self.assertRaises(ValueError):
            weight_gain_from_history([70])


if __name__ == "__main__":
    unittest.main()
