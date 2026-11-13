---
name: cutlog-project
description: "CutLog SaaS prototype — laser cutting parameter logger with machine-specific suggestions, built for customer validation with Facebook community contacts"
metadata: 
  node_type: memory
  type: project
  originSessionId: 848e1716-17cf-40bc-9d61-e53e72b82e2b
---

# CutLog — Complete Project Context

## What It Is

CutLog is a machine-specific laser cutting parameter journal with smart suggestions. Operators log cuts daily (30 seconds each), building a personal + community database that learns per-machine. The daily logging habit creates the data moat — this is NOT a generic parameter lookup tool.

**Tagline**: "Stop keeping parameters in your head. Let your machine remember."

**Why:** Static parameter tables (lasertips.org) already exist but operators aren't satisfied. LLMs give "80% good enough" generic answers. The core insight from validation: "how can someone else's results help MY machine?" — generic lookup fails, must be machine-specific first, community second.

---

## Business Context

### Origin
Discovered through systematic 4-cycle venture-scale startup idea research (auto_research project). Laser cutting optimization emerged as winner from deep research into manufacturing pain points.

### Customer Validation (Facebook Outreach, 2026-06-10)

| Contact | Key Quote | Implication |
|---------|-----------|-------------|
| Sean BeardyWeirdo | "I have reservations on how this could be achieved by another person" | Generic lookup fails — must be machine-specific |
| Nate Keen | "Once you've mastered YOUR particular machine it's just small adjustments" / "It's all in my head from years of experience" | Product captures tacit knowledge per-machine |
| Nate Keen | "Line interval can be the difference from making a clean cut or having cut weld itself back together" | Line interval is THE critical parameter most tools ignore |
| Mike AJ Guindon | Shared lasertips.org but still interested in AI tool | Static tables aren't enough — dynamic learning system is the gap |

### Status (as of 2026-06-13)
- Messages sent to all 3 contacts proposing call times — awaiting replies
- Generating additional leads in parallel
- Prototype fully functional and seeded with 724 parameter sets
- App accessible via SSH tunnel for demo calls

### Competitive Position
- vs lasertips.org: Dynamic, personal, machine-specific (not static tables)
- vs LLM/ChatGPT: Verified outcomes, per-machine calibration, persistent memory
- vs OEM tables: Cross-brand, community-powered, learns from outcomes
- vs operator notebooks: Searchable, shareable, never retires

### Revenue Model (Future)
- Freemium: Free logging, paid suggestions from community
- Target: $10-20/month for pro features
- Validation metric: "Would you pay for this?" from beta users

---

## Technical Architecture

### Stack
- **Frontend**: Next.js 14 + Tailwind CSS (dark theme, mobile-first)
- **Backend**: Next.js API routes + Supabase client (serverless)
- **Database**: Supabase PostgreSQL (free tier: 500MB, 50K rows)
- **Auth**: Supabase Auth (email-based)
- **Hosting**: Currently on Pluto job machine, planned for Vercel

### Code Location
- **App**: `/mnt/localssd/laser_log/app/`
- **GitHub**: `git@github.com:hooman67/cutlog.git` (personal account, NOT work)
- **SSH key for GitHub**: `/mnt/localssd/laser_log/hs_personal_github_ssh_key` (ed25519)
- **Git SSH config**: `git config core.sshCommand "ssh -i /mnt/localssd/laser_log/hs_personal_github_ssh_key"`

### Supabase Credentials
- **Project URL**: `https://aobzsonuemamitlrakqs.supabase.co`
- **Anon Key**: `sb_publishable_YPIJ6BJmNhKx0tPFMIx4HA_c3vuMqC-`
- **Service Role Key**: `sb_secret_TdtA6v3mYBtb8SDOBP52WQ_lZcrC0CQ`
- **Stored in**: `/mnt/localssd/laser_log/app/.env.local`

### Deployment (Vercel — Production)
- **Live URL**: https://cutlog-two.vercel.app
- **Vercel team**: `cutlog`, connected to `hooman67` GitHub
- **Auto-deploys**: Push to `main` → Vercel rebuilds automatically
- **PWA**: Installable on iPhone via Safari Share → "Add to Home Screen"

### Dev Access / Testing
- **Pluto machine**: `100.64.21.99` (SSH gateway port `3000`)
- **SSH tunnel from Mac**: `ssh -L 8000:localhost:8000 colligo@100.64.21.99 -p 3000`
- **Dev server**: port 8000, start with `export PATH="/opt/conda/bin:$PATH" && cd /mnt/localssd/laser_log/app && npx next dev -p 8000`
- **Node.js**: `/opt/conda/bin/node` (v18.20.2) — must add to PATH manually

### Database Schema

**Tables**: `machines`, `cuts`, `materials`

**cuts** (main table):
- `id` uuid PK
- `machine_id` uuid FK (nullable — NULL for baseline data)
- `user_id` uuid FK (nullable — NULL for baseline data)
- `material` text NOT NULL
- `thickness_mm` numeric NOT NULL
- `power_pct`, `speed_mm_min`, `gas_type`, `gas_pressure_bar`, `focus_position_mm`, `nozzle_diameter_mm`, `nozzle_distance_mm`, `line_interval_mm` (all nullable)
- `quality_rating` integer (1-5)
- `edge_quality` text CHECK ('clean', 'slight_dross', 'heavy_dross', 'burn_marks')
- `source` text CHECK ('user_logged', 'ai_baseline', 'scraped_public') DEFAULT 'user_logged'
- `is_shared` boolean DEFAULT true
- `created_at` timestamptz

**RLS Policies on cuts**:
- "Users can view own cuts" — `auth.uid() = user_id`
- "Users can view shared and baseline cuts" — `is_shared = true OR source = 'ai_baseline'`
- "Users can insert own cuts" — `auth.uid() = user_id OR user_id IS NULL`

**machines**:
- brand, model, wattage_w, source_type (fiber/co2/diode), resonator_hours, gas_types[], controller, location_country, nickname

**materials**: Pre-seeded 85+ materials with categories and aliases

### App Pages (5 screens)
1. `/` — Home dashboard (Log Cut, Get Suggestion, Cut History, Machine Settings)
2. `/auth` — Email signup/signin
3. `/machine` — Machine registration (one-time)
4. `/log` — Cut logging form (30-second workflow, 10+ parameters)
5. `/suggest` — Suggestion engine (3-tier: Your Data → AI Baseline → Community)
6. `/history` — Searchable cut history

### Data Pipeline

**Current data in DB: ~724 parameter sets**:
- 554 AI-generated baseline (20 materials, scientifically realistic)
- 52 from LightBurn GitHub repos (real community settings)
- 43 from lasertips.org + Wikipedia (reference data)
- 80 from Reddit/forums (real user-reported)
- 2 manually logged by user during testing

**Generator script**: `/mnt/localssd/laser_log/app/scripts/generate-baseline-data.py`
- Produces SQL INSERT statements to `/mnt/localssd/laser_log/app/data/baseline-parameters.sql`
- 20 materials: SS304, SS316, SS430, Mild Steel, Carbon Steel, Galvanized Steel, Aluminum, Copper, Brass, Titanium, Inconel, Hastelloy, Acrylic, Leather, Plywood, MDF, Polycarbonate, Rubber, Felt, Cork

**Scraping research**: `/home/colligo/hs_scripts/claude/auto_research/deep_research/laser_cutting_optimization/`
- `data_sources.md` — 8 source categories, 800-1200+ potential params
- `extraction_strategy.md` — Python code for LightBurn XML, Epilog PDFs, Reddit API
- `SCRAPING_ROADMAP.md` — 3-phase plan (Phase 1: 500-700 auto, Phase 2: +200-300 semi-auto)
- `source_validation.md` — Quality assessment of all sources

### Key Bugs Fixed
1. Suggestion search used exact `eq` → changed to `ilike` with `%` wildcards for partial matching
2. RLS blocked JOINs on machines table → removed JOIN, query cuts directly
3. `!machine` guard silently blocked search → removed (suggestions work without machine)
4. Typed material (not dropdown selected) didn't trigger search → now uses `material || materialSearch`
5. NULL thickness in scraped data violated NOT NULL → filtered out those rows
6. Source column needed before baseline insert → combined migration 003+004

### Migrations Applied (in order)
1. `001_initial_schema.sql` — Core tables + RLS
2. `002_seed_materials.sql` — 85+ materials
3. `PASTE_003_AND_004.sql` — Added `source` column + made user_id/machine_id nullable for baseline
4. `COMBINED_PASTE_ALL.sql` — 724 parameter sets inserted

---

## Validation Plan (Next Steps)

### Immediate
1. Wait for Nate/Mike/Sean to respond to call invites
2. Demo app via SSH tunnel during calls
3. Ask validation questions:
   - "Would you log your cuts after each job?"
   - "What would make you NOT log a cut?"
   - "Would you share data with similar-machine operators?"
   - "What's missing?"
   - "Is there a parameter I'm not capturing?"

### Success Metrics
| Metric | Target | Timeframe |
|--------|--------|-----------|
| Beta users | 5-10 | Week 2-3 |
| Cuts logged/user/week | 5+ | After week 1 |
| Return after week 1 | 60%+ | Week 2 |
| "Would you pay?" | 3+ yes | Week 4 |

### Future Phases (NOT built yet)
- Phase 2: PWA (installable on phone), offline support, invite system
- Phase 3: OPC-UA machine connectivity (auto-log without manual entry)
- Phase 4: ML model (XGBoost/LightGBM) trained on accumulated data
- Phase 5: Drift detection, fleet view, LLM cold-start for exotic materials

---

## User Preferences (for this project)
- Personal GitHub account (hooman67), NOT work account (hshariati)
- Prefers manual credential passing, NOT MCP authentication for Supabase
- Supabase SQL changes via copy-paste into SQL Editor (no direct DB connection from Pluto)
- Node.js at `/opt/conda/bin/` on this Pluto machine
