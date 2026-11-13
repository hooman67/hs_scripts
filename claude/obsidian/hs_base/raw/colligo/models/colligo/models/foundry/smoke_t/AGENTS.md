# Load test work

I want to make scome scripts to check the health of a deployed service at https://gen-foundry-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/

In all instructions below, assume $RepoRoot is the colligo/ repository root folder at ../../../../../ relative to this AGENTS.md.

## Task

### Design

I want to structure the files in the following format

```
shared/
  # any shared utility needed.

nbcu_gabby/
  artifacts/
    .gitignore # artifact manifest
  # Payloads for a few test cases. To be added by you!
  # Allow using inheritence for test cases to make files ismpler
  # e.g. each case can say inherits: ... from a common section.
  gen5-image.yaml
  gen6-image.yaml
  gen6-video.yaml
  # Register the inputs, e.g. have a function get_inputs() that returns
  {endponit: test case}
  __init__.py 
  
<other workstream if needed>/

# entrypoint to run the tests
__main__.py
```

### Entrypoint params

- `--host` The host prefix to test, default https://gen-foundry-dev.ethos851-stage-or2.ethos.adobe.net/ 
- `--token` The token to use. If not provided use the method I have in application token section below.
- `--num-users` Have this many users send request, keep poll for result. Once done, send next one. 
- `--duration`: How long to keep sending request. Once this amount passes and all users are done, stop.
- `--timeout`: after this one user give up and send next requst, call this request abandoned.

Then generate a report with a table that has

endpoint, request status, average time taken  

The status can be
- failed to place job (upload assets, get links, ...)
- job placed, response never retreived by status in timeout
- job placed, got failed repsonse.
- job placed, response came back as done.


### Gabby test cases

For gabby test cases include these:
- /v1/images/generate-async: An instruct edit image request. use first frame and ask for some change (e.g. change gabby's pose). 
- /v1/images/generate-async: A text to image request
- /v1/foundry-gr6/image: A text to image request
- /v1/foundry-gr6/video: A text to video with audio
- /v1/foundry-gr6/video: A text to video with audio with first frame and audio condition

You can find various gabby assets and instructions from links below. This will required an auth token for assets, prompt me to give it to you. The default one I mentioned below wont work.

- gen6-video: https://foundry-html-dev.corp.ethos851-stage-or2.ethos.adobe.net/asset/foundry-nbcu-adobe-assets-us-east-2/training_logs/FFP-64647-dit-FFP-70631-gr6_ultra_prod_beta_hr_conversational_gabby_base_i2v_specialist_24fps-2026.01.18-17.37.52/inference/gr6_ultra_prod_beta_hr_conversational_gabby_base_i2v_specialist_24fps_step00309000_ema=True_2026-01-20T02:12:16/inference_gabby_ai2v_480p_3sec_ema_2026-01-20T02:54:56_7ce9e79e-fe87-4361-af75-8b9a0152d836/index.html
- https://adobe-xingtail.s3.us-west-2.amazonaws.com/foundry/visualize_results.html

If there are pictures you need from links above, you can download and add the the `gabby/artifacts`. (you need to pull the assets using the lfs.pull I mention below)

## Context

### URL access

Access all from local machine. Do not use remote sandbox feb fetch. You will be blocked.

### Endpoints

The API schema is at https://gen-foundry-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/docs/openapi.json

Endpionts that need binaries, need to upload it first and get a id through the following endpoint
- /v2/storage 

The endpoints we are interested in are:
- /v2/images/generate: Image 5 generation 
- /v1/foundry-gr6/video: Video 6 (gen6) generation
- /v1/foundry-gr6/image: Image 6 (gen6) generation

After you submit a job with above, you can then use the
- /jobs: query status or cancel the async jobs

The flow is that one will post a request through the generation endpoints (group 1). Then you get a set of links to cancel to query the status.

Status will return either
- In progress
- cancelled/timed out/ failed
- Done. With the response.


### Python venv

Development happens from $RepoRoot/.venvs/dev/bin/activate.

If the env does not exist, you can create it by running `./m deps.create` from the $RepoRoot.

### Authentication token

The APIs above need a token. you can use this code snippet to get one.

```py
from colligo.base.config import get_config
from colligo.external_services.ims.ims_service import (
    create_ims_service_with_credentials,
)

ims_config = get_config().dev_ims_credentials
ims_service = create_ims_service_with_credentials("http-client", ims_config)
token = await self.ims_service.get_token()
```

### Code quality

Before calling something done, make sure that
```
./m lint
```
passes.

Also make sure any unit tests for the module you are developing passes. 
```
. .venvs/dev/bin/activate
pytest <path to the test folder>
```

### Checking in binaries

Binaries should not be checked in directly . To check in binaries, you can use the command on a folder
```
./m lfs.sync <path to folder>
```
it makes a specical .gitignore that when you check in means binaries are checked in

To download binaries, you can do
```
./m lfs.pull <path to folder>
```
it recusrively finds all <binary> folders and downlaods their assets.