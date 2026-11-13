# Foundry Modeling

Shared code related to building, training, and serving models for Foundry that does not already have a dedicated place (e.g. colligo, foundation exploration).

## Structure

- `processes/` — modeling-related operational processes, templates, and local agent skills that are more than reference docs but do not belong in Colligo or Genie.
- `terraform/` — AWS infrastructure (S3 storage, IAM) for modeling resources across staging and production environments.
