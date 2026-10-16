# Teacher Agency Harness

One task a developer can run. An Eedi misconception goes in. A proposed next move comes out. The teacher can accept it, edit it, or stop it.

This is the first slice of an open package for the K-12 AI Infrastructure Program request, Integrating Digital Public Goods to Advance AI-Enabled Formative Assessment. It is not an award, not a pilot, and not a score.

Code is Apache-2.0. The eight-pair data excerpt is CC BY 4.0, copyright 2026 Eedi Ltd. See NOTICE.

## Run

From this directory, with Python 3.12:

```
py -3.12 -m teacher_agency
py -3.12 -m teacher_agency --action accept
py -3.12 -m teacher_agency --action edit --move "Your replacement"
py -3.12 -m teacher_agency --action stop
py -3.12 -m teacher_agency --demo-mismatch
py -3.12 -m unittest discover -s tests -v
```

No API key. No network call at run time. No install step.

## What the task does

The shipped task is the first of the four coordination tasks in that request: adapt the next move from the named misconception.

1. Evidence. The misconception, and the construct the graph says it hinders.
2. Proposed next move. A fixed template that names both. A developer replaces `proposed_move` in `teacher_agency/harness.py` with their own model. The rest of the harness stays.
3. Flag. If a move does not contain the misconception text and the construct text, the harness says so. This is a literal name check, not a judgment of teaching quality.
4. Teacher control.
   - Accept keeps the proposed move and proceeds.
   - Edit proceeds with the teacher's text. If that text drops a name, the flag stays visible.
   - Stop does not proceed.

An unguided move, "Assign another set of practice problems.", is flagged. The template move is not.

## Data

`data/eedi_sample.json` holds eight real `hinders` edges from the Eedi Misconceptions Graph in the Learning Commons Knowledge Graph, export v1.15.0, retrieved 16 October 2026.

The edges were kept when the misconception and the construct share a topic word, so the link is visible in a short demo. Other edges in the graph are not less valid. The excerpt is aggregated misconception text. It is not a student record and it is not the full graph.

The Kaggle Eedi competition files are CC BY-NC 4.0. They are not in this repository and the loader will refuse a NonCommercial or ShareAlike record.

To refresh the excerpt from the open export:

```
py -3.12 scripts/fetch_sample.py
```

That download is about a gigabyte of graph files. The script keeps eight pairs and does not write the full files.

## What this repository is not

The other three tasks are not here. There is no benchmark score. There is no school count. There is no letter from a developer. No ALA assessment product is required to run it.

## License

Code: Apache License 2.0. Copyright 2026 Advanced Learning Academy LLC.

Data excerpt: CC BY 4.0. Copyright 2026 Eedi Ltd. Attribute Eedi and Learning Commons. The attribution string from the graph is on each pair.
