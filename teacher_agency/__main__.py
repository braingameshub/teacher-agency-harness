"""Run one of the four coordination skills.

From the repo root:

    py -3.12 -m teacher_agency
    py -3.12 -m teacher_agency --action accept
    py -3.12 -m teacher_agency --task differentiate --teacher-input "Use a tape diagram"
    py -3.12 -m teacher_agency --task coordinate --stalled --prior-move "Assign another set of practice problems."
    py -3.12 -m teacher_agency --task check --action accept
    py -3.12 -m teacher_agency --demo-mismatch
"""

import argparse
import json
import sys

from teacher_agency.harness import UNGUIDED_MOVE, Harness
from teacher_agency.tasks import TASKS, run_task

TASK_LABEL = {
    "adapt": "adapt the next move from a named misconception",
    "differentiate": "differentiate the next move using the teacher's own input",
    "coordinate": "coordinate a new move when the teacher reports no progress",
    "check": "set one shared improvement check and record the teacher's decision",
}


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Teacher Agency Harness")
    parser.add_argument("--id", help="Misconception id. Defaults to the first shipped pair.")
    parser.add_argument("--list", action="store_true", help="List the shipped misconception ids.")
    parser.add_argument("--task", choices=TASKS, default="adapt")
    parser.add_argument("--teacher-input", help="Required for --task differentiate. The teacher's own words.")
    parser.add_argument(
        "--stalled",
        action="store_true",
        help="Required for --task coordinate. The teacher reports that the student is not progressing.",
    )
    parser.add_argument("--prior-move", help="Required for --task coordinate. The previous move.")
    parser.add_argument("--action", choices=("accept", "edit", "stop"))
    parser.add_argument("--move", help="Replacement move text. Required with --action edit.")
    parser.add_argument("--demo-mismatch", action="store_true", help="Show the flag on an unguided move.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of text.")
    args = parser.parse_args(argv)

    harness = Harness()
    if args.list:
        for item in harness.list_ids():
            proposal = harness.propose(item)
            print(f"{item}  {proposal.misconception}")
        return 0

    try:
        result = run_task(
            args.task,
            harness,
            misconception_id=args.id,
            teacher_input=args.teacher_input,
            stalled=True if args.stalled else False,
            prior_move=args.prior_move,
            action=None if args.demo_mismatch else args.action,
            edited_move=args.move,
        )
    except (ValueError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.demo_mismatch:
        flag = harness.check(result.proposal, UNGUIDED_MOVE)
        payload = {
            "task": result.task,
            "unguided_move": UNGUIDED_MOVE,
            "flagged": flag.flagged,
            "reason": flag.reason,
            "evidence": result.proposal.evidence,
        }
        _emit(payload, args.json, _mismatch_text(payload))
        return 0

    if result.decision is not None:
        payload = {"task": result.as_dict(), "decision": result.decision.as_dict()}
        _emit(payload, args.json, _decision_text(result, result.decision))
        return 0

    _emit(result.as_dict(), args.json, _proposal_text(result))
    return 0


def _emit(payload, as_json, text):
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(text)


def _proposal_text(result):
    proposal = result.proposal
    return "\n".join(
        [
            "Teacher Agency Harness",
            f"Task: {TASK_LABEL[result.task]}.",
            "",
            "Evidence",
            proposal.evidence,
            "",
            "Proposed next move",
            proposal.next_move,
            "",
            "Flag",
            proposal.flag.reason,
            "",
            "Source",
            proposal.attribution,
            proposal.license,
            "",
            "Teacher control: py -3.12 -m teacher_agency --action accept",
            'Or --action edit --move "..."    Or --action stop',
        ]
    )


def _decision_text(result, decision):
    lines = [
        f"Task: {TASK_LABEL[result.task]}.",
        f"Decision: {decision.status}",
        f"Proceeds: {'yes' if decision.proceeds else 'no'}",
        "Stored student record: no",
    ]
    if decision.move:
        lines.extend(["", "Move that stands", decision.move])
    if decision.flag is not None:
        lines.extend(["", "Flag", decision.flag.reason])
    lines.extend(["", "Evidence", result.proposal.evidence])
    return "\n".join(lines)


def _mismatch_text(payload):
    return "\n".join(
        [
            "Unguided move",
            payload["unguided_move"],
            "",
            "Flag",
            payload["reason"],
            "",
            "Evidence the unguided move ignored",
            payload["evidence"],
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
