from __future__ import annotations

from .models import Attempt, EvidenceKind


def classify_attempt(attempt: Attempt) -> EvidenceKind:
    return attempt.kind()


def project_can_promote(attempt: Attempt) -> bool:
    return (
        attempt.project_completion
        and attempt.correct
        and attempt.kind() is EvidenceKind.QUALIFYING
    )
