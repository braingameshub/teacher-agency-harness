"""Named evidence in, a proposed next move out, teacher control.

The move text is a deterministic template. A developer replaces
`proposed_move` with their own model. The harness still shows the
evidence, flags a move that drops a required name or repeats the previous
move, and records accept, edit, or stop. No student record is read or written.
"""

from teacher_agency.sample import load_sample

UNGUIDED_MOVE = "Assign another set of practice problems."


def proposed_move(misconception, construct):
    return (
        f'Revisit "{construct}". '
        f'The error pattern to name is "{misconception}". '
        f'Give one short check on "{construct}" that fails if "{misconception}" is still in place.'
    )


class Proposal:
    def __init__(self, pair, next_move, also_require=None, forbid_exact=None):
        self.misconception_id = pair["misconception_id"]
        self.misconception = pair["misconception"]
        self.construct_id = pair["construct_id"]
        self.construct = pair["construct"]
        self.attribution = pair["attribution"]
        self.license = pair["license"]
        self.also_require = list(also_require or [])
        self.forbid_exact = forbid_exact
        self.evidence = (
            f'Misconception: {self.misconception}. '
            f'This hinders the construct: {self.construct}.'
        )
        self.next_move = next_move
        self.flag = flag_move(self, next_move)

    def as_dict(self):
        return {
            "misconception_id": self.misconception_id,
            "misconception": self.misconception,
            "construct_id": self.construct_id,
            "construct": self.construct,
            "evidence": self.evidence,
            "next_move": self.next_move,
            "flagged": self.flag.flagged,
            "missing": list(self.flag.missing),
            "license": self.license,
            "attribution": self.attribution,
        }


class Flag:
    def __init__(self, missing):
        self.missing = tuple(missing)
        self.flagged = bool(missing)
        if self.missing == ("repeated move",):
            self.reason = "The move repeats the previous move."
        elif "repeated move" in self.missing:
            others = [name for name in self.missing if name != "repeated move"]
            self.reason = (
                "The move repeats the previous move and does not name the "
                + " and ".join(others)
                + "."
            )
        elif self.flagged:
            names = " and ".join(self.missing)
            self.reason = f"The move does not name the {names}."
        else:
            self.reason = "The move names the misconception and the construct."


class Decision:
    def __init__(self, status, move, proceeds, flag):
        self.status = status
        self.move = move
        self.proceeds = proceeds
        self.flag = flag

    def as_dict(self):
        return {
            "status": self.status,
            "move": self.move,
            "proceeds": self.proceeds,
            "flagged": None if self.flag is None else self.flag.flagged,
            "reason": None if self.flag is None else self.flag.reason,
        }


def flag_move(proposal, move_text):
    text = (move_text or "").casefold()
    missing = []
    if proposal.misconception.casefold() not in text:
        missing.append("misconception")
    if proposal.construct.casefold() not in text:
        missing.append("construct")
    for label, required in getattr(proposal, "also_require", ()):
        if required.casefold() not in text:
            missing.append(label)
    forbid = getattr(proposal, "forbid_exact", None)
    if forbid and text.strip() == forbid.casefold().strip():
        missing.append("repeated move")
    return Flag(missing)


class Harness:
    def __init__(self, catalog=None, sample_path=None):
        rows = catalog if catalog is not None else load_sample(sample_path)
        self.by_id = {}
        for row in rows:
            key = row["misconception_id"]
            if key in self.by_id:
                raise ValueError(f"Duplicate misconception id {key}")
            self.by_id[key] = row

    def list_ids(self):
        return list(self.by_id)

    def pair(self, misconception_id):
        found = self.by_id.get(misconception_id)
        if found is None:
            raise KeyError(f"Unknown misconception id {misconception_id}")
        return found

    def propose(self, misconception_id):
        pair = self.pair(misconception_id)
        return Proposal(pair, proposed_move(pair["misconception"], pair["construct"]))

    def propose_text(self, misconception_id, move, also_require=None, forbid_exact=None):
        return Proposal(
            self.pair(misconception_id),
            move,
            also_require=also_require,
            forbid_exact=forbid_exact,
        )

    def first(self):
        return self.propose(self.list_ids()[0])

    def check(self, proposal, move_text):
        return flag_move(proposal, move_text)

    def decide(self, proposal, action, edited_move=None):
        choice = (action or "").strip().lower()
        if choice == "accept":
            return Decision("accepted", proposal.next_move, True, proposal.flag)
        if choice == "edit":
            replacement = (edited_move or "").strip()
            if not replacement:
                raise ValueError("An edit needs the teacher's replacement move.")
            return Decision("edited", replacement, True, flag_move(proposal, replacement))
        if choice == "stop":
            return Decision("stopped", None, False, None)
        raise ValueError("Action must be accept, edit, or stop.")
