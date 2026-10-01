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


if __name__ == "__main__":
    unittest.main()
