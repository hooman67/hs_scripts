"""Run the bounded nine-case corrected-input composition experiment."""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
import time

from foundry_aws_gateway import llm
from PIL import Image


PROJECT = Path("/home/colligo/hs_scripts/claude/mixology")
TOPIC = PROJECT / "research/group-composition-corrected-inputs"
DATA = Path("/home/colligo/mixology_data/refraction_research_2026-10-19")
SOURCE = DATA / "assets/ref_input_originals"
OLD_RUNS = DATA / "composition/runs"
RUNS = DATA / "composition-corrected-inputs/runs"
CLI = Path("/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py")
CASES = TOPIC / "cases.json"
JOURNAL = TOPIC / "generation_journal.json"
JUDGE = TOPIC / "prompts/judge.md"
CEILING = 9

INPUTS = {
    "cola": ("TCCC – Crafted Sept 2026-1.png", "dark cola with red syrup"),
    "clear": ("TCCC – Crafted Sept 2026-2.png", "clear drink with red upper layer"),
    "red": ("TCCC – Crafted Sept 2026-3.png", "red iced drink"),
    "orange": ("TCCC – Crafted Sept 2026-4.png", "orange iced drink with red syrup"),
    "amber": ("TCCC – Crafted Sept 2026-5.png", "amber iced drink"),
}
EXPECTED = {
    "cola": "73a0ad77a7494b07d276ccb2c39c562e442e7a9975870b7d972221d16ff6fd9f",
    "clear": "acca9199a122fa019bc1aa50893b38ef29b2b1b026dec0da054a4f121a084b60",
    "red": "c4220cfc21ea441712eb92c7acd6512e320ae86ea93b9403a3eeda41ed3ed0ee",
    "orange": "b8db3d8278c2edc5cc4d64085e53c9fdeb02226a91ab47078f4126a9eb6bbbb1",
    "amber": "faf0cb3902c18e770876027d76eead7de6bef470d97eca7d383e16049b4f7670",
}


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if exclusive:
        with path.open("x") as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        return
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    temporary.replace(path)


def image_record(identity: str, index: int) -> dict:
    filename, description = INPUTS[identity]
    path = SOURCE / filename
    assert digest(path) == EXPECTED[identity], path
    with Image.open(path) as image:
        dimensions = list(image.size)
        mode = image.mode
    return {
        "identity": identity,
        "image_index": index,
        "role": f"Image {index}: authoritative compositing input for one finished drink, {description}",
        "path": str(path),
        "filename": filename,
        "sha256": digest(path),
        "bytes": path.stat().st_size,
        "dimensions": dimensions,
        "mode": mode,
    }


def image_content(path: Path) -> dict:
    encoded = base64.b64encode(path.read_bytes()).decode()
    return {"type": "input_image", "image_url": f"data:image/png;base64,{encoded}"}


def response_meta(response) -> dict:
    return {
        "response_id": response.id,
        "request_id": response._request_id,
        "returned_model": response.model,
        "status": response.status,
        "created_at": getattr(response, "created_at", None),
        "completed_at": getattr(response, "completed_at", None),
        "usage": response.usage.model_dump(mode="json") if response.usage else None,
    }


def direct_client():
    return llm.get_openai().with_options(timeout=300, max_retries=0)


def increment_journal(run_id: str, record_path: Path) -> int:
    journal = json.loads(JOURNAL.read_text())
    if any(item["run_id"] == run_id for item in journal["entries"]):
        raise RuntimeError(f"Generation already counted: {run_id}")
    count = int(journal["generation_calls_started"])
    if count >= CEILING:
        raise RuntimeError(f"Generation ceiling reached: {count}/{CEILING}")
    number = count + 1
    journal["generation_calls_started"] = number
    journal["entries"].append({
        "run_id": run_id,
        "generation_number": number,
        "status": "image_post_starting",
        "counted_at": utc(),
        "record": str(record_path),
    })
    write_json(JOURNAL, journal)
    return number


def update_journal(run_id: str, status: str, **fields) -> None:
    journal = json.loads(JOURNAL.read_text())
    matches = [item for item in journal["entries"] if item["run_id"] == run_id]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one journal entry for {run_id}")
    matches[0].update(status=status, updated_at=utc(), **fields)
    journal["generation_outputs_completed"] = sum(
        item["status"] == "complete" for item in journal["entries"]
    )
    write_json(JOURNAL, journal)


def generate(run_id: str) -> None:
    plan = json.loads(CASES.read_text())
    if run_id not in plan:
        raise KeyError(run_id)
    spec = plan[run_id]
    folder = RUNS / run_id
    record_path = folder / "record.json"
    output_path = folder / "output.png"
    if record_path.exists():
        old = json.loads(record_path.read_text())
        if old.get("status") == "complete" and output_path.exists():
            print(f"SKIP complete {run_id}")
            return
        raise RuntimeError(f"Existing incomplete or uncertain attempt requires review: {folder}")
    if output_path.exists():
        raise RuntimeError(f"Unrecorded output exists: {output_path}")

    old_folder = OLD_RUNS / spec["original_id"]
    original = json.loads((old_folder / "record.json").read_text())
    if original["status"] != "complete":
        raise RuntimeError(f"Original counterpart is not complete: {spec['original_id']}")
    if original["system_version"] != spec["system_version"]:
        raise RuntimeError("System-version mismatch")
    system_path = PROJECT / f"research/group-composition/prompts/system_{spec['system_version']}.md"
    system = system_path.read_text()
    if system != original["system_prompt"]:
        raise RuntimeError("Original record and frozen system prompt differ")
    user_prompt = original["user_prompt"]
    inputs = [image_record(identity, index) for index, identity in enumerate(spec["input_identities"], 1)]
    content = [{"type": "input_text", "text": user_prompt}]
    for item in inputs:
        content.append({"type": "input_text", "text": item["role"]})
        content.append(image_content(Path(item["path"])))

    folder.mkdir(parents=True, exist_ok=False)
    record = {
        "id": run_id,
        "kind": "group_composition_corrected_inputs",
        "status": "rewriter_starting",
        "started_at": utc(),
        "original_counterpart": {
            "id": spec["original_id"],
            "provider": original.get("provider", "fal.ai"),
            "output": original["output"],
            "output_sha256": original["output_sha256"],
            "record": str(old_folder / "record.json"),
        },
        "case_id": original["case_id"],
        "case": original["case"],
        "system_version": spec["system_version"],
        "system_path": str(system_path),
        "system_sha256": digest(system_path),
        "system_prompt": system,
        "user_prompt": user_prompt,
        "input_images": inputs,
        "rewriter_model": "gpt-6-astra",
        "rewriter_reasoning": {"effort": "high"},
        "image_model": "gpt-image-2.5-sunburst",
        "image_settings": {"quality": "high", "size": "1536x1024", "output_format": "png", "n": 1},
        "scope": "composition only; no refractions; no auxiliary images",
        "transport": "Foundry-vended direct OpenAI credentials; unchanged bundled imagegen CLI",
        "provider_comparison_limitation": "Original counterpart used fal.ai with unexposed Astra effort/backend snapshot. New run uses direct OpenAI and fixed Astra high effort; observed differences cannot be attributed to source inputs alone.",
        "cli_path": str(CLI),
        "cli_sha256": digest(CLI),
        "output": str(output_path),
        "visual_review": None,
    }
    write_json(record_path, record, exclusive=True)
    (folder / "system_prompt.md").write_text(system)
    (folder / "user_prompt.txt").write_text(user_prompt + "\n")
    rewriter_request = {
        "created_at": utc(),
        "endpoint": "https://api.openai.com/v1/responses",
        "model": "gpt-6-astra",
        "reasoning": {"effort": "high"},
        "max_output_tokens": 5000,
        "system_prompt": system,
        "user_prompt": user_prompt,
        "images": inputs,
    }
    write_json(folder / "rewriter_request.json", rewriter_request, exclusive=True)
    response = direct_client().responses.create(
        model="gpt-6-astra",
        reasoning={"effort": "high"},
        max_output_tokens=5000,
        instructions=system,
        input=[{"role": "user", "content": content}],
    )
    prompt = response.output_text.strip()
    if response.status != "completed" or not prompt:
        record.update(status="rewriter_failed", rewriter_response_meta=response_meta(response), updated_at=utc())
        write_json(record_path, record)
        raise RuntimeError(f"Rewriter failed: {response.status}")
    (folder / "image_prompt.txt").write_text(prompt + "\n")
    write_json(folder / "rewriter_response.json", {
        "meta": response_meta(response), "output_text": prompt, "saved_at": utc()
    }, exclusive=True)
    record.update(
        status="image_prepared",
        image_prompt=prompt,
        rewriter_response_meta=response_meta(response),
        rewriter_completed_at=utc(),
    )
    write_json(record_path, record)
    image_request = {
        "prepared_at": utc(),
        "endpoint": "https://api.openai.com/v1/images/edits",
        "model": "gpt-image-2.5-sunburst",
        "settings": record["image_settings"],
        "prompt": prompt,
        "input_images": inputs,
        "request_id_limitation": "The unchanged bundled CLI does not expose HTTP request ID, returned model snapshot, usage or cost.",
        "retry_policy": "No blind retry: an uncertain POST consumes one bounded slot and requires manual review.",
    }
    write_json(folder / "image_request.json", image_request, exclusive=True)
    generation_number = increment_journal(run_id, record_path)
    write_json(folder / "image_submission.json", {
        "generation_number": generation_number,
        "post_starting_at": utc(),
        "request": str(folder / "image_request.json"),
    }, exclusive=True)
    record.update(status="image_post_started", generation_number=generation_number, image_post_started_at=utc())
    write_json(record_path, record)

    credentials = llm.get_openai()
    environment = os.environ.copy()
    environment["OPENAI_API_KEY"] = credentials.api_key
    environment["OPENAI_BASE_URL"] = str(credentials.base_url)
    if credentials.project:
        environment["OPENAI_PROJECT_ID"] = credentials.project
    command = [sys.executable, str(CLI), "edit", "--model", "gpt-image-2.5-sunburst"]
    for item in inputs:
        command.extend(["--image", item["path"]])
    command.extend([
        "--prompt-file", str(folder / "image_prompt.txt"),
        "--quality", "high",
        "--size", "1536x1024",
        "--output-format", "png",
        "--out", str(output_path),
        "--no-augment",
    ])
    before = time.monotonic()
    process = subprocess.run(command, env=environment, capture_output=True, text=True, timeout=600)
    seconds = round(time.monotonic() - before, 2)
    log = (process.stdout + "\n" + process.stderr).replace(credentials.api_key, "[REDACTED]")
    (folder / "image_cli.log").write_text(log)
    write_json(folder / "image_response.json", {
        "finished_at": utc(),
        "cli_returncode": process.returncode,
        "elapsed_seconds": seconds,
        "request_id": None,
        "request_id_limitation": image_request["request_id_limitation"],
    }, exclusive=True)
    if process.returncode or not output_path.exists():
        record.update(status="image_failed_or_uncertain", image_seconds=seconds, cli_returncode=process.returncode, updated_at=utc())
        write_json(record_path, record)
        update_journal(run_id, "failed_or_uncertain", cli_returncode=process.returncode)
        raise RuntimeError(f"Image generation failed or uncertain for {run_id}; do not retry automatically")
    with Image.open(output_path) as output:
        output.load()
        dimensions = list(output.size)
        mode = output.mode
    if digest(CLI) != record["cli_sha256"]:
        raise RuntimeError("Bundled CLI changed during execution")
    record.update(
        status="complete",
        completed_at=utc(),
        cli_returncode=process.returncode,
        image_seconds=seconds,
        output_sha256=digest(output_path),
        output_bytes=output_path.stat().st_size,
        output_dimensions=dimensions,
        output_mode=mode,
    )
    write_json(record_path, record)
    update_journal(run_id, "complete", output_sha256=record["output_sha256"], dimensions=dimensions)
    print(json.dumps({"id": run_id, "generation_number": generation_number, "seconds": seconds, "sha256": record["output_sha256"]}))


def judge(run_id: str) -> None:
    folder = RUNS / run_id
    destination = folder / "judge.json"
    if destination.exists():
        print(f"SKIP judged {run_id}")
        return
    record = json.loads((folder / "record.json").read_text())
    if record["status"] != "complete":
        raise RuntimeError(f"Incomplete run: {run_id}")
    instructions = JUDGE.read_text()
    content = [{"type": "input_text", "text": "Judge this corrected-input candidate independently. Return only the requested JSON object."}]
    roles = []
    for item in record["input_images"]:
        label = f"Corrected source Image {item['image_index']} — {item['identity']}; authoritative for source identity, contents and intended cup family."
        content.extend([{"type": "input_text", "text": label}, image_content(Path(item["path"]))])
        roles.append({"label": label, **item})
    original = Path(record["original_counterpart"]["output"])
    old_label = "Original-input counterpart output — FAL condition; comparison only, never a model input for generation."
    content.extend([{"type": "input_text", "text": old_label}, image_content(original)])
    roles.append({"label": old_label, "path": str(original), "sha256": digest(original), "bytes": original.stat().st_size})
    candidate = Path(record["output"])
    new_label = "New corrected-input candidate output — direct OpenAI condition; judge this output."
    content.extend([{"type": "input_text", "text": new_label}, image_content(candidate)])
    roles.append({"label": new_label, "path": str(candidate), "sha256": digest(candidate), "bytes": candidate.stat().st_size})
    request = {
        "created_at": utc(),
        "fresh_context": True,
        "endpoint": "https://api.openai.com/v1/responses",
        "model": "gpt-6-astra",
        "reasoning": {"effort": "high"},
        "max_output_tokens": 7000,
        "text_format": {"type": "json_object"},
        "instructions": instructions,
        "images": roles,
    }
    write_json(folder / "judge_request.json", request, exclusive=True)
    response = direct_client().responses.create(
        model="gpt-6-astra",
        reasoning={"effort": "high"},
        max_output_tokens=7000,
        text={"format": {"type": "json_object"}},
        instructions=instructions,
        input=[{"role": "user", "content": content}],
    )
    result = {
        "request": request,
        "response_meta": response_meta(response),
        "output": json.loads(response.output_text),
        "saved_at": utc(),
    }
    write_json(destination, result, exclusive=True)
    print(json.dumps({"id": run_id, "judge_request_id": result["response_meta"]["request_id"]}))


def finalize() -> None:
    reviews = json.loads((TOPIC / "direct_reviews.json").read_text())
    plan = json.loads(CASES.read_text())
    assert set(reviews) == set(plan)
    for run_id, review in reviews.items():
        record_path = RUNS / run_id / "record.json"
        record = json.loads(record_path.read_text())
        assert record["status"] == "complete"
        assert (RUNS / run_id / "judge.json").exists()
        record["visual_review"] = review
        record["transport_retry_limitation"] = (
            "The bounded counter records one unchanged-CLI invocation/submission per case. "
            "The CLI/OpenAI SDK default retry behavior is not exposed, so wire-level image POST count is unknown. "
            "No failed or uncertain invocation was manually retried."
        )
        record["reviewed_at"] = utc()
        write_json(record_path, record)
        image_request_path = RUNS / run_id / "image_request.json"
        image_request = json.loads(image_request_path.read_text())
        image_request["sdk_retry_observability"] = record["transport_retry_limitation"]
        write_json(image_request_path, image_request)
    validate()


def validate() -> None:
    plan = json.loads(CASES.read_text())
    journal = json.loads(JOURNAL.read_text())
    assert len(plan) == CEILING
    assert journal["generation_calls_started"] == CEILING
    assert journal["generation_outputs_completed"] == CEILING
    original_hashes = {}
    results = []
    for run_id, spec in plan.items():
        folder = RUNS / run_id
        record = json.loads((folder / "record.json").read_text())
        assert record["status"] == "complete"
        assert record["original_counterpart"]["id"] == spec["original_id"]
        assert record["system_version"] == spec["system_version"]
        assert [item["identity"] for item in record["input_images"]] == spec["input_identities"]
        assert Path(record["output"]).exists()
        assert digest(Path(record["output"])) == record["output_sha256"]
        assert record["output_dimensions"] == [1536, 1024]
        assert record["visual_review"]
        assert (folder / "judge.json").exists()
        assert (folder / "image_request.json").exists()
        assert (folder / "image_submission.json").exists()
        assert (folder / "image_response.json").exists()
        for item in record["input_images"]:
            assert digest(Path(item["path"])) == item["sha256"] == EXPECTED[item["identity"]]
        original_path = Path(record["original_counterpart"]["output"])
        old_hash = digest(original_path)
        assert old_hash == record["original_counterpart"]["output_sha256"]
        original_hashes[spec["original_id"]] = old_hash
        results.append({
            "id": run_id,
            "original_id": spec["original_id"],
            "output": record["output"],
            "output_sha256": record["output_sha256"],
            "input_sha256": [item["sha256"] for item in record["input_images"]],
            "rewriter_request_id": record["rewriter_response_meta"]["request_id"],
            "judge_request_id": json.loads((folder / "judge.json").read_text())["response_meta"]["request_id"],
        })
    evidence = {
        "validated_at": utc(),
        "status": "pass",
        "bounded_cli_invocations": CEILING,
        "wire_level_image_post_count": "unknown; unchanged CLI/OpenAI SDK default retry behavior is not exposed",
        "completed_outputs": len(results),
        "original_counterpart_hashes_verified": original_hashes,
        "runs": results,
        "limitations": [
            "Original counterparts used fal.ai; new candidates used direct OpenAI.",
            "Original Astra effort/backend snapshot was not exposed; new Astra effort is high.",
            "One stochastic output per condition cannot establish input-change causality.",
            "Source geometry landmarks are approximate 2D projections, not physical measurements.",
            "The bounded counter establishes nine CLI invocations/submissions and nine outputs, not the wire-level POST count.",
        ],
    }
    write_json(DATA / "_review/corrected_composition_execution_validation.json", evidence)
    print(json.dumps({"status": "pass", "outputs": len(results), "journal": journal}))


def main() -> None:
    os.umask(0o077)
    logging.disable(logging.CRITICAL)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    generate_parser = sub.add_parser("generate")
    generate_parser.add_argument("run_id")
    judge_parser = sub.add_parser("judge")
    judge_parser.add_argument("run_id")
    sub.add_parser("finalize")
    sub.add_parser("validate")
    args = parser.parse_args()
    if args.command == "generate":
        generate(args.run_id)
    elif args.command == "judge":
        judge(args.run_id)
    elif args.command == "finalize":
        finalize()
    else:
        validate()


if __name__ == "__main__":
    main()
