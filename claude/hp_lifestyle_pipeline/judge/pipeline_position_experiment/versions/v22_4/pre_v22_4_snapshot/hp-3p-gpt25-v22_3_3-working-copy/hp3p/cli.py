import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .catalog import load_catalog
from .evalset import download_hero, load_rows
from .report import publish, render

ROOT = Path(__file__).resolve().parent.parent
CATALOG = "/mnt/localssd/inference4-film-grounding-v2-20260917/hp/styles.json"
PREFIX = "s3://foundry-hp-enterprise-adobe-assets/adarabi/hp-3p-gpt25/"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["caption", "run", "report", "publish"])
    ap.add_argument("--run-id", default="captions")
    ap.add_argument("--rows", type=int, default=None)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--refs", type=int, choices=[1, 4], default=4, help="number of style references")
    ap.add_argument("--size", choices=["1216x912", "2368x1776"], default="1216x912",
                    help="native input/output canvas; no output upscaling")
    ap.add_argument("--grade", action="store_true", help="save a separate whole-image grade (requires --refs 1)")
    ap.add_argument("--no-captions", action="store_true")
    ap.add_argument("--catalog", default=CATALOG, help="reference catalog JSON, including human/no_humans tags")
    ap.add_argument("--blue-histogram", type=Path, help="full per-element exact HEX CSV.gz; enables reference-blue mode")
    ap.add_argument("--ids", default=None, help="comma-separated row ids, e.g. 0008,0023")
    a = ap.parse_args()
    if a.grade and a.refs != 1:
        ap.error("--grade requires --refs 1")
    if a.blue_histogram and a.refs != 1:
        ap.error("--blue-histogram requires --refs 1")
    if a.cmd == "caption":
        from .captions import CAPTIONS, caption_catalog
        from .openai_client import OpenAIClient

        caps = caption_catalog(load_catalog(a.catalog), OpenAIClient(), CAPTIONS, a.workers)
        print(f"{len(caps)} captions -> {CAPTIONS}")
        return
    run_dir = ROOT / "runs" / a.run_id
    rows = load_rows(ROOT / "foundry_subset_48_pr35902_gemini.json", ROOT / "baseline_compare.json")
    if a.ids:
        want = {f"baseline-{i.strip().zfill(4)}" for i in a.ids.split(",")}
        rows = [r for r in rows if r.id in want]
    rows = rows[: a.rows]
    title = f"HP 3P GPT Image 2.5 + {a.refs} HP style ref{'s' if a.refs != 1 else ''} vs HP12 — {a.run_id}"
    grade_failed = False
    if a.cmd == "run":
        import json

        from .captions import CAPTIONS
        from .openai_client import OpenAIClient
        from .pipeline import grade_row, run_row

        catalog = load_catalog(a.catalog)
        reference_blue = None
        if a.blue_histogram:
            from .histogram import HistogramLookup, build_index
            from .reference_blue import ReferenceBlue

            index = run_dir / "exact_lookup"
            build_index(a.blue_histogram, index)
            reference_blue = ReferenceBlue(catalog, HistogramLookup(index))
        client = OpenAIClient()
        captions = None if a.no_captions or reference_blue is not None else json.loads(CAPTIONS.read_text())
        width, height = (int(value) for value in a.size.split("x"))

        def one(row):
            d = run_dir / "rows" / row.id
            d.mkdir(parents=True, exist_ok=True)
            res = run_row(row, client, catalog, run_dir, download_hero(row, d).read_bytes(), captions,
                          ref_count=a.refs, size=(width, height), reference_blue=reference_blue)
            print(row.id, res["status"], res["tone"], res["content"], res["error"] or "", flush=True)

        with ThreadPoolExecutor(a.workers) as pool:
            list(pool.map(one, rows))
        if a.grade:
            with ThreadPoolExecutor(min(a.workers, 4)) as pool:
                graded = list(pool.map(lambda row: grade_row(run_dir / "rows" / row.id), rows))
            for result in graded:
                print(result["id"], "graded" if result["graded"] else "grade error",
                      result.get("grade_error") or "", flush=True)
            grade_failed = any(not result["graded"] for result in graded)
    run_dir.mkdir(parents=True, exist_ok=True)
    render(rows, run_dir, title)
    if grade_failed:
        raise RuntimeError("Reference grading failed; raw outputs and errors retained.")
    if a.cmd == "publish":
        print(publish(run_dir, PREFIX + a.run_id + "/"))


if __name__ == "__main__":
    main()
