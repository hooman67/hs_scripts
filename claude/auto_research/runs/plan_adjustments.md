# Plan Adjustments & Major Findings

Document for Hooman to review — changes made to the research plan during execution of cycles 001-040.

---

## Adjustments to the Original Plan

### 1. Effective TRL minimum raised to 5-6
**Original**: TRL ≥ 5
**Adjusted**: TRL 4-5 technologies almost never survive Step 4 (feasibility). In practice, TRL 6+ technologies have the best pass-through rate because they've been demonstrated in relevant environments, not just labs.

### 2. Competitive density ≥ 4 = automatic reject
**Added rule**: If 3+ funded companies ($10M+ each) or 1 dominant player ($100M+) exist in the exact space, reject immediately at Step 2. Saves significant research time on Steps 3-4 for ideas that are clearly too late.

### 3. Capital efficiency became primary ranking factor
**Original**: Ranked by feasibility score alone
**Adjusted**: A $200K idea scoring 7/10 outranks a $3.5M idea scoring 7/10. The capital-adjusted ranking better reflects startup reality — lower capital = faster to validate, less dilution, more attempts possible.

### 4. Condensed Step 5 format for later cycles
**Original**: Full 7-section execution plan for every graduate
**Adjusted**: After proving the format works (Cycles 001-010), cycles 011-040 used condensed 1-page execution summaries. The detailed format is available for deep-dives on top picks later.

### 5. Domain rotation became pattern-testing
**Original**: Rotate domains to discover new technologies
**Adjusted**: After Cycle 010 confirmed the winning archetype, later cycles deliberately tested the pattern in new verticals rather than looking for new archetypes. This was more productive — 3-4 graduates per cycle when applying the pattern vs 0-1 when exploring novel domains.

### 6. "Democratize expensive tools" became the meta-strategy
**Discovery**: By Cycle 010, it was clear that the highest-scoring ideas all follow one pattern: take a $50-500K professional system that only large companies use, replicate 80% of its capability on $200-5K commodity hardware + AI, and sell to the 10x larger mid-market that was previously unserved.

### 7. European industrial QC company check (NEW — Cycle 021+)
**Added rule**: Before promoting at Step 2, specifically search for German/Swiss/Dutch/Scandinavian industrial QC companies. Many "niche" markets that appear empty from US-centric searches are actually well-served by $50-200M European companies operating globally.
**Examples found**: SIKORA (wire/cable), Pixargus (surface inspection), GlassQuality/LiteSentry (glass), Dr. Schenk (web inspection), Precitec (laser process), Marposs (grinding). These don't show up on Crunchbase but dominate their verticals.

### 8. Printing & packaging inspection = instant reject (NEW — Cycle 021)
**Finding**: Cycle 021 found 6+ funded competitors for EVERY sub-segment of printing/packaging inspection (flexo plates, inline print, corrugated, labels, color). AVT, Isra Vision, Lake Image, Global Vision, PrintQualityAI all have established products. Domain is fully saturated.
**Exception**: Very narrow niches like "label die-cut registration using existing cameras" (pure software, no new hardware) can still work at 1/10th incumbent price point.

### 9. "Software on existing hardware" is the preferred model (NEW — Cycle 026+)
**Discovery**: Ideas that layer AI on equipment customers ALREADY own score higher than even commodity-hardware ideas because they eliminate:
- Hardware BOM and sourcing risk
- Installation complexity
- Manufacturing/inventory
- Physical distribution
**Examples**: XRF Workflow AI (layers on $30K XRF guns), DPF Regen (layers on Samsara/Geotab telematics), Label Die-Cut AI (uses existing press cameras), TAB Platform (pairs with Bluetooth instruments techs already carry), InverterIQ (connects to SolarEdge/Enphase APIs)

### 10. Regulatory compliance as demand DRIVER (NEW — Cycle 036)
**Original assumption**: Regulatory = barrier = reject
**Revised**: Regulatory compliance MANDATES (not approval processes) are actually the strongest demand driver because:
- Customers cannot say "nice to have, we'll wait"
- Budget already allocated for compliance
- Non-compliance = fines/shutdowns
**Key distinction**: A product that REQUIRES regulatory approval to sell = bad. A product that HELPS customers meet EXISTING regulations = gold.
**Examples**: IPM Compliance AI (pest control compliance reporting), DOT aggregate gradation monitoring, food safety temperature documentation.

### 11. Domain exhaustion confirmed at ~35 cycles (NEW — Cycle 035+)
**Observation**: Graduate quality and quantity declined noticeably after Cycle 035:
- Cycles 021-035: Average 2.3 graduates/cycle at 7.6/10 average score
- Cycles 036-040: Average 1.8 graduates/cycle at 7.3/10 average score
- Overlap between ideas increases (CNC router wear is similar to CNC tool wear from Cycle 010)
**Conclusion**: 40 cycles is the natural limit for this research methodology. Further cycles would produce diminishing returns and increasing duplication.

---

## Major Findings (Updated for 40 Cycles)

### The Winning Formula (validated across 400 technologies)

```
Commodity sensor/hardware ($1-5K) OR existing customer hardware
+ AI/ML software layer (the moat)
+ Underserved mid-market (can't afford $50K+ incumbents)
+ No regulatory barriers to SELL (regulatory mandates to BUY = bonus)
+ Immediate measurable ROI (visible on next month's invoice)
= High-feasibility startup idea
```

### The Capital Hierarchy (NEW finding from 40 cycles)

Ideas rank in this order of capital efficiency and feasibility:

1. **Pure SaaS on existing APIs** ($80-200K) — PestDoc, DPF Regen, InverterIQ
2. **Software on customer's existing hardware** ($150-300K) — XRF Workflow, Label Die-Cut AI, TAB Platform
3. **Software + commodity IoT sensor** ($200-400K) — Welding Gas, NitroGuard, Grain Dryer
4. **Software + custom hardware module** ($300-500K) — Wire Vision, Aggregate Gradation
5. **Novel hardware system** ($500K+) — rarely survives feasibility for solo founder

### What Always Fails (Confirmed + New)
1. **Construction tech** — certification + conservatism + Katerra's ghost
2. **Regulatory-gated markets** — FDA, nuclear, novel food = 5-7 year timelines
3. **Government/utility buyers** — 12-24 month procurement kills cash flow
4. **Consumer hardware** — Amazon, marketing costs, razor margins
5. **"Platform" plays without users** — need specific vertical focus first
6. **Printing/packaging inspection** — NEW: fully saturated by 6+ incumbents per niche
7. **Glass manufacturing QC** — NEW: GlassQuality (3000+ systems) dominates all segments
8. **Injection molding optimization** — NEW: OSPHIM, Engel, RJG, SIMCON all compete

### The Best New Verticals Discovered (Cycles 021-040)

| Vertical | Why It Works | Example Graduate |
|----------|-------------|-----------------|
| Metal fabrication (plasma, press brake) | 50K+ shops, expensive trial-and-error, no software | Plasma Consumable (9/10) |
| Fleet maintenance prediction | API-only (no hardware), huge installed base of telematics | DPF Regen (8/10) |
| Building services/field trades | Fragmented, paper-based, compliance-driven | PestDoc, TAB Platform (8/10) |
| Agriculture post-harvest | Gap between manual and $100K+ systems | DryerIQ, FreshGuard (8/10) |
| Food/beverage processing | Clear $ savings, existing sensors, fragmented | FoulCast, BrewOx (8/10) |
| Woodworking/furniture | 50K+ CNC shops, metal CNC proven the demand | Router Bit Wear (8/10) |
| Scrap/recycling operations | Software on existing expensive instruments | XRF Workflow (8/10) |
| Industrial gas/chemicals | Zero visibility into usage, waste is invisible | NitroGuard, Welding Gas (8/10) |

### What I Would Do Differently in a Re-run
1. Start with the "software on existing hardware" archetype from Cycle 001
2. Search for European niche industrial companies at Step 2 from the start
3. Skip all printing/packaging, glass, injection molding, and construction domains
4. Focus 80% of research time on: metal fabrication, field services, fleet, agriculture post-harvest, food processing, industrial gas/chemical
5. Add "regulatory compliance driver?" as a positive signal in Step 3
6. Stop at 35 cycles (diminishing returns after that)

---

## Round 3 Adjustments (2026-07-01) — post deep-research of cycle-21–40 graduates

After deep-researching all 19 Tier-1 cycle-21–40 graduates (see `deep_research/
MASTER_COMPARISON_V2.md` and `BIG_PICTURE_LEARNINGS.md`), four changes were baked into
`research-plan.md` for the next round:

### 12. MANDATORY incumbent/OEM check at Step 2 (was the #1 failure of round 2)
14 of 19 "8–9/10, zero-competition" ideas actually had a funded incumbent or OEM already
shipping the core. The cycle stage was blind to them. Step 2 now has a required checklist:
OEM-does-it, entrenched-European/private-firm, funded-horizontal-platform-lists-your-vertical,
incumbent-marketing-copy-is-your-pitch, and "the-gap-is-just-plumbing." Any hit ⇒ density ≥3.

### 13. MANDATORY moat gate at Step 2
Moat collapsed to 2.8/10 avg in round 2 because cheap+buildable ideas are cheap *because*
they're easy to copy. New gate: "what stops a cloner/incumbent in 6 months?" Valid answers =
data/network flywheel, proprietary data, genuine tech difficulty the founder can solve,
integration lock-in. "Cheap + trivial + no flywheel" = reject even at 9s elsewhere.

### 14. MANDATORY growth-rate check at Step 3
Round 2 promoted flat/shrinking markets (dental labs, craft breweries, cabinet shops) that
looked large. Now must verify CAGR from a real source and count the true buyer universe.
Trajectory > size.

### 15. WIDER-NET domain directive (round 3 goal)
Rounds 1–2 converged on ONE archetype (AI/software on industrial equipment). That vein is
mined. Round 3 deliberately explores untouched domains: software-native/digital-only, consumer
& prosumer software, digital health (non-FDA), education, climate/energy SOFTWARE, robotics/
autonomy software layers, media/generative-AI apps (founder's day-job strength), bio/health
data informatics, trust & safety / provenance. Industrial-QC/shop-floor sensor ideas are now
deprioritized unless they carry a real moat.

---

## Source Quality Notes (Updated)

### Best sources found
- **IEEE Spectrum** — highest signal for near-commercial technologies
- **Company websites** — essential for competitive analysis (especially European companies)
- **Trade publications** (Welding Journal, Modern Plastics, Food Engineering) — reveal which problems practitioners actually have
- **ArXiv (cs.RO, eess.SP)** — useful for cutting-edge approaches
- **Industry association websites** (GAWDA, NEBB, NPMA) — reveal market structure and pain points

### Sources that didn't work well
- **TechCrunch** — mostly consumer/fintech, not industrial
- **Nature/Science** — paywalled, too academic
- **Product Hunt** — consumer software, not B2B industrial
- **Crunchbase/PitchBook** — paywalled/blocked (still a gap)

### Key gap still unresolved
No good free source for:
- Competitive funding amounts (Crunchbase/PitchBook blocked)
- Market sizing data (Grand View Research, paid reports)
- Patent landscape analysis (USPTO search is clunky)
- European company revenue data (private companies don't disclose)
