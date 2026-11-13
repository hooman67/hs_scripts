# 02_competitive_analysis.md

## AI-Powered Thermal Inspection Tool — Competitive Analysis

### Direct Competitors

#### 1. FLIR / Teledyne — THREAT LEVEL: HIGH

- **Revenue**: ~$1.9B (thermal imaging division); parent Teledyne acquired for $8B (2021)
- **Product range**: FLIR ONE ($204) to T-Series ($13,499+)
- **AI status**: ACTIVELY entering this space. The iXX-Series ($4,999-$7,999) features "app-powered" workflows with the FLIR Ace platform — an open SDK for third-party inspection apps on-device.
- **Key development**: Condoit (third-party partner) has built electrical inspection workflow automation on FLIR Ace. This validates the thesis but shows FLIR is approaching via platform, not integrated product.
- **Weakness**: Enterprise DNA. Their cameras cost $5K-$13K. They cannot sell a $399 AI-smart camera without cannibalizing their core business. Their "intelligence" is workflow automation (guided steps), not true anomaly interpretation. Report generation remains manual.
- **Window**: 18-24 months before Ace ecosystem matures enough to offer competitive AI interpretation.

**Confidence**: HIGH — based on published FLIR product specs, Ace platform documentation, and Condoit partnership announcements.

#### 2. Fluke (Fortive Corporation) — THREAT LEVEL: MEDIUM

- **Parent**: Fortive Corp (~$6B revenue)
- **Products**: TiS20+ ($800) to Ti480 PRO ($5,500+); pocket thermal PTi120 ($1,200)
- **AI status**: Zero AI interpretation. Software (SmartView) is basic manual annotation/reporting.
- **Weakness**: Hardware-only mentality. No cloud platform, no AI R&D visible in thermal division.
- **Could**: Acquire a startup doing this. Historically slow to innovate in software.

**Confidence**: HIGH — based on current Fluke product catalog and SmartView software capabilities.

#### 3. Seek Thermal — THREAT LEVEL: LOW-MEDIUM

- **Status**: Private, US-based, designs own microbolometer sensors
- **Products**: Consumer ($250) through professional ($600)
- **AI status**: Markets as "AI-ready" but no concrete AI features shipping
- **Weakness**: Smaller engineering team than FLIR, no AI products in market

**Confidence**: MEDIUM — limited public information on R&D pipeline.

#### 4. InfiRay (IRay Technology, China) — THREAT LEVEL: LOW

- **Status**: Public (Shenzhen Stock Exchange), aggressive pricing
- **Products**: P2 Pro phone module (~$300), handheld cameras ($400-$2,000)
- **AI status**: None found
- **Weakness**: Chinese company (trade restriction risk), no software ecosystem, hardware-only

**Confidence**: HIGH — based on product catalog and community reviews.

#### 5. HikMicro (Hikvision subsidiary) — THREAT LEVEL: LOW (US/EU)

- **Parent**: Hikvision (~$12B revenue, on US Entity List)
- **Products**: Industrial handheld thermography
- **AI status**: Hikvision has world-class AI/ML in surveillance; could theoretically port to thermal. No evidence in trades segment.
- **Weakness**: US regulatory/trust barrier is near-insurmountable for trades professionals

**Confidence**: HIGH — regulatory status is public record.

### Indirect Competitors

#### Report-Generation Software (Manual)

- **HomeGauge, Spectora, Horizon** (home inspection report platforms): Templated report builders but require manual entry. No thermal AI. Could be integration partners rather than competitors.
- **FLIR Ignite** (cloud): Stores and annotates thermal images but requires manual interpretation.

#### Connected Worker Platforms

- **XOi Technologies**: Video-first field service platform for HVAC/plumbing. AI for video documentation, not thermal.
- **Augmentir**: AI-powered work instructions. Could theoretically add thermal but not their focus.
- **BuildOps**: Commercial contractor management. No thermal features.

#### Drone-Based Thermal Inspection

- **DJI (Matrice 350 + Zenmuse H30T)**: Aerial thermal for roofing, solar, utilities. Different form factor but adjacent use case.
- **Skydio**: Autonomous inspection drones. Could move into handheld but unlikely.
- Relevance: These compete for some inspection budgets (roof surveys) but complement handheld for interior/panel work.

### Adjacent Movers (Watch Closely)

| Entity | Move | Risk | Timeline |
|--------|------|------|----------|
| FLIR Ace Platform | Open SDK for iXX cameras, third-party AI apps | Third-party could build our exact product on their hardware | 12-18 months |
| Apple/Google | Phone-based thermal via accessory + AI | If Apple ships native thermal in iPhone, game changes | Unlikely <3 years |
| Insurance tech (Hippo, Cape Analytics) | AI property assessment expanding to interior thermal | More likely to be customer than competitor | 2-3 years |
| Condoit (on FLIR Ace) | Electrical inspection workflows on iXX cameras | Currently workflow, not AI interpretation; but could add | 6-12 months |

### Open Source / DIY Risk

**Assessment: MODERATE — not fatal**

Relevant open source:
- **DIY-Thermocam** (1.2K GitHub stars): Full DIY thermal camera build with FLIR Lepton. Proves hardware is commodity.
- **Flirpy** (236 stars): Python library for FLIR camera data extraction
- **Thermal-Image-Analysis** (168 stars): Desktop analysis for thermal files
- **AI-Thermometer** (152 stars): Deep learning temperature measurement

**What open source CANNOT provide**:
1. Proprietary labeled dataset of 100K+ trade-specific thermal faults (this does not exist publicly)
2. On-device real-time inference optimized for edge hardware
3. One-tap professional report generation with code compliance formatting
4. Field-ready UX for non-technical workers at 6am on a job site
5. OTA model updates trained on fleet-wide inspection data

**Confidence**: HIGH — surveyed GitHub, academic papers, and maker forums. No project combines AI interpretation + report generation for trades.

### Big Tech Risk

**Assessment: LOW-MEDIUM**

- **Google/Apple/Microsoft/Amazon**: Too niche. Thermal inspection tools for electricians is not a platform play. None of these companies manufacture thermal sensors. None have shown interest.
- **Teledyne/FLIR**: This IS the relevant big-tech risk. Specifically, FLIR adding native AI interpretation to iXX-Series cameras or a third-party building a compelling app on Ace.
- **NVIDIA**: Provides inference hardware (Jetson) that could power competitor devices, but would not build the end product.

**The defensibility question**: Why can't FLIR just add AI to their cameras?

Answer: They can, eventually. But:
1. FLIR optimizes for hardware margin ($5K-$13K ASP). A $399 AI device cannibalizes their core business.
2. FLIR's Ace platform approach means they are being a platform, not building the app themselves. This creates opportunity for third parties (including us).
3. Training data is the moat: FLIR has millions of thermal images but they are NOT labeled by fault type. We can build a purpose-trained model faster by partnering directly with inspectors.
4. Report generation is a software problem that hardware companies historically ignore.

### Final Verdict: CONDITIONAL-GO

**GO factors**:
- Clear market gap: NO product ships AI interpretation + one-tap reporting for trades thermal today (Confidence: HIGH)
- Large addressable market: 800K+ electricians + 400K+ HVAC techs + 100K+ home inspectors in US alone
- Hardware is commodity ($200 sensor); value is in software/AI (high margins)
- First-mover data advantage compounds: 10K active users = insurmountable training data moat within 2 years
- FLIR's platform approach validates the thesis while creating a 18-24 month window
- Clear ROI: saves 30min/inspection at $100/hr = $50+ saved per use = payback in weeks

**CONDITIONS for GO (must be true)**:
1. Ship within 12 months (before FLIR Ace ecosystem matures)
2. Secure 10K+ labeled thermal fault images within 6 months (through inspector partnerships)
3. AI accuracy above 85% for top-3 fault categories at launch
4. Hardware strategy uses commodity modules, not custom sensor development
5. Distribution via trade channels (not D2C marketing war)

**STOP signals (would change to NO-GO)**:
- FLIR announces native AI fault interpretation on any camera under $2,000
- A funded startup ($5M+) emerges with this exact product thesis
- Thermal sensor supply chain disruption (FLIR Lepton goes on allocation)
- AI accuracy cannot exceed 80% after 6 months of model development

**Competitive density**: LOW. This is a gap in the market, not a crowded space. Risk is incumbent (FLIR) rather than startup competition.
