# 03 - Feasibility & Prototype Plan: TEG Design-as-a-Service

## Architecture Overview

```
[Customer Web Portal] --> [Intake Form / API]
        |
        v
[Feasibility Engine]
  - TEGNet inference (material selection, performance prediction)
  - Boundary condition validation
  - Automated go/no-go assessment
        |
        v
[Optimization Pipeline]
  - TEGNet multi-objective optimization (geometry, materials, fill factor)
  - COMSOL LiveLink automation (thermal/electrical FEA validation)
  - Parametric CAD generation (CadQuery/FreeCAD)
        |
        v
[Report Generator]
  - LaTeX/PDF engineering report
  - STEP file export
  - Manufacturing specifications
        |
        v
[Delivery Portal] --> Customer downloads package
```

**Infrastructure:** Single cloud VM (AWS/GCP) for web portal + TEGNet inference. COMSOL runs on a dedicated workstation (license requirement). CAD generation is CPU-only.

## Bill of Materials

### Software & Licenses

| Item | Cost | Frequency | Confidence |
|------|------|-----------|------------|
| COMSOL Multiphysics + Heat Transfer Module | $7,195 | Annual license | VERIFIED (comsol.com academic pricing varies; commercial single-seat ~$7K base + $2K-$4K per module) |
| COMSOL Heat Transfer Module add-on | $3,000 | Annual | ASSUMED (module pricing not publicly listed; range $2K-$4K) |
| COMSOL LiveLink for MATLAB | $1,500 | Annual | ASSUMED |
| AWS EC2 (t3.xlarge for web + inference) | $125/mo = $1,500 | Annual | VERIFIED |
| Domain + SSL + Email (Google Workspace) | $150 | Annual | VERIFIED |
| GitHub Pro (private repos, CI/CD) | $48 | Annual | VERIFIED |
| CadQuery (open source) | $0 | - | VERIFIED |
| TEGNet (Apache-2.0, open source) | $0 | - | VERIFIED |
| Python ecosystem (NumPy, PyTorch, FastAPI) | $0 | - | VERIFIED |

### Hardware

| Item | Cost | Confidence |
|------|------|------------|
| Workstation for COMSOL (Dell Precision 3680, 64GB RAM, i9) | $3,500 | VERIFIED (dell.com) |
| Monitor + peripherals | $500 | ASSUMED |

### Services & Marketing

| Item | Cost | Confidence |
|------|------|------------|
| Website design (Webflow or custom) | $2,000 | ASSUMED |
| Logo + branding | $500 | ASSUMED |
| Technical content marketing (10 blog posts) | $3,000 | ASSUMED (freelance technical writer) |
| Conference attendance (1 event: Thermoelectrics conference) | $3,000 | ASSUMED (registration + travel) |
| Legal (LLC formation, terms of service, engagement contract template) | $2,500 | ASSUMED |
| Professional liability insurance (E&O) | $2,000 | ASSUMED (annual) |

### Total Startup Cost

| Category | Cost |
|----------|------|
| Software licenses (Year 1) | $13,393 |
| Hardware | $4,000 |
| Services & Marketing | $13,000 |
| Operating runway (6 months living expenses, assuming side project initially) | $0 |
| **TOTAL** | **$30,393** |

**Note:** The $171K capital estimate in the original idea description appears inflated. This can realistically be launched for $30-40K. The $171K figure may include salary replacement / 12-month runway, which is reasonable for full-time commitment.

## Software Stack

| Layer | Technology | License | Notes |
|-------|-----------|---------|-------|
| Frontend | Next.js + Tailwind | MIT | Customer portal |
| Backend API | FastAPI (Python) | MIT | Intake, job management |
| ML Inference | PyTorch + TEGNet | Apache-2.0 | Material/geometry optimization |
| Simulation | COMSOL Multiphysics | Commercial ($7K+/yr) | FEA validation |
| Automation | COMSOL LiveLink for Python/MATLAB | Commercial (add-on) | Scripted simulation |
| CAD | CadQuery | Apache-2.0 | Parametric STEP generation |
| Reports | LaTeX + Jinja templates | Free | PDF engineering reports |
| Database | PostgreSQL | PostgreSQL License | Project/customer data |
| Hosting | AWS (EC2 + S3 + RDS) | Pay-as-you-go | Infrastructure |
| Auth/Payments | Stripe + Auth0 | SaaS pricing | Billing |

## Step-by-Step Build Instructions (Prototype)

### Phase 1: Core Pipeline (Weeks 1-3)

**Week 1: TEGNet Integration**
1. Clone TEGNet repository from GitHub
2. Set up Python environment (PyTorch, dependencies)
3. Write wrapper class that accepts thermal boundary conditions (T_hot, T_cold, surface area, target power) and returns optimized material/geometry recommendations
4. Validate against published benchmarks in TEGNet paper
5. Build CLI tool for batch optimization runs

**Week 2: COMSOL Automation**
1. Install COMSOL Multiphysics + Heat Transfer Module on workstation
2. Build parametric TEG model in COMSOL (single couple, then multi-couple)
3. Set up LiveLink for MATLAB/Python to script simulation runs
4. Create automation script: accept TEGNet output parameters, run COMSOL simulation, extract performance metrics (voltage, current, power, efficiency)
5. Validate: compare COMSOL results with TEGNet predictions (should be within 5-10%)

**Week 3: CAD Generation**
1. Install CadQuery, build parametric TEG module model
2. Parameters: leg height, leg cross-section, number of couples, substrate thickness, interconnect geometry
3. Export to STEP format
4. Build report template (LaTeX/Jinja): auto-populate with simulation results, material specs, geometry dimensions
5. End-to-end test: input specs -> TEGNet -> COMSOL -> CAD -> PDF report

### Phase 2: Web Platform (Weeks 4-5)

**Week 4: Backend**
1. FastAPI application: intake form endpoint, project status API, file delivery
2. PostgreSQL schema: customers, projects, simulation_runs, deliverables
3. Job queue (Celery + Redis) for async simulation pipeline
4. Stripe integration for payments

**Week 5: Frontend + Integration**
1. Next.js customer portal: inquiry form, project dashboard, file downloads
2. Admin dashboard: project queue, manual review/approval step
3. Email notifications (SendGrid): project received, feasibility complete, design delivered
4. End-to-end integration testing

### Phase 3: Validation (Weeks 6-8)

**Week 6-7:** Run 3-5 pilot projects (free or deeply discounted) with real customers
**Week 8:** Iterate based on feedback, finalize pricing, launch marketing

## Risk Register

| Risk | Likelihood | Impact | Mitigation | Fallback |
|------|-----------|--------|------------|----------|
| TEGNet predictions diverge from COMSOL validation (>15% error) | MEDIUM | HIGH | Calibration dataset; use COMSOL as ground truth, TEGNet as fast first-pass only | Rely primarily on COMSOL; TEGNet for screening only |
| COMSOL license cost increases or licensing model changes | LOW | MEDIUM | Annual license lock-in; explore OpenFOAM as backup | Switch to open-source simulation (longer run times but feasible) |
| No customers in first 6 months | HIGH | HIGH | Pre-sell before building; content marketing; conference networking | Pivot to academic design validation service (lower price, higher volume) |
| Customer disputes design quality / performance claims | MEDIUM | HIGH | Clear disclaimers (design only, no performance warranty); professional liability insurance | Limit scope to "optimization recommendation" not "guaranteed performance" |
| NIMS (TEGNet creators) launches competing service | LOW | MEDIUM | Move fast; build customer relationships; add proprietary validation data | Differentiate on speed, customer service, and vertical expertise |
| Founder burnout (solo consulting grind) | MEDIUM | HIGH | Automate pipeline to reduce per-project labor to <8 hours; raise prices | Hire junior engineer at ~$70K/year after 10+ projects |
| COMSOL simulation takes too long for 5-day promise | MEDIUM | MEDIUM | Pre-build parametric model library; use coarse mesh for first pass, fine mesh for final | Extend delivery to 7-10 days (still faster than 3-6 months traditional) |

## Validation Plan

**Success Criteria:**
1. Complete 3 pilot projects within first 3 months of launch
2. At least 1 pilot converts to a paid engagement ($15K+)
3. Customer NPS > 7/10 on design quality and turnaround speed
4. TEGNet-to-COMSOL prediction error < 10% for validated designs
5. Per-project labor < 16 hours (to maintain $900+/hr effective rate at $15K)

**How to Test:**
1. **Technical validation:** Run TEGNet + COMSOL pipeline on 10 known TEG designs from literature; compare predicted vs. published performance
2. **Market validation:** Cold outreach to 50 potential customers; measure response rate and interest level (target: >5% positive response)
3. **Operational validation:** Time yourself on 3 end-to-end design projects; can you deliver in 5 days at acceptable quality?
4. **Price validation:** Quote 3 different price points to different prospects; measure conversion sensitivity

**Timeline:**
- Weeks 1-5: Build prototype
- Weeks 6-8: Technical validation + pilot projects
- Weeks 9-12: Market validation + first paid engagement
- Month 4+: Steady state operations

## Total Cost and Time Estimate

| Metric | Value |
|--------|-------|
| Capital required (hard costs) | $30,000 - $40,000 |
| Capital required (with 6-month runway) | $100,000 - $170,000 |
| Time to working prototype | 5 weeks (part-time evenings/weekends: 8-10 weeks) |
| Time to first revenue | 3-6 months |
| Break-even point | 3-4 projects ($45K-$60K revenue) |

## Founder-Market Fit Assessment

**Founder profile:** Hooman Shariati - AI/ML infrastructure engineer at Adobe, deep Python/systems/cloud expertise, no hardware background, no thermoelectrics domain knowledge, no industrial customer network.

**Fit Score: 4/10**

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Technical ability to build platform | 9/10 | Python, ML, cloud, web dev - all strong |
| Domain expertise (thermoelectrics) | 2/10 | No background in thermoelectric physics, materials science, or thermal engineering |
| Customer network | 2/10 | No connections in industrial waste heat recovery, automotive thermal, or aerospace |
| Sales ability for $15-50K B2B services | 3/10 | Engineering manager background, not enterprise sales |
| Credibility with buyers | 3/10 | No publications, no track record in TE field |

**Critical gap:** Thermoelectric design is a deep-expertise domain. Customers paying $15-50K for a design package need to trust that the designer understands the physics, failure modes, and manufacturing constraints. A software engineer wrapping an open-source ML model will struggle to earn this trust without either:
1. A co-founder with TE PhD + industry experience
2. 6-12 months of intensive self-education + published case studies
3. Advisory board of recognized TE experts
