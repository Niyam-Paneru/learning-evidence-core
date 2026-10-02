import unittest
from datetime import datetime, timedelta, timezone

from learning_evidence.mastery import mastery_for
from learning_evidence.models import Attempt, Mastery


BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


class MasteryTests(unittest.TestCase):
    def test_one_success_is_not_durable(self):
        self.assertEqual(
            mastery_for("pointers", [Attempt("pointers", BASE, correct=True)], now=BASE),
            Mastery.QUALIFIED,
        )

    def test_spacing_matters(self):
        attempts = [
            Attempt("pointers", BASE, correct=True),
            Attempt("pointers", BASE + timedelta(hours=2), correct=True),
        ]
        self.assertEqual(
            mastery_for("pointers", attempts, now=BASE + timedelta(hours=2)),
            Mastery.QUALIFIED,
        )

    def test_spaced_successes_become_durable(self):
        attempts = [
            Attempt("pointers", BASE, correct=True),
            Attempt("pointers", BASE + timedelta(days=2), correct=True),
        ]
        self.assertEqual(
            mastery_for("pointers", attempts, now=BASE + timedelta(days=3)),
            Mastery.DURABLE,
        )

    def test_configured_three_successes_require_spacing_between_counted_successes(self):
        attempts = [
            Attempt("pointers", BASE, correct=True),
            Attempt("pointers", BASE + timedelta(hours=2), correct=True),
            Attempt("pointers", BASE + timedelta(days=2), correct=True),
        ]
        self.assertEqual(
            mastery_for(
                "pointers",
                attempts,
                now=BASE + timedelta(days=3),
                min_independent_successes=3,
                min_spacing=timedelta(days=1),
            ),
            Mastery.QUALIFIED,
        )

    def test_configured_three_spaced_successes_become_durable(self):
        attempts = [
            Attempt("pointers", BASE, correct=True),
            Attempt("pointers", BASE + timedelta(days=1), correct=True),
            Attempt("pointers", BASE + timedelta(days=2), correct=True),
        ]
        self.assertEqual(
            mastery_for(
                "pointers",
                attempts,
                now=BASE + timedelta(days=3),
                min_independent_successes=3,
                min_spacing=timedelta(days=1),
            ),
            Mastery.DURABLE,
        )

    def test_invalid_thresholds_are_rejected(self):
        attempts = [Attempt("pointers", BASE, correct=True)]

        with self.assertRaisesRegex(ValueError, "min_independent_successes"):
            mastery_for("pointers", attempts, min_independent_successes=0)

        with self.assertRaisesRegex(ValueError, "min_spacing"):
            mastery_for("pointers", attempts, min_spacing=timedelta(seconds=-1))

        with self.assertRaisesRegex(ValueError, "refresh_after"):
            mastery_for("pointers", attempts, refresh_after=timedelta(seconds=-1))

    def test_later_independent_success_refreshes_durable_evidence(self):
        attempts = [
            Attempt("pointers", BASE, correct=True),
            Attempt("pointers", BASE + timedelta(days=2), correct=True),
            Attempt("pointers", BASE + timedelta(days=35), correct=True),
        ]
        self.assertEqual(
            mastery_for("pointers", attempts, now=BASE + timedelta(days=40)),
            Mastery.DURABLE,
        )

    def test_old_mastery_becomes_refresh_due(self):
        attempts = [
            Attempt("pointers", BASE, correct=True),
            Attempt("pointers", BASE + timedelta(days=2), correct=True),
        ]
        self.assertEqual(
            mastery_for("pointers", attempts, now=BASE + timedelta(days=40)),
            Mastery.REFRESH_DUE,
        )


if __name__ == "__main__":
    unittest.main()
