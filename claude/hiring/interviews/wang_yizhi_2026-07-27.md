# Interview Feedback — Yizhi Wang

- **Candidate:** Yizhi Wang (C7083578)
- **Req:** R161074 — Staff Applied Scientist, Firefly Foundry (Evergreen)
- **Interviewer:** Hooman Shariati · **Date:** 2026-07-27 · **Type:** Pre-screen (~33 min)
- **Score:** **Technical 2/4 · Experience 2/3 · Culture 2.5/3 → 6.5/10**

*Answers below are recorded from the transcript with a per-question score (technical = correctness;
experience/culture = quality of the evidence given). No hire/advance recommendation — scoring only.*

## Part 1 — Technical — 2/4

### Q1. Walk me through what a diffusion model learns — forward vs. reverse, and what we predict.
- **A:** "It wants to learn the model function that can translate from a noise distribution to the
  targeted distribution of the data." Forward = inject noise at a chosen level; reverse = learn a
  function that takes the noisy data + conditions (class label / other) and outputs the injected
  noise, iteratively turning noise into clean data. When pressed ("forward predicts noise?") he
  clarified: "the forward process is to inject noise and the reverse is to remove the noise."
- **Score: 8/10** — correct forward/reverse framing and objective.

### Q2. What do we actually predict in the forward pass?
- **A:** "Depends which formulation… recently we use flow matching. The noisy version is a linear
  interpolation between clean data and noise — (1−T)·data + T·noise — and we are predicting… the
  noise you are adding."
- **Score: 4/10** — muddled: flow matching predicts the **velocity** (the vector field), not "the
  noise"; also didn't cleanly enumerate ε / x₀ / v-prediction as the options.

### Q3. Flow matching vs. DDPM at a high level?
- **A:** "Flow matching is an ODE — the process is deterministic; once the schedule is determined
  you get a deterministic output at each step. Traditional diffusion is a random/stochastic process
  at each step."
- **Score: 7/10** — correct core distinction (deterministic ODE vs. stochastic); didn't tie it to
  the "fewer steps" consequence.

### Q4. Difference between SFT and DPO?
- **A:** SFT = after pre-training, collect high-quality data for your purpose and fine-tune with the
  same objective (diffusion loss). DPO = involve human feedback: collect model outputs per prompt,
  humans indicate which they prefer.
- **Score: 8/10** — both correct.

### Q5. Difference between DPO and GRPO/RLHF?
- **A:** "GRPO basically is you have a number of models that can give you certain scores on the
  model input." (That was the whole answer.)
- **Score: 2/10** — near content-free and inaccurate; no group sampling, no advantage normalization,
  no reward-model-vs-preference-pairs distinction.

### Q6. How does text conditioning enter the diffusion transformer?
- **A:** "Cross attention… the queries and the keys are from the images and the values are from the
  text."
- **Score: 3/10** — the keys are wrong: in standard T2I cross-attention the text supplies **keys
  and values**, only the query comes from the image. Mechanism (cross-attention) named correctly.

### Q7. (sub) How would you encode the text — give an example encoder?
- **A:** Tokenize, use an existing open-source text encoder; example — "the [T5] model from Google."
- **Score: 7/10** — correct (T5), reached after a small nudge.

### Q8. You said there's another way besides cross-attention — continue.
- **A:** "Full attention — you view the tokens of text and images as one, concat them, and perform
  self-attention. In my experiment it brings much better performance, but the computation cost is
  higher than cross-attention."
- **Score: 8/10** — correct (joint / MMDiT-style attention), with a first-person tradeoff.

### Q9. What's CFG?
- **A:** Classifier-free guidance — controls the guidance of the text on the output. In training you
  drop out the prompt text so the model learns an unconditional process; at inference you combine
  the positive-prompt output and the negative/unconditional one ("positive minus…").
- **Score: 8/10** — correct.

### Q10. What happens when CFG is too high?
- **A:** "You really get over-saturated results, the color is very [strong]."
- **Score: 8/10** — correct.

### Q11. 50 steps → 5 steps — methods and trade-offs?
- **A:** Distillation — train a student to produce the same output in fewer steps; "a very popular
  method called DM[D], which matches the distribution of the student's output to the teacher's."
- **Score: 8/10** — correct, named DMD.

### Q12. Name a couple of other distillation methods.
- **A:** "I'm not directly working on this, but I hear of OPD, which distills the trajectory of the
  generation process."
- **Score: 5/10** — honest about the limit; one partial additional method.

### Q13. What else, other than distillation, to make it faster?
- **A:** Quantization — quantize floats to integers, less memory, runs faster.
- **Score: 5/10** — correct but limited (no faster samplers, caching, or guidance distillation).

### Q14. Blurry T2I outputs — first thing you'd look at? (+ "what else?")
- **A:** Check the output of each diffusion step — whether the noise decreases across steps (if not,
  the network may be going the wrong direction); then check the inference setup (sampling from pure
  noise, CFG, params); then whether the model weights loaded correctly. (Did not mention the VAE
  decoder; Hooman noted he looks at the decoder first.)
- **Score: 5/10** — reasonable checks, missed the decoder as a primary suspect.

### Q15. Mode collapse — how do you investigate?
- **A:** Check the training data — whether each item is correctly labeled with its prompt; a
  data-loader problem could make the model learn incorrect information and collapse.
- **Score: 4/10** — one plausible cause; missed the more common causes (over-strong guidance, reward
  over-optimization, low diversity).

### Q16. Model ignores the prompt / low prompt adherence — what do you check?
- **A:** "The model learns a shortcut to satisfy the training objective… look into the data
  distribution and whether the training loss is correctly reduced."
- **Score: 3/10** — vague; didn't reach concrete checks (is CFG on, caption quality/re-captioning,
  cross-attention maps, base-vs-finetune).

**Part 1 subtotal: 2/4** — correct on fundamentals, SFT/DPO, joint attention, CFG (mechanism +
high-CFG failure), and distillation basics; wrong/hollow on the two most core gate items (GRPO
near-content-free; cross-attention keys backwards), plus a muddled flow-matching prediction and a
vague prompt-adherence answer.

## Part 2 — Experience — 2/3

### Q17. Seedance 1.0/2.0 — what exactly have YOU done (the part you did, not the team)?
- **A:** Two self-owned pieces on **reference-to-video, identity-preserving generation** (on-modality
  I2V):
  1. **Data construction.** "The biggest challenge is you cannot directly segment the elements from
     the video and use them as input, because that way you only [get] a copy-paste function. So I
     built a system that, if you input a video, can recall a relevant video from a database" — using
     the relevant video as the training pair so the model produces genuine (not copy-paste) results.
  2. **Applying the data / architecture.** In the middle training stage, after T2V/I2I pre-training,
     "you switch to the specific video customization goals… modify the network architecture, [e.g.]
     inject rotary embeddings into the input reference images and videos," then train on the
     collected data.
- **Score: 7/10** — piece #1 is specific, personally-owned, with a named failure mode and fix
  (strongest moment); piece #2 is thinner (what changed, less on why/eval). No scale, eval
  framework, or outcome metric was given.

**Part 2 subtotal: 2/3** — on-modality with one clearly-owned, well-reasoned contribution; missing
the eval/scale/outcome legs of the full E2E chain.

## Part 3 — Culture — 2.5/3

*(Scored against Hooman's stated preferences — including that a company-impact-over-interest
motivation is a positive.)*

### Q18. Why are you leaving ByteDance?
- **A:** Looking for broader impact — his models currently serve TikTok social-media video; sees a
  bigger impact deploying models across different businesses at Adobe / changing professional
  creative workflows rather than "just the social media things."
- **Score: 8/10** — impact-driven, on-target.

### Q19. Tell me about something you shipped that broke/slipped — what did you do?
- **A:** A reference-image feature launched but had low adoption. He worked with design, PM, and
  engineering to investigate the whole pipeline: "I take the lead talking to the different teams and
  check the results at each stage… finally I find the problem happens in the deployment stage — they
  deployed a wrong version of the decoder." After locating it he worked with engineering to fix it,
  and the feature "became more and more popular."
- **Score: 7/10** — strong cross-team debugging and lead-of-resolution; the root cause was another
  team's deployment error rather than a personal mistake (recorded factually).

### Q20. Something you started that no one asked you to do?
- **A:** TikTok regulation blocked using celebrity/recognizable-identity videos as reference inputs,
  reducing the feature's usable input pool. "I kept up with an idea — we can only extract the motions
  from the video instead of the identity… I took the lead to tell this idea to other teams," and
  after integrating it the feature could accept many more input videos.
- **Score: 9/10** — genuine self-started initiative, pitched cross-team, shipped.

### Q21. Why Firefly / what do you want to own?
- **A:** A bigger platform to connect large video foundation models with professional creative
  workflows; wants to bring his data-construction / data-curation experience ("data quality
  determines the capabilities of models… I know what is good data"); his TikTok multi-product-line
  experience aligns with collaborating across different businesses.
- **Score: 8/10** — specific and aligned with the role (data + cross-business).

### Q22. What's your biggest motivating factor?
- **A:** "Scope and impact. I don't want to only work in social-media video generation — I want to
  make video-generation models [serve] more different goals and more different businesses."
- **Score: 8/10** — impact/scope-driven.

### Q23. We're a product org, not research — are you more interested in productionization or bigger research problems?
- **A:** "I'm more interested in the production side… I value the real application of the models, not
  [just] good results on benchmarks. Only [if] you solve the real-world problems, your projects will
  be remembered and be a real impact in the world."
- **Score: 9/10** — strongly aligned with the product/impact focus of the team.

### Q24. Split your motivation: % interestingness of the problem vs. % impact on the company.
- **A:** "The impact to the company is 70% and the other one is 30%."
- **Score: 9/10** — a company-impact-weighted motivation, which is the preferred lean for this team.

**Part 3 subtotal: 2.5/3** — strong and consistent impact-oriented motivation (aligned with the
team's preference), a genuine self-started initiative, and clear product focus; the one "what broke"
example resolved to another team's error rather than a personal mistake.

## Final score: 6.5/10

Yizhi's post-training/RL depth on the hard-gate question (GRPO) was thin and his cross-attention
key/value assignment was backwards, though he was correct on diffusion fundamentals, SFT/DPO, joint
attention, CFG (including the high-CFG failure mode), and distillation basics. His experience is
on-modality (Seedance reference-to-video generation) with one specific, personally-owned data
contribution (a retrieval-based training-pair pipeline built to avoid a copy-paste shortcut) and a
thinner architecture piece, with no eval/scale/outcome detail given. On culture, his motivation is
consistently impact- and production-oriented (70/30 toward company impact), he gave a strong
self-started initiative example, and his one "something broke" story was a cross-team investigation
he led where the root cause was another team's decoder deployment.
