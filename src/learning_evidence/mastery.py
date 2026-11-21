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

    if now is None:
        now = datetime.now(timezone.utc)
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now_must_be_timezone_aware")
    now = now.astimezone(timezone.utc)

    # Normalize before comparing: same-zone datetime arithmetic can use wall
    # time instead of elapsed time across daylight-saving transitions.
    rows: list[tuple[datetime, Attempt]] = []
    for attempt in attempts:
        if attempt.skill != skill:
            continue
        instant = attempt.at.astimezone(timezone.utc)
        if instant <= now:
            rows.append((instant, attempt))
    rows.sort(key=lambda row: row[0])

    if not rows:
        return Mastery.UNSEEN

    independent_successes = [
        instant
        for instant, attempt in rows
        if attempt.correct and attempt.kind() is EvidenceKind.QUALIFYING
    ]

    if not independent_successes:
        return Mastery.PRACTICE

    spaced_successes: list[datetime] = []
    for instant in independent_successes:
        if not spaced_successes or instant - spaced_successes[-1] >= min_spacing:
            spaced_successes.append(instant)
            if len(spaced_successes) >= min_independent_successes:
                break

    if len(spaced_successes) < min_independent_successes:
        return Mastery.QUALIFIED

    latest_qualifying_success = independent_successes[-1]
    if now - latest_qualifying_success > refresh_after:
        return Mastery.REFRESH_DUE

    return Mastery.DURABLE
