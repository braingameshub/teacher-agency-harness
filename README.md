# Teacher Agency Harness

Four coordination skills a developer can run. An Eedi misconception goes in. A proposed next move comes out. The teacher can accept it, edit it, or stop it.

This is the open package for the K-12 AI Infrastructure Program request, Integrating Digital Public Goods to Advance AI-Enabled Formative Assessment. It is not an award, not a pilot, and not a score.

Code is Apache-2.0. The eight-pair data excerpt is CC BY 4.0, copyright 2026 Eedi Ltd. The developer note, the benchmark specification, and the safety note are CC BY 4.0. See NOTICE.

## Run

From this directory, with Python 3.12:

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

No API key. No network call at run time. No install step.

## What the four skills do

The skills are the four coordination tasks in that request.

1. Adapt. The misconception, and the construct the graph says it hinders.
2. Differentiate. The same pair, plus a line the teacher typed. A move that drops that line is flagged.
3. Coordinate. Runs only when the teacher reports no progress and passes the previous move. The new move must not be that previous move. The harness does not infer a stall.
4. Check. One shared check that names the construct and the misconception. Accept, edit, or stop is kept in memory for that run.

On every skill:

- Evidence is shown.
- The proposed next move is a fixed template that names the misconception and the construct. A developer replaces `proposed_move` in `teacher_agency/harness.py` with their own model. The rest of the harness stays.
- The flag is a literal name check, not a judgment of teaching quality.
- Accept keeps the proposed move and proceeds.
- Edit proceeds with the teacher's text. If that text drops a required name, the flag stays visible.
- Stop does not proceed.

An unguided move, "Assign another set of practice problems.", is flagged. The template move is not.

`teacher_agency/adapter.py` loads the excerpt and refuses a NonCommercial, ShareAlike, or NoDerivatives license.

## Data

`data/eedi_sample.json` holds eight real `hinders` edges from the Eedi Misconceptions Graph in the Learning Commons Knowledge Graph, export v1.15.0, retrieved 16 October 2026.

The edges were kept when the misconception and the construct share a topic word, so the link is visible in a short demo. Other edges in the graph are not less valid. The excerpt is aggregated misconception text. It is not a student record and it is not the full graph.

The Kaggle Eedi competition files are CC BY-NC 4.0. They are not in this repository and the loader will refuse a NonCommercial or ShareAlike record.

To refresh the excerpt from the open export:

```
py -3.12 scripts/fetch_sample.py
```

That download is about a gigabyte of graph files. The script keeps eight pairs and does not write the full files.

## What this repository does not do

It does not call Learning Commons standards, the Math Coherence Map, EssayJudge, or GSM8k. Those remain Phase 1 calls in the proposal. They are not wired here.

There is no benchmark score. `docs/BENCHMARK-SPEC.md` defines the comparison and reports no number. There is no school count. There is no letter from a developer. No ALA assessment product is required to run it.

The notes for a developer, the benchmark, and safety are in `docs/`.

## License

Code: Apache License 2.0. Copyright 2026 Advanced Learning Academy LLC.

Data excerpt: CC BY 4.0. Copyright 2026 Eedi Ltd. Attribute Eedi and Learning Commons. The attribution string from the graph is on each pair.
