"""Reproduce the isolated V3.1 rubric/schema delta from hash-recorded V3 sources."""
from __future__ import annotations

import difflib
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
V3 = ROOT.parent / "v3"
V2 = ROOT.parent / "v2"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_one(text, before, after):
    if text.count(before) != 1:
        raise ValueError(f"Expected one exact source passage: {before[:80]}")
    return text.replace(before, after, 1)


def replace_section(text, start, end, replacement):
    first = text.index(start)
    last = text.index(end, first)
    return text[:first] + replacement.strip() + "\n\n" + text[last:]


def main():
    metadata = json.loads((ROOT / "astra/attempt_1/metadata.json").read_text())
    if (metadata["model_returned"] != "gpt-6-astra" or metadata["finish_reason"] != "stop"
            or not (ROOT / "astra/attempt_1/output.md").read_text().strip()):
        raise RuntimeError("Substantive actual Astra consultation required before implementation")
    rules = json.loads((ROOT / "reviewed_rules.json").read_text())
    prompts = ROOT / "prompts"
    prompts.mkdir(exist_ok=True)
    transformations = []

    def save(source, destination, value):
        destination.parent.mkdir(exist_ok=True, parents=True)
        if destination.exists() and destination.read_text() != value and (ROOT / "protocol_freeze.json").exists():
            raise RuntimeError(f"Rebuild differs; preserve current implementation: {destination}")
        destination.write_text(value)
        diff = "".join(difflib.unified_diff(
            source.read_text().splitlines(keepends=True), value.splitlines(keepends=True),
            fromfile=str(source), tofile=str(destination)))
        diff_path = ROOT / "deltas" / f"{destination.parent.name}_{destination.name}.diff"
        diff_path.parent.mkdir(exist_ok=True)
        diff_path.write_text(diff)
        transformations.append({
            "source": str(source), "source_sha256": sha(source),
            "output": str(destination), "output_sha256": sha(destination),
            "diff": str(diff_path), "diff_sha256": sha(diff_path),
        })

    # Keep unrelated printer/contact/room-use criteria verbatim.
    source = V2 / "system_prompt.md"
    baseline = source.read_text()
    before = ("Judge this arrangement AS SHOWN. Do not imagine another chair outside the frame, "
              "move the visible chair in your explanation, suppose the device is temporarily on "
              "display, or invent a person who could approach from a different direction to excuse "
              "a visible problem. If a visible chair clearly belongs to this workstation, it is the "
              "user position to assess. A close crop with no visible seat/edge is uncertainty, not "
              "proof of bad placement and not proof of good access.")
    baseline = replace_one(baseline, before, rules["chair_relation"])
    baseline = replace_one(baseline, "a laptop away from its user",
                           "a laptop visibly inaccessible from its working edge")
    baseline = replace_section(baseline, "Laptop: the keyboard", "The person's approach,",
                               rules["laptop_access"] + "\n")
    baseline = replace_section(
        baseline, "3. orientation_alignment — 20% weight", "4. scale_perspective",
        "3. orientation_alignment — 20% weight\n" + rules["alignment"])
    baseline = replace_section(
        baseline, "4. scale_perspective — 15% weight", "5. contact_integration",
        "4. scale_perspective — 15% weight\n"
        + source.read_text().split("4. scale_perspective — 15% weight\n", 1)[1]
        .split("\n\n5. contact_integration", 1)[0] + "\n\n" + rules["geometry"])
    baseline = replace_one(
        baseline,
        "1 = A small cosmetic imperfection with natural use and alignment intact. Do NOT use 1 for a clearly misplaced device, diagonal mismatch, laptop away from its chair, blocked access or an implausible printer station.",
        "1 = A small optional refinement, slight edge offset or harmless perspective difference that leaves a believable usable arrangement. Do NOT use 1 for a consequential device/table rotation, clearly blocked use or materially impossible furniture construction.")
    baseline = replace_one(
        baseline,
        "2 = Clear unnatural placement that needs correction, even if use is physically possible. Explicit diagonal misalignment, a laptop noticeably too far from its actual seat, an unmotivated printer in the middle of a large wall-backed table, or a blocked usable work area belongs here or worse. This produces FAIL, not review.",
        "2 = A clear unnatural arrangement needing correction: consequential device/table rotation, genuinely excessive working-edge reach or obstruction, materially malformed table/chair construction, an unmotivated printer in the middle of a large wall-backed table, or blocked usable workspace. This produces FAIL, not review; chair pose/centering alone does not qualify.")
    baseline = baseline.replace(", chair_alignment_conflict", "")
    baseline = replace_one(
        baseline, "scale_perspective: implausible_scale, conflicting_perspective",
        "scale_perspective: implausible_scale, conflicting_perspective, malformed_support_furniture")
    baseline += "\n\n" + rules["mapping"] + "\n"
    save(source, prompts / "baseline.md", baseline)

    source = V3 / "system_prompt.md"
    compact = source.read_text()
    compact = replace_section(
        compact, "3. Device to person:", "\n\nPRINTERS",
        "3. Device to person: " + rules["chair_relation"])
    compact = replace_section(compact, "LAPTOPS\n", "ALIGNMENT AND PHYSICS",
                              "LAPTOPS\n" + rules["laptop_access"])
    compact = replace_section(
        compact, "ALIGNMENT AND PHYSICS\n", "SCENE COHERENCE",
        "ALIGNMENT AND PHYSICS\n" + rules["alignment"] + "\n\n" + rules["geometry"]
        + "\n\nCheck relative scale with depth in mind and weight-bearing contact. "
        "Report visible floating, sinking, detached shadows or impossible reflections. "
        "Soft shadows are valid. Product prominence and lack of a dark contact outline alone are not defects.")
    compact = compact.replace(", chair_alignment_conflict", "")
    compact = replace_one(
        compact, "product/support axes and associated furniture.",
        "consequential product/support-axis conflicts, not movable chair pose.")
    compact = replace_one(
        compact, "credible size, perspective and supporting furniture construction.",
        "credible size, perspective and visible table/chair construction.")
    compact += "\n\n" + rules["mapping"] + "\n"
    save(source, prompts / "compact.md", compact)

    for stage, relative in (
        ("proposal", "experiments/verify_additions/system_prompt.md"),
        ("independent", "experiments/independent_component_check/system_prompt.md"),
    ):
        source = V3 / relative
        text = source.read_text()
        if stage == "proposal":
            text = replace_one(
                text,
                "- Judge product/support alignment in 3D using corresponding width and depth edges, not raw image slopes, screens or raised trays. A clearly diagonal device/table relationship is material; ordinary perspective convergence is not.",
                "- " + rules["alignment"])
        else:
            text = replace_one(
                text,
                "- orientation_alignment: product/support/adjacent furniture axes should form a coherent arrangement in 3D; compare corresponding base width/depth edges, not screen/tray slopes. Check the actual product-to-seat relation as described above. Perspective convergence is normal. Rotated corner-facing placement or a clearly reversed working side is a defect.",
                "- orientation_alignment: " + rules["alignment"])
            text = replace_one(
                text,
                "- scale_perspective: believable product-to-furniture scale and consistent perspective; materially malformed supporting furniture is a defect.",
                "- scale_perspective: believable product-to-furniture scale and consistent perspective. "
                + rules["geometry"])
        text += ("\n\nV3.1 C-Tech clarification (apply to the requested components only):\n"
                 + rules["chair_relation"] + "\n" + rules["laptop_access"] + "\n"
                 + rules["geometry"] + "\n" + rules["mapping"] + "\n")
        save(source, prompts / f"{stage}.md", text)

    source = V3 / "scoring.py"
    save(source, ROOT / "scoring.py", source.read_text())
    source = V3 / "observation_schema.json"
    save(source, ROOT / "observation_schema.json", source.read_text())

    source = V2 / "data/visual_anchors.json"
    anchors = json.loads(source.read_text())
    for anchor in anchors["examples"]:
        if anchor["asset_id"] == "regression-userfail-row29-v13":
            anchor["guidance"] = (
                "Historical human failure example for excessive laptop reach, not a chair-pose "
                "or chair-centering rule. Under V3.1, inspect actual device distance from a usable "
                "working edge and visible obstruction. A movable chair's lateral position alone "
                "does not establish this defect; do not transfer the historical chair-alignment accusation.")
        elif anchor["asset_id"] == "regression-userfail-row09-v14":
            anchor["guidance"] += (
                " V3.1 clarification: confirm excessive working-edge reach/obstruction independently "
                "of the movable chair's current position; chair displacement alone is not a failure.")
    save(source, ROOT / "visual_anchors.json", json.dumps(anchors, indent=2) + "\n")

    provenance = {
        "baseline_lineage": "Selected V3 consensus ensemble, including its V2 exemplar branch.",
        "not_based_on": "V4/V4.x; no runtime, prompts or numerical geometry thresholds imported.",
        "astra_review": {
            "path": str(ROOT / "astra/attempt_1/output.md"),
            "sha256": sha(ROOT / "astra/attempt_1/output.md"), "metadata": metadata,
        },
        "git_head_at_build": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "transformations": transformations,
        "compatibility": (
            "Same five dimensions, weights, severity thresholds and decision functions. "
            "The exact V3 observation schema/code registry is retained for compatibility. "
            "V3.1's request protocol and rubric hashes identify the new semantics; runtime "
            "rejects new chair_alignment_conflict emission without rewriting any model output."),
    }
    (ROOT / "implementation_provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")


if __name__ == "__main__":
    main()
