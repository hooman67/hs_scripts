"""Collect exact source evidence and native-size review copies; no model calls."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
R1 = ROOT.parent
PROJECT = R1.parents[3]
SOURCE = ROOT / "source"
REPORT = PROJECT / "eval_sets/hp_lifestyle_v6_2_v6_3_pr4523_pr4417_20261109/report.py"
BUCKET = "foundry-hp-enterprise-adobe-assets"
PREFIX = "refiner_evals/hp_judge_refiner/hpjr-all-fixable-20261109T225123Z/"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


class Text(HTMLParser):
    def __init__(self, value):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.feed(value)

    def handle_data(self, value):
        self.parts.append(value)


def plain(value):
    return "".join(Text(value).parts).strip()


def parse_cases(source):
    blocks = re.findall(r'<div class="case">(.*?)(?=<div class="case">|</body>)', source, re.S)
    cases = []
    for block in blocks:
        heading = re.search(r'<h3>(.*?) <span class="status">\((.*?)\)</span>', block, re.S)
        feedback = re.search(r'<p class="feedback"><b>Reviewer feedback:</b>(.*?)</p>', block, re.S)
        if heading is None or feedback is None:
            raise ValueError("unrecognized report case structure")
        case_id, status = heading.groups()
        if not re.fullmatch(r"\d\d_[A-Za-z0-9_]+__run[12]", case_id):
            raise ValueError("unsafe or unexpected source case ID")
        images = re.findall(r'<img src="([^"]+)"', block)
        if images != [case_id + "/" + name + ".png" for name in ("product", "baseline", "refined")]:
            raise ValueError("image order or case binding changed")
        full_feedback = plain(feedback.group(1))
        comment, separator, scope = full_feedback.partition("\n\nScope decision:")
        if not separator:
            raise ValueError("human feedback and generated scope decision cannot be separated")
        cases.append({
            "id": case_id, "status": status, "reviewer_feedback": comment.strip(),
            "refiner_scope_text": scope.strip(), "media": images,
        })
    if len(cases) != 64 or len({case["id"] for case in cases}) != 64:
        raise ValueError("expected exactly64 unique report cases")
    return cases


def client():
    spec = importlib.util.spec_from_file_location("hp_report", REPORT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.s3_client(Path("/mnt/localssd/temp_creds.txt"))


def prepare():
    from PIL import Image

    cases = parse_cases((SOURCE / "full_evalset.html").read_text())
    screening = {row["case_id"]: row for row in json.loads((SOURCE / "screening.json").read_text())}
    root_run = json.loads((SOURCE / "run.json").read_text())
    if [case["id"] for case in cases] != root_run["cases"] or set(screening) != set(root_run["cases"]):
        raise ValueError("HTML, run and feedback inventories disagree")
    for case in cases:
        feedback = screening[case["id"]]["original_feedback"]
        if (feedback or "(No reviewer comment.)") != case["reviewer_feedback"]:
            raise ValueError("HTML feedback differs from preserved original comment")
        case["screening"] = screening[case["id"]]
    inventory = {item["key"]: item for item in json.loads((SOURCE / "object_inventory.json").read_text())}
    tasks = []
    for case in cases:
        for name in ("product.png", "baseline.png", "refined.png", "judge.json", "result.json"):
            relative = case["id"] + "/" + name
            directory = "images" if name.endswith(".png") else "records"
            tasks.append((relative, SOURCE / directory / relative))
    for index in range(1, 7):
        name = f"review-{index}.jpg"
        tasks.append((name, SOURCE / "images" / name))
    s3 = client()

    def download(task):
        relative, path = task
        key = PREFIX + relative
        expected = inventory[key]
        response = s3.get_object(Bucket=BUCKET, Key=key)
        try:
            body = response["Body"].read()
        finally:
            response["Body"].close()
        if response["ETag"] != expected["etag"] or len(body) != expected["bytes"]:
            raise ValueError("live object changed since inventory: " + relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_bytes() != body:
            raise ValueError("existing durable evidence differs: " + relative)
        path.write_bytes(body)
        return {
            "relative": relative, "path": str(path), "sha256": sha(path), "bytes": len(body),
            "url": "https://foundry-aws-corp.adobe.io/asset/" + BUCKET + "/" + key,
            "etag": response["ETag"], "version_id": response.get("VersionId"),
        }

    with ThreadPoolExecutor(max_workers=8) as pool:
        objects = list(pool.map(download, tasks))
    by_name = {item["relative"]: item for item in objects}
    review_images = {}
    for case in cases:
        case["images"] = {}
        for kind in ("product", "baseline", "refined"):
            item = by_name[case["id"] + "/" + kind + ".png"]
            original = Path(item["path"])
            with Image.open(original) as image:
                dimensions = list(image.size)
                rgb = image.convert("RGB")
                if "A" in image.getbands():
                    rgb = Image.new("RGB", image.size, "white")
                    rgb.paste(image, mask=image.getchannel("A"))
                derived = ROOT / "review_images" / (item["sha256"] + ".jpg")
                if not derived.exists():
                    derived.parent.mkdir(parents=True, exist_ok=True)
                    rgb.save(derived, quality=94, subsampling=0)
            media = {
                **item, "dimensions": dimensions, "review_path": str(derived),
                "review_sha256": sha(derived), "review_bytes": derived.stat().st_size,
                "transformation": "Native-size JPEG quality94, subsampling0; transparent product pixels "
                                  "composited on white; no crop/resize/annotations; original PNG preserved.",
            }
            case["images"][kind] = media
            review_images[media["review_sha256"]] = media
        result = json.loads((SOURCE / "records" / case["id"] / "result.json").read_text())
        if result["case_id"] != case["id"] or result["status"] != case["status"]:
            raise ValueError("result status/case differs from HTML")
        if case["status"] == "passthrough" and (
                case["images"]["baseline"]["sha256"] != case["images"]["refined"]["sha256"]):
            raise ValueError("passthrough is not byte-identical")
        case["result"] = result
    expected_source = json.loads((SOURCE / "object.json").read_text())
    current = s3.get_object(Bucket=BUCKET, Key=PREFIX + "full_evalset.html")
    try:
        html_body = current["Body"].read()
    finally:
        current["Body"].close()
    if hashlib.sha256(html_body).hexdigest() != expected_source["sha256"]:
        raise ValueError("live HTML changed during collection")
    anchor_manifest = json.loads((R1 / "r2/calibration_manifest.json").read_text())
    for case in anchor_manifest["cases"]:
        for name in ("generated_image", "twin_image"):
            if sha(case[name]["local_path"]) != case[name]["sha256"]:
                raise ValueError("frozen annotated example/control image changed")
    manifest = {
        "prepared_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": expected_source, "cases": cases, "downloaded_objects": objects,
        "counts": {"cases": len(cases), "source_image_references": 192,
                   "unique_source_pngs": len({case["images"][kind]["sha256"] for case in cases
                                             for kind in ("product", "baseline", "refined")}),
                   "review_jpeg_bytes": sum(item["review_bytes"] for item in review_images.values())},
        "feedback_boundary": "Original comments are development evidence, not comprehensive gold. "
                             "Buttons/ratings, refiner eligibility, empty issues and passthrough are "
                             "not placement passes. Comments target baseline, not proof of refined success.",
        "historical_annotated_examples_and_controls": anchor_manifest["cases"],
        "review_notes": json.loads((SOURCE / "visual_review.json").read_text()),
    }
    write_json(ROOT / "evidence_manifest.json", manifest)
    print(json.dumps(manifest["counts"]))


if __name__ == "__main__":
    prepare()
