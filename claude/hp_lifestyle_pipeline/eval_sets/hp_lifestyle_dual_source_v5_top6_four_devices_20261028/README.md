# V5 top-six prompt set for four products and four views

This eval produces 20 V5 candidates for each of 16 device/view banks, then selects the first six after the frozen V5 source-relevance ordering. The final set contains 96 prompts.

Final exports:

- `data/prompts_top6_96.json` contains complete prompt, score, explanation, and render-lookup metadata.
- `data/prompts_top6_96.csv` is the tabular equivalent.
- `data/prompts_top6_96.txt` is a compact human-readable prompt list.
- `validation/top6_validation.json` records the final bank counts, score ranges, distribution, and validation gates.

Device/source mapping:

- Cashmere uses the Cashmere Smart Brief and source messaging.
- EliteBook uses the EliteBook Smart Brief and source messaging.
- Tassel uses the DeskJet 2955 Smart Brief and source messaging.
- Magic uses the LaserJet Smart Brief and source messaging.

Laptop tags are `laptop_FrontCloseUp`, `laptop_BackRightCloseUp`, `laptop_FrontLeftMedium`, and `laptop_FrontWide`. Printer tags are `printer_FrontCloseUp`, `printer_FrontRightCloseUp`, `printer_FrontLeftMedium`, and `printer_FrontWide`. All eight tags resolve exactly in the frozen V5 camera registry. Runtime image analysis remains disabled.

Build the immutable inputs and manifest:

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_top6_four_devices_20261028/build_inputs.py
```

Run or resume all 16 GPT-5.5 banks with at most two concurrent calls:

```bash
uv run --script /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_top6_four_devices_20261028/run_gpt55.py --all-authorized --max-concurrency 2
```

The runner preserves one semantic response per exact case/request hash, applies the frozen V5 normalizer and deterministic validator, and safely resumes completed banks. The supervisor then applies the frozen minimal review plan, validates every reviewed bank, and builds the final exports.

For an unattended resumable run that also builds the final exports after all banks pass:

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_top6_four_devices_20261028/supervise.py
```

Build the final 96-prompt JSON, CSV, and plain-text exports:

```bash
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_top6_four_devices_20261028/build_reviewed.py
python /home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_dual_source_v5_top6_four_devices_20261028/build_top6.py
```
