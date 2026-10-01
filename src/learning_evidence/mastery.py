from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timedelta, timezone

from .models import Attempt, EvidenceKind, Mastery


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
    rows = sorted((attempt for attempt in attempts if attempt.skill == skill), key=lambda a: a.at)

    if not rows:
        return Mastery.UNSEEN

    independent_successes = [
        attempt
        for attempt in rows
        if attempt.correct and attempt.kind() is EvidenceKind.QUALIFYING
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
