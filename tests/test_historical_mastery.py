import unittest
from datetime import datetime, timedelta, timezone

from learning_evidence import Attempt, Mastery, mastery_for


BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


class PointInTimeMasteryTests(unittest.TestCase):
    def test_future_only_attempts_do_not_create_past_mastery(self):
        attempts = [
            Attempt("python", BASE + timedelta(days=2), correct=True),
            Attempt("python", BASE + timedelta(days=4), correct=True),
        ]
        self.assertEqual(mastery_for("python", attempts, now=BASE), Mastery.UNSEEN)

    def test_future_success_cannot_make_a_single_past_success_durable(self):
        attempts = [
            Attempt("python", BASE, correct=True),
            Attempt("python", BASE + timedelta(days=3), correct=True),
        ]
        self.assertEqual(
            mastery_for("python", attempts, now=BASE + timedelta(days=1)),
            Mastery.QUALIFIED,
        )

    def test_future_assisted_attempt_does_not_create_past_practice(self):
        future = Attempt("python", BASE + timedelta(days=10), correct=True, help_level=1)
        self.assertEqual(mastery_for("python", [future], now=BASE), Mastery.UNSEEN)

    def test_future_success_cannot_refresh_expired_mastery_early(self):
        attempts = [
            Attempt("python", BASE, correct=True),
            Attempt("python", BASE + timedelta(days=2), correct=True),
            Attempt("python", BASE + timedelta(days=40), correct=True),
        ]
        self.assertEqual(
            mastery_for(
                "python",
                attempts,
                now=BASE + timedelta(days=35),
                refresh_after=timedelta(days=10),
            ),
            Mastery.REFRESH_DUE,
        )
        self.assertEqual(
            mastery_for(
                "python",
                attempts,
                now=BASE + timedelta(days=40),
                refresh_after=timedelta(days=10),
            ),
            Mastery.DURABLE,
        )

    def test_same_instant_with_different_timezones_is_included(self):
        nepal = timezone(timedelta(hours=5, minutes=45))
        instant = BASE.astimezone(nepal)
        attempt = Attempt("python", instant, correct=True)
        self.assertEqual(mastery_for("python", [attempt], now=BASE), Mastery.QUALIFIED)

    def test_naive_query_clock_is_rejected_even_without_attempts(self):
        with self.assertRaisesRegex(ValueError, "now_must_be_timezone_aware"):
            mastery_for("python", [], now=datetime(2026, 1, 1))


if __name__ == "__main__":
    unittest.main()
