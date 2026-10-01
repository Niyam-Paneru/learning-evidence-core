from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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

    def __post_init__(self) -> None:
        if not self.skill.strip():
            raise ValueError("skill_required")
        if not isinstance(self.help_level, int) or self.help_level < 0:
            raise ValueError("help_level_must_be_non_negative_integer")
        if self.at.tzinfo is None or self.at.utcoffset() is None:
            raise ValueError("attempt_time_must_be_timezone_aware")

    def kind(self) -> EvidenceKind:
        return EvidenceKind.PRACTICE if self.help_level > 0 else EvidenceKind.QUALIFYING
