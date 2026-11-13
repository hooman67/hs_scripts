# Foundry Smoke / Load Test

Scripts to check the health of a deployed Foundry service by running concurrent requests against its generation endpoints.

## Setup

```bash
# From the repo root
./m deps.create          # create dev venv (if not already)
. .venvs/dev/bin/activate

# Pull binary test assets (images, audio)
./m lfs.pull models/colligo/models/foundry/smoke_t/nbcu_gabby/artifacts
./m lfs.pull models/colligo/models/foundry/smoke_t/wdi/artifacts
```

## Usage

```bash
python -m colligo.models.foundry.smoke_t [OPTIONS]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--host` | `https://gen-foundry-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net` | Service host URL |
| `--token` | *(auto via IMS)* | Bearer token. If omitted, uses `dev_ims_credentials` from colligo config |
| `--num-users` | `1` | Number of concurrent simulated users |
| `--duration` | `0` | How long (seconds) each user keeps working. 0 = run a single pass over all tests. |
| `--log` | `smoke.log` | Path to write debug-level logs to |
| `--only-project` | *(all)* | Only run cases from these projects. Repeatable (OR) |
| `--only-endpoint` | *(all)* | Only run cases whose endpoint contains this substring. Repeatable (OR) |

## Examples

```bash
# Quick single-pass smoke test (run each case once, the default)
python -m colligo.models.foundry.smoke_t

# 5-minute load test with 2 concurrent users. I recommend to do this at least
# for 30 min before deploying anything to prod.
python -m colligo.models.foundry.smoke_t --num-users 2 --duration 300

# Test against a different host
python -m colligo.models.foundry.smoke_t --host https://gen-foundry-dev.ethos851-stage-or2.ethos.adobe.net

# Provide an explicit token instead of auto-obtaining via IMS
python -m colligo.models.foundry.smoke_t --token "$MY_TOKEN"

# Only run video endpoint tests for the nbcu_gabby project
python -m colligo.models.foundry.smoke_t --only-project nbcu_gabby --only-endpoint foundry-gr6/video

# Only run tests for the wdi project
python -m colligo.models.foundry.smoke_t --only-project wdi

# Only run all foundry-gr6 endpoints (image + video)
python -m colligo.models.foundry.smoke_t --only-endpoint foundry-gr6
```

## Test cases

All test cases are defined as YAML files under each project folder with defaults inheritance.

For example for `nbcu_gabby/`:

| File | Endpoint | Cases |
|------|----------|-------|
| `gen5-image.yaml` | `/v1/images/generate-async` | text-to-image, instruct edit (with reference image) |
| `gen6-image.yaml` | `/v1/foundry-gr6/image` | text-to-image |
| `gen6-video.yaml` | `/v1/foundry-gr6/video` | text-to-video with audio, conditioned video (first frame + audio) |

## Output

A summary table is printed at the end:

```
Endpoint                                 Status                                                Count  Avg Time (s)
/v1/images/generate-async                job placed, response came back as done                     2          12.3
/v1/foundry-gr6/image                    job placed, response came back as done                     1          18.7
/v1/foundry-gr6/video                    job placed, response came back as done                     2          45.1
```

Status categories:
- **failed to place job** -- upload or submit request failed
- **job placed, response never retrieved in timeout** -- polling exceeded 300s
- **job placed, got failed response** -- server returned an error
- **job placed, response came back as done** -- success

However, don't just rely on this, I recommend take a look at the dashboards as well. See links in the [runbook](https://wiki.corp.adobe.com/display/GenAI/Firefly%3A+Gen-Foundry+Runbook).

## Instructions

### What to do before deploying to prod

- Deploy your change to dev first.
- Warmup up all the models.
- Try all requests. Look at the outputs they should look reasonable. And all requests should pass.
  ```sh
  python -m colligo.models.foundry.smoke_t
  ```
- If doing major changes, also check system can handle some more load over time.
  ```sh
  python -m colligo.models.foundry.smoke_t --duration 3600 --num-users 2
  ```
  * All requests should go through.
  * Also look at the logs and make sure all workers did not suddenly use crazy amount of memory / GPU or have queue piling up.


### Adding new test cases

To add a new test case to an existing project (e.g. `nbcu_gabby`):

1. Pick the YAML file for the endpoint you want to test (e.g. `gen6-video.yaml` for `/v1/foundry-gr6/video`), or create a new YAML file if targeting a new endpoint.
2. Add a new entry under `cases:`. It automatically inherits values from the `defaults:` section. Only specify the fields that differ.
3. If the test case needs binary inputs (images, video, audio), place them in the project's `artifacts/` folder and run `./m lfs.sync <path to artifacts>` to track them. Then declare them under `assets:` in the YAML and reference them in the payload with `$asset:<name>` placeholders.
4. If you created a new YAML file, register it in the project's `__init__.py` by adding its filename to the `_YAML_FILES` list.

Example — adding a new video case to `gen6-video.yaml`:

```yaml
cases:
  # ... existing cases ...

  my_new_case:
    description: "Description of what this case tests"
    assets:
      my_image:
        file: artifacts/my-image.jpg
        storage_type: image
    payload:
      prompt: "A prompt describing the desired output"
      first_frame:
        id: "$asset:my_image"
```

### Adding a new project

To add a new workstream alongside `nbcu_gabby` (e.g. a different character or content domain):

1. Create a new directory under `smoke_t/` (e.g. `my_project/`).
2. Add an `artifacts/` subfolder for binary assets and run `./m lfs.sync <path to artifacts>` to set up tracking.
3. Create YAML test case files following the same `defaults:` / `cases:` format used in `nbcu_gabby/`.
4. Create an `__init__.py` with a `get_inputs()` function that loads the YAML files and returns `dict[str, list[TestCase]]` (endpoint -> test cases). You can copy `nbcu_gabby/__init__.py` as a starting point and update `_YAML_FILES`.
5. Wire it into the runner by adding your project to the `get_all_inputs()` function in `__main__.py`:

```python
def get_all_inputs() -> dict[str, list[TestCase]]:
    ...
    # -- add new projects below --
    from colligo.models.foundry.smoke_t.my_project import get_inputs as get_my_project_inputs
    for endpoint, cases in get_my_project_inputs().items():
        by_endpoint[endpoint].extend(cases)
```
