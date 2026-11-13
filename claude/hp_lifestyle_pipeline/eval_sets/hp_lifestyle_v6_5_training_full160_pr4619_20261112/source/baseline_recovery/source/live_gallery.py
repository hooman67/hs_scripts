import argparse
import copy
import json
import mimetypes
import time
from datetime import datetime, timezone
from pathlib import Path

import color_full160 as batch
from pilot import BUCKET, digest, load, maybe_s3_client, save

LABELS = [
    "V6.4 / PR 4523 - V15.7 shapes",
    "V6.4 / PR 4619 - V15.8 stats in rewriter + strong lighting",
    "V6.4 / PR 4619 - V15.8 stats in rewriter + strong lighting + better colors and walls",
]


def optional(path):
    try:
        return load(path)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def owner_alive(owner):
    try:
        fields = Path(f"/proc/{owner['pid']}/stat").read_text().rpartition(")")[2].split()
        return fields[0] != "Z" and fields[19] == owner["identity"]
    except FileNotFoundError:
        return False


class Gallery:
    def __init__(self):
        self.root = batch.ROOT
        self.manifest = load(self.root / "pilot-manifest.json")
        self.cases = load(self.root / "pilot-cases.json")
        self.prefix = self.manifest["s3_prefix"] + "-live/gallery"
        self.url = "https://foundry-aws-corp.adobe.io/asset/" + BUCKET + "/" + self.prefix + "/index.html"
        self.output = self.root / "live-gallery"
        self.output.mkdir(exist_ok=True)
        self.state = optional(self.root / "live-gallery-receipt.json") or {"images": {}}
        self.s3 = None

    def client(self):
        if self.s3 is None:
            self.s3 = maybe_s3_client(BUCKET)
        return self.s3

    def put_new(self, name, body):
        response = self.client().put_object(
            Bucket=BUCKET, Key=self.prefix + "/" + name, Body=body,
            ContentType=mimetypes.guess_type(name)[0] or "application/octet-stream",
            CacheControl="no-store" if not name.startswith("images/") else "max-age=300",
            Metadata={"sha256": digest(body)}, IfNoneMatch="*",
        )
        assert self.client().get_object(Bucket=BUCKET, Key=self.prefix + "/" + name)["Body"].read() == body
        return response

    def new_image(self, source, name):
        checksum = digest(source.read_bytes())
        if name not in self.state["images"]:
            body = source.read_bytes()
            self.put_new(name, body)
            target = self.output / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
            self.state["images"][name] = checksum
            save(self.root / "live-gallery-receipt.json", self.state)
        assert self.state["images"][name] == checksum
        return "./" + name

    def snapshot(self, upload=False):
        source = load(batch.blue.SCRIPTS / "gallery-data.json")
        groups = copy.deepcopy(source["groups"])
        by_key = {case["prompt_key"]: case for case in self.cases}
        native_prefix = self.manifest["prior_native_report"].rsplit("/", 1)[0]
        color_prefix = self.manifest["prior_color_report"].rsplit("/", 1)[0]
        counts = {name: {"ok": 0, "error": 0, "pending": 0} for name in ("shapes", "native", "color")}
        for group in groups:
            base = next(e for e in group["experiments"] if e["id"] == "v6_4_pr4523")
            group["contexts"] = [c for c in group["contexts"] if "V6.4" in c["label"]]
            experiments = [{"id": name, "label": label, "cards": []}
                           for name, label in zip(("shapes", "native", "color"), LABELS)]
            for old_card in base["cards"]:
                case = by_key[old_card["prompt_key"]]
                native_folder = self.root / "native/rows" / case["id"]
                color_folder = self.root / "color/rows" / case["id"]
                native, color = optional(native_folder / "result.json"), optional(color_folder / "result.json")
                context = (native or {}).get("scap_context") or optional(native_folder / "scap_context.json") or {}
                stage = optional(self.root / "stages" / (case["id"] + ".json")) or {}
                for experiment, result in zip(experiments, (None, native, color)):
                    kind = experiment["id"]
                    card = {
                        "rank": case["rank"], "prompt_key": case["prompt_key"],
                        "prompt": case["user_prompt"], "environment": case["environment"],
                        "status": "ok" if kind == "shapes" else (result or {}).get("status", "pending"),
                        "stage": stage.get("stage", "Queued"), "error": (result or {}).get("error"),
                        "no_statistics_fallback": kind != "shapes" and context.get("statistics_disabled", False),
                        "reused": (kind == "native" and case["native_reused"])
                        or (kind == "color" and case["color_reused"]),
                    }
                    if kind == "shapes":
                        card.update(image=f"{native_prefix}/images/{case['row_idx']}-before.png",
                                    image_sha256=case["baseline_sha256"], rewritten_prompt=case["baseline_prompt"])
                    elif result:
                        card["rewritten_prompt"] = result.get("prompt")
                        if result["status"] == "ok":
                            if kind == "native" and case["native_reused"]:
                                card["image"] = f"{native_prefix}/images/{case['row_idx']}-after.png"
                            elif kind == "color" and case["color_reused"]:
                                card["image"] = f"{color_prefix}/images/{case['rank']}-poc.png"
                            else:
                                path = (native_folder if kind == "native" else color_folder) / "gpt_1.png"
                                name = f"images/{case['row_idx']}-{kind}.png"
                                card["image"] = self.new_image(path, name) if upload else "./" + name
                    counts[kind][card["status"]] += 1
                    experiment["cards"].append(card)
            group["experiments"] = experiments
        status = optional(self.root / "background-status.json") or {}
        owner = optional(self.root / "generation-owner.json")
        phase = status.get("phase", "prepared")
        if owner and not owner_alive(owner) and phase != "published":
            phase = "Stopped - unfinished cards remain pending; no automatic retries"
        receipt = optional(self.root / "pilot-publication-receipt.json")
        return {
            "title": "HP lifestyle diversity - live V6.4 comparison",
            "source_url": "https://foundry-aws-corp.adobe.io/asset/" + BUCKET
                          + "/eval_sets/hp_lifestyle_grouped_diversity_20261111/gallery/index.html",
            "group_count": 16, "experiment_count": 3, "image_count": 480,
            "groups": groups, "counts": counts, "phase": phase,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "detailed_url": receipt["url"] if receipt else None,
        }

    def publish(self):
        if not self.state.get("static_published"):
            assert not self.client().list_objects_v2(
                Bucket=BUCKET, Prefix=self.prefix + "/", MaxKeys=1,
            ).get("KeyCount", 0), "Live prefix already exists"
            for source, target in (
                ("live-gallery-style.css", "style.css"), ("live-gallery-main.js", "main.js"),
                ("live-gallery-index.html", "index.html"),
            ):
                body = (batch.blue.SCRIPTS / source).read_bytes()
                (self.output / target).write_bytes(body)
                self.put_new(target, body)
            self.state["static_published"] = True
        data = self.snapshot(upload=True)
        save(self.output / "data.json", data)
        body = (self.output / "data.json").read_bytes()
        condition = {"IfMatch": self.state["etag"]} if self.state.get("etag") else {"IfNoneMatch": "*"}
        response = self.client().put_object(
            Bucket=BUCKET, Key=self.prefix + "/data.json", Body=body,
            ContentType="application/json", CacheControl="no-store",
            Metadata={"sha256": digest(body)}, **condition,
        )
        assert self.client().get_object(Bucket=BUCKET, Key=self.prefix + "/data.json")["Body"].read() == body
        self.state.update(etag=response["ETag"], url=self.url, updated_at=data["updated_at"], counts=data["counts"])
        save(self.root / "live-gallery-receipt.json", self.state)
        print(json.dumps({"live_url": self.url, "phase": data["phase"], "counts": data["counts"]}), flush=True)
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("publish", "watch"))
    action = parser.parse_args().action
    gallery = Gallery()
    if action == "watch":
        with (batch.ROOT / "live-gallery.lock").open("x") as lock:
            lock.write(str(time.time()))
        while True:
            data = gallery.publish()
            if data["phase"] == "published" or data["phase"].startswith("Stopped"):
                break
            time.sleep(15)
    else:
        gallery.publish()
