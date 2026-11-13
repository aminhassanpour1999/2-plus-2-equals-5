import unittest
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

import two_plus_two as project


class PixelArtTests(unittest.TestCase):
    def test_phrase_and_year_are_explicit(self):
        self.assertEqual(project.PHRASE, "2 + 2 = 5")
        self.assertEqual(project.TARGET_YEAR, 2025)

    def test_bitmap_has_five_rows_and_equal_width(self):
        bitmap = project.build_bitmap()
        self.assertEqual(len(bitmap), 5)
        self.assertTrue(all(len(row) == len(bitmap[0]) for row in bitmap))

    def test_bitmap_width_is_19(self):
        self.assertEqual(len(project.build_bitmap()[0]), 19)

    def test_phrase_is_centered_in_53_week_calendar(self):
        self.assertEqual(project.phrase_start_column(), 17)

    def test_all_pixel_dates_are_in_2025(self):
        dates = project.active_pixel_dates()
        self.assertTrue(dates)
        self.assertTrue(all(date(2025, 1, 1) <= day <= date(2025, 12, 31) for day in dates))

    def test_active_pixel_count_is_44(self):
        self.assertEqual(len(project.active_pixel_dates()), 44)

    def test_pixel_dates_are_unique(self):
        dates = project.active_pixel_dates()
        self.assertEqual(len(dates), len(set(dates)))

    def test_pixels_only_use_monday_through_friday(self):
        self.assertTrue(all(day.weekday() < 5 for day in project.active_pixel_dates()))

    def test_no_2026_dates_are_generated(self):
        self.assertNotIn(2026, {day.year for day in project.active_pixel_dates()})

    @patch("two_plus_two.subprocess.run")
    def test_existing_pixel_batch_is_rejected(self, mocked_run):
        mocked_run.return_value = SimpleNamespace(
            stdout="pixel: 001/044 for 2025"
        )
        with self.assertRaisesRegex(RuntimeError, "already exist"):
            project.ensure_no_existing_pixel_commits()

    @patch("two_plus_two.subprocess.run")
    def test_history_without_pixel_batch_is_allowed(self, mocked_run):
        mocked_run.return_value = SimpleNamespace(stdout="docs: initial commit")
        project.ensure_no_existing_pixel_commits()


if __name__ == "__main__":
    unittest.main()
