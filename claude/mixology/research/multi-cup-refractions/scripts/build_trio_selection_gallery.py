#!/usr/bin/env python3
"""Build the standalone three-cup, two-stage iteration selection gallery."""

from __future__ import annotations

import hashlib
import html
import json
import shutil
from pathlib import Path


PROJECT = Path("/home/colligo/hs_scripts/claude/mixology")
DATA = Path("/home/colligo/mixology_data/refraction_research_2026-10-19")
RUNS = DATA / "multi-cup-refractions/runs"
OUT = DATA / "trio-two-stage-selection"
GALLERY = OUT / "gallery"
TEMPLATE_IMS = Path(
    "/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/"
    "research/generation/smoke_2026-10-07/gallery/imsauth.js"
)

STRICT_IDS = [
    "i02_trio_two_stage_origstyle",
    "i05_trio_two_stage_benchmark",
    "i07_trio_two_stage_focusclause",
]
FOLLOWUP_ID = "i09_trio_floor_correction"
CONTEXT_ID = "i01_trio_one_stage_origstyle"

SHORT_LABELS = {
    "i02_trio_two_stage_origstyle": "Iteration 2 · original style reference",
    "i05_trio_two_stage_benchmark": "Iteration 5 · corrected V3 benchmark",
    "i07_trio_two_stage_focusclause": "Iteration 7 · corrected V3 + focus clause",
    "i09_trio_floor_correction": "Iteration 9 · third-stage floor correction",
    "i01_trio_one_stage_origstyle": "Iteration 1 · one-stage context",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def ensure_copy(source: Path, destination: Path, expected_sha: str | None = None) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    actual = sha256(source)
    if expected_sha and actual != expected_sha:
        raise RuntimeError(f"Source hash mismatch: {source}\n{actual} != {expected_sha}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if sha256(destination) != actual:
            raise RuntimeError(f"Refusing to overwrite different artifact: {destination}")
        return
    shutil.copy2(source, destination)


def write_generated(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_run(candidate_id: str) -> dict:
    run = RUNS / candidate_id
    record = json.loads((run / "record.json").read_text(encoding="utf-8"))
    judge = json.loads((run / "judge.json").read_text(encoding="utf-8"))
    if record["candidate_id"] != candidate_id or record["status"] != "complete":
        raise RuntimeError(f"Incomplete or mismatched record: {run}")
    output = Path(record["output"])
    if sha256(output) != record["output_sha256"]:
        raise RuntimeError(f"Output hash mismatch: {output}")
    return {"id": candidate_id, "run": run, "record": record, "judge": judge}


def asset_name(path: Path, digest: str) -> str:
    return f"{digest[:12]}_{path.name}"


def copy_inputs_and_outputs(runs: list[dict]) -> dict[str, str]:
    source_to_rel: dict[str, str] = {}
    for item in runs:
        record = item["record"]
        output = Path(record["output"])
        output_rel = f"candidates/{item['id']}/output{output.suffix.lower()}"
        ensure_copy(output, OUT / output_rel, record["output_sha256"])
        source_to_rel[str(output)] = output_rel

        for filename in (
            "record.json",
            "judge.json",
            "judge_request.json",
            "system_prompt.md",
            "user_prompt.txt",
            "image_prompt.txt",
        ):
            source = item["run"] / filename
            if source.exists():
                ensure_copy(source, OUT / f"candidates/{item['id']}/{filename}")

    for item in runs:
        for source_record in item["record"]["input_images"]:
            source = Path(source_record["path"])
            source_key = str(source)
            if source_key in source_to_rel:
                continue
            name = asset_name(source, source_record["sha256"])
            rel = f"assets/{name}"
            ensure_copy(source, OUT / rel, source_record["sha256"])
            source_to_rel[source_key] = rel

    return source_to_rel


def image_figure(src: str, caption: str, role: str = "") -> str:
    return (
        '<figure class="image-card">'
        f'<button class="image-button" type="button" data-lightbox="../{html.escape(src)}" '
        f'aria-label="Open {html.escape(caption)} full size">'
        f'<img src="../{html.escape(src)}" alt="{html.escape(caption)}" loading="lazy"></button>'
        f'<figcaption><span>{html.escape(caption)}</span>'
        f'{f"<small>{html.escape(role)}</small>" if role else ""}</figcaption></figure>'
    )


def score_chips(judge_output: dict) -> str:
    scores = judge_output["scores"]
    return "".join(
        f'<span class="score"><b>{html.escape(key.title())}</b> {value}/5</span>'
        for key, value in scores.items()
    )


def prompt_block(record: dict, candidate_id: str) -> str:
    return f"""
      <details class="prompts">
        <summary>Exact prompts and run settings</summary>
        <div class="prompt-stack">
          <section><h4>User prompt</h4><pre>{html.escape(record['user_prompt'])}</pre></section>
          <section><h4>Final image-edit prompt</h4><pre>{html.escape(record['image_prompt'])}</pre></section>
          <section><h4>System prompt</h4><pre>{html.escape(record['system_prompt'])}</pre></section>
          <section><h4>Generation</h4><p><code>{html.escape(record['image_model'])}</code> ·
            <code>{html.escape(record['image_settings']['size'])}</code> ·
            quality <code>{html.escape(record['image_settings']['quality'])}</code></p>
            <p class="artifact-links"><a href="../candidates/{candidate_id}/record.json">record.json</a>
            <a href="../candidates/{candidate_id}/judge.json">judge.json</a>
            <a href="../candidates/{candidate_id}/judge_request.json">judge request</a></p>
          </section>
        </div>
      </details>
    """


def strict_card(item: dict, source_to_rel: dict[str, str], number: int) -> str:
    record = item["record"]
    judged = item["judge"]["output"]
    output_rel = source_to_rel[record["output"]]
    inputs = "".join(
        image_figure(
            source_to_rel[source["path"]],
            f"Input {index}",
            source["label"],
        )
        for index, source in enumerate(record["input_images"], 1)
    )
    pass_class = "pass" if judged["overall_pass"] else "fail"
    verdict = "Judge pass" if judged["overall_pass"] else "Judge did not pass"
    return f"""
    <article class="candidate strict-candidate" id="{item['id']}" data-candidate="{item['id']}">
      <header class="candidate-head">
        <div><p class="eyebrow">Strict two-stage candidate {number}</p>
          <h2>{html.escape(SHORT_LABELS[item['id']])}</h2></div>
        <button class="pick-button" type="button" data-pick="{item['id']}" data-label="{html.escape(SHORT_LABELS[item['id']])}">Pick this iteration</button>
      </header>
      <div class="compare-grid">
        <div class="input-grid">{inputs}</div>
        {image_figure(output_rel, SHORT_LABELS[item['id']] + ' output', 'Generated output')}
      </div>
      <div class="assessment">
        <div class="verdict {pass_class}">{verdict}</div>
        <div class="scores">{score_chips(judged)}</div>
        <p><b>Dominant issue:</b> {html.escape(judged['dominant_failure'])}</p>
        <p><b>Benchmark match:</b> {html.escape(judged['benchmark_match'])}</p>
        <p><b>Smallest next change:</b> {html.escape(judged['next_smallest_change'])}</p>
      </div>
      {prompt_block(record, item['id'])}
    </article>
    """


def supplementary_card(item: dict, source_to_rel: dict[str, str], kind: str) -> str:
    record = item["record"]
    judged = item["judge"]["output"]
    output_rel = source_to_rel[record["output"]]
    inputs = "".join(
        image_figure(source_to_rel[source["path"]], f"Input {index}", source["label"])
        for index, source in enumerate(record["input_images"], 1)
    )
    pass_class = "pass" if judged["overall_pass"] else "fail"
    verdict = "Judge pass" if judged["overall_pass"] else "Judge did not pass"
    return f"""
    <article class="candidate supplementary" id="{item['id']}">
      <header class="candidate-head"><div><p class="eyebrow">{html.escape(kind)}</p>
        <h2>{html.escape(SHORT_LABELS[item['id']])}</h2></div></header>
      <div class="compare-grid"><div class="input-grid">{inputs}</div>
        {image_figure(output_rel, SHORT_LABELS[item['id']] + ' output', 'Generated output')}</div>
      <div class="assessment"><div class="verdict {pass_class}">{verdict}</div>
        <div class="scores">{score_chips(judged)}</div>
        <p><b>Dominant issue:</b> {html.escape(judged['dominant_failure'])}</p>
        <p><b>Benchmark match:</b> {html.escape(judged['benchmark_match'])}</p>
        <p><b>Smallest next change:</b> {html.escape(judged['next_smallest_change'])}</p></div>
      {prompt_block(record, item['id'])}
    </article>
    """


def build_html(runs: dict[str, dict], source_to_rel: dict[str, str]) -> str:
    strict = [runs[candidate_id] for candidate_id in STRICT_IDS]
    overview_figures = "".join(
        image_figure(
            source_to_rel[item["record"]["output"]],
            SHORT_LABELS[item["id"]],
            "Strict two-stage candidate",
        )
        for item in strict
    )
    strict_cards = "".join(
        strict_card(item, source_to_rel, number)
        for number, item in enumerate(strict, 1)
    )
    followup = supplementary_card(
        runs[FOLLOWUP_ID], source_to_rel, "Three-stage follow-up · not a strict two-stage candidate"
    )
    context = supplementary_card(
        runs[CONTEXT_ID], source_to_rel, "One-stage baseline · context only"
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mixology · Three-cup two-stage picker</title>
  <link rel="stylesheet" href="style.css">
  <script src="https://auth-stg1.services.adobe.com/imslib/imslib.js"></script>
  <script defer src="imsauth.js"></script>
  <script defer src="data.js"></script>
  <script defer src="main.js"></script>
</head>
<body>
  <div id="loading">Loading secure review…</div>
  <main id="content" class="hidden">
    <header class="hero">
      <div class="hero-copy"><p class="eyebrow">Mixology refraction research</p>
        <h1>Three-cup · two-stage iteration picker</h1>
        <p class="lede">Choose among the three strict two-stage outputs below. All use the same neutral three-cup composition as the edit target. Iteration 9 is shown separately because it adds a third correction stage.</p>
      </div>
      <div id="ims" class="ims"></div>
    </header>

    <nav class="jump-nav" aria-label="Review sections">
      <a href="#strict-comparison">Strict two-stage</a>
      <a href="#follow-up">3-stage follow-up</a>
      <a href="#context">1-stage context</a>
    </nav>

    <section class="selection-banner" id="selection-banner" aria-live="polite">
      <span>No iteration selected yet.</span>
      <button id="copy-selection" type="button" disabled>Copy selection</button>
      <button id="clear-selection" type="button" disabled>Clear</button>
    </section>

    <section class="section" id="strict-comparison">
      <div class="section-head"><div><p class="eyebrow">Selection set</p><h2>Strict two-stage outputs</h2></div>
        <p>Click any image to inspect it full-size. The independent judge scores are advisory; the visual choice is yours.</p></div>
      <div class="overview-grid">{overview_figures}</div>
      <div class="score-table-wrap"><table><thead><tr><th>Iteration</th><th>Style reference</th><th>Morphology</th><th>Fidelity</th><th>Color</th><th>Direction</th><th>Judge</th></tr></thead>
      <tbody>
        <tr><td><a href="#i02_trio_two_stage_origstyle">2</a></td><td>Original customer example 027</td><td>2/5</td><td>5/5</td><td>5/5</td><td>5/5</td><td>Did not pass</td></tr>
        <tr><td><a href="#i05_trio_two_stage_benchmark">5</a></td><td>Corrected V3 positive benchmark</td><td>1/5</td><td>4/5</td><td>4/5</td><td>5/5</td><td>Did not pass</td></tr>
        <tr><td><a href="#i07_trio_two_stage_focusclause">7</a></td><td>Corrected V3 + explicit focus clause</td><td>2/5</td><td>5/5</td><td>5/5</td><td>5/5</td><td>Did not pass</td></tr>
      </tbody></table></div>
      <p class="note">“Positive benchmark” means the morphology reference Hooman selected for this research. It does not imply customer approval.</p>
      <div class="candidate-stack">{strict_cards}</div>
    </section>

    <section class="section separated" id="follow-up">
      <div class="section-head"><div><p class="eyebrow">Separate result</p><h2>Third-stage correction</h2></div>
        <p>This starts from iteration 7 and edits only the floor-light pattern. It passed the independent visual gates, but it is not eligible if the decision is strictly limited to two stages.</p></div>
      {followup}
    </section>

    <section class="section separated" id="context">
      <details class="context-details"><summary>Show one-stage baseline for context</summary>{context}</details>
    </section>

    <footer><p>Generated from immutable run records on 2026-10-20. Outputs are research candidates, not customer-approved assets.</p></footer>
  </main>
  <dialog id="lightbox"><button id="lightbox-close" type="button" aria-label="Close">×</button><img id="lightbox-image" alt="Full-size review image"></dialog>
  <script>document.addEventListener("DOMContentLoaded",()=>initializeIMS());</script>
</body>
</html>
"""


STYLE = r"""
:root{--ink:#171613;--muted:#6e6a62;--paper:#f5f2eb;--card:#fff;--line:#d9d3c8;--accent:#d84c32;--accent2:#257b69;--soft:#ebe5d9;--shadow:0 16px 50px rgba(40,32,22,.09)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}button,a{font:inherit}a{color:#185f54}a:hover{color:var(--accent)}.hidden{display:none!important}#loading{min-height:100vh;display:grid;place-items:center;color:var(--muted);letter-spacing:.03em}.hero{padding:46px clamp(20px,5vw,76px) 32px;display:flex;gap:32px;align-items:flex-start;justify-content:space-between;background:#1e1d19;color:#fff}.hero-copy{max-width:900px}.hero h1{font:600 clamp(38px,6vw,76px)/.98 Georgia,serif;margin:.18em 0}.lede{font-size:18px;max-width:780px;color:#ded8cd}.eyebrow{text-transform:uppercase;letter-spacing:.13em;font-size:12px;font-weight:750;color:var(--accent);margin:0 0 7px}.hero .eyebrow{color:#ff8b70}.ims{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end;font-size:12px;color:#ddd}.ims-button,.pick-button,.selection-banner button{border:1px solid currentColor;background:transparent;border-radius:999px;padding:8px 13px;cursor:pointer}.ims-button{color:#fff}.jump-nav{position:sticky;top:0;z-index:10;display:flex;gap:8px;padding:10px clamp(20px,5vw,76px);background:rgba(245,242,235,.94);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}.jump-nav a{text-decoration:none;color:var(--ink);padding:6px 10px;border-radius:999px}.jump-nav a:hover{background:var(--soft)}.selection-banner{display:flex;align-items:center;gap:12px;padding:14px clamp(20px,5vw,76px);background:#fff7d9;border-bottom:1px solid #e3d28e}.selection-banner span{font-weight:700;margin-right:auto}.selection-banner button:disabled{opacity:.4;cursor:not-allowed}.section{padding:52px clamp(20px,5vw,76px)}.section-head{display:flex;align-items:end;justify-content:space-between;gap:30px;margin-bottom:22px}.section-head h2{font:600 clamp(28px,4vw,48px)/1.05 Georgia,serif;margin:0}.section-head>p{max-width:570px;color:var(--muted);margin:0}.overview-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.image-card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;margin:0;box-shadow:var(--shadow)}.image-button{display:block;width:100%;padding:0;border:0;background:#ece9e2;cursor:zoom-in}.image-button img{display:block;width:100%;height:auto;aspect-ratio:3/2;object-fit:contain}.image-card figcaption{padding:10px 12px;display:flex;gap:6px;flex-direction:column;font-weight:700}.image-card figcaption small{color:var(--muted);font-weight:450;line-height:1.35}.score-table-wrap{overflow:auto;margin:22px 0 8px;border:1px solid var(--line);border-radius:12px;background:#fff}table{border-collapse:collapse;width:100%;min-width:720px}th,td{padding:11px 13px;text-align:left;border-bottom:1px solid var(--line)}th{font-size:12px;text-transform:uppercase;letter-spacing:.06em;background:#ede8dd}.note{color:var(--muted);font-size:13px}.candidate-stack{display:grid;gap:36px;margin-top:42px}.candidate{scroll-margin-top:75px;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:clamp(18px,3vw,34px);box-shadow:var(--shadow)}.candidate.is-selected{outline:4px solid #f1a33d;outline-offset:3px}.candidate-head{display:flex;justify-content:space-between;align-items:center;gap:18px;margin-bottom:18px}.candidate-head h2{font:600 clamp(24px,3vw,38px)/1.08 Georgia,serif;margin:0}.pick-button{border-color:var(--accent);color:var(--accent);white-space:nowrap;font-weight:750}.pick-button:hover,.pick-button.is-selected{background:var(--accent);color:#fff}.compare-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start}.input-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.input-grid:has(.image-card:nth-child(4)){grid-template-columns:repeat(2,minmax(0,1fr))}.assessment{margin-top:18px;padding:16px 18px;border-radius:12px;background:#f5f2eb}.assessment p{margin:.55em 0}.verdict{display:inline-block;border-radius:999px;padding:5px 10px;font-weight:800;font-size:12px;text-transform:uppercase;letter-spacing:.05em}.verdict.pass{background:#dff3e9;color:#17644f}.verdict.fail{background:#f3e4e0;color:#8d3425}.scores{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0}.score{padding:5px 9px;background:#fff;border:1px solid var(--line);border-radius:999px;font-size:12px}.prompts{margin-top:18px;border-top:1px solid var(--line);padding-top:14px}.prompts summary,.context-details>summary{font-weight:800;cursor:pointer}.prompt-stack{display:grid;gap:12px;margin-top:14px}.prompt-stack section{border:1px solid var(--line);border-radius:10px;padding:14px}.prompt-stack h4{margin:0 0 8px}.prompt-stack pre{white-space:pre-wrap;overflow-wrap:anywhere;margin:0;font:12px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace;color:#393631}.artifact-links{display:flex;gap:12px;flex-wrap:wrap}.separated{border-top:6px solid #ddd6ca}.supplementary{margin-top:22px}.context-details>summary{font-size:22px}.context-details[open]>summary{margin-bottom:22px}footer{padding:30px clamp(20px,5vw,76px);border-top:1px solid var(--line);color:var(--muted)}dialog{width:min(96vw,1700px);max-width:none;padding:0;border:0;border-radius:12px;background:#151515;box-shadow:0 30px 90px rgba(0,0,0,.55)}dialog::backdrop{background:rgba(0,0,0,.84)}dialog img{display:block;width:100%;height:auto;max-height:90vh;object-fit:contain}#lightbox-close{position:absolute;right:10px;top:8px;width:40px;height:40px;border:0;border-radius:50%;background:rgba(0,0,0,.65);color:#fff;font-size:27px;cursor:pointer}
@media(max-width:900px){.hero,.section-head,.candidate-head{align-items:flex-start;flex-direction:column}.overview-grid{grid-template-columns:1fr}.compare-grid{grid-template-columns:1fr}.jump-nav{overflow:auto}.pick-button{width:100%}.ims{justify-content:flex-start}.selection-banner{position:relative}.input-grid{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.hero{padding-top:30px}.section{padding-top:36px;padding-bottom:36px}.input-grid{grid-template-columns:1fr}.selection-banner{align-items:stretch;flex-direction:column}.selection-banner span{margin:0}.selection-banner button{width:100%}}
"""


MAIN_JS = r"""
const STORAGE_KEY = "mixology-trio-two-stage-selection";
function onAuthReady(){
  const banner=document.getElementById("selection-banner");
  const bannerText=banner.querySelector("span");
  const copyButton=document.getElementById("copy-selection");
  const clearButton=document.getElementById("clear-selection");
  const pickButtons=[...document.querySelectorAll("[data-pick]")];
  function renderSelection(){
    const picked=localStorage.getItem(STORAGE_KEY)||"";
    document.querySelectorAll("[data-candidate]").forEach(card=>card.classList.toggle("is-selected",card.dataset.candidate===picked));
    pickButtons.forEach(button=>{const chosen=button.dataset.pick===picked;button.classList.toggle("is-selected",chosen);button.textContent=chosen?"Selected":"Pick this iteration";});
    const selected=pickButtons.find(button=>button.dataset.pick===picked);
    bannerText.textContent=selected?`Selected: ${selected.dataset.label} (${picked})`:"No iteration selected yet.";
    copyButton.disabled=!selected; clearButton.disabled=!selected;
  }
  pickButtons.forEach(button=>button.addEventListener("click",()=>{localStorage.setItem(STORAGE_KEY,button.dataset.pick);renderSelection();banner.scrollIntoView({behavior:"smooth",block:"center"});}));
  clearButton.addEventListener("click",()=>{localStorage.removeItem(STORAGE_KEY);renderSelection();});
  copyButton.addEventListener("click",async()=>{const picked=localStorage.getItem(STORAGE_KEY);const selected=pickButtons.find(button=>button.dataset.pick===picked);if(!selected)return;const text=`Mixology three-cup two-stage selection: ${selected.dataset.label} (${picked})`;await navigator.clipboard.writeText(text);copyButton.textContent="Copied";setTimeout(()=>copyButton.textContent="Copy selection",1200);});
  const dialog=document.getElementById("lightbox");const fullImage=document.getElementById("lightbox-image");
  document.querySelectorAll("[data-lightbox]").forEach(button=>button.addEventListener("click",()=>{fullImage.src=button.dataset.lightbox;fullImage.alt=button.getAttribute("aria-label");dialog.showModal();}));
  document.getElementById("lightbox-close").addEventListener("click",()=>dialog.close());
  dialog.addEventListener("click",event=>{if(event.target===dialog)dialog.close();});
  renderSelection();
}
"""


def main() -> None:
    candidate_ids = [*STRICT_IDS, FOLLOWUP_ID, CONTEXT_ID]
    loaded = {candidate_id: load_run(candidate_id) for candidate_id in candidate_ids}
    source_to_rel = copy_inputs_and_outputs(list(loaded.values()))

    GALLERY.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEMPLATE_IMS, GALLERY / "imsauth.js") if not (GALLERY / "imsauth.js").exists() else None
    if sha256(GALLERY / "imsauth.js") != sha256(TEMPLATE_IMS):
        raise RuntimeError("imsauth.js differs from the known-working template")

    manifest = {
        "title": "Mixology three-cup two-stage selection",
        "strict_candidates": STRICT_IDS,
        "followup": FOLLOWUP_ID,
        "context": CONTEXT_ID,
        "candidate_records": {
            candidate_id: {
                "label": SHORT_LABELS[candidate_id],
                "output": source_to_rel[loaded[candidate_id]["record"]["output"]],
                "output_sha256": loaded[candidate_id]["record"]["output_sha256"],
                "pipeline": loaded[candidate_id]["record"]["pipeline"],
                "scores": loaded[candidate_id]["judge"]["output"]["scores"],
                "overall_pass": loaded[candidate_id]["judge"]["output"]["overall_pass"],
            }
            for candidate_id in candidate_ids
        },
    }
    write_generated(GALLERY / "index.html", build_html(loaded, source_to_rel))
    write_generated(GALLERY / "style.css", STYLE.strip() + "\n")
    write_generated(GALLERY / "main.js", MAIN_JS.strip() + "\n")
    write_generated(
        GALLERY / "data.js",
        "window.REVIEW_DATA = " + json.dumps(manifest, indent=2, ensure_ascii=False) + ";\n",
    )
    write_generated(OUT / "manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"Built {GALLERY}")
    print(f"Strict candidates: {len(STRICT_IDS)}; follow-up: 1; context: 1")


if __name__ == "__main__":
    main()
