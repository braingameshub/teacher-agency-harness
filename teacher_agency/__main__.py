"""Run one misconception through the harness.

From the repo root:

    py -3.12 -m teacher_agency
    py -3.12 -m teacher_agency --action accept
    py -3.12 -m teacher_agency --demo-mismatch
"""

import argparse
import json
import sys

from teacher_agency.harness import UNGUIDED_MOVE, Harness


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="One-task Teacher Agency Harness")
    parser.add_argument("--id", help="Misconception id. Defaults to the first shipped pair.")
    parser.add_argument("--list", action="store_true", help="List the shipped misconception ids.")
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

    proposal = harness.propose(args.id) if args.id else harness.first()
    if args.demo_mismatch:
        flag = harness.check(proposal, UNGUIDED_MOVE)
        payload = {
            "unguided_move": UNGUIDED_MOVE,
            "flagged": flag.flagged,
            "reason": flag.reason,
            "evidence": proposal.evidence,
        }
        _emit(payload, args.json, _mismatch_text(payload))
        return 0

    if args.action:
        decision = harness.decide(proposal, args.action, args.move)
        payload = {"proposal": proposal.as_dict(), "decision": decision.as_dict()}
        _emit(payload, args.json, _decision_text(proposal, decision))
        return 0

    _emit(proposal.as_dict(), args.json, _proposal_text(proposal))
    return 0


def _emit(payload, as_json, text):
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(text)


def _proposal_text(proposal):
    return "\n".join(
        [
            "Teacher Agency Harness",
            "Task: adapt the next move from a named misconception.",
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
            "Or --action edit --move \"...\"    Or --action stop",
        ]
    )


def _decision_text(proposal, decision):
    lines = [
        f"Decision: {decision.status}",
        f"Proceeds: {'yes' if decision.proceeds else 'no'}",
    ]
    if decision.move:
        lines.extend(["", "Move that stands", decision.move])
    if decision.flag is not None:
        lines.extend(["", "Flag", decision.flag.reason])
    lines.extend(["", "Evidence", proposal.evidence])
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
