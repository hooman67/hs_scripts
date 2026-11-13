# Third-Party Models

Adobe third-party model assets use a modeling process package because the topic includes live process docs, repo templates, and local agent automation.

> [!TIP]
> **Go here first:** [`modeling/processes/third-party-models/README.md`](../modeling/processes/third-party-models/README.md). From that folder, use the nested `third-party-models` Claude skill to walk through the process steps, run read-only audits, and produce setup/onboarding checklists.

## What This Covers

- Source repos for third-party model code.
- Private S3 buckets for base and derived model artifacts.
- Model-specific IAM/GitHub access groups.
- Foundry auth gateway bucket access.
- Inference-service private-bucket consumption.
- Team onboarding and offboarding.
- Process step guidance, setup checklists, onboarding checklists, and drift audits with a topic-local Claude skill.

## Policy Source

Approval policy is owned by PgM/legal. Use the [PgM/legal process](https://wiki.corp.adobe.com/x/gQpJ6Q) before asking engineering to grant access.

## Related Docs

| When you need... | See |
|---|---|
| Cloud accounts, access tiers, S3 credentials | [Cloud Resources and Access](project-setup-and-access.md) |
| Training artifact storage | [Model Training](training.md) |
| Inference private-bucket consumption | [Private bucket weights guide](https://docs.ai.corp.adobe.com/managed_services/services/firefly/foundry/aidoc/private-bucket-weights.html) |
