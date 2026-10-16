import unittest

from teacher_agency.adapter import EediSampleAdapter, assert_shippable


class AdapterTests(unittest.TestCase):
    def test_open_licenses_pass(self):
        assert_shippable("https://creativecommons.org/licenses/by/4.0/")
        assert_shippable("https://www.apache.org/licenses/LICENSE-2.0")
        assert_shippable("https://opensource.org/licenses/MIT")
        assert_shippable("Apache-2.0")
        assert_shippable("MIT")

    def test_closed_licenses_fail(self):
        blocked = (
            "https://creativecommons.org/licenses/by-nc/4.0/",
            "https://creativecommons.org/licenses/by-sa/4.0/",
            "https://creativecommons.org/licenses/by-nc-sa/4.0/",
            "https://creativecommons.org/licenses/by-nd/4.0/",
            "Custom license",
            "",
        )
        for license_text in blocked:
            with self.assertRaises(ValueError):
                assert_shippable(license_text)

    def test_shipped_excerpt_loads_through_the_adapter(self):
        rows = EediSampleAdapter().load()
        self.assertGreaterEqual(len(rows), 8)
        for row in rows:
            self.assertIn("creativecommons.org/licenses/by/4.0", row["license"])
            self.assertNotIn("student_id", row)


if __name__ == "__main__":
    unittest.main()
