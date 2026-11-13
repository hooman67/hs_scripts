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
from .mask import prepare
from .openai_client import TEXT_MODEL, load_prompt
from .reference_blue import attachments

WIDTH, HEIGHT = 1216, 912
SIZE = f"{WIDTH}x{HEIGHT}"
PIPELINE_VERSION = "unified-blue-scale-v20-surface-shape-r1"


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
_GEOMETRY_ONLY = ("""

THIS CALL PLANS GEOMETRY ONLY. Return only geometry and product_category. Camera text, composition, the image prompt, materials and scale notes are written in a later call after the geometry guide is drawn.

SUPPORT PLAUSIBILITY: The support must be real furniture that people actually use to hold this product in this kind of room, standing where such furniture normally stands. The requested support type names the furniture; it does not fix its size. Keep that category and its body: a cabinet, credenza or fitted counter does not become a table because its top is rectangular. For a printer with no specified support category, choose a credible substantial cabinet, low credenza, fitted counter or dedicated equipment table. A requested printer table is a substantial dedicated equipment table, not a person's occupied workstation desk; allow standing access and unobstructed operation. Choose support_width_m, support_depth_m and support_height_m typical for that furniture and for using this product: the top is only as deep as such furniture normally is while still holding the product's whole base, and the height suits how people reach and use the product. Set back_edge_against_wall true when that furniture would normally stand against a wall in this room; the wall then stands at the support's rear boundary, never through its top.""" + _PRINTER_WALL + """ The wall can never stand between camera and product. Round or oval laptop tables are often freestanding; set back_edge_against_wall false unless the original request or normal placement of the requested furniture calls for wall adjacency. Secondary furniture in furniture_boxes stands beside, behind or in front of the support, never inside it.

SUPPORT SHAPE: Set support_top_shape to rectangular, round or oval, retaining the requested top shape. When shape is unspecified, retain the existing rectangular default. Printer cabinets, credenzas, fitted counters and equipment tables normally have rectangular tops. The shape field describes only the top outline, not the furniture category. Rectangular retains the existing construction and gap/offset meanings. For round, support_width_m and support_depth_m are equal physical diameters; for oval, they are unequal physical diameters. The guide must project the ellipse in the same support plane and camera. All four unchanged product-base corners must lie inside the ellipse. Choose physically normal dimensions and modest gap and lateral offset; leave full footprint-width and curved-rim clearance. For round and oval tops, user_edge_gap_m is measured along the selected user-side axis (width for width_left/width_right, depth for near_camera/far_from_camera) to the user-facing rim point aligned with the product center, not to an invented straight side. Keep the product footprint, original pixel bounds, orientation, position and size fixed. Do not widen the camera or require a complete perimeter or visible furniture base: the fixed crop may show only an arc.""")

_WRITE_HEAD = ("Write camera, composition and editing text from Image 1 (the fixed geometry guide containing the "
               "real product), Image 3 (the same product on white), the FIXED GEOMETRY below and the original "
               "user request.")
_PRIORITY = """STAGE B. Geometry is already fixed and drawn in Image 1 around the real product, at the exact Image 3 framing. Do not change it.

PRIORITY ORDER (strict):
1. The product (its real pixels in Image 1; Image 3 shows the same product on white for detail): its pixel position, size, orientation and visibility. Never move, resize, rotate, crop or occlude it.
2. The FIXED GEOMETRY (Image 1 and the text below): support top shape and orientation, the user-facing edge or curved rim and its position in the frame, the product-to-boundary distance, how far the top extends to each side, frame crop and camera.
3. The original user request. It chooses the room, support category and body, material, props, lighting, palette and mood. Its requested top shape is resolved in Stage A; do not redraw the fixed outline in Stage B.

When the user request asks for a different layout, extent, emphasis, framing, focal point, product size, or a table that fills or dominates the foreground, drop that part and follow 1 and 2. Your camera, composition and prompt must describe exactly the geometry of Image 1: the same support top shape and orientation, the user-facing boundary identified by user_side on the gray support area, top surface only on the drawn support, nothing beyond its user-facing boundary, props on the drawn top at plausible scale beside the product, and nothing occluding the product. Describe straight edges and visible corners only for rectangular tops; describe curved rims and visible arcs for round or oval tops. Both round and oval physical tops project as ellipses, so use support_top_shape to name the physical shape and Image 1 to describe its projection. A cropped arc is sufficient; do not demand the full perimeter or furniture base or change the camera to reveal them. Keep the original support category beneath the fixed top: a rectangular cabinet, credenza or fitted-counter top is not an instruction to replace its body with a table. Keep the user side and operating access.

WRITE IN PLAIN VISUAL WORDS. The image model follows pictures and plain descriptions, not measurements. Use the numbers below only to choose your words. In layout, camera, composition and prompt, describe sizes, distances, angles and positions the way a photographer briefs a set builder: by comparison with the product, the frame edges and nearby objects (for example "the tabletop continues about two laptop widths to the left of the laptop and a little less to the right", "the tabletop is about three times as deep as the laptop", "the table ends inside the frame on both sides", "the curved rim exits the frame on the left", "camera at standing eye height, looking gently down").

FIXED GEOMETRY (derived by code from Image 1):
"""

_WRITE_OVERRIDE = """

STAGE B OVERRIDE: geometry is a fixed input in this call, not an output. Image 1 is the drawn geometry guide and is visible to you now. Follow the PRIORITY ORDER in the user message: product first, fixed geometry second, user request third. Return layout, camera, composition and prompt, each written in plain visual words. layout opens the image prompt as its GEOMETRY section: short lines on the support's physical top shape, how its axes are turned and how its straight edges or curved rim run across the frame; which boundary faces the user and where it sits relative to the product; how close the product sits to that boundary, using the rim point aligned with the product center for a round or oval top; how much top surface continues on each side of the product and how deep the support is compared with the product; which ends and corners stay inside the frame for a rectangular top, or which arcs are visible or cropped for a round or oval top; the camera height and how steeply it looks down; and the product unchanged in its place. Do not invent straight sides or four corners for a curved top, or require its full perimeter or furniture base to be visible. Keep the support category and body from the original request, not from the shape field: a cabinet, credenza or fitted counter remains that furniture beneath its drawn top. Preserve user-side access, including standing operating access for printers.

IMAGE MODEL INPUT: the image model receives ONLY Image 1 and your text. It never sees the style reference or the product on white. In layout, camera, composition and prompt, never mention any image other than Image 1, the reference, or where a style or material came from. Describe the lighting, palette, materials and textures you take from the style reference directly in words, as a brief for a photographer who has never seen it. Never explain where a color, material or blue carrier was adapted or transferred from. Product detail comes from the real product pixels in Image 1."""

_WRITE_PRINTER_WALL = ("\n\nPRINTER AGAINST THE WALL: the printer's back stands right against the wall at the "
                       "support's back edge, with no gap, shelf or objects between them. State this plainly in the "
                       "prompt.")
_LEGEND = """Image 1 is the canvas to edit: a geometry-only diagram at the final framing whose product pixels are the real product. Keep those product pixels unchanged. The flat gray area with a thin darker outline is the exact top surface of the support: the top covers exactly that area, with its boundary where the gray area's boundary is; the gray is not its color. Rectangular tops have straight edges; round and oval tops have projected elliptical rims, which the frame may crop to visible arcs. Use the fixed support_top_shape to distinguish a physically round top from an oval one, not its apparent projected proportions. Do not replace curved boundaries with straight sides or four corners, or widen the view to reveal the full outline or furniture base. The outline specifies the top, not the furniture category: retain the cabinet, credenza, fitted counter, equipment table or other support body described in the original request. Replace everything else in Image 1, including the white background and the gray fill, with the photographic scene. Never render any diagram mark. """

_FINAL_CHECK = """

Final check before rendering: the product pixels, footprint, position, size and orientation are unchanged; the support top shape and orientation, user-facing edge or curved rim, product-to-boundary distance and top extent match the GEOMETRY section and Image 1. For round or oval tops, describe the actual visible arcs rather than straight sides or four corners, and measure the user-edge gap at the rim point aligned with the product center. Do not change the camera or crop to show the full perimeter or furniture base. The support category and body still match the original request; a rectangular top has not turned a cabinet, credenza or fitted counter into a table. Keep user-side and operating access, standing access for printers, shared perspective, and no extra people or devices. Where other scene text conflicts, follow GEOMETRY, with unchanged product pixels always first."""

_STALE_IMAGE = re.compile(r"\bImages?\s+(?:[2-9]|1\d)\b|\breference(?:'s|\u2019s)|\b(?:style|selected) references?\b"
                          r"|\breference (?:image|photo|photograph|picture)\b|\bthe reference\b"
                          r"(?! (?:books?|photographs|binders?|boards?)\b)", re.I)


def _check_image_prompt(prompt: str) -> None:
    """The image call sees only Image 1, so its prompt must not point at the style reference or product render."""
    match = _STALE_IMAGE.search(prompt)
    if match:
        context = prompt[max(0, match.start() - 60):match.end() + 40]
        raise ValueError(f"Image prompt mentions an image the image model does not receive: {context!r}")


def _wording(text: str, category: str, product_image: str) -> str:
    """Adapt laptop/table wording to the planned product category and the product render's image number."""
    text = text.replace("Image 3", product_image)
    if category == "laptop":
        return text
    for pattern, value in ((r"\blaptop\b", "product" if category == "other" else category),
                           (r"\btabletop\b", "support top"), (r"\bTable\b", "Support"), (r"\btable\b", "support")):
        text = re.sub(pattern, value, text)
    return text


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
                "Keep the requested room, support type, objects and lighting. The fixed product and "
                "planned support geometry take priority over requested layout, extent and emphasis; "
                "adapt those to the geometry. When blue is unspecified, "
                "include one large blue surface/furnishing or multiple clearly visible blue elements "
                "whose combined area makes blue immediately noticeable, not a token accent. "
                "Tiny props, thin partition frames, screen graphics, sky and lighting casts alone "
                "do not qualify. Name the blue materials, visible extent and anchored placement "
                "consistently in composition and the final prompt. Keep small props neutral by default. "
                "Keep the product's color, finish, orientation, position, scale and visibility unchanged; "
                "never change the product or camera to make room for blue. Warm-neutral lighting "
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
        (out / "geometry_text.txt").write_text(geometry_text)
        # Stage B writes camera, composition and prompt after seeing the drawn guide.
        images = [("image/png", guide)] + images[1:] + [images[0]]
        system = load_prompt("system_3p").format(style_images=style_images, product_image=product_image,
                                                 guide_image="Image 1")
        write_text = (_wording(_PRIORITY, category, product_image) + geometry_text + "\n\nFixed geometry JSON: "
                      + json.dumps(plan["geometry"]) + "\n\n" + _wording(_WRITE_HEAD, category, product_image)
                      + body + context)
        override = _wording(_WRITE_OVERRIDE, category, product_image)
        if category == "printer" and plan["geometry"].get("back_edge_against_wall"):
            override += _WRITE_PRINTER_WALL
        if reference_blue is None:
            rewrite = client.chat_json(system + override, write_text, images, _WRITE_SCHEMA)
        else:
            rewrite = reference_blue.rewrite(client, system, write_text, images, _WRITE_SCHEMA,
                                             selection, row.user_prompt, out, suffix=override)
        res["layout"], res["camera"], res["composition"] = rewrite["layout"], rewrite["camera"], rewrite["composition"]
        res["prompt"] = (f"GEOMETRY \u2014 highest priority. Follow Image 1 exactly.\n{res['layout']}\n\n"
                         f"Camera: {res['camera']}\n\nComposition: {res['composition']}\n\n"
                         + _wording(_LEGEND, category, product_image) +
                         "Render the lighting, palette, materials and textures described here photographically. "
                         "When blue is unspecified, "
                         "include one large blue surface/furnishing or multiple clearly visible blue elements "
                         "whose combined area makes blue immediately noticeable, not a token accent. "
                         "Tiny props, thin partition frames, screen graphics, sky and lighting casts alone "
                         "do not qualify. Keep the planned blue materials, visible extent and placement "
                         "consistent; leave small props neutral by default. "
                         "Explicit minimal-blue or no-blue requests override that default, as do explicit "
                         "blue amounts or carriers. Keep the product's original color, finish, orientation, "
                         "position, scale and visibility; never change the product or camera to make room "
                         "for blue. Retain requested warm-neutral lighting alongside physical blue materials. "
                         "Do not impose a universal blue hue or coverage percentage. "
                         "Match soft, uniform exposure and gentle contrast; no bright-hero/dark-room treatment "
                         "and no orange or global blue color cast. "
                         "The product pixels in Image 1 control all product details, including any unlit display. "
                         "Never reproduce any diagram lines, boxes, labels, text or flat guide colors.\n\n"
                         + rewrite["prompt"] + _wording(_FINAL_CHECK, category, product_image))
        _check_image_prompt(res["prompt"])
        # The image model receives only the guide and no mask; its product pixels are the real product, unprotected.
        image_inputs = images[:1]
        res["image_calls"] = 1
        if reference_blue is not None:
            reference_blue.record_image(out, res["prompt"], image_inputs, requested_size, None)
        gpt = client.edit_image(res["prompt"], image_inputs, requested_size)
        (out / "gpt_1.png").write_bytes(gpt)
        width, height = Image.open(io.BytesIO(gpt)).size
        if (width, height) != size:
            raise ValueError(f"GPT Image returned {width}x{height}; expected {requested_size}. Raw output kept without resizing.")
        (out / "ours.png").write_bytes(gpt)
        res["status"] = "ok"
    except Exception as e:  # recorded, never retried automatically
        res["error"] = f"{type(e).__name__}: {e}"[:500]
    res["elapsed_s"] = round(time.monotonic() - started, 1)
    result_path.write_text(json.dumps(res, indent=1, default=float))
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
