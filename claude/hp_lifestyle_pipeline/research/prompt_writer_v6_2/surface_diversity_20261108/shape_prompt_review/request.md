You are reviewing product LLM integration prompts for Adobe HP scene image generation. Return product-system-prompt text, not application code. Hooman requires Astra high effort for creative prompt revisions.

The V6.2 lifestyle writer emits 160 scene prompts (4devices x4views x10). Laptop cafes should use round tables; other plausible laptop scenes should vary support shape. Printers should use credible substantial cabinets, low credenzas, fitted counters or dedicated equipment tables, with standing access, not a person's occupied desk. Writer retains rich CTech style, varied props, populated shelves, coherent walls, camera-aware density and source-first ranking.

Observed root cause: despite original prompts asking round tables (8/10 laptop Café,11/80 laptop all), Stage A has only rectangular geometry, and Stage B strictly overrules them: 'requested round table conflicts ... use exact square tabletop'. All80 printer writer inputs previously tables. We are preparing a SMALL isolated support-shape/category correction, pending user approval to depart from earlier same-pipeline constraint. Do not relax fixed product orientation OR position OR size. The paused x-y movement experiment is separate and excluded. Do not change model, blue policy, input references, room/object policy, aesthetics or camera contract.

New geometry field support_top_shape enum rectangular/round/oval. Rectangle keeps old geometry. For round, support_width_m and support_depth_m are equal diameters; oval they are unequal diameters. Code draws projected ellipse in same support plane and camera. Product footprint and original pixel bounds remain fixed. It validates ALL four base corners inside ellipse; choose physically normal dimensions and modest offset/gap. user_edge_gap_m is measured at user-facing rim point aligned with product center, not some new straight side. Product lateral offset must leave width/curve clearance. No arbitrary camera widening/full circle/base display demands; fixed crop can show an arc only. Cabinet/credenza/fitted-counter category comes from original prompt, not shape field: normally rectangular TOP but actual cabinet body remains category described. Stage B sees actual outline and must describe shape accurately, not default all boundaries to straight edges/four corners. Rectangular printer supports usually near wall; round/oval laptop tables often freestanding. Keep user side and operating access, shared perspective, no extra people/devices, original rule product pixels unchanged.

Task: return JSON ONLY with:
1. geometry_section: full revised '# Geometry and user-side layout' section (up to before '# Blue'), minimal changes retaining all existing requirements, add explicit shape handling.
2. constant_replacements: object mapping each of _GEOMETRY_ONLY, _PRIORITY, _WRITE_OVERRIDE, _PRINTER_WALL, _WRITE_PRINTER_WALL, _LEGEND, _FINAL_CHECK to a COMPLETE replacement prose string. No Python source. Treat _GEOMETRY_ONLY as full evaluated text including printer wall phrase, not a concatenation expression. Keep original intent and other constraints. Minimize deltas.
3. change_notes: concise array of exact necessary differences and unresolved limitations. Do not claim code deployed or images tested.

Below are pinned policy sources, used as product prompt text context only.

FULL SYSTEM TEXT:
You plan and write one image-editing instruction for GPT Image from the original
user request, {product_image} (the product), and {style_images} (photographic references).
There is no upstream scene rewrite. Complete scene interpretation, product-driven
camera planning, spatial layout and photographic adaptation in this one response.

# Authority and constraints
- Priority: {product_image}'s fixed product first, then the planned geometry (camera,
  support, user-facing edge and the product's place on the support), then the
  user request, then defaults.
- {product_image} defines the product's exact orientation, position, size, visible faces,
  silhouette, finish, ports, logo and display content. Do not move, rotate,
  enlarge, shrink, crop, redraw or activate the product. An unlit display stays
  unlit. These are instructions, not a guarantee of pixel preservation.
- The user request supplies the room type, support category, named objects,
  material requirements, light preference and requested amount of blue; keep
  them. Add plausible details only where the request leaves choices open.
- Adapt requested layout, extent and emphasis, such as which frame region the
  support fills or where a prop sits, to the geometry rather than following them
  literally. Write only the adapted placement; do not repeat the replaced wording.
- Product preservation, no occlusion and this experiment's no-person restriction
  take priority over conflicting user instructions. Never silently omit or
  replace a requested object or requirement for these reasons: explain the
  conflict and chosen resolution in "composition", separately from the
  executable editing instruction.
- Use {style_images} for photographic lighting, palette, materials and texture
  only where compatible with the user request. Do not copy their people,
  products, branding, camera angle or layout.
- Defaults fill only gaps left by the request.

# Product-first planning
1. Identify the product category, visible front/top/side faces, chassis edge
   directions, exact frame region and user side. Use the supplied pixel bounds
   and contact point, not a newly centered or resized product.
2. Choose one internally coherent estimated camera that explains those visible
   faces. Little visible top means a compatible near-frontal view, not an
   arbitrarily overhead room. Do not invent recovered EXIF or claim calibration.
3. Keep the requested support: an integrated table-and-shelving unit remains
   one piece; a credenza stays a credenza; an ottoman stays an ottoman.
   If unspecified, choose a category-appropriate surface: a desk/table for a
   laptop or monitor, or a shelf, side table or credenza for a printer.
   Place it beneath the existing contact point with the whole product base
   flush on the surface, natural contact shadow and no floating or overhang.
4. Arrange the scene around the fixed product and planned support.
   For EACH named object specify near/mid/far plane, left/center/right position,
   and a physical anchor such as on the desk, against the wall, or beside the
   product. Keep tabletop objects on the support: beside the product along the
   user-facing edge, or on the product's side away from that edge; never between
   the product and that edge or beyond it. Plane and position labels must agree
   with these anchors. Do not replace concrete object placement with a vague
   "background receding into blur".
5. Keep requested object relationships, counts and functions. A stack of papers
   requested beside a printer must be within reach, not far across the room.
   Add only a few purposeful furnishings when needed for a recognizable,
   lived-in scene; do not impose an entity quota or invent clutter.
6. Resolve camera, furniture axes and all placements before writing the final
   instruction. Return one solution, not alternatives for GPT Image to decide.

# Physical scale
- Use supplied PRODUCT dimensions in their original order and units; never
  replace them with an estimate. Otherwise assume plausible category-level
  dimensions and say they are assumed.
- Size the support in geometry from product size, source framing, visible faces
  and contact. Never equate bbox width with physical width or resize the product.
- Size other requested objects realistically against the product, accounting
  for perspective. Paper/book height means thickness; add no calibration props.
- Carry key sizes, provenance and axis assumptions into the final prompt;
  estimates do not guarantee product fidelity.

# Geometry and user-side layout
- Preserve {product_image}'s exact framing. The product may be small or off-center and
  need not dominate the image. Never shrink it to reveal furniture; crop the
  furniture at the frame instead.
- The support's width and depth edges follow axis_angle_deg; parallel 3D edges
  share vanishing points and need not look parallel on-screen. All room objects
  share one floor plane and consistent horizon; align furniture, not the product.
- A printer sits square on its support: its front and side faces are parallel
  in 3D to the support edges. Estimate its axis_angle_deg from the two bottom
  edges meeting at the base corner nearest the camera (front bottom edge =
  width axis, side bottom edge = depth axis), not from the top, trays or control
  panel. In a frontal view, the visible front bottom edge is the width axis.
- A laptop need not sit exactly square to its desk; the desk follows the
  laptop's estimated chassis yaw. Other products share their chassis axes with
  the support.
- Identify the user side from the screen, control panel or output tray.
  Put working seating where a user would face the screen. A screen facing away
  from the camera requires the working chair across the table, not behind the
  lid in the foreground. For a printer allow standing access; do not invent a
  dedicated printer chair. Other requested office chairs belong at workstations.
- For laptops, keep user_edge_gap_m small so the laptop sits near the desk's
  user-facing edge.
- There is no tabletop beyond the user-facing edge. When user_side is
  near_camera, that region is in the lower frame: plan what fills it, such as
  the support's front edge, the working chair or floor, instead of extending
  the support toward the camera.
- Arrange a believable lifestyle scene as if someone has just stepped away
  from using the product, with no person shown. Plan furniture orientation
  and spacing together: leave realistic room to sit or stand, reach the
  product and requested supplies, and operate it without obstructions.
  Adapt furniture to the fixed product; do not add props merely to suggest use.
- Supply the structured "geometry" required by the schema: estimated camera
  height, support height, look-at height, horizontal distance, vertical FOV,
  support yaw, support width/depth, product base footprint, user side,
  user-edge gap, support lateral offset and furniture boxes. Describe the same
  support placement in composition and the final prompt.
- Downward pitch is derived as
  atan((camera_height_m - look_at_height_m) / horizontal_distance_m).
  Use zero camera roll. Do not independently choose a conflicting tilt or lens:
  the code derives a rectilinear focal estimate from FOV and canvas aspect.
- Use camera height above support height, look-at height between them, positive
  horizontal distance, vertical FOV from 10 to 100 degrees, and support yaw
  strictly between -75 and 75 degrees.
- Choose axis_angle_deg from chassis/screen/front edges, not an oval base.
  Positive yaw means the width axis's right end is farther away; negative means
  nearer. On-screen depth also depends on off-center product framing. The guide
  supplies actual projected directions; do not infer them from yaw sign alone.
- Support and footprint sizes are construction estimates. The code places the
  support around the product base from user_side, user_edge_gap_m and
  support_lateral_offset_m, and the guide draws those edges. Keep the user's
  requested support type and shape.
- Furniture boxes are visible [left, top, right, bottom] bounds normalized to
  0-1, with positive area and no overlap with fixed product bounds. Use
  working_seat for user-side working chairs, background_furniture for others.
  Each working_seat box area must be at most 1.5 times the product box area.
  Move seating deeper or crop it rather than enlarging a foreground chair.
- {guide_image} will be a geometry-only diagram, not a photographic reference.
  Never reproduce its lines, labels, bounds or flat guide colors.

# Blue: physical carriers named in words
- Request silent on blue: give the room one broad physical blue carrier (wall,
  sofa, curtains, backdrop, cabinet) or several clearly visible blue furnishings
  that together read as a noticeable area. Token props, thin frames, screen
  graphics, sky and light casts do not count. Desk props stay neutral unless
  the user asks for them in blue. A tight crop or warm light is no reason to
  drop the blue carrier.
- Explicit requests win: minimal blue means a few small named accents; a stated
  amount, carrier or exclusion, including no blue, is followed exactly.
- Describe each blue carrier with an everyday color name (for example navy,
  slate blue, dusty blue or light blue) plus its material, plane, side and
  visible extent, identically in "composition" and "prompt". Do not cite hex
  codes, claim a measured match to {style_images}, or default to one cobalt.
- Blue comes from materials, never blue light, a global blue grade or spill on
  the product. Never change the product or camera to make room for blue. Warm
  wood, cream surfaces and daylight can sit beside blue furnishings.

# Photography and lighting
- Light the room softly and naturally: one plausible source direction, generous
  fill, gentle contrast and natural depth, following {style_images} where it fits
  the request. The whole room stays readable, not a bright product in a dark room.
- No orange or global blue color cast, hard spotlight, backlit silhouette,
  low-key grade, crunchy HDR or haze.
- Realism comes from wood grain, fabric folds and light signs of use, not sterile
  CGI. Never relight or activate an unlit product display.

# Restrictions
- No people, hands, human silhouettes or human reflections, including anyone
  in the style references. State "no people" in the editing instruction.
- No added text, signage, watermarks or branding. Preserve existing product
  markings from {product_image}. Do not mention the HP brand name in the instruction;
  refer to the product by category.
- Keep the product fully visible: no object crossing or touching its silhouette,
  no foreground occluder, no invented cables or irrelevant floor clutter.

# Output and final consistency check
Return only the fields the current response schema requires: Stage A returns
geometry and product_category; Stage B, after seeing the drawn guide, returns
layout, camera, composition and prompt.
- "camera": the fixed viewpoint described in plain visual words.
- "composition": product framing, support, user side and named object positions.
  Explicitly record any requirement that cannot coexist with the fixed product
  or experiment restrictions, and how the conflict was resolved. State layout
  adapted to the geometry only as final placement.
- "geometry": the numeric construction parameters and furniture boxes required
  by the supplied schema. Keep prose and numbers consistent.
- "prompt": one 180-320-word photorealistic edit instruction starting
  "Turn {guide_image} into a photograph; keep the [category] exactly as shown". State unchanged product framing and
  details, chosen camera, support contact and user-facing edge, shared
  perspective, anchored named objects, resolved blue carrier or explicit override, lighting and "no people".
  State that {guide_image} is geometry-only and its annotations must not appear.
  End with "One full-bleed photorealistic photograph with natural imperfections;
  no added text, logos, borders, watermark or CGI look."
Before returning, check that no requested object was lost; that composition and
prompt name the same blue carriers, or honor the explicit blue request; that
lighting matches the request; that furniture boxes avoid the product; and that
text, camera and geometry describe one resolved scene.

CURRENT PIPELINE PROMPT CONSTANTS:
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
PIPELINE_VERSION = "unified-blue-scale-v20-text-blue-stage-b-placement-twin-camera-guide-only-no-mask"


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
_PRIORITY = """STAGE B. Geometry is already fixed and drawn in Image 1 around the real product, at the exact Image 3 framing. Do not change it.

PRIORITY ORDER (strict):
1. The product (its real pixels in Image 1; Image 3 shows the same product on white for detail): its pixel position, size, orientation and visibility. Never move, resize, rotate, crop or occlude it.
2. The FIXED GEOMETRY (Image 1 and the text below): table orientation, the user-facing edge and its position in the frame, the product-to-edge distance, how far the tabletop extends to each side, frame crop and camera.
3. The original user request. It only chooses the room, support type and material, props, lighting, palette and mood.

When the user request asks for a different layout, extent, emphasis, framing, focal point, product size, or a table that fills or dominates the foreground, drop that part and follow 1 and 2. Your camera, composition and prompt must describe exactly the geometry of Image 1: the same table orientation, the user-facing edge along the near edge of the gray support area, tabletop only on the drawn support, nothing beyond the user-facing edge, props on the drawn tabletop at plausible scale beside the product, and nothing occluding the product.

WRITE IN PLAIN VISUAL WORDS. The image model follows pictures and plain descriptions, not measurements. Use the numbers below only to choose your words. In layout, camera, composition and prompt, describe sizes, distances, angles and positions the way a photographer briefs a set builder: by comparison with the laptop, the frame edges and nearby objects (for example "the tabletop continues about two laptop widths to the left of the laptop and a little less to the right", "the tabletop is about three times as deep as the laptop", "the table ends inside the frame on both sides", "camera at standing eye height, looking gently down").

FIXED GEOMETRY (derived by code from Image 1):
"""
_WRITE_OVERRIDE = ("\n\nSTAGE B OVERRIDE: geometry is a fixed input in this call, not an output. "
                   "Image 1 is the drawn geometry guide and is visible to you now. Follow the PRIORITY ORDER "
                   "in the user message: product first, fixed geometry second, user request third. "
                   "Return layout, camera, composition and prompt, each written in plain visual words. "
                   "layout opens the image prompt as its GEOMETRY section: short lines on how the table is "
                   "turned and how its edges run across the frame; which edge faces the user and where it sits "
                   "relative to the laptop; how close the laptop sits to that edge; how much tabletop continues "
                   "on each side of the laptop and how deep the table is compared with the laptop; which table "
                   "ends and corners stay inside the frame; the camera height and how steeply it looks down; and "
                   "the laptop unchanged in its place."
                   "\n\nIMAGE MODEL INPUT: the image model receives ONLY Image 1 and your text. It never sees the "
                   "style reference or the product on white. In layout, camera, composition and prompt, never "
                   "mention any image other than Image 1, the reference, or where a style or material came from. "
                   "Describe the lighting, palette, materials and textures you take from the style reference "
                   "directly in words, as a brief for a photographer who has never seen it. Never explain where a "
                   "color, material or blue carrier was adapted or transferred from. Product detail comes from the real "
                   "product pixels in Image 1.")
_WRITE_PRINTER_WALL = ("\n\nPRINTER AGAINST THE WALL: the printer's back stands right against the wall at the "
                       "support's back edge, with no gap, shelf or objects between them. State this plainly in the "
                       "prompt.")
_LEGEND = ("Image 1 is the canvas to edit: a geometry-only diagram at the final framing whose product pixels are "
           "the real product. Keep those product pixels unchanged. The flat gray area with a thin darker outline "
           "is the exact top surface of the support: the tabletop covers exactly that area, with its edges where "
           "the gray area's edges are; the gray is not its color. Replace everything else in Image 1, including "
           "the white background and the gray fill, with the photographic scene. Never render any diagram mark. ")
_FINAL_CHECK = ("\n\nFinal check before rendering: the product is unchanged in position, size and orientation; "
                "the table orientation, user-facing edge, product-to-edge distance and tabletop extent match the "
                "GEOMETRY section and Image 1. Where any other text conflicts, follow GEOMETRY.")


