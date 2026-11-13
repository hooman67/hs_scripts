"""Fixed whole-image/native-pixel coverage and independent unscored acquisition."""

import fcntl
import json
from pathlib import Path

import common
from jsonschema import Draft202012Validator
from PIL import Image

ACQUISITION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["record"],
    "properties": {"record": {"type": "string", "minLength": 1}},
}


def positions(length, size, overlap):
    last = max(0, length - size)
    values = list(range(0, last + 1, size - overlap))
    return values if values[-1] == last else [*values, last]


def prepare(runtime):
    policy_path = common.ROOT / "visual_policy.json"
    policy = json.loads(policy_path.read_text())
    size, overlap = policy["tile_size_pixels"], policy["overlap_pixels"]
    if (size, overlap) != (768, 192):
        raise ValueError("Native tile policy differs from Astra's specified mechanism")
    sources = {
        role: {"local_path": runtime[role], "sha256": common.sha(runtime[role])}
        for role in ("generated_image", "twin_image")
    }
    identity = {"sources": sources, "policy_sha256": common.sha(policy_path)}
    directory = common.ROOT / "evaluation/visual_packets" / common.fingerprint(identity)
    directory.mkdir(parents=True, exist_ok=True)
    manifest_path = directory / "manifest.json"
    with (directory / "packet.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if manifest_path.exists():
            packet = json.loads(manifest_path.read_text())
            if packet["identity"] != identity or any(
                common.sha(item["local_path"]) != item["sha256"]
                for item in [*packet["delivered_images"], *packet["coverage"]]
            ):
                raise ValueError("Cached native-pixel packet changed")
            return packet
        delivered, coverage = [], []
        for label, role in (("A", "generated_image"), ("B", "twin_image")):
            source = sources[role]
            delivered.append({**source, "label": label + ": full original image"})
            with Image.open(source["local_path"]) as image:
                image.load()
                if common.sha(source["local_path"]) != source["sha256"]:
                    raise ValueError("Source changed while decoding native pixels")
                width, height = image.size
                xs = positions(width, size, overlap)
                ys = positions(height, size, overlap)
                seen = set()
                number = 0
                for y in ys:
                    for x in xs:
                        number += 1
                        box = (x, y, min(width, x + size), min(height, y + size))
                        tile = directory / f"{label}_tile_{number:03d}.png"
                        if tile.exists():
                            raise ValueError(
                                "Incomplete packet needs explicit recovery"
                            )
                        image.crop(box).save(tile, format="PNG")
                        digest = common.sha(tile)
                        unique = digest not in seen
                        seen.add(digest)
                        entry = {
                            "local_path": str(tile.resolve()),
                            "sha256": digest,
                            "label": f"{label}: neutral tile {number:03d}",
                        }
                        coverage.append(
                            {
                                "source_role": role,
                                "source_dimensions": [width, height],
                                "crop_box": list(box),
                                "tile_dimensions": [box[2] - box[0], box[3] - box[1]],
                                "delivered": unique,
                                **entry,
                            }
                        )
                        if unique:
                            delivered.append(entry)
        encoded = sum(
            4 * ((Path(item["local_path"]).stat().st_size + 2) // 3)
            for item in delivered
        )
        if encoded > policy["max_encoded_image_bytes"]:
            raise ValueError("Complete lossless packet exceeds safe API image budget")
        packet = {
            "identity": identity,
            "delivered_images": delivered,
            "coverage": coverage,
            "base64_image_bytes": encoded,
            "image_adapter_detail": policy["image_adapter_detail"],
            "image_transform": "Full originals plus lossless decoded-pixel tiles; no resizing or sharpening.",
        }
        common.write_json(manifest_path, packet)
        return packet


def parts(packet):
    content = []
    for item in packet["delivered_images"]:
        if common.sha(item["local_path"]) != item["sha256"]:
            raise ValueError("Delivered full image/tile changed")
        content += common.LEGACY.image_parts(item["label"], item["local_path"])
    return content


def check_request_budget(messages):
    encoded = sum(
        len(item["image_url"]["url"].split(",", 1)[1])
        for message in messages
        if isinstance(message["content"], list)
        for item in message["content"]
        if item["type"] == "image_url"
    )
    budget = json.loads((common.ROOT / "visual_policy.json").read_text())[
        "max_encoded_request_image_bytes"
    ]
    if encoded > budget:
        raise ValueError(f"Complete request exceeds image budget: {encoded} > {budget}")
    return encoded


def acquire(runtime, stage, output, packet, scope, client):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    prompt_path = common.ROOT / "prompts/visual_acquisition.txt"
    request = {
        "stage": stage,
        "image_stage": runtime["image_stage"],
        "authorized_scope": scope,
        "protocol_freeze_sha256": common.verify_freeze(),
        "prompt_sha256": common.sha(prompt_path),
        "visual_packet": packet,
        "model": common.MODEL,
        "reasoning_effort": "high",
        "scored": False,
        "other_judge_findings_withheld": True,
        "scene_prompt_and_target_feedback_withheld": True,
        "max_completion_tokens": 12000,
        "schema": ACQUISITION_SCHEMA,
    }
    fingerprint = common.fingerprint(request)
    result_path = output / "result.json"
    if result_path.exists():
        result = json.loads(result_path.read_text())
        if result["fingerprint"] != fingerprint:
            raise ValueError("Acquisition belongs to a different branch/request")
        if common.sha(result["chunks_path"]) != result["chunks_sha256"]:
            raise ValueError("Actual acquisition stream changed")
        collector = common.Collector()
        for line in Path(result["chunks_path"]).read_text().splitlines():
            collector.feed(json.loads(line))
        value = collector.result()
        if value != result["observation"]:
            raise ValueError("Acquisition differs from actual Astra response")
    else:
        common.write_json(output / "request.json", request)
        payload = {
            "authorized_placement_scope": scope,
            "image_stage": runtime["image_stage"],
        }
        value, receipt = common.model_completion(
            [
                {"role": "system", "content": prompt_path.read_text()},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": json.dumps(payload)},
                        *parts(packet),
                    ],
                },
            ],
            ACQUISITION_SCHEMA,
            request["max_completion_tokens"],
            output,
            client=client,
        )
        Draft202012Validator(ACQUISITION_SCHEMA).validate(value)
        result = {"fingerprint": fingerprint, "observation": value, **receipt}
        common.write_json(result_path, result)
    Draft202012Validator(ACQUISITION_SCHEMA).validate(value)
    if not value["record"].strip():
        raise ValueError("Acquisition contains no actual observation record")
    return {
        "record": value["record"],
        "path": str(result_path.resolve()),
        "sha256": common.sha(result_path),
        "fingerprint": fingerprint,
        "scored": False,
    }
