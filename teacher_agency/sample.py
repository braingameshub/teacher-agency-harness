"""Load the shipped Eedi excerpt. Refuse a record that is not CC BY 4.0."""

import json
from pathlib import Path

CC_BY = "https://creativecommons.org/licenses/by/4.0/"
ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "eedi_sample.json"


def load_sample(path=None):
    source = Path(path) if path else SAMPLE
    if not source.is_file():
        raise FileNotFoundError(
            f"Missing {source}. From the repo root, run: py -3.12 scripts/fetch_sample.py"
        )
    document = json.loads(source.read_text(encoding="utf-8"))
    pairs = []
    for row in document.get("pairs") or []:
        pairs.append(_require_cc_by(row))
    if not pairs:
        raise ValueError(f"{source} has no pairs")
    return pairs


def _require_cc_by(row):
    license_url = row.get("license") or ""
    if "creativecommons.org/licenses/by/4.0" not in license_url:
        raise ValueError("A shipped pair is not CC BY 4.0")
    lowered = license_url.lower()
    if "by-nc" in lowered or "by-sa" in lowered or "noncommercial" in lowered:
        raise ValueError("A NonCommercial or ShareAlike record cannot ship in this package")
    for key in ("misconception_id", "misconception", "construct_id", "construct", "attribution"):
        if not str(row.get(key) or "").strip():
            raise ValueError(f"A shipped pair is missing {key}")
    if "eedi" not in row["attribution"].lower():
        raise ValueError("A shipped pair does not attribute Eedi")
    return {
        "misconception_id": row["misconception_id"].strip(),
        "misconception": row["misconception"].strip(),
        "construct_id": row["construct_id"].strip(),
        "construct": row["construct"].strip(),
        "license": CC_BY,
        "attribution": row["attribution"].strip(),
    }
