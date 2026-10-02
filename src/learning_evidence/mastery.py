from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timedelta, timezone

from .models import Attempt, EvidenceKind, Mastery


def _validate_thresholds(
    *,
    min_independent_successes: int,
    min_spacing: timedelta,
    refresh_after: timedelta,
) -> None:
    if not isinstance(min_independent_successes, int) or isinstance(min_independent_successes, bool):
        raise ValueError("min_independent_successes_must_be_integer")
    if min_independent_successes < 1:
        raise ValueError("min_independent_successes_must_be_positive")
    if min_spacing < timedelta(0):
        raise ValueError("min_spacing_must_be_non_negative")
    if refresh_after < timedelta(0):
        raise ValueError("refresh_after_must_be_non_negative")


def mastery_for(
    skill: str,
    attempts: Iterable[Attempt],
    *,
    now: datetime | None = None,
    min_independent_successes: int = 2,
    min_spacing: timedelta = timedelta(days=1),
    refresh_after: timedelta = timedelta(days=30),
) -> Mastery:
    _validate_thresholds(
        min_independent_successes=min_independent_successes,
        min_spacing=min_spacing,
        refresh_after=refresh_after,
    )

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

    spaced_successes: list[Attempt] = []
    for attempt in independent_successes:
        if not spaced_successes or attempt.at - spaced_successes[-1].at >= min_spacing:
            spaced_successes.append(attempt)
            if len(spaced_successes) >= min_independent_successes:
                break

    if len(spaced_successes) < min_independent_successes:
        return Mastery.QUALIFIED

    latest_qualifying_success = independent_successes[-1].at
    if now - latest_qualifying_success > refresh_after:
        return Mastery.REFRESH_DUE

    return Mastery.DURABLE
