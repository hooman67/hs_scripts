# Candidate Ledger — Foundry Generative Models hiring

Running record of every candidate reviewed, across batches, so we can compare over time and
detect patterns. Scored against [profile.md](profile.md) (E2E lead · eng+ML in image/video
**generation** · go-getter; hard modality filter on *generation*).

Tiers: **Interview** (top) · **Second** (strong but off-target/adjacent modality or vague gen
evidence) · **Pass** (generation peripheral/absent or thin).

---

## Pre-screen interviews (post-resume-screen outcomes)

*Scores parse/score answers only; the advance/reject decision is Hooman's and is recorded here only
where he actually made one.*

| Candidate | Req/level | Date | Score | Notes (factual) | Hooman's decision | Report |
|---|---|---|---|---|---|---|
| **Wenqi Xian** (ex-Adobe intern) | R161073 — Applied Scientist (non-Staff) | 2026-07-30 | Technical 3/4 · Experience 2/3 · Culture 2/3 → **7/10** | On-modality (Luma Ray 3.2 video-editing gen), first-person-owned data/conditioning/eval detail; correct diffusion/flow/CFG fundamentals, no backwards answers; impact-first motivation. Untested/incomplete: post-training gate stayed textbook (no named reward model), ownership cross-check (individual-vs-team, outcome, train/deploy) not finished, collaborator/initiative not directly asked. | — | `interviews/xian_wenqi_2026-07-30.md` |
| **Yizhi Wang** | R161074 — Staff Applied Scientist | 2026-07-27 | Technical 2/4 · Experience 2/3 · Culture 2.5/3 → **6.5/10** | On-modality (Seedance I2V reference-video gen) with one clearly-owned data-pipeline contribution (retrieval-based training pairs). Technical misses: GRPO near-content-free, cross-attention keys backwards, prompt-adherence vague. Culture: impact-first / product-oriented motivation (70/30 company impact — aligned with team preference), strong self-started initiative; "what broke" story resolved to another team's decoder error. | — | `interviews/wang_yizhi_2026-07-27.md` |
| **Liu He** | R161074 — Staff Applied Scientist | 2026-07-16 | Technical 2/4 · Experience 1/3 · Culture 1/3 → **4/10** | CFG/cross-attention backwards, off-modality flagship project. | **Rejected (Hooman)** | `interviews/liu_he_2026-07-16.md` |

---

## Batch 6 — 2026-07-24 (8 resumes; recruiter batch, ALL tagged "3D", addressed to @vokim first)

**This is Vova's 3D/CG-squad batch, not Hooman's gen roles** — recruiter tag accurate for 7/8.
Scored strict, **proof over claims**. Nobody meets the image/video generation training gate.

| Candidate | Now | Modality (proof) | Gate | Tier |
|---|---|---|---|---|
| **Ahmad Zareei** | Meta Senior RS | ⚠️ adjacent — shipped Ray-Ban VTO **neural-rendering/compositing** (meta.com), NOT diffusion/gen training; core is PDE-sim physics + 3D face recon | ❌ NOT MET (rendering, not gen-model training) | **Second** (only shipped image-synthesis artifact + strong go-getter; discretionary screen only if rendering-adjacent OK) |
| **Rui Zhu** | ByteDance PicoXR RS | ⚠️ adjacent-lite — diffusion-based relighting mentioned but **claim-level only**, no model/method/result; core inverse rendering | ❌ NOT MET | **Pass** |
| **Tom Bu** | Meta RL MLE | ❌ off-target — eye-tracking/calibration/AV perception; one minor 6-yr-old eye-gen challenge (NN, not deep-gen) | ❌ NOT MET | **Pass** |
| **Balakrishnan (Bala) Varadarajan** | Meta Senior Staff (E7) | ❌ off-target — perception/segmentation/trajectory-prediction; "sticker gen" = matting | ❌ NOT MET | **Pass** (excellent perception eng, zero gen) |
| **Ariyan Zarei** | Meta RL RS | ❌ off-target — motion/hand tracking, Codec Avatar reconstruction, point-cloud segmentation | ❌ NOT MET | **Pass** |
| **Hao Li** | Helm.ai RE | ❌ off-target — 3D perception for AV + ranking; PhD petroleum-eng ML | ❌ NOT MET | **Pass** |
| **Leonid Pishchulin** | Amazon Principal AS | ❌ off-target — human pose/shape estimation; thin LinkedIn-export resume (also "awaiting fuller resume") | ❌ NOT MET | **Pass** |
| **Jason Lin** | Google DeepMind RS (GenAI title) | ❌ off-target — VLM/multimodal *understanding* (Gemini encoder/MoE/RLHF); buzzword-dense, unverifiable ownership; prior 3D detection | ❌ NOT MET | **Pass** |

**Batch-6 recommendation:** **Screen none for the gen role.** Entirely Vova's 3D/perception squad.
Only **Ahmad Zareei** is a discretionary maybe (shipped VTO rendering + strong go-getter) but it's
compositing/neural-rendering, not diffusion/gen-model training — a Second, not an interview. Route
the rest to Vova. Reinforces the Batch-5 lesson: recruiter tags ≠ modality; verify by reading.

---

## Batch 5 — 2026-07-08 (9 resumes; recruiter batch tagged by domain)

Scored against v0.2 rubric. Recruiter domain tags were often wrong — most "Multimodal/VLM"
tags = understanding (off-target); "Image/Video Gen" tags needed verification for real *training*
vs. usage/curation.

| Candidate | Now | Modality | Gate | Tier | Note + Slack cross-signal |
|---|---|---|---|---|---|
| **Yu Ding** | Meta Research Engineer | ✅ video diffusion (physics-guided), SFT/post-train + eval | ✅ MET | **Interview — BUT re-tread** | Only on-modality gate-passer in the batch (E2E: data→SFT→eval). ⚠️ **NOT new: already did a full Foundry panel (Feb 2026, P40, 3D-side) — mixed/mid feedback (Vova 6.5, Prathyusha 8, Zhiqin no, Haiting 6), NO offer.** Re-surfaced May as "interviewed well, no offer." **Pull the existing IV feedback before re-interviewing.** |
| **Yanli Liu** | Meta Senior MLE (E5) | ⚠️ adjacent — image-gen *data curation* (Emu/Omni) + training-free diffusion paper (FreeControl); real post-train (CPT/SFT/GRPO) was on generative *recommendation*, not image/video | ❌ NOT MET (for image/video gen) | **Second** | Strongest leadership/go-getter in the batch (0→1 launches, Dept Super Star 4/120). Closest-to-target of the Seconds, but hands-on gen-model training is wrong modality. |
| **Xiaohui Chen** | Meta Research Scientist | ⚠️ adjacent — one T2I diffusion-adapter internship; diffusion pubs are graphs/molecules; current role recsys/MLLM | ⚠️ thin/partial | **Second** | Genuine but dated/thin on-target exposure (one internship); <1yr FT (fresh PhD 2025). Strong publication record. |
| **Kalyan Raman** | Amazon AGI Senior MLE (L6) | ❌ off-target — pure data infra/dedup for Nova gen training data | ❌ NOT MET (no modeling) | **Second** | Superb infra leader + go-getter, but ~zero ML/modeling depth — fails "eng AND ML." Not a modeling-lead fit. |
| **Giang Nguyen** | Meta Reality Labs RS | ❌ off-target — smart-glasses VLM understanding / data synthesis | ❌ NOT MET | **Pass** | Strong engineer/go-getter ($2M saved, 400× throughput) but entirely understanding, zero gen. |
| **Aravind Manoharan** | Amazon AGI Senior MLE | ❌ off-target — curation/dedup for text FMs + VLM/translation | ❌ NOT MET | **Pass** | Solid data-infra engineer; no gen modality, no modeling depth. |
| **Kamlesh Kumar** | Williams-Sonoma Senior SWE | ⚠️ thin — consumes gen APIs (Flux/Veo/Seedance); one Adobe DiT-matting internship | ⚠️ weak (1 internship) | **Pass** | ⚠️ Title-inflation flag: intern→SWE→"Senior" in ~1yr, <1yr total FT. Mostly API integration, not training. |
| **Abhay Mittal** | Meta RE, Multimodal AI | ❌ off-target — detection/scene-graph/JWO perception; current role one vague sentence | ❌ NOT MET | **Pass** | Vague current-role red flag over an off-target perception career. |
| **Hossein Daraei** | Magic Leap Staff RE | ❌ off-target — NeRF/3DGS/SLAM for XR; "diffusion" is a skills-line bullet only | ❌ NOT MET | **Pass** | Strong senior 3D/XR researcher, no generative-media overlap. |

**Batch-5 recommendation:** Only **Yu Ding** clears the gate on-modality — but he's a **re-interview
who already landed mid with no offer**, so pull his prior panel feedback before spending a screen;
a repeat is likely unless his Meta video-diffusion work is genuinely new signal. **Yanli Liu** is
the one Second worth a discretionary screen purely on leadership/go-getter strength (culture-fit
rescue), with eyes open that her hands-on gen training is in the wrong modality. Everyone else is
off-target/infra/understanding — pass. Net: **this batch adds ~0–1 genuinely new interviewables.**

---

## Batch 4 — 2026-07-06 — FULL RE-ANALYSIS of the whole pool (~49 unique resumes in ~/Downloads/hiring_resumes_review_claude)

Re-scored **every** resume in the folder against the **v0.2 rubric** (senior IC/tech-lead · image
AND video equal · training/post-training gate is **method-agnostic** — SFT/distillation/RL all
count · modality filter is a **strong demote, not auto-reject** · culture-fit can rescue an
adjacent candidate to Second). Merges the Batch 1–3 candidates (re-surfaced with refreshed PDFs)
with new names. Cross-checked against the recruiter Slack channel **#tmp-foundry-hiring-2025
(C09H6QJKSKY)** — pipeline status noted in the last column.

### Interview tier — on-modality, all bars, gate met

| Candidate | Now | Gen modality | Gate | Slack pipeline status |
|---|---|---|---|---|
| **Liu He** | Amazon Applied Scientist | ✅ image+video ads gen (Qwen-Image-Edit, Wan2.2 I2V) | ✅ GRPO | ❌ **REJECTED — pre-screened by Hooman 2026-07-16 → 4/10 (Tech 2/4 · Exp 1/3 · Culture 1/3).** Scored on **proof, not claims:** got core conditioning wrong (CFG backwards, cross-attn Q/KV backwards, adaLN missed), no distillation; the only project he actually owned/walked through is video *understanding* not generation (gen work stayed at claim level, individual ownership unclear); motivation lukewarm/opportunistic + couldn't own a real mistake. Do not advance. Full report: `interviews/liu_he_2026-07-16.md`. |
| **Yizhi Wang** | ByteDance (Seedance 1.0/2.0) | ✅ I2V reference-video / identity-preserving generation | ✅ hands-on (data pipeline + customization training) | **Pre-screened 2026-07-27 → 6.5/10.** See the Pre-screen interviews table at the top + `interviews/wang_yizhi_2026-07-27.md`. |
| **Yuanhao Zhai** | Meta RS | ✅ video/image gen, editing (UniGen, Product-in-Use) | ✅ SFT/RL/distill; 56% adoption | ❌ **INTERVIEWED by Hooman (~06-26) → NO.** Lacked the E2E delivery / whole-project leadership we need — strong IC/research contributor, not a project lead. Resume's "led the end-to-end lifecycle" overstated actual ownership. |
| **Seonghyeon Nam** | Meta Senior RS | ✅ I2I post-train, I2V LoRA VFX, lipsync (Vibes) | ✅ SFT/GRPO | **Ajinkya shortlisted → screening** (06-17). |
| **Jiali Duan** | Apple Sr RS, Foundational Diffusion | ✅ 20B+ AV gen; ⚠️ pre-Apple 3D/VLM | ✅ DPO/GRPO | **Ajinkya shortlisted → screening** (06-17). |
| **Shamit Lal** | Amazon Nova Sr Applied Scientist | ✅ Nova Canvas/Reel/Titan (T2I/I2I/I2V/edit) | ✅ SFT/DPO/RLHF; 1B→30B; beat Flux2 Pro | **Ajinkya shortlisted → screening** (06-17). Prior Vova prescreen 7/10 "maybe covered in that space" (Feb). Amazon Nova caveat. |
| **Matan Goldman** | Meta GenAI | ✅ post-training pipeline for DiT T2I/I2I/I2V | ✅ pipeline owner + RLHF/distill | **Being interviewed** (assigned to Purvak Lapsiya, scheduled). |
| **Fangzhou Mu** | Meta Superintelligence Labs (video gen) | ✅ building native video gen; PhD GLIGEN/FreeControl | ✅ adapter fine-tuning | **Prior ASML OFFER (late 2025)**, re-engaged; **screen w/ Hareesh Ravi**. |
| **Haolin Jia** | Google Core ML SWE | ✅ Imagen 3 nano, Veo distill, MobileDiffusion editing | ✅ distillation/post-train | ⚠️ **Submitted 06-19, NOT yet picked up — Hooman should request.** |
| **Sriharsha Sammeta** | Apple Senior MLE (now "Independent Researcher") | ⚠️ ONE gen project (Image Playground: on-device diffusion + LoRA guardrails) amid an otherwise off-target Siri/location/ranking/agentic/VLA career | ⚠️ gate technically met via that one project only | ~~Interview~~ → **PASS (corrected 2026-07-14)** | **CORRECTION:** a memory-less Batch-4 reviewer flipped him from his Batch-3 **Pass** to Interview on the strength of the single Image Playground bullet + "beat DALL-E"; I failed to reconcile against the prior Pass and wrongly listed him "worth requesting." Real read: gen = 1 shared project of ~1yr; center of gravity is Siri/location/ranking/agentic/robotics; current role is independent paper-reimplementation (self-study, not shipping). **Do not request. Pass — marginal Second at most.** |
| **Mehmet Saygın Seyfioğlu** | Amazon (Nova Canvas VTO lead) | ✅ VTO / Diffuse-to-Choose (image gen/edit) | ✅ RL post-train on shipped model | ❌ **PASSED — requires O1 sponsorship (~6mo transfer); Ajinkya declined 06-12.** Skills = clear interview; killed on visa timeline only. |

### Interview / Second boundary — genuine 2D gen work but current center is 3D-adjacent (Vova is pulling both for the 3D squad, not this gen role)

| Candidate | Now | Note | Slack |
|---|---|---|---|
| **Kai-Hung Chang** | Moonlake AI (MTS) | Diffusion+GAN+LoRA+ControlNet, 0→1 founder (DateSmart); current role 3D/agentic gen | **Vova requested screen** (07-02); Ben setting up. |
| **Konstantinos-Nektarios Lianos** | Waymo (ex-Geomagical/IKEA) | Diffusion image editing/inpainting shipped at IKEA scale; founding tech lead; current Waymo AV-sim | **Vova requested prescreen** (05-31, 3D squad). |

### Second tier — adjacent modality / vague-gen / gate or tenure concern, rescued by culture/go-getter

| Candidate | Now | Why Second |
|---|---|---|
| **Tao Hu** | Stability AI RS | Real video-diffusion post-training, but pubs are 3D-human gen. **Vova requested prescreen (3D squad).** NeurIPS'26 AC. |
| **Nikolaos Sarafianos** | Meta Staff RS | 3D world/asset gen (AssetGen/TextureGen/WorldGen), shipped; training evidence generic. **Vova requested prescreen.** |
| **Numair Khan** | Meta RS | Diffusion video/3D-gen (LaVR CVPR'26) + self-pitched Project Portall, but career core is 3D reconstruction. |
| **Xiaoxu Meng** | Meta RE (Codec Avatar) | Video-gen module + image-to-3D generative system amid mostly-reconstruction pubs. **Vova: potential backup 3D-squad tech lead.** |
| **Minh P. Vo** | SpreeAI Head of Eng | Founder-level VTO impact ($12M→$1.5B), but own IC gen depth asserted at team level; pubs are 3D recon. |
| **Lelin Zhang** | ByteDance Staff SWE | On-modality video gen (Seedance) but gate thin — bullets are inference/serving optimization, not training ownership. **Ajinkya shortlisted (06-17).** |
| **Jeanne Vu** | Meta Imaging Scientist | Real generative-fill lighting-estimation w/ E2E ownership, but one project in an off-target imaging/perception career. |
| **Lezi Wang** | Meta Senior RS | Textbook E2E owner + strong culture, but DiT work is motion synthesis, not image/video pixels. |
| **Junming Chen** | Meta AI RS | Diffusion motion/gesture gen (DiffSHEG) + 3D-object gen; adjacent + brand-new industry tenure (<1yr). |
| **Hamid Izadinia** | Amazon Sr AS | Repeat vague-gen pattern (Batch 3): SFT/RLHF/GRPO/DPO buzzwords, zero first-author gen pubs. **Probe screen, not auto-interview.** Amazon caveat. |
| **Filip Marić** | Meta AI RS | Strong E2E (shipped XR-Poser, led AI pod) but motion/pose gen for AR/VR, not image/video. |
| **Haochen Zhang** | Amazon AGI AS | Gen work is a Meta GenAI internship (WACV'26); gate now MET via internship, but <1yr FT new-grad. Amazon caveat. |
| **Bindita Chaudhuri** | Flawless Sr AS/Manager | Some I2V/T2V slices, but core is 3D face/body recon, gate unmet, now people-manager (target is IC). |
| **Savinay Nagendra** | Meta RS | Off-target core (moderation/rec) + only old MoCoGAN intern gen work, but exceptional competition/award record rescues to Second. |
| **Dongseok Shim** | Sony RS | Diffusion hands-on scattered across depth-estimation/short internships; strong pubs, weak E2E + <1yr tenure. |
| **Peiye Liu** | TikTok Senior RS | First-author diffusion/RL-for-editing pubs, but job duties are LLM/rec infra (disconnect). ❌ **Ajinkya explicitly rejected — "poor resume, filter out" (06-09).** |

### Pass — generation peripheral/absent, off-domain core, or thin

Hao Yang (Amazon, multimodal understanding) · Jun Seok Lee (Meta, recsys/commerce) · Laurent Guigues (Amazon JWO, tracking/3D-recon) · Michael Padilla (Inworld, audio/speech TTS gen — wrong medium) · Chenchen Zhu (Meta, perception/VLM/SAM) · Tao Wu (TikTok, moderation/embeddings) · Zhicheng Yang (PAII, medical VLM/detection) · Zitian Chen (Xpeng, AD VLA; unedited placeholder on resume) · Tian Cao (Apple, multimodal understanding/RAG; thin) · Yen-Cheng Liu (Niantic, SLAM/AR; thin) · Yang Liu (Waymo, AD perception) · Namrata Parikh (Standard AI, retail CV) · Neil Rodrigues (Wyze, ReID/edge) · Suchismita Padhy (Log10, TTS/recsys; unbacked gen claim) · Chelhwon Kim (Sony, localization/HCI; unbacked gen claim) · Mohammad Farazi (VW, GUI-agent + AD 3DGS) · Yajie Yan (Meta RL, 3D geometry/perception) · Chen Tang (AbbVie, biomedical/geophysics imaging) · Deep Doshi (Valeo, AD perception) · Noranart Vesdapunt (Amazon Principal, detection/reID) · Ardalan Mehrani (TikTok Staff, VLM T&S/perception).

**Batch-4 recommendation (for Hooman's gen role):** Interview-first, on-modality, all bars —
**Liu He · Yuanhao Zhai · Seonghyeon Nam · Jiali Duan · Shamit Lal · Matan Goldman · Fangzhou Mu**,
plus the **one** not-yet-in-pipeline pick worth proactively requesting: **Haolin Jia**.
(**Sriharsha Sammeta** was previously listed here in error — corrected to Pass 2026-07-14; see his
row.) **Mehmet** is a skills-clear interview but is already dead on O1
sponsorship. **Kai-Hung Chang / Lianos** are strong but 3D-adjacent and Vova is already pulling
them for the 3D squad. Leadership steer to weigh: Ajinkya has said to look beyond Amazon
AGI/Nova (affects Liu He, Shamit Lal, Hamid, Haochen, Hao Yang).

---

## Batch 3 — 2026-06-25 (resumes in ~/Downloads/hiring_resumes_review_claude)

Ranked against the **sharpened** rubric: senior IC/tech-lead · image AND video equal · prefer 2+
yrs shipping · **RL post-training (GRPO/DPO/RLHF) is a hard gate.**

| Candidate | Now | Gen? | RL post-train? | Tenure | Tier | One-line |
|---|---|---|---|---|---|---|
| **Liu He** | Amazon Applied Scientist | ✅ image+video (I2V/edit) | ✅ GRPO central | ~2 yrs | **Interview 🥇** | Led full-stack video/image gen + GRPO post-training; prolific research. Clears every gate. |
| **Yuanhao Zhai** | Meta Research Scientist | ✅ core image+video | ✅ RL in lifecycle | <1 yr ⚠️ | **Interview 🥈** | Owns E2E lifecycle, 56%/58% adoption lifts, distillation+RL. Elite, but PhD finished Jun'25 — below 2yr pref; flag tenure. |
| **Hamid Izadinia** | Amazon Sr Applied Scientist | ⚠️ claimed image/video/3D | ✅ SFT/RLHF/GRPO/DPO | 8+ yrs | **Interview (probe) 🥉** | Elite pedigree + go-getter + explicit RL post-training + deep tenure. Probe whether he's *owned* gen E2E — gen language is vague ("contributed/collaborated"), first-author depth is 3D recon. |
| **Haolin Jia** | Google Core ML (SWE) | ✅ image+video (Imagen/Veo) | ❌ none (distill/on-device) | 4 yrs | **Second** | Shipped Imagen 3 nano/Veo distill/MobileDiffusion editing. Strong tenure+modality, but **no RL post-training** (the gate) and MS/builder not research-lead. |
| **Kai-Hung Chang** | Moonlake AI (MTS) | ⚠️ 3D/agentic gen | ❌ | strong | **Second** | Excellent go-getter/founder/E2E leader, but 3D + agentic-3D gen, no RL post-training. |
| **Hao Yang** | Amazon Principal Applied Scientist | ⚠️ understanding-leaning | ✅ Nova RL | strong | **Second** | Principal; Nova multimodal RL — but focus is understanding/embeddings, and role is IC not manager. ATS-tagged "Sr Mgr ASML–Firefly". |
| **Chenchen Zhu** | Meta AI Research Scientist | ❌ perception | ⚠️ GRPO on VLM | strong | **Second** | Perception encoders/VLM/SAM, not generation; RL is on understanding models. |
| **Sriharsha Sammeta** | Apple Senior MLE | ⚠️ one slice | ❌ | strong | **Pass** | Gen = one project; core is Siri/location/agentic/VLA. No RL-on-gen. |
| **Yang Liu** | Waymo Senior Research Scientist | ❌ AD perception | ❌ | strong | **Pass** | Strong scientist, but autonomous-driving perception. Wrong modality. |
| **Tian Cao** | Apple Staff MLE | ❌ understanding | ❌ | strong | **Pass** | Multimodal understanding/RAG + old medical CV. ATS-tagged "Applied Scientist–Firefly (Eric)". |
| **Neil Rodrigues** | WYZE Senior Applied Scientist | ❌ detection/edge | ❌ | ~4 yrs | **Pass** | ReID/EdgeAI/detection. No generation, no RL post-train. |
| **Haochen Zhang** | Amazon AGI Applied Scientist | ⚠️ adjacent (conv. image-gen) | ❌ | <1 yr ⚠️ | **Pass** | Conversational image-gen intern work + med-image diffusion + SR; core is data pipelines/restoration. Fails tenure + RL gates. |

**Batch-3 recommendation:** Interview **Liu He** (#1 — clears every gate, GRPO post-training
central) and **Yuanhao Zhai** (#2 — strongest gen profile, but flag the <1yr tenure vs. your 2+yr
preference). Add **Hamid Izadinia** as a probe-interview (clears RL + tenure gates, elite pedigree;
verify he's *owned* generation E2E rather than contributed). **Haolin Jia** is the strongest miss —
directly shipped image+video gen with great tenure, but knocked out of the top by the RL-post-training
gate; reconsider if RL weight relaxes.

---

## Batch 2 — prior (resumes in ~/Downloads/resumes_review_2)

| Candidate | Now | Tier | One-line |
|---|---|---|---|
| **Shamit Lal** | Amazon Nova Sr Applied Scientist | **Interview 🥇** | Best all-around; full lifecycle Nova Canvas/Reel; lowest-risk shipper. |
| **Jiali Duan** | Apple Foundational Diffusion | **Interview 🥈** | E2E pre/post-train of 20B+ AV gen on 1K+ GPUs; research-leaning frontier lead. |
| **Seonghyeon Nam** | Meta Senior RS | **Interview** | Production diffusion post-training specialist (I2I→prod, I2V LoRA VFX, lipsync). |
| **Lelin Zhang** | ByteDance/TikTok Staff SWE | **Conditional** | Engineering powerhouse (Seedance I2V/T2V, 10K+ GPUs); lighter on novel-model training. |
| **Numair Khan** | Meta Reality Labs RS | **Second** | Strong go-getter/E2E, but 3D/neural-rendering-leaning. |
| **Xiaoxu Meng** | Meta Codec Avatar RS | **Second** | More 3D reconstruction than generation. |
| **Bindita Chaudhuri** | Flawless Sr AS/Mgr | **Weak** | Niche lip-sync/3D-face/human. |
| **Savinay Nagendra** | Meta RS | **Weak** | Gen work thin; understanding/segmentation/rec; most junior. |
| **Jun Seok Lee** | Meta RS | **Weak** | Commerce/recommendation/causal-inference. |
| **Deep Doshi** | (Master's) | **Weak** | Autonomous-driving perception/VLM. |

## Batch 1 — prior (resumes in ~/Downloads/resumes_review)

| Candidate | Now | Tier | One-line |
|---|---|---|---|
| **Fangzhou Mu** | Meta Superintelligence Labs | **Interview 🥇** | All three bars hard + directly I2V; ex-NVIDIA eng + CVPR×6 researcher. |
| **Mehmet Saygın Seyfioğlu** | Amazon (Nova Canvas VTO lead) | **Interview** | Strongest pure image-gen builder; RL post-training. |
| **Matan Goldman** | Meta GenAI | **Interview** | Strongest eng/E2E for the modality (T2I/I2I/I2V post-training to prod); safest shipper. |
| **Noranart (Sol) Vesdapunt** | Amazon Principal | **Second** | Excellent E2E, but understanding/detection/3D-face. |
| **Lezi Wang** | — | **Second** | Strong E2E+go-getter, but 3D motion synthesis. |
| **Ardalan Mehrani** | Staff | **Second** | Best people-leadership/scale, but VLM understanding/T&S. |
| **Peiye Liu** | — | **Pass** | Infra/efficiency; only peripheral diffusion. |
| **Suchismita Padhy** | — | **Pass** | Thin/generic; ETL core; unbacked gen claims. |

---

## Process guardrails (learned the hard way)

- **Always reconcile a re-analysis against the candidate's PRIOR verdict.** Parallel per-resume
  reviewers have no cross-batch memory and will re-score in isolation. Sriharsha Sammeta got
  flipped Batch-3 `Pass` → Batch-4 `Interview` purely because a fresh reviewer weighted his single
  Image Playground bullet against the softened method-agnostic gate. **If a tier changes across
  batches, state why explicitly and sanity-check it — don't let a silent flip through.**
- **"Gate technically met" ≠ interview-worthy.** One shipped gen project on an otherwise off-target
  career (Siri/location/ranking/agentic) clears the method-agnostic gate on a technicality but
  still fails the "strong eng AND ML *in generation*" + E2E-ownership bars. Weight center-of-gravity
  of the career, not the single closest bullet.
- **Check the CURRENT role.** "Independent Researcher / paper reimplementations" = self-study, not a
  shipping role; treat as a tenure/seriousness flag, not as gen experience.

## Patterns observed (update as the pool grows)

- **Generation modality is the decisive filter.** Across all 3 batches, every Principal/Staff
  candidate whose core was understanding/perception/3D/AD got demoted to Second/Pass. Title and
  scale do not rescue an off-modality candidate.
- **The winning archetype:** direct image/video generation + owned E2E lifecycle with shipped
  adoption/impact metrics + eng-and-research combo (Fangzhou Mu, Shamit Lal, Yuanhao Zhai).
- **Common near-miss:** strong leader/go-getter in an *adjacent* generation modality — 3D,
  motion synthesis, agentic-3D (Kai-Hung Chang, Numair Khan, Lezi Wang). Great people, wrong target.
- **Vague-gen yellow flag:** senior candidates who *claim* image/video gen but whose first-author
  depth is elsewhere, with "contributed/collaborated" hedging (Hamid Izadinia).
- **Apple on-device pull:** several Apple candidates ship to millions but generation is one slice
  of a systems/Siri/location career (Sriharsha Sammeta, Tian Cao).
- **ATS cross-signal:** Adobe Firefly recruiting is already tagging some of these candidates
  (Hao Yang → Sr Mgr ASML–Firefly Research; Tian Cao → Applied Scientist–Firefly). Worth
  reconciling picks against the existing pipeline each batch.
- **Candidates recur across batches with refreshed resumes.** Batch 4 re-surfaced 7 of 10
  candidates already in the ledger (Liu He, Seonghyeon Nam, Jiali Duan, Hamid Izadinia, Haochen
  Zhang, Bindita Chaudhuri, Deep Doshi) under new filenames/PDF exports. Always read full content,
  not just filenames, to catch duplicates — one file (`CV20260217_R_1073u2o7e8y2u8.pdf`) had no
  name hint at all and turned out to be Haochen Zhang.
- **The v0.2 rubric softening (method-agnostic gate + modality-demote-not-reject) moved exactly
  one candidate's gate status** (Haochen Zhang: gate now MET via internship SFT work, still
  demoted on tenure) but **zero candidates crossed a tier boundary** — the hard-gate winners and
  off-domain passes from Batch 2/3 held under the new rubric.
- **3D-human generation is a recurring near-miss shape distinct from 3D reconstruction.**
  Tao Hu (StructLDM/SurMo/FashionEngine) is 3D-human *generation* (diffusion-based), not pure
  reconstruction — still demoted to Second because the role's bar is 2D image/video, but this is
  a slightly different miss pattern than the Kai-Hung Chang/Numair Khan 3D-adjacent misses in
  Batch 3, worth distinguishing if the role ever broadens to include 3D avatar generation.
- **"Vague gen claims + elite pedigree" is now a repeat pattern for one specific candidate**
  (Hamid Izadinia, seen in both Batch 3 and Batch 4 with the same hedged language and zero
  first-author gen publications) — worth resolving via an actual probe screen rather than
  re-litigating from the resume each batch.
