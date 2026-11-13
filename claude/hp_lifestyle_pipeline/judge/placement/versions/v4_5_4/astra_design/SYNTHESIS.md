# V4.5 natural-placement judge recommendation

**Status:** local synthesis after all bounded Astra design requests timed out. This is a development proposal, not a validated judge or an Astra answer.

## Evidence boundary

V4.4 was tested on six reused labeled development cases with three repeats each. It produced 18/18 scoreable results, 4/21 repeat-level required-issue detections, 1/7 majority required issues, and 0/9 correct `fail` verdicts on material-fail repeats. All four predicted issue instances were correct, so the dominant problem was false-negative recall rather than false-positive precision.

The focused V4.5 root probe removed the scene prompt and used one smaller seven-check scan. It improved required-issue recall from 1/7 to 3/7, while verdict matches fell from 2/5 to 1/5 because the model assigned severity inconsistently. It recovered chair displacement, central support placement, and incoherent prop placement, but still missed malformed furniture, missing load path, product/support axis conflict, and shared perspective. The clean control remained clean.

These results support changing task decomposition and making severity application-owned. Adding more prose to one broad scout is not supported.

## Failure diagnosis

1. **Chair displacement:** V4.4 succeeded in all three repeats. The scout saw the only visible chair laterally offset, assigned severity 1, and the verifier confirmed it. Preserve this visual relation and make its severity deterministic.
2. **Central malformed home table:** V4.4 found central placement in only one of three repeats and never found malformed sides. The two misses accepted prompt-consistent “sorting area” stories and described visibly questionable table edges as coherent. The focused no-prompt probe recovered central placement, showing prompt removal helps room-use perception. Furniture shape needs a separate topology task.
3. **Missing printer-table legs/load path:** V4.4 missed all three times. It treated a dark rail/partial visible support as a complete load path and did not inventory which exposed tabletop regions actually connect to the floor. This requires a topology-specific crop and explicit support-element inventory.
4. **Slanted printer plus puzzle:** V4.4 missed both issues in every repeat. The scene prompt explicitly described a puzzle on a nearby rug, which encouraged narrative acceptance. The no-prompt probe recovered the incoherent prop but still missed the product/support axis conflict. Axis comparison needs a focused geometric pass.
5. **Wall/table/cabinet perspective conflict:** V4.4 missed all three repeats and asserted coherence without recording comparable edge families or depth constraints. This requires a room-geometry view and explicit pairwise relation facts.
6. **Clean control:** V4.4 and the no-prompt probe correctly passed it. The unrelated disfigured glasses should remain an advisory and must not affect placement scoring.

## Selected minimal architecture

Use **two independent, disjoint perception calls** followed by deterministic synthesis. Do not use a scout-positive-only verifier in the first V4.5 experiment: it cannot recover omissions, and current evidence shows precision is already high while recall is the failure. Do not pass the scene prompt to either perception call.

### Call A: functional and room-layout observer

Inputs:

- raw generated scene, authoritative;
- original twin only to identify product and functional front;
- product type;
- no scene prompt, human label, score, prior model result, or target-specific anchor.

Owned relations:

- `support_role`
- `support_room_placement`
- `device_surface_position`
- `prop_activity_relation`
- `operating_access`
- `user_position`

Required output is an observation table, not a verdict or severity:

```json
{
  "stage_status": "assessed | unable",
  "unable_reason": null,
  "product_front": {"state": "observed | partial | hidden", "region": [0,0,1,1], "evidence": "..."},
  "visible_user_positions": [{"kind": "chair | standing_zone", "region": [0,0,1,1]}],
  "relations": [
    {
      "test_id": "support_room_placement",
      "observability": "visible | partial | hidden",
      "state": "coherent | defect | unresolved",
      "subtype": "central_rectangular_home_support_without_shared_use | coherent_wall_edge | not_applicable",
      "direct_evidence": "visible objects and relation only",
      "counterevidence": "visible benign evidence only",
      "region": [0,0,1,1]
    }
  ],
  "unrelated_artifacts": [{"region": [0,0,1,1], "evidence": "..."}]
}
```

Semantic invariants:

- Return all six test IDs exactly once.
- `defect` requires a positive visible relation and a positive-area region.
- `hidden` must map to `unresolved`; missing evidence cannot map to `defect`.
- A visible chair is evaluated as visible; do not invent an off-frame chair.
- A central rectangular home-printer support is coherent only when pixels show a shared work/equipment use. Prompt intent is unavailable.
- Props are defective only when pixels show blocked operation or a contradictory activity/use zone.
- No score, verdict, severity, or issue code is model-owned.

### Call B: geometry and support-topology observer

Inputs:

- raw generated scene, authoritative;
- original twin for footprint and functional-front identity;
- deterministic unwarped product/support crop;
- a deterministic larger furniture/room crop that retains the entire visible support, floor junction, nearest wall/cabinet, and neighboring furniture;
- optional Canny/Hough overlay as a navigation aid, labeled as possibly false or incomplete;
- product type;
- no scene prompt, label, score, Call A output, or target-specific anchor.

Owned relations:

- `device_support_axes`
- `furniture_room_axes`
- `product_scale`
- `load_path`
- `support_anatomy`
- `shared_perspective`
- `support_contact`
- `shadows_reflections`

The output shape matches Call A's observation pattern but adds compact structured facts:

```json
{
  "stage_status": "assessed | unable",
  "support_inventory": {
    "visible_elements": ["top", "leg", "panel", "pedestal", "rail", "bracket", "wall_attachment"],
    "exposed_required_regions": [{"region": [0,0,1,1], "connected_support_visible": true}],
    "visible_breaks_or_negative_space": [{"region": [0,0,1,1], "kind": "gap | disconnection | unsupported_span"}]
  },
  "edge_observations": [
    {"owner": "product_front | support_front | support_side | wall | cabinet | floor", "p0": [0,0], "p1": [1,1]}
  ],
  "relations": [
    {
      "test_id": "load_path",
      "observability": "visible | partial | hidden",
      "state": "coherent | defect | unresolved",
      "subtype": "visible_missing_support | coherent_leg | coherent_panel | coherent_pedestal | unresolved",
      "direct_evidence": "...",
      "counterevidence": "...",
      "region": [0,0,1,1]
    }
  ],
  "unrelated_artifacts": []
}
```

Semantic invariants:

- Return all eight test IDs exactly once.
- The model records edge segments, junctions, support elements, and relation states; it never assigns scores or severities.
- `load_path:defect` requires an exposed required region plus a visible gap, disconnection, or unsupported span. A cropped underside is `unresolved`.
- One visible rail cannot establish a complete furniture load path unless it visibly connects the relevant supported region to a leg/panel/pedestal/wall attachment.
- `support_anatomy:defect` needs a visible impossible junction, inconsistent connected surfaces, or incompatible corresponding side boundaries.
- `device_support_axes:defect` needs product and support edge observations plus a visible conflict. A diagonal is coherent only when visible use geometry supports it; no narrative rescue is allowed.
- `shared_perspective:defect` needs named edge/depth relations that cannot share one camera interpretation. Merely different 2D slopes are insufficient.
- Overlay lines can direct attention but cannot populate evidence fields unless the raw pixels show the same edge.

## Deterministic synthesis

The application validates both outputs and owns issue codes, severity, score, and verdict.

### Issue mapping

| Test | Defect subtype | Issue code |
|---|---|---|
| support_role | occupied personal workstation | `occupied_workstation` |
| support_role | incompatible support | `inappropriate_support` |
| support_room_placement | central/misplaced support | `misplaced_support_furniture` |
| support_room_placement | incoherent visible use zone | `incoherent_use_zone` |
| device_surface_position | visibly stranded/awkward position | `unmotivated_device_position` |
| prop_activity_relation | blocking/contradictory prop | `incoherent_prop_arrangement` |
| operating_access | blocked | `blocked_operating_path` |
| operating_access | excessive reach | `excessive_reach` |
| user_position | chair offset | `chair_displacement` |
| user_position | no feasible position | `no_feasible_user_position` |
| device_support_axes | visible conflict | `device_support_axis_conflict` |
| furniture_room_axes | visible conflict | `furniture_layout_conflict` |
| product_scale | implausible | `implausible_scale` |
| load_path | exposed missing support | `missing_required_support` |
| support_anatomy | malformed connected furniture | `malformed_support_furniture` |
| shared_perspective | incompatible geometry/depth | `conflicting_perspective` |
| support_contact | unsupported/float/intersection | existing narrow contact subtype |
| shadows_reflections | inconsistent | existing narrow light subtype |

### Application-owned severity

- `chair_displacement`: severity 1 unless the visible relation makes laptop use infeasible, in which case `no_feasible_user_position` is severity 2.
- Central rectangular/square home printer support without visible shared use: severity 2.
- Visible missing load path or malformed load-bearing furniture: severity 2; severity 3 only for impossible collapse/floating structure.
- Clear product/support axis conflict requiring product repositioning: severity 2.
- Clear shared-perspective contradiction affecting product/support/furniture integration: severity 2.
- Prop contradiction that is odd but does not block use: severity 1; blocking the functional path is severity 2 under operating access.
- Unrelated malformed glasses or décor: warning only, zero placement penalty.

Unknown/unresolved is never a defect. If a stage is unable, or a material relation is contradictory within its own structured facts, return a `review` sentinel with `score_valid:false`; do not silently pass.

Use frozen penalty groups from V4.4 so one physical cause incurs one penalty. Suggested amounts remain 12/40/70 for severities 1/2/3. Any severity >=2 yields `fail` with score <=59. Severity 1 yields `review` with score 60–89. No defects and both stages valid yields `pass`/100. The score is diagnostic; verdict and issue evidence are primary.

## Prompt language

### Call A core instruction

> Inspect only visible functional and room-layout relations in RAW_SCENE. ORIGINAL_TWIN identifies the product and functional front; it does not prove a scene relation. No scene prompt is available. Record observations, not stories, scores, verdicts, or severities. For every fixed relation, report coherent, defect, or unresolved. A defect requires a named visible relation and region. Hidden or cropped evidence is unresolved. Do not invent an off-frame user, shared-work narrative, or unseen support. Visible benign evidence may defeat a defect; hypothetical intent may not.

### Call B core instruction

> Inspect only visible product/support geometry, furniture topology, load path, contact, scale, perspective, shadows, and reflections. RAW_SCENE controls. Crops and edge overlays are attention aids and may be wrong. Inventory visible support elements and trace named raw-pixel edges/junctions before classifying any relation. Record observations, not stories, scores, verdicts, or severities. A missing support requires an exposed required region plus a visible gap, disconnection, or unsupported span. A geometry conflict requires named raw-pixel edge/depth relations that cannot share a coherent interpretation. Hidden structure is unresolved, not defective or healthy.

## Call budget and failures

- Normal: 2 calls, one for each specialist. Run independently; neither sees the other's output.
- Worst case: 3 calls total, using one global objective repair only for invalid JSON/schema/transport failure. A valid visual conclusion is never retried.
- SDK retries: 0. Application handles bounded transport retry explicitly and records it.
- Per-call timeout: 600 seconds.
- If the global repair is consumed and the other stage then fails, return an execution-error `review` sentinel with `score_valid:false`.
- Cache keys include input image hashes, twin hash, product type, both prompt/schema hashes, crop/overlay algorithm hashes, model returned, and deterministic synthesis hash.

No visual anchors are recommended for the first V4.5 gate. The two-pass decomposition is the smallest supported experiment. If geometry recall remains low, the next change is frozen generic non-target geometry anchors or separate topology and perspective calls, not target-case examples.

## Development and held-out gates

### Gate A: reused six development cases

Run three repeats per case. Promote only if all are true:

1. 18/18 results are structurally valid or explicit error sentinels; no silent pass on execution failure.
2. Each of the three labeled-fail cases returns majority `fail` (at least 2/3 repeats).
3. Every one of the seven required issue codes is detected in at least 2/3 repeats for its case; repeat-level required-issue recall is at least 16/21.
4. The chair case returns `review` in at least 2/3 and never `fail`.
5. The clean placement control returns `pass` in 3/3 with zero forbidden placement issues; disfigured glasses may appear only as an unrelated warning.
6. No target label/comment/expected answer enters either request.

Failure of any item means stop; diagnose before a fresh gate. These are tuning examples and cannot estimate accuracy.

### Gate B: frozen held-out 8–12 cases

Freeze images, hashes, expected issue families, and labels before any run. Include at least:

- two clean/tight-crop controls;
- two functional/room-layout defects;
- two topology/load-path defects;
- two axis/perspective defects;
- one unrelated-artifact control;
- laptop and printer coverage.

With labels withheld from requests, require:

- all material-defect cases detected by majority across two repeats;
- at least 80% required-issue recall across held-out labels;
- zero majority false fails on clean controls and no more than one false review;
- 100% schema-valid or explicit sentinel outputs;
- at least 80% exact verdict stability across repeats.

Only then run 160 cases, and describe that run as a diagnostic distribution, not calibrated accuracy.

## Falsification and next step

This design is inadequate if Call B still asserts coherent topology/perspective without recording usable edges/junctions, if any clean control false-fails, or if Gate A cannot reach majority detection of all four previously missed geometry families.

The next smallest change would split Call B into two independent calls: (B1) support topology/load/contact and (B2) axes/shared perspective/scale. Normal cost would rise from two to three calls. A generic frozen visual-anchor bank should be considered only after that split is tested and only with non-eval exemplars.
