# Interview Feedback — Wenqi Xian

- **Candidate:** Wenqi Xian (Prior Worker / former Adobe intern 2019) (5197742)
- **Req:** R161073 — Applied Scientist, Firefly Foundry (Evergreen)
- **Interviewer:** Hooman Shariati · **Date:** 2026-07-30 · **Type:** Pre-screen (~65 min)
- **Score:** **Technical 3/4 · Experience 2/3 · Culture 2/3 → 7/10**

*Answers below are recorded from the transcript with a per-question score (technical = correctness;
experience/culture = quality of the evidence given). No hire/advance recommendation — scoring only.*

## Part 1 — Technical — 3/4

### Q1. Walk me through how diffusion models work — what's learned, forward vs. reverse, what's predicted.
- **A:** "Diffusion model basically learns this reverse denoising process. You start with the data,
  you add noise — the forward process. Then we train this model to undo that noise step by step to
  generate samples that match the distribution of the training data… at every random step the model
  sees the noisy image and tries to predict the noise, and you minimize the difference from the
  ground-truth noise."
- **Score: 9/10** — correct and unaided.

### Q2. In the forward pass, what's the output of the network?
- **A:** "The output of the network is the noise… it also depends on what loss/objective you use —
  sometimes the clean image, sometimes there's a V predictor, which is the velocity. But classic
  DDPM uses noise prediction."
- **Score: 9/10** — correct, names ε / x₀ / v-prediction.

### Q3. Difference between DDPM and flow matching / rectified flow?
- **A:** "DDPM learns the reverse denoising process over many discrete steps and it's pretty
  stochastic. Flow matching… reminds me of ODE, rectified flow — it learns a continuous vector field
  from noise to data, often with a straight path, cheaper sampling because it requires ODE
  integration, which is efficient."
- **Score: 9/10** — correct.

### Q4. If DDPM predicts the noise, what does flow matching predict?
- **A:** "Flow matching predicts the velocity, like the vector field."
- **Score: 10/10** — correct.

### Q5. (bonus) Difference between flow matching and rectified flow?
- **A:** "Rectified flow is a subsequent kind of flow-matching algorithm — it learns a straighter
  trajectory." (Hooman: "That's exactly what it is.")
- **Score: 10/10** — correct.

### Q6. Difference between SFT and DPO?
- **A:** "SFT is supervised fine-tuning; DPO trains on preference pairs — you distinguish between
  [chosen vs. rejected]."
- **Score: 8/10** — correct.

### Q7. Difference between DPO and GRPO/RLHF?
- **A:** "GRPO is a reinforcement-learning algorithm — you define reward functions, sampling from
  your distribution… they're quite similar." (Hooman supplied the framing: "It's in the reward —
  one is a pair, the other has a reward function.")
- **Score: 5/10** — correct shape but vague; the DPO-vs-reward distinction wasn't volunteered.

### Q8. Give an example of a reward function for RLHF/GRPO.
- **A:** "DPO uses pairwise preferences, A better than B; RLHF and GRPO use more of a scalar reward
  you can optimize against — like a user preference percentage, or a score, or correctness."
- **Score: 5/10** — correct shape; no named reward model (e.g. HPS/PickScore/ImageReward/aesthetic).

### Q9. Which is more compute-expensive, GRPO or DPO?
- **A:** "GRPO — people usually do online updates, which is more expensive; with DPO you can get away
  with offline, you don't have to roll out during training."
- **Score: 8/10** — correct.

### Q10. What is distillation?
- **A:** "Classic DMD — you have a student model, usually smaller and faster, that learns to mimic
  the teacher's performance and distribution while taking fewer steps."
- **Score: 8/10** — correct, named DMD.

### Q11. (bonus) What can go wrong with reward models (GRPO/RLHF failure modes)?
- **A:** "On top of my head, reward hacking — the model tries to exploit the reward without doing any
  of the [real] stuff."
- **Score: 6/10** — one correct failure mode; didn't name others (diversity collapse, reward-model OOD).

### Q12. How does text conditioning enter the diffusion transformer (T2I)? (+ example encoder)
- **A:** Text encoder → text embedding (example, after a nudge: "Clip or T5") → token embeddings →
  "diffusion DiT conditions on them through cross attention, and sometimes you plus the time step."
- **Score: 7/10** — correct; needed a nudge for a concrete encoder name.

### Q13. How does DiT handle this differently from classic UNet / SDXL?
- **A:** "Depends how you trigger activation of the spatial features. For DiT it's easier/cleaner via
  cross attention; for other networks you need sequence concat or different activation… or ControlNet."
- **Score: 5/10** — muddled; didn't cleanly state the actual distinction.

### Q14. (bonus) How do Flux and SD3 do this specially?
- **A:** First answered about SDXL (residual blocks / multi-scale) by mistake; after correction,
  guessed "isn't it just DiT or M[M]DiT?" Hooman supplied the answer (DiT: pooled text+time embedding
  modulating layer norms / adaLN; Flux: joint/concatenated attention), which Wenqi echoed back
  ("adaptive layer norm… the conditioning is more global").
- **Score: 3/10** — supplied, not produced.

### Q15. What is classifier-free guidance?
- **A:** "A way to combine both conditional and unconditional prediction — you apply random drop of
  conditions during training, so at inference you can ask the model to do both with or without the
  text; it improves overall prompt adherence without really hurting quality and diversity."
- **Score: 9/10** — correct, unaided.

### Q16. What happens if CFG is very high?
- **A:** "You'll see artifacts like color saturations — that specific kind of artifact."
- **Score: 8/10** — correct direction.

### Q17. 50-step → 5-step — techniques and trade-offs?
- **A:** Distillation (student to sample fewer steps; "quality can drop, it's really tricky to
  train"; named DMD, self-forcing, "a lot of papers on making it consistent/stable"); smaller model
  via pruning/quantization; system/infra optimization. On infra (probed): memory optimization,
  caching, frame-sharing for video. On train-free sampling (probed): DDIM. (Hooman: "Good answer.")
- **Score: 9/10** — broad and current; named real methods (DMD, self-forcing, DDIM).

### Q18. Blurry T2I outputs — first suspect (as a system engineer)?
- **A:** Too-few sampling steps; inference-vs-training setting mismatch. Reframed to systems: CFG /
  noise scheduling; training data (low-res / too-compressed). (Missed the VAE decoder — Hooman noted
  this is a near-universal miss.)
- **Score: 6/10** — several correct areas; missed the decoder.

### Q19. Mode collapse?
- **A:** "Data diversity could be a problem — look at the training data and how it's processed."
  After Hooman's hint ("you've mentioned this before, three times"): "over-strong guidance or
  decoding" (CFG too high).
- **Score: 6/10** — reached the primary cause (high CFG) after a hint.

### Q20. Prompt adherence is bad — what do you check?
- **A:** "CFG may be too low" (Hooman: "or maybe it's not on"); "look at your text encoder and see if
  there's a problem with it."
- **Score: 7/10** — correct.

**Part 1 subtotal: 3/4** — correct and unaided on fundamentals, flow-matching/rectified-flow, CFG
(mechanism + direction), and sampling/distillation with real named methods; the reward/GRPO gate was
correct in shape but textbook (no named reward model), and the DiT-vs-UNet and Flux/adaLN answers
were muddled or supplied. No backwards/wrong core answers.

## Part 2 — Experience — 2/3

### Q21. Luma — Ray 3 vs. video editing: take whichever you did more of, walk me through the blocks, and deep-dive the parts you personally did.
- **A:** "Ray 3.2 / video editing — I'm the main contributor of that model. Before I joined we had an
  okay video-editing model, more traditional ControlNet-style conditioning with depth maps; then we
  made a major move to training a multi-modal image-and-video model, and that's when I started — I
  worked end-to-end from creating the synthetic training data to designing the model." On-modality
  (video generation/editing), first-person ownership.

### Q22. How did you generate the synthetic data? (in detail)
- **A:** "Paired video edits don't exist on the internet, so we make them synthetically with the
  needed diversity and quality. We took a really good localized image-edit model (like nano-banana)
  plus our own unified model, applied image edits on the first frame, then propagated the changes to
  the rest of the frames to create a video-editing pair."

### Q23. What model propagates the edit across frames — and how is it chosen?
- **A:** "We design different conditioning depending on the edit task. For style transfer /
  relighting we use depth-map or surface-normal conditioning (emphasizing structure adherence); for
  changing an object with a different shape we use point trajectories, flow, or motion embedding."

### Q24. How did you solve motion editing specifically?
- **A:** "Face is really hard — you have to maintain the expressions of a different person doing the
  same thing. We trained a specific face embedding, fine-tuned from a motion embedding, used as a
  condition for our video model — and it worked much better than all the other motion embeddings
  we'd ever used."

### Q25. Data is created — what did you do next?
- **A:** "None of the pairs are 100% correct, so I designed the filtering mechanism. Criteria: face
  identity match (compare the reference/celebrity face to the generated face); camera-motion
  preservation (run camera estimation to check it's kept when it should be); and a VLM like Gemini
  (plus cheaper ones) to check other criteria. It's a data-engineering pipeline."

- **Score (Q21–Q25, experience block): 8/10** — specific, first-person, decision-level detail on an
  on-modality video-generation project (data creation, per-task conditioning, a fine-tuned face
  embedding, a full filtering/eval pipeline).

**Part 2 subtotal: 2/3** — detailed and clearly-owned on the data/conditioning/eval side; the
training/architecture and deployment stages, the team-vs-individual split, and a quantified outcome
were not walked through (conversation moved to culture before those were covered).

## Part 3 — Culture — 2/3

*(Scored against Hooman's stated preferences — including that a company-impact-over-interest
motivation is a positive.)*

### Q26. Why are you leaving Luma?
- **A:** The last months at Luma were "a highlight of my career" — great team, delivered top models —
  but "these last two weeks" the CEO decided to pivot the company to robotics and the chief scientist
  ("Jammy," a main reason he joined) left.
- **Score: 7/10** — candid, external/structural reasons.

### Q27. Why did you leave Netflix Eyeline Studios?
- **A:** Hired as a 3D-reconstruction / Gaussian-splat expert, but "I got interested in video
  generation and diffusion… Netflix has really limited resources and compute for that kind of
  research, so I wanted to be in a frontier lab where I can train bigger models and have bigger
  impact."
- **Score: 8/10** — a modality-driven, impact-oriented pivot.

### Q28. Stack-rank your motivators: impact, visibility, solving an interesting problem.
- **A:** "Impact, [then] solving an interesting problem, [then] visibility."
- **Score: 9/10** — impact first (the preferred lean).

### Q29. A project you were particularly passionate about?
- **A:** The video-editing model becoming successful and seeing artists use it (e.g. animators
  feeding 3D-rendered output as input, the model respecting the required motion/camera control) —
  "very fulfilling." Now leading the professional-enterprise-suite expansion of that model (video
  inpainting, motion control, animation) working side-by-side with technical artists and
  forward-deployed engineers: "besides model training and being a researcher, seeing these through is
  quite nice… really rewarding to deliver end results to our customers and enterprises."
- **Score: 9/10** — passion tied to real-world delivery/impact.

### Q30. After your 2019 Adobe internship, why not join Adobe full-time?
- **A:** Timing — he was still in his PhD (graduated 2023), so full-time wasn't on the table then.
- **Score: 7/10** — straightforward clarification.

### Q31. Tell me about something you shipped that broke / had something wrong with it. (+ "what was YOUR role specifically?")
- **A:** Two stories:
  1. **Agent orchestration:** Luma's app/agents layered on top of the model "did things unexpectedly
     and sometimes broke our model" (prompt interpretation, skill orchestration). "I found out the
     reason by inspecting all the different modules of that agent orchestration and proposed to design
     a complete set of dedicated agent skills for using our model — that helped a lot in getting
     stable outcomes and a better user experience."
  2. **Product-vs-research release conflict:** the head of product wanted the model hosted exclusively
     in the Luma app; researchers wanted a public API. "We started a comprehensive analysis and
     evaluation of our own model through third parties and our internal eval team… we had good stats
     and confidence it'd be one of the top models, so there was no reason to hold it off," which
     convinced the CEO/executives to publicize it. Asked what he did specifically: "basically doing
     comprehensive emails on the model, trying to show results that are convincing enough… it was the
     first time we'd released at this scale, so a lot of us were new."
- **Score: 7/10** — story #1 is a genuinely owned root-cause-and-fix; the conflict story is more of a
  team effort and his specific individual role (the "emails/eval evidence") was thinner under the
  direct probe.

### Q32. We're a product org, not pure research — thoughts on building products for real applications rather than publishing?
- **A:** "Two years ago I'd have said there are lots of interesting problems in video generation to
  explore. But in 2026, video generation for movie production is at a relatively mature stage — we can
  take a reasonably good model and improve it based on clear, positive signals and feedback from
  customers. Adobe's strength is access to all kinds of vendors and enterprise studios — a holistic
  view and position to put this technology in the hands of creatives. That's why I jumped from Netflix
  (one studio) to Luma (potentially 10 studios); I want to be on an even higher platform to make
  impact."
- **Score: 9/10** — strongly aligned with the product/impact focus.

**Part 3 subtotal: 2/3** — impact-first motivation and clear product alignment (both aligned with the
team's preferences), passion tied to delivery, and one genuinely owned "what broke" story; a dedicated
collaborator/disagreement question and a stand-alone initiative question were not asked, and the
individual role in the release-conflict story was thin under a direct probe.

## Final score: 7/10

Wenqi's diffusion/flow fundamentals and CFG answers were correct and unaided (including
flow-matching-predicts-velocity, rectified flow, and the high-CFG oversaturation failure), and he
named real, current sampling/distillation methods (DMD, self-forcing, DDIM); the reward/GRPO gate was
correct in shape but stayed textbook (no named reward model), and the DiT-vs-UNet and Flux/adaLN
answers were muddled or supplied. His experience is on-modality (Ray 3.2 video editing at Luma),
described first-person with granular, decision-level detail on synthetic-data creation, per-task
conditioning, a fine-tuned face embedding, and a filtering/eval pipeline — though the
training/architecture and deployment stages, the team-vs-individual split, and a quantified outcome
were not covered. On culture, his motivation is impact-first and product-oriented, his passion is
tied to real-world delivery, and he gave one genuinely owned root-cause-and-fix story (agent
orchestration) plus a team-level release-conflict story where his individual role was thin under a
direct probe.
