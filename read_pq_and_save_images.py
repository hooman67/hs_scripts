#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable, Optional

import duckdb  # type: ignore
import numpy as np

# Image writing (PIL or imageio both fine; using imageio here)
import imageio.v3 as iio  # pip install imageio

# Ensure repo import works whether run from repo root or not
try:
    from genie.stages.image.get import get_image_with_source
except Exception:
    import sys
    # Add common candidates for repo root; adjust if needed
    candidates = [Path.cwd(), Path.cwd().parent, Path.cwd().parent.parent]
    for c in candidates:
        p = c / "genie"
        if p.exists():
            sys.path.insert(0, str(c))
            break
    from genie.stages.image.get import get_image_with_source  # type: ignore


def _duckdb_connect_for_s3() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")
    # Adjust region if needed
    con.execute("SET s3_region='us-west-2';")
    # If you rely on env AWS creds, no change needed. To use anonymous:
    # con.execute("SET s3_use_ssl=true;")
    # con.execute("SET s3_url_style='path';")
    return con


def iter_hashes_from_parquet(parquet_uri: str, limit: Optional[int]) -> Iterable[str]:
    con = _duckdb_connect_for_s3()
    try:
        sql = "SELECT unique_id FROM read_parquet(?) WHERE unique_id IS NOT NULL"
        params: list[object] = [parquet_uri]
        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)
        for (unique_id,) in con.execute(sql, params).fetchall():
            # Ensure str
            yield str(unique_id)
    finally:
        con.close()


def save_image_to_disk(image_array: np.ndarray, dest_path: Path) -> None:
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    iio.imwrite(dest_path, image_array)


def fetch_and_save_images(
    parquet_uri: str,
    output_dir: str | Path,
    limit: Optional[int] = None,
    scale: int | str = 256,
    overwrite: bool = False,
) -> None:
    output_dir = Path(output_dir)
    saved = 0
    failed = 0

    for image_hash in iter_hashes_from_parquet(parquet_uri, limit):
        dest = output_dir / f"{image_hash}.png"
        if dest.exists() and not overwrite:
            print(f"Skipping existing: {dest}")
            continue
        try:
            img, from_piat = get_image_with_source(str_image_hash=image_hash, scale=scale)  # returns (np.ndarray, bool)
            save_image_to_disk(img, dest)
            saved += 1
            src = "PIAT" if from_piat else "MLDP"
            print(f"Saved [{src}] {image_hash} -> {dest}")
        except Exception as e:
            failed += 1
            print(f"Failed {image_hash}: {e}")

    print(f"\nDone. Saved={saved}, Failed={failed}, Output={output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read image hashes from a parquet and save the resolved images to disk."
    )
    parser.add_argument("parquet_uri", help="Local path or s3:// URI to the parquet file containing column 'unique_id'")
    parser.add_argument("--out", required=True, help="Directory to save images")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit on number of rows to process")
    parser.add_argument("--scale", type=str, default="256", help="Image scale (e.g. 256 or 'orig')")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    fetch_and_save_images(
        parquet_uri=args.parquet_uri,
        output_dir=args.out,
        limit=args.limit,
        scale=args.scale,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()