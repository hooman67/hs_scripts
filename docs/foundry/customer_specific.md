## HP debug
https://pluto-prod-dongshenga-dylan-hp-new-9nmp4k-2-0-8000.or2.colligo.dev/debug/

{
  "prompt": "<scene prompt>",
  "size": {"width": 2368, "height": 1776},
  "referenceBlobs": [{"id":"6f45e85f-a5d0-4696-b3ae-dbf1d89f133a"}],
  "n": 1,
  "modelSpecificPayload": {
    "enablePromptRewrite": true,
    "rewriterModel": "gemini-3.1-pro",
    "numInferenceSteps": 50
  }
}

the ref image is the 2D projection of the digital twin. 


## THD video pipeline with seedance 09/18/2026 delivery
endpoint: https://gen-foundry-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/debug/#
full test here: /Users/hshariati/Downloads/temp_work/thd_debug_shot1/ 
{
  "input": {
    "text": {
      "type": "raw",
      "prompt": "SCENE: A living room @Image1. To the right of the coffee table is a couch. The coffee table has 3 books on it and a small white pot with a house plant. Lighting: even and diffuse studio lighting. Two finished bookshelves painted the same color as the walls are on either side of the window. CHARACTERS: Woman: A brunette caucasian woman, about 5'7\", in a light blue denim button up shirt, white jeans, and sneakers. PROPS: Couch: @Image2 Two bookshelves. Single unpainted example: Bookshelf @Image3 PRODUCTS: None SHOT DESCRIPTION AND BEAT TIMING: Camera: wide shot. [0:00 - 0:03] A woman walks into a living-room from left of frame, then sits down in the chair. The camera gently pans to keep her in the center of the frame. [0:03 - 0:08] The woman picks up a book from the coffee-table, which is situated in the middle of the room on the black and white carpet, briefly looks behind her, proud of finishing her bookshelves, then begins to read, smiling. @Image1\n\nREFERENCE IMAGES:\n@Image1: A pastel blue living room with a carpet, potted plant, and framed drawing. No furniture.\n@Image2: A long rectangular couch with dark wood furniture and gray cushions.\n@Image3: The front of an unpainted bookshelf.\n@Image4: Storyboard frame."
    },
    "image": [
      {
        "role": "reference",
        "source": {
          "type": "tempStorage",
          "tempStorageId": "1eed4822-1969-4c00-9297-7e55a10b825d"
        }
      },
      {
        "role": "reference",
        "source": {
          "type": "tempStorage",
          "tempStorageId": "a60f91bb-d9f5-4183-85d4-f5b96687001d"
        }
      },
      {
        "role": "reference",
        "source": {
          "type": "tempStorage",
          "tempStorageId": "1cdaec81-9254-4d97-a64c-08eb0af1c02e"
        }
      },
      {
        "role": "storyboard",
        "source": {
          "type": "tempStorage",
          "tempStorageId": "387461ca-8a24-43fb-978c-c12b7f866fc7"
        }
      }
    ]
  },
  "controls": {
    "resolution": "720p",
    "spatial": {
      "aspectRatio": "auto"
    },
    "temporal": {
      "durationSeconds": "auto"
    }
  },
  "options": {
    "promptRewrite": {
      "mode": "auto",
      "returnResult": true
    }
  }
}


{
  "input": {
    "text": {
      "type": "raw",
      "prompt": "SCENE: Close-up on a @miter-saw base; background is a plain wall, blurred out of focus. CHARACTERS: Woman: a brunette caucasian woman, about 5 ft 7 in, in a light blue denim button-up shirt, white jeans, and sneakers. PROPS: None. PRODUCTS: @miter-saw. SHOT DESCRIPTION AND BEAT TIMING (see @Image1 for the storyboard): Camera static, close-up from a slightly high angle, shallow depth of field with the wood and cut-point in sharp focus and the hand/blade/background blurred; no movement. [0:00-0:03] Hand holds the board steady on the saw deck, aligned under the lowered, non-spinning blade. [0:03-0:07] Blade starts to spin, and the hand slowly brings the miter saw blade down onto the wood, making a smooth cut. [0:07-0:11] The blade continues to spin as she pulls the saw blade up and out of the wood, and finally powers off the saw."
    },
    "image": [
      {
        "role": "reference",
        "source": {
          "type": "tempStorage",
          "tempStorageId": "0b2bf7ca-07b7-49df-ac15-39dfc5020924"
        }
      }
    ]
  },
  "controls": {
    "resolution": "720p",
    "temporal": {
      "durationSeconds": 11
    }
  },
  "options": {
    "promptRewrite": {
      "mode": "auto",
      "returnResult": true
    },
    "debug": {
      "disableIpGuardrails": true,
      "pickMotionVideo": false
    }
  }
}

  {
    "input": {
      "text": { "type": "raw", "prompt": "A cordless jigsaw cuts a curved line through a plywood board on a workbench, sawdust spraying from the blade." },
      "image": [
        { "role": "reference", "source": { "type": "tempStorage", "tempStorageId": "2ebc17b9-7565-4f58-91ab-c253d13c2ddd" } }
      ]
    },
    "controls": { "resolution": "720p" },
    "options": {
      "promptRewrite": { "mode": "auto", "returnResult": true },
      "debug": { "disableIpGuardrails": true, "pickMotionVideo": false }
    }
  }


{
    "input": {
      "text": {
        "type": "raw",
        "prompt": "A man is installing a washing machine at Lowes."
      },
      "image": [
        {
          "role": "reference",
          "source": {
            "type": "tempStorage",
            "tempStorageId": "2f82de80-090d-45e4-9b09-4e659794bb9c"
          }
        }
      ]
    },
    "controls": {
      "resolution": "720p",
      "spatial": {
        "aspectRatio": "16:9"
      }
    },
    "options": {
      "promptRewrite": {
        "mode": "auto",
        "returnResult": true
      },
      "debug": {
        "disableIpGuardrails": true
      }
    }
  }





## password for SFTP transfer of Tesco
Host: asset-transfer-sftp-uat.westeurope.azurecontainer.io
Host: asset-transfer-sftp-prod.westeurope.azurecontainer.io
Port: 22
Username: rebecca
Protocol: SFTP (not FTP or FTPS)
Password: RebeccaSftp2024


## integration testing endpoint for TCCC release 05/08/2026
According to Dongsheng: it is 1094750 ckpt. i''ll go back to this one and make sure we deploy it
** Make sure to use v1/images/tccc-generate-async
{
      "modelVersion": "image5_foundry",
      "prompt": "Replace the women in left with @deja_lighty",
      "modelSpecificPayload": {
          "foundryModelId": "tccc",
          "enablePromptRewrite": true
      },
      "referenceBlobs": [
          {"id":"fd7c4b82-1785-4764-8dc7-0b0a6286454a"}
      ],
      "seeds": [42],
      "n": 1
  }

  input/output from Dongsheng: https://adoberesearch.slack.com/archives/D0AAWNZ8CBV/p1777918321136789
  Downloads/05-06-26-parity-tccc-release-ref1.jpg
  DOwnloads/05-06-26-parity-tccc-release-ref1-out.jpg

Marian Petre  [10:00 PM]
Stage is https://gen-foundry-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/debug/
Enpoint v1/images/tccc-generate-async
You might need to warm up the workers before testing.
Worker list:

lego_vllm_v4_397b_a17b_fp8
gen45_conv_tccc_multiref_worker
internvl_3_8b_v1



## for boards to access pluto local deploy you need this string in colligo.dev.yaml
remote_deploy: {}

# This is the per-app variant - you can add more.
remote_deploy_per_spec:
  foundry:
    local_deploys: [lego_pipeline, gen45_text_encoder_v1_1024, image5_dit_gen45_t2i_foundry_tccc]
    remote_deploys: []
    endpoint: https://gen-foundry-dev.ethos851-stage-or2.ethos.adobe.net/

async_endpoint_url: https://pluto-prod-dongshenga-dylan-hp-2-0-8000.jobs.colligo.dev/
request:
  timeout: 1000000

**What you put here is not the pod name or the unique name. Conect using vscode (from Pluto) and get the vscode url for this.


## slimming checkpoint
-- install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
source "$HOME/.local/bin/env"
```

more steps in wiki:https://wiki.corp.adobe.com/display/FOUNDRY/%5B3%5D+Invisible+Universe+Deployment#id-[3]InvisibleUniverseDeployment-DeploymentPlan


python /home/colligo/colligo/models/colligo/models/common/asml_generation_utils/viq_scripts/consolidate_ckpt.py --ckpt-dir /mnt/localssd/ckpt_step01083000 --slim --output-dir /mnt/localssd/ckpt_slimmed_step01083000/


copy the ckpt over:
mkdir -p /mnt/localssd/ckpt_step1084000

s5cmd cp --concurrency 20 --show-progress s3://foundry-tccc-enterprise-adobe-assets/training_logs/FFP-foundry-58012-tccc_santa_ie_0129-2026.02.07-12.31.26/model-checkpoints/xingtail/ckpt_step01084000/*  /mnt/localssd/ckpt_step1084000
 


## ethos dev endpoint up date init
example PR:
https://git.corp.adobe.com/firefly/colligo-deploy/pull/27691/files

This should be the config for foundry dev on ethos - https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/dev/or2/e851/gen-foundry/values.yaml

@hshariati the worker also needs to be added to the chart like here https://git.corp.adobe.com/firefly/colligo-deploy/pull/27691/files
4:58
in charts/rhode/modules/applications/gen-foundry/deploy_hx00.yaml

## Data synthesis with gpt
export AZURE_OPENAI_TOKEN=BOhhd8hoOZhMDViNI6OcWZFwxU7af188qBHoeF0KjmZXvh4ZJ6l8JQQJ99BIACHYHv6XJ3w3AAABACOGhfeU

python /Users/hshariati/hs_scripts/image_synth_gpt.py \
  --ref-image /Users/hshariati/Desktop/ref_images_trimmer/ref1.png \
  --prompts-file /Users/hshariati/hs_scripts/cordless_battery_string_trimmer_prompts.txt \
  --out-dir /Users/hshariati/Desktop/output_images_trimmer \
  --concurrency 20 \
  --size 1536x1024
  --start 20 (skip first 20 prompts)
--limit 10 (only run next 10 prompts)

python3 /Users/hshariati/hs_scripts/image_synth_gpt_and_gemini.py \
  --model gpt \
  --ref-image /path/to/ref.png \
  --prompts-file /path/to/prompts.txt \
  --out-dir /path/to/out \
  --size 1536x1024


# data synthesis with gemeni

export GOOGLE_APPLICATION_CREDENTIALS=/Users/hshariati/Documents/gemeni_cred.json


{
  "type": "service_account",
  "project_id": "adbe-gcp0805",
  "private_key_id": "290eb7f01b89326629a06ac9d5bc5a621353becb",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC8p4xVZ4njEQ7o\nMN4SgroDujzKZqaGZl0vIhw4H6P+m6So9OFlUXKEbVGVf9g2UQBj+k2FzE09B0GM\nUA+lD+fo3CjUQmz68WOlIMCc7lrK0bBt7GOAo1GlPtxMznDA5VTkgDrzj1ZOy1Ml\n6lRfZ2jpywELqaX02MVtVEQh1z+gSfSWpGcoziJ4CTO9JBwF/RKwwfV87pcII3LQ\neAgDP9NFE1c1RqYgO6IXov5H7yOT95BYdXt7Y5Ww5CN7imow4D6f1TL7pLAGxk9O\ngqNL1Vl6Upb0D6bGQsWVHy6YgwT/ktJIpMTcPAWhFpSaPphV7VkCdZcXYyBDeNr5\nxzdhDMinAgMBAAECggEAW6hHzUK1woWKKZN8gZ/UAnWcjXXcGFZplbnL3hS5V72E\n/bWkQNaWffKi/bCUeqdWOjzlJ0mAiVMaLLLFNxwIP6GfkKkJS8617AeCrXw8zmec\ngXulSF2REGj/Ha37KC0D1tTaT3VnqHau2jAEeCnE1joUMvdksxYSrbCQPaTXu+b9\nDAPeNgP9gs9D4cuSZbL+EBu5o6FHaRD0rGvJhwkMgpBYq0zVpQhpQ5pKo2QFyfwd\nBMXl/OyeM23wjl3Ae0D8rI1zLWR+qiSAnZdZBB91LOfMscZ18XsFk3QZyU+bhHou\nw+Et9nTeJjvKVPZYA7DNtQOsdLAxusYDRK7dSMpjgQKBgQDb3O+M7tZy/Eb7jobY\n4AlSWj6txDlaJQQK5WiHlSWTySDY3PLwuHS2bxsah9UCdU43c0pi3kb6NinJSdri\nzs8XRDgr9fCey81x43CsxfScLVtnXS7Yse+o1CgA7QqbPbvUtbS33dkVu/aGx62W\nhPGMF2Lt/lINsD/+ZLCC4aT15wKBgQDbqXdoyq9al1qDv8OOFiBb3rQFNlMkYO/X\n++iYxsdNsaGR0AWNfwMUwihfhRmANUt06lKXHZ4Ou0/MizdPB/GGcSbDD9YbpR9K\nLpHhuEbJwng45R8mJkMWl2Kx198wbHMuP1CMKA0Eb6+otMHFAosV0WPmgx3N8kOw\n7YsLG1W/QQKBgAVNziWbOWcquNemt5ARz4fCD5MHkc6f5/oPULc8nNx01KsGoYG3\nIXGpOoEoV7YoeEuUJ249KH8uwVFOy83+6TYJekVtOHHMPteJghVY7S67VWIn+FJX\n8I0lGRX0ofXexmI6Q/LPkkYY87iKpqBj8qPLiKJvKTGVV+XeLffqU51vAoGBAIQz\nuzUrf1wDaauPd0+Fi5YfM7NLXcCwQsl3yCZixELDXJ1YWG8veRg+PnQ2tAFQkghc\nmrZuUdlF7KILS49aFYe3g/+0AUWEHI/V9WCnOptlWlvLsfKQ5qGrHPAyHxaSvsOf\nwYeI90SrP0pG97Ptcu3/pqNuWDrByvGqFZvqqLHBAoGBAJjFD5ORvYSxxIFZDLaI\nmRdNfsxLe83SPhYRi/NtrARkETGmZ5jCIQMFMa4YB+ppFGHAQ6aWjmWWLEd788Xt\nx81hWfM0yLbJRlz2ka+Ak2bsfQqUoL0pf0ulX+2IZVcUurlF7GZX9neUx44IlwJw\nWgme7rRjl2Zr5qp8VcUzs5XZ\n-----END PRIVATE KEY-----\n",
  "client_email": "foundry-services-sa@adbe-gcp0805.iam.gserviceaccount.com",
  "client_id": "118418701606309435864",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/foundry-services-sa%40adbe-gcp0805.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

python3 /Users/hshariati/hs_scripts/image_synth_gpt_and_gemini.py \
  --model gemini \
  --ref-image /path/to/ref.png \
  --prompts-file /path/to/prompts.txt \
  --out-dir /path/to/out \
  --size 1920x1088

## THD request
### after 05/27/2026
endpoint: https://pluto-prod-mingdongw-thd-img-l2a-d-lkp5gz-0-8000.jobs.colligo.dev/debug/

{
    "prompt": "Replace the leafblower with @<314742167>",
    "referenceBlobs": [
        {"id":"b92bf743-09b2-4c3d-84fe-4cd6b2cb4325"}
    ],
    "aspectRatio": "16:9",
    "n": 1,
    "seeds": [1816417070],
    "enablePromptRewrite": true
}

Make sure to set:
Additional headers: 
{"x-foundry-model-id": "thd-l2a"}

### before:

https://gen-foundry-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/debug/
To send a request:
paste this in "x-colligo-debug-input": {"nsfw_disable": true} to disable nsfw checks.
make sure to select:
lego pipelines - v1/images/generate-async
```bash
{
    "n": 1,
    "seeds": [
        1
    ],
    "size": {
        "width": 1920,
        "height": 1088
    },
    "output": {
        "cai": {
            "directive": "sign_for_policy_mandate"
        },
        "storeInputs": false
    },
    "modelId": "firefly_image",
    "modelVersion": "image5_foundry",
    "prompt": "a close-up of a woman's hands holding a green power drill as she drills a screw into a white wooden shelf. studio lighting, neutral color temperature, long focal length.",
    "modelSpecificPayload": {
        "foundry_model_id": "thd"
    }
}
```

## THD local deploy
teps to spin up a local server for inference:
setup colligo following https://docs.ai.corp.adobe.com/aidoc/monorepo/env-setup.html
THD code is on main so pulling latest main should be fine
Add the following block under remote_deploy_per_spec section of colligo.dev.yaml file in root of the repo.
You'll need 4 H100s to run this config.
docker image docker-matrix-experiments-snapshot.ff.adobe.io/colligo/colligo-dev:v63
```bash
  foundry:
    local_deploys: [lego_pipeline, image5_dit_gen45_t2i_foundry_thd, gen45_text_encoder_v1_512_foundry, vae_f16_lego]
    remote_deploys: []
    endpoint: https://gen-foundry-dev.ethos851-stage-or2.ethos.adobe.net/
```
Start the server on vscode/cursor by clicking Run and Debug->Inference: Rhode Debug Deploy->foundry. Wait for server to come up, then go to localhost:8000 to access the debug UI. 


## Steps to slim ckpt
Steps to slim ckpt - https://adobesearch.slack.com/archives/C094TVAPUJ2/p1757133159719139?thread_ts=1757130813.759279&cid=C094TVAPUJ2 (edited) 

Abhinav Sharma
Here's the script - https://github.com/Adobe-Firefly/colligo/blob/main/models/colligo/models/common/asml_generation_utils/viq_scripts/consolidate_ckpt.py
Sample command
python models/colligo/models/common/asml_generation_utils/viq_scripts/consolidate_ckpt.py --ckpt-dir=<s3-path> --output-dir=<local-output-dir> --slim
From a private conversation | Sep 5th, 2025
4:17
https://adobesearch.slack.com/archives/C094TVAPUJ2/p1757133294437419?thread_ts=1757130813.759279&cid=C094TVAPUJ2

Abhinav Sharma
This will download and give the slimmed ckpt, this key should be model.denoiser for non-ema and ema for ema weights. Also I run it from the mori venv and the model branch, otherwise it can give dependency errors when loading the ckpt.
From a private conversation | Sep 5th, 2025
4:18
training branch - thd_b200
steps to setup inference - https://adoberesearch.slack.com/archives/C09LANGU4MP/p1765389858151449?thread_ts=1765330643.375269&cid=C09LANGU4MP

Abhinav Sharma
Steps to spin up a local server for inference:
setup colligo following https://docs.ai.corp.adobe.com/aidoc/monorepo/env-setup.html
THD code is on main so pulling latest main should be fine
Add the following block under remote_deploy_per_spec section of colligo.dev.yaml file in root of the repo.
You'll need 4 H100s to run this config.


# TCCC Instruct edit IE request
{
    "n": 1,
    "seeds": [
        1
    ],
    "output": {
        "cai": {
            "directive": "sign_for_policy_mandate"
        },
        "storeInputs": false
    },
    "referenceBlobs": [
        {"id":"460e846e-31ed-4379-af0d-98fcf3464539"}
    ],
    "modelId": "firefly_image",
    "modelVersion": "image5_foundry",
    "prompt": "<instruction> Replace all existing food (including the tacos being held and the plated dishes) with Golgappa / Pani Puri. Show crisp hollow puris with spiced pani and fillings, naturally held in the people’s hands and placed on the table where the original food was. Keep all people, poses, hand positions, facial expressions, camera angle, lighting, environment, and all Coca-Cola bottles unchanged. Ensure realistic scale, perspective, and lighting so the new food blends seamlessly into the scene. # tccc",
    "modelSpecificPayload": {
        "foundry_model_id": "tccc"
    }
}

### TCCC Local deploy
remote_deploy_per_spec:
  foundry:
    local_deploys: [lego_pipeline, image5_dit_gen45_t2i_foundry_tccc]
    remote_deploys: []
    endpoint: https://gen-foundry-dev.ethos851-stage-or2.ethos.adobe.net/
request:
  # Timeout for the requests. Default is 60, but for development, increase it to a much larger values, so hitting breakpoints
  # in the debugger does not cause timeout.
  timeout: 1000000


## Running the Stock search script
### installation
```bash
uv pip install --prerelease=allow --index-strategy unsafe-best-match \
  --extra-index-url https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-kineto-release/simple \
  --extra-index-url https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-piat-release/simple \
  -e ."[glimmer]"
```


## Deployment for prod
wiki: https://wiki.corp.adobe.com/display/GenAI/Firefly%3A+Gen-Foundry+Runbook#Firefly:GenFoundryRunbook-Updatingdeployments

1. You need a deployment from main into dev.
https://git.corp.adobe.com/firefly/colligo-deploy/pull/30950/files
2. You need to add a test for your deployment
Guide: https://github.com/Adobe-Firefly/colligo/tree/7d9cd614e7350b80b7c3a3725b67f68d6ff6bcb0/models/colligo/models/foundry/smoke_t
my PR: https://github.com/Adobe-Firefly/colligo/pull/21192
you can run just your test (on a Pluto machine like this): 
```bash
python -m colligo.models.foundry.smoke_t --host https://gen-foundry-dev.ethos851-stage-or2.ethos.adobe.net --only-project coke
```
check the log file for errors. And for the location the outputs are saved at.
But you need to run everything (remove the --only-project) to make sure you're not breaking other projects.

3. Edit this file:  https://git.corp.adobe.com/firefly/colligo-deploy/edit/main/k8s/helm/prod/or2/e855/release/gen-foundry/values.yaml
3.1 add your init script here
```bash
# =============== [The app itself] ======================
rhode:
  applications:
    gen-foundry:
      _extends: applications/common/colligo_workergroups
      init_script: s3://colligo-dev-main/deploy_v2/colligo-rhode/foundry/foundry-version=0.1-main.109215-commit=b8de4f2e-platform=1.9.0.sh
      vars:
        - gen-foundry
      default_rollout: "canary-analysis"
```
3.2 Then you need to allow list the model_id and also the specific users. Like this:
```bash
authz_anchor: &authz_anchor
    foundry_model_authorization_config:
      authorizations:
        nbcu-gabbys-dollhouse:
          allowlisted_user_ids:
            - 3cc022cf690a71aa0a495e7e@techacct.adobe.com # Michael Gossen dev
            - 52a521d86949d70d0a495fc2@techacct.adobe.com # NBCU tech acc
          allowlisted_org_ids:
            # internal adobe inc
            - "821b1f78631c0ced495c57.e"
            - "adobe.com"
          allowlisted_emails:
            - 5b596d86-0627-4a10-a891-b0cb4d71c224@techacct.adobe.com # NBCU tech acc email
            - 2b8aa851-8945-4a3e-832c-8b57b520118d@techacct.adobe.com # Michael Gossen dev
            - caroline.horn@nbcuni.com
            - cod00214@adobe.com # vendor worker
```

You can find the model id in: models/colligo/models/firefly/pipelines/lego_v1/FoundryWorkflow.py 
```bash
FOUNDRY_MODEL_MAPPING = {
    "nbcu-gabbys-dollhouse": {
        "t2i": Image5DiTWorker.IMAGE5_DIT_GEN45_T2I_FOUNDRY_NBCU_GABBYS_DOLLHOUSE,
        "ie": Image5DiTWorker.IMAGE5_DIT_GEN45_IE_FOUNDRY_NBCU_GABBYS_DOLLHOUSE,
    },
    "invisible-universe-squeaky": {
        "t2i": Image5DiTWorker.IMAGE5_DIT_GEN45_T2I_FOUNDRY_INVISIBLE_UNIVERSE_SQUEAKY,
        "ie": Image5DiTWorker.IMAGE5_DIT_GEN45_IE_FOUNDRY_INVISIBLE_UNIVERSE_SQUEAKY,
    },
    "wdi": {
        "t2i": Image5DiTWorker.IMAGES_DIT_GEN45_IMAGING_FOUNDRY_WDI,
        "ie": Image5DiTWorker.IMAGES_DIT_GEN45_IMAGING_FOUNDRY_WDI,
    },
    "thd": {
        "t2i": Image5DiTWorker.IMAGE5_DIT_GEN45_T2I_FOUNDRY_THD,
    },
    "tccc": {
        "t2i": Image5DiTWorker.IMAGE5_DIT_GEN45_T2I_FOUNDRY_TCCC,
        "ie": Image5DiTWorker.IMAGE5_DIT_GEN45_T2I_FOUNDRY_TCCC,
    },
}
```

You also need to add the surface they use to connect (board, ff.com, etc). This is not deployment specific.
```bash
      ingress:
        user_profile_enabled: true
        dev_ingress: true
        allowed_client_ids:
          - colligo_testing
          - clio-playground-web
          - firefly-service-testing
          - foundry-web
```
3.3 then add your worker. 
if you want 1 GPU you add under gpu_hx00_x1 if you want 2 gpus add under gpu_hx00_x2.
Note that 1 replica under gpu_hx00_x2 means you get 2 GPUs. 

my PR: https://git.corp.adobe.com/firefly/colligo-deploy/pull/30955

4. Create a ticket for SRE and put in the SRE support channel. 
https://wiki.corp.adobe.com/display/GenAI/Firefly+Intake+Process
https://jira.corp.adobe.com/secure/CreateIssueDetails!init.jspa?pid=97100&issuetype=10201&labels=FireflyAPIAccess
my ticket: https://jira.corp.adobe.com/browse/FFP-74798
message to SREs: https://adoberesearch.slack.com/archives/C05B6F46E4C/p1771372998028769
5. Update the run book and change log. 




## endpoint for hosting reference images Used by UXP plugin for TCCC
 Endpoint                                                                                                                                                                          
  GET https://naugo8ump4.execute-api.us-west-2.amazonaws.com/prod/v1/images/<filename>
  Header: x-api-key: VpFScrd2ykcbnLNEfXOK3eYbJAYchfo32MOFCGq9                                                                                                                       
                                                                                                                                                                                    
  Curl smoke test for them
  curl -L -H "x-api-key: VpFScrd2ykcbnLNEfXOK3eYbJAYchfo32MOFCGq9" \                                                                                                                
    -o ref_out.jpg \                         
    https://naugo8ump4.execute-api.us-west-2.amazonaws.com/prod/v1/images/Deja_Lighty.jpg                                                                        
                                                                                                                                                                                    
  The -L (or any HTTP client following 302s) is required — the API responds with a 302 to a 5-minute presigned S3 URL, so the bytes come from S3, not the API. No second API call   
  needed; their HTTP library handles the redirect.                                                                                                                                  
                                                                                                                                                                                    
  Available filenames are exactly what you had in ~/Downloads/{product,talent}_reference_uxp_tccc_04-28-26/ (8 product .jpg + 12 talent .jpg, all in                                
  s3://foundry-dropbox-tccc-enterprise/uxp_plugin_ref_image_rep/).

   Key admin reference                                    

  - Key ID (for revoke/rotate, safe to log/share internally): 4mskde5pyi                                                                                                            
  - Disable instantly: aws apigateway update-api-key --api-key 4mskde5pyi --patch-operations op=replace,path=/enabled,value=false
  - Quotas in effect: 5 req/s sustained, 10 burst, 1000 req/day                                                                                                                     
  - Audit: CloudWatch log group /aws/lambda/foundry-tccc-image-api                                                                                                                  
                                                                                                                                                                                    
  What's checked in                                                                                                                                                                 
                                                                                                                                                                                    
  - Branch: hshariati/feat/tccc-image-api pushed to origin                                                                                                                          
  - Open PR at: https://github.com/Adobe-Firefly/foundry/pull/new/hshariati/feat/tccc-image-api  (gh CLI isn't authenticated locally, so I couldn't open it for you)
  - Files: modeling/terraform/adhoc/2026-04-tccc-image-api/{providers.tf,main.tf,lambda/image_handler.py,.gitignore,.terraform.lock.hcl}            



## endpoint for hosting reference images Used by UXP plugin for THD
  curl -L -H "x-api-key: T5AcrGT2zA605cREmLcEK4j2sSYyvJgy4pGSfs2G" \
    -o 100678374.jpg \
    https://vwbqd4vw76.execute-api.us-west-2.amazonaws.com/prod/v1/images/100678374.jpg


  Two CSV endpoints (live now):
  KEY=T5AcrGT2zA605cREmLcEK4j2sSYyvJgy4pGSfs2G

  # full catalog (29.5 MB, byte-identical to source)
  curl -sL -H "x-api-key: $KEY" -o full.csv \
    https://vwbqd4vw76.execute-api.us-west-2.amazonaws.com/prod/v1/images/thd_product_catalog.csv

  # minimal catalog (3.2 MB, omsid + hd_title)
  curl -sL -H "x-api-key: $KEY" -o minimal.csv \
    https://vwbqd4vw76.execute-api.us-west-2.amazonaws.com/prod/v1/images/thd_product_catalog_minimal.csv

  Both verified: 200, correct byte count, content-type: text/csv.

  Filenames are intentionally stable across revisions — when you give me v3 later, the helper script just overwrites in place and the vendor URLs don't change.


# Humain eval
technical-quality-matrix-internal-foundry
Saudi Arabian Cultural Alignment Study
foundry_adobe_stock_missions_
https://adoberesearch.slack.com/archives/D0ADFN8MKU6/p1778774102897899


Hello! This is a test internal Humain study for cultural accuracy:
Link https://clio-evaluation-platform-deploy-ethos501-prod-or2-20a96f.cloud.adobe.io/study/69fb812e6164e810f2360636?T[…]6f48adf36d9c201e54a30639cf5420ac6
Study 69fb812e6164e810f2360636
Template 69fb812e6164e810f2360636Arpit Mathur  [11:05 AM]
was added to the conversation by .Kate Sousa  [11:35 AM]
Here is the cultural relevance task: https://view.appen.io/channels/cf_internal/jobs/3582488/editor_preview?token=ChS4e7ZLwS1ZUIi77uHjXQ


Appen credentials:
username: hshariati@adobe.com
pass: MypencilcaseisPink1#


### Shared with Humain around 05/19/2026

#### 650 set
  Run ID: h06_v13_iter_1026000_expanded_prompts_humain_t2i_gpt_592_1779300549
  View: https://evaluation-hub.adobe.io/asset-viewer?run_ids=h06_v13_iter_1026000_expanded_prompts_humain_t2i_gpt_592_1779300549

  Same identity as before (humain_t2i_gpt_592 v1.0, h06_v13_iter_1026000_expanded_prompts, hshariati, 2 variations, 1184 assets).
  Prompt body now reads:

Cultural relevance study link: https://clio-evaluation-platform-deploy-ethos501-prod-or2-20a96f.cloud.adobe.io/study/6a1f6680111bdcb31bd291ee?TOKEN=85c61b9b348694de9b4b66d09468b2991dcf24cd4d8618fb66dfa67723e9e658

Technical Quality Study Link: https://clio-evaluation-platform-deploy-ethos501-prod-or2-20a96f.cloud.adobe.io/study/6a1f65ef021034f61675efd3?TOKEN=0d3e7fe2bcb3cdc3f0ec3e587bbd2584d61c591235ebdcc522d19ed2577b822c

#### 211 set
  Run ID: h06_v13_iter_1026000_expanded_prompts_humain_t2i_gpt_211_1780018310
  View: https://evaluation-hub.adobe.io/asset-viewer?run_ids=h06_v13_iter_1026000_expanded_prompts_humain_t2i_gpt_211_1780018310

Cultrual relevance study link: https://clio-evaluation-platform-deploy-ethos501-prod-or2-20a96f.cloud.adobe.io/study/6a1f67ccfdb03c0076986755?TOKEN=f301a5d9ff8a57011bd98b6ec58e0299bab00edd73b926cf0d44a0b899c736dd

Technical Quality Study Link: https://clio-evaluation-platform-deploy-ethos501-prod-or2-20a96f.cloud.adobe.io/study/6a1f67baf55630b2f64c5ec9?TOKEN=4f227146e8a2a04fabdb3834a50aac2123f2c53e9603bff90ada557ea97365d8




  - Gallery: https://foundry-aws-corp.adobe.io/asset/foundry-humain-default-adobe-assets/hs_results/2026-05-22_humain_prompts/gallery/index.html
  - S3: s3://foundry-humain-default-adobe-assets/hs_results/2026-05-22_humain_prompts/
  - Remaining 7 failures: 6 prompt_unsafe (safety filter — permanent), 1 http_503 on id 196 seed 333.

  - Eval set: humain_t2i_gpt_211 v1.0
  - Model id: h06_v13_iter_1026000_expanded_prompts (same as before)
  - Created by: hshariati, 2 variations
  - 415 assets uploaded (422 generations − 7 failures: 6 prompt_unsafe + 1 http_503), spanning all 211 prompt_ids
  - 415 assets uploaded (422 generations − 7 failures: 6 prompt_unsafe + 1 http_503), spanning all 211 prompt_ids
  - Per-asset layout: model_input.prompt = original prompt, metadata.prompt = that seed's rewritten/expanded prompt — set per variant, since the endpoint rewrites
  per-generation (205 of 211 prompts had different rewrites across the two seeds)

  How I read the data: the results.csv in your S3 root had everything mapped explicitly — prompt_id, original_prompt, rewritten_prompt, image_filename, status. No
  guessing needed. Failed rows have empty image_filename and were skipped automatically.

  Skill changes (~/.claude/scripts/eval_hub_upload.py + .md):
  - Added Mode D (--results-csv + --images-s3) that consumes the /generate-from-endpoint results.csv format directly — this is the reusable path for future endpoint runs.
  - Refactored all four modes onto a unified internal AssetSpec manifest, so per-asset prompts/expanded handling is consistent everywhere.
  - s3_client now falls back to ambient AWS env creds (so /aws-creds → source aws_creds.env + --creds /dev/null works cleanly).
  - Updated the memory reference so future sessions know about Mode D and the /aws-creds flow.



## Humain stage (dev) endpoint
https://gen-foundry-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/debug/#
v1/images/generate-async

{
    "seed": 333,
    "referenceBlobs": [],
    "modelVersion": "image5_foundry",
    "prompt": "Portrait of two people exploring a Saudi mud-brick heritage village in AlUla, gazing upward in wonder at warm terracotta walls, soft afternoon sunlight, foreground yellow dates and woven textiles leading into the architectural depth behind​. No jewelry",
    "model_specific_payload": {
        "foundry_model_id": "humain"
    },
    "size": {
        "height": 2048,
        "width": 2048
    }
}



