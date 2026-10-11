"""Malformed ingestion data cannot silently become independent mastery evidence."""

import unittest
from datetime import datetime, timezone

from learning_evidence import Attempt, Mastery, mastery_for, project_can_promote


AT = datetime(2026, 1, 1, tzinfo=timezone.utc)


class EvidenceInputValidationTests(unittest.TestCase):
    def test_truthy_string_false_must_not_be_accepted_as_correct(self):
        for bad in ("false", "true", 0, 1, None):
            with self.subTest(correct=bad):
                with self.assertRaisesRegex(ValueError, "correct_must_be_boolean"):
                    Attempt("python", AT, correct=bad)

    def test_truthy_string_false_must_not_claim_project_completion(self):
        for bad in ("false", "true", 0, 1, None):
            with self.subTest(project_completion=bad):
                with self.assertRaisesRegex(ValueError, "project_completion_must_be_boolean"):
                    Attempt("python", AT, correct=True, project_completion=bad)

    def test_bool_help_level_is_not_integer_evidence(self):
        for bad in (True, False, 1.5, "0"):
            with self.subTest(help_level=bad):
                with self.assertRaisesRegex(ValueError, "help_level_must_be_non_negative_integer"):
                    Attempt("python", AT, correct=True, help_level=bad)

    def test_invalid_skill_and_timestamp_have_controlled_refusals(self):
        with self.assertRaisesRegex(ValueError, "skill_required"):
            Attempt(None, AT, correct=True)
        with self.assertRaisesRegex(ValueError, "attempt_time_must_be_timezone_aware"):
            Attempt("python", "2026-01-01T00:00:00Z", correct=True)
        with self.assertRaisesRegex(ValueError, "attempt_time_must_be_timezone_aware"):
            Attempt("python", datetime(2026, 1, 1), correct=True)

    def test_proper_boolean_evidence_still_preserves_practice_vs_mastery(self):
        assisted = Attempt("python", AT, correct=True, help_level=1, project_completion=True)
        independent = Attempt("python", AT, correct=True, help_level=0, project_completion=True)
        wrong = Attempt("python", AT, correct=False, help_level=0, project_completion=True)
        self.assertFalse(project_can_promote(assisted))
        self.assertFalse(project_can_promote(wrong))
        self.assertTrue(project_can_promote(independent))
        self.assertEqual(mastery_for("python", [assisted], now=AT), Mastery.PRACTICE)
        self.assertEqual(mastery_for("python", [wrong], now=AT), Mastery.PRACTICE)


if __name__ == "__main__":
    unittest.main()
