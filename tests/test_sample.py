import unittest

from teacher_agency.harness import Harness
from teacher_agency.sample import load_sample


class SampleTests(unittest.TestCase):
    def test_shipped_excerpt_is_attributed_cc_by(self):
        pairs = load_sample()
        self.assertGreaterEqual(len(pairs), 8)
        harness = Harness(catalog=pairs)
        for pair in pairs:
            self.assertIn("creativecommons.org/licenses/by/4.0", pair["license"])
            self.assertIn("eedi", pair["attribution"].lower())
            proposal = harness.propose(pair["misconception_id"])
            self.assertFalse(proposal.flag.flagged)
            self.assertNotIn("student_id", pair)


if __name__ == "__main__":
    unittest.main()
