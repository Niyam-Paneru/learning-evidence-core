# Learning Evidence Core

If I solve a coding exercise with somebody telling me what to type, and it prints the right answer, I've demonstrated at least one skill: typing.

I wanted a learning log that doesn't confuse getting help with getting it. This Python module separates **assisted practice** from independently correct attempts, then checks whether the evidence is recent and repeated.

## How much of that solution was mine?

| What happened | What the module can conclude |
| --- | --- |
| No attempts | unseen |
| An attempt was helped or not independently correct | practice evidence |
| Correct, independently, once | qualified |
| Enough independent successes separated in time | potentially durable |
| No recent independent refresh after the configured window | refresh_due |

The default policy requires **two independent successes at least one day apart** and checks a **30-day refresh window**. Those are configurable **software defaults**, not a claim about how many hours human brains need to master Python.

An assisted solution can be useful practice, but it can't count as independent mastery evidence. Nor does proving one skill magically unlock evidence for another.

Code: [mastery rules](src/learning_evidence/mastery.py), [attempt evidence](src/learning_evidence/evidence.py), [models](src/learning_evidence/models.py), and [tests](tests/). The specific thresholds and behavior checks are in [verification](docs/verification.md).

Historical queries only count attempts at or before the supplied timezone-aware `now`. Spacing and recency use elapsed UTC time, so changing a clock for daylight saving cannot change mastery. Ingestion requires real Boolean success and project flags, a non-negative integer help level, and a timezone-aware attempt timestamp.

## Not a whole learning platform

No hosted lessons, login, student history service, or private Learning OS application is included. This is the **evidence rule engine**.

When a skill goes stale, it gets `refresh_due`. Not a punishment — just the system politely asking whether the knowledge still lives in your head or only in your notes. [Provenance](PROVENANCE.md).
