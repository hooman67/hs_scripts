# 01 - Product Definition: TEG Design-as-a-Service

## Problem Statement

**Who:** Mechanical and thermal engineers at industrial companies (cement, steel, glass, oil & gas), automotive OEMs, aerospace contractors, and remote power system integrators who need custom thermoelectric generator designs for waste heat recovery applications.

**How painful:** Currently, designing a TEG system for a specific waste heat source requires 3-6 months of iterative simulation work using COMSOL Multiphysics ($25K-$50K/year license), deep expertise in thermoelectric material science, and trial-and-error optimization of geometry, material selection, and thermal interface design. Most companies lack in-house TE expertise. The few consultants available (e.g., Applied Thermoelectric Solutions) offer traditional physics-based approaches without ML-accelerated optimization.

**What they do today:**
1. Hire a specialized thermoelectric PhD consultant ($200-$400/hr) for 3-6 months
2. License COMSOL + build custom models internally (requires 6-12 months ramp-up)
3. Use rule-of-thumb calculations and off-the-shelf TEG modules (suboptimal performance, 30-50% efficiency loss vs. optimized design)
4. Abandon the project entirely due to cost/time barriers

**Pain intensity: MODERATE.** This is a real pain but affects a small number of buyers per year globally (estimated 50-200 design projects/year worldwide). Most waste heat goes unrecovered not because design is hard, but because TEG economics (5-8% efficiency) make ROI marginal for many applications.

## Product Scope v1 (Maximum 3 Features)

**Feature 1: Intake Specification Portal**
- Web form where customer inputs: heat source temperature, cold side temperature, available surface area, target power output, operating environment constraints (vibration, corrosion, space)
- Outputs a feasibility assessment within 24 hours (go/no-go with estimated performance range)

**Feature 2: AI-Optimized TEG Design Package**
- TEGNet-powered material selection and geometry optimization
- COMSOL-validated thermal/electrical simulation results
- Parametric CAD files (STEP format) ready for manufacturer quoting
- Delivered in 5 business days

**Feature 3: Design Report with Manufacturing Specs**
- Full engineering report: material specifications, dimensional tolerances, thermal interface requirements, expected power output curves across operating range
- Bill of materials with suggested suppliers (e.g., Marlow Industries, II-VI/Coherent for TE materials)
- Integration guidelines for customer's thermal system

**What it does NOT do:**
- Does NOT manufacture or sell TEG hardware
- Does NOT provide ongoing monitoring/maintenance services
- Does NOT guarantee performance (design only, no warranty on built systems)
- Does NOT handle system integration (heat exchangers, power conditioning, mounting)
- Does NOT offer sub-$10K projects (minimum engagement is $15K)

## User Workflow (Day 1)

1. Customer visits website, fills out "Project Inquiry" form (10-15 fields: temperatures, surface area, power target, environment, timeline, budget range)
2. Within 4 hours: automated feasibility pre-screen using TEGNet inference (is this thermodynamically viable? What ZT materials could work?)
3. Within 24 hours: founder reviews, sends customer a "Feasibility Brief" (2-page PDF) with go/no-go recommendation and rough cost estimate
4. If GO: customer signs engagement letter ($15K-$50K fixed fee, 50% upfront)
5. Days 1-2: Detailed thermal boundary condition modeling, TEGNet optimization runs (material selection, leg geometry, fill factor, number of couples)
6. Days 3-4: COMSOL validation simulation, parametric CAD generation
7. Day 5: Delivery of Design Package (CAD files, simulation report, manufacturing specs, supplier recommendations)
8. Optional: 2-hour review call to walk through design and answer questions

## Pricing Model

| Tier | Price | Scope | Justification |
|------|-------|-------|---------------|
| Feasibility Study | $3,000 | Go/no-go assessment, material screening, estimated performance | Low barrier entry; covers ~4 hours of expert time + compute |
| Standard Design | $15,000 | Single operating point optimization, CAD, simulation report | Comparable to 1-2 weeks of PhD consultant time at $300/hr |
| Premium Design | $35,000 | Multi-point optimization (variable heat source), sensitivity analysis, 3 design iterations | Replaces 2-3 months of traditional consulting |
| Enterprise | $50,000+ | Multi-module system design, custom material recommendations, ongoing support | Large automotive/aerospace programs |

**Justification:** Traditional TEG design consulting runs $60K-$180K for a 3-6 month engagement. Pricing at $15K-$50K with 5-day delivery offers 70-80% cost reduction AND 90%+ time reduction. The value prop is clear even if the customer is skeptical of AI.

## Ideal First Customer Profile

**Company type:** Mid-size industrial equipment manufacturer (500-5000 employees) with an active R&D program exploring waste heat recovery for ESG/sustainability goals.

**Specific profile:**
- VP of Engineering or Director of R&D at a cement, glass, or steel company
- Has budget authority for $15-50K engineering services without board approval
- Currently in "exploration phase" - has identified waste heat sources but hasn't committed to a recovery technology
- Located in US, Germany, or Japan (strongest TEG adoption markets)
- Has tried to get quotes from traditional consultants and been frustrated by 6-month timelines

**Example companies:** Holcim (cement), Corning (glass), Nucor (steel), Cummins (diesel engines), Caterpillar (heavy equipment)
