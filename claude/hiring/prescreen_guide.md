# Pre-Screen Guide — Foundry Generative Models (Hooman's 30–40 min screen)

> Hooman runs this screen before the 5-round panel (see `interview_process.md`). Structure:
> **10 min technical · 10 min experience · 10–20 min culture fit.** Score against `profile.md`
> (E2E lead · eng+ML in image/video **generation** · go-getter; culture fit can outweigh a
> slightly-off skillset). Deeper coding is the panel's job — this is a calibration screen.

## Before you start (2 min)
- One line on the role: senior IC / tech-lead who owns a generation project end-to-end.
- Ask what they'd call their core strength (gen research? training systems? post-training?) and
  **calibrate the technical questions to that** — then probe one level deeper than they're comfy.
- Take notes verbatim per the review format: **every Q + their answer, a /10, hire/no-hire for
  the level, notes.** You'll reuse these notes to write the panel brief.

---

## Part 1 — Technical (10 min)

Pick **~3**: one warm-up fundamental, one on the **training/post-training gate**, one debugging.
These are verbal — ask them to sketch/whiteboard if remote. Goal is depth of real hands-on
understanding, not trivia. (Deeper coding — attention/RoPE/softmax from
`~/Downloads/interview_questions.ipynb` — is reserved for the panel coding round.)

**A. Diffusion/flow fundamentals (warm-up)**
- "Walk me through what a diffusion model actually learns — forward vs. reverse process, and
  what the network predicts (ε / x₀ / v)." → then: "DDPM vs. flow-matching / rectified flow —
  what changes and why do we care about it for few-step sampling?"
- 🟢 Explains objective crisply, knows the prediction-target trade-offs, connects to sampling.
- 🔴 Hand-waves "it denoises," can't say what the loss is on, only knows the API.

**B. Post-training & the gate (ASK EVERYONE — this is the hard gate)**
- "SFT vs. preference optimization (DPO) vs. RL (RLHF/GRPO) vs. distillation for a T2I/T2V model
  — when do you reach for each, and what do you actually need to run each one?"
- Follow-up: "Where does the **reward / preference signal** come from for an image or video
  model, and what goes wrong with it?" (reward hacking, aesthetic vs. alignment, eval noise)
- 🟢 Has personally run at least one; can talk data/compute cost, failure modes, eval. Method
  is secondary — depth of hands-on is what you're checking.
- 🔴 Only names techniques; can't describe building the signal or a run they did.

**C. Conditioning & guidance (architecture depth)**
- "How does text conditioning enter a diffusion transformer — cross-attention vs. adaLN? What is
  classifier-free guidance and what breaks at high CFG?" (oversaturation, artifacts, diversity loss)
- 🟢 Concrete, has tuned this. 🔴 Textbook-only.

**D. Sampling acceleration / deployment (great for the "shipped it" claim)**
- "You have a 50-step model; product needs 1–4 steps at interactive latency. Options and
  trade-offs?" (distillation, consistency/LCM, guidance distillation, quantization, caching)
- 🟢 Knows quality/latency trade-offs from experience. 🔴 Only "use fewer steps."

**E. Debugging (best signal for real practitioners)**
- "Your T2I model gives blurry / mode-collapsed / prompt-ignoring outputs. How do you diagnose,
  in order?" (data → conditioning → loss/schedule → CFG → eval harness)
- 🟢 Systematic, isolates variables, has war stories. 🔴 Guesses randomly.

*Optional systems depth (only if they claim training-infra strength):* numerically stable softmax /
mixed-precision in attention; why RoPE encodes **relative** position; sharding a big DiT run.

---

## Part 2 — Experience (10 min) — *the E2E-ownership probe*

> **Why this matters:** a resume that says "led the end-to-end lifecycle / X% adoption lift" can
> mask a strong-IC-but-not-project-lead (this is exactly why Yuanhao Zhai screened out). Verify
> real ownership; don't take the bullet at face value.

**The "one project" drill (spend most of the 10 min here):**
1. "Pick the project you consider **most your own**. Take me from the initial problem to what
   shipped." Let them talk, then drill:
2. **Whose idea was it?** Who decided the architecture / data strategy / eval?
3. "Draw the full pipeline — data → training → post-training → eval → deployment — and mark which
   boxes **you personally owned end-to-end**, which you **collaborated** on, which you **handed off**."
   → This one question separates a project lead from a strong contributor.
4. "What broke, and how did you personally unblock it?" (technical + cross-team)
5. "What was the measurable outcome — and how do you know **your** part caused it?"
6. "Who else was on it, and what did they do?" (cross-check the ownership story)

- 🟢 Owns decisions under ambiguity, drove data/train/post-train/deploy, can attribute impact,
  generous about naming teammates while still clearly the driver.
- 🔴 "We" with no "I"; owned one component (e.g. just the distillation, just a paper) but frames
  it as leading the whole thing; can't explain decisions outside their slice; vague on outcome.

**Scale/scope quickies:** biggest model (params) & GPU count they've driven; largest dataset;
latency/throughput or adoption numbers they're proud of.

---

## Part 3 — Culture fit (10–20 min)

> Screen for: **collaborator · listens · responsible · takes initiative.** Per `profile.md`,
> strong culture fit can outweigh a slightly-off skillset; a strong-skills candidate who **can't
> listen / doesn't own failure / is dismissive is a NO** unless you believe it's coachable.
> Some of this you score from *how they've behaved in the screen itself*, not just their answers.

**Collaborator**
- "Tell me about a technical disagreement with a peer or a partner team. How did it resolve?"
- 🟢 Sought to understand the other view, changed their mind at least once, kept the relationship.
  🔴 "They were wrong"; steamrolled; only wins.

**Listens (score live + one question)**
- Live signal: do they answer the question you actually asked? Build on your follow-ups? Ask
  clarifying questions before answering a vague prompt?
- "A time real feedback changed your technical approach — what was it and what did you do?"
- 🟢 Concrete example, integrated it. 🔴 Can't recall one; treats feedback as obstacle.

**Responsible / owns outcomes**
- "Something you shipped broke, or a project slipped. What did you do?"
- 🟢 Owns it, root-causes, fixes the system, no blame. 🔴 Blames team/manager/data; passive.

**Takes initiative (go-getter)**
- "Something you started that nobody asked you to do" — bonus if it grew the team/org investment,
  or you convinced leadership to fund it."
- 🟢 Self-started 0→1, pitched up, competition/challenge wins, intern→lead conversions.
  🔴 Only executes assigned work.

**Motivation (2 min):** "Why Firefly / generative media, and what do you want to own next?"
- 🟢 Wants to lead a gen project E2E; excited about the modality. 🔴 Generic "big models"; or only
  wants pure research with no shipping appetite.

---

## Wrap & scoring (per interviewer review format)

For each of the three parts, write: questions asked + their answers (notes), the part score, and a
one-line read. Then an overall **hire / no-hire for the intended level**, with the deciding factor.
**Scoring: Technical /4 · Experience /3 · Culture /3 → total /10.**

| Part | Score | Notes |
|---|---|---|
| Technical (gen depth + gate) | / 4 | |
| Experience (real E2E ownership) | / 3 | |
| Culture (collaborate/listen/own/initiate) | / 3 | |

**Advance decision rules of thumb:**
- Clear yes → all three solid, real E2E ownership, on-modality gen depth.
- **Skills a bit off but strong culture + initiative → advance** (screen is where we rescue these).
- **Strong skills but weak culture (can't listen / won't own failure / dismissive) → no**, unless
  you explicitly believe it's coachable — say so in the notes.
- **Strong senior IC = the bar for "project lead"** (they're the same to Hooman). A strong senior
  IC who can't lead a whole project *immediately* is still a **yes** (leadership grows; IC depth
  can't be faked). A would-be "lead" who is **not** a strong senior IC is a **no**. The Yuanhao
  pattern to catch = ownership that's really slice-level contribution dressed as E2E leadership —
  that fails the *IC-depth* bar, not a title bar.
