# Unified Foundation Exploration Codebase

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [Pluto GPU Machine Quickstart](#pluto-gpu-machine-quickstart)
- [Code Structure](#code-structure)
- [MoriCTL](#morictl)
- [Training Environment](#training-environment)
- [Training](#training)
  - [Launch spec](#launch-spec)
  - [CUDA Sync Debug Mode](#cuda-sync-debug-mode)
  - [Resuming jobs:](#resuming-jobs)
  - [Monitoring training jobs](#monitoring-training-jobs)
- [Inference](#inference)
  - [Overview](#overview)
  - [Yaml Spec](#yaml-spec)
  - [Examples](#examples)
    - [Diffusion](#diffusion)
    - [MLLM Evaluation](#mllm-evaluation)
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

Docker: `docker-matrix-experiments-snapshot.ff.adobe.io/training-base-11-27-25:12.8.1-runtime-ubuntu22.04-NCCL-v2.27.3-1-eagain-fix4-PY-3.10`

To update the Docker image, see the [build-image repository](https://github.com/OneAdobe/build-image) - [FE Training Image Section](https://github.com/OneAdobe/build-image?tab=readme-ov-file#add-additional-linux-packages-to-fe-training-image). The Dockerfile is [Dockerfile.advanced](https://github.com/OneAdobe/build-image/blob/main/Dockerfile.advanced).

When transitioning to a new dockerfile, the following should be updated in the code
- [ ] The reference docker image url in README.md
- [ ] The docker image urls in the training and interactive [configs](configs)
- [ ] The docker image used for action runners in [scripts/ci/launch.py](scripts/ci/launch.py). Then the action runners should be re-lauched.

## Pluto GPU Machine Quickstart

First, make sure you have these environment variables set on your local machine:

```bash
export LDAP=...
export WANDB_API_KEY=...
export GITHUB_TOKEN=...
export SLACK_MEMBER_ID=...
export DATA_LINEAGE_TOKEN_PATH=... # Path to a file containing your Data Lineage token (see details below)
```

* `WANDB_API_KEY` can be obtained at our self-hosted Weights and Biases instance, [here](https://adobesensei.wandb.io/home).
* `GITHUB_TOKEN` can be created [here](https://github.com/settings/apps), or by asking around for the token that everyone shares (this is not good practice)
* `SLACK_MEMBER_ID` can be obtained by visiting your Slack profile, clicking the hamburger for the drop down menu, and then selecting "Copy Member ID".

* `DATA_LINEAGE_TOKEN_PATH` is required to access internal Adobe datasets. You can obtain your Data Lineage token by following the instructions [here](https://wiki.corp.adobe.com/display/adobestock/How+to+request+access+to+training+data+and+get+a+token).
Save the token to a file — preferably stored on S3 — and set the environment variable to point to that file.
Example:
```bash
export DATA_LINEAGE_TOKEN_PATH="s3://colligo-dev-artifacts/lineage-v1/token/default_lineage_token.txt"
```

Then, install `morictl`:

```bash
make morictl
```

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

To add a new dependency, first `cd` to the following directory.
```bash
cd "${MORI_BASE}/collections/foundation_exploration/training_env"
```
Then:
- Edit the `requirements.yaml` with the required dependency.
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

See docstring in [scripts/ci/launch.py](scripts/ci/launch.py) for more details.


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
