import argparse
import concurrent.futures
import io
import json
import mimetypes
import shutil

from PIL import Image
from pilot import BUCKET, CODE, ROOT, digest, load, maybe_s3_client, save

TEMPLATE = ROOT.parent / "v64-full30/viewer-template.html"
SCRIPTS = {name: ROOT / name for name in ("pilot.py", "report_pilot.py")}


def validate():
    cases = load(ROOT / "pilot-cases.json")
    manifest = load(ROOT / "pilot-manifest.json")
    summary = load(ROOT / "pilot-generation-summary.json")
    assert summary["completed"] == len(cases) == manifest["cases"] and summary["status"] != "running"
    assert {case["group"] for case in cases} == set(manifest["authorized_groups"])
    assert len({case.get("row_idx", case["rank"]) for case in cases}) == len(cases)
    for name, checksum in manifest["source_files"].items():
        assert digest((CODE / name).read_bytes()) == checksum
    records = []
    for case in cases:
        folder = ROOT / "run/rows" / case["id"]
        result = load(folder / "result.json")
        calls = load(folder / "native_calls.json")
        assert result["input_fingerprint"] == case["user_prompt_sha256"]
        assert result["scap_inputs"] == manifest["scap_identity"]
        assert digest((ROOT / case["baseline_path"]).read_bytes()) == case["baseline_sha256"]
        if result["status"] == "ok":
            assert [call["kind"] for call in calls] == ["text"] * 5 + ["image"]
            assert all(call["status"] == "ok" for call in calls)
            raw = (folder / "gpt_1.png").read_bytes()
            assert raw == (folder / "ours.png").read_bytes()
            assert digest(raw) == calls[-1]["sha256"]
            assert Image.open(io.BytesIO(raw)).size == (2368, 1776)
            assert result["image_calls"] == 1 and not result["graded"] and not result["aligned"]
            source_pixels = Image.open(ROOT / case["product_path"]).convert("RGB").tobytes()
            assert Image.open(folder / "input.png").convert("RGB").tobytes() == source_pixels
            image_request = load(folder / "native_06_request.json")
            assert image_request["prompt"] == result["prompt"]
            assert len(image_request["images"]) == 1 and image_request["mask"] is None
            assert image_request["images"][0]["sha256"] == digest((folder / "geometry_guide.png").read_bytes())
            base = load(folder / "scap_base_writing_response.json")
            assert (result["camera"], result["layout"]) == (base["camera"], base["layout"])
            plan = load(folder / "geometry_response.json")
            assert result["scap_context"]["environment_selection"] == plan["statistics_environment"]
            context = result["scap_context"]
            assert context["family"] == {"laptop": "Laptop", "printer": "Printer"}[case.get("category", "laptop")]
            assert context["environment_selection"]["prompt_quote"] in case["user_prompt"]
            assert context["original_user_prompt"] == case["user_prompt"]
        else:
            assert result["error"] and sum(c["kind"] == "image" for c in calls) <= 1
        records.append({
            "id": case["id"], "rank": case["rank"], "status": result["status"],
            "error": result["error"], "native_calls": len(calls),
        })
    receipt = {
        "passed": True, "cases": len(cases), "success": summary["success"], "failed": summary["failed"],
        "commit": manifest["commit"], "native_contracts_checked": True,
        "exact_prompts_and_baselines_checked": True, "records": records,
    }
    save(ROOT / "pilot-validation.json", receipt)
    print(json.dumps(receipt), flush=True)


def build():
    assert load(ROOT / "pilot-validation.json")["passed"]
    cases, manifest = load(ROOT / "pilot-cases.json"), load(ROOT / "pilot-manifest.json")
    summary = load(ROOT / "pilot-generation-summary.json")
    output = ROOT / "comparison"
    output.mkdir(exist_ok=True)

    def asset(path, relative):
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        return relative

    def image(src, label, kind="model_output"):
        return {"asset_type": "image", "is_model_input_or_output": kind,
                "image_src": src, "meta_text": {"label": label}}

    def text(label, value):
        return {"asset_type": "text", "text_content": value, "meta_text": {"label": label}}

    rows, records = [], []
    for case in cases:
        rank = case.get("row_idx", case["rank"])
        folder = ROOT / "run/rows" / case["id"]
        result = load(folder / "result.json")
        before = asset(ROOT / case["baseline_path"], f"images/{rank}-before.png")
        product = asset(ROOT / case["product_path"], f"inputs/{case['product_sha256']}-product.png")
        media = [image(product, "Original product input", "model_input"),
                 image(before, "V6.4 / archived PR #4523 baseline")]
        context = result.get("scap_context", {})
        details = {
            "Generation": "Complete; no user visual acceptance" if result["status"] == "ok" else result["error"],
            "Device": case["device"], "Camera": case["camera"], "Prompt rank": case["rank"],
            "Input group": case["group"],
            "Output provenance": "Pilot output reused unchanged" if case.get("reused_from") else "New native output",
            "Environment": case["environment"], "Execution": "Fresh native PR #4619",
            "Source commit": manifest["commit"], "Controls": manifest["limits"],
        }
        inputs = {"product": product}
        if result["status"] == "ok":
            after = asset(folder / "gpt_1.png", f"images/{rank}-after.png")
            guide = asset(folder / "geometry_guide.png", f"inputs/{rank}-native-guide.png")
            reference = next(folder.glob("ref_2.*"))
            ref = asset(reference, f"inputs/{rank}-native-reference{reference.suffix}")
            inputs.update(guide=guide, reference=ref)
            media.extend([
                image(after, "V6.4 / native PR #4619 + adaptive backgrounds + realism"),
                image(ref, "Native generation style reference", "model_input"),
            ])
            density = result["background_density"]
            details.update({
                "Support shape": result["geometry"]["support_top_shape"],
                "Statistics cohort": f"{context['family']} / {context['matched_environment']}",
                "Cohort match": "Direct" if context["exact_environment_match"] else "Related same-product fallback",
                "Cohort reason": context["match_reason"],
                "Requested setting evidence": context["environment_selection"]["prompt_quote"],
                "Planned additions": "; ".join(a["component"] for a in density["additions"]) or "None",
                "Reference ID": ", ".join(result["ref_ids"]),
            })
            media.extend([
                text("Semantic environment and background plan", json.dumps({
                    "cohort": {k: v for k, v in context.items() if k != "fields"},
                    "density": density,
                }, indent=2, ensure_ascii=False)),
                text("Text-only realism plan", json.dumps(load(folder / "realism_rewrite_response.json")["realism_plan"],
                                                          indent=2, ensure_ascii=False)),
            ])
        else:
            media.append(text("Native generation failed - no replacement image", result["error"]))
        media.extend([
            text("V6.4 user prompt", case["user_prompt"]),
            text("Exact baseline image prompt", case["baseline_prompt"]),
            text("Exact native image prompt", result["prompt"] or "No image prompt produced."),
        ])
        rows.append({
            "meta_data": {"row_idx": rank, "evalset_item_id": case["id"], "key_val_informations": details},
            "images": media,
        })
        records.append({"case": case, "result": result, "published_inputs": inputs})
        for path in sorted(folder.glob("*.json")):
            asset(path, f"records/{case['id']}/{path.name}")
    save(output / "data.json", {
        "is_secure": True,
        "meta_texts": [
            manifest.get("title", "V6.4 native PR #4619 pilot: Cashmere / Back_Right_CloseUp - 10 variations"),
            ["Experiment", {
                "Scope": manifest.get("scope", "Only the first grouped-gallery row, ranks 1-10. No other device/camera rows run."),
                "Results": f"{summary['success']}/{len(cases)} complete; {summary['failed']} failed.",
                "Left": "Archived V6.4 / PR #4523 V15.7 shapes, exact matching prompt.",
                "Right": "Fresh native PR #4619, adaptive backgrounds + text-only realism.",
                "Source": manifest["commit"],
                "Camera": manifest["camera_input"], "Replanned": manifest["replanned"],
                "Limits": manifest["limits"],
                "Calls": f"{summary['text_calls']} text / {summary['image_calls']} image calls; no retries or grading.",
                "Reused pilot outputs": summary.get("reused", 0),
                "Prior failed pilot case": manifest.get("prior_failure_policy", "Preserved as failed without retry."),
                "Spelling": "Semantic Stage A setting selection, supported labels and exact prompt evidence; no extra classification call.",
                "Review": "Good/Bad per method; all-good/all-bad applies to every loaded variation; browser save and JSON export.",
                "Inputs": "Toggle Inputs off to compare only the two output images.",
            }],
        ],
        "links": {
            "Source grouped gallery": "https://foundry-aws-corp.adobe.io/asset/" + BUCKET
            + "/eval_sets/hp_lifestyle_grouped_diversity_20261111/gallery/index.html",
            "PR #4619": "https://github.com/Adobe-Firefly/foundry/pull/4619",
            "Exact inputs, prompts and provenance": "results.json",
            "Run manifest": "manifest.json",
        },
        "rows": rows,
    })
    save(output / "results.json", records)
    for name in ("viewer.html", "index.html"):
        asset(TEMPLATE, name)
    for source, target in (
        ("pilot-manifest.json", "manifest.json"), ("pilot-cases.json", "cases.json"),
        ("pilot-generation-summary.json", "generation_summary.json"),
        ("pilot-validation.json", "validation.json"), ("profiles.json", "profiles.json"),
    ):
        asset(ROOT / source, target)
    for name, path in SCRIPTS.items():
        asset(path, "source/" + name)
    for name in manifest["source_files"]:
        asset(CODE / name, "source/" + name)
    receipt = {"files": {
        p.relative_to(output).as_posix(): digest(p.read_bytes())
        for p in sorted(output.rglob("*")) if p.is_file()
    }}
    save(ROOT / "pilot-build-receipt.json", receipt)
    print(json.dumps({"built": len(cases), "success": summary["success"], "files": len(receipt["files"])}), flush=True)


def publish():
    manifest, receipt = load(ROOT / "pilot-manifest.json"), load(ROOT / "pilot-build-receipt.json")
    browser = load(ROOT / "pilot-browser-check.json")
    assert browser["passed"] and browser["build_receipt"] == receipt
    s3 = maybe_s3_client(BUCKET)
    prefix = manifest["s3_prefix"]
    assert prefix == "hp-data-artifacts/hp-3p-gpt25/" + manifest["run_id"]
    assert not s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix + "/", MaxKeys=1).get("KeyCount", 0)

    def upload(relative):
        body = (ROOT / "comparison" / relative).read_bytes()
        assert digest(body) == receipt["files"][relative]
        key = prefix + "/" + relative
        s3.put_object(
            Bucket=BUCKET, Key=key, Body=body,
            ContentType=mimetypes.guess_type(relative)[0] or "application/octet-stream",
            CacheControl="no-cache" if relative.endswith(".html") else "max-age=300",
            Metadata={"sha256": digest(body)}, IfNoneMatch="*",
        )
        assert s3.get_object(Bucket=BUCKET, Key=key)["Body"].read() == body
        return {"path": relative, "sha256": digest(body), "bytes": len(body)}

    names = list(receipt["files"])
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        objects = list(pool.map(upload, [name for name in names if not name.endswith(".html")]))
    objects.extend(upload(name) for name in names if name.endswith(".html"))
    url = "https://foundry-aws-corp.adobe.io/asset/" + BUCKET + "/" + prefix + "/viewer.html?q=W10%3D"
    save(ROOT / "pilot-publication-receipt.json", {"url": url, "verified_objects": len(objects), "files": objects})
    print(json.dumps({"url": url, "verified_objects": len(objects)}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("validate", "build", "publish"))
    args = parser.parse_args()
    {"validate": validate, "build": build, "publish": publish}[args.action]()
