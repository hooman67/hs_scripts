#!/usr/bin/env python3
"""Deterministic, coverage-oriented 160-to-30 selection and exact-rank pairing."""

import argparse
import copy
import hashlib
import itertools
import json
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

ALGORITHM_VERSION = "hp-approved-props-160-to30-v1"
TARGET_SIZE = 30
SOURCE_SIZE = 160
TARGET_PROPORTION = TARGET_SIZE / SOURCE_SIZE
RESTARTS = 12
MAX_PASSES = 12
WEIGHTS = {
    "environment": 6,
    "device_environment": 2,
    "reference": 2,
    "source_relationship": 3,
    "source_score_band": 1,
    "reference_score_band": 1,
    "prop_count": 2,
    "approved_prop": 1,
    "creative_departure": 1,
    "rank": 0.5,
    "bank_environment": 1,
}
CAVEAT = (
    "Deterministic coverage heuristic, not an optimality guarantee or a probability "
    "sample. Exact device/view/rank matching is not semantic or environment equivalence."
)


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _canonical_sha(data):
    return _sha(
        json.dumps(
            data, sort_keys=True, ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
    )


def _string(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")
    return value


def _hash(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError(f"{label} must be a lowercase SHA-256 hex digest")
    return value


def _snapshot(data):
    # The real r5 V6.2 export stores its snapshot in provenance, not at root.
    if "snapshot_manifest_path" in data or "snapshot_manifest_sha256" in data:
        path = data.get("snapshot_manifest_path")
        sha = data.get("snapshot_manifest_sha256")
        origin = "root"
    else:
        provenance = data.get("provenance", {})
        snapshot = (
            provenance.get("validation_snapshot", {})
            if isinstance(provenance, dict)
            else {}
        )
        if not isinstance(snapshot, dict):
            raise ValueError("provenance.validation_snapshot must be an object")
        path = snapshot.get("manifest_path")
        sha = snapshot.get("manifest_sha256")
        origin = "provenance.validation_snapshot"
    return {
        "snapshot_manifest_path": _string(path, "snapshot_manifest_path"),
        "snapshot_manifest_sha256": _hash(sha, "snapshot_manifest_sha256"),
        "metadata_location": origin,
    }


def _bank(row):
    return row["device_id"], row["camera_tag"]


def _key(row):
    return (*_bank(row), row["bank_rank"])


def _quota_map(banks):
    devices = sorted({device for device, _ in banks})
    singles = {
        min(bank for bank in banks if bank[0] == device) for device in devices[:2]
    }
    return {bank: 1 if bank in singles else 2 for bank in sorted(banks)}


def _quota_json(quotas):
    result = {}
    for (device, camera), count in sorted(quotas.items()):
        result.setdefault(device, {})[camera] = count
    return result


def _validate_document(data, *, full=True):
    if not isinstance(data, dict):
        raise ValueError("document must be an object")
    for field in ("version", "selection_rule"):
        _string(data.get(field), field)
    _snapshot(data)
    counts = data.get("counts")
    expected_counts = {
        "devices": 4,
        "views_per_device": 4,
        "banks": 16,
        "prompts": SOURCE_SIZE if full else TARGET_SIZE,
    }
    if full:
        expected_counts["candidates_per_bank"] = 10
    if not isinstance(counts, dict) or any(
        type(counts.get(k)) is not int or counts[k] != v
        for k, v in expected_counts.items()
    ):
        raise ValueError(f"counts must declare {expected_counts}")
    rows = data.get("prompts")
    if not isinstance(rows, list) or len(rows) != expected_counts["prompts"]:
        raise ValueError(f"prompts must contain {expected_counts['prompts']} records")
    banks = defaultdict(list)
    prompt_keys = set()
    pair_keys = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each prompt must be an object")
        for field in (
            "prompt_key",
            "device_id",
            "camera_tag",
            "text",
            "environment",
            "relationship",
            "ctech_reference_id",
        ):
            _string(row.get(field), field)
        if row["prompt_key"] in prompt_keys:
            raise ValueError(f"duplicate prompt_key: {row['prompt_key']}")
        prompt_keys.add(row["prompt_key"])
        rank = row.get("bank_rank")
        if type(rank) is not int or not 1 <= rank <= 10:
            raise ValueError("bank_rank must be an integer in 1..10")
        if _key(row) in pair_keys:
            raise ValueError(f"duplicate bank_rank: {_key(row)}")
        pair_keys.add(_key(row))
        if _hash(row.get("text_sha256"), "text_sha256") != _sha(
            row["text"].encode("utf-8")
        ):
            raise ValueError(f"text_sha256 mismatch: {row['prompt_key']}")
        for field in ("source_relevance_score", "ctech_reference_score"):
            score = row.get(field)
            if (
                type(score) not in (int, float)
                or not 0 <= score <= 100
                or not math.isfinite(score)
            ):
                raise ValueError(f"{field} must be finite and in 0..100")
        for field in ("prop_ids", "creative_departures"):
            values = row.get(field)
            if not isinstance(values, list) or any(
                not isinstance(value, str) for value in values
            ):
                raise ValueError(f"{field} must be a string list")
            if field == "prop_ids" and len(set(values)) != len(values):
                raise ValueError("prop_ids must not contain duplicates")
        banks[_bank(row)].append(row)
    devices = {device for device, _ in banks}
    if len(devices) != 4 or len(banks) != 16 or any(
        sum(bank[0] == device for bank in banks) != 4 for device in devices
    ):
        raise ValueError("expected four devices, four views each, sixteen banks")
    mapping = data.get("device_source_mapping")
    if (
        not isinstance(mapping, list)
        or len(mapping) != 4
        or any(not isinstance(item, dict) for item in mapping)
        or any(not isinstance(item.get("device_id"), str) for item in mapping)
        or {item["device_id"] for item in mapping} != devices
    ):
        raise ValueError("device_source_mapping must contain each of four devices")
    for bank, records in banks.items():
        ranks = {row["bank_rank"] for row in records}
        if full and (len(records) != 10 or ranks != set(range(1, 11))):
            raise ValueError(f"missing bank_rank: {bank} must contain ranks 1..10")
    if not full:
        quotas = _quota_map(banks)
        if any(len(records) != quotas[bank] for bank, records in banks.items()):
            raise ValueError("selected records do not satisfy the fixed 30 quotas")
        selection = data.get("selection")
        if not isinstance(selection, dict):
            raise ValueError("selected document requires selection metadata")
        if selection.get("bank_quotas") != _quota_json(quotas):
            raise ValueError("selected bank_quotas do not match selected records")
        _hash(selection.get("source_document_sha256"), "source_document_sha256")
        if type(selection.get("seed")) is not int:
            raise ValueError("selected document requires an integer seed")
    return {
        bank: sorted(records, key=lambda row: row["bank_rank"])
        for bank, records in sorted(banks.items())
    }


def _features(row):
    device, camera = _bank(row)
    environment = row["environment"]
    result = Counter(
        {
            ("environment", environment): 1,
            ("device_environment", device, environment): 1,
            ("reference", row["ctech_reference_id"]): 1,
            ("source_relationship", row["relationship"]): 1,
            ("source_score_band", int(row["source_relevance_score"] // 10)): 1,
            ("reference_score_band", int(row["ctech_reference_score"] // 5)): 1,
            ("prop_count", len(row["prop_ids"])): 1,
            ("creative_departure", bool(row["creative_departures"])): 1,
            ("rank", row["bank_rank"]): 1,
            ("bank_environment", device, camera, environment): 1,
        }
    )
    result.update(("approved_prop", prop) for prop in row["prop_ids"])
    return result


def _option(rows):
    features = Counter()
    for row in rows:
        features.update(_features(row))
    similarity = 0.0
    for left, right in itertools.combinations(rows, 2):
        a = set(re.findall(r"\b\w+\b", left["text"].lower()))
        b = set(re.findall(r"\b\w+\b", right["text"].lower()))
        similarity += len(a & b) / len(a | b) if a | b else 1.0
    return {
        "rows": rows,
        "features": features,
        "texts": Counter(row["text"] for row in rows),
        "similarity": similarity,
    }


def _objective(options, targets, bank_count):
    counts = Counter()
    texts = Counter()
    for option in options:
        counts.update(option["features"])
        texts.update(option["texts"])
    deviation = math.fsum(
        WEIGHTS[key[0]] * abs(counts[key] - target)
        for key, target in sorted(targets.items())
    ) / TARGET_SIZE
    similarity = math.fsum(option["similarity"] for option in options) / bank_count
    duplicates = sum(max(0, count - 1) for count in texts.values())
    missing = sum(
        not counts[key] for key in targets if key[0] == "environment"
    )
    return {
        "weighted_absolute_deviation_divided_by_30": deviation,
        "within_bank_jaccard_divided_by_16": similarity,
        "duplicate_texts": duplicates,
        "missing_environments": missing,
        "total": deviation + similarity + 1000 * duplicates + missing,
    }, counts, texts


def _delta(old, new, counts, texts, targets, bank_count):
    feature_keys = sorted(old["features"].keys() | new["features"].keys())
    changes = {
        key: new["features"][key] - old["features"][key] for key in feature_keys
    }
    deviation = math.fsum(
        WEIGHTS[key[0]]
        * (
            abs(counts[key] + changes[key] - targets[key])
            - abs(counts[key] - targets[key])
        )
        for key in feature_keys
    ) / TARGET_SIZE
    missing = sum(
        int(counts[key] + changes[key] == 0) - int(counts[key] == 0)
        for key in feature_keys
        if key[0] == "environment"
    )
    duplicates = sum(
        max(0, texts[text] + new["texts"][text] - old["texts"][text] - 1)
        - max(0, texts[text] - 1)
        for text in sorted(old["texts"].keys() | new["texts"].keys())
    )
    return (
        deviation
        + (new["similarity"] - old["similarity"]) / bank_count
        + 1000 * duplicates
        + missing
    )


def _selected_document(data, rows, selection):
    result = copy.deepcopy(data)
    result["prompts"] = copy.deepcopy(rows)
    result["counts"] = {
        "devices": 4,
        "views_per_device": 4,
        "banks": 16,
        "prompts": TARGET_SIZE,
        "selected_per_bank_min": 1,
        "selected_per_bank_max": 2,
    }
    result["selection_rule"] = selection["method"]
    result["selection"] = {
        "algorithm_version": ALGORITHM_VERSION,
        "target_proportion": TARGET_PROPORTION,
        "source_document_sha256": _canonical_sha(data),
        "source_hash_kind": "canonical-json-sha256",
        "source_counts": copy.deepcopy(data["counts"]),
        "source_selection_rule": data["selection_rule"],
        "source_snapshot": _snapshot(data),
        "caveat": CAVEAT,
        **selection,
    }
    return result


def select_prompts(data, seed=42):
    """Return a selected 30-record document; do not mutate data or access models."""
    if type(seed) is not int:
        raise ValueError("seed must be an integer")
    banks = _validate_document(data)
    quotas = _quota_map(banks)
    options = [
        [_option(rows) for rows in itertools.combinations(banks[bank], quotas[bank])]
        for bank in banks
    ]
    full_counts = Counter()
    for bank in banks:
        for row in banks[bank]:
            full_counts.update(_features(row))
    targets = {
        key: count * TARGET_PROPORTION for key, count in sorted(full_counts.items())
    }
    rng = random.Random(seed)
    best = None
    passes_run = []
    for restart in range(RESTARTS):
        state = [
            0 if restart == 0 else rng.randrange(len(bank_options))
            for bank_options in options
        ]
        current = [bank_options[index] for bank_options, index in zip(options, state)]
        _, counts, texts = _objective(current, targets, len(banks))
        for pass_index in range(MAX_PASSES):
            changed = False
            for bank_index, bank_options in enumerate(options):
                old_index = state[bank_index]
                old = bank_options[old_index]
                best_index, best_delta = old_index, 0.0
                for index, option in enumerate(bank_options):
                    delta = _delta(old, option, counts, texts, targets, len(banks))
                    if delta < best_delta - 1e-12:
                        best_index, best_delta = index, delta
                if best_index != old_index:
                    new = bank_options[best_index]
                    counts.subtract(old["features"])
                    counts.update(new["features"])
                    texts.subtract(old["texts"])
                    texts.update(new["texts"])
                    state[bank_index] = best_index
                    changed = True
            if not changed:
                break
        passes_run.append(pass_index + 1)
        current = [bank_options[index] for bank_options, index in zip(options, state)]
        objective, _, _ = _objective(current, targets, len(banks))
        candidate = (objective["total"], tuple(state))
        if best is None or candidate < best[0]:
            best = candidate, current, objective
    _, chosen, objective = best
    rows = [row for option in chosen for row in option["rows"]]
    selection = {
        "method": "coverage-weighted coordinate descent on V6.3 only",
        "seed": seed,
        "restarts": RESTARTS,
        "max_passes": MAX_PASSES,
        "passes_per_restart": passes_run,
        "bank_quotas": _quota_json(quotas),
        "quota_rule": (
            "Singleton at lexicographically first camera in each of the first "
            "two sorted devices; all other banks contribute two."
        ),
        "feature_weights": WEIGHTS.copy(),
        "objective": objective,
    }
    return _selected_document(data, rows, selection)


def match_baseline(selected, baseline):
    """Copy V6.2 records matching exact V6.3 (device_id, camera_tag, bank_rank)."""
    selected_banks = _validate_document(selected, full=False)
    baseline_banks = _validate_document(baseline)
    if set(selected_banks) != set(baseline_banks):
        raise ValueError("V6.3 and baseline device/view bank keys must match exactly")
    index = {_key(row): row for row in baseline["prompts"]}
    rows = [index[_key(row)] for row in selected["prompts"]]
    return _selected_document(
        baseline,
        rows,
        {
            "method": "exact V6.3 (device_id, camera_tag, bank_rank) matching only",
            "seed": selected["selection"]["seed"],
            "bank_quotas": copy.deepcopy(selected["selection"]["bank_quotas"]),
            "matched_v6_3_source_document_sha256": selected["selection"][
                "source_document_sha256"
            ],
            "matched_v6_3_selection_sha256": _canonical_sha(selected),
        },
    )


def _distribution(rows):
    def counts(field):
        return dict(sorted(Counter(row[field] for row in rows).items()))

    return {
        "prompts": len(rows),
        "devices": counts("device_id"),
        "banks": _quota_json(Counter(_bank(row) for row in rows)),
        "environments": counts("environment"),
        "references": counts("ctech_reference_id"),
        "source_relationships": counts("relationship"),
        "prop_ids": dict(
            sorted(Counter(prop for row in rows for prop in row["prop_ids"]).items())
        ),
        "source_relevance_score_mean": math.fsum(
            row["source_relevance_score"] for row in rows
        ) / len(rows),
        "ctech_reference_score_mean": math.fsum(
            row["ctech_reference_score"] for row in rows
        ) / len(rows),
    }


def _coverage(source, selected):
    result = {}
    for name in ("environments", "prop_ids", "references"):
        available = set(source[name])
        present = set(selected[name])
        result[name] = {
            "source_unique": len(available),
            "selected_unique": len(present),
            "fraction_covered": len(present) / len(available) if available else None,
            "missing": sorted(available - present),
        }
    return result


def _read_input(path):
    path = path.resolve(strict=True)
    raw = path.read_bytes()
    data = json.loads(raw)
    _validate_document(data)
    snapshot = _snapshot(data)
    manifest = Path(snapshot["snapshot_manifest_path"])
    if not manifest.is_absolute():
        manifest = path.parent / manifest
    manifest = manifest.resolve(strict=True)
    if _sha(manifest.read_bytes()) != snapshot["snapshot_manifest_sha256"]:
        raise ValueError(f"snapshot manifest hash mismatch: {manifest}")
    return data, {
        "path": str(path),
        "sha256": _sha(raw),
        "canonical_json_sha256": _canonical_sha(data),
        "snapshot": {**snapshot, "verified_manifest_path": str(manifest)},
    }


def _text_export(data):
    return "".join(
        f"[{row['prompt_key']}] device={row['device_id']} "
        f"camera={row['camera_tag']} rank={row['bank_rank']} "
        f"environment={row['environment']}\n{row['text']}\n\n"
        for row in data["prompts"]
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="160-record V6.3 JSON")
    parser.add_argument(
        "--baseline", type=Path, required=True, help="160-record V6.2 JSON"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="new directory only; existing paths are rejected",
    )
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)
    try:
        if args.output_dir.exists() or args.output_dir.is_symlink():
            raise ValueError("--output-dir must be a new path")
        v63, source63 = _read_input(args.input)
        v62, source62 = _read_input(args.baseline)
        if source63["path"] == source62["path"]:
            raise ValueError("V6.3 input and V6.2 baseline must be different files")
        selected63 = select_prompts(v63, seed=args.seed)
        selected62 = match_baseline(selected63, v62)
        selected63["selection"]["source_file_sha256"] = source63["sha256"]
        selected62["selection"]["source_file_sha256"] = source62["sha256"]
        selected62["selection"]["matched_v6_3_selection_sha256"] = _canonical_sha(
            selected63
        )
        if [_key(row) for row in selected63["prompts"]] != [
            _key(row) for row in selected62["prompts"]
        ]:
            raise ValueError("selected V6.3/V6.2 pair keys are not identical")
        report = {
            **copy.deepcopy(selected63["selection"]),
            "sources": {"v6_3": source63, "v6_2": source62},
            "distributions": {},
            "coverage": {},
            "pair_keys": [list(_key(row)) for row in selected63["prompts"]],
        }
        for name, source, selected in (
            ("v6_3", v63, selected63), ("v6_2", v62, selected62)
        ):
            full = _distribution(source["prompts"])
            subset = _distribution(selected["prompts"])
            report["distributions"][name] = {"all_160": full, "selected_30": subset}
            report["coverage"][name] = _coverage(full, subset)
        outputs = {
            "selected_v6_3_30.json": selected63,
            "selected_v6_2_30.json": selected62,
            "selection_report.json": report,
        }
        serialized = {
            name: json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
            for name, data in outputs.items()
        }
        serialized["selected_v6_3_30.txt"] = _text_export(selected63)
        serialized["selected_v6_2_30.txt"] = _text_export(selected62)
        report["output_sha256"] = {
            name: _sha(text.encode("utf-8"))
            for name, text in serialized.items()
            if name != "selection_report.json"
        }
        serialized["selection_report.json"] = json.dumps(
            report, ensure_ascii=False, indent=2, allow_nan=False
        ) + "\n"
        for source in (source63, source62):
            if _sha(Path(source["path"]).read_bytes()) != source["sha256"]:
                raise ValueError(f"input changed during selection: {source['path']}")
            snapshot = source["snapshot"]
            if _sha(Path(snapshot["verified_manifest_path"]).read_bytes()) != snapshot[
                "snapshot_manifest_sha256"
            ]:
                raise ValueError("snapshot manifest changed during selection")
        args.output_dir.mkdir(parents=True, exist_ok=False)
        for name, text in serialized.items():
            with (args.output_dir / name).open("x", encoding="utf-8") as handle:
                handle.write(text)
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, f"selection failed: {exc}\n")
    print(f"Wrote five exclusive-create outputs to {args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
