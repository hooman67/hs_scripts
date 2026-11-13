import hashlib
import io
import json
import re
import time
from pathlib import Path

from PIL import Image

from .captions import format_caption
from .catalog import StyleRef, labels, pick_refs
from .geometry import (
    GEOMETRY_SCHEMA,
    TWIN_GEOMETRY_SCHEMA,
    build_guide,
    describe_geometry,
    product_anchor,
    supplied_product_size,
    twin_camera_summary,
    twin_camera_text,
)
from .grade import describe, match_reference, nearest_reference
from .histogram import save
from .invariants import GUARD_VERSION, assess_product_affine, json_native
from .mask import prepare
from .openai_client import IMAGE_MODEL, TEXT_MODEL, load_prompt
from .reference_blue import attachments

WIDTH, HEIGHT = 1216, 912
SIZE = f"{WIDTH}x{HEIGHT}"
PIPELINE_VERSION = "unified-blue-scale-v22.3.3-clean-fixed-rewrite-affine-guard-twin-camera-guide-only-no-mask"

_HIGH_FILL_THRESHOLD = 0.45


def _select_schema(tones, contents) -> dict:
    return {"type": "object", "additionalProperties": False, "required": ["tone", "content", "rationale"],
            "properties": {"tone": {"type": "string", "enum": list(tones)},
                           "content": {"type": "string", "enum": list(contents)},
                           "rationale": {"type": "string"}}}


def _plan_schema(geometry_schema: dict) -> dict:
    return {"type": "object", "additionalProperties": False,
            "required": ["geometry", "product_category"],
            "properties": {"geometry": geometry_schema,
                           "product_category": {"type": "string",
                                                "enum": ["laptop", "printer", "monitor", "desktop", "other"],
                                                "description": "Category of the fixed product in Image 1."}}}


_PLAN_SCHEMA = _plan_schema(GEOMETRY_SCHEMA)
_TWIN_PLAN_SCHEMA = _plan_schema(TWIN_GEOMETRY_SCHEMA)
_WRITE_SCHEMA = {"type": "object", "additionalProperties": False,
                 "required": ["layout", "camera", "composition", "prompt"],
                 "properties": {"layout": {"type": "string"}, "camera": {"type": "string"},
                                "composition": {"type": "string"}, "prompt": {"type": "string"}}}
_PLAN_HEAD = ("Plan camera, composition, geometry and editing text directly from the original "
              "user request and Image 1.")
_PRINTER_WALL = (" Printers normally stand against a wall: for a printer, set back_edge_against_wall true unless "
                 "the original user request clearly places it away from walls.")
_GEOMETRY_ONLY = ("\n\nTHIS CALL PLANS GEOMETRY ONLY. Return only geometry and product_category. "
                  "Camera text, composition, the image prompt, materials and scale notes are written in a later "
                  "call after the geometry guide is drawn."
                  "\n\nSUPPORT PLAUSIBILITY: The support must be real furniture that people actually use to hold "
                  "this product in this kind of room, standing where such furniture normally stands. The requested "
                  "support type names the furniture; it does not fix its size. Choose support_width_m, "
                  "support_depth_m and support_height_m typical for that furniture and for using this product: the "
                  "top is only as deep as such furniture normally is while still holding the product's base, and "
                  "the height suits how people reach and use the product. Set back_edge_against_wall true when that "
                  "furniture would normally stand against a wall in this room; the wall then stands at the "
                  "support's back edge." + _PRINTER_WALL + " The wall can never stand between camera and product. "
                  "Secondary furniture "
                  "in furniture_boxes stands beside, behind or in front of the support, never inside it.")
_WRITE_HEAD = ("Write camera, composition and editing text from Image 1 (the fixed geometry guide containing the "
               "real product), Image 3 (the same product on white), the FIXED GEOMETRY below and the original "
               "user request.")
_TRANSLATION_ONLY = """TRANSLATION-ONLY PRODUCT PLACEMENT; RECOMPOSED SUPPORT
Determine density from the existing product guide bounds on the current canvas. HIGH-FILL/CLOSE applies when product width or height is at least 45% of the corresponding canvas dimension. LOWER-FILL/MEDIUM-WIDE applies only when both are below 45%.

In both branches, preserve product identity, exact pixel width and height, yaw, pitch, roll, viewing angle, visible faces, camera-facing surfaces, projection, perspective, foreshortening, silhouette proportions, state, finish, details, logo, display content and full visibility.

HIGH-FILL/CLOSE: Preserve the product's exact initial x-y coordinates from the supplied guide. This is unconditional: do not test relocation feasibility and do not move the product even if exact size and all other invariants could be preserved. Drop any user relocation, centering, layout, emphasis, support-edge or composition request that conflicts with this fixed product position. Independently recompose support and room around the fixed product.

LOWER-FILL/MEDIUM-WIDE: Choose product x-y freely for usable composition using rigid image-plane translation only; movement is optional. Independently recompose support and room beneath or around the product; product and support need not move together. Preserve every product invariant. Do not move the product merely to center it or make it more prominent.

Preserve exact product pixel width and height and every other product invariant. Never shrink, enlarge, zoom, reframe, rotate, reproject, or crop the product to make a move feasible. Where translation is allowed, if a move cannot preserve every invariant, retain the initial x-y coordinates instead.

For HIGH-FILL/CLOSE, no geometric product change is permitted. For LOWER-FILL/MEDIUM-WIDE, the only permitted product change is one rigid image-plane x-y translation. Keep its exact pixel width and height, yaw, pitch, roll, viewing angle, visible faces, camera-facing surfaces, perspective, projection, foreshortening, silhouette, aspect proportions, open/closed and powered state, finish, details, logo and display content. Do not rotate, mirror, resize, shear, warp, reproject, redraw or activate the product. Do not zoom, reframe or change the viewpoint in a way that alters the product.

At the chosen product position, compose a category- and scenario-appropriate support beneath its weight-bearing base. The support may change independently of the product's translation: do not preserve baseline product-to-edge distances, tabletop extents or absolute support-edge locations as requirements. Fully support the base without floating or overhang, with believable front, back and side clearances, natural weight-bearing contact, a contact shadow and material-appropriate reflections on the support.

Construct furniture around the unchanged product orientation. A printer must sit square to its support in 3D with usable access to its operating front. A laptop must face a usable seating or working edge with clear access to its keyboard and display. Do not rotate the product or reveal a different face to fit the furniture. Support axes, room perspective, horizon and vanishing geometry must be compatible with the unchanged product projection at its chosen position; do not retain incompatible geometry from the initial layout.

Keep exactly one product, entirely inside the frame and fully visible. No prop, furniture edge or foreground object may occlude it. Remove the gray guide, diagram marks and any ghost or duplicate product. If the product moves, complete the vacated location as part of the scene. If a candidate placement violates any product or support requirement, choose another placement or recompose the support and room without relaxing the product invariants."""
_PRIORITY = """STAGE B. Image 1 contains an initial support diagram and the real product at its initial x-y position. The product's exact orientation/view and pixel size are fixed. HIGH-FILL permits no geometric product change; LOWER-FILL permits only rigid image-plane x-y translation.

PRIORITY ORDER (strict):
1. The product: exact identity, orientation/view, perspective, foreshortening, scale, silhouette, state, details and full visibility. Never rotate, mirror, resize, reproject, redraw, crop or occlude it.
2. A believable, category- and scenario-appropriate support and room constructed around the unchanged product at its density-permitted position, with full base support, usable access and consistent furniture/perspective geometry. For LOWER-FILL only, initial position, baseline product-to-edge distances, tabletop extents and support-edge locations are not requirements.
3. The original user request, followed by defaults, wherever compatible with priorities 1 and 2.

""" + _TRANSLATION_ONLY + """

When the user request requires a different product size, viewpoint or orientation, drop that part. Adapt support and layout requests around the unchanged product. Layout, emphasis, framing and focal-point requests do not authorize rotation, resizing, reprojection, crop or occlusion.

Your camera, composition and prompt must preserve the product view and pixel size shown in Image 1 while describing the density-permitted product position and support. The gray region is baseline planning evidence, not a required tabletop shape, extent, edge location or product-to-edge distance. Compose the support and room around the unchanged product at its permitted position. Retain restrictions on plausible physical scale, props and product visibility, but do not carry forward baseline tabletop extents or edge clearances as constraints.

WRITE IN PLAIN VISUAL WORDS. The image model follows pictures and plain descriptions, not measurements. Use the numbers below only to choose your words. In layout, camera, composition and prompt, describe sizes, distances, angles and positions the way a photographer briefs a set builder: by comparison with the laptop, the frame edges and nearby objects (for example "the tabletop continues about two laptop widths to the left of the laptop and a little less to the right", "the tabletop is about three times as deep as the laptop", "the table ends inside the frame on both sides", "camera at standing eye height, looking gently down").

FIXED GEOMETRY (derived by code from Image 1):
"""
_WRITE_OVERRIDE = ("\n\nSTAGE-B PLACEMENT AND SUPPORT OVERRIDE: geometry is an initial layout in this call, not an output. "
                   "Image 1 is the drawn geometry guide and is visible to you now. Follow the PRIORITY ORDER "
                   "in the user message: product invariants first, believable recomposed support and room second, user request third. "
                   "Return layout, camera, composition and prompt, each written in plain visual words. "
                   "Treat product view, geometry, pixel width and pixel height as authoritative. Treat product frame "
                   "coordinates according to the active density branch. Treat all gray-support edges, distances, extents and "
                   "support-crop descriptions as baseline evidence that may be replaced. Apply the deterministic "
                   "guide-density policy in the user message when choosing a usable product position. In layout, camera, "
                   "composition and prompt, describe the chosen position and the support built beneath it: the usable "
                   "approach or working edge, full support of the weight-bearing base, believable front/back/side "
                   "clearances, and consistent furniture and room perspective. Describe resulting geometry, not "
                   "baseline distances unless they remain appropriate. Support edges and tabletop extents may be "
                   "recomposed independently of product translation. Construct a printer's support square to its fixed "
                   "orientation in 3D; construct a laptop's support and user position around its fixed working "
                   "orientation. Include the translation-only product-placement and recomposed-support policy. Use the "
                   "actual product category, not laptop, for other products."
                   "\n\nIMAGE MODEL INPUT: the image model receives ONLY Image 1 and your text. It never sees the "
                   "style image or the product on white. In layout, camera, composition and prompt, never "
                   "mention any image other than Image 1 or where a style or material came from. "
                   "Describe the lighting, palette, materials and textures you take from the style image "
                   "directly in words, as a brief for a photographer who has never seen it. Never explain where a "
                   "color, material or blue carrier was adapted or transferred from. Product detail comes from the real "
                   "product pixels in Image 1.")
_WRITE_PRINTER_WALL = ("\n\nPRINTER AGAINST THE WALL: the printer's back stands right against the wall at the "
                       "support's back edge, with no gap, shelf or objects between them. State this plainly in the "
                       "prompt.")
_LEGEND = ("GUIDE LEGEND: Image 1 is the current canvas to edit. Its real product pixels establish the exact product "
           "appearance, view and pixel size to preserve. The active density branch determines whether their frame position "
           "is fixed or may change by rigid x-y translation. The flat "
           "gray region and its boundaries show an initial support plan, not output pixels or required support edges, "
           "distances or extents. At the chosen product position, compose an appropriate support beneath the unchanged "
           "product. Remove all gray-guide and diagram remnants, any duplicate product and any product-shaped remnant "
           "at the initial location. Keep only one intact product at the final location. ")
_FINAL_CHECK = ("\n\nFinal check before rendering: the product retains its exact identity, orientation/view, "
                "visible faces, perspective/foreshortening, scale, silhouette, state and details. HIGH-FILL permits no "
                "geometric product change. LOWER-FILL permits only one rigid x-y translation. The support is recomposed beneath the product's chosen "
                "position with believable edge clearances, access, full base contact and a plausible contact shadow. "
                "The surrounding scene has consistent perspective. The product is fully visible and unoccluded. No "
                "product distortion is allowed. Preserve exact product pixel width and height and every other product "
                "invariant. Never shrink, enlarge, zoom, reframe, rotate, reproject, or crop the product to make a move "
                "feasible. Where translation is allowed, if a move cannot preserve every invariant, retain the initial "
                "x-y coordinates instead. No diagram remnants, old contact shadow, ghost or duplicate "
                "product remain.")
_FIXED_POSITION_FALLBACK = """

PRODUCT-INVARIANT FALLBACK — EXECUTE THIS OVERRIDE. Keep the product at the exact initial x-y coordinates shown in Image 1. Preserve its exact pixel width and height, orientation/view, projection, perspective, foreshortening, silhouette, state, finish and every detail. Ignore every earlier product-relocation, centering, emphasis or conflicting layout instruction. Independently recompose the support and room around the fixed product position. Keep the whole product fully visible and unoccluded, with its base fully supported and a natural contact shadow. Do not shrink, enlarge, zoom, reframe, rotate, reproject, shear, warp or crop the product.
"""

_FIXED_REWRITE_PRIORITY = """STAGE B FIXED-POSITION FALLBACK. Image 1 contains the real product and an initial support diagram. Keep the product at the exact initial frame position shown in Image 1. Preserve its exact pixel width and height, orientation/view, visible faces, projection, perspective, foreshortening, silhouette, state, finish, details and full visibility.

PRIORITY ORDER (strict):
1. The product remains at the exact initial frame position, with its appearance, view and size unchanged. Never move, rotate, mirror, resize, reproject, redraw, crop or occlude it.
2. Recompose a believable category- and scenario-appropriate support and room around that fixed product, with full base support, usable access and consistent furniture and room perspective.
3. Follow the original request and style guidance only where compatible with priorities 1 and 2. Ignore requests to reposition, center or otherwise change the product.

The gray support region is planning evidence rather than output pixels. It does not require preserving an implausible support edge or tabletop extent. Build a support beneath the fixed product position. A printer must sit square to its support in 3D with usable access to its operating front. A laptop must face a usable seating or working edge with clear access to its keyboard and display. Keep exactly one product, entirely inside the frame and fully visible. Remove the gray guide, diagram marks and any ghost or duplicate product.

WRITE IN PLAIN VISUAL WORDS. Return layout, camera, composition and prompt that all describe the product at its exact initial frame position and a coherent scene built around it. Output only the resolved fixed-position scene. Do not echo, quote, mention, explain or discuss any rejected movement or alternate placement request, even to say that it conflicts or was ignored.

FIXED GEOMETRY (derived by code from Image 1):
"""

_FIXED_REWRITE_OVERRIDE = ("\n\nSTAGE-B FIXED-POSITION FALLBACK OVERRIDE: Image 1 is visible now. Return layout, "
                           "camera, composition and prompt in plain visual words. Keep the product at the exact initial "
                           "frame position shown in Image 1, with exact pixel width, pixel height, orientation, view, "
                           "projection, perspective, foreshortening, silhouette, state, finish and details. Do not describe "
                           "any alternate product position. Output only the resolved fixed-position scene; never echo, "
                           "mention or explain a rejected movement request, even to say that it conflicts. Build the "
                           "support and room around the fixed product. Preserve "
                           "the requested setting, props, lighting and materials where compatible. The image model receives "
                           "only Image 1 and your text; describe the complete photographic scene directly and do not mention "
                           "other images or references.")

_FIXED_EXECUTABLE_POLICY = ("Keep the product at the exact initial frame position shown in Image 1. Preserve its exact "
                            "pixel width and height, orientation/view, visible faces, projection, perspective, "
                            "foreshortening, silhouette, state, finish and every detail. Build a believable support and "
                            "room around that fixed product position. Fully support its weight-bearing base with natural "
                            "contact and a plausible contact shadow, maintain usable access, and keep furniture and room "
                            "perspective consistent with the unchanged product view. Keep exactly one complete, fully "
                            "visible product. Never move, rotate, mirror, resize, reproject, redraw, crop or occlude it. "
                            "Remove the gray guide, diagram marks and any ghost or duplicate product.")

_FIXED_LEGEND = ("GUIDE LEGEND: Image 1 is the current canvas to edit. Its real product pixels establish the exact "
                 "product appearance, view, pixel size and frame position to preserve. The flat gray region and its "
                 "boundaries show an initial support plan rather than output pixels. Compose an appropriate support "
                 "beneath the fixed product. Remove all gray-guide and diagram remnants and any duplicate product. ")

_FIXED_FINAL_CHECK = ("\n\nFinal check before rendering: the product remains at the exact initial frame position "
                      "shown in Image 1 and retains its exact identity, orientation/view, visible faces, projection, "
                      "perspective, foreshortening, pixel width and height, silhouette, state, finish and details. "
                      "The support is recomposed beneath that fixed product with believable edge clearances, usable "
                      "access, full base contact and a plausible contact shadow. The surrounding scene has consistent "
                      "perspective. The product is fully visible and unoccluded. Never move, shrink, enlarge, zoom, "
                      "reframe, rotate, reproject, shear, warp or crop the product. No diagram remnants, old contact "
                      "shadow, ghost or duplicate product remain.")

_FIXED_CONTRADICTIONS = (
    ("lower-fill branch", re.compile(r"\blower[ -]fill\b", re.I)),
    ("x-y placement freedom", re.compile(r"\bx\s*[-–]\s*y\b", re.I)),
    ("permitted product movement", re.compile(
        r"(?:\b(?:may|can|could|should|freely)\s+(?:be\s+)?(?:mov\w*|relocat\w*|translat\w*)|"
        r"\b(?:move|moving|relocate|relocating|translate|translating)\s+(?:the\s+)?"
        r"(?:product|laptop|printer|monitor|desktop)|"
        r"\b(?:product|laptop|printer|monitor|desktop)(?:'s)?\s+(?:position\s+)?(?:may|can|could)\s+change)",
        re.I,
    )),
)

_FIXED_META_SENTENCE = re.compile(
    r"[^.!?]*(?:request(?:ed)?|instruction)[^.!?]*"
    r"(?:mov\w*|relocat\w*|translat\w*|alternate\s+placement)[^.!?]*"
    r"(?:conflict\w*|reject\w*|ignor\w*|instead|remain\w*|fixed)[^.!?]*[.!?]?",
    re.I,
)


_STALE_IMAGE = re.compile(r"\bImages?\s+(?:[2-9]|1\d)\b|\breference(?:'s|\u2019s)|\b(?:style|selected) references?\b"
                          r"|\breference (?:image|photo|photograph|picture)\b|\bthe reference\b"
                          r"(?! (?:books?|photographs|binders?|boards?)\b)", re.I)


def _check_image_prompt(prompt: str) -> None:
    """The image call sees only Image 1, so its prompt must not point at the style reference or product render."""
    match = _STALE_IMAGE.search(prompt)
    if match:
        context = prompt[max(0, match.start() - 60):match.end() + 40]
        raise ValueError(f"Image prompt mentions an image the image model does not receive: {context!r}")


def _sha_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def _sha_json(value: dict) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _validate_fixed_executable_prompt(prompt: str) -> None:
    """Reject a fallback prompt that still grants product-placement freedom."""
    # Fixed-position prohibitions are valid and must not be mistaken for active
    # movement commands. Remove only the leading negation, verb and immediate
    # category noun before scanning the remaining executable text.
    scan = re.sub(
        r"\b(?:never|do\s+not|must\s+not|cannot|can't|may\s+not)\s+"
        r"(?:move|relocate|translate)\s+(?:the\s+)?(?:product|laptop|printer|monitor|desktop)\b",
        "fixed-product-prohibition",
        prompt,
        flags=re.I,
    )
    failures = [name for name, pattern in _FIXED_CONTRADICTIONS if pattern.search(scan)]
    if failures:
        raise ValueError("Fixed-position fallback prompt contains contradictory placement language: "
                         + ", ".join(failures))


def _strip_fixed_meta_commentary(text: str) -> str:
    """Remove rejected-movement discussion; the image model only needs the resolved scene."""
    cleaned = _FIXED_META_SENTENCE.sub(" ", text)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r" *\n *", "\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    if not cleaned:
        raise ValueError("Fixed-position Stage-B field became empty after removing movement meta-commentary.")
    return cleaned


def _stage_b_audit(out: Path, attempt: int, system: str, text: str,
                   images: list[tuple[str, bytes]], response: dict) -> dict:
    request = {
        "model": TEXT_MODEL,
        "system": system,
        "text": text,
        "schema": _WRITE_SCHEMA,
        "image_sha256": [hashlib.sha256(data).hexdigest() for _, data in images],
        "image_mime": [mime for mime, _ in images],
        "max_retries": 0,
    }
    save(out / f"stage_b_attempt_{attempt}_request.json", request)
    save(out / f"stage_b_attempt_{attempt}_response.json", response)
    return {
        "attempt": attempt,
        "system_sha256": _sha_text(system),
        "text_sha256": _sha_text(text),
        "request_sha256": _sha_json(request),
        "response_sha256": _sha_json(response),
    }


def _human_policy(selection: dict) -> tuple[str, str]:
    """Mirror reference-blue's explicit human policy for a separately audited fallback call."""
    if selection["human_policy"] == "human":
        return (
            "The original request explicitly asks for people. Include only the requested people, naturally placed "
            "without product occlusion. This explicitly overrides the baseline no-person restriction. Do not copy "
            "identities or faces from the style image.",
            "Include only the requested people, naturally placed without product occlusion.",
        )
    return (
        "Human policy: no people, hands, human silhouettes or human reflections.",
        "No people, hands, human silhouettes or human reflections.",
    )


def _wording(text: str, category: str, product_image: str) -> str:
    """Adapt laptop/table wording to the planned product category and the product render's image number."""
    text = text.replace("Image 3", product_image)
    if category == "laptop":
        return text
    for pattern, value in ((r"\blaptop\b", "product" if category == "other" else category),
                           (r"\btabletop\b", "support top"), (r"\bTable\b", "Support"), (r"\btable\b", "support")):
        text = re.sub(pattern, value, text)
    return text


def _density_policy(guide_info: dict, size: tuple[int, int]) -> tuple[str, str]:
    """Classify Stage-B placement from product occupancy in the already-rendered guide."""
    x0, y0, x1, y1 = guide_info["product_bounds_px"]
    width, height = size
    width_fraction = (x1 - x0) / width
    height_fraction = (y1 - y0) / height
    if width_fraction >= _HIGH_FILL_THRESHOLD or height_fraction >= _HIGH_FILL_THRESHOLD:
        return (
            "HIGH-FILL/CLOSE",
            "ACTIVE BRANCH: HIGH-FILL/CLOSE. Keep the product at its exact initial x-y coordinates in the "
            "supplied guide, preserving exact pixel width and height and every other product invariant. Do not "
            "test whether relocation is feasible; do not move the product even if exact size could be preserved. "
            "This rule overrides any conflicting user relocation, centering, layout, emphasis, support-edge, or "
            "composition instruction. Independently recompose support and room around the fixed product position.",
        )
    return (
        "LOWER-FILL/MEDIUM-WIDE",
        "ACTIVE BRANCH: LOWER-FILL/MEDIUM-WIDE. Choose product x-y freely for usable composition using rigid "
        "image-plane translation only; movement is optional. Preserve exact pixel width and height and every "
        "other product invariant. Never resize, reorient, reproject, or crop the product. Independently recompose "
        "support and room beneath or around the product; product and support need not move together.",
    )


def run_row(row, client, catalog, run_dir: Path, hero: bytes, captions: dict | None = None,
            *, ref_count: int = 4, size: tuple[int, int] = (WIDTH, HEIGHT), reference_blue=None,
            camera: dict | None = None) -> dict:
    """camera: optional digital-twin camera and product footprint for this render (see geometry.build_guide)."""
    from .reference_blue import VERSION as REFERENCE_BLUE_VERSION

    if size not in ((1216, 912), (2368, 1776)):
        raise ValueError("size must be (1216, 912) or (2368, 1776).")
    canvas_width, canvas_height = size
    requested_size = f"{canvas_width}x{canvas_height}"
    policy_version = REFERENCE_BLUE_VERSION if reference_blue is not None else PIPELINE_VERSION
    if reference_blue is not None:
        captions = None
    out = run_dir / "rows" / row.id
    result_path = out / "result.json"
    input_fingerprint = hashlib.sha256(row.user_prompt.encode()).hexdigest()
    if result_path.exists():
        cached = json.loads(result_path.read_text())
        if cached.get("pipeline_version") != policy_version:
            raise ValueError("Existing row uses a different rewriting policy; choose a fresh run ID.")
        if cached.get("size") != requested_size:
            raise ValueError("Existing row uses a different size; choose a fresh run ID.")
        if cached.get("input_fingerprint") != input_fingerprint:
            raise ValueError("Existing row uses a different user input; choose a fresh run ID.")
        stored_count = cached.get("ref_count", len(cached.get("ref_ids", [])))
        if stored_count not in (0, ref_count):
            raise ValueError(f"Existing row uses {stored_count} references; choose a fresh run ID.")
        if reference_blue is not None and cached.get("reference_blue_inputs") != reference_blue.identity:
            raise ValueError("Reference catalog or histogram changed; choose a fresh run ID.")
        return cached
    out.mkdir(parents=True, exist_ok=True)
    res = {"id": row.id, "status": "error", "tone": None, "content": None, "rationale": None,
           "ref_ids": [], "layout": None, "camera": None, "composition": None, "prompt": None,
           "geometry": None, "guide_info": None,
           "error": None, "size": requested_size, "masked": False,
           "pipeline_version": policy_version, "baseline_prompt_used": False,
           "input_fingerprint": input_fingerprint,
           "captioned": bool(captions), "graded": False, "locate": None, "aligned": False, "align": None,
           "generation_mode": "direct", "image_calls": 0, "ref_count": ref_count,
           "grade_error": None, "elapsed_s": None}
    started = time.monotonic()
    if reference_blue is not None:
        res["reference_blue_inputs"] = reference_blue.identity
    selection = None
    try:
        if ref_count not in (1, 4):
            raise ValueError("ref_count must be 1 or 4.")
        if not row.user_prompt.strip():
            raise ValueError("An original user request is required; rewritten briefs are not a fallback.")
        if reference_blue is not None and ref_count != 1:
            raise ValueError("Reference-blue histogram mode requires exactly one style reference.")
        supplied_size = supplied_product_size(row.user_prompt)
        style_images = "Image 2" if ref_count == 1 else "Images 2-5"
        # Stage A sees [product, refs]; stage B and the image call see [guide, refs, product].
        product_image = f"Image {ref_count + 2}"
        hero, mask = prepare(hero, size)
        (out / "input.png").write_bytes(hero)
        (out / "mask.png").write_bytes(mask)
        observation = product_anchor(mask)
        x0, y0, x1, y1 = observation["product_bounds_px"]
        observation.update(canvas_size_px=list(size),
                           product_width_fraction=(x1 - x0) / canvas_width,
                           product_height_fraction=(y1 - y0) / canvas_height)
        if reference_blue is None:
            tones, contents = labels(catalog)
            system = load_prompt("select").format(tones=", ".join(tones), contents=", ".join(contents))
            sel = client.chat_json(system, f"Scene request: {row.user_prompt}", [], _select_schema(tones, contents))
            res.update(tone=sel["tone"], content=sel["content"], rationale=sel["rationale"])
            refs = pick_refs(catalog, sel["tone"], sel["content"], seed=row.id, k=ref_count)
        else:
            reference, selection, rationale = reference_blue.select(client, row.user_prompt, out)
            refs = [reference]
            res.update(tone=reference.tone, content=reference.content, rationale=rationale,
                       reference_selection=selection, human_policy=selection["human_policy"])
        if len(refs) != ref_count:
            raise ValueError(f"Requested {ref_count} style references; only {len(refs)} available.")
        res["ref_ids"] = [r.id for r in refs]
        for i, r in enumerate(refs, 2):
            (out / f"ref_{i}.{r.mime.split('/')[1]}").write_bytes(r.data)
        images = [("image/png", hero)] + [(r.mime, r.data) for r in refs]
        body = (" No upstream rewritten scene brief is supplied. "
                "Keep the requested room, support type, objects and lighting. The product's exact orientation/view, "
                "scale and visibility and a physically plausible initial support plan take priority over requested "
                "layout, extent and emphasis. Plan the structured support geometry around the supplied baseline product "
                "bounds and contact point. Do not pretranslate the guide or invent a new viewpoint. Stage B applies "
                "the deterministic density branch and independently recomposes a usable support beneath the permitted "
                "product position under the product-placement and recomposed-support policy. "
                "When blue is unspecified, "
                "include one large blue surface/furnishing or multiple clearly visible blue elements "
                "whose combined area makes blue immediately noticeable, not a token accent. "
                "Tiny props, thin partition frames, screen graphics, sky and lighting casts alone "
                "do not qualify. Name the blue materials, visible extent and anchored placement "
                "consistently in composition and the final prompt. Keep small props neutral by default. "
                "Keep the product's color, finish, exact orientation/view, scale, details and full visibility unchanged. "
                "Never change the product or its camera viewpoint to make room for blue. Blue does not justify a "
                "translation; any translation must independently satisfy the product-placement policy. "
                "Warm-neutral lighting "
                "can coexist with physical blue. Explicit minimal-blue, blue amount/carrier or no-blue "
                "requests override this default.\n\n"
                f"Original user request: {row.user_prompt}\n\n"
                f"Fixed source geometry on a {canvas_width}x{canvas_height} canvas: {json.dumps(observation)}.\n"
                "Furniture boxes use normalized visible bounds outside the product box. "
                "Mark user-side seating as working_seat and keep its box area <=1.5 times the product "
                "box area; crop furniture instead of "
                "shrinking the product.")
        context = "\n\n" + describe([r.data for r in refs])
        if supplied_size is not None:
            context += ("\n\nExplicit user-supplied product size (order preserved, axes not inferred by code): "
                        f"{json.dumps(supplied_size)}. Link this size, the observed pixel fractions and "
                        "visible faces to geometry and scene-object sizes.")
        if captions:
            context += (f"\n\nStyle captions for {style_images} (palette hex values are measured from pixels):\n"
                        + "\n".join(format_caption(i, captions[r.id]) for i, r in enumerate(refs, 2) if r.id in captions))
        system = load_prompt("system_3p").format(style_images=style_images, product_image="Image 1",
                                                 guide_image=product_image)
        # Stage A plans geometry only; code draws the guide and its plain-language summary.
        if camera is None:
            plan_schema = _PLAN_SCHEMA
            camera_text = " Choose coherent estimated camera dimensions for the guide."
        else:
            plan_schema = _TWIN_PLAN_SCHEMA
            res["twin_camera"] = facts = twin_camera_summary(camera, size)
            camera_text = " " + twin_camera_text(facts)
        plan_text = _PLAN_HEAD + body + camera_text + context + _GEOMETRY_ONLY
        save(out / "geometry_request.json", {"model": TEXT_MODEL, "system": system, "text": plan_text,
                                             "schema": plan_schema, "images": attachments(images),
                                             "max_retries": 0})
        plan = client.chat_json(system, plan_text, images, plan_schema)
        save(out / "geometry_response.json", plan)
        category = plan["product_category"]
        res["geometry"], res["product_category"] = plan["geometry"], category
        guide, res["guide_info"] = build_guide(hero, mask, plan["geometry"], camera)
        (out / "geometry_guide.png").write_bytes(guide)
        geometry_text = _wording(describe_geometry(plan["geometry"], res["guide_info"], size,
                                                     product_category=category), category, product_image)
        res["geometry_text"] = geometry_text
        res["guide_density_class"], density_policy = _density_policy(res["guide_info"], size)
        res["guide_density_policy"] = density_policy
        (out / "geometry_text.txt").write_text(geometry_text)
        # Stage B writes camera, composition and prompt after seeing the drawn guide.
        images = [("image/png", guide)] + images[1:] + [images[0]]
        system = load_prompt("system_3p").format(style_images=style_images, product_image=product_image,
                                                 guide_image="Image 1")
        write_text = (_wording(_PRIORITY, category, product_image) + "\n\n" + density_policy + "\n\n"
                      + geometry_text + "\n\nFixed geometry JSON: "
                      + json.dumps(plan["geometry"]) + "\n\n" + _wording(_WRITE_HEAD, category, product_image)
                      + body + context)
        override = _wording(_WRITE_OVERRIDE, category, product_image)
        if category == "printer" and plan["geometry"].get("back_edge_against_wall"):
            override += _WRITE_PRINTER_WALL
        if reference_blue is None:
            rewrite = client.chat_json(system + override, write_text, images, _WRITE_SCHEMA)
            stage_b_system = system + override
        else:
            rewrite = reference_blue.rewrite(client, system, write_text, images, _WRITE_SCHEMA,
                                             selection, row.user_prompt, out, suffix=override)
            stage_b_system = json.loads((out / "planning_request.json").read_text())["system"]
        stage_b_attempts = [_stage_b_audit(out, 1, stage_b_system, write_text, images, rewrite)]
        res["layout"], res["camera"], res["composition"] = rewrite["layout"], rewrite["camera"], rewrite["composition"]
        res["prompt"] = ("GEOMETRY \u2014 subordinate only to the product invariants.\n"
                         "Use Image 1 for the product's exact appearance, view and pixel size; the active density branch "
                         "determines whether its x-y position is fixed or may translate. Apply the product-placement and "
                         "recomposed-support policy below.\n"
                         f"{density_policy}\n\n"
                         f"{res['layout']}\n\n"
                         f"Camera: {res['camera']}\n\nComposition: {res['composition']}\n\n"
                         + _wording(_TRANSLATION_ONLY, category, product_image) + "\n\n"
                         + _wording(_LEGEND, category, product_image) +
                         "Render the lighting, palette, materials and textures described here photographically. "
                         "When blue is unspecified, "
                         "include one large blue surface/furnishing or multiple clearly visible blue elements "
                         "whose combined area makes blue immediately noticeable, not a token accent. "
                         "Tiny props, thin partition frames, screen graphics, sky and lighting casts alone "
                         "do not qualify. Keep the planned blue materials, visible extent and placement "
                         "consistent; leave small props neutral by default. "
                         "Explicit minimal-blue or no-blue requests override that default, as do explicit "
                         "blue amounts or carriers. Keep the product's original color, finish, exact orientation/view, "
                         "scale, details and full visibility. HIGH-FILL keeps exact initial x-y; only LOWER-FILL may "
                         "change x-y by rigid image-plane translation. Never change the product or its camera viewpoint to make room for blue. "
                         "Retain requested warm-neutral lighting alongside physical blue materials. "
                         "Do not impose a universal blue hue or coverage percentage. "
                         "Match soft, uniform exposure and gentle contrast; no bright-hero/dark-room treatment "
                         "and no orange or global blue color cast. "
                         "The product pixels in Image 1 control all product details, including any unlit display. "
                         "Never reproduce any diagram lines, boxes, labels, text or flat guide colors.\n\n"
                         + rewrite["prompt"] + _wording(_FINAL_CHECK, category, product_image))
        _check_image_prompt(res["prompt"])
        stage_b_attempts[0]["executable_prompt_sha256"] = _sha_text(res["prompt"])
        res["stage_b_attempts"] = stage_b_attempts
        # The image model receives only the guide and no mask; its product pixels are the real product, unprotected.
        image_inputs = images[:1]
        res["image_calls"] = 1
        if reference_blue is not None:
            # Retain the established reference-blue audit filename while also
            # recording the attempt-numbered request used by the invariant guard.
            reference_blue.record_image(out, res["prompt"], image_inputs, requested_size, None)
        save(out / "image_request_attempt_1.json", {
            "model": IMAGE_MODEL, "prompt": res["prompt"], "prompt_sha256": _sha_text(res["prompt"]),
            "images": attachments(image_inputs), "size": requested_size, "quality": "high", "n": 1,
            "mask_sha256": None, "max_retries": 0,
        })
        gpt = client.edit_image(res["prompt"], image_inputs, requested_size)
        (out / "gpt_1.png").write_bytes(gpt)
        width, height = Image.open(io.BytesIO(gpt)).size
        if (width, height) != size:
            raise ValueError(f"GPT Image returned {width}x{height}; expected {requested_size}. Raw output kept without resizing.")
        fixed_position = res["guide_density_class"] == "HIGH-FILL/CLOSE"
        first_guard = json_native(assess_product_affine(
            guide, gpt, res["guide_info"]["product_bounds_px"], fixed_position=fixed_position,
        ))
        save(out / "product_invariant_attempt_1.json", first_guard)
        guard = {"guard_version": GUARD_VERSION, "attempts": [first_guard], "selected_attempt": None}
        if first_guard["verdict"] == "pass":
            selected = gpt
            guard["selected_attempt"] = 1
        elif fixed_position:
            # Preserve the v22.3.1 HIGH-FILL behavior: append one fixed-position
            # reminder and make one bounded second image call without rewriting.
            fallback_prompt = res["prompt"] + _wording(_FIXED_POSITION_FALLBACK, category, product_image)
            _check_image_prompt(fallback_prompt)
            res["fallback_prompt"] = fallback_prompt
            save(out / "image_request_attempt_2.json", {
                "model": IMAGE_MODEL, "prompt": fallback_prompt,
                "prompt_sha256": _sha_text(fallback_prompt), "images": attachments(image_inputs),
                "size": requested_size, "quality": "high", "n": 1, "mask_sha256": None,
                "max_retries": 0, "reason": first_guard["verdict"], "stage_b_rewritten": False,
            })
            res["image_calls"] = 2
            second = client.edit_image(fallback_prompt, image_inputs, requested_size)
            (out / "gpt_2.png").write_bytes(second)
            second_width, second_height = Image.open(io.BytesIO(second)).size
            if (second_width, second_height) != size:
                raise ValueError(f"Fallback GPT Image returned {second_width}x{second_height}; expected "
                                 f"{requested_size}. Both raw attempts kept without resizing.")
            second_guard = json_native(assess_product_affine(
                guide, second, res["guide_info"]["product_bounds_px"], fixed_position=True,
            ))
            save(out / "product_invariant_attempt_2.json", second_guard)
            guard["attempts"].append(second_guard)
            if second_guard["verdict"] != "pass":
                res["product_invariant_guard"] = guard
                raise ValueError("Product invariant guard rejected both image attempts; raw attempts and metrics kept.")
            selected = second
            guard["selected_attempt"] = 2
        else:
            # LOWER-FILL attempt 1 failed the invariant guard. Run exactly one
            # new fixed-position Stage-B writing call. Its executable prompt is
            # rebuilt from fixed-only instructions rather than appending an
            # override to the translation-permitting first prompt.
            fixed_body = (" No upstream rewritten scene brief is supplied. Keep the requested room, support type, "
                          "objects and lighting wherever compatible with the fixed product position and invariants. "
                          "Recompose a physically plausible support and room around the product's exact initial frame "
                          "position. Ignore any request to reposition or center the product. When blue is unspecified, "
                          "include one large blue surface or furnishing, or multiple clearly visible blue elements whose "
                          "combined area is immediately noticeable. Tiny props, thin partition frames, screen graphics, "
                          "sky and lighting casts alone do not qualify. Name blue materials and their anchored placement "
                          "consistently. Keep small props neutral by default. Keep the product's color, finish, exact "
                          "position, orientation/view, scale, details and full visibility unchanged. Warm-neutral lighting "
                          "can coexist with physical blue. Explicit minimal-blue, blue amount/carrier or no-blue requests "
                          "override this default.\n\nOriginal user request: " + row.user_prompt + "\n\n"
                          f"Fixed source geometry on a {canvas_width}x{canvas_height} canvas: "
                          f"{json.dumps(observation)}.\nFurniture boxes use normalized visible bounds outside the "
                          "product box. Mark user-side seating as working_seat and keep its box area <=1.5 times the "
                          "product box area; crop furniture instead of shrinking the product.")
            fixed_write_text = (_wording(_FIXED_REWRITE_PRIORITY, category, product_image)
                                + "\n\nInitial geometry JSON for support reconstruction: "
                                + json.dumps(plan["geometry"]) + "\n\n"
                                + _wording(_WRITE_HEAD, category, product_image) + fixed_body + context)
            fixed_system = load_prompt("system_3p_fixed_position").format(
                style_images=style_images, product_image=product_image, guide_image="Image 1",
            ) + _wording(_FIXED_REWRITE_OVERRIDE, category, product_image)
            fixed_prompt_suffix = ""
            if selection is not None:
                human_system, fixed_prompt_suffix = _human_policy(selection)
                fixed_system += "\n\n" + human_system
            if category == "printer" and plan["geometry"].get("back_edge_against_wall"):
                fixed_system += _WRITE_PRINTER_WALL
            fixed_raw_rewrite = client.chat_json(fixed_system, fixed_write_text, images, _WRITE_SCHEMA)
            save(out / "stage_b_attempt_2_raw_response.json", fixed_raw_rewrite)
            meta_commentary_removed = any(_FIXED_META_SENTENCE.search(value)
                                          for value in fixed_raw_rewrite.values())
            fixed_rewrite = {key: _strip_fixed_meta_commentary(value)
                             for key, value in fixed_raw_rewrite.items()}
            if fixed_prompt_suffix:
                fixed_rewrite = {**fixed_rewrite,
                                 "prompt": fixed_rewrite["prompt"] + "\n\n" + fixed_prompt_suffix}
            second_stage_b = _stage_b_audit(out, 2, fixed_system, fixed_write_text, images, fixed_rewrite)
            second_stage_b["raw_response_sha256"] = _sha_json(fixed_raw_rewrite)
            second_stage_b["meta_commentary_removed"] = meta_commentary_removed
            fallback_prompt = ("GEOMETRY — fixed product position and invariant appearance.\n"
                               + _wording(_FIXED_EXECUTABLE_POLICY, category, product_image) + "\n\n"
                               + fixed_rewrite["layout"] + "\n\nCamera: " + fixed_rewrite["camera"]
                               + "\n\nComposition: " + fixed_rewrite["composition"] + "\n\n"
                               + _wording(_FIXED_LEGEND, category, product_image)
                               + "Render the requested lighting, palette, materials and textures photographically. "
                               "Keep the product's original color and finish. Match soft, uniform exposure and gentle "
                               "contrast. Never reproduce diagram lines, boxes, labels, text or flat guide colors.\n\n"
                               + fixed_rewrite["prompt"] + _wording(_FIXED_FINAL_CHECK, category, product_image))
            stage_b_attempts.append(second_stage_b)
            res["stage_b_attempts"] = stage_b_attempts
            res["product_invariant_guard"] = guard
            _check_image_prompt(fallback_prompt)
            _validate_fixed_executable_prompt(fallback_prompt)
            second_stage_b["executable_prompt_sha256"] = _sha_text(fallback_prompt)
            res["fallback_prompt"] = fallback_prompt
            res["fallback_layout"] = fixed_rewrite["layout"]
            res["fallback_camera"] = fixed_rewrite["camera"]
            res["fallback_composition"] = fixed_rewrite["composition"]
            save(out / "image_request_attempt_2.json", {
                "model": IMAGE_MODEL, "prompt": fallback_prompt,
                "prompt_sha256": _sha_text(fallback_prompt), "images": attachments(image_inputs),
                "size": requested_size, "quality": "high", "n": 1, "mask_sha256": None,
                "max_retries": 0, "reason": first_guard["verdict"], "stage_b_rewritten": True,
            })
            res["image_calls"] = 2
            second = client.edit_image(fallback_prompt, image_inputs, requested_size)
            (out / "gpt_2.png").write_bytes(second)
            second_width, second_height = Image.open(io.BytesIO(second)).size
            if (second_width, second_height) != size:
                raise ValueError(f"Fallback GPT Image returned {second_width}x{second_height}; expected "
                                 f"{requested_size}. Both raw attempts kept without resizing.")
            second_guard = json_native(assess_product_affine(
                guide, second, res["guide_info"]["product_bounds_px"], fixed_position=True,
            ))
            save(out / "product_invariant_attempt_2.json", second_guard)
            guard["attempts"].append(second_guard)
            if second_guard["verdict"] != "pass":
                res["product_invariant_guard"] = guard
                raise ValueError("Product invariant guard rejected both image attempts; raw attempts and metrics kept.")
            selected = second
            guard["selected_attempt"] = 2
        res["product_invariant_guard"] = guard
        (out / "ours.png").write_bytes(selected)
        res["status"] = "ok"
    except Exception as e:  # recorded; only the bounded invariant fallback may make a second image call
        res["error"] = f"{type(e).__name__}: {e}"[:500]
    res["elapsed_s"] = round(time.monotonic() - started, 1)
    res = json_native(res)
    result_path.write_text(json.dumps(res, indent=1))
    return res


def grade_row(out: Path, *, catalog: list[StyleRef] | None = None,
              reference_stats: dict | None = None) -> dict:
    """Grade raw output separately, optionally choosing a target across the full catalog."""
    result_path = out / "result.json"
    res = json.loads(result_path.read_text())
    graded_path = out / "ours_graded.png"
    if catalog is None and reference_stats is None and res.get("graded") and graded_path.exists():
        return res
    try:
        if res["status"] != "ok":
            raise ValueError("Cannot grade an unsuccessful generation.")
        raw = (out / "ours.png").read_bytes()
        selection = None
        if catalog is not None or reference_stats is not None:
            if catalog is None or reference_stats is None:
                raise ValueError("Nearest-reference grading requires both catalog and statistics.")
            reference, selection = nearest_reference(raw, catalog, reference_stats)
            reference_path = out / f"grade_reference.{reference.mime.split('/')[-1]}"
            reference_path.write_bytes(reference.data)
        else:
            if len(res["ref_ids"]) != 1:
                raise ValueError("Whole-image grading requires exactly one style reference.")
            refs = list(out.glob("ref_2.*"))
            if len(refs) != 1:
                raise ValueError("Expected exactly one saved reference file for Image 2.")
            reference_path = refs[0]
        graded, metadata = match_reference(raw, reference_path.read_bytes())
        if selection is not None:
            metadata["selection"] = selection
        graded_path.write_bytes(graded)
        res.update(graded=True, grading={**metadata, "reference_file": reference_path.name}, grade_error=None)
    except (OSError, ValueError) as error:
        res.update(graded=False, grade_error=f"{type(error).__name__}: {error}"[:500])
    result_path.write_text(json.dumps(res, indent=1, default=float))
    return res
