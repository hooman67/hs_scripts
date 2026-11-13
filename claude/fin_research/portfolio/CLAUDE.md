# Portfolio Analysis & Management — Project Charter

**Owner:** Hooman Shariati (hshariati@adobe.com)  
**Created:** 2026-07-07  
**Goal:** Build a diversified, quality-first portfolio optimized for (a) wealth preservation + growth, (b) USD-hedge strategy, (c) house purchase in 3–5 years.

---

## 1. The Portfolio Context

**Total investable assets:** $557,491 (as of 2026-07-06)
- $280,407 cash (Bucket A: volatility reducers)
- $157,115 in commodities (Bucket B: inflation hedge)
- $119,970 in individual stocks/growth (Bucket C: opportunistic growth)

**Separate asset:** $250,000 reserved for house down-payment (with father, not in this portfolio analysis)

**Portfolio constraints:**
- Timeline: 3–5 years until house purchase
- Max portfolio volatility: ≤10% (stress-test: can tolerate growth bucket losing 40%+)
- Geographic: target 50% USA / 25% developed ex-US / 25% emerging markets (currently 43/52/5 — imbalanced)
- Currency: CAD + USD mixed; minimize USD exposure due to inflation/printing concerns

---

## 2. Macro Thesis (to be verified independently)

**HIGH-CONVICTION beliefs (Hooman's stated):**
1. **USD decay** (10-yr horizon, ~70% loss) — most important conviction
2. **Commodity super-cycle** (3–5 yr horizon) — geopolitical/onshoring/war-driven
3. **Energy underinvestment** → oil/gas rally (structural supply deficit)
4. **Canadian energy outperformance** (pro-oil government, energy supply)

**MEDIUM-CONVICTION beliefs:**
5. **Uranium boom** (AI data centers, nuclear push) — but expensive now, waiting for pullback
6. **Gold/precious metals as inflation hedge** — same as uranium, expensive, waiting
7. **AI bubble will burst BUT diversified winners exist** (Google/Amazon > MSFT/Meta > OpenAI)
8. **Energy = indirect AI bet** (avoids picking AI winners directly)

**RESEARCH NEEDED:**
- Verify macro themes against real data (not AI-generated analysis)
- Test conflicting claims (e.g., uranium "cheap" vs "bubble") by going deeper
- Validate China allocation strategy + regulatory risk / opportunity
- Grade each macro theme 1–10 on conviction + evidence strength

---

## 3. Portfolio Holdings & Categorization Issues (to be audited)

**Current holdings:** 60+ individual positions, many micro-cap (<$1k)  
**Categorization problems:**
- Bucket A/B/C assignments may be wrong (Hooman found it hard to categorize)
- Geography tags (USA/dev-exUS/EM) need validation
- Some positions are off-thesis or redundant (e.g., 7 Canadian E&P names when CNQ dominates)
- Micro-positions create tax drag without material diversification

**Research needed:**
- Re-categorize all 60+ holdings (verify A/B/C bucket fit)
- Fix geography labels
- Identify overlap + redundancy
- Flag positions that contradict stated beliefs (e.g., owns KWEB/BABA but says China risk; owns AI names but says AI bubble)

---

## 4. Ideal Allocation & Buy/Sell Framework (Phase 1 output)

By end of this audit, we will produce:

**Ideal Allocation table:**
- Target % per bucket (A/B/C)
- Target % per geography (USA/dev-exUS/EM)
- Target % per sector/theme
- Target % per asset class (stocks/commodities/cash/crypto)

**Buy List:**
- Specific names + quantities to reach ideal allocation
- Entry price targets + rationale
- When to buy (now / on weakness / wait for correction)

**Sell Rules:**
- Exit triggers per position (price target / thesis break / better alternative)
- Rebalancing cadence (quarterly / semi-annual / on signal)
- Tax-loss harvesting opportunities

---

## 5. Key Questions Being Investigated (Phase 1 scope)

1. **China allocation:** How much should be allocated to China? What's the regulatory risk? VIE/sanction profile?
2. **AI exposure:** Are Google + Amazon the real winners? Should you own them directly or via proxies (energy, chips)?
3. **Energy thesis:** Is it underinvested (upside) or fairly priced (neutral)?
4. **Gold/uranium:** Bubble or value? At what prices do you buy?
5. **USD hedge:** Are your current real-asset holdings sufficient? Need more commodities / real estate?
6. **Volatility stress-test:** If market crashes 30% in 2027, is your house purchase still safe?

---

## 6. Working Rules (from fin_research project)

1. **Every claim is verified or marked UNVERIFIED.** No hallucinated numbers.
2. **Parallel agents for independent workstreams.** Synthesize after all are done.
3. **All findings recorded to disk immediately** so we can resume if machine dies.
4. **Living records updated after every session:**
   - PROJECT_STATE.md — current action items + progress
   - DECISIONS.md — what was decided + why
   - LEARNINGS.md — durable insights
5. **Deep dives only on top ~20 holdings.** (Micro-positions get summary treatment.)
6. **All records in `/portfolio` folder** (mirrors fin_research structure).

---

## 7. File Organization

Current topic index: `/home/colligo/hs_scripts/claude/fin_research/portfolio/research/build_canada/SUMMARY.md` — eight Canadian-company quality/valuation/AI/portfolio comparison and Omelchak/LionGuard interview/past-pick review; open for the October 20 research shortlist and evidence gates. Recommendations are unaccepted; use `PROJECT_STATE.md` for current operational status.

```
fin_research/portfolio/
├── CLAUDE.md                    # THIS FILE — stable context
├── PROJECT_STATE.md             # LIVE status + action items
├── DECISIONS.md                 # Decisions made + rationale
├── LEARNINGS.md                 # Durable insights
├── PHASE1_AUDIT.md              # Phase 1 comprehensive report
├── ideal_allocation.md          # Target allocation + reasoning
├── buy_list.md                  # Positions to acquire + prices
├── holdings_reclassified.csv    # All 60+ holdings with corrected A/B/C + geography
├── deep_dives/                  # (Phase 2) per-holding thesis docs
│   ├── CNQ.md
│   ├── XOM.md
│   ├── PFE.md
│   └── ...
└── research/                    # Agent findings (macro themes, etc.)
    ├── macro_themes.md
    ├── ai_thesis_analysis.md
    ├── china_allocation.md
    └── ...
```

---

## 8. Success Criteria (end of Phase 1)

- ✅ All macro themes verified (not AI-generated hand-waving)
- ✅ Conflicting claims resolved + deeper patterns identified
- ✅ All 60+ holdings re-categorized + geography fixed
- ✅ China allocation strategy decided (how much + how)
- ✅ AI exposure decided (direct vs indirect)
- ✅ Ideal allocation table produced + buy list generated
- ✅ Sell rules defined
- ✅ House purchase timeline validated (volatility stress test)
- ✅ Rebalancing cadence + discipline rules set

---

## Next Steps

→ Launch 7 parallel research agents (macro, AI, China, gold/uranium, holdings audit, portfolio structure, rebalancing framework)  
→ Synthesize findings into PHASE1_AUDIT.md  
→ Produce ideal_allocation.md + buy_list.md  
→ Schedule Phase 2 deep dives on top 20 holdings
