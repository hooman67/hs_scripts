# Model access

As of 2026-10-20 UTC (2026-10-19 Pacific). Scope: the restarted Pluto machine and the user's Foundry access.

## Contents

- [Current finding](#current-finding)
- [Restart access diagnosis](#restart-access-diagnosis)
- [Access and reproduction](#access-and-reproduction)
- [Prior-project context](#prior-project-context)
- [Evidence and limits](#evidence-and-limits)
- [Sources](#sources)

## Current finding

FRESH RETRY on 2026-10-20 18:24 UTC: the correct `https://foundry-aws-pluto.adobe.io/iam/credentials/azure` route still returns HTTP 200, but its fresh 12-item deployment manifest has no entry matching `gpt-image-2.5`, Sunburst or Flare. A new low-quality 1024×1024 synthetic `gpt-image-2.5-sunburst` request returned HTTP 404 `DeploymentNotFound` through both `AzureOpenAI.images.generate` and `/openai/v1/images/generations`. No customer data was sent, no image was returned and no model was substituted. Sanitized evidence: `/home/colligo/hs_scripts/claude/mixology/research/model-access/data/azure_sunburst_retry_2026-10-20T1824Z.json`.

VERIFIED RECOVERY on 2026-10-20 18:11 UTC: the new-cluster ingress fix is live for this job. `foundry_aws_gateway.llm.get_azure_openai()` obtained Azure credentials from `https://foundry-aws-pluto.adobe.io/iam/credentials/azure` and created a client in 0.021 seconds. An authenticated Azure model-list call returned 475 models, including `gpt-image-2.5-sunburst`, its `2026-09-08` snapshot, Flare and Astra. This supersedes the HTTP 403 blocker below.

VERIFIED REMAINING BLOCKER: the gateway credential response advertises 12 Azure deployments, but its only image deployments are `gpt-image-1` and `gpt-image-1.5`. It does not advertise a deployment for `gpt-image-2.5-sunburst`. One low-quality 1024×1024 synthetic Sunburst generation through `AzureOpenAI.images.generate` reached Azure and returned HTTP 404 `DeploymentNotFound` in 0.73 seconds. The Azure `/openai/v1/images/generations` form returned the same 404 in 0.509 seconds. The catalog says the base model supports inference, but a catalog entry is not a deployment. No image was returned and no customer data was sent. Sanitized evidence: `/home/colligo/hs_scripts/claude/mixology/research/model-access/data/azure_gateway_recovery_2026-10-20.json`; raw sanitized attempt records: `/home/colligo/mixology_data/model_access_2026-10-20/azure_sunburst_probe/record.json` and `/home/colligo/mixology_data/model_access_2026-10-20/azure_v1_sunburst_probe/record.json`.

RESEARCHER BOUND: do not silently substitute the deployed `gpt-image-1.5`. To use exact Sunburst through Azure, the Azure resource needs a Sunburst deployment and the Foundry credential response should advertise its deployment name. The already verified direct Foundry OpenAI route remains a separate alternative, but was not rerun in this Azure-specific recovery check.

USER-CONFIRMED UPDATE: Hooman requested new-cluster allowlisting and authorized fal.ai as the temporary provider. VERIFIED inference: nine image requests completed (five refraction, four composition), together with nine successful Astra rewrites and nine advisory critiques. Exact requested endpoints are `openai/gpt-image-2.5/sunburst/edit` and `openrouter/router/vision` with `model=openai/gpt-6-astra`. Both returned real outputs through the first supplied fal key. Five images are 848 × 1264; four group images are 1536 × 1024. Evidence: run folders under `/home/colligo/mixology_data/refraction_research_2026-10-19/runs/v3fal_*` and `/home/colligo/mixology_data/refraction_research_2026-10-19/composition/runs/v1fal_*` / `v2fal_*`, including full prompts, ordered source hashes, sanitized request payloads, queue IDs and downloaded PNGs.

The first Astra request with `reasoning=false` returned HTTP 400: reasoning is mandatory. The retry and all subsequent requests used `reasoning=true`. The failed attempt is preserved under the first clear/red run and caused no image request. Neither exact reasoning effort nor backend model snapshot is exposed by the fal schema; do not infer settings equivalence or a verified returned model identifier. The default router temperature was not overridden. Original model/input safety checks remained enabled; no alternative model was requested.

Official schemas: https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=openai/gpt-image-2.5/sunburst/edit and https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=openrouter/router/vision . Queue behavior and requested privacy controls: https://fal.ai/docs/inference-api/queue/submit.md . Fal's `units` pricing response is not a per-image cost estimate. Exact invocation is saved by `/home/colligo/hs_scripts/claude/mixology/research/model-access/scripts/run_fal_experiments.py` and `/home/colligo/hs_scripts/claude/mixology/research/model-access/scripts/fal_transport.py`. Successful queue IDs are reused on resume; uncertain submissions are not silently repeated. Credentials remain outside the project/gallery.

SUPERSEDED FOUNDRY-ROUTE BLOCKER: after restart, both `llm.get_openai()` and `llm.get_azure_openai()` had failed during credential vending with HTTP 403. The stage Azure route now succeeds after the user-reported gateway resync. Dev was not retested because stage succeeded. Fal inference above remains separately verified.

HISTORICAL VERIFIED RESULT (before restart): both requested models executed successfully through `foundry_aws_gateway.llm.get_openai()`, using credentials from `https://foundry-aws-pluto.adobe.io` and the direct `https://api.openai.com/v1/` endpoint.

| Probe | Actual result | Observed duration |
| --- | --- | --- |
| `gpt-image-2.5-sunburst`, Image API edit | One decodable 1024×1024 RGB PNG, 1,202,435 bytes | 11.4 seconds, CLI report |
| `gpt-6-astra`, Responses API with image input | Completed response; correctly identified the synthetic blue mug and right-side handle | 2.87 seconds, including client creation |

The Sunburst output visibly changed the flat illustration into watercolor while preserving the principal subject, handle orientation, broad composition, and pale background. Astra also recognized the light rim, rounded body, and left-side highlight. These findings verify access and basic behavior for this single input, not general performance on customer references.

Output: `/home/colligo/hs_scripts/claude/mixology/output/imagegen/sunburst_access_test_2026-10-19.png`.

Input: `/home/colligo/hs_scripts/claude/mixology/research/model-access/data/synthetic_reference.png`.

Full prompt: “Restyle this illustration as a soft watercolor painting. Keep the single blue mug, its shape, handle on the right, composition, and pale background.”

Sanitized run records: `/home/colligo/hs_scripts/claude/mixology/research/model-access/data/sunburst_probe_2026-10-19.json` and `/home/colligo/hs_scripts/claude/mixology/research/model-access/data/astra_probe_2026-10-19.json`.

## Restart access diagnosis

### Recovery result — 2026-10-20

USER-CONFIRMED context: Hooman relayed that this job had moved to Pluto cluster `trn01-od-or2-prod`; its outbound IPs were added to `laser_prod_od`, and stage/dev Foundry gateways were manually resynced to revision `3af2a14652`. Those organizational/deployment details are user evidence. Independently VERIFIED from this job: the stage Pluto Azure credential route now returns 200 and the token authenticates against the Azure model catalog.

The exact image error to relay is: HTTP 404, code `DeploymentNotFound`, message “The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.” This is consistent with the gateway's current 12-item deployment list, which contains only `gpt-image-1` and `gpt-image-1.5` among image models. It is no longer consistent with an ingress/source-IP failure.

VERIFIED on 2026-10-20 UTC:

- Recovered the exact successful setup from `/home/colligo/.codex/sessions/2026/10/19/rollout-2026-10-19T10-20-17-01a1552d-a5de-7863-9847-485fe91fc5bd.jsonl`: the 17:30 UTC call used SDK 2.0.0, `llm.get_openai()`, the injected Pluto token and the default Pluto host. It returned direct OpenAI credentials and listed Astra/Sunburst. There was no special host override or manually supplied OpenAI key in that setup. No credential values were recovered from or copied out of the transcript.
- The rebuilt SDK is also 2.0.0. Both OpenAI and Azure helpers include the exact acknowledgement automatically. The shared Azure skill's claim that no machine-token broker exists is stale and was not used to override the user's documented SDK method.
- Stage and dev Pluto hosts return empty HTTP 403 responses with `server: adobe` for both credential routes. An unauthenticated control produces the same empty 403; root paths return empty 404. The two corporate hosts time out from this job.
- Locally decoded token metadata names `hshariati@adobe.com`, `GAI-415 Foundry`, and `Foundry-Presale-And-Partnership-Support`; its expiry is in the future. This is metadata inspection, not independent verification of the signature, revocation status or server-side membership.
- The actual SDK cache is `/mnt/localssd/.cache/ai_platform/foundry_aws_gateway`, containing only OpenAI/Azure lock files. There is no cached model credential or MSAL login to recover there. The configured permanent-token YAML and home MSAL cache are also absent.
- Local gateway ingress source allows the Pluto hosts only for source-IP groups `laser_prod` and `laser_prod_od`, and only paths prefixed `/iam/credentials`. The application source returns JSON details for missing acknowledgement or rejected identity/project membership. The observed empty responses differ from those application errors.

ASSUMED LEADING EXPLANATION: the restarted job's egress is being rejected at gateway ingress, possibly by the source-IP allowlist. This fits both routes/hosts and the response shape better than a missing SDK acknowledgement. It is **not proven**: the local source is not proof of live deployment state, and no ingress logs or current egress-to-allowlist match were obtained. Token/server authorization remains an alternative.

Sanitized, reproducible live HTTP evidence: `/home/colligo/hs_scripts/claude/mixology/research/model-access/data/gateway_restart_diagnostic_2026-10-20.json`. Collector: `/home/colligo/hs_scripts/claude/mixology/research/model-access/scripts/check_gateway_access.py`. The collector never saves credential response bodies, tokens or keys and makes no inference request.

Next exact access step: the Foundry/Azure owner should either deploy `gpt-image-2.5-sunburst` on the Azure resource and expose the deployment name in `/iam/credentials/azure`, or confirm that exact Sunburst should continue through the direct Foundry OpenAI credential route. After a deployment change, retry one synthetic low-quality image before any customer batch. No ingress, deployment or authorization change is made by this research task.

Primary source paths (local Colligo revision `a879f443bb86eed81f43122794e3a40d48cc864e`; ingress files had no local changes when inspected):

- `/home/colligo/colligo/managed_services/services/firefly/foundry/deploys/aws_gateway/stage/values-ingress.yaml`
- `/home/colligo/colligo/managed_services/services/firefly/foundry/deploys/aws_gateway/dev/values-ingress.yaml`
- `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/aws_gateway/README.md`
- `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/aws_gateway/shared/auth.py`
- `/home/colligo/colligo/managed_services/services/firefly/foundry/standalone_apps/aws_gateway/shared/llm_ack.py`

## Access and reproduction

Current durable Python environment: `/home/colligo/.venvs/mixology/bin/python` (Python 3.12). The former `/mnt/localssd/mixology_venv` was wiped. Gateway: `foundry-aws-gateway[llm]==2.0.0`. OpenAI SDK: 3.35.1. Pillow: 13.0.0.

Install the gateway from Adobe's authenticated `pypi-adobeshared-release` index. Default public PyPI does not contain it; unauthenticated internal-index access returns 401. Use existing Artifactory environment credentials without printing them. Install the `llm` extra: importing `foundry_aws_gateway.llm` also needs Google GenAI and Bedrock type dependencies.

The SDK uses `PLUTO_AUTH_TOKEN` and the required acknowledgement header. Its private credential cache is outside the repository. Use `umask 077` when retrieving credentials. Recreate the direct client for later batches: version 2.0.0 passes a fixed key to each OpenAI client, so an existing long-lived client is not itself a refresh mechanism. Azure's helper instead installs a token-provider callback.

Model execution uses the unchanged bundled CLI at `/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py`, `edit`, model `gpt-image-2.5-sunburst`, quality `low`, size `1024x1024`, PNG, `--no-augment`, and no `input_fidelity`. The KDP historical test reported that Sunburst rejected that legacy parameter.

Synthetic-reference builder: `/home/colligo/hs_scripts/claude/mixology/research/model-access/scripts/create_reference.py`.

Exact edit prompt: `/home/colligo/hs_scripts/claude/mixology/research/model-access/data/edit_prompt.txt`.

Historical reproduction of the completed image request is below. After the restart, its synthetic input/output PNGs were absent from the restored files; the sanitized records survive. Use the durable Python environment above, recreate the synthetic reference with its builder if needed, and choose a new output filename. Do not rerun until gateway access works. This bootstrap only supplies credentials to the bundled CLI; it does not implement another image API client.

```bash
umask 077
/mnt/localssd/mixology_venv/bin/python - <<'PY'
import os, sys
from foundry_aws_gateway import llm
client = llm.get_openai()
env = os.environ.copy()
env['OPENAI_API_KEY'] = client.api_key
env['OPENAI_PROJECT_ID'] = client.project
env['OPENAI_BASE_URL'] = str(client.base_url)
args = [
    sys.executable, '/home/colligo/.codex/skills/.system/imagegen/scripts/image_gen.py',
    'edit', '--model', 'gpt-image-2.5-sunburst',
    '--image', '/home/colligo/hs_scripts/claude/mixology/research/model-access/data/synthetic_reference.png',
    '--prompt-file', '/home/colligo/hs_scripts/claude/mixology/research/model-access/data/edit_prompt.txt',
    '--quality', 'low', '--size', '1024x1024', '--output-format', 'png',
    '--out', '/home/colligo/hs_scripts/claude/mixology/output/imagegen/sunburst_access_test_2026-10-19.png',
    '--no-augment',
]
os.execve(sys.executable, args, env)
PY
```

Astra's reproducible probe is `/home/colligo/hs_scripts/claude/mixology/research/model-access/scripts/probe_astra.py`. It preserves the exact text/image inputs, model, reasoning setting, output, token usage, and request ID; it refuses to overwrite its existing record.

## Prior-project context

- HP: source messaging → environment prompts → downstream rewriter + digital twin. V1 is selected; V2's blue-coverage experiment is archived. Do not inherit its palette target. Its context records 192 generated outputs but no user acceptance of visual quality.
- 3D research: preserve results and provenance; prompt additions should address measured failures. Its checkpoint explicitly does not establish a general Astra rig-authoring benchmark.
- KDP: prior Sunburst image edits used clean product references, high quality, 1536×1024. It records 22 displayed outputs, with exact SKU fidelity still requiring review. Prior successful access is a lead that required fresh verification.

## Evidence and limits

The historical paragraphs below describe the pre-restart access-test batch. Current Azure recovery evidence and the later AWS-file check are recorded above and in the project checkpoint.

VERIFIED on 2026-10-19: corporate root access timed out; `docs.ai.corp.adobe.com` failed DNS. This does not imply the Pluto gateway is unavailable; fresh gateway access succeeded. The old `/mnt/localssd/kdp_imagegen_venv/bin/python` environment is absent.

The supplied `/mnt/localssd/temp_creds.txt` exists with mode 0600. It has not been sourced or copied; no AWS operation was necessary. No customer reference was sent or result published. No general model-quality or production-readiness claim is supported by a connectivity test.

Sunburst's bundled CLI saves decoded output and elapsed time, but does not save the image response's request ID, returned snapshot identity, usage, or cost. Those fields remain unknown. Exact pixel reproduction is not guaranteed. Astra's response does expose its returned model, request ID, and token usage, preserved in its record. Both historical calls used the requested exact model IDs with no model substitution. Azure Sunburst inference was tested on 2026-10-20 and failed before generation because the requested deployment does not exist; this says nothing about image quality.

Confidence labels: VERIFIED = current direct evidence; USER-CONFIRMED = user instruction; ASSUMED = explicit working interpretation; UNVERIFIED = unsupported or historical outcome not rechecked.

## Sources

Retrieved/inspected 2026-10-19 unless marked historical:

- OpenAI, GPT Image 2.5 Sunburst model reference: https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst — primary, model ID and supported image operations.
- OpenAI, image-generation guide: https://developers.openai.com/api/docs/guides/image-generation — primary, generation/edit distinction and direct Image API versus Astra + image tool.
- OpenAI, Astra model reference: https://developers.openai.com/api/docs/models/gpt-6-astra — primary, requested reasoning-model identity.
- Adobe SDK source: `/mnt/localssd/mixology_venv/lib/python3.12/site-packages/foundry_aws_gateway/llm/__init__.py`, `/mnt/localssd/mixology_venv/lib/python3.12/site-packages/foundry_aws_gateway/llm/_client_openai.py`, and `/mnt/localssd/mixology_venv/lib/python3.12/site-packages/foundry_aws_gateway/_constants.py` — installed version 2.0.0, authentication, cache, and acknowledgement behavior.
- Adobe historical documentation snapshot: `/home/colligo/hs_scripts/claude/obsidian/hs_base/raw/foundry/docs/project-setup-and-access.md` — package index and credential paths, checked against the live SDK/API where possible.
- Historical project context: `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/README.md`, `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/PROJECT_STATE.md`, `/home/colligo/hs_scripts/claude/3d_research/README.md`, `/home/colligo/hs_scripts/claude/3d_research/PROJECT_STATE.md`, `/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/PROJECT_NOTES.md`, and `/home/colligo/hs_scripts/claude/kdp_ffdy_8567_research/research/generation/smoke_2026-10-07/SUMMARY.md`.
