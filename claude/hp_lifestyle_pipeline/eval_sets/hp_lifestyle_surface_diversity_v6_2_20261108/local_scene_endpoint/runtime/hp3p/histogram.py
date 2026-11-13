import csv
import gzip
import hashlib
import json
import re
from array import array
from collections.abc import Mapping
from pathlib import Path

import numpy as np

from .reference_style import lab, rgb

DTYPE = np.dtype([("code", "<u4"), ("pixel_count", "<u8"), ("lab", "<f8", (3,))])
EXCLUDED = {"unassigned_blue_region", "unclassified_object"}


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")
    temporary.replace(path)


def eligible(rgb_values, labs):
    values = np.asarray(rgb_values, dtype=float) / 255
    red, green, blue = values.T
    high, low = values.max(axis=1), values.min(axis=1)
    delta = high - low
    safe = np.where(delta > 0, delta, 1)
    hue = np.select([high == red, high == green],
                    [((green - blue) / safe) % 6, (blue - red) / safe + 2],
                    default=(red - green) / safe + 4) * 60
    saturation = np.divide(delta, high, out=np.zeros_like(delta), where=high > 0)
    return (hue >= 160) & (hue <= 280) & (saturation >= .10) & (high >= .08) & (labs[:, 0] >= 8)


def build_index(source, destination):
    source, destination = Path(source), Path(destination)
    digest = sha(source)
    destination.mkdir(parents=True, exist_ok=True)
    if (destination / "index.json").exists():
        if json.loads((destination / "index.json").read_text())["source_sha256"] != digest:
            raise ValueError("Histogram index has a different source; choose a fresh index")
        return
    summary, seen = {}, set()
    current = None
    codes, counts = array("I"), array("Q")
    source_records = source_pixels = 0

    def flush(category):
        if category in EXCLUDED or category is None:
            return
        if not re.fullmatch(r"[a-z0-9_]+", category):
            raise ValueError("Invalid histogram category name")
        values = np.frombuffer(codes, dtype=np.uint32)
        pixel_counts = np.frombuffer(counts, dtype=np.uint64)
        chunks = []
        for offset in range(0, len(codes), 65536):
            batch = values[offset:offset + 65536]
            colors = np.stack([(batch >> 16) & 255, (batch >> 8) & 255, batch & 255], axis=-1)
            labs = lab(colors)
            mask = eligible(colors, labs)
            records = np.empty(int(mask.sum()), dtype=DTYPE)
            records["code"], records["lab"] = batch[mask], labs[mask]
            records["pixel_count"] = pixel_counts[offset:offset + 65536][mask]
            chunks.append(records)
        records = np.concatenate(chunks) if chunks else np.empty(0, dtype=DTYPE)
        records = records[np.argsort(records["code"])]
        if len(records) > 1 and np.any(records["code"][1:] == records["code"][:-1]):
            raise ValueError("Duplicate category/HEX in histogram")
        path = destination / (category + ".npy")
        np.save(path, records, allow_pickle=False)
        summary[category] = {
            "source_hex_count": len(codes), "source_blue_pixels": sum(counts),
            "eligible_hex_count": len(records), "file": path.name, "sha256": sha(path),
        }

    with gzip.open(source, "rt", newline="") as stream:
        reader = csv.reader(stream)
        if next(reader) != ["category", "hex", "pixel_count", "fraction_of_category_blue_pixels"]:
            raise ValueError("Unexpected histogram schema")
        for category, color, count, _fraction in reader:
            if category != current:
                flush(current)
                seen.add(current)
                if category in seen:
                    raise ValueError("Histogram categories must be contiguous")
                current, codes, counts = category, array("I"), array("Q")
            number = int(count)
            source_records += 1
            source_pixels += number
            if category not in EXCLUDED:
                if not re.fullmatch(r"#[0-9A-Fa-f]{6}", color) or number < 1:
                    raise ValueError("Invalid histogram record")
                codes.append(int(color[1:], 16))
                counts.append(number)
        flush(current)
    if not summary:
        raise ValueError("Histogram has no named elements")
    save(destination / "index.json", {
        "source_sha256": digest, "source_file": source.name, "source_records": source_records,
        "source_blue_pixels": source_pixels, "categories": summary,
        "selection": "Nearest CIELAB76 among every eligible exact HEX for the selected element; frequency only breaks equal-distance ties",
        "eligibility": "Hue160-280 degrees; S>=0.10; V>=0.08; L*>=8",
    })


class ExactCodes:
    def __init__(self, path):
        self.records = np.load(path, mmap_mode="r", allow_pickle=False)
        if self.records.dtype != DTYPE:
            raise ValueError("Unexpected histogram index dtype")

    def __contains__(self, color):
        if not isinstance(color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
            return False
        code = int(color[1:], 16)
        index = int(np.searchsorted(self.records["code"], code))
        return index < len(self.records) and int(self.records[index]["code"]) == code


class HistogramLookup(Mapping):
    def __init__(self, directory):
        self.directory = Path(directory)
        self.manifest = json.loads((self.directory / "index.json").read_text())
        self.cache = {}

    def __iter__(self):
        return iter(self.manifest["categories"])

    def __len__(self):
        return len(self.manifest["categories"])

    def __getitem__(self, element):
        if element not in self.manifest["categories"]:
            raise KeyError(element)
        if element not in self.cache:
            item = self.manifest["categories"][element]
            path = self.directory / item["file"]
            if path.name != element + ".npy" or path.parent != self.directory or sha(path) != item["sha256"]:
                raise ValueError("Histogram index bytes changed")
            self.cache[element] = ExactCodes(path)
        return self.cache[element]

    def inventory(self):
        return {
            "source_sha256": self.manifest["source_sha256"], "matching": self.manifest["selection"],
            "elements": {name: {"source_hex_count": item["source_hex_count"], "eligible_hex_count": item["eligible_hex_count"]}
                         for name, item in self.manifest["categories"].items()},
            "note": "Category inventory, not a16-code palette; code queries all eligible exact colors before the image call.",
        }

    def nearest(self, anchor, element):
        if element not in self:
            raise ValueError("Unknown histogram element")
        records = self[element].records
        if not len(records):
            raise ValueError("No visibly blue source code for " + element)
        distance = np.linalg.norm(records["lab"] - lab(rgb(anchor["hex"])), axis=-1)
        order = np.lexsort((records["code"], -records["pixel_count"].astype(float), distance))[:3]
        candidates = [
            {"hex": f"#{int(records[index]['code']):06X}", "distance_CIELAB76": round(float(distance[index]), 4),
             "exact_source_pixel_count": int(records[index]["pixel_count"])}
            for index in order
        ]
        return {
            "hex": candidates[0]["hex"], "reference_anchor": anchor,
            "distance_CIELAB76": candidates[0]["distance_CIELAB76"],
            "exact_source_pixel_count": candidates[0]["exact_source_pixel_count"],
            "nearest_candidates": candidates, "eligible_lookup_codes": len(records),
            "full_category_hex_count": self.manifest["categories"][element]["source_hex_count"],
            "lookup_source_sha256": self.manifest["source_sha256"],
            "selection_rule": self.manifest["selection"],
            "large_color_distance_warning": float(distance[order[0]]) > 10,
        }
