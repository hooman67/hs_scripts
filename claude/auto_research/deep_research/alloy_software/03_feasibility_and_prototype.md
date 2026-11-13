# 03 Feasibility & Prototype Plan: Custom Alloy Software Plugin for Metal 3D Printers

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER WORKSTATION                              │
│                                                                   │
│  ┌──────────┐    ┌──────────────────┐    ┌──────────────────┐   │
│  │ EOSPRINT │───▶│  ALLOY PLUGIN    │───▶│ Modified Build   │   │
│  │ (Slicer) │    │  (Post-Processor)│    │ File (.sli/.opj) │   │
│  └──────────┘    └────────┬─────────┘    └──────────────────┘   │
│                           │                                       │
│                           │ API calls                             │
└───────────────────────────┼───────────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────────┐
│                     CLOUD BACKEND (AWS)                            │
│                                                                   │
│  ┌────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │ OpenFOAM CFD   │  │ Thermo-Calc      │  │ Recipe Database  │ │
│  │ (Melt Pool Sim)│  │ (Phase Diagrams) │  │ (Validated Alloys│ │
│  │ [HPC Instances]│  │ [Licensed Server]│  │  + Parameters)   │ │
│  └────────────────┘  └──────────────────┘  └──────────────────┘ │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │              CORE ENGINE                                     │ │
│  │  • Elliptical path generator (Python/Cython)               │ │
│  │  • Parameter optimizer (Bayesian optimization)             │ │
│  │  • Build file encoder/decoder (per-platform)               │ │
│  └────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
```

## Bill of Materials

### Software & Licenses

| Item | Cost/Year | Confidence | Notes |
|------|-----------|------------|-------|
| Thermo-Calc SDK license (commercial) | $15,000 | VERIFIED (public pricing page lists "from EUR 12,000") | Programmatic API access for phase calculations |
| OpenFOAM | $0 | VERIFIED | Open-source GPLv3. Custom solvers needed for melt pool. |
| AWS EC2 HPC (c5.18xlarge or p3.2xlarge) | $30,000 | ASSUMED (based on ~500 simulation hours at $40-60/hr) | For CFD simulation runs |
| EOS EOSPRINT documentation/SDK | $5,000-15,000 | UNVERIFIED -- EOS does not publicly list SDK pricing. May require partnership agreement. | Critical dependency. |
| MatWeb Pro database subscription | $2,395/year | VERIFIED (public pricing) | Materials property reference |
| Python ecosystem (NumPy, SciPy, etc.) | $0 | VERIFIED | Open-source |
| Desktop GUI framework (Qt/PySide6) | $0 (LGPL) or $5,500/yr (commercial) | VERIFIED | PySide6 is LGPL; Qt commercial if needed |
| CI/CD, cloud infrastructure (misc.) | $3,000 | ASSUMED | Standard DevOps tooling |

### Hardware for Validation (Access, Not Purchase)

| Item | Cost | Confidence | Notes |
|------|------|------------|-------|
| EOS M290 print time (500 hours) | $50,000-75,000 | ASSUMED ($100-150/hr typical service bureau rate) | For validating alloy recipes. Must negotiate research rate. |
| Elemental metal powders (Co, Cr, Fe, Ni, Mn, Al, Ti, Nb, Zr, Mo) | $15,000 | ASSUMED (research-grade powders $100-500/kg, need ~50kg total) | Must be gas-atomized, correct PSD (15-45 micron) |
| SEM/EDS characterization | $12,000 | ASSUMED ($200-400/hr, ~40 hours total) | Composition mapping |
| XRD analysis | $5,000 | ASSUMED ($150-300/hr, ~20 hours) | Phase identification |
| Mechanical testing (tensile, hardness) | $15,000 | ASSUMED ($500-2000 per sample set, 15 sets) | Property validation |
| Synchrotron beam time (Argonne APS) | $0 (if user proposal accepted) or $5,000-10,000/day | UNVERIFIED | Optional but extremely valuable for in-situ observation |

### Personnel (12 Months)

| Role | Salary | Confidence | Critical Skills |
|------|--------|------------|-----------------|
| Computational Metallurgist (PhD, Lead) | $180,000 | ASSUMED (Bay Area PhD-level) | CALPHAD, thermodynamics, melt pool physics, HEA expertise |
| AM Process Engineer | $160,000 | ASSUMED | EOS machine operation, build parameter development, materials characterization |
| Software Engineer (Systems) | $170,000 | ASSUMED | Build file reverse-engineering, desktop app, cloud backend, Python/C++ |
| Technical CEO / BD | $140,000 | ASSUMED | Aerospace/AM industry relationships, fundraising |
| **Total Personnel** | **$650,000** | | |

### Total Cost Summary

| Category | Cost |
|----------|------|
| Personnel (12 months) | $650,000 |
| Print time validation | $62,500 |
| Materials characterization | $32,000 |
| Metal powders | $15,000 |
| Software licenses | $55,000 |
| Cloud compute | $30,000 |
| Conferences/travel/BD | $30,000 |
| Legal (patent filing) | $25,000 |
| Contingency (15%) | $135,000 |
| **TOTAL** | **~$990,000** |

## Software Stack with Licenses

| Layer | Technology | License | Cost |
|-------|------------|---------|------|
| Core algorithm | Python 3.11+ / Cython / NumPy | BSD/MIT | Free |
| CFD simulation | OpenFOAM v11+ | GPLv3 | Free (must open-source modifications to solver) |
| Thermodynamic calc | Thermo-Calc TC-Python SDK | Commercial | $15K/yr |
| Optimization | BoTorch (Bayesian optimization) | MIT | Free |
| Desktop GUI | PySide6 (Qt) | LGPLv3 | Free |
| Build file I/O | Custom (reverse-engineered) | Proprietary | N/A |
| Cloud backend | FastAPI + Celery + Redis | MIT/BSD | Free |
| Database | PostgreSQL | PostgreSQL License | Free |
| HPC orchestration | AWS ParallelCluster | Apache 2.0 | Free (pay for compute) |

## Step-by-Step Build Instructions for First Prototype

### Phase 0: Foundation (Weeks 1-4)

**Step 1: Replicate NIST Melt Pool Mixing in Simulation**
- Literature review: Collect all NIST AM-Bench publications on multi-material mixing (key papers: Lane et al. 2020, Heigel et al. 2021).
- Set up OpenFOAM with custom solver for two-phase melt pool with Marangoni convection.
- Implement elliptical laser path as heat source boundary condition.
- Validate: simulation of single-track melt pool with two metals shows mixing comparable to NIST measurements.
- **Deliverable:** Working melt pool simulation that demonstrates stirring effect.
- **Go/No-Go:** Does elliptical path produce measurably better mixing than linear raster in simulation? If <10% improvement, KILL.

**Step 2: Characterize EOS M290 Constraints**
- Obtain EOS M290 technical specifications (max scan speed, power, spot size, minimum feature size for scan strategy).
- Map elliptical path parameters to machine-achievable values (key constraint: M290 scanner has finite repositioning speed -- cannot do arbitrary curves).
- Determine if M290 galvanometer system can execute elliptical patterns at required speeds.
- **Deliverable:** Feasibility assessment of stirring patterns on M290 hardware.
- **CRITICAL RISK:** If M290 scanner cannot execute elliptical paths at required speeds/accelerations, the entire concept fails on commercial machines.

### Phase 1: Algorithm Development (Weeks 5-12)

**Step 3: Build Elliptical Path Generator**
- Implement parameterized path generation: inputs (composition target, powder blend, layer thickness) -> outputs (laser path coordinates, power profile, timing).
- Optimize via Bayesian search over simulation: maximize predicted mixing homogeneity.
- Generate parameter lookup tables for 5 target alloy compositions.
- **Deliverable:** Python module that generates optimized stirring paths.

**Step 4: Build EOS Build File Post-Processor**
- Reverse-engineer EOS .sli build file format (binary format, partially documented in academic literature -- Catchpole-Smith et al. 2017 provides some structure).
- Implement reader/writer that can modify scan vectors within existing build files.
- Replace standard raster vectors with elliptical stirring vectors for specified layers/regions.
- **Deliverable:** Working post-processor that outputs modified .sli files.
- **CRITICAL RISK:** EOS build file format is proprietary. Reverse-engineering may violate EULA. Format may change between firmware versions.

### Phase 2: Physical Validation (Weeks 10-20)

**Step 5: First Physical Prints**
- Partner with university AM lab or service bureau (ideally one with EOS M290 and materials characterization).
- Print single-track experiments first (individual laser tracks on powder bed of mixed elements).
- Characterize cross-sections via SEM/EDS for mixing quality.
- Then print small cubes (10mm) with full stirring strategy.
- **Cost:** ~$30K for this phase.
- **Deliverable:** Physical evidence that stirring patterns improve mixing on commercial hardware.
- **Go/No-Go:** Does physical mixing match simulation predictions within 30%? If yes, proceed. If mixing is fundamentally worse than simulated, PIVOT or KILL.

**Step 6: Alloy Property Validation**
- Print 5 alloy compositions as test coupons (tensile bars, cubes for hardness).
- Full characterization: composition (EDS), phase (XRD), mechanical (tensile, hardness, corrosion).
- Compare to literature values for same compositions made via arc melting or pre-alloyed powder.
- **Deliverable:** Property data for 5 HEAs printed with stirring approach.
- **Go/No-Go:** Do >= 3 alloys achieve >80% of literature-reported properties? If not, concept has fundamental materials science limitations.

### Phase 3: Productization (Weeks 18-26)

**Step 7: Desktop Application**
- Build GUI around path generator + post-processor.
- Recipe selection, parameter preview, simulation launch, build file export.
- License management (hardware-locked, annual subscription).
- **Deliverable:** Installable desktop application.

**Step 8: Pilot Deployment**
- Identify 3-5 beta customers (service bureaus with EOS M290).
- Free pilot (3 months) in exchange for printing validation, feedback, testimonials.
- **Deliverable:** Real-world validation on customer machines.

## Risk Register

| # | Risk | Likelihood | Impact | Mitigation | Fallback |
|---|------|-----------|--------|------------|----------|
| R1 | EOS scanner cannot execute elliptical paths at required speed/precision | MEDIUM (40%) | CRITICAL -- kills concept | Early feasibility test (Week 2). Contact EOS applications engineers. | Pivot to modified raster strategies (less optimal but machine-compatible) |
| R2 | Build file reverse-engineering violates EULA / EOS blocks access | HIGH (60%) | HIGH -- no path to market without OEM cooperation | Approach EOS partnership early. Use open-architecture machines (Aconity) for validation. | Pivot to open-architecture printers only (much smaller market) |
| R3 | Physical mixing quality far worse than simulation predicts | MEDIUM (35%) | HIGH -- invalidates core premise | Use conservative simulation assumptions. Early single-track experiments (Week 10). | Pivot to gradient composition (less mixing needed) or multi-pass strategies |
| R4 | Cannot hire computational metallurgist at $180K in Bay Area | MEDIUM (40%) | HIGH -- no technical leadership | Recruit from national labs (NIST, ORNL, Sandia). Offer equity. Consider non-Bay Area HQ. | Consulting arrangement with university professor + postdoc hire |
| R5 | Alloy properties disappointing vs. pre-alloyed equivalents | MEDIUM (45%) | MEDIUM -- limits value proposition | Target compositions where NO pre-alloyed powder exists (true HEAs). | Position as "rapid prototyping for alloy development" not "production alloy replacement" |
| R6 | OEM builds competing feature within 18 months | LOW-MEDIUM (25%) | CRITICAL -- destroys business | Build recipe library moat (validated alloys). Seek exclusive OEM partnership. | Pivot to alloy design consulting using the simulation tools built |
| R7 | Service bureaus unwilling to adopt (risk-averse) | MEDIUM-HIGH (50%) | HIGH -- no revenue | Target R&D-focused bureaus first. Offer guaranteed results or money back. | Pivot to selling directly to aerospace OEM R&D labs |
| R8 | OpenFOAM modifications must be open-sourced (GPLv3) | HIGH (80%) | MEDIUM -- reveals technical approach | Architect so core IP (path generation) is separate from OpenFOAM solver. Use OpenFOAM only for offline validation. | License commercial CFD (FLOW-3D or COMSOL, $50-100K/yr) |

## Validation Plan

### Success Criteria

| Criterion | Threshold | How to Test |
|-----------|-----------|-------------|
| Mixing homogeneity | <5% composition variation across printed volume (EDS mapping) | Print 10mm cubes, section, map composition |
| Property achievement | >80% of arc-melted reference for yield strength and hardness | Standard ASTM tensile and hardness testing |
| Machine compatibility | Build file executes without error on EOS M290 | Run on actual machine (partner lab) |
| Simulation accuracy | Predicted vs. actual composition within 30% | Compare simulation predictions to EDS measurements |
| Customer willingness to pay | 2+ service bureaus sign LOI at $50K+/year | Customer discovery interviews + pilot program |
| Build time overhead | <20% increase vs. standard raster scan for same geometry | Time comparison on same part geometry |

### Timeline

| Month | Validation Milestone |
|-------|---------------------|
| 1-2 | Simulation proves stirring concept (computational only) |
| 3 | EOS M290 feasibility confirmed (scanner can execute paths) |
| 4-5 | First physical prints show mixing improvement |
| 5-6 | Property data confirms 3+ alloys meet targets |
| 6-7 | Working desktop plugin deployed to 1 beta site |
| 7-9 | 3+ pilot customers running software on their machines |
| 9-10 | First revenue (pilot conversions to paid) |

## Total Cost and Time Estimate

- **Total capital required:** $990,000
- **Time to first revenue:** 9-10 months (optimistic) / 14-16 months (realistic with delays)
- **Monthly burn rate:** $65,000 (4 FTEs + overhead)
- **Runway at $990K:** ~15 months
- **Break-even:** Requires 10 customers at $60K/year = $600K ARR (unlikely before month 18-24)

## Founder-Market Fit Assessment

**Founder profile:** Hooman Shariati -- AI/ML infrastructure engineering manager at Adobe. Deep Python/systems/cloud expertise. No hardware background. No metal AM industry connections. No materials science training.

| Dimension | Fit Score (1-10) | Notes |
|-----------|-----------------|-------|
| Technical skills (software) | 7/10 | Strong Python, cloud, systems. Can build the software layer. |
| Technical skills (domain) | 2/10 | No metallurgy, no CALPHAD, no AM process knowledge. Must hire ALL domain expertise. |
| Industry connections | 1/10 | No relationships with service bureaus, OEMs, or materials researchers. Cold start. |
| Hardware/physical product | 1/10 | No experience with physical validation, lab work, or manufacturing. |
| Fundraising for deep-tech | 4/10 | Adobe brand recognition helps, but deep-tech AM investors are a specialized community. |
| Team building (domain PhDs) | 3/10 | Recruiting metallurgy PhDs from outside the field is extremely difficult. They prefer national labs or established companies. |
| Sales to industrial customers | 3/10 | Enterprise SW sales at Adobe is different from selling to 10-person service bureaus. |
| **Overall Founder-Market Fit** | **3/10** | **Severe mismatch.** This is a materials science company that happens to use software. The founder has the software skills but none of the domain expertise, industry access, or physical science background required. |

**Critical gap:** The founder would be entirely dependent on hired domain experts (the computational metallurgist and AM process engineer) for all technical decisions. In a 4-person startup, if the founder cannot evaluate the core technology, they cannot lead effectively.
