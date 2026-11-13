# Unified Foundation Exploration Codebase

> **📦 Inference-only wheel — quick install (latest).** Installs the
> `gen6-conversational-inference` extras: the runtime deps needed to *run* inference
> (torch, mori, omegaconf, pydantic, …) — **not** the training stack. Every merge to `main`
> that touches this folder publishes a new wheel; omitting `==<version>` resolves the newest.
>
> ```bash
> uv add "foundation_exploration[gen6-conversational-inference]" \
>   --index https://artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple \
>   --index https://artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-kineto-release/simple \
>   --index-strategy unsafe-best-match
> ```
>
> To pin a specific version, add the PyTorch CUDA index, or consume the wheel from a Colligo
> env, see [Consuming the Inference Wheel in Colligo](#consuming-the-inference-wheel-in-colligo).

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [Pluto GPU Machine Quickstart](#pluto-gpu-machine-quickstart)
- [Code Structure](#code-structure)
- [MoriCTL](#morictl)
- [Training Environment](#training-environment)
- [Training](#training)
  - [Launch spec](#launch-spec)
  - [Job Priority](#job-priority)
  - [CUDA Sync Debug Mode](#cuda-sync-debug-mode)
  - [Resuming jobs:](#resuming-jobs)
  - [Monitoring training jobs](#monitoring-training-jobs)
- [Inference](#inference)
  - [Overview](#overview)
  - [Yaml Spec](#yaml-spec)
  - [Examples](#examples)
    - [Diffusion](#diffusion)
    - [MLLM Evaluation](#mllm-evaluation)
  - [Async eval runners](#async-eval-runners)
- [Consuming the Inference Wheel in Colligo](#consuming-the-inference-wheel-in-colligo)
  - [Step 1: Pin the version in your environment](#step-1-pin-the-version-in-your-environment)
  - [Step 2: Declare the dependency in colligo.yaml](#step-2-declare-the-dependency-in-colligoyaml)
  - [Step 3: Handle mypy's import-untyped warning](#step-3-handle-mypys-import-untyped-warning)
- [Development](#development)
  - [Conventions](#conventions)
  - [Preparing PRs](#preparing-prs)
  - [Modifying the environment](#modifying-the-environment)
  - [Adding new models to pre-caching](#adding-new-models-to-pre-caching)
  - [VSCode](#vscode)
  - [Consuming a model from the Model Hub](#consuming-a-model-from-the-model-hub)
    - [Find your Model](#find-your-model)
    - [Determine which model version to use](#determine-which-model-version-to-use)
    - [Getting the model into the training environment](#getting-the-model-into-the-training-environment)
    - [Modifying your config file](#modifying-your-config-file)
- [Miscellaneous](#miscellaneous)
  - [Github actions management](#github-actions-management)
  - [Batch Packing](#batch-packing)
  - [Using access controlled buckets for training logs](#using-access-controlled-buckets-for-training-logs)
  - [Running Foundry Jobs in us-east-2](#running-foundry-jobs-in-us-east-2)

______________________________________________________________________

<!--TOC-->

Docker: `docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/training-base-01-28-26:12.8.1-runtime-ubuntu22.04-CUDNN-v9.17.1.4-NCCL-v2.27.3-1-eagain-fix4-PY-3.10`

To update the Docker image, see the [build-image repository](https://github.com/OneAdobe/build-image) - [FE Training Image Section](https://github.com/OneAdobe/build-image?tab=readme-ov-file#add-additional-linux-packages-to-fe-training-image). The Dockerfile is [Dockerfile.advanced](https://github.com/OneAdobe/build-image/blob/main/Dockerfile.advanced).

When transitioning to a new dockerfile, the following should be updated in the code
- [ ] The reference docker image url in README.md
- [ ] The docker image urls in the training and interactive [configs](configs)
- [ ] The docker image used for the CI action runners, configured in the `colligo-deploy` Helm `values.yaml` for the `actions-runner` / `actions-runner-gpu-p4d` apps (see [aidoc/continuous-integration/overview.md](../../../../aidoc/continuous-integration/overview.md)).

New FE training Docker images should also run the fixed-step GenRenderer6 image benchmark. See
[GenRenderer6 CUDA Image Benchmarks](docs/gen6_image_benchmarks.md) for the CI trigger, metrics, and review expectations.

## Pluto GPU Machine Quickstart

First, make sure you have these environment variables set on your local machine:

```bash
export LDAP=...
export WANDB_API_KEY=...
export GITHUB_TOKEN=...
export SLACK_MEMBER_ID=...
export ORION_API_KEY=... # Authorizes async-eval dispatch; set to "" if not using async eval
export DATA_LINEAGE_TOKEN_PATH=... # Path to a file containing your Data Lineage token (see details below)
```

* `WANDB_API_KEY` can be obtained at our self-hosted Weights and Biases instance, [here](https://adobesensei.wandb.io/home).
* `GITHUB_TOKEN` is your **own** GitHub Personal Access Token, created [here](https://github.com/settings/tokens) (authorize it for the `Adobe-Firefly` org via *Configure SSO*). It is only needed for `morictl interactive` (which clones your repos on the dev box); `morictl launch` no longer needs it — training code is shipped as an S3 snapshot, not a git clone.
* `SLACK_MEMBER_ID` can be obtained by visiting your Slack profile, clicking the hamburger for the drop down menu, and then selecting "Copy Member ID".
* `ORION_API_KEY` authorizes async-eval jobs dispatched to the Orion router. To get one: go to https://fedemo.corp.adobe.com/api-keys, press the "+ Create Key" button in the top-right corner, specify a name, and press Create (this is the same key the `orion` SDK/CLI reads). It must be set, but if you are not using async eval you may set it to the empty string: `export ORION_API_KEY=`.

* `DATA_LINEAGE_TOKEN_PATH` is required to access internal Adobe datasets. You can obtain your Data Lineage token by following the instructions [here](https://wiki.corp.adobe.com/display/adobestock/How+to+request+access+to+training+data+and+get+a+token).
Save the token to a file — preferably stored on S3 — and set the environment variable to point to that file.
Example:
```bash
export DATA_LINEAGE_TOKEN_PATH="s3://dit-scale-up/lineage-v1/token/default_lineage_token.txt"
```

Then, install `morictl`:

```bash
make morictl
```

> **Credentials.** On a Mac (or a Pluto dev pod building the launcher venv from scratch), installing
> `morictl` resolves its dependencies from Adobe's private Artifactory, so put **your own**
> Artifactory API token in `~/.netrc` (`uv` reads it automatically):
>
> ```
> machine artifactory-uw2.adobeitc.com login <ldap> password <your-artifactory-api-token>
> ```
>
> `touch ~/.netrc && chmod 600 ~/.netrc` first (the `600` perms are required; macOS and Linux are
> identical). Generate the token from your Artifactory profile page. On CI and training pods the
> venvs come prebuilt from S3, so no token is needed there.

Then, you can launch an interactive development environment using:
```bash
morictl interactive configs/interactive/default.yaml --pluto_project <project> --gpu_instance <gpu_type>
```

This will create a 2-GPU interactive Pluto job with the Mori development environment pre-configured.

Once the interactive job is running and set up (make take a few minutes), you can connect to it using:
```bash
morictl edit $LDAP-dev --pluto_project <project>
```

This will open the interactive environment in your local editor (e.g., Cursor) with full access to the remote filesystem.
To use a different editor, you can pass in `--editor [vscode, ssh, cursor]`. 

---

For the rest of this section, we assume you are in the `foundation_exploration` folder.

## Code Structure

- `common | data | models | optimization | pretrained_models | tools | utils | train_entrypoint.py`
  - shared code, free to use by everyone.
  - Owned by the code foundation squad
- `components/`
  - code for specific components, such as MLLM, DIT, etc.
  - Owned by the respective component squads.
  - Components cannot have cyclic dependencies.
  - For component A to be able to use component B's code in main, they need to explicitly get allowlisted in B's `visibility.yaml`.


## MoriCTL

This CLI tool can be used to launch remote jobs from your Mac, Pluto CPU or Pluto GPU machines.
Run the following to install and login. First, set your
```bash
make morictl
source scripts/env/activate.sh
morictl login
```
To access `morictl` anywhere, add a line to source the above `activate.sh` to your `~/.bash_profile`.

## Training Environment

This needs to be run on a Pluto GPU machine.
Run the below to install the virtual environment:
```bash
make install
```

This will add the following line to your `~/.bash_profile`. If you are using a different shell or running in an
environment where the below is not sourced, you would need to manually run the following:
```bash
source scripts/env/activate.sh
```

To uninstall the environment, run the following:
```bash
make clean
```

## Training

Now, you will have the `morictl` command available. 

To launch a local training on your Pluto GPU machine, pass in the desired config file as an argument.
The configs must be specified relative to the `foundation_exploration` folder.
The node and launch information is provided in the config only.

For example,
```bash
morictl local_run configs/dit/gen45_2B.yaml --mutate-config
```

`--mutate-config` changes the config on the fly to match the local training environment, so that the config has a
chance of working without editing it. Note that for some configs, you will likely still have to make some edits. However,
the config above (`configs/dit/gen45_2B.yaml`) should work correctly.

### Launch spec

The `train.launch` spec allows you to configure various things related to the training job. Here are some of the most important ones:

```yaml
train:
  launch:
    # Trainer entrypoint, example
    trainer: foundation_exploration.components.diffusion.recipes.train_dit

    num_nodes: ...
    num_gpus: ...

    # docker image
    image: ...

vault_secrets:
      # allow hooking up vault secrets. Format is: ENV_VAR:vault_path:vault_key
      # Example:
      AWS_ACCESS_KEY_ID: dme_colligo/services/pluto/projects/foundry/nbcu/aws:aws_access_key_id
      AWS_SECRET_ACCESS_KEY: dme_colligo/services/pluto/projects/foundry/nbcu/aws:aws_secret_access_key```
    
    # Allow putting the results in a different folder
    s3_experiment_prefix: "s3://foundry-nbcu-adobe-assets/training_logs"
    # Allow viewing results through secure html viewer that only allows people
    # that have access to associated pluto project of the bucket in s3_experiment_prefix
    # to see results
    s3_experiment_folder_secure: true
```

### Job Priority

Jobs are submitted with an allocation mode that determines scheduling priority:

| Config value | Allocation Mode | CLI Flag |
|---|---|---|
| `guaranteed` | Guaranteed (P0) | _(default)_ |
| `in-quota-preemptible` | Reclaimable (P1) | `--in-quota-preemptible` |
| `preemptible` | Spare Capacity (P2) | `--preemptible` |

https://docs.ai.corp.adobe.com/pylibs/colligo/pluto/aidoc/jobs.html#allocation-mode

**Set priority in your config** (`launch.job_priority`):
```yaml
launch:
  job_priority: in-quota-preemptible  # guaranteed | in-quota-preemptible | preemptible
```

**Or override via CLI flags:**
```bash
morictl launch configs/my_training.yaml --in-quota-preemptible
morictl launch configs/my_training.yaml --preemptible
```

Resolution: CLI flags (`--preemptible` / `--in-quota-preemptible`) > config `job_priority` > default `guaranteed`.

> **Foundry projects** should set `job_priority: in-quota-preemptible` in their configs.
See `configs/foundry/integration_tests/conditional_vid_training.yaml` for an example.


### CUDA Sync Debug Mode

The training entrypoint automatically enables CUDA sync debug mode to help catch synchronization issues:
- **Strict mode for debugging**: To make synchronization issues raise errors during forward/backward pass (more strict),
  ```bash
  export ERROR_ON_SYNC=1
  morictl local_run configs/dit/gen45_2B.yaml
  ```
  This is useful for debugging synchronization issues locally as errors will halt execution immediately.

To launch a distributed training run:
```bash
morictl launch configs/dit/gen45_2B.yaml
```

To launch a distributed training run on preemptible compute, add the preemptible flag:
```bash
morictl launch configs/dit/gen45_2B.yaml --preemptible
```

To enable automatic job requeue on failure (useful for long-running preemptible jobs), use the `--auto-requeue` flag with `--preemptible`:
```bash
morictl launch configs/dit/gen45_2B.yaml --preemptible --auto-requeue
```

Try running `morictl login` again if you get an error. You can see more help with `morictl launch --help`.

### Resuming jobs:

* Once the job is launched on pluto, if the same job is restarted using pluto UI, the checkpoint and the dataloader states will be resumed
* However, if the `morictl launch` command is used with the same config, a new job will be created with new timestamp.
  Therefore, you will need to manually update the `resume_from:` variable of the config with the s3 path of the checkpoint.

### Monitoring training jobs

**Wandb**: Both local and remote job automatically launches a wandb run in the `foundation-exploration` project.
The local runs are started with a prefix `local_run` for easy separation of them from multi-node training launch. 
The s3 checkpoint path for the job can also be found in the wandb overview page.

**Logging Page**  
We create an [experiment overview](https://dit-scale-up.s3.us-west-2.amazonaws.com/fe-experiments/FFP-33934-dit-FFP-38154-gen45_t2x_2b_singlevae_8x_parity_32x_densecap_guard2.5-2025.05.02-11.44.10/logs/33a41cc9-27eb-4bc6-9618-dd28b29a4081/1/index.html)
page link to which can be found in logs, in Wandb and in the `#foundation-job-butler` channel

**Slack**: Job status is posted in the `#foundation-job-butler` channel

It is recommended to use the **Experiment_overview->Log Viewer** for checking logs instead of pluto which might have
slight latency in our case due to additional logging to log viewer.

**Custom Metrics with OpenTelemetry**

You can add custom metrics to your training jobs using Mori's OpenTelemetry utilities. These metrics will appear in the [Mori Telemetry Dashboard](https://observability.ai.corp.adobe.com/d/fery58xvhi0hsa/mori-telemetry-dashboard).

Here's a quick example of how to create and use a custom counter:

```python
from mori.training.utils.otel_metrics import get_training_framework_counter

# Create the metric once
_, record_my_event = get_training_framework_counter(
    name="my_event_total",
    description="Counts the total number of my custom events."
)

# Use it in your code
record_my_event(1)
```

For detailed documentation on creating different types of metrics (gauges, histograms), managing attributes, and best practices, please see the [full OpenTelemetry documentation](https://docs.ai.corp.adobe.com/contrib/Mori/aidoc/open_telemetry.html).

## Inference

### Overview

Inference happens in two ways:
- Training run when `train.inference_mode=false` (default) after `train.save_html_freq` steps.
- Standalone inference run when configs sets `train.inference_mode=true`.
Additionally,
- If `train.inference_mode=true`, we will try to export the main model in a standalone way. This is **work in progress**.

### Yaml Spec

```yaml
# This configurs inference in the config
inference:
  - name: # name of the inference run
    runner:
      target: # path to inferenceRunner object
      params: # params for the inferenceRunner object
    prompt_sets: 
      - prompt_name: # name for prompt set
        # other params for prompt set, depends on used  inferenceRunner object
    runtime:
        # runtime params, depends on used  inferenceRunner object
    sampling:
        # Any input here will be passed as-in to LDMInference.Input associated with the
        # used InferenceRunner.
```

### Examples

#### Diffusion

For example, to export Gen 4.5:
```bash
morictl local_run configs/dit/gen45_quick_export.yaml
```

Similarly, to export a Filix3 2B model from `mori-foundation`:
```bash
morictl local_run configs/dit/filix3_t2x_simple_2B_quick_export.yaml
```

This exports the models and uploads them to S3 which then can be used for stand-alone inference.
To see an example, look-at/ run:
```bash
python scripts/inference/ldm_inference.py
```
This assumes the `mori-venv` python environment has been activated.
Note that you will need to edit the `model_key` in the script to download/ inference a particular model.

#### MLLM Evaluation

To run T2I inference, you can use the following command:
```bash
morictl local_run configs/mllm/metamorph_qwen2p5_vl_7b_t2i_inf.yaml
```

### Async eval runners

Eval runners come in two kinds. **Sync** runners (`vqa`, `nsfw_v9`, `ocr`, …) run inline on
the GPU worker. **Async** runners (`t2i_judge`, `t2v_judge`, `v2v_judge`, …) are
fire-and-forget: the worker POSTs the inference's `data.json` to an Orion router, which
forwards it to a judge deployment; the judge scores it and patches the scores back into
`data.json` on S3.

A runner is async when its `eval_runners` entry carries an `async_eval` block:

```yaml
eval_runners:
- target: ...inference.eval_runner.conversational_runners.AsyncEvalRunner
  params:
    key: 't2i_judge'
  async_eval:                 # presence of this block marks the runner async
    router_id: "<router id>"  # Orion router the job is POSTed to
    deployment_id: "<id>"     # EITHER: the judge deployment to forward to
    evaluator_key: "<key>"    # OR: a registry key the router resolves to a deployment
```

Set **exactly one** of `deployment_id` / `evaluator_key` (if both are set, `deployment_id`
wins). Also export `ORION_API_KEY` so the worker can authenticate to the router (see the
env-var setup above).

> **Where do the `deployment_id` / `evaluator_key` / `router_id` values come from?**
> Deployment IDs are **not** static — judges are redeployed and IDs change. Look up the
> current IDs in the evaluator registry rather than copying stale values:
>
> **https://dit-scale-up.s3.us-west-2.amazonaws.com/vlm_judge/evaluator_registry.html**
>
> Prefer `evaluator_key` over `deployment_id` when possible: the router resolves the key to
> the live deployment at dispatch time, so your config does not need updating each time a
> judge is redeployed.

## Consuming the Inference Wheel in Colligo

When CI merges a change to `main` it automatically builds and publishes a wheel to Artifactory.
The published version and the exact install command are printed in the GitHub Actions job summary
for the "Publish Wheel" step.

The wheel exposes a `gen6-conversational-inference` extras group that contains only the runtime
dependencies needed for inference (torch, mori, omegaconf, pydantic, …) — without the
training-only deps that require internal git sources and cannot be resolved from a standard PyPI
index.

### Step 1: Pin the version in your environment

In `envs/<your-env>/constraints.txt`, add the pinned version:

```
foundation_exploration[gen6-conversational-inference]==<VERSION>
```

For example:
```
foundation_exploration[gen6-conversational-inference]==20260514.91494335
```

**Finding a valid `<VERSION>`.** Every merge to `main` publishes a new wheel to `pypi-adobeshared-release`. Three ways to discover the version to pin:

- **Artifactory browse UI** (lists every published wheel, newest at the top): [`pypi-adobeshared-release-local/foundation_exploration/`](https://artifactory-uw2.adobeitc.com/ui/repos/tree/General/pypi-adobeshared-release-local/foundation_exploration). Note the underscore — recent publishes land here. (A stale hyphenated `foundation-exploration/` tree also exists from earlier builds; ignore it.)
- **Per-build CI summary** — the "Publish Wheel" step of the FE training workflow prints the version and a copy-pasteable `uv add` line in its job summary. Useful when you want the wheel built from a specific commit.
- **Programmatic** — `pip index versions foundation_exploration --index-url "https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple"` prints every published version (newest first). uv has no built-in equivalent today.

You don't pin transitive versions (mori, magi-attention, torch, etc.) directly — they're locked in by the wheel's `requires-dist`. To audit what your chosen `<VERSION>` actually resolves to, regenerate your env's lockfile (step below) and inspect it.

colligo's default uv configuration already exposes `pypi-remote` and `pypi-adobeshared-release`.
The inference closure additionally pulls from two indexes that aren't in the default set —
`pypi-kineto-release` (for `mori` and a number of its transitive deps) and the public
PyTorch CUDA 12.8 wheels. Add both to your env's `pyproject.toml`:

```toml
[[tool.uv.index]]
name = "kineto"
url = "https://artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-kineto-release/simple"

[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cu128"
```

The kineto index uses the same `ARTIFACTORY_UW2_API_TOKEN` you already have configured for
`pypi-adobeshared-release`; no new auth is required.

After editing, regenerate the lockfile:

```bash
./m deps.lock --env <your-env>
```

### Step 2: Declare the dependency in colligo.yaml

Add `foundation_exploration` to the `deps` list of your package's `colligo.yaml`:

```yaml
custom_pyenv: <your-env>
deps:
  - foundation_exploration
  # ... other deps
```

### Step 3: Handle mypy's import-untyped warning

The wheel does not ship a `py.typed` marker, so mypy emits `import-untyped` for every
`foundation_exploration.*` import. Suppress this in the repo-root `pyproject.toml`, scoped to
your modules only — a global entry would silence `# type: ignore[import-not-found]` comments
in packages whose environments don't install the wheel:

```toml
[[tool.mypy.overrides]]
module = [
    "colligo.models.your_package.*",
]
disable_error_code = ["import-untyped"]
```

> **Note**: The proper long-term fix is to add a `py.typed` marker to this wheel ([PEP 561](https://peps.python.org/pep-0561/)).
> Once that is done, all `disable_error_code` workarounds above can be removed.

---

## Development


### Conventions

- Counters in the code assume 0-index. This is also true for config options like `ema_start_step`
- The only exception is `train_step` which is 1-indexed. That is to say, the first training step is step `1`. 

### Preparing PRs

- Lint your code with `make lint` in the foundation_exploration directory
- Test your code with `make test` in the foundation_exploration directory
- Test your code in a distributed setting with `make test-dist` in the foundation_exploration directory (needs machines with at least 2 GPUs)
- Type check your code with `make type-check` in the foundation_exploration directory
- **Alternatively**, you can run `make prep-dev` to run all of the above at once

### Modifying the environment

To add a new dependency:
- Edit `pyproject.toml` in the `foundation_exploration` directory (add to `[project.dependencies]`, and pin in `constraint-dependencies` if needed).
- Run `make lock`.
- Add and commit the resulting changes to your branch. You can now run training on that branch with the new dependency.

### Adding new models to pre-caching

 - Upload model weights to `s3://dit-scale-up/frozen-models/model_weights/<model_name>`. `<model_name>` can be a folder or a checkpoint file.
 - Modify the `CACHE_CONFIGS` in `utils/cache_utils.py` for the new model.
 - Test it locally by executing `pre_cache_models([ <model_name> ])` in `utils/cache_utils.py`. 

### VSCode

The only-supported path for local jobs and distributed jobs is through `morictl`.
However, for convenience, there is an example `vscode.json` available in `misc` to launch local jobs via `vscode`'s job
launcher.
This is _not_ supported as `morictl` can do some pre-processing before launching the job, which is bypassed by using
`vscode.json`.

### Consuming a model from the Model Hub

The following instructions assume that you are trying consume a model hosted in the Model Hub by modifying your training config file, for example, switch from using the cliocore T5 text encoder to using the T5 text encoder hosted in the model hub. 

If all you want to do is use a model in the model hub you'd be better off reading the [Model Hub documentation](https://docs.ai.corp.adobe.com/v3/models/aidoc/index.html) directly.

#### Find your Model
First, you need to find the model that you are interested in using, check [here](https://docs.ai.corp.adobe.com/v3/models/aidoc/models/index.html) for a list of all the contributed models. Each model has documentation outlining the use cases, API, and configuration options.

#### Determine which model version to use
Next, you'll need to determine which version of the model you want to use. The model version that you install via pip defines both the code as well as the model weights that will be used. Once a model is contributed to the Model Hub the owners _should_ maintain backward compatability with the model API (input/output contract). It is possible, however that a new published version of a model will update the model weights (retraining, for example) changing the results that the model produces. As a result, it is recommended that users pin to a specific version of the model to avoid unexpected changes in model behavior.

If the model you are consuming is intended to be a drop in replacement for one that is already being used in the foundation exploration codebase then it is best to communicate with the model owners to ensure that it matches your requirements. The owner can tell you which version(s) are going to work. If you don't care about the version you can just use the latest one. To find the latest version look in the [tags](https://github.com/Adobe-Firefly/ai-platform/tags) of the AI Platform for a tag starting with the string `release/models`.

#### Getting the model into the training environment
The steps to add the model to the training environment are the same as what is described in [Modifying the environment](#modifying-the-environment). You can look for `models.tx_xxl` as an example.

#### Modifying your config file
Specifying a Model Hub model in your config file follows the same pattern as any other model in the codebase with a few caveats.

Here is an annotated example of consuming the T5Xxl model from the Model Hub.

```yaml
text_encoder:
  target: "models.t5_xxl.T5Xxl" 
  hub_params: # optional, if left blank then all default values are taken
    config: # Whatever config params your model exposes. See the model's documentation for options and default values.
      max_length: 256 
    device: "cpu" # optional, defaults to "cuda:0"
    binaries_root: "/path/to/binaries" # optional, advanced parameter. Override this if you want to manage downloading   
                                       # the model's binaries yourself. Most users will ignore this and just let the
                                       # system do this for them.
```

Lastly there are a couple code changes that might need to happen. 

First, if your code is using mori's `instantiate_from_config` you need to change to use `instantiate_from_config_with_hub` from `foundation_exploration.utils.config_utils`.

Finally, you are ready to use the model. You have 2 options:

1. Call the model's `execute` method directly (see [documentation](https://docs.ai.corp.adobe.com/v3/models/aidoc/models/index.html))
2. Use the `__call__` method. This is a convenience method that will call `execute` for you but might have some rough edges.

Here is a complete listing of how to instantiate and with a couple examples of calling the T5Xxl model from the Model Hub.

```python
from foundation_exploration.utils.config_utils import instantiate_from_config_with_hub
from omegaconf import OmegaConf

config = OmegaConf.create(
        {
            "target": "models.t5_xxl.T5Xxl",
            "hub_params": {
                "config": {"max_length": 256}
            },
            "device": "cuda:0"
        }
    )

model = instantiate_from_config_with_hub(config)

input_text = ["Hello, world!"]

# Option 1. Call the model's execute method directly.
output = model.execute(model.Input(text=input_text))
print(output.text_embeddings.shape)

# Option 2. Use the model's __call__ method providing keyword arguments. Internally just calls execute with model.Input(**kwargs).
output = model(text=input_text, padding=True)
# NOTE: The output is now converted to a dict with keys matching the Output model fields.
print(output["text_embeddings"].shape)

# Option 3. Use the model's __call__ method but provide a combination of args and kwargs.
# The ordering of args will follow the ordering that fields are defined in the model.Input
output = model(input_text, padding=True)
print(output["text_embeddings"].shape)
```



## Miscellaneous


### Github actions management

CI runs on Ethos-hosted GitHub Actions runners (the `fe-arc-*` runner groups),
provisioned via the Actions Runner Controller and managed in the `colligo-deploy`
Helm charts. See [aidoc/continuous-integration/overview.md](../../../../aidoc/continuous-integration/overview.md) for details.


### Batch Packing

- The generic batch packing and unpacking (without accounting for caching: TBD) are already defined in
  `src/foundation_exploration/models/model_utils/packing_utils.py`.
- As such, they should work for most use cases, and the most critical piece is the location of the packing and unpacking
  ops.
- In general, the workflow of the MLLMs should follow
   - Input Ids, Input images
   - Text Embedding, Vision Embedding
   - Replace <image_pad> token with Vision Embedding
   - Calculate the rope pos emb
   - **packing_op**(input_embeds, pos_embs, attention_mask)
     - let, b: batch_size, s: seq_len, d: dim, rd: rope_dimensionality(typically 3)
     - inputs:
       - input_embeds.shape: torch.Size([b, s, d])
       - attention_mask.shape: torch.Size([b, s])
       - pos_embs.shape: torch.Size([rd, b, s])
     - outputs: 
       - seq_lens: list([b, ])
       - packed_input_embeds.shape: torch.Size([1, sum(seq_lens), d])
       - packed_pos_embs.shape: torch.Size([rd, 1, sum(seq_lens)])
   - Transformer blocks
  - **unpacking_op**(hidden_states):
    - inputs:
      - hidden_states: torch.Size([1, sum(seq_lens), d])
    - outputs:
      - unpacked_hidden_states: torch.Size([b, s, d])

### Using access controlled buckets for training logs

**Usecase**: foundry projects where assets are customer IP and not all Adobe users should see the images / videos.

**How to use**:

Set the following in your config:
```yaml
launch:
  s3_experiment_folder_secure: true
  s3_experiment_prefix: ... # e.g. "s3://foundry-nbcu-adobe-assets/training_logs"
```

or directly set the following in your JOB:
    - Set `S3_EXPERIMENT_FOLDER=...` to desired bucket.
    - Set `S3_EXPERIMENT_FOLDER_SECURE=1`.
  
Once you do this, all assets will be uploaded to desired bucket, and .html / asset links will point
to a special service (`foundry-html-gateway`) that will first need you to log in to let you see images and videos. The mapping between s3 buckets and which pluto project members can view them is set in that service.

See [Foundry HTML Gateway](https://docs.ai.corp.adobe.com/pr-551/v3/services/services/firefly/foundry/apps/html_gateway/README.html) for more details.

### Running Foundry Jobs in us-east-2

Foundry has limited P6 capacity in the us-east-2 Pluto cluster.  When running training jobs in Ohio, you need to be sure that the checkpoint you're resuming from and your experiment storage are configured to buckets regionalized to us-east-2.  Foundry already automatically [provisions](https://github.com/Adobe-Firefly/foundry/blob/main/terraform/modules/franchise-storage/adobe-assets-bucket/main.tf#L3-L6) S3 buckets for each company/franchise in the us-east-2 region.

1. In your training configuration, set `launch.s3_experiment_prefix` to the S3 bucket corresponding to the franchise or company you're working on.  E.g. for NBCU this would be `s3://foundry-nbcu-adobe-assets-us-east-2`.  You can find a list of all these buckets in the Foundry Prod AWS account.
2. Set `checkpoint.resume_from.path` to be the S3 location of the starting weights for the model you are training.  Weights for Adobe-1P models in us-east-2 can be found in the bucket `s3://foundry-s3-cache-us-east-2`.
3. In your configuration, set `launch.node_group` to colligo-laser01-prod-ue2/colligo-laser01-prod-p6-b200-48x-02-gpu-efa-b200-03

If you are resuming from a base 1P Adobe model (i.e. *not* a prior checkpoint) that does not yet have weights in `s3://foundry-s3-cache-us-east-2`, then follow [these](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=GenAI&title=Runbook%3A+Reducing+Cross-Region+S3+Usage) instructions to perform a 1-time transfer of the base model from the us-west-2 bucket to the us-east-2 bucket.
