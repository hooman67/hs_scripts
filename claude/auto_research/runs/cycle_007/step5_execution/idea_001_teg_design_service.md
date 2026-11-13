# Execution Plan: Waste Heat Recovery Design-as-a-Service

## 5a. Product Definition

**Core value proposition**: Get a custom-optimized thermoelectric generator design in days instead of months, at 1/10th the cost of traditional engineering — ready to send to a fabricator.

**Key features for MVP (max 3)**:
1. Web intake form: customer specifies heat source temperature, cold side conditions, geometry constraints, target power output
2. AI-optimized TEG design delivered as CAD + fabrication spec within 5 business days
3. Performance guarantee: if fabricated TEG underperforms spec by >15%, redesign free

**What it does NOT do**:
- Does not manufacture TEGs (partner with fabricators)
- Does not install or integrate systems
- Does not handle thermal interface engineering (customer's responsibility)

**Success metrics**:
- 5 paid design projects completed in first 6 months
- Designed TEGs achieve within 10% of predicted performance when fabricated
- Average project value >$20K

---

## 5b. Technical Architecture

**System components**:
1. TEGNet neural network (publicly available) + custom training on additional material databases
2. Parametric CAD generation (FreeCAD/OpenSCAD API)
3. Thermal simulation validation (COMSOL or Elmer FEM)
4. Web platform for project intake + results delivery
5. Materials database (thermoelectric properties of commercially available materials)

**Technology stack**:
- ML: TEGNet (PyTorch, published codebase) + custom fine-tuning
- Simulation: COMSOL Multiphysics or open-source Elmer FEM for validation
- CAD: FreeCAD Python API for automated geometry generation
- Web: Next.js + PostgreSQL + S3 for deliverables
- Hosting: AWS (compute-heavy simulation on EC2 instances)

**Build vs buy**:
- TEGNet core: USE (publicly available, extend/fine-tune)
- Materials database: BUILD (compile from literature + supplier datasheets)
- CAD automation: BUILD (scripted parametric generation)
- Thermal simulation: BUY (COMSOL license $15K/year)
- Web platform: BUILD (standard stack)

---

## 5c. Resources Required

| Item | Cost | Notes |
|------|------|-------|
| COMSOL license (annual) | $15,000 | Multiphysics + Heat Transfer module |
| AWS compute (simulation) | $500/month | GPU instances for TEGNet + FEM |
| Web hosting | $200/month | Standard Next.js deployment |
| Thermoelectric materials database compilation | $10,000 | Literature review + supplier outreach (contract) |
| Domain expertise: thermoelectric PhD consultant | $150/hour | 20 hrs/month for 6 months = $18,000 |
| Marketing: conference attendance (ITES, ICT) | $10,000 | International Thermoelectric Society |
| Legal (contracts, IP) | $5,000 | Client agreements, terms of service |

---

## 5d. Build Instructions

1. **Weeks 1-4: Platform Development** (1 full-stack developer)
   - Set up TEGNet model + inference pipeline
   - Build materials property database (top 20 commercial TE materials)
   - Create web intake form + project management dashboard
   - Integrate parametric CAD generation

2. **Weeks 3-6: Validation Pipeline** (TE consultant + developer)
   - Set up COMSOL simulation workflow
   - Validate TEGNet designs against published benchmarks
   - Create automated report generation (PDF with design specs, predicted performance, fabrication instructions)

3. **Weeks 5-8: First Pilot Projects** (founder + consultant)
   - Reach out to 20 industrial contacts with waste heat problems
   - Offer 3 free/discounted pilot designs to validate workflow
   - Partner with 1-2 TEG fabricators for manufacturing quotes

4. **Weeks 8-12: Iterate + Commercialize** (team)
   - Refine based on pilot feedback
   - Build case studies from pilot results
   - Launch commercial pricing ($15-50K per project)
   - Attend International Conference on Thermoelectrics

---

## 5e. Validation Plan

**Target**: 3 pilot projects with real industrial waste heat sources

**Key hypotheses**:
1. AI-designed TEGs perform within 10% of prediction when fabricated
2. Design delivery in 5 days (vs industry standard 3-6 months) is valued at $20K+
3. At least 2/3 pilot customers convert to paid follow-on projects

**Go/no-go criteria**:
- GO: Fabricated TEGs within 15% of predicted output AND 2+ customers willing to pay $15K+ for next design
- NO-GO: TEG performance >30% below prediction OR customers unwilling to pay >$5K

---

## 5f. Timeline & Milestones

| Week | Milestone |
|------|-----------|
| 4 | Platform MVP (intake → AI design → report) |
| 6 | First 3 pilot designs delivered |
| 12 | Pilot TEGs fabricated and tested |
| 14 | Commercial launch with case studies |
| 20 | 5 paid projects completed |
| 26 | Monthly revenue target: $30K+ |

---

## 5g. Cost Estimate

| Category | Amount |
|----------|--------|
| Full-stack developer (6 months) | $90,000 |
| TE domain consultant (6 months, part-time) | $18,000 |
| COMSOL license | $15,000 |
| AWS compute (6 months) | $3,000 |
| Materials database compilation | $10,000 |
| Marketing + conferences | $10,000 |
| Legal + misc | $10,000 |
| Pilot fabrication costs (3 TEGs) | $15,000 |
| **Total to first revenue** | **~$171,000** |

**Monthly burn rate**: ~$20K (founder + consultant + compute)

**Funding strategy**: Bootstrap-friendly at $171K. Could self-fund or small angel check ($200K). Revenue starts at month 4-5 with pilot conversions.

**Revenue projection (Year 1)**:
- 15 design projects × $25K average = $375K
- Recurring design optimization subscriptions (5 customers × $2K/month × 6 months) = $60K
- **Year 1 total: ~$435K**
