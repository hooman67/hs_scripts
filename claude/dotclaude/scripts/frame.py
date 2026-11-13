# /// script
# requires-python = ">=3.10"
# dependencies = ["requests", "pyyaml"]
# ///
"""Frame.io v2 (legacy) CLI: download/upload folders, gather comments.

Subcommands:
  whoami                                Sanity check auth.
  list <target>                         List immediate children of a folder/asset.
  comments <target> [--out FILE]        Dump comments for an asset/folder tree to CSV.
  download <target> <local_dir>         Download a folder tree (originals + comments.csv).
  upload <local_path> <parent>          Upload a local file or folder under a Frame.io folder.

`target` / `parent` may be a Frame.io URL or a raw UUID. The last UUID found in
the URL is used. Project URLs (no folder UUID) are resolved to root_asset_id.
"""
import argparse
import csv
import json
import math
import mimetypes
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
import yaml

CREDS_PATH = Path.home() / ".claude" / "hshariati" / "credentials.yaml"
BASE = "https://api.frame.io/v2"
UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
PAGE_SIZE = 50
DOWNLOAD_WORKERS = 6
UPLOAD_WORKERS = 4


def load_token() -> str:
    if not CREDS_PATH.exists():
        sys.exit(f"Credentials file missing: {CREDS_PATH}")
    with open(CREDS_PATH) as f:
        creds = yaml.safe_load(f) or {}
    tok = (creds.get("frame") or {}).get("token")
    if not tok:
        sys.exit(
            "Frame.io token missing. Add to ~/.claude/hshariati/credentials.yaml:\n"
            "frame:\n  token: <your_developer_token>\n"
            "Generate at https://developer.frame.io/app/tokens (scopes: project.read, asset.read, asset.create, comment.read)."
        )
    return tok


class Client:
    def __init__(self, token: str):
        self.s = requests.Session()
        self.s.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        })

    def _request(self, method: str, url: str, retries: int = 6, **kwargs):
        for attempt in range(retries):
            r = self.s.request(method, url, timeout=60, **kwargs)
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After") or (2 ** attempt))
                time.sleep(min(wait, 30))
                continue
            if 500 <= r.status_code < 600:
                time.sleep(2 ** attempt)
                continue
            return r
        return r  # type: ignore[return-value]

    def get(self, path: str, **kwargs):
        url = path if path.startswith("http") else f"{BASE}{path}"
        r = self._request("GET", url, **kwargs)
        if not r.ok:
            raise requests.HTTPError(f"GET {url} -> {r.status_code} {r.text[:300]}")
        return r.json()

    def post(self, path: str, **kwargs):
        url = path if path.startswith("http") else f"{BASE}{path}"
        r = self._request("POST", url, **kwargs)
        if not r.ok:
            raise requests.HTTPError(f"POST {url} -> {r.status_code} {r.text[:300]}")
        return r.json()

    def me(self):
        return self.get("/me")

    def get_asset(self, asset_id: str):
        return self.get(f"/assets/{asset_id}")

    def list_children(self, asset_id: str):
        page = 1
        while True:
            data = self.get(
                f"/assets/{asset_id}/children",
                params={"page": page, "page_size": PAGE_SIZE, "include": "children"},
            )
            if not data:
                return
            for item in data:
                yield item
            if len(data) < PAGE_SIZE:
                return
            page += 1

    def get_comments(self, asset_id: str):
        page = 1
        while True:
            data = self.get(
                f"/assets/{asset_id}/comments",
                params={"page": page, "page_size": PAGE_SIZE, "include": "replies"},
            )
            if not data:
                return
            for c in data:
                yield c
            if len(data) < PAGE_SIZE:
                return
            page += 1


def resolve_id(arg: str, client: Client | None = None) -> str:
    """Extract Frame.io UUID from a URL or accept raw UUID.

    For URLs like /projects/<project_id> with no folder UUID after, fetch the
    project and return its root_asset_id (so callers see a folder).
    """
    matches = list(UUID_RE.finditer(arg))
    if not matches:
        sys.exit(f"Could not extract Frame.io UUID from: {arg}")
    last_uuid = matches[-1].group(0)
    if client and "/projects/" in arg and arg.rstrip("/").endswith(last_uuid):
        try:
            proj = client.get(f"/projects/{last_uuid}")
            return proj.get("root_asset_id") or last_uuid
        except Exception:
            return last_uuid
    return last_uuid


def asset_type(a: dict) -> str:
    return a.get("_type") or a.get("type") or ""


def walk(client: Client, root_id: str, path_prefix: str = ""):
    """Yield (asset, parent_path) for every file in the tree rooted at root_id.

    Folders and version_stacks are recursed. The root may itself be a file.
    """
    root = client.get_asset(root_id)
    rt = asset_type(root)
    if rt == "file":
        yield root, path_prefix
        return
    for child in client.list_children(root_id):
        ct = asset_type(child)
        cname = child.get("name") or child["id"]
        if ct == "folder":
            yield from walk(client, child["id"], os.path.join(path_prefix, cname))
        elif ct == "version_stack":
            yield from walk(client, child["id"], os.path.join(path_prefix, cname))
        elif ct == "file":
            yield child, path_prefix


COMMENT_FIELDS = [
    "folder", "asset_name", "asset_id", "comment_id", "parent_comment_id",
    "owner_name", "owner_email", "text", "timestamp_seconds", "has_drawing",
    "completed", "annotation", "created_at", "updated_at",
]


def comment_row(asset: dict, folder: str, c: dict, parent_id: str = "") -> dict:
    owner = c.get("owner") or {}
    return {
        "folder": folder,
        "asset_name": asset.get("name", ""),
        "asset_id": asset["id"],
        "comment_id": c["id"],
        "parent_comment_id": parent_id or (c.get("parent_id") or ""),
        "owner_name": owner.get("name") or owner.get("email", ""),
        "owner_email": owner.get("email", ""),
        "text": c.get("text", "") or "",
        "timestamp_seconds": c.get("timestamp"),
        "has_drawing": bool(c.get("has_drawing")),
        "completed": bool(c.get("completed")),
        "annotation": c.get("annotation") or "",
        "created_at": c.get("inserted_at", ""),
        "updated_at": c.get("updated_at", ""),
    }


def collect_comments(client: Client, asset: dict, folder: str) -> list[dict]:
    rows: list[dict] = []
    if not asset.get("comment_count"):
        return rows
    for c in client.get_comments(asset["id"]):
        rows.append(comment_row(asset, folder, c))
        for reply in (c.get("replies") or []):
            rows.append(comment_row(asset, folder, reply, parent_id=c["id"]))
    return rows


def write_comments_csv(rows: list[dict], path: Path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COMMENT_FIELDS)
        w.writeheader()
        w.writerows(rows)


# ---------- subcommands ----------

def cmd_whoami(client: Client):
    me = client.me()
    print(json.dumps({
        "name": me.get("name"),
        "email": me.get("email"),
        "id": me.get("id"),
        "account_id": me.get("account_id"),
    }, indent=2))


def cmd_list(client: Client, target: str):
    root_id = resolve_id(target, client)
    for child in client.list_children(root_id):
        print(f"{asset_type(child):14} {child['id']}  {child.get('name', '')}  "
              f"comments={child.get('comment_count', 0)}")


def cmd_comments(client: Client, target: str, out: str):
    root_id = resolve_id(target, client)
    rows: list[dict] = []
    n_assets = 0
    for asset, folder in walk(client, root_id):
        n_assets += 1
        rows.extend(collect_comments(client, asset, folder))
        if n_assets % 50 == 0:
            print(f"  scanned {n_assets} assets, {len(rows)} comments so far", file=sys.stderr)
    out_path = Path(out)
    write_comments_csv(rows, out_path)
    print(json.dumps({"assets_scanned": n_assets, "comments": len(rows), "out": str(out_path)}, indent=2))


def _download_one(asset: dict, folder: str, local_dir: Path) -> tuple[str, str]:
    """Returns ('downloaded'|'skipped'|'no_url'|'error: ...', target_path)."""
    target_dir = local_dir / folder if folder else local_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / asset["name"]
    if target.exists() and target.stat().st_size > 0:
        return "skipped", str(target)
    url = asset.get("original")
    if not url:
        return "no_url", str(target)
    tmp = target.with_suffix(target.suffix + ".part")
    try:
        with requests.get(url, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
        tmp.rename(target)
        return "downloaded", str(target)
    except Exception as e:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
        return f"error: {e}", str(target)


def cmd_download(client: Client, target: str, local_dir: str, with_comments: bool):
    root_id = resolve_id(target, client)
    out_dir = Path(local_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Walking tree from {root_id} ...", file=sys.stderr)
    items = list(walk(client, root_id))
    print(f"Found {len(items)} files. Downloading with {DOWNLOAD_WORKERS} workers.", file=sys.stderr)

    counts = {"downloaded": 0, "skipped": 0, "no_url": 0, "errors": 0}
    errors: list[str] = []
    with ThreadPoolExecutor(max_workers=DOWNLOAD_WORKERS) as pool:
        futures = {pool.submit(_download_one, a, f, out_dir): (a, f) for a, f in items}
        for i, fut in enumerate(as_completed(futures), 1):
            status, path = fut.result()
            if status == "downloaded":
                counts["downloaded"] += 1
            elif status == "skipped":
                counts["skipped"] += 1
            elif status == "no_url":
                counts["no_url"] += 1
            else:
                counts["errors"] += 1
                errors.append(f"{path}: {status}")
            if i % 25 == 0 or i == len(items):
                print(f"  [{i}/{len(items)}] dl={counts['downloaded']} "
                      f"skip={counts['skipped']} err={counts['errors']}", file=sys.stderr)

    out = {"out_dir": str(out_dir), **counts}

    if with_comments:
        print("Gathering comments ...", file=sys.stderr)
        rows: list[dict] = []
        for i, (asset, folder) in enumerate(items, 1):
            rows.extend(collect_comments(client, asset, folder))
            if i % 100 == 0:
                print(f"  comments scanned {i}/{len(items)} ({len(rows)} comments)", file=sys.stderr)
        comments_path = out_dir / "comments.csv"
        write_comments_csv(rows, comments_path)
        out["comments"] = len(rows)
        out["comments_csv"] = str(comments_path)

    if errors:
        err_log = out_dir / "download_errors.log"
        err_log.write_text("\n".join(errors))
        out["error_log"] = str(err_log)

    print(json.dumps(out, indent=2))


def _upload_file(client: Client, parent_id: str, file_path: Path) -> str:
    size = file_path.stat().st_size
    mime, _ = mimetypes.guess_type(str(file_path))
    mime = mime or "application/octet-stream"
    create = client.post(
        f"/assets/{parent_id}/children",
        json={"type": "file", "name": file_path.name, "filetype": mime, "filesize": size},
    )
    asset_id = create["id"]
    upload_urls = create.get("upload_urls") or []
    if not upload_urls:
        raise RuntimeError(f"No upload URLs returned for {file_path.name}")

    n = len(upload_urls)
    chunk_size = max(1, math.ceil(size / n)) if size > 0 else 0
    with open(file_path, "rb") as f:
        for url in upload_urls:
            chunk = f.read(chunk_size) if chunk_size else b""
            r = requests.put(
                url,
                data=chunk,
                headers={"Content-Type": mime, "x-amz-acl": "private"},
                timeout=600,
            )
            r.raise_for_status()
    return asset_id


def cmd_upload(client: Client, local_path: str, parent: str):
    parent_id = resolve_id(parent, client)
    local = Path(local_path).expanduser().resolve()
    if not local.exists():
        sys.exit(f"Local path does not exist: {local}")

    if local.is_file():
        asset_id = _upload_file(client, parent_id, local)
        print(json.dumps({"uploaded_files": 1, "asset_id": asset_id}, indent=2))
        return

    counts = {"files": 0, "folders": 0, "errors": 0}
    errors: list[str] = []
    file_jobs: list[tuple[str, Path]] = []  # (parent_id, file_path)

    def make_tree(parent: str, dir_path: Path):
        folder = client.post(f"/assets/{parent}/children", json={"type": "folder", "name": dir_path.name})
        counts["folders"] += 1
        fid = folder["id"]
        for entry in sorted(dir_path.iterdir()):
            if entry.name.startswith("."):
                continue
            if entry.is_dir():
                make_tree(fid, entry)
            elif entry.is_file():
                file_jobs.append((fid, entry))
        return fid

    root_folder = make_tree(parent_id, local)
    print(f"Created folder tree ({counts['folders']} folders, {len(file_jobs)} files queued).", file=sys.stderr)

    with ThreadPoolExecutor(max_workers=UPLOAD_WORKERS) as pool:
        futures = {pool.submit(_upload_file, client, fid, fp): fp for fid, fp in file_jobs}
        for i, fut in enumerate(as_completed(futures), 1):
            fp = futures[fut]
            try:
                fut.result()
                counts["files"] += 1
            except Exception as e:
                counts["errors"] += 1
                errors.append(f"{fp}: {e}")
            if i % 25 == 0 or i == len(file_jobs):
                print(f"  [{i}/{len(file_jobs)}] up={counts['files']} err={counts['errors']}", file=sys.stderr)

    out = {"root_folder_id": root_folder, **counts}
    if errors:
        out["errors_sample"] = errors[:10]
    print(json.dumps(out, indent=2))


# ---------- entry ----------

def main():
    parser = argparse.ArgumentParser(description="Frame.io v2 CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami")

    p_ls = sub.add_parser("list")
    p_ls.add_argument("target")

    p_co = sub.add_parser("comments")
    p_co.add_argument("target")
    p_co.add_argument("--out", default="comments.csv")

    p_dn = sub.add_parser("download")
    p_dn.add_argument("target")
    p_dn.add_argument("local_dir")
    p_dn.add_argument("--no-comments", action="store_true")

    p_up = sub.add_parser("upload")
    p_up.add_argument("local_path")
    p_up.add_argument("parent")

    args = parser.parse_args()
    client = Client(load_token())

    if args.cmd == "whoami":
        cmd_whoami(client)
    elif args.cmd == "list":
        cmd_list(client, args.target)
    elif args.cmd == "comments":
        cmd_comments(client, args.target, args.out)
    elif args.cmd == "download":
        cmd_download(client, args.target, args.local_dir, with_comments=not args.no_comments)
    elif args.cmd == "upload":
        cmd_upload(client, args.local_path, args.parent)


if __name__ == "__main__":
    main()
