# Feasibility & Prototype Plan: AI Fire Sprinkler Inspection App

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MOBILE APP (iPad/iPhone)                       │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────┐  │
│  │ Camera Feed  │→ │ On-Device ML │→ │ Detection Overlay + UI    │  │
│  │ (AVFoundation│  │ (CoreML/ONNX)│  │ (SwiftUI)                 │  │
│  └──────────────┘  └──────────────┘  └───────────────────────────┘  │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────┐  │
│  │ Offline DB   │  │ Report Engine│  │ Sync Manager              │  │
│  │ (SQLite/     │  │ (PDF gen)    │  │ (Background upload)       │  │
│  │  Core Data)  │  │              │  │                           │  │
│  └──────────────┘  └──────────────┘  └───────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ (When connected)
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         CLOUD BACKEND                                 │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────┐  │
│  │ API Gateway  │  │ Auth Service │  │ Model Training Pipeline   │  │
│  │ (FastAPI)    │  │ (Firebase/   │  │ (AWS SageMaker or         │  │
│  │              │  │  Auth0)      │  │  Vertex AI)               │  │
│  └──────────────┘  └──────────────┘  └───────────────────────────┘  │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────┐  │
│  │ Image Store  │  │ Inspection   │  │ NFPA 25 Rules Engine      │  │
│  │ (S3)         │  │ Database     │  │ (Python + code mappings)  │  │
│  │              │  │ (PostgreSQL) │  │                           │  │
│  └──────────────┘  └──────────────┘  └───────────────────────────┘  │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │ Model Serving (for complex cases / cloud fallback)            │    │
│  │ TorchServe or Triton Inference Server                         │    │
│  └──────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Primary inference | On-device (CoreML) | Offline capability is critical. Many buildings have poor connectivity (basements, mechanical rooms). Inspectors cannot wait for cloud round-trips. |
| Model format | PyTorch → CoreML export (via coremltools) | Train in PyTorch (best ecosystem), deploy as CoreML for iOS. ONNX as fallback for Android. |
| Cloud role | Training, sync, complex cases | Cloud handles model retraining, data aggregation, and optional "second opinion" for low-confidence detections. |
| Database | PostgreSQL (cloud) + SQLite (device) | Standard choices. Core Data is an option for iOS but SQLite gives cross-platform portability. |
| Report generation | On-device PDF + cloud backup | Reports must generate offline. Use Swift PDF libraries on device, store in cloud for history. |
| Authentication | Firebase Auth or Auth0 | Fast to implement, handles team/org structures, SSO for enterprise tier. |

## Bill of Materials (BOM)

### Development Costs (6-Month MVP)

| Item | Cost | Confidence | Notes |
|------|------|------------|-------|
| **iOS Developer (Senior, 6 months)** | $90,000 | VERIFIED | Based on $150K/yr senior iOS contractor rate. Could be $70-120K depending on market. |
| **ML Engineer (6 months, part-time 60%)** | $54,000 | VERIFIED | Based on $150K/yr at 60% allocation. Handles model training, CoreML export, accuracy tuning. |
| **Fire Protection Domain Expert (Contract, 3 months)** | $25,000 | ASSUMED | NICET IV certified inspector or fire PE consultant. ~$8K/month for part-time engagement. Market rate uncertain. |
| **Cloud Infrastructure (6 months)** | $3,000 | VERIFIED | AWS: S3 ($50/mo) + RDS ($200/mo) + SageMaker training ($200/mo) + API hosting ($50/mo) |
| **Apple Developer Program** | $99 | VERIFIED | Annual fee for App Store distribution |
| **Training Data Collection** | $15,000 | ASSUMED | Paying inspectors to label existing photos, or contracting annotation service. Could be $5K-30K depending on partnership deals. |
| **NFPA 25 Standard Purchase** | $500 | VERIFIED | Digital copy of NFPA 25 for reference |
| **UI/UX Design (Contract)** | $12,000 | ASSUMED | 2-3 weeks of contract design work for app screens, AR overlay, report templates |
| **Legal (Terms of Service, liability disclaimer)** | $5,000 | ASSUMED | Fire inspection has liability implications; need proper disclaimers |
| **Contingency (10%)** | $20,000 | -- | Buffer for unknowns |
| **TOTAL** | **$224,599** | -- | Within $200K budget with tight management, $225K realistic |

### Ongoing Monthly Costs (Post-Launch)

| Item | Monthly Cost | Confidence |
|------|-------------|------------|
| Cloud hosting (API + DB + storage) | $500-2,000 | ASSUMED (scales with users) |
| Model retraining compute | $200-500 | ASSUMED |
| Apple Developer + TestFlight | $8 | VERIFIED |
| Customer support tooling | $100-300 | ASSUMED |
| **Total monthly (pre-revenue)** | **$800-2,800** | -- |

## Software Stack

### Mobile App (iOS - Primary Platform)

| Layer | Technology | Maturity |
|-------|-----------|----------|
| Language | Swift 5.9+ | Production-ready |
| UI Framework | SwiftUI | Production-ready |
| Camera/AR | AVFoundation + Vision framework | Production-ready |
| ML Inference | CoreML + Vision | Production-ready (Apple's own stack) |
| Local Storage | Core Data or SQLite (via GRDB) | Production-ready |
| PDF Generation | PDFKit or TPPDF | Production-ready |
| Networking | URLSession + Combine | Production-ready |
| Offline Sync | Custom sync engine or Realm | Production-ready |

### ML Pipeline (Cloud)

| Layer | Technology | Maturity |
|-------|-----------|----------|
| Training Framework | PyTorch 2.x | Production-ready |
| Object Detection | YOLOv8 or Faster R-CNN (torchvision) | Production-ready |
| Image Classification | EfficientNet-V2 or MobileNetV3 | Production-ready |
| Data Labeling | Label Studio (self-hosted) or Roboflow | Production-ready |
| Model Export | coremltools (Apple) | Production-ready |
| Training Infrastructure | AWS SageMaker or local GPU | Production-ready |
| Experiment Tracking | Weights & Biases or MLflow | Production-ready |
| Model Versioning | DVC or MLflow Model Registry | Production-ready |

### Backend API

| Layer | Technology | Maturity |
|-------|-----------|----------|
| Framework | FastAPI (Python) | Production-ready |
| Database | PostgreSQL 15+ | Production-ready |
| Object Storage | AWS S3 | Production-ready |
| Auth | Firebase Auth or Auth0 | Production-ready |
| Deployment | AWS ECS Fargate or Railway | Production-ready |
| CI/CD | GitHub Actions | Production-ready |

### Android (Phase 2, Month 8+)

| Layer | Technology | Notes |
|-------|-----------|-------|
| Framework | Kotlin + Jetpack Compose | Or React Native / Flutter for cross-platform |
| ML Inference | ONNX Runtime or TensorFlow Lite | CoreML models export to ONNX |
| Camera | CameraX | Android's modern camera API |

## Build Instructions (MVP in 6 Months)

### Phase 1: Foundation (Months 1-2)

**Week 1-2: Data Collection Sprint**
- Partner with 1-2 fire protection companies for image access
- Set up Label Studio for annotation
- Define taxonomy: head types (pendent, upright, sidewall, concealed, ESFR, dry, residential), deficiencies (paint, corrosion, obstruction, leaking, missing escutcheon, wrong temp)
- Begin labeling target: 500 images annotated by end of Month 1

**Week 3-4: Model V0 Training**
- Train YOLOv8-small on initial dataset (even with 200-300 images + augmentation)
- Establish baseline accuracy metrics
- Export to CoreML, verify inference runs on iPad

**Week 5-8: iOS App Shell**
- Camera pipeline (AVFoundation → frame capture → CoreML inference → overlay)
- Basic UI: inspection list, camera view, detection results
- Local SQLite database for inspections
- Offline-first architecture established

### Phase 2: Core Product (Months 3-4)

**Week 9-12: Model Improvement**
- Expand dataset to 1,000+ labeled images
- Add deficiency detection (separate model or multi-task)
- Temperature rating color classification
- Target: >90% accuracy on head type, >85% on deficiency detection

**Week 13-16: Inspection Workflow**
- Complete inspection workflow (start → scan → confirm → next)
- Building/zone organization
- Inspector override mechanism (confirm/reject AI findings)
- Photo evidence auto-capture with metadata

### Phase 3: Reports & Polish (Months 5-6)

**Week 17-20: NFPA 25 Report Engine**
- Code violation mapping (finding → NFPA 25 section reference)
- PDF report generation (executive summary, per-device detail, photos)
- Report customization (company branding, AHJ-specific fields)
- Digital signature

**Week 21-24: Beta & Launch Prep**
- Beta with 3-5 inspectors at partner companies
- Performance optimization (inference speed, battery usage)
- App Store submission
- Cloud backend deployment (auth, sync, storage)
- Landing page, onboarding flow, billing (Stripe)

## Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| 1 | **Insufficient training data** -- Cannot get 1,000+ labeled sprinkler images in time | MEDIUM | CRITICAL | Pre-negotiate data partnerships before starting. Use synthetic data augmentation. Offer free product to companies that share data. |
| 2 | **Model accuracy too low** -- Below 85% causes inspector frustration and abandonment | MEDIUM | HIGH | Start with high-confidence detections only (show nothing below 90% confidence). Iterate with real-world feedback. Use "suggestion" framing, not "definitive answer." |
| 3 | **iPad camera limitations** -- Poor lighting in mechanical rooms, distance to ceiling heads | MEDIUM | MEDIUM | Support iPad Pro LiDAR for distance estimation. Recommend/provide clip-on lens for zoom. Implement image enhancement preprocessing. |
| 4 | **NFPA compliance errors** -- Generated report contains incorrect code references | LOW | CRITICAL | Hire fire PE to validate every code mapping. Include disclaimer that AI assists but inspector is responsible. Never claim "certified" compliance without third-party audit. |
| 5 | **Apple App Store rejection** -- AR/camera apps face additional scrutiny | LOW | MEDIUM | Follow Apple's Human Interface Guidelines strictly. No background camera use. Clear privacy disclosures. |
| 6 | **Slow adoption** -- Fire protection companies resist new technology | MEDIUM | HIGH | Free trial (30 days). Ride-along demos. Target early adopters identified through NFSA events. Show ROI calculator (time saved × hourly rate). |
| 7 | **Inspect Point builds competing feature** | MEDIUM (18-24 mo) | HIGH | Move fast. Build data moat. Consider partnership/integration rather than pure competition. |
| 8 | **Liability concerns** -- If AI misses a deficiency that causes fire damage | LOW | CRITICAL | Clear terms: AI is assistive tool, inspector retains professional responsibility. Errors & omissions insurance. Never market as "replacement" for human judgment. |
| 9 | **Single-platform risk** -- iOS only limits addressable market | LOW (initially) | MEDIUM | Most inspectors use iPads. Plan Android for Phase 2 (Month 8-12). Use ONNX for model portability. |
| 10 | **Founder has no fire protection domain expertise** | HIGH | MEDIUM | Hire domain expert early (Month 1). Embed with inspection teams. Join NFSA. This is solvable with money and humility. |

## Validation Plan

### Stage Gate Approach

| Gate | Criteria | Timeline | Go/No-Go Decision |
|------|----------|----------|-------------------|
| **Gate 1: Data Feasibility** | Secure 500+ labeled sprinkler images from at least 1 partner | Month 1 | If cannot get data, STOP. The product cannot exist without training data. |
| **Gate 2: Model Viability** | Achieve >85% mAP on sprinkler head detection with 500 images + augmentation | Month 2 | If accuracy is below 70% with augmentation, reconsider approach (maybe different model architecture or more data needed). |
| **Gate 3: On-Device Performance** | CoreML inference <2 seconds per frame on iPad Air 5 | Month 3 | If >5 seconds, need model optimization (quantization, pruning) or simpler architecture. |
| **Gate 4: User Trust** | 3/5 beta inspectors use AI suggestions >60% of the time (vs. overriding) | Month 5 | If inspectors override >80% of the time, accuracy is insufficient or UX needs rework. |
| **Gate 5: Willingness to Pay** | 2/5 beta companies commit to paid subscription ($200+/mo/seat) | Month 6 | If no one will pay, revisit pricing or value proposition. |

### Metrics to Track

- **Model accuracy**: mAP@0.5 for detection, top-1 accuracy for classification
- **Inference speed**: ms per frame on target devices
- **Inspector override rate**: % of AI suggestions accepted vs. rejected
- **Time savings**: minutes per inspection vs. baseline (manual process)
- **Report quality**: % of generated reports accepted by AHJ without revision
- **User retention**: weekly active inspectors / total registered

## Cost & Time Estimate Summary

| Scenario | Timeline | Cost | Notes |
|----------|----------|------|-------|
| **Aggressive (best case)** | 5 months to beta, 6 months to launch | $180K | Data partnership secured quickly, experienced iOS dev available immediately |
| **Realistic** | 6 months to beta, 7 months to launch | $225K | Some data collection delays, 1-2 model iteration cycles needed |
| **Conservative** | 8 months to beta, 10 months to launch | $300K | Data collection takes 3 months, model needs 3+ iterations, iOS dev harder to find |

**Recommendation:** Budget $225K, plan for 7 months, with Gate 1 (data) as the critical path item that should be started immediately (before writing any code).

## Founder-Market Fit Assessment

**Founder profile:** AI/ML infrastructure engineer, deep Python/systems/cloud, no hardware background.

| Dimension | Score | Assessment |
|-----------|-------|------------|
| **ML/AI capability** | 9/10 | STRONG. Can build training pipeline, deploy models, optimize inference. This is the core technical challenge and founder has it covered. |
| **Cloud/backend** | 9/10 | STRONG. FastAPI, PostgreSQL, AWS, CI/CD -- all in wheelhouse. Backend is straightforward for this founder. |
| **iOS/mobile development** | 4/10 | GAP. Will need to hire/contract iOS developer. Founder can architect but not implement the mobile layer. CoreML integration specifically requires Swift expertise. |
| **Fire protection domain** | 1/10 | CRITICAL GAP. Zero knowledge of NFPA 25, sprinkler types, inspection procedures, AHJ requirements. Must be acquired through hiring/partnership. |
| **Go-to-market / sales** | 3/10 | GAP. Enterprise selling to fire protection companies requires industry relationships, trade show presence, and trust-building with a conservative customer base. |
| **Product management** | 7/10 | ADEQUATE. Engineer-founder can build product, but needs domain expert to guide feature prioritization and UX decisions. |

### Key Gaps to Fill

1. **iOS developer** (hire/contract) -- Month 1 priority
2. **Fire protection domain expert** (contract, then advisory) -- Month 1 priority
3. **Sales/BD person with fire protection industry relationships** -- Month 4-5 (before launch)

### Founder Strengths for This Specific Product

- Can personally build the ML pipeline (the hardest, most differentiated part)
- Can architect the system correctly from day 1 (no technical debt from non-technical founders)
- Understands model deployment, inference optimization, CoreML export
- Can evaluate model accuracy rigorously (not fooled by demo-quality results)
- Cloud infrastructure is trivial for this founder

### Honest Assessment

**Founder-market fit is MODERATE (6/10).** The technical core (ML) is a strong match, but the two critical gaps (iOS mobile development and fire protection domain expertise) require significant investment in people. This is a viable founder for this product IF they:
1. Accept they must hire for iOS and domain expertise (not try to learn it themselves)
2. Spend significant time embedded with inspectors in the first 2 months
3. Find a domain expert co-founder or early employee who can be the "fire protection voice"

The founder's ML expertise is rare and valuable -- most fire protection industry people cannot build ML systems. The domain gap is easier to fill (hire an expert) than the technical gap would be (teaching a fire inspector to build ML).
