"""Preserve the supplied comparisons and assemble four exact-key V15.8 review views."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import copy
import html
import io
import json
import mimetypes
from pathlib import Path
import re
from urllib.parse import urljoin

from PIL import Image

import generate
import study

CELL = "v6_5_pr4619"
BASELINE_CELL = "v6_4_pr4619"
RECOVERY = "hp-data-artifacts/hp-3p-gpt25/hp160-v64-bluehex-lighting-artistic-walls-20w-20261111T212915Z"
LIVE = study.GATEWAY + RECOVERY + "-live/gallery/index.html"
TITLE = "HP V6.4 vs V6.5 / PR4619 - V15.8"
PUBLIC = study.HERE / "public"
STAGING = study.HERE / "extension"


def once(text, before, after):
    if text.count(before) != 1:
        raise ValueError(f"Customization anchor is not unique: {before[:90]}")
    return text.replace(before, after, 1)


def mime(path):
    if str(path).endswith(".js"):
        return "application/javascript"
    value = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    return value + "; charset=utf-8" if value in ("text/html", "text/css") else value


def statistics(context):
    if context.get("statistics_disabled"):
        return "NO STATISTICS - approved fallback; strong-lighting pass retained; no borrowed cohort."
    family, requested, matched = (context[k] for k in ("family", "requested_environment", "matched_environment"))
    if not context["exact_environment_match"]:
        return f"RELATED SAME-PRODUCT COHORT: {family}/{requested} -> {matched}; n={context['cohort_n']}."
    return f"MATCHED COHORT: {family}/{matched}; n={context['cohort_n']} (caption-derived evidence)."


def prepare_baseline():
    root, cases = generate.verify()
    c = study.client()
    objects = {}
    for name in ("data.json", "results.json"):
        response = c.get_object(Bucket=study.BUCKET, Key=RECOVERY + "/" + name)
        body = response["Body"].read()
        study.emit(study.HERE / "baseline_source" / name, body)
        objects[name] = {
            "key": RECOVERY + "/" + name, "etag": response["ETag"],
            "version_id": response.get("VersionId"), "sha256": study.digest(body),
        }
    original = study.load(study.HERE / "source/fe/data.json")
    fe = {study.prompt_key(row): row for row in original["rows"]}
    records = {row["case"]["prompt_key"]: row
               for row in study.load(study.HERE / "baseline_source/results.json")}
    media = {row["meta_data"]["evalset_item_id"]: row
             for row in study.load(study.HERE / "baseline_source/data.json")["rows"]}
    native_cards = {}
    for group in study.load(study.HERE / "source/baseline_recovery/data.json")["groups"]:
        native = next(item for item in group["experiments"] if item["id"] == "native")
        for card in native["cards"]:
            key = card["prompt_key"]
            if key in native_cards:
                raise ValueError("Duplicated final V6.4 native slot")
            native_cards[key] = {**card, "image": urljoin(LIVE, card["image"])}
    if not (len(cases) == len(fe) == len(records) == len(media) == len(native_cards) == 160):
        raise ValueError("The final original baseline does not cover160 unique slots")
    catalogue = {ref.id: ref for ref in generate.load_catalog(generate.CATALOG)}

    def one(case):
        key = case["prompt_key"]
        record, original_row, card = records[key], fe[key], native_cards[key]
        native, previous = record["native"], record["case"]
        if (native["status"] != "ok" or native["size"] != "2368x1776"
                or native["input_fingerprint"] != previous["user_prompt_sha256"]
                or previous["user_prompt"] != original_row["images"][5]["text_content"]
                or card["prompt"] != previous["user_prompt"] or card["status"] != "ok"
                or card["image"] != original_row["images"][1]["image_src"]):
            raise ValueError("Displayed second-column image/prompt differs from its final native record")
        folder = RECOVERY + "/records/" + case["id"] + "/native/"
        response = c.get_object(Bucket=study.BUCKET, Key=folder + "native_calls.json")
        journal = response["Body"].read()
        study.emit(study.HERE / "baseline_source/calls" / (case["id"] + ".json"), journal)
        calls = json.loads(journal)
        edits = [(i, call) for i, call in enumerate(calls, 1) if call["kind"] == "image"]
        if len(edits) != 1 or edits[0][1]["status"] != "ok":
            raise ValueError("The original native image has no unambiguous single completed image call")
        image_request_key = folder + f"native_{edits[0][0]:02d}_request.json"
        image_request = c.get_object(Bucket=study.BUCKET, Key=image_request_key)["Body"].read()
        study.emit(study.HERE / "baseline_source/image_requests" / (case["id"] + ".json"), image_request)
        request = json.loads(image_request)
        if request["prompt"] != native["prompt"] or len(request["images"]) != 1:
            raise ValueError("The baseline image prompt/guide is not from its displayed generation")
        image_response = c.get_object(Bucket=study.BUCKET, Key=study.key_for(card["image"]))
        pixels = image_response["Body"].read()
        if (study.digest(pixels) != edits[0][1]["sha256"]
                or Image.open(io.BytesIO(pixels)).size != generate.SIZE
                or not image_response["ContentType"].startswith("image/")):
            raise ValueError("The reused V6.4 pixels differ from the actual original native image call")
        image_path = root / "baseline_images" / (study.digest(pixels) + ".png")
        study.emit(image_path, pixels)
        source_row = media[case["id"]]
        guides = [urljoin(study.GATEWAY + RECOVERY + "/viewer.html", asset["image_src"])
                  for asset in source_row["images"]
                  if asset.get("meta_text", {}).get("label") == "Shared native geometry guide"]
        if len(guides) != 1:
            raise ValueError("The original native guide is unavailable or ambiguous")
        guide_response = c.get_object(Bucket=study.BUCKET, Key=study.key_for(guides[0]))
        guide = guide_response["Body"].read()
        if study.digest(guide) != request["images"][0]["sha256"]:
            raise ValueError("Original native guide differs from the original actual image-model input")
        guide_path = root / "baseline_guides" / (study.digest(guide) + ".png")
        study.emit(guide_path, guide)
        reference = catalogue[native["ref_ids"][0]]
        reference_path = root / "baseline_references" / (
            study.digest(reference.data) + "." + reference.mime.split("/")[1])
        study.emit(reference_path, reference.data)
        return key, {
            "case_id": case["id"], "image": card["image"], "image_path": str(image_path),
            "image_sha256": study.digest(pixels), "etag": image_response["ETag"],
            "version_id": image_response.get("VersionId"), "content_type": image_response["ContentType"],
            "result": native, "prompt": previous["user_prompt"],
            "guide": {"url": guides[0], "path": str(guide_path), "sha256": study.digest(guide)},
            "reference": {"path": str(reference_path), "sha256": study.digest(reference.data),
                          "id": reference.id},
            "original_record_url": study.GATEWAY + folder + "result.json",
            "image_request_url": study.GATEWAY + image_request_key,
        }

    with ThreadPoolExecutor(max_workers=8) as pool:
        bindings = dict(pool.map(one, cases))
    result = {
        "at_utc": study.now(), "rows": len(bindings), "objects": objects, "bindings": bindings,
        "frozen_files": {
            str(path): study.sha(path)
            for path in (study.HERE / "baseline_source").rglob("*") if path.is_file()
        },
        "original_primary_outcome": {"success": 138, "failed": 22},
        "final_no_statistics_cases": sum(
            item["result"]["scap_context"].get("statistics_disabled", False) for item in bindings.values()),
    }
    study.emit(study.HERE / "baseline_bindings.json", result)
    study.emit(root / "baseline_bindings.json", result)
    print({"reused_baseline_images": len(bindings), "actual_native_pixel_and_guide_bindings": len(bindings),
           "final_no_statistics_cases": result["final_no_statistics_cases"]})


def merge_fe(original, new):
    result = copy.deepcopy(original)
    pair = copy.deepcopy(original)
    pair["rows"] = []
    seen = set()
    for row in result["rows"]:
        key = study.prompt_key(row)
        if key in seen or key not in new:
            raise ValueError("Missing or duplicated exact native/source row binding")
        seen.add(key)
        item = new[key]
        if ([a["asset_type"] for a in row["images"]] != ["image"] * 5 + ["text"] * 2
                or row["images"][6]["text_content"] != item["prompt"]["text"]):
            raise ValueError("The original V6.5 source prompt or five-column contract differs")
        image = {
            "asset_type": "image", "is_model_input_or_output": "model_output",
            "image_src": item["output"]["image"], "meta_text": {"label": study.LABEL},
        }
        row["images"].insert(5, image)
        details = row["meta_data"]["key_val_informations"]
        details["V6.5 / V15.8 environment"] = item["prompt"]["environment"]
        details["V6.5 / V15.8 statistics"] = item["output"]["statistics_status"]
        paired = copy.deepcopy(row)
        paired["images"] = [copy.deepcopy(row["images"][i]) for i in (1, 5, 6, 7)]
        pair["rows"].append(paired)
    if seen != set(new) or len(seen) != 160:
        raise ValueError("The FE comparison omits native slots")
    result["meta_texts"][0] = "HP lifestyle - V6.4 four-way + V6.5 V15.7 / V15.8 (160 matched rows)"
    pair["meta_texts"][0] = TITLE + " (160 matched rows)"
    for data, count in ((result, 6), (pair, 2)):
        data["meta_texts"][1][1].update({
            "Layout": f"160 device/camera/rank-matched rows; {count} image columns.",
            "Images": "Existing images retained unchanged;160 new V6.5 native PR4619 outputs.",
            "Matching": "Device/camera/prompt rank, not identical scenes or paired random seeds.",
            "V6.5": "Training-grounded original source texts; exact pinned PR4619/V15.8 native2368x1776.",
            "Statistics": "Per-row V6.5 status is explicit; approved no-statistics cases retain strong lighting.",
        })
    return result, pair


def viewer(original, labels, title, count):
    match = re.search(r"const METHOD_RATING_DEFS = (\[[^\n]*\])\.map\(text => \(\{", original)
    if match is None or len(json.loads(match[1])) != 5:
        raise ValueError("Original five-method rating definitions differ")
    original_labels = json.loads(match[1])
    if (count == 6 and labels[:5] != original_labels) or (count == 2 and labels[0] != original_labels[1]):
        raise ValueError("Original method-rating identities do not match the retained columns")
    text = once(original, match[0], match[0].replace(match[1], json.dumps(labels)))
    title_match = re.search(r"<title>[^<]+</title>", text)
    if title_match is None:
        raise ValueError("Original review title is missing")
    text = once(text, title_match[0], "<title>" + html.escape(title) + "</title>")
    text = once(text, "grid-template-columns: repeat(5, auto);",
                f"grid-template-columns: repeat({count}, auto);")
    text = once(text, "repeat(5,minmax(0,1fr))", f"repeat({count},minmax(0,1fr))")
    text = once(text, "repeat(5,240px)", f"repeat({count},240px)")
    summary = re.search(r'<details id="columnChangeSummary".*?</details>', text, re.S)
    if summary is None or summary[0].count("<section>") != 5:
        raise ValueError("Original five-column designer brief differs")
    addition = (
        "<section><h3>Column 6 - V6.5 / V15.8</h3><ul>"
        "<li>Same original training-grounded V6.5 user prompt as Column 5.</li>"
        "<li>Exact PR4619 pipeline: statistics-supported background and strong natural lighting.</li>"
        "<li>Approved no-statistics cases are labeled; the lighting pass is retained.</li>"
        "<li>No extra lookup-blue or artistic-wall intervention; no people.</li>"
        "</ul></section>"
    )
    if count == 6:
        brief = once(summary[0], "</div></details>", addition + "</div></details>")
    else:
        brief = (
            '<details id="columnChangeSummary" open><summary>V6.4 vs V6.5 - same V15.8 pipeline</summary>'
            '<div class="column-change-grid">'
            "<section><h3>V6.4 / V15.8</h3><ul><li>Existing second-column images, unchanged.</li>"
            "<li>Statistics and strong lighting, with the original disclosed exceptions.</li></ul></section>"
            "<section><h3>V6.5 / V15.8</h3><ul><li>New images from training-grounded V6.5 user prompts.</li>"
            "<li>Same native canvas and source product/camera assignments.</li>"
            "<li>Explicit no-statistics labels; strong lighting retained.</li></ul></section>"
            "</div></details>"
        )
    text = once(text, summary[0], brief)
    text = once(text, "'Mark all five methods '",
                "'Mark all six methods '" if count == 6 else "'Mark both methods '")
    text = once(text, "'v64-v65-five-method-ratings.json'",
                "'v64-v65-six-method-ratings.json'" if count == 6 else "'v64-v65-v158-paired-ratings.json'")
    return text


def merge_grouped(original, new_cards, baseline_cards):
    extended, paired = copy.deepcopy(original), copy.deepcopy(original)
    seen = set()
    for old_group, pair_group in zip(extended["groups"], paired["groups"]):
        if len(old_group["experiments"]) != 2:
            raise ValueError("Original grouped report no longer has two experiments")
        keys = [old_group["id"] + "::p" + str(rank) for rank in range(1, 11)]
        if any(key in seen or key not in new_cards or key not in baseline_cards for key in keys):
            raise ValueError("Grouped comparison omits or duplicates native ranks")
        for experiment in old_group["experiments"]:
            if ([card["prompt_key"] for card in experiment["cards"]] != keys
                    or [card["rank"] for card in experiment["cards"]] != list(range(1, 11))):
                raise ValueError("An existing grouped rank/input binding differs")
        for rank, key in enumerate(keys, 1):
            for cards in (new_cards, baseline_cards):
                if cards[key]["prompt_key"] != key or cards[key]["rank"] != rank:
                    raise ValueError("A new or reused grouped card has an incorrect key/rank binding")
        seen.update(keys)
        candidate = {"id": CELL, "label": study.LABEL, "cards": [copy.deepcopy(new_cards[k]) for k in keys]}
        old_group["experiments"].append(candidate)
        pair_group["experiments"] = [{
            "id": BASELINE_CELL, "label": baseline_cards[keys[0]]["label"],
            "cards": [copy.deepcopy(baseline_cards[k]) for k in keys],
        }, copy.deepcopy(candidate)]
    if len(seen) != 160 or seen != set(new_cards) or seen != set(baseline_cards):
        raise ValueError("Grouped comparison is not complete160-way coverage")
    extended.update(title="HP lifestyle - V6.4/V6.5 V15.7 + V6.5 V15.8",
                    experiment_count=3, image_count=480,
                    source_url=study.GATEWAY + study.FE_PREFIX + "/viewer.html?q=W10%3D&ldap=hshariati")
    paired.update(title=TITLE + " -16 inputs x10 prompts", experiment_count=2, image_count=320,
                  source_url=study.GATEWAY + study.PREFIX + "/fe/viewer.html?q=W10%3D&ldap=hshariati")
    return extended, paired


def build():
    root, cases = generate.verify()
    audit = study.load(study.HERE / "generation_audit.json")
    if (not audit["full160_complete"] or audit["status"] != "passed"
            or audit["auditor_sha256"] != study.sha(study.HERE / "audit.py")):
        raise ValueError("Do not build or publish before all160 actual native audits pass")
    baseline = study.load(study.HERE / "baseline_bindings.json")
    original_fe = study.load(study.HERE / "source/fe/data.json")
    original_grouped = study.load(study.HERE / "source/grouped/data.json")
    source_fe = {study.prompt_key(row): row for row in original_fe["rows"]}
    for path, expected in baseline["frozen_files"].items():
        if study.sha(path) != expected:
            raise ValueError("Frozen final-baseline evidence changed")
    entries = {}

    def add(key, path, original=None):
        path = Path(path)
        value = {"path": str(path), "sha256": study.sha(path), "bytes": path.stat().st_size,
                 "content_type": mime(path), "original": original}
        if key in entries:
            if any(entries[key][field] != value[field]
                   for field in ("sha256", "bytes", "content_type", "original")):
                raise ValueError("Publication key collision")
        else:
            entries[key] = value
        return study.GATEWAY + key

    def asset(path, expected=None):
        path = Path(path)
        checksum = study.sha(path)
        if expected is not None and checksum != expected:
            raise ValueError("Audited native image/input changed before publication")
        return add(study.PREFIX + "/assets/inputs/" + checksum + path.suffix, path)

    by_audit = {row["prompt_key"]: row for row in audit["audits"]}
    new, new_cards, baseline_cards = {}, {}, {}
    baseline_label = original_fe["rows"][0]["images"][1]["meta_text"]["label"]
    for case in cases:
        key = case["prompt_key"]
        proof = by_audit[key]
        complete = proof["native_completion"]
        native = study.load(complete["result_path"])
        image = add(study.PREFIX + "/assets/outputs/" + case["id"] + ".png",
                    complete["image_path"])
        if entries[study.key_for(image)]["sha256"] != complete["image_sha256"]:
            raise ValueError("Native output changed")
        inputs = {role: asset(proof[role]["path"], proof[role]["sha256"])
                  for role in ("product", "reference", "geometry_guide")}
        record_path = PUBLIC / "records" / (case["id"] + ".json")
        study.emit(record_path, {
            "case": case, "native_result": native, "native_audit": proof,
            "execution_manifest_sha256": audit["execution_manifest_sha256"],
            "raw_image_sha256": complete["image_sha256"],
        })
        record_url = add(study.PREFIX + "/records/" + record_path.name, record_path)
        inputs["audit_url"] = record_url
        output = {
            "status": "done", "image": image, "image_sha256": complete["image_sha256"],
            "inputs": inputs, "record_url": record_url, "native_result": native,
            "statistics_status": statistics(native["scap_context"]),
        }
        new[key] = {"prompt": case["prompt"], "source_input": case["source_input"], "output": output}
        new_cards[key] = {
            "rank": case["rank"], "prompt_key": key, "prompt": case["prompt"]["text"],
            "environment": case["prompt"]["environment"], "image": image,
            "image_sha256": complete["image_sha256"], "inputs": inputs,
            "generation_prompt": native["prompt"], "record_url": record_url,
            "statistics_status": output["statistics_status"],
        }
        previous = baseline["bindings"][key]
        old_inputs = {
            "product": inputs["product"], "reference": asset(previous["reference"]["path"]),
            "geometry_guide": previous["guide"]["url"], "audit_url": previous["image_request_url"],
        }
        baseline_cards[key] = {
            "rank": case["rank"], "prompt_key": key, "prompt": previous["prompt"],
            "environment": source_fe[key]["meta_data"]["key_val_informations"]["Environment"],
            "image": previous["image"], "image_sha256": previous["image_sha256"],
            "inputs": old_inputs, "generation_prompt": previous["result"]["prompt"],
            "record_url": previous["original_record_url"], "label": baseline_label,
            "statistics_status": statistics(previous["result"]["scap_context"]),
        }
    six, pair = merge_fe(original_fe, new)
    three, grouped_pair = merge_grouped(original_grouped, new_cards, baseline_cards)
    labels = [a["meta_text"]["label"] for a in original_fe["rows"][0]["images"][:5]]
    viewer_source = (study.HERE / "source/fe/viewer.html").read_text()
    source = study.load(study.HERE / "source_manifest.json")

    def output(path, key, value, original=None):
        study.emit(path, value)
        add(key, path, original)

    output(STAGING / "fe/data.json", study.FE_PREFIX + "/data.json", six, source["objects"]["fe/data.json"])
    output(STAGING / "fe/viewer.html", study.FE_PREFIX + "/viewer.html",
           viewer(viewer_source, labels + [study.LABEL], six["meta_texts"][0], 6).encode(),
           source["objects"]["fe/viewer.html"])
    output(PUBLIC / "fe/data.json", study.PREFIX + "/fe/data.json", pair)
    output(PUBLIC / "fe/viewer.html", study.PREFIX + "/fe/viewer.html",
           viewer(viewer_source, [baseline_label, study.LABEL], pair["meta_texts"][0], 2).encode())
    main = (study.HERE / "source/grouped/main.js").read_text()
    main = once(main, "![2, 4].includes(value.experiment_count)", "![2, 3, 4].includes(value.experiment_count)")
    main = once(main, '<details class="source-prompt"',
                '${card.statistics_status ? `<p class="statistics-status">${escapeHtml(card.statistics_status)}</p>` : ""}\n'
                '        <details class="source-prompt"')
    index = (study.HERE / "source/grouped/index.html").read_text()
    for directory, prefix, data, count, name in (
        (STAGING / "grouped", study.GROUP_PREFIX, three, 3, "v6_5_pr4619_20261112"),
        (PUBLIC / "gallery", study.PREFIX + "/gallery", grouped_pair, 2, None),
    ):
        data_name = f"data_{name}.json" if name else "data.json"
        script_name = f"main_{name}.js" if name else "main.js"
        style_name = f"style_{name}.css" if name else "style.css"
        output(directory / data_name, prefix + "/" + data_name, data)
        output(directory / script_name, prefix + "/" + script_name,
               once(main, '"./data.json"', json.dumps("./" + data_name)).encode())
        output(directory / style_name, prefix + "/" + style_name,
               (study.HERE / "source/grouped/style.css").read_bytes()
               + b"\n.controls label{max-width:100%;min-width:0}.controls select{min-width:0;max-width:100%}\n")
        page = once(index, "each of 2 experiments.", f"each of {count} experiments.")
        page = once(page, "All 2 experiments", f"All {count} experiments")
        page = once(page, "V6.5 is the training-grounded replacement:30 reused images and130 new. No judge scores.",
                    "V6.5/V15.8 adds160 new native PR4619 outputs. Statistics exceptions are explicit. No judge scores.")
        page = once(page, '<script src="./main.js">', f'<script src="./{script_name}">')
        page = once(page, 'href="./style.css"', f'href="./{style_name}"')
        page = once(page, "<title>HP lifestyle diversity - V6.4 vs training-grounded V6.5</title>",
                    "<title>" + html.escape(data["title"]) + "</title>")
        page = once(page, "<h1>HP lifestyle diversity - V6.4 vs training-grounded V6.5</h1>",
                    "<h1>" + html.escape(data["title"]) + "</h1>")
        if name is None:
            output(directory / "imsauth.js", prefix + "/imsauth.js",
                   (study.HERE / "source/grouped/imsauth.js").read_bytes())
        output(directory / "index.html", prefix + "/index.html", page.encode(),
               source["objects"]["grouped/index.html"] if name else None)
    output(PUBLIC / "data/generation.json", study.PREFIX + "/data/generation.json", {
        "at_utc": audit["at_utc"], "commit": study.COMMIT, "rows": list(new.values()),
        "counts": {key: audit[key] for key in ("rows", "no_statistics_cases", "native_attempts",
                                             "sdk_requests", "sdk_completed_responses")},
    })
    links = [
        study.GATEWAY + study.GROUP_PREFIX + "/index.html",
        study.GATEWAY + study.FE_PREFIX + "/viewer.html?q=W10%3D&ldap=hshariati",
        study.GATEWAY + study.PREFIX + "/fe/viewer.html?q=W10%3D&ldap=hshariati",
        study.GATEWAY + study.PREFIX + "/gallery/index.html",
    ]
    output(PUBLIC / "data/provenance.json", study.PREFIX + "/data/provenance.json", {
        "commit": study.COMMIT, "size": list(generate.SIZE), "new_images": 160,
        "new_no_statistics_cases": audit["no_statistics_cases"],
        "baseline_no_statistics_cases": baseline["final_no_statistics_cases"],
        "execution_manifest_sha256": audit["execution_manifest_sha256"],
        "source_manifest_sha256": study.sha(study.HERE / "source_manifest.json"),
        "generation_audit_sha256": study.sha(study.HERE / "generation_audit.json"),
        "matching": "Exact device/camera/rank; not identical scenes or paired image seeds.",
        "old_columns_and_native_pixels_preserved": True,
        "reports": links,
    })
    study.emit(study.HERE / "report_links.txt", ("\n".join(links) + "\n").encode())
    study.emit(study.HERE / "publication_manifest.json", {
        "at_utc": audit["at_utc"], "entries": entries, "links": links,
        "builder_sha256": study.sha(Path(__file__)),
        "generation_audit_sha256": study.sha(study.HERE / "generation_audit.json"),
        "baseline_bindings_sha256": study.sha(study.HERE / "baseline_bindings.json"),
    })
    print({"publication_objects": len(entries), "report_bindings": [480, 960, 320, 320]})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare_baseline", "build"])
    args = parser.parse_args()
    if args.command == "prepare_baseline":
        prepare_baseline()
    else:
        build()
