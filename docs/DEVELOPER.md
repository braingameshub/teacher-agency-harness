# Developer note

Copyright 2026 Advanced Learning Academy LLC. Licensed under CC BY 4.0.
https://creativecommons.org/licenses/by/4.0/

This note is for a developer who already ships a tutor, a feedback tool, or a classroom dashboard. The harness is the layer you drop in. It is not a new product, and it does not require an Advanced Learning Academy assessment.

## What you can run today

Python 3.12. No install. No API key. No network call.

```
py -3.12 -m teacher_agency
py -3.12 -m teacher_agency --action accept
py -3.12 -m teacher_agency --action edit --move "Your replacement"
py -3.12 -m teacher_agency --action stop
py -3.12 -m teacher_agency --task differentiate --teacher-input "Use a tape diagram"
py -3.12 -m teacher_agency --task coordinate --stalled --prior-move "Assign another set of practice problems."
py -3.12 -m teacher_agency --task check --action accept
py -3.12 -m teacher_agency --demo-mismatch
py -3.12 -m unittest discover -s tests -v
```

The four skills match the four tasks in Integrating Digital Public Goods to Advance AI-Enabled Formative Assessment.

1. Adapt. A named misconception and the construct it hinders go in. A proposed next move comes out.
2. Differentiate. The same pair, plus a line the teacher typed. The move must keep that line.
3. Coordinate. Runs only when the teacher reports that the student is not progressing, and only when the teacher passes the previous move. The new move must not be that previous move. The harness does not infer a stall.
4. Check. One shared check that names the construct and the misconception. Accept, edit, or stop is held in memory for that run. Nothing is written to disk.

Each skill shows the evidence, the proposed next move, and the three controls.

## Where your model goes

Replace `proposed_move` in `teacher_agency/harness.py`, or pass your own text through `Harness.propose_text`. Keep the evidence, the flag, and accept / edit / stop. The template is a stand-in so the package runs with no key. It is not a claim that the wording is research-validated.

The flag is a literal check. The move must contain the misconception sentence and the construct sentence. On differentiate it must also contain the teacher's line. On coordinate it must not be the previous move with only case differences. A flagged edit still proceeds, because the teacher chose it. Stop is how a move is blocked.

## License gate

`teacher_agency/adapter.py` loads the eight-pair excerpt and refuses a NonCommercial, ShareAlike, or NoDerivatives license. CC BY 4.0, Apache-2.0, and MIT pass. The excerpt is CC BY 4.0, copyright 2026 Eedi Ltd. It is aggregated misconception text. It is not a student record. The Kaggle Eedi files are CC BY-NC 4.0 and are not in this repository.

## What is not wired

Learning Commons standards and crosswalks, the Math Coherence Map, EssayJudge, and GSM8k are named as Phase 1 calls in the proposal. They are not wired in this repository. Bridge, TalkMoves, MRBench, SAGE/SemEval, and DrawEduMath are not shipped. Their licenses do not meet the RFP rule for a vendored file.

## Rogers checks this repository can show

- Observability. Run one skill and read the evidence, the move, and the flag.
- Trialability. No account and no key.
- Complexity. One Python package and one sample file.
- Quality assurance. `docs/BENCHMARK-SPEC.md` defines the comparison. No score is claimed.
- Relative advantage. `--demo-mismatch` shows the same evidence beside an unguided move that names neither the misconception nor the construct.

There is no letter in this repository from a company that has agreed to try the harness.
