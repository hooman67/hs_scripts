---
document_type: tutorial
---

# Tutorial for making an inference application

Refer template application: [/models/colligo/models/template/t1](/models/colligo/models/template/t1/)

To help expedite adding a new application onto AI Platform monorepo, we have created a template. This application is very simple, it takes in the user's input, prepended it with "Hello World", and return that to the client. The goal is to make it faster for new users to build an inference worker. 

This page serves as documentation for this template. Hopefully by going through this documentation, the reader will have a deeper understanding of the inference platform.

This template serves as a jumping off point to make it faster to make new applications.

For first time users, we would recommend the following steps:
1. Go through this guide
2. Make a copy of the template application, and rename it.
3. Start adding code to make your new app.

## Overview

This guide will be a bottoms up approach. Here are the steps we will follow:

Step #1: Identify where you want to place your new application

Step #2: Implement the core logic 

Step #3: Build the inference worker and wrap the core logic described in Step #1.

Step #4: Registering the worker with Inference Platform

[Optional] Step #5: Expose the worker via a public endpoint

[Optional] Step #6: Storing models on cloud storage

Let's go through each step in detail.

### Identify where you want to place your new worker

In the colligo framework, each directory in the /models/colligo/models/ directory represents a collection of applications typically bundled by products or teams. Each application is a collection of one ore more workers.

Identify where you want to place the new worker. Create a new directory to represent this worker. 

For the purpose of this guide, we are creating a directory named t1 [/models/colligo/models/template/t1](/models/colligo/models/template/t1/)

### Implement the core logic

The first step is to implement the core logic. For our purposes, our application is to simply take in some text prompt from the user, and then add "Hello World!" before the prompt, and display it. 

For this, first we will create a src package [/models/colligo/models/template/t1/src](/models/colligo/models/template/t1/src)

Within that we will create a respond.py within the and implement the respond_to_user function.

(One can imagine extending this to receiving text from a user, and then sending said text to a ML model, and then returning that text back).

In this case, our logic is simply:
<blockquote>

```{colligo_docstring} colligo.models.template.t1.src.respond:respond_to_user
```

</blockquote>


```py
def respond_to_user(prompt: str) -> str:
    return "Hello World!" + prompt
```
Now that we have our core logic done, in the following steps, let's create the worker class that will be used to wrap the core logic.


### Implement types.py

Next we will create a worker directory [/models/colligo/models/template/t1/worker](/models/colligo/models/template/t1/worker)

Within the worker directory, let's create a new python file [models/colligo/models/template/t1/worker/types.py](/models/colligo/models/template/t1/worker/types.py) 

Define the input type class (TemplateRequest) and output type class (TemplateResponse). They should extend the BaseModel class from colligo.base.types.common

Define a config class TemplateConfig that extends the BaseWorkerConfig class from colligo.base.types.deploy

Define an executor class TemplateExecutor that must extend the BaseExecutor class from colligo.base.worker_registery. This class will be used to call the worker.

The executor class must have a name attribute that is the name of the worker. This name will be used to identify the worker in the inference platform.

This will describe the worker name, input/output types, configuration and an executor that will be used to call the worker.


```py
from colligo.base.types.common import BaseModel
from colligo.base.types.deploy import BaseWorkerConfig
from colligo.base.worker_registery import BaseExecutor

# The name that the inference platform will now the worker with
TEMPLATE_WORKER_V1 = "template_v1"

# Represents the input to the worker
class TemplateRequest(BaseModel):
    prompt: str

# Represents the output from the worker
class TemplateResponse(BaseModel):
    result: list[str]

class TemplateConfig(BaseWorkerConfig): ...

class TemplateExecutor(BaseExecutor[TemplateRequest, TemplateResponse]):
    # This is an object that will be the interface to call the worker.
    # response = await TemplateExecutor.call(request)
    name = TEMPLATE_WORKER_V1
```

### Build the inference worker and wrap the core logic described in Step #1.

In this step, we will make a worker that will take in `TemplateRequest` and respond with `TemplateResponse`.

Let's create a new file called template_worker.py within the worker directory [models/colligo/models/template/t1/worker/template_worker.py](/models/colligo/models/template/t1/worker/template_worker.py) and define the worker class. 

Workers can one of the two types:
(1) Pipeline workers (must extend ColligoPipeline): Primarily used for orchestrating workflows, calling other workers, and async I/O.
(2) ML workers (must extend ColligoMLModel): Heavy GPU/CPU computation. Used for model inference and compute-intensive tasks.

For the purpose of this tutorial we will only build an ML worker

This ML worker class must extend the ColligoMLModel class from colligo.base.types.worker and implement the load_model, warmup_model and handle_model_request methods. These methods will be called during the worker's lifecycle.

```py
import logging
 
from colligo.base.types.worker import ColligoMLModel
from colligo.models.template.t1.src.respond import respond_to_user
from colligo.models.template.t1.worker.types import TemplateConfig, TemplateRequest, TemplateResponse
 
logger = logging.getLogger(__name__)
 
 
class TemplateWorker(ColligoMLModel[TemplateConfig]):
    def load_model(self) -> None: ...
 
    def warmup_model(self) -> None: ...
 
    def handle_model_request(self, request: TemplateRequest) -> TemplateResponse:
        prompt = request.prompt
        response = respond_to_user(prompt)
        return TemplateResponse(result=[response])
```

This worker object will serve as our main entry point to our application. 

Create a colligo.yaml file in same directory. [models/colligo/models/template/t1/worker/colligo.yaml](/models/colligo/models/template/t1/worker/colligo.yaml). This file indicates the dependencies and defines the public API (i.e. what files other packages can import)

```yaml
public:
  files:
  - types.py
  deps:
  - colligo.base
deps:
- colligo.models.template.t1.src
```

### Registering the worker with Inference Platform

We have our core logic setup. Now, it's time to register it with inference platform so we can run it!

So far, we have written code that will do the work we want. But now, we need to figure out how to instantiate the objects we have created.

We will add [/models/colligo/models/template/t1/worker/build.py](/models/colligo/models/template/t1/worker/build.py) file so that inference platform will know how to instantiate the worker we just created. The build file should be in the same python module as the worker. Here we will deploy the worker that we just created. Include the correct request and response types we created in step #3. 

```py
import colligo.models.build.api as build
from colligo.models.template.t1.worker.types import (TEMPLATE_WORKER_V1, TemplateRequest, TemplateResponse, TEMPLATE_ENDPOINT)
 

build.deploy_worker(
    name=TEMPLATE_WORKER_V1, # Name of the worker. This name is used to find the correct worker
    worker_type="colligo.models.template.t1.worker.template_worker.TemplateWorker", # Class of the worker
    request_type=TemplateRequest,  # type: ignore[arg-type]
    response_type=TemplateResponse,  # type: ignore[arg-type]
    gpu=build.gpu_info(memory_gb=4),
    # *optional* - list of endpoints, read along for more details
    # public_http_endpoints=[TEMPLATE_ENDPOINT],
    # *optional*
    # supports_batch=False,
)
```
This is telling inference platform that we are making a worker. The worker is being identified by the name, `TEMPLATE_WORKER_V1`, and this symbol will be used throughout inference platform to refer to our application. This also defines other things about the worker:

1. The input is of type `TemplateRequest` (which matches the signature of `handle_model_request` inside `TemplateWorker`)
2. The response type is `TemplateResponse` (again, matching the signature of `handle_model_request`)
3. We are specifying 4GB of GPU memory for our model. (Our application doesn't actually use any GPU memory, but it's included here for illustrative purposes)
4. We specify a list of *optional* http endpoints that our worker will be hooked up to. In this case, it's just one endpoint, which we defined earlier

> `supports_batch=false` is needed when you want inference platform to break your request to separate instances (break a batch), send to separate workers, then stitch them. This is useful for workers whose request is actually a batch, but running the batch on a single worker is slow and we want it to be split when calling the worker. 
Note that this will then impose constraints on what kind of objects are allowed in your request or response. **Most of the time, you can just leave this parameter to have its default `true` value**.


### Expose the worker via a public endpoint

If you want to test your worker via the inference platform's debug UI, you can expose the worker via a public endpoint. To do this, let's create an endpoint definition in the types.py file. Let's add these lines to the types.py file we created in step #3: [/models/colligo/models/template/t1/worker/types.py](/models/colligo/models/template/t1/worker/types.py) file:

```py
from colligo.base.types.deploy import (
    BaseWorkerConfig,
    MimeType,
    OpenAPITag,
    PublicEndpoint,
)
 
TEMPLATE_ENDPOINT = PublicEndpoint(
    path="v1/template",
    allowed_request_encodings=[MimeType.JSON],
    allowed_response_encodings=[MimeType.JSON],
    requires_upload_endpoint=True,
    tags=[OpenAPITag.Public, OpenAPITag.V2],
    sample_request=TemplateRequest(prompt="sunny beach").model_dump_json(),
    request_type=TemplateRequest,  # type: ignore[arg-type]
    response_type=TemplateResponse,  # type: ignore[arg-type]
    operation_id="template_operation",
    is_async=False,
)
```

Now that we have defined the endpoint template, next we need to modify the build.py file to include the public endpoint. Open the [/models/colligo/models/template/t1/worker/build.py](/models/colligo/models/template/t1/worker/build.py) file and populate the `public_http_endpoints` attribute list with the endpoint we just created.

Now that we have defined the worker, we need to make an application that has the worker as a member. Inference platform works with applications which are collection of workers that can depend on each other. In this case, our application has just one worker inside it. 

This is done inside of [models/colligo/models/build/apps/app_debug.py](/models/colligo/models/build/apps/app_debug.py)

Include the following line to build the application. 

```py
from colligo.models.template.t1.worker.types import TEMPLATE_WORKER_V1
 
build.application(name="template_v1_spec", deployments=[TEMPLATE_WORKER_V1])
```

### Storing models on cloud storage ie S3

If serving a ML model, we need a way to load that model onto Colligo. It's usually not feasible to store model weights as part of the git repo. Instead, the preferred practice is to upload the model weights to some remote, cloud storage, and then have the worker download them when they are deployed. Currently, the preferred storage for model weights is S3.

For our example, let's say we have a text file with the prefix "Hello World!" We want our application to download this text file from S3, and read the prefix from file. And then, when it's running, it will read the prefix from file and use that, instead of being hard coded.

This section is a quick summary of how to upload/download models. For more information, refer to the official docs at: [Dependency Management](/aidoc/dependency-management/monorepo-tutorials.md)

#### Uploading

First, we make the text file, and call it hello.txt

Next, we will tar the file using: `tar -zcvf hello.tar.gz hello.txt`

Now, we will upload to S3 with: `./m deps.upload_artifact models/colligo/models/template/t1/artifacts/hello.tar.gz template`

(The form of the command is `./m deps.upload_artifact <path to artifact> <group name>`)

This will upload the artifact to S3. It will also spit out information about how to download the artifact. It will look something like:

```
build.s3_source(
        bucket="s3://colligo-dev-artifacts/artifacts-v1",
        key="template/hello.tar.2024-09-09.11-52.2a527.gz",
        version_id="CpaCxFL7g4X71fsi9ijmKDB5nIL6uHwk",
        sha256="2a5277d47f2739af82ddda198e208a5016a5a229a32e5299122d3f9e1a7ccd56",
)
```

#### Downloading

To download the artifact that we have just uploaded, we need to modify the build.py file. As part of the build process, Colligo needs to know what artifacts the worker will need to download/unzip. Once it knows, it will download and unzip these files on to disk before it tries to load any models.

We modify the [build.py](/models/colligo/models/template/t1/worker/build.py) file like this:

```py
PREFIX_ARTIFACT = build.archive_source(
    archive_type="targz",
    source=build.s3_source(
        bucket="s3://colligo-dev-artifacts/artifacts-v1",
        key="template/hello.tar.2024-09-09.11-52.2a527.gz",
        version_id="CpaCxFL7g4X71fsi9ijmKDB5nIL6uHwk",
        sha256="2a5277d47f2739af82ddda198e208a5016a5a229a32e5299122d3f9e1a7ccd56",
    ),
)
 
build.deploy_worker(
    name=TEMPLATE_WORKER_V1,
    worker_type="colligo.models.template.worker.template_worker.TemplateWorker",
    supports_batch=False,
    request_type=TemplateRequest,
    response_type=TemplateResponse,
    gpu=build.gpu_info(memory_gb=4),
    public_http_endpoints=[create_template_endpoint()],
    is_async=False,
    data=[  # List of artifacts to download. The name field is what we will use later to load from disk
        build.data_item(
            name="prefix",
            source=PREFIX_ARTIFACT,
        ),
    ],
)
```

We only added the data field to the deploy_worker method. This field provides information to Colligo about what artifacts should be downloaded.

Finally, we just need to have our worker load the downloaded text file from disk. 

```py
class TemplateWorker(ColligoMLModel[TemplateConfig]):
    prefix: str = ""
 
    def load_model(self) -> None:
        """We can load any models from disk into memory here"""
        prefix_file_path = self.get_file("prefix").path / "hello.txt"
        self.prefix = prefix_file_path.read_text()
```

`self.get_file` is used here to find out where the "prefix" artifact is downloaded onto disk.


## How to run your application locally?

### On same process as you python code

We have an example in [models/colligo/models/template/t1/scripts/sandbox.py](/models/colligo/models/template/t1/scripts/sandbox.py). It is based on [inference sdk](/pylibs/colligo/sdk/aidoc/index.md#using-sdk-to-run-models-locally-eg-in-jupyter-notebook)

### As separate service and calling via HTTP

We can run inference platform dev entry point via this command line: `python -m colligo.rhode.commands.dev_supervisor --spec template_v1_spec` (Or through the run and debug GUI on VS code and selecting template_v1_spec) 

If running on Pluto, we may need to do port forwarding 

Then you can either
- Call via [inference sdk](/pylibs/colligo/sdk/aidoc/index.md), this does not need a public endpoint.
- Call the model via debug UI (go to localhost:8000 in your browser), this would need having a public endpoint.

To summarize, we will now illustrate this flow from the top down:

First, `python -m colligo.rhode.commands.dev_supervisor --spec <spec_name>` was ran. This will look for `<spec_name>` defined in an `app_<x>.py`. In our example, <spec_name> is `template_v1_spec`, and it is defined in `app_debug.py`.  From `app_debug.py`, we are telling Colligo to look for a worker named `TEMPLATE_V1`. This worker is defined in our `build.py` script, which is pointing to the `TemplateWorker` class as the entry point to our endpoints.

```{mermaid}
:caption: flow from the top down.
---
config:
  theme: neutral
  
---
flowchart TD
    A[colligo.rhode.commands.dev_supervisor] --> B[colligo.rhode.commands.workers.model_worker]
    B --> C[TemplateWorker]
```


For a more detailed tutorial on running applications see <project:/aidoc/inference-platform/user-guides/tutorials/serve.md>

## Unit tests

It is strongly recommended to also add a unit test for your worker. We have included an example in [models/colligo/models/template/t1/tests/test_template_worker.py](/models/colligo/models/template/t1/tests/test_template_worker.py)

The unit test uses the [inference sdk](/pylibs/colligo/sdk/aidoc/index.md) to call the worker.

You can learn more about unit testing and its guidelines at <project:/aidoc/testing/index.md>
