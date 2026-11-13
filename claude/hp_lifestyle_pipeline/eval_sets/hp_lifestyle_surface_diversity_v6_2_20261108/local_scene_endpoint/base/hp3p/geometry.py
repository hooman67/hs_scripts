"""Estimated-camera layout diagrams; never applied to generated pixels."""
import io
import math
import re
from typing import Literal, TypedDict

import numpy as np
from PIL import Image, ImageDraw


class FurnitureBox(TypedDict):
    kind: Literal["working_seat", "background_furniture"]
    label: str
    box: list[float]


class Geometry(TypedDict):
    camera_height_m: float
    support_height_m: float
    look_at_height_m: float
    horizontal_distance_m: float
    vertical_fov_deg: float
    axis_angle_deg: float
    support_width_m: float
    support_depth_m: float
    product_footprint_width_m: float
    product_footprint_depth_m: float
    user_side: Literal["near_camera", "far_from_camera", "width_left", "width_right"]
    user_edge_gap_m: float
    support_lateral_offset_m: float
    back_edge_against_wall: bool
    furniture_boxes: list[FurnitureBox]


_FIELDS = {
    "camera_height_m": "Estimated camera height above floor, greater than support height.",
    "support_height_m": "Estimated support top height above floor, positive metres.",
    "look_at_height_m": "Estimated look-at height, between support and camera heights.",
    "horizontal_distance_m": "Positive horizontal camera-to-look-at distance in metres.",
    "vertical_fov_deg": "Estimated vertical field of view, 10 to 100 degrees.",
    "axis_angle_deg": "World-vertical support yaw relative to camera floor-forward, strictly "
                      "between -75 and 75 degrees. Positive: width axis right end farther away; "
                      "negative: right end nearer. Zero: frontal horizontal width edge. "
                      "On-screen depth direction also depends on off-center product placement; "
                      "do not infer left/right depth from yaw sign alone. Use chassis/screen, not oval base; "
                      "for a printer, its bottom edges at the base corner nearest the camera.",
    "support_width_m": "Positive physical support length along the width axis.",
    "support_depth_m": "Positive physical support length along the depth axis.",
    "product_footprint_width_m": "Positive product base length along the support width axis.",
    "product_footprint_depth_m": "Positive product base length along the support depth axis.",
    "user_edge_gap_m": "Non-negative distance from the product base to the user-facing support edge.",
    "support_lateral_offset_m": "Signed shift of the support center from the product base center along "
                                "the user-facing edge: positive toward the width axis right end, or "
                                "farther from the camera when user_side is width_left/width_right.",
}
_USER_SIDES = ("near_camera", "far_from_camera", "width_left", "width_right")
GEOMETRY_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": [*_FIELDS, "user_side", "back_edge_against_wall", "furniture_boxes"],
    "properties": {**{k: {"type": "number", "description": v} for k, v in _FIELDS.items()},
                   "user_side": {"type": "string", "enum": list(_USER_SIDES),
                                 "description": "Support edge the product's user front faces: near_camera "
                                 "(-depth), far_from_camera (+depth), width_left (-width) or width_right (+width)."},
                   "back_edge_against_wall": {
                       "type": "boolean",
                       "description": "True when this support furniture would normally stand with the edge opposite "
                       "the user-facing edge against a wall in this room. The wall can never stand between camera "
                       "and product."},
                   "furniture_boxes": {
                       "type": "array", "description": "Visible bounds of critical secondary furniture, "
                       "not the primary support or props. No overlap with fixed product bounds. "
                       "Working-seat box area at most 1.5 times product box area. Each item stands beside, "
                       "behind or in front of the primary support, never inside its footprint or on its top.",
                       "items": {"type": "object", "additionalProperties": False,
                                 "required": ["kind", "label", "box"],
                                 "properties": {"kind": {"type": "string",
                                                        "enum": ["working_seat", "background_furniture"]},
                                                "label": {"type": "string"},
                                                "box": {"type": "array", "items": {"type": "number"},
                                                        "description": "[left, top, right, bottom], "
                                                        "normalized 0-1 visible image coordinates."}}}}},
}

# With a digital-twin camera these come from the twin, so Astra A does not estimate them.
TWIN_FIELDS = ("camera_height_m", "look_at_height_m", "horizontal_distance_m", "vertical_fov_deg",
               "axis_angle_deg", "product_footprint_width_m", "product_footprint_depth_m")
TWIN_GEOMETRY_SCHEMA = {**GEOMETRY_SCHEMA,
                        "required": [k for k in GEOMETRY_SCHEMA["required"] if k not in TWIN_FIELDS],
                        "properties": {k: v for k, v in GEOMETRY_SCHEMA["properties"].items()
                                       if k not in TWIN_FIELDS}}

_NUMBER_UNIT = r'([+-]?\d+(?:\.\d+)?)\s*((?:mm|cm|m|inches|inch|in)\b|["\u2033])?'
_DIMENSIONS = re.compile(
    r"(?<![\w.+-])" + _NUMBER_UNIT + r"\s*[x\u00d7*]\s*" + _NUMBER_UNIT
    + r"\s*[x\u00d7*]\s*" + _NUMBER_UNIT + r"(?!\w)",
    re.IGNORECASE,
)
_SIZE_LABEL = re.compile(
    r"\b(?:product|device|printer|laptop|monitor)\s+(?:physical\s+)?"
    r"(?:dimensions|size)\s*[:=]\s*", re.IGNORECASE,
)
_UNIT_METRES = {"mm": 0.001, "cm": 0.01, "m": 1, "in": 0.0254,
                "inch": 0.0254, "inches": 0.0254, '"': 0.0254, "\u2033": 0.0254}


def dimension_values(text: str) -> list[float]:
    matches = list(_DIMENSIONS.finditer(text))
    if len(matches) != 1:
        raise ValueError("Product dimensions need one three-length expression with explicit units.")
    groups = matches[0].groups()
    units = [unit.lower() if unit else None for unit in groups[1::2]]
    factors = {_UNIT_METRES[unit] for unit in units if unit}
    if not factors or (None in units and len(factors) != 1):
        raise ValueError("Product dimension units are missing or ambiguous.")
    shared = next(iter(factors))
    values = [float(f"{float(value) * (_UNIT_METRES[unit] if unit else shared):.12g}")
              for value, unit in zip(groups[::2], units)]
    if any(not math.isfinite(value) or value <= 0 for value in values):
        raise ValueError("Product dimensions must be finite positive lengths.")
    return values


def supplied_product_size(text: str) -> dict | None:
    """Recognize explicitly labelled sizes; other phrasing is interpreted by the same rewriter."""
    matches = list(_SIZE_LABEL.finditer(text))
    if len(matches) > 1:
        raise ValueError("Multiple product-size declarations require one unambiguous specification.")
    if not matches:
        return None
    dimensions = _DIMENSIONS.match(text, matches[0].end())
    if dimensions is None:
        raise ValueError("Labelled product size needs three lengths with explicit units.")
    quote = text[matches[0].start():dimensions.end()].strip()
    return {"source_quote": quote, "dimensions_m_in_supplied_order": dimension_values(quote)}


def product_anchor(mask: bytes) -> dict:
    alpha = Image.open(io.BytesIO(mask)).getchannel("A")
    bounds = alpha.getbbox()
    if bounds is None:
        raise ValueError("Product mask is empty; cannot anchor geometry.")
    x0, _, x1, y1 = bounds
    foot = alpha.crop((x0, y1 - 1, x1, y1)).getbbox()
    if foot is None:
        raise ValueError("Product mask has no contact row.")
    return {"product_bounds_px": list(bounds),
            "contact_px": [x0 + (foot[0] + foot[2]) / 2, y1 - 0.5]}


def fit_source_camera(edges: list[dict], size: tuple[int, int]) -> dict:
    """Fit source edge directions under the guide's zero-roll, centered-pinhole assumption."""
    w, h = size
    if w <= 0 or h <= 0 or any(e["axis"] not in ("width", "depth") for e in edges):
        raise ValueError("Invalid source camera dimensions or edge axes.")
    if any(sum(e["axis"] == axis for e in edges) < 2 for axis in ("width", "depth")):
        raise ValueError("Source camera fitting needs two edges per physical axis.")
    segments = np.asarray([[e["start_px"], e["end_px"]] for e in edges], dtype=float)
    if (segments.shape != (len(edges), 2, 2) or not np.isfinite(segments).all()
            or (segments < 0).any() or (segments > np.array([w, h])).any()):
        raise ValueError("Source edge coordinates must be finite and inside the image.")
    directions = segments[:, 1] - segments[:, 0]
    if (np.linalg.norm(directions, axis=1) < 20).any():
        raise ValueError("Source edges are too short to constrain a camera.")
    midpoints = segments.mean(axis=1)
    depth = np.array([e["axis"] == "depth" for e in edges])[None, :]

    def errors(parameters):
        pitch, fov, yaw = np.deg2rad(parameters).T
        focal = h / (2 * np.tan(fov / 2))
        sy, cy = np.sin(yaw)[:, None], np.cos(yaw)[:, None]
        sp, cp = np.sin(pitch)[:, None], np.cos(pitch)[:, None]
        dx = np.where(depth, -sy, cy)
        dy = -sp * np.where(depth, cy, sy)
        dz = cp * np.where(depth, cy, sy)
        # Homogeneous vanishing directions remain defined for vanishing points at infinity.
        px = focal[:, None] * dx + (w / 2 - midpoints[:, 0]) * dz
        py = focal[:, None] * dy + (h / 2 - midpoints[:, 1]) * dz
        cross = px * directions[:, 1] - py * directions[:, 0]
        dot = px * directions[:, 0] + py * directions[:, 1]
        angles = np.rad2deg(np.arctan2(np.abs(cross), np.abs(dot)))
        return np.where(np.hypot(px, py) < 1e-8, np.inf, angles)

    limits = ((5, 89), (10, 98), (-74, 74))
    best = None
    for radius, step in ((None, 2), (2, 0.2), (0.2, 0.05)):
        ranges = [np.arange(low, high + step / 2, step) if best is None else
                  np.clip(np.arange(center - radius, center + radius + step / 2, step), low, high)
                  for (low, high), center in zip(limits, best if best is not None else (0, 0, 0))]
        candidates = np.stack(np.meshgrid(*ranges, indexing="ij"), axis=-1).reshape(-1, 3)
        residuals = errors(candidates)
        index = int(np.argmin(np.mean(residuals ** 2, axis=1)))
        best, edge_errors = candidates[index], residuals[index]
    if float(edge_errors.max()) > 3:
        raise ValueError("Source edges cannot be explained within 3 degrees by the guide camera model.")
    return {
        "camera_pitch_deg": float(best[0]), "vertical_fov_deg": float(best[1]),
        "axis_angle_deg": float(best[2]),
        "rms_edge_error_deg": float(np.sqrt(np.mean(edge_errors ** 2))),
        "max_edge_error_deg": float(edge_errors.max()), "edge_errors_deg": edge_errors.tolist(),
        "at_search_boundary": any(min(abs(value - low), abs(value - high)) < 0.1
                                  for value, (low, high) in zip(best, limits)),
        "limitations": "Approximate source-edge direction fit, not calibrated camera recovery. "
                       "Assumes zero roll, square pixels, canvas-centered principal point, and "
                       "correctly annotated orthogonal chassis axes. Cutout reframing and taper "
                       "can violate these assumptions; does not establish physical heights or distances.",
    }


def _clip_near(points: list[np.ndarray]) -> list[np.ndarray]:
    clipped = []
    for a, b in zip(points, points[1:] + points[:1]):
        if a[2] >= 0.05:
            clipped.append(a)
        if (a[2] >= 0.05) != (b[2] >= 0.05):
            clipped.append(a + (b - a) * ((0.05 - a[2]) / (b[2] - a[2])))
    return clipped


SURFACE_FILL, SURFACE_OUTLINE = (200, 200, 200), (110, 110, 110)


def _unit(v) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v)


def _twin_frame(camera: dict, support_height: float, size: tuple[int, int]) -> dict:
    """Express a digital-twin camera (Z-up metres, horizontal aperture fit) in the guide's
    right/up/forward world, with the product's support top at support_height."""
    w, _ = size
    position = np.asarray(camera["position_m"], dtype=float)
    footprint = np.asarray(camera["footprint_corners_m"], dtype=float)
    top = float(footprint[:, 2].mean())
    look = -_unit(camera["back"])
    forward = _unit([look[0], look[1], 0])
    right = np.cross(forward, [0, 0, 1])
    frame = np.array([right, [0, 0, 1], forward])
    origin = np.array([position[0], position[1], top - support_height])
    rotation = np.array([frame @ _unit(camera["right"]), -(frame @ _unit(camera["up"])), frame @ look])
    corners = [frame @ (p - origin) for p in footprint]
    edges = [corners[1] - corners[0], corners[3] - corners[0]]
    # Depth is the footprint axis closest to the camera's floor-forward direction.
    depth_index = int(abs(_unit(edges[1])[2]) > abs(_unit(edges[0])[2]))
    depth, width = edges[depth_index], edges[1 - depth_index]
    return {"camera": frame @ (position - origin), "rotation": rotation, "frame": frame,
            "focal": w * camera["focal_length"] / camera["horizontal_aperture"],
            "base_center": np.mean(corners, axis=0),
            "width_axis": _unit(width) * (1 if width[0] >= 0 else -1),
            "depth_axis": _unit(depth) * (1 if depth[2] >= 0 else -1),
            "base_w": float(np.linalg.norm(width)), "base_d": float(np.linalg.norm(depth))}


def twin_camera_summary(camera: dict, size: tuple[int, int]) -> dict:
    """All digital-twin camera facts for the planner. Heights are relative to the support top.
    camera also needs front_xy (product front, world XY unit vector) and product_height_m."""
    w, h = size
    t = _twin_frame(camera, 0.0, size)
    rotation, position, center, focal = t["rotation"], t["camera"], t["base_center"], t["focal"]
    forward = rotation[2]

    def pixel(point):
        x, y, z = rotation @ (point - position)
        return [float(w / 2 + focal * x / z), float(h / 2 + focal * y / z)]

    corners = np.asarray(camera["footprint_corners_m"], dtype=float)
    top, mid = float(corners[:, 2].mean()), corners[:, :2].mean(axis=0)

    def guide_point(xy, z):  # world -> guide frame (origin on the floor under the camera, support top at 0)
        return t["frame"] @ np.array([xy[0] - camera["position_m"][0], xy[1] - camera["position_m"][1], z - top])

    # Azimuth and faces in world XY (right-handed); the guide frame is left-handed.
    front = _unit(camera["front_xy"])
    user_right = np.array([-front[1], front[0]])  # right hand of a user facing the product front
    to_camera = np.asarray(camera["position_m"][:2], dtype=float) - mid
    half_front = float(np.abs((corners[:, :2] - mid) @ front).max())
    half_right = float(np.abs((corners[:, :2] - mid) @ user_right).max())
    base_px = pixel(center)
    faces = []
    for name, normal, half in [("front", front, half_front), ("back", -front, half_front),
                               ("user's right side", user_right, half_right),
                               ("user's left side", -user_right, half_right)]:
        if float((to_camera - normal * half) @ normal) > 0:
            u = pixel(guide_point(mid + normal * half, top + camera["product_height_m"] / 2))[0]
            faces.append({"face": name, "image_side": "right" if u > base_px[0] else "left"})
    front_guide = guide_point(mid + front, top) - guide_point(mid, top)
    user_side = max([("near_camera", -t["depth_axis"]), ("far_from_camera", t["depth_axis"]),
                     ("width_left", -t["width_axis"]), ("width_right", t["width_axis"])],
                    key=lambda item: float(item[1] @ front_guide))[0]
    offset = center - position
    return {"camera_above_support_top_m": float(position[1]),
            "camera_horizontal_distance_m": float(math.hypot(offset[0], offset[2])),
            "camera_distance_to_product_center_m": float(np.linalg.norm(
                offset + [0, camera["product_height_m"] / 2, 0])),
            "camera_azimuth_from_product_front_deg": math.degrees(math.atan2(to_camera @ user_right,
                                                                             to_camera @ front)),
            "camera_pitch_down_deg": math.degrees(math.atan2(-forward[1], math.hypot(forward[0], forward[2]))),
            "camera_roll_deg": math.degrees(math.asin(float(np.clip(rotation[0][1], -1, 1)))),
            "camera_aim_offset_deg": math.degrees(math.atan2(offset[0], offset[2])),
            "product_base_center_px": base_px,
            "lens_35mm_equivalent_mm": math.hypot(36, 24) * focal / math.hypot(w, h),
            "horizontal_fov_deg": math.degrees(2 * math.atan(w / 2 / focal)),
            "vertical_fov_deg": math.degrees(2 * math.atan(h / 2 / focal)),
            "base_edge_yaw_deg": math.degrees(math.atan2(t["width_axis"][2], t["width_axis"][0])),
            "product_footprint_width_m": t["base_w"], "product_footprint_depth_m": t["base_d"],
            "product_height_m": float(camera["product_height_m"]),
            "product_front_faces_user_side": user_side, "visible_faces": faces}


def twin_camera_text(facts: dict) -> str:
    """Plain-language digital-twin camera facts for the geometry planner."""
    az, yaw, aim = (facts[k] for k in ("camera_azimuth_from_product_front_deg", "base_edge_yaw_deg",
                                       "camera_aim_offset_deg"))
    faces = ", ".join(f"{f['face']} (image {f['image_side']})" for f in facts["visible_faces"])
    u, v = facts["product_base_center_px"]
    return (
        "Digital-twin camera (ground truth that rendered this product image; code draws the guide with it): "
        f"camera {facts['camera_above_support_top_m']:.2f} m above the support top, "
        f"{facts['camera_horizontal_distance_m']:.2f} m horizontally from the product base center "
        f"({facts['camera_distance_to_product_center_m']:.2f} m to the product center); "
        f"{abs(az):.0f} degrees around from straight in front of the product toward the user's "
        f"{'right' if az >= 0 else 'left'} (0 = straight in front, 180 = straight behind); "
        f"pitched {facts['camera_pitch_down_deg']:.1f} degrees down, roll {facts['camera_roll_deg']:.1f} degrees; "
        f"the product base center lies {abs(aim):.1f} degrees {'right' if aim >= 0 else 'left'} of the camera's "
        f"forward direction and projects to pixel ({u:.0f}, {v:.0f}); lens about "
        f"{facts['lens_35mm_equivalent_mm']:.0f} mm "
        f"full-frame equivalent, horizontal FOV {facts['horizontal_fov_deg']:.1f} degrees, vertical FOV "
        f"{facts['vertical_fov_deg']:.1f} degrees. Product base {facts['product_footprint_width_m']:.2f} m along "
        f"the support width axis by {facts['product_footprint_depth_m']:.2f} m along its depth axis, "
        f"{facts['product_height_m']:.2f} m tall; base width edges turned {abs(yaw):.1f} degrees from frontal, "
        f"right end {'farther' if yaw >= 0 else 'nearer'}. The product front faces the {facts['product_front_faces_user_side']} "
        f"support edge. Visible product faces: {faces}. Code places the support top under the product base "
        "with its edges parallel to the base; choose only the support and layout.")


def build_guide(hero: bytes, mask: bytes, geometry: Geometry, camera: dict | None = None) -> tuple[bytes, dict]:
    """Draw the support guide. camera is an optional digital-twin camera plus product footprint;
    when given, it replaces Astra's estimated camera, yaw and footprint."""
    product = Image.open(io.BytesIO(hero)).convert("RGB")
    alpha = Image.open(io.BytesIO(mask)).getchannel("A")
    if product.size != alpha.size:
        raise ValueError("Product and mask dimensions differ.")
    for name in _FIELDS:
        if camera is not None and name in TWIN_FIELDS:
            continue
        value = geometry[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"{name} must be finite.")
        if name == "user_edge_gap_m" and value < 0:
            raise ValueError(f"{name} must be non-negative.")
        if name.endswith("_m") and name not in ("user_edge_gap_m", "support_lateral_offset_m") and value <= 0:
            raise ValueError(f"{name} must be positive.")
    if geometry["user_side"] not in _USER_SIDES:
        raise ValueError(f"user_side must be one of {', '.join(_USER_SIDES)}.")
    w, h = product.size
    info = product_anchor(mask)
    x0, y0, x1, y1 = info["product_bounds_px"]
    sh = geometry["support_height_m"]
    if camera is None:
        ch, target = geometry["camera_height_m"], geometry["look_at_height_m"]
        if not sh <= target <= ch or ch <= sh:
            raise ValueError("camera_height_m must exceed support_height_m; look-at must lie between them.")
        if not 10 <= geometry["vertical_fov_deg"] <= 100:
            raise ValueError("vertical_fov_deg must be between 10 and 100.")
        if not -75 < geometry["axis_angle_deg"] < 75:
            raise ValueError("axis_angle_deg must be between -75 and 75.")
        u, v = info["contact_px"]
        pitch = math.atan2(ch - target, geometry["horizontal_distance_m"])
        yaw = math.radians(geometry["axis_angle_deg"])
        focal = h / (2 * math.tan(math.radians(geometry["vertical_fov_deg"]) / 2))
    else:
        twin = _twin_frame(camera, sh, product.size)
        focal, rotation, camera_position = twin["focal"], twin["rotation"], twin["camera"]
        ch = float(camera_position[1])
        if ch <= sh:
            raise ValueError("Digital-twin camera lies below the support top.")
        pitch = math.atan2(-rotation[2][1], math.hypot(rotation[2][0], rotation[2][2]))
        width_axis, depth_axis = twin["width_axis"], twin["depth_axis"]
        yaw = math.atan2(width_axis[2], width_axis[0])
        base_w, base_d, base_center = twin["base_w"], twin["base_d"], twin["base_center"]
        center = base_center
    equivalent_mm = math.hypot(36, 24) * focal / math.hypot(w, h)
    family = ("ultra-wide" if equivalent_mm < 24 else "wide" if equivalent_mm < 35 else
              "normal" if equivalent_mm <= 60 else "short-telephoto" if equivalent_mm <= 135 else "telephoto")
    info.update(lens_35mm_equivalent_mm=equivalent_mm, lens_family=family,
                lens_estimate_basis="Diagonal-FOV equivalent to 36x24mm full frame, assuming a rectilinear "
                                    "camera and the chosen canvas aspect. Construction estimate, not recovered EXIF."
                if camera is None else "Digital-twin camera focal length and horizontal aperture.",
                camera_source="estimated" if camera is None else "digital_twin")
    if camera is None:
        # World is right/up/forward. Camera image axes are right/down/forward.
        rotation = np.array([[1, 0, 0], [0, -math.cos(pitch), -math.sin(pitch)],
                             [0, -math.sin(pitch), math.cos(pitch)]])
        ray = rotation.T @ np.array([(u - w / 2) / focal, (v - h / 2) / focal, 1])
        if ray[1] >= -1e-6:
            raise ValueError("Estimated camera places product contact at/above the support horizon.")
        camera_position = np.array([0, ch, 0])
        center = camera_position + ray * ((sh - ch) / ray[1])
        width_axis = np.array([math.cos(yaw), 0, math.sin(yaw)])
        depth_axis = np.array([-math.sin(yaw), 0, math.cos(yaw)])
        # The lowest mask point is the base point nearest the camera: a near corner, or the near
        # edge midpoint for a frontal base. Place the support around that base, not the contact.
        base_w, base_d = geometry["product_footprint_width_m"], geometry["product_footprint_depth_m"]
        near_end = 0.0 if yaw == 0 else -math.copysign(1, yaw)
        base_center = center - near_end * base_w / 2 * width_axis + base_d / 2 * depth_axis
    center_depth = float((rotation @ (center - camera_position))[2])
    if center_depth < 0.05:
        raise ValueError("Product contact lies behind the estimated camera near plane.")
    info.update(axis_angle_deg=math.degrees(yaw), camera_height_m=ch,
                product_footprint_width_m=base_w, product_footprint_depth_m=base_d)
    side = geometry["user_side"]
    if side in ("near_camera", "far_from_camera"):
        user_axis, lateral_axis = depth_axis, width_axis
        base_half, base_lateral, support_half, support_lateral = (
            base_d / 2, base_w / 2, geometry["support_depth_m"] / 2, geometry["support_width_m"] / 2)
    else:
        user_axis, lateral_axis = width_axis, depth_axis
        base_half, base_lateral, support_half, support_lateral = (
            base_w / 2, base_d / 2, geometry["support_width_m"] / 2, geometry["support_depth_m"] / 2)
    user_sign = -1 if side in ("near_camera", "width_left") else 1
    gap, lateral = geometry["user_edge_gap_m"], geometry["support_lateral_offset_m"]
    if 2 * support_half < 2 * base_half + gap - 1e-9:
        raise ValueError("Support must contain the product base plus user_edge_gap_m along the user axis.")
    if abs(lateral) + base_lateral > support_lateral + 1e-9:
        raise ValueError("Support must contain the product base after support_lateral_offset_m.")
    support_center = (base_center + user_sign * (base_half + gap - support_half) * user_axis
                      + lateral * lateral_axis)
    user_edge = [support_center + user_sign * support_half * user_axis + sign * support_lateral * lateral_axis
                 for sign in (-1, 1)]

    def project(points: list[np.ndarray]) -> list[tuple[float, float]]:
        return [(float(w / 2 + focal * p[0] / p[2]), float(h / 2 + focal * p[1] / p[2])) for p in points]

    corners = [rotation @ (support_center + sx * geometry["support_width_m"] / 2 * width_axis
                          + sz * geometry["support_depth_m"] / 2 * depth_axis - camera_position)
               for sx, sz in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
    polygon = project(_clip_near(corners))
    if len(polygon) < 3:
        raise ValueError("Support plane is behind the estimated camera.")
    edge = [rotation @ (point - camera_position) for point in user_edge]
    if min(edge[0][2], edge[1][2]) < 0.05 <= max(edge[0][2], edge[1][2]):
        a, b = edge
        cut = a + (b - a) * ((0.05 - a[2]) / (b[2] - a[2]))
        edge = [a, cut] if a[2] >= 0.05 else [cut, b]
    user_edge_px = project(edge) if min(edge[0][2], edge[1][2]) >= 0.05 else None
    guide = Image.new("RGB", product.size, "white")
    draw = ImageDraw.Draw(guide)
    wall_px = None
    if geometry.get("back_edge_against_wall"):
        toward_user = user_sign * user_axis
        back = support_center - support_half * toward_user
        if float(np.dot(camera_position - back, toward_user)) <= 0:
            raise ValueError("Wall at the support's back edge would stand between camera and product.")
        up = np.array([0, 1, 0])
        span = support_lateral + 2.0
        wall = [rotation @ (back + s * span * lateral_axis + (y - sh) * up - camera_position)
                for s, y in [(-1, sh), (1, sh), (1, sh + 1.5), (-1, sh + 1.5)]]
        wall_px = project(_clip_near(wall))
    # The guide shows only the support surface and the product; wall, edge, axes and furniture stay in text.
    draw.polygon(polygon, fill=SURFACE_FILL, outline=SURFACE_OUTLINE, width=2)
    for name, direction in [("width_axis_px", width_axis), ("depth_axis_px", depth_axis)]:
        length = min(0.2, center_depth / 4)
        points = project([rotation @ (center + sign * length * direction - camera_position) for sign in (-1, 1)])
        info[name] = [list(point) for point in points]

    for furniture in geometry["furniture_boxes"]:
        if furniture["kind"] not in ("working_seat", "background_furniture"):
            raise ValueError("Furniture kind must identify working_seat or background_furniture.")
        box = furniture["box"]
        if len(box) != 4 or any(isinstance(n, bool) or not isinstance(n, (int, float))
                               or not math.isfinite(n) or not 0 <= n <= 1 for n in box):
            raise ValueError("Furniture box needs four finite normalized coordinates.")
        left, top, right, bottom = box[0] * w, box[1] * h, box[2] * w, box[3] * h
        if right <= left or bottom <= top:
            raise ValueError("Furniture box has no positive area.")
        if left < x1 and right > x0 and top < y1 and bottom > y0:
            raise ValueError("Furniture box overlaps fixed product bounds.")
        if furniture["kind"] == "working_seat" and (right - left) * (bottom - top) > 1.5 * (x1 - x0) * (y1 - y0):
            raise ValueError("Working seat box dominates fixed product; move it deeper or crop furniture.")

    horizon = h / 2 - focal * math.tan(pitch)
    # The guide is the masked edit canvas: its protected region must be the exact product pixels.
    guide.paste(product, (0, 0), alpha)
    info.update(camera_pitch_deg=math.degrees(pitch), horizon_y_px=horizon,
                wall_polygon_px=None if wall_px is None else [list(point) for point in wall_px],
                support_polygon_px=[list(point) for point in polygon],
                user_edge_px=None if user_edge_px is None else [list(point) for point in user_edge_px])
    buf = io.BytesIO()
    guide.save(buf, "PNG")
    return buf.getvalue(), info


def describe_geometry(geometry: Geometry, info: dict, size: tuple[int, int], guide_image: str = "Image 1",
                      product_category: str = "laptop", product_image: str = "Image 3") -> str:
    """Plain-language guide summary for the prompt writer and image prompt (laptop/table wording)."""
    g, (w, h) = geometry, size
    side = g["user_side"]
    along_width = side in ("near_camera", "far_from_camera")
    pw, pd = info["product_footprint_width_m"], info["product_footprint_depth_m"]
    lateral_axis = info["width_axis_px"] if along_width else info["depth_axis_px"]
    half = (g["support_width_m"] / 2 - pw / 2) if along_width else (g["support_depth_m"] / 2 - pd / 2)
    plus, minus = half + g["support_lateral_offset_m"], half - g["support_lateral_offset_m"]
    right_m, left_m = (plus, minus) if lateral_axis[1][0] > lateral_axis[0][0] else (minus, plus)
    wa, da, ue = info["width_axis_px"], info["depth_axis_px"], info["user_edge_px"]
    tilt = math.degrees(math.atan2(wa[1][1] - wa[0][1], wa[1][0] - wa[0][0]))
    if wa[1][0] < wa[0][0]:
        tilt = math.degrees(math.atan2(wa[0][1] - wa[1][1], wa[0][0] - wa[1][0]))
    recede = "upper right" if da[1][0] > da[0][0] else "upper left"
    x0, y0, x1, y1 = info["product_bounds_px"]

    def pct(p):
        return f"{p[0] / w * 100:.0f}% across, {p[1] / h * 100:.0f}% down"

    edge_name = {"near_camera": "the table edge nearest the camera, in front of the laptop",
                 "far_from_camera": "the far table edge, behind the laptop as seen from the camera",
                 "width_left": "the table's short edge on the image-left side",
                 "width_right": "the table's short edge on the image-right side"}[side]
    lines = [f"GEOMETRY \u2014 highest priority. Follow {guide_image} exactly.",
             f"- Table orientation: the table is turned about {abs(info['axis_angle_deg']):.0f} degrees to the camera. "
             f"Its long edges run left to right, {'descending' if tilt > 0 else 'rising'} about {abs(tilt):.0f} degrees "
             f"toward image right; its short edges recede toward the {recede}. "
             + ("The laptop faces the user-facing edge." if product_category == "laptop" else
                "The laptop's front and sides are parallel to the table edges.")]
    if ue:
        where = f"In the image it runs from {pct(ue[0])} to {pct(ue[1])}"
        if side == "near_camera":
            where += (f", about {(max(ue[0][1], ue[1][1]) - y1) / h * 100:.0f}% of image height below the "
                      "laptop's lowest point")
        lines.append(f"- User-facing edge: {edge_name}. {where}. No tabletop beyond this edge.")
    else:
        lines.append(f"- User-facing edge: {edge_name}; it lies outside the frame.")
    corners_out = sum(not (0 <= px <= w and 0 <= py <= h) for px, py in info["support_polygon_px"])
    lines += [f"- Product on the table: the laptop is {g['user_edge_gap_m'] * 100:.1f} cm "
              f"(about {g['user_edge_gap_m'] / (pd if along_width else pw):.1f} laptop "
              f"{'depths' if along_width else 'widths'}) from the user-facing edge. The tabletop extends "
              f"{left_m:.2f} m (about {left_m / pw:.1f} laptop widths) toward image left of the laptop and "
              f"{right_m:.2f} m (about {right_m / pw:.1f} laptop widths) toward image right.",
              f"- Table size: {g['support_width_m']:.2f} m x {g['support_depth_m']:.2f} m, about "
              f"{g['support_width_m'] / pw:.1f} laptop widths by {g['support_depth_m'] / pd:.1f} laptop depths.",
              f"- Frame crop: {corners_out} of {len(info['support_polygon_px'])} table corners fall outside the "
              "frame; keep them cropped and never shrink the product to show them.",
              f"- Product: exactly as in {guide_image} (details: {product_image}), occupying "
              f"{x0 / w * 100:.0f}-{x1 / w * 100:.0f}% across and "
              f"{y0 / h * 100:.0f}-{y1 / h * 100:.0f}% down. Same size; never enlarge or move it.",
              f"- Camera: {info['camera_height_m']:.2f} m high, looking down {info['camera_pitch_deg']:.1f} degrees, "
              f"about {info['lens_35mm_equivalent_mm']:.0f} mm lens."]
    return "\n".join(lines)
