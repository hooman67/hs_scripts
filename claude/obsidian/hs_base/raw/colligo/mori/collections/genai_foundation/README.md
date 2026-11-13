# Mori
A pure PyTorch framework for large-scale DiT text-to-image and text-to-video training.


## Submit Training Job

Please refer to Run.ai [wiki page](https://git.corp.adobe.com/pages/adobesensei/training-framework/runai/training.html) about how to use Run.ai to submit general training jobs.

To submit Mori trainnig jobs, copy and modify the Run.ai submission script `scripts/submit_runai.sh`:
- Basic info
    - `USER`: Your own LDAP.
    - `WANDB_API_KEY`: Your own WandB API key.
    - `JOB_NAME`: Run.ai job name. 
    - `EXP_NAME`: Folder name of the experiment.
    - `CONFIG`: Config file name under `train_pytorch/dit_train/configs`.
    - `EXP_ROOT`: Path to where the `EXP_NAME` folder will be created.
    - `REPO_FOLDER`: Path to your own AdobeDiffusion repo.

- Run.ai related
    - `RUNAI_PROJ`: Run name.
    - `RESEARCH_JACK_ID`: Please ask project manager or mentor about the jack id.
    - `NODE_POOL`: Look at the Run.ai dashboard for available pools.
    - In `submit-pytorch` command, add/modify labels in `-l` flag.

Run command, assuming the new script is named `submit_runai_new.sh`.
```bash
bash submit_runai_new.sh
```

### Automatic job status monitoring
To resolve the issue of the job getting stuck or killed due to unexpected errors,
you can enable the `MONITOR_JOBS` function in the submission script. In this way,
the script will launch a monitoring process that tracks the training progress, 
and if the training steps do not advance for a certain amount of time 
(default 1800 seconds), it will automatically delete the job and resumbit it.
For more details, please refer to `scripts/monitor_job.py`.

Some reminders:
1. To use this function, the submission script must be run on `Sensei` (instead of your local computer) since it needs
to access the training logging file. The best practice would be create a `devbox` and 
then submit the jobs there.
2. Set path to `RUNAI_BIN` `RUNAI_CONFIG` as specified in the submission script. 


## Run Training in Run.ai interactive mode (beta)
Please refer to Run.ai [wiki page](https://git.corp.adobe.com/pages/adobesensei/training-framework/runai/interactive.html) about how to use Run.ai to submit interactive jobs.


When creating interactive jobs, make sure to toggle on Jupyter Notebook and use the proper docker image
```
docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/dit-cuda12.4-pytorch2.3:v4
```

Once you succesfully access the terminal of the interactive job, set `WANDB_API_KEY`, `USER` and `HOME` environment variables.
```bash
export WANDB_API_KEY=<YOUR_WANDB_API_KEY>
export USER=<YOUR_LDAP>
export HOME=/home/$USER
```

Install required packages.
```bash
cd ./scripts/base_scripts
bash ./setup_env.sh
```

Run training, assuming 8 GPUs.
```bash
torchrun --nnodes=1 --nproc_per_node=8 ./src/dit_train/train.py \
    --config <CONFIG_PATH> \
    --logdir <LOG_DIR> \
    --wandb-project <WANDB_PROJECT_NAME> \
    --wandb-run-name <WANDB_RUN_NAME>
```


## Local Inference

Set checkpoint and output directory. For example (assume that you are in the `scripts/` foler):
```bash
CONFIG="../configs/filix_t2i_3B.yaml"
CKPT="/sensei-fs/projects/firefly/clio/training/logs/jianmzha/dit-filix-fuse-cosine-att-3b-0506/checkpoints/ckpt_step00300000.pth"
PROMPT_NAME="interesting"
PROMPT_PATH="../test_data/text_prompts/eval_sentences_interesting_drawbench.txt"
OUTDIR="<your_output_folder>"
```

Run inference with default configuraiton:
```bash
# python -m 
torchrun --nnodes=1 --nproc_per_node=4 \
--master_addr=127.0.0.1 --master_port=9998 \
../src/dit_train/app/sample_ediffi.py \
--config=$CONFIG \
--ckpt=$CKPT \
--outdir=$OUTDIR \
--prompt-name=$PROMPT_NAME \
--prompt-path=$PROMPT_PATH \
--eval-first-n=10
```

Run inference with advanced configuraiton:
```bash
torchrun --nnodes=1 --nproc_per_node=4 \
--master_addr=127.0.0.1 --master_port=9998 \
../src/dit_train/app/sample_ediffi.py \
--config=$CONFIG \
--ckpt=$CKPT \
--outdir=$OUTDIR \
--prompt-name=$PROMPT_NAME \
--prompt-path=$PROMPT_PATH \
--custom-neg-prompt=" & bad aesthetics  & poor aesthetics " \
--match-energy \
--format="png" \
--width=38 \
--height=26 \
--eval-first-n=10 \
--cfg-cutoff-t=20
```

## Submit Run.ai job for inference:
Copy and modify the Run.ai submission script `scripts/submit_runai_sample.sh`:
- `JOB_NAME`: Run.ai job name. 
- `EXP_NAME`: Folder name of the experiment.
- `EXP_ROOT`: Path to your exp log folder logs/.
- `OUT_DIR`: Output dir to save the inference results, results will be output to `OUT_DIR/EXP_NAME`. 
- `CKPT_NAME`: Name of the checkpoint. 
- `REPO_FOLDER`: Path to your own AdobeDiffusion repo.

Modify other arguments as needed.


## Reference
1. https://git.corp.adobe.com/wlin/ImprovedDiffusion