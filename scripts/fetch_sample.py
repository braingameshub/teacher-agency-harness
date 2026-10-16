"""Pull eight Eedi pairs from the open Knowledge Graph.

The full export is hundreds of megabytes. This script keeps eight
misconception-construct pairs and does not write the full files.
The Kaggle Eedi competition files are CC BY-NC 4.0 and are not used.
"""

import json
import sys
import urllib.request
from pathlib import Path

NODES = "https://cdn.learningcommons.org/knowledge-graph/v1.15.0/exports/nodes.jsonl"
EDGES = "https://cdn.learningcommons.org/knowledge-graph/v1.15.0/exports/relationships.jsonl"
CC_BY = "https://creativecommons.org/licenses/by/4.0/"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "eedi_sample.json"
PAIRS = 8


def stream(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ALA-teacher-agency-harness/1.0"})
    read = 0
    last = 0
    with urllib.request.urlopen(req, timeout=120) as resp:
        for raw in resp:
            read += len(raw)
            if read - last >= 40_000_000:
                print(f"read_mb {read // 1_000_000} {url.rsplit('/', 1)[-1]}", flush=True)
                last = read
            yield raw
    print(f"done_mb {read // 1_000_000} {url.rsplit('/', 1)[-1]}", flush=True)


def props(node):
    return node.get("properties") or {}


def keep_node(node):
    labels = node.get("labels") or []
    if "Misconception" not in labels and "Construct" not in labels:
        return None
    fields = props(node)
    license_url = fields.get("license") or ""
    if "creativecommons.org/licenses/by/4.0" not in license_url:
        return None
    if "by-nc" in license_url or "by-sa" in license_url:
        return None
    description = (fields.get("description") or "").strip()
    attribution = (fields.get("attributionStatement") or "").strip()
    if not description or not attribution or "Eedi" not in attribution:
        return None
    return {
        "id": node.get("identifier") or fields.get("identifier"),
        "label": "Misconception" if "Misconception" in labels else "Construct",
        "description": description,
        "license": CC_BY,
        "attribution": attribution,
        "author": fields.get("author") or "",
        "publisher_identifier": fields.get("publisherIdentifier") or "",
    }


def words(text):
    token = []
    found = []
    for char in text.casefold():
        if char.isalpha():
            token.append(char)
        elif token:
            found.append("".join(token))
            token = []
    if token:
        found.append("".join(token))
    return [word for word in found if len(word) >= 4]


def shares_topic(left, right):
    """Demo filter only. The edge is still a real hinders edge from the graph."""
    left_words = words(left)
    right_words = words(right)
    for one in left_words:
        for other in right_words:
            if len(one) >= 5 and len(other) >= 5 and (one.startswith(other[:5]) or other.startswith(one[:5])):
                return True
    left_pairs = {f"{left_words[i]} {left_words[i + 1]}" for i in range(len(left_words) - 1)}
    right_pairs = {f"{right_words[i]} {right_words[i + 1]}" for i in range(len(right_words) - 1)}
    return bool(left_pairs & right_pairs)


def main():
    nodes = {}
    for raw in stream(NODES):
        if b"Misconception" not in raw and b"Construct" not in raw:
            continue
        try:
            node = json.loads(raw)
        except json.JSONDecodeError:
            continue
        kept = keep_node(node)
        if kept and kept["id"]:
            nodes[kept["id"]] = kept
    print(f"nodes_kept {len(nodes)}", flush=True)

    pairs = []
    seen = set()
    for raw in stream(EDGES):
        if b"hinders" not in raw:
            continue
        try:
            edge = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if edge.get("label") != "hinders":
            continue
        source = edge.get("source_identifier")
        target = edge.get("target_identifier")
        left = nodes.get(source)
        right = nodes.get(target)
        if not left or not right:
            continue
        if left["label"] != "Misconception" or right["label"] != "Construct":
            continue
        if source in seen:
            continue
        if not shares_topic(left["description"], right["description"]):
            continue
        seen.add(source)
        pairs.append(
            {
                "misconception_id": left["id"],
                "misconception": left["description"],
                "construct_id": right["id"],
                "construct": right["description"],
                "license": CC_BY,
                "attribution": left["attribution"],
                "author": left["author"] or "Eedi",
                "misconception_publisher_identifier": left["publisher_identifier"],
                "construct_publisher_identifier": right["publisher_identifier"],
            }
        )
        print(f"pair {len(pairs)}", flush=True)
        if len(pairs) >= PAIRS:
            break

    if len(pairs) < PAIRS:
        print(f"SHORT {len(pairs)}", flush=True)
        return 1

    document = {
        "dataset": "Eedi Misconceptions Graph",
        "graph_version": "v1.15.0",
        "retrieved": "2026-10-16",
        "dataset_page": "https://docs.learningcommons.org/knowledge-graph/datasets/learning-components/eedi-misconceptions-graph",
        "nodes_url": NODES,
        "edges_url": EDGES,
        "license": CC_BY,
        "copyright": "Copyright 2026 Eedi Ltd",
        "note": (
            "Eight real hinders edges from the open graph. "
            "Kept when the misconception and the construct share a topic word, so a reviewer can see the link. "
            "Other real edges are not less valid. This is not the full graph and it is not a student record. "
            "The Kaggle competition files are not included."
        ),
        "pairs": pairs,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(document, indent=2), encoding="utf-8")
    print(f"wrote {OUT} pairs {len(pairs)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
