# V4.5 focused visual-scan probe

**Decision: diagnostic only; do not promote.**

This one-call probe removes the scene prompt and inspects seven fixed visual relations. The six cases are reused development examples, not validation.

- Required issue recall: 3/7 (V4.4 majority: 1/7).
- Labeled verdict matches: 1/5 (V4.4 majority: 2/5).
- It recovered central support placement and incoherent floor-prop evidence, but under-scored both as severity 1.
- It still missed malformed furniture, missing support, product/support axis conflict, and shared perspective conflict.
- It over-scored the movable-chair offset as severity 2 instead of the requested review-level severity 1.

| Case | Expected | Actual | Required detected |
|---|---|---|---|
| `elitebook__laptop_FrontLeftMedium__p1` | review / user_position | fail / user_position | user_position |
| `tassel__printer_FrontWide__p1` | fail / support_anatomy, support_room_placement | review / support_room_placement | support_room_placement |
| `magic__printer_FrontLeftMedium__p1` | fail / load_path | pass / clean | none |
| `tassel__printer_FrontCloseUp__p2` | fail / device_support_axes, prop_activity_relation | review / prop_activity_relation | prop_activity_relation |
| `tassel__printer_FrontRightCloseUp__p1` | issue-only / shared_perspective | pass / clean | none |
| `magic__printer_FrontRightCloseUp__p2` | pass / clean | pass / clean | none |

This shows that independent defect scanning improves issue discovery, but a single broad scan remains inadequate for furniture topology and perspective. V4.5 needs separate functional/room and geometry/topology passes plus deterministic severity policy and bounded adjudication.
