# Execution Plan: Custom Alloy Software Plugin for Metal 3D Printers

## 5a. Product Definition

**Core value proposition**: Turn any existing metal 3D printer into an on-demand alloy creation machine — mix elemental metal powders during printing to create novel high-entropy alloys, gradient compositions, and application-specific materials without buying pre-alloyed feedstock.

**Key features for MVP (max 3)**:
1. Laser path optimization software that generates elliptical stirring patterns for atomic-level powder mixing
2. Library of validated alloy recipes (5-10 compositions with known properties for aerospace/energy applications)
3. Integration plugin for major metal AM platforms (EOS, SLM Solutions, Trumpf, Velo3D)

**What it does NOT do**:
- Not a 3D printer manufacturer (software-only, runs on existing hardware)
- Not a materials testing lab (we provide recipes; customer handles qualification)
- Not a general AM slicing/CAD tool (we add alloy mixing capability to existing workflows)
- Not consulting-only (productized software, not just expertise)

**Success metrics for prototype validation**:
- Produce 3+ novel alloys on a commercial metal printer using our laser paths
- Achieve verified atomic-level mixing (confirmed by EDS/XRD analysis)
- At least 2 paying pilot customers (service bureaus or OEMs)
- Demonstrate one alloy with properties exceeding any commercial pre-alloyed powder

---

## 5b. Technical Architecture

**System diagram**:
```
[Customer CAD File] → [Existing Slicer (EOS EOSPRINT, Materialise)] → [Our Plugin: Alloy Path Generator]
                                                                              ↓
[Printed Part with Custom Alloy] ← [Modified Machine Code with Stirring Patterns] ← [Multi-Powder Feeder Setup]
```

**Technology stack**:
- **Core algorithm**: Elliptical laser path generation (replicating NIST's approach)
  - Parameterized by: alloy composition target, powder bed composition, laser power, scan speed
  - Optimized via computational fluid dynamics (CFD) of melt pool stirring
- **Simulation engine**: OpenFOAM (open-source CFD) for melt pool modeling + thermodynamic databases (CALPHAD/Thermo-Calc) for phase prediction
- **Machine interface**: Post-processors for major AM platforms (each vendor's proprietary build file format)
- **Alloy database**: Recipes stored as parameter sets (composition → laser path → validated properties)
- **Frontend**: Desktop application (Python/Qt or Electron) with cloud-hosted simulation backend (AWS HPC)

**Build vs. Buy**:
| Component | Decision | Rationale |
|-----------|----------|-----------|
| Laser path algorithm | BUILD | Core IP — the stirring patterns are the differentiator |
| CFD simulation | BUY (OpenFOAM) | Open-source, well-validated for melt pool physics |
| Thermodynamic database | BUY (CALPHAD/Thermo-Calc) | Industry standard, $10K/year license |
| Machine post-processors | BUILD | Must reverse-engineer each vendor's format |
| Testing/validation | PARTNER | Use university/national lab beam time for synchrotron verification |
| Cloud compute | BUY (AWS) | Standard HPC instances for simulation runs |

**Key technical risks and mitigation**:
1. **Each printer model behaves differently**: Mitigate by starting with ONE platform (EOS M290 — most common) and expanding
2. **Alloy properties unpredictable**: Mitigate with extensive simulation before physical trials; partner with materials characterization labs
3. **Powder mixing in bed is imprecise**: Mitigate by designing for composition tolerance; use multi-hopper systems where available

---

## 5c. Bill of Materials / Resources

### Software & Licenses (one-time + annual)

| Item | Cost | Notes |
|------|------|-------|
| Thermo-Calc license (academic → commercial) | $15,000/yr | Phase diagram calculations |
| OpenFOAM (open-source) | $0 | CFD simulation engine |
| AWS HPC credits (first year) | $30,000 | GPU instances for simulation |
| EOS EOSPRINT SDK / documentation | $5,000 | For post-processor development |
| Materials database subscription (MatWeb Pro) | $2,000/yr | Reference properties |
| Development tools (IDE, CI/CD) | $2,000/yr | Standard |

### Hardware for Validation (access, not purchase)

| Item | Approach | Cost |
|------|----------|------|
| Metal AM printer (EOS M290) | University partnership or service bureau rental | $50-100/hr print time; ~$50K total for R&D prints |
| Materials characterization (SEM/EDS, XRD) | University lab access | $200-500/hr; ~$20K total |
| Mechanical testing (tensile, hardness) | Commercial test lab | $500-2000/sample set; ~$15K total |
| Synchrotron beam time (optional) | Apply to Argonne APS user program | $0 (if accepted) or $5K/day |

### Personnel (first 12 months)

| Role | Count | Annual Cost | Notes |
|------|-------|-------------|-------|
| Computational metallurgist (PhD, lead) | 1 | $180,000 | Must understand CALPHAD + melt pool physics |
| AM process engineer | 1 | $160,000 | Experience with EOS/SLM machines and build parameter development |
| Software engineer (systems) | 1 | $170,000 | Post-processor development, desktop app, cloud backend |
| CEO/technical BD | 1 | $140,000 | Aerospace/AM industry relationships |
| **Total personnel** | 4 | **$650,000** | |

---

## 5d. Build Instructions

### Phase 1: Algorithm Development & Simulation (Weeks 1-12)

**Step 1**: Replicate NIST results in simulation (Weeks 1-4)
- Implement elliptical laser path generator in Python
- Set up OpenFOAM melt pool simulation matching NIST parameters
- Validate: simulation shows atomic mixing for known NIST compositions
- **Output**: Working simulation pipeline that predicts alloy mixing

**Step 2**: Optimize for commercial printers (Weeks 4-8)
- Adapt laser paths for EOS M290 constraints (power, speed, spot size)
- Account for real powder bed characteristics (layer thickness, particle distribution)
- Run parameter sweeps to map: composition → optimal path parameters
- **Output**: Optimized path library for EOS M290 platform

**Step 3**: Design 5 target alloys (Weeks 6-12)
- Use Thermo-Calc to identify promising high-entropy compositions for:
  - High-temperature aerospace (CoCrFeNiMn variants)
  - Corrosion-resistant marine/chemical (AlCoCrFeNi variants)
  - Radiation-hardened nuclear (HfNbTaTiZr variants)
  - Tool steel alternatives (multiple principal elements)
  - Biomedical (TiNbZrMo — non-toxic, bone-matching modulus)
- Predict phase stability, mechanical properties, printability
- **Output**: 5 alloy recipes with predicted properties ready for physical validation

### Phase 2: Physical Validation (Weeks 10-20)

**Step 4**: Print test coupons on EOS M290 (Weeks 10-14)
- Partner with university AM lab or service bureau
- Print small test coupons (10mm cubes) using our laser paths with mixed powders
- 5 alloys × 3 parameter variations = 15 builds
- **Cost**: ~$30K in machine time + powders
- **Output**: Physical samples for characterization

**Step 5**: Characterize alloy properties (Weeks 14-18)
- SEM/EDS mapping to verify compositional homogeneity
- XRD to confirm crystal structure matches prediction
- Tensile testing, hardness, corrosion testing
- **Go/no-go**: Do ≥3/5 alloys match predicted properties within 20%?
- **Output**: Validated alloy recipes with measured properties

**Step 6**: Build post-processor for EOS (Weeks 12-18, parallel)
- Reverse-engineer EOSPRINT build file format
- Implement custom laser path injection
- Test on machine: verify paths execute as designed
- **Output**: Working plugin that modifies EOS build files

### Phase 3: Product & Customers (Weeks 18-30)

**Step 7**: Package into desktop application (Weeks 18-22)
- User selects target alloy from library
- Software generates modified build file with stirring paths
- Include simulation preview (predicted mixing quality)
- License management (per-machine annual subscription)
- **Output**: Installable software product

**Step 8**: Pilot customers (Weeks 20-26)
- Engage 3-5 metal AM service bureaus and aerospace companies
- Free pilot program (3 months) in exchange for:
  - Printing our recipes on their machines
  - Sharing characterization results
  - Providing feedback on workflow integration
- **Output**: 3+ pilot deployments with validated results

**Step 9**: Commercial launch (Weeks 26-30)
- Convert pilots to paid subscriptions
- Publish case studies with pilot results
- Present at RAPID + TCT (AM industry conferences)
- **Output**: Revenue, pipeline, market presence

---

## 5e. Validation Plan

**How to test with real users**:
1. Partner with 2-3 AM service bureaus during Phase 2 (they provide machine time; we provide novel capability)
2. Target aerospace R&D teams at Boeing/Airbus/GE who are already exploring novel alloys
3. Academic partnerships with metallurgy departments for validation and publication

**Minimum sample size**:
- 5 alloys validated with measured properties matching predictions
- 3 different printer installations (confirm portability)
- 2 customer applications where our alloy outperforms commercial alternatives

**Key hypotheses to test**:
1. Elliptical laser stirring works on commercial EOS machines (not just lab setups)
2. Mixed-powder alloys achieve properties comparable to pre-alloyed feedstock
3. Service bureaus will adopt new workflow if it unlocks premium pricing for customers
4. Aerospace OEMs will pay $50-100K/year for novel material capability

**Go/no-go**:
- PROCEED: 3+ alloys validated, 2+ pilot customers converting to paid
- PIVOT: If mixing works but properties underwhelm → focus on gradient compositions instead of novel alloys
- KILL: If mixing doesn't work on commercial machines (fundamental incompatibility)

---

## 5f. Timeline & Milestones

| Week | Milestone |
|------|-----------|
| 1-4 | Simulation replicates NIST mixing results |
| 5-8 | Optimized paths for EOS M290 |
| 9-12 | 5 alloy recipes designed with predicted properties |
| 10-14 | First physical prints on commercial machine |
| 14-18 | Characterization confirms ≥3 alloys work |
| 18-22 | Desktop software product packaged |
| 20-26 | 3+ pilot customers running software |
| 26-30 | Commercial launch, first revenue |

---

## 5g. Cost Estimate

| Category | Cost |
|----------|------|
| Personnel (12 months, 4 people) | $650,000 |
| Print time for validation (~500 hours) | $50,000 |
| Materials characterization | $35,000 |
| Metal powders (elemental, 10+ types) | $15,000 |
| Software licenses | $25,000 |
| Cloud compute (simulation) | $30,000 |
| Conferences, travel, BD | $30,000 |
| Legal (IP filing) | $25,000 |
| Contingency (15%) | $130,000 |
| **Total to commercial launch** | **~$990K** |

**Monthly burn rate**: ~$65,000

**Funding strategy**:
- Pre-seed/angel ($500K-1M): Covers through physical validation
- Seed ($3-5M): After pilot customers validate, scale to more printer platforms + more alloys
- Revenue by Month 7-8 (pilot fees), meaningful by Month 12

**Revenue model at scale**:
- Per-machine license: $50-100K/year (300+ service bureaus worldwide = $15-30M potential)
- Alloy recipe marketplace: $5-20K per custom alloy recipe
- Consulting: $200-500K per custom alloy development project
- Year 3 target: $5-10M ARR
