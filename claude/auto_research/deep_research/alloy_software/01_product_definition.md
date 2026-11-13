# 01 Product Definition: Custom Alloy Software Plugin for Metal 3D Printers

## Problem Statement

**Who has the problem:** Metal additive manufacturing (AM) service bureaus (approximately 300-400 worldwide) and aerospace/defense OEMs with in-house metal printers. Specific personas: AM process engineers and materials engineers at these organizations.

**How painful it is:** MODERATE. Today, service bureaus are limited to printing with pre-alloyed powders (IN718, Ti-6Al-4V, SS316L, AlSi10Mg) available from a handful of powder suppliers (Carpenter Additive, AP&C, Sandvik). When a customer needs a novel alloy composition (e.g., for extreme corrosion resistance, radiation hardening, or high-temperature aerospace), the bureau must either:
1. Commission custom pre-alloyed powder atomization ($50K-150K, 3-6 month lead time, 50kg minimum order), or
2. Decline the job entirely.

This is NOT a daily pain point. Most service bureau revenue comes from standard alloys. The pain emerges for maybe 5-15% of RFQs involving advanced applications -- primarily aerospace R&D, nuclear, and specialty medical devices.

**What they do today:** Decline non-standard alloy jobs, refer customers to research labs, or (rarely) manually attempt powder blending with no software optimization -- resulting in inconsistent mixing and unreliable properties.

## Product Scope v1 (3 Features Maximum)

### Feature 1: Elliptical Laser Path Generator
Software that takes a target alloy composition (e.g., CoCrFeNiMn equiatomic) and generates optimized elliptical/oscillating laser scan strategies that create convective stirring in the melt pool to homogeneously mix elemental powders. Outputs a modified build file for the target printer platform.

### Feature 2: Alloy Recipe Library (5-10 Validated Compositions)
Pre-validated recipes for specific high-entropy alloy compositions, each containing: required elemental powder blend ratios, laser parameters (power, speed, hatch spacing), stirring pattern parameters, expected mechanical properties with tolerances. Initially validated on EOS M290 only.

### Feature 3: Melt Pool Simulation Preview
Before committing to a print, users run a quick thermal/CFD simulation showing predicted mixing quality for their specific geometry and parameters. Provides confidence score (predicted composition homogeneity).

### What It Does NOT Do
- Does NOT design new alloy compositions (users select from the library or input known targets)
- Does NOT handle powder feeding/dispensing hardware (assumes pre-mixed powder bed or manual multi-powder setup)
- Does NOT replace the existing slicer (runs as post-processor on existing build files)
- Does NOT provide materials qualification/certification services
- Does NOT support non-laser PBF processes (no electron beam, no binder jet, no DED)

## User Workflow (Day 1)

1. **Install plugin** on workstation alongside EOSPRINT (or equivalent slicer). Enter license key.
2. **Open existing build file** -- the part is already sliced with standard parameters.
3. **Select target alloy** from recipe library (e.g., "CoCrFeNiMn-01 - Cantor Alloy").
4. **Configure powder setup** -- specify which elemental powders are loaded in the machine's powder supply (Co, Cr, Fe, Ni, Mn at specified mesh sizes).
5. **Generate modified build file** -- software replaces standard raster scan patterns with elliptical stirring patterns. Adjusts power/speed to maintain proper energy density while achieving mixing.
6. **Run simulation preview** (optional, 5-15 minutes) -- see predicted composition map, homogeneity score, thermal history.
7. **Export modified build file** to printer. Load mixed elemental powder into machine.
8. **Print.** Post-print: characterize sample to verify composition meets target.

## Pricing Model

| Tier | Price | Justification |
|------|-------|---------------|
| Base License (1 printer) | $60,000/year | Unlocks 50+ new alloy possibilities per machine. If bureau charges $5K premium per novel-alloy job and wins 15 jobs/year, that is $75K incremental revenue. ROI positive in year 1. |
| Additional printer | $30,000/year | Lower marginal cost since same recipes apply. |
| Custom recipe development | $15,000 per alloy | Covers simulation + validation consulting. |
| Simulation compute (cloud) | Usage-based, ~$500/month typical | Passes through AWS HPC costs at 3x markup. |

**Justification:** Metal AM service bureaus operate printers that cost $500K-1.5M each. A $60K/year software license is 4-12% of machine cost -- similar to what they already pay for monitoring software (Sigma Additive Solutions: ~$50K/yr), simulation tools (Ansys AM: $40-80K/yr), or quality assurance software (Velo3D Assure: included with $1.5M machine). The key justification is that this software enables NEW revenue streams (novel alloy jobs) rather than just optimizing existing ones.

## Ideal First Customer Profile

**Company type:** Mid-size metal AM service bureau (5-20 printers) with R&D orientation and aerospace/defense customers.

**Specific attributes:**
- Owns 2+ EOS M290 or M400 systems (our first supported platform)
- Already does parameter development for customers (not just running certified recipes)
- Has in-house metallurgist or materials engineer on staff
- Located near characterization facilities (university partnership or in-house SEM/XRD)
- Serves aerospace R&D customers (Boeing Research, NASA, Lockheed Skunk Works) who request novel materials
- Revenue $5-20M/year (large enough to invest in new capability, small enough to be accessible)

**Example organizations (specific):**
- Sintavia (Hollywood, FL) -- defense/aerospace focused, known for novel alloy qualification
- Morf3D (El Segundo, CA) -- Boeing HorizonX backed, aerospace AM specialist
- Beehive Industries (Knoxville, TN) -- defense/propulsion focused, aggressive growth
- Materialise Metal (Leuven, Belgium) -- R&D oriented, global reach
- Rosswag Engineering (Pfinztal, Germany) -- known for custom alloy AM development
