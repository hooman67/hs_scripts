"""Unintegrated proposal for detecting extreme tabletop edge asymmetry.

This module is deliberately outside the V4.5.4 runtime path. It turns already
structured, visibly traced edge coordinates into a proposed support-anatomy
defect; it does not attempt to decide whether the furniture is rectilinear,
tapered, or hinged.
"""

from __future__ import annotations

from itertools import combinations
from typing import Any


def propose_malformed_support_anatomy(
    edge_observations: list[dict[str, Any]],
    tabletop_width: float,
    *,
    near_vertical_max: float = 0.03,
    strong_lateral_min: float = 0.15,
    comparable_dy_ratio_min: float = 0.8,
) -> dict[str, Any] | None:
    """Return a proposed defect when two support-side edges meet the criterion.

    Coordinates and ``tabletop_width`` must use the same normalized coordinate
    system. Edge observations are assumed to satisfy the observer contract that
    traced segments are visible in raw pixels. Threshold comparisons are strict:
    below 3% and above 15% by default. The caller must independently establish
    ordinary rectilinear construction.
    """
    if not isinstance(tabletop_width, (int, float)) or tabletop_width <= 0:
        raise ValueError("tabletop_width must be positive")

    sides = []
    for edge in edge_observations:
        if edge.get("owner") != "support_side":
            continue
        p0, p1 = edge.get("p0"), edge.get("p1")
        if not (
            isinstance(p0, list)
            and isinstance(p1, list)
            and len(p0) == 2
            and len(p1) == 2
            and all(isinstance(value, (int, float)) for value in (*p0, *p1))
        ):
            continue
        sides.append(
            {
                "p0": p0,
                "p1": p1,
                "dx": abs(p1[0] - p0[0]),
                "dy": abs(p1[1] - p0[1]),
            }
        )

    for first, second in combinations(sides, 2):
        if first["p0"] == second["p0"] and first["p1"] == second["p1"]:
            continue
        larger_dy = max(first["dy"], second["dy"])
        if larger_dy == 0 or min(first["dy"], second["dy"]) / larger_dy < comparable_dy_ratio_min:
            continue
        first_ratio = first["dx"] / tabletop_width
        second_ratio = second["dx"] / tabletop_width
        low, high = sorted((first_ratio, second_ratio))
        if low < near_vertical_max and high > strong_lateral_min:
            evidence = (
                f"Two distinct support_side edges have comparable |dy| "
                f"({first['dy']:.4f}, {second['dy']:.4f}) but horizontal runs/tabletop width "
                f"of {first_ratio:.2%} and {second_ratio:.2%}; endpoints are "
                f"{first['p0']}->{first['p1']} and {second['p0']}->{second['p1']}, "
                f"with tabletop width {tabletop_width:.4f}."
            )
            return {
                "test_id": "support_anatomy",
                "state": "defect",
                "subtype": "malformed_connected_furniture",
                "direct_evidence": evidence,
                "measurements": {
                    "tabletop_width": tabletop_width,
                    "horizontal_run_fractions": [first_ratio, second_ratio],
                    "absolute_vertical_runs": [first["dy"], second["dy"]],
                },
            }
    return None
