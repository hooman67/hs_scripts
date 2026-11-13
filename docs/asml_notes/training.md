```markdown
## Training Image Models of DiT

Start a runai machine with this docker:
A100: `docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/kineto:0.0.16-rc4`
H100: `docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/kineto:0.0.16-h100-squashed-test7`

1.  Then, go to AD, Dev branch.
2.  `export ARTIFACTORY_UW2_USER=<your_username> export ARTIFACTORY_UW2_API_TOKEN=<your_api_token>`
3.  `./activate_dev_basemodels.sh`
4.  `pip install -e ./train/`
5.  `pip install -e ../../piat`
6.  `pip install -e ../../streaming`
7.  `export WANDB_API_KEY=local-5d401450c511c7a7d16ffae17fc1aa71da24ff8c`
    * Follow this wiki essentially: [Tracking a training job on WandB](https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=GenAI&title=Tracking+a+training+job+on+WandB) [cite: 2]
8.  Create a wandb config:
    * `train/cliotrain/wandb_config.yaml.template train/cliotrain/wandb_config.yaml` [cite: 2]
    * Edit it [cite: 3]
9.  `python3 -m cliotrain.train --config train/configs/dit_configs/dit_t2i_small_base.yaml --name debug --gpus 8 --logdir ./logs/ --use_wandb true --wandb_project asml-debugging` [cite: 3]

**The first 50 iters are benchmarking so they're slower.** In the config you can turn this on/off[cite: 4].
**All the logs, checkpoints etc will be in `--logir ./logs/`**[cite: 4].
**It will tell you where in wandb to monitor stuff.** [cite: 4]
**You can also use tensorboard. You can run tensorboard on your devbox and pass it the location to the tensorboard event file.** [cite: 5]

## Notes on Efficiency

### First meeting with Naveen

#### Profiling

His suggestion was to profile the runtime / computation of the training job with pytorch profiler: [pytorch profiler](https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html)[cite: 6]. Then focus on the bottle necks[cite: 6].

#### Activation Checkpointing

For improving memory (at a cost of more compute) you can use activation checkpointing[cite: 7]. This involves deleting the gradients of the layers you have passed through (or saving them to disk?) in the forward pass to reduce memory[cite: 8]. In the backward pass, then you can re-calculate the gradient (or load it from disk)[cite: 9]. This reduces memory usage but increases compute (runtime)[cite: 10].

In adobe diffusion: [Activation Checkpointing in Adobe Diffusion](https://github.com/Adobe-Firefly/AdobeDiffusion/blob/48dfe5d2906f95a3ce2411c7d990023210af9826/train/cliotrain/train.py#L748)[cite: 10].

You can try it with this config: [Activation Checkpointing Config](https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/b2e8f61e24d4b510f8966e238dd4e415352a4c58/train/configs/text_to_image/clio_v2/clio2_old_configs/clio2_L78_64px_config_mds.yaml#L4-L5)[cite: 10].

### Optimizer state sharding (fstp) = fully sharded data parallelism

This method helps with compute[cite: 11]. They use fstp for this right now. You can use it by setting this config: [FSTP Config](https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/b2e8f61e24d4b510f8966e238dd4e415352a4c58/train/configs/text_to_image/clio_v2/clio2_old_configs/clio2_L78_64px_config_mds.yaml#L209)[cite: 11].

This is I'ts usage in `train.py`: [FSTP Usage in train.py](https://github.com/Adobe-Firefly/AdobeDiffusion/blob/48dfe5d2906f95a3ce2411c7d990023210af9826/train/cliotrain/train.py#L661)[cite: 11].

This ZeRo optimizer from deepspeed does the same thing too: [DeepSpeed ZeRo Optimizer](https://www.deepspeed.ai/tutorials/zero/)[cite: 11]. [DeepSpeed ZeRo3](https://deepspeed.readthedocs.io/en/latest/zero3.html)[cite: 11].

### Tensor Parallelization

According to Naveen this helps mostly with wide networks[cite: 12]. Not with the deep networks that we're using right now[cite: 12].

#### Colossal AI

They do the different parallelizations: [ColossalAI Parallelism Paradigms](https://colossalai.org/docs/concepts/paradigms_of_parallelism)[cite: 13]. However, Queng told me that they don't support Pytorch Lightening which is what we use[cite: 13]. But Ratheesh sent me this page that says that they actually have an experimental feature with lightening: [ColossalAIStrategy with Lightning](https://lightning.ai/docs/pytorch/2.1.0/integrations/strategies/colossalai.html)[cite: 14].

So I'm gonna create a ticket to try it with DiT[cite: 15]. I have set up a meeting with Kevin to onboard me with it. But apparently, Qiang has already tried this[cite: 15].

If you are interested, you can also dive more deep with the webpage: [ColossalAIStrategy with Lightning](https://lightning.ai/docs/pytorch/2.1.0/integrations/strategies/colossalai.html)[cite: 16]. Maybe my observation (the lightning feature for colossal AI strategy does not contain sequence parallelism) is wrong[cite: 16].
Another possibility is, although there is no sequence parallelism, lightning for colossal contains some other techs such as model parallelism, which can also make our sequence length reach 100k, then that is what we would like to see[cite: 16]. But this is waiting to be confirmed and you can dive deep, this will not lead to duplicate work[cite: 17].

### NeMo from Nvidia

This is another training efficiency framework that does work with pytorch lightening[cite: 17]. We Queng has created a ticket for me to evaluate it. And make a knowledge share[cite: 18].
```