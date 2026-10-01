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

    def kind(self) -> EvidenceKind:
        return EvidenceKind.PRACTICE if self.help_level > 0 else EvidenceKind.QUALIFYING
