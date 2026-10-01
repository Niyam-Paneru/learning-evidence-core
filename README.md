# Learning Evidence Core

A small deterministic Python module for keeping **assisted practice**, **independent evidence**, and **mastery state** separate.

It does not try to be a learning platform. It answers one narrower question: **what does the recorded evidence justify saying right now?**

![Mastery evidence timeline](docs/workflow.svg)

## State rules

`mastery_for()` evaluates attempts for one skill at a time.

| Evidence seen | State |
|---|---|
| No attempts | `unseen` |
| Attempts, but no correct independent success | `practice` |
| At least one correct independent success | `qualified` |
| Enough independent successes with enough spacing | `durable` |
| Durable evidence whose latest qualifying success is too old | `refresh_due` |

The current defaults in `src/learning_evidence/mastery.py` are:

- `min_independent_successes = 2`
- `min_spacing = 1 day`
- `refresh_after = 30 days`

These are **configurable software rules**, not scientifically validated universal thresholds for human learning.

## Concrete example

Using the defaults above for one skill:

| Time | Attempt | Resulting state |
|---|---|---|
| 2026-01-01 | Correct with help | `practice` |
| 2026-01-02 | First correct independent attempt | `qualified` |
| 2026-01-04 | Second correct independent attempt, spaced by 2 days | `durable` |
| 2026-02-10 | No new qualifying attempt; 37 days since the latest one | `refresh_due` |

Assistance still counts as practice evidence. It just does not silently become proof of independent performance.

## Other boundaries enforced by the module

- `help_level > 0` classifies an attempt as practice evidence.
- A correct independent attempt is qualifying evidence.
- Evidence is filtered by skill, so success in one skill cannot promote another.
- An assisted project completion does not auto-promote the underlying skill.
- Attempt timestamps must be timezone-aware and `help_level` cannot be negative.

## Inspect the implementation

- [`src/learning_evidence/models.py`](src/learning_evidence/models.py) — attempt validation and evidence/mastery enums
- [`src/learning_evidence/evidence.py`](src/learning_evidence/evidence.py) — evidence classification and project-promotion boundary
- [`src/learning_evidence/mastery.py`](src/learning_evidence/mastery.py) — state derivation and configurable thresholds
- [`tests/test_core.py`](tests/test_core.py) — end-to-end learning-state journey
- [`tests/test_mastery.py`](tests/test_mastery.py) — repetition, spacing, and refresh behavior

## Verify

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

The CircleCI config runs the same behavior suite after compiling `src/` and checking the public proof files. A CI configuration existing in the repo is not the same thing as a published passing status; check the current commit status on GitHub when judging CI.

## Scope and provenance

This repository is a public extraction of evidence/mastery rules from private Learning OS work. It intentionally excludes learner history, exercises, personal progress, UI state, recordings, and provider integrations. See [`PROVENANCE.md`](PROVENANCE.md) and [`SECURITY.md`](SECURITY.md) for those boundaries.
