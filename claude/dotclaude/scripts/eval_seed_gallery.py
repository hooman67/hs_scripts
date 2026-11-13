# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Build a prompt x seed comparison HTML from an eval-hub-style CSV.

Given a CSV that has one row per (image, ...) with an asset URL column and a
prompt column (e.g. the Humain study export: AssetURL, Asset, Prompt, ...),
this groups images by prompt and lays out every seed/variant of a prompt side
by side, with the prompt text above. Images are referenced by their (public)
URLs, so the HTML renders anywhere with no auth or download.

Grouping:
  - Primary: parse `prompt<N>_seed<S>` out of the asset filename (the Asset
    column, or the URL) -> group by prompt number, label each image "seed <S>",
    sort prompts numerically and seeds within a prompt.
  - Fallback: if that pattern isn't present, group by the prompt TEXT and label
    each image by its filename.

Examples:
  uv run --script eval_seed_gallery.py --csv study.csv
  uv run --script eval_seed_gallery.py --csv study.csv --out ~/Downloads/run.html --limit 3
  uv run --script eval_seed_gallery.py --csv other.csv --url-col image_url --prompt-col original_prompt
"""
from __future__ import annotations

import argparse
import csv
import html
import re
from collections import OrderedDict
from pathlib import Path

SEED_RE = re.compile(r"prompt(\d+)_seed(\d+)", re.I)


def esc(s: str) -> str:
    return html.escape(s or "")


def build(args: argparse.Namespace) -> None:
    rows = list(csv.DictReader(open(args.csv, encoding="utf-8", errors="replace")))
    if not rows:
        raise SystemExit(f"No rows in {args.csv}")
    cols = rows[0].keys()
    for need in (args.url_col, args.prompt_col):
        if need not in cols:
            raise SystemExit(f"Column {need!r} not in CSV. Columns: {list(cols)}")

    # dedupe by url, remember prompt + parsed (pnum, seed)
    seen: set[str] = set()
    groups: "OrderedDict[object, dict]" = OrderedDict()
    numeric = True
    for r in rows:
        url = (r.get(args.url_col) or "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        prompt = (r.get(args.prompt_col) or "").strip()
        basis = (r.get(args.asset_col) or "") if args.asset_col in cols else url
        m = SEED_RE.search(basis) or SEED_RE.search(url)
        if m:
            key = int(m.group(1))
            label = f"seed {m.group(2)}"
            sortk = int(m.group(2))
        else:
            numeric = False
            key = prompt                       # group by prompt text
            label = url.rsplit("/", 1)[-1]     # filename
            sortk = label
        g = groups.setdefault(key, {"prompt": prompt, "imgs": []})
        if not g["prompt"]:
            g["prompt"] = prompt
        g["imgs"].append((sortk, label, url))

    keys = sorted(groups) if numeric else list(groups)
    if args.limit > 0:
        keys = keys[: args.limit]

    cards = ""
    n_img = 0
    for k in keys:
        g = groups[k]
        pnum_label = f"prompt{k}" if numeric else "prompt"
        figs = ""
        for _, label, url in sorted(g["imgs"], key=lambda t: t[0]):
            n_img += 1
            figs += (f'<figure><a href="{esc(url)}" target="_blank" rel="noopener">'
                     f'<img loading="lazy" decoding="async" src="{esc(url)}"></a>'
                     f'<figcaption>{esc(label)}</figcaption></figure>')
        cards += (f'<section class="card"><div class="pnum">{esc(pnum_label)}</div>'
                  f'<p class="prompt">{esc(g["prompt"])}</p><div class="imgs">{figs}</div></section>')

    title = args.title or f"{Path(args.csv).stem} — seed comparison ({len(keys)} prompts)"
    doc = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><style>
body{{margin:0 auto;max-width:1200px;background:#0f1216;color:#e6eaf0;font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;padding:24px}}
h1{{font-size:19px}} .sub{{color:#98a2b3;font-size:13px;margin-bottom:20px}}
.card{{background:#1c222b;border:1px solid #2a323d;border-radius:10px;padding:16px;margin-bottom:18px}}
.pnum{{font-size:11px;color:#98a2b3;text-transform:uppercase;letter-spacing:.05em}}
.prompt{{font-size:15px;margin:4px 0 14px}}
.imgs{{display:flex;gap:14px;flex-wrap:wrap}}
figure{{margin:0;flex:1;min-width:280px}}
figure img{{width:100%;height:auto;border-radius:8px;border:1px solid #2a323d;background:#0a0c0f;display:block}}
figcaption{{font-size:11px;color:#98a2b3;margin-top:5px}}
@media(max-width:640px){{figure{{min-width:100%}}}}
</style></head><body>
<h1>{esc(title)}</h1>
<div class="sub">{len(keys)} prompts · {n_img} images · grouped by prompt, all seeds side by side</div>
{cards}
</body></html>'''

    out = Path(args.out) if args.out else Path.home() / "Downloads" / f"{Path(args.csv).stem}_seed_gallery.html"
    out.write_text(doc, encoding="utf-8")
    print(f"wrote {out}: {len(keys)} prompts, {n_img} images, {len(doc)//1024}KB")


def main() -> None:
    p = argparse.ArgumentParser(description="Build a prompt x seed comparison HTML from an eval CSV.")
    p.add_argument("--csv", required=True, help="CSV with an asset-URL column and a prompt column.")
    p.add_argument("--out", help="Output HTML path (default ~/Downloads/<csvname>_seed_gallery.html).")
    p.add_argument("--url-col", default="AssetURL", help="Column holding the image URL (default AssetURL).")
    p.add_argument("--prompt-col", default="Prompt", help="Column holding the prompt text (default Prompt).")
    p.add_argument("--asset-col", default="Asset",
                   help="Column with the filename used to parse prompt<N>_seed<S> (default Asset; falls back to URL).")
    p.add_argument("--limit", type=int, default=0, help="Only the first N prompts (0 = all).")
    p.add_argument("--title", help="Custom page title.")
    build(p.parse_args())


if __name__ == "__main__":
    main()
