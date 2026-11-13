#!/usr/bin/env python3
"""Freeze a bounded, reproducible visual sample of the user-supplied HP corpus."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

from PIL import Image, ImageDraw, ImageOps

HERE = Path(__file__).resolve().parent
API = "https://pluto-prod-ttermini-cpu-i-9awf6j-0-8000.jobs.colligo.dev/"
BUCKET = "foundry-dropbox-hp-enterprise"
QUERIES = {
    "chair": "chair",
    "home": "home interior with a workspace desk and shelves",
    "office": "office interior with desks chairs and shelves",
    "education": "library study interior with tables and books",
    "studio": "artist studio interior with a worktable and art supplies",
    "cafe": "cafe interior with tables and chairs",
    "gaming": "gaming room interior with a desk and chair",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")


def discover(name):
    request = {
        "positive": [QUERIES[name]], "negative": [], "prefix": "hp-assets/",
        "offset": 0, "limit": 64, "presign": False,
        "deduplicate": True, "min_score": 0.0001,
    }
    root = HERE / "data/search" / name
    write(root / "request.json", request)
    req = urllib.request.Request(
        API + "v1/search", data=json.dumps(request).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as response:
        body = response.read()
    with (root / "response.json").open("xb") as stream:
        stream.write(body)
    data = json.loads(body)
    if (
        data["bucket"] != BUCKET or data["index"] != "hp-assets"
        or data["offset"] != 0 or data["limit"] != 64
        or data.get("deduplication", {}).get("algorithm") != "phash"
        or len(data["results"]) != min(64, data["total"])
        or len({row["key"] for row in data["results"]}) != len(data["results"])
    ):
        raise ValueError(f"unexpected corpus/search identity or pagination: {name}")
    write(root / "receipt.json", {
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "api": API + "v1/search", "response_sha256": sha(body),
        "total_groups": data["total"], "matched_images": data["matched_total"],
        "reviewed_scope": "first page of 64 relevance-ranked pHash representatives",
        "not_a_random_or_exhaustive_corpus_sample": True,
    })
    print(json.dumps({"query": name, "groups": data["total"],
                      "matched": data["matched_total"]}), flush=True)
    return name, data


def main():
    with ThreadPoolExecutor(max_workers=2) as pool:
        pages = dict(pool.map(discover, QUERIES))
    selected, used = [], set()
    for name in QUERIES:
        rows = pages[name]["results"]
        preferred = (
            [0, 1, 2, 3, 5, 7, 10, 14, 20, 28, 40, 63]
            if name == "chair" else [0, 2, 5, 10, 20, 40]
        )
        order = list(dict.fromkeys([*preferred, *range(len(rows))]))
        target = 12 if name == "chair" else 6
        count = 0
        for rank in order:
            if rank >= len(rows):
                continue
            row = rows[rank]
            members = {row["key"], *(item["key"] for item in row["duplicates"])}
            if members & used:
                continue
            if not row["key"].startswith("hp-assets/") or not row["thumbnail_url"]:
                raise ValueError("unscoped or missing visual evidence")
            used.update(members)
            selected.append({
                "sample_id": f"T{len(selected) + 1:02d}", "query": name,
                "query_rank": rank + 1, "source_bucket": BUCKET, **row,
            })
            count += 1
            if count == target:
                break
        if count != target:
            raise ValueError(f"not enough cross-query distinct groups: {name}")

    def download(row):
        relative = row["thumbnail_url"]
        if not relative.startswith("/media/assets/hp-assets/") or "?" in relative:
            raise ValueError("unexpected thumbnail origin/path")
        with urllib.request.urlopen(API.rstrip("/") + relative, timeout=60) as response:
            body = response.read()
        target = HERE / "data/images" / (row["sample_id"] + ".webp")
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(body)
        with Image.open(target) as image:
            image.load()
            row["dimensions"] = list(image.size)
        return {
            **row, "review_path": str(target), "review_sha256": sha(body),
            "review_source": "actual API-generated source-revision thumbnail",
            "transform": "thumbnail bytes preserved unchanged; no parent crop/resize",
            "original_url": "https://foundry-aws-corp.adobe.io/asset/" + BUCKET + "/" + row["key"],
        }

    with ThreadPoolExecutor(max_workers=4) as pool:
        images = list(pool.map(download, selected))
    write(HERE / "data/images.json", {
        "as_of_utc": datetime.now(timezone.utc).isoformat(),
        "method": "Purposive stratified relevance-rank sample: 12 linked-chair and 6 per six wider setting queries; no overlapping returned pHash groups.",
        "limitations": [
            "48 of76157 indexed images, not exhaustive or statistically representative.",
            "Search similarity and machine labels are discovery aids, not human content labels.",
            "pHash grouping is query-specific and can miss edits or merge distinct photographs.",
            "Astra must distinguish usable room photographs from isolated objects, close crops and irrelevant search results.",
            "Review images are supplied thumbnails, not source-native-resolution originals.",
            "People/electronics in reference evidence are not approved output content.",
        ],
        "images": images,
        "queries": {name: {
            "text": QUERIES[name], "total_groups": page["total"],
            "matched_images": page["matched_total"],
        } for name, page in pages.items()},
    })
    for page in range(2):
        batch = images[page * 24:(page + 1) * 24]
        sheet = Image.new("RGB", (4 * 400, 6 * 300), "white")
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(batch):
            x, y = (i % 4) * 400, (i // 4) * 300
            with Image.open(row["review_path"]) as image:
                thumb = ImageOps.contain(image.convert("RGB"), (392, 260))
                sheet.paste(thumb, (x + (400 - thumb.width) // 2, y + 28))
            draw.text((x + 5, y + 5), f"{row['sample_id']} {row['query']} rank{row['query_rank']}", fill="black")
        sheet.save(HERE / f"data/contact_sheet_{page + 1}.jpg", quality=94)
    print(json.dumps({"training_photographs_frozen": len(images)}), flush=True)


if __name__ == "__main__":
    main()
