# Verification

Run from the repository root.

```bash
PYTHONPATH=src python -m unittest discover -s tests
python -m compileall -q src
```

The behavior suite checks the evidence-state journey, skill isolation, spacing, configurable thresholds, and the rule that a later correct independent success refreshes recency after durable evidence exists.

CircleCI runs the same behavior suite plus lightweight public-proof file checks. A CI configuration being present is not evidence that a particular commit passed; use the current GitHub check status for that claim.

The historical and strict-input regression suites preserve the original fixes from PRs #4 and #5. `tests/test_elapsed_time.py` additionally checks spring-forward, fall-back, repeated-hour cutoffs, ordering, spacing, refresh boundaries and UTC equivalence. Its IANA-zone tests skip explicitly when timezone data is unavailable; use an environment with the timezone database installed for full coverage.
