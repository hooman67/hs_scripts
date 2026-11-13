```markdown
## Optimizing new glimmer on image caption module:
    These remained unchanged.
        max_tokens: 700
        temperature: 0.1
        top_p: 0.9
        top_k: 1
        seed: 17
python -m glimmer_queue.sqs_run \
  --queue-url https://sqs.us-west-2.amazonaws.com/760168217311/hs_exploration_queue4 \
  --region us-west-2 \
  --wait-time 10 \
  --visibility-timeout 300 \
  --batch-size 1 \
  --config /sensei-fs/users/hshariati/hs_scripts/glimmer/hs_vllm_test_new_glimmer.yaml \
  --gpus 0 --num-cpu-processes 32
    
  ## new glimmer
    ### new_1 (corresponding screenshots in Desktop)
        num_workers: 0 #2
        batch_size: 64 #same as batch size of 1 when we have row_groups (no row_grop has nothing to do with it)
        num_threads: 2 #8
        batch_concurrency: 80
        concurrency: 32 # 2-4 x CPU cores
        num-cpu-processes 32

    ### new_2 (corresponding screenshots in Desktop)
        num_workers: 0 #2
        batch_size: 1
        num_threads: 2 #8
        batch_concurrency: 80
        concurrency: 32 # removed
        num-cpu-processes 32


  ## old glimmer 
    ### old_1 (find corresponding screenshots in Desktop)
        num_workers: 2
        batch_size: 1
        num_threads: 2 #8
        # batch_concurrency: 80
        concurrency: 32 # 2-4 x CPU cores
        num-cpu-processes 32



## Docker Image and Evaluation Path

`docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v1.0`

`/sensei-fs/users/hshariati/worktree_AdobeDiffusion/clio3-cso-feb29-eval/`

## Runai Commands

```bash
runai submit -i [docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v1.0](https://www.google.com/search?q=https://docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v1.0) -p asml-eval-p4d --run-as-user --backoff-limit 0 -l asml_project_name=asml-eval --node-pool a100-3 a100-2 a100-1 --name ad4cee1f81cc6de68966d7585804df8c721d1ac5d6d --gpu 1 --command -- /bin/bash -c "export ARTIFACTORY_UW2_USER=cliobot && export PDM_BUILD_SCM_VERSION=0.1.0 && \ export ARTIFACTORY_UW2_API_TOKEN=AKCp8nGu2aaQsbfn6HNUww9JR9KKNJkX7zZCN3MP8tu5S7i6PHGSzytUMSgsxvu9c5vbRMjuT && \ sudo chmod 777 ~ && cd /sensei-fs/users/simranjyotsg/auto-eval/eval-repos/37f13375-e7dd-4b95-9a3d-65d963edfe80 && chmod 777 ./activate_dev_basemodels.sh && ./activate_dev_basemodels.sh && pip install clip@git+[https://github.com/openai/CLIP.git@a1d071733d7111c9c014f024669f959182114e33](https://github.com/openai/CLIP.git@a1d071733d7111c9c014f024669f959182114e33) && pip install pandas && python3 scripts/clio3/run_inference_clio3_mc.py \ --config /sensei-fs/tenants/Sensei-AdobeResearchTeam/clio/tmp_configs_for_eval/G_slimmed_version_0=4000_20240312002618.yaml \ --prompt \"/sensei-fs/users/fchen/controlnet/test_clio-mm_v2.txt\" \ --application \"text2image_mc\" \ --limit_prompts 10 \ --control \"\" \ --aesthetic_class 6 \ --return_file_path /sensei-fs/tenants/Sensei-AdobeResearchTeam/clio/clio_eval_v1/ad4cee1f81cc6de68966d7585804df8c721d1ac5d6d/output_ad4cee1f81cc6de68966d7585804df8c721d1ac5d6d.txt"
```

```bash
runai submit --interactive --name mc-autoeval-test -p clio-model-efficiency -g 8 -i [docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v1.0](https://www.google.com/search?q=https://docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v1.0) -l asml_project_name=clio-model-efficiency --node-pool a100-80gb-1 --service-type=external-url --port 8888 -e pname=clio-model-efficiency -e jname=mc-autoeval-test
--large-shm --command -- /bin/bash -c /runai_entrypoint.sh
```

## Hs\_task 5

```python
print(config)
+
+    for ckpt in config.model_configs.diffusion_unet.torch_checkpoint:
+        ckpt.sensei = (
+            expand_dmd_ckpt(ckpt.sensei)
+        )
+
     app = Inference(config)
     return app

@@ -272,6 +275,18 @@ def get_controls(
     return entity_result, depth_result, edge_result


+def expand_dmd_ckpt(filename):
+    unet = torch.load(filename, map_location="cpu")
+    keys = list(unet.keys())
+    for key in keys:
+
+        if key.startswith("G.eps_model.D"):
+            unet[key.replace("G.eps_model.D", "eps_model")] = unet.pop(key)
+    unet.pop("g_optimizer")
+    output_path = filename.replace(".ckpt", "_expanded.ckpt")
+    torch.save(unet, output_path)
+    return output_path
```

Teacher model: prod3\_18
[http://clio.corp.adobe.com/model\_evaluation/image\_comparison\_output/Y-03-13-11-50-23-4cede7b2c2/Y-03-13-11-50-23-4cede7b2c2.html](http://clio.corp.adobe.com/model_evaluation/image_comparison_output/Y-03-13-11-50-23-4cede7b2c2/Y-03-13-11-50-23-4cede7b2c2.html)

Student checkpt: `/sensei-fs/users/hshariati/dmd-ck/global_step_22000_G_slimmed.ckpt`
[http://clio.corp.adobe.com/model\_evaluation/image\_comparison\_output/Y-03-13-12-26-04-d763832f4c/Y-03-13-12-26-04-d763832f4c.html](http://clio.corp.adobe.com/model_evaluation/image_comparison_output/Y-03-13-12-26-04-d763832f4c/Y-03-13-12-26-04-d763832f4c.html)

After adding anchor prompting:
`/sensei-fs/users/alse/dmd/dmd/implementations/models/dmd_prod3_18_inference_config_attn_composition.yaml`

`depth_model_config`

Successfully installed lightning-2.1.0
```python
(hs_AD_3.10.13) hshariati@training-effic-test2-dit-0-0:/sensei-fs/users/hshariati/lightning-ColossalAI$ python
Python 3.10.13 (main, Sep 11 2023, 13:44:35) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import lightning as L
>>> trainer = L.Trainer(strategy="lightning-colossalai", precision="16-mixed", devices=8)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/opt/conda/envs/hs_AD_3.10.13/lib/python3.10/site-packages/lightning/pytorch/utilities/argparse.py", line 70, in insert_env_defaults
    return fn(self, **kwargs)
  File "/opt/conda/envs/hs_AD_3.10.13/lib/python3.10/site-packages/lightning/pytorch/trainer/trainer.py", line 402, in __init__
    self._accelerator_connector = _AcceleratorConnector(
  File "/opt/conda/envs/hs_AD_3.10.13/lib/python3.10/site-packages/lightning/pytorch/trainer/connectors/accelerator_connector.py", line 124, in __init__
    _register_external_accelerators_and_strategies()
  File "/opt/conda/envs/hs_AD_3.10.13/lib/python3.10/site-packages/lightning/pytorch/trainer/connectors/accelerator_connector.py", line 688, in _register_external_accelerators_and_strategies
    from lightning_colossalai import ColossalAIStrategy
  File "/sensei-fs/users/hshariati/lightning-ColossalAI/src/lightning_colossalai/__init__.py", line 5, in <module>
    from lightning_colossalai.strategy import ColossalAIStrategy
  File "/sensei-fs/users/hshariati/lightning-ColossalAI/src/lightning_colossalai/strategy.py", line 30, in <module>
    from lightning.pytorch.overrides.base import _LightningModuleWrapperBase,
_LightningPrecisionModuleWrapperBase
ModuleNotFoundError: No module named 'lightning.pytorch.overrides.base'
>>>


>>> from lightning_colossalai import ColossalAIStrategy
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/sensei-fs/users/hshariati/lightning-ColossalAI/src/lightning_colossalai/__init__.py", line 5, in <module>
    from lightning_colossalai.strategy import ColossalAIStrategy
  File "/sensei-fs/users/hshariati/lightning-ColossalAI/src/lightning_colossalai/strategy.py", line 30, in <module>
    from lightning.pytorch.overrides.base import _LightningModuleWrapperBase, _LightningPrecisionModuleWrapperBase
ModuleNotFoundError: No module named 'lightning.pytorch.overrides.base'
>>>



Successfully installed lightning-2.0.0
(hs_AD_3.10.13) hshariati@training-effic-test2-dit-0-0:/sensei-fs/users/hshariati/lightning-ColossalAI$ python
Python 3.10.13 (main, Sep 11 2023, 13:44:35) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from lightning_colossalai import ColossalAIStrategy
>>>

>>> my_strategy = ColossalAIStrategy(placement_policy="gpu")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/sensei-fs/users/hshariati/lightning-ColossalAI/src/lightning_colossalai/strategy.py", line 169, in __init__
    raise ModuleNotFoundError(
ModuleNotFoundError: To use the `ColossalAIStrategy`, please install `colossalai` first. Download `colossalai` by consulting `https://colossalai.org/download`.

my_strategy = ColossalAIStrategy(placement_policy="cuda")
```

## Lama, Gpt2, Vit

## Experiments notes 03/19/2024:

### Worked:

`Docker pull nvcr.io/nvidia/nemo:24.01.01`

### This command worked:

```bash
docker run --gpus all -it --rm --shm-size=4g -p 8000:8000 -v ${PWD}/GPT-2B-001_bf16_tp1.nemo:/opt/checkpoints/GPT-2B.nemo -w /opt/NeMo nvcr.io/nvidia/nemo:24.01.01
```

### What I ran:

```bash
docker run --gpus all -it --rm --shm-size=4g -p 8000:8000 -v ${PWD}/GPT-2B-001_bf16_tp1.nemo:/opt/checkpoints/GPT-2B.nemo -v /mnt/localssd/hshariati:/workspace/mount_dir -w /opt/NeMo nvcr.io/nvidia/nemo:24.01.01
```

Then I went into `/opt/NeMo-Megatron-Launcher`

```bash
root@8d5134db9512:/opt/NeMo-Megatron-Launcher# pip install -r ./requirements.txt
```

Got this error:

```
ERROR: pip's dependency resolver does
not currently take into account all the packages that are installed.
This behaviour is the source of the following dependency conflicts.
tensorboard 2.9.0 requires tensorboard-data-server<0.7.0,>=0.6.0, but you have tensorboard-data-server 0.7.2 which is incompatible.
ndc 0.1.0 requires charset_normalizer>=3.1.0, but you have charset-normalizer 2.0.12 which is incompatible.
ndc 0.1.0 requires zstandard==0.18.0, but you have zstandard 0.15.2 which is incompatible.
```

Then I edited the config files. Once the repository has been cloned and the cluster configuration is set, the configuration files can be modified to launch the data preparation stage for The Pile dataset. First, a few config files need to be updated. Back at the `launcher_scripts` directory from before, open `conf/config.yaml` in a text editor. The following settings need to be modified:

* `cluster`: This needs to be “k8s”.
* `data_preparation`: This should be “gpt3/download\_gpt3\_pile”.
* `stages`: This needs to be just “data\_preparation” and no other stage.
* `cluster_type`: This needs to be “k8s”. Note that this is different from the “cluster” parameter above.
* `launcher_scripts_path`: This is the path to the cloned `nemo-megatron-launcher` repository. This needs to end in `launcher_scripts`.
* `container`: Replace this with the latest version of the training container available on NGC, such as “nvcr.io/ea-bignlp/ga-participants/nemofw-training:<TAG>”. Replace `<TAG>` with the latest container tag available.

Next, open `conf/data_preparation/gpt3/download_gpt3_pile.yaml` in a text editor. Update the `node_array_size` to the number of worker nodes in the cluster. The higher the worker count, the faster data preparation will finish. [https://api.ngc.nvidia.com/v2/catalog/containers/public-key](https://api.ngc.nvidia.com/v2/catalog/containers/public-key)

## Streaming

```
main
git@git.corp.adobe.com:colligo/streaming.git
commit 75ddca7f0779bc9170369299545f0701a2981837 (HEAD -> main, origin/main, origin/HEAD)
Merge: 44985cb 34699f7
Author: Dibyajyoti Ghosh <dghosh@adobe.com>
Date:   Tue Feb 27 16:46:24 2024 -0800

    Merge pull request #44 from colligo/dghosh-patch-1

    Update downloader_worker.py
```

## Piat

```
twotrainings-dmd

commit e3e5fee4bcaf8ec83c5cc48ea2778ff3d79e6fe2 (HEAD -> twotrainings-dmd, origin/twotrainings-dmd)
Author: Ben Bowles <bowles@adobe.com>
Date:   Thu Mar 7 16:55:46 2024 -0800

    updates
```

`/sensei-fs/projects/firefly/clio/runai_training/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-03-28T14-34-13/lightning_logs/version_25/checkpoints`

```bash
git remote set-url origin git@github.com:Adobe-Firefly/piat.git
```

## Save Decoded Image

To save a decoded (colligo tensor) image:

```python
from torchvision.transforms.functional import to_pil_image
k = to_pil_image(response.images.as_torch()[0])
k.save("/sensei-fs/users/hshariati/colligo_files_backup/shayan_colligo/colligo/delete/test.png")
```

## Next for DMD

Two 32 node experiments:

* One with t2i (no MC) == drop all MC
* Just t2i same as above and then 5 times more images with people (i.e., with faces)
* Run some MC conditions on the latest ckpt. Use depth (not edges).
* Rerun on the training tests. Run the checkpoint on the training set.

```
commit 8a075c06c51a57fb3d107242e4e455941c51808b (HEAD -> main,
origin/main, origin/HEAD)
Author: Shayan Hoshyari <hoshyari@adobe.com>
Date:   Wed Apr 10 13:31:24 2024 -0700

    [colligo.dev.example.yaml] Add info about runai and authorization token.
```

```python
python3 scripts/clio3/run_inference_pipelines_clio3.py \
--checkpoints_yaml /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/apps/inference/inference/configs/model_explore/clio3/prod/checkpoints.yaml \
--config /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/apps/inference/inference/configs/model_explore/clio3/prod/c3_prod3_128px_inference_config.yaml \
--text_prompt /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/cliocore/prototyping_tools/src/clio/prototyping_tools/data/eval_sentences/tests/FF_presets_structure_prompts.txt \
--structure_image /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/cliocore/prototyping_tools/src/clio/prototyping_tools/data/eval_sentences/tests/FF_presets_structure_images.txt \
--controls canny \
--model_id prod5_mc_aes \
--limit_prompts 3 \
--model_name prod5_mc_aes \
--save_to /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/delete \
--return_file_path /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/delete/file.html
```

```bash
hshariati@dmd-mc-test-0-0:/sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion$ python3 scripts/clio3/run_inference_pipelines_clio3.py --checkpoints_yaml /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/apps/inference/inference/configs/model_explore/clio3/prod/checkpoints.yaml --config /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/apps/inference/inference/configs/model_explore/clio3/prod/c3_prod3_128px_inference_config.yaml --text_prompt /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/cliocore/prototyping_tools/src/clio/prototyping_tools/data/eval_sentences/tests/FF_presets_structure_prompts.txt --structure_image /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/cliocore/prototyping_tools/src/clio/prototyping_tools/data/eval_sentences/tests/FF_presets_structure_images.txt --controls canny --model_id prod5_mc_aes --limit_prompts 3 --model_name prod5_mc_aes --save_to /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/delete --return_file_path /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/delete/file.html
```

```bash
(hs_AD_3.10.13) hshariati@dmd-mc-test-0-0:/sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion$ python3 scripts/clio3/run_inference_pipelines_clio3.py --checkpoints_yaml /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/apps/inference/inference/configs/model_explore/clio3/prod/checkpoints.yaml --config /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/apps/inference/inference/configs/model_explore/clio3/prod/c3_prod3_128px_inference_config.yaml --text_prompt /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/cliocore/prototyping_tools/src/clio/prototyping_tools/data/eval_sentences/tests/FF_presets_structure_prompts.txt --structure_image /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/cliocore/prototyping_tools/src/clio/prototyping_tools/data/eval_sentences/tests/FF_presets_structure_images.txt --controls canny --model_id prod3_27 --limit_prompts 3 --model_name prod5_mc_aes --save_to /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/delete --return_file_path /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/delete/file.html
```

`clio3_dmd_guide8_mp_v4_2024_03_22-2024-04-18T14-48-50    ode_loss	0.11865234375`
`clio3_dmd_guide8_mp_v4_2024_03_22-2024-04-18T14-48-50`

`/sensei-fs/users/hshariati/training/dmd_train_2/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-04-18T14-48-50/lightning_logs/version_0/checkpoints`

```bash
python3 scripts/clio3/run_inference_pipelines_clio3.py --checkpoints_yaml /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/apps/inference/inference/configs/model_explore/clio3/prod/checkpoints.yaml --config /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/apps/inference/inference/configs/model_explore/clio3/prod/c3_prod3_128px_inference_config.yaml --text_prompt /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/cliocore/prototyping_tools/src/clio/prototyping_tools/data/eval_sentences/tests/FF_presets_structure_prompts.txt --structure_image /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/cliocore/prototyping_tools/src/clio/prototyping_tools/data/eval_sentences/tests/FF_presets_structure_images.txt --controls canny --model_id prod3_27 --limit_prompts 30 --model_name prod3_27 --save_to /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/dele --return_file_path /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/dele/file.html --device 0
```

```python
build.s3_source(
    bucket="s3://colligo-dev-artifacts/artifacts-v1",
    key="diffusion/global_step_30000_Gcombined_colligoSlimmed.2024-04-26.18-39.c3ea0.ckpt",
    version_id="TFcpUKdMqibCBjLKgGVx3PiUcQjmTsqt",
    sha256="c3ea0b688e16e0b2b0e06ff09a0e829dc38bd95baa596d22b7bef61ff4987b57",
)
```

```python
python run_colligo_htmls.py --endpoint http://localhost:8000/v2/images/generate --token eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEtc3RnMS1rZXktYXQtMS5jZXIiLCJraWQiOiJpbXNfbmExLXN0ZzEta2V5LWF0LTEiLCJpdHQiOiJhdCJ9.eyJpZCI6IjE3MTQ1MDU1NDQ0NzlfYmE3ZWE3MzAtNTVmZC00ZGI3LThmODUtZjliZWU2N2EyOGRkX3VlMSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiJjb2xsaWdvX3Rlc3RpbmciLCJ1c2VyX2lkIjoiMDJCQTREQkE2NTMwODFDNDBBNDk0MTNEQGM2MmYyNGNjNWI1YjdlMGUwYTQ5NDAwNCIsImFzIjoiaW1zLW5hMS1zdGcxIiwiYWFfaWQiOiIwMkJBNERCQTY1MzA4MUM0MEE0OTQxM0RAYzYyZjI0Y2M1YjdlMGUwYTQ5NDAwNCIsImN0cCI6MCwiZmciOiJZTUNDSURORTdaNjZBNERaM0daTUEySUFLTT09PT09PT0iLCJzaWQiOiIxNzE0MTcxODkxODM2Xzk1OTJlNTNlLTE2NDQtNDI3MC04MmIzLWNiZDQ2Y2UzYTk5Y191ZTEiLCJtb2kiOiIyODliNjYiLCJwYmEiOiJNZWRTZWNOb0VWLExvd1NlYyIsImV4cGlyZXNfaW4iOiI4NjQwMDAwMCIsInNjb3BlIjoiQWRvYmJJRCxmaXJlZmx5X2FwaSxvcGVuaWQiLCJjcmVhdGVkX2F0IjoiMTcxNDUwNTU0NDQ3OSJ9.HYaR6E3HaNoiwergTEsXbO_UffCIVaPAkb11K8NOTdVv4lEkMjZIagU7UtS72PnsyZ7dFxomTTfH0j2U9jnGFuO5jU-e7tXFcT5DSqEWx4DJvUr-3mkQ28fBkx2LML3c_pIGE13CVwDy_lXPnHbXG_3Ps6AleUa6-vTBvKff1r9Fs6ShZHdBPEhg167cCRt0pdvt2hbp3tnQj1CGGZlq4ZJyUnqJ_Uy8J68hMg8sUsLrAvvZYAhoQtvO5KCHkOvbXZtBHnv0NTqhGarfnIuXgktqGQwk-7CrMtbccWyUgWXoQIEL3bMxIYTROArx5K0eNu7j314UnatiRlpo3dpkzQ --text_prompt /sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/cliocore/prototyping_tools/src/clio/prototyping_tools/data/eval_sentences/tests/new_eval_sentences_people.txt --limit_prompts 112 --aesthetic_score 6.0 --save_to /sensei-fs/users/hshariati/eval/clio3_dmd_guide8_mp_v4_2024_02_28-2024-03-07T11-20-43/dmd_MoE42_MoE38_people_withRag_apr30
```

## Details for Wiki

1.  Production code
2.  How to train
3.  Past experiments
4.  Colligo integration.

```python
training_config = cast(str, unet_config.training_config[0].sensei)
self.diff_config[0].model_configs.diffusion_unet.training_config[0].sensei
'prod3-18-mc-2024-01-12T21-41-30_config.yaml'

self.diff_config[0].model_configs.diffusion_unet.training_config[0]
FilePath(sensei='prod3-18-mc-2024-01-12T21-41-30_config.yaml', uw2=None, raw=None)
```

`/mnt/localssd/hshariati/colligo/models/colligo/models/firefly/diffusion/DiffusionModelMD.py`

```bash
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ ls
@spl  CODEOWNERS  Jenkinsfile  README.md  lerna.json  link.sh  package.json  packages  pnpm-lock.yaml  pnpm-workspace.yaml  publish.sh  scripts  tools  tsconfig.json
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ node -v
v12.22.9
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ curl -o- [https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh](https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh) |
bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 14984  100 14984    0     0  99609      0 --:--:-- --:--:-- --:--:-- 99893
=>
Downloading nvm from git to '/home/runai-home/.nvm'
=> Cloning into '/home/runai-home/.nvm'...
remote: Enumerating objects: 365, done.
remote: Counting objects: 100% (365/365), done.
remote: Compressing objects: 100% (313/313), done.
remote: Total 365 (delta 43), reused 167 (delta 26), pack-reused 0
Receiving objects: 100% (365/365), 365.08 KiB |
10.14 MiB/s, done.
Resolving deltas: 100% (43/43), done.
* (HEAD detached at FETCH_HEAD)
  master
=> Compressing and cleaning up git repository

=> Profile not found.
Tried ~/.bashrc, ~/.bash_profile, ~/.zshrc, and ~/.profile.
=> Create one of them and run this script again
   OR
=> Append the following lines to the correct file yourself:

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \.
"$NVM_DIR/nvm.sh"  # This loads nvm

=> Close and reopen your terminal to start using nvm or run the following to use it now:

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \.
"$NVM_DIR/nvm.sh"  # This loads nvm
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ nvm -v
bash: nvm: command not found
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ npm -v
bash: npm: command not found
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \.
"$NVM_DIR/nvm.sh"
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ npm -v^C
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ npm -v
bash: npm: command not found
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ nvm -v
0.39.0
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ nvm install 20
Downloading and installing node v20.13.1...
Downloading [https://nodejs.org/dist/v20.13.1/node-v20.13.1-linux-x64.tar.xz](https://nodejs.org/dist/v20.13.1/node-v20.13.1-linux-x64.tar.xz)...
######################################################################################################################################################################################################################################################### 100.0%
Computing checksum with sha256sum
Checksums matched!
Now using node v20.13.1 (npm v10.5.2)
Creating default alias: default -> 20 (-> v20.13.1)
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ nvm use 20
Now using node v20.13.1 (npm v10.5.2)
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ node -v
v20.13.1
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$ npm -v
10.5.2
hshariati@hs-colligo-dev-2-0-0:/sensei-fs/users/hshariati/spl-web-client$


export ARTFY_APIKEY=cmVmdGtuOjAxOjE3NDc0MTg1Njc6ZWxoU1YzeHVMMEQ3eHdiSnRSWXFmTFFpMlpl;
export ARTFY_USER=hshariati


export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A; export ARTIFACTORY_UW2_USER=hshariati


export ARTFY_APIKEY=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A

export ARTFY_APIKEY=AKCp8pRjLxcs2suDvnKdyogEU76pNmcBuBXJ1zR13WCSyMJ1S8X8wwktpH6JhPFxbhUysWNwN



On mac:
export ARTFY_USER=hshariati
export ARTFY_APIKEY=AKCp8pRjLxcs2suDvnKdyogEU76pNmcBuBXJ1zR13WCSyMJ1S8X8wwktpH6JhPFxbhUysWNwN
curl -o-  [https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh](https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh) |
bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \.
"$NVM_DIR/bash_completion"  # This loads nvm bash_completion
nvm install 20
nvm use 20

*make sure:
	node -v
	Gives above v20 like: v20.13.1

npm -g i pnpm
./scripts/onetime-setup.sh
corepack enable pnpm
corepack use pnpm@8.6.2
brew install pkg-config cairo pango libpng jpeg giflib librsvg pixman python-setuptools
export PKG_CONFIG_PATH="/opt/homebrew/opt/jpeg/lib/pkgconfig"
echo 'export PATH="/opt/homebrew/opt/jpeg/bin:$PATH"' >> ~/.zshrc
pnpm install
pnpm start
[https://localhost.adobe.com:8080/](https://localhost.adobe.com:8080/)

Then login and select:
Neal's ETLA Express Firefly



mmcv==2.1.0
Mmcv==


export SESSION_NAME="clineto-temp-demo" export PROJECT="asml-dev" export NODE_POOL="a100-80gb-2" export NUM_GPUS=4 export EXPOSED_PORT=9000 export PREEMTIBLE=0 export EXTRA_FLAGS="-l asml_project_name=clio-model-efficiency -l activity_type=productization -l research_jack_id=5382"

We use the following checkpoints:
	For DiT:
		/sensei-fs/projects/firefly/clio/training/logs/aminian/may_t2v_dit_mds_phase4_mixed_train-2024-05-25T09-38-06/lightning_logs/version_0/checkpoints/115k_ema.ckpt
	For SSR:
		/sensei-fs/users/diliu/weights/yhong/basicvsrpp-09x-upx3-2024-05-23T17-36-33/epoch=0-step=70000.ckpt
	For 3D-VAE:


with open(
    "/sensei-fs/users/hshariati/del/clineto/dit_output.pkl", "wb"
) as file:
    pickle.dump(dit_output,file)
```

`C800a26fe617d44d1169c5d1074c15bec1a15adb.` fixes fps issue

Read from:
`/mnt/localssd/data/tmp/tmp4k08l5n2/a515bacc-a56d-41e8-a41e-a5b6f9f4119c_in.mp4`

`/mnt/localssd/data/tmp/tmpy56io32c/53b249b1-f7c5-4fa8-b927-8e0d6625ea27_gen_extend_output.mp4`

`/mnt/localssd/data/tmp/tmpy56io32c/53b249b1-f7c5-4fa8-b927-8e0d6625ea27_gen_extend_output.mp4`

Pipeline checkpoint: pipeline=video\_gen\_extend, checkpoint=Reading video from `/mnt/localssd/data/tmp/tmp4a88zvxm/9101c922-3ad1-458f-83d3-b5c5883eac19_in.mp4`, work\_flow=TextToImageWorkflow.TEXT\_TO\_IMAGE, endpoint\_name="video\_gen\_extend", input\_path="/mnt/localssd/data/tmp/tmp4a88zvxm/9101c922-3ad1-458f-83d3-b5c5883eac19\_in.mp4" {"client\_id": "colligo\_testing", "request\_id": "FD4ZYs951VvPHI4x9OyW", "session\_id": "b204047b-d125-4799-8ce3-061d96484210"}

```python
with iio.imopen(video_file, "r", plugin="pyav") as ff: it = ff.iter() for frame in it: print(frame)
```

`s3://clio-web-app/video/data_set/people_interview_shoulder_addedJun2024/videos/99786-720.mp4`

`" https://pre-signed-firefly-dev.s3.amazonaws.com/images/989f10f6-5343-4ea9-b358-ca14c0f739c9?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA4KAGRHX6XW442I3D%2F20240619%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240619T230027Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=22efc7b2c19aa5eb2cdd07c025a99d4a8de71467cc9f7eda1bc0fa5af6edebd8"`

`https://clio-web-app.s3.amazonaws.com/images/989f10f6-5343-4ea9-b358-ca14c0f739c9`

`1920x1056`

```bash
pip install clip@git+[https://github.com/openai/CLIP.git@a1d071733d7111c9c014f024669f959182114e33](https://github.com/openai/CLIP.git@a1d071733d7111c9c014f024669f959182114e33) --no-dependencies
```

Double check in `guidance.py`:

1.  `Uncond_schedule` switch none (line 6110) this should be not done
2.  handle edify switch should be no op (line 614)
3.  Line 415, normalize direction should be false
4.  Line 422, dynamic threshold direction should be None/False
5.  Is the scheduler seeded correctly? Also, their noise is generated dynamically is that different? Dump their noise at each step, to see if we can match. We ensured the following to achieve parity: Same normalize direction

## LDL

137 mg/dL, range 0, 99 March
135 mg/dL, July

## HDL

32 March
32 July

## ALT+AST

89 and 51, (0 to 40, 0 to 44) March
38, and 44 July

check\_circleAST (SGOT)
An enzyme found in the cells throughout the body but mostly in the cells of the heart and liver. High aspartate aminotransferase (AST) levels could be a sign of liver damage, among other conditions.
Normal ≤ 40 IU/L (38)
Moderately High 41-55 IU/L
High 56-400 IU/L
Very High ≥ 401 IU/L

check\_circleALT (SGPT)
An enzyme found mostly in the cells of the liver and kidney. High levels of alanine aminotransferase (ALT) could be a sign of liver damage or infection, among other conditions.
Normal ≤ 44 IU/L (44)
Moderately High 45-70 IU/L
High 71-400 IU/L
Very High ≥ 401 IU/L

Find examples of times that suffering actually helped. Times where suffering is necessary:

1.  Studying, all the final exams
2.  Job interviews
3.  Going on heavy diets to meet people
4.  But is the suffering of not doing weed necessary?

Home work:
Start a blog or email address for the kids. Write letters to the kid. Write a little letter of what's on your mind next week. I want to tell you that I want you to have autonomy but also I'm doing what I can as a parent to make sure you're serious. Family cook book. With recipes that each of us like (Ana, Hooman, Florance) And you can have the adam's family cook book on Etsy. And you can write down their favorite food, etc.

`/sensei-fs/users/hshariati/worktree_AdobeDiffusion/kduarte/dmd-sliders/hs_scripts/SDEdit.ipynb`

[http://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/gpathak/git\_repos/colligo/contrib/Mori/collections/genai\_foundation/results/t2v\_798K/checkpoints\_\_size-40x44x80\_steps-50\_timestepInterpSteps-25\_cfg-7.5\_eta-1.0\_negstyle-custom\_ness-none\_matchenergy-True\_ema-True\_cfgcutofft-600\_frames-40/interesting/09-17-2024\_15-46-03/interesting.html](http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/gpathak/git_repos/colligo/contrib/Mori/collections/genai_foundation/results/t2v_798K/checkpoints__size-40x44x80_steps-50_timestepInterpSteps-25_cfg-7.5_eta-1.0_negstyle-custom_ness-none_matchenergy-True_ema-True_cfgcutofft-600_frames-40/interesting/09-17-2024_15-46-03/interesting.html),[http://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/gpathak/git\_repos/colligo/contrib/Mori/collections/genai\_foundation/asml-prod-phase4-morix-128n-6m-data-genieimage-hsdp-condition-simplified-run4/t2v\_800K/asml-prod-phase4-morix-128n-6m-data-genieimage-hsdp-condition-simplified-run4\_ckpt\_step00800000.pth\_size-40x44x80\_steps-50\_timestepInterpSteps-25\_cfg-7.5\_eta-1.0\_negstyle-custom\_ness-none\_matchenergy-True\_ema-True\_cfgcutofft-20\_frames-40/interesting/09-17-2024\_16-14-31/interesting.html](http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/gpathak/git_repos/colligo/contrib/Mori/collections/genai_foundation/asml-prod-phase4-morix-128n-6m-data-genieimage-hsdp-condition-simplified-run4/t2v_800K/asml-prod-phase4-morix-128n-6m-data-genieimage-hsdp-condition-simplified-run4_ckpt_step00800000.pth_size-40x44x80_steps-50_timestepInterpSteps-25_cfg-7.5_eta-1.0_negstyle-custom_ness-none_matchenergy-True_ema-True_cfgcutofft-20_frames-40/interesting/09-17-2024_16-14-31/interesting.html)

```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/hshariati/del/clineto/i2v_morgan.txt --endpoint http://localhost:8000 --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/baseline_i2v_h100_allDefault_09-24-24_morgan5 --width 1280 --height 720 --num_frames 128  --seeds "0, 24" --save_fps 24 --overwrite True --limit_prompts 100
```

```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/hshariati/del/clineto/i2v_morgan.txt --endpoint http://localhost:8000 --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/baseline_i2v_h100_newSamplingParams_09-24-24_morgan6 --width 1280 --height 720 --num_frames 128  --seeds "0, 24" --save_fps 24 --overwrite True --limit_prompts 100
```

t2v, morgan prompts, 814k TRT

* no prompty: [http://clio.corp.adobe.com/model\_evaluation//mnt/localssd/temp/siddhantg/t2v\_morgan\_prompts\_no\_prompty\_sep\_24\_1815hrs/t2v.html](http://clio.corp.adobe.com/model_evaluation//mnt/localssd/temp/siddhantg/t2v_morgan_prompts_no_prompty_sep_24_1815hrs/t2v.html)
* with prompty: [http://clio.corp.adobe.com/model\_evaluation//mnt/localssd/temp/siddhantg/t2v\_morgan\_prompts\_with\_prompty\_sep\_24\_1815hrs/t2v.html](http://clio.corp.adobe.com/model_evaluation//mnt/localssd/temp/siddhantg/t2v_morgan_prompts_with_prompty_sep_24_1815hrs/t2v.html)
* [http://clio.corp.adobe.com/model\_evaluation//home/sannavajjala/morgan\_sampling\_prompty\_t2v/t2v.html](http://clio.corp.adobe.com/model_evaluation//home/sannavajjala/morgan_sampling_prompty_t2v/t2v.html) (With prompty)
* [http://clio.corp.adobe.com/model\_evaluation//home/sannavajjala/morgan\_sampling\_no\_prompty\_t2v/t2v.html](http://clio.corp.adobe.com/model_evaluation//home/sannavajjala/morgan_sampling_no_prompty_t2v/t2v.html) (Without prompty)

```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/hshariati/del/clineto/t2v_morgan_short_prompts.txt --endpoint http://localhost:8000 --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/baseline_t2v_short_prompts_h100_withForceLowerCase_09-26-24_6 --width 1280 --height 720 --num_frames 128  --seeds "0, 24" --save_fps 24 --overwrite True --limit_prompts
100
```

```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/hshariati/del/clineto/t2v_morgan_short_prompts.txt --endpoint http://localhost:8000 --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/baseline_t2v_short_prompts_h100_oldPromptReWrite_09-26-24_3 --width 1280 --height 720 --num_frames 128  --seeds "0, 24" --save_fps 24 --overwrite True --limit_prompts 100
```

```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/hshariati/del/clineto/i2v_morgan.txt --endpoint http://localhost:8000 --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/baseline_i2v_h100_noPrompty_09-26-24_morgan_2 --width 1280 --height 720 --num_frames 128  --seeds "0, 24" --save_fps 24 --overwrite True --limit_prompts 100
```

```bash
cd contrib/AdobeDiffusion/scripts/clineto
```

```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/hshariati/del/clineto/i2v_morgan.txt --endpoint http://localhost:8000 --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/baseline_i2v_h100_allDefaults_09-26-24_morgan_1 --width 1280 --height 720 --num_frames 128  --seeds "0, 24" --save_fps 24 --overwrite True --limit_prompts 100
```

```
[colligo frontend:2109740 INFO 1381473ms]   Started frontend_request {"client_id": "ASMLSenseiTest", "guid": null, "log_code": "COLLIGO-007", "method": "POST", "path": "/v2/videos/generate", "request_id": "e79b90f4-c6c6-499c-9f79-06427fb384dd", "session_id": "f7c586f2-bf70-4342-b6d4-f328b0c20918", "zone": "frontend_request"}
[colligo
clineto_proxy_pipeline:2109805 INFO 1381175ms]   User request content: b'{"seeds": [853], "prompt": "A jaguar runs at full speed on a wide open grassland, it is a hot sunny day, there are no other animals in the frame"}' {"client_id": "ASMLSenseiTest", "log_code": "COLLIGO-007", "request_content": "b'{\"seeds\": [853], \"prompt\": \"A jaguar runs at full speed on a wide open grassland, it is a hot sunny day, there are no other animals in the frame\"}'", "request_id": "e79b90f4-c6c6-499c-9f79-06427fb384dd", "session_id": "f7c586f2-bf70-4342-b6d4-f328b0c20918"}
/v2/videos/generate/jobs/result/679bcf7c-f6a6-4564-a1ff-562e7c6e8d6a
```

`/sensei-fs/users/thinz/colligo/contrib/Mori/eval_sentences_harm_and_bias.txt`

```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/thinz/colligo/contrib/Mori/eval_sentences_harm_and_bias.txt --endpoint http://localhost:8000 --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/harm_with_adobeOne_6 --width 1280 --height 720 --num_frames 128  --seeds "0,24" --save_fps 24 --overwrite True --limit_prompts 100
```

`"enable_prompty":false,"dit_model_name":"filix2_t2v_prod1_814k32n"`

```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/thinz/colligo/contrib/Mori/eval_sentences_harm_and_bias.txt
--endpoint http://localhost:8000 --task i2v --save_to /sensei-fs/users/hshariati/del/clineto/html/harm_no_adobeOne_4 --width 1280 --height 720 --num_frames 128  --seeds "0,24" --save_fps 24 --overwrite True --limit_prompts 100
```

Contract negotiation (we still have to do it)
Manual work on upload (well automate it)

`s3://clio-web-app/video/data_set/abobe_stock/HD/653748716.mp4`
`https://clio-web-app.s3.amazonaws.com/video/data_set/abobe_stock/HD/653748716.mp4`
`https://clio-web-app.s3.amazonaws.com/video/data_set/abobe_stock/HD/842307808.mp4`

```python
def download_video_from_s3(s3_url: str, local_dir: str) -> Path:
    """
    Downloads a video from an S3 URL and stores it on disk at the specified location.
Args:
        s3_url (str): The S3 URL of the video.
local_dir (str): The local directory where the video should be stored.
Returns:
        Path: The path to the downloaded video file.
"""
    # Parse the URL to get the file name
    parsed_url = urlparse(s3_url)
    file_name = os.path.basename(parsed_url.path)
    # Create the local directory if it doesn't exist
    local_path = Path(local_dir)
    local_path.mkdir(parents=True, exist_ok=True)
    # Full path to the local file
    local_file_path = local_path / file_name
    # Download the file
    response = requests.get(s3_url, stream=True)
    response.raise_for_status()  # Raise an error for bad status codes
    with open(local_file_path, "wb") as
f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return local_file_path

# Example usage
s3_url = "[https://clio-web-app.s3.amazonaws.com/video/data_set/abobe_stock/HD/740645080.mp4](https://clio-web-app.s3.amazonaws.com/video/data_set/abobe_stock/HD/740645080.mp4)"
local_dir = "/sensei-fs/users/hshariati/del/clineto/data_for_flickering"
downloaded_file_path = download_video_from_s3(s3_url, local_dir)
print(f"Downloaded video to: {downloaded_file_path}")
```

```python
from colligo.models.compare.v2.videos.extend.utils.storage import (
    _ensure_storage_item,
    download_video_from_s3
)
```

```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/hshariati/colligo/contrib/autoX/experiments/data_for_chris/commands/data/stereotypes_t2v_2_part2.txt --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) --task t2v --save_to /sensei-fs/users/hshariati/colligo/contrib/autoX/experiments/data_for_chris/commands/data/stereotypes_t2v_2_part4 --width 1280 --height 720 --num_frames 128  --seeds "0" --save_fps 24 --overwrite True --limit_prompts 55;
[https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/colligo/contrib/autoX/experiments/data_for_chris/commands/data/stereotypes_t2v_2_part4/t2v.html](https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/colligo/contrib/autoX/experiments/data_for_chris/commands/data/stereotypes_t2v_2_part4/t2v.html)
```

```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/hshariati/colligo/contrib/autoX/experiments/data_for_chris/commands/data/violence_weapons_t2v_part2.txt --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) --task t2v --save_to /sensei-fs/users/hshariati/colligo/contrib/autoX/experiments/data_for_chris/commands/data/violence_weapons_t2v_part6 --width 1280 --height 720 --num_frames 128  --seeds "0" --save_fps 24 --overwrite True --limit_prompts 23;
```

Aug 29 5:51pm
`0.0.1-main.3223-commit=1aa72423`
ENVIRONMENTS:

1.  STAGE- clio-video on [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  DEV - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG

1.  \[FFP-5724] CAI for Gen-extend (#4284)
2.  \[FFP-17270] Make prompt optional and provide a default value for I2V (#4502)
3.  \[FFP-17407] Make cai signing in clineto optional (#4506)
4.  \[FFP-15369] Integrate TRT engines for gen-extend DiT (#4212)
5.  Update T2V/I2V ckpt (#4516)
6.  \[FFP-17271] Allow any size input image for I2V (#4510)

Aug 30 10:43pm
`0.0.1-main.3327-commit=62fa5274.sh` in progress
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE- clio-video on [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-17433] fix write video when floating point fps (#4518)
2.  Switch to old 3dvae decoder and cfg fix for i2v (#4511)
3.  Added warp\_t for colligo prod (#4500)
4.  \[FFP-1382] - color metadata for DVA (#4419)
5.  \[FFP-15823]Colligo.AOTI fixes and new version + 3DVae multi chunk decoder compile script (#4355)

Aug 30 2:29pm
`0.0.1-main.3327-commit=62fa5274.sh` in progress
ENVIRONMENTS:

1.  DEV - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net)

CHANGE LOG:

1.  \[FFP-17433] fix write video when floating point fps (#4518)
2.  Switch to old 3dvae decoder and cfg fix for i2v (#4511)
3.  Added warp\_t for colligo prod (#4500)
4.  \[FFP-1382] - color metadata for DVA (#4419)
5.  \[FFP-15823]Colligo.AOTI fixes and new version + 3DVae multi chunk decoder compile script (#4355)

Aug 30 3:54
`0.0.1-main.3375-commit=762a541e.sh` in progress
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  FFP-17505: default prompt\_negative for t2v and i2v (#4542)
2.  \[FFP-17230] Add TRT support for T2V, I2V (#4483)
3.  \[FFP-17539] Separate out I2V, T2V and V2v models in build.py (#4546)

Sep 3 1:37pm
`0.0.1-main.3532-commit=b3fc0bf6` in progress
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-8274] mori-restructure (#4552)
2.  \[FFP-15369] Update TRT engine for gen-extend 1080p (#4547)
3.  \[FFP-1382]: Use mediainfo for color read (#4555)
4.  \[FFP-15823]Clean code in Multichunk decoder code and AOT compiler specific fixes (#4354)
5.  \[FFP-17731] Add robust vid utils (#4576)
6.  Adding prompt forge filix worker (#4522)

Sep 4 9:28am
`0.0.1-main.3703-commit=7d8d8d78`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-17816] Use crop and resize for reference images (#4586)
2.  debug i2v (#4589)
3.  \[FFP-17829] Add clineto debug parameters (#4590)
4.  \[FFP-17790][Clio Video][Profiling the pipeline] replace .\_run with .call (#4599)
5.  \[FFP-17822] Integrate prompt forge + rewrite (#4587)
6.  Added configurable parameters for diffusion\_loop (#4579)
7.  Flag for disabling rewrite, reusing the previous autocomplete flag (#4601)
8.  Update multichunk decoder with non gan (#4603)
9.  Integrating reduced sampling steps into minimal inference. (#4471)

Sep 4 11:33am
`0.0.1-main.3733-commit=796973c1`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-17919] Make trt default (#4617)
2.  Making vae3d run on pytorch 2.3 (#4618)

Sep 4 4:07pm
`0.0.1-main.3814-commit=2e261529`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-17938] Disable prompty control in Clineto (#4621)
2.  move resize inside SSR model for reducing overhead time, further reduce chunk size (#4622)
3.  Update build.py (#4625)
4.  \[FFP-17951] Add prompt length condition for rewrite (#4630)
5.  \[FFP-17444] Fix defaults for clineto pipeline (#4640)
6.  update trt engine for v2v (#4638)

Sep 5 10:00 am
`0.0.1-main.3928-commit=71187d2a`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-17951] Update prompt rewrite condition (#4641)
2.  Xxue/log (#4647)
3.  TRT inference improvements for clio-video (#4645)
4.  Add 360p for gen extend (#4649)
5.  cai parallel (#4673)
6.  fix output schema (#4666)

Sep 5 1:25Pm
`0.0.1-main.4031-commit=da048684`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  Filix2 file reversion to unblock clio4 (#4670)
2.  \[CAI-5999][FFP-1133] CAI lib update (#4122)
3.  \[FFP-18038] Validate num frames in clineto (#4681)
4.  Configurable cfg scale (#4685)
5.  \[FFP-18059] Move DiT pytorch models to experimental (#4689)
6.  \[FFP-5724] Add signing to high res video (#4680)
7.  genExtend: 1) decode 16 frames only, 2) NSFW and VAE in parallel (#4690)
8.  \[FFP-18070] Throw 422 error for prompts > 2048 characters (#4691)

Sep 5 3:36
`0.0.1-main.4078-commit=bc2fd6a5`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  Adding support for 30 steps and timestep interpolation for gen extend (#4687)
2.  \[FFP-17938] Prompty disable control in clineto (#4692)
3.  \[FFP-18089] Raise exception for prompty nsfw error (#4700)
4.  Making diffusion loop more configurable (#4699)

Sep 6 11:39am
`0.0.1-main.4232-commit=b190f7c4`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  post diffusion nsfw parallel (#4704)
2.  \[FFP-18104] Update nsfw video policy (#4709)
3.  AOT decoder and encoder integration (#4593)
4.  Move heavy tasks to the background thread on Clineto pipeline (#4714)

Sep 6 12:24pm
`0.0.1-main.4250-commit=3ce25bf7`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  Make torch default for decoder (#4736)
2.  Update AOT encoder (#4734)

Sep 6 6:36pm
`main.4295-commit=b6813cf4.sh`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  debug pipeline: low res (#4748)
2.  prompt validation (#4738)

Sep 6 8:21pm
`main.4295-commit=b6813cf4.sh` (DONE)
ENVIRONMENTS:

1.  PROD firefly-gen-video-preview.adobe.io, firefly-gen-video.adobe.io

CHANGE LOG:

1.  debug pipeline: low res (#4748)
2.  prompt validation (#4738)

Sep 9 11:40am
`main.4390-commit=3f083ad2`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-18221] Add a proxy pipeline in front of the clineto pipeline (#4743)

Sep 10 6:37pm
`0.0.1-main.4715-e1f0c221`
ENVIRONMENTS: STAGE, EVAL and DEV (DEPLOYED)

CHANGE LOG:

* FFP-18539 Address nsfw exceptions: (ColligoPromptUnsafeException, ColligoImageUnsafeException) throwing 500 errors instead of returning 451 errors
* \[FFP-18619] Increase pipeline default timeout to 10 minutes (Optimization on the pipeline to address timeouts for longer running (p99) requests)
* \[FFP-18539]: fix nsfw exception2: consistency with image (#4794) (Follow-up PR from FFP-18539 Address nsfw exceptions )

Sep 11 5:11pm
`0.0.1-main.5135-commit=975dec2d`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-18699] Add ColligoFileNotFoundException to Clineto passthrough errors (#4853)
2.  \[FFP-16340] Moved AOTI model specific export/runtime code next to the source torch models (#4805)
3.  \[FFP-18660] Add support for mode P images (#4836)
4.  \[FFP-18692] Move Diffusion code to standalone module from clineto folder in colligo (#4828)
5.  \[FFP-18797][Clineto] Convert all modes to RGB (#4891)

Sep 18. 10:01am
`0.0.1-main.6261-commit=031a53aa`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-16001] Etesfa/Load test - comparison suite integration (#4588)
2.  \[FFP-18104] Add child classifier to Clineto (#5026)
3.  \[FFP-18645] Turn off debiasing for I2V (#4827)
4.  Revert "[FFP-18104] Add child classifier to Clineto" (#5076)
5.  \[FFP-19293] TRT FP8 improvements for T2V (#5061)
6.  \[FFP-19328] Fix clineto expansion condition (#5085)
7.  \[FFP-18104] Add child classifier to Clineto (#5079)

Sep 18 3:55pm
`0.0.1-main.6392-commit=f7f5948c`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-19358] Add missing asset back (#5090)
2.  \[FFP-19323] Handle errors during html generation (#5081)
3.  \[FFP-18981, FFP-18726]tensor format consistent (#5044)
4.  \[FFP-19176] Add match-energy configurability (#5096)
5.  \[FFP-18726] fix comment (#5100)
6.  \[FFP-19375] Temp fix for vae3d decoder oom error (#5086)

Sep 23 1:05 pm
`0.0.1-main.6882-commit=9e91856e`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
4.  load-test [https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-16001][Clio Video] Clineto I2V Load Test mods (#5110)
2.  \[FFP-19506]turn encoder aot on (#5144)
3.  \[FFP-19505] Turn off child classifier for t2v, v2v (#5152)
4.  \[FFP-19216] Sparsity updates (#5036)
5.  Fix timestep split for I2V (#5196)
6.  Add missing interface values (#5173)
7.  \[FFP-18979] Support 2 DiffusionTransformerModels running side by side (#5165)

Sep 24 10:32am
`0.0.1-main.7092-commit=913613fe`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
4.  load-test [https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-16965] Merge Clineto-prod into main (#4980)
2.  Turn off aot (#5215)

Sept 24 12:26pm
`0.0.1-main.7121-commit=a9fddeb5`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
4.  load-test [https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[NO JIRA] Update build.py to replace 810k ckpt with 814k ckpt (but actually 813k ckpt, 32node finetune) (#5233)

Sep 24 4:15pm
`0.0.1-main.7208-commit=c5ea8afa`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-19901 ] Add trt bf16 engine for 814k t2v (#5250)

Sep 25 11:54am
`0.0.1-main.7421-commit=7b911113`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  load-test [https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-19926] Add fp8 engines for 814k ckpt T2V (#5268)
2.  \[FFP-19870] Use MAX\_CLINETO\_PROMPT\_LENGTH for gen video (#5294)

Sep 25 3:12pm
`0.0.1-main.7489-commit=8eee3927`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  load-test [https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  Updating Prompt Forge to not alter text case until the end (#5265)
2.  \[FFP-18512][FFP-19776]video prompt rewrite integration (#5272)
3.  Hshariati/t2v sampling param update (#5297)

Sept 25 5:11pm
`0.0.1-main.7561-commit=39394893`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
4.  load-test [https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  Fixing configs pydantic issue (#5310)
2.  \[FFP-18512Video prompt rewrite final checkpoint drop (#5322)
3.  \[FFP-18179]: updating sampling params for t2v and i2v (round 2) (#5323)

Sep 25 5:43pm
`0.0.1-main.7580-commit=38b07f58`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
4.  load-test [https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-19926] Update fp8 engine for T2V (#5326)

Sep 26 3:51pm
`0.0.1-main.7874-commit=a98b3d78`
ENVIRONMENTS:

1.  DEV - clio-video [https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
4.  load-test [https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-20178] Cleanup diffusion workers for T2V (#5359)

Sept 27 10:08am
`0.0.1-main.8053-commit=343d4d4c`
ENVIRONMENTS:

1.  DEV - gen-video [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://clio-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
4.  load-test [https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-20004] Turn aot on (#5368)

Sep 27 2:58pm
`0.0.1-main.8053-commit=343d4d4c`
ENVIRONMENTS:

1.  PROD- gen-video (firefly-gen-video.adobe.io)

CHANGE LOG:
I2V/T2V

1.  \[FFP-19901 ] Add trt bf16 engine for 814k t2v (#5250)
2.  \[FFP-19926] Add fp8 engines for 814k ckpt T2V (#5268)
3.  \[FFP-19870] ADD MAX PROMPT\_LENGTH for gen video (#5294)
4.  Updating Prompt Forge to not alter text case until the end (#5265)
5.  \[FFP-18512][FFP-19776]video prompt rewrite integration (#5272)
6.  sampling param update (#5297)
7.  \[FFP-18512Video prompt rewrite final checkpoint drop (#5322)
8.  \[FFP-18179]: updating sampling params for t2v and i2v (round 2) (#5323)
9.  \[FFP-19926] Update fp8 engine for T2V (#5326)
10. \[FFP-20178] Cleanup diffusion workers for T2V (#5359)

Extend

1.  \[FFP-20004] Turn aot on (#5368)

Common/Pipeline

1.  FFP-18512 Fixing configs pydantic issue (#5310)

Sep 28 9:38AM
`0.0.1-main.8147-commit=be81bbe1`
ENVIRONMENTS:

1.  DEV - gen-video [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  STAGE - clio-video [https://gen-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-19926] Make fp8 default for t2v / i2v (#5397)

Sep 30 3:04pm
`0.0.1-release-firefly_clineto-main.8147.8262-commit=9eec8d5b`
ENVIRONMENTS:

1.  STAGE - gen-video [https://gen-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-20446]Use avoid prompt cartoon, vector art, & bad aesthetics & poor aesthetic (#5413)

Sept 30 1:39pm
`0.0.1-main.8246-commit=64a86df3`
ENVIRONMENTS:

1.  DEV - gen-video [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-20329]: return dit model name and all other configs (#5396)
2.  \[FFP-20446]Use avoid prompt cartoon, vector art, & bad aesthetics & poor aesthetic (#5413)

Oct 2 4:20pm
`0.0.1-release-firefly_clineto-main.8147.8812-commit=3f7d8477`
ENVIRONMENTS:

1.  STAGE - gen-video [https://gen-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-20590]: Fixes concurrency limiter issue with service/user tokens
2.  \[FFP-20735] Activate Torch as default for decoder V2V - DVA (#5502)

Oct 3 2:02pm
`0.0.1-main.9078-commit=c2ecfd13`
ENVIRONMENTS:

1.  Dev - gen-video [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  Filix2 refactor (#5461)
2.  Reduce cpu usage for VAE 3D decoder (#5516)
3.  \[FFP-20664]: add adobeOne to I2V (#5477)
4.  \[FFP-20669] Integrate dentro (internvl 8b) into Clineto (#5508)
5.  \[FFP-20840] Changes for dentro deployment (#5555)

Oct 4 1:10pm
`0.0.1-main.9389-commit=f78357d8`
ENVIRONMENTS:

1.  Dev - gen-video [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-20785] Dentro Post + Fix outputs + Update trees + Some cleanup (#5585)

Oct 4 7:22am
`0.0.1-main.9216-commit=edf154af`
ENVIRONMENTS:

1.  Dev - gen-video [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-18794] Moved T5 padding to model (#5017)
2.  \[FFP-20840] Add dentro dependencies + cleanup (#5571)
3.  \[FFP-20926] celeb check via AWS rekognition (cherry picked from rohan) (#5556)

Oct 4 3:01pm
`0.0.1-main.9449-commit=3867a635`
ENVIRONMENTS:

1.  Dev - gen-video [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Load Test - [https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-20785] dentro hot fix celeb (#5607)
2.  \[FFP-21004] Remove child classifier from NSFW Clineto (#5609)

Oct 6 12:48pm
`0.0.1-main.9550-commit=66809134`
ENVIRONMENTS:

1.  Dev - gen-video [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
2.  Eval - gen-video-eval [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)
3.  Load Test - [https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://load-test-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-21036] Fix Rekognition Service + Enable some Dentro parallelism (#5633)

Oct 7 11:52AM
`0.0.1-main.9629-commit=6f237202`
ENVIRONMENTS:

1.  Dev - gen-video [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-21092][Gen-video] Prompt Rewrite: Disable per PM recommendation (Sandhya)

Oct 8 12:47pm
`main.8147.9094-commit=b4a95a4d.sh`
ENVIRONMENTS:

1.  prod

CHANGE LOG:

1.  support DVA 5 rpm
2.  apply throttling/concurrency limit
3.  sync up gen extend prod with stg build: use decoder torch version…

Oct 8 12:02pm
`0.0.1-release-firefly_clineto-main.8147.9653-commit=2ed39ece`
ENVIRONMENTS:

1.  STAGE - gen-video [https://gen-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  \[FFP-20664]: add adobeOne to I2V (#5477)
2.  Aligns xreadgroup timeout with the redis socket timeout (#5610)
3.  \[FFP-21092][Gen-video] Prompt Rewrite: Disable per PM recommendation (Sandhya) (#5651)

Oct 8 1:47pm
`0.0.1-main.9677-commit=95309a35`
ENVIRONMENTS:

1.  Dev - gen-video [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/)

CHANGE LOG:

1.  No gen-video related change. Doing a redeploy to flush out old nodes.

```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/thinz/colligo/contrib/Mori/eval_sentences_morgan.txt --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/baseline_evalEndPoint_11-08-24_2 --width 1280 --height 720 --num_frames 128  --seeds "0" --save_fps 24 --overwrite True --limit_prompts 100 --fix_seeds
```

T2v from morgan: `/sensei-fs/users/thinz/colligo/contrib/Mori/eval_sentences_morgan.txt`

1.  8/30: switch to old 3DVAE decoder, cfg fix for I2V, warped timesteps, default negative prompt for TI2V, TRT support for TI2V
2.  9/4: make TRT default
3.  9/5: TRT inference improvements
4.  9/6: make torch default for decoder
5.  9/24: turn off AOT decoder (use torch), switch to 814K checkpoint
6.  9/25: update sampling to reduce confetti
7.  9/27: turn on aot
8.  9/28: FP8 for TI2V
9.  9/30: update avoid prompt

Sep 24: T2V, before sampling param changes, no prompty, 814k-32n-TRT, H100
[http://clio.corp.adobe.com/model\_evaluation//mnt/localssd/temp/siddhantg/t2v\_morgan\_prompts\_no\_prompty\_sep\_24\_1815hrs/t2v.html](http://clio.corp.adobe.com/model_evaluation//mnt/localssd/temp/siddhantg/t2v_morgan_prompts_no_prompty_sep_24_1815hrs/t2v.html)
Sep 26: T2V, after sampling param changes, no prompty, 814k-32n-TRT, H100
[http://clio.corp.adobe.com/model\_evaluation//home/sannavajjala/morgan\_sampling\_no\_prompty\_t2v/t2v.html](http://clio.corp.adobe.com/model_evaluation//home/sannavajjala/morgan_sampling_no_prompty_t2v/t2v.html)
Sep 27: T2V, after sampling parameter change, with prompty, H100
First row (baseline) 814k-32n-TRT BF16,
Second row FP8 baseline
[http://clio.corp.adobe.com/files/merged\_content\_2024-09-27-15-38-48-15d293c0f4\_md5\_62ee4157d877d45b4d804092cbaec2d2.html](http://clio.corp.adobe.com/files/merged_content_2024-09-27-15-38-48-15d293c0f4_md5_62ee4157d877d45b4d804092cbaec2d2.html)

Today's production (not morgan prompts)
[https://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/baseline\_evalEndPoint\_11-08-24\_1/t2v.html](https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/baseline_evalEndPoint_11-08-24_1/t2v.html)

Today's production as is(morgan prompts)
[https://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/baseline\_evalEndPoint\_11-08-24\_2/t2v.html](https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/baseline_evalEndPoint_11-08-24_2/t2v.html)

Todays production Torch DiT:
```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/thinz/colligo/contrib/Mori/eval_sentences_morgan.txt --endpoint http://localhost:8000 --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/torchDiT_evalEndPoint_11-08-24_3 --width 1280 --height 720 --num_frames 128  --seeds "0" --save_fps 24 --overwrite True --limit_prompts 100 --fix_seeds
```

Wrong
[https://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/torchDiT\_evalEndPoint\_11-08-24\_2/t2v.html](https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/torchDiT_evalEndPoint_11-08-24_2/t2v.html)

[https://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/torchDiT\_evalEndPoint\_11-08-24\_3/t2v.html](https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/torchDiT_evalEndPoint_11-08-24_3/t2v.html)

```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/hshariati/del/clineto/text2video_bite_size.txt --endpoint [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/evalBiteSize_evalEndPoint_11-08-24_1 --width 1280 --height 720 --num_frames 128  --seeds "0" --save_fps 24 --overwrite True --limit_prompts 100 --fix_seeds
```

`/sensei-fs/users/hshariati/del/clineto/text2video_bite_size.txt`

[https://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/evalBiteSize\_evalEndPoint\_11-08-24\_1/t2v.html](https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/evalBiteSize_evalEndPoint_11-08-24_1/t2v.html)

```python
python generate_html_from_inputs.py
--input_file /sensei-fs/users/hshariati/del/clineto/text2video_bite_size.txt --endpoint  http://localhost:8000 --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/evalBiteSize_740k_torch_evalEndPoint_11-08-24_1 --width 1280 --height 720 --num_frames 128  --seeds "0" --save_fps 24 --overwrite True --limit_prompts 100 --fix_seeds
```

[https://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/evalBiteSize\_740k\_torch\_evalEndPoint\_11-08-24\_1/t2v.html](https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/evalBiteSize_740k_torch_evalEndPoint_11-08-24_1/t2v.html)

Everything off morgan:
```python
python generate_html_from_inputs.py --input_file /sensei-fs/users/thinz/colligo/contrib/Mori/eval_sentences_morgan.txt --endpoint http://localhost:8000 --task t2v --save_to /sensei-fs/users/hshariati/del/clineto/html/torch814k_noAot_noPrompty_noNSFW_11-09-24_3 --width 1280 --height 720 --num_frames 128  --seeds "0" --save_fps 24 --overwrite True --limit_prompts 100 --fix_seeds
```

[https://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/torch814k\_noAot\_noPrompty\_noNSFW\_11-09-24\_3/t2v.html](https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/torch814k_noAot_noPrompty_noNSFW_11-09-24_3/t2v.html)

[https://s3.us-west-2.amazonaws.com/clio.corp.adobe.com/files/merged\_content\_2024-10-09-20-32-45-9858da9f5b\_md5\_f64c856e10a77ce6e9fc7afabc0c8b88.html/.](https://s3.us-west-2.amazonaws.com/clio.corp.adobe.com/files/merged_content_2024-10-09-20-32-45-9858da9f5b_md5_f64c856e10a77ce6e9fc7afabc0c8b88.html/),[http://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/baseline\_evalEndPoint\_11-08-24\_2/ab0757bf-8f3e-4d75-bf97-91000a658bd2.mp4](http://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/baseline_evalEndPoint_11-08-24_2/ab0757bf-8f3e-4d75-bf97-91000a658bd2.mp4)

Yeah that part I'm aware of. I made a change so they don't need to worry about format E.g., A cat and a dog fighting outdoors, camera pan right will be interpreted as A cat and a dog fighting outdoors + "& {camera pan right}"

I realize the problem tho. They're using classes that don't exist.

For example, shot angle eye-level is not a class. It has to be "eye-level shot" Like in row 17 or row 22.

"camera random" is not a class

It's "camera handheld" not "camera hand held"

No ", shot size random." class

Abstract blue marble texture with gold splashes, blue luxury background while the camera moves in for a close-up at the climax of the action.

Put htmls in a canvas.

Figure out with Eval connect at IC level.
Figure out the charter for us meet with Ratheesh (what we wanna own)

10. 8/29: 740K checkpoint
11. 8/30: switch to old 3DVAE decoder, cfg fix for I2V, warped timesteps, default negative prompt for TI2V, TRT support for TI2V
12. 9/4: make TRT default
13. 9/5: TRT inference improvements
14. 9/6: make torch default for decoder
15. 9/18: disable debiasing for I2V
16. 9/23: fix timestep split for I2V
17. 9/24: turn off AOT decoder (use torch), switch to 814K checkpoint
18. 9/25: update sampling to reduce confetti
19. 9/27: turn on aot
20. 9/28: FP8 for TI2V
21. 9/30: update avoid prompt
22. 10/3: add A1 to I2V

All on vs all off: small
[https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/for\_liorae43edc1793d4cf4af1fbea3aa066b3b\_md5\_86ed8465e6db1214f1ee7ef4b949f8be.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/for_liorae43edc1793d4cf4af1fbea3aa066b3b_md5_86ed8465e6db1214f1ee7ef4b949f8be.html)

large
[http://clio.corp.adobe.com/files/merged\_content\_2024-10-09-20-32-45-9858da9f5b\_md5\_f64c856e10a77ce6e9fc7afabc0c8b88.html](http://clio.corp.adobe.com/files/merged_content_2024-10-09-20-32-45-9858da9f5b_md5_f64c856e10a77ce6e9fc7afabc0c8b88.html)

Sep 24: T2V, before sampling param changes, no prompty, 814k-32n-TRT, H100
[http://clio.corp.adobe.com/model\_evaluation//mnt/localssd/temp/siddhantg/t2v\_morgan\_prompts\_no\_prompty\_sep\_24\_1815hrs/t2v.html](http://clio.corp.adobe.com/model_evaluation//mnt/localssd/temp/siddhantg/t2v_morgan_prompts_no_prompty_sep_24_1815hrs/t2v.html)
Sep 26: T2V, after sampling param changes, no prompty, 814k-32n-TRT, H100
[http://clio.corp.adobe.com/model\_evaluation//home/sannavajjala/morgan\_sampling\_no\_prompty\_t2v/t2v.html](http://clio.corp.adobe.com/model_evaluation//home/sannavajjala/morgan_sampling_no_prompty_t2v/t2v.html)
Sep 27: T2V, after sampling parameter change, with prompty, H100
First row (baseline) 814k-32n-TRT BF16,
Second row FP8 baseline
[http://clio.corp.adobe.com/files/merged\_content\_2024-09-27-15-38-48-15d293c0f4\_md5\_62ee4157d877d45b4d804092cbaec2d2.html](http://clio.corp.adobe.com/files/merged_content_2024-09-27-15-38-48-15d293c0f4_md5_62ee4157d877d45b4d804092cbaec2d2.html)

@thinz @kalarot On the few prompts from the eval set that was shared from the slides 740k ckpt works better than 814k. I know @lshapira said not to run on old ckpt. But the slides were comparing us to the old ckpt. HTMLS: Production pipeline (Dentro, NSFW, sampling params) but torch DiT (for both 740k and 814k ckpts)
740k
814k
9:49

in here: [https://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/hshariati/del/clineto/html/evalBiteSize\_evalEndPoint\_11-08-24\_1/t2v.html](https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/hshariati/del/clineto/html/evalBiteSize_evalEndPoint_11-08-24_1/t2v.html)

**gpal of min inf is to increase the productivity of model developers
Add a point to the hand off that
** everything in prod pipelines will be represented by min inf but not the other way around

SOHEIL:

1.  We gave him a platform to talk so that he endorses min inf
2.  Is there a reason he's not doing it
3.  ASML is all behind min inf. + Rajan (he is onboard)
4.  Last time I gave feedback on Xij the sentiment was maybe hes protecting his job sec
5.  After what he did with Decoder, assumption was that he's doing it because of job security too
6.  Modelers spend 1 day to build min inf, and they realized results they get is different, and instead of chasing parity themselves they re
    Recruited xijec. This is now on Xiaj
7.  Sentiment is that Lyn and Soheil are the people who don't want self serve to happen because they want to protect their job security
8.  Xiaj messed with the process and he's under the bus too.

XIAJEN

1.  Lior, rajan, are all on board.
2.  Modelers spend 1 day to build min inf, and they realized results they get is different, and instead of chasing parity themselves they re
    Recruited xijec. This is now on Xiaj
3.  The consensus is that Xiaj is trying to stop self serve from happening

RAJAN

1.  We build min inf for self serve, and soheil and xiajen are the only people not using it.

TOBAIS

1.  Need to get tobais on board.

42: [https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_123e75fdd36fcc0d44086188ccf79fc7.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_123e75fdd36fcc0d44086188ccf79fc7.html)
40: [https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_16224723d88995b50706483563cdb256.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_16224723d88995b50706483563cdb256.html)
38: [https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_b4dfb252e0e8214e01766575579a2986.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_b4dfb252e0e8214e01766575579a2986.html)
36: [https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_e1854c2fa5bd41156d4d5a86be3f3251.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_e1854c2fa5bd41156d4d5a86be3f3251.html)
34: [https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_678f50af76332e259c2cec1f819f5fa6.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_678f50af76332e259c2cec1f819f5fa6.html)
32: [https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_2c65620936ed7552d194b8a340b05eae.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_2c65620936ed7552d194b8a340b05eae.html)
[https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_ac871b9ccb29ce914e7a1b4c35f6c610.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_ac871b9ccb29ce914e7a1b4c35f6c610.html)

[https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_ac871b9ccb29ce914e7a1b4c35f6c610.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_ac871b9ccb29ce914e7a1b4c35f6c610.html),[https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_2c65620936ed7552d194b8a340b05eae.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_2c65620936ed7552d194b8a340b05eae.html),[https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_678f50af76332e259c2cec1f819f5fa6.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_678f50af76332e259c2cec1f819f5fa6.html),[https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_e1854c2fa5bd41156d4d5a86be3f3251.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_e1854c2fa5bd41156d4d5a86be3f3251.html),[https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_b4dfb252e0e8214e01766575579a2986.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_b4dfb252e0e8214e01766575579a2986.html),[https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_16224723d88995b50706483563cdb256.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_16224723d88995b50706483563cdb256.html),[https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded\_videos\_md5\_123e75fdd36fcc0d44086188ccf79fc7.html](https://s3.us-west-2.amazonaws.com/kalarot-clio-data/files/reencoded_videos_md5_123e75fdd36fcc0d44086188ccf79fc7.html)

Original,CRF-32,CRF-34,CRF-36,CRF-38,CRF-40,CRF-42

```python
python minimal_v2v.py --video_path /sensei-fs/users/lakshya/video_gen/Data/bug_reports/flickering_bug/_videos/DJI_0514.mov  --save_to /mnt/localssd/hshariati/colligo/colligo_output.mp4 --width_latent 120 --height_latent 68 --num_frames 20 --n_channels 12
```

--Set the context (agenda)
-- Have arpit describe how the current integration works
--exploration and production are two different goals
--stability vs exploration.
--In deployment we need to take care of a lot of things (libs, sensei paths, missing libs) example from Dentro.
Background threads. And Asunc processing.
--Legal won't allow us to disable prompty, NSFW, etc. Distribution of prompt is different.
Load testing, CPU utilization tooling. If we take all this into account for each experiment it'll take a lot of time.
--Deployability + release block

--Hooman goes over motivation, and features of min inference.
--Start by saying this is not another production pipeline.
And putting things there does not mean integration.
Why is it different than inf app.
--Current production paint point.

--Adiyta starts with the details.

--Features to come. AutoX.
Improve dev experience. Autogen during training, auto eval during training.
--MoriX doesn't come with any of the prod optimizations such as AOT, FP8, TRT

`firefly_clineto -> s3://colligo-dev-pr/deploy_v2/colligo-rhode/firefly_clineto/firefly_clineto-version=0.0.1-custom-commit=50af4b61.sh`

Run Id for T2V: runid
`'[FFP-23567]t2v-baseline_t2v-regression-bitesized_1731017771'`

Oct 23: 1650 (deposit)
Oct 28: 3300

Dec 01: 3300

Jan 01: 3300
Feb 01: 3300
Mar 01: missed
Mar 08: 3300 (should have been Mar 01)

Mar 30: 635
Mar 31: 2700
3335
Apr 01: missed (missing 3300)

May 01: missed
May 04: 500
May 07: 500
May 22: 1000
May 22: 300
2300 (missing 1000)

June 01: 2000
June 05: 1300
3300

July 01: 1750
July 12: 700
July 26: 500
2950 (missing 350)

Aug 01: 350
Aug 01: 500
Aug 03: 800
Aug 09: 800
2450 (missing 850)

Sep 06: 1300 (missing 2000)

Oct 01: 0 (missing 3300)

Nov 01: 0 (missing 3300/30 \* 3 = 330 )

Total missing: 11130
Deposit: 1650 + Last month 3300 = 4950
Tenant owes: 11130 - 4950 = 6180

`/sensei-fs/users/sannavajjala/dump/v2v_sseval_baseline/v2v_baseline_stitched.csv`

[https://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/sannavajjala/dump/v2v\_sseval\_baseline/stitched//stitched.html](https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/sannavajjala/dump/v2v_sseval_baseline/stitched//stitched.html)

`/sensei-fs/users/sannavajjala/dump/sseval_ref_decoder/v2v_refdecoder_stitched.csv`

[https://clio.corp.adobe.com/model\_evaluation//sensei-fs/users/sannavajjala/dump/v2v\_sseval\_refdecoder/stitched//stitched.html](https://clio.corp.adobe.com/model_evaluation//sensei-fs/users/sannavajjala/dump/v2v_sseval_refdecoder/stitched//stitched.html)

[https://clio.corp.adobe.com//colligo-dev-artifacts/artifacts-v1/vae3d/epoch=0-step=125000\_vqgan.2024-09-03.17-53.b8eb9.ckp](https://clio.corp.adobe.com//colligo-dev-artifacts/artifacts-v1/vae3d/epoch=0-step=125000_vqgan.2024-09-03.17-53.b8eb9.ckp)

`/mnt/localssd/hshariati/colligo/contrib/AdobeDiffusion/cliocore/core_models/latent_transformers/src/clio/core_models/latent_transformers/filix2_t2x_ediffi_prod.py`

```python
vae3d_output = await decoder_component.call(
    Vae3dDecoderComponentInput(
        model_name=config.decoder_model_name,
        latent=frames_to_decode_t,
        frame_params=VAE3DFrameParams(
            image_chunk_input_num_frames=16,
            image_chunk_output_num_frames=1,
            video_chunk_input_num_frames=16,
            video_chunk_output_num_frames=16,
        ),
        ref_frames=ref_frames,
        extend_forward=config.extend_forward,
        decoder_prefix_chunk=config.decoder_prefix_chunk,
    )
)
decoded_frames_hs = vae3d_output.images
```

`filix2_t2v_prod1_814k32n_trt` (3 -> 0)
`filix2_t2v_prod1_540p_winattn`: (5 ->0)

4

Update ckpt

Did we train the red-decoder-v2 with the objective of working with the previous frame.
`filix2_t2v_prod2_540p_winattn`
`ref_decoder_v2_aot`
`t5_v2_256_torch`
`internvl_4b_v1`
`ssr`
`nsfw_adobe_one`
`vae3d_prod_2`

```python
+        torch.save(hs_temp_t5_text_embedding, "/sensei-fs/users/hshariati/del/clineto/latents_for_mamshad.pt")
```

1.  Lead VIQ (Video Inference Quality) squad which delivered Clineto's production pipelines for T2V, I2V, V2V (GenExtend), and Guided Transform in a way that ensured ASML's work gets presented in the best light from quality and user experience perspectives, and every single deadline is met. We received feedback that our deliveries to this year's MAX were among the most smooth operations ever.
2.  Lead the effort in creating and evangelizing Min Inference Scripts. These are lower bar pipelines that allow modelers and researchers access to production components without the complexities arising from production requirements. Following our presentation of Min Inference to ASML and Colligo, we have seen a wide adaptation and have supported many individuals in using Min Inference to find out how their models/ideas will look like in production. As a part of this effort, we also built a large number of tools for HTMLs generation and distributed batch processing that extend the current capabilities (increased GPU utilization, distributed processing over many runAi nodes, resume functionality for crashed jobs, modeler friendly interface, etc). Our tools are currently used by many teams inside and outside of ASML.
3.  Lead the effort in training auto evaluation to monitor the quality of the models during training. We have created a self-serve infrastructure for modelers to use this service and we have integrated several metrics including LLM based solutions (Dentro). This is an ongoing effort which will result in us maintaining a catalogue of all quality issues observed in our models, examples for each issues, ways to detect them, and potential mitigation strategies.
4.  Made sure that quality from production doesn't fall out of parity with research prototypes and there is accountability and record keeping of every change that affected our baselines. I did this by continuously monitoring the changes going into the pipeline and making sure that every change comes with before/after HTMLs measuring quality. Every time, a pixel change was observed I ensured that PMs, execs, and modelers are all aware and approve the changes. Also built tooling for our team to gain access to the new eval hub. We completed approximately 2 SSEval studies every week and are keeping a running record of our models progression (based on SSEval) over time. Grant Pass Oragan

```python
self.eps_model.append(instantiate_from_config(training_config.model.params.denoiser_config))

from mori.training.utils.config_utils import (
    instantiate_from_config,
)
```

:35 PM - 4:30 PM

Enable people to do it themselves. Make it easy, and teach them how to do it. `/mnt/localssd/hshariati/colligo/.venvs/dev/bin/python -m colligo.rhode.commands.dev_supervisor --spec firefly_clineto --locust --replicas filix2_t2v_prod1_540p_winattn_trt 3`

Talk to Juwen on Sequence Parallel.
```python
FILIX2_T2V_PROD1_8_540P_1_CKPT = build.s3_source(
    bucket="s3://colligo-dev-artifacts/artifacts-v1",
    key="slimmed_ckpt/ckpt_step01254000_slimmed.2025-02-10.17-32.a7010.pth",
    version_id="Z_mFGcQzzZwExtQIaLM6EHEKu2WuNoWj",
    sha256="a7010868e325178afa919520f6de89a54eac193a629bb87f2e9ac8a6e266bd44",
)
```

Change 17 to 33

`torch.Size([1, 17, 64, 68, 120])`

16 for dev
8 for demos
8 for training CME

Follow up with variable lengths for FPS with Zhengang. 2/20 on stage?

Can we give 2/24 Gen Extend in stage? What about quality ?
2/20:
GenExtend latest v1.8
SSR issue
Gamma shift issue
17 frames of original being returned
Follow up on variable num frames. (Model supports it, but we need to enable in the pipeline (1.3 to 4.6 s))
(VAE 10):
Arch changes for DiT

2/21
A branch merged to main where T2V, V2V, I2V, GT work with any model
Will look like T2V, V2V come from V1.8
I2V ang GT come form V1.5

```python
FILIX2_T2V_PROD1_8_540P_1_CKPT = build.s3_source(
    bucket="s3://colligo-dev-artifacts/artifacts-v1",
    key="slimmed_ckpt/ckpt_step01372000_slimmed.2025-02-25.18-38.09e44.pth",
    version_id="sNOE_U1mePXmUsYTj44y04hfQfsENjHL",
    sha256="09e44831501ac50e5068e40205a4639b248e2bd8450899e6b2350f6e3fcce2a9",
)
```

`/sensei-fs/pr/sensei-fs/projects/firefly/clineto/autoX/data_log/sannavajjala/lakshya-clineto-v1.8-test-0226/ckpt_1368000/1080p-vid-byte-sized-eval/job_0/video_eval_bytesized/02-26-2025_13-51-37/video_eval_bytesized.csv`

1.  Increase integration velocity. **This impacts Adobe business by reducing the time between a model being trained and it becoming available in production.** I am planning to speed up integration through:
    A. Training/Educating ASML modelers to take a more active role in integration. Currently, integration is done completely by VIQ squad and is limited by the bandwidth of our members.
    B. Refactoring the production pipeline to make integration easier. The idea here is to structure the current production pipeline to separate the portion that is relevant to modelers from portions that are production focus. For example, modelers shouldn't know the details of NSFW/input pre-processing and should work with code that only receives Tensors and literals.
    C. Reducing the scope of integration by using as much of Mori as we safely can. We already did a lot of work last quarter to make sure Mori and Colligo use the same diffusion loop. This effort could be extended to sharing utility functions between Colligo and Mori as well. This is a big task, but the more we make progress on it, the easier integration becomes.
    D. Establishing integration best practices. This includes documented protocols for parity matching, ensuring deployability, and adequate integration tests to ensure we don't regress or break other tasks in the pipeline. For example, we previously, we built "minimal inference" infrastructure to allow for modelers to pass us quality and latency benchmarks that we can actually aim for (as opposed to reporting numbers from their research prototype that will not be achievable in production). Now, we are moving on to how to investigate and fix lack of parity.
2.  Improve the automatic evaluations during training. **This impacts Adobe business by catching quality issues earlier in the training cycle which will reduce over all training costs by avoiding wasted iterations.** I am planning to achieve this through:
    A. Curating the eval sets that we run on a higher frequency during training (bite sizes) to focus on issues that we have historically seen. I'm also planning to have a better break-down of these (with better reporting) so that instead of looking at 100 prompts in one set without realizing what each one of them focus on. We will have several smaller sets each focusing on a specific issue. I will also work on increasing our test set coverage since there are several areas that we don't have eval sets for.
    B. Enforcing eval cadence on larger evaluations. Previously, we would run these after the integration into production pipeline. This leads to a lot of last minute fixes. I'm planning to run these larger scale evals several times during training (but at lower frequency than bite size sets). I will work with modelers to agree on proper mile stones for when these generations/evaluations should happen.
    C. Regularly running human annotations and informing everyone of the results. Human annotations are not the most reliable but they have a role in identifying areas of concern. I'm planning to publish weekly results during production training to keep everyone motivated and focused.
3.  Improve usability and adoptability of Kaizen. **This will reduce model development costs by providing a consistent historical view of how quality/runtime/learning evolves across the many experiments that different teams run.** This includes two parts:
    A. Adding new evaluation metrics to Kaizen. This includes both implementing metrics that are requested/found by others as well researching and coming up with new metrics for problem that we see in our models.
    B. Integrating Kaizen with new workflows and systems. We'd like to bring Kaizen to every team in ASML (imaging, prompty, vae, ssr, etc) but also to other teams such as audio, and research. We'd like to also integrate Kaizen in existing systems. For example, integrating with eval hub will give modelers access to more auto evaluators that they can use during training. We are also working on making it easier for users to submit their Kaizen results for human annotation.
    C. Adding new features (as requested by users). For example, we have received requests to add a global experiment view to Kaizen. This will help each team to have a historical understanding of all the experiments they have done and how their results have evolved on different metrics.
    Prompt: "a beautiful horse in a field of grass"
    Neg\_prompt: 'cartoon, vector art, & bad aesthetics & poor aesthetic'
    "videoSettings": {
    "cameraMotion": "camera tilt down",
    "shotAngle": "aerial shot",
    "shotSize": "close-up shot",
    "promptStyle": "cinematic"
    },

Appended prompt: 'in cinematic style & a beautiful horse in a field of grass & camera tilt down & camera tilt down & aerial shot & aerial shot & close-up shot & close-up shot & in cinematic style'

Appended neg\_prompt: 'illustration, art, text, low quality, ugly'


python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net --input_file /sensei-fs/users/hshariati/eval_sets/structure_match_tv/v2v_transformVideo_311.csv --save_to /sensei-fs/users/hshariati/del/clineto/html/v1.8_1376ckpt_tv_bitesize_1080p_04-09-25_del --overwrite --task structure_match --seeds 24 --num_frames 121  --num_jobs 1 --width 1920 --height 1080 --n_jobs 1 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}'

python /sensei-fs/users/hshariati/hs_scripts/upload_to_eval_hub.py --jira FFP-37517_clineto1.8 --csv_paths /sensei-fs/users/hshariati/del/clineto/html/v1.8_prod_t2v_motion_1080p_04-25-24/t2v_final_2025_04_11_20:22.csv --eval_set motion --eval_set_version 0.0 --task t2v --link_to_eval false


python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net --input_file /sensei-fs/users/hshariati/eval_sets/t2v/t2vid_general_100.csv --overwrite --task t2v --seeds 24 --num_frames 121  --num_jobs 1 --width 540 --height 540 --n_jobs 1 --limit_prompts 2 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}' --initiative "test_init" --experiment "test_exp" --save_to /sensei-fs/users/hshariati/del/clineto/html/delete_102 --ckpt "509k";python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net --input_file /sensei-fs/users/hshariati/eval_sets/t2v/t2vid_general_100.csv --overwrite --task t2v --seeds 24 --num_frames 121  --num_jobs 1 --width 540 --height 540 --n_jobs 1 --limit_prompts 2 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}' --initiative "test_init" --experiment "test_exp" --save_to /sensei-fs/users/hshariati/del/clineto/html/delete_101 --ckpt "510k";python models/colligo/models/firefly/pipelines/clineto/tests/utils/colligo2html.py --endpoint https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net --input_file /sensei-fs/users/hshariati/eval_sets/t2v/t2vid_general_100.csv --overwrite --task t2v --seeds 24 --num_frames 121  --num_jobs 1 --width 540 --height 540 --n_jobs 1 --limit_prompts 2 --debug_params '{ "enable_dentro_post": false, "enable_video_nsfw_only": false, "disable_nsfw": true, "enable_dentro": false, "enable_dentro_pre": false}' --initiative "test_init" --experiment "test_exp" --save_to /sensei-fs/users/hshariati/del/clineto/html/delete_100 --ckpt "511k"



## SSIM scores for structure match parity check 05/30/2025
SSIM between boy_stage_all_remote.mp4 and boy_baseline_from_gunjan.mp4: 0.679215
SSIM between boy_baseline_from_gunjan.mp4 and boy_baseline_from_gunjan.mp4: 1.0
SSIM between boy_by_us_from_gunjan_branch.mp4 and boy_baseline_from_gunjan.mp4: 0.679215
SSIM between boy_stage_dit_enc_local.mp4 and boy_baseline_from_gunjan.mp4: 0.679215


SSIM between owl_baseline_from_gunjan.mp4 and owl_baseline_from_gunjan.mp4: 1.0
SSIM between owl_by_us_from_gunjan_branch.mp4 and owl_baseline_from_gunjan.mp4: 0.595337
SSIM between owl_stage_all_remote.mp4 and owl_baseline_from_gunjan.mp4: 0.608504
SSIM between owl_stage_dit_enc_local.mp4 and owl_baseline_from_gunjan.mp4: 0.600116


SSIM between owl_by_us_from_gunjan_branch.mp4 and owl_by_us_from_gunjan_branch.mp4: 1.0
SSIM between owl_stage_all_remote.mp4 and owl_by_us_from_gunjan_branch.mp4: 0.658186
SSIM between owl_stage_dit_enc_local.mp4 and owl_by_us_from_gunjan_branch.mp4: 0.643984
SSIM between owl_baseline_from_gunjan.mp4 and owl_by_us_from_gunjan_branch.mp4: 0.595337


SSIM between boy_stage_all_remote.mp4 and boy_by_us_from_gunjan_branch.mp4: 1.0
SSIM between boy_baseline_from_gunjan.mp4 and boy_by_us_from_gunjan_branch.mp4: 0.679215
SSIM between boy_by_us_from_gunjan_branch.mp4 and boy_by_us_from_gunjan_branch.mp4: 1.0



SSIM between owl_by_us_from_gunjan_branch.mp4 and owl_by_us_from_gunjan_branch.mp4: 1.0
SSIM between owl_stage_all_remote.mp4 and owl_by_us_from_gunjan_branch.mp4: 0.658186

SSIM between owl_baseline_from_gunjan.mp4 and owl_by_us_from_gunjan_branch.mp4: 0.595337


SSIM between owl_by_us_from_gunjan_branch.mp4 and owl_stage_dit_enc_local.mp4: 0.643984

SSIM between owl_stage_dit_enc_local.mp4 and owl_stage_dit_enc_local.mp4: 1.0
SSIM between owl_baseline_from_gunjan.mp4 and owl_stage_dit_enc_local.mp4: 0.600116


SSIM between owl_stage_all_remote.mp4 and owl_stage_dit_enc_local.mp4: 0.820942 (will repeat)
SSIM between boy_stage_dit_enc_local.mp4 and boy_by_us_from_gunjan_branch.mp4: 1.0
SSIM between owl_stage_dit_enc_local.mp4 and owl_by_us_from_gunjan_branch.mp4: 0.643984 (will repeat)

SSIM between boy_stage_dit_enc_local.mp4 and boy_baseline_from_gunjan.mp4: 0.679215