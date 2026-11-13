"""Create a checksum inventory of the durable local research evidence bundle."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "source_manifest.json"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    files = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path == TARGET or "__pycache__" in path.parts:
            continue
        files.append({"path": str(path), "relative_path": str(path.relative_to(ROOT)),
                      "bytes": path.stat().st_size, "sha256": sha256(path)})
    result = {"created_at": datetime.now(timezone.utc).isoformat(), "root": str(ROOT),
              "storage": "Resolved checkout under /home/colligo, backed-up location per user policy; not an independent off-host restoration test.",
              "source_metadata": ["data/primary_review/*.json", "data/materials_batteries/findings.json",
                                  "data/aerospace_services/findings.json", "data/infrastructure_finance/evidence.json",
                                  "data/interview/recovery_status.json"],
              "limitations": "Original PDFs/audio/HTML/XML are ignored by Git but retained at the listed home paths; committed text and metadata are the smaller recovery bundle. This manifest excludes itself and Python caches.",
              "files": files}
    TARGET.write_text(json.dumps(result, indent=2) + "\n")
    assert all(Path(f["path"]).stat().st_size == f["bytes"] and sha256(Path(f["path"])) == f["sha256"] for f in files)
    print(json.dumps({"manifest": str(TARGET), "verified_files": len(files),
                      "bytes": sum(f["bytes"] for f in files)}))


if __name__ == "__main__":
    main()
