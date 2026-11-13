"""Direct-route multi-cup refraction refinement with a durable 20-image counter."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from foundry_aws_gateway import llm
from PIL import Image


TOPIC = Path("/home/colligo/hs_scripts/claude/mixology/research/multi-cup-refractions")
DATA = Path("/home/colligo/mixology_data/refraction_research_2026-10-19")
RUN_ROOT = DATA / "multi-cup-refractions" / "runs"
CLI = Path("/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py")
CASES = TOPIC / "cases.json"
JOURNAL = TOPIC / "iteration_journal.json"
V3 = TOPIC / "prompts" / "system_v3_frozen.md"
V4 = TOPIC / "prompts" / "system_v4_focus_clause.md"
FLOOR_CORRECTION = TOPIC / "prompts" / "system_floor_correction.md"
FIVE_GLOBAL_FOCUS = TOPIC / "prompts" / "system_five_global_focus.md"
FIVE_GLOBAL_FOCUS_NOSTYLE = TOPIC / "prompts" / "system_five_global_focus_nostyle.md"
FIVE_BRANCH_RESHAPE = TOPIC / "prompts" / "system_five_branch_reshape.md"
FIVE_FACETED_BRANCHES = TOPIC / "prompts" / "system_five_faceted_branches.md"
FIVE_BENCHMARKED_BRANCHES = TOPIC / "prompts" / "system_five_benchmarked_branches.md"
FIVE_FRESH_GLOBAL_FOCUS = TOPIC / "prompts" / "system_five_fresh_global_focus.md"
FIVE_SUBTLE_FORKS = TOPIC / "prompts" / "system_five_subtle_forks.md"
FIVE_BRANCH_BUNDLES = TOPIC / "prompts" / "system_five_branch_bundles.md"
COMBINED_V1 = Path("/home/colligo/hs_scripts/claude/mixology/research/combined-composition/prompts/system_v1.md")
JUDGE = TOPIC / "prompts" / "judge.md"
CEILING = 20


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, data: object, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if exclusive:
        with path.open("x") as stream:
            json.dump(data, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        return
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w") as stream:
        json.dump(data, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    temporary.replace(path)


def picture(path: Path) -> dict:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    payload = base64.b64encode(path.read_bytes()).decode()
    return {"type": "input_image", "image_url": f"data:{mime};base64,{payload}"}


def add_role(content: list[dict], label: str, path: Path) -> None:
    content.append({"type": "input_text", "text": label})
    content.append(picture(path))


def image_record(label: str, path: Path) -> dict:
    with Image.open(path) as image:
        dimensions = list(image.size)
    return {
        "label": label,
        "path": str(path),
        "sha256": digest(path),
        "bytes": path.stat().st_size,
        "dimensions": dimensions,
    }


def direct_client():
    return llm.get_openai().with_options(timeout=300, max_retries=1)


def response_meta(response) -> dict:
    usage = response.usage.model_dump(mode="json") if response.usage else None
    return {
        "id": response.id,
        "request_id": response._request_id,
        "model": response.model,
        "status": response.status,
        "created_at": response.created_at,
        "completed_at": response.completed_at,
        "error": response.error.model_dump(mode="json") if response.error else None,
        "incomplete_details": (
            response.incomplete_details.model_dump(mode="json")
            if response.incomplete_details
            else None
        ),
        "usage": usage,
        "output_types": [getattr(item, "type", type(item).__name__) for item in response.output],
    }


def read_plan() -> dict:
    return json.loads(CASES.read_text())


def count_before_call(candidate_id: str, record: dict) -> None:
    journal = json.loads(JOURNAL.read_text())
    if any(entry.get("candidate_id") == candidate_id for entry in journal["entries"]):
        raise RuntimeError(f"Candidate already has a journal entry: {candidate_id}")
    started = int(journal["generation_calls_started"])
    if started >= CEILING:
        raise RuntimeError(f"Generation ceiling reached: {started}/{CEILING}")
    journal["generation_calls_started"] = started + 1
    journal["entries"].append(
        {
            "candidate_id": candidate_id,
            "generation_number": started + 1,
            "status": "image_post_starting",
            "counted_at": utc(),
            "run_record": str(record["run_record"]),
            "pipeline": record["pipeline"],
            "arrangement": record["arrangement"],
            "style": record["style"],
        }
    )
    write_json(JOURNAL, journal)


def update_journal(candidate_id: str, status: str, **fields) -> None:
    journal = json.loads(JOURNAL.read_text())
    matching = [entry for entry in journal["entries"] if entry["candidate_id"] == candidate_id]
    if len(matching) != 1:
        raise RuntimeError(f"Expected one journal entry for {candidate_id}")
    matching[0].update(status=status, updated_at=utc(), **fields)
    journal["generation_outputs_completed"] = sum(
        entry.get("status") == "complete" for entry in journal["entries"]
    )
    write_json(JOURNAL, journal)


def make_rewriter_content(candidate: dict, arrangement: dict, style_path: Path) -> tuple[list[dict], list[dict]]:
    user_prompt = candidate.get("user_prompt") or (
        arrangement["one_stage_user_prompt"]
        if candidate["pipeline"] == "one_stage"
        else arrangement["two_stage_user_prompt"]
    )
    content = [{"type": "input_text", "text": user_prompt}]
    records: list[dict] = []
    if candidate["pipeline"] in {"two_stage", "correction"}:
        target = (
            Path(arrangement["neutral_target"])
            if candidate["pipeline"] == "two_stage"
            else RUN_ROOT / candidate["base_candidate"] / "output.png"
        )
        label = "Image 1 — edit target, authoritative for cup count, identity, arrangement, camera and crop."
        add_role(content, label, target)
        records.append(image_record(label, target))
        if style_path is not None:
            style_label = "Image 2 — lighting STYLE reference only. Match optical hierarchy, focal intensity, branching scale variation and falloff; do not copy its drinks, colors, camera or placement."
            add_role(content, style_label, style_path)
            records.append(image_record(style_label, style_path))
    else:
        for index, value in enumerate(arrangement["source_images"], start=1):
            path = Path(value)
            label = f"Image {index} — DRINK identity source. Include this finished drink exactly once."
            add_role(content, label, path)
            records.append(image_record(label, path))
        index = len(arrangement["source_images"]) + 1
        if style_path is not None:
            style_label = f"Image {index} — lighting STYLE reference only. Match optical hierarchy, focal intensity, branching scale variation and falloff; do not copy its drinks, colors, camera or placement."
            add_role(content, style_label, style_path)
            records.append(image_record(style_label, style_path))
    return content, records


def diagnose() -> None:
    output = TOPIC / "data" / "diagnosis_astra_high.json"
    if output.exists():
        raise RuntimeError(f"Diagnosis already exists: {output}")
    plan = read_plan()
    benchmark = Path(plan["benchmark"])
    bad_trio, bad_five = map(Path, plan["bad_examples"])
    trio = Path(plan["arrangements"]["trio"]["neutral_target"])
    five = Path(plan["arrangements"]["five"]["neutral_target"])
    instructions = (
        "Analyze visible evidence for a controlled image-editing experiment. Distinguish observations from hypotheses. "
        "The user approves the benchmark morphology and rejects the two failures. Identify the exact visual difference, "
        "rank plausible causes for the regression without claiming causality from stochastic single images, and assess the "
        "information value of comparing one-stage composition+relighting against two-stage relighting of the supplied neutral targets. "
        "Return JSON with observed_differences, hypotheses (each with rationale, confidence and falsifying_test), confounds, "
        "recommended_control_order, and prompt_language_risks. Do not call any arrangement example customer approved."
    )
    content = [{"type": "input_text", "text": "Perform the comparison using only concrete visible evidence and the supplied provenance. Return the requested JSON object."}]
    roles = []
    for label, path in (
        ("A — user-approved positive benchmark morphology", benchmark),
        ("B — rejected three-cup combined output", bad_trio),
        ("C — rejected five-cup combined output", bad_five),
        ("D — neutral three-cup composition available as two-stage edit target", trio),
        ("E — neutral five-cup composition available as two-stage edit target", five),
    ):
        add_role(content, label, path)
        roles.append(image_record(label, path))
    request = {
        "created_at": utc(),
        "model": "gpt-6-astra",
        "reasoning": {"effort": "high"},
        "max_output_tokens": 8000,
        "text_format": {"type": "json_object"},
        "instructions": instructions,
        "images": roles,
    }
    write_json(TOPIC / "data" / "diagnosis_request_attempt2.json", request, exclusive=True)
    response = direct_client().responses.create(
        model="gpt-6-astra",
        reasoning={"effort": "high"},
        max_output_tokens=8000,
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
    write_json(output, result, exclusive=True)
    print(json.dumps(result["response_meta"], indent=2))


def prompt_advice() -> None:
    output = TOPIC / "data" / "prompt_advice_astra_high.json"
    if output.exists():
        raise RuntimeError(f"Prompt advice already exists: {output}")
    plan = read_plan()
    benchmark = Path(plan["benchmark"])
    trio = RUN_ROOT / "i05_trio_two_stage_benchmark" / "output.png"
    five = RUN_ROOT / "i06_five_two_stage_benchmark" / "output.png"
    instructions = (
        "You are advising a controlled image-edit prompt experiment. The two candidates used the frozen V3 prompt and the exact "
        "positive benchmark as style reference, but still produced dominant uniform cellular mesh. The user's required morphology is "
        "a compact dominant bright concentration with a small number of irregular outward branches that taper and lose energy, rendered "
        "as photographic transmitted light. It must not become a starburst, literal bolt, global glow, white fog, wave, vein or mesh. "
        "Return JSON with visible_failure, why_current_language_is_ambiguous, smallest_prompt_delta, exact_added_clause, risks, and expected_test. "
        "The exact_added_clause must be one or two concise sentences suitable for appending to the frozen V3 system prompt. Do not change "
        "cup identity, composition, color attribution, shared direction or receiving-plane constraints."
    )
    content = [{"type": "input_text", "text": "Use the images to propose the smallest controlled prompt change. Return the requested JSON object."}]
    roles = []
    for label, path in (
        ("A — exact user-approved positive benchmark morphology", benchmark),
        ("B — three-cup V3 plus benchmark-style candidate that failed morphology", trio),
        ("C — five-cup V3 plus benchmark-style candidate that failed morphology", five),
        ("D — rejected historical three-cup mesh example", Path(plan["bad_examples"][0])),
        ("E — rejected historical five-cup mesh example", Path(plan["bad_examples"][1])),
    ):
        add_role(content, label, path)
        roles.append(image_record(label, path))
    request = {
        "created_at": utc(), "model": "gpt-6-astra", "reasoning": {"effort": "high"},
        "max_output_tokens": 6000, "text_format": {"type": "json_object"},
        "instructions": instructions, "images": roles,
    }
    write_json(TOPIC / "data" / "prompt_advice_request.json", request, exclusive=True)
    response = direct_client().responses.create(
        model="gpt-6-astra", reasoning={"effort": "high"}, max_output_tokens=6000,
        text={"format": {"type": "json_object"}}, instructions=instructions,
        input=[{"role": "user", "content": content}],
    )
    result = {"request": request, "response_meta": response_meta(response), "output": json.loads(response.output_text), "saved_at": utc()}
    write_json(output, result, exclusive=True)
    print(json.dumps(result, indent=2))


def generate(candidate_id: str) -> None:
    plan = read_plan()
    spec = plan["candidates"][candidate_id]
    arrangement = plan["arrangements"][spec["arrangement"]]
    folder = RUN_ROOT / candidate_id
    folder.mkdir(parents=True, exist_ok=True)
    record_path = folder / "record.json"
    if record_path.exists() or (folder / "output.png").exists():
        raise RuntimeError(f"Refusing to reuse existing candidate: {folder}")
    style_path = (
        None
        if spec["style"] == "none"
        else Path(plan["original_style"] if spec["style"] == "original" else plan["benchmark"])
    )
    system_path = {
        "combined_v1": COMBINED_V1,
        "v3": V3,
        "v4_focus_clause": V4,
        "floor_correction": FLOOR_CORRECTION,
        "five_global_focus": FIVE_GLOBAL_FOCUS,
        "five_global_focus_nostyle": FIVE_GLOBAL_FOCUS_NOSTYLE,
        "five_branch_reshape": FIVE_BRANCH_RESHAPE,
        "five_faceted_branches": FIVE_FACETED_BRANCHES,
        "five_benchmarked_branches": FIVE_BENCHMARKED_BRANCHES,
        "five_fresh_global_focus": FIVE_FRESH_GLOBAL_FOCUS,
        "five_subtle_forks": FIVE_SUBTLE_FORKS,
        "five_branch_bundles": FIVE_BRANCH_BUNDLES,
    }[spec["system"]]
    system = system_path.read_text()
    content, inputs = make_rewriter_content(spec, arrangement, style_path)
    user_prompt = spec.get("user_prompt") or arrangement[
        "one_stage_user_prompt" if spec["pipeline"] == "one_stage" else "two_stage_user_prompt"
    ]
    record = {
        "candidate_id": candidate_id,
        "started_at": utc(),
        "status": "rewriter_starting",
        "pipeline": spec["pipeline"],
        "arrangement": spec["arrangement"],
        "style": spec["style"],
        "system_name": spec["system"],
        "system_path": str(system_path),
        "system_sha256": digest(system_path),
        "system_prompt": system,
        "user_prompt": user_prompt,
        "input_images": inputs,
        "rewriter_model": "gpt-6-astra",
        "rewriter_reasoning": {"effort": "high"},
        "image_model": "gpt-image-2.5-sunburst",
        "image_settings": {"quality": "high", "size": "1536x1024", "output_format": "png", "n": 1},
        "transport": "Foundry-vended direct OpenAI credentials; unchanged bundled imagegen CLI",
        "run_record": str(record_path),
        "cli_path": str(CLI),
        "cli_sha256": digest(CLI),
    }
    write_json(record_path, record, exclusive=True)
    (folder / "system_prompt.md").write_text(system)
    (folder / "user_prompt.txt").write_text(user_prompt + "\n")
    fixed_prompt_from = spec.get("fixed_image_prompt_from")
    if fixed_prompt_from:
        source_prompt = RUN_ROOT / fixed_prompt_from / "image_prompt.txt"
        image_prompt = source_prompt.read_text().strip()
        rewriter_request = {
            "created_at": utc(),
            "rewriter_used": False,
            "control": "Byte-identical image prompt repeat; no new Astra rewrite.",
            "source_candidate": fixed_prompt_from,
            "source_prompt_path": str(source_prompt),
            "source_prompt_sha256": digest(source_prompt),
            "images": inputs,
        }
        write_json(folder / "rewriter_request.json", rewriter_request, exclusive=True)
        rewriter_response = {"rewriter_used": False, "output_text": image_prompt}
        write_json(folder / "rewriter_response.json", rewriter_response, exclusive=True)
        record.update(rewriter_model=None, rewriter_reasoning=None, fixed_image_prompt_from=fixed_prompt_from)
    else:
        rewriter_request = {
            "created_at": utc(),
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
        if response.status != "completed" or not response.output_text.strip():
            record.update(status="rewriter_failed", rewriter_response_meta=response_meta(response), updated_at=utc())
            write_json(record_path, record)
            raise RuntimeError(f"Rewriter failed for {candidate_id}: {response.status}")
        image_prompt = response.output_text.strip()
        rewriter_response = {"meta": response_meta(response), "output_text": image_prompt}
        write_json(folder / "rewriter_response.json", rewriter_response, exclusive=True)
        record.update(rewriter_response_meta=rewriter_response["meta"])
    (folder / "image_prompt.txt").write_text(image_prompt + "\n")
    record.update(
        status="image_prepared",
        image_prompt=image_prompt,
        rewriter_completed_at=utc(),
    )
    write_json(record_path, record)
    image_request = {
        "prepared_at": utc(),
        "endpoint": "https://api.openai.com/v1/images/edits",
        "model": "gpt-image-2.5-sunburst",
        "settings": record["image_settings"],
        "prompt": image_prompt,
        "input_images": inputs,
        "request_id_limitation": "The unchanged bundled CLI does not expose the HTTP request ID or returned model snapshot.",
        "retry_policy": "No orchestration-level retry. The unchanged CLI uses SDK defaults; internal wire-level retry behavior is not inspected or claimed. An uncertain candidate invocation consumes one generation slot and requires manual evidence review.",
    }
    write_json(folder / "image_request.json", image_request, exclusive=True)
    count_before_call(candidate_id, record)
    record.update(status="image_post_started", image_post_started_at=utc())
    write_json(record_path, record)
    credential_client = llm.get_openai()
    environment = os.environ.copy()
    environment["OPENAI_API_KEY"] = credential_client.api_key
    environment["OPENAI_BASE_URL"] = str(credential_client.base_url)
    if credential_client.project:
        environment["OPENAI_PROJECT_ID"] = credential_client.project
    command = [sys.executable, str(CLI), "edit", "--model", "gpt-image-2.5-sunburst"]
    for item in inputs:
        command.extend(["--image", item["path"]])
    command.extend(
        [
            "--prompt-file", str(folder / "image_prompt.txt"),
            "--quality", "high",
            "--size", "1536x1024",
            "--output-format", "png",
            "--out", str(folder / "output.png"),
            "--no-augment",
        ]
    )
    before = time.monotonic()
    process = subprocess.run(command, env=environment, capture_output=True, text=True, timeout=600)
    elapsed = round(time.monotonic() - before, 2)
    sanitized = (process.stdout + "\n" + process.stderr).replace(credential_client.api_key, "[REDACTED]")
    (folder / "image_cli.log").write_text(sanitized)
    record.update(cli_returncode=process.returncode, image_seconds=elapsed, image_post_finished_at=utc())
    if process.returncode or not (folder / "output.png").exists():
        record.update(status="image_failed_or_uncertain", updated_at=utc())
        write_json(record_path, record)
        update_journal(candidate_id, "failed_or_uncertain", cli_returncode=process.returncode)
        raise RuntimeError(f"Image call failed or uncertain for {candidate_id}; do not auto-retry")
    with Image.open(folder / "output.png") as output:
        output.load()
        dimensions = list(output.size)
        mode = output.mode
    record.update(
        status="complete",
        completed_at=utc(),
        output=str(folder / "output.png"),
        output_sha256=digest(folder / "output.png"),
        output_bytes=(folder / "output.png").stat().st_size,
        output_dimensions=dimensions,
        output_mode=mode,
    )
    write_json(record_path, record)
    update_journal(candidate_id, "complete", output_sha256=record["output_sha256"], dimensions=dimensions)
    print(json.dumps({"candidate": candidate_id, "dimensions": dimensions, "seconds": elapsed, "sha256": record["output_sha256"]}, indent=2))


def judge(candidate_id: str) -> None:
    folder = RUN_ROOT / candidate_id
    destination = folder / "judge.json"
    if destination.exists():
        raise RuntimeError(f"Judge already exists: {destination}")
    record = json.loads((folder / "record.json").read_text())
    if record["status"] != "complete":
        raise RuntimeError(f"Candidate incomplete: {candidate_id}")
    plan = read_plan()
    arrangement = plan["arrangements"][record["arrangement"]]
    instructions = JUDGE.read_text()
    content = [{"type": "input_text", "text": "Judge this candidate independently. Return only the requested JSON object with concrete visible evidence."}]
    roles: list[dict] = []
    for index, value in enumerate(arrangement["source_images"], start=1):
        path = Path(value)
        label = f"Source {index} — original authoritative drink identity and contents."
        add_role(content, label, path)
        roles.append(image_record(label, path))
    neutral = Path(arrangement["neutral_target"])
    label = "Neutral composition target — authoritative for the requested cup arrangement in two-stage candidates; useful layout comparator for one-stage candidates."
    add_role(content, label, neutral)
    roles.append(image_record(label, neutral))
    benchmark = Path(plan["benchmark"])
    label = "User-approved positive benchmark — morphology and photographic optical hierarchy only. Do not copy its drinks, colors, camera or exact placement."
    add_role(content, label, benchmark)
    roles.append(image_record(label, benchmark))
    for number, value in enumerate(plan["bad_examples"], start=1):
        path = Path(value)
        label = f"User-rejected negative {number} — calibrates uniform mesh/vein/wave failure only."
        add_role(content, label, path)
        roles.append(image_record(label, path))
    candidate = folder / "output.png"
    label = "Candidate output to judge."
    add_role(content, label, candidate)
    roles.append(image_record(label, candidate))
    request = {
        "created_at": utc(),
        "fresh_context": True,
        "model": "gpt-6-astra",
        "reasoning": {"effort": "high"},
        "max_output_tokens": 8000,
        "text_format": {"type": "json_object"},
        "instructions": instructions,
        "images": roles,
    }
    write_json(folder / "judge_request.json", request, exclusive=True)
    response = direct_client().responses.create(
        model="gpt-6-astra",
        reasoning={"effort": "high"},
        max_output_tokens=8000,
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
    print(json.dumps({"candidate": candidate_id, "response_meta": result["response_meta"], "judgment": result["output"]}, indent=2))


def main() -> None:
    os.umask(0o077)
    logging.disable(logging.CRITICAL)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("diagnose")
    sub.add_parser("prompt-advice")
    generate_parser = sub.add_parser("generate")
    generate_parser.add_argument("candidate_id")
    judge_parser = sub.add_parser("judge")
    judge_parser.add_argument("candidate_id")
    args = parser.parse_args()
    if args.command == "diagnose":
        diagnose()
    elif args.command == "prompt-advice":
        prompt_advice()
    elif args.command == "generate":
        generate(args.candidate_id)
    else:
        judge(args.candidate_id)


if __name__ == "__main__":
    main()
