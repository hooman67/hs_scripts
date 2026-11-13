"""Audit actual160 outputs and extend the frozen live reports without replacing old cells."""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import posixpath
from urllib.parse import urljoin

import study

HERE = study.HERE
PUBLIC = HERE / "public"
STAGING = HERE / "extension"
BASE = study.GATEWAY + study.PREFIX + "/"
FULL = "eval_sets/" + study.COMPARISON.name
GROUPED = "eval_sets/" + study.GROUPED.name
CELL = "v6_5_pr4523"
SUFFIX = "v6_5_training_160_20261112"
FULL_DATA = f"data/comparison_{SUFFIX}.json"
FULL_JS = f"gallery/main.{SUFFIX}.js"
FULL_CSS = f"gallery/style.{SUFFIX}.css"
GROUP_DATA = f"gallery/data.{SUFFIX}.json"
GROUP_JS = f"gallery/main.{SUFFIX}.js"
GROUP_CSS = f"gallery/style.{SUFFIX}.css"


def emit(path, value):
    body = value if isinstance(value, bytes) else (
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode()
    path = Path(path)
    if path.exists():
        if path.read_bytes() != body:
            raise ValueError(f"saved artifact differs: {path}")
    else:
        study.write(path, body)


def native():
    return study.module("v65_full160_strong_native_auditor", study.LEGACY / "report.py")


def audit():
    manifest = study.verify()
    counts = study.counts()
    if counts["done"] != 160 or counts["failed"] or counts["pending"]:
        raise ValueError("all160 successful final outputs are required")
    auditor = native()
    twins = {
        (row["digital_twin_id"], row["camera_id"]): row
        for row in study.load(study.ENDPOINT / "input_bundle/manifest.json")["entries"]
    }
    reused = {row["prompt_key"]: row for row in manifest["reused"]}
    successful_models, new_successful_models = Counter(), Counter()
    final_jobs, hashes = set(), set()
    for prompt in study.load(study.SOURCE)["prompts"]:
        old = prompt["prompt_key"] in reused
        item = auditor.audit_one(prompt, twins, old)
        successful_models.update(item["models"])
        if not old:
            new_successful_models.update(item["models"])
        run = study.PRIOR / "run" if old else HERE / "run"
        record = study.image_runner().valid_completed_record(run, study.row_for(prompt))
        final_jobs.add(record["job_id"])
        hashes.add(record["image_sha256"])
    if (
        len(final_jobs) != 160 or len(hashes) != 160
        or successful_models != Counter({"gpt-6-astra": 480, "gpt-image-2.5-sunburst-2026-09-08": 160})
        or new_successful_models != Counter({"gpt-6-astra": 390, "gpt-image-2.5-sunburst-2026-09-08": 130})
    ):
        raise ValueError("final unique jobs/raw PNGs/native model calls do not reconcile")
    failed_jobs = {}
    extra_by_row = Counter()
    for path in sorted((HERE / "recovery").glob("attempt_*/manifest.json")):
        attempt = study.load(path)
        if attempt["study_manifest_sha256"] != study.sha(HERE / "study_manifest.json"):
            raise ValueError("recovery belongs to another study")
        for failure in attempt["failures"]:
            job_id = failure["failed_job_id"]
            if job_id in failed_jobs or job_id in final_jobs:
                raise ValueError("failed native attempt is duplicated or was silently relabeled")
            for metadata in failure["client_files"].values():
                if study.sha(Path(metadata["archived_path"])) != metadata["sha256"]:
                    raise ValueError("original failed client evidence changed")
            for name, digest in failure["native_files_sha256"].items():
                if study.sha(Path(name)) != digest:
                    raise ValueError("original failed native evidence changed")
            failed_jobs[job_id] = failure
            extra_by_row[failure["row_id"]] += 1
    runner = study.image_runner()
    extra_models = Counter()
    for job_id in failed_jobs:
        root = study.ENDPOINT / "run/jobs" / job_id
        status = study.load(root / "status.json")
        if not status["done"] or status["stages"]["scene"]["status"] != "error":
            raise ValueError("preserved failed job is not terminal failed")
        for call in study.load(root / "calls.json"):
            request = study.load(root / call["requestArtifact"])
            response = study.load(root / call["responseArtifact"])
            if (
                runner.canonical_sha256(request) != call["requestSha256"]
                or runner.canonical_sha256(response) != call["responseSha256"]
                or call["kind"] != "chat_json" or call["status"] != "done"
                or request["model"] != "gpt-6-astra" or response["model"] != "gpt-6-astra"
                or response["choices"][0]["finish_reason"] != "stop"
                or request["max_completion_tokens"] != 16384 or request["store"] is not False
                or "reasoning_effort" in request or "temperature" in request
            ):
                raise ValueError("extra failed-attempt native call differs from the frozen contract")
            extra_models.update([request["model"]])
    events = [
        json.loads(line) for line in (HERE / "run/journals/events.jsonl").read_text().splitlines()
    ]
    submitted = [event["row_id"] for event in events if event["event"] == "submit_started"]
    saved = [str(event["job_id"]) for event in events if event["event"] == "submit_saved"]
    expected_submissions = Counter(manifest["new_row_ids"]) + extra_by_row
    new_final_ids = final_jobs - {item["job_id"] for item in manifest["reused"]}
    native_ids = {path.name for path in (study.ENDPOINT / "run/jobs").iterdir() if path.is_dir()}
    if (
        Counter(submitted) != expected_submissions or len(saved) != len(set(saved))
        or set(saved) != native_ids or native_ids != new_final_ids | set(failed_jobs)
    ):
        raise ValueError("primary/replacement submissions and actual native jobs do not reconcile")
    initial = study.load(HERE / "generation_terminal.json")
    result = {
        "status": "passed", "at_utc": study.now(), "rows": 160, "reused": 30, "new": 130,
        "new_submissions": len(submitted), "failures": 0, "replacements": len(failed_jobs),
        "initial_primary_terminal": initial, "failed_attempts_preserved": len(failed_jobs),
        "unique_jobs": 160, "unique_raw_pngs": 160, "total_new_native_jobs": len(native_ids),
        "combined_models": dict(successful_models + extra_models),
        "new_models": dict(new_successful_models + extra_models),
        "successful_output_models": dict(successful_models),
        "new_successful_output_models": dict(new_successful_models),
        "extra_failed_attempt_models": dict(extra_models),
        "all_native_request_response_and_raw_output_hashes_verified": True,
        "successful_images_resampled": 0, "new_model_calls_for_audit": 0,
    }
    emit(HERE / "generation_audit.json", result)
    print(json.dumps({key: result[key] for key in (
        "rows", "new", "replacements", "new_models", "extra_failed_attempt_models",
    )}), flush=True)


def rebase(value, prefix, origin=None):
    key = study.key_for(urljoin(origin or BASE, value))
    return posixpath.relpath(key, prefix + "/gallery")


def full_merge(old, source):
    if len(old["rows"]) != 160 or len(old["cells"]) != 3 or CELL in old["cells"]:
        raise ValueError("expected the frozen three-column160 comparison")
    by_slot = {tuple(row["key"]): row for row in source["rows"]}
    if len(by_slot) != 160 or set(by_slot) != {tuple(row["key"]) for row in old["rows"]}:
        raise ValueError("all160 unique device/camera/rank slots must match")
    result = copy.deepcopy(old)
    for row in result["rows"]:
        new = by_slot[tuple(row["key"])]
        for field in ("device_id", "camera_tag", "bank_rank", "source_camera_name", "render_lookup"):
            if new["prompt"][field] != row["prompt_v6_4"][field]:
                raise ValueError("new prompt changed fixed product/view/rank")
        if new["source_input"] != row["source_input_v6_4"] or new["output"]["status"] != "done":
            raise ValueError("new source input differs or actual output is incomplete")
        row["prompt_v6_5"] = copy.deepcopy(new["prompt"])
        row["source_input_v6_5"] = copy.deepcopy(new["source_input"])
        row["bank_audit_v6_5"] = copy.deepcopy(new["bank_audit"])
        output = copy.deepcopy(new["output"])
        for field in ("image", "record_url", "job_url", "status_url"):
            output[field] = rebase(output[field], FULL)
        output["inputs"] = {name: rebase(value, FULL) for name, value in output["inputs"].items()}
        row["outputs"][CELL] = output
    result["cells"][CELL] = copy.deepcopy(source["counts"])
    result["actual_input_audits"] = 640
    result["built_at_utc"] = source["built_at_utc"]
    result["v6_5_text_recovery_provenance"] = source["text_recovery_provenance"]
    return result


def fe_merge(old, original, source):
    if len(old["rows"]) != 160 or any(len(row["images"]) != 3 for row in old["rows"]):
        raise ValueError("expected160 original FE rows with three image columns")
    by_slot = {tuple(row["key"]): row for row in source["rows"]}
    if len(by_slot) != 160 or len(original["rows"]) != 160:
        raise ValueError("missing or duplicate new FE slots")
    vendor = study.module(
        "v65_full160_official_fe",
        Path.home() / ".claude/scripts/fe_html/parquet_to_fe_html.py",
    )
    result = copy.deepcopy(old)
    for row, original_row in zip(result["rows"], original["rows"]):
        if row["meta_data"]["evalset_item_id"] != original_row["prompt"]["prompt_key"]:
            raise ValueError("original FE row/annotation identity differs")
        new = by_slot[tuple(original_row["key"])]
        study.key_for(new["output"]["image"])
        item = vendor.manifest_to_data_json({"rows": [{
            "row_idx": row["meta_data"]["row_idx"],
            "evalset_item_id": row["meta_data"]["evalset_item_id"],
            "assets": [{"kind": "image", "src": new["output"]["image"], "label": study.TITLE}],
        }]}, is_secure=True, title=None)
        row["images"].append(item["rows"][0]["images"][0])
    result["meta_texts"][0] += " + training-grounded V6.5 / V15.7"
    return result


def grouped_merge(old, source, full):
    if old["group_count"] != 16 or old["experiment_count"] != 3 or old["image_count"] != 480:
        raise ValueError("expected the original sixteen three-experiment input groups")
    by_slot = {tuple(row["key"]): row for row in source["rows"]}
    if len(by_slot) != 160:
        raise ValueError("expected160 unique actual V6.5 slots")
    result = copy.deepcopy(old)
    origin = study.GATEWAY + GROUPED + "/gallery/index.html"
    full_origin = study.GATEWAY + FULL + "/gallery/index.html"
    full_slots = {tuple(row["key"]): row for row in full["rows"]}
    used = set()
    for group in result["groups"]:
        if len(group["experiments"]) != 3:
            raise ValueError("original input group has unexpected experiment count")
        for experiment in group["experiments"]:
            if [card["rank"] for card in experiment["cards"]] != list(range(1, 11)):
                raise ValueError("original group has missing, duplicated or reordered ranks")
            for card in experiment["cards"]:
                slot = (group["device_id"], group["camera_tag"], card["rank"])
                original = full_slots[slot]
                field = "prompt_v6_4" if experiment["id"] == "v6_4_pr4523" else "prompt"
                output = original["outputs"][experiment["id"]]
                if (
                    card["prompt"] != original[field]["text"]
                    or card["image_sha256"] != output["image_sha256"]
                    or urljoin(origin, card["image"]) != urljoin(full_origin, output["image"])
                ):
                    raise ValueError("existing grouped card differs from its actual detailed source")
        cards = []
        context = None
        for rank in range(1, 11):
            slot = (group["device_id"], group["camera_tag"], rank)
            new = by_slot[slot]
            prompt, output = new["prompt"], new["output"]
            if (
                output["status"] != "done" or prompt["bank_rank"] != rank
                or prompt["device_id"] != slot[0] or prompt["camera_tag"] != slot[1]
                or new["source_input"] != full_slots[slot]["source_input_v6_4"]
            ):
                raise ValueError("new grouped output/source/rank binding differs")
            if context is not None and context != new["source_input"]:
                raise ValueError("new group mixes source inputs")
            context = new["source_input"]
            cards.append({
                "rank": rank, "prompt_key": prompt["prompt_key"], "prompt": prompt["text"],
                "environment": prompt["environment"], "image": rebase(output["image"], GROUPED),
                "image_sha256": output["image_sha256"],
                "inputs": {name: rebase(value, GROUPED) for name, value in output["inputs"].items()},
                "generation_prompt": output["scene_debug"]["finalPrompt"],
                "record_url": rebase(output["record_url"], GROUPED),
            })
            used.add(slot)
        group["experiments"].append({"id": CELL, "label": study.TITLE, "cards": cards})
        group["contexts"].append({"label": "V6.5 - training-grounded replacement", "input": context})
    if used != set(by_slot):
        raise ValueError("grouped report omits or duplicates input slots")
    result.update(
        title="HP lifestyle diversity - 16 inputs x 10 prompts x 4 experiments",
        experiment_count=4, image_count=640,
    )
    two = copy.deepcopy(result)
    two.update(
        title="HP lifestyle diversity - V6.4 vs training-grounded V6.5",
        experiment_count=2, image_count=320,
    )
    for group in two["groups"]:
        group["contexts"] = group["contexts"][1:]
        group["experiments"] = [
            item for item in group["experiments"] if item["id"] in ("v6_4_pr4523", CELL)
        ]
        if [item["id"] for item in group["experiments"]] != ["v6_4_pr4523", CELL]:
            raise ValueError("V6.4/V6.5-only comparison has unexpected experiment identity")
        for experiment in group["experiments"]:
            for card in experiment["cards"]:
                slot = (group["device_id"], group["camera_tag"], card["rank"])
                card["image"] = rebase(card["image"], study.PREFIX, origin)
                if experiment["id"] == "v6_4_pr4523":
                    output = full_slots[slot]["outputs"]["v6_4_pr4523"]
                    card["inputs"] = {
                        name: rebase(value, study.PREFIX, full_origin)
                        for name, value in output["inputs"].items()
                    }
                    card["generation_prompt"] = output["scene_debug"]["finalPrompt"]
                    card["record_url"] = rebase(output["record_url"], study.PREFIX, full_origin)
                else:
                    card["inputs"] = {
                        name: rebase(value, study.PREFIX, origin)
                        for name, value in card["inputs"].items()
                    }
                    card["record_url"] = rebase(card["record_url"], study.PREFIX, origin)
    return result, two


def once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f"template anchor is not unique: {old[:100]}")
    return text.replace(old, new, 1)


def templates():
    main = (HERE / "gallery/main.js").read_text()
    old_grouped = (HERE / "baseline_live/grouped/gallery/index.html").read_text()
    css = (HERE / "baseline_live/grouped/gallery/style.css").read_bytes() + (
        b"\n.model-inputs img{max-width:100%;height:auto}.model-inputs p{overflow-wrap:anywhere}\n"
    )
    for label, destination, count, data_path, js_path, css_path in (
        ("V6.4 vs training-grounded V6.5", PUBLIC, 2, "./data.json", "main.js", "style.css"),
        ("Four-experiment diversity comparison", STAGING / "grouped", 4,
         "./" + GROUP_DATA.split("/")[-1], GROUP_JS.split("/")[-1], GROUP_CSS.split("/")[-1]),
    ):
        html = once(old_grouped, "<title>HP lifestyle diversity - grouped inputs</title>",
                    f"<title>HP lifestyle diversity - {label}</title>")
        html = once(html, "<h1>HP lifestyle diversity</h1>", f"<h1>HP lifestyle diversity - {label}</h1>")
        html = once(html, "each of three experiments.", f"each of {count} experiments.")
        if count == 2:
            html = once(html, "V6.4 uses different source documents.",
                        "V6.4 and V6.5 use the same structured source inputs.")
        html = once(html, "No new generation or judging.",
                    "V6.5 is the training-grounded replacement:30 reused images and130 new. No judge scores.")
        html = once(html, 'src="./main.js"', f'src="./{js_path}"')
        html = once(html, 'href="./style.css"', f'href="./{css_path}"')
        html = once(html, "All three experiments", f"All {count} experiments")
        emit(destination / "gallery/index.html", html.encode())
        emit(destination / ("gallery/" + js_path), once(main, '"./data.json"', json.dumps(data_path)).encode())
        emit(destination / ("gallery/" + css_path), css)
    emit(PUBLIC / "gallery/imsauth.js",
         (HERE / "baseline_live/grouped/gallery/imsauth.js").read_bytes())
    old_main = (HERE / "baseline_live/full/gallery/main.js").read_text()
    old_data = study.load(HERE / "study_manifest.json")["baseline_live_objects"]["full/data.json"]["key"]
    relative_data = posixpath.relpath(old_data, FULL + "/gallery")
    full_main = once(old_main, json.dumps(relative_data), json.dumps("../" + FULL_DATA))
    anchor = '        <div class="image-scroll"><div class="image-grid">'
    full_main = once(full_main, anchor, """        <p><strong>V6.5 training-grounded source prompt</strong></p>
        <p class="prompt">${escapeHtml(row.prompt_v6_5.text)}</p>
        ${jsonDetails("Full V6.5 Smart Brief, source messaging and camera input", row.source_input_v6_5)}
        ${jsonDetails("Full V6.5 writer record and recovered text provenance", row.prompt_v6_5)}
        ${jsonDetails("V6.5 bank debug and source provenance", row.bank_audit_v6_5)}
""" + anchor)
    anchor = '        ${outputHtml(row.outputs.v6_4_pr4523, "V6.4 / PR 4523 - V15.7 shapes")}'
    full_main = once(full_main, anchor, anchor + (
        '\n        ${outputHtml(row.outputs.v6_5_pr4523, "V6.5 / PR 4523 - V15.7 shapes")}'
    ))
    full_main = once(full_main, "${JSON.stringify(row.prompt_v6_4)}",
                     "${JSON.stringify(row.prompt_v6_4)} ${JSON.stringify(row.prompt_v6_5)}")
    emit(STAGING / "full" / FULL_JS, full_main.encode())
    css = (HERE / "baseline_live/full/gallery/style.css").read_text()
    emit(STAGING / "full" / FULL_CSS, once(css, "repeat(3,", "repeat(4,").encode())
    html = (HERE / "baseline_live/full/gallery/index.html").read_text()
    manifest = study.load(HERE / "study_manifest.json")["baseline_live_objects"]
    for label, target in (("main.js", FULL_JS), ("style.css", FULL_CSS)):
        current = manifest["full/gallery/" + label]["key"].split("/")[-1]
        html = once(html, "./" + current, "./" + target.split("/")[-1])
    html = once(html, "<title>HP V6.3 vs V6.4 full160 - exact PR4417 / PR4523</title>",
                "<title>HP V6.3 / V6.4 / V6.5 full160 - exact PR4417 / PR4523</title>")
    html = once(html, "HP V6.3 vs V6.4 full160 - three generation columns",
                "HP V6.3 / V6.4 / V6.5 full160 - four generation columns")
    html = once(html, "for480 outputs total.", "for480 pre-existing outputs, plus160 V6.5 outputs =640 total.")
    intro = (
        '<p>The fourth column is the training-grounded replacement '
        '<strong>V6.5 / PR 4523 - V15.7 shapes</strong>, with30 reused images and130 new. '
        'Its original native text trial remains0 successful/16 failed;15 authorized extra repairs '
        'and recognition-only revalidation completed the160 unchanged final texts. '
        f'<a href="{BASE}data/text_completion_audit.json">Text recovery audit</a> | '
        f'<a href="{BASE}gallery/index.html">V6.4/V6.5 groups-of-ten comparison</a></p>'
    )
    emit(STAGING / "full/gallery/index.html", once(html, "</header>", intro + "</header>").encode())


def build():
    manifest = study.verify()
    auditor = native()
    audit_result = study.load(HERE / "generation_audit.json")
    if audit_result["status"] != "passed" or audit_result["rows"] != 160:
        raise ValueError("all160 actual native audits are required")
    source = study.load(study.SOURCE)
    reused = {row["prompt_key"]: row for row in manifest["reused"]}
    rows = []
    for prompt in source["prompts"]:
        row = study.row_for(prompt)
        old = reused.get(prompt["prompt_key"])
        paths = study.image_runner().paths(study.PRIOR / "run" if old else HERE / "run", row)
        record = study.image_runner().valid_completed_record(
            study.PRIOR / "run" if old else HERE / "run", row)
        if record is None:
            raise ValueError("audited successful output changed")
        audit_path = HERE / "input_audit" / (row["row_slug"] + ".json")
        inputs = study.load(audit_path)
        if inputs["record_sha256"] != study.sha(paths["record"]):
            raise ValueError("audited record changed before build")
        if old:
            prior_base = study.GATEWAY + "eval_sets/" + study.PRIOR.name + "/"
            image = prior_base + "assets/outputs/" + row["row_slug"] + ".png"
            urls = {
                role: prior_base + "assets/inputs/" + inputs[role]["sha256"] + "." + inputs[role]["suffix"]
                for role in auditor.ROLES
            }
        else:
            image = auditor.copy_asset(paths["image"], "assets/outputs/" + row["row_slug"] + ".png",
                                       record["image_sha256"])
            urls = {
                role: auditor.copy_asset(inputs[role]["path"], "assets/inputs/" +
                                         inputs[role]["sha256"] + "." + inputs[role]["suffix"],
                                         inputs[role]["sha256"]) for role in auditor.ROLES
            }
        urls["audit_url"] = auditor.copy_asset(audit_path, "data/input_audits/" + audit_path.name)
        output = {
            "status": "done", "error": None, "reuse_status": "reused" if old else "new",
            "image": image, "inputs": urls, "job_id": record["job_id"],
            "image_sha256": record["image_sha256"], "run_sha256": record["run_sha256"],
            "record_sha256": study.sha(paths["record"]), "lineage": record["lineage"],
            "origin_study_manifest_sha256": study.sha(
                (study.PRIOR if old else HERE) / "study_manifest.json"),
            "scene_debug": record["scene_debug"],
            **{name + "_url": auditor.copy_asset(paths[name], f"data/{folder}/" + paths[name].name)
               for name, folder in (("record", "records"), ("job", "jobs"), ("status", "status"))},
        }
        bank = source["bank_audit"][prompt["bank_debug_ref"]]
        rows.append({
            "key": [prompt["device_id"], prompt["camera_tag"], prompt["bank_rank"]],
            "prompt": prompt, "source_input": bank["source_input"], "bank_audit": bank, "output": output,
        })
    prior = study.module("v65_full160_final_text_source", study.PRIOR / "study.py")
    text_completion = study.load(prior.TEXT_SNAPSHOT / "exports/completion_audit.json")
    provenance = {
        key: text_completion[key] for key in (
            "original_native_successful_banks", "original_native_failed_banks",
            "accepted_unchanged_banks", "additional_semantic_calls", "actual_semantic_calls",
            "bounded_recovery_successful_banks", "bounded_recovery_failed_banks",
            "extra_replies_offline_revalidated",
        )
    }
    data = {
        "title": study.TITLE, "status": "complete", "built_at_utc": audit_result["at_utc"],
        "counts": study.counts(), "actual_input_audits": 160, "rows": rows,
        "matching": "device/camera/bank rank; not semantic equivalence or paired seeds",
        "text_recovery_provenance": provenance,
    }
    emit(PUBLIC / "data/generation.json", data)
    for path, name in (
        (Path(manifest["source_export"]), "data/prompts_all_v6_5_160.json"),
        (Path(manifest["source_export"]).with_suffix(".txt"), "data/prompts_all_v6_5_160.txt"),
        (prior.TEXT_SNAPSHOT / "exports/completion_audit.json", "data/text_completion_audit.json"),
        (HERE / "study_manifest.json", "data/study_manifest.json"),
        (HERE / "generation_audit.json", "data/generation_audit.json"),
    ):
        auditor.copy_asset(path, name)
    old = study.load(HERE / "baseline_live/full/data.json")
    emit(STAGING / "full" / FULL_DATA, full_merge(old, data))
    emit(STAGING / "full/fe/data.json", fe_merge(
        study.load(HERE / "baseline_live/full/fe/data.json"), old, data))
    four, two = grouped_merge(study.load(HERE / "baseline_live/grouped/data.json"), data, old)
    emit(STAGING / "grouped" / GROUP_DATA, four)
    emit(PUBLIC / "gallery/data.json", two)
    templates()
    assets = {
        path.relative_to(PUBLIC).as_posix(): {"sha256": study.sha(path), "bytes": path.stat().st_size}
        for path in sorted(PUBLIC.rglob("*")) if path.is_file()
    }
    emit(PUBLIC / "asset_manifest.json", {
        "assets": assets, "reused_images_referenced_in_place": 30, "new_image_uploads": 130,
        "study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
    })
    entries = {}
    for root, prefix in ((PUBLIC, study.PREFIX), (STAGING / "full", FULL), (STAGING / "grouped", GROUPED)):
        for path in sorted(root.rglob("*")):
            if path.is_file():
                key = prefix + "/" + path.relative_to(root).as_posix()
                entries[key] = {"path": str(path), "sha256": study.sha(path), "bytes": path.stat().st_size}
    emit(HERE / "publication_manifest.json", {
        "entries": entries, "mutable_keys": [
            FULL + "/gallery/index.html", FULL + "/fe/data.json", GROUPED + "/gallery/index.html",
        ], "study_manifest_sha256": study.sha(HERE / "study_manifest.json"),
        "source_code_sha256": {name: study.sha(HERE / name) for name in ("report.py", "gallery/main.js")},
    })
    print(json.dumps({"new_grouped_images": 320, "existing_grouped_images": 640,
                      "full160_columns": 4, "publication_objects": len(entries)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("audit", "build"))
    globals()[parser.parse_args().command]()
