# Feasibility & Prototype: Food Processing Quality Prediction Platform

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CUSTOMER PLANT                             │
│                                                                   │
│  ┌──────────┐    ┌──────────┐    ┌────────────────────────────┐ │
│  │   PLCs   │    │  SCADA/  │    │      Edge Gateway          │ │
│  │(Rockwell,│◄──►│Historian │◄──►│  - OPC-UA Client           │ │
│  │ Siemens) │    │(PI, Ign) │    │  - Modbus TCP/RTU Client   │ │
│  └──────────┘    └──────────┘    │  - Data buffering (SQLite)  │ │
│                                   │  - TLS uplink to cloud      │ │
│                                   │  - Heartbeat/health check   │ │
│                                   └──────────────┬───────────────┘ │
└──────────────────────────────────────────────────┼───────────────┘
                                                   │ HTTPS/MQTT
                                                   │ (outbound only)
┌──────────────────────────────────────────────────┼───────────────┐
│                         CLOUD (AWS)              │               │
│                                                   ▼               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Ingestion Layer                         │   │
│  │  - AWS IoT Core / MQTT broker                             │   │
│  │  - Kinesis Data Streams (buffering)                       │   │
│  │  - Lambda (tag validation, normalization)                 │   │
│  └──────────────────────────────┬───────────────────────────┘   │
│                                  │                               │
│  ┌──────────────────────────────▼───────────────────────────┐   │
│  │                    Storage Layer                           │   │
│  │  - TimescaleDB on RDS (time-series sensor data)           │   │
│  │  - S3 (raw data archive, model artifacts)                 │   │
│  │  - Redis (real-time feature cache)                        │   │
│  └──────────────────────────────┬───────────────────────────┘   │
│                                  │                               │
│  ┌──────────────────────────────▼───────────────────────────┐   │
│  │                  ML Pipeline Layer                         │   │
│  │  - Feature engineering (rolling stats, rate of change)    │   │
│  │  - Model training (SageMaker / custom EC2)                │   │
│  │  - Model serving (SageMaker endpoint / ECS)               │   │
│  │  - Inference: every 60 seconds per line                   │   │
│  │  - Retraining: weekly with operator feedback              │   │
│  └──────────────────────────────┬───────────────────────────┘   │
│                                  │                               │
│  ┌──────────────────────────────▼───────────────────────────┐   │
│  │                  Application Layer                         │   │
│  │  - FastAPI backend (Python)                               │   │
│  │  - React dashboard (real-time via WebSocket)              │   │
│  │  - Alert engine (SNS → SMS, email, Slack webhook)         │   │
│  │  - Multi-tenant auth (Auth0 or Cognito)                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Key Architecture Decisions

1. **Cloud-first (no edge inference in v1)**: Simplifies deployment, centralizes model management, avoids edge GPU costs. Requires stable internet at plant -- acceptable for 95%+ of target customers. Latency budget: 30-minute prediction window means 5-10 second cloud round-trip is negligible.

2. **Outbound-only connectivity**: Edge gateway initiates all connections outbound (MQTT over TLS). No inbound ports opened in plant firewall. Critical for customer IT approval.

3. **Per-customer ML models**: Not a shared model. Each production line gets its own trained model. Avoids cross-contamination of process-specific patterns. Limits generalization but maximizes per-customer accuracy.

4. **60-second inference cycle**: Predict every 60 seconds. Fast enough for 30-minute advance warning. Slow enough to control compute costs.

## Bill of Materials (Per Deployment)

### Edge Gateway

| Component | Estimated Cost | Confidence | Notes |
|-----------|---------------|------------|-------|
| Raspberry Pi 4 (8GB) + case + power | $120 | VERIFIED | Industrial alternative: OnLogic Helix 500 at $600 |
| Industrial DIN-rail enclosure | $80 | VERIFIED | Phoenix Contact or equivalent |
| MicroSD 128GB (industrial grade) | $40 | VERIFIED | Samsung PRO Endurance or similar |
| Ethernet cable + connectors | $20 | VERIFIED | |
| Cellular modem (backup connectivity) | $150 | VERIFIED | Sierra Wireless or Quectel |
| **Total edge hardware** | **$410** | | Add $400 if customer requires industrial-grade IPC |

### Cloud Infrastructure (Per Line, Monthly)

| Component | Estimated Cost | Confidence | Notes |
|-----------|---------------|------------|-------|
| AWS IoT Core (messages) | $15/month | ASSUMED | ~2.5M messages/month at 1 msg/sec |
| TimescaleDB on RDS (db.r6g.medium) | $80/month | ASSUMED | Shared across lines, amortized |
| SageMaker endpoint (ml.t3.medium) | $50/month | VERIFIED | On-demand inference |
| ECS Fargate (API + dashboard) | $60/month | ASSUMED | Shared across customers |
| S3 storage (raw data) | $10/month | VERIFIED | ~50GB/month/line |
| Redis (ElastiCache) | $30/month | VERIFIED | cache.t3.micro shared |
| CloudWatch + monitoring | $15/month | ASSUMED | |
| **Total cloud per line** | **~$260/month** | | At $5K/line revenue = 95% gross margin |

### Software Development Costs (Initial Build)

| Component | Estimated Cost | Confidence | Notes |
|-----------|---------------|------------|-------|
| OPC-UA/Modbus connector (edge) | $40K | ASSUMED | 2 engineers x 2 months. Must handle edge cases, reconnection, buffering. |
| ML pipeline (training + serving) | $80K | ASSUMED | 2 ML engineers x 3 months. Feature engineering, model selection, retraining automation. |
| Dashboard + alert system | $50K | ASSUMED | 1 full-stack + 1 frontend x 3 months. Real-time WebSocket, mobile-responsive. |
| Auth + multi-tenancy + billing | $30K | ASSUMED | 1 engineer x 2 months. Stripe integration, tenant isolation. |
| DevOps/infra (Terraform, CI/CD) | $20K | ASSUMED | 1 DevOps x 1.5 months. |
| Food domain consulting | $30K | ASSUMED | Domain expert advisor, 6 months part-time. |
| QA + security audit | $20K | ASSUMED | Penetration testing, load testing. |
| Buffer (integration surprises) | $50K | ASSUMED | OPC-UA edge cases, PLC vendor quirks. |
| **Total development** | **$320K** | | 8 months to MVP with 4-5 person team. |

[CONFIDENCE on development costs: MEDIUM -- highly dependent on team efficiency and integration complexity. OPC-UA is notoriously quirky across PLC vendors.]

## Software Stack

### Edge Gateway
- **OS**: Raspberry Pi OS Lite (Debian-based) or Ubuntu Server 22.04
- **OPC-UA client**: asyncua (Python, maintained fork of opcua-asyncio) or node-opcua (Node.js)
- **Modbus client**: pymodbus (Python)
- **Local buffer**: SQLite (WAL mode for concurrent read/write)
- **MQTT client**: Paho MQTT (Python) or EMQX client
- **Supervisor**: systemd services with watchdog
- **Remote management**: Tailscale or WireGuard VPN for remote debugging

### Cloud Backend
- **Language**: Python 3.11+ (FastAPI for API, asyncio throughout)
- **ML framework**: scikit-learn (baseline models), PyTorch (LSTM/Transformer for sequence prediction), statsmodels (ARIMA baselines)
- **Feature engineering**: Pandas, NumPy, tsfresh (time-series feature extraction)
- **Model serving**: SageMaker real-time endpoints or BentoML on ECS
- **Database**: TimescaleDB (PostgreSQL extension) for time-series, PostgreSQL for application data
- **Cache**: Redis (real-time feature store, WebSocket pub/sub)
- **Message broker**: AWS IoT Core (MQTT) + Kinesis Data Streams
- **Orchestration**: Prefect or Airflow (model retraining pipelines)
- **Infrastructure**: Terraform, AWS CDK
- **CI/CD**: GitHub Actions, Docker, ECR

### Frontend Dashboard
- **Framework**: React 18 + TypeScript
- **Real-time**: WebSocket via Socket.io or AWS API Gateway WebSocket
- **Charting**: Recharts or ECharts (time-series visualization)
- **State management**: Zustand or React Query
- **Mobile**: Responsive web (no native app in v1)

### Monitoring & Observability
- **Application**: Datadog or Grafana Cloud (metrics, traces, logs)
- **ML-specific**: Evidently AI (data drift, model performance monitoring)
- **Alerting**: PagerDuty (internal), AWS SNS (customer-facing)
- **Edge health**: Custom heartbeat + Tailscale status

## Build Instructions (8-Month Plan)

### Month 1-2: Foundation
- [ ] Set up development environment, CI/CD, Terraform
- [ ] Build OPC-UA connector with mock PLC simulator (Prosys OPC-UA Simulation Server)
- [ ] Build Modbus connector with mock RTU
- [ ] Implement edge data buffering and MQTT uplink
- [ ] Set up cloud ingestion pipeline (IoT Core → Kinesis → TimescaleDB)
- [ ] Recruit food domain advisor (part-time consultant)

### Month 3-4: ML Core
- [ ] Acquire training data: partner with 1-2 food processors for historical historian exports (PI data)
- [ ] Feature engineering pipeline: rolling statistics, rate of change, lag features, cross-tag correlations
- [ ] Baseline models: Isolation Forest (anomaly detection), XGBoost (classification: off-spec vs. in-spec)
- [ ] Sequence models: LSTM or Temporal Fusion Transformer for 30-minute lookahead
- [ ] Evaluation framework: precision/recall against labeled off-spec events
- [ ] Model serving infrastructure (SageMaker endpoints)

### Month 5-6: Application Layer
- [ ] FastAPI backend (multi-tenant, REST + WebSocket)
- [ ] React dashboard (real-time process health score, trend charts, alert feed)
- [ ] Alert engine (configurable thresholds, SMS/email/Slack delivery)
- [ ] Auth + tenant management (Cognito or Auth0)
- [ ] Edge remote management (deployment, updates, health monitoring)

### Month 7-8: Pilot & Iteration
- [ ] Deploy at first pilot customer (1-2 production lines)
- [ ] 2-week baseline learning period
- [ ] Begin predictions in advisory mode
- [ ] Iterate on model accuracy with operator feedback
- [ ] Bug fixes, UX improvements based on real usage
- [ ] Security audit and penetration testing
- [ ] Documentation and sales materials

### Milestone Gates

| Month | Gate | Success Criteria |
|-------|------|-----------------|
| 2 | Edge connectivity proven | Successfully read 50+ tags from 3 different PLC simulators at 1 Hz |
| 4 | ML baseline working | >60% precision, >50% recall on historical off-spec detection (using acquired historical data) |
| 6 | End-to-end demo | Live demo with simulated data: sensor drift → prediction → alert in <90 seconds |
| 8 | Pilot deployed | 1 customer, 1 line, predictions in advisory mode, no critical bugs for 2 weeks |

## Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| 1 | OPC-UA integration fails on specific PLC vendor (e.g., older Allen-Bradley, proprietary protocols) | HIGH | HIGH | Budget extra time for edge cases. Partner with OPC-UA experts. Limit v1 to Rockwell ControlLogix + Siemens S7-1500 (most common in food). |
| 2 | Insufficient training data (can't access historical process data pre-deployment) | MEDIUM | HIGH | Offer free 3-month monitoring period before prediction mode. Partner with OSIsoft/AVEVA for data export tooling. Synthetic data augmentation. |
| 3 | Model accuracy too low (<50% precision = too many false alarms, operators ignore) | MEDIUM | HIGH | Start with simple anomaly detection (high recall, lower precision). Add operator feedback loop to reduce false positives. Set conservative thresholds initially. |
| 4 | Plant IT blocks edge gateway deployment (firewall, security policy) | HIGH | MEDIUM | Outbound-only architecture. SOC 2 certification. Offer air-gapped demo mode. Customer IT security questionnaire prepared in advance. |
| 5 | Sales cycle too long (>6 months to first paying customer) | HIGH | HIGH | Target plants that already have a "digital transformation" budget approved. Offer 90-day free pilot to reduce friction. Focus on quality director (feels pain) not IT (creates friction). |
| 6 | ProcessMiner/Augury moves down-market to $5K/line pricing | MEDIUM | HIGH | Build vertical depth in ONE subsector (dairy) faster than they can. Data moat from first 5-10 dairy deployments. Compete on time-to-value (deploy in days vs. months). |
| 7 | Key engineer leaves before MVP | MEDIUM | HIGH | Ensure no single-person dependencies. Document architecture decisions. Competitive equity packages. |
| 8 | Food safety incident from missed prediction (false negative) | LOW | CRITICAL | Clear Terms of Service: advisory only, does not replace quality programs. Professional liability insurance. Never market as "safety system" -- market as "waste reduction." |
| 9 | Regulatory compliance burden (FDA 21 CFR Part 11) | MEDIUM | MEDIUM | v1 explicitly does NOT claim compliance. Target quality/waste reduction use case, not safety-critical decisions. Add compliance in v2 after revenue funds it. |
| 10 | Cloud outage disrupts predictions | LOW | MEDIUM | Edge gateway buffers data locally. Predictions resume automatically when connectivity restores. 30-minute prediction window provides buffer. |

## Validation Plan

### Phase 1: Technical Validation (Month 1-2)
- **Objective**: Prove OPC-UA/Modbus data collection works reliably
- **Method**: Set up lab with PLC simulator (Rockwell Emulate or Prosys). Simulate 1 week of continuous operation. Verify zero data loss, correct tag mapping, reconnection after network interruption.
- **Success**: 99.9% data capture rate over 7 days continuous operation

### Phase 2: ML Validation (Month 3-4)
- **Objective**: Prove ML can predict off-spec from sensor data with useful accuracy
- **Method**: Acquire 6-12 months of historical data from a dairy plant (PI historian export). Label off-spec events. Train/test split (80/20, temporal). Measure precision/recall.
- **Success**: >65% precision, >50% recall at 30-minute prediction horizon. (Meaning: when system says "off-spec coming," it's right 65%+ of the time, and it catches 50%+ of actual events.)
- **Fallback**: If 30-minute horizon fails, try 15-minute or 10-minute horizon (shorter = easier to predict)

### Phase 3: Customer Validation (Month 5-6)
- **Objective**: Prove a real customer will install and use the system
- **Method**: Deploy edge gateway at 1 pilot customer. Run in monitoring mode. Present predictions to quality director weekly. Measure prediction vs. actual.
- **Success**: Customer agrees to continue and expand to second line. At least 1 confirmed "save" (prediction that could have prevented waste if acted upon).

### Phase 4: Commercial Validation (Month 7-8)
- **Objective**: Prove customer will pay
- **Method**: Convert pilot to paid subscription. Begin onboarding customer #2.
- **Success**: First customer signs 12-month contract at $5K/line/month. Pipeline of 3+ additional qualified prospects.

## Cost & Time Estimate Summary

| Category | Cost | Timeline |
|----------|------|----------|
| Engineering team (4-5 people, 8 months) | $250K | Months 1-8 |
| Cloud infrastructure (development) | $15K | Months 1-8 |
| Domain advisor (food scientist, part-time) | $30K | Months 1-8 |
| Hardware (edge dev kits, lab PLCs) | $10K | Month 1 |
| Security audit + legal | $15K | Month 7-8 |
| **Total to MVP + first pilot** | **$320K** | **8 months** |

| Milestone | Timeline | Revenue |
|-----------|----------|---------|
| MVP complete | Month 8 | $0 |
| First paying customer | Month 9-10 | $10K/month |
| 5 lines deployed | Month 12 | $25K/month |
| 10 lines deployed | Month 14-16 | $50K/month |
| Break-even (monthly) | Month 14-16 | ~$50K/month |
| Year 1 cumulative revenue | Month 12 | ~$550K |

[CONFIDENCE: MEDIUM on Year 1 revenue -- highly dependent on sales execution and pilot conversion rate]

## Founder-Market Fit Assessment

**Founder profile**: AI/ML infrastructure engineer, deep Python/systems/cloud expertise, no hardware background.

### Strengths (fit)

| Dimension | Assessment |
|-----------|-----------|
| ML pipeline architecture | STRONG FIT. Building scalable ML training/serving infra is core competency. Feature stores, model serving, retraining pipelines -- founder has done this before. |
| Cloud infrastructure | STRONG FIT. AWS/GCP, Terraform, Kubernetes, CI/CD -- all in wheelhouse. |
| Python ecosystem | STRONG FIT. scikit-learn, PyTorch, FastAPI, asyncio -- primary language for all components. |
| Systems engineering | STRONG FIT. Edge gateway software, MQTT, data buffering, reliability engineering -- systems thinking maps well. |
| Data engineering | STRONG FIT. Time-series data pipelines, stream processing, data normalization. |

### Gaps (risk)

| Dimension | Assessment | Mitigation |
|-----------|-----------|------------|
| Food science domain knowledge | CRITICAL GAP. Cannot build credible models or sell to food processors without understanding what causes off-spec yogurt, how pasteurization fails, what pH drift means. | Hire food domain advisor immediately ($5K/month consulting). Target co-founder with food science or process engineering background. |
| OPC-UA / industrial protocols | MODERATE GAP. OPC-UA is well-documented but has vendor-specific quirks. Modbus is simple. Founder likely has no OT (Operational Technology) experience. | Self-learnable in 2-4 weeks. Open-source libraries (asyncua, pymodbus) are well-maintained. OPC-UA Foundation resources available. Partner with a controls engineer consultant for first 2 deployments. |
| Enterprise food industry sales | SIGNIFICANT GAP. Selling to food plant VPs requires domain credibility, patience for long cycles, and understanding of procurement processes. | Hire sales advisor/fractional VP Sales with food manufacturing background. Attend PROCESS EXPO, IBIE, Pack Expo trade shows. Join Food Processing Suppliers Association (FPSA). |
| Hardware / edge deployment | MINOR GAP. Raspberry Pi deployment is software-centric. No custom hardware design needed. | Use off-the-shelf industrial PCs (OnLogic, Advantech) if RPi insufficient. No custom PCB or mechanical design required in v1. |
| Regulatory / food safety | MODERATE GAP. FDA regulations, HACCP, FSMA -- founder likely unfamiliar. | v1 positions as "waste reduction" not "food safety." Domain advisor covers regulatory awareness. Add compliance expertise if/when expanding to safety-critical claims. |

### Overall Founder-Market Fit: 6.5/10

**Honest assessment:** The founder is technically capable of building 80% of this product (ML pipeline, cloud infra, edge software, dashboard). The critical 20% gap is food industry domain expertise -- both for building credible models and for selling to food manufacturing buyers who value domain credibility over technical sophistication.

**Path to success requires:**
1. A food domain co-founder or very early hire (food scientist, process engineer with 10+ years in dairy/beverage)
2. Willingness to spend 3-6 months learning the food processing world (plant visits, trade shows, industry reading)
3. Acceptance that the founder's role is CTO, not CEO -- the company needs a food-industry-native face for customer relationships

**Comparable success patterns:** Many successful industrial AI startups were founded by technical ML engineers who paired with domain experts. Uptake (transportation AI) was founded by tech people but hired industry veterans for sales. Augury's founders were signal processing PhDs, not maintenance technicians -- but they hired industry deeply.
