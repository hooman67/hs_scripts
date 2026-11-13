#!/usr/bin/env python3
"""Inventory supplied formats for a proposal; never invoke or alter a writer."""

from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import zipfile


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
BACKUP = Path("/home/colligo/hp_lifestyle_source_format_review_20261110")
ROOTS = {
    "old": Path("/mnt/localssd/HP_scenes/smart_brief_and_source_messaging"),
    "new": Path("/mnt/localssd/HP_scenes/new_smart_brief_and_source_messaging"),
}
BASELINE = PROJECT / "research/source_messaging_v1_to_v6/versions/v6_3"


def digest(body):
    return hashlib.sha256(body).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    body = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
    if path.exists() and path.read_bytes() != body:
        raise ValueError(f"refusing to overwrite existing research evidence: {path}")
    path.write_bytes(body)


def leaves(value, pointer=""):
    if isinstance(value, dict):
        for key, child in value.items():
            token = key.replace("~", "~0").replace("/", "~1")
            yield from leaves(child, pointer + "/" + token)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from leaves(child, pointer + "/" + str(index))
    else:
        yield {"path": pointer, "type": type(value).__name__, "value": value}


def shape(value):
    if isinstance(value, dict):
        return {key: shape(child) for key, child in value.items()}
    if isinstance(value, list):
        types = {json.dumps(shape(child), sort_keys=True) for child in value}
        return {"list_length": len(value), "item_shapes": [json.loads(item) for item in sorted(types)]}
    return type(value).__name__


def load_extractor():
    path = PROJECT / "research/dual_source_v5/scripts/extract_inputs.py"
    spec = importlib.util.spec_from_file_location("existing_hp_extractor", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    extractor = load_extractor()
    files, documents, extras = [], [], []

    def document(group, pair, origin, body, parsed):
        rows = list(leaves(parsed))
        strings = [row for row in rows if isinstance(row["value"], str)]
        identity = digest(body)
        destination = BACKUP / "documents" / group / pair / (identity[:16] + ".json")
        write_json(destination, {"origin": origin, "value": parsed, "leaves": rows})
        documents.append({
            "group": group, "pair": pair, "origin": origin, "sha256": identity,
            "document_path": str(destination), "top_keys": list(parsed) if isinstance(parsed, dict) else [],
            "shape": shape(parsed), "leaf_types": dict(Counter(row["type"] for row in rows)),
            "string_characters": sum(len(row["value"]) for row in strings),
            "metadata_characters": sum(len(row["value"]) for row in strings
                                       if "/_chatSession/" in row["path"]),
            "empty_strings": [row["path"] for row in strings if not row["value"].strip()],
            "null_paths": [row["path"] for row in rows if row["value"] is None],
        })

    for group, root in ROOTS.items():
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.name == ".DS_Store":
                continue
            relative = path.relative_to(root)
            body = path.read_bytes()
            destination = BACKUP / "originals" / group / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                if destination.read_bytes() != body:
                    raise ValueError(f"durable copy conflicts: {destination}")
            else:
                shutil.copy2(path, destination)
            if destination.read_bytes() != body:
                raise ValueError(f"copy mismatch: {path}")
            files.append({
                "group": group, "source_path": str(path), "durable_path": str(destination),
                "bytes": len(body), "sha256": digest(body),
            })
            if path.suffix == ".zip":
                with zipfile.ZipFile(destination) as archive:
                    for member in archive.infolist():
                        if member.is_dir() or member.filename.startswith("__MACOSX/"):
                            continue
                        content = archive.read(member)
                        origin = str(path) + "::" + member.filename
                        if member.filename.endswith(".json"):
                            document(group, path.stem, origin, content, json.loads(content))
                        else:
                            extras.append({"origin": origin, "bytes": len(content), "sha256": digest(content)})
            elif path.suffix == ".json":
                document(group, relative.parent.as_posix(), str(path), body, json.loads(body))
            else:
                extracted = extractor.extract_file(destination)
                parsed = extracted.get("json_value")
                if parsed is None:
                    if path.suffix == ".txt":
                        text = extracted["raw_text"]
                    elif path.suffix == ".docx":
                        text = "\n".join(p["text"] for story in extracted["stories"]
                                         for p in story["all_paragraphs_xml_order"])
                    else:
                        text = "\n".join(str(cell["value"]) for sheet in extracted["sheets"]
                                         for cell in sheet["cells"] if cell["value"] is not None)
                    parsed = {"extracted_text": text}
                document(group, relative.parent.as_posix(), str(path), body, parsed)
    duplicates = defaultdict(list)
    for item in documents:
        duplicates[item["sha256"]].append(item["origin"])
    baseline = {
        str(path.relative_to(BASELINE)): digest(path.read_bytes())
        for path in sorted(BASELINE.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }
    manifest = {
        "as_of_date": datetime.now(timezone.utc).date().isoformat(),
        "scope": "read-only format/content analysis and proposal; no runtime changes or model calls",
        "files": files, "documents": documents, "extra_archive_members": extras,
        "exact_document_duplicate_groups": [origins for origins in duplicates.values() if len(origins) > 1],
        "v63_baseline_sha256": baseline,
        "restore": "Copy a manifest-listed durable original to its source_path only after checking SHA256; "
                   "archives retain original member names and bytes.",
    }
    write_json(HERE / "data/source_manifest.json", manifest)
    write_json(BACKUP / "source_manifest.json", manifest)
    print(json.dumps({
        "files": len(files), "documents": len(documents), "new_json_documents": sum(
            item["group"] == "new" for item in documents),
        "extra_archive_members": extras, "exact_duplicate_groups": manifest["exact_document_duplicate_groups"],
        "durable_backup": str(BACKUP), "v63_files_frozen": len(baseline),
    }, indent=2))


if __name__ == "__main__":
    main()
