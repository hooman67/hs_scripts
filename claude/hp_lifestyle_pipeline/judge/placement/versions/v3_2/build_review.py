"""Publishable judge comparisons with exact media bindings and exportable comments."""

import argparse
import html
import json
import posixpath
import shutil
from pathlib import Path

import common
from refiner import BUCKET

STORE = common.ROOT / "publication"
PREFIX = "judge_evals/hp_placement_v3_2_astra_20261111/gallery/"
BASE = "https://foundry-aws-corp.adobe.io/asset/" + BUCKET + "/"
AUTH = (
    common.ROOT.parents[3]
    / "eval_sets/hp_lifestyle_v6_3_full160_pr4523_pr4417_20261110/public/gallery/imsauth.js"
)


def configure(version):
    global STORE, PREFIX
    version = version.resolve()
    if version.parent != common.ROOT.parent:
        raise ValueError("Use an isolated sibling judge version")
    if version.name in ("v3_2", "v3_2_r2"):
        STORE = common.ROOT / "publication"
        PREFIX = "judge_evals/hp_placement_v3_2_astra_20261111/gallery/"
    elif version.name.startswith("v3_2_r") and version.name[6:].isdigit():
        revision = int(version.name[6:])
        if revision < 3:
            raise ValueError("Unsupported judge revision")
        STORE = version / "publication"
        PREFIX = f"judge_evals/hp_placement_v3_2_astra_20261111/r{revision}/gallery/"
    else:
        raise ValueError("Unsupported judge publication version")


def s3_client():
    import foundry_aws_gateway

    client = foundry_aws_gateway.maybe_s3_client(BUCKET)
    if client is None:
        raise RuntimeError("Foundry gateway did not provide authenticated S3 access")
    return client


def load(path):
    return json.loads(path.read_text())


def escape(value):
    return html.escape(str(value), quote=True)


def asset(url):
    if not url.startswith(BASE):
        raise ValueError("Gallery assets must remain on the approved HP bucket")
    return posixpath.relpath(url[len(BASE) :], PREFIX)


def localized_feedback():
    directory = common.ROOT / "astra_localized_feedback"
    if not (directory / "proposal.json").exists():
        return None
    receipt = load(directory / "receipt.json")
    if common.sha(receipt["chunks_path"]) != receipt["chunks_sha256"]:
        raise ValueError("Localized Astra feedback raw stream changed")
    collector = common.Collector()
    from pathlib import Path

    with Path(receipt["chunks_path"]).open() as stream:
        for line in stream:
            collector.feed(json.loads(line))
    analysis = load(directory / "proposal.json")
    if collector.result() != analysis:
        raise ValueError("Localized analysis differs from the actual Astra response")
    inputs = load(directory / "input.json")
    return {
        **inputs["new_user_feedback"],
        "analysis": analysis,
        "receipt": receipt,
        "input_sha256": common.sha(directory / "input.json"),
        "old_labels_and_predictions_unchanged": True,
    }


def clarification_html(case_id, feedback, appearance=False):
    if feedback is None or case_id != feedback["case_id"]:
        return ""
    interpretation = (
        "This revision uses the user-confirmed appearance-sensitive standard: "
        "explicit concerns and score penalties even when physically plausible, "
        "not necessarily FAIL. Earlier material-geometry disagreement remains "
        "preserved, not retrospectively resolved."
        if appearance
        else "Astra inspected these specific features but still does not "
        "substantiate material defects. This disagreement is unresolved, not "
        "a correction of the human feedback."
    )
    return (
        '<aside class="warning"><strong>Latest human clarification '
        "(separate from frozen checks)</strong><p>"
        + escape(feedback["verbatim"])
        + "</p><p>"
        + interpretation
        + ' <a href="astra_localized_feedback.json">'
        "Read actual Astra evidence and counter-evidence</a>.</p></aside>"
    )


def snapshot():
    inventory = load(common.R1 / "evaluation/inventory.json")
    url = inventory["source_viewer"]["url"]
    response = s3_client().get_object(Bucket=BUCKET, Key=url[len(BASE) :])
    try:
        body = response["Body"].read()
    finally:
        response["Body"].close()
    target = STORE / "source/viewer.html"
    if target.exists() and target.read_bytes() != body:
        raise ValueError(
            "Snapshot changed; preserve it and create another snapshot version"
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(body)
    common.write_json(
        target.with_name("object.json"),
        {
            "url": url,
            "etag": response["ETag"],
            "version_id": response.get("VersionId"),
            "sha256": common.sha(target),
            "bytes": len(body),
        },
    )
    shutil.copy2(AUTH, STORE / "source/imsauth.js")


def panel(label, row):
    if row["status"] == "error":
        return f'<div class="judge error"><strong>{escape(label)}: ERROR / no score</strong><p>{escape(row["error"])}</p></div>'
    if row["status"] != "complete":
        raise ValueError("Non-terminal judge result cannot be displayed as a verdict")
    observation = row["observation"]
    title = f"{label}: {row['verdict'].upper()} | {row['score']:g}/100"
    checks = row.get("checks")
    failed = [name for name, matched in checks.items() if not matched] if checks else []
    gate = (
        f'<p class="failed-check">Criterion mismatch: {escape("; ".join(failed))}</p>'
        if failed
        else ""
    )
    return (
        f'<div class="judge {escape(row["verdict"])}"><strong>{escape(title)}</strong>'
        f"<p>{escape(observation['summary'])}</p>{gate}"
        "<details><summary>Evidence by component</summary><pre>"
        + escape(json.dumps(observation["components"], indent=2, ensure_ascii=False))
        + "</pre></details></div>"
    )


def card(case_id, image, title, rows, previous=""):
    path = asset(image["url"])
    return (
        f'<article class="scene" data-scene="{escape(case_id)}" data-sha="{escape(image["sha256"])}">'
        f'<strong>{escape(title)}</strong><img loading="lazy" data-src="{escape(path)}" alt="{escape(case_id)}">'
        f'<a href="{escape(path)}" target="_blank" rel="noopener">Full image</a>'
        + "".join(panel(label, row) for label, row in rows)
        + (
            f"<details><summary>Previous judges (unchanged evidence)</summary>{previous}</details>"
            if previous
            else ""
        )
        + "<details><summary>Comment on this image / judges</summary>"
        f'<textarea data-case="{escape(case_id)}" data-sha="{escape(image["sha256"])}" data-image="{escape(path)}" '
        'placeholder="Name the judge/criterion you agree or disagree with, and the visible evidence."></textarea></details></article>'
    )


def document(
    title, sections, protocol, notice, calibration_only=False, appearance=False
):
    feedback_link = (
        '<p><a href="astra_localized_feedback.json">Latest human clarification / '
        "Astra response</a></p>"
        if (STORE / "public/astra_localized_feedback.json").exists()
        else ""
    )
    links = (
        f'<a href="{escape(asset(load(STORE / "source/object.json")["url"]))}">Original32-row source (prior judges)</a>'
        f'<a href="{escape(asset(BASE + "refiner_evals/hp_judge_refiner/hpjr-all-fixable-20261109T225123Z/full_evalset.html"))}">64-case source (historical feedback)</a>'
        if calibration_only
        else '<a href="historical.html">Original32-row comparison</a>'
        '<a href="refiner.html">64-case baseline / refined comparison</a>'
    )
    if appearance and not calibration_only:
        links += (
            '<a href="ctech.html">New30-image C-Tech feedback</a>'
            '<a href="feedback_coverage_audit.json">Actual Astra coverage audit</a>'
        )
    if appearance:
        links += (
            '<a href="astra_appearance_design.json">Actual Astra rubric proposal</a>'
            '<a href="feedback_requirements.json">Preregistered feedback scope</a>'
        )
    if (STORE.parent / "visual_policy.json").exists():
        links += '<a href="visual_acquisition_trace.json">Actual acquisition / stage trace</a>'
    if (STORE / "public/astra_successor_diagnosis.json").exists():
        links += '<a href="astra_successor_diagnosis.json">Actual Astra failure diagnosis (not new predictions)</a>'
    if (STORE / "public/astra_exemplar_audit.json").exists():
        links += '<a href="astra_exemplar_audit.json">Actual Astra exemplar audit (proposals only)</a>'
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{escape(title)}</title><link rel="stylesheet" href="review.css"></head>'
        f'<body data-protocol="{escape(protocol)}"><div id="ims"></div><div id="loading">Sign in to load images.</div>'
        f'<main id="content" class="hidden"><header><h1>{escape(title)}</h1>'
        '<nav><a href="index.html">Calibration / revisions</a>'
        + links
        + '<a href="results.json">Current judge results</a>'
        '<a href="astra_visual_analysis.json">Earlier Astra native-pixel probe</a></nav>'
        f'<p class="warning">{escape(notice)}</p>'
        + feedback_link
        + "<p>Astra judges the images and authors the system prompts; the application computes the unchanged placement score. "
        "A high score is not a probability or automatic approval. Target comments/labels were withheld from judge calls.</p>"
        '<button id="export-feedback">Export my comments (JSON)</button>'
        '<span id="feedback-status">Comments stay in this browser only; export them to share.</span></header>'
        + "".join(sections)
        + '</main><script src="https://auth-stg1.services.adobe.com/imslib/imslib.js"></script>'
        '<script src="imsauth.js"></script><script src="review.js"></script></body></html>'
    )


def indexed(summary):
    if len(summary["records"]) != summary["expected"] or any(
        row["status"] not in {"complete", "error"} for row in summary["records"]
    ):
        raise ValueError(
            "Every expected case must have a terminal result or explicit error"
        )
    values = {(row["id"], row["candidate"]): row for row in summary["records"]}
    if len(values) != len(summary["records"]):
        raise ValueError("Duplicate case/candidate results")
    for row in values.values():
        if row["status"] != "complete":
            continue
        if common.sha(row["result_path"]) != row["result_sha256"]:
            raise ValueError("Published model result changed")
        from pathlib import Path

        result = load(Path(row["result_path"]))
        for role in ("generated_image", "twin_image"):
            if common.sha(result["runtime_input"][role]) != row[role]["sha256"]:
                raise ValueError("Judgment is bound to another scene/reference")
        if (
            result["candidate"] != row["candidate"]
            or result["protocol_freeze_sha256"] != summary["protocol_freeze_sha256"]
            or result["application_merged_judgment"]["observation"]
            != row["observation"]
            or result["application_merged_judgment"]["natural_placement_score"]
            != row["score"]
            or result["final_decision"]["verdict"] != row["verdict"]
        ):
            raise ValueError(
                "Published candidate/score/evidence differs from actual result"
            )
        for stage in result["stages"].values():
            path = Path(stage["path"])
            if common.sha(path) != stage["sha256"]:
                raise ValueError("Published stage result changed")
            stage_result = load(path)
            chunks = Path(stage_result["chunks_path"])
            if common.sha(chunks) != stage_result["chunks_sha256"]:
                raise ValueError("Published raw model stream changed")
            collector = common.Collector()
            with chunks.open() as stream:
                for line in stream:
                    collector.feed(json.loads(line))
            if collector.result() != stage_result["observation"]:
                raise ValueError(
                    "Published stage evidence differs from actual Astra stream"
                )
    return values


def input_html(case):
    return (
        "<details><summary>Original scene prompt and product reference</summary>"
        f"<p>{escape(case['scene_prompt'])}</p>"
        f'<img loading="lazy" data-src="{escape(asset(case["twin_image"]["url"]))}" '
        'alt="Original product reference" style="max-width:450px;width:100%;height:auto">'
        "</details>"
    )


def predecessor_panels(index, case_id, version_name="v3_2_r2"):
    return "".join(
        panel(
            f"Astra {candidate.upper()} / {version_name} (unchanged)",
            index[(case_id, candidate)],
        )
        for candidate in ("p1", "p2")
    )


def appearance_design(version):
    from appearance_feedback import replay

    preparation = load(version / "preparation.json")
    path = Path(preparation["prompt_source_path"])
    design = load(path)
    if (
        common.sha(path) != preparation["prompt_source_sha256"]
        or replay(preparation["actual_astra_receipt"]).result() != design
    ):
        raise ValueError("Appearance design differs from actual Astra source")
    return design


def successor_diagnosis(version):
    from appearance_feedback import replay

    directory = version / "astra_successor_consult"
    if not (directory / "proposal.json").exists():
        return None
    analysis = load(directory / "proposal.json")
    receipt = load(directory / "receipt.json")
    inputs = load(directory / "input.json")
    if (
        replay(receipt).result() != analysis
        or inputs["source_revision"] != version.name
        or inputs["frozen_protocol_sha256"]
        != common.sha(version / "protocol_freeze.json")
    ):
        raise ValueError("Successor diagnosis differs from actual Astra source")
    sources = [("actual_calibration_predictions", version)]
    if "immediate_predecessor_calibration" in inputs:
        gates = load(version / "promotion_gates.json")
        sources.append(
            ("immediate_predecessor_calibration", Path(gates["predecessor"]["path"]))
        )
    bindings = []
    for field, root in sources:
        path = root / "evaluation/calibration/summary.json"
        summary = load(path)
        manifest = Path(summary["source"])
        if (
            summary != inputs[field]
            or common.sha(manifest) != summary["source_sha256"]
            or common.sha(root / "protocol_freeze.json")
            != summary["protocol_freeze_sha256"]
        ):
            raise ValueError("Diagnosis calibration provenance differs from source")
        indexed(summary)
        bindings.append(
            {
                "version": root.name,
                "summary_path": str(path),
                "prediction_summary_sha256": common.sha(path),
                "dataset_manifest_path": str(manifest),
                "dataset_manifest_sha256": summary["source_sha256"],
                "protocol_freeze_sha256": summary["protocol_freeze_sha256"],
            }
        )
    return {
        "interpretation": "Post-feedback Astra diagnosis, not a new blind prediction, applied penalty or promotion.",
        "analysis": analysis,
        "receipt": receipt,
        "input_sha256": common.sha(directory / "input.json"),
        "calibration_bindings": bindings,
        "source_hash_explanation": (
            "summary.source_sha256 hashes the input dataset manifest, not predictions. "
            "Unchanged manifests legitimately share that hash. Distinct prediction-summary "
            "and frozen-protocol hashes above bind the actual revision-specific results. "
            "The original Astra response, including its provenance question, is unchanged."
        ),
    }


def exemplar_audit(version):
    from appearance_feedback import replay
    from revise_appearance import exemplar_messages

    directory = version / "astra_exemplar_audit"
    if not (directory / "analysis.json").exists():
        return None
    analysis = load(directory / "analysis.json")
    receipt = load(directory / "receipt.json")
    inputs = load(directory / "input.json")
    config = load(Path(receipt["chunks_path"]).with_name("config.json"))
    artifact = Path(inputs["actual_exemplar_artifact"])
    if (
        replay(receipt).result() != analysis
        or inputs["source_revision"] != version.name
        or inputs["protocol_freeze_sha256"]
        != common.sha(version / "protocol_freeze.json")
        or common.sha(artifact) != inputs["actual_exemplar_artifact_sha256"]
        or load(artifact) != inputs["actual_exemplars"]
        or common.fingerprint(exemplar_messages(inputs)) != config["messages_sha256"]
    ):
        raise ValueError(
            "Exemplar audit differs from actual source or delivered messages"
        )
    return {
        "interpretation": "Post-feedback Astra exemplar audit. Corrections are proposals only; no runtime, labels, blind predictions or promotion changed.",
        "analysis": analysis,
        "receipt": receipt,
        "actual_inputs": inputs,
        "input_sha256": common.sha(directory / "input.json"),
    }


def acquisition_trace(summaries):
    from appearance_feedback import replay

    trace = []
    seen = set()
    for dataset, summary in summaries.items():
        for row in indexed(summary).values():
            identity = (row["id"], row["candidate"])
            if identity in seen:
                continue
            seen.add(identity)
            if row["status"] != "complete":
                trace.append(
                    {
                        "dataset": dataset,
                        "id": row["id"],
                        "candidate": row["candidate"],
                        "status": row["status"],
                        "error": row["error"],
                        "final_prediction_available": False,
                    }
                )
                continue
            result = load(Path(row["result_path"]))
            stages = []
            for name, binding in result["stages"].items():
                stage = load(Path(binding["path"]))
                acquisition = stage["visual_acquisition"]
                if acquisition is not None:
                    path = Path(acquisition["path"])
                    raw = load(path)
                    request = load(path.parent / "request.json")
                    if (
                        common.sha(path) != acquisition["sha256"]
                        or common.fingerprint(request) != acquisition["fingerprint"]
                        or raw["fingerprint"] != acquisition["fingerprint"]
                        or request["protocol_freeze_sha256"]
                        != summary["protocol_freeze_sha256"]
                        or request["stage"]
                        != ("p1_" + name if row["candidate"] == "p1" else name)
                        or raw["observation"] != {"record": acquisition["record"]}
                        or replay(raw).result() != raw["observation"]
                        or acquisition["scored"] is not False
                    ):
                        raise ValueError("Acquisition trace differs from actual source")
                stages.append(
                    {
                        "stage": name,
                        "actual_acquisition": acquisition,
                        "actual_stage_observation": stage["observation"],
                        "stage_result_sha256": binding["sha256"],
                    }
                )
            trace.append(
                {
                    "dataset": dataset,
                    "id": row["id"],
                    "candidate": row["candidate"],
                    "stages": stages,
                    "application_selected_observation": row["observation"],
                    "application_score": row["score"],
                    "application_verdict": row["verdict"],
                }
            )
    return {
        "interpretation": "Actual chronological acquisition/stage/final evidence, not a parent-authored semantic coverage judgment. Acquisition and repeated image views are not scored votes.",
        "records": trace,
    }


def build(version, calibration_only):
    destination = STORE / "public"
    destination.mkdir(parents=True, exist_ok=True)
    protocol = common.sha(version / "protocol_freeze.json")
    gates = load(version / "promotion_gates.json")
    appearance = gates.get("criterion_mode") == "appearance_review"
    predecessor = common.ROOT.parent / "v3_2_r2"
    feedback = localized_feedback()
    if feedback is not None:
        common.write_json(destination / "astra_localized_feedback.json", feedback)
    status_path = version / "release_status.json"
    status = (
        load(status_path)
        if status_path.exists()
        else {"status": "NOT PROMOTED; evaluation in progress"}
    )
    notice = (
        status["status"]
        + ". Historical anchors are E2E diagnostics, not held-out scene-stage accuracy. All64 feedback cases informed Astra design."
    )
    diagnosis = successor_diagnosis(version)
    if diagnosis is not None:
        common.write_json(destination / "astra_successor_diagnosis.json", diagnosis)
        notice += " A post-feedback Astra failure diagnosis is linked; it is not a new blind prediction or recovered penalty."
    exemplar_analysis = exemplar_audit(version)
    if exemplar_analysis is not None:
        common.write_json(destination / "astra_exemplar_audit.json", exemplar_analysis)
    if appearance:
        notice += (
            " User-authorized appearance concerns receive explicit evidence and score penalties "
            "even if physically plausible; minor concerns need not FAIL. This is a prospective "
            "rubric change, not recovery of the original physical gate. New30-image C-Tech "
            "feedback informed design; whole-image FAIL/OK is not placement gold."
        )
        from appearance_feedback import replay
        from feedback_requirements import verify_requirements

        design = appearance_design(version)
        common.write_json(destination / "astra_appearance_design.json", design)
        requirements = load(version / "feedback_requirements.json")
        verify_requirements(
            requirements, load(version / "evaluation/ctech/corpus.json")
        )
        common.write_json(destination / "feedback_requirements.json", requirements)
    summaries = {"calibration": load(version / "evaluation/calibration/summary.json")}
    current = indexed(summaries["calibration"])
    earlier = (
        indexed(load(common.ROOT / "evaluation/calibration/summary.json"))
        if version != common.ROOT
        else None
    )
    cases = load(
        version / "calibration_manifest.json"
        if appearance
        else common.R1 / "r2/calibration_manifest.json"
    )["cases"]
    previous_calibration = (
        indexed(load(predecessor / "evaluation/calibration/summary.json"))
        if appearance
        else None
    )
    immediate = Path(gates["predecessor"]["path"]) if appearance else None
    immediate_calibration = (
        indexed(load(immediate / "evaluation/calibration/summary.json"))
        if immediate is not None and immediate not in (predecessor, common.ROOT)
        else None
    )
    sections = []
    for case in cases:
        entries = [
            (
                f"Astra {candidate.upper()} / {version.name}",
                current[(case["id"], candidate)],
            )
            for candidate in ("p1", "p2")
        ]
        previous = (
            "".join(
                panel(
                    f"Astra {candidate.upper()} / v3_2 first attempt",
                    earlier[(case["id"], candidate)],
                )
                for candidate in ("p1", "p2")
            )
            if earlier
            else ""
        )
        if previous_calibration is not None:
            previous = predecessor_panels(previous_calibration, case["id"]) + previous
        if immediate_calibration is not None:
            previous = (
                predecessor_panels(immediate_calibration, case["id"], immediate.name)
                + previous
            )
        sections.append(
            f'<section class="study-row"><h2>{escape(case["id"])}</h2>'
            f"<p>Criterion labels (not global ground truth): {escape(json.dumps(case['expectation']))}</p>"
            + clarification_html(case["id"], feedback, appearance)
            + (input_html(case) if appearance else "")
            + card(
                case["id"], case["generated_image"], case["variant"], entries, previous
            )
            + "</section>"
        )
    (destination / "index.html").write_text(
        document(
            "HP placement judges - Astra calibration and revisions",
            sections,
            protocol,
            notice,
            calibration_only=calibration_only,
            appearance=appearance,
        )
    )
    if not calibration_only:
        summaries["historical"] = load(version / "evaluation/historical/summary.json")
        summaries["refiner"] = load(version / "evaluation/refiner/summary.json")
        historical = indexed(summaries["historical"])
        refiner = indexed(summaries["refiner"])
        previous_historical = (
            indexed(load(predecessor / "evaluation/historical/summary.json"))
            if appearance
            else None
        )
        previous_refiner = (
            indexed(load(predecessor / "evaluation/refiner/summary.json"))
            if appearance
            else None
        )
        inventory = load(common.R1 / "evaluation/inventory.json")
        old = common.load(
            "v32_old_gallery",
            common.R1 / "original_gallery_update_20261110/gallery_update.py",
        )
        source = (STORE / "source/viewer.html").read_text()
        slots = {item["url"]: item for item in old.GalleryParser(source).slots}
        old_results = {
            row["id"]: row
            for row in load(
                common.R1
                / "original_gallery_update_20261110/evaluation/gallery_results.json"
            )["records"]
        }
        sections = []
        for start in range(0, 128, 4):
            records = inventory["records"][start : start + 4]
            row_id = records[0]["source_row_id"]
            cards = []
            if len(records) != 4 or any(
                row["source_row_id"] != row_id for row in records
            ):
                raise ValueError("Original four-column row binding changed")
            for case in records:
                previous = slots[case["generated_image"]["url"]]["original_judge"]
                previous += old.result_html("r1", old_results[case["id"]]["r1"])
                previous += old.result_html("r2", old_results[case["id"]]["r2"])
                if previous_historical is not None:
                    previous = (
                        predecessor_panels(previous_historical, case["id"]) + previous
                    )
                entries = [
                    (
                        f"Astra {candidate.upper()} / {version.name}",
                        historical[(case["id"], candidate)],
                    )
                    for candidate in ("p1", "p2")
                ]
                cards.append(
                    card(
                        case["id"],
                        case["generated_image"],
                        case["variant"],
                        entries,
                        previous,
                    )
                )
            sections.append(
                f'<section class="study-row"><h2>{escape(row_id)}</h2>'
                + "".join(
                    clarification_html(case["id"], feedback, appearance)
                    for case in records
                )
                + '<div class="image-scroll">'
                '<div class="study-grid" style="--columns:4">'
                + "".join(cards)
                + "</div></div></section>"
            )
        (destination / "historical.html").write_text(
            document(
                "HP placement judges - original32 rows / four outputs",
                sections,
                protocol,
                notice,
                appearance=appearance,
            )
        )
        corpus = load(version / "evaluation/refiner/corpus.json")
        evidence = load(
            common.R1 / "astra_refiner_followup_20261110/evidence_manifest.json"
        )
        bindings = {(row["case_id"], row["role"]): row for row in corpus["bindings"]}
        scenes = {row["id"]: row for row in corpus["records"]}
        sections = []
        for case in evidence["cases"]:
            cards = []
            for role in ("baseline", "refined"):
                binding = bindings[(case["id"], role)]
                record = scenes[binding["scene_id"]]
                entries = [
                    (
                        f"Astra {candidate.upper()} / {version.name}",
                        refiner[(binding["scene_id"], candidate)],
                    )
                    for candidate in ("p1", "p2")
                ]
                image = {**record["generated_image"], "url": binding["url"]}
                title = role.title()
                if role == "refined" and binding["scene_id"].endswith("--baseline"):
                    title += " - exact passthrough; same judgment reused"
                previous = (
                    predecessor_panels(previous_refiner, binding["scene_id"])
                    if previous_refiner is not None
                    else ""
                )
                cards.append(
                    card(case["id"] + "--" + role, image, title, entries, previous)
                )
            sections.append(
                f'<section class="study-row"><h2>{escape(case["id"])}</h2>'
                f"<p>Original baseline feedback: {escape(case['reviewer_feedback'])}</p>"
                '<p class="muted">Feedback is about the baseline, not a label for the refined image. Execution status is not quality approval.</p>'
                '<div class="image-scroll"><div class="study-grid" style="--columns:2">'
                + "".join(cards)
                + "</div></div></section>"
            )
        (destination / "refiner.html").write_text(
            document(
                "HP placement judges - baseline / refined feedback set",
                sections,
                protocol,
                notice,
                appearance=appearance,
            )
        )
        if appearance:
            summaries["ctech"] = load(version / "evaluation/ctech/summary.json")
            ctech = indexed(summaries["ctech"])
            corpus = load(version / "evaluation/ctech/corpus.json")
            concerns = {
                row["case_id"]: row["concerns"] for row in requirements["cases"]
            }
            audit = load(version / "evaluation/feedback_coverage_audit.json")
            checks = {}
            audit_records = []
            for run in audit["runs"]:
                response = replay(run["receipt"]).result()
                audit_records.extend(response["records"])
                for row in response["records"]:
                    checks[(row["id"], row["candidate"])] = row["checks"]
            common.write_json(
                destination / "feedback_coverage_audit.json",
                {"metadata": audit, "actual_astra_records": audit_records},
            )
            sections = []
            for case in corpus["records"]:
                feedback_text = " ".join(
                    item["comment"] for item in case["human_feedback"]
                )
                entries = [
                    (
                        f"Astra {candidate.upper()} / {version.name}",
                        ctech[(case["id"], candidate)],
                    )
                    for candidate in ("p1", "p2")
                ]
                coverage = {
                    candidate: checks[(case["id"], candidate)]
                    for candidate in ("p1", "p2")
                }
                human_concerns = [
                    item
                    for item in concerns[case["id"]]
                    if item["origin"] == "human_feedback"
                ]
                extras = [
                    item
                    for item in concerns[case["id"]]
                    if item["origin"] == "astra_extra_finding"
                ]
                sections.append(
                    f'<section class="study-row"><h2>{escape(case["id"])}</h2>'
                    f"<p><strong>Original C-Tech comment:</strong> {escape(feedback_text)}</p>"
                    + input_html(case)
                    + card(
                        case["id"],
                        case["generated_image"],
                        "Original reviewed scene-generation image",
                        entries,
                    )
                    + "<details><summary>Feedback scope and actual Astra coverage audit</summary><pre>"
                    + escape(
                        json.dumps(
                            {
                                "human_concerns": human_concerns,
                                "actual_audit": coverage,
                            },
                            indent=2,
                        )
                    )
                    + "</pre></details>"
                    + (
                        "<details><summary>Additional Astra findings (not human feedback or required coverage)</summary><pre>"
                        + escape(json.dumps(extras, indent=2))
                        + "</pre></details>"
                        if extras
                        else ""
                    )
                    + "</section>"
                )
            (destination / "ctech.html").write_text(
                document(
                    "HP placement judges - new30-image C-Tech feedback",
                    sections,
                    protocol,
                    notice,
                    appearance=True,
                )
            )
    if (version / "visual_policy.json").exists():
        common.write_json(
            destination / "visual_acquisition_trace.json",
            acquisition_trace(summaries),
        )
    common.write_json(
        destination / "results.json",
        {
            "version": version.name,
            "protocol_freeze_sha256": protocol,
            "release_status": status,
            "summaries": summaries,
            "earlier_calibration": load(
                common.ROOT / "evaluation/calibration/summary.json"
            ),
            "latest_human_feedback": feedback,
            **({"feedback_requirements": requirements} if appearance else {}),
        },
    )
    for name in ("review.js", "review.css"):
        shutil.copy2(common.ROOT / name, destination / name)
    shutil.copy2(
        common.ROOT / "astra_native_tile_probe/analysis.json",
        destination / "astra_visual_analysis.json",
    )
    shutil.copy2(STORE / "source/imsauth.js", destination / "imsauth.js")
    common.write_json(
        STORE / "build_receipt.json",
        {
            "version": version.name,
            "protocol_freeze_sha256": protocol,
            "auth_sha256": common.sha(destination / "imsauth.js"),
            "files": {
                path.name: common.sha(path)
                for path in destination.iterdir()
                if path.is_file()
            },
            "calibration_only": calibration_only,
            "original_remote_report_unchanged": True,
            "publication_prefix": PREFIX,
        },
    )


def publish():
    from botocore.exceptions import ClientError

    client = s3_client()
    receipt = load(STORE / "build_receipt.json")
    if receipt.get("publication_prefix", PREFIX) != PREFIX:
        raise ValueError("Build belongs to another publication prefix")
    receipt_path = STORE / "publication_receipt.json"
    previous = (
        {row["url"]: row for row in load(receipt_path)["objects"]}
        if receipt_path.exists()
        else {}
    )
    written = []
    names = sorted(
        receipt["files"],
        key=lambda name: (name.endswith(".html"), name == "index.html", name),
    )
    for name in names:
        digest = receipt["files"][name]
        path = STORE / "public" / name
        if common.sha(path) != digest:
            raise ValueError("Report changed since build")
        body = path.read_bytes()
        content_type = {
            ".html": "text/html",
            ".js": "application/javascript",
            ".css": "text/css",
            ".json": "application/json",
        }[path.suffix]
        key = PREFIX + name
        try:
            client.put_object(
                Bucket=BUCKET,
                Key=key,
                Body=body,
                ContentType=content_type,
                Metadata={"sha256": digest},
                IfNoneMatch="*",
            )
        except ClientError as error:
            if error.response["ResponseMetadata"]["HTTPStatusCode"] != 412:
                raise
            live = client.get_object(Bucket=BUCKET, Key=key)
            try:
                existing = live["Body"].read()
            finally:
                live["Body"].close()
            if existing != body:
                known = previous.get(BASE + key)
                if (
                    known is None
                    or common.hashlib.sha256(existing).hexdigest() != known["sha256"]
                ):
                    raise ValueError(
                        "Live report differs from the last owned publication"
                    )
                client.put_object(
                    Bucket=BUCKET,
                    Key=key,
                    Body=body,
                    ContentType=content_type,
                    Metadata={"sha256": digest},
                    IfMatch=live["ETag"],
                )
        response = client.get_object(Bucket=BUCKET, Key=key)
        try:
            actual = response["Body"].read()
        finally:
            response["Body"].close()
        if actual != body or response["ContentType"] != content_type:
            raise ValueError("Published bytes or content type differ")
        written.append({"url": BASE + key, "sha256": digest, "etag": response["ETag"]})
        known = {**previous, **{row["url"]: row for row in written}}
        common.write_json(
            STORE / "publication_receipt.json",
            {"objects": list(known.values()), "verified": False},
        )
    common.write_json(
        STORE / "publication_receipt.json", {"objects": written, "verified": True}
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("snapshot", "build", "publish"))
    parser.add_argument("--version-root", default=str(common.ROOT))
    parser.add_argument("--calibration-only", action="store_true")
    args = parser.parse_args()
    version = Path(args.version_root).resolve()
    configure(version)
    if args.command == "build":
        build(version, args.calibration_only)
    else:
        {"snapshot": snapshot, "publish": publish}[args.command]()


if __name__ == "__main__":
    main()
