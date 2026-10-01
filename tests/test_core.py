import unittest
from datetime import datetime, timedelta, timezone

from learning_evidence.core import Attempt, EvidenceKind, Mastery, classify_attempt, mastery_for, project_can_promote


BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


class LearningEvidenceTests(unittest.TestCase):
    def test_material_help_is_practice(self):
        attempt = Attempt("pointers", BASE, correct=True, help_level=1)
        self.assertEqual(classify_attempt(attempt), EvidenceKind.PRACTICE)

    def test_independent_attempt_is_qualifying(self):
        attempt = Attempt("pointers", BASE, correct=True, help_level=0)
        self.assertEqual(classify_attempt(attempt), EvidenceKind.QUALIFYING)

    def test_wrong_independent_attempt_does_not_create_mastery(self):
        attempt = Attempt("pointers", BASE, correct=False, help_level=0)
        self.assertEqual(mastery_for("pointers", [attempt], now=BASE), Mastery.PRACTICE)

    def test_one_independent_success_is_qualified(self):
        attempt = Attempt("pointers", BASE, correct=True, help_level=0)
        self.assertEqual(mastery_for("pointers", [attempt], now=BASE), Mastery.QUALIFIED)

    def test_two_successes_without_spacing_are_not_durable(self):
        attempts = [
            Attempt("pointers", BASE, correct=True),
            Attempt("pointers", BASE + timedelta(hours=2), correct=True),
        ]
        self.assertEqual(
            mastery_for("pointers", attempts, now=BASE + timedelta(hours=2)),
            Mastery.QUALIFIED,
        )

    def test_spaced_independent_successes_become_durable(self):
        attempts = [
            Attempt("pointers", BASE, correct=True),
            Attempt("pointers", BASE + timedelta(days=2), correct=True),
        ]
        self.assertEqual(
            mastery_for("pointers", attempts, now=BASE + timedelta(days=3)),
            Mastery.DURABLE,
        )

    def test_old_durable_evidence_becomes_refresh_due(self):
        attempts = [
            Attempt("pointers", BASE, correct=True),
            Attempt("pointers", BASE + timedelta(days=2), correct=True),
        ]
        self.assertEqual(
            mastery_for("pointers", attempts, now=BASE + timedelta(days=40)),
            Mastery.REFRESH_DUE,
        )

    def test_assisted_project_completion_does_not_promote(self):
        attempt = Attempt("api-design", BASE, correct=True, help_level=2, project_completion=True)
        self.assertFalse(project_can_promote(attempt))

    def test_independent_project_completion_can_count(self):
        attempt = Attempt("api-design", BASE, correct=True, help_level=0, project_completion=True)
        self.assertTrue(project_can_promote(attempt))

    def test_unrelated_skill_evidence_is_ignored(self):
        attempts = [Attempt("python", BASE, correct=True)]
        self.assertEqual(mastery_for("c", attempts, now=BASE), Mastery.UNSEEN)


if __name__ == "__main__":
    unittest.main()
