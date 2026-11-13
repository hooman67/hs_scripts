# Auto-Research — Project State & Operating Manual

**This is the single source of truth for this project.** If you are a new agent picking
this up, read this file top to bottom first. It tells you exactly what the goal is, what
has been done, where execution currently stands, and how to behave.

Last updated: 2026-06-28 by Claude (Opus 4.8). Owner: Hooman Shariati (hshariati@adobe.com).

---

## 1. The Goal (what Hooman actually wants)

Find a **business idea for a secondary income stream**. Two acceptable shapes:
1. A small niche business that is **easy to execute solo**, OR
2. Something that could become a **bigger venture** (funding, etc.).

**"Easy to execute" means:** Hooman does NOT want to hunt for specialist co-founders.
Prefer **pure software / AI ideas he can build himself.**

**Founder profile (drives "founder-market fit" scoring):**
- Engineering manager at Adobe — AI platform infra, generative models (Firefly).
- Strong in: ML/AI, software, cloud/infra, systems.
- Bachelor's in **electrical engineering**.
- Has friends who are **mechanical engineers** (so mech-heavy hardware is *possible* but
  not preferred — it still adds risk/coordination).
- Weak/avoid: anything needing PhD specialists (metallurgists, geneticists), wet labs,
  novel hardware manufacturing, FDA/regulatory-approval-gated products.

**Implication for ranking:** Pure software / AI-on-existing-hardware ideas score highest.
Hardware carries a real penalty. This is already baked into the scorecard's
"Founder-market fit (15%)" weight — keep applying it.

---

## 2. Where We Are Right Now (PROJECT STATE)

### The big picture
This project has run TWO research rounds and produced a clear #1 winner that is already
being executed as a separate product.

| Round | Who | When | What happened |
|-------|-----|------|---------------|
| 1 | older AI model | Jun 7–8 2026 | Cycles 001–020 → deep-researched 30 ideas → `MASTER_COMPARISON.md` → **Laser Cutting SaaS won (8.85/10)** |
| 2 | newer AI model ("second run") | Jun 9–14 2026 | Extended to cycles 021–040 (+45 graduates); rewrote final_report / patterns / plan_adjustments; **began executing the laser-cutting winner** (data-collection/scraping plan) |

### What "the laser cutting winner" became
The #1 idea (Laser Cutting Parameter Optimization SaaS) is now the **CutLog** product —
live at cutlog-two.vercel.app. Its execution work (scraping roadmap, data sources,
extraction strategy) was **moved OUT of this repo** to the CutLog project (commit
`17542b2c "move laster cut out"`, Jun 14). It is no longer here. See the global memory
file `project_cutlog.md` for CutLog details. **CutLog = round-1 winner, already in flight.**

### THE GAP — where the previous agent left off (this is what to continue)
Round 2 extended the funnel to 40 cycles and found **45 new graduates** (cycles 021–040),
several scoring as high or higher than the original winners for a software founder:
- **Plasma Consumable Life Prediction (9/10)** — highest score ever recorded
- **IPM Compliance AI "PestDoc" ($80–150K)** — lowest capital ever, pure SaaS, regulatory mandate
- **DPF Regen Scheduling Optimizer** — zero hardware, pure API "parasitic SaaS"
- **SpringbackAI**, **XRF Workflow AI**, **LabFlow**, **Welding Gas Analytics**, **NitroGuard**, etc.

**BUT** the deep-research stage (Step 6) and `MASTER_COMPARISON.md` still only cover the
**original 30 ideas from cycles 1–20.** None of the 45 cycle-21–40 graduates were ever
deep-researched or scored head-to-head. **That is the unfinished work.**

→ See `PROJECT_STATE.md` (companion file) for the live, frequently-updated execution
checklist. This CLAUDE.md holds stable context; PROJECT_STATE.md holds moment-to-moment status.

### Current decision pending
Hooman wants a SECONDARY idea (distinct from CutLog, which he's already executing). The
natural continuation is: **deep-research the best never-deep-researched cycle-21–40
graduates, score them on the standard scorecard, and produce an updated master comparison**
to surface the strongest #2 idea for a solo software founder. Confirm scope with Hooman
before launching (deep research on ~10 ideas is token-expensive).

---

## 3. The Research Methodology (how the funnel works)

Full spec lives in `research-plan.md`. Summary:

- **Step 1** — Find 10 recent technologies (TRL ≥ 5, ≤18mo to product).
- **Step 2** — Competitive density (1–5). Score ≥4 = auto-reject.
- **Step 3** — Market sizing (TAM>$1B, SAM>$100M, >15% CAGR).
- **Step 4** — Feasibility (tech/market/execution/timing risk; capital).
- **Step 5** — Execution plan (condensed 1-pager for later cycles).
- **Step 6** — Deep research on finalists: 5 docs (product def, competitive, feasibility/
  prototype, customer validation, scorecard) + confidence-marked claims (VERIFIED/ASSUMED/
  UNVERIFIED). Output a weighted scorecard, then a head-to-head comparison.

### The validated winning archetype (from 400 technologies across 40 cycles)
```
Software/AI intelligence (the moat)
+ on commodity hardware ($1–5K) OR (better) hardware the customer ALREADY owns
+ underserved mid-market (can't afford the $50K+ incumbent)
+ no regulatory barrier to SELL (regulatory mandate to BUY = bonus)
+ immediate, measurable ROI (shows up on next month's invoice)
= high-feasibility, solo-founder-friendly startup
```
Capital hierarchy (best → worst for a solo founder):
1. Pure SaaS on existing APIs ($80–200K)
2. Software on customer's existing hardware ($150–300K)
3. Software + commodity IoT sensor ($200–400K)
4. Software + custom hardware module ($300–500K)
5. Novel hardware system ($500K+) — rarely survives for a solo founder

---

## 4. File / Folder Organization (so anyone can navigate)

Keep files **organized by topic, few in number.** One file per topic, not one per artifact.

```
auto_research/
├── CLAUDE.md                    # THIS FILE — stable context + operating manual
├── PROJECT_STATE.md             # LIVE status: action items, current step, what's next
├── LEARNINGS.md                 # all durable learnings (consolidated)
├── DECISIONS.md                 # all decisions Hooman & I have made + rationale
├── LONG_TERM_PLANS.md           # roadmap / where this is all heading
├── research-plan.md             # the funnel methodology (Steps 1–6) — stable spec
├── patterns.md                  # per-cycle observations across all 40 cycles
├── sources.md                   # curated good/bad sources
├── runs/
│   ├── final_report.md          # 40-cycle summary, top-15 ranking, all 45 new graduates
│   ├── plan_adjustments.md      # how the plan changed during execution
│   ├── cycle_NNN/               # per-cycle reports + step5 execution plans
│   └── ideas/                   # misc idea workspaces
└── deep_research/
    ├── MASTER_COMPARISON.md     # head-to-head scorecard (CURRENTLY only the original 30)
    ├── deep_research_adjustments.md
    └── {idea_slug}/             # 5-doc deep dive per idea (29 folders, all cycles 1–20)
```

**Note on overlap:** Some ideas have deep-research docs in BOTH `deep_research/{slug}/` and
under `runs/cycle_NNN/step5_execution/deep_research/`. The canonical location is the
top-level `deep_research/{slug}/`. The duplicates under `runs/` are legacy — leave them but
don't add new ones there.

---

## 5. How To Work Here (operating rules — from Hooman)

These are Hooman's standing rules for how he wants agents to behave. Follow them.

1. **Diligent, human-readable records.** Maintain four living sections/files:
   - **Action items** → `PROJECT_STATE.md`
   - **Learnings** → `LEARNINGS.md`
   - **Decisions** → `DECISIONS.md`
   - **Long-term plans** → `LONG_TERM_PLANS.md`
   After every working session, check whether each needs updating. **If you're unsure
   whether Hooman actually acted on advice, how he did something, or whether he agreed to a
   plan change — ASK him. Don't assume.**

2. **Organize by topic, minimize file count.** One file per topic (e.g. all Reddit work in
   one file, all Facebook work in one file). Don't spawn a new file per post/experiment.
   Files & folders must be navigable by someone with zero context — names should let you
   narrow down where to look. Use judgment; don't be overly prescriptive. Fix legacy
   fragmentation when you reasonably can.

3. **Fan out subagents for parallel work — but keep the main session free.** The single most
   important thing: **do work in the background so Hooman can hand the main session other
   tasks.** Distribute work so independent pieces run in parallel, but **serialize steps that
   depend on earlier learnings** (e.g. deep-research depends on knowing which ideas to pick).
   Don't over-parallelize. When unsure how to split, ask. More subagents ≠ better; background
   + correctness is what matters.

4. **Cite sources, quantify, mark confidence.** Every claim links to a source. Numbers over
   adjectives. Mark feasibility claims VERIFIED / ASSUMED / UNVERIFIED.

5. **Bias toward action in the funnel** (when borderline, promote and let the next stage
   filter), but **bias toward asking** on direction/scope decisions that are Hooman's to make.

---

## 6. Hard-Won Learnings (the short version — full list in LEARNINGS.md)

- **Pure software ideas score 2–3 pts higher than hardware** for this founder. Hardware =
  inherent penalty.
- **"Software on existing hardware" > "software + commodity hardware" > "hardware."**
  Parasitic SaaS on existing APIs (Samsara, SolarEdge, SCADA) is the capital-efficient extreme.
- **Always check for entrenched European industrial-QC firms** (SIKORA, Pixargus, Dr. Schenk,
  GlassQuality, Precitec, Marposs) before promoting — they don't show on Crunchbase but
  dominate niches.
- **Regulatory compliance MANDATES are a demand driver, not a barrier.** (Helping meet an
  existing reg = gold. Needing approval to sell = death.)
- **Instant-reject domains:** printing/packaging inspection (saturated), glass QC, injection
  molding, construction tech, consumer hardware, government/utility buyers, FDA/regulatory-
  gated, anything needing PhDs/wet labs.
- **Facebook groups are the highest-signal validation channel** for B2B manufacturing
  (laser/CNC/welding shop owners are active there).
- **Domain exhaustion hits ~35 cycles** — more cycles = diminishing returns. Don't just run
  more cycles; deep-research and validate what we already have.

---

## 7. Quick Reference — Top Candidates Not Yet Deep-Researched

From `runs/final_report.md`, the cycle-21–40 graduates most fitting the founder profile
(pure software / low capital), as candidates for the next deep-research pass:

| Idea | Cycle | Capital | Type | Why it fits |
|------|-------|---------|------|-------------|
| IPM Compliance AI "PestDoc" | 036 | $80–150K | Pure SaaS | Lowest capital ever, regulatory mandate, 15K+ PCOs |
| DPF Regen Scheduling Optimizer | 029 | $150–250K | Pure SaaS | Zero hardware, API-only, 500K+ trucks |
| SpringbackAI (press brake) | 030 | $200–300K | Pure SaaS | "Laser cutting params for press brakes," data moat |
| Plasma Consumable Life Prediction | 030 | $150–250K | HW+SW | Highest score ever (9/10), 50K+ tables |
| XRF Workflow AI (scrap yards) | 028 | $150–250K | Pure SaaS | Software on existing $30K guns, 5K+ yards |
| Dental Lab Workflow AI "LabFlow" | 027 | $200K | Pure SaaS | 6K+ labs, remake-risk prediction |
| Wireless TAB Documentation Platform | 026 | $150–250K | Pure SaaS | Near-zero competition, daily pain |
| Label Die-Cut Registration AI | 040 | $150–250K | Pure SaaS | Uses existing press cameras, 90%+ margin |

(Pure-SaaS ones are the strongest founder-fit. Plasma scores highest overall but has a
hardware/sensor component — friends-who-are-mech-engineers territory.)
</content>
