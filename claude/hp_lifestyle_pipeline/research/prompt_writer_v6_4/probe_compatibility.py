#!/usr/bin/env python3
"""Probe frozen V6.3 locally; never call a provider or implement V6.4."""

import copy
import hashlib
import json
import sys
from pathlib import Path

import jsonschema

from analyze_inputs import BASELINE, HERE, write_json


sys.path.insert(0, str(BASELINE.parent))
from v6_3 import validation  # noqa: E402


def citation_probe(request, document, pointer):
    value, _ = validation._pointer_value(request[document], pointer)
    if not isinstance(value, str) or not value:
        raise ValueError(f"probe requires a nonempty string: {document} {pointer}")
    candidate = {
        "prompts": [{
            "evidence": [{
                "document": document, "path": pointer, "quote": value[:80],
            }],
        }],
    }
    original = copy.deepcopy(candidate)
    normalized, changes = validation.normalize_invalid_evidence(candidate, request)
    if candidate != original:
        raise AssertionError("citation probe mutated its original input")
    return {
        "document": document, "path": pointer,
        "citation_retained": bool(normalized["prompts"][0]["evidence"]),
        "removal_reasons": [
            change["reason"] for change in changes
            if change["action"] == "remove_invalid_evidence"
        ],
    }


def main():
    manifest = json.loads((HERE / "data/source_manifest.json").read_text())
    schema = json.loads((BASELINE / "input.schema.json").read_text())
    pairs = {}
    for document in manifest["documents"]:
        if document["group"] != "new":
            continue
        value = json.loads(Path(document["document_path"]).read_text())["value"]
        role = "source_messaging" if "product_identity" in value else "smart_brief"
        pair = pairs.setdefault(document["pair"], {})
        if role in pair:
            raise ValueError(f"ambiguous role in research pair: {document['pair']} {role}")
        pair[role] = value
    results = []
    for name, pair in sorted(pairs.items()):
        if set(pair) != {"smart_brief", "source_messaging"}:
            raise ValueError(f"incomplete research pair: {name}")
        if name.startswith("matineer"):
            camera = "miniPC_FrontRightMedium"
        elif name in {"elitebook", "viktor-smart-brief-source-messaging"}:
            camera = "laptop_FrontCloseUp"
        else:
            camera = "printer_FrontCloseUp"
        request = {**pair, "camera_tag": camera}
        jsonschema.validate(request, schema)
        errors = validation._validate_request(request)
        if errors:
            raise AssertionError(errors)
        content = [
            citation_probe(request, "smart_brief", "/USE CASES/content"),
            citation_probe(request, "source_messaging", "/source_messaging/0/fields/1/value"),
            citation_probe(request, "source_messaging", "/etail_messaging/0/value"),
        ]
        if not all(item["citation_retained"] for item in content):
            raise AssertionError(content)
        results.append({
            "pair": name, "input_schema_passed": True,
            "local_request_validation_passed": True,
            "camera_tag_for_structural_probe_only": camera,
            "content_citations": content,
            "first_ksp_field_row_label": pair["source_messaging"]["source_messaging"][1]["fields"][0]["row"],
        })
    elitebook = pairs["elitebook"]
    metadata = [
        citation_probe(elitebook, document, pointer)
        for document, pointer in (
            ("smart_brief", "/USE CASES/confidence"),
            ("smart_brief", "/USE CASES/confidence_rationale"),
            ("source_messaging", "/template_id"),
            ("source_messaging", "/source_messaging/0/block"),
            ("source_messaging", "/source_messaging/0/fields/0/label"),
            ("source_messaging", "/etail_messaging/0/container"),
            ("source_messaging", "/_chatSession/model"),
        )
    ]
    changed = [
        name for name, expected in manifest["v63_baseline_sha256"].items()
        if hashlib.sha256((BASELINE / name).read_bytes()).hexdigest() != expected
    ]
    if changed:
        raise AssertionError(f"frozen V6.3 source changed: {changed}")
    report = {
        "scope": "offline compatibility diagnostics, not generated outputs or semantic acceptance",
        "provider_calls": 0, "writer_runs": 0,
        "paired_samples": results,
        "metadata_citation_diagnostics": metadata,
        "baseline_files_unchanged": len(manifest["v63_baseline_sha256"]),
        "limitations": [
            "Camera tags are structural probes, not approved digital-twin mappings.",
            "Passing request/citation mechanics does not establish generated-bank or image quality.",
            "Retained metadata is a local mechanical gap, not evidence that a model cited it.",
        ],
    }
    destination = HERE / "data/compatibility_probe.json"
    write_json(destination, report)
    print(f"Saved offline diagnostics for {len(results)} pairs to {destination}")


if __name__ == "__main__":
    main()
