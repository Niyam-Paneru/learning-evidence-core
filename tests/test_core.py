import unittest
from datetime import datetime, timedelta, timezone

from learning_evidence import Attempt, Mastery, mastery_for


BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


class LearningJourneyTests(unittest.TestCase):
    def test_assistance_then_spaced_independence_moves_through_honest_states(self):
        attempts = [
            Attempt("pointers", BASE, correct=True, help_level=1),
        ]
        self.assertEqual(
            mastery_for("pointers", attempts, now=BASE),
            Mastery.PRACTICE,
        )

        attempts.append(
            Attempt("pointers", BASE + timedelta(days=1), correct=True, help_level=0)
        )
        self.assertEqual(
            mastery_for("pointers", attempts, now=BASE + timedelta(days=1)),
            Mastery.QUALIFIED,
        )

        attempts.append(
            Attempt("pointers", BASE + timedelta(days=3), correct=True, help_level=0)
        )
        self.assertEqual(
            mastery_for("pointers", attempts, now=BASE + timedelta(days=4)),
            Mastery.DURABLE,
        )

        self.assertEqual(
            mastery_for("pointers", attempts, now=BASE + timedelta(days=40)),
            Mastery.REFRESH_DUE,
        )

    def test_evidence_from_another_skill_does_not_leak(self):
        attempts = [
            Attempt("python", BASE, correct=True),
            Attempt("python", BASE + timedelta(days=2), correct=True),
        ]
        self.assertEqual(
            mastery_for("c", attempts, now=BASE + timedelta(days=3)),
            Mastery.UNSEEN,
        )


if __name__ == "__main__":
    unittest.main()
