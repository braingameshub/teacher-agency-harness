# Teacher-agency benchmark specification

Copyright 2026 Advanced Learning Academy LLC. Licensed under CC BY 4.0.
https://creativecommons.org/licenses/by/4.0/

No score is claimed. No classroom result is claimed. This file defines the comparison. It does not report one.

## Question

When a next move is built from a named misconception and the construct that misconception hinders, does the move keep those names, keep the teacher's own input when the teacher supplied it, and avoid repeating the previous move when the teacher reports no progress?

The comparison is a name-and-control check. It is not a learning gain, not a psychometric result, and not a school outcome.

## Conditions

Use one pair from `data/eedi_sample.json`, or a later pair that passes `assert_shippable`.

- Guided. The move returned by the skill, or the developer's replacement of `proposed_move`.
- Unguided. The constant `Assign another set of practice problems.` A developer may add other unguided texts. An unguided text is any move that was not required to name the pair.

The teacher action is a third record, not a score: accept, edit, or stop.

## What to count

Count these only. Do not convert them into a single score in this specification.

1. Name flag. The guided or unguided move is flagged when it omits the misconception sentence or the construct sentence. On differentiate, also when it omits the teacher's line.
2. Repeat flag. On coordinate, the move is flagged when it matches the previous move after case folding and trimming.
3. Stop. The teacher chose stop, so the move does not proceed.
4. Edited-and-flagged. The teacher replaced the move, the replacement proceeds, and the flag is still on. That count is agency, not a failure of the teacher.

## What not to count

- No percent correct for students.
- No time-on-task.
- No number of schools, teachers, or developers.
- No comparison against a published model score.
- No result from EssayJudge, GSM8k, standards crosswalks, or the Math Coherence Map. Those files are not loaded here.

## When a number would be allowed

A number belongs in a later report, after a developer runs this comparison on a product they ship, and after the program safety review named in the proposal. This repository does not contain that report.

The reference unguided move is flagged on every shipped pair by the tests in this repository. That is a check that the flag fires. It is not a benchmark score.
