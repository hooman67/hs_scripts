from merge_consensus import final_policy, resolve_component


def comp(severity, confidence="high", visibility="observed", codes=None, evidence="evidence"):
    return {"visibility": visibility, "severity": severity, "confidence": confidence, "evidence": evidence, "consequence": "consequence" if severity else "", "issue_codes": codes or []}


def test_confirmed_consensus_uses_intersection_and_minima():
    selected, resolution = resolve_component("access_usability", comp(3, "high", "observed", ["no_user_position", "blocked_operating_side"], "proposal"), comp(2, "medium", "partial", ["no_user_position"], "independent"), comp(0))
    assert resolution["status"] == "confirmed_consensus"
    assert selected["severity"] == 2 and selected["confidence"] == "medium" and selected["visibility"] == "partial"
    assert selected["issue_codes"] == ["no_user_position"]
    assert "proposal" in selected["evidence"] and "independent" in selected["evidence"]


def test_confident_clear_rejects_and_keeps_baseline():
    baseline = comp(1, "medium", codes=["unmotivated_position"])
    selected, resolution = resolve_component("support_scenario", comp(3, codes=["inappropriate_support"]), comp(0), baseline)
    assert resolution["status"] == "rejected_confident_clear_or_minor"
    assert selected == baseline
    decision = final_policy("pass", {"verdict": "pass", "verdict_reasons": ["pass_criteria_met"], "confidence": "high"}, {"support_scenario": resolution})
    assert decision["verdict"] == "pass" and decision["reported_overall_confidence"] == "medium"


def test_disjoint_material_codes_reject():
    selected, resolution = resolve_component("orientation_alignment", comp(2, codes=["chair_alignment_conflict"]), comp(2, codes=["furniture_layout_conflict"]), comp(0))
    assert resolution["status"] == "rejected_disjoint_material_issue_codes"
    assert selected["severity"] == 0


def test_unobservable_without_clear_counter_defers_baseline_pass():
    selected, resolution = resolve_component("orientation_alignment", comp(None, "low", "unobservable", []), comp(2, codes=["chair_alignment_conflict"]), comp(0))
    assert resolution["status"] == "unconfirmed_uncertain"
    decision = final_policy("pass", {"verdict": "pass", "verdict_reasons": ["pass_criteria_met"], "confidence": "high"}, {"orientation_alignment": resolution})
    assert decision["verdict"] == "review"
    assert decision["reported_overall_confidence"] == "medium"


def test_confident_clear_takes_precedence_over_low_confidence_material():
    _, resolution = resolve_component("access_usability", comp(2, "low", codes=["no_user_position"]), comp(0, "high"), comp(0))
    assert resolution["status"] == "rejected_confident_clear_or_minor"


def test_existing_fail_is_preserved_for_unconfirmed():
    _, resolution = resolve_component("access_usability", comp(None, "low", "unobservable", []), comp(2, codes=["no_user_position"]), comp(0))
    decision = final_policy("fail", {"verdict": "fail", "verdict_reasons": ["clear_placement_defect_veto"], "confidence": "high"}, {"access_usability": resolution})
    assert decision["verdict"] == "fail"
