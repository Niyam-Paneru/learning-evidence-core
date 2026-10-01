from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Iterable


class EvidenceKind(str, Enum):
    PRACTICE = "practice"
    QUALIFYING = "qualifying"


class Mastery(str, Enum):
    UNSEEN = "unseen"
    PRACTICE = "practice"
    QUALIFIED = "qualified"
    DURABLE = "durable"
    REFRESH_DUE = "refresh_due"


@dataclass(frozen=True)
class Attempt:
    skill: str
    at: datetime
    correct: bool
    help_level: int = 0
    project_completion: bool = False

    def kind(self) -> EvidenceKind:
        if self.help_level > 0:
            return EvidenceKind.PRACTICE
        return EvidenceKind.QUALIFYING


def classify_attempt(attempt: Attempt) -> EvidenceKind:
    return attempt.kind()


def mastery_for(
    skill: str,
    attempts: Iterable[Attempt],
    *,
    now: datetime | None = None,
    min_independent_successes: int = 2,
    min_spacing: timedelta = timedelta(days=1),
    refresh_after: timedelta = timedelta(days=30),
) -> Mastery:
    now = now or datetime.now(timezone.utc)
    rows = sorted((a for a in attempts if a.skill == skill), key=lambda a: a.at)

    if not rows:
        return Mastery.UNSEEN

    independent_successes = [
        a for a in rows
        if a.correct and a.kind() is EvidenceKind.QUALIFYING
    ]

    if not independent_successes:
        return Mastery.PRACTICE

    if len(independent_successes) < min_independent_successes:
        return Mastery.QUALIFIED

    first = independent_successes[0].at
    last = independent_successes[-1].at

    if last - first < min_spacing:
        return Mastery.QUALIFIED

    if now - last > refresh_after:
        return Mastery.REFRESH_DUE

    return Mastery.DURABLE


def project_can_promote(attempt: Attempt) -> bool:
    return (
        attempt.project_completion
        and attempt.correct
        and attempt.kind() is EvidenceKind.QUALIFYING
    )
