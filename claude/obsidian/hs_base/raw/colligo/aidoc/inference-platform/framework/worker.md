---
document_type: guide
---

# Inference Worker

```{seealso}
**Prerequisites**: Before reading this document, we higly suggest you have:
- Reviewed the [Inference Platform landing page](/aidoc/inference-platform/index.md)
- Got Access and set up your [development environment](/aidoc/inference-platform/index.md#quick-start-path)
```

```{admonition} Related guides
:class: hint
- [Adding an inference worker](/models/colligo/models/template/t1/aidoc/index.md)
- [Serving an application](/aidoc/inference-platform/user-guides/tutorials/serve.md)
```

An inference worker is a unit that can perform computational work. A worker is either invoked by another worker, or by an HTTP endpoint.

A collection of inference workers that depend on each other and can be deployed together (either on developer machine or cloud) are refered to as an application.

This document is a referenece guide for various components and best practices related to an inference worker.

## Required components of a worker

All colligo workers are located at `models/colligo/`. Each model has
- Request and response types: e.g. [the t5 model](/models/colligo/models/firefly/t5/types.py).
- Worker specific config: e.g. [the t5 model](/models/colligo/models/firefly/t5/types.py).
- The worker itself that defines a handle request function that  turns the request to the response: e.g. [the t5 model](/models/colligo/models/firefly/t5/T5Model.py). Here you need to couple the worker with its config type, e.g. via `T5Model(ColligoMLModel[T5Config])`.
- A build file that tells colligo about the request type, response type, dependencies (code, data), and finally the worker code: e.g. [t5 model](/models/colligo/models/firefly/t5/build.py).
- A `colligo.yaml` file that declares the model's dependencies and can optionally declare a `public` sub-package, e.g. [`autocomplete_bl/colligo.yaml`](/models/colligo/models/firefly/t5/colligo.yaml).

## Using local files in model workers
- A lot of model workers have their config files checked into the repo and the files are needed when loading the model.
- We maintain the file structure when uploading the code to S3.
- You can read the file directly in your model.py file and pass the file path as a worker config.
- If for local development you want to use a different file, you can override the file path in the colligo config file.
  - See [overriding worker config](/aidoc/inference-platform/framework/api.md#overriding-worker-config) for more details.
- As an example you can check [minlrm build.py](/models/colligo/models/substance3d/minlrm/build.py) file that uses config files, and the file paths are passed as a worker config.
- The files are then read in [MinLRMModel.py](/models/colligo/models/substance3d/minlrm/MinLRMModel.py) file.


## Worker Configuration

The worker configuration can have a default value in the `build.py` files. It can also be overriden through colligo configuration.

See [](/aidoc/inference-platform/framework/api.md#overriding-worker-config) for the API and where this config goes.


## The `colligo.yaml` file

**Related document**: [Build System](/aidoc/dependency-management/build-system.md)

In summary, the `colligo.yaml` file for each colligo worker is a file that mentions the 
1. The files that should be included when another worker depends on this worker's API.
2. Python dependencies for the code mentioned in item *1*.
3. Python dependencies for all the code.
4. Marking files as dev only (also known as `excluded`)

**More on 1 & 2**

It is possible to define a “public” part of a package. This allows _other_ packages that e.g. only need the `types.py` file _not_ to pull in all of the code during deployment.
Through this mechanism, it is also possible to model scenarios where package _A_ depends on package _B,_ which in turn depends on the public files of _A._

The `public:` subsection of `colligo.yaml` files contains dependencies. These work just like the top level dependencies, and can be auto-filled by the linter.
It also needs a list of files and directories under `files:`. Any listed directory will be included recursively.

A public dependency on a package uses the `[public]` suffix after the dependency name, as in `colligo.models.prompty_v2[public]`.

The `public` section is required if the package defines (a) worker(s) (i.e.`build.py` file is present). `public.files` and `public.deps` arrays contain files and dependencies needed for other workers to call this worker, respectively.

**More on 4**

`colligo.yaml` allows to exclude files and directories from packaging and dependency scanning.
By default, the `tests/` directory and `build.py` will be excluded. When providing a package-specific exclude list, it is possible to append the defaults [by adding `...`](/models/colligo/models/text2design/text2design_bl/colligo.yaml#L35-L37). (Quoting is not necessary, just a tooling artifact).

Excluding from dependency scanning means that any imports in these files won’t be added to the list of dependencies. When packaging for deployment, excluded files and directories aren’t added, either.

**Example**

```yaml
# Optional: dependencies required in worker code
deps:
- <dependency-a>
- <dependency-b>

# Optional: public sub-package
public:
  # Required: public files
  files:
  - types.py
  - preprocess

  # Optional: dependencies of public files
  deps:
  - <dependency-c>
  - <dependency-d>

# Optional: Excluded files
exclude:
- <excluded-file>
- ... # insert default excludes (build.py and tests)
```


## Application

Colligo uses the concept of applications to serve workers. The infra servers applications and not individual workers.

Applications can be registered at `models/build/app_....py` files via the `build.application(...)` syntax. For example [app_firefly.py](/models/colligo/models/build/apps/app_firefly.py).

You can pass a collections of workers to each application, then all those workres and their dependencies will be included in that application.

## Worker guidelines

- Always do post and pre-processing on the pipeline, and not the model. For example, let's say AdobeOne image encoder needs image input size 256. Do this resizing before sending the image to AdobeOne. Because:
  - sending the smaller image can save bandwidth.
  - the pre/post processing are CPU operations. Running them on the GPU worker, will waste GPU resources (as GPU will be idle waiting for CPU to do the pre/post processing).
- If you are using a `torch.Tensor` to refer to an image, always attach the range of the image to the tensor via `.with_image_range(...)`, so when it needs to be normalized or encoded, the code does not need to guess the range.
- Workers should only use data that they need. If you see a model is using more than 10GB of data, it should raise an eyebrow. __A common mistake is using non trimmed torch checkpoints that can be huge__!

## Public endpoints for workers

```{note}
Public endpionts are optional
```

By default each worker will have internal endpoints that you can call to via the inference SDK python code. But if you want nicer http endpoints that can be used by Javascript code you need to add them separately. That is because a lot of the common items in the internal request of each model are not JS friendly. E.g. images are tensors, but for JS requests you want them to be proper encoded images. 

For more details see <project:./endpoints.md>.


## Concurrency And Parallelism

### Overview

Inference Framework and platform provides several ways to control the concurrency and parallelism 
of workers.
This document explains the concepts and how to configure them.
We start from the most narrow concept and move to the broader ones.

### ML Thread Pool

Each ML worker extending `ColligoMLModel` class has a thread pool to perform ML work.
The size of the thread pool is controlled by `concurrent_ml_threads` parameter in the worker configuration.

The default value is 1.

If your worker code is thread safe, this parameter can be increased to allow concurrent execution of ML work
on the same device. This can be useful if your model doesn't fully utilize the device.
The parameter only controls the number of threads in the thread pool, and doesn't affect resource allocation in any way.

**Note**: If your model overrides `handle_request`, ML thread pool won't be used.
You explicitly need to call `self.ml_executor.run_in_bg(...)` to run ML work in the thread pool.

### Worker Replicas

When Inference Platform starts a worker it spawns several python processes: supervisor and a set of worker processes.
The number of worker processes is controlled by `workers_per_replica` parameter in the worker configuration.

The default value is 1. 
For CPU workers such as frontend workers `colligo-deploy` sets the default to 4.

If your worker is CPU bound or has a lot of IO work, you can increase the number of worker processes to utilize the CPU better.
Same applies to GPU workers which are not thread safe and are deployed to a node with larger GPU they can utilize.

It is important that each of the replicas consumes the amount of resources (GPU memory) defined in the worker configuration.
e.g. you won't be able to run 3 replicas of a worker that requires 20GB of GPU memory on a node with 40GB of GPU memory.

### Pod Replicas

Each application deployed in Ethos is represented by a Deployment and a ReplicaSet in k8s.
The number of replicas is controlled by `replicas` parameter in the application configuration.

The default value is 1. 

Increasing the value of `replicas` will create more pods in k8s, each running the same application code.

### Complete Example for Ethos

The example below summarizes all of the above concept configured in 
colligo-deploy for an application deployed in Ethos:

```yaml
rhode:
  applications:
    some_application:
      workers:
        foo_worker:
          # 2 pods will be created in k8s
          replicas: 2
          # Each pod will have a container running 2 python processes for workers
          workers_per_replica: 2
        bar_worker:
          # 1 pod will be created in k8s
          replicas: 1
          # Each pod will have a container running 1 python process for workers
          workers_per_replica: 1
      config:
        workers:
          foo_worker:
            # Each worker process will have a thread pool of size 1 to do ML work
            concurrent_ml_threads: 1
          bar_worker:
            # Each worker process will have a thread pool of size 4 to do ML work
            concurrent_ml_threads: 4
```

## Multi-Model Deployment and GPU Sharing

The Inference Platform supports deploying multiple ML models within a single worker pod, with intelligent GPU memory sharing. This enables efficient utilization of GPU resources when individual models don't require an entire GPU.

### Architecture Overview

Each model runs as a **separate Python subprocess** managed by the Rhode Supervisor. This provides:

- **Process isolation**: Models run independently and a crash in one model doesn't affect others
- **Independent scaling**: Different replica counts per model
- **Shared infrastructure**: Common metrics, logging, and status reporting

```
┌─────────────────────────────────────────────────────────────┐
│                     Rhode Supervisor                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Model A    │  │  Model B    │  │  Model C    │         │
│  │  (GPU 0)    │  │  (GPU 0)    │  │  (GPU 1)    │         │
│  │  20GB VRAM  │  │  10GB VRAM  │  │  30GB VRAM  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### GPU Memory Allocation

When multiple models are deployed, the framework automatically allocates GPU memory using a bin-packing algorithm:

1. **Models are sorted by memory requirement** (largest first)
2. **GPUs are allocated based on available capacity** 
3. **Memory fractions are enforced** via `torch.cuda.set_per_process_memory_fraction()`

#### Specifying GPU Requirements

In your `build.py`, specify GPU memory requirements using the `gpu` parameter:

```python
from colligo.base.types.deploy import GpuInfo

build.deploy_worker(
    name="my_model",
    worker_type=MyModel,
    request_type=MyRequest,
    response_type=MyResponse,
    gpu=GpuInfo(
        memory_gb=20,  # Maximum GPU memory this model can consume (in GB)
        count=1,       # Number of GPUs required (default: 1)
    ),
)
```

For CPU-only models, omit the `gpu` parameter or set `memory_gb=0`.

### GPU Isolation Mechanisms

The framework uses two mechanisms to enforce GPU boundaries:

1. **Memory Fraction Limiting**: PyTorch's `set_per_process_memory_fraction()` caps memory usage per process
2. **CUDA_VISIBLE_DEVICES Isolation**: Each subprocess only sees its assigned GPU(s)

```{warning}
Some libraries (notably vLLM) don't respect `torch.cuda.set_current_device()` and attempt to occupy all visible GPUs. The framework works around this by setting `CUDA_VISIBLE_DEVICES` for each subprocess, which is a "nuclear option" that the model cannot bypass.
```

### Configuring Replica Counts

You can control how many instances of each model to run using the `replicas` parameter:

**Via command line (for local development):**
```bash
python -m colligo.rhode.commands.models_supervisor \
    --app-config /path/to/config.json \
    --replicas model_a 2 \
    --replicas model_b 1
```

**Via colligo-deploy configuration (for Ethos):**
```yaml
rhode:
  applications:
    my_app:
      workers:
        adobe_one_image_v2:
          replicas: 2 # Number of pods for this worker
          autoScaler: disabled # Advised to disable auto-scaling for multi-model
          additional_workers:
            # Additional models to co-locate with the primary worker
            # Format: worker_name: replica_count
            nsfw_adobe_one: 1
```

The `additional_workers` field allows you to specify additional models that will be deployed alongside the primary worker in the same pod, sharing the GPU resources.

### Fill Remaining GPU Capacity

For applications where you want to maximize GPU utilization, you can use the `fill_with_model` option to automatically create additional replicas of a specific model using any remaining GPU capacity:

```python
from colligo.base.types.deploy import ReplicaCount

replicas = ReplicaCount(
    counts={"model_a": 1, "model_b": 1},
    default_value=0,
    fill_with_model="model_a",  # Auto-fill remaining GPU capacity with model_a
)
```

### Limitations and Considerations

| Limitation | Description |
|------------|-------------|
| **Soft Memory Enforcement** | `set_per_process_memory_fraction()` is a PyTorch feature and may not be respected by all libraries |
| **No CUDA MPS** | The framework uses process isolation rather than NVIDIA's Multi-Process Service (MPS). Models time-share GPU compute rather than truly sharing simultaneously |
| **Memory Fragmentation** | GPU memory fragmentation can occur if multiple models allocate/deallocate frequently, potentially causing OOM errors |
| **Multi-GPU Models are Exclusive** | If a model requires multiple GPUs (`count > 1`), those GPUs are exclusively assigned to that model |
| **Static Allocation** | GPU assignments are made at startup and don't change dynamically based on load |
| **vLLM and Similar** | Libraries that aggressively claim GPU memory require `CUDA_VISIBLE_DEVICES` isolation (handled automatically) |
| **Predictive Autoscaling** | Autoscaling may behave unexpectedly when co-located models have very different latencies, as the autoscaler bases decisions on aggregated metrics. Consider disabling autoscaling (`autoScaler: disabled`) or thoroughly testing autoscaling behavior for your specific model combination |

### Best Practices

1. **Accurate Memory Estimates**: Specify `memory_gb` as accurately as possible. Too low may cause OOM; too high wastes resources.

2. **Test Locally First**: Use the dev supervisor to validate multi-model deployments before cloud deployment:
   ```bash
   python -m colligo.rhode.commands.dev_supervisor --app-config /path/to/config.json
   ```

3. **Consider Model Compatibility**: Some models work better together than others. Avoid pairing models with unpredictable memory patterns.

4. **Use GPU-Based Overrides**: For models that can adapt to different GPU types, use [GPU-based overrides](/aidoc/inference-platform/framework/gpu-based-overrides.md) to optimize resource usage.
