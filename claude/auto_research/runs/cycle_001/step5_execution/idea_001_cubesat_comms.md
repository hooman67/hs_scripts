# Execution Plan: High-Bandwidth CubeSat Communication Modules

## 5a. Product Definition

**Core value proposition**: Enable CubeSat operators to downlink data 1000x faster than current solutions using origami-inspired deployable reflectarray antennas — turning $100K CubeSats into capable Earth observation platforms previously requiring $10M+ satellites.

**Key features for MVP (max 3)**:
1. Deployable origami reflectarray antenna module (25x expansion ratio, 18+ dBi gain)
2. Integrated Ka/X-band transceiver achieving 20+ Mbps downlink
3. Standardized CubeSat form factor (3U compatible) with simple deployment mechanism

**What it does NOT do**:
- Not a full satellite bus (we sell the comm module, not the satellite)
- Not ground station infrastructure (partner with existing ground networks like AWS Ground Station, KSAT)
- Not inter-satellite links (focus on ground downlink first)
- Not custom one-off designs (standardized product with limited configuration)

**Success metrics for prototype validation**:
- Successful deployment in thermal-vacuum chamber simulating space conditions
- Achieve 15+ Mbps sustained data rate in ground RF testing
- Survive 100+ deployment/stow cycles without performance degradation
- At least 2 letters of intent from CubeSat operators for flight heritage

---

## 5b. Technical Architecture

**System diagram (components and data flow)**:
```
[Satellite Bus] → [Interface Board] → [SDR Transceiver] → [Feed Network] → [Deployment Mechanism] → [Origami Reflectarray]
                                                                                                           ↓
                                                                                              [Ground Station Rx]
```

**Technology stack**:
- **Reflectarray substrate**: Copper-patterned polyimide film (Kapton-based) — chosen for space heritage, thermal stability, and foldability
- **Deployment mechanism**: Spring-loaded hinges with shape memory alloy (SMA) actuators — reliable, no motors, space-qualified
- **Transceiver**: Software-defined radio (SDR) based on Xilinx Zynq UltraScale+ — flexible frequency selection, FPGA-accelerated modulation
- **Feed antenna**: Patch array feeding the reflectarray — compact, no moving parts
- **Interface**: Standard CubeSat PC/104 connector + CAN bus for commands

**Build vs. Buy decisions**:
| Component | Decision | Rationale |
|-----------|----------|-----------|
| Reflectarray panels | BUILD | Core IP — origami fold pattern + copper element design |
| Deployment mechanism | BUILD | Critical to reliability, must integrate with specific fold geometry |
| SDR transceiver | BUY (modify) | Use existing space-rated SDR boards, customize firmware |
| Interface board | BUILD | Simple but must match specific CubeSat bus standards |
| Ground test equipment | BUY | Standard RF test equipment (VNA, anechoic chamber rental) |

**Key technical risks and mitigation**:
1. **Fold reliability in space**: Mitigate with extensive thermal-vac cycling (50+ cycles at -150°C to +150°C)
2. **Copper fatigue at fold lines**: Mitigate by routing copper traces around (not across) fold lines (validated in OrigamiSat-2)
3. **Antenna pointing accuracy**: Mitigate with ground-in-the-loop tracking + wider beam options for initial product

---

## 5c. Bill of Materials / Resources

### Hardware BOM (per prototype unit)

| Component | Supplier | Unit Cost | Lead Time |
|-----------|----------|-----------|-----------|
| Kapton polyimide film (50μm, Cu-clad) | DuPont / Sheldahl | $2,000 | 4 weeks |
| PCB etching service (flex circuit) | Flexible Circuit Technologies | $5,000 | 3 weeks |
| SMA wire actuators (Nitinol) | Dynalloy / SAES | $500 | 2 weeks |
| Spring hinges (custom) | Custom CNC | $1,500 | 4 weeks |
| SDR module (Xilinx Zynq-based) | Abaco Systems / Xilinx eval board | $8,000 | 6 weeks |
| RF connectors & cabling (space-grade) | SV Microwave | $1,200 | 3 weeks |
| Patch array feed antenna | Custom PCB | $800 | 3 weeks |
| CubeSat structure (3U frame) | Pumpkin Space / ISIS | $4,000 | 4 weeks |
| Deployment sensor suite (microswitches, potentiometers) | Various | $500 | 2 weeks |
| Thermal blankets & coatings | Sheldahl | $1,000 | 3 weeks |
| **Total per prototype** | | **~$25,000** | |

### Software & Services

| Item | Cost | Notes |
|------|------|-------|
| Antenna simulation (HFSS/CST license) | $15,000/yr | Or use open-source OpenEMS for initial design |
| Thermal-vacuum chamber rental | $5,000/day × 10 days | For qualification testing |
| Anechoic chamber RF testing | $3,000/day × 5 days | For antenna pattern validation |
| Vibration testing | $2,000/day × 3 days | Launch vibration qualification |
| FPGA development tools (Vivado) | $3,000/yr | For SDR firmware |

### Personnel (first 12 months)

| Role | Count | Annual Cost | Notes |
|------|-------|-------------|-------|
| RF/Antenna engineer (lead) | 1 | $180,000 | Must have space antenna experience |
| Mechanical engineer (deployment) | 1 | $160,000 | Origami mechanisms, space mechanisms |
| Embedded/FPGA engineer | 1 | $170,000 | SDR firmware, CubeSat bus interface |
| Business/sales (founder) | 1 | $120,000 | Space industry relationships |
| **Total personnel** | 4 | **$630,000** | |

---

## 5d. Build Instructions

### Phase 1: Design & Simulation (Weeks 1-8)

**Step 1**: Reflectarray electromagnetic design (Weeks 1-4)
- Design copper element pattern for target frequency (Ka-band, 26 GHz)
- Simulate in HFSS/CST to optimize gain, bandwidth, and polarization
- Define fold pattern ensuring no copper crosses fold lines
- **Skills**: RF engineering, computational electromagnetics
- **Output**: Verified antenna design files

**Step 2**: Mechanical deployment design (Weeks 2-6)
- Design origami fold geometry (Miura-ori or modified)
- Design spring-hinge mechanism with SMA release
- FEA analysis for deployment forces and structural loads
- **Skills**: Mechanical engineering, origami mathematics
- **Dependency**: Fold pattern from Step 1
- **Output**: CAD files for mechanism, deployment simulation results

**Step 3**: SDR firmware development (Weeks 3-8)
- Configure Zynq SDR for Ka-band operation
- Implement DVB-S2 or custom modulation scheme for 20+ Mbps
- Develop CubeSat bus interface (CAN, I2C commands)
- **Skills**: FPGA/embedded, RF signal processing
- **Output**: Functional SDR firmware

### Phase 2: Prototype Fabrication (Weeks 8-16)

**Step 4**: Manufacture reflectarray panels (Weeks 8-12)
- Order Cu-clad Kapton
- Etch copper elements via flex-circuit PCB process
- Laser-score fold lines (do NOT cut through copper)
- **Lead time**: 4 weeks fabrication
- **Output**: Flat reflectarray panels ready for folding

**Step 5**: Fabricate deployment mechanism (Weeks 9-13)
- CNC hinge components
- Procure SMA actuators and springs
- Assemble mechanism with panels
- Test deployment 50+ times manually
- **Output**: Working mechanical assembly

**Step 6**: Integrate electronics (Weeks 12-16)
- Mount SDR on interface board
- Connect feed antenna
- Wire deployment actuators and sensors
- Functional test (RF output, deployment command, telemetry)
- **Output**: Complete integrated prototype

### Phase 3: Testing & Validation (Weeks 16-24)

**Step 7**: RF performance testing (Weeks 16-18)
- Rent anechoic chamber
- Measure antenna pattern (gain, sidelobes, polarization)
- Verify 20 Mbps link budget
- **Go/no-go**: Must achieve >15 dBi gain and >15 Mbps

**Step 8**: Environmental testing (Weeks 18-22)
- Thermal-vacuum cycling (50 cycles, -150°C to +150°C)
- Vibration testing (launch profiles: Falcon 9, PSLV)
- Deployment testing in vacuum
- **Go/no-go**: Must survive without performance degradation

**Step 9**: End-to-end link demonstration (Weeks 22-24)
- Simulate LEO pass with ground station
- Demonstrate data transfer at predicted rates
- Document results for customer presentations
- **Output**: Test report, marketing materials, customer demos

---

## 5e. Validation Plan

**How to test with real users**:
1. Engage 5-10 CubeSat operators (university programs, startups, government labs) for design feedback during Phase 1
2. Offer first flight unit at cost ($50K vs. list $150K) to 1-2 early customers for in-orbit validation
3. Target a rideshare launch opportunity (SpaceX Transporter, ISRO PSLV) within 6 months of prototype completion

**Minimum sample size**: 2 in-orbit demonstrations (different orbits/conditions)

**Key hypotheses to test**:
1. Deployment mechanism works reliably in actual space conditions (microgravity, thermal cycling)
2. 20 Mbps data rate is achievable over real LEO pass (~10 min window)
3. CubeSat operators will pay $100-200K premium for 1000x data rate improvement
4. Product survives launch vibration without degradation

**Go/no-go criteria**:
- PROCEED: Both orbital demos achieve >10 Mbps sustained, mechanism deploys successfully, 2+ customers place orders
- PIVOT: Good RF performance but deployment issues → simplify mechanism, reduce expansion ratio
- KILL: Fundamental RF performance gap (antenna doesn't work in space as designed) or zero customer interest

---

## 5f. Timeline & Milestones

| Week | Milestone | Decision Point |
|------|-----------|---------------|
| 1-4 | Antenna design complete & simulated | Design review: predicted gain meets spec? |
| 5-8 | Mechanism designed, SDR firmware working | Can we achieve 25x expansion reliably in sim? |
| 9-12 | First panels fabricated | Copper quality on folds acceptable? |
| 13-16 | Integrated prototype assembled | System powers on, deploys, transmits |
| 17-18 | RF testing complete | >15 dBi gain achieved? |
| 19-22 | Environmental testing complete | Survives thermal-vac and vibe? |
| 23-24 | End-to-end demo, customer pitches | Customer LOIs received? |
| 25-30 | Flight unit fabrication | Launch slot booked? |
| 31-40 | In-orbit demonstration | Data rate confirmed in space? |
| 41-52 | First commercial sales | Revenue started? |

---

## 5g. Cost Estimate

| Category | Cost |
|----------|------|
| Personnel (12 months, 4 people) | $630,000 |
| Prototype hardware (3 units) | $75,000 |
| Testing facilities (chamber rental) | $65,000 |
| Software licenses | $20,000 |
| Launch costs (rideshare, 3U) | $150,000 |
| Travel, conferences, customer visits | $40,000 |
| Miscellaneous / contingency (20%) | $196,000 |
| **Total to first flight demonstration** | **~$1.18M** |
| **Total to first revenue (add 6 months)** | **~$1.8M** |

**Monthly burn rate**: ~$70,000

**Funding strategy**: 
- Bootstrap/angel ($200-500K) for Phase 1 (design) + early Phase 2
- Pre-seed/seed ($1-2M) for prototype completion and flight demo
- Series A ($5-10M) after successful orbital demonstration for production scaling

**Revenue model at scale**:
- Flight-qualified modules: $100-200K each
- Annual production (Year 3): 50-100 units = $5-20M revenue
- Gross margin: 60-70% (hardware with significant IP)
