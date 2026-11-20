# Learning Evidence Core

Suppose I finish a Python exercise while someone tells me exactly what to type. Who passed the exercise — me or the person whispering the answers?

I didn't want a learning tracker that gave us both the same gold star. This Python module records **assisted practice** separately from **independent evidence** for one skill at a time.

## Who actually solved it?

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

“Refresh due” is a reminder to check the skill again, not an invitation to repeat the easiest example until it files a complaint. [Provenance](PROVENANCE.md).
