# Learning Evidence Core

If someone tells me exactly what to type and I get a Python exercise right, I'd love to claim mastery. The person who actually solved it might have opinions.

So I made a learning-evidence module that distinguishes **practice with help** from **doing it independently**. Otherwise you could become a senior engineer by watching someone else type very enthusiastically.

## How much of that gold star is yours?

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

When a skill goes stale, it gets `refresh_due`. Not a punishment — just the system politely asking whether the knowledge still lives in your head or only in your notes. [Provenance](PROVENANCE.md).
