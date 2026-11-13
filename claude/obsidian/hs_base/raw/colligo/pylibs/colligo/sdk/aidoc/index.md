---
document_type: tutorial
---

# Inference SDK


AI Platform inference SDK is a pip package that allows easy running or calling inference workers without the full monorepo developer env, e.g. in a jupyter lab.

**The SDK can be used either via a `pip` package (without monorepo dev env setup), or from the monorepo dev env.**

<!-- If you are interested in versioning scheme for these wheels and how they are uploaded see [guides/misc/wheels](../misc/wheels.md). **Note that you don't need this info to actually use them**. -->

Within [monorepo dev env](/aidoc/monorepo/env-setup.md), the SDK is readily available.

To install as pip package, use the following (torch is currently required separately):

```
pip install -U           \
  torch                  \
  "adobe-aip[inference]"   \
  --extra-index-url=https://:$ARTIFACTORY_UW2_API_TOKEN@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple
```

If you need help setting up the Artifactory credentials, see the page [Set Artifactory credentials](https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/cli-using.html#set-artifactory-credentials).

Above works if you want to run workers remotely, if you want to run workers locally, you need to
replace `adobe-aip[inference]` with `adobe-aip[inference-workers]` *or* alternatively manually download the dependencies of the worker that you need to work with.

## Using SDK to call into models served remotely

```python
import asyncio

from colligo.base.worker_registery import set_worker_registery
from colligo.base.request_ctx import RequestContext, set_request_ctx
from colligo.models.firefly.t5.types import T5Executor, T5Request, T5ModelName
from colligo.sdk import HttpClient

# See up to date URLs at: https://wiki.corp.adobe.com/x/vT6atg
# Note: this is an example -- corp endpoints are only accessible from VPN
HTTP_ENDPOINT = "https://clio-imaging-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net"
# You may need to set AUTH_TOKEN here depending on your configuration

# (for devbox use the relevant URL in the link above)
# HTTP_ENDPOINT = "https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net"
# AUTH_TOKEN = <see `https://git.corp.adobe.com/pages/colligo/guides/integration-tests/cli-tool.html#local-ims-setup-for-remote-endpoints` how to retrieve it>
# You have to pass the auth_token to HttpClient too.

async def main() -> None:
    # Using HTTP to contact the worker
    set_worker_registery(HttpClient(HTTP_ENDPOINT))
    # When using an authentication token, don't forget to add the token with:
    # set_worker_registery(HttpClient(HTTP_ENDPOINT, AUTH_TOKEN))

    request = T5Request(prompts=["My name is Mike"])
    response = await T5Executor.call(request, model_name=T5ModelName.T5_V2)
    print(response)


asyncio.run(main())
```
<!-- 
```{admonition} Authentication
:class: attention
There are two way to set the IMS authentication to call models served remotely:
1. Using the config file `colligo.dev.yaml` mentioned at [using external server for some models](./local-run.md#running-the-project). Note that if you are not in colligo development environment (e.g. pip install), you would need to point colligo SDK to the config file via defining the `COLLIGO_CONFIG_PATH=...` env variable.
2. By directly setting the token `AUTH_TOKEN` in the code, and setting the worker with: `set_worker_registery(HttpClient(HTTP_ENDPOINT, AUTH_TOKEN))`. FYI, the IMS token is a very long string that starts with *"ey"*, which you can find in the Debug UI (click on the button: *Copy access token*).
``` -->

````{admonition} Warning about Numpy
:class: note
When running the code above you may get the following warning (depending on version of torch installed):
```
UserWarning: Failed to initialize NumPy: No module named 'numpy' (Triggered internally at /Users/runner/work/pytorch/pytorch/pytorch/torch/csrc/utils/tensor_numpy.cpp:84.)
  t = torch.empty((0,), dtype=storage.dtype, device=storage._untyped_storage.device)
```
it is just a warning, you may ignore it.
````

## Using SDK to run models locally (E.g. in Jupyter notebook)

```python
import asyncio
from pathlib import Path

from colligo.base.worker_registery import set_worker_registery
from colligo.models.firefly.clio.types import CLIO_V2, ClioExecutor, ClioRequest
from colligo.sdk import NativeClient


async def main() -> None:
    registery = await NativeClient.create([CLIO_V2])
    set_worker_registery(registery)

    request = ClioRequest(gi_PROMPT="A man in black suite", gi_SEED=[132434, 234])
    response = await ClioExecutor.call(request)
    images = await tensor_to_encoded_images(response.OUTPUT_GEN_IMAGE)
    for i, image_tensor in enumerate(response.OUTPUT_GEN_IMAGE):
        # You can use PIL to convert `image_tensor` to your desired format.
        pass


asyncio.run(main())
```

### Calling workers remotely 

Note that this mode, also supports delegating some workers to remote endpoint, via the configuration in the `colligo.dev.yaml` file. To learn more, see the comments in [colligo.dev.example.yaml](/colligo.dev.example.yaml) under `Calling models remotely` on how to use the feature.


## Jupyter example

You can find a jupyter example of using the SDK here [colligo_sdk_example.ipynb](https://git.corp.adobe.com/hoshyari/colligo-experiments/blob/main/colligo_sdk_example.ipynb)

