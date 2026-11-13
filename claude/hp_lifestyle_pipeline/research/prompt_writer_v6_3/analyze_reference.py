"""Recompute the evidence used by the proposal without model or network calls."""

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
UPSTREAM = ROOT / "data" / "upstream"
WRITER = ROOT.parent / "source_messaging_v1_to_v6" / "versions" / "v6_2"
CATALOG = WRITER / "approved-v6.2-20261106.catalog.json"
FIELDS = {
    "environments": lambda row, family: [row["environment"]],
    "roles": lambda row, family: [row["device_observations"][family]["role"]],
    "supports": lambda row, family: [
        placement["immediate"]
        for placement in row["device_observations"][family]["placements"]
    ],
    "support_materials": lambda row, family: [
        material
        for placement in row["device_observations"][family]["placements"]
        for material in placement["materials"]
    ],
    "surrounding_objects": lambda row, family: [
        name for name in row["objects"] if name != family
    ],
}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def counts(rows, family, getter):
    result = Counter(value for row in rows for value in set(getter(row, family)))
    return dict(sorted(result.items(), key=lambda item: (-item[1], item[0])))


def summarize(rows, family):
    return {
        "n": len(rows),
        "source_rows": [row["source_row"] for row in rows],
        "cohorts": dict(Counter(row["cohort"] for row in rows)),
        **{
            field: counts(rows, family, getter)
            for field, getter in FIELDS.items()
        },
    }


def main():
    rows = load(UPSTREAM / "rows.json")
    profiles = load(UPSTREAM / "statistics.json")
    metadata = load(UPSTREAM / "metadata.json")
    source_manifest = load(ROOT / "data" / "source_manifest.json")
    if len(rows) != metadata["identities"] or len({r["image_hash"] for r in rows}) != len(rows):
        raise ValueError("Source identity accounting does not reconcile")
    if digest(ROOT / "data" / "ctech_report.html") != source_manifest["index_sha256"]:
        raise ValueError("Report bytes differ from the source snapshot")

    evidence = {
        "source_url": source_manifest["source_url"],
        "scope": "Caption-derived laptop/printer evidence; no new visual assessment",
        "metadata": metadata,
        "sources": {
            str(path.relative_to(ROOT)): {"bytes": path.stat().st_size, "sha256": digest(path)}
            for path in sorted((ROOT / "data").rglob("*"))
            if path.is_file() and path.name not in {"evidence.json"}
        },
        "v62_baseline": {
            path.name: {"bytes": path.stat().st_size, "sha256": digest(path)}
            for path in (WRITER / "system_prompt.md", CATALOG)
        },
        "devices": {},
        "reported_profile_comparisons": 0,
    }
    for family in ("Laptop", "Printer"):
        members = [row for row in rows if family in row["device_presence"]]
        selected = [
            profile for profile in profiles
            if profile.get("device_family") == family
            and profile["kind"] in {"Device presence", "Device presence x environment"}
        ]
        for profile in selected:
            subset = [row for row in members if row["source_row"] in profile["source_rows"]]
            if len(subset) != profile["n"]:
                raise ValueError(f"Profile size mismatch: {profile['name']}")
            for field, getter in FIELDS.items():
                actual = counts(subset, family, getter)
                expected = {entry["value"]: entry["n"] for entry in profile[field]}
                if actual != expected:
                    raise ValueError(f"Profile count mismatch: {profile['name']} / {field}")
                evidence["reported_profile_comparisons"] += 1
        evidence["devices"][family] = {
            "all": summarize(members, family),
            "primary_only": summarize([
                row for row in members
                if row["device_observations"][family]["role"] == "Primary / foreground"
            ], family),
            "by_environment": {
                environment: summarize([
                    row for row in members if row["environment"] == environment
                ], family)
                for environment in sorted({row["environment"] for row in members})
            },
        }
        if family == "Printer":
            evidence["devices"][family]["desktop_only"] = summarize([
                row for row in members
                if row["printer_observation"]["kind"] == "Desktop printer"
            ], family)

    candidate_families = {
        "bags": "Bag / backpack / luggage",
        "clocks_and_calendars": "Clock / calendar",
        "ceramics_and_stock": "Ceramics / stock inventory",
    }
    evidence["candidate_object_evidence"] = {
        name: [
            {
                "source_row": row["source_row"],
                "environment": row["environment"],
                "device_role": row["device_observations"]["Laptop"]["role"],
                "object_labels": row["objects"][object_family],
            }
            for row in rows
            if "Laptop" in row["device_presence"] and object_family in row["objects"]
        ]
        for name, object_family in candidate_families.items()
    }
    evidence["approved_catalogue"] = [
        {key: entry[key] for key in ("id", "environment", "name", "repetition_groups")}
        for entry in load(CATALOG)["entries"]
    ]
    output = ROOT / "data" / "evidence.json"
    output.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output),
        "reported_profile_comparisons": evidence["reported_profile_comparisons"],
        "laptops": evidence["devices"]["Laptop"]["all"]["n"],
        "printers": evidence["devices"]["Printer"]["all"]["n"],
        "desktop_printers": evidence["devices"]["Printer"]["desktop_only"]["n"],
    }, indent=2))


if __name__ == "__main__":
    main()
