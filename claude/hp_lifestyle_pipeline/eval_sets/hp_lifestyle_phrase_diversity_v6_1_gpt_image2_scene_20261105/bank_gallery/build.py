#!/usr/bin/env python3
"""Reformat the completed V6.1 gallery using the published V6 bank UI."""
import hashlib
import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source"
OUT = ROOT / "built"
PROJECT = ROOT.parents[2]
MANIFEST = PROJECT / "judge/placement/versions/v3/data/new_v6_1_eval_20261105/manifest.json"
PREFIX = "eval_sets/hp_lifestyle_phrase_diversity_v6_1_gpt_image2_scene_20261105"
BUCKET = "foundry-hp-enterprise-adobe-assets"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    live = json.loads((SOURCE / "data.json").read_text())
    prompt_path = Path(live["source"]["path"])
    prompt_raw = prompt_path.read_bytes()
    assert digest(prompt_raw) == live["source"]["sha256"]
    document = json.loads(prompt_raw)
    candidates = {p["prompt_key"]: p for p in document["prompts"]}
    assets = json.loads(MANIFEST.read_text())
    assets_by_key = {r["scene_prompt_source"]["prompt_key"]: r for r in assets["records"]}
    assert len(candidates) == len(assets_by_key) == len(live["rows"]) == 160
    assert set(candidates) == {r["row_id"] for r in live["rows"]} == set(assets_by_key)
    assert live["status_counts"] == {"done": 160}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "assets/digital_twins").mkdir(parents=True, exist_ok=True)
    (OUT / "downloads").mkdir(parents=True, exist_ok=True)
    (OUT / "downloads/prompts_all_160.json").write_bytes(prompt_raw)

    rows, banks, sources, copied = [], {}, {}, {}
    for original in live["rows"]:
        key = original["row_id"]
        p = candidates[key]
        a = assets_by_key[key]
        assert original["prompt"] == p["text"] == a["scene_prompt"]
        assert original["environment"] == p["environment"]
        assert original["source_relevance_score"] == p["source_relevance_score"]
        assert original["ctech_reference_score"] == p["ctech_reference_score"]
        assert original["bank_rank"] == p["bank_rank"]
        assert original["device_id"] == p["device_id"] == a["device"]
        assert original["camera_tag"] == p["camera_tag"] == a["view"]["camera_tag"]
        assert original["job_id"] == a["generation_provenance"]["job_id"]
        assert original["image_url"] == a["generated_image"]["public_url"]
        assert original["scene_debug"]["originalPrompt"] == p["text"]
        bank_id = key.split("::")[0]
        twin = a["twin_image"]
        twin_path = Path(twin["local_path"])
        if twin["render_id"] not in copied:
            raw = twin_path.read_bytes()
            assert digest(raw) == twin["sha256"] and len(raw) == twin["bytes"]
            filename = twin["filename"]
            assert Path(filename).name == filename
            (OUT / "assets/digital_twins" / filename).write_bytes(raw)
            copied[twin["render_id"]] = {**twin, "published_path": f"assets/digital_twins/{filename}"}
        assert copied[twin["render_id"]]["sha256"] == twin["sha256"]
        image = a["generated_image"]
        assert image["s3_uri"] == f"s3://{BUCKET}/{PREFIX}/images/{image['filename']}"
        assert digest(Path(image["local_path"]).read_bytes()) == image["sha256"]
        render = {**twin, "gallery_path": f"./assets/digital_twins/{twin['filename']}"}
        generated = {**image, "gallery_path": f"../images/{image['filename']}",
                     "native_width": image["width"], "native_height": image["height"]}
        record = {"job_id": original["job_id"], "original_gallery_row_id": key,
                  "generation_endpoint": live["endpoint"], "catalog": live["catalog"],
                  "digital_twin_id": original["digital_twin_id"], "camera_id": original["camera_id"],
                  "prompt": original["prompt"], "usedPrompt": original["scene_debug"].get("finalPrompt"),
                  "generated_image": generated, "debugData": original["scene_debug"],
                  "provenance": a["generation_provenance"], "stage_provenance": a["stage_provenance"],
                  "raw_request_available": False}
        rows.append({"row_id": a["id"], "prompt_key": key, "bank_id": bank_id,
                     "device_id": p["device_id"], "device_type": p["device_type"],
                     "camera_tag": p["camera_tag"], "candidate": p, "status": "done",
                     "corrected_input": render, "record": record,
                     "provenance": {"generation": a["generation_provenance"],
                                    "prompt_document_sha256": live["source"]["sha256"]}})
        if bank_id not in banks:
            banks[bank_id] = {k: p[k] for k in ["device_id", "device_display_name", "device_type", "source_pair", "camera_tag", "source_camera_name", "view_role"]}
            banks[bank_id].update(bank_id=bank_id, prompt_keys=[], candidate_count=10,
                                  generated_selection_count=10, prompt_only_count=0)
            audit = document["bank_audit"][bank_id]
            sources[bank_id] = {**audit["source_input"],
                               "input_path": audit["case_metadata"]["input_source_path"],
                               "input_sha256": audit["source_input_sha256"],
                               "source_revision": audit["selected_source_revision"]}
        banks[bank_id]["prompt_keys"].append(key)

    by_key = {r["prompt_key"]: r for r in rows}
    for bank in banks.values():
        bank["prompt_keys"].sort(key=lambda k: by_key[k]["candidate"]["bank_rank"])
        assert [by_key[k]["candidate"]["bank_rank"] for k in bank["prompt_keys"]] == list(range(1, 11))
    # Match the reference's device/view grouping rather than generation queue order.
    ordered_banks = list(dict.fromkeys(p["bank_debug_ref"] for p in document["prompts"]))
    assert len(ordered_banks) == len(banks) == len(copied) == 16
    ordered_rows = [by_key[k] for b in ordered_banks for k in banks[b]["prompt_keys"]]
    data = {"version": "v6.1-gpt-image-2.5-bank-gallery-v1",
            "metadata": {"bank_count": 16, "generation_row_count": 160,
                         "generation_status_counts": {"done": 160},
                         "built_at_utc": datetime.now(timezone.utc).isoformat(),
                         "source_updated_at_utc": live["updated_at_utc"],
                         "environments": sorted({r["candidate"]["environment"] for r in rows}),
                         "downloads": [{"label": "All 160 prompts (JSON)", "path": "./downloads/prompts_all_160.json"},
                                       {"label": "Gallery data (JSON)", "path": "./downloads/gallery_data.json"},
                                       {"label": "Original gallery", "path": "../gallery/index.html"}]},
            "sources": sources, "banks": [banks[b] for b in ordered_banks], "rows": ordered_rows}
    raw = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    for forbidden in ["x-amz-signature=", "x-amz-credential=", '"authorization":', '"access_token":', '"api_key":']:
        assert forbidden not in raw.lower(), forbidden
    (OUT / "data.js").write_text("const GENERATION_DATA = " + raw + ";\n")
    (OUT / "downloads/gallery_data.json").write_text(raw + "\n")
    for name in ["style.css", "imsauth.js"]:
        shutil.copyfile(SOURCE / "reference_gallery" / name, OUT / name)
    html = (SOURCE / "reference_index.html").read_text()
    html = html.replace("HP Lifestyle V6 · Preview generation", "HP Lifestyle V6.1 · GPT Image 2.5 scene generations")
    html = html.replace("bank-organized V6 preview gallery", "bank-organized V6.1 scene gallery")
    html = html.replace("V6 authored 10 ranked prompts for every bank. Ranks 1–6 were sent to image generation; ranks 7–10 are shown as prompt-only candidates.", "V6.1 authored 10 ranked prompts for every bank. All 10 have completed scene-generation images using GPT Image 2.5.")
    html = html.replace('aria-label="V6 prompts,', 'aria-label="V6.1 prompts,')
    html = html.replace("Full debug / request", "Pipeline debug / provenance")
    (OUT / "index.html").write_text(html)
    js = (SOURCE / "reference_gallery/main.js").read_text()
    js = js.replace('const imagePath = value => `../${value}`;', 'const imagePath = value => value;')
    js = js.replace('"Top-six generated"', '"Generated"')
    js = js.replace('View full debug / request', 'View pipeline debug / generation context')
    js = js.replace('  refreshBankSelector();\n', '  refreshBankSelector(new URLSearchParams(location.search).get("bank") || "");\n')
    (OUT / "main.js").write_text(js)
    dump(ROOT / "build_manifest.json", {"built_at_utc": data["metadata"]["built_at_utc"],
         "counts": {"prompts": 160, "banks": 16, "twins": 16, "generated": 160},
         "bank_sizes": dict(Counter(r["bank_id"] for r in rows)),
         "source_gallery_sha256": digest((SOURCE / "data.json").read_bytes()),
         "prompt_document_sha256": digest(prompt_raw), "asset_manifest_sha256": digest(MANIFEST.read_bytes()),
         "actual_twin_sources": list(copied.values()),
         "files": [{"path": str(f.relative_to(OUT)), "bytes": f.stat().st_size, "sha256": digest(f.read_bytes())}
                   for f in sorted(OUT.rglob("*")) if f.is_file()]})
    print(json.dumps({"output": str(OUT), "rows": 160, "banks": 16, "twins": 16}))


if __name__ == "__main__":
    main()
