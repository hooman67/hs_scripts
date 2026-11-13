# CM5 IE Eval Hub

Two-step workflow: upload assets to temp storage for 12h, then run the inferences.

## 1. Store eval hub assets

Downloads images via s5cmd and uploads them to temp storage for 12h. Run once before starting the inferences.
In the future we aim to give a list of eval sets to automatically scan for assets instead of hardcoding them in the JSON files.

**IE:**
```bash
python -m colligo.models.firefly.clio_tyom.scripts.cm5.ie.eval_hub_helpers store \
  --type ie \
  --path models/colligo/models/firefly/clio_tyom/scripts/cm5/ie/data/eval_hub_assets_ie.json \
  --output models/colligo/models/firefly/clio_tyom/scripts/cm5/ie/data/eval_hub_assets_temp_storage.json
```

**Composition Reference:**
```bash
python -m colligo.models.firefly.clio_tyom.scripts.cm5.ie.eval_hub_helpers store \
  --type comp_ref \
  --path models/colligo/models/firefly/clio_tyom/scripts/cm5/ie/data/eval_hub_assets_comp_ref.json \
  --output models/colligo/models/firefly/clio_tyom/scripts/cm5/ie/data/eval_hub_assets_comp_ref_temp_storage.json
```

Input manifests: `eval_hub_assets_ie.json` / `eval_hub_assets_comp_ref.json`  
Output: JSON file mapping asset paths to their temp storage blob ids.

## 2. Run the inferences

Submits inference jobs to the CM5 endpoint.
You need to export the `EVAL_HUB_ASSETS_PATH` environment variable with the path to the mapping for the assets.
You can add it in the top-level `.env` file of the Colligo monorepo, e.g.:
```bash
EVAL_HUB_ASSETS_PATH=models/colligo/models/firefly/clio_tyom/scripts/cm5/ie/data/eval_hub_assets_comp_ref_temp_storage.json
```

```bash
python -m colligo.models.compare.v2.images.cm \
  --host https://cm-imaging-v5-dev.ethos851-stage-or2.ethos.adobe.net \
  --pipeline v1/images/generate-async \
  --json-config-file-path cm5_ie/batch_0.json \
  --ldap <your-ldap> \
  --override-ims-token \
  --max-jobs 1 \
  --limit-prompts 1
```

* `batch_0.json` example for `IE`:
```jsonc
[
    {
        "eval_set_name": "cm5_ie_eval_style_icons_2d_vector:stock_color_circle",
        "eval_set_version": "1.0",
        "use_rewritten_instruction": "true",
        "model_id": "cm5_service_ie_ffp_90058",
        "request": {
            "model_id": "firefly_image",
            "model_version": "image5_custom",
            "custom_model_id": "urn:aaid:sc:VA6C2:fd49cccb-ca45-38ae-8eb3-c7c3202d056b"
        }
    }
]
```

* `batch_0.json` example for `Composition Reference`:
```jsonc
[
    {
        "eval_set_name": "cm5_ie_composition_eval_subject_illus_2d_char:stock_smart_apple",
        "eval_set_version": "1.0",
        "use_rewritten_instruction": "true",
        "model_id": "cm5_service_comp_ref_ffp_90058",
        "request": {
            "model_id": "firefly_image",
            "model_version": "image5_custom",
            "custom_model_id": "urn:aaid:sc:VA6C2:c082f1c5-5581-3114-95d3-3576c510d46f"
        }
    }
]

```


## VS Code launch configs

Add these to `.vscode/launch.json` under `configurations` to debug from the IDE:

```jsonc
{
    "name": "CM5 IE: Store Eval Hub Assets",
    "type": "debugpy",
    "request": "launch",
    "module": "colligo.models.firefly.clio_tyom.scripts.cm5.ie.eval_hub_helpers",
    "console": "integratedTerminal",
    "justMyCode": true,
    "args": [
        "store",
        "--type", "ie",
        "--path", "${workspaceFolder}/models/colligo/models/firefly/clio_tyom/scripts/cm5/ie/data/eval_hub_assets_ie.json",
        "--output", "${workspaceFolder}/models/colligo/models/firefly/clio_tyom/scripts/cm5/ie/data/eval_hub_assets_temp_storage.json",
    ],
    "envFile": "${workspaceFolder}/.env",
},
{
    "name": "CM5 Comp Ref: Store Eval Hub Assets",
    "type": "debugpy",
    "request": "launch",
    "module": "colligo.models.firefly.clio_tyom.scripts.cm5.ie.eval_hub_helpers",
    "console": "integratedTerminal",
    "justMyCode": true,
    "args": [
        "store",
        "--type", "comp_ref",
        "--path", "${workspaceFolder}/models/colligo/models/firefly/clio_tyom/scripts/cm5/ie/data/eval_hub_assets_comp_ref.json",
        "--output", "${workspaceFolder}/models/colligo/models/firefly/clio_tyom/scripts/cm5/ie/data/eval_hub_assets_comp_ref_temp_storage.json",
    ],
    "envFile": "${workspaceFolder}/.env",
},
{
    "name": "CM5 IE: Run Eval Hub",
    "type": "debugpy",
    "request": "launch",
    "module": "colligo.models.compare.v2.images.cm",
    "console": "integratedTerminal",
    "justMyCode": true,
    "args": [
        "--host",
        "https://cm-imaging-v5-dev.ethos851-stage-or2.ethos.adobe.net",
        "--pipeline",
        "v1/images/generate-async",
        "--json-config-file-path",
        "${workspaceFolder}/cm5_ie/batch_0.json",
        "--ldap",
        "gbranescu",
        "--override-ims-token",
        "--max-jobs",
        "1",
        "--limit-prompts",
        "1",
    ],
    "envFile": "${workspaceFolder}/.env",
},
```
