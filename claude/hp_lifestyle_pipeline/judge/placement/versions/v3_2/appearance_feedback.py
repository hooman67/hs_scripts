"""Bind live FE comments to exact native images and ask Astra for visual analysis."""

import argparse
import json
import re
from pathlib import Path

import common
import transport

OUTPUT = common.ROOT / "astra_appearance_revision"
SOURCE = OUTPUT / "source"
STUDY = common.ROOT.parents[3] / "eval_sets/hp_lifestyle_v6_4_pr4523_30_20261110"
BUCKET = "foundry-hp-enterprise-adobe-assets"
BASE = "https://foundry-aws-corp.adobe.io/asset/" + BUCKET + "/"
PREFIX = "eval_sets/hp_lifestyle_v6_4_pr4523_30_20261110/"
USER_STANDARD = {
    "judging_standard": "Visibly awkward or misaligned appearance, even if physically plausible",
    "expected_disposition_for_localized_elitebook_concerns": (
        "Explicit concerns and score penalties, not necessarily fail"
    ),
    "additional_requirement": (
        "ALso, the C-Tech put feedback in this HTML: "
        "https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/"
        "eval_sets/hp_lifestyle_v6_4_pr4523_30_20261110/fe/viewer.html"
        "?src=data_source_prompts_20261110.json&ldap=hshariati&q=W10%3D\n"
        "Make sure judge addresses them (i.e catches them) if relevant."
    ),
}


def load(path):
    return json.loads(path.read_text())


def completed_reviews(text):
    match = re.search(r'"case_reviews"\s*:\s*\[', text)
    if match is None:
        raise ValueError("Truncated response has no case-review array")
    position = match.end()
    decoder = json.JSONDecoder()
    reviews = []
    while position < len(text):
        while position < len(text) and text[position] in " \r\n\t,":
            position += 1
        if position < len(text) and text[position] == "]":
            return reviews, position + 1
        try:
            value, position = decoder.raw_decode(text, position)
        except json.JSONDecodeError as error:
            raise ValueError(
                "A case review is incomplete; footer-only recovery forbidden"
            ) from error
        if not isinstance(value, dict):
            raise TypeError("Expected a complete case-review object")
        reviews.append(value)
    raise ValueError("Case-review array is incomplete")


def replay(receipt):
    if common.sha(receipt["chunks_path"]) != receipt["chunks_sha256"]:
        raise ValueError("Astra source stream changed")
    collector = common.Collector()
    with Path(receipt["chunks_path"]).open() as stream:
        for line in stream:
            collector.feed(json.loads(line))
    return collector


def verified_analysis(batch):
    directory = OUTPUT / f"visual_batch{batch}"
    receipt = load(directory / "receipt.json")
    analysis = load(directory / "analysis.json")
    if receipt.get("completion_recovery") == "size_limited_packets":
        packets = []
        for source in receipt["packet_sources"]:
            path = Path(source["analysis_path"])
            if common.sha(path) != source["analysis_sha256"]:
                raise ValueError("Packet analysis changed")
            packet = load(path)
            if replay(source["receipt"]).result() != packet:
                raise ValueError("Packet analysis differs from actual Astra response")
            packets.append(packet)
        if merge_packets(packets) != analysis:
            raise ValueError("Compiled packet evidence differs from original responses")
    elif receipt.get("completion_recovery") == "footer_only":
        original = replay(receipt["incomplete_case_source"])
        if original.models != {common.MODEL} or original.finish != "length":
            raise ValueError("Unexpected incomplete case source identity/finish")
        reviews, _ = completed_reviews("".join(original.parts))
        footer = replay(receipt["footer_receipt"]).result()
        if {**footer, "case_reviews": reviews} != analysis:
            raise ValueError("Recovered analysis differs from its two actual responses")
    elif replay(receipt).result() != analysis:
        raise ValueError("Case analysis differs from actual Astra response")
    return analysis


def recover_footer(batch):
    output = OUTPUT / f"visual_batch{batch}"
    if (output / "analysis.json").exists():
        raise ValueError("Case batch already completed; do not redraw it")
    attempt = output / "attempt01"
    error = load(attempt / "error.json")
    if error["finish_reason"] != "length" or error["models_seen"] != [common.MODEL]:
        raise ValueError(
            "Only the observed completion-limit failure permits this recovery"
        )
    source_receipt = {
        "chunks_path": str((attempt / "chunks.jsonl").resolve()),
        "chunks_sha256": common.sha(attempt / "chunks.jsonl"),
    }
    collector = replay(source_receipt)
    partial = "".join(collector.parts)
    reviews, end = completed_reviews(partial)
    expected = load(output / "input.json")["cases"]
    if len(reviews) != 10 or {row["case_id"] for row in reviews} != {
        row["id"] for row in expected
    }:
        raise ValueError(
            "Not all ten case reviews were delivered; no image reanalysis is authorized here"
        )
    source_receipt.update(
        model_returned=common.MODEL,
        finish_reason=collector.finish,
        response_id=collector.response_id,
        usage=collector.usage,
        source_error_path=str((attempt / "error.json").resolve()),
    )
    directory = output / "footer_completion"
    directory.mkdir(exist_ok=False)
    inputs = {
        "task": (
            "The previous visual consultation emitted ALL ten complete case-review JSON "
            "objects, then hit its output-token limit while writing policy sections. "
            "Do NOT reanalyze images, change individual findings or repeat case_reviews. "
            "Complete only the transferable prompt-policy synthesis/footer from these "
            "actual already-delivered reviews and the unfinished policy text."
        ),
        "user_standard": USER_STANDARD,
        "already_completed_case_reviews": reviews,
        "unfinished_policy_tail": partial[end:],
        "required_output_keys": [
            "transferable_policy_changes",
            "scope_gaps",
            "remaining_uncertainty",
        ],
        "constraints": "Concise policy synthesis only. Preserve case findings and human/model disagreements; no new visual claims or promotion.",
    }
    common.write_json(directory / "input.json", inputs)
    footer, receipt = transport.model_completion(
        [
            {
                "role": "system",
                "content": "You are Astra, the HP placement prompt-policy specialist. Finish the incomplete policy sections without rejudging any completed images.",
            },
            {"role": "user", "content": json.dumps(inputs)},
        ],
        None,
        16384,
        directory,
    )
    if set(footer) != set(inputs["required_output_keys"]):
        raise ValueError(
            "Footer recovery must not add or replace completed case reviews"
        )
    common.write_json(directory / "footer.json", footer)
    common.write_json(directory / "receipt.json", receipt)
    common.write_json(output / "analysis.json", {**footer, "case_reviews": reviews})
    common.write_json(
        output / "receipt.json",
        {
            "completion_recovery": "footer_only",
            "incomplete_case_source": source_receipt,
            "footer_receipt": receipt,
            "completed_case_reviews_preserved_exactly": True,
            "new_image_judgments": 0,
        },
    )
    verified_analysis(batch)
    print(
        json.dumps(
            {"batch": batch, "footer_recovered": True, "new_image_judgments": 0}
        ),
        flush=True,
    )


def prepare():
    import foundry_aws_gateway

    target = OUTPUT / "corpus.json"
    if target.exists():
        raise ValueError("Feedback corpus already exists; do not overwrite it")
    documents = load(SOURCE / "annotations/snapshot_receipt.json")["objects"]
    rows = load(SOURCE / "data_source_prompts_20261110.json")["rows"]
    native = load(STUDY / "public/data/generation.json")["rows"]
    native_rows = {" / ".join(map(str, row["key"])): row for row in native}
    if len(rows) != 30 or len(native_rows) != 30:
        raise ValueError("Expected exactly the authorized thirty-image source")
    comments = {}
    source_dir = BASE + PREFIX + "fe/"
    for item in documents:
        path = Path(item["path"])
        if common.sha(path) != item["sha256"]:
            raise ValueError("Annotation source changed after snapshot")
        document = load(path)
        if document.get("schema") != "fe-html/annotations@1":
            raise ValueError("Unsupported annotation document")
        report = document["report"]
        if (
            report["dir"] != source_dir
            or report["sources"] != ["data_source_prompts_20261110.json"]
            or report["total_rows"] != 30
        ):
            raise ValueError("Annotation identifies another report or source variant")
        for row in document["rows"]:
            row_id = row["evalset_item_id"]
            if row_id not in native_rows:
                raise ValueError("Annotation identifies an unknown source image")
            comments.setdefault(row_id, []).append(
                {
                    "comment": row["comment"],
                    "answers": row["answers"],
                    "question_comments": row.get("question_comments"),
                    "complete": row["complete"],
                    "source_row_idx": row["row_idx"],
                    "source_key": row["key"],
                    "source_document_path": str(path),
                    "source_document_sha256": item["sha256"],
                    "reviewer_ldap": document["ldap"],
                    "submitted_at": document["submitted_at"],
                }
            )
    client = foundry_aws_gateway.maybe_s3_client(BUCKET)
    if client is None:
        raise RuntimeError("No authenticated Foundry S3 client")

    def image(url, digest):
        if not url.startswith(BASE + PREFIX):
            raise ValueError("Unexpected feedback image origin")
        destination = SOURCE / "images" / (digest + ".png")
        if not destination.exists():
            response = client.get_object(Bucket=BUCKET, Key=url[len(BASE) :])
            with response["Body"] as body:
                pixels = body.read()
            if common.hashlib.sha256(pixels).hexdigest() != digest:
                raise ValueError("Live annotated image differs from native source")
            destination.parent.mkdir(exist_ok=True)
            destination.write_bytes(pixels)
        if common.sha(destination) != digest:
            raise ValueError("Preserved annotated image changed")
        return {"url": url, "local_path": str(destination.resolve()), "sha256": digest}

    records = []
    for row in rows:
        row_id = row["meta_data"]["evalset_item_id"]
        source = native_rows[row_id]
        photo = [asset for asset in row["images"] if asset["asset_type"] == "image"]
        prompts = [asset for asset in row["images"] if asset["asset_type"] == "text"]
        if len(photo) != 1 or len(prompts) != 1:
            raise ValueError("Expected one source image and one actual source prompt")
        output = source["output"]
        expected_url = BASE + PREFIX + output["image"].removeprefix("../")
        if photo[0]["image_src"] != expected_url:
            raise ValueError("FE and native generation bind different output images")
        if prompts[0]["text_content"] != source["prompt"]["text"]:
            raise ValueError("FE and native generation bind different source prompts")
        slug = expected_url.rsplit("/", 1)[1].removesuffix(".png")
        audit_path = STUDY / "input_audit" / (slug + ".json")
        audit = load(audit_path)
        reference = output["inputs"]["product"]
        if Path(reference).name != Path(audit["product"]["path"]).name:
            raise ValueError("Native product reference lost its audit binding")
        records.append(
            {
                "id": "v64_ctech__" + slug,
                "source_row_id": row_id,
                "source_row_idx": row["meta_data"]["row_idx"],
                "variant": "V6.4 / PR4523 / C-Tech feedback",
                "product_type": "laptop"
                if source["key"][0] in ("cashmere", "elitebook")
                else "printer",
                "scene_prompt": prompts[0]["text_content"],
                "generated_image": image(expected_url, output["image_sha256"]),
                "twin_image": image(
                    BASE + PREFIX + reference.removeprefix("../"),
                    audit["product"]["sha256"],
                ),
                "human_feedback": comments.get(row_id, []),
                "native_input_audit_path": str(audit_path),
                "native_input_audit_sha256": common.sha(audit_path),
                "source_stage": (
                    "Scene-generation image, SHA-matched to the native image-edit output; "
                    "original generation audit reports one image edit per case and no relighting."
                ),
            }
        )
    if len({row["id"] for row in records}) != 30:
        raise ValueError("Duplicate feedback image identities")
    common.write_json(
        target,
        {
            "user_standard": USER_STANDARD,
            "records": records,
            "source_objects": load(SOURCE / "objects.json"),
            "annotation_documents": documents,
            "native_generation_audit_path": str(STUDY / "generation_audit.json"),
            "native_generation_audit_sha256": common.sha(
                STUDY / "generation_audit.json"
            ),
            "feedback_is_comprehensive_gold": False,
            "feedback_scope": (
                "Free-text whole-image C-Tech comments, not structured placement labels. "
                "Preserve FAIL/OK wording but do not convert it to placement ground truth. "
                "Blank/OK comments are not exhaustive negative labels. Astra determines "
                "visual relevance and separates lighting, branding and stylistic scope."
            ),
        },
    )
    print(json.dumps({"prepared": True, "images": 30, "annotated_rows": len(comments)}))


def image_packets(records, limit=30_000_000):
    packets, current, seen, size = [], [], set(), 0
    for row in records:
        images = {
            row[role]["sha256"]: row[role] for role in ("generated_image", "twin_image")
        }
        additional = sum(
            4 * ((Path(image["local_path"]).stat().st_size + 2) // 3)
            for digest, image in images.items()
            if digest not in seen
        )
        if current and size + additional > limit:
            packets.append(current)
            current, seen, size = [], set(), 0
            additional = sum(
                4 * ((Path(image["local_path"]).stat().st_size + 2) // 3)
                for image in images.values()
            )
        if additional > limit:
            raise ValueError(
                "One exact scene/reference exceeds the safe image payload limit"
            )
        current.append(row)
        seen.update(images)
        size += additional
    if current:
        packets.append(current)
    return packets


def merge_packets(packets):
    reviews = [case for packet in packets for case in packet["case_reviews"]]
    if len({row["case_id"] for row in reviews}) != len(reviews):
        raise ValueError("A feedback image was analyzed in multiple packets")
    return {
        "case_reviews": reviews,
        **{
            key: [
                {"packet": index, "value": packet[key]}
                for index, packet in enumerate(packets, 1)
            ]
            for key in (
                "transferable_policy_changes",
                "scope_gaps",
                "remaining_uncertainty",
            )
        },
    }


def packet_consult(batch):
    corpus = load(OUTPUT / "corpus.json")
    records = corpus["records"][(batch - 1) * 10 : batch * 10]
    output = OUTPUT / f"visual_batch{batch}"
    if (output / "analysis.json").exists():
        raise ValueError("Completed batch must not be analyzed again")
    error_path = output / "attempt01/error.json"
    if output.exists():
        if not error_path.exists():
            raise ValueError("Existing incomplete batch requires explicit diagnosis")
        error = load(error_path)
        if error["status_code"] != 400 or error["chunks"] != 0 or error["models_seen"]:
            raise ValueError("Do not packetize a batch with delivered model judgments")
    output.mkdir(exist_ok=True)
    groups = image_packets(records)
    common.write_json(
        output / "packet_manifest.json",
        {
            "groups": [[row["id"] for row in group] for group in groups],
            "max_base64_image_bytes": 30_000_000,
            "image_transform": "None; exact original PNG bytes with SHA deduplication within each packet.",
            "prior_request_rejection": str(error_path) if error_path.exists() else None,
        },
    )
    sources, packets = [], []
    for index, group in enumerate(groups, 1):
        directory = output / f"packet{index:02d}"
        if not (directory / "analysis.json").exists():
            consult(batch, packet=index, records_override=group)
        analysis = load(directory / "analysis.json")
        receipt = load(directory / "receipt.json")
        if replay(receipt).result() != analysis:
            raise ValueError("Packet analysis failed actual-stream validation")
        packets.append(analysis)
        sources.append(
            {
                "analysis_path": str((directory / "analysis.json").resolve()),
                "analysis_sha256": common.sha(directory / "analysis.json"),
                "receipt": receipt,
            }
        )
    merged = merge_packets(packets)
    if {row["case_id"] for row in merged["case_reviews"]} != {
        row["id"] for row in records
    }:
        raise ValueError("Packet compilation omitted or changed feedback images")
    common.write_json(output / "analysis.json", merged)
    common.write_json(
        output / "receipt.json",
        {"completion_recovery": "size_limited_packets", "packet_sources": sources},
    )
    verified_analysis(batch)
    print(
        json.dumps(
            {
                "batch": batch,
                "complete": True,
                "cases": len(records),
                "packets": len(groups),
            }
        ),
        flush=True,
    )


def consult(batch, *, packet=None, records_override=None):
    corpus = load(OUTPUT / "corpus.json")
    records = (
        records_override
        if records_override is not None
        else corpus["records"][(batch - 1) * 10 : batch * 10]
    )
    if records_override is None and len(records) != 10:
        raise ValueError("Expected ten exact cases in each of three visual batches")
    output = OUTPUT / f"visual_batch{batch}"
    if packet is not None:
        output /= f"packet{packet:02d}"
    if (output / "analysis.json").exists():
        raise ValueError("Completed visual batch must not be redrawn")
    inputs = {
        "task": (
            f"Analyze the actual {len(records)} source images/reference products and the actual "
            "C-Tech feedback. Identify each placement-relevant concern that a judge "
            "should explicitly catch under the user's newly confirmed appearance-sensitive "
            "standard. You do sensitive image analysis and transferable prompt-policy "
            "design only; the engineer handles code, retrieval, binding and evaluation."
        ),
        "user_confirmed_standard": corpus["user_standard"],
        "important_change": (
            "Previously a physically plausible explanation was often treated as clearance. "
            "The user explicitly wants visibly awkward/misaligned appearance penalized even "
            "if physically plausible, with explicit concerns/score reductions rather than "
            "necessarily FAIL for subtle issues. This is an authorized rubric change, not "
            "a claim that earlier calls detected them or proved a physical impossibility. "
            "Keep severity0 for genuinely coherent visible appearance, severity1 for minor "
            "visible awkwardness, and materially worse defects at appropriate higher bands. "
            "Do not inflate confidence or invent hidden supports/defects. Missing supports "
            "need a visible appearance cue, not merely a crop or occlusion."
        ),
        "cases": [
            {
                key: row[key]
                for key in (
                    "id",
                    "source_row_id",
                    "scene_prompt",
                    "product_type",
                    "generated_image",
                    "twin_image",
                )
            }
            | {
                "ctech_feedback": [
                    {
                        key: item[key]
                        for key in ("comment", "answers", "question_comments")
                    }
                    for item in row["human_feedback"]
                ]
            }
            for row in records
        ],
        "fixed_final_schema": common.OBSERVATION_SCHEMA,
        "constraints": (
            "Use exact pixels and keep human comments distinct from your interpretation. "
            "Whole-image FAIL may be solely lighting/branding/editorial styling, so it "
            "is not automatically placement FAIL. Map relevant concerns to the existing "
            "five components/allowed codes only; identify unsupported scope explicitly, "
            "never silently ignore it or invent a new code. Consider support/furniture "
            "appearance, product/support alignment, usable access and credible arrangement; "
            "chair offset alone is not a defect. A real seat/support omission, warped "
            "table, collision, impossible circulation or incoherent staging is different "
            "from ordinary offset. Do not add scene IDs, coordinates or desired labels to "
            "runtime prompts. These are design/development examples, not held-out accuracy. "
            "You have not seen new candidate predictions; do not claim promotion."
        ),
        "required_json_output": {
            "case_reviews": (
                f"Exactly {len(records)} records, identified by case_id. For EACH C-Tech concern "
                "give original wording, placement relevance, actual visible evidence/"
                "counter-evidence, supported/uncertain/disputed/out-of-scope status, "
                "appropriate component/code and qualitative severity/confidence if "
                "representable. Distinguish a minor appearance concern from a material "
                "physical claim. Do not turn your interpretations into human gold labels."
            ),
            "transferable_policy_changes": "Concise rules to catch supported concerns without false positives.",
            "scope_gaps": "Relevant but unrepresentable issues, and excluded lighting/branding/styling concerns.",
            "remaining_uncertainty": "Explicit evidence limitations and disputed C-Tech assertions.",
        },
    }
    output.mkdir(exist_ok=True)
    common.write_json(output / "input.json", inputs)
    parts = [{"type": "text", "text": json.dumps(inputs)}]
    seen = set()
    for row in records:
        for role in ("generated_image", "twin_image"):
            entry = row[role]
            if common.sha(entry["local_path"]) != entry["sha256"]:
                raise ValueError("Feedback image bytes changed")
            if entry["sha256"] not in seen:
                parts += common.LEGACY.image_parts(
                    row["id"] + " / " + role, entry["local_path"]
                )
                seen.add(entry["sha256"])
            else:
                parts.append(
                    {
                        "type": "text",
                        "text": row["id"]
                        + " / "
                        + role
                        + " reuses image SHA256 "
                        + entry["sha256"],
                    }
                )
    result, receipt = transport.model_completion(
        [
            {
                "role": "system",
                "content": (
                    "You are Astra, the HP placement visual-analysis and prompt-policy "
                    "specialist. Apply the user's appearance-sensitive review standard, "
                    "not a proof-of-impossibility standard. Preserve honest uncertainty "
                    "and the boundary between whole-image review and placement."
                ),
            },
            {"role": "user", "content": parts},
        ],
        None,
        32768,
        output,
    )
    ids = [row["case_id"] for row in result["case_reviews"]]
    if len(ids) != len(records) or set(ids) != {row["id"] for row in records}:
        raise ValueError("Astra omitted or rebound feedback images")
    common.write_json(output / "analysis.json", result)
    common.write_json(output / "receipt.json", receipt)
    print(
        json.dumps(
            {"batch": batch, "packet": packet, "complete": True, "cases": len(ids)}
        ),
        flush=True,
    )


def synthesize():
    from feedback_followup import FEEDBACK, ROLES

    output = OUTPUT / "synthesis"
    if (output / "proposal.json").exists():
        raise ValueError("Completed prompt synthesis must not be redrawn")
    analyses = []
    for batch in (1, 2, 3):
        analyses.append(verified_analysis(batch))
    cases = load(common.R1 / "r2/calibration_manifest.json")["cases"]
    predecessor = common.ROOT.parent / "v3_2_r2"
    inputs = {
        "task": (
            "Author seven complete runnable successor system prompts implementing the "
            "user-confirmed APPEARANCE-sensitive placement rubric and the relevant "
            "C-Tech feedback mechanisms from all thirty actual-image analyses. You do "
            "sensitive visual reasoning and system-prompt design only; the engineer "
            "implements/freezes/tests/runs/publishes the isolated successor."
        ),
        "user_confirmed_standard": USER_STANDARD,
        "user_localized_elitebook_feedback": FEEDBACK,
        "prior_localized_analysis": load(
            common.ROOT / "astra_localized_feedback/proposal.json"
        ),
        "actual_ctech_case_analyses": analyses,
        "historical_cases": cases,
        "prospective_calibration_change": (
            "Original versions/checks/results remain frozen and unpromoted. For a NEW "
            "appearance-review version, the user explicitly requests concern detection "
            "and score penalties for the EliteBook front-edge difference and upper "
            "chair-backrest feature, NOT necessarily FAIL or proof of physical rotation/"
            "extra-member construction. Represent minor visible awkwardness at severity1 "
            "with accurate appearance evidence, not invented physical certainty. Genuine "
            "Cashmere material misalignment must still fail; harmless chair offset alone "
            "must remain unpenalized. The other three controls remain non-gold stability "
            "checks. Clearly distinguish a changed user standard from retrospective "
            "improved detection under the original physical/material-failure gate."
        ),
        "current_system_prompts": {
            role: (predecessor / "prompts" / (role + ".txt")).read_text()
            for role in ROLES
        },
        "current_calibration_predictions": load(
            predecessor / "evaluation/calibration/summary.json"
        ),
        "fixed_final_schema": common.OBSERVATION_SCHEMA,
        "fixed_verifier_schema_example": common.LEGACY.component_schema(
            list(common.SCORING.COMPONENT_WEIGHTS)
        ),
        "architecture_and_constraints": (
            "Keep five existing components/issue codes, deterministic weights and scoring "
            "unchanged. P1 = complementary full-observation primaries, with component-only "
            "proposal/independent verifiers restricted to exactly requested components. "
            "P2 = mutually blind always-on geometry/use specialists and final image "
            "reconciler. The engineer raises the new reconciler budget from6000 to12000 "
            "to address a real preserved completion-length failure and hardens streaming "
            "recovery; this is separate from prompt sensitivity. Runtime target IDs/"
            "labels/comments are withheld. No image IDs, coordinates, memorized target "
            "features, confidence inflation or retired chair_alignment_conflict code "
            "in prompts. Write concise transferable visual policies, not a giant checklist "
            "or exhaustive reasoning trace. Explain represented placement/scene-arrangement "
            "concerns and explicitly excluded global lighting, brand visibility, wall-art "
            "taste and depth preferences where not relevant to existing components. "
            "Do not silently promise a placement judge catches every whole-image FAIL. "
            "Do not demand geometric impossibility for an appearance penalty; equally, "
            "ordinary offset/occlusion/unfamiliar furniture cannot automatically fail. "
            "All thirty comments informed this design and are not held-out gold."
        ),
        "required_json_output": {
            "change_hypothesis": "Transferable mechanisms and why the new appearance policy differs from previous clearance.",
            "historical_case_analysis": "Six actual cases, including minor appearance concerns versus physical certainty and controls.",
            "revised_prompts": {
                role: "Complete runnable system-prompt string" for role in ROLES
            },
            "ctech_coverage_policy": "Which relevant concern families are represented, which remain outside scope and why.",
            "remaining_limitations": "Uncertainty, possible regressions, original-gate non-promotion and development-only evidence.",
        },
    }
    output.mkdir(exist_ok=True)
    common.write_json(output / "input.json", inputs)
    parts = [{"type": "text", "text": json.dumps(inputs)}]
    for case in cases:
        for role in ("generated_image", "twin_image"):
            entry = case[role]
            if common.sha(entry["local_path"]) != entry["sha256"]:
                raise ValueError("Historical image changed before appearance synthesis")
            parts += common.LEGACY.image_parts(
                case["id"] + " / " + role, entry["local_path"]
            )
    proposal, receipt = transport.model_completion(
        [
            {
                "role": "system",
                "content": (
                    "You are Astra, the HP placement visual-analysis and system-prompt "
                    "specialist. Implement the user's explicit appearance-review standard "
                    "with honest uncertainty, not a proof-of-impossibility threshold or "
                    "a forced material fail. Produce complete runnable prompts."
                ),
            },
            {"role": "user", "content": parts},
        ],
        None,
        32768,
        output,
    )
    prompts = proposal["revised_prompts"]
    if (
        not isinstance(prompts, dict)
        or set(prompts) != set(ROLES)
        or any(
            not isinstance(text, str) or len(text.strip()) < 400
            for text in prompts.values()
        )
    ):
        raise ValueError("Missing seven complete appearance-review prompts")
    common.write_json(output / "proposal.json", proposal)
    common.write_json(output / "receipt.json", receipt)
    print(
        json.dumps({"synthesis_complete": True, "system_prompts": len(prompts)}),
        flush=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=(
            "prepare",
            "consult",
            "synthesize",
            "recover-footer",
            "packet-consult",
        ),
    )
    parser.add_argument("--batch", type=int, choices=(1, 2, 3))
    args = parser.parse_args()
    if args.command == "prepare":
        prepare()
    elif args.command == "synthesize":
        synthesize()
    elif args.command == "recover-footer":
        if args.batch is None:
            raise ValueError("Select the exact incomplete batch")
        recover_footer(args.batch)
    elif args.command == "packet-consult":
        if args.batch is None:
            raise ValueError("Select one exact feedback batch")
        packet_consult(args.batch)
    else:
        for batch in (args.batch,) if args.batch else (1, 2, 3):
            if (OUTPUT / f"visual_batch{batch}/analysis.json").exists():
                raise ValueError("Use an explicit unfinished-batch command to resume")
            consult(batch)
        if not args.batch:
            synthesize()


if __name__ == "__main__":
    main()
