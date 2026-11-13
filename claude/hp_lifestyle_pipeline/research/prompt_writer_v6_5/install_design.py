#!/usr/bin/env python3
"""Compile the received Astra design into an isolated, unfrozen V6.5 candidate."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
VERSIONS = PROJECT / "research/source_messaging_v1_to_v6/versions"
BASE = VERSIONS / "v6_4"
DEST = VERSIONS / "v6_5"
CATALOGUE_NAME = "approved-v6.5-20261111.catalog.json"
CATALOGUE_VERSION = "hp-v6.5-approved-props-v1"
REVISION = "approved-v6.5-20261111-r1-astra-rich-scenes"
ENV_CODES = {
    "Home": "HOM", "Office": "OFF", "Education": "EDU", "Gaming": "GAM",
    "Café": "CAF", "Creative Studio": "STU",
}
ROLES = {"tabletop_or_movable", "background_furnishing_or_decor"}
CSV_FIELDS = (
    "candidate_id", "environment", "role", "name", "repetition_groups", "status",
    "runtime_allowed", "review_reason", "reviewer_decision", "reviewer_notes",
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def received_design():
    spec = importlib.util.spec_from_file_location("v65_consultation_replay", HERE / "consult_astra.py")
    if spec is None or spec.loader is None:
        raise ValueError("Astra replay collector unavailable")
    replay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(replay)
    receipt = load(HERE / "astra/receipt.json")
    if not receipt["ok"] or receipt["semantic_resampling"]:
        raise ValueError("consultation did not complete under its authorized contract")
    if sha(receipt["frames_path"]) != receipt["frames_sha256"]:
        raise ValueError("Astra raw response stream changed")
    if sha(HERE / "astra/proposal.json") != receipt["proposal_sha256"]:
        raise ValueError("Astra proposal changed")
    collector = replay.Collector()
    for line in Path(receipt["frames_path"]).read_text().splitlines():
        collector.feed(json.loads(line))
    proposal = load(HERE / "astra/proposal.json")
    if collector.result() != proposal:
        raise ValueError("Astra design does not equal the raw semantic response")
    return proposal, receipt


def main():
    if DEST.exists():
        raise FileExistsError("V6.5 candidate already exists; never overwrite or silently refreeze it")
    proposal, receipt = received_design()
    if proposal["bank_policy"].get("retain_global_non_repetition") is not True:
        raise PermissionError("Astra proposed changing bank non-repetition; inspect and obtain a specific decision")
    base_release = load(BASE / "assets_manifest.json")
    for name, digest in base_release["files"].items():
        if sha(BASE / name) != digest:
            raise ValueError(f"frozen V6.4 predecessor changed: {name}")
    prompt = (BASE / "system_prompt.md").read_text()
    if not isinstance(proposal["prompt_patches"], list) or not proposal["prompt_patches"]:
        raise ValueError("Astra did not supply executable prompt patches")
    for patch in proposal["prompt_patches"]:
        if set(patch) != {"old", "new"} or not all(isinstance(patch[k], str) for k in ("old", "new")):
            raise ValueError("Astra prompt patch is malformed")
        if not patch["old"] or prompt.count(patch["old"]) != 1:
            raise ValueError("Astra prompt patch does not uniquely match its frozen source")
        prompt = prompt.replace(patch["old"], patch["new"], 1)
    if not isinstance(proposal["repair_addendum"], str) or not proposal["repair_addendum"].strip():
        raise ValueError("Astra repair addendum missing")
    additions = proposal["camera_additions"]
    if set(additions) != {"tight", "medium", "wide"} or any(
        not isinstance(value, str) or not value.strip() for value in additions.values()
    ):
        raise ValueError("Astra camera additions must be three qualitative strings")
    families = proposal["catalogue_families"]
    if not isinstance(families, list) or not families:
        raise ValueError("Astra catalogue expansion missing")

    sys.path.insert(0, str(VERSIONS))
    from v6_4.catalog import _normalise_phrase, _plural_phrase

    base_catalogue = load(BASE / "approved-v6.3-20261109.catalog.json")
    lexicon = load(BASE / "prop_lexicon.json")
    phrase_groups = {}
    for entry in lexicon["entries"]:
        phrase = _normalise_phrase(entry["phrase"])
        phrase_groups.setdefault(phrase, set()).update(entry["groups"])
    existing_groups = {group for groups in phrase_groups.values() for group in groups}
    lexicon_new = []
    new_rows = []
    usage_guidance = []
    family_keys = set()
    existing_entries = {
        (entry["environment"], entry["role"], _normalise_phrase(entry["name"]),
         tuple(sorted(entry["repetition_groups"])))
        for entry in base_catalogue["entries"]
    }
    skipped = []
    for family in families:
        key = family["key"]
        if not isinstance(key, str) or not key or key in family_keys:
            raise ValueError("Astra catalogue family identity missing or duplicated")
        family_keys.add(key)
        name, role, groups = family["name"], family["role"], family["repetition_groups"]
        environments, aliases = family["environments"], family["aliases"]
        if (
            not isinstance(name, str) or not name.strip() or role not in ROLES
            or not isinstance(groups, list) or not groups
            or len(groups) != len(set(groups))
            or not isinstance(environments, list) or not environments
            or len(environments) != len(set(environments))
            or any(env not in ENV_CODES for env in environments)
            or not isinstance(aliases, list)
            or any(not isinstance(alias, str) or not alias.strip() for alias in aliases)
        ):
            raise ValueError(f"malformed Astra catalogue family: {key}")
        for alias in [name, *aliases]:
            phrase = _normalise_phrase(alias)
            previous = phrase_groups.get(phrase, set())
            if previous and not previous.issubset(groups):
                raise ValueError(f"Astra alias splits an existing visual family: {phrase}")
            for variant in {phrase, _plural_phrase(phrase)}:
                lexicon_new.append({"phrase": variant, "groups": groups})
        for group in groups:
            if group not in existing_groups:
                phrase = group.replace("_", " ")
                for variant in {phrase, _plural_phrase(phrase)}:
                    lexicon_new.append({"phrase": variant, "groups": [group]})
        for environment in environments:
            identity = (environment, role, _normalise_phrase(name), tuple(sorted(groups)))
            if identity in existing_entries:
                skipped.append({"family": key, "environment": environment, "reason": "exact choice already approved"})
                continue
            existing_entries.add(identity)
            candidate_id = f"V65-{ENV_CODES[environment]}-{key}"
            new_rows.append({
                "candidate_id": candidate_id,
                "environment": environment, "role": role, "name": name,
                "repetition_groups": ",".join(groups), "status": "Astra proposal",
                "runtime_allowed": "true", "review_reason": family["rationale"],
                "reviewer_decision": "approve",
                "reviewer_notes": (
                    "User-authorized V6.5 catalogue expansion, authored by Astra; not individual C-Tech acceptance. "
                    + family["placement_notes"]
                ),
            })
            usage_guidance.append({
                "id": candidate_id, "instruction": family["placement_notes"],
                "reason": family["rationale"],
            })
    if not new_rows:
        raise ValueError("Astra expansion produces no new approved choices")
    for item in lexicon_new:
        phrase_groups.setdefault(item["phrase"], set()).update(item["groups"])
    lexicon["version"] = CATALOGUE_VERSION
    lexicon["entries"] = [
        {"phrase": phrase, "groups": sorted(groups)}
        for phrase, groups in sorted(phrase_groups.items())
    ]

    shutil.copytree(BASE, DEST, ignore=shutil.ignore_patterns(
        "__pycache__", ".pytest_cache", "*.pyc", "*.pyo", "assets_manifest.json",
    ))
    old_catalogue = DEST / "approved-v6.3-20261109.catalog.json"
    old_catalogue.rename(DEST / CATALOGUE_NAME)
    for path in sorted(DEST.rglob("*.py")):
        text = path.read_text()
        text = text.replace("versions.v6_4", "versions.v6_5")
        text = text.replace("from v6_4", "from v6_5")
        text = text.replace("hp_lifestyle_v6_4", "hp_lifestyle_v6_5")
        text = text.replace("hp-v6.3-approved-props-v1", CATALOGUE_VERSION)
        text = text.replace("approved-v6.3-20261109.catalog.json", CATALOGUE_NAME)
        text = text.replace(
            "v6.4-writer-runtime-r1-structured-sources", "v6.5-writer-runtime-r1-astra-rich-scenes"
        )
        path.write_text(text)
    (DEST / "system_prompt.md").write_text(prompt)
    (DEST / "repair_addendum.txt").write_text(proposal["repair_addendum"])
    write_json(DEST / "prop_lexicon.json", lexicon)
    write_json(DEST / "prop_guidance.json", {
        "version": CATALOGUE_VERSION, "entries": usage_guidance,
    })
    registry = load(DEST / "camera_profiles.json")
    registry["version"] = "camera-v6.5-qualitative-20261111-r1-astra"
    registry["limitations"] += " V6.5 additions are Astra-authored offline composition guidance, not runtime product-coordinate or visibility measurement."
    for profile in registry["profiles"]:
        profile["guidance"].append(additions[profile["framing"]])
    write_json(DEST / "camera_profiles.json", registry)
    rows = [{
        "candidate_id": entry["id"], "environment": entry["environment"],
        "role": entry["role"], "name": entry["name"],
        "repetition_groups": ",".join(entry["repetition_groups"]),
        "status": "retained V6.4 approval", "runtime_allowed": "true",
        "review_reason": "Previously approved V6.4 catalogue choice, retained unchanged.",
        "reviewer_decision": "approve", "reviewer_notes": "Predecessor catalogue SHA256 " + sha(BASE / "approved-v6.3-20261109.catalog.json"),
    } for entry in base_catalogue["entries"]]
    csv_path = DEST / "approved_additions.csv"
    with csv_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows([*rows, *new_rows])
    from v6_5.catalog import compile_catalog, validate_catalog

    compiled = compile_catalog(csv_path, REVISION)
    # Retained entries preserve their exact reviewed aliases; only new rows use
    # aliases compiled from the expanded lexicon.
    compiled["entries"] = base_catalogue["entries"] + compiled["entries"][len(rows):]
    validate_catalog(compiled)
    write_json(DEST / CATALOGUE_NAME, compiled)
    write_json(DEST / "baseline_manifest.json", {
        "version": "v6.4-predecessor-for-v6.5", "root": str(BASE),
        "assets_manifest_sha256": sha(BASE / "assets_manifest.json"),
        "files": base_release["files"],
    })
    write_json(DEST / "authoring_provenance.json", {
        "version": "v6.5-astra-design-compilation-v1",
        "astra_receipt_path": str(HERE / "astra/receipt.json"),
        "astra_receipt_sha256": sha(HERE / "astra/receipt.json"),
        "astra_proposal_path": str(HERE / "astra/proposal.json"),
        "astra_proposal_sha256": sha(HERE / "astra/proposal.json"),
        "actual_model": receipt["model_returned"],
        "current_system_prompt_sha256": sha(DEST / "system_prompt.md"),
        "new_family_count": len(families), "new_entry_count": len(new_rows),
        "retained_entry_count": len(rows), "skipped_duplicate_choices": skipped,
        "camera_profile_count": len(registry["profiles"]),
        "policy_text_author": "Astra", "compiler_author": "parent engineering session",
        "catalogue_approval_basis": "explicit user authorization of realistic V6.5 catalogue expansion",
        "human_image_acceptance_claimed": False,
    })
    print(json.dumps({
        "candidate_created": str(DEST), "new_entries": len(new_rows),
        "approved_entries": len(compiled["entries"]),
        "distinct_groups": len({g for e in compiled["entries"] for g in e["repetition_groups"]}),
        "not_yet_frozen_or_runtime_validated": True,
    }), flush=True)


if __name__ == "__main__":
    main()
