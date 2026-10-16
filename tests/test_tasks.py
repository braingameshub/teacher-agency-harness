import unittest
from pathlib import Path

from teacher_agency.harness import UNGUIDED_MOVE, Harness
from teacher_agency.sample import load_sample
from teacher_agency.tasks import run_task
from teacher_agency.__main__ import main

PAIR = {
    "misconception_id": "m1",
    "misconception": "Believes the larger denominator is the larger fraction",
    "construct_id": "c1",
    "construct": "Compare fractions with the same numerator",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "attribution": "Test fixture. Not the Eedi graph.",
}


class TaskTests(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(catalog=[PAIR])

    def test_adapt_is_the_default_and_is_not_flagged(self):
        result = run_task("adapt", self.harness)
        self.assertEqual(result.task, "adapt")
        self.assertIsNone(result.decision)
        self.assertFalse(result.proposal.flag.flagged)
        self.assertFalse(result.as_dict()["stores_student_record"])

    def test_differentiate_keeps_the_teacher_words(self):
        result = run_task("differentiate", self.harness, teacher_input="Use a tape diagram")
        self.assertIn("Use a tape diagram", result.proposal.next_move)
        self.assertFalse(result.proposal.flag.flagged)
        dropped = result.proposal.next_move.replace("Use a tape diagram", "a different request")
        flag = self.harness.check(result.proposal, dropped)
        self.assertIn("teacher input", flag.missing)
        self.assertNotIn("misconception", flag.missing)

    def test_differentiate_refuses_a_blank_teacher_line(self):
        with self.assertRaises(ValueError):
            run_task("differentiate", self.harness, teacher_input="  ")

    def test_coordinate_requires_an_explicit_stall_and_a_new_move(self):
        with self.assertRaises(ValueError):
            run_task("coordinate", self.harness, stalled=False, prior_move=UNGUIDED_MOVE)
        result = run_task(
            "coordinate",
            self.harness,
            stalled=True,
            prior_move=UNGUIDED_MOVE,
        )
        self.assertNotEqual(result.proposal.next_move.casefold(), UNGUIDED_MOVE.casefold())
        self.assertFalse(result.proposal.flag.flagged)
        repeated = self.harness.decide(result.proposal, "edit", UNGUIDED_MOVE)
        self.assertIn("repeated move", repeated.flag.missing)
        self.assertFalse(result.as_dict()["stores_student_record"])

    def test_check_records_the_teacher_decision_in_memory(self):
        result = run_task("check", self.harness, action="stop")
        self.assertEqual(result.decision.status, "stopped")
        self.assertFalse(result.decision.proceeds)
        self.assertIsNone(result.decision.move)
        self.assertNotIn("student_id", result.as_dict()["proposal"])

    def test_unknown_task_fails(self):
        with self.assertRaises(ValueError):
            run_task("grade", self.harness)

    def test_shipped_excerpt_runs_all_four_skills(self):
        harness = Harness(catalog=load_sample())
        adapt = run_task("adapt", harness)
        differentiate = run_task("differentiate", harness, teacher_input="Show one worked example")
        coordinate = run_task("coordinate", harness, stalled=True, prior_move=UNGUIDED_MOVE)
        check = run_task("check", harness, action="accept")
        for result in (adapt, differentiate, coordinate, check):
            self.assertFalse(result.proposal.flag.flagged)
        self.assertTrue(check.decision.proceeds)

    def test_cli_keeps_accept_and_refuses_an_unstated_stall(self):
        self.assertEqual(main(["--action", "accept"]), 0)
        self.assertEqual(main(["--task", "coordinate"]), 2)
        self.assertEqual(main(["--task", "check", "--action", "accept"]), 0)


class DocTests(unittest.TestCase):
    def test_required_notes_are_cc_by_and_claim_no_score(self):
        root = Path(__file__).resolve().parents[1] / "docs"
        for name in ("DEVELOPER.md", "BENCHMARK-SPEC.md", "SAFETY-AND-AGENCY.md"):
            text = (root / name).read_text(encoding="utf-8")
            self.assertIn("CC BY 4.0", text)
        bench = (root / "BENCHMARK-SPEC.md").read_text(encoding="utf-8")
        self.assertIn("No score is claimed", bench)
        safety = (root / "SAFETY-AND-AGENCY.md").read_text(encoding="utf-8")
        self.assertIn("stop", safety.casefold())
        developer = (root / "DEVELOPER.md").read_text(encoding="utf-8")
        self.assertIn("not wired", developer.casefold())


if __name__ == "__main__":
    unittest.main()
