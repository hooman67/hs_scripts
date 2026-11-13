from __future__ import annotations

import ast
import json
import subprocess

from common import require, sha256_file
from config import PACKAGE, PIPELINE_VERSION, PR_COMMIT, PROMPTS, PROMPTS_SHA256, RECORDS, SOURCE_HASHES, WORKTREE


def verify() -> dict:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=WORKTREE, text=True).strip()
    require(commit == PR_COMMIT, f"PR worktree moved: {commit}")
    actual = {name: sha256_file(PACKAGE / name) for name in SOURCE_HASHES}
    require(actual == SOURCE_HASHES, "PR 4403 source hashes changed")
    require(sha256_file(PROMPTS) == PROMPTS_SHA256, "V6.1 prompt export changed")
    records = list(RECORDS.glob("*.json"))
    require(len(records) == 160, f"expected 160 frozen controls, found {len(records)}")
    document = json.loads(PROMPTS.read_text())
    require(len(document.get("prompts", [])) == 160, "expected 160 exported prompts")
    tree = ast.parse((PACKAGE / "hp3p/pipeline.py").read_text())
    version = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "PIPELINE_VERSION" for target in node.targets):
            version = ast.literal_eval(node.value)
            break
    require(version == PIPELINE_VERSION, f"pipeline version differs: {version}")
    return {"pr_commit": commit, "pipeline_version": version, "records": len(records)}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
