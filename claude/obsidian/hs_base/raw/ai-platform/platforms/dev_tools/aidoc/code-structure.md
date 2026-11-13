# Code Structure

In the AI Platform repo we are following this structure for consistency:

```
+--------------------------------------------------------------+
|                            cloud                             |
+--------------------------------------------------------------+

+--------------------------------------------------------------+
|                            models                            |
+--------------------------------------------------------------+

+--------------------------------------------------------------+
|                        frameworks                            |
| +------------+ +------------+ +------------+ +------------+  |
| | agent      | | training   | | data       | | inference  |  |
| +------------+ +------------+ +------------+ +------------+  |
+--------------------------------------------------------------+

+----------------------------------------------------------------------------+
|                               platforms                                    |
| +------------+ +------------+ +------------+ +------------+ +------------+ |
| | agent      | | dev_tools  | | compute    | | data       | | inference  | |
| +------------+ +------------+ +------------+ +------------+ +------------+ |
+----------------------------------------------------------------------------+

```
- `models`: Models that are shared among different use-cases and follow relatively strict shareability rules (aka model hub).
- `frameworks`: Libraries offered by the AI Platform as a product. They provide a stable (often Python) API that users will need to directly use.
  - `agent`: Shared runtime for building thin agents with pluggable frontends (Slack, terminal) and MCP providers, plus configuration, secret management, prompt composition, and the FastAPI lifecycle.
  - `inference`: Inference-focused frameworks.
  - `data`: Data processing / loading-focused frameworks.
  - `training`: Training-related frameworks.
- `platforms`: Any code / documentation owned by the AI Platform team that is not a framework.
  - `agent`: Bazel macro and Python tooling that generate K8s deployment manifests (ConfigMap, PodMonitor, config hash, timeout validation) for agents built on `frameworks.agent`.
  - `data`: Data processing / loading code and docs.
  - `dev_tools`: General repository and development management tools.
  - `inference`: All inference-related components from the platform team (build tools for managed services).

Anything else is out of scope for this repo.

```{note}
Reference: [AI Platform Code Management ](https://adobe.sharepoint.com/:w:/r/sites/GenTechWorkingGroup/Shared%20Documents/AI%20Platform/Inference%20Platform/AI%20Platform%20Code%20Management%20v2.docx?d=w63813e4a819244fbb30cb6afb735f7d5&csf=1&web=1&e=CcpOQ0)
```

## Frameworks: Package name and import guidelines

For sake of consistency and being able to map software usage to where it lives, we recommend that:

1. **Required**: Not every code is meant to be in this repo as `frameworks`. Roughly, they should have passed prototype stage and have two or more owners under the Genai organization.
2. **Required**: Match your github workflow name with the folder name of your code, e.g. `frameworks_training_mori.yaml` for code at `frameworks/training/mori`, and use path filters so that it only runs when your code or its CI is changed.
3. **Strongly recommended** Start framework names with `frameworks.*`.
4. **Strongly recommended** Have consistent package name and import structure.
5. **Optional** You can use [uv-dynamic-versioning](https://github.com/ninoseki/uv-dynamic-versioning) to release wheels based on tags for your frameworks.
6. **Optional**: You don't need to use the `src/<import prefix>` for your code. To help avoid boilerplate, we provide the `ai.hatch` build backend that allows your code to be placed flat in the sub-repo and auto-add your desired prefix. See more at [ai.hatch](./shared-tooling.md#aihatch) docs.
