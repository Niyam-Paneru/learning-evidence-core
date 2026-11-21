# Failure modes

## Assisted work is promoted as mastery
The learner succeeds with material help. Response: record practice evidence, not independent mastery.

## Two rapid successes look durable
Correct attempts happen minutes apart. Response: require spacing before durable mastery.

## Project completion inflates prerequisites
A large project is completed with help and all underlying skills are marked mastered. Response: project evidence does not auto-promote every prerequisite.

## Old mastery is treated as permanent
Evidence ages without a retention check. Response: move to refresh-due.

## Wrong independent attempt disappears
Only successful attempts are considered. Response: the mastery logic still distinguishes practice state from qualifying success.

## Unrelated evidence leaks across skills
Success in one topic affects another. Response: mastery is computed per skill.

## Future attempts rewrite historical mastery
A historical query sees evidence from later dates. Response: only include attempts at or before the aware query instant.

## Wall-clock changes distort spacing and recency
A 23-hour day appears to be 24 hours, or a repeated hour is incorrectly ordered. Response: normalize timestamps to UTC before sorting, filtering, or subtracting.

## Truthy malformed values inflate evidence
The string `"false"` is truthy in Python. Response: require real Boolean flags, a genuine non-negative integer help level, and an aware timestamp at ingestion.
