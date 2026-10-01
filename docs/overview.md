# Design overview

This repository models a distinction most learning dashboards blur:

**practice is not the same thing as independent evidence.**

Help is useful. Hints are useful. Projects are useful. But a system should not quietly convert “completed with material help” into “mastered independently.”

The public module separates:

- the attempt model;
- evidence classification;
- mastery state over time.

Durable mastery requires repeated independent success with spacing. Old evidence can become refresh-due without pretending the learner never knew the skill.

The private Learning OS adds UI, exercises, RS-1 decisions, AI labs, persistence, and session planning. This repo isolates the evidence contract.
