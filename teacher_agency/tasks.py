"""Four coordination skills on one published excerpt.

The teacher supplies classroom input, a stall report, and the previous
move. The harness does not invent a roster, a stall, or a student record.
"""

from teacher_agency.harness import proposed_move

TASKS = ("adapt", "differentiate", "coordinate", "check")


class TaskResult:
    def __init__(self, task, proposal, decision=None):
        self.task = task
        self.proposal = proposal
        self.decision = decision

    def as_dict(self):
        return {
            "task": self.task,
            "proposal": self.proposal.as_dict(),
            "recorded": None if self.decision is None else self.decision.as_dict(),
            "stores_student_record": False,
        }


def run_task(
    task,
    harness,
    misconception_id=None,
    teacher_input=None,
    stalled=False,
    prior_move=None,
    action=None,
    edited_move=None,
):
    name = (task or "adapt").strip().lower()
    if name not in TASKS:
        raise ValueError("Task must be adapt, differentiate, coordinate, or check.")
    pair_id = misconception_id or harness.list_ids()[0]
    pair = harness.pair(pair_id)

    if name == "adapt":
        proposal = harness.propose(pair_id)
    elif name == "differentiate":
        text = (teacher_input or "").strip()
        if not text:
            raise ValueError("Differentiate needs the teacher's own input.")
        proposal = harness.propose_text(
            pair_id,
            _differentiate_move(pair, text),
            also_require=[("teacher input", text)],
        )
    elif name == "coordinate":
        if stalled is not True:
            raise ValueError(
                "Coordinate runs only when the teacher reports that the student is not progressing."
            )
        prior = (prior_move or "").strip()
        if not prior:
            raise ValueError("Coordinate needs the previous move.")
        proposal = harness.propose_text(
            pair_id,
            _coordinate_move(pair, prior),
            forbid_exact=prior,
        )
    else:
        proposal = harness.propose_text(pair_id, _check_move(pair))

    decision = harness.decide(proposal, action, edited_move) if action else None
    return TaskResult(name, proposal, decision)


def _differentiate_move(pair, teacher_input):
    return (
        f'Revisit "{pair["construct"]}". '
        f'The error pattern to name is "{pair["misconception"]}". '
        f'The teacher asked: "{teacher_input}". '
        f'Give one short check on "{pair["construct"]}" that uses that request '
        f'and fails if "{pair["misconception"]}" is still in place.'
    )


def _coordinate_move(pair, prior):
    candidates = (
        (
            f'Change the representation of "{pair["construct"]}". '
            f'The error pattern that is still in place is "{pair["misconception"]}". '
            f'Use a different worked example on "{pair["construct"]}". '
            f"Do not repeat the previous move."
        ),
        (
            f'Use a diagram for "{pair["construct"]}" instead of the previous wording. '
            f'The error pattern that is still in place is "{pair["misconception"]}". '
            f"The previous move is not reused."
        ),
    )
    folded = prior.casefold().strip()
    for move in candidates:
        if move.casefold().strip() != folded:
            return move
    raise ValueError("The new move matched the previous move.")


def _check_move(pair):
    return (
        f'One shared check on "{pair["construct"]}". '
        f'The check fails if "{pair["misconception"]}" is still in place. '
        f"Record only whether the teacher accepts, edits, or stops this check."
    )


def adapt_template(misconception, construct):
    """The task-1 template. Kept as a named function so a developer can find it."""
    return proposed_move(misconception, construct)
