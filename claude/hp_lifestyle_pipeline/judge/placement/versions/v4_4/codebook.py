"""Fixed V4.4 defect tests and issue-code ownership."""

TEST_ISSUES = {
    "support_role": ["inappropriate_support", "occupied_workstation"],
    "support_room_placement": ["misplaced_support_furniture", "incoherent_use_zone"],
    "device_surface_position": ["unmotivated_device_position"],
    "prop_activity_relation": ["incoherent_prop_arrangement"],
    "operating_access": ["blocked_operating_path", "excessive_reach"],
    "user_position": ["no_feasible_user_position", "chair_displacement"],
    "device_support_axes": ["device_support_axis_conflict"],
    "furniture_room_axes": ["furniture_layout_conflict"],
    "product_scale": ["implausible_scale"],
    "load_path": ["missing_required_support"],
    "support_anatomy": ["malformed_support_furniture"],
    "shared_perspective": ["conflicting_perspective"],
    "support_contact": ["unsupported_product", "floating", "sinking_or_intersection"],
    "shadows_reflections": ["inconsistent_shadow", "inconsistent_reflection"],
}

# V4.4 owns one broad, deterministic issue code per visual test. The model
# proposes a test and cause; it never selects taxonomy labels.
ISSUE_BY_TEST = {
    "support_role": "inappropriate_support",
    "support_room_placement": "misplaced_support_furniture",
    "device_surface_position": "unmotivated_device_position",
    "prop_activity_relation": "incoherent_prop_arrangement",
    "operating_access": "blocked_operating_path",
    "user_position": "chair_displacement",
    "device_support_axes": "device_support_axis_conflict",
    "furniture_room_axes": "furniture_layout_conflict",
    "product_scale": "implausible_scale",
    "load_path": "missing_required_support",
    "support_anatomy": "malformed_support_furniture",
    "shared_perspective": "conflicting_perspective",
    "support_contact": "unsupported_product",
    "shadows_reflections": "inconsistent_shadow",
}

SUBTYPE_ISSUES = {
    "support_role": {"occupied_personal_workstation": "occupied_workstation", "incompatible_support": "inappropriate_support"},
    "support_room_placement": {"misplaced_furniture": "misplaced_support_furniture", "incoherent_use_zone": "incoherent_use_zone"},
    "operating_access": {"blocked": "blocked_operating_path", "excessive_reach": "excessive_reach"},
    "user_position": {"chair_displacement": "chair_displacement", "no_feasible_user_position": "no_feasible_user_position"},
    "support_contact": {"unsupported": "unsupported_product", "floating": "floating", "sinking_or_intersection": "sinking_or_intersection"},
    "shadows_reflections": {"inconsistent_shadow": "inconsistent_shadow", "inconsistent_reflection": "inconsistent_reflection"},
}

SUBTYPE_FIELD = {
    "support_role": "support_role_class",
    "support_room_placement": "support_room_class",
    "operating_access": "operating_access_class",
    "user_position": "user_position_class",
    "support_contact": "support_contact_class",
    "shadows_reflections": "light_transport_class",
}

DEFECT_SUBTYPES = {test_id: frozenset(mapping) for test_id, mapping in SUBTYPE_ISSUES.items()}
NONDEFECT_SUBTYPE = {
    "support_role": "compatible_support",
    "support_room_placement": "coherent",
    "operating_access": "open",
    "user_position": "coherent",
    "support_contact": "supported",
    "shadows_reflections": "coherent",
}


def issue_for(test_id, inventory):
    field = SUBTYPE_FIELD.get(test_id)
    if field:
        return SUBTYPE_ISSUES[test_id].get(inventory.get(field), ISSUE_BY_TEST[test_id])
    return ISSUE_BY_TEST[test_id]


def issue_for_subtype(test_id, subtype):
    """Map a verifier-observed visual subtype to a public issue code."""
    return SUBTYPE_ISSUES.get(test_id, {}).get(subtype, ISSUE_BY_TEST[test_id])
