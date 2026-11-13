#!/usr/bin/env python3
"""Derive the frozen V6.2 catalogue from the approved V6.1 catalogue.

V6.2 does not grant new prop approvals. It tightens two approved board entries
so wall-mounted boards contain non-legible, nonhuman visual detail instead of
being empty. All other entries and repetition groups remain unchanged.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "v6_1" / "approved-v6.1-20261103.catalog.json"
OUT = HERE / "approved-v6.2-20261106.catalog.json"

VERSION = "hp-v6.2-approved-props-v1"
REVISION = "v6.2-spatial-composition-20261106-r1"

NAME_UPDATES = {
    "V61-OFF-036": "corkboard or pinboard with sparse unlabeled color and texture blocks",
    "V61-EDU-036": "whiteboard with sparse distant non-legible geometric marks",
    "V61-OFF-014": "clear glass paperweight",
}

REMOVED_IDS = {"V61-HOM-014"}


def main() -> None:
    catalog = json.loads(BASE.read_text())
    catalog["version"] = VERSION
    catalog["revision"] = REVISION
    catalog["source_sha256"] = hashlib.sha256(BASE.read_bytes()).hexdigest()
    catalog["entries"] = [
        entry for entry in catalog["entries"] if entry["id"] not in REMOVED_IDS
    ]
    seen = set()
    for entry in catalog["entries"]:
        if entry["id"] in NAME_UPDATES:
            entry["name"] = NAME_UPDATES[entry["id"]]
            if entry["id"] == "V61-OFF-014":
                entry["aliases"] = [
                    alias for alias in entry["aliases"] if "stone" not in alias.casefold()
                ]
            seen.add(entry["id"])
    if seen != set(NAME_UPDATES):
        raise RuntimeError(f"missing expected base entries: {sorted(set(NAME_UPDATES) - seen)}")
    OUT.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
    print(
        json.dumps(
            {
                "output": str(OUT),
                "version": VERSION,
                "revision": REVISION,
                "entries": len(catalog["entries"]),
                "base_sha256": catalog["source_sha256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
