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


DEFAULT_MANIFEST = V2_ROOT / "eval/manifest.json"
DEFAULT_RUN_DIR = V2_ROOT / "eval/runs/gpt55_bounded"
DEFAULT_VALIDATION = V2_ROOT / "eval/validation.json"
DEFAULT_CATALOG = PROJECT_ROOT / "research/camera_aware/data/camera_catalog.json"
DEFAULT_TASSEL_IMAGE = PROJECT_ROOT / "local_data/HP_scenes/review/tassel_example_13.png"
DEFAULT_REFERENCE_AUDIT = PROJECT_ROOT / "research/reference_integrity/SUMMARY.md"
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
    if isinstance(request_input, dict) and {
        "source_messaging",
        "product_name",
        "camera_tag",
    }.issubset(request_input):
        return request_input

    for field in ("raw_request_json", "raw_input_json"):
        raw = record.get(field)
        if isinstance(raw, str):
            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict) and {
                "source_messaging",
                "product_name",
                "camera_tag",
            }.issubset(value):
                return value

    input_path = case.get("input_path")
    if isinstance(input_path, str):
        path = (manifest_path.parent / input_path).resolve()
        if path.is_file():
            value = load_json(path)
            if isinstance(value, dict) and {
                "source_messaging",
                "product_name",
                "camera_tag",
            }.issubset(value):
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
    catalog: dict[str, Any], resolved_product: str, source_camera_name: str
) -> dict[str, Any] | None:
    matches = []
    for report in catalog.get("pdf_reports", []):
        if report.get("source_id") != "standalone_printer_development":
            continue
        for page in report.get("pages", []):
            if page.get("page_device_asset_name_exact") != resolved_product:
                continue
            for image in page.get("images", []):
                if image.get("camera_name_exact") == source_camera_name:
                    matches.append(
                        {
                            "source_id": report["source_id"],
                            "pdf_absolute_path": report["pdf_absolute_path"],
                            "pdf_sha256": report["pdf_sha256"],
                            "page_number": page["page_number"],
                            **image,
                        }
                    )
    if len(matches) > 1:
        raise ValueError(
            f"Multiple standalone Tassel PDF matches for {resolved_product}/{source_camera_name}"
        )
    return matches[0] if matches else None


def select_reference(
    resolution: dict[str, Any],
    profile: dict[str, Any] | None,
    catalog: dict[str, Any],
    tassel_image: Path,
) -> dict[str, Any]:
    if resolution["used_minimal_fallback"]:
        reason = resolution.get("incompatible_reason") or (
            "camera_unknown_or_missing" if resolution.get("resolved_tag") is None else "minimal_fallback"
        )
        return {"available": False, "reason": reason}
    if resolution.get("resolved_product") is None:
        return {"available": False, "reason": "product_unknown_or_missing"}
    if profile is None:
        return {"available": False, "reason": "resolved_camera_profile_unavailable"}

    product = resolution["resolved_product"]
    source_camera = resolution.get("source_camera_name")
    if not source_camera or source_camera != profile["source_camera_name"]:
        raise ValueError(
            "Resolver source_camera_name disagrees with its exact registry profile"
        )
    family = profile["device_family"]
    matches = [
        asset
        for asset in catalog.get("high_resolution_assets", [])
        if asset.get("device_asset_name_from_folder") == product
        and asset.get("camera_name_exact") == source_camera
        and asset.get("device_family") == family
    ]
    if len(matches) == 1:
        asset = matches[0]
        path = Path(asset["extracted_absolute_path"])
        if not path.is_file():
            return {
                "available": False,
                "reason": "exact_catalog_asset_file_missing",
                "expected_path": str(path),
            }
        actual_sha = sha256_file(path)
        if actual_sha != asset["sha256"]:
            raise ValueError(f"Catalog asset hash mismatch: {path}")
        data_uri, local = embedded_image(path)
        return {
            "available": True,
            "kind": "exact_zip_asset",
            "match_rule": "resolved full product name + source camera name + device family, all exact",
            "resolved_product": product,
            "source_camera_name": source_camera,
            "catalog": asset,
            "local": local,
            "data_uri": data_uri,
        }
    if len(matches) > 1:
        raise ValueError(f"Ambiguous exact catalog assets for {product}/{source_camera}")

    if product == "Tassel_ConnectivityFacet-Wireless.printer.usdz":
        pdf_match = tassel_catalog_match(catalog, product, source_camera)
        if source_camera == "Front_CloseUp" and pdf_match:
            if not tassel_image.is_file():
                return {
                    "available": False,
                    "reason": "verified_tassel_front_closeup_extraction_missing",
                    "expected_path": str(tassel_image.resolve()),
                }
            actual_sha = sha256_file(tassel_image)
            if actual_sha != pdf_match["sha256"]:
                raise ValueError(
                    "Tassel Front_CloseUp extraction does not match catalog PDF image hash"
                )
            data_uri, local = embedded_image(tassel_image)
            return {
                "available": True,
                "kind": "exact_pdf_extraction",
                "match_rule": "resolved full product name + source camera name, exact; standalone printer PDF",
                "resolved_product": product,
                "source_camera_name": source_camera,
                "catalog": pdf_match,
                "local": local,
                "index_note": (
                    "Local filename suffix 13 is the zero-based extraction position; "
                    "the catalog's one-based PDF image_index is 14."
                ),
                "data_uri": data_uri,
            }
        return {
            "available": False,
            "reason": "tassel_is_pdf_only_and_no_exact_extracted_image_for_this_camera",
            "resolved_product": product,
            "source_camera_name": source_camera,
        }

    return {
        "available": False,
        "reason": "no_exact_product_and_source_camera_asset",
        "resolved_product": product,
        "source_camera_name": source_camera,
    }


def collect_cases(
    manifest_path: Path,
    run_dir: Path,
    validation_path: Path | None,
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
    manifest_cases = manifest.get("cases")
    if not isinstance(manifest_cases, list) or not manifest_cases:
        raise ValueError("Manifest has no nonempty cases array")

    cases = []
    missing = []
    for index, declared in enumerate(manifest_cases, 1):
        identifier = case_id(declared, index)
        try:
            path = record_path(run_dir, declared, identifier)
        except FileNotFoundError:
            if allow_partial:
                missing.append(identifier)
                continue
            raise
        record = load_json(path)
        wrapper = wrapper_from_record(record, declared, manifest_path)
        output = record.get("parsed_output")
        if not isinstance(output, dict):
            raise ValueError(f"Record has no parsed_output object: {path}")
        if not isinstance(output.get("prompts"), list) or not isinstance(
            output.get("debug"), dict
        ):
            raise ValueError(f"Record has invalid parsed_output shape: {path}")

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

        resolution = resolve_profile(
            registry, wrapper["camera_tag"], wrapper["product_name"]
        )
        profile = exact_profile_for_resolution(registry, resolution)
        reference = select_reference(
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
            "requested_product": resolution["requested_product"],
            "resolved_product": resolution["resolved_product"],
            "product_resolution": resolution["product_resolution"],
        }
        camera_matches = all(
            output_camera.get(key) == value
            for key, value in expected_camera_subset.items()
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
                "resolution": resolution,
                "base_profile": profile,
                "reference": reference,
                "output_camera_matches_resolver": camera_matches,
                "validation": validation.get(identifier),
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
            "missing_cases": missing,
        },
        cases,
    )


def render_reference_html(reference: dict[str, Any]) -> str:
    if not reference["available"]:
        return (
            '<div class="reference unavailable"><strong>No reference thumbnail</strong>'
            f'<p>{escaped(reference["reason"])}</p>{code_block(reference)}</div>'
        )
    metadata = {key: value for key, value in reference.items() if key != "data_uri"}
    return (
        '<div class="reference"><img loading="lazy" src="'
        + reference["data_uri"]
        + '" alt="Exact offline camera reference">'
        + f'<p><strong>{escaped(reference["kind"])}</strong> · '
        + escaped(reference["source_camera_name"])
        + "</p><details><summary>Reference provenance</summary>"
        + code_block(metadata)
        + "</details></div>"
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
        validation_label = (
            "not supplied"
            if validation is None
            else ("PASS" if not validation.get("failures") else "FAIL")
        )
        cards.append(
            '<section class="case" id="'
            + escaped(item["case_id"])
            + '"><header><h2>'
            + escaped(item["case_id"])
            + "</h2><p>"
            + escaped(item["case"].get("purpose", ""))
            + '</p><div class="badges"><span>'
            + escaped(item["wrapper"]["product_name"])
            + "</span><span>"
            + escaped(item["wrapper"]["camera_tag"])
            + "</span><span>validation "
            + validation_label
            + "</span><span>resolver "
            + ("matches" if item["output_camera_matches_resolver"] else "DIFFERS")
            + "</span></div></header>"
            + '<div class="grid"><div><h3>Generated text prompts</h3>'
            + prompts
            + '<h3>Exact resolved profile limits</h3><dl class="limits">'
            + "".join(
                f"<dt>{escaped(key)}</dt><dd>{escaped(value)}</dd>"
                for key, value in limits.items()
            )
            + "</dl><details open><summary>Deterministic resolver diagnostic</summary>"
            + code_block(item["resolution"])
            + "</details></div><div><h3>Matching offline camera reference</h3>"
            + render_reference_html(item["reference"])
            + "</div></div>"
            + "<details><summary>Full input JSON</summary>"
            + code_block(item["wrapper"])
            + "</details><details><summary>Complete output debug</summary>"
            + code_block(item["output"]["debug"])
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
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Camera-aware V2 text sample review</title>
<style>
:root{{--ink:#172033;--muted:#5d687c;--line:#d8deea;--paper:#fff;--bg:#f3f6fb;--accent:#3157c8}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}
main{{max-width:1500px;margin:auto;padding:28px}} h1,h2,h3,h4{{line-height:1.2}} .intro,.case{{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:22px;margin:0 0 22px;box-shadow:0 4px 18px #20345a12}}
nav{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}} nav a,.badges span{{background:#e9efff;color:#24449c;border-radius:999px;padding:5px 10px;text-decoration:none;font-size:12px}}
.badges{{display:flex;flex-wrap:wrap;gap:7px}} .grid{{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(340px,.85fr);gap:24px;margin-top:18px}} @media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
.prompt{{border-left:4px solid var(--accent);padding:1px 14px;margin:12px 0}} .prompt h4{{margin-bottom:4px}} .prompt p{{margin-top:4px;font-size:17px}}
.reference img{{display:block;max-width:100%;max-height:520px;margin:auto;background:#eef1f6;border:1px solid var(--line);border-radius:10px}} .unavailable{{padding:20px;border:1px dashed #aab4c8;border-radius:10px}}
details{{border-top:1px solid var(--line);margin-top:14px;padding-top:11px}} summary{{cursor:pointer;font-weight:650;color:#263b71}} pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#111827;color:#e5ecf8;border-radius:9px;padding:14px;max-height:650px;overflow:auto}}
.limits{{display:grid;grid-template-columns:max-content 1fr;gap:5px 13px}} .limits dt{{font-weight:700}} .limits dd{{margin:0}} .appendix,.scope{{color:var(--muted)}} code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
</style></head><body><main>
<section class="intro"><h1>Camera-aware V2 text sample review</h1>
<p class="scope">Local text review only. The report made no model or image-generation calls. Thumbnails are exact supplied offline camera references embedded as base64; unavailable references remain unavailable rather than borrowing another product.</p>
<p><strong>{len(cases)}</strong> complete cases shown. Every case includes its full wrapper input, all prompt text, complete debug, deterministic resolver result, exact effective limits, and request/hash metadata.</p>
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
        "Local text review only. No model or image-generation call was made by this builder. The HTML companion embeds exact supplied offline reference thumbnails as base64. Missing, unknown, and incompatible references remain unavailable.",
        "",
        f"Cases included: **{len(cases)}**.",
    ]
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
                f"- Requested product: `{item['wrapper']['product_name']}`",
                f"- Requested camera: `{item['wrapper']['camera_tag']}`",
                f"- Offline resolver agrees with output debug: **{'yes' if item['output_camera_matches_resolver'] else 'NO'}**",
                "",
                "### Generated text prompts",
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
                "### Matching offline camera reference",
                "",
            ]
        )
        reference = item["reference"]
        if reference["available"]:
            lines.extend(
                [
                    f"Exact local reference: `{reference['local']['path']}`",
                    "",
                    f"SHA-256: `{reference['local']['sha256']}`",
                    "",
                    fenced_json({k: v for k, v in reference.items() if k != "data_uri"}),
                ]
            )
        else:
            lines.extend(
                [
                    f"Unavailable: `{reference['reason']}`.",
                    "",
                    fenced_json(reference),
                ]
            )
        for title, value in (
            ("Full input JSON", item["wrapper"]),
            ("Complete output debug", item["output"]["debug"]),
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
    parser.add_argument("--registry", type=Path, default=V2_ROOT / "camera_profiles.json")
    parser.add_argument("--camera-catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--tassel-image", type=Path, default=DEFAULT_TASSEL_IMAGE)
    parser.add_argument("--html", type=Path, default=V2_ROOT / "eval/review.html")
    parser.add_argument("--markdown", type=Path, default=V2_ROOT / "eval/REVIEW.md")
    parser.add_argument("--reference-audit", type=Path, default=DEFAULT_REFERENCE_AUDIT)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    sources, cases = collect_cases(
        args.manifest,
        args.run_dir,
        args.validation,
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
