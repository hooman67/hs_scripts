import io
import math

import numpy as np
import pytest
from PIL import Image


def scene(bottom=180):
    hero = Image.new("RGB", (400, 300), "white")
    hero.paste((30, 30, 30), (220, 100, 300, bottom))
    mask = Image.new("RGBA", hero.size, (255, 255, 255, 0))
    mask.paste((255, 255, 255, 255), (220, 100, 300, bottom))
    data = []
    for image in (hero, mask):
        buf = io.BytesIO()
        image.save(buf, "PNG")
        data.append(buf.getvalue())
    return data


def spec(**changes):
    return {
        "camera_height_m": 1.5, "support_height_m": 0.75, "look_at_height_m": 1.0,
        "horizontal_distance_m": 1.0, "vertical_fov_deg": 50, "axis_angle_deg": 20,
        "support_width_m": 1.2, "support_depth_m": 0.7, "product_footprint_width_m": 0.3,
        "product_footprint_depth_m": 0.2, "user_side": "near_camera", "user_edge_gap_m": 0.05,
        "support_lateral_offset_m": 0.0, "furniture_boxes": [], **changes,
    }

@pytest.mark.parametrize("text,expected", [
    ('15.7" x 15.7" x 13.4"', [0.39878, 0.39878, 0.34036]),
    ("40 x 40 x 34 cm", [0.4, 0.4, 0.34]),
    ("400 mm x 40 cm x 0.34 m", [0.4, 0.4, 0.34]),
])
def test_product_dimensions_normalize_units_without_assigning_axes(text, expected):
    from hp3p.geometry import dimension_values

    assert dimension_values(text) == pytest.approx(expected)


@pytest.mark.parametrize("text", ["0 x 40 x 34 cm", "-40 x 40 x 34 cm",
                                 "40 x 40 x 34", "400 mm x 40 x 0.34 m",
                                 "40 x 40 x 34 cm or 30 x 30 x 20 cm"])
def test_product_dimensions_reject_invalid_or_ambiguous_measurements(text):
    from hp3p.geometry import dimension_values

    with pytest.raises(ValueError):
        dimension_values(text)


def test_product_size_is_not_inferred_from_furniture_or_product_category():
    from hp3p.geometry import supplied_product_size

    assert supplied_product_size("A printer on a desk 120 x 70 x 75 cm.") is None
    assert supplied_product_size("A typical office printer.") is None
    size = supplied_product_size("Office.\nActual product dimensions: 40 x 40 x 34 cm.")
    assert size["dimensions_m_in_supplied_order"] == pytest.approx([0.4, 0.4, 0.34])


@pytest.mark.parametrize("angle,width_rises,depth_left", [(20, True, True), (-20, False, False)])
def test_guide_projects_shared_axes_at_fixed_product_contact(angle, width_rises, depth_left):
    from hp3p.geometry import build_guide

    hero, mask = scene()
    guide, info = build_guide(hero, mask, spec(axis_angle_deg=angle))
    image = Image.open(io.BytesIO(guide))
    assert image.size == (400, 300) and image.getpixel((260, 140)) == (30, 30, 30)
    assert info["product_bounds_px"] == [220, 100, 300, 180]
    assert info["contact_px"] == [260, 179.5]
    assert info["camera_pitch_deg"] == pytest.approx(26.565051)
    a, b = info["width_axis_px"]
    assert b[0] > a[0] and bool(b[1] < a[1]) == width_rises
    a, b = info["depth_axis_px"]
    assert b[1] < a[1] and bool(b[0] < a[0]) == depth_left
    assert np.asarray(Image.open(io.BytesIO(hero)))[140, 260].tolist() == [30, 30, 30]
    protected = np.asarray(Image.open(io.BytesIO(mask)))[..., 3] == 255
    assert (np.asarray(image.convert("RGB"))[protected] == np.asarray(Image.open(io.BytesIO(hero)))[protected]).all()


def test_rectangle_default_and_explicit_shape_are_byte_compatible():
    from hp3p.geometry import build_guide

    implicit_guide, implicit_info = build_guide(*scene(), spec())
    explicit_guide, explicit_info = build_guide(*scene(), spec(support_top_shape="rectangular"))
    assert explicit_guide == implicit_guide
    assert explicit_info == implicit_info


@pytest.mark.parametrize("shape,width,depth", [("round", 0.8, 0.8), ("oval", 1.2, 0.7)])
def test_curved_support_projects_perimeter_without_moving_product(shape, width, depth):
    from hp3p.geometry import build_guide

    hero, mask = scene()
    rectangular_guide, rectangular = build_guide(hero, mask, spec())
    curved_guide, curved = build_guide(
        hero, mask, spec(support_top_shape=shape, support_width_m=width, support_depth_m=depth))
    assert curved_guide != rectangular_guide
    assert curved["support_top_shape"] == shape
    assert len(curved["support_polygon_px"]) == 128
    assert len(curved["user_edge_curve_px"]) == 33
    assert curved["product_bounds_px"] == rectangular["product_bounds_px"]
    assert curved["contact_px"] == rectangular["contact_px"]
    assert curved["width_axis_px"] == rectangular["width_axis_px"]
    assert curved["depth_axis_px"] == rectangular["depth_axis_px"]
    protected = np.asarray(Image.open(io.BytesIO(mask)))[..., 3] == 255
    expected = np.asarray(Image.open(io.BytesIO(hero)).convert("RGB"))
    actual = np.asarray(Image.open(io.BytesIO(curved_guide)).convert("RGB"))
    assert (actual[protected] == expected[protected]).all()


def test_oval_outline_back_projects_to_an_ellipse_on_the_support_plane():
    from hp3p.geometry import build_guide

    geometry = spec(support_top_shape="oval")
    _, info = build_guide(*scene(), geometry)
    w, h = 400, 300
    pitch = math.atan2(geometry["camera_height_m"] - geometry["look_at_height_m"],
                       geometry["horizontal_distance_m"])
    focal = h / (2 * math.tan(math.radians(geometry["vertical_fov_deg"]) / 2))
    rotation = np.array([[1, 0, 0], [0, -math.cos(pitch), -math.sin(pitch)],
                         [0, -math.sin(pitch), math.cos(pitch)]])
    camera = np.array([0, geometry["camera_height_m"], 0])
    world = []
    for u, v in info["support_polygon_px"]:
        ray = rotation.T @ np.array([(u - w / 2) / focal, (v - h / 2) / focal, 1])
        world.append(camera + ray * ((geometry["support_height_m"] - camera[1]) / ray[1]))
    world = np.asarray(world)
    assert world[:, 1] == pytest.approx(geometry["support_height_m"])
    center = world.mean(axis=0)
    yaw = math.radians(geometry["axis_angle_deg"])
    width_axis = np.array([math.cos(yaw), 0, math.sin(yaw)])
    depth_axis = np.array([-math.sin(yaw), 0, math.cos(yaw)])
    normalized = (((world - center) @ width_axis / (geometry["support_width_m"] / 2)) ** 2
                  + ((world - center) @ depth_axis / (geometry["support_depth_m"] / 2)) ** 2)
    assert normalized == pytest.approx(np.ones(128), abs=1e-10)


def test_curved_support_uses_digital_twin_projection_without_changing_product_pixels():
    from hp3p.geometry import build_guide

    position = np.array([2.1 * math.sin(math.radians(35)), -2.1 * math.cos(math.radians(35)), 1.2])
    target = np.array([0.0, 0.0, 0.8])
    look = (target - position) / np.linalg.norm(target - position)
    right = np.cross(look, [0, 0, 1])
    right /= np.linalg.norm(right)
    camera = {"position_m": position.tolist(), "right": right.tolist(),
              "up": np.cross(right, look).tolist(), "back": (-look).tolist(),
              "focal_length": 50.0, "horizontal_aperture": 36.0,
              "footprint_corners_m": [[-0.2, -0.15, 0.75], [0.2, -0.15, 0.75],
                                      [0.2, 0.15, 0.75], [-0.2, 0.15, 0.75]],
              "front_xy": [0.0, -1.0], "product_height_m": 0.3}
    hero, mask = scene()
    guide, info = build_guide(hero, mask, spec(support_top_shape="oval"), camera)
    assert info["camera_source"] == "digital_twin"
    assert len(info["support_polygon_px"]) == 128
    protected = np.asarray(Image.open(io.BytesIO(mask)))[..., 3] == 255
    assert (np.asarray(Image.open(io.BytesIO(guide)))[protected]
            == np.asarray(Image.open(io.BytesIO(hero)))[protected]).all()


def test_ellipse_rejects_product_corner_outside_curved_perimeter():
    from hp3p.geometry import build_guide

    # This lateral shift fits the old rectangular bounding box but pushes a base corner
    # through an ellipse, which needs the stronger four-corner containment check.
    with pytest.raises(ValueError, match="all four product footprint corners"):
        build_guide(*scene(), spec(support_top_shape="oval", support_lateral_offset_m=0.4))


def test_round_support_requires_a_physical_circle():
    from hp3p.geometry import build_guide

    with pytest.raises(ValueError, match="equal support_width_m and support_depth_m"):
        build_guide(*scene(), spec(support_top_shape="round"))


def test_shape_schema_is_strict_and_bounded_while_direct_callers_keep_default():
    from hp3p.geometry import GEOMETRY_SCHEMA

    assert "support_top_shape" in GEOMETRY_SCHEMA["required"]
    assert GEOMETRY_SCHEMA["properties"]["support_top_shape"]["enum"] == ["rectangular", "round", "oval"]


def test_printer_geometry_prose_does_not_force_primary_support_to_be_a_table():
    from hp3p.geometry import build_guide, describe_geometry

    _, info = build_guide(*scene(), spec(support_top_shape="rectangular"))
    text = describe_geometry(spec(support_top_shape="rectangular"), info, (400, 300),
                             product_category="printer")
    assert "primary support" in text.lower()
    assert "table" not in text.lower()
    assert "laptop" not in text.lower()


def test_round_geometry_prose_names_curved_rim_instead_of_corners():
    from hp3p.geometry import build_guide, describe_geometry

    geometry = spec(support_top_shape="round", support_width_m=0.8, support_depth_m=0.8)
    _, info = build_guide(*scene(), geometry)
    text = describe_geometry(geometry, info, (400, 300))
    assert "round" in text.lower()
    assert "curved rim" in text.lower()
    assert "table corners" not in text.lower()


@pytest.mark.parametrize("changes,field", [
    ({"horizontal_distance_m": 0}, "horizontal_distance_m"),
    ({"camera_height_m": float("nan")}, "camera_height_m"),
    ({"camera_height_m": 0.5}, "camera_height_m"),
    ({"support_depth_m": -1}, "support_depth_m"),
    ({"user_edge_gap_m": -0.1}, "user_edge_gap_m"),
    ({"user_side": "left"}, "user_side"),
    ({"support_depth_m": 0.2}, "contain"),
    ({"support_lateral_offset_m": 0.5}, "contain"),
    ({"vertical_fov_deg": 180}, "vertical_fov_deg"),
    ({"axis_angle_deg": 90}, "axis_angle_deg"),
    ({"furniture_boxes": [{"kind": "working_seat", "label": "chair", "box": [0.5, 0.3, 0.9, 0.8]}]}, "product"),
    ({"furniture_boxes": [{"kind": "working_seat", "label": "chair", "box": [0.1, 0.8, 0.0, 0.9]}]}, "box"),
])
def test_guide_rejects_invalid_geometry(changes, field):
    from hp3p.geometry import build_guide

    with pytest.raises(ValueError, match=field):
        build_guide(*scene(), spec(**changes))


def test_guide_allows_support_to_extend_outside_frame():
    from hp3p.geometry import build_guide

    guide, info = build_guide(*scene(), spec(support_width_m=4, support_depth_m=3))
    assert Image.open(io.BytesIO(guide)).size == (400, 300)
    polygon = np.asarray(info["support_polygon_px"])
    assert np.isfinite(polygon).all()
    assert polygon[:, 0].min() < 0 and polygon[:, 0].max() > 400


def _side_of_edge(info):
    (ax, ay), (bx, by) = info["user_edge_px"]
    u, v = info["contact_px"]
    # Positive: contact lies above the edge line in image coordinates.
    return ((bx - ax) * (v - ay) - (by - ay) * (u - ax)) / math.hypot(bx - ax, by - ay)


@pytest.mark.parametrize("angle", [0, 20, -20])
def test_user_facing_edge_is_placed_from_the_product_base_not_a_centered_support(angle):
    from hp3p.geometry import build_guide

    # The base's near edge passes through the contact, so a zero near-side gap puts the edge there.
    _, flush = build_guide(*scene(), spec(axis_angle_deg=angle, user_edge_gap_m=0))
    assert _side_of_edge(flush) == pytest.approx(0, abs=0.5)
    _, near = build_guide(*scene(), spec(axis_angle_deg=angle, user_edge_gap_m=0.1))
    assert _side_of_edge(near) < -5
    _, far = build_guide(*scene(), spec(axis_angle_deg=angle, user_side="far_from_camera"))
    assert _side_of_edge(far) > 5
    polygon = np.asarray(near["support_polygon_px"])
    assert polygon[:, 1].max() == pytest.approx(max(y for _, y in near["user_edge_px"]))


def test_guide_rejects_contact_behind_projection_near_plane():
    from hp3p.geometry import build_guide

    with pytest.raises(ValueError, match="contact.*near"):
        build_guide(*scene(bottom=280), spec(camera_height_m=0.76, look_at_height_m=0.755))


def test_working_seat_budget_does_not_depend_on_caption_wording():
    from hp3p.geometry import build_guide

    with pytest.raises(ValueError, match="seat.*dominates"):
        build_guide(*scene(), spec(furniture_boxes=[
            {"kind": "working_seat", "label": "foreground seating", "box": [0, 0.1, 0.5, 0.9]},
        ]))


@pytest.mark.parametrize("fov,mm,family", [(90, 12.98, "ultra-wide"), (20, 73.61, "short-telephoto")])
def test_lens_estimate_uses_camera_fov_and_canvas_aspect(fov, mm, family):
    from hp3p.geometry import build_guide

    _, info = build_guide(*scene(), spec(vertical_fov_deg=fov))
    assert info["lens_35mm_equivalent_mm"] == pytest.approx(mm, abs=0.02)
    assert info["lens_family"] == family


def source_edges():
    return [
        {"axis": "width", "start_px": [712.49758, 449.94049], "end_px": [587.50242, 350.05951]},
        {"axis": "width", "start_px": [912.15773, 700.36285], "end_px": [787.84227, 599.63715]},
        {"axis": "depth", "start_px": [597.49915, 460.36275], "end_px": [702.50085, 339.63725]},
        {"axis": "depth", "start_px": [799.79766, 712.28744], "end_px": [900.20234, 587.71256]},
    ]


def test_source_camera_fit_explains_edges_instead_of_accepting_a_free_camera_guess():
    from hp3p.geometry import fit_source_camera

    # Independent pinhole fixture: 75-degree pitch, 30-degree vertical FOV, -40-degree yaw.
    fitted = fit_source_camera(source_edges(), (1216, 912))
    assert fitted["camera_pitch_deg"] == pytest.approx(75, abs=1)
    assert fitted["vertical_fov_deg"] == pytest.approx(30, abs=2)
    assert fitted["axis_angle_deg"] == pytest.approx(-40, abs=0.5)
    assert fitted["max_edge_error_deg"] < 0.1


@pytest.mark.parametrize("failure", ["missing_axis", "zero_length", "nonfinite", "inconsistent"])
def test_source_camera_fit_rejects_unusable_observations(failure):
    from hp3p.geometry import fit_source_camera

    edges = source_edges()
    if failure == "missing_axis":
        edges = edges[:2]
    elif failure == "zero_length":
        edges[0]["end_px"] = edges[0]["start_px"]
    elif failure == "nonfinite":
        edges[0]["start_px"][0] = float("nan")
    else:
        edges[0].update(start_px=[600, 500], end_px=[800, 500])
        edges[1].update(start_px=[700, 400], end_px=[700, 600])
    with pytest.raises(ValueError):
        fit_source_camera(edges, (1216, 912))


def test_guide_plans_wall_behind_support_only():
    from hp3p.geometry import build_guide

    _, info = build_guide(*scene(), spec(back_edge_against_wall=True))
    wall = np.asarray(info["wall_polygon_px"])
    assert len(wall) >= 3 and wall[:, 1].min() < np.asarray(info["support_polygon_px"])[:, 1].min()
    _, plain = build_guide(*scene(), spec(back_edge_against_wall=False))
    assert plain["wall_polygon_px"] is None
    with pytest.raises(ValueError, match="between camera and product"):
        build_guide(*scene(), spec(user_side="far_from_camera", back_edge_against_wall=True))


def test_guide_draws_only_support_surface_and_product():
    from hp3p.geometry import SURFACE_FILL, SURFACE_OUTLINE, build_guide

    hero, mask = scene()
    guide, _ = build_guide(hero, mask, spec(back_edge_against_wall=True, furniture_boxes=[
        {"kind": "background_furniture", "label": "shelf", "box": [0.0, 0.0, 0.3, 0.3]}]))
    pixels = np.asarray(Image.open(io.BytesIO(guide)).convert("RGB"))
    keep = np.asarray(Image.open(io.BytesIO(mask)).getchannel("A")) == 255
    assert (pixels[keep] == np.asarray(Image.open(io.BytesIO(hero)).convert("RGB"))[keep]).all()
    colors = {tuple(c) for c in np.unique(pixels[~keep], axis=0)}
    assert colors == {(255, 255, 255), SURFACE_FILL, SURFACE_OUTLINE}


def test_twin_camera_summary_reports_azimuth_faces_and_user_edge():
    from hp3p.geometry import twin_camera_summary, twin_camera_text

    position = np.array([2.1 * math.sin(math.radians(35)), -2.1 * math.cos(math.radians(35)), 1.2])
    target = np.array([0.0, 0.0, 0.8])
    look = (target - position) / np.linalg.norm(target - position)
    right = np.cross(look, [0, 0, 1])
    right /= np.linalg.norm(right)
    camera = {"position_m": position.tolist(), "right": right.tolist(), "up": np.cross(right, look).tolist(),
              "back": (-look).tolist(), "focal_length": 50.0, "horizontal_aperture": 36.0,
              "footprint_corners_m": [[-0.2, -0.15, 0.75], [0.2, -0.15, 0.75], [0.2, 0.15, 0.75], [-0.2, 0.15, 0.75]],
              "front_xy": [0.0, -1.0], "product_height_m": 0.3}
    facts = twin_camera_summary(camera, (1216, 912))
    assert facts["camera_azimuth_from_product_front_deg"] == pytest.approx(35, abs=0.5)
    assert facts["camera_above_support_top_m"] == pytest.approx(0.45)
    assert facts["product_front_faces_user_side"] == "near_camera"
    assert facts["visible_faces"] == [{"face": "front", "image_side": "left"},
                                      {"face": "user's right side", "image_side": "right"}]
    assert "35 degrees around from straight in front of the product toward the user's right" in twin_camera_text(facts)
