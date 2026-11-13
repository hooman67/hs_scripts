# Model Training

Overview doc for the Model Training work area. See the [org diagram](../README.md#1-org-overview) for context.

Training code lives primarily in [`foundation_exploration`](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration) in the `colligo` repo — not in this foundry repo.

> [!TIP]
> **Related docs:**
> | When you need... | See |
> |---|---|
> | Cloud credentials, S3 bucket setup, auth | [Cloud Resources and Access](project-setup-and-access.md) |
> | Compute jobs, priority, quota | [Compute Jobs](compute-jobs.md) |
> | Access-controlled buckets for training logs | [FE docs: Using access controlled buckets](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration#using-access-controlled-buckets-for-training-logs) |
> | Third-party model asset process | [Third-Party Models](third-party-models.md) |

<!--TOC-->

- [1. Key Principles](#1-key-principles)
- [2. Codebase Map](#2-codebase-map)
- [3. Uploading Training Artifacts to Foundry Buckets](#3-uploading-training-artifacts-to-foundry-buckets)
- [4. Engineering Process](#4-engineering-process)

<!--TOC-->

---

## 1. Key Principles

- **Analysis over training.** Understanding why a model behaves a certain way is harder and more valuable than running more training. Training is easy; diagnosis is the skill.
- **No training starts without a validated PR.** Debug run, charts, validation loop, data visualization, and eval sets are required before training at scale.

---

## 2. Codebase Map

All paths are relative to [`foundation_exploration`](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration) in `colligo` (`colligo_rootdir`).

| What | Where |
|---|---|
| Training code root | [`foundation_exploration/`](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration) |
| Training configs (per base model) | [`configs/<basemodel>/`](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration/configs) — e.g. `configs/lego/`, `configs/gen45/`, `configs/genrender6/` |
| Training configs (customer-specific) | [`configs/foundry/<customer>/`](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration/configs/foundry) — e.g. `configs/foundry/nbcu/` |
| Data configs (common) | [`configs/data/conversational/`](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration/configs/data/conversational) |
| Data configs (customer-specific) | [`configs/data/conversational/custom/`](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration/configs/data/conversational/custom) |
| Foundry data/model utils | [`src/foundation_exploration/components/foundry/`](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration/src/foundation_exploration/components/foundry) |
| General scripts | [`scripts/`](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration/scripts) |
| Rewriting scripts | [`scripts/rewrite/`](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration/scripts/rewrite) |
| HTML / visualization utils | [`scripts/<basemodel>/visualization/`](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration/scripts/lego/visualization) — e.g. `scripts/lego/visualization/` |
| Tests | [`tests/components/`](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration/tests/components) |
| Captioning utils (VLM client, Glimmer modules) | [`genie/glimmer/modules/vllm_client/foundry/`](https://github.com/Adobe-Firefly/genie/tree/main/glimmer/modules/vllm_client/foundry) |

---

## 3. Uploading Training Artifacts to Foundry Buckets

When running training or inference Pluto jobs from the FE codebase, you need to configure your job so that all artifacts (training logs, batch visualizations, checkpoints, inference outputs) land on a Foundry bucket instead of the default non-Foundry bucket.

The two key config values are:
- `s3_experiment_prefix` — must point to the target Foundry bucket (e.g. `s3://foundry-<company>-adobe-assets/training_logs`). This becomes the `S3_EXPERIMENT_FOLDER` env var at runtime, which is the root path for all experiment outputs.
- `s3_experiment_folder_secure: true` — ensures generated HTML/asset links use the Foundry HTML Gateway for IMS-authenticated viewing.

```yaml
launch:
  s3_experiment_prefix: "s3://foundry-<company>-adobe-assets/training_logs"
  s3_experiment_folder_secure: true
```

Jobs running on Pluto automatically get credentials for `foundry-*` buckets via the Foundry AWS Gateway — no extra credential setup is needed.

> [!IMPORTANT]
> If the job uses a third-party base model, base weights, derived weights, checkpoints, LoRA adapters, and training outputs must stay in the model-specific bucket. See [Third-Party Models](third-party-models.md).

> [!TIP]
> For full details and working config examples, see the [foundation_exploration README — Using access controlled buckets for training logs](https://github.com/Adobe-Firefly/colligo/tree/main/contrib/Mori/collections/foundation_exploration#using-access-controlled-buckets-for-training-logs).

---

## 4. Engineering Process

Different squads may have their own engineering process docs. For example, the consumer squad's process (PR requirements, debug training checklist, validation loops, customer wiki structure) is documented on the wiki:

For example, see: [Consumer Squad — Foundry Science Engineering Process](https://wiki.corp.adobe.com/x/_wui4Q)
