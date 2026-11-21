"""Historical cutoffs and thresholds use elapsed time, not wall-clock labels."""

import unittest
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from learning_evidence import Attempt, Mastery, mastery_for


class ElapsedTimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.zone = ZoneInfo("America/New_York")
        except ZoneInfoNotFoundError:
            raise unittest.SkipTest("IANA timezone data unavailable")

    def test_spring_forward_does_not_turn_23_hours_into_a_day(self):
        first = datetime(2026, 3, 7, 12, tzinfo=self.zone)
        second = datetime(2026, 3, 8, 12, tzinfo=self.zone)
        attempts = [Attempt("python", first, True), Attempt("python", second, True)]
        self.assertEqual(mastery_for("python", attempts, now=second), Mastery.QUALIFIED)

    def test_fall_back_25_elapsed_hours_meets_spacing(self):
        first = datetime(2026, 10, 31, 12, tzinfo=self.zone)
        second = datetime(2026, 11, 1, 12, tzinfo=self.zone)
        attempts = [Attempt("python", first, True), Attempt("python", second, True)]
        self.assertEqual(
            mastery_for("python", attempts, now=second, min_spacing=timedelta(hours=25)),
            Mastery.DURABLE,
        )

    def test_future_repeated_hour_is_not_yet_evidence(self):
        before = datetime(2026, 11, 1, 1, 45, tzinfo=self.zone, fold=0)
        after = datetime(2026, 11, 1, 1, 15, tzinfo=self.zone, fold=1)
        self.assertEqual(
            mastery_for("python", [Attempt("python", after, True)], now=before),
            Mastery.UNSEEN,
        )

    def test_repeated_hour_sorting_and_exact_spacing(self):
        before = datetime(2026, 11, 1, 1, 45, tzinfo=self.zone, fold=0)
        after = datetime(2026, 11, 1, 1, 15, tzinfo=self.zone, fold=1)
        attempts = [Attempt("python", after, True), Attempt("python", before, True)]
        self.assertEqual(
            mastery_for("python", attempts, now=after, min_spacing=timedelta(minutes=30)),
            Mastery.DURABLE,
        )
        self.assertEqual(
            mastery_for("python", attempts, now=after, min_spacing=timedelta(minutes=31)),
            Mastery.QUALIFIED,
        )

    def test_recency_uses_elapsed_hours_through_fall_back(self):
        first = datetime(2026, 10, 29, 12, tzinfo=self.zone)
        latest = datetime(2026, 10, 31, 12, tzinfo=self.zone)
        now = datetime(2026, 11, 1, 12, tzinfo=self.zone)
        attempts = [Attempt("python", first, True), Attempt("python", latest, True)]
        self.assertEqual(
            mastery_for("python", attempts, now=now, refresh_after=timedelta(hours=24)),
            Mastery.REFRESH_DUE,
        )
        self.assertEqual(
            mastery_for("python", attempts, now=now, refresh_after=timedelta(hours=25)),
            Mastery.DURABLE,
        )

    def test_mixed_offsets_produce_same_result_as_utc(self):
        first = datetime(2026, 11, 1, 1, 45, tzinfo=self.zone, fold=0)
        second = datetime(2026, 11, 1, 1, 15, tzinfo=self.zone, fold=1)
        expected = mastery_for(
            "python",
            [Attempt("python", t.astimezone(timezone.utc), True) for t in (first, second)],
            now=second.astimezone(timezone.utc), min_spacing=timedelta(minutes=30),
        )
        actual = mastery_for(
            "python", [Attempt("python", first, True), Attempt("python", second, True)],
            now=second, min_spacing=timedelta(minutes=30),
        )
        self.assertEqual(expected, Mastery.DURABLE)
        self.assertEqual(actual, expected)
