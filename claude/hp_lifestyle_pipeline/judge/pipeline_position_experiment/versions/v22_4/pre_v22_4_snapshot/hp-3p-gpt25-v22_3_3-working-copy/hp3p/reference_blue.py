import hashlib
import io
import json
import math

from PIL import Image, ImageDraw, ImageFont

from .histogram import save
from .openai_client import IMAGE_MODEL, TEXT_MODEL, load_prompt
from .reference_style import photometry, select_reference

VERSION = "unified-blue-v24.3.3-clean-fixed-rewrite-affine-guard-twin-camera-guide-only-no-mask"


def digest(body):
    return hashlib.sha256(body).hexdigest()


def attachments(images):
    return [{"mime": mime, "sha256": digest(body), "bytes": len(body)} for mime, body in images]


class ReferenceBlue:
    def __init__(self, catalog, lookup):
        self.catalog = [ref for ref in catalog if ref.human_presence in ("human", "no_humans")]
        if not self.catalog or len({ref.id for ref in self.catalog}) != len(self.catalog):
            raise ValueError("Reference blue requires unique IDs and existing human/no_humans tags")
        self.lookup = lookup
        self.metadata = [
            {"id": ref.id, "tone": ref.tone, "content": ref.content, "human_presence": ref.human_presence,
             "sha256": digest(ref.data), **photometry(ref.data)} for ref in self.catalog
        ]
        self.identity = {
            "histogram_sha256": lookup.manifest["source_sha256"],
            "catalog_sha256": digest(json.dumps(self.metadata, sort_keys=True).encode()),
        }
        self.contacts = []
        font = ImageFont.load_default(size=14)
        for offset in range(0, len(self.catalog), 60):
            batch = self.catalog[offset:offset + 60]
            sheet = Image.new("RGB", (1152, math.ceil(len(batch) / 6) * 150), "white")
            draw = ImageDraw.Draw(sheet)
            for index, ref in enumerate(batch):
                image = Image.open(io.BytesIO(ref.data)).convert("RGB")
                image.thumbnail((184, 124))
                x, y = index % 6 * 192, index // 6 * 150
                sheet.paste(image, (x + (192 - image.width) // 2, y + 22 + (124 - image.height) // 2))
                draw.text((x + 4, y + 2), ref.id + (" H" if ref.human_presence == "human" else " NH"),
                          font=font, fill="#172b46")
            buffer = io.BytesIO()
            sheet.save(buffer, format="JPEG", quality=90)
            self.contacts.append(("image/jpeg", buffer.getvalue()))

    def select(self, client, prompt, out):
        schema = {
            "type": "object", "additionalProperties": False,
            "required": ["tone", "content", "brightness", "human_policy", "reference_ids", "rationale"],
            "properties": {
                "tone": {"type": "string", "enum": sorted({item["tone"] for item in self.metadata})},
                "content": {"type": "string", "enum": sorted({item["content"] for item in self.metadata})},
                "brightness": {"type": "string", "enum": ["bright", "balanced", "dim", "unspecified"]},
                "human_policy": {"type": "string", "enum": ["human", "no_humans"]},
                "reference_ids": {"type": "array", "minItems": 1, "maxItems": 8,
                                  "items": {"type": "string", "enum": [ref.id for ref in self.catalog]}},
                "rationale": {"type": "string"},
            },
        }
        system = load_prompt("select_reference")
        text = "Original user request: " + prompt + "\n\nCANDIDATE_METADATA:\n" + json.dumps(self.metadata)
        save(out / "selection_request.json", {
            "model": TEXT_MODEL, "system": system, "text": text, "schema": schema,
            "images": attachments(self.contacts), "max_retries": 0,
        })
        proposal = client.chat_json(system, text, self.contacts, schema)
        save(out / "selection_response.json", proposal)
        selected = select_reference(proposal, self.metadata, prompt)
        save(out / "selection_result.json", {**selected, "rationale": proposal["rationale"]})
        return next(ref for ref in self.catalog if ref.id == selected["reference_id"]), selected, proposal["rationale"]

    def rewrite(self, client, system, text, images, schema, selection, prompt, out, suffix=""):
        """Stage B with the single selected reference; blue stays plain-language text (no HEX anchoring)."""
        human = selection["human_policy"] == "human"
        human_policy = (
            "The original request explicitly asks for people. Include only the requested people, "
            "naturally placed without product occlusion. This explicitly overrides the baseline "
            "no-person restriction. Do not copy identities or faces from the style image."
            if human else "Human policy: no people, hands, human silhouettes or human reflections."
        )
        system += "\n\n" + human_policy + suffix
        save(out / "planning_request.json", {
            "model": TEXT_MODEL, "system": system, "text": text, "schema": schema,
            "images": attachments(images), "max_retries": 0, **self.identity,
        })
        response = client.chat_json(system, text, images, schema)
        save(out / "planning_response.json", response)
        rewritten = {**response, "prompt": response["prompt"] + "\n\n" + (
            "Include only the requested people, naturally placed without product occlusion." if human else
            "No people, hands, human silhouettes or human reflections.")}
        save(out / "derived_rewrite.json", rewritten)
        return rewritten

    def record_image(self, out, prompt, images, size, mask):
        save(out / "image_request.json", {
            "model": IMAGE_MODEL, "prompt": prompt, "images": attachments(images),
            "size": size, "quality": "high", "n": 1, "mask_sha256": digest(mask) if mask else None, "max_retries": 0,
        })
