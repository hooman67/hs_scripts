#!/usr/bin/env python3
"""Four-fixture controlled smoke for the PR4349 translation-only prompt experiment.

The control guide and output come from the frozen V6.1 endpoint run. The treatment
invokes the exact isolated PR4349 ``hp3p.pipeline.run_row`` code, while replaying the
control selection, Stage-A geometry and guide. Replaying the guide holds the actual
GPT Image input image constant and isolates the Stage-B/final prompt policy. There is
one Astra writing call and one GPT Image call per fixture, with no API retries.
"""

from __future__ import annotations

import base64
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path

import foundry_aws_gateway.llm

WORKTREE = Path("/home/colligo/foundry-pr4349-position-exp")
PACKAGE = WORKTREE / "experimental/adarabi/hp-3p-gpt25"
PROJECT = Path("/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/judge/pipeline_position_experiment")
BASELINE = PROJECT / "smoke/baseline"
TREATMENT = PROJECT / "smoke/treatment"
PR_COMMIT = "8c358bc7989cb0e137e89db0fd325168249e2a22"
FIXTURES = (
    "cashmere__laptop_FrontCloseUp__p1",
    "cashmere__laptop_FrontWide__p1",
    "magic__printer_FrontCloseUp__p1",
    "magic__printer_FrontWide__p1",
)

sys.path.insert(0, str(PACKAGE))

from hp3p.catalog import StyleRef  # noqa: E402
from hp3p.evalset import Row  # noqa: E402
import hp3p.pipeline as pipeline  # noqa: E402
from hp3p.openai_client import IMAGE_MODEL, TEXT_MODEL  # noqa: E402


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    return sha(path.read_bytes())


class FrozenInputsClient:
    """Replay selection/geometry; call Direct OpenAI only for treatment writing/image."""

    def __init__(self, debug: dict, expected_guide: bytes, audit_dir: Path):
        self.debug = debug
        self.expected_guide = expected_guide
        self.audit_dir = audit_dir
        self.client = foundry_aws_gateway.llm.get_openai().with_options(max_retries=0, timeout=600.0)
        self.calls: list[dict] = []

    def chat_json(self, system: str, text: str, images: list[tuple[str, bytes]], schema: dict) -> dict:
        fields = set(schema["properties"])
        if fields == {"tone", "content", "rationale"}:
            self.calls.append({"kind": "selection_replay"})
            return dict(self.debug["selection"])
        if "geometry" in fields:
            self.calls.append({"kind": "geometry_replay"})
            return dict(self.debug["geometryResponse"])
        if fields != {"layout", "camera", "composition", "prompt"}:
            raise RuntimeError(f"Unexpected schema fields: {sorted(fields)}")
        if not images or images[0][1] != self.expected_guide:
            raise RuntimeError("Treatment Stage B did not receive the byte-identical frozen control guide")
        content = [{"type": "text", "text": text}] + [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime};base64,{base64.b64encode(data).decode()}",
                    "detail": "high",
                },
            }
            for mime, data in images
        ]
        response = self.client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[{"role": "developer", "content": system}, {"role": "user", "content": content}],
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "result", "strict": True, "schema": schema},
            },
            max_completion_tokens=16384,
            store=False,
        )
        choice = response.choices[0]
        if choice.finish_reason != "stop" or not choice.message.content:
            raise RuntimeError(f"Astra incomplete: {choice.finish_reason}")
        self.calls.append(
            {
                "kind": "astra_write",
                "model": response.model,
                "finish_reason": choice.finish_reason,
                "usage": getattr(response.usage, "model_dump", lambda: {})(),
            }
        )
        return json.loads(choice.message.content)

    def edit_image(
        self,
        prompt: str,
        images: list[tuple[str, bytes]],
        size: str,
        mask: bytes | None = None,
    ) -> bytes:
        if mask is not None or len(images) != 1 or images[0][1] != self.expected_guide:
            raise RuntimeError("Treatment image call must use only the frozen guide and no mask")
        files = [
            (f"image{i}.{mime.split('/')[1]}", io.BytesIO(data), mime)
            for i, (mime, data) in enumerate(images, 1)
        ]
        response = self.client.images.edit(
            model=IMAGE_MODEL,
            image=files,
            prompt=prompt,
            n=1,
            size=size,
            quality="high",
            output_format="png",
            background="opaque",
        )
        output = base64.b64decode(response.data[0].b64_json)
        self.calls.append(
            {
                "kind": "image_edit",
                "model": IMAGE_MODEL,
                "size": size,
                "guide_sha256": sha(images[0][1]),
                "mask": False,
            }
        )
        return output


def main() -> None:
    TREATMENT.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=WORKTREE, text=True).strip()
    if commit != PR_COMMIT:
        raise RuntimeError(f"Unexpected worktree commit: {commit}")
    manifest = []
    original_builder = pipeline.build_guide
    for slug in FIXTURES:
        source = BASELINE / slug
        record = json.loads((source / "record.json").read_text())
        debug = record["scene_debug"]
        guide = (source / "control_guide.png").read_bytes()
        hero = (source / "control_product.png").read_bytes()
        reference = (source / "control_reference.png").read_bytes()
        fixture_dir = TREATMENT / slug
        run_dir = fixture_dir / "run"
        fixture_dir.mkdir(parents=True, exist_ok=True)
        ref_meta = debug["reference"]
        ref = StyleRef(
            ref_meta["id"],
            ref_meta["name"],
            ref_meta["tone"],
            ref_meta["content"],
            "image/png",
            reference,
        )
        row = Row(slug, record["prompt"], "frozen-endpoint-artifact", 2368, 1776, [])
        client = FrozenInputsClient(debug, guide, fixture_dir)

        def frozen_guide(_hero, _mask, geometry, camera):
            if geometry != debug["geometryResponse"]["geometry"] or camera != debug["twinCamera"]:
                raise RuntimeError("Frozen guide replay received different geometry or camera")
            return guide, dict(debug["guideInfo"])

        pipeline.build_guide = frozen_guide
        try:
            result = pipeline.run_row(
                row,
                client,
                [ref],
                run_dir,
                hero,
                ref_count=1,
                size=(2368, 1776),
                camera=debug["twinCamera"],
            )
        finally:
            pipeline.build_guide = original_builder
        (fixture_dir / "calls.json").write_text(json.dumps(client.calls, indent=2))
        if result["status"] != "ok":
            raise RuntimeError(f"{slug}: {result['error']}")
        output = run_dir / "rows" / slug / "ours.png"
        persisted_guide = run_dir / "rows" / slug / "geometry_guide.png"
        if persisted_guide.read_bytes() != guide:
            raise RuntimeError(f"{slug}: persisted guide differs from frozen control")
        fixture = {
            "slug": slug,
            "control_job_id": record["job_id"],
            "device_id": record["device_id"],
            "camera_id": record["camera_id"],
            "prompt": record["prompt"],
            "pr_commit": commit,
            "pipeline_version": result["pipeline_version"],
            "text_model": TEXT_MODEL,
            "image_model": IMAGE_MODEL,
            "guide_sha256": sha(guide),
            "control_output_sha256": file_sha(source / "control_scene.png"),
            "treatment_output_sha256": file_sha(output),
            "final_prompt_sha256": sha(result["prompt"].encode()),
            "image_calls": result["image_calls"],
            "mask_applied": result["masked"],
            "calls": client.calls,
        }
        (fixture_dir / "provenance.json").write_text(json.dumps(fixture, indent=2))
        manifest.append(fixture)
        print(json.dumps({"completed": slug, "treatment_output_sha256": fixture["treatment_output_sha256"]}), flush=True)

    changed = [
        PACKAGE / "hp3p/prompts/system_3p.txt",
        PACKAGE / "hp3p/pipeline.py",
        PACKAGE / "hp3p/geometry.py",
        PACKAGE / "hp3p/grade.py",
        PACKAGE / "hp3p/reference_blue.py",
    ]
    summary = {
        "schema_version": 1,
        "experiment": "PR4349 translation-only product relocation; fixed orientation/view/scale",
        "pr_commit": commit,
        "worktree": str(WORKTREE),
        "prompt_source_sha256": {str(path.relative_to(WORKTREE)): file_sha(path) for path in changed},
        "fixtures": manifest,
        "controls": "Frozen endpoint PR4349 V6.1 outputs and byte-identical geometry guides",
        "treatment": "Exact isolated PR4349 run_row with frozen selection, geometry and guide replay",
        "api_retries": 0,
        "best_of": 1,
    }
    (TREATMENT / "manifest.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps({"complete": len(manifest), "manifest": str(TREATMENT / "manifest.json")}), flush=True)


if __name__ == "__main__":
    main()
