import html
import json
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

FOUNDRY = "https://foundry-aws-corp.adobe.io/asset/"
_CSS = """body{font:13px system-ui;margin:16px}table{border-collapse:collapse}td,th{border:1px solid #ccc;
padding:4px;vertical-align:top}img.m{width:300px}img.r{width:70px;margin:1px}details{max-width:300px}
.err{color:#b00}"""


def render(rows, run_dir: Path, title: str) -> Path:
    e = html.escape
    labels: list[str] = []
    for r in rows:
        labels += [label for label, _ in r.baselines if label not in labels]
    head = "".join(f"<th>{e(label)}</th>" for label in labels) + "<th>GPT 2.5 (ours)</th><th>GPT 2.5 + ref grade match</th><th>Style refs</th>"
    body = []
    for r in rows:
        p = run_dir / "rows" / r.id / "result.json"
        res = json.loads(p.read_text()) if p.exists() else {"status": "pending"}
        srcs = dict(r.baselines)
        cells = "".join(
            f'<td><a href="{e(srcs[label])}"><img class=m loading=lazy src="{e(srcs[label])}"></a></td>'
            if label in srcs else "<td></td>" for label in labels)
        if res["status"] == "ok":
            ours = f'<a href="rows/{r.id}/ours.png"><img class=m loading=lazy src="rows/{r.id}/ours.png"></a>'
        else:
            ours = f'<span class=err>{e(res["status"])}: {e(str(res.get("error")))}</span>'
        graded = run_dir / "rows" / r.id / "ours_graded.png"
        direct = res.get("generation_mode") == "direct"
        graded_cell = (f'<span class=err>{e(res["grade_error"])}</span>' if res.get("grade_error") else
                       f'<a href="rows/{r.id}/ours_graded.png"><img class=m loading=lazy '
                       f'src="rows/{r.id}/ours_graded.png"></a>'
                       + ("<div>Whole-image tint/contrast match; changes product colors.</div>"
                          if res.get("grading", {}).get("scope") == "whole_image" else "")
                       if graded.exists() and (not direct or res.get("graded")) else
                       "<i>Not applied: no post-processing</i>" if direct else
                       f'<i class=err>{e(res["warning"])}</i>' if res.get("warning") else
                       "<i>not aligned/graded: product location not confident</i>" if res.get("locate") else "")
        grading = res.get("grading") or {}
        selection = grading.get("selection")
        if res.get("graded") and selection and not res.get("grade_error"):
            target = f'rows/{r.id}/{grading["reference_file"]}'
            graded_cell += (f'<div>Nearest grading reference: {e(selection["reference_id"])}'
                            f' · distance {selection["distance"]:.3f}'
                            f' · searched {selection["candidate_count"]} refs</div>'
                            f'<a href="{e(target)}"><img class=r loading=lazy src="{e(target)}"></a>')
        if direct:
            generation = (f'Reused raw from {e(res["source_generation_run"])} · 0 new image calls'
                          if res.get("postprocess_only") else
                          f'Direct generation · {res.get("image_calls", 0)} image call')
            ours += (f'<div>{generation}'
                     ' · geometry not validated'
                     + (f' · <a href="rows/{r.id}/gpt_1.png">raw GPT</a>'
                        if res["status"] == "ok" else "") + "</div>")
            if (run_dir / "rows" / r.id / "geometry_guide.png").exists():
                ours += f'<div><a href="rows/{r.id}/geometry_guide.png">Estimated geometry guide</a></div>'
            info = res.get("guide_info") or {}
            if "lens_35mm_equivalent_mm" in info:
                ours += (f'<div>Lens estimate: {info["lens_35mm_equivalent_mm"]:.1f}mm eq '
                         f'({e(info["lens_family"])}), not recovered metadata.</div>')
        elif res.get("attempts"):
            al = res.get("align") or {}
            ours += (f'<div>attempt {res.get("chosen_attempt")}/{len(res["attempts"])}'
                     + (f' · aligned (GPT scale {al.get("scale", 0):.2f}, upscale {al.get("upscale", 0):.2f}x)'
                        if res.get("aligned") else " · <b class=err>not aligned</b>")
                     + "".join(f' · <a href="rows/{r.id}/gpt_{n}.png">raw GPT {n}</a>'
                               for n in range(1, len(res["attempts"]) + 1)) + "</div>")
        ours += (f'<details><summary>prompt</summary>{e(str(res.get("prompt")))}</details>'
                 f'<div>{e(str(res.get("tone")))} · {e(str(res.get("content")))}</div>')
        refs = "".join(f'<img class=r loading=lazy src="rows/{r.id}/{f.name}" title="{e(f.name)}">'
                       for f in sorted((run_dir / "rows" / r.id).glob("ref_*")))
        body.append(f"<tr><td><b>{e(r.id)}</b><details><summary>user_prompt</summary>{e(r.user_prompt)}"
                    f"</details></td>{cells}<td>{ours}</td><td>{graded_cell}</td><td>{refs}</td></tr>")
    out = run_dir / "viewer.html"
    out.write_text(f"<!doctype html><meta charset=utf-8><title>{e(title)}</title><style>{_CSS}</style>"
                   f"<h2>{e(title)}</h2><table><tr><th>Row</th>{head}</tr>{''.join(body)}</table>")
    return out


def render_comparison(rows, run_dir: Path, asset_base_url: str, *,
                      graded_output_urls: dict[str, str] | None = None,
                      prompt_overrides: dict[str, str] | None = None) -> Path:
    """Compare products, generation references, prompts and outputs without technical details."""
    e = html.escape
    graded_output_urls = graded_output_urls or {}
    prompt_overrides = prompt_overrides or {}
    unknown_rows = (graded_output_urls.keys() | prompt_overrides.keys()) - {row.id for row in rows}
    if unknown_rows:
        raise ValueError(f"Unknown comparison output rows: {sorted(unknown_rows)}")
    labels = list(dict.fromkeys(label for row in rows for label, _ in row.baselines if label != "Input"))
    if not rows or not labels:
        raise ValueError("A comparison requires rows and baseline methods.")
    methods = ["Original product", *labels, "Style reference", "GPT Image 2.5 + grade match"]
    body = []
    for row in rows:
        d = run_dir / "rows" / row.id
        result = json.loads((d / "result.json").read_text())
        if (result["status"] != "ok" or not result.get("graded") or result.get("grade_error")
                or not (d / "ours_graded.png").is_file()):
            raise ValueError(f"No successful graded output for {row.id}.")
        if not (d / "hero.png").is_file():
            raise ValueError(f"No original product image for {row.id}.")
        refs = sorted(ref for ref in d.glob("ref_*") if ref.is_file())
        if not refs:
            raise ValueError(f"No generation style reference for {row.id}.")
        baselines = dict(row.baselines)
        if any(not baselines.get(label) for label in labels):
            raise ValueError(f"Missing comparison method for {row.id}.")
        row_url = f"{asset_base_url.rstrip('/')}/rows/{row.id}"
        default_output = f"{row_url}/ours_graded.png"
        output = graded_output_urls.get(row.id, default_output)
        if output != default_output and row.id not in prompt_overrides:
            raise ValueError(f"A replacement output requires its exact generation prompt: {row.id}.")
        final_prompt = prompt_overrides.get(row.id, result.get("prompt"))
        if not row.baseline_prompt.strip() or not isinstance(final_prompt, str) or not final_prompt.strip():
            raise ValueError(f"Missing HP12 rewritten input or final GPT2.5 prompt for {row.id}.")
        sources = [[f"{row_url}/hero.png"], *[[baselines[label]] for label in labels],
                   [f"{row_url}/{ref.name}" for ref in refs],
                   [output]]
        if any(urlsplit(src).scheme != "https" or not urlsplit(src).netloc
               for cell_sources in sources for src in cell_sources):
            raise ValueError("Comparison images require absolute HTTPS URLs.")
        cells = "".join(
            "<td>" + "".join(f'<a href="{e(src)}" target="_blank" rel="noopener">'
                            f'<img src="{e(src)}" alt="{e(row.id)}: {e(method)}" loading="lazy"></a>'
                            for src in cell_sources) + "</td>"
            for method, cell_sources in zip(methods, sources))
        body.append(f'<tr><th scope="row">{e(row.id)}</th>'
                    f'<td class="prompt">{e(row.user_prompt)}</td>'
                    '<td class="model-prompts">'
                    '<details><summary>HP12 rewritten input</summary>'
                    f'<pre>{e(row.baseline_prompt)}</pre></details>'
                    '<details><summary>GPT2.5 final input</summary>'
                    f'<pre>{e(final_prompt)}</pre></details></td>{cells}</tr>')
    head = ('<th scope="col">Case</th><th scope="col">Original user prompt</th>'
            '<th scope="col">Model prompts</th>'
            + "".join(f'<th scope="col">{e(method)}</th>' for method in methods))
    css = ("body{font:13px system-ui;margin:16px}table{border-collapse:collapse}"
           "th,td{border:1px solid #ccc;padding:6px;vertical-align:top}"
           "thead th{position:sticky;top:0;background:white;z-index:1}"
           ".prompt{min-width:220px;max-width:260px;white-space:pre-wrap;overflow-wrap:anywhere}"
           ".model-prompts{min-width:180px;max-width:400px}"
           ".model-prompts pre{white-space:pre-wrap;overflow-wrap:anywhere}"
           "img{display:block;width:300px;height:auto}")
    out = run_dir / "team_comparison.html"
    out.write_text("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
                   '<meta name="viewport" content="width=device-width,initial-scale=1">'
                   f"<title>HP image comparison</title><style>{css}</style></head>"
                   f"<body><table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}"
                   "</tbody></table></body></html>")
    return out


def publish(run_dir: Path, s3_prefix: str) -> str:
    subprocess.run(["aws", "s3", "sync", str(run_dir), s3_prefix, "--only-show-errors",
                    "--exclude", "*", "--include", "viewer.html", "--include", "rows/*"], check=True)
    return FOUNDRY + s3_prefix.removeprefix("s3://").rstrip("/") + "/viewer.html"
