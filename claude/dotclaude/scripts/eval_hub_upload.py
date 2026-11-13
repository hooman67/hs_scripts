# /// script
# requires-python = ">=3.10"
# dependencies = ["boto3", "httpx", "tqdm"]
# ///
"""Upload a generation to the Adobe Evaluation Hub.

Four input modes:

  A) Foundry viz HTML gallery (old `<td class="prompt">`-style table):
       --html <foundry-aws-corp URL or s3://...index.html>
     Parses prompts from <td class="prompt"> cells and image filenames from
     <img src> attributes. Images are pulled from the same S3 prefix.

  B) S3 prefix already in the row{i}_img{j} naming convention
     (e.g. modern data.json-driven viewers, training_logs/.../assets/):
       --source-s3 s3://<bucket>/<prefix>/
       --prompts-source <file|s3://...> (one prompt per line, OR list-of-dicts JSON with "prompt")
       [--expanded-prompts-source <file|s3://...>]  # optional, paired by index

  C) Pre-staged locally:
       --prompts-file path/to/prompts.txt
       --asset-dir path/with/row{i}_img{j}.<ext>
       [--expanded-prompts-source <file>]  # optional, paired by index

  D) results.csv from the /generate-from-endpoint skill:
       --results-csv <path|s3://...results.csv>
       --images-s3 s3://<bucket>/<prefix>/images/   (where image_filename lives)
     Uses CSV columns: prompt_id, original_prompt, rewritten_prompt,
     image_filename, status. Only rows with status==done (configurable via
     --status-ok) are uploaded. Each row becomes its own asset, so each seed
     keeps its own rewritten prompt.

In every mode, the original prompt populates PromptInput.prompt (the "user
prompt"). When an expanded/rewritten prompt is available, it populates
Asset.metadata.prompt on each variant independently, so the Eval Hub UI can
render it as a separate field.

After staging, the script runs:
    EvalService().create_generation(...)  -> run_id
    S3Uploader(eval_service).upload_directory(staged_dir, run_id)
    eval_service.create_assets(run_id, [AssetCreateRequest...])
and prints the run ID + asset-viewer URL.

Dependency note: eval_service_common comes from Adobe artifactory and is
injected via `uv --with` in the wrapper command (see eval_hub_upload.md), so
the token never lives in this file.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import boto3
from eval_service_common.api_types import AssetCreateRequest
from eval_service_common.eval_service import EvalService
from eval_service_common.model_input_types import PromptInput
from eval_service_common.uploader import S3Uploader
from tqdm import tqdm

FOUNDRY_PREFIX = "https://foundry-aws-corp.adobe.io/asset/"
IMG_EXT_RE = re.compile(r"row(\d+)_img(\d+)\.(png|jpg|jpeg|webp)$", re.I)


@dataclass
class AssetSpec:
    """One image to register: its staged file, item grouping, and prompts."""
    local_path: Path
    item_index: int           # groups variants of the same eval-set item
    prompt: str               # original / user prompt -> PromptInput.prompt
    expanded: str | None      # expanded prompt -> Asset.metadata.prompt


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Upload a generation to Eval Hub.")
    p.add_argument("--html", help="(mode A) Foundry viz HTML URL or s3:// URI")
    p.add_argument("--source-s3", help="(mode B) s3://bucket/prefix/ containing row{i}_img{j}.<ext> files")
    p.add_argument("--prompts-source", help="(mode B) prompts file (txt or json), local path or s3:// URI")
    p.add_argument("--expanded-prompts-source",
                   help="(mode B/C) optional expanded prompts file paired by index. Attached as "
                        "Asset.metadata.prompt; PromptInput.prompt still holds the original user prompt.")
    p.add_argument("--prompts-file", help="(mode C) local text file, one prompt per line")
    p.add_argument("--asset-dir", help="(mode C) dir with pre-staged row{i}_img{j}.<ext> files")
    p.add_argument("--results-csv", help="(mode D) results.csv (from /generate-from-endpoint), path or s3:// URI")
    p.add_argument("--images-s3", help="(mode D) s3://bucket/prefix/ where CSV image_filename values live")
    p.add_argument("--status-ok", default="done",
                   help="(mode D) comma-separated status values to upload (default: done)")

    p.add_argument("--num-prompts", type=int, default=0,
                   help="cap on prompts/items processed (0 = use all available)")
    p.add_argument("--num-variations", type=int, default=2,
                   help="variations per item; for create_generation metadata and to cap modes A/B columns")
    p.add_argument("--asset-ext", default="jpg", help="image extension under --source-s3 (mode B, default jpg)")

    p.add_argument("--eval-set", required=True, help="eval set name")
    p.add_argument("--version", default="1.0", help="eval set version (default 1.0)")
    p.add_argument("--model-id", required=True, help="model id")
    p.add_argument("--created-by", default="hshariati")
    p.add_argument("--link-to-eval-set", action="store_true",
                   help="link to an existing eval set in Eval Hub (default off)")

    p.add_argument("--api-key", default=os.environ.get("EVAL_SERVICE_API_KEY", "humain_eval_upload"))
    p.add_argument("--creds", default=str(Path.home() / "Downloads" / "creds.txt"),
                   help="AWS creds file (key=value) for source S3 reads (mode A/B). Mode D may use env creds.")
    p.add_argument("--workdir", help="local staging dir; default: ./eval_hub_staging_<eval-set>")
    p.add_argument("--parallel", type=int, default=16, help="parallel S3 downloads (default 16)")
    return p.parse_args()


def load_aws_creds(path: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in Path(path).read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition("=")
            out[k.strip()] = v.strip()
    return out


def s3_client(creds_path: str):
    """Build an S3 client. Prefer a creds file if present; otherwise fall back to
    the ambient environment / default chain (e.g. sourced aws_creds.env)."""
    if creds_path and Path(creds_path).exists():
        c = load_aws_creds(creds_path)
        if "aws_access_key_id" in c:
            return boto3.client(
                "s3",
                aws_access_key_id=c["aws_access_key_id"],
                aws_secret_access_key=c["aws_secret_access_key"],
                aws_session_token=c.get("aws_session_token"),
                region_name=c.get("region", "us-west-2"),
            )
    return boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-west-2"))


def url_to_s3(url: str) -> tuple[str, str]:
    if url.startswith("s3://"):
        rest = url[5:]
    elif url.startswith(FOUNDRY_PREFIX):
        rest = url[len(FOUNDRY_PREFIX):]
    else:
        raise ValueError(f"Unsupported URL (need s3:// or foundry-aws-corp URL): {url}")
    bucket, _, key = rest.partition("/")
    return bucket, key


def split_s3_prefix(uri: str) -> tuple[str, str]:
    if not uri.startswith("s3://"):
        raise SystemExit(f"Expected s3:// URI, got: {uri}")
    bucket, _, prefix = uri[5:].partition("/")
    if prefix and not prefix.endswith("/"):
        prefix += "/"
    return bucket, prefix


def fetch_text(source: str, s3) -> str:
    if source.startswith("s3://") or source.startswith(FOUNDRY_PREFIX):
        bucket, key = url_to_s3(source)
        return s3.get_object(Bucket=bucket, Key=key)["Body"].read().decode("utf-8", errors="replace")
    return Path(source).read_text(encoding="utf-8")


def load_prompts(source: str, s3) -> list[str]:
    """Read prompts from a .txt (one per line) or a .json (list of strings, or list of {prompt: ...})."""
    text = fetch_text(source, s3)
    if source.endswith(".json") or source.endswith(".jsonl"):
        if source.endswith(".jsonl"):
            items = [json.loads(line) for line in text.splitlines() if line.strip()]
        else:
            items = json.loads(text)
        if not isinstance(items, list):
            raise SystemExit(f"Expected list in JSON prompts source: {source}")
        prompts = []
        for it in items:
            if isinstance(it, str):
                prompts.append(it)
            elif isinstance(it, dict) and "prompt" in it:
                prompts.append(it["prompt"])
            else:
                raise SystemExit(f"Unrecognized prompt item in {source}: {type(it).__name__}")
        return prompts
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_html(html: str) -> list[tuple[str, list[str]]]:
    rows = []
    tr_re = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
    prompt_re = re.compile(r'<td class="prompt">(.*?)</td>', re.S)
    img_re = re.compile(r'<img src="([^"]+\.(?:png|jpg|jpeg|webp))"', re.S)
    tag_re = re.compile(r"<[^>]+>")
    for tr in tr_re.findall(html):
        pm = prompt_re.search(tr)
        if not pm:
            continue
        prompt = re.sub(r"\s+", " ", tag_re.sub("", pm.group(1))).strip()
        filenames = img_re.findall(tr)
        if filenames:
            rows.append((prompt, filenames))
    return rows


def stage_workdir(args: argparse.Namespace) -> Path:
    w = Path(args.workdir or f"./eval_hub_staging_{args.eval_set}").resolve()
    (w / "assets").mkdir(parents=True, exist_ok=True)
    return w


def parallel_download(s3, bucket: str, jobs: list[tuple[str, Path]], parallel: int, desc: str) -> set[Path]:
    """Download (key -> dest) pairs in parallel. Returns the set of dests that succeeded."""
    if not jobs:
        return set()
    bar = tqdm(total=len(jobs), desc=desc, unit="img")
    ok: set[Path] = set()

    def _dl(key, dest):
        s3.download_file(bucket, key, str(dest))
        return dest

    with ThreadPoolExecutor(max_workers=parallel) as ex:
        futures = {ex.submit(_dl, k, d): (k, d) for k, d in jobs}
        for fut in as_completed(futures):
            k, d = futures[fut]
            try:
                fut.result()
                ok.add(d)
            except Exception as e:
                print(f"  failed {k}: {e}", file=sys.stderr)
            bar.update(1)
    bar.close()
    return ok


def load_expanded(args: argparse.Namespace, s3, n_expected: int) -> list[str] | None:
    if not args.expanded_prompts_source:
        return None
    expanded = load_prompts(args.expanded_prompts_source, s3)
    print(f"Loaded {len(expanded)} expanded prompts from {args.expanded_prompts_source}", file=sys.stderr)
    if len(expanded) != n_expected:
        raise SystemExit(f"original ({n_expected}) and expanded ({len(expanded)}) prompt counts differ")
    return expanded


def stage_from_html(args: argparse.Namespace, s3) -> tuple[Path, list[AssetSpec]]:
    bucket, html_key = url_to_s3(args.html)
    prefix = html_key.rsplit("/", 1)[0] + "/" if "/" in html_key else ""
    html = s3.get_object(Bucket=bucket, Key=html_key)["Body"].read().decode("utf-8", errors="replace")
    rows = parse_html(html)
    print(f"Parsed {len(rows)} rows from s3://{bucket}/{html_key}", file=sys.stderr)

    workdir = stage_workdir(args)
    assets = workdir / "assets"
    cap = len(rows) if args.num_prompts <= 0 else min(args.num_prompts, len(rows))
    take_rows = rows[:cap]
    expanded = load_expanded(args, s3, len(take_rows)) if args.expanded_prompts_source else None

    jobs: list[tuple[str, Path]] = []
    specs: list[AssetSpec] = []
    for i, (prompt, filenames) in enumerate(take_rows):
        for j in range(min(args.num_variations, len(filenames))):
            ext = Path(filenames[j]).suffix or ".png"
            dest = assets / f"row{i}_img{j}{ext}"
            jobs.append((prefix + filenames[j], dest))
            specs.append(AssetSpec(dest, i, prompt, expanded[i] if expanded else None))
    ok = parallel_download(s3, bucket, jobs, args.parallel, "downloading")
    specs = [s for s in specs if s.local_path in ok]
    print(f"Staged {len(specs)} images for {cap} prompts -> {workdir}", file=sys.stderr)
    return assets, specs


def stage_from_s3(args: argparse.Namespace, s3) -> tuple[Path, list[AssetSpec]]:
    if not args.source_s3 or not args.prompts_source:
        raise SystemExit("Mode B requires --source-s3 and --prompts-source.")
    bucket, prefix = split_s3_prefix(args.source_s3)
    originals = load_prompts(args.prompts_source, s3)
    print(f"Loaded {len(originals)} prompts from {args.prompts_source}", file=sys.stderr)

    cap = len(originals) if args.num_prompts <= 0 else min(args.num_prompts, len(originals))
    expanded = load_expanded(args, s3, len(originals)) if args.expanded_prompts_source else None

    workdir = stage_workdir(args)
    assets = workdir / "assets"
    ext = "." + args.asset_ext.lstrip(".")
    jobs: list[tuple[str, Path]] = []
    specs: list[AssetSpec] = []
    for i in range(cap):
        for j in range(args.num_variations):
            dest = assets / f"row{i}_img{j}{ext}"
            jobs.append((f"{prefix}row{i}_img{j}{ext}", dest))
            specs.append(AssetSpec(dest, i, originals[i], expanded[i] if expanded else None))
    ok = parallel_download(s3, bucket, jobs, args.parallel, "downloading")
    specs = [s for s in specs if s.local_path in ok]
    print(f"Staged {len(specs)} images for {cap} prompts -> {workdir}", file=sys.stderr)
    return assets, specs


def stage_from_local(args: argparse.Namespace) -> tuple[Path, list[AssetSpec]]:
    if not args.prompts_file or not args.asset_dir:
        raise SystemExit("Mode C requires --prompts-file and --asset-dir.")
    assets = Path(args.asset_dir).resolve()
    if not assets.is_dir():
        raise SystemExit(f"Asset dir does not exist: {assets}")
    prompts = [l.strip() for l in Path(args.prompts_file).read_text(encoding="utf-8").splitlines() if l.strip()]
    expanded = load_expanded(args, None, len(prompts)) if args.expanded_prompts_source else None

    specs: list[AssetSpec] = []
    for f in sorted(assets.iterdir()):
        m = IMG_EXT_RE.match(f.name)
        if not m:
            continue
        i = int(m.group(1))
        if i >= len(prompts):
            print(f"  skipping {f.name}: row {i} >= {len(prompts)} prompts", file=sys.stderr)
            continue
        specs.append(AssetSpec(f, i, prompts[i], expanded[i] if expanded else None))
    print(f"Found {len(specs)} images across {len(prompts)} prompts in {assets}", file=sys.stderr)
    return assets, specs


def stage_from_csv(args: argparse.Namespace, s3) -> tuple[Path, list[AssetSpec]]:
    """results.csv produced by /generate-from-endpoint.

    Columns used: prompt_id, original_prompt, rewritten_prompt, image_filename, status.
    Each done row becomes one asset; each row carries its own rewritten prompt.
    """
    if not args.results_csv or not args.images_s3:
        raise SystemExit("Mode D requires --results-csv and --images-s3.")
    bucket, img_prefix = split_s3_prefix(args.images_s3)
    text = fetch_text(args.results_csv, s3)
    rows = list(csv.DictReader(text.splitlines()))
    ok_statuses = {s.strip() for s in args.status_ok.split(",") if s.strip()}

    required = {"prompt_id", "original_prompt", "rewritten_prompt", "image_filename", "status"}
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise SystemExit(f"results.csv missing columns: {sorted(missing)}")

    done = [r for r in rows if r["status"] in ok_statuses and r["image_filename"]]
    skipped = len(rows) - len(done)
    print(f"CSV: {len(rows)} rows, {len(done)} uploadable (status in {sorted(ok_statuses)}), {skipped} skipped",
          file=sys.stderr)

    # Map prompt_id -> 0-based contiguous item_index (sorted numerically).
    pids = sorted({r["prompt_id"] for r in rows}, key=lambda x: int(x) if x.isdigit() else x)
    pid_to_index = {pid: i for i, pid in enumerate(pids)}
    if args.num_prompts > 0:
        keep = set(pids[: args.num_prompts])
        done = [r for r in done if r["prompt_id"] in keep]
        print(f"Capped to first {args.num_prompts} prompt_ids -> {len(done)} rows", file=sys.stderr)

    workdir = stage_workdir(args)
    assets = workdir / "assets"
    jobs: list[tuple[str, Path]] = []
    specs: list[AssetSpec] = []
    for r in done:
        fn = r["image_filename"]
        dest = assets / fn
        jobs.append((img_prefix + fn, dest))
        specs.append(AssetSpec(dest, pid_to_index[r["prompt_id"]], r["original_prompt"], r["rewritten_prompt"]))
    ok = parallel_download(s3, bucket, jobs, args.parallel, "downloading")
    specs = [s for s in specs if s.local_path in ok]
    print(f"Staged {len(specs)} images across {len(pids)} prompt_ids -> {workdir}", file=sys.stderr)
    return assets, specs


def main() -> None:
    args = parse_args()
    os.environ["EVAL_SERVICE_API_KEY"] = args.api_key
    s3 = s3_client(args.creds)

    if args.html:
        asset_dir, specs = stage_from_html(args, s3)
    elif args.source_s3:
        asset_dir, specs = stage_from_s3(args, s3)
    elif args.results_csv:
        asset_dir, specs = stage_from_csv(args, s3)
    else:
        asset_dir, specs = stage_from_local(args)

    if not specs:
        raise SystemExit("No assets staged; nothing to upload.")

    print("\n1. Initializing EvalService...")
    eval_service = EvalService()

    print(f"\n2. Creating generation (eval_set={args.eval_set} v{args.version}, model={args.model_id})...")
    run_id: str = eval_service.create_generation(
        eval_set=args.eval_set,
        eval_set_version=args.version,
        model_input_type="PromptInput",
        model_id=args.model_id,
        created_by=args.created_by,
        num_of_variations=args.num_variations,
        link_to_eval_set=args.link_to_eval_set,
    )
    print(f"   Run ID: {run_id}")

    print(f"\n3. Uploading assets from {asset_dir}...")
    uploader = S3Uploader(eval_service)
    uploaded = uploader.upload_directory(directory_path=str(asset_dir), run_id=run_id)
    print(f"   Uploaded {len(uploaded)} files")

    print("\n4. Building asset requests...")
    has_expanded = any(s.expanded for s in specs)
    asset_create_list = []
    for spec in specs:
        filename = spec.local_path.name
        asset_url = eval_service.get_asset_url(run_id, filename)
        mime = "image/png" if filename.lower().endswith(".png") else "image/jpeg"
        metadata = {"prompt": spec.expanded} if spec.expanded else None
        asset_create_list.append(AssetCreateRequest(
            asset_url=asset_url,
            model_input=PromptInput(
                eval_set_item_id=f"{args.eval_set}_{args.version}_{spec.item_index}",
                eval_set_name=args.eval_set,
                prompt=spec.prompt,
            ),
            mime_type=mime,
            metadata=metadata,
        ))
    print(f"   Created {len(asset_create_list)} asset requests"
          + (" (with metadata.prompt = expanded)" if has_expanded else ""))

    print("\n5. Registering assets with EvalHub...")
    eval_service.create_assets(run_id=run_id, assets=asset_create_list)

    print(f"\nSuccess! Run ID: {run_id}")
    print(f"View: https://evaluation-hub.adobe.io/asset-viewer?run_ids={run_id}")


if __name__ == "__main__":
    main()
