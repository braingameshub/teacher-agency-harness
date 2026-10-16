"""License gate for a published dataset.

Ships CC BY 4.0, Apache-2.0, and MIT. Refuses NonCommercial, ShareAlike,
and NoDerivatives. This adapter loads the shipped Eedi excerpt only.
It does not download standards, the coherence map, EssayJudge, or GSM8k.
"""

from teacher_agency.sample import load_sample

_BLOCK = ("by-nc", "noncommercial", "by-sa", "sharealike", "by-nd", "noderivatives")
_ALLOW = (
    "creativecommons.org/licenses/by/4.0",
    "apache.org/licenses/license-2.0",
    "opensource.org/licenses/mit",
    "opensource.org/license/mit",
)
_EXACT = {"apache-2.0", "mit", "cc-by-4.0", "cc by 4.0"}


def assert_shippable(license_text):
    raw = (license_text or "").strip()
    folded = raw.casefold()
    if not folded:
        raise ValueError("A license is required before a dataset can ship.")
    if any(token in folded for token in _BLOCK):
        raise ValueError(
            "A NonCommercial, ShareAlike, or NoDerivatives dataset cannot ship in this package."
        )
    if any(fragment in folded for fragment in _ALLOW) or folded in _EXACT:
        return raw
    raise ValueError("The license is not CC BY 4.0, Apache-2.0, or MIT.")


class EediSampleAdapter:
    """Phase 1 adapter for the eight-pair excerpt already in this repository."""

    name = "eedi-misconceptions-excerpt"

    def load(self, path=None):
        rows = load_sample(path)
        for row in rows:
            assert_shippable(row["license"])
        return rows
