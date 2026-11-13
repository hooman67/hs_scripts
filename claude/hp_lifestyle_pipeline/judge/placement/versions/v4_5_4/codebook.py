"""Application-owned V4.5.2 placement taxonomy, severities, and penalty groups."""

FUNCTIONAL_TESTS = (
    "support_role", "support_room_placement", "device_surface_position",
    "prop_activity_relation", "operating_access", "user_position",
)
GEOMETRY_TESTS = (
    "device_support_axes", "furniture_room_axes", "product_scale", "load_path",
    "support_anatomy", "shared_perspective", "support_contact", "shadows_reflections",
)
ALL_TESTS = FUNCTIONAL_TESTS + GEOMETRY_TESTS

DEFECT_SUBTYPES = {
    "support_role": {"occupied_personal_workstation", "incompatible_support"},
    "support_room_placement": {"central_rectangular_home_printer_support_without_shared_use", "misplaced_support_in_room", "incoherent_visible_use_zone"},
    "device_surface_position": {"stranded_on_support", "awkward_foreground_position", "too_far_from_usable_edge", "aimed_toward_corner"},
    "prop_activity_relation": {"prop_blocks_operation", "prop_contradicts_activity_zone"},
    "operating_access": {"blocked", "excessive_reach"},
    "user_position": {"chair_offset", "no_feasible_position"},
    "device_support_axes": {"visible_axis_conflict"},
    "furniture_room_axes": {"visible_furniture_room_axis_conflict"},
    "product_scale": {"implausible_context_scale"},
    "load_path": {"visible_missing_support"},
    "support_anatomy": {"malformed_connected_furniture"},
    "shared_perspective": {"incompatible_geometry_or_depth"},
    "support_contact": {"floating", "sinking", "interpenetrating", "overhanging", "unsupported_base"},
    "shadows_reflections": {"inconsistent_contact_light_transport"},
}

COHERENT_SUBTYPES = {
    "support_role": {"dedicated_equipment_support", "usable_laptop_work_surface"},
    "support_room_placement": {"coherent_wall_edge", "coherent_shared_use", "coherent_room_placement"},
    "device_surface_position": {"usable_surface_position"},
    "prop_activity_relation": {"coherent_activity_zone", "not_applicable"},
    "operating_access": {"open"},
    "user_position": {"coherent", "not_applicable"},
    "device_support_axes": {"coherent_axes"},
    "furniture_room_axes": {"coherent_axes"},
    "product_scale": {"plausible_context_scale"},
    "load_path": {"coherent_leg", "coherent_panel", "coherent_pedestal", "coherent_bracket", "coherent_wall_attachment", "not_applicable"},
    "support_anatomy": {"coherent_connected_furniture"},
    "shared_perspective": {"coherent_geometry_and_depth"},
    "support_contact": {"supported"},
    "shadows_reflections": {"coherent_contact_light_transport"},
}

ISSUE_BY_SUBTYPE = {
    "occupied_personal_workstation": "occupied_workstation",
    "incompatible_support": "inappropriate_support",
    "central_rectangular_home_printer_support_without_shared_use": "misplaced_support_furniture",
    "misplaced_support_in_room": "misplaced_support_furniture",
    "incoherent_visible_use_zone": "incoherent_use_zone",
    "stranded_on_support": "unmotivated_device_position",
    "awkward_foreground_position": "unmotivated_device_position",
    "too_far_from_usable_edge": "unmotivated_device_position",
    "aimed_toward_corner": "unmotivated_device_position",
    "prop_blocks_operation": "incoherent_prop_arrangement",
    "prop_contradicts_activity_zone": "incoherent_prop_arrangement",
    "blocked": "blocked_operating_path",
    "excessive_reach": "excessive_reach",
    "chair_offset": "chair_displacement",
    "no_feasible_position": "no_feasible_user_position",
    "visible_axis_conflict": "device_support_axis_conflict",
    "visible_furniture_room_axis_conflict": "furniture_layout_conflict",
    "implausible_context_scale": "implausible_scale",
    "visible_missing_support": "missing_required_support",
    "malformed_connected_furniture": "malformed_support_furniture",
    "incompatible_geometry_or_depth": "conflicting_perspective",
    "floating": "floating",
    "sinking": "sinking_or_intersection",
    "interpenetrating": "sinking_or_intersection",
    "overhanging": "unsupported_product",
    "unsupported_base": "unsupported_product",
    "inconsistent_contact_light_transport": "inconsistent_shadow",
}

# Severity is never accepted from a model.
SEVERITY_BY_SUBTYPE = {
    "chair_offset": 1,
    "prop_contradicts_activity_zone": 1,
    "awkward_foreground_position": 1,
    "inconsistent_contact_light_transport": 1,
    **{subtype: 2 for subtype in ISSUE_BY_SUBTYPE},
}
SEVERITY_BY_SUBTYPE.update({
    "chair_offset": 1,
    "prop_contradicts_activity_zone": 1,
    "awkward_foreground_position": 1,
    "inconsistent_contact_light_transport": 1,
})

SEVERITY_PENALTY = {1: 12, 2: 40, 3: 70}
PENALTY_GROUPS = {
    "support_scene": {"support_role", "support_room_placement", "device_surface_position"},
    "operating_use": {"prop_activity_relation", "operating_access", "user_position"},
    "orientation_perspective": {"device_support_axes", "furniture_room_axes", "shared_perspective"},
    "scale": {"product_scale"},
    "structure_contact": {"load_path", "support_anatomy", "support_contact"},
    "light_transport": {"shadows_reflections"},
}
COMPONENT_TESTS = {
    "support_scenario": ("support_role", "support_room_placement", "device_surface_position", "prop_activity_relation"),
    "access_usability": ("operating_access", "user_position"),
    "orientation_alignment": ("device_support_axes", "furniture_room_axes"),
    "scale_perspective": ("product_scale", "load_path", "support_anatomy", "shared_perspective"),
    "contact_integration": ("support_contact", "shadows_reflections"),
}

