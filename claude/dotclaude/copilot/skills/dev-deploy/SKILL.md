---
name: dev-deploy
description: "Deploy a Foundry standalone app (e.g. thd_video) to its dev Ethos environment, end to end — build the image, bump the deploy config, regenerate manifests, open/merge the PR, and verify the rollout in ArgoCD. Includes a troubleshooting playbook for the environment problems we've actually hit (Artifactory perms, buildkit, generated-file drift, Doc CI, GitOps l"
---

Read `~/.claude/commands/dev_deploy.md` completely before acting. It is the authoritative shared workflow for this skill. Interpret its `$ARGUMENTS` from the user's request rather than literally. Translate Claude-specific tool names to Copilot tools while preserving approval, credential, and stopping boundaries. Shared scripts are at `~/.claude/scripts/`. If a required MCP server or dependency is unavailable, report it; do not claim the operation succeeded.
