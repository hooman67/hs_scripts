import argparse
import concurrent.futures
import hashlib
import io
import json
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

from foundry_aws_gateway import maybe_s3_client
from PIL import Image

ROOT = Path(__file__).resolve().parent
CODE = ROOT / "code-semantic"
BUCKET = "foundry-hp-enterprise-adobe-assets"
COMMIT = "db074bd9ab8f832712aa45415435dfa647e51ced"
GROUP = "cashmere__laptop_BackRightCloseUp"
BASELINE = "eval_sets/hp_lifestyle_v6_4_full160_pr4523_20261110/"
CATALOG = Path(
    "/home/colligo/.copilot/session-state/5f54e036-596a-48cc-a064-ae83ffe2bb38/"
    "files/stats-rewriter-experiment/reference_catalog.json"
)
sys.path.insert(0, str(CODE))


def load(path):
    return json.loads(path.read_text())


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


def digest(body):
    return hashlib.sha256(body).hexdigest()


def prepare():
    from hp3p.catalog import load_catalog
    from hp3p.mask import prepare as prepare_product
    from hp3p.scap import ScapProfiles

    assert not (ROOT / "pilot-manifest.json").exists(), "Pilot already prepared"
    gallery = load(ROOT / "gallery-data.json")
    group = gallery["groups"][0]
    assert group["id"] == GROUP
    experiment = next(e for e in group["experiments"] if e["id"] == "v6_4_pr4523")
    assert len(experiment["cards"]) == 10
    assert [card["rank"] for card in experiment["cards"]] == list(range(1, 11))
    sources = {r["prompt"]["prompt_key"]: r for r in load(ROOT / "generation.json")["rows"]}
    prompts = {p["prompt_key"]: p for p in load(ROOT / "prompts_all_v6_4_160.json")["prompts"]}
    s3 = maybe_s3_client(BUCKET)
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)

    def fetch(url, expected):
        parsed = urlparse(url)
        prefix = "/asset/" + BUCKET + "/"
        assert parsed.hostname == "foundry-aws-corp.adobe.io" and parsed.path.startswith(prefix)
        key = unquote(parsed.path[len(prefix):])
        assert key.startswith((
            BASELINE, "eval_sets/hp_lifestyle_v6_4_pr4523_30_20261110/",
        )) and ".." not in key.split("/")
        suffix = Path(key).suffix
        assert re.fullmatch(r"[a-f0-9]{64}", expected) and suffix in (".png", ".webp", ".jpg")
        path = assets / (expected + suffix)
        if not path.exists():
            path.write_bytes(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())
        assert digest(path.read_bytes()) == expected
        return path.relative_to(ROOT).as_posix()

    cases = []
    for card in experiment["cards"]:
        source = sources[card["prompt_key"]]
        prompt = prompts[card["prompt_key"]]
        assert source["prompt"]["text"] == prompt["text"] == card["prompt"]
        assert digest(card["prompt"].encode()) == prompt["text_sha256"]
        output = source["output"]
        debug = output["scene_debug"]
        assert output["image_sha256"] == card["image_sha256"]
        assert debug["originalPrompt"] == card["prompt"]
        product_url = output["inputs"]["product"]
        product_sha = Path(urlparse(product_url).path).stem
        case = {
            "id": card["prompt_key"].replace("::", "__"),
            "prompt_key": card["prompt_key"], "rank": card["rank"],
            "group": GROUP, "device": group["device"], "camera": group["camera"],
            "environment": card["environment"], "user_prompt": card["prompt"],
            "user_prompt_sha256": prompt["text_sha256"],
            "product_path": fetch(product_url, product_sha), "product_sha256": product_sha,
            "baseline_path": fetch(output["image"], card["image_sha256"]),
            "baseline_sha256": card["image_sha256"], "baseline_prompt": debug["finalPrompt"],
            "baseline_reference": output["inputs"]["reference"],
            "baseline_guide": output["inputs"]["geometry_guide"],
            "source_camera_metadata": debug["twinCamera"],
            "source_input": source["source_input"], "prompt_provenance": prompt,
        }
        assert re.fullmatch(r"[A-Za-z0-9_-]+", case["id"])
        cases.append(case)
    assert len({c["product_sha256"] for c in cases}) == 1
    assert len({json.dumps(c["source_camera_metadata"], sort_keys=True) for c in cases}) == 1
    for case in cases:
        body = (ROOT / case["product_path"]).read_bytes()
        prepared, _ = prepare_product(body, (2368, 1776))
        assert Image.open(io.BytesIO(body)).convert("RGB").tobytes() == Image.open(
            io.BytesIO(prepared)
        ).tobytes()
    shutil.copyfile(ROOT.parent / "v64-full30/profiles.json", ROOT / "profiles.json")
    shutil.copyfile(CATALOG, ROOT / "reference_catalog.json")
    catalog = load_catalog(ROOT / "reference_catalog.json")
    captions = load(ROOT / "ref_captions.json")
    assert len(catalog) == 341 and all(ref.id in captions for ref in catalog)
    profiles = ScapProfiles(ROOT / "profiles.json", realism=True)
    run_id = "hp10-v64-native-pr4619-cashmere-backright-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    manifest = {
        "run_id": run_id, "s3_prefix": "hp-data-artifacts/hp-3p-gpt25/" + run_id,
        "commit": COMMIT, "pr": 4619, "cases": 10, "authorized_groups": [GROUP],
        "execution": "Fresh native hp3p.pipeline.run_row, not the frozen-input adapter.",
        "reference_count": 1, "captions": True, "size": "2368x1776", "workers": 2,
        "camera_input": "Original digital-twin camera metadata, not archived Stage B wording or layout.",
        "replanned": ["reference selection", "support geometry", "guide", "Stage B", "adaptive backgrounds", "realism"],
        "limits": "Not an isolated background/realism A/B: references, support geometry, guide and writing are replanned. Raw product pixels and source digital-twin camera are shared inputs, not pixel-fidelity guarantees.",
        "automatic_retries": 0, "grading": False, "postprocessing": False,
        "scap_identity": profiles.identity,
        "catalog_sha256": digest((ROOT / "reference_catalog.json").read_bytes()),
        "captions_sha256": digest((ROOT / "ref_captions.json").read_bytes()),
        "gallery_sha256": digest((ROOT / "gallery-data.json").read_bytes()),
        "source_files": {
            p.relative_to(CODE).as_posix(): digest(p.read_bytes())
            for p in sorted((CODE / "hp3p").rglob("*")) if p.is_file() and p.suffix in (".py", ".txt")
        },
        "validation": "194 offline tests passed; Ruff and whitespace checks passed.",
    }
    save(ROOT / "pilot-cases.json", cases)
    save(ROOT / "pilot-manifest.json", manifest)
    print(json.dumps({"prepared": 10, "group": GROUP, "commit": COMMIT, "run_id": run_id}), flush=True)


class AuditClient:
    def __init__(self, base, out):
        self.base, self.out, self.calls = base, out, []

    def chat_json(self, system, text, images, schema):
        from hp3p.reference_blue import attachments

        number = len(self.calls) + 1
        call = {"kind": "text", "status": "running", "started_at": time.time()}
        self.calls.append(call)
        save(self.out / f"native_{number:02}_request.json", {
            "kind": "text", "system": system, "text": text, "schema": schema,
            "images": attachments(images), "max_retries": 0,
        })
        try:
            response = self.base.chat_json(system, text, images, schema)
            save(self.out / f"native_{number:02}_response.json", response)
            call["status"] = "ok"
            return response
        except Exception as exc:
            call.update(status="error", error=str(exc))
            raise
        finally:
            call["ended_at"] = time.time()
            save(self.out / "native_calls.json", self.calls)

    def edit_image(self, prompt, images, size, mask=None):
        from hp3p.reference_blue import attachments

        assert len(images) == 1 and size == "2368x1776" and mask is None
        number = len(self.calls) + 1
        call = {"kind": "image", "status": "running", "started_at": time.time()}
        self.calls.append(call)
        save(self.out / f"native_{number:02}_request.json", {
            "kind": "image", "prompt": prompt, "images": attachments(images),
            "size": size, "mask": None, "n": 1, "max_retries": 0,
        })
        try:
            body = self.base.edit_image(prompt, images, size)
            call.update(status="ok", sha256=digest(body), bytes=len(body))
            return body
        except Exception as exc:
            call.update(status="error", error=str(exc))
            raise
        finally:
            call["ended_at"] = time.time()
            save(self.out / "native_calls.json", self.calls)


def generate():
    from hp3p.catalog import load_catalog
    from hp3p.evalset import Row
    from hp3p.openai_client import OpenAIClient
    from hp3p.pipeline import run_row
    from hp3p.scap import ScapProfiles

    manifest, cases = load(ROOT / "pilot-manifest.json"), load(ROOT / "pilot-cases.json")
    assert len(cases) == manifest["cases"] == 10 and {c["group"] for c in cases} == {GROUP}
    for name, checksum in manifest["source_files"].items():
        assert digest((CODE / name).read_bytes()) == checksum, name
    with (ROOT / "generation.lock").open("x") as lock:
        lock.write(manifest["run_id"] + "\n")
    run = ROOT / "run"
    assert not (run / "rows").exists(), "Never retry or reuse a partial native run silently"
    catalog = load_catalog(ROOT / "reference_catalog.json")
    captions = load(ROOT / "ref_captions.json")
    profiles = ScapProfiles(ROOT / "profiles.json", realism=True)
    assert profiles.identity == manifest["scap_identity"]
    base = OpenAIClient()
    summary = {"status": "running", "expected": 10, "completed": 0, "success": 0, "failed": 0, "rows": []}
    save(ROOT / "pilot-generation-summary.json", summary)
    print(json.dumps({"started": 10, "workers": 2, "commit": COMMIT}), flush=True)

    def one(case):
        out = run / "rows" / case["id"]
        out.mkdir(parents=True)
        audit = AuditClient(base, out)
        row = Row(case["id"], case["user_prompt"], case["product_path"], 2368, 1776, [])
        result = run_row(
            row, audit, catalog, run, (ROOT / case["product_path"]).read_bytes(), captions,
            ref_count=1, size=(2368, 1776), camera=case["source_camera_metadata"], scap=profiles,
        )
        return {
            "id": case["id"], "rank": case["rank"], "status": result["status"],
            "error": result["error"], "text_calls": sum(c["kind"] == "text" for c in audit.calls),
            "image_calls": sum(c["kind"] == "image" for c in audit.calls),
        }

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(one, cases):
            summary["rows"].append(result)
            summary["completed"] += 1
            summary["success" if result["status"] == "ok" else "failed"] += 1
            save(ROOT / "pilot-generation-summary.json", summary)
            print(json.dumps(result), flush=True)
    summary["status"] = "complete" if summary["success"] == 10 else "completed_with_errors"
    summary["text_calls"] = sum(row["text_calls"] for row in summary["rows"])
    summary["image_calls"] = sum(row["image_calls"] for row in summary["rows"])
    save(ROOT / "pilot-generation-summary.json", summary)
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("prepare", "generate"))
    args = parser.parse_args()
    {"prepare": prepare, "generate": generate}[args.action]()
