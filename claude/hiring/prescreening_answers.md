# Pre-Screen Answer Key — Foundry Generative Models

> Companion to `prescreen_guide.md`. Model answers + what to listen for, so you can calibrate a
> candidate's depth in a 10-min technical without being a diffusion specialist yourself. You don't
> need every point below — use them to tell **"has actually trained/shipped gen models"** from
> **"read the papers / used the API."** Depth-of-hands-on is the signal; exact vocabulary is not.

---

## Part 1 — Technical: model answers

### A. Diffusion / flow fundamentals

**Model answer.**
- **Forward process:** progressively add Gaussian noise to a clean image over many steps. Thanks
  to the closed form, you can jump to any noise level in one shot:
  `x_t = √(ᾱ_t)·x_0 + √(1−ᾱ_t)·ε`, where `ᾱ_t` decreases with t.
- **Reverse process:** a network learns to *undo* one step of noising, conditioned on the timestep
  (and text/image conditioning). Sampling = start from pure noise, denoise iteratively to an image.
- **What the network predicts:** usually the **noise ε** (ε-prediction, DDPM default). Alternatives:
  **x₀-prediction** (predict the clean image) and **v-prediction** (`v = α_t·ε − σ_t·x_0`).
  v-pred behaves better across noise levels and at high resolution, and is common for distillation.
- **Loss:** simple MSE on the target, e.g. `E‖ε − ε_θ(x_t, t, c)‖²`.
- **DDPM vs. flow-matching / rectified flow:** flow-matching learns a **velocity field** that
  transports noise → data along a probability path; **rectified flow** makes those paths nearly
  **straight**, so you need **far fewer sampling steps** and training is more stable. This is the
  **modern default** — SD3 and FLUX use rectified-flow / MMDiT, not classic DDPM. (Score-based
  diffusion and flow-matching are two views of the same underlying idea.)

**Strong answer sounds like:** picks a prediction target and says *why* (v-pred for high-res/
distillation), knows rectified flow is why step counts dropped, connects the loss to the target.
**Weak / red flag:** "it removes noise" with no idea what the loss is on; thinks it's a GAN;
only knows `pipe(prompt)`; can't say what conditioning `c` is or how it enters.

---

### B. Post-training & the gate *(ask everyone — this is the hard gate)*

**Model answer — the four levers and when to reach for each:**
- **SFT (supervised fine-tuning):** fine-tune on a curated set of high-quality (prompt, image/video)
  pairs. Use it to set a **quality/style/domain baseline**. Cheapest & most stable; risk = mode
  narrowing / overfitting; **everything depends on data curation.**
- **DPO / preference optimization (Diffusion-DPO):** train on **preference pairs** (winner vs. loser
  for the same prompt). Directly optimizes relative preference, **no separate reward model**. Use
  it to nudge aesthetics/prompt-adherence when you have paired preference data.
- **RL (RLHF / PPO / GRPO / DDPO):** optimize the sampler against a **reward model**. **GRPO** =
  group-relative: sample a *group* of outputs per prompt, normalize rewards within the group as the
  advantage (no separate critic). Use it for harder preference/alignment objectives; costs more
  compute and is less stable.
- **Distillation:** compress a many-step teacher into a **few-step student** (progressive
  distillation, consistency models / LCM, guidance distillation, adversarial/DMD). This is for
  **latency**, not primarily quality.

**Where the reward/preference signal comes from (the follow-up):** human preference labels, or
automated proxies — **HPS, PickScore, ImageReward, aesthetic predictors, CLIP/prompt-alignment,
VQA-as-a-judge** — or a trained reward model. **Failure modes:** **reward hacking** (over-saturated,
over-smoothed, "fried" images that game the metric), reward model going out-of-distribution,
**diversity collapse**, and noisy/misaligned proxy vs. true human preference.

**Strong answer sounds like:** has personally run at least one, and volunteers the *practical* pain
— building the preference/reward data, reward hacking, eval noise, keeping diversity. Method choice
is secondary; **hands-on depth is what clears the gate.**
**Weak / red flag:** lists the acronyms but can't describe building the signal or a run they did;
conflates SFT with RL; thinks distillation improves quality. **Gate NOT MET if they've only
consumed/served/prompted gen models** — usage ≠ training/post-training.

---

### C. Conditioning & guidance

**Model answer.**
- **How text enters:** **cross-attention** (text tokens from T5/CLIP as keys/values, image latent
  tokens as queries) — classic UNet/SDXL. Or **adaLN / adaLN-zero** (DiT), where a pooled text+time
  embedding modulates the LayerNorm scale/shift. Modern **MMDiT** (SD3/FLUX) runs **joint attention**
  over concatenated text+image tokens so both streams attend to each other.
- **Classifier-free guidance (CFG):** at inference, compute a conditional and an **unconditional
  (null-text)** prediction and extrapolate: `ε = ε_uncond + w·(ε_cond − ε_uncond)`. Higher `w` =
  stronger prompt adherence, less diversity. Enabled by **dropping conditioning ~10%** during training.
- **High-CFG failure modes:** **oversaturation / blown-out contrast, artifacts, reduced diversity.**
  Mitigations: **dynamic thresholding** (Imagen), **CFG rescale**, **limited-interval guidance**
  (only guide in a mid-noise band), or just lower `w`.

**Strong answer:** knows more than one conditioning mechanism, knows CFG needs training-time
conditioning dropout, has actually seen and fixed the oversaturation failure.
**Weak / red flag:** "you put the prompt in"; thinks CFG is a training loss; never tuned guidance.

---

### D. Sampling acceleration / deployment

**Model answer.**
- **Better samplers first (train-free):** DPM-Solver++, UniPC, DEIS → good quality at ~20 steps.
- **Distillation for 1–4 steps:** progressive distillation, **consistency models / LCM**, **guidance
  distillation** (fold CFG into the model), **adversarial distillation** (ADD/SDXL-Turbo, **DMD/DMD2**,
  LADD); **reflow** for rectified-flow models.
- **Systems levers:** quantization (fp8/int8), **caching** (DeepCache/TeaCache), TensorRT, distilling
  the VAE decoder, flash-attention.
- **Trade-offs:** fewer steps → **quality/diversity loss, texture degradation, mode collapse**;
  adversarial methods add sharpness but bring **training instability**.

**Strong answer:** separates train-free samplers from distillation, names the quality/latency
trade-off from experience. **Weak / red flag:** only "use fewer steps" or "buy more GPUs."

---

### E. Debugging (best signal for real practitioners)

**Model answer — diagnose in order, isolate one variable at a time:**
- **Blurry:** check the **VAE decode** first; then over-smoothing from **too-high CFG**, LR/EMA
  issues, undertraining, or **noise-schedule/resolution mismatch** at high res (need SNR shift /
  **zero-terminal-SNR**); or **over-distillation**.
- **Mode collapse / same-looking outputs:** **reward hacking** from over-optimized RL/DPO, **LoRA
  overfitting**, too-narrow SFT data, or guidance too high.
- **Prompt-ignoring (poor alignment):** verify **CFG is actually on** and conditioning-dropout isn't
  too high; check **caption quality** in training data (dense re-captioning is often the fix); token
  truncation; inspect **cross-attention maps** to see if it attends to the right tokens; does the
  **base model** do it (isolate fine-tune vs. base)?

**Strong answer:** methodical, forms a hypothesis and isolates it, has war stories ("re-captioning
the dataset fixed our prompt adherence"). **Weak / red flag:** random guessing, jumps to "train
longer," no notion of isolating the cause.

---

### Optional systems depth *(only if they claim training-infra strength)*

- **Numerically stable softmax:** subtract the max before exp — `softmax(x) = softmax(x − max(x))` —
  because `exp(1000)` overflows in fp16/fp32. (This is Q1c of the reference notebook.)
- **Why RoPE is *relative*:** rotating query at position *m* and key at position *n* makes their dot
  product depend only on `(m − n)` — the rotation matrices compose as `R_mᵀ R_n = R_{n−m}` — so the
  attention logit sees only the **relative offset**, not absolute positions.
- **Sharding a big DiT / video model:** FSDP/ZeRO for params+optimizer states (data parallel),
  **tensor/sequence parallelism** for large activations (long video-token sequences), activation
  checkpointing, bf16 mixed precision, flash-attention. Sequence parallel across frames for video.

---

## Part 2 — Experience: what I'm listening for

The one thing to verify: **is this a strong senior IC (= our bar for a lead), or a slice-level
contributor with lead-sounding bullets?** (See profile decision #1 and the Yuanhao pattern.)

- 🟢 **Owns decisions, not just tasks.** Chose the architecture/data/eval strategy; can explain *why*
  and what they'd do differently. Drove data → training → post-training → eval → deploy, even if they
  didn't personally write every line. Attributes impact honestly ("my part was X; the adoption number
  came from the whole surface"). Names teammates generously **and** is still clearly the driver.
- 🟢 **A strong IC who hasn't formally "led" yet is still a yes** — depth + ownership instinct matter
  more than a title. Don't down-rank for lacking a lead label.
- 🔴 **Slice dressed as leadership:** "led the end-to-end lifecycle" but under drilling only owned one
  component (just the distillation, just a paper, just the eval); can't explain choices outside their
  slice; all "we," no "I"; vague on the outcome or how their piece caused it. **This fails the
  IC-depth bar** — it's what screened Yuanhao out.
- 🔴 **Manager-only:** coordinated people but no recent hands-on depth. Not our bar.

---

## Part 3 — Culture: what I'm listening for

Score partly from **how they behave in the screen itself**, not just their stories. Culture fit can
**outweigh a slightly-off skillset**; strong skills + bad culture (can't listen / won't own failure /
dismissive) is a **no** unless you explicitly believe it's coachable.

- **Collaborator** — 🟢 genuinely engaged an opposing view and *changed their mind* at least once;
  kept the relationship. 🔴 "they were wrong," only-wins, steamrolls.
- **Listens** — 🟢 answers the question you actually asked, builds on your follow-ups, asks a
  clarifying question before diving in. 🔴 monologues, ignores redirects, answers a different question.
- **Responsible** — 🟢 owns a failure/slip, root-causes it, fixes the system, no blame. 🔴 blames
  team/manager/data; passive voice about their own mistakes.
- **Takes initiative (go-getter)** — 🟢 started something no one asked for; pitched up; competition
  wins; grew the team/org investment; intern→FT/lead conversion. 🔴 only executes assigned work.
- **Motivation** — 🟢 wants to own a generation project E2E and is excited about the modality.
  🔴 generic "big models," or pure-research with no appetite to ship.
