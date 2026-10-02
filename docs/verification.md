# Verification

Run from the repository root.

```bash
PYTHONPATH=src python -m unittest discover -s tests
python -m compileall -q src
```

The behavior suite checks the evidence-state journey, skill isolation, spacing, configurable thresholds, and the rule that a later correct independent success refreshes recency after durable evidence exists.

CircleCI runs the same behavior suite plus lightweight public-proof file checks. A CI configuration being present is not evidence that a particular commit passed; use the current GitHub check status for that claim.
