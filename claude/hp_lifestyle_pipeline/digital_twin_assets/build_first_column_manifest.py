"""Build tracked provenance for the first image column of an fe-html data.json."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit


VIEWER_URL = (
    "https://foundry-aws-corp.adobe.io/asset/foundry-hp-enterprise-adobe-assets/"
    "training_logs/FFP-83052-foundry-FFP-88382-hp12_pr33690_v4_gemini_v3_4seed_"
    "step01102000_inference-2026.09.29-11.07.03/inference/hp12_pr33690_v4_gemini_"
    "v3_4seed_step01102000_inference_step01102000_ema=False_2026-09-29T11:25:04/"
    "compare_old_vs_new_rewriter_2026-09-29T11.40.39/viewer.html"
)


def s3_uri(url: str) -> str:
    path = unquote(urlsplit(url).path)
    marker = "/asset/"
    if marker not in path:
        raise ValueError(f"Not a Foundry asset URL: {url}")
    bucket_and_key = path.split(marker, 1)[1]
    return "s3://" + bucket_and_key


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-json", type=Path, required=True)
    parser.add_argument("--asset-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()

    data = json.loads(args.data_json.read_text())
    assets = []
    for position, row in enumerate(data["rows"]):
        image = row["images"][0]
        eval_id = row["meta_data"]["evalset_item_id"]
        extension = Path(urlsplit(image["image_src"]).path).suffix.lower() or ".bin"
        local_filename = f"{position:02d}_{eval_id}{extension}"
        local_path = args.asset_dir / local_filename
        if not local_path.is_file():
            raise FileNotFoundError(local_path)
        assets.append(
            {
                "viewer_position": position,
                "evalset_item_id": eval_id,
                "column_label": image["meta_text"]["label"],
                "model_role": image["is_model_input_or_output"],
                "width": image["width"],
                "height": image["height"],
                "source_url": image["image_src"],
                "s3_uri": s3_uri(image["image_src"]),
                "local_filename": local_filename,
                "bytes": local_path.stat().st_size,
                "sha256": file_sha256(local_path),
            }
        )

    if len({asset["s3_uri"] for asset in assets}) != len(assets):
        raise ValueError("First-column source paths are not unique")
    if len({asset["sha256"] for asset in assets}) != len(assets):
        raise ValueError("Downloaded first-column files contain byte-identical duplicates")

    viewer_s3 = s3_uri(VIEWER_URL)
    manifest = {
        "as_of": date.today().isoformat(),
        "source_viewer_url": VIEWER_URL,
        "source_viewer_s3_uri": viewer_s3,
        "source_data_s3_uri": viewer_s3.removesuffix("viewer.html") + "data.json",
        "selection": "images[0] from every row",
        "column_label": "Input: Input 3: First Frame Cond",
        "local_directory": str(args.asset_dir),
        "asset_count": len(assets),
        "assets": assets,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "first_column_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    (args.output_dir / "first_column_s3_paths.txt").write_text(
        "\n".join(asset["s3_uri"] for asset in assets) + "\n"
    )
    print(f"Wrote {len(assets)} assets to {args.output_dir}")


if __name__ == "__main__":
    main()
