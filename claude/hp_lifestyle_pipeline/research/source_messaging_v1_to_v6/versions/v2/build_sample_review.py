#!/usr/bin/env python3
"""Build local-only HTML and Markdown review artifacts for camera-aware V2 text samples.

The report embeds only supplied offline camera-reference renders. It does not call
models, generate images, edit prompts, or publish anything.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import mimetypes
import os
import re
import sys
from pathlib import Path
from typing import Any


V2_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = V2_ROOT.parents[3]
sys.path.insert(0, str(V2_ROOT))

from camera_profile_resolver import (  # noqa: E402
    load_registry,
    normalize_lookup,
    resolve_profile,
    validate_registry,
)


DEFAULT_MANIFEST = V2_ROOT / "eval/current/manifest.json"
DEFAULT_RUN_DIR = V2_ROOT / "eval/current/runs/gpt55_type_camera"
DEFAULT_VALIDATION = V2_ROOT / "eval/current/accepted_validation.json"
DEFAULT_VALIDATED_OUTPUTS = V2_ROOT / "eval/current/accepted_validated_outputs.json"
DEFAULT_CITATION_REPAIRS = V2_ROOT / "eval/current/citation_repairs.json"
DEFAULT_ACCEPTED_SAMPLES = V2_ROOT / "eval/current/accepted_samples.json"
DEFAULT_CATALOG = PROJECT_ROOT / "research/camera_aware_v2/data/camera_catalog.json"
DEFAULT_TASSEL_IMAGE = PROJECT_ROOT / "local_data/HP_scenes/review/tassel_example_13.png"
DEFAULT_REFERENCE_AUDIT = PROJECT_ROOT / "research/reference_integrity_v1/SUMMARY.md"
SECRET_PATTERNS = (
    re.compile(r"AWS_SECRET_ACCESS_KEY", re.I),
    re.compile(r"AWS_SESSION_TOKEN", re.I),
    re.compile(r"X-Amz-Signature", re.I),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def pretty(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False)


def escaped(value: Any) -> str:
    return html.escape(str(value), quote=True)


def code_block(value: Any) -> str:
    return f'<pre><code>{html.escape(pretty(value))}</code></pre>'


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_sha256(value: Any) -> str:
    return sha256_bytes(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )


def case_id(case: dict[str, Any], index: int) -> str:
    value = case.get("case_id") or case.get("id") or case.get("label")
    if not isinstance(value, str) or not value:
        raise ValueError(f"Manifest case {index} has no case_id/id/label")
    return value


def wrapper_from_record(
    record: dict[str, Any], case: dict[str, Any], manifest_path: Path
) -> dict[str, Any]:
    request_input = record.get("request_input")
    required = {"source_messaging", "camera_tag"}
    if isinstance(request_input, dict) and required.issubset(request_input):
        return request_input

    for field in ("raw_request_json", "raw_input_json"):
        raw = record.get(field)
        if isinstance(raw, str):
            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict) and required.issubset(value):
                return value

    input_path = case.get("input_path")
    if isinstance(input_path, str):
        path = (manifest_path.parent / input_path).resolve()
        if path.is_file():
            value = load_json(path)
            if isinstance(value, dict) and required.issubset(value):
                return value
    raise ValueError(
        f"Could not recover full wrapper input for {case.get('case_id', case.get('id'))}"
    )


def record_path(run_dir: Path, case: dict[str, Any], identifier: str) -> Path:
    declared = case.get("record_path") or case.get("output_path")
    if isinstance(declared, str):
        candidate = (run_dir / declared).resolve()
        if candidate.is_file():
            return candidate
    direct = run_dir / f"{identifier}.json"
    if direct.is_file():
        return direct
    matches = []
    for candidate in sorted(run_dir.glob("*.json")):
        if candidate.name.endswith(".pending.json"):
            continue
        try:
            value = load_json(candidate)
        except (json.JSONDecodeError, OSError):
            continue
        if value.get("case_id") == identifier or value.get("case", {}).get(
            "case_id"
        ) == identifier:
            matches.append(candidate)
    if len(matches) != 1:
        raise FileNotFoundError(
            f"Expected one record for {identifier} in {run_dir}; found {matches}"
        )
    return matches[0]


def output_model(record: dict[str, Any]) -> str | None:
    response = record.get("response") or {}
    model = response.get("model")
    return model if isinstance(model, str) else None


def validation_index(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.is_file():
        return {}
    payload = load_json(path)
    return {
        item["case_id"]: item
        for item in payload.get("cases", [])
        if isinstance(item, dict) and isinstance(item.get("case_id"), str)
    }


def validated_output_index(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.is_file():
        return {}
    payload = load_json(path)
    outputs = payload.get("outputs")
    if not isinstance(outputs, dict):
        raise ValueError(f"Validated-output artifact has no outputs mapping: {path}")
    return outputs


def citation_repair_index(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.is_file():
        return {}
    payload = load_json(path)
    cases = payload.get("cases")
    if not isinstance(cases, dict):
        raise ValueError(f"Citation-repair artifact has no cases mapping: {path}")
    return cases


def accepted_sample_index(
    path: Path | None,
) -> tuple[dict[str, Any] | None, dict[str, dict[str, Any]]]:
    if path is None or not path.is_file():
        return None, {}
    payload = load_json(path)
    cases = payload.get("cases")
    if payload.get("status") != "complete" or not isinstance(cases, list):
        raise ValueError(f"Accepted-sample manifest is incomplete or invalid: {path}")
    index = {
        item["case_id"]: item
        for item in cases
        if isinstance(item, dict) and isinstance(item.get("case_id"), str)
    }
    if len(index) != len(cases):
        raise ValueError(f"Accepted-sample manifest has duplicate/invalid cases: {path}")
    return payload, index


def selected_record_path(
    selection_path: Path, selection_case: dict[str, Any]
) -> Path:
    value = selection_case.get("accepted_record_path")
    if not isinstance(value, str):
        raise ValueError("Accepted selection has no accepted_record_path")
    path = (selection_path.parent / value).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Accepted record does not exist: {path}")
    expected = selection_case.get("accepted_record_sha256")
    if expected and sha256_file(path) != expected:
        raise ValueError(f"Accepted record hash mismatch: {path}")
    return path


def rejected_attempt_details(
    selection_path: Path, selection_case: dict[str, Any]
) -> list[dict[str, Any]]:
    details = []
    for rejected in selection_case.get("rejected_attempts", []):
        path = (selection_path.parent / rejected["record_path"]).resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Rejected attempt record does not exist: {path}")
        actual_sha = sha256_file(path)
        if actual_sha != rejected["record_sha256"]:
            raise ValueError(f"Rejected attempt record hash mismatch: {path}")
        record = load_json(path)
        details.append(
            {
                "selection": rejected,
                "record_path": str(path),
                "record_sha256": actual_sha,
                "raw_model_output": record.get("parsed_output"),
                "raw_api_response": record.get("response"),
            }
        )
    return details


def exact_profile_for_resolution(
    registry: dict[str, Any], resolution: dict[str, Any]
) -> dict[str, Any] | None:
    resolved_tag = resolution.get("resolved_tag")
    if not resolved_tag:
        return None
    matches = [
        profile
        for profile in registry["profiles"]
        if normalize_lookup(profile["tag"]) == normalize_lookup(resolved_tag)
    ]
    if len(matches) != 1:
        raise ValueError(f"Resolved tag has {len(matches)} registry profiles: {resolved_tag}")
    return matches[0]


def embedded_image(path: Path) -> tuple[str, dict[str, Any]]:
    raw = path.read_bytes()
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return (
        f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}",
        {
            "path": str(path.resolve()),
            "bytes": len(raw),
            "sha256": sha256_bytes(raw),
            "mime_type": mime,
        },
    )


def tassel_catalog_match(
    catalog: dict[str, Any], source_camera_name: str
) -> dict[str, Any] | None:
    matches = []
    for report in catalog.get("pdf_reports", []):
        if report.get("source_id") != "standalone_printer_development":
            continue
        for page in report.get("pages", []):
            if (
                page.get("page_device_asset_name_exact")
                != "Tassel_ConnectivityFacet-Wireless.printer.usdz"
            ):
                continue
            for image in page.get("images", []):
                if image.get("camera_name_exact") == source_camera_name:
                    matches.append(
                        {
                            "source_id": report["source_id"],
                            "pdf_absolute_path": report["pdf_absolute_path"],
                            "pdf_sha256": report["pdf_sha256"],
                            "page_number": page["page_number"],
                            "source_declared_device_type": page.get(
                                "source_declared_device_type"
                            ),
                            "effective_device_type": page.get(
                                "effective_device_type"
                            ),
                            "device_type_correction": page.get(
                                "device_type_correction"
                            ),
                            **image,
                        }
                    )
    if len(matches) > 1:
        raise ValueError(
            f"Multiple standalone Tassel PDF matches for {source_camera_name}"
        )
    return matches[0] if matches else None


def select_references(
    resolution: dict[str, Any],
    profile: dict[str, Any] | None,
    catalog: dict[str, Any],
    tassel_image: Path,
) -> dict[str, Any]:
    if resolution["used_minimal_fallback"]:
        return {
            "match_rule": "exact effective device type + exact source camera name",
            "review_only": True,
            "available": [],
            "unavailable": [
                {
                    "kind": "all_offline_examples",
                    "reason": "camera_unknown_or_missing",
                }
            ],
        }
    if profile is None:
        return {
            "match_rule": "exact effective device type + exact source camera name",
            "review_only": True,
            "available": [],
            "unavailable": [
                {
                    "kind": "all_offline_examples",
                    "reason": "resolved_camera_profile_unavailable",
                }
            ],
        }

    device_type = resolution.get("device_type")
    if not device_type:
        return {
            "match_rule": "exact effective device type + exact source camera name",
            "review_only": True,
            "available": [],
            "unavailable": [
                {
                    "kind": "all_offline_examples",
                    "reason": "resolved_camera_has_no_authoritative_device_type",
                }
            ],
        }
    source_camera = resolution.get("source_camera_name")
    if not source_camera or source_camera != profile["source_camera_name"]:
        raise ValueError(
            "Resolver source_camera_name disagrees with its exact registry profile"
        )
    matches = [
        asset
        for asset in catalog.get("high_resolution_assets", [])
        if asset.get("camera_name_exact") == source_camera
        and asset.get("effective_device_type") == device_type
    ]
    matches.sort(key=lambda asset: asset.get("device_asset_name_from_folder", ""))
    available = []
    unavailable = []
    for asset in matches:
        path = Path(asset["extracted_absolute_path"])
        if not path.is_file():
            unavailable.append(
                {
                    "kind": "exact_zip_asset",
                    "reason": "exact_catalog_asset_file_missing",
                    "source_asset_name": asset.get("device_asset_name_from_folder"),
                    "expected_path": str(path),
                }
            )
            continue
        actual_sha = sha256_file(path)
        if actual_sha != asset["sha256"]:
            raise ValueError(f"Catalog asset hash mismatch: {path}")
        data_uri, local = embedded_image(path)
        available.append(
            {
                "kind": "exact_zip_asset",
                "source_asset_name": asset.get("device_asset_name_from_folder"),
                "device_type": device_type,
                "source_camera_name": source_camera,
                "catalog": asset,
                "local": local,
                "data_uri": data_uri,
            }
        )

    if device_type == "printer":
        pdf_match = tassel_catalog_match(catalog, source_camera)
        if source_camera == "Front_CloseUp" and pdf_match is not None:
            if pdf_match.get("effective_device_type") != device_type:
                raise ValueError(
                    "Tassel PDF effective device type disagrees with resolver output"
                )
            if not tassel_image.is_file():
                unavailable.append(
                    {
                        "kind": "exact_pdf_extraction",
                        "reason": "verified_tassel_front_closeup_extraction_missing",
                        "source_asset_name": "Tassel_ConnectivityFacet-Wireless.printer.usdz",
                        "expected_path": str(tassel_image.resolve()),
                    }
                )
            else:
                actual_sha = sha256_file(tassel_image)
                if actual_sha != pdf_match["sha256"]:
                    raise ValueError(
                        "Tassel Front_CloseUp extraction does not match catalog PDF image hash"
                    )
                data_uri, local = embedded_image(tassel_image)
                available.append(
                    {
                        "kind": "exact_pdf_extraction",
                        "source_asset_name": "Tassel_ConnectivityFacet-Wireless.printer.usdz",
                        "device_type": device_type,
                        "source_camera_name": source_camera,
                        "catalog": pdf_match,
                        "local": local,
                        "index_note": (
                            "Local filename suffix 13 is the zero-based extraction position; "
                            "the catalog's one-based PDF image_index is 14."
                        ),
                        "data_uri": data_uri,
                    }
                )
        elif pdf_match is not None:
            unavailable.append(
                {
                    "kind": "exact_pdf_extraction",
                    "reason": "tassel_pdf_exact_camera_exists_but_no_local_extraction",
                    "source_asset_name": "Tassel_ConnectivityFacet-Wireless.printer.usdz",
                    "device_type": device_type,
                    "source_camera_name": source_camera,
                    "catalog": pdf_match,
                }
            )
        else:
            unavailable.append(
                {
                    "kind": "exact_pdf_extraction",
                    "reason": "tassel_pdf_has_no_exact_camera",
                    "source_asset_name": "Tassel_ConnectivityFacet-Wireless.printer.usdz",
                    "device_type": device_type,
                    "source_camera_name": source_camera,
                }
            )

    if not matches:
        unavailable.insert(
            0,
            {
                "kind": "exact_zip_asset",
                "reason": "no_offline_zip_asset_for_exact_effective_type_and_source_camera",
                "device_type": device_type,
                "source_camera_name": source_camera,
            },
        )
    return {
        "match_rule": (
            "all offline examples matching authoritative effective device type + "
            "source camera name, both exact; source asset names are review provenance only"
        ),
        "review_only": True,
        "device_type": device_type,
        "source_camera_name": source_camera,
        "available": available,
        "unavailable": unavailable,
    }


def collect_cases(
    manifest_path: Path,
    run_dir: Path,
    validation_path: Path | None,
    validated_outputs_path: Path | None,
    citation_repairs_path: Path | None,
    accepted_samples_path: Path | None,
    registry_path: Path,
    catalog_path: Path,
    tassel_image: Path,
    allow_partial: bool,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest = load_json(manifest_path)
    registry = load_registry(registry_path)
    validate_registry(registry)
    catalog = load_json(catalog_path)
    validation = validation_index(validation_path)
    validated_outputs = validated_output_index(validated_outputs_path)
    citation_repairs = citation_repair_index(citation_repairs_path)
    accepted_samples, accepted_cases = accepted_sample_index(accepted_samples_path)
    manifest_cases = manifest.get("cases")
    if not isinstance(manifest_cases, list) or not manifest_cases:
        raise ValueError("Manifest has no nonempty cases array")
    if accepted_samples is not None and accepted_samples_path is not None:
        canonical = (
            accepted_samples_path.parent
            / accepted_samples["canonical_manifest_path"]
        ).resolve()
        if canonical != manifest_path.resolve():
            raise ValueError(
                f"Accepted-sample manifest selects {canonical}, not {manifest_path.resolve()}"
            )
        if sha256_file(manifest_path) != accepted_samples["canonical_manifest_sha256"]:
            raise ValueError("Accepted-sample canonical manifest hash mismatch")
        manifest_ids = {
            case_id(declared, index)
            for index, declared in enumerate(manifest_cases, 1)
        }
        if set(accepted_cases) != manifest_ids:
            raise ValueError("Accepted-sample cases do not exactly match manifest cases")
        if set(validated_outputs) != manifest_ids:
            raise ValueError("Accepted validated outputs do not exactly match manifest cases")

    cases = []
    missing = []
    for index, declared in enumerate(manifest_cases, 1):
        identifier = case_id(declared, index)
        selection_case = accepted_cases.get(identifier)
        try:
            path = (
                selected_record_path(accepted_samples_path, selection_case)
                if selection_case is not None and accepted_samples_path is not None
                else record_path(run_dir, declared, identifier)
            )
        except FileNotFoundError:
            if allow_partial:
                missing.append(identifier)
                continue
            raise
        record = load_json(path)
        wrapper = wrapper_from_record(record, declared, manifest_path)
        raw_output = record.get("parsed_output")
        if not isinstance(raw_output, dict):
            raise ValueError(f"Record has no parsed_output object: {path}")
        output = validated_outputs.get(identifier, raw_output)
        if not isinstance(output.get("prompts"), list) or not isinstance(
            output.get("debug"), dict
        ):
            raise ValueError(f"Record has invalid selected output shape: {path}")

        input_semantic = semantic_sha256(wrapper)
        declared_input_sha = declared.get("input_semantic_sha256")
        recorded_input_sha = record.get("input_semantic_sha256")
        for label, expected in (
            ("manifest", declared_input_sha),
            ("record", recorded_input_sha),
        ):
            if expected and expected != input_semantic:
                raise ValueError(
                    f"{identifier}: {label} input semantic hash differs from full wrapper"
                )

        resolution = resolve_profile(registry, wrapper["camera_tag"])
        profile = exact_profile_for_resolution(registry, resolution)
        references = select_references(
            resolution, profile, catalog, tassel_image
        )
        output_camera = output["debug"].get("camera") or {}
        expected_camera_subset = {
            "requested_tag": resolution["requested_tag"],
            "resolved_tag": resolution["resolved_tag"],
            "profile_version": resolution["profile_version"],
            "resolution": resolution["resolution"],
            "framing": resolution["effective_profile"]["framing"],
            "elevation": resolution["effective_profile"]["elevation"],
            "device_type": resolution["device_type"],
        }
        camera_matches = all(
            output_camera.get(key) == value
            for key, value in expected_camera_subset.items()
        )
        accepted_audit = (
            selection_case.get("accepted_automated_audit", {})
            if selection_case is not None
            else validation.get(identifier)
        )
        selected_repairs = (
            {
                "citation_repairs": accepted_audit.get("citation_repairs", []),
                "failures": accepted_audit.get("validated_failures", []),
            }
            if selection_case is not None
            else citation_repairs.get(
                identifier, {"citation_repairs": [], "failures": []}
            )
        )
        rejected_attempts = (
            rejected_attempt_details(accepted_samples_path, selection_case)
            if selection_case is not None and accepted_samples_path is not None
            else []
        )
        cases.append(
            {
                "case_id": identifier,
                "case": declared,
                "record_path": str(path.resolve()),
                "record_sha256": sha256_file(path),
                "wrapper": wrapper,
                "input_semantic_sha256": input_semantic,
                "output": output,
                "output_source": (
                    "accepted_validated_outputs"
                    if selection_case is not None and identifier in validated_outputs
                    else (
                        "validated_outputs"
                        if identifier in validated_outputs
                        else "raw_record"
                    )
                ),
                "raw_output": raw_output,
                "raw_api_response": record.get("response"),
                "resolution": resolution,
                "base_profile": profile,
                "references": references,
                "output_camera_matches_resolver": camera_matches,
                "validation": accepted_audit,
                "citation_repair": selected_repairs,
                "selection": selection_case,
                "rejected_attempts": rejected_attempts,
                "metadata": {
                    "request_key": record.get("request_key"),
                    "system_prompt_sha256": record.get("system_prompt_sha256"),
                    "input_schema_sha256": record.get("input_schema_sha256"),
                    "output_schema_sha256": record.get("output_schema_sha256"),
                    "manifest_sha256": record.get("manifest_sha256"),
                    "source_semantic_sha256": record.get("source_semantic_sha256"),
                    "input_raw_sha256": record.get("input_raw_sha256"),
                    "recorded_input_semantic_sha256": record.get("input_semantic_sha256"),
                    "settings": record.get("settings"),
                    "model": output_model(record),
                    "response_id": (record.get("response") or {}).get("id"),
                    "usage": record.get("usage") or (record.get("response") or {}).get("usage"),
                    "attempt": record.get("attempt"),
                    "latency_seconds": record.get("latency_seconds"),
                    "started_at": record.get("started_at"),
                    "completed_at": record.get("completed_at"),
                    "schema_valid": record.get("schema_valid"),
                    "retry_events": record.get("retry_events"),
                },
            }
        )
    if not allow_partial and len(cases) != len(manifest_cases):
        raise ValueError("Not every manifest case was included")
    return (
        {
            "manifest": manifest,
            "manifest_path": str(manifest_path.resolve()),
            "manifest_sha256": sha256_file(manifest_path),
            "registry_path": str(registry_path.resolve()),
            "registry_sha256": sha256_file(registry_path),
            "catalog_path": str(catalog_path.resolve()),
            "catalog_sha256": sha256_file(catalog_path),
            "validation_path": (
                str(validation_path.resolve()) if validation_path and validation_path.is_file() else None
            ),
            "validation_sha256": (
                sha256_file(validation_path) if validation_path and validation_path.is_file() else None
            ),
            "validated_outputs_path": (
                str(validated_outputs_path.resolve())
                if validated_outputs_path and validated_outputs_path.is_file()
                else None
            ),
            "validated_outputs_sha256": (
                sha256_file(validated_outputs_path)
                if validated_outputs_path and validated_outputs_path.is_file()
                else None
            ),
            "citation_repairs_path": (
                str(citation_repairs_path.resolve())
                if citation_repairs_path and citation_repairs_path.is_file()
                else None
            ),
            "citation_repairs_sha256": (
                sha256_file(citation_repairs_path)
                if citation_repairs_path and citation_repairs_path.is_file()
                else None
            ),
            "accepted_samples_path": (
                str(accepted_samples_path.resolve())
                if accepted_samples_path and accepted_samples_path.is_file()
                else None
            ),
            "accepted_samples_sha256": (
                sha256_file(accepted_samples_path)
                if accepted_samples_path and accepted_samples_path.is_file()
                else None
            ),
            "selection_summary": (
                {
                    key: accepted_samples.get(key)
                    for key in (
                        "version",
                        "status",
                        "scope",
                        "case_count",
                        "accepted_case_count",
                        "primary_successful_sample_count",
                        "isolated_retry_successful_sample_count",
                        "successful_sample_attempt_count",
                        "api_transport_attempt_count",
                        "transient_retry_event_count",
                        "rejected_successful_sample_count",
                        "selection_policy",
                    )
                }
                if accepted_samples is not None
                else None
            ),
            "missing_cases": missing,
        },
        cases,
    )


def render_references_html(references: dict[str, Any]) -> str:
    cards = []
    for reference in references["available"]:
        metadata = {key: value for key, value in reference.items() if key != "data_uri"}
        cards.append(
            '<div class="reference"><img loading="lazy" src="'
            + reference["data_uri"]
            + '" alt="Offline type-camera example">'
            + f'<p><strong>{escaped(reference["source_asset_name"])}</strong></p>'
            + f'<p>{escaped(reference["kind"])} · '
            + escaped(reference["source_camera_name"])
            + "</p><details><summary>Reference provenance</summary>"
            + code_block(metadata)
            + "</details></div>"
        )
    for unavailable in references["unavailable"]:
        cards.append(
            '<div class="reference unavailable"><strong>Reference unavailable</strong>'
            f'<p>{escaped(unavailable["reason"])}</p>{code_block(unavailable)}</div>'
        )
    if not cards:
        cards.append(
            '<div class="reference unavailable"><strong>No matching offline examples</strong></div>'
        )
    return (
        '<p class="scope"><strong>Review-only examples.</strong> These are all exact '
        'offline matches for effective device type and source camera. Source asset names '
        'are provenance captions; the runtime input does not select a product.</p>'
        '<div class="reference-grid">' + "".join(cards) + "</div>"
        '<details><summary>Reference selection diagnostic</summary>'
        + code_block(
            {
                key: value
                for key, value in references.items()
                if key not in {"available"}
            }
        )
        + "</details>"
    )


def render_html(
    sources: dict[str, Any],
    cases: list[dict[str, Any]],
    output_path: Path,
    reference_audit: Path | None,
) -> str:
    cards = []
    for item in cases:
        prompts = "".join(
            '<article class="prompt"><h4>'
            + escaped(prompt.get("id", ""))
            + " · "
            + escaped(prompt.get("environment", ""))
            + "</h4><p>"
            + escaped(prompt.get("text", ""))
            + "</p></article>"
            for prompt in item["output"]["prompts"]
        )
        limits = item["resolution"]["effective_profile"]
        validation = item["validation"]
        raw_validation_label = (
            "not supplied"
            if validation is None
            else ("PASS" if not validation.get("raw_failures") else "FAIL")
        )
        validated_validation_label = (
            "not supplied"
            if validation is None
            else ("PASS" if not validation.get("validated_failures") else "FAIL")
        )
        repair_record = item["citation_repair"]
        repairs = repair_record.get("citation_repairs") or []
        repair_panel = (
            '<div class="repair"><strong>Citation path repaired deterministically</strong>'
            '<p>Only the evidence path changed after the same verbatim quote uniquely '
            'matched another field within the same KSP or Value Proposition. Prompt prose '
            'and quoted text were not edited.</p>'
            + code_block(repair_record)
            + "</div>"
            if repairs
            else ""
        )
        repair_badge = (
            f'<span class="repair-badge">{len(repairs)} citation repair</span>'
            if repairs
            else ""
        )
        selection = item.get("selection") or {}
        rejected_attempts = item.get("rejected_attempts") or []
        selection_badge = (
            '<span class="selection-badge">accepted '
            + escaped(selection.get("accepted_attempt_id"))
            + "</span>"
            if selection
            else ""
        )
        rejection_panel = ""
        if rejected_attempts:
            rejected_cards = []
            for rejected in rejected_attempts:
                declared = rejected["selection"]
                reason = declared.get("reason") or {}
                rejected_repairs = declared.get("citation_repairs") or []
                rejected_audit = (
                    '<p><strong>Raw audit: '
                    + ("PASS" if not declared.get("raw_failures") else "FAIL")
                    + " · Validated audit: "
                    + ("PASS" if not declared.get("validated_failures") else "FAIL")
                    + " · Citation repairs: "
                    + escaped(len(rejected_repairs))
                    + "</strong></p>"
                )
                if rejected_repairs:
                    rejected_audit += (
                        '<div class="repair"><strong>Rejected attempt citation repair details</strong>'
                        + code_block(rejected_repairs)
                        + "</div>"
                    )
                rejected_cards.append(
                    '<div class="rejected-attempt"><p><strong>Rejected '
                    + escaped(declared.get("attempt_id"))
                    + ": "
                    + escaped(reason.get("code"))
                    + "</strong></p><p>"
                    + escaped(reason.get("detail"))
                    + "</p>"
                    + rejected_audit
                    + "<details><summary>Rejected attempt selection and audit record</summary>"
                    + code_block(declared)
                    + "</details><details><summary>Rejected raw model output</summary>"
                    + code_block(rejected["raw_model_output"])
                    + "</details><details><summary>Rejected raw API response</summary>"
                    + code_block(rejected["raw_api_response"])
                    + "</details></div>"
                )
            rejection_panel = (
                '<div class="rejection"><strong>Accepted retry with preserved rejected '
                'successful attempt</strong><p>The original record remains immutable and '
                'is shown below with its rejection reason.</p>'
                + "".join(rejected_cards)
                + "</div>"
            )
        cards.append(
            '<section class="case" id="'
            + escaped(item["case_id"])
            + '"><header><h2>'
            + escaped(item["case_id"])
            + "</h2><p>"
            + escaped(item["case"].get("purpose", ""))
            + '</p><div class="badges"><span>'
            + escaped(item["wrapper"]["camera_tag"])
            + "</span><span>resolved type "
            + escaped(item["resolution"].get("device_type") or "unresolved")
            + "</span><span>raw audit "
            + raw_validation_label
            + "</span><span>validated audit "
            + validated_validation_label
            + "</span><span>output "
            + escaped(item["output_source"])
            + "</span>"
            + repair_badge
            + selection_badge
            + "<span>resolver "
            + ("matches" if item["output_camera_matches_resolver"] else "DIFFERS")
            + "</span></div></header>"
            + repair_panel
            + rejection_panel
            + '<div class="grid"><div><h3>Generated text prompts (validated output)</h3>'
            + prompts
            + '<h3>Exact resolved profile limits</h3><dl class="limits">'
            + "".join(
                f"<dt>{escaped(key)}</dt><dd>{escaped(value)}</dd>"
                for key, value in limits.items()
            )
            + "</dl><details open><summary>Deterministic resolver diagnostic</summary>"
            + code_block(item["resolution"])
            + "</details></div><div><h3>Offline type-camera examples (review only)</h3>"
            + render_references_html(item["references"])
            + "</div></div>"
            + "<details><summary>Full input JSON</summary>"
            + code_block(item["wrapper"])
            + "</details><details><summary>Complete validated output debug</summary>"
            + code_block(item["output"]["debug"])
            + "</details><details><summary>Raw model output before deterministic validation</summary>"
            + code_block(item["raw_output"])
            + "</details><details><summary>Raw API response (immutable record)</summary>"
            + code_block(item["raw_api_response"])
            + "</details><details><summary>Accepted-sample selection record</summary>"
            + code_block(selection if selection else {"status": "not supplied"})
            + "</details><details><summary>Model, request, and hash metadata</summary>"
            + code_block(item["metadata"])
            + "</details><details><summary>Manifest case metadata</summary>"
            + code_block(item["case"])
            + "</details><details><summary>Validation record</summary>"
            + code_block(validation if validation is not None else {"status": "not supplied"})
            + "</details></section>"
        )
    audit_link = ""
    if reference_audit and reference_audit.is_file():
        relative = os.path.relpath(reference_audit.resolve(), output_path.parent.resolve())
        audit_link = (
            '<p class="appendix">Optional historical reference-integrity appendix: '
            f'<a href="{escaped(relative)}">{escaped(str(reference_audit.resolve()))}</a></p>'
        )
    nav = "".join(
        f'<a href="#{escaped(item["case_id"])}">{escaped(item["case_id"])}</a>'
        for item in cases
    )
    selection_summary = sources.get("selection_summary")
    selection_counts = ""
    if selection_summary:
        selection_counts = (
            '<div class="count-grid"><div><strong>'
            + escaped(selection_summary["accepted_case_count"])
            + '</strong><span>accepted cases</span></div><div><strong>'
            + escaped(selection_summary["successful_sample_attempt_count"])
            + '</strong><span>successful sample attempts</span></div><div><strong>'
            + escaped(selection_summary["api_transport_attempt_count"])
            + '</strong><span>API transport attempts</span></div><div><strong>'
            + escaped(selection_summary["rejected_successful_sample_count"])
            + '</strong><span>rejected successful attempts</span></div></div>'
            '<p class="scope">Counts are deliberately separate: a selected case, a '
            'successful model sample, and a transport attempt are different units.</p>'
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Camera-aware V2 text sample review</title>
<style>
:root{{--ink:#172033;--muted:#5d687c;--line:#d8deea;--paper:#fff;--bg:#f3f6fb;--accent:#3157c8}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}
main{{max-width:1500px;margin:auto;padding:28px}} h1,h2,h3,h4{{line-height:1.2}} .intro,.case{{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:22px;margin:0 0 22px;box-shadow:0 4px 18px #20345a12}}
nav{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}} nav a,.badges span{{background:#e9efff;color:#24449c;border-radius:999px;padding:5px 10px;text-decoration:none;font-size:12px}}
.badges .repair-badge{{background:#fff0c2;color:#714b00}} .badges .selection-badge{{background:#e3f7e8;color:#17602b}} .repair,.rejection{{margin:16px 0;padding:14px;border:1px solid #e4ba4d;border-radius:10px;background:#fff9e8}} .repair p{{margin-bottom:0}} .rejection{{border-color:#db8d8d;background:#fff2f2}} .rejected-attempt{{border-top:1px solid #e4b6b6;margin-top:12px;padding-top:8px}}
.count-grid{{display:grid;grid-template-columns:repeat(4,minmax(130px,1fr));gap:10px;margin:16px 0}} .count-grid div{{display:flex;flex-direction:column;padding:12px;background:#f5f7fc;border:1px solid var(--line);border-radius:10px}} .count-grid strong{{font-size:24px}} .count-grid span{{color:var(--muted);font-size:12px}} @media(max-width:700px){{.count-grid{{grid-template-columns:repeat(2,1fr)}}}}
.badges{{display:flex;flex-wrap:wrap;gap:7px}} .grid{{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(340px,.85fr);gap:24px;margin-top:18px}} @media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
.prompt{{border-left:4px solid var(--accent);padding:1px 14px;margin:12px 0}} .prompt h4{{margin-bottom:4px}} .prompt p{{margin-top:4px;font-size:17px}}
.reference-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}} .reference{{min-width:0;border:1px solid var(--line);border-radius:10px;padding:12px}} .reference img{{display:block;width:100%;aspect-ratio:16/9;object-fit:contain;margin:auto;background:#eef1f6;border:1px solid var(--line);border-radius:8px}} .reference p{{overflow-wrap:anywhere}} .unavailable{{border-style:dashed;background:#fafbfe}}
details{{border-top:1px solid var(--line);margin-top:14px;padding-top:11px}} summary{{cursor:pointer;font-weight:650;color:#263b71}} pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#111827;color:#e5ecf8;border-radius:9px;padding:14px;max-height:650px;overflow:auto}}
.limits{{display:grid;grid-template-columns:max-content 1fr;gap:5px 13px}} .limits dt{{font-weight:700}} .limits dd{{margin:0}} .appendix,.scope{{color:var(--muted)}} code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
</style></head><body><main>
<section class="intro"><h1>Camera-aware V2 text sample review</h1>
<p class="scope">Local text review only. The report made no model or image-generation calls. Each case shows all supplied offline references matching its resolved effective device type and source camera. Product filenames are review provenance only; runtime inputs do not select products. Thumbnails are embedded as base64, and unavailable examples are reported without substitution.</p>
<p><strong>{len(cases)}</strong> selected cases shown. Validated outputs are primary. Each case separately reports the raw and validated audit result, visibly identifies deterministic citation-path repairs, and retains the raw model output and immutable API response for inspection.</p>
{selection_counts}
{audit_link}<details><summary>Review source files and hashes</summary>{code_block(sources)}</details><nav>{nav}</nav></section>
{''.join(cards)}
</main></body></html>
"""


def fenced_json(value: Any) -> str:
    return "```json\n" + pretty(value) + "\n```"


def render_markdown(
    sources: dict[str, Any],
    cases: list[dict[str, Any]],
    output_path: Path,
    reference_audit: Path | None,
) -> str:
    lines = [
        "# Camera-aware V2 text sample review",
        "",
        "Local text review only. No model or image-generation call was made by this builder. The HTML companion embeds all supplied offline examples that exactly match the resolved effective device type and source camera. Source asset filenames are review provenance only; runtime inputs do not select products. Missing examples remain visibly unavailable.",
        "",
        f"Cases included: **{len(cases)}**.",
    ]
    selection_summary = sources.get("selection_summary")
    if selection_summary:
        lines.extend(
            [
                "",
                "## Selection and API accounting",
                "",
                f"- Accepted cases: **{selection_summary['accepted_case_count']}**",
                f"- Successful sample attempts: **{selection_summary['successful_sample_attempt_count']}**",
                f"- API transport attempts: **{selection_summary['api_transport_attempt_count']}**",
                f"- Transient retry events: **{selection_summary['transient_retry_event_count']}**",
                f"- Rejected successful attempts: **{selection_summary['rejected_successful_sample_count']}**",
                "",
                "These are separate units. Retries remain visible and do not inflate the accepted-case count.",
            ]
        )
    if reference_audit and reference_audit.is_file():
        relative = os.path.relpath(reference_audit.resolve(), output_path.parent.resolve())
        lines.extend(
            [
                "",
                f"Optional historical reference-integrity appendix: [{reference_audit.resolve()}]({relative})",
            ]
        )
    lines.extend(["", "<details><summary>Review source files and hashes</summary>", "", fenced_json(sources), "", "</details>"])
    for item in cases:
        lines.extend(
            [
                "",
                f"## {item['case_id']}",
                "",
                item["case"].get("purpose", ""),
                "",
                f"- Requested camera: `{item['wrapper']['camera_tag']}`",
                f"- Resolved effective device type: `{item['resolution'].get('device_type')}`",
                f"- Output shown: **{item['output_source']}**",
                f"- Accepted attempt: **{(item.get('selection') or {}).get('accepted_attempt_id', 'not supplied')}**",
                f"- Raw audit: **{'not supplied' if item['validation'] is None else ('PASS' if not item['validation'].get('raw_failures') else 'FAIL')}**",
                f"- Validated audit: **{'not supplied' if item['validation'] is None else ('PASS' if not item['validation'].get('validated_failures') else 'FAIL')}**",
                f"- Offline resolver agrees with output debug: **{'yes' if item['output_camera_matches_resolver'] else 'NO'}**",
                "",
            ]
        )
        repairs = item["citation_repair"].get("citation_repairs") or []
        if repairs:
            lines.extend(
                [
                    f"**Citation path repaired deterministically ({len(repairs)}).** Only the evidence path changed after the same verbatim quote uniquely matched another field within the same KSP or Value Proposition. Prompt prose and quoted text were not edited.",
                    "",
                    fenced_json(item["citation_repair"]),
                    "",
                ]
            )
        rejected_attempts = item.get("rejected_attempts") or []
        if rejected_attempts:
            lines.extend(
                [
                    "### Preserved rejected successful attempts",
                    "",
                    "The accepted retry is shown above. Each original record remains immutable and is retained below with its rejection reason.",
                    "",
                ]
            )
            for rejected in rejected_attempts:
                declared = rejected["selection"]
                reason = declared.get("reason") or {}
                rejected_repairs = declared.get("citation_repairs") or []
                lines.extend(
                    [
                        f"#### Rejected {declared.get('attempt_id')}: {reason.get('code')}",
                        "",
                        reason.get("detail", ""),
                        "",
                        f"- Raw audit: **{'PASS' if not declared.get('raw_failures') else 'FAIL'}**",
                        f"- Validated audit: **{'PASS' if not declared.get('validated_failures') else 'FAIL'}**",
                        f"- Citation repairs: **{len(rejected_repairs)}**",
                        "",
                        *(
                            [
                                "**Rejected attempt citation repair details:**",
                                "",
                                fenced_json(rejected_repairs),
                                "",
                            ]
                            if rejected_repairs
                            else []
                        ),
                        "<details><summary>Rejected attempt selection and audit record</summary>",
                        "",
                        fenced_json(declared),
                        "",
                        "</details>",
                        "",
                        "<details><summary>Rejected raw model output</summary>",
                        "",
                        fenced_json(rejected["raw_model_output"]),
                        "",
                        "</details>",
                        "",
                        "<details><summary>Rejected raw API response</summary>",
                        "",
                        fenced_json(rejected["raw_api_response"]),
                        "",
                        "</details>",
                        "",
                    ]
                )
        lines.extend(
            [
                "### Generated text prompts (validated output)",
            ]
        )
        for prompt in item["output"]["prompts"]:
            lines.extend(
                [
                    "",
                    f"**{prompt.get('id', '')} · {prompt.get('environment', '')}**",
                    "",
                    prompt.get("text", ""),
                ]
            )
        lines.extend(
            [
                "",
                "### Exact resolved profile limits",
                "",
                fenced_json(item["resolution"]),
                "",
                "### Offline type-camera examples (review only)",
                "",
                "These are all exact offline matches for effective device type and source camera. Source asset names are provenance captions and do not indicate runtime product selection.",
                "",
            ]
        )
        references = item["references"]
        if references["available"]:
            for reference in references["available"]:
                lines.extend(
                    [
                        f"#### {reference['source_asset_name']}",
                        "",
                        f"Exact local reference: `{reference['local']['path']}`",
                        "",
                        f"SHA-256: `{reference['local']['sha256']}`",
                        "",
                        fenced_json({k: v for k, v in reference.items() if k != "data_uri"}),
                        "",
                    ]
                )
        else:
            lines.extend(
                [
                    "No embedded offline example matched.",
                    "",
                ]
            )
        if references["unavailable"]:
            lines.extend(
                [
                    "#### Unavailable offline references",
                    "",
                    fenced_json(references["unavailable"]),
                ]
            )
        for title, value in (
            ("Full input JSON", item["wrapper"]),
            ("Complete validated output debug", item["output"]["debug"]),
            ("Raw model output before deterministic validation", item["raw_output"]),
            ("Raw API response (immutable record)", item["raw_api_response"]),
            ("Accepted-sample selection record", item.get("selection") or {"status": "not supplied"}),
            ("Model, request, and hash metadata", item["metadata"]),
            ("Manifest case metadata", item["case"]),
            ("Validation record", item["validation"] or {"status": "not supplied"}),
        ):
            lines.extend(
                [
                    "",
                    f"<details><summary>{title}</summary>",
                    "",
                    fenced_json(value),
                    "",
                    "</details>",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def assert_no_credentials(value: str, label: str) -> None:
    hits = [pattern.pattern for pattern in SECRET_PATTERNS if pattern.search(value)]
    if hits:
        raise ValueError(f"Credential-like material found in {label}: {hits}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    parser.add_argument(
        "--validated-outputs", type=Path, default=DEFAULT_VALIDATED_OUTPUTS
    )
    parser.add_argument(
        "--citation-repairs", type=Path, default=DEFAULT_CITATION_REPAIRS
    )
    parser.add_argument(
        "--accepted-samples", type=Path, default=DEFAULT_ACCEPTED_SAMPLES
    )
    parser.add_argument("--registry", type=Path, default=V2_ROOT / "camera_profiles.json")
    parser.add_argument("--camera-catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--tassel-image", type=Path, default=DEFAULT_TASSEL_IMAGE)
    parser.add_argument("--html", type=Path, default=V2_ROOT / "eval/current/review.html")
    parser.add_argument("--markdown", type=Path, default=V2_ROOT / "eval/current/REVIEW.md")
    parser.add_argument("--reference-audit", type=Path, default=DEFAULT_REFERENCE_AUDIT)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    sources, cases = collect_cases(
        args.manifest,
        args.run_dir,
        args.validation,
        args.validated_outputs,
        args.citation_repairs,
        args.accepted_samples,
        args.registry,
        args.camera_catalog,
        args.tassel_image,
        args.allow_partial,
    )
    if not cases:
        raise ValueError("No completed sample records were found")
    html_text = render_html(sources, cases, args.html, args.reference_audit)
    markdown_text = render_markdown(sources, cases, args.markdown, args.reference_audit)
    assert_no_credentials(html_text, "HTML review")
    assert_no_credentials(markdown_text, "Markdown review")
    args.html.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.html.write_text(html_text, encoding="utf-8")
    args.markdown.write_text(markdown_text, encoding="utf-8")
    print(
        json.dumps(
            {
                "cases": len(cases),
                "missing_cases": sources["missing_cases"],
                "html": str(args.html.resolve()),
                "html_bytes": len(html_text.encode("utf-8")),
                "html_sha256": sha256_bytes(html_text.encode("utf-8")),
                "markdown": str(args.markdown.resolve()),
                "markdown_bytes": len(markdown_text.encode("utf-8")),
                "markdown_sha256": sha256_bytes(markdown_text.encode("utf-8")),
                "model_called": False,
                "image_generation_called": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
