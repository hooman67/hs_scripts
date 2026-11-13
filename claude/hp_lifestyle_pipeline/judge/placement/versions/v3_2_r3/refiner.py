"""Recover exact scene context and evaluate the complete source/refinement corpus."""

import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import common
import evaluate

ROOT = common.ROOT / "evaluation/refiner"
SOURCE = common.R1 / "astra_refiner_followup_20261110"
BUCKET = "foundry-hp-enterprise-adobe-assets"


def s3_client():
    return common.load("v32_source_prepare", SOURCE / "prepare.py").client()


def source_identity(client, url):
    parsed = urlparse(url)
    prefix = "/asset/" + BUCKET + "/"
    if (
        parsed.scheme != "https"
        or parsed.netloc != "foundry-aws-corp.adobe.io"
        or not parsed.path.startswith(prefix)
    ):
        raise ValueError("Unexpected source asset origin")
    key = parsed.path[len(prefix) :]
    response = client.get_object(Bucket=BUCKET, Key=key)
    try:
        body = response["Body"].read()
    finally:
        response["Body"].close()
    return {
        "url": url,
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "etag": response["ETag"],
        "version_id": response.get("VersionId"),
    }


def prepare():
    target = ROOT / "corpus.json"
    if target.exists():
        raise ValueError("Corpus already frozen; do not overwrite")
    metadata = json.loads((ROOT / "source/data.json").read_text())
    source_object = json.loads((ROOT / "source/object.json").read_text())
    if common.sha(ROOT / "source/data.json") != source_object["sha256"]:
        raise ValueError("Recovered original context changed")
    evidence_path = SOURCE / "evidence_manifest.json"
    evidence = json.loads(evidence_path.read_text())
    rows = {row["meta_data"]["evalset_item_id"]: row for row in metadata["rows"]}
    client = s3_client()
    identities = {}

    def identity(url):
        if url not in identities:
            identities[url] = source_identity(client, url)
        return identities[url]

    records, bindings, stage_checks = [], [], []
    for case in evidence["cases"]:
        row_id, run = case["id"].rsplit("__", 1)
        row = rows[row_id]
        context = row["meta_data"]["key_val_informations"]
        prompt = context["V6.1 user prompt"]
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Missing original scene prompt")
        product = next(
            item
            for item in row["images"]
            if item["meta_text"]["Label"] == "Product input"
        )
        product_identity = identity(product["image_src"])
        if product_identity["sha256"] != case["images"]["product"]["sha256"]:
            raise ValueError("Original product and refiner reference differ")
        selected = [
            item
            for item in row["images"]
            if item.get("meta_text", {}).get("Run")
            == ("1st run" if run == "run1" else "2nd run")
        ]
        matched = []
        for item in selected:
            source = identity(item["image_src"])
            if source["sha256"] == case["images"]["baseline"]["sha256"]:
                matched.append({**source, "label": item["meta_text"]["Label"]})
        if len(matched) != 1:
            raise ValueError(
                "Baseline scene/relighting lineage is missing or ambiguous"
            )
        stage = (
            "scene_generation"
            if "Image generation" in matched[0]["label"]
            else "relighting"
        )
        stage_checks.append(
            {
                "id": case["id"],
                "source_stage": stage,
                "original_product": product_identity,
                "baseline_source": matched[0],
            }
        )
        for role in ("baseline", "refined"):
            image = case["images"][role]
            baseline_id = case["id"] + "--baseline"
            scene_id = (
                baseline_id
                if role == "baseline"
                or image["sha256"] == case["images"]["baseline"]["sha256"]
                else case["id"] + "--refined"
            )
            bindings.append(
                {
                    "case_id": case["id"],
                    "role": role,
                    "scene_id": scene_id,
                    "sha256": image["sha256"],
                    "url": image["url"],
                }
            )
            if role == "refined" and scene_id == baseline_id:
                continue
            records.append(
                {
                    "id": scene_id,
                    "source_row_id": row_id,
                    "variant": role,
                    "source_case_id": case["id"],
                    "source_image_stage": stage
                    if role == "baseline"
                    else "refiner_edit_of_" + stage,
                    "product_type": "printer"
                    if context["Device"] in ("tassel", "adf_printer")
                    else "laptop",
                    "scene_prompt": prompt,
                    "scene_prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                    "generated_image": {**image, "local_path": image["path"]},
                    "twin_image": {
                        **case["images"]["product"],
                        "local_path": case["images"]["product"]["path"],
                    },
                }
            )
    if len(records) != 81 or len(bindings) != 128:
        raise ValueError("Expected64 baselines,17 edited scenes and128 report bindings")
    common.write_json(
        target,
        {
            "source_evidence_path": str(evidence_path),
            "source_evidence_sha256": common.sha(evidence_path),
            "original_context": source_object,
            "records": records,
            "bindings": bindings,
            "source_stage_checks": stage_checks,
            "all64_used_by_astra_designer": True,
            "interpretation": "Development comparison, not unseen holdout. Human feedback applies to baselines only; 47 exact passthroughs reuse one judgment, not extra samples.",
        },
    )
    print(
        json.dumps(
            {
                "unique_scenes": len(records),
                "bindings": len(bindings),
                "baseline_stages": sorted(
                    {row["source_stage"] for row in stage_checks}
                ),
                "corpus_sha256": common.sha(target),
            }
        )
    )


def run(workers):
    corpus = json.loads((ROOT / "corpus.json").read_text())
    rows = []
    summary = {
        "corpus_sha256": common.sha(ROOT / "corpus.json"),
        "protocol_freeze_sha256": common.verify_freeze(),
        "actual_judge_model": common.MODEL,
        "expected": len(corpus["records"]) * 2,
        "records": rows,
        "source_stage_checks": corpus["source_stage_checks"],
        "target_labels_withheld": True,
        "development_only": True,
    }
    common.write_json(ROOT / "summary.json", summary)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(evaluate.assess, case, candidate, ROOT)
            for case in corpus["records"]
            for candidate in ("p1", "p2")
        ]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            rows.sort(key=lambda item: (item["id"], item["candidate"]))
            common.write_json(ROOT / "summary.json", summary)
            print(
                json.dumps(
                    {
                        key: row.get(key)
                        for key in (
                            "id",
                            "candidate",
                            "status",
                            "verdict",
                            "score",
                            "error_type",
                        )
                    }
                ),
                flush=True,
            )
    summary["complete"] = all(row["status"] == "complete" for row in rows)
    common.write_json(ROOT / "summary.json", summary)
    if not summary["complete"]:
        raise SystemExit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "evaluate"))
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        raise ValueError("Use1-8 bounded workers")
    if args.command == "prepare":
        prepare()
    else:
        run(args.workers)


if __name__ == "__main__":
    main()
