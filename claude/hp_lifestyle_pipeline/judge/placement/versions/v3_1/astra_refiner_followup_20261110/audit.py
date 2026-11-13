"""Verify durable source, actual Astra responses and exact proposed prompt artifacts."""

from datetime import datetime, timezone
import argparse
import json
from pathlib import Path

from prepare import ROOT, sha, write_json


def verify(visual_only=False, resumed=False):
    source = json.loads((ROOT / "evidence_manifest.json").read_text())
    if sha(ROOT / "source/full_evalset.html") != source["source"]["sha256"]:
        raise ValueError("source HTML changed")
    statuses = {}
    source_hashes = set()
    for case in source["cases"]:
        statuses[case["status"]] = statuses.get(case["status"], 0) + 1
        for item in case["images"].values():
            if sha(Path(item["path"])) != item["sha256"]:
                raise ValueError("preserved original source media changed")
            source_hashes.add(item["sha256"])
        if case["status"] == "passthrough":
            if case["images"]["baseline"]["sha256"] != case["images"]["refined"]["sha256"]:
                raise ValueError("passthrough is not byte-identical")
    if len(source["cases"]) != 64 or statuses != {"passthrough": 47, "refined": 17}:
        raise ValueError("source case accounting changed")
    for case in source["historical_annotated_examples_and_controls"]:
        for role in ("generated_image", "twin_image"):
            item = case[role]
            if sha(Path(item["local_path"])) != item["sha256"]:
                raise ValueError("historical image changed")
    all_case_ids = []
    receipts = []
    previous_end = ""
    for number in range(1, 5):
        directory = ROOT / "batches" / f"batch{number}"
        package = json.loads((directory / "input.json").read_text())
        config = json.loads((directory / "config.json").read_text())
        receipt = json.loads((directory / "receipt.json").read_text())
        raw = json.loads((directory / "response.json").read_text())
        result = json.loads((directory / "analysis.json").read_text())
        if result != json.loads(raw["choices"][0]["message"]["content"]):
            raise ValueError("stored review differs from raw Astra response")
        if (receipt["response_sha256"] != sha(directory / "response.json")
                or config["input_sha256"] != sha(directory / "input.json")
                or config["brief_sha256"] != sha(ROOT / "brief.txt")):
            raise ValueError("consultation input/output identity changed")
        if raw["model"] != "gpt-6-astra" or raw["choices"][0]["finish_reason"] != "stop":
            raise ValueError("unexpected actual visual model or incomplete result")
        if config["started_at_utc"] < previous_end:
            raise ValueError("Astra calls overlapped")
        previous_end = receipt["completed_at_utc"]
        expected = [row["case_id"] for row in package["case_inputs"]]
        actual = [row["case_id"] for row in result["case_reviews"]]
        if len(actual) != 16 or set(actual) != set(expected):
            raise ValueError("case review binding mismatch")
        actual_anchors = [row["case_id"] for row in result["anchor_reviews"]]
        expected_anchors = [row["case_id"] for row in package["historical_examples"]]
        if len(actual_anchors) != len(expected_anchors) or set(actual_anchors) != set(expected_anchors):
            raise ValueError("historical review binding mismatch")
        for item in package["image_inventory"]:
            if sha(Path(item["path"])) != item["sha256"]:
                raise ValueError("submitted review image changed")
        for contract in package["frozen_contracts"]:
            if sha(Path(contract["path"])) != contract["sha256"]:
                raise ValueError("frozen predecessor contract changed")
        all_case_ids.extend(actual)
        receipts.append(receipt)
    if len(all_case_ids) != 64 or set(all_case_ids) != {case["id"] for case in source["cases"]}:
        raise ValueError("visual consultation omitted or duplicated source cases")
    if visual_only:
        seeds = []
        for number in range(1, 5):
            path = ROOT / "batches" / f"batch{number}" / "analysis.json"
            for item in json.loads(path.read_text())["proposal_seeds"]:
                seeds.append({"batch": number, "source_analysis": str(path),
                              "astra_proposal_seed": item})
        write_json(ROOT / "astra_proposal_seeds.json", seeds)
        report = {
            "verified_at_utc": datetime.now(timezone.utc).isoformat(),
            "status": "visual_analysis_complete_full_prompt_synthesis_blocked",
            "source_case_count": 64, "reviewed_case_count": len(all_case_ids),
            "source_statuses_not_judge_outcomes": statuses,
            "unique_original_source_pngs": len(source_hashes),
            "historical_criterion_examples": 3, "non_gold_stability_controls": 3,
            "successful_visual_responses": 4, "model": "gpt-6-astra",
            "reasoning_effort": "high", "max_visual_concurrency": 1,
            "proposal_seed_count_including_overlaps": len(seeds),
            "complete_replacement_prompt_count": 0,
            "known_visual_response_usage": {
                key: sum(item["usage"][key] for item in receipts)
                for key in ("prompt_tokens", "completion_tokens", "total_tokens")},
            "call_accounting": "Successful logical responses, not instrumented SDK transport attempts. Two unresolved/failed synthesis attempts have unknown upstream completion and usage.",
            "checked_source_media_html_and_predecessor_contracts_unchanged": True,
            "new_judge_execution": False, "promoted": False,
            "limitation": "Identity/coverage audit, not validation of visual truth, prompt compatibility or judge accuracy.",
        }
        write_json(ROOT / "visual_completion_audit.json", report)
        print(json.dumps(report), flush=True)
        return
    if resumed:
        from resume_synthesis import Collector, RUN

        selected = json.loads((RUN / "selected_attempt.json").read_text())
        synthesis_dir = Path(selected["attempt"])
        if synthesis_dir.parent != RUN:
            raise ValueError("selected attempt is outside the resumed run")
        config = json.loads((synthesis_dir / "config.json").read_text())
        receipt = json.loads((synthesis_dir / "receipt.json").read_text())
        collector = Collector()
        with (synthesis_dir / "chunks.jsonl").open() as stream:
            for line in stream:
                collector.feed(json.loads(line))
        proposed = json.loads((synthesis_dir / "proposals.json").read_text())
        if collector.result() != proposed:
            raise ValueError("proposed prompts differ from the actual raw Astra stream")
        if (receipt["stream_sha256"] != sha(synthesis_dir / "chunks.jsonl")
                or receipt["output_sha256"] != sha(synthesis_dir / "proposals.json")
                or selected["receipt_sha256"] != sha(synthesis_dir / "receipt.json")
                or selected["proposals_sha256"] != sha(synthesis_dir / "proposals.json")
                or config["input_sha256"] != sha(RUN / "input.json")
                or config["brief_sha256"] != sha(RUN / "brief.txt")
                or sha(RUN / "input.json") != sha(ROOT / "synthesis/input.json")
                or sha(RUN / "brief.txt") != sha(ROOT / "synthesis_brief.txt")
                or config["started_at_utc"] < previous_end
                or receipt["usage"] != collector.usage
                or config["sdk_max_retries"] != 0):
            raise ValueError("resumed synthesis source/stream/configuration identity mismatch")
        artifact_root = RUN
    else:
        synthesis_dir = ROOT / "synthesis_recovery"
        raw = json.loads((synthesis_dir / "response.json").read_text())
        proposed = json.loads((synthesis_dir / "proposals.json").read_text())
        if proposed != json.loads(raw["choices"][0]["message"]["content"]):
            raise ValueError("proposal document differs from actual synthesis output")
        config = json.loads((synthesis_dir / "config.json").read_text())
        receipt = json.loads((synthesis_dir / "receipt.json").read_text())
        if (raw["model"] != "gpt-6-astra" or raw["choices"][0]["finish_reason"] != "stop"
                or config["started_at_utc"] < previous_end
                or config["input_sha256"] != sha(synthesis_dir / "input.json")
                or config["brief_sha256"] != sha(ROOT / "synthesis_brief.txt")
                or receipt["response_sha256"] != sha(synthesis_dir / "response.json")):
            raise ValueError("synthesis identity/configuration mismatch")
        artifact_root = ROOT
    anchor_ids = [item["case_id"] for item in proposed["historical_anchor_reconciliation"]]
    if len(anchor_ids) != 6 or set(anchor_ids) != {
            item["id"] for item in source["historical_annotated_examples_and_controls"]}:
        raise ValueError("synthesis historical-example coverage differs")
    if len(proposed["proposals"]) != 3 or len({item["id"] for item in proposed["proposals"]}) != 3:
        raise ValueError("synthesis must contain exactly three distinct candidates")
    receipts.append(receipt)
    artifacts = json.loads(((artifact_root if resumed else synthesis_dir) / "artifact_manifest.json").read_text())
    expected_artifacts = []
    for proposal in proposed["proposals"]:
        for prompt in proposal["system_prompts"]:
            path = artifact_root / "proposals" / proposal["id"] / prompt["artifact_name"]
            if path.read_text() != prompt["text"]:
                raise ValueError("prompt artifact differs from exact Astra proposal")
            expected_artifacts.append((proposal["id"], prompt["role"], str(path), sha(path)))
    actual_artifacts = [(row["proposal"], row["role"], row["path"], row["sha256"])
                        for row in artifacts]
    if actual_artifacts != expected_artifacts:
        raise ValueError("prompt extraction inventory mismatch")
    bundle_path = None
    if resumed:
        sections = [
            "ASTRA JUDGE PROPOSALS - UNTESTED, NOT PROMOTED\n",
            "The complete prompt text below is copied unchanged from Astra's successful response.\n",
            "Parent integration caveat: P1 claims drop-in compatibility, but its verifier prompts\n"
            "request full placement-observations-v3 objects. The frozen r1 runner instead requires\n"
            "placement-verifier-components-v1 with only requested components. Resolve that\n"
            "contract conflict before evaluation. These files do not modify any existing judge.\n\n",
        ]
        for proposal in proposed["proposals"]:
            sections.extend([
                f"=== {proposal['id']}: {proposal['short_name']} ===\n",
                "Compatibility proposed by Astra:\n",
                json.dumps(proposal["compatibility"], indent=2) + "\n\n",
            ])
            for prompt in proposal["system_prompts"]:
                sections.extend([
                    f"--- BEGIN {prompt['artifact_name']} | {prompt['role']} ---\n",
                    prompt["text"],
                    f"\n--- END {prompt['artifact_name']} ---\n\n",
                ])
        bundle_path = RUN / "proposal_bundle.txt"
        bundle_text = "".join(sections)
        if bundle_path.exists():
            if bundle_path.read_text() != bundle_text:
                raise ValueError("existing review bundle differs from verified prompts")
        else:
            with bundle_path.open("x") as stream:
                stream.write(bundle_text)
    report = {
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_case_count": 64, "source_statuses_not_judge_outcomes": statuses,
        "unique_original_source_pngs": len(source_hashes),
        "refiner_case_review_count": len(all_case_ids),
        "historical_criterion_examples": 3, "non_gold_stability_controls": 3,
        "successful_visual_responses": 4, "successful_text_only_synthesis_responses": 1,
        "call_accounting": "Successful returned responses, not a billing total. Earlier SDK transport attempts are not independently instrumented.",
        "unresolved_prior_synthesis": "One initial request was stopped without a response; one30-minute recovery timed out. Upstream completion/usage of failed attempts remain unknown.",
        "selected_synthesis_attempt": str(synthesis_dir),
        "model": "gpt-6-astra", "reasoning_effort": "high", "max_concurrency": 1,
        "proposal_count": len(proposed["proposals"]), "prompt_artifact_count": len(artifacts),
        "review_bundle": str(bundle_path) if bundle_path else None,
        "review_bundle_sha256": sha(bundle_path) if bundle_path else None,
        "known_successful_response_usage": {key: sum(item["usage"][key] for item in receipts if item["usage"])
                  for key in ("prompt_tokens", "completion_tokens", "total_tokens")},
        "responses_without_usage": sum(item["usage"] is None for item in receipts),
        "new_judge_execution": False, "promoted": False,
        "checked_source_media_html_and_predecessor_contracts_unchanged": True,
        "prompt_extraction_exact": True,
        "limitation": "Identity/coverage audit only, not validation of visual truth, prompt compatibility or judge accuracy.",
    }
    write_json(ROOT / "completion_audit.json", report)
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--visual-only", action="store_true",
                        help="Audit completed visual evidence without claiming final prompt completion.")
    parser.add_argument("--resumed", action="store_true",
                        help="Verify successful resumed synthesis against its original streaming chunks.")
    args = parser.parse_args()
    if args.visual_only and args.resumed:
        parser.error("--visual-only and --resumed are mutually exclusive")
    verify(args.visual_only, args.resumed)
