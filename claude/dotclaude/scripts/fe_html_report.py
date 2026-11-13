# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3", "pandas", "pyarrow", "s3fs"]
# ///
"""Build a foundry annotation-viewer report (data.json + viewer.html) from a
**folder of images**, an **S3 prefix**, or a **parquet** — and upload it to S3.

This is the `/fe_html` skill's workhorse. It wraps the vendored, verbatim copy of
foundry's `parquet_to_fe_html.py` (which owns the exact `data.json` contract and the
viewer deploy) and adds the two inputs Hooman actually has: a directory of image/video
files, or an S3 key prefix full of them. A parquet is still accepted and is treated as
an intermediate — it is routed straight through the vendored parquet path.

Input auto-detection (override with --input-kind):
  * ends with `.parquet`                      -> parquet
  * `s3://bucket/prefix` (no .parquet)        -> S3 prefix listing (assets referenced in place)
  * an existing local directory               -> local folder (assets uploaded to <output>/assets/)

Output: an S3 report directory holding `data.json` + `viewer.html`. Open `.../viewer.html`.

Examples
--------
  # S3 folder of images -> report in a sibling _fe-html/ dir (assets referenced in place)
  uv run --script fe_html_report.py \
      --input s3://foundry-thd-enterprise-adobe-assets/THD_laundry_sink_storyboard/images \
      --title "THD laundry sink storyboard"

  # Local folder -> uploads the images, then builds the report
  uv run --script fe_html_report.py \
      --input ~/Downloads/temp_work/images \
      --output s3://foundry-thd-enterprise-adobe-assets/hs_galleries/laundry_sink \
      --title "Laundry sink storyboard"

  # Parquet (intermediate path) -> handed to the vendored CLI unchanged
  uv run --script fe_html_report.py \
      --input s3://bucket/data.parquet \
      --output s3://bucket/_fe-html/report --title "Sweep" --limit 200

Credentials: source your Foundry AWS creds first (same shell), e.g.
  source ~/.claude/hshariati/aws_creds.env && uv run --script fe_html_report.py ...
boto3 picks up the AWS_* env vars. Run /aws-creds if they are missing/expired.
"""
from __future__ import annotations

import argparse
import json
import logging
import mimetypes
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

logger = logging.getLogger("fe_html")

# Import the vendored foundry CLI as a library, so the data.json contract and the
# viewer deploy come from ONE canonical implementation and never drift.
_VENDOR_DIR = Path(__file__).resolve().parent / "fe_html"
sys.path.insert(0, str(_VENDOR_DIR))
try:
    import parquet_to_fe_html as fe  # type: ignore
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        f"Cannot import the vendored parquet_to_fe_html from {_VENDOR_DIR}. "
        "Re-vendor it (see fe_html/VENDORED_FROM.txt)."
    ) from e

_MEDIA_EXTS = tuple(fe._IMAGE_EXTS) + tuple(fe._VIDEO_EXTS)


# ---------------------------------------------------------------------------
# input listing
# ---------------------------------------------------------------------------
def _kind_for(name: str) -> str:
    low = name.lower()
    if low.endswith(tuple(fe._VIDEO_EXTS)):
        return "video"
    return "image"


def _s3_client(region: str):
    import boto3

    return boto3.client("s3", region_name=region)


def list_s3_media(bucket: str, prefix: str, region: str) -> list[dict[str, Any]]:
    """List image/video objects under s3://bucket/prefix. Returns dicts with s3 uri, key, size."""
    client = _s3_client(region)
    prefix = prefix.lstrip("/")
    items: list[dict[str, Any]] = []
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.endswith("/") or not key.lower().endswith(_MEDIA_EXTS):
                continue
            rel = key[len(prefix):].lstrip("/") if key.startswith(prefix) else key
            items.append(
                {
                    "src": f"s3://{bucket}/{key}",
                    "rel": rel or Path(key).name,
                    "name": Path(key).name,
                    "size": obj.get("Size", 0),
                }
            )
    items.sort(key=lambda d: d["rel"])
    return items


def list_local_media(folder: Path) -> list[dict[str, Any]]:
    files = [p for p in sorted(folder.rglob("*")) if p.is_file() and p.suffix.lower() in _MEDIA_EXTS]
    return [
        {
            "path": p,
            "rel": str(p.relative_to(folder)),
            "name": p.name,
            "size": p.stat().st_size,
        }
        for p in files
    ]


def upload_local_assets(items: list[dict[str, Any]], out_bucket: str, assets_prefix: str, region: str) -> None:
    """Upload each local file to s3://out_bucket/assets_prefix/<rel>, set src to that s3 uri."""
    client = _s3_client(region)
    assets_prefix = assets_prefix.strip("/")
    for it in items:
        key = f"{assets_prefix}/{it['rel']}"
        ctype = mimetypes.guess_type(it["name"])[0] or "application/octet-stream"
        client.upload_file(str(it["path"]), out_bucket, key, ExtraArgs={"ContentType": ctype})
        it["src"] = f"s3://{out_bucket}/{key}"
        logger.info("uploaded %s -> s3://%s/%s", it["name"], out_bucket, key)


# ---------------------------------------------------------------------------
# manifest building (folder / S3 prefix -> the vendored manifest schema)
# ---------------------------------------------------------------------------
def build_manifest(items: list[dict[str, Any]], group_by: str) -> dict[str, Any]:
    """Turn a flat media list into the vendored manifest: {"rows": [...]}.

    group_by:
      none      -> one asset per row (annotation-native: one image, its own questions)
      subfolder -> one row per immediate parent folder; its media are side-by-side tiles
      all       -> a single row holding every asset (a pure contact sheet)
    """
    def folder_of(rel: str) -> str:
        parent = str(Path(rel).parent)
        return "." if parent in ("", ".") else parent

    def size_kb(n: int) -> str:
        return f"{n / 1024:.0f} KB" if n < 1024 * 1024 else f"{n / 1024 / 1024:.1f} MB"

    rows: list[dict[str, Any]] = []
    if group_by == "all":
        assets = [{"kind": _kind_for(it["name"]), "src": it["src"], "label": it["rel"]} for it in items]
        rows.append({"row_idx": 0, "evalset_item_id": "all", "meta": {"count": len(items)}, "assets": assets})
    elif group_by == "subfolder":
        groups: dict[str, list[dict[str, Any]]] = {}
        for it in items:
            groups.setdefault(folder_of(it["rel"]), []).append(it)
        for i, (folder, its) in enumerate(sorted(groups.items())):
            assets = [{"kind": _kind_for(x["name"]), "src": x["src"], "label": x["name"]} for x in its]
            rows.append(
                {
                    "row_idx": i,
                    "evalset_item_id": folder,
                    "meta": {"folder": folder, "count": len(its)},
                    "assets": assets,
                }
            )
    else:  # none: one asset per row
        for i, it in enumerate(items):
            rows.append(
                {
                    "row_idx": i,
                    "evalset_item_id": it["rel"],
                    "meta": {"file": it["name"], "folder": folder_of(it["rel"]), "size": size_kb(it["size"])},
                    "assets": [{"kind": _kind_for(it["name"]), "src": it["src"], "label": it["name"]}],
                }
            )
    return {"rows": rows}


# ---------------------------------------------------------------------------
# orchestration
# ---------------------------------------------------------------------------
def _detect_kind(inp: str) -> str:
    if inp.lower().endswith(".parquet"):
        return "parquet"
    if inp.startswith("s3://"):
        return "s3"
    if Path(inp).expanduser().is_dir():
        return "folder"
    raise SystemExit(f"Cannot tell what --input {inp!r} is. Pass --input-kind {{folder,s3,parquet}}.")


def _default_output_for_s3(bucket: str, prefix: str) -> str:
    """A sibling _fe-html/<leaf> report dir next to the source prefix."""
    leaf = prefix.strip("/").rsplit("/", 1)[-1] or "report"
    base = prefix.strip("/").rsplit("/", 1)[0] if "/" in prefix.strip("/") else ""
    parent = f"{base}/" if base else ""
    return f"s3://{bucket}/{parent}_fe-html/{leaf}"


def run(args: argparse.Namespace) -> None:
    kind = args.input_kind or _detect_kind(args.input)
    region = args.region

    # parquet: hand straight to the vendored path, untouched.
    if kind == "parquet":
        if not args.output:
            raise SystemExit("--output s3://... is required for a parquet input")
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            manifest_path = tmp.name
        fe.to_json(
            parquet_path=args.input,
            out_json=manifest_path,
            image_cols=args.image_cols,
            video_cols=args.video_cols,
            text_cols=args.text_cols,
            meta_cols=args.meta_cols,
            id_col=args.id_col,
            limit=args.limit,
            require_cols=args.require,
        )
        fe.to_viewer(manifest_path, args.output.rstrip("/"), title=args.title, is_secure=args.is_secure)
        return

    # folder / s3 prefix: build a manifest ourselves, then reuse the vendored deploy.
    if kind == "s3":
        bucket, prefix = fe._bucket_key(args.input)
        items = list_s3_media(bucket, prefix, region)
        if not items:
            raise SystemExit(f"No image/video objects found under {args.input}")
        output = (args.output or _default_output_for_s3(bucket, prefix)).rstrip("/")
    elif kind == "folder":
        folder = Path(args.input).expanduser()
        items = list_local_media(folder)
        if not items:
            raise SystemExit(f"No image/video files found under {folder}")
        if not args.output:
            raise SystemExit("--output s3://... is required for a local folder input")
        output = args.output.rstrip("/")
        out_bucket, out_key = fe._bucket_key(output)
        upload_local_assets(items, out_bucket, f"{out_key}/assets", region)
    else:
        raise SystemExit(f"Unknown input kind {kind!r}")

    manifest = build_manifest(items, args.group_by)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        json.dump(manifest, tmp)
        manifest_path = tmp.name

    logger.info("Built %d row(s) from %d asset(s); deploying report -> %s", len(manifest["rows"]), len(items), output)
    fe.to_viewer(manifest_path, output, title=args.title, is_secure=args.is_secure)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--input", required=True, help="folder of images, s3://bucket/prefix, or a .parquet")
    p.add_argument("--output", default=None, help="s3://bucket/prefix report dir (auto-derived for S3 input)")
    p.add_argument("--title", default=None, help="report title (shown in the viewer header)")
    p.add_argument("--input-kind", choices=["folder", "s3", "parquet"], default=None, help="override auto-detection")
    p.add_argument(
        "--group-by",
        choices=["none", "subfolder", "all"],
        default="none",
        help="none = one image per row (default); subfolder = one row per folder; all = single contact-sheet row",
    )
    p.add_argument("--region", default=os.getenv("AWS_REGION", "us-west-2"))
    p.add_argument(
        "--secure",
        dest="is_secure",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="gateway asset URLs (default, for secure foundry buckets); --no-secure for public buckets",
    )
    # parquet passthrough options
    p.add_argument("--image-cols", type=fe._csv, default=[])
    p.add_argument("--video-cols", type=fe._csv, default=[])
    p.add_argument("--text-cols", type=fe._csv, default=[])
    p.add_argument("--meta-cols", type=fe._csv, default=[])
    p.add_argument("--id-col", default=None)
    p.add_argument("--require", type=fe._csv, default=[])
    p.add_argument("--limit", type=fe._row_limit, default=fe.DEFAULT_ROW_LIMIT, help="parquet row cap (0 = all)")

    run(p.parse_args())


if __name__ == "__main__":
    main()
