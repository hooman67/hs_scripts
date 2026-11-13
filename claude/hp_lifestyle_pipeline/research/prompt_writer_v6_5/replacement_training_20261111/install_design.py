#!/usr/bin/env python3
"""Compile actual Astra text/choices into a separate replacement runtime."""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
VERSIONS = PROJECT / "research/source_messaging_v1_to_v6/versions"
BASE = VERSIONS / "v6_5"
DEST = VERSIONS / "v6_5_training"
CATALOG = "approved-v6.5-20261111.catalog.json"
ENV = {"Home": "HOM", "Office": "OFF", "Education": "EDU", "Gaming": "GAM",
       "Café": "CAF", "Creative Studio": "STU"}


def main(refresh_assets=False):
    if DEST.exists() and not refresh_assets:
        raise FileExistsError("replacement runtime already exists; inspect instead of overwriting")
    if refresh_assets and (DEST / "assets_manifest.json").exists():
        raise FileExistsError("frozen replacement assets cannot be refreshed")
    spec = importlib.util.spec_from_file_location("training_design_replay", HERE / "consult_astra.py")
    consultation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(consultation)
    tools = consultation.transport
    proposal = tools.load(HERE / "astra/proposal.json")
    receipt = tools.load(HERE / "astra/receipt.json")
    if (
        not receipt["ok"] or receipt["semantic_resampling"]
        or receipt["model_returned"] != ["gpt-6-astra"] or receipt["finish_reason"] != "stop"
        or tools.sha(receipt["frames_path"]) != receipt["frames_sha256"]
        or tools.sha(HERE / "astra/proposal.json") != receipt["proposal_sha256"]
    ):
        raise ValueError("actual Astra provenance failed")
    collector = tools.Collector()
    for line in Path(receipt["frames_path"]).read_text().splitlines():
        collector.feed(json.loads(line))
    if collector.result() != proposal:
        raise ValueError("design does not replay from actual Astra stream")
    release = tools.load(BASE / "assets_manifest.json")
    for name, digest in release["files"].items():
        if tools.sha(BASE / name) != digest:
            raise ValueError("rejected predecessor changed: " + name)
    policy = proposal["bank_policy"]
    if policy["retain_global_non_repetition"] or not policy["allow_cross_scene_prop_reuse"]:
        raise ValueError("design contradicts explicit familiar-prop reuse decision")
    if not all(isinstance(proposal[k], str) and proposal[k].strip()
               for k in ("system_prompt", "repair_instruction")):
        raise ValueError("actual complete prompt/repair text missing")
    sys.path.insert(0, str(VERSIONS))
    from v6_5.catalog import _normalise_phrase, _plural_phrase
    from v6_5.validation import _SEMANTIC_PHRASE_FAMILIES
    if set(policy["repeatable_phrase_families"]) - _SEMANTIC_PHRASE_FAMILIES.keys():
        raise ValueError("unknown repeatable phrase family in Astra design")
    original_catalog = tools.load(BASE / CATALOG)
    excluded = {"V61-GAM-012", "V61-OFF-001", "V61-STU-001"}
    retained = [dict(entry) for entry in original_catalog["entries"] if entry["id"] not in excluded]
    for entry in retained:
        name = _normalise_phrase(entry["name"])
        concrete = {
            alias for alias in entry["aliases"]
            if re.search(r"\b" + re.escape(_normalise_phrase(alias)) + r"\b", name)
        }
        concrete.update({name, _plural_phrase(name)})
        concrete_name = re.sub(
            r"^(?:(?:small|large|plain|handmade|unbranded|unmarked|closed|simple)\s+)+", "", name,
        )
        concrete.add(concrete_name)
        if re.search(r"\b(?:shelf|shelves|shelving)\b", name):
            concrete.update({"shelf", "shelves", "shelving"})
        concrete.update(_plural_phrase(alias) for alias in list(concrete))
        entry["aliases"] = sorted(concrete)
    lexicon = tools.load(BASE / "prop_lexicon.json")
    phrases = {row["phrase"]: set(row["groups"]) for row in lexicon["entries"]}
    original_guidance = tools.load(BASE / "prop_guidance.json")["entries"]
    guidance = {}
    for row in original_guidance:
        if row["id"] in excluded:
            continue
        instruction = row["instruction"].split("Reserves the bank's paper form")[0]
        instruction = instruction.replace(" and reserves adhesive", "")
        instruction = re.sub(r"Reserves the plate family.*?elsewhere\.\s*", "", instruction)
        guidance[row["id"]] = {**row, "instruction": instruction.strip()}
    old_choices = {
        (e["environment"], e["role"], _normalise_phrase(e["name"]),
         tuple(sorted(e["repetition_groups"]))): e["id"] for e in retained
    }
    new_rows, keys, family_aliases = [], set(), {}
    for family in proposal["catalogue_families"]:
        key, name, groups = family["key"], family["name"], family["repetition_groups"]
        if key in keys or not key or not groups:
            raise ValueError("duplicate or empty family")
        keys.add(key)
        if family["role"] not in {"tabletop_or_movable", "background_furnishing_or_decor"}:
            raise ValueError("new role changes the schema")
        if set(family["training_evidence_ids"]) - {f"T{i:02d}" for i in range(1, 49)}:
            raise ValueError("unknown training evidence citation")
        for alias in [name, *family["aliases"]]:
            phrase = _normalise_phrase(alias)
            for variant in {phrase, _plural_phrase(phrase)}:
                phrases[variant] = set(groups)
        for environment in family["environments"]:
            if environment not in ENV:
                raise ValueError("new environment changes the contract")
            identity = (environment, family["role"], _normalise_phrase(name), tuple(sorted(groups)))
            prop_id = old_choices.get(identity)
            if prop_id is None:
                prop_id = f"V65-TR-{ENV[environment]}-{key}"
                new_rows.append({
                    "candidate_id": prop_id, "environment": environment, "role": family["role"],
                    "name": name, "repetition_groups": ",".join(groups),
                    "status": "Astra training-derived proposal", "runtime_allowed": "true",
                    "review_reason": family["rationale"], "reviewer_decision": "approve",
                    "reviewer_notes": "User-authorized expansion, not individual C-Tech acceptance. " + family["placement_notes"],
                })
                old_choices[identity] = prop_id
            guidance[prop_id] = {"id": prop_id, "instruction": family["placement_notes"],
                                 "reason": family["rationale"]}
            family_aliases[prop_id] = sorted({
                variant for alias in [name, *family["aliases"]]
                for phrase in [_normalise_phrase(alias)]
                for variant in (phrase, _plural_phrase(phrase))
            })
    if not new_rows:
        raise ValueError("no actual catalogue expansion")
    if not refresh_assets:
        shutil.copytree(BASE, DEST, ignore=shutil.ignore_patterns(
            "__pycache__", ".pytest_cache", "*.pyc", "*.pyo", "assets_manifest.json",
        ))
        for path in DEST.rglob("*.py"):
            text = path.read_text().replace("versions.v6_5", "versions.v6_5_training")
            text = text.replace("from v6_5", "from v6_5_training")
            text = text.replace("v6.5-writer-runtime-r1-astra-rich-scenes",
                                "v6.5-writer-runtime-r1-astra-training")
            path.write_text(text)
    (DEST / "system_prompt.md").write_text(proposal["system_prompt"])
    (DEST / "repair_addendum.txt").write_text(proposal["repair_instruction"])
    (DEST / "bank_policy.json").write_text(json.dumps(policy, indent=2) + "\n")
    lexicon["entries"] = [{"phrase": phrase, "groups": sorted(groups)}
                           for phrase, groups in sorted(phrases.items())]
    (DEST / "prop_lexicon.json").write_text(json.dumps(lexicon, ensure_ascii=False, indent=2) + "\n")
    fields = ("candidate_id", "environment", "role", "name", "repetition_groups",
              "status", "runtime_allowed", "review_reason", "reviewer_decision", "reviewer_notes")
    csv_path = DEST / "approved_training_additions.csv"
    with csv_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(new_rows)
    from v6_5_training.catalog import compile_catalog, validate_catalog
    additions = compile_catalog(csv_path, "approved-v6.5-training-20261111-r1")
    for entry in [*retained, *additions["entries"]]:
        if entry["id"] in family_aliases:
            entry["aliases"] = family_aliases[entry["id"]]
    compiled = {
        **additions, "entries": retained + additions["entries"],
        "source_sha256": tools.fingerprint({
            "retained_catalogue_sha256": tools.sha(BASE / CATALOG),
            "actual_astra_proposal_sha256": receipt["proposal_sha256"],
            "new_rows_sha256": tools.sha(csv_path),
        }),
    }
    validate_catalog(compiled)
    (DEST / CATALOG).write_text(json.dumps(compiled, ensure_ascii=False, indent=2) + "\n")
    (DEST / "prop_guidance.json").write_text(json.dumps({
        "version": compiled["version"], "entries": list(guidance.values()),
    }, ensure_ascii=False, indent=2) + "\n")
    registry = tools.load(DEST / "camera_profiles.json")
    registry["version"] = "camera-v6.5-training-20261111-r1-astra"
    registry["limitations"] += " Training-derived styling is offline and cannot certify product coordinates or generated geometry."
    previous_additions = tools.load(HERE.parent / "astra/proposal.json")["camera_additions"]
    for profile in registry["profiles"]:
        profile["people_policy"] = "excluded"
        profile["guidance"] = [note for note in profile["guidance"]
                                if note != previous_additions[profile["framing"]]]
        profile["guidance"].append(proposal["camera_additions"][profile["framing"]])
    (DEST / "camera_profiles.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")
    (DEST / "authoring_provenance.json").write_text(json.dumps({
        "version": "v6.5-training-astra-design-compilation-v1",
        "astra_receipt_path": str(HERE / "astra/receipt.json"),
        "astra_receipt_sha256": tools.sha(HERE / "astra/receipt.json"),
        "astra_proposal_path": str(HERE / "astra/proposal.json"),
        "astra_proposal_sha256": receipt["proposal_sha256"],
        "actual_model": receipt["model_returned"], "reasoning_effort": "medium",
        "current_system_prompt_sha256": tools.sha(DEST / "system_prompt.md"),
        "repair_instruction_sha256": tools.sha(DEST / "repair_addendum.txt"),
        "bank_policy_sha256": tools.sha(DEST / "bank_policy.json"),
        "retained_entries": len(retained), "new_entries": len(new_rows),
        "removed_legacy_ids": sorted(excluded),
        "removal_reason": "Actual Astra excludes plasma electronics and replaces ambiguous one-paper-form scarcity entries with concrete new forms.",
        "alias_policy": "Retained literal form aliases plus actual Astra aliases; broad repetition-group ownership no longer grants form approval.",
        "training_manifest_sha256": tools.sha(HERE / "data/images.json"),
        "rejected_engineering_predecessor_path": str(BASE),
        "rejected_predecessor_asset_manifest_sha256": tools.sha(BASE / "assets_manifest.json"),
        "human_image_acceptance_claimed": False,
    }, indent=2) + "\n")
    print(json.dumps({"installed_unfrozen": str(DEST), "entries": len(compiled["entries"]),
                      "new_entries": len(new_rows), "families": len(keys)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-unfrozen-assets-only", action="store_true")
    main(parser.parse_args().refresh_unfrozen_assets_only)
