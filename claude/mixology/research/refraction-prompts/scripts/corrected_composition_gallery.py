"""Render the independent corrected-input composition tab."""
from __future__ import annotations

import json
from pathlib import Path
import shutil


TAB_ID = "composition-corrected-inputs"
TAB_TITLE = "Group composition corrected inputs"


def render(run, project, esc, rel, figure, details):
    topic = project.parent / "group-composition-corrected-inputs"
    package = run / "composition-corrected-inputs/prompt_package"
    package.mkdir(parents=True, exist_ok=True)
    for name in ["SUMMARY.md", "cases.json", "generation_journal.json", "direct_reviews.json"]:
        shutil.copy2(topic / name, package / name)
    for name in ["prompts", "scripts", "data"]:
        shutil.copytree(
            topic / name,
            package / name,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__"),
        )

    records = [
        json.loads(path.read_text())
        for path in sorted((run / "composition-corrected-inputs/runs").glob("*/record.json"))
    ]
    order = list(json.loads((topic / "cases.json").read_text()))
    records.sort(key=lambda record: order.index(record["id"]))
    completed = sum(record["status"] == "complete" for record in records)
    if len(records) != 9 or completed != 9:
        raise RuntimeError(f"Expected nine completed corrected-input cases, got {completed}/{len(records)}")

    content = [f'''<section id="{TAB_ID}" role="tabpanel" aria-labelledby="{TAB_ID}-tab" hidden>
      <section class="notice"><h2>{TAB_TITLE}</h2>
      <p>Nine one-to-one composition reruns using the user-supplied common-cup source set. Existing Group composition outputs are preserved and shown only as separately labeled FAL-condition comparators.</p>
      <p><b>{completed} generated outputs · exactly one per active original case · composition only · no refractions.</b></p>
      <p><a href="../composition-corrected-inputs/prompt_package/SUMMARY.md">Method, findings and limits</a> ·
      <a href="../composition-corrected-inputs/prompt_package/data/input_manifest.json">Corrected input manifest</a> ·
      <a href="../composition-corrected-inputs/prompt_package/data/source_geometry.json">Projected source geometry</a> ·
      <a href="../composition-corrected-inputs/prompt_package/generation_journal.json">Bounded generation journal</a></p>
      <p class="small"><b>Provider confound:</b> original counterparts used fal.ai and an unexposed Astra effort/backend snapshot; these reruns use Foundry-vended direct OpenAI credentials and Astra high effort. Old/new differences cannot establish input-only causality. Manual source ratios are approximate 2D landmarks, not physical measurements.</p></section>''']
    content.append('''<section class="notice"><p><b>Direct finding:</b> all nine corrected-input outputs read as a tighter common cup family, especially at rims and molded bases. Eight preserve their requested slots; the V1 five-drink staggered case swaps the red and cola depth positions and is retained as the single authorized sample rather than silently revised.</p><p>The new sources are authoritative for cup and drink evidence. Internally generated arrangement examples are not model inputs and are not customer-approved geometry.</p></section>''')
    catalog = {}
    for record in records:
        rid = record["id"]
        folder = run / "composition-corrected-inputs/runs" / rid
        old = record["original_counterpart"]
        old_output = Path(old["output"])
        content.append(f'<article class="sku corrected-composition-run" id="corrected-composition-{esc(rid)}">')
        content.append(f'<p class="eyebrow">Corrected inputs · {esc(record["system_version"].upper())} · direct OpenAI · complete</p>')
        content.append(f'<h2>{esc(record.get("case", {}).get("description", record["case_id"]))}</h2>')
        content.append(f'<p class="user-prompt">User prompt: {esc(record["user_prompt"])}</p>')
        content.append(f'<p class="small provider-note">New output: exact <b>{esc(record["image_model"])}</b> through direct OpenAI; Astra rewrite and independent critique used <b>{esc(record["rewriter_model"])}</b> with effort high. Original comparison: {esc(old["id"])} · {esc(old["provider"])}. It was not sent to the generator.</p>')
        content.append(f'<h3>All corrected model inputs · ordered · {len(record["input_images"])} drinks</h3><div class="grid composition-inputs" style="--input-count:{len(record["input_images"])}">')
        key = "composition_corrected_" + rid
        catalog[key] = []
        for item in record["input_images"]:
            content.append(figure(item["path"], f'Input {item["image_index"]} · {item["identity"]}', item["role"]))
            path = Path(item["path"])
            catalog[key].append({"n": path.name, "s": path.stat().st_size, "p": rel(path)[3:]})
        content.append('</div><h3>Condition comparison · original FAL versus corrected-input direct output</h3><div class="grid composition-comparison">')
        content.append(figure(
            old_output,
            "Original-input output · FAL condition · comparison only",
            "Preserved historical counterpart. Different sources/provider/reasoning exposure; NOT a model input for this rerun.",
            "real",
        ))
        content.append(figure(
            record["output"],
            "Corrected-input output · direct OpenAI",
            f'{record["output_dimensions"]} · exact {record["image_model"]}',
            "generated",
        ))
        content.append("</div>")
        content.append('<p class="review"><b>Direct visual review:</b> ' + esc(record["visual_review"]) + '</p>')
        content.append(details("Independent Astra-high critique", (folder / "judge.json").read_text()))
        content.append(details("Independent critique request · exact", (folder / "judge_request.json").read_text()))
        content.append(details("GPT system prompt · exact", record["system_prompt"]))
        content.append(details("GPT-generated image-edit prompt actually sent · exact", record["image_prompt"]))
        content.append(details("Settings and provenance", json.dumps({
            key_: value for key_, value in record.items()
            if key_ not in ["system_prompt", "image_prompt"]
        }, indent=2, ensure_ascii=False)))
        for filename, label in [
            ("rewriter_request.json", "Astra rewrite request · exact"),
            ("rewriter_response.json", "Astra rewrite response metadata and text"),
            ("image_request.json", "Sunburst image request · exact"),
            ("image_submission.json", "Bounded image submission record"),
            ("image_response.json", "Image response metadata available from unchanged CLI"),
        ]:
            content.append(details(label, (folder / filename).read_text()))
        evidence = [path for path in sorted(folder.glob("*.json")) if path.name != "record.json"]
        content.append('<p class="small">Run evidence files: ' + ' · '.join(
            f'<a href="{esc(rel(path))}">{esc(path.name)}</a>' for path in evidence
        ) + '</p>')
        for path, name in [(old_output, old["id"] + " original FAL output"), (Path(record["output"]), rid + " direct output")]:
            catalog[key].append({"n": name, "s": path.stat().st_size, "p": rel(path)[3:]})
        content.append("</article>")
    content.append("</section>")
    return "\n".join(content), catalog
