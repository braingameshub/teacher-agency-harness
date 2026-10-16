import unittest

from teacher_agency.harness import UNGUIDED_MOVE, Harness

PAIR = {
    "misconception_id": "m1",
    "misconception": "Believes the larger denominator is the larger fraction",
    "construct_id": "c1",
    "construct": "Compare fractions with the same numerator",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "attribution": "Test fixture. Not the Eedi graph.",
}


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(catalog=[PAIR])
        self.proposal = self.harness.first()

    def test_proposal_names_the_evidence_and_is_not_flagged(self):
        self.assertIn(PAIR["misconception"], self.proposal.evidence)
        self.assertIn(PAIR["construct"], self.proposal.evidence)
        self.assertIn(PAIR["misconception"], self.proposal.next_move)
        self.assertIn(PAIR["construct"], self.proposal.next_move)
        self.assertFalse(self.proposal.flag.flagged)

    def test_unguided_move_is_flagged(self):
        flag = self.harness.check(self.proposal, UNGUIDED_MOVE)
        self.assertTrue(flag.flagged)
        self.assertEqual(flag.missing, ("misconception", "construct"))

    def test_accept_proceeds_with_the_proposed_move(self):
        decision = self.harness.decide(self.proposal, "accept")
        self.assertEqual(decision.status, "accepted")
        self.assertTrue(decision.proceeds)
        self.assertEqual(decision.move, self.proposal.next_move)

    def test_edit_uses_the_teacher_text_and_still_flags_a_miss(self):
        decision = self.harness.decide(self.proposal, "edit", edited_move="Try a different worksheet.")
        self.assertEqual(decision.status, "edited")
        self.assertTrue(decision.proceeds)
        self.assertEqual(decision.move, "Try a different worksheet.")
        self.assertTrue(decision.flag.flagged)

    def test_edit_can_clear_the_flag(self):
        move = f'Reteach {PAIR["construct"]} because of {PAIR["misconception"]}.'
        decision = self.harness.decide(self.proposal, "edit", edited_move=move)
        self.assertFalse(decision.flag.flagged)

    def test_stop_does_not_proceed(self):
        decision = self.harness.decide(self.proposal, "stop")
        self.assertEqual(decision.status, "stopped")
        self.assertFalse(decision.proceeds)
        self.assertIsNone(decision.move)

    def test_blank_edit_and_unknown_id_fail(self):
        with self.assertRaises(ValueError):
            self.harness.decide(self.proposal, "edit", edited_move="  ")
        with self.assertRaises(KeyError):
            self.harness.propose("missing")


if __name__ == "__main__":
    unittest.main()
