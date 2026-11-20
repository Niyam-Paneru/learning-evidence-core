# Learning Evidence Core

If I finish a programming problem while someone tells me what to type, did I learn it?

Maybe. But giving that attempt the same score as solving it alone would make my tutor an exceptionally successful student.

This Python module tracks **assisted practice** separately from **independent evidence** for one skill at a time.

## What each attempt proves

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

## Not a whole learning platform

No hosted lessons, login, student history service, or private Learning OS application is included. This is the **evidence rule engine**.

If it says “refresh due,” that's not an insult. It's just a better study plan than endlessly replaying the exercise you already remember. [Provenance](PROVENANCE.md).
