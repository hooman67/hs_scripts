from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import types
import unittest
from argparse import Namespace
from pathlib import Path
from unittest import mock

import run_generation as runner
import build_grouped_report as report
import build_distribution as distribution
import progressive_publish as publisher


def synthetic_document() -> dict:
    prompts = []
    for device in runner.DEVICE_ORDER:
        kind = "printer" if device in {"tassel", "magic"} else "laptop"
        for camera in runner.VIEW_ORDER[device]:
            for rank in range(1, 11):
                support_phrase = "round table" if kind == "laptop" else "dedicated equipment table"
                prompts.append({
                    "prompt_key": f"{device}__{kind}_{camera.replace('_', '')}::p{rank}",
                    "device_id": device,
                    "device_display_name": device.title(),
                    "device_type": kind,
                    "source_camera_name": camera,
                    "bank_debug_ref": f"{device}__{camera}",
                    "camera_tag": f"{kind}_{camera.replace('_', '')}",
                    "view_role": camera,
                    "bank_rank": rank,
                    "environment": "Office",
                    "text": f"A {support_phrase} anchors synthetic prompt {device} {camera} {rank}.",
                    "source_relevance_score": 60 + rank,
                    "ctech_reference_score": 50 + rank,
                    "ctech_reference_id": "CT01",
                    "primary_support": {"family": "table", "shape": "round" if kind == "laptop" else "unspecified",
                                        "phrase": support_phrase, "shape_evidence": None},
                    "prop_ids": ["P1"] if rank % 2 else [],
                    "score_components": {"smart_brief": {"setting": rank}},
                    "evidence": [{"document": "smart_brief", "path": "setting",
                                  "quote": "A shared setting supports focused work."}],
                })
    return {"prompts": prompts}


class RunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "prompts.json"
        self.path.write_text(json.dumps(synthetic_document()), encoding="utf-8")
        self.path.with_suffix(".txt").write_text("synthetic frozen prompt export\n", encoding="utf-8")
        self.digest = hashlib.sha256(self.path.read_bytes()).hexdigest()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_validates_16_by_10(self) -> None:
        rows = runner.validate_prompt_document(synthetic_document(), self.path, self.digest)
        self.assertEqual(160, len(rows))

    def test_rejects_wrong_frozen_hash(self) -> None:
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            runner.validate_prompt_document(synthetic_document(), self.path, "0" * 64)

    def test_latin_square_waves_cover_devices_and_view_positions(self) -> None:
        rows = runner.interleave(runner.validate_prompt_document(synthetic_document(), self.path, self.digest))
        for start in range(0, 160, 4):
            wave = rows[start:start + 4]
            self.assertEqual(set(runner.DEVICE_ORDER), {item["device_id"] for item in wave})
            positions = {runner.VIEW_ORDER[item["device_id"]].index(item["camera_id"]) for item in wave}
            self.assertEqual({0, 1, 2, 3}, positions)

    def test_catalog_defaults_to_baseline_and_can_strictly_pin_candidate(self) -> None:
        rows = runner.validate_prompt_document(synthetic_document(), self.path, self.digest)
        catalog = {
            "generator": runner.EXPECTED_GENERATOR,
            "rewriterVersion": runner.EXPECTED_REWRITER,
            "digitalTwins": [
                {"id": twin, "cameras": [{"id": camera} for camera in runner.VIEW_ORDER[device]]}
                for device, twin in runner.DEVICE_MAP.items()
            ],
        }
        runner.validate_catalog(catalog, rows)
        catalog["rewriterVersion"] = "changed"
        with self.assertRaisesRegex(ValueError, "rewriterVersion"):
            runner.validate_catalog(catalog, rows)
        candidate_rewriter = (
            "Adobe-Firefly/foundry#4349 / 8c358bc7989c + surface-shape-r1 / "
            "unified-blue-scale-v20-surface-shape-r1"
        )
        catalog["rewriterVersion"] = candidate_rewriter
        runner.validate_catalog(catalog, rows, runner.EXPECTED_GENERATOR, candidate_rewriter)
        with self.assertRaisesRegex(ValueError, "rewriterVersion"):
            runner.validate_catalog(catalog, rows)

    def test_lineage_keeps_source_and_deployment_manifests_distinct(self) -> None:
        args = Namespace(
            endpoint_base_url="http://127.0.0.1:9000", expected_generator="generator",
            expected_rewriter="rewriter", expected_pipeline_version="pipeline-r1", lineage_label="candidate",
            lineage_source_commit="a" * 40, lineage_patch_sha256="b" * 64,
            lineage_runtime_tree_sha256="c" * 64, lineage_source_manifest_sha256="d" * 64,
            lineage_deployment_manifest_sha256="e" * 64, lineage_candidate_config_sha256="f" * 64,
        )
        lineage = runner.lineage_from_args(args)
        self.assertEqual("d" * 64, lineage["source_manifest_sha256"])
        self.assertEqual("e" * 64, lineage["deployment_manifest_sha256"])
        self.assertEqual("f" * 64, lineage["candidate_config_sha256"])
        self.assertEqual("pipeline-r1", lineage["pipelineVersion"])
        self.assertEqual(runner.EXPECTED_SCENE_CONTRACT, lineage["scene_contract"])

    def test_candidate_catalog_must_report_exact_deployment_lineage(self) -> None:
        rows = runner.validate_prompt_document(synthetic_document(), self.path, self.digest)
        args = Namespace(
            endpoint_base_url="http://127.0.0.1:9000", expected_generator="generator",
            expected_rewriter="rewriter", expected_pipeline_version="pipeline-r1", lineage_label="candidate",
            lineage_source_commit="a" * 40, lineage_patch_sha256="b" * 64,
            lineage_runtime_tree_sha256="c" * 64, lineage_source_manifest_sha256="d" * 64,
            lineage_deployment_manifest_sha256="e" * 64, lineage_candidate_config_sha256="f" * 64,
        )
        lineage = runner.lineage_from_args(args)
        actual = {
            "candidateId": "candidate", "sourceCommit": "a" * 40, "patchSha256": "b" * 64,
            "codeTreeSha256": "c" * 64, "candidateManifestSha256": "d" * 64,
            "deploymentManifestSha256": "e" * 64, "configSha256": "f" * 64,
            "pipelineVersion": "pipeline-r1", "generator": "generator", "rewriterVersion": "rewriter",
            "textModel": runner.EXPECTED_SCENE_CONTRACT["textModel"],
            "imageModel": runner.EXPECTED_SCENE_CONTRACT["imageModel"],
            "imageSettings": {"operation": "images.edit", "count": 1, "size": "2368x1776",
                              "inputs": "one generated geometry guide", "mask": False},
        }
        catalog = {"generator": "generator", "rewriterVersion": "rewriter", "candidateLineage": actual,
                   "digitalTwins": [{"id": twin, "cameras": [{"id": camera} for camera in runner.VIEW_ORDER[device]]}
                                    for device, twin in runner.DEVICE_MAP.items()]}
        runner.validate_catalog(catalog, rows, "generator", "rewriter", lineage)
        catalog["candidateLineage"]["deploymentManifestSha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "candidate catalog lineage mismatch"):
            runner.validate_catalog(catalog, rows, "generator", "rewriter", lineage)

    def test_bounded_selection_keeps_full_latin_square_queue_identity(self) -> None:
        rows = runner.interleave(runner.validate_prompt_document(synthetic_document(), self.path, self.digest))
        for position, row in enumerate(rows, 1):
            row["queue_position"] = position
        queue = runner.queue_document(rows)
        requested = [f"{rows[9]['row_id']},{rows[0]['row_id']}"]
        selected = runner.select_rows(rows, requested)
        self.assertEqual([rows[0]["row_id"], rows[9]["row_id"]], [row["row_id"] for row in selected])
        self.assertEqual(160, queue["expected_count"])
        self.assertEqual(list(range(1, 161)), [row["queue_position"] for row in queue["rows"]])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            runner.select_rows(rows, [rows[0]["row_id"], rows[0]["row_id"]])
        with self.assertRaisesRegex(ValueError, "unknown"):
            runner.select_rows(rows, ["missing-row"])
        document = synthetic_document()
        selection_path = Path(self.temp.name) / "selection.json"
        selected_records = [document["prompts"][0], document["prompts"][27]]
        selection_path.write_text(json.dumps({
            "source_prompts_sha256": self.digest,
            "row_ids": [item["prompt_key"] for item in selected_records], "rows": selected_records,
        }), encoding="utf-8")
        row_ids, provenance = runner.load_selection_file(selection_path, document, self.digest)
        self.assertEqual([item["prompt_key"] for item in selected_records], row_ids)
        self.assertEqual(2, provenance["row_count"])
        changed = json.loads(selection_path.read_text())
        changed["rows"][0]["text"] = "changed"
        selection_path.write_text(json.dumps(changed), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "differs from frozen prompt"):
            runner.load_selection_file(selection_path, document, self.digest)

    def test_completed_smoke_row_resumes_without_endpoint_and_requires_lineage(self) -> None:
        row = runner.validate_prompt_document(synthetic_document(), self.path, self.digest)[0]
        row["queue_position"] = 1
        run_dir = Path(self.temp.name) / "resume"
        lineage = {
            "label": "candidate", "endpoint_base_url": "http://127.0.0.1:9999",
            "endpoint": "http://127.0.0.1:9999/api/generate", "generator": "generator",
            "rewriterVersion": "rewriter", "source_commit": None, "patch_sha256": None,
            "runtime_tree_sha256": None, "deployment_manifest_sha256": None,
        }
        runner.atomic_json(run_dir / "run_manifest.json", {
            "schema_version": 3, "run_sha256": "a" * 64, "catalog_sha256": "b" * 64, "lineage": lineage,
        })
        image_path = runner.paths(run_dir, row)["image"]
        image_path.parent.mkdir(parents=True, exist_ok=True)
        runner.Image.new("RGB", (1, 1)).save(image_path, format="PNG")
        runner.atomic_json(runner.paths(run_dir, row)["record"], {
            "status": "done", "row_id": row["row_id"], "prompt_sha256": row["prompt_sha256"],
            "image_sha256": runner.sha256_path(image_path), "run_sha256": "a" * 64,
            "catalog_sha256": "b" * 64, "lineage": lineage,
        })
        with mock.patch.object(runner, "endpoint_client") as endpoint:
            result = runner.process(run_dir, row, "b" * 64, 60, "a" * 64, lineage)
        endpoint.assert_not_called()
        self.assertEqual("done", result["status"])
        record = json.loads(runner.paths(run_dir, row)["record"].read_text())
        record["lineage"] = {**lineage, "label": "wrong"}
        runner.atomic_json(runner.paths(run_dir, row)["record"], record)
        self.assertIsNone(runner.valid_completed_record(run_dir, row))

    def test_scene_debug_contract_rejects_downstream_or_mode_drift(self) -> None:
        row = runner.validate_prompt_document(synthetic_document(), self.path, self.digest)[0]
        lineage = {
            "rewriterVersion": "candidate-rewriter", "pipelineVersion": "candidate-r1",
            "scene_contract": runner.EXPECTED_SCENE_CONTRACT,
        }
        detail = {
            "rewriterVersion": "candidate-rewriter", "pipelineVersion": "candidate-r1",
            "originalPrompt": row["prompt"]["text"], **runner.EXPECTED_SCENE_CONTRACT,
        }
        runner.validate_scene_detail(detail, row, lineage)
        for key, wrong in (("imageCalls", 2), ("graded", True), ("imageMaskApplied", True),
                           ("imageInputOrder", ["hp16_reference.png"]),
                           ("pipelineVersion", "reference-blue-cache")):
            changed = {**detail, key: wrong}
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "scene provenance mismatch"):
                runner.validate_scene_detail(changed, row, lineage)

    def test_missing_image_order_requires_exact_debug_guide_call_evidence(self) -> None:
        row = runner.validate_prompt_document(synthetic_document(), self.path, self.digest)[0]
        lineage = {
            "rewriterVersion": "candidate-rewriter", "pipelineVersion": "candidate-r1",
            "scene_contract": runner.EXPECTED_SCENE_CONTRACT,
        }
        detail = {
            "rewriterVersion": "candidate-rewriter", "pipelineVersion": "candidate-r1",
            "originalPrompt": row["prompt"]["text"],
            **{key: value for key, value in runner.EXPECTED_SCENE_CONTRACT.items()
               if key != "imageInputOrder"},
        }
        request = {
            "digitalTwinId": row["digital_twin_id"], "cameraId": row["camera_id"],
            "prompt": row["prompt"]["text"],
        }
        job_id, guide_sha, output_sha = "job-1", "a" * 64, "b" * 64
        job = {"submit_response": {"jobId": job_id}}
        final_status = {"jobId": job_id, "imageSha256": output_sha}
        call = {
            "kind": "image_edit", "model": runner.EXPECTED_SCENE_CONTRACT["imageModel"],
            "size": runner.EXPECTED_SCENE_CONTRACT["size"], "quality": "high",
            "outputFormat": "png", "background": "opaque", "count": 1, "mask": False,
            "promptSha256": "c" * 64, "guideSha256": guide_sha, "outputSha256": output_sha,
        }
        debug = {
            "job": {"jobId": job_id, "request": request,
                    "requestSha256": runner.canonical_sha256(request)},
            "status": {"jobId": job_id},
            "calls": [{"kind": "chat_json"}, call],
        }
        evidence = runner.validate_debug_image_input_evidence(
            debug, guide_sha, row, job, final_status, lineage)
        runner.validate_scene_detail(detail, row, lineage, evidence)

        for label, changed in (
            ("guide hash", {**call, "guideSha256": "d" * 64}),
            ("output hash", {**call, "outputSha256": "e" * 64}),
            ("hidden extra input", {**call, "referenceSha256": "f" * 64}),
        ):
            invalid = {**debug, "calls": [{"kind": "chat_json"}, changed]}
            with self.subTest(label=label), self.assertRaisesRegex(ValueError, "debug image-input"):
                runner.validate_debug_image_input_evidence(
                    invalid, guide_sha, row, job, final_status, lineage)
        with self.assertRaisesRegex(ValueError, "scene provenance mismatch"):
            runner.validate_scene_detail(detail, row, lineage)

    def test_pending_report_row_includes_every_review_input(self) -> None:
        row = runner.validate_prompt_document(synthetic_document(), self.path, self.digest)[0]
        rendered = report.build_row(row, None, None, "bucket", "prefix", 1,
                                    {"smart_brief": "full smart brief", "source_messaging": "full source messaging"})
        self.assertEqual(5, len(rendered["images"]))
        labels = [asset["meta_text"]["label"] for asset in rendered["images"]]
        self.assertEqual([
            "Digital twin / exact fixed camera input", "Generation output status",
            "Full frozen prompt, scores, source, and explanations", "Output provenance and debug", "New judgment only",
        ], labels)
        self.assertIn("No prior judgment was copied", rendered["images"][-1]["text_content"])
        self.assertIn("FULL SMART BRIEF\nfull smart brief", rendered["images"][2]["text_content"])
        values = rendered["meta_data"]["key_val_informations"]
        self.assertEqual("table", values["Surface family"])
        self.assertEqual("round", values["Surface shape"])

    def test_distribution_uses_text_metadata_and_real_record_presence_only(self) -> None:
        document = synthetic_document()
        rows = runner.validate_prompt_document(document, self.path, self.digest)
        sources = {item["bank_debug_ref"]: {"smart_brief": "full", "source_messaging": {}}
                   for item in document["prompts"]}
        catalog = Path(self.temp.name) / "catalog.json"
        catalog.write_text(json.dumps({"version": "test-v1", "revision": "r1", "entries": [
            {"id": "P1", "name": "Test prop", "repetition_groups": ["test_group"]}
        ]}), encoding="utf-8")
        analysis = distribution.build_analysis(document, rows, {}, sources, self.path, self.digest, catalog)
        self.assertEqual(160, analysis["scope"]["text_prompt_rows"])
        self.assertEqual(0, analysis["scope"]["generated_artifact_count"])
        self.assertEqual(0, analysis["scope"]["image_content_rows_audited"])
        self.assertEqual(0, analysis["scope"]["new_judgment_scores_used"])
        self.assertEqual({"pending": 160}, analysis["scope"]["generation_status_counts"])
        self.assertEqual(80, analysis["approved_prop_groups"]["groups"][0]["prompt_count"])
        self.assertEqual(160, analysis["text_metrics"]["word_count"]["count"])
        self.assertEqual(1, analysis["source_coverage"]["ctech_references"]["distinct_count"])
        self.assertIn("bank_group_compliance", analysis["approved_prop_groups"])
        self.assertIn("closest_token_pairs", analysis["lexical_audit"])
        self.assertIn("?rows=1&per=1", analysis["rows"][0]["fe_url"])
        page = distribution.render_html(analysis)
        self.assertIn("TEXT CENSUS", page)
        self.assertIn("Image content audited: 0", page)
        self.assertNotIn("<script src=", page)
        fake_records = {rows[0]["row_id"]: {"row_id": rows[0]["row_id"], "status": "done"}}
        fake = distribution.build_analysis(document, rows, fake_records, sources, self.path, self.digest,
                                           catalog, Path(self.temp.name) / "empty-run")
        self.assertEqual(0, fake["scope"]["generated_artifact_count"])
        self.assertEqual("invalid done record / artifact missing or mismatched", fake["rows"][0]["generation_status"])

    def test_old_v62_laptop_text_baseline_is_11_round_and_8_of_10_cafe(self) -> None:
        project = Path(__file__).resolve().parents[2]
        module_path = project / "research/source_messaging_v1_to_v6/versions/v6_2/surfaces.py"
        spec = importlib.util.spec_from_file_location("legacy_surface_inference_for_test", module_path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        old_path = project / (
            "eval_sets/hp_lifestyle_spatial_composition_v6_2_four_devices_20261106/"
            "revisions/v6.2-full160-20261107-r5-validated-composite/exports/final/prompts_all_160.json"
        )
        old = json.loads(old_path.read_text(encoding="utf-8"))
        laptop_rows = []
        for prompt in old["prompts"]:
            if prompt["device_type"] != "laptop":
                continue
            laptop_rows.append({
                "row_id": prompt["prompt_key"], "device_type": "laptop", "environment": prompt["environment"],
                "primary_support": module.infer_primary_support(prompt["text"], "laptop"),
            })
        summary = distribution.support_summary(laptop_rows)
        self.assertEqual(11, summary["shape_counts"]["round"])
        self.assertEqual(1, summary["shape_counts"]["oval"])
        self.assertEqual(8, summary["round_cafe"]["numerator"])
        self.assertEqual(10, summary["round_cafe"]["denominator"])

    def test_rejects_non_integer_rank_and_cross_origin_resume_url(self) -> None:
        document = synthetic_document()
        document["prompts"][0]["bank_rank"] = True
        changed = Path(self.temp.name) / "changed.json"
        changed.write_text(json.dumps(document), encoding="utf-8")
        digest = hashlib.sha256(changed.read_bytes()).hexdigest()
        with self.assertRaisesRegex(ValueError, "bank_rank must be an integer"):
            runner.validate_prompt_document(document, changed, digest)
        with self.assertRaisesRegex(ValueError, "cross-origin"):
            runner.endpoint_url("https://example.com/api/jobs/1", "statusUrl")

    def test_gateway_env_api_and_publication_allowlist(self) -> None:
        fake_gateway = types.SimpleNamespace(maybe_s3_env_vars=lambda bucket: {
            "AWS_ACCESS_KEY_ID": "id", "AWS_SECRET_ACCESS_KEY": "secret", "AWS_SESSION_TOKEN": "session",
            "AWS_REGION": "us-test-1",
        })
        with mock.patch.dict(sys.modules, {"foundry_aws_gateway": fake_gateway}), mock.patch.object(runner.boto3, "client") as client:
            runner.s3_client("bucket", Path(self.temp.name) / "absent.env")
            client.assert_called_once_with("s3", region_name="us-test-1", aws_access_key_id="id",
                                           aws_secret_access_key="secret", aws_session_token="session")
        run_dir = Path(self.temp.name) / "run"
        for relative in ("run_manifest.json", "images/a.png", "twins/a.png", "source/a.json", "report/viewer.html",
                         "records/a.json", "jobs/a.json", "status/a.json", "journals/events.jsonl",
                         "journals/tmux.stdout.log", "source/private-token.env"):
            path = run_dir / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"x")
        names = {path.relative_to(run_dir).as_posix() for path in runner.publishable_paths(run_dir)}
        self.assertTrue({"run_manifest.json", "images/a.png", "twins/a.png", "source/a.json", "report/viewer.html"} <= names)
        self.assertFalse(any(name.startswith("journals/") for name in names))
        self.assertNotIn("source/private-token.env", names)

    def test_progressive_publisher_delta_upload_and_remote_sha_cache(self) -> None:
        run_dir = Path(self.temp.name) / "delta-publish"
        runner.atomic_json(run_dir / "run_manifest.json", {"run": "test"})
        runner.atomic_json(run_dir / "summary.json", {"done": 1})
        (run_dir / "images").mkdir(parents=True)
        (run_dir / "report").mkdir(parents=True)
        (run_dir / "twins").mkdir(parents=True)
        (run_dir / "images/one.png").write_bytes(b"one")
        (run_dir / "report/viewer.html").write_bytes(b"viewer")
        (run_dir / "twins/one.png").write_bytes(b"twin")
        uploads: list[str] = []
        objects: dict[str, bytes] = {}

        class Body:
            def __init__(self, value: bytes): self.value = value
            def iter_chunks(self, chunk_size):
                yield self.value

        class FakeS3:
            def upload_file(self, filename, bucket, key, ExtraArgs):
                uploads.append(key)
                objects[key] = Path(filename).read_bytes()
            def head_object(self, Bucket, Key):
                value = objects[Key]
                return {"ContentLength": len(value), "ETag": f'"etag-{hashlib.sha256(value).hexdigest()}"'}
            def get_object(self, Bucket, Key):
                return {"Body": Body(objects[Key])}

        fake = FakeS3()
        manifest = {"bucket": "bucket", "prefix": "prefix"}
        with mock.patch.object(publisher.generation, "s3_client", return_value=fake):
            count, first = publisher.publish_changed_tree(run_dir, manifest, Path("unused"), {})
            self.assertEqual(5, count)
            count, second = publisher.publish_changed_tree(run_dir, manifest, Path("unused"), first)
            self.assertEqual(0, count)
            verified = publisher.verify_published(run_dir, manifest, Path("unused"))
            self.assertEqual(3, verified["remote_get_count"])
            cached = publisher.verify_published(run_dir, manifest, Path("unused"), verified["objects"])
            self.assertEqual(0, cached["remote_get_count"])
            (run_dir / "images/one.png").write_bytes(b"changed")
            count, third = publisher.publish_changed_tree(run_dir, manifest, Path("unused"), second)
            self.assertEqual(1, count)
            changed = publisher.verify_published(run_dir, manifest, Path("unused"), cached["objects"])
        self.assertEqual(1, changed["remote_get_count"])
        self.assertEqual(5, len(third))
        self.assertEqual(6, len(uploads))

    def test_summary_does_not_count_unverified_done_as_success(self) -> None:
        rows = runner.validate_prompt_document(synthetic_document(), self.path, self.digest)
        run_dir = Path(self.temp.name) / "summary-run"
        row = rows[0]
        record_path = runner.paths(run_dir, row)["record"]
        runner.atomic_json(record_path, {"row_id": row["row_id"], "prompt_sha256": row["prompt_sha256"],
                                         "status": "done", "image_sha256": "0" * 64})
        summary = runner.summarize(run_dir, rows, "bucket", "prefix")
        self.assertEqual(1, summary["status_counts"]["invalid_done_artifact"])
        self.assertNotIn("done", summary["status_counts"])

    def test_offline_initialize_and_grouped_report_are_exact_160(self) -> None:
        root = Path(self.temp.name)
        document = synthetic_document()
        bank_audit = {}
        for case_id in sorted({item["bank_debug_ref"] for item in document["prompts"]}):
            source = root / "bank_sources" / f"{case_id}.json"
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(json.dumps({"smart_brief": f"brief {case_id}", "source_messaging": {"message": case_id}}),
                              encoding="utf-8")
            bank_audit[case_id] = {"source_input_path": str(source),
                                   "source_input_sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
        document["bank_audit"] = bank_audit
        self.path.write_text(json.dumps(document), encoding="utf-8")
        digest = hashlib.sha256(self.path.read_bytes()).hexdigest()
        rows = runner.interleave(runner.validate_prompt_document(document, self.path, digest))
        for position, row in enumerate(rows, 1):
            row["queue_position"] = position
        catalog = {"generator": runner.EXPECTED_GENERATOR, "rewriterVersion": runner.EXPECTED_REWRITER,
                   "digitalTwins": [{"id": twin, "cameras": [{"id": camera} for camera in runner.VIEW_ORDER[device]]}
                                    for device, twin in runner.DEVICE_MAP.items()]}
        twins = root / "twins"
        twins.mkdir()
        for device in runner.DEVICE_ORDER:
            for camera in runner.VIEW_ORDER[device]:
                (twins / f"{device}__{camera}.png").write_bytes(b"frozen-twin")
        run_dir = root / "run"
        runner.initialize_run(Namespace(run_dir=run_dir, prompts=self.path, prompts_sha256=digest,
                                        bucket="bucket", prefix="prefix", twin_dir=twins), document, rows, catalog)
        immutable_run_manifest = (run_dir / "run_manifest.json").read_bytes()
        queue_manifest = json.loads((run_dir / "queue_manifest.json").read_text())
        self.assertEqual(160, len(queue_manifest["rows"]))
        self.assertEqual(160, len({row["row_id"] for row in queue_manifest["rows"]}))
        runner.initialize_run(Namespace(run_dir=run_dir, prompts=self.path, prompts_sha256=digest,
                                        bucket="bucket", prefix="prefix", twin_dir=twins), document, rows, catalog)
        self.assertEqual(immutable_run_manifest, (run_dir / "run_manifest.json").read_bytes())
        prop_catalog = root / "props.json"
        prop_catalog.write_text(json.dumps({"version": "v", "revision": "r", "entries": [
            {"id": "P1", "name": "Test", "environment": "Office", "role": "decor",
             "repetition_groups": ["test_group"]}
        ]}), encoding="utf-8")
        viewer = root / "viewer.html"
        viewer.write_text("<!doctype html><title>canonical test viewer</title>", encoding="utf-8")
        output = run_dir / "report"
        argv = ["build_grouped_report.py", "--prompts", str(self.path), "--prompts-sha256", digest,
                "--run-dir", str(run_dir), "--output", str(output), "--viewer", str(viewer),
                "--bucket", "bucket", "--prefix", "prefix", "--catalog", str(prop_catalog)]
        with mock.patch.object(sys, "argv", argv):
            self.assertEqual(0, report.main())
        root_data = json.loads((output / "data.json").read_text())
        manifest = json.loads((output / "build_manifest.json").read_text())
        self.assertEqual(160, len(root_data["rows"]))
        self.assertEqual(16, len(manifest["groups"]))
        self.assertTrue(all(group["rows"] == 10 for group in manifest["groups"]))
        self.assertEqual(160, manifest["pending_judgment_count"])
        self.assertEqual(runner.EXPECTED_GENERATOR, manifest["run_identity"]["generator"])
        self.assertEqual(runner.EXPECTED_REWRITER, manifest["run_identity"]["rewriterVersion"])
        self.assertIn(runner.EXPECTED_REWRITER, json.dumps(root_data["meta_texts"]))
        first_labels = [asset["meta_text"]["label"] for asset in root_data["rows"][0]["images"]]
        self.assertEqual("Digital twin / exact fixed camera input", first_labels[0])
        self.assertEqual("Generation output status", first_labels[1])


if __name__ == "__main__":
    unittest.main()

