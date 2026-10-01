import unittest
from datetime import datetime, timezone

from learning_evidence.evidence import classify_attempt, project_can_promote
from learning_evidence.models import Attempt, EvidenceKind


BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


class EvidenceTests(unittest.TestCase):
    def test_help_turns_success_into_practice_evidence(self):
        attempt = Attempt("pointers", BASE, correct=True, help_level=1)
        self.assertEqual(classify_attempt(attempt), EvidenceKind.PRACTICE)

    def test_independent_success_is_qualifying(self):
        attempt = Attempt("pointers", BASE, correct=True)
        self.assertEqual(classify_attempt(attempt), EvidenceKind.QUALIFYING)

    def test_assisted_project_does_not_auto_promote(self):
        attempt = Attempt("api-design", BASE, correct=True, help_level=2, project_completion=True)
        self.assertFalse(project_can_promote(attempt))

    def test_negative_help_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "help_level"):
            Attempt("pointers", BASE, correct=True, help_level=-1)

    def test_blank_skill_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "skill_required"):
            Attempt("   ", BASE, correct=True)

    def test_naive_attempt_time_is_rejected(self):
        naive = datetime(2026, 1, 1)
        with self.assertRaisesRegex(ValueError, "timezone_aware"):
            Attempt("pointers", naive, correct=True)


if __name__ == "__main__":
    unittest.main()
