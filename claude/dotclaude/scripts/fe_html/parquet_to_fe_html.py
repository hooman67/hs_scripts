"""Convert *any* parquet of media references into an annotation-viewer report.

Two-step flow (run either step independently):

  1. parquet  ->  intermediate JSON manifest   (plain, inspectable, editable)
  2. manifest ->  data.json + viewer.html on S3, assets referenced **in place**

Step 2 (`to-viewer`, the default) needs no `fe_htmls` and re-uploads no pixels: the
viewer leaves absolute asset srcs untouched, so `data.json` can just point at the
objects the parquet already names. `to-html` is the legacy path -- it goes through
fe-html's `create_html`, which accepts only *tensor* assets, so it decodes,
re-encodes and re-uploads a second copy of every asset.

Column roles are **auto-detected** by default: any column whose values look like
image / video URIs (or embedded image bytes) becomes a media asset, long free-text
columns become text cards, and short scalar columns become per-row key/value info.
You never need to know the schema up front — but you can still override any role
with the `--image-cols/--video-cols/--text-cols/--meta-cols` flags.

Reports are capped at `DEFAULT_ROW_LIMIT` rows, **sampled at random** from the whole
file (`--limit 0` for every row, `--seed` to reshuffle) -- a gallery is for eyeballing,
and the first N rows of a parquet are usually one shard or one generation batch.

Usage
-----
  # Inspect the parquet schema + the auto-detected role for each column.
  python parquet_to_fe_html.py inspect s3://bucket/data.parquet

  # One-shot: parquet -> report on S3 (auto-detects all columns; 100 random rows).
  python parquet_to_fe_html.py run s3://bucket/data.parquet s3://bucket/._fe-html/report \
      --title "My report" --require output_image_path

  # Or run the two steps separately (auto by default; flags override):
  python parquet_to_fe_html.py to-json s3://bucket/data.parquet manifest.json --limit 200
  python parquet_to_fe_html.py to-viewer manifest.json s3://bucket/._fe-html/report

This is a reference implementation for the `generate-html` skill.
"""

from __future__ import annotations

import argparse
import io
import json
import logging
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Literal

logger = logging.getLogger(__name__)


def _resolve_viewer_html() -> Path:
    """Locate the annotation viewer template ("New UI"-style, self-contained).

    This skill folder is self-contained: the template sits next to this script, so the
    CLI works from any checkout with nothing else installed. Overrides, in order:

    1. ``$ANNOTATION_VIEWER_HTML`` -- point at a newer template without editing code.
    2. The ``foundation_exploration`` package assets, when importable. That copy is the
       upstream original (training-job reports upload it via ``upload_annotation_viewer``),
       so preferring it means a report built inside a colligo env picks up viewer fixes
       that have not been copied here yet.
    3. ``annotation_viewer.html`` beside this script -- the vendored copy, and the only
       one that exists in a bare foundry checkout.

    Returns:
        Path to ``annotation_viewer.html``. May not exist -- callers must handle that.
    """
    override = os.getenv("ANNOTATION_VIEWER_HTML")
    if override:
        return Path(override).expanduser()

    rel = Path("assets") / "annotation_viewer.html"
    try:
        import foundation_exploration

        installed = Path(foundation_exploration.__file__).parent / rel
        if installed.exists():
            return installed
    except ImportError:  # expected outside a colligo env; use the vendored copy below
        logger.debug("foundation_exploration not importable; using the vendored viewer template")
    # resolve() first: __file__ is relative when invoked by a relative path.
    return Path(__file__).resolve().parent / "annotation_viewer.html"


_VIEWER_HTML = _resolve_viewer_html()

_IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff")
_VIDEO_EXTS = (".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v")
_URI_RE = re.compile(r"^(s3|gs|https?|file)://|^/|^\./|^[A-Za-z]:[\\/]")

# A string column is treated as free text (its own card) rather than compact
# key/value meta once its typical value exceeds this many characters.
_TEXT_LEN_THRESHOLD = 80
# How many non-null values to sample when guessing a column's role.
_SAMPLE_SIZE = 20

# Default cap on rows in a report. A gallery is for eyeballing, and a page of a few
# thousand rows is both unusable (the browser holds every asset) and unreviewable, so
# the CLI samples down to this many by default; pass --limit 0 for the whole file.
DEFAULT_ROW_LIMIT = 100
# Seed for that sampling. Fixed so the same parquet always yields the same report --
# see `_select_rows` for why reproducibility matters to a reviewer.
DEFAULT_SAMPLE_SEED = 0

Role = Literal["image", "video", "text", "meta", "skip"]


# ---------------------------------------------------------------------------
# parquet reading + role auto-detection
# ---------------------------------------------------------------------------
def _read_parquet(path: str, limit: int | None = None) -> "Any":  # returns a DataFrame
    import pandas as pd

    # pandas reads s3:// transparently when s3fs is installed.
    df = pd.read_parquet(path)
    if limit is not None:
        df = df.head(limit)
    return df


def _select_rows(df: "Any", limit: int | None, seed: int) -> "Any":
    """Take at most `limit` rows, sampled at RANDOM rather than from the head.

    A report is for eyeballing quality, and `head(n)` is a biased window: parquets are
    routinely written grouped by shard, entity or generation batch, so the first N rows
    can all share one prompt or one failure mode. A random sample across the whole file
    is representative of what the run actually produced.

    Sampling is seeded, so the same parquet + seed always yields the same report -- a
    re-run reproduces the rows a reviewer already annotated instead of shuffling under
    them (the viewer keys annotations on `evalset_item_id`). Rows keep their sampled
    order sorted by original position, so `row_idx` stays monotonic in the file's order.
    """
    if limit is None or len(df) <= limit:
        return df
    sampled = df.sample(n=limit, random_state=seed)
    logger.info("Sampled %d of %d row(s) at random (seed=%d)", limit, len(df), seed)
    return sampled.sort_index()


def _media_ext(value: str) -> Role | None:
    """Return "image"/"video" if `value` is a URI/path with a known media extension."""
    low = value.strip().lower().split("?", 1)[0]  # drop query string
    if low.endswith(_IMAGE_EXTS):
        return "image"
    if low.endswith(_VIDEO_EXTS):
        return "video"
    return None


def _looks_like_uri(value: str) -> bool:
    return bool(_URI_RE.match(value.strip()))


def _detect_role(series: "Any") -> Role:
    """Guess the role of a column from its dtype and a sample of its values.

    Priority: embedded image bytes / media URIs -> image|video; long free text or
    JSON-ish strings -> text; everything scalar/short -> meta.
    """
    import pandas as pd

    non_null = series.dropna()
    if len(non_null) == 0:
        return "skip"

    sample = non_null.head(_SAMPLE_SIZE).tolist()

    # Raw bytes almost always means an embedded image blob.
    if all(isinstance(v, (bytes, bytearray)) for v in sample):
        return "image"

    # Numeric / boolean dtypes are compact metadata.
    if pd.api.types.is_bool_dtype(series) or pd.api.types.is_numeric_dtype(series):
        return "meta"

    # Datetimes are metadata too.
    if pd.api.types.is_datetime64_any_dtype(series):
        return "meta"

    # Everything else: inspect string content. Also handle list/array columns
    # (multiple URIs per row) by flattening the first element.
    str_sample: list[str] = []
    for v in sample:
        if isinstance(v, (list, tuple)) and len(v) > 0:
            v = v[0]
        if isinstance(v, (bytes, bytearray)):
            return "image"
        str_sample.append(str(v))

    if not str_sample:
        return "meta"

    # Media URIs: require a majority to agree, and pick the dominant media kind.
    media_votes = [_media_ext(s) for s in str_sample if _looks_like_uri(s)]
    media_votes = [m for m in media_votes if m is not None]
    if media_votes and len(media_votes) >= max(1, len(str_sample) // 2):
        return "video" if media_votes.count("video") > media_votes.count("image") else "image"

    # Free text vs compact meta: JSON-ish or long strings become text cards.
    max_len = max(len(s) for s in str_sample)
    looks_json = any(s.strip()[:1] in ("{", "[") for s in str_sample)
    if looks_json or max_len > _TEXT_LEN_THRESHOLD:
        return "text"
    return "meta"


def _detect_roles(df: "Any") -> dict[str, Role]:
    return {col: _detect_role(df[col]) for col in df.columns}


def inspect(path: str) -> None:
    """Print columns, dtypes, the auto-detected role, and a sample value."""
    df = _read_parquet(path, limit=200)
    roles = _detect_roles(df)
    print(f"rows (sampled to {len(df)}), columns = {len(df.columns)}")
    print("\n== columns (auto-detected role) ==")
    for col in df.columns:
        val = df.iloc[0][col]
        preview = str(val).replace("\n", " ")
        if len(preview) > 90:
            preview = preview[:87] + "..."
        print(f"  [{roles[col]:>5}] {col} ({df[col].dtype}): {preview}")
    print("\nRun `to-json`/`run` with no --*-cols flags to use these roles,")
    print("or override any of them with --image-cols/--video-cols/--text-cols/--meta-cols.")


# ---------------------------------------------------------------------------
# Step 1: parquet -> intermediate JSON manifest
# ---------------------------------------------------------------------------
def _is_missing(val: Any) -> bool:
    """True for any pandas/numpy missing value.

    `val is None` alone is not enough: only object columns yield a real `None`. A missing
    value stringifies differently per dtype -- float64 -> "nan", Int64/string[python] ->
    "<NA>", datetime64 -> "NaT" -- and each of those is a non-empty, truthy string. Left
    unnormalized they leak into the report as literal "nan"/"<NA>" text (and, for
    `evalset_item_id`, as one annotation key shared by every ID-less row).
    """
    try:
        import pandas as pd

        # pd.isna is elementwise on containers; only a scalar answer is meaningful here.
        res = pd.isna(val)
        return bool(res) if isinstance(res, bool) or getattr(res, "ndim", 0) == 0 else False
    except ImportError:  # pragma: no cover - pandas is a hard dep of the read path
        return val is None or str(val) == "nan"


def _is_blank_src(val: Any) -> bool:
    """True for a cell that cannot name a media asset.

    Beyond the dtype-specific missing values `_is_missing` covers, a producer may
    signal "no asset for this row" with an **empty string** -- a common sentinel when
    the column is non-nullable `string`/`object`. Blank is never a usable URI, and
    passing one through costs a real row: `to_html` would fail to load it and
    substitute a `[failed to load image: ]` card, so a partially-populated column
    would fill the report with dead tiles instead of simply omitting them.
    """
    return _is_missing(val) or not str(val).strip()


def _values_as_srcs(val: Any) -> list[str]:
    """Normalize a cell into a list of asset sources (handles list/array columns)."""
    if isinstance(val, (list, tuple)):
        return [str(v) for v in val if not _is_blank_src(v)]
    try:
        import numpy as np

        if isinstance(val, np.ndarray):
            return [str(v) for v in val.tolist() if not _is_blank_src(v)]
    except ImportError:
        pass
    return [] if _is_blank_src(val) else [str(val)]


def to_json(
    parquet_path: str,
    out_json: str,
    image_cols: list[str] | None,
    video_cols: list[str] | None,
    text_cols: list[str] | None,
    meta_cols: list[str] | None,
    id_col: str | None,
    limit: int | None = DEFAULT_ROW_LIMIT,
    require_cols: list[str] | None = None,
    seed: int = DEFAULT_SAMPLE_SEED,
) -> None:
    """Convert parquet rows into a list-of-rows manifest.

    When no explicit `*_cols` are given, every column's role is auto-detected.
    Explicit flags override detection for the named columns; unnamed columns still
    fall back to their detected role. Passing at least one flag while wanting the
    rest auto-detected works too.

    `require_cols` drops any row whose value in one of those columns is missing or
    blank, before roles are applied. Use it when a column is only partially
    populated and a row without it is not worth reviewing -- e.g. a generation
    output that failed, where an input-only row would just be noise in the gallery.

    `limit` (default `DEFAULT_ROW_LIMIT`) caps the report at a *random* sample of that
    many rows; pass `limit=None` for every row. The cap is applied AFTER `require_cols`,
    so dropped rows do not eat into the budget -- requiring an output column on a file
    that is half-empty still yields a full `limit` rows rather than half of them.

    Manifest schema (plain JSON, no torch):
        {
          "columns": {"col": "image", ...},          # resolved role per column
          "rows": [
            {
              "row_idx": 0,
              "evalset_item_id": "<optional>",
              "meta": {"col": "value", ...},          # scalar columns -> key/value info
              "assets": [
                {"kind": "image", "src": "<uri/path>", "label": "source_image"},
                {"kind": "video", "src": "<uri/path>", "label": "clip"},
                {"kind": "text",  "content": "<string>", "label": "edit_instruction"}
              ]
            }, ...
          ]
        }
    """
    # Read the whole file: the row cap is a random sample, so it has to be drawn from
    # every row rather than from a head() window.
    df = _read_parquet(parquet_path)

    # Drop rows missing a required column *before* detection, so a column that is
    # blank only in the dropped rows is still classified from the rows that remain.
    for col in require_cols or []:
        if col not in df.columns:
            raise ValueError(f"--require references unknown column {col!r}; columns={list(df.columns)}")
        keep = ~df[col].map(_is_blank_src)
        dropped = int((~keep).sum())
        if dropped:
            logger.info("Dropping %d/%d row(s) with a missing/blank %s", dropped, len(df), col)
        df = df[keep]
    if df.empty:
        raise ValueError(f"no rows left after --require {require_cols}")

    # Sample *after* the filter, so dropped rows do not eat into the cap.
    df = _select_rows(df, limit, seed)

    # Start from auto-detection, then apply any explicit overrides.
    roles: dict[str, Role] = _detect_roles(df)
    overrides: list[tuple[list[str] | None, Role]] = [
        (image_cols, "image"),
        (video_cols, "video"),
        (text_cols, "text"),
        (meta_cols, "meta"),
    ]
    for cols, role in overrides:
        for col in cols or []:
            if col not in df.columns:
                raise ValueError(f"--{role}-col references unknown column {col!r}; columns={list(df.columns)}")
            roles[col] = role

    logger.info("Resolved column roles: %s", {c: r for c, r in roles.items() if r != "skip"})

    rows: list[dict[str, Any]] = []
    for i, (_, r) in enumerate(df.iterrows()):
        assets: list[dict[str, Any]] = []
        meta: dict[str, Any] = {}
        for col in df.columns:
            role = roles[col]
            val = r.get(col)
            if role == "image":
                for src in _values_as_srcs(val):
                    assets.append({"kind": "image", "src": src, "label": col})
            elif role == "video":
                for src in _values_as_srcs(val):
                    assets.append({"kind": "video", "src": src, "label": col})
            elif role == "text":
                if not _is_missing(val):
                    assets.append({"kind": "text", "content": str(val), "label": col})
            elif role == "meta":
                meta[col] = _jsonable(val)

        rows.append(
            {
                "row_idx": i,
                "evalset_item_id": _row_id(r, id_col, i),
                "meta": meta,
                "assets": assets,
            }
        )

    Path(out_json).parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"columns": roles, "rows": rows}, f, indent=2, default=str)
    logger.info("Wrote manifest with %d rows -> %s", len(rows), out_json)


def _row_id(row: Any, id_col: str | None, row_idx: int) -> str | None:
    """The row's `evalset_item_id`: the cell's value, or `"row<idx>"` when it is missing.

    The viewer keys per-row annotations on `evalset_item_id || ('row' + row_idx)` and aligns
    compare-mode sources by it, so a non-unique ID silently merges rows: every ID-less row
    would share one comment/answer set. A missing cell must therefore never become the string
    "nan"/"<NA>"/"NaT". It falls back to `"row<idx>"` -- the same value the viewer derives from
    `row_idx` on its own -- so the ID stays unique and compare-mode alignment by position still
    works. Returns None only when no `--id-col` was configured at all.
    """
    if not id_col:
        return None
    val = row.get(id_col)
    if _is_missing(val):
        # Fall back to the row index so the ID stays unique within the report.
        return f"row{row_idx}"
    text = str(val).strip()
    return text or f"row{row_idx}"


def _jsonable(val: Any) -> str | int | float | bool | None:
    if isinstance(val, bool):
        return val
    if _is_missing(val):
        return None
    if isinstance(val, (str, int, float)):
        return val
    return str(val)


# ---------------------------------------------------------------------------
# Step 2a: manifest -> data.json referencing assets IN PLACE (no fe-html, no torch)
# ---------------------------------------------------------------------------
S3_HTTP_GATEWAY = "https://foundry-aws-corp.adobe.io"


def _bucket_key(s3_uri: str) -> tuple[str, str]:
    rest = s3_uri[len("s3://") :]
    bucket, _, key = rest.partition("/")
    return bucket, key


def asset_url(s3_uri: str, is_secure: bool) -> str:
    """Absolute HTTPS URL for an object already in S3.

    Secure foundry buckets are only readable through the gateway's ``/asset/<bucket>/<key>``
    path (IMS cookie auth); public buckets can use the direct virtual-hosted S3 URL.
    Returns non-``s3://`` inputs unchanged, so a parquet already holding HTTPS URLs works.
    """
    if not s3_uri.startswith("s3://"):
        return s3_uri
    bucket, key = _bucket_key(s3_uri)
    if is_secure:
        return f"{S3_HTTP_GATEWAY}/asset/{bucket}/{key}"
    return f"https://{bucket}.s3.us-west-2.amazonaws.com/{key}"


def manifest_to_data_json(manifest: dict[str, Any], is_secure: bool, title: str | None) -> dict[str, Any]:
    """Convert a manifest into the viewer's ``data.json`` contract, in memory.

    The heavy `to_html` path exists because fe-html's ``create_html`` only accepts *tensor*
    assets: it decodes every image, re-encodes it, and uploads a fresh copy. When the parquet
    already points at durable S3 objects that is pure waste -- and it forces a dependency on
    ``fe_htmls`` (Artifactory-only) plus torch/torchvision. The viewer leaves any absolute
    asset src untouched (``rebaseAssetPaths`` skips values matching a URL scheme), so a
    data.json can simply reference the originals and nothing needs re-encoding.

    Emits the same field names the viewer reads, so filters, sort, search, the Columns bar,
    the inspector and CSV export all behave exactly as on an fe-html-generated report.
    """
    rows: list[dict[str, Any]] = []
    for row in manifest["rows"]:
        images: list[dict[str, Any]] = []
        for a in row["assets"]:
            kind, label = a["kind"], a.get("label", "")
            meta_text = {"label": label} if label else {}
            if kind == "image":
                images.append({"asset_type": "image", "image_src": asset_url(a["src"], is_secure), "meta_text": meta_text})
            elif kind == "video":
                images.append({"asset_type": "video", "video_src": asset_url(a["src"], is_secure), "meta_text": meta_text})
            elif kind == "text":
                images.append({"asset_type": "text", "text_content": a["content"], "meta_text": meta_text})
        rows.append(
            {
                "meta_data": {
                    "row_idx": row["row_idx"],
                    "evalset_item_id": row.get("evalset_item_id"),
                    "key_val_informations": {k: v for k, v in (row.get("meta") or {}).items() if v is not None} or None,
                },
                "images": images,
            }
        )
    return {"is_secure": is_secure, "meta_texts": [title] if title else [], "rows": rows}


def to_viewer(
    manifest_json: str,
    output_dir: str,
    title: str | None = None,
    is_secure: bool | None = None,
) -> str | None:
    """Publish a report by uploading only ``data.json`` + ``viewer.html``.

    The assets stay where the parquet already put them. This needs no ``fe_htmls``, no torch
    and no re-upload of pixels, so it is both the fast path and the one that works in an
    environment without Artifactory access. Returns the viewer URL.
    """
    with open(manifest_json, encoding="utf-8") as f:
        manifest = json.load(f)

    if is_secure is None:
        # Foundry buckets are gateway-only; maybe_credentials answers None for public ones.
        bucket, _ = _bucket_key(output_dir)
        try:
            import foundry_aws_gateway

            is_secure = foundry_aws_gateway.maybe_credentials(bucket) is not None
        except ImportError:
            is_secure = False
        logger.info("is_secure=%s (auto-detected for bucket %s)", is_secure, bucket)

    data = manifest_to_data_json(manifest, is_secure=is_secure, title=title)

    if not _VIEWER_HTML.exists():
        raise FileNotFoundError(f"annotation viewer template not found at {_VIEWER_HTML}")

    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp)
        with open(staged / "data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1, default=str)
        shutil.copyfile(_VIEWER_HTML, staged / "viewer.html")
        _upload_dir(staged, output_dir)

    n_assets = sum(len(r["images"]) for r in data["rows"])
    logger.info("Published %d rows / %d asset refs (no pixels re-uploaded)", len(data["rows"]), n_assets)
    url = asset_url(f"{output_dir.rstrip('/')}/viewer.html", is_secure)
    print(url)
    return url


def _upload_dir(local_dir: Path, s3_dir: str) -> None:
    """Upload every file in `local_dir` to `s3_dir` with boto3 (via the gateway when needed)."""
    import boto3

    bucket, key_prefix = _bucket_key(s3_dir.rstrip("/"))
    client = None
    try:
        import foundry_aws_gateway

        client = foundry_aws_gateway.maybe_s3_client(bucket)
    except ImportError:
        logger.debug("foundry_aws_gateway unavailable; using ambient boto3 credentials")
    if client is None:
        client = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-west-2"))

    for path in sorted(local_dir.iterdir()):
        if not path.is_file():
            continue
        ctype = "application/json" if path.suffix == ".json" else "text/html"
        client.upload_file(str(path), bucket, f"{key_prefix}/{path.name}", ExtraArgs={"ContentType": ctype})
        logger.info("uploaded %s -> s3://%s/%s/%s", path.name, bucket, key_prefix, path.name)


# ---------------------------------------------------------------------------
# Step 2b: manifest -> HtmlStruct -> create_html (fe-html; re-encodes every asset)
# ---------------------------------------------------------------------------
def _load_image_tensor(src: str) -> "Any":  # returns torch.Tensor [C,H,W] in [0,1]
    """Load an image from a local path or s3:// URI into a CPU float tensor."""
    from PIL import Image
    from torchvision.transforms.functional import to_tensor

    raw = _read_bytes(src)
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    t = to_tensor(img)  # [C,H,W], float in [0,1], CPU
    return t.detach().float().cpu().clamp(0.0, 1.0)


def _read_bytes(src: str) -> bytes:
    """Read bytes from a local path or s3:// URI.

    S3 works via s3fs if installed, else falls back to pyarrow.fs (bundled with
    pandas' parquet support) so the script runs without an extra dependency.
    """
    if src.startswith("s3://"):
        try:
            import s3fs

            fs = s3fs.S3FileSystem()
            with fs.open(src, "rb") as f:
                return f.read()
        except ImportError:
            from pyarrow.fs import S3FileSystem

            bucket_key = src[len("s3://") :]
            with S3FileSystem().open_input_stream(bucket_key) as f:
                return f.read()
    if src.startswith(("http://", "https://")):
        import urllib.request

        with urllib.request.urlopen(src) as resp:  # noqa: S310 - trusted report inputs
            return resp.read()
    return Path(src).read_bytes()


def to_html(
    manifest_json: str,
    output_dir: str,
    image_format: Literal["png", "jpg"] = "jpg",
    title: str | None = None,
) -> None:
    """Build an fe-html HtmlStruct from the manifest and upload it to S3."""
    from fe_htmls import (
        HtmlRow,
        HtmlStruct,
        ImageAsset,
        MetaData,
        TextAsset,
        VideoAsset,
        create_html,
    )

    with open(manifest_json, encoding="utf-8") as f:
        manifest = json.load(f)

    html_rows: list[HtmlRow] = []
    for row in manifest["rows"]:
        assets: list[Any] = []
        for a in row["assets"]:
            kind = a["kind"]
            label = a.get("label", "")
            try:
                if kind == "image":
                    assets.append(ImageAsset(image_tensor=_load_image_tensor(a["src"]), meta_text={"label": label}))
                elif kind == "video":
                    assets.append(VideoAsset(video_tensor=_load_video_tensor(a["src"]), meta_text={"label": label}))
                elif kind == "text":
                    assets.append(TextAsset(text_content=a["content"], meta_text={"label": label}))
            except Exception:
                # A single unreadable asset must not sink the whole report.
                logger.exception("Failed to load asset %s (row %s); substituting text card", a, row["row_idx"])
                assets.append(TextAsset(text_content=f"[failed to load {kind}: {a.get('src', '')}]"))

        meta = MetaData(
            row_idx=row["row_idx"],
            evalset_item_id=row.get("evalset_item_id"),
            key_val_informations={k: v for k, v in (row.get("meta") or {}).items() if v is not None} or None,
        )
        html_rows.append(HtmlRow(meta_data=meta, images=assets))

    html_struct = HtmlStruct(rows=html_rows, meta_texts=[title] if title else None)
    urls = create_html(data=html_struct, output_dir=output_dir, image_format=image_format)
    if urls is not None:
        old_url, syncedview_url = urls
        logger.info("classic viewer:   %s", old_url)
        logger.info("SyncedView (new): %s", syncedview_url)
        # Deploy the self-contained annotation viewer alongside data.json and make it
        # the primary URL — SyncedView cannot load reports from secure foundry buckets.
        viewer_url = deploy_viewer(output_dir, is_secure=html_struct.is_secure)
        if viewer_url:
            logger.info("annotation viewer: %s", viewer_url)
            print(viewer_url)
        else:
            print(syncedview_url)


def deploy_viewer(output_dir: str, is_secure: bool) -> str | None:
    """Upload the self-contained annotation viewer next to data.json, as ``viewer.html``.

    Returns the viewer's HTTPS URL, or None if the template is missing or the upload
    fails (in which case the caller falls back to the SyncedView URL).

    This viewer is the default "New UI"-equivalent: it provides filter/search/sort,
    side-by-side compare, per-row keep/reject annotations and CSV export, and — unlike
    SyncedView — it loads correctly from secure foundry-bucket gateway paths because it
    is a single file with no ES-module/dynamic-import chunk loading. The template is
    ``annotation_viewer.html`` next to this script (see _resolve_viewer_html); it is
    published under the name ``viewer.html`` to match the training-job reports.
    """
    from fe_htmls.s3_utils import s3_to_https_url, upload_to_s3

    if not _VIEWER_HTML.exists():
        logger.warning("annotation viewer template not found at %s; skipping annotation viewer", _VIEWER_HTML)
        return None
    try:
        # upload_to_s3 uploads a whole directory; stage the single file in a temp dir.
        with tempfile.TemporaryDirectory() as tmp:
            staged = Path(tmp) / "viewer.html"
            shutil.copyfile(_VIEWER_HTML, staged)
            upload_to_s3(Path(tmp), output_dir)
        return s3_to_https_url(f"{output_dir}/viewer.html", is_secure=is_secure)
    except Exception:
        logger.exception("Failed to deploy annotation viewer; falling back to SyncedView URL")
        return None


def _load_video_tensor(src: str) -> "Any":  # returns torch.Tensor [C,F,H,W] in [0,1]
    """Load a video from a local path or s3:// URI into a CPU float tensor."""
    import tempfile

    from torchvision.io import read_video

    raw = _read_bytes(src)
    suffix = Path(src).suffix or ".mp4"
    with tempfile.NamedTemporaryFile(suffix=suffix) as tmp:
        tmp.write(raw)
        tmp.flush()
        frames, _, _ = read_video(tmp.name, pts_unit="sec")  # [F,H,W,C] uint8
    t = frames.permute(3, 0, 1, 2).float() / 255.0  # [C,F,H,W] in [0,1]
    return t.detach().cpu().clamp(0.0, 1.0)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _csv(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


def _row_limit(value: str) -> int | None:
    """Parse --limit, mapping 0 (and negatives) to "no cap"."""
    n = int(value)
    return n if n > 0 else None


def _add_col_flags(parser: "argparse.ArgumentParser") -> None:
    parser.add_argument("--image-cols", type=_csv, default=[], help="override: force these columns to image")
    parser.add_argument("--video-cols", type=_csv, default=[], help="override: force these columns to video")
    parser.add_argument("--text-cols", type=_csv, default=[], help="override: force these columns to text cards")
    parser.add_argument("--meta-cols", type=_csv, default=[], help="override: force these columns to key/value meta")
    parser.add_argument("--id-col", default=None, help="column used as evalset_item_id")
    parser.add_argument(
        "--limit",
        type=_row_limit,
        default=DEFAULT_ROW_LIMIT,
        help=(
            f"cap the report at N rows, sampled at random from the whole file "
            f"(default {DEFAULT_ROW_LIMIT}; 0 = every row)"
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SAMPLE_SEED,
        help=f"seed for the --limit random sample (default {DEFAULT_SAMPLE_SEED}); same seed = same rows",
    )
    parser.add_argument(
        "--require",
        type=_csv,
        default=[],
        help="skip rows whose value in these columns is missing/blank (e.g. a failed generation)",
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("inspect", help="print parquet schema + auto-detected role per column")
    pi.add_argument("parquet")

    pj = sub.add_parser("to-json", help="parquet -> manifest.json (roles auto-detected; flags override)")
    pj.add_argument("parquet")
    pj.add_argument("out_json")
    _add_col_flags(pj)

    pv = sub.add_parser(
        "to-viewer",
        help="manifest.json -> data.json + viewer.html on S3, assets referenced in place (default; no fe-html)",
    )
    pv.add_argument("manifest")
    pv.add_argument("output_dir", help="s3://... destination (must be an S3 path)")
    pv.add_argument("--title", default=None)
    pv.add_argument(
        "--secure",
        dest="is_secure",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="force gateway (--secure) or direct-S3 (--no-secure) asset URLs; default auto-detects",
    )

    ph = sub.add_parser("to-html", help="manifest.json -> HTML on S3 via fe-html (re-encodes+re-uploads every asset)")
    ph.add_argument("manifest")
    ph.add_argument("output_dir", help="s3://... destination (must be an S3 path)")
    ph.add_argument("--image-format", choices=["png", "jpg"], default="jpg")
    ph.add_argument("--title", default=None)

    pr = sub.add_parser("run", help="one-shot parquet -> report on S3 (auto-detects columns)")
    pr.add_argument("parquet")
    pr.add_argument("output_dir", help="s3://... destination (must be an S3 path)")
    pr.add_argument("--image-format", choices=["png", "jpg"], default="jpg")
    pr.add_argument("--title", default=None)
    pr.add_argument(
        "--secure",
        dest="is_secure",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="force gateway (--secure) or direct-S3 (--no-secure) asset URLs; default auto-detects",
    )
    pr.add_argument(
        "--copy-assets",
        action="store_true",
        help="re-encode and re-upload every asset through fe-html instead of referencing them in place",
    )
    _add_col_flags(pr)

    args = p.parse_args()
    if args.cmd == "inspect":
        inspect(args.parquet)
    elif args.cmd == "to-json":
        to_json(
            parquet_path=args.parquet,
            out_json=args.out_json,
            image_cols=args.image_cols,
            video_cols=args.video_cols,
            text_cols=args.text_cols,
            meta_cols=args.meta_cols,
            id_col=args.id_col,
            limit=args.limit,
            require_cols=args.require,
            seed=args.seed,
        )
    elif args.cmd == "to-viewer":
        to_viewer(
            manifest_json=args.manifest,
            output_dir=args.output_dir,
            title=args.title,
            is_secure=args.is_secure,
        )
    elif args.cmd == "to-html":
        to_html(
            manifest_json=args.manifest,
            output_dir=args.output_dir,
            image_format=args.image_format,
            title=args.title,
        )
    elif args.cmd == "run":
        import tempfile

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            manifest_path = tmp.name
        to_json(
            parquet_path=args.parquet,
            out_json=manifest_path,
            image_cols=args.image_cols,
            video_cols=args.video_cols,
            text_cols=args.text_cols,
            meta_cols=args.meta_cols,
            id_col=args.id_col,
            limit=args.limit,
            require_cols=args.require,
            seed=args.seed,
        )
        if args.copy_assets:
            to_html(
                manifest_json=manifest_path,
                output_dir=args.output_dir,
                image_format=args.image_format,
                title=args.title,
            )
        else:
            to_viewer(
                manifest_json=manifest_path,
                output_dir=args.output_dir,
                title=args.title,
                is_secure=args.is_secure,
            )


if __name__ == "__main__":
    main()