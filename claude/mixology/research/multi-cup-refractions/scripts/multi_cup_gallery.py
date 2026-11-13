"""Multi-cup refraction refinement tab renderer for the shared gallery."""
from __future__ import annotations

import json
import shutil
from pathlib import Path


def _title(candidate_id: str) -> str:
    return candidate_id.split("_", 1)[1].replace("_", " ").title()


def render(run, project, esc, rel, figure, details):
    topic = project.parent / "multi-cup-refractions"
    root = run / "multi-cup-refractions"
    package = root / "prompt_package"
    package.mkdir(exist_ok=True)
    for name in ["SUMMARY.md", "cases.json", "iteration_journal.json"]:
        shutil.copy2(topic / name, package / name)
    for name in ["prompts", "scripts", "data"]:
        source = topic / name
        if source.exists():
            shutil.copytree(source, package / name, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__"))

    journal = json.loads((topic / "iteration_journal.json").read_text())
    entries = journal["entries"]
    records = {
        p.parent.name: json.loads(p.read_text())
        for p in (root / "runs").glob("*/record.json")
    }
    benchmark = run / "runs/v3corrected_group_clean/output.png"
    bad_trio = run / "combined/runs/v1_trio_orange_front/output.png"
    bad_five = run / "combined/runs/v1_five_staggered/output.png"

    content = ['''<section id="multi-cup-refractions" role="tabpanel" aria-labelledby="multi-cup-refractions-tab" hidden>
      <section class="notice"><h2>Multi-cup refractions · morphology refinement</h2>
      <p>The target is a compact bright focal concentration with a few irregular, tapering outward branches,
      rendered as photographic transmitted light—not literal lightning, mesh, veins, waves, a starburst or global glow.</p>
      <p><b>Outcome at the fixed ceiling:</b> 20 of 20 candidate image-generation CLI jobs completed.
      The three-cup stop criterion passed at iteration 9. No five-cup candidate passed every essential gate;
      iteration 12 is the strongest five-cup compromise, not an approval or solved recipe.</p>
      <p>Every iteration is retained below in generation order with all generator inputs, exact prompts,
      settings, hashes, and its independent fresh-context Astra-high critique.</p>
      <p><a href="../multi-cup-refractions/prompt_package/SUMMARY.md">Findings and limitations</a> ·
      <a href="../multi-cup-refractions/prompt_package/iteration_journal.json">Machine-readable iteration journal</a> ·
      <a href="../multi-cup-refractions/prompt_package/cases.json">Frozen experiment design</a></p>
      <p class="small">Image model: exact GPT Image 2.5 Sunburst through Foundry-vended direct OpenAI credentials.
      Judge: actual returned GPT-6 Astra, Responses API, high reasoning. The image count is a CLI job/invocation count;
      the unchanged CLI uses SDK defaults, so no exact wire-level POST count or absence of internal retry is claimed.</p></section>''']
    content.append('<section class="sku"><h2>Visual calibration</h2><div class="grid three">')
    content.append(figure(benchmark, "User-approved positive benchmark", "Morphology and photographic hierarchy only", "real"))
    content.append(figure(bad_trio, "Rejected three-cup example", "Uniform network / weak focal hierarchy", "real"))
    content.append(figure(bad_five, "Rejected five-cup example", "Repeated mesh / similarly weighted fields", "real"))
    content.append('</div><p class="small">Approval applies only to the supplied positive benchmark. No newly generated result is described as customer-approved.</p></section>')
    content.append('<section class="sku"><h2>Stop-rule result</h2><div class="grid two">')
    content.append(figure(root / "runs/i09_trio_floor_correction/output.png",
                          "Best three-cup · iteration 9", "Researcher stop-criterion pass; not customer approval", "generated"))
    content.append(figure(root / "runs/i12_five_global_focus_nostyle/output.png",
                          "Best five-cup · iteration 12", "Best compromise; irregular-branch gate fails", "generated"))
    content.append('</div><p class="review"><b>Remaining blocker:</b> retain iteration 12’s compact dominant focus and quiet fields while replacing its smooth X-like bands with sparse, locally splitting, rapidly tapering photographic branches—without restoring mesh or creating electrical streaks.</p></section>')

    catalog = {
        "multi_cup_calibration": [
            {"n": p.name, "s": p.stat().st_size, "p": rel(p)[3:]}
            for p in [benchmark, bad_trio, bad_five]
        ]
    }
    for entry in entries:
        cid = entry["candidate_id"]
        record = records[cid]
        folder = root / "runs" / cid
        judge = json.loads((folder / "judge.json").read_text())
        judge_request = json.loads((folder / "judge_request.json").read_text())
        outcome = judge["output"]
        meta = judge["response_meta"]
        is_best = cid in {journal["best_trio"], journal["best_five"]}
        status = "PASS — all essential gates" if outcome["overall_pass"] else "Does not pass all essential gates"
        content.append(f'<article class="sku mcr-run{" recommended" if is_best else ""}" id="mcr-{esc(cid)}">')
        content.append(f'<div class="sku-head"><div><p class="eyebrow">Iteration {entry["generation_number"]:02d} · {esc(record["arrangement"])} · {esc(record["pipeline"])}</p><h2>{esc(_title(cid))}</h2></div><span class="badge">{esc(status)}</span></div>')
        content.append(f'<p class="user-prompt">User prompt: {esc(record["user_prompt"])}</p>')
        content.append(f'<p class="small">Style input: {esc(record["style"])} · Image job {entry["generation_number"]}/20 · {esc(record["image_model"])} · {record["image_seconds"]:.1f} s</p>')
        content.append(f'<h3>Generator inputs · ordered · {len(record["input_images"])} image(s)</h3><div class="grid composition-inputs" style="--input-count:{len(record["input_images"])}">')
        items = []
        for index, item in enumerate(record["input_images"], 1):
            path = Path(item["path"])
            content.append(figure(path, f'Generator input {index}', item["label"]))
            items.append({"n": path.name, "s": path.stat().st_size, "p": rel(path)[3:]})
        content.append('</div><div class="grid composition-output">')
        output = Path(record["output"])
        content.append(figure(output, f'Generated candidate · iteration {entry["generation_number"]}',
                              f'{record["output_dimensions"][0]} × {record["output_dimensions"][1]} · SHA-256 {record["output_sha256"]}', "generated"))
        content.append('</div>')
        items.append({"n": cid + " output", "s": output.stat().st_size, "p": rel(output)[3:]})

        gates = outcome["gate_results"]
        gate_labels = {
            "focal_hierarchy": "Focal hierarchy", "irregular_tapering_branches": "Irregular branches",
            "photographic_transmission": "Photographic optics", "no_dominant_network": "No dominant network",
            "subject_fidelity": "Subject fidelity", "color_attribution": "Color attribution",
            "coherent_direction": "Coherent direction",
        }
        tags = ''.join(f'<span class="tag">{esc(gate_labels[k])}: {"PASS" if v["pass"] else "FAIL"}</span>' for k, v in gates.items())
        content.append(f'<p>{tags}</p><p class="review"><b>Independent Astra-high result:</b> {esc(status)}. {esc(outcome["dominant_failure"])}</p>')
        content.append(details("Gate-by-gate visual evidence", json.dumps(gates, indent=2, ensure_ascii=False), is_best))
        content.append(details("Full independent critique · advisory", json.dumps(outcome, indent=2, ensure_ascii=False)))
        content.append(details("GPT system prompt · exact", record["system_prompt"]))
        content.append(details("GPT-generated image-edit prompt · exact", record["image_prompt"]))
        content.append(details("Generation settings, ordered image roles, hashes and provenance",
                               json.dumps({k: v for k, v in record.items() if k not in ["system_prompt", "image_prompt"]}, indent=2, ensure_ascii=False)))
        content.append(details("Independent judge request · exact instructions and ordered image inputs",
                               json.dumps(judge_request, indent=2, ensure_ascii=False)))
        content.append(details("Independent judge returned model/status/request metadata",
                               json.dumps(meta, indent=2, ensure_ascii=False)))
        judge_links = []
        for item in judge_request["images"]:
            path = Path(item["path"])
            judge_links.append(f'<a href="{esc(rel(path))}" target="_blank">{esc(item["label"])}</a>')
            items.append({"n": path.name, "s": path.stat().st_size, "p": rel(path)[3:]})
        content.append('<p class="small"><b>Ordered judge image inputs:</b> ' + ' · '.join(judge_links) + '</p>')
        evidence_files = [folder / name for name in ["record.json", "image_request.json", "rewriter_request.json", "rewriter_response.json", "judge_request.json", "judge.json"] if (folder / name).exists()]
        content.append('<p class="small"><b>Machine-readable evidence:</b> ' + ' · '.join(f'<a href="{esc(rel(p))}">{esc(p.name)}</a>' for p in evidence_files) + '</p>')
        content.append('</article>')
        # De-duplicate catalog entries without losing first-seen input order.
        seen = set()
        catalog["multi_cup_" + cid] = [item for item in items if not (item["p"] in seen or seen.add(item["p"]))]

    content.append('<section class="method"><h2>Interpretation limits</h2><ul><li>The paired controls support task load as a contributor to arrangement and direction drift, but not as the sole cause of mesh morphology.</li><li>The exact benchmark as a style input was not sufficient; it can reproduce subordinate mesh without reproducing brightness hierarchy.</li><li>Only two exact-prompt repeats were made, so stochastic variance and scene crowding remain confounded.</li><li>The strongest trio is an explicit three-stage result: neutral composition → V3-derived relight → floor-light topology correction.</li><li>The five-cup case did not meet the stop rule before the 20-image ceiling.</li></ul></section>')
    content.append('</section>')
    return '\n'.join(content), catalog
