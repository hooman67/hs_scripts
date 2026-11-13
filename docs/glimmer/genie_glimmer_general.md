## For slack notifications
You can run this on any machine (I use a CPU box).
For channel id, look at the bottom of the channel details. But for me this complained that it couldn't find the channel.
```bash
glim_sqs notify \
    --queue-name hs_exploration_queue4 \
    --period-secs 10 \
    --user-ldap "hshariati"

glim_sqs notify \
    --queue-name hs_exploration_queue4 \
    --period-secs 10 \
    --channel-id "C09NN1KJZQR"
```

## finding out average receive count metric
this prints the average number of times we received each message.
it'll print the results and also put it on cloud watch. Does have 
some performance hit.
```bash
python -m enrichment.populate_sqs publish-receive-count-metrics \
  --queue-name hs_small_org \
  --sample-size 100 \
  --visibility-timeout 1 \
  --max-wait-seconds 0
```

to get just the stats
```bash
python /mnt/localssd/genie/enrichment/populate_sqs.py stats --queue-name hs_exploration_queue8 --region us-west-2
```


## to write to feature registry with S3 backend:
```bash
fr create -f /sensei-fs/users/hshariati/hs_scripts/glimmer/example_schema_for_feature_registry.yaml
```
**you should put the schema in your module folder.

Then you can put these in your config:
```bash
      writer:
        overwrite_mode: overwrite
        outputs:
          - feature_name: asml_image_qwen3_32B_captions
            primary_key: unique_id
            feature_version: 2025-10-23-0000
      # writer:
      #   outputs:
      #   - output_location: /mnt/localssd/hs_image_captioning/
      #   # - rendition: hs-vllm-test-new-glimmer
      #     extension: json
```
Look at /sensei-fs/users/hshariati/hs_scripts/glimmer/used_for_gen6_cap_sqs_2.yaml
for full example. 

if you wanna see the results locally:
run 
```bash
fr publish asml_image_gen6_qwen3_32B_captions_glimq_20251024 2025-10-23-0000
```
Then in an ipynb terminal run:
```bash
import feature_registry as fr
fr.get(feature_name="asml_image_qwen3_32B_captions", asset_id="5521dcc13ee899d30ef08dc5b09a8918")
```
You can get the asset id by going to 
DynamoDB on aws account (using klam), 
then go to Tables, click on your table name (asml_image_qwen3_32B_captions)
Then click on Explore items, and you can see your entries. 

***You also need
This change: https://github.com/Adobe-Firefly/genie/blob/main/glimmer/modules/common/vllm_async_module.py#L100-L107
I just commented out in the code but we should fix this later
```bash
        # Initialize writer
        # if self.use_fr:
        logger.info("using FRBaseWriter")
        self.writer = FRBaseWriter(**self.writer_init_args)
        # else:
        #     logger.info("using GlimmerWriter")
        #     self.writer = GlimmerWriter(**self.writer_init_args)
        self.writer.on_predict_start(self.trainer, self)
        logger.info("writer_initialized")
```

## Running glimmer 2.0 sqs Miray version 
local
```bash
python -m glimmer.inference --config glimmer/modules/adobeone/config.yaml --gpus 1 --test-mode
and  export AWS_SQS_NAME="hs_exploration_queue4"

export AWS_SQS_NAME="hs_exploration_queue4";
#hide GPUS to avoid cuda mem error
export RANK=0; export WORLD_SIZE=1; export CUDA_VISIBLE_DEVICES=""; export MASTER_ADDR=127.0.0.1; export MASTER_PORT=23456

python -m glimmer.inference --config /sensei-fs/users/hshariati/hs_scripts/glimmer/used_for_gen6_cap_sqs_2.yaml --gpus 0 --num-cpu-processes 32
```

### create and populate sqs
```bash
python glimmer/utilities/populate_sqs.py create \
  --table /sensei-fs/users/hshariati/hs_scripts/glimmer/used_for_gen6_cap_sqs_2.yaml \
  --queue-name hs_exploration_queue8 \
  --workers 16 \
  --batch-size 65536 \
  --row-group-size 100 \
  --add-deadletter
```



## Installing glimmer and genie (directly copied from docs) and for hs first sqs prototype
### for hshariati/enrichment_merge2main branch
```bash
cd /mnt/localssd/genie
uv venv --python 3.13
source .venv/bin/activate

export GENIE_SHORT_SHA=$(git rev-parse --short=7 HEAD)
uv pip install --prerelease=allow --index-strategy unsafe-best-match \
  --extra-index-url "https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-kineto-release/simple" \
  --extra-index-url "https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-piat-release/simple" \
  -e . "genie[glimmer,lint,dev]==1.0.0+$GENIE_SHORT_SHA"

uv pip install -e /mnt/localssd/ai-platform/frameworks/data/enrichment .
```

### for SQS before moving to its own repo
The only difference is that instead of glimmer we target glimmer-sqs.
05d36c9 is shaw on hshariati/enrichment_final. If you see a version of genie 
not found error. Check your shaw, or copy and paste from here and try again.
export GENIE_SHORT_SHA=5a9adfb # tested with this

```bash
cd /mnt/localssd/genie
uv venv --python 3.11
source .venv/bin/activate

export GENIE_SHORT_SHA=$(git rev-parse --short=7 HEAD)
uv pip install --prerelease=allow --index-strategy unsafe-best-match \
  --extra-index-url "https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-kineto-release/simple" \
  --extra-index-url "https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-piat-release/simple" \
  -e . "genie[glimmer-sqs,lint,dev]==1.0.0+$GENIE_SHORT_SHA"

uv pip install -e /mnt/localssd/ai-platform/frameworks/data/enrichment .
```


### better env management with uv
This works as long as you have dev. Because dev forces the pinned version of torchaudio 2.8.
Without dev, you'll get torchaudio2.9 which then gives you this error gives no module named torch audio.
unless you change the usage of torchaudio like this:
try:
    # torchaudio <= 2.8.x
    from torchaudio.io import StreamReader
except ModuleNotFoundError:
    # torchaudio 2.9+ moved StreamReader to a separate package (torio)
    try:
        from torio import StreamReader  # type: ignore
        
```bash
cd /mnt/localssd/genie
uv venv --python 3.11
source .venv/bin/activate

export GENIE_SHORT_SHA=f158246 # this works. Its the last shaw on hshariati/enrichment_v2.
uv pip install --prerelease=allow --index-strategy unsafe-best-match \
  --extra-index-url "https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-kineto-release/simple" \
  --extra-index-url "https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-piat-release/simple" \
  -e . "genie[glimmer,lint,dev]==1.0.0+$GENIE_SHORT_SHA"
```




### from default docs. Env is a bit weird
These work. With this shaw from hshariati/enrichment_v2.
You just have to set interpretor to /opt/venv/bin/python
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh;
export PATH="$HOME/.local/bin:$PATH"
source "$HOME/.local/bin/env"


export GENIE_SHORT_SHA=f158246
uv pip install --prerelease=allow --index-strategy unsafe-best-match \
  --extra-index-url https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-kineto-release/simple \
  --extra-index-url https://:${ARTIFACTORY_UW2_API_TOKEN}@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-piat-release/simple \
  -e . genie[glimmer,lint]==1.0.0+$GENIE_SHORT_SHA
```
for specific modules:
```bash
pip install -v -r glimmer/modules/image_captioning/requirements.txt
```


### Need pluto sdk cli
```bash
export EXTRA_INDEX_URL=https://$ARTIFACTORY_UW2_USER:$ARTIFACTORY_UW2_API_TOKEN@artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple;
pip install "adobe-aip[compute]" --extra-index-url=$EXTRA_INDEX_URL;
alias aip="python3 -m colligo.pluto.sdk.cli";
aip login
```


## Installing glimmer and genie only for chicu prototype only
my creds
```bash
export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A; export ARTIFACTORY_UW2_USER=hshariati; export GITHUB_TOKEN=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
```
```bash
bash /sensei-fs/users/achicu/uv.installer.sh
source ~/.local/bin/env

export UV_CACHE_DIR="/mnt/localssd/.cache/uv"
mkdir -p $UV_CACHE_DIR
```

# inject the UV index passwords.
```bash
echo "machine artifactory-uw2.adobeitc.com login $ARTIFACTORY_UW2_USER password $ARTIFACTORY_UW2_API_TOKEN" >> ~/.netrc
```

```bash
cd /mnt/localssd/genie
uv venv --python 3.11
source .venv/bin/activate

# below only works for chicu. and hshariati/new_glimmer_SQS_with_PL
uv pip install -v -e ./glimmer_queue -e ".[glimmer-core]"

for specific modules:
```bash
uv pip install -v -r glimmer/modules/image_captioning/requirements.txt
```


## Glimmer 2.0 new glimmer
source .venv/bin/activate

1. get credentials from klam
export AWS_ACCESS_KEY_ID=ASIA3B7MOPLPWEBBRPEV
export AWS_SECRET_ACCESS_KEY=oAjVKTSJStPsWQwcUt16AkLdoLH6jpc84a33/zT/
export AWS_SESSION_TOKEN=FwoGZXIvYXdzEFkaDOCecL3PtuMorx7qDCLtAbV2gI1yV2iDcYlSTyoEFGr0IB4li8/0Yb8hG8HvPSoUvP22ePPBCHvb2B4pR2ehbvmJK79wXDidutFpvv83zI/J8wGa/b0luvldhkxVARZ2dIcEJLPQExV7TqCKSxRRzW8ZXKVqQ3eIbEfTRv7dzwoCHevc/UFjJ7ND8prlX8P3oKE1HL9MWS1rZgIGOe+reXsFC7wTuiNeWeEaVw2YpJMdCP7kN9vkvxGahnvTHp+TGtPtJC5F7vxZL5jlQtIVPR1vDuimaywS/YnJY/n4e/tmFotwNdlmsGwFbe9OoMrd9TJWK5WFmwAYJLBDsyjX48nIBjItaXPmIn5XRA8MaGmlPWd33mzHfDAWqji3LHJVnpj3+bVPcXD51+X27dPXDozJ


export AWS_ACCESS_KEY_ID=ASIAUW4RARUUWOSZJ3MJ
export AWS_SECRET_ACCESS_KEY=QqzzoDIZ0+0uCic1ZA8jxJZElYpBGHlVzcy2T2eB
export AWS_SESSION_TOKEN=IQoJb3JpZ2luX2VjECEaCXVzLXdlc3QtMiJIMEYCIQD+9NTs7IZLzD8I5voCSIaDLi+73LyzHOdeWKNpNQ8HXAIhALiKHipV73KuTGnFt2FyEDoCfBFllMT/oipcSv8KLOeSKt8CCOr//////////wEQABoMMzI0MDM3MjgzMTEzIgy/oe2s4U01v9Whsj0qswJTBgPrTEUojgZ+Z1BJlrhmdGvtG+ZEnQsGnrKzgfYr7ju/dzdGAW/2BLGdYC/nh2IP+gtRti9COuHex0n6et0kj0hPQmcAKoRQc7Dbb7NkUvdDtG3AgqZl1SSSlNjaRuM8mjLEUQMot+/o3+U5yxsrP8quIawEiBjpOa3O3bIMygBYDNmpwq11kR+hs1o9ROa19E95NStZFCOqfrLMrCvmM5yuFG3dWiuDPlWjk7Pwb9JFZsV3y7obeOiNEP31b6n6KyFRP8IrMNZrJwQRJthSI/kTb42L5uJBmRTToArbSs3SZOs04bYrQ8OA4bOgyqhhd30ykzzvwd0nNqVAETtwzhZjt923gJH/IXQst88flIKOSWXV1tDcU/UlsDtPlV9853Y1PoyhfxSi5Bjjq/XpT1OPMM/e88wGOpwBDSW1fJpXgCnU442rOIa2AN3uOmh3T3uZdgpW/u6iczYmJn9vYSPce5OmegN1eb5kGOT19DKCt3bnl+La4MxlDLmV/B6GxkhrWhoMdskvUluRlIj9OuPsm/eAQLE/NzEcBMtvxNO3gUjp2RTY8wSQGjKn9iDLhgFJyJWJosQNUc4gsCdy4+tqRv/Q+ybtVJt+17KByT87cqvnUUyd

(genie) colligo@pluto-prod-hshariati-glimmer-debug-3-0:/mnt/localssd/genie$ python -m glimmer_queue.sqs_run   --queue-url https://sqs.us-west-2.amazonaws.com/760168217311/hs_exploration_queue4   --region us-west-2   --wait-time 10   --visibility-timeout 60   --batch-size 8   --config /mnt/localssd/genie/glimmer/modules/image_captioning/config_non_gentech.yaml   --gpus 0 --num-cpu-processes 2

```bash
python -m glimmer_queue.sqs_run \
  --queue-url https://sqs.us-west-2.amazonaws.com/760168217311/hs_exploration_queue4 \
  --region us-west-2 \
  --wait-time 10 \
  --visibility-timeout 300 \
  --batch-size 1 \
  --config /sensei-fs/users/hshariati/hs_scripts/glimmer/hs_vllm_test_new_glimmer.yaml \
  --gpus 0 --num-cpu-processes 32
```
  

## prometheus queries:
this is the metrics job you can clone:
https://pluto-prod-hshariati-vllm-metrics-jc63uh-1-0-8001.colligo.dev

it will pickup metrics from any job under your name.

Note that these logs come from 8002 of your job. Like this:
 https://pluto-prod-hshariati-vllm-metrics-efn8zx-1-0-8002.colligo.dev/debug/

```bash
sum by (finished_reason, job_name)(rate(vllm:request_success_total{job_name=~"vllm-test-.*"}[1m]))
sum by (finished_reason) (rate(vllm:request_success_total[1m]))
sum(colligo_frontend_requests_in_progress)

# gives rate of request_success_total counter incrementing per second for each of the GPUS/processes? (clarify with Chicu/Suresh)
rate(vllm:request_success_total{job_name="vllm-test-new-glimmer"}[1m])

# You can get the sum of all these together to see result for all processes to see how many requests you can handle in total.
sum(rate(vllm:request_success_total{job_name="vllm-test-new-glimmer"}[1m]))

# The only issue is that above might count the ones that where successful but finished because they ran out of tokens etc. So we can further count in each group controlled by finished_reason. So this will give you one count for each finished_reason (lenght, stop, abort)
sum by (finished_reason)(rate(vllm:request_success_total{job_name="vllm-test-new-glimmer"}[1m]))

# this one will group both by finished reason and job name
sum by (finished_reason, job_name)(rate(vllm:request_success_total{job_name=~"vllm.*"}[1m]))

# This is total number of requests all the GPUs combined can handle simulatenously
sum(vllm:num_requests_running{job_name="vllm-test-new-glimmer"})

# this is total number of requests waiting for all the GPUs
sum by (job_name)(vllm:num_requests_waiting{job_name="vllm-test-new-glimmer"})
```
## star vllm serv (chicu's)
this is the metrics job:
https://pluto-prod-hshariati-vllm-metrics-jc63uh-1-0-8001.colligo.dev

this is the job running the vllm serve and glimmer
https://pluto-prod-hshariati-vllm-test-new-1-0-8002.colligo.dev/debug/

If you look here you can see if a model is using tp (tensor parallel) or not. If nothing is mentioned is TP 1.
IF TP2, and you give it 8 GPUs that means you have 2 replicas. if you give it TP1, that meanst you have 1 replica.
https://github.com/Adobe-Firefly/colligo/blob/achicu/vllm_serve_bench/models/colligo/models/firefly/vllm_serve/build.py

### running the actual vllm server
job example:
https://ai.corp.adobe.com/compute/jobs/499f781d-04aa-4c14-a3ec-326c886aee12?view=project&filterop=or&filter-owner=equals-achicu%40adobe.com

```bash
  cd /mnt/localssd;mkdir vllm_server;cd vllm_server/;cp /sensei-fs/users/hshariati/hs_scripts/glimmer/scripts/vllm_serve_main.sh .;chmod +x vllm_serve_main.sh;./vllm_serve_main.sh;
```

### more info
this is the vllm server code we're using
https://github.com/vllm-project/vllm/blob/767cbb011dfa6e7685739dd29b68cde0727e459a/vllm/v1/core/sched/scheduler.py#L266

PR for adding a new model on colligo vllm server side
https://github.com/Adobe-Firefly/colligo/pull/17158


## starting glimmer manually
source .venv/bin/activate
export ARTIFACTORY_USER_KINETO=kineto
export ARTIFACTORY_UW2_USER=kineto
export ARTIFACTORY_UW2_API_TOKEN=AKCpBvWUY1qMpFTLYPP911ppArqmnzov5d7S2c8oNi3ge3FQCnCoq6EgpGhCRE4Ekc7iXXFxy


export KINETOBOT_GITHUB_API_TOKEN=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
export GLIMMER_DB=postgresql://glimmer:CbbHcArD8rS7DyIrKzdQtIT3@glimmer-queue-db.cq0ijarroa7i.us-west-2.rds.amazonaws.com:5432/glimmer

export RANK=0
export WORLD_SIZE=1
export CUDA_VISIBLE_DEVICES=""
export MASTER_ADDR=127.0.0.1
export MASTER_PORT=23456
export LOG_DIR="/mnt/localssd/logs/hs_glimmer_logs"

glimrelay --job-name hs_vllm_tes > $LOG_DIR/hs.grpc.out 2>> $LOG_DIR/hs.grpc.err

python -m glimmer.inference \
--config /sensei-fs/users/hshariati/hs_scripts/glimmer/hs_vllm_test_baseline.yaml \
--gpus 0 \
--num-cpu-processes 1
# --num-cpu-processes 7



## Logic for optimizing for vllm
https://jira.corp.adobe.com/browse/FFP-58217

We need to cover the amount of requests the GPUs can handle simultaneously + some slack. You need to keep a watch on vllm:num_requests_waiting to make sure there's always a number of requests waiting for all the GPUs, then vllm:num_requests_running would tell the amount a GPU can handle. Multiply the num_requests_running by the GPU count (or sum it in the query), add 10% (for the "waiting") and that should be the amount of requests the client should send simultaneously. If you send a lot more requests they have the possibility of adding timeouts, so make sure to not go a lot over.

 


preemption is when a request gets out in order to let another higher priority request get in. never seen it go this high.
so, you are sending 32 * 80 =2560 . the frontend requests are spot on.
with this new setup, we never run with more than 14 glimmer workers so far (edited) 
you need to compute like 8gpus  * 128 / 80 => 12.8 workers. Then add a bit of slack to ensure some are waiting.

that is 8 vllm instances use 4 for TP2
128 is the max simultaneous requests per vllm instance.
80 is your batch concurrency per glimmer process.

if vllm:num_requests_running is the sum of 8 vllm instances = 160, then it means it can only handle 20 requests in parallel per GPU.
that is pretty low, what GPU is this?
do you have the fix with the kv cache? the system prompt was inserted after the image instead of before. (edited) 
if 20 is the top it can do on these GPUs, you may want to reduce the amount of workers to 8 * 20 / 80  -> 2 (use 4 to ensure you get some waiting)

1. Start with some guess of how many requests vllm server can handle (vllm:num_requests_running). 
  - Note: On the vllms server side, the max limit (that is hardcoded in the colligo build) is 128 parallel requests per VLLM instance. Basically, colligo will only pick 128 out of the frontend requests at a time, so that it protects the GPUs from overwhelming. However, the frontends will pick up as many as you send.

  So a start for colligo_frontend_requests_in_progress would be 
  maximum vllm:num_requests_running = GPUs(8) * 128 = 1024
  so you want colligo_frontend_requests_in_progress to be about 1024*1.1 (10% to wait on each gpu) = 1126



2. Apply this formula to decide on concurrency and num_cpu_processes:
colligo_frontend_requests_in_progress = concurrency(40) * batch_size(1) * num_cpu_processes(32) = 1280
set the num_cpu_processes to 32 or as many cores as you have. And then concorrency would be 

3. In practice, I realized that it's harder to control the number of requests we send out by changing the num_cpu_processes because going from 32 to 16 with same concurrency 80 drops the requests we send out by a lot more than half. However, concurrency and batch_size have much more predictable affect. 

colligo_frontend_requests_in_progress = 1280
request_success_total = 16
num_requests_running = 500
num_requests_waiting = 42
  



For example, for 

### for hs:
I have 8.6 captions/s.
I always have 856 requests waiting, My GPUs can handle 160 requests simultaneously.

vllm:request_success_total 8.6
vllm:num_requests_waiting 856
vllm:num_requests_running 160
colligo_frontend_requests_in_progress: 1280


colligo_frontend_requests_in_progress = concurrency(40) * batch_size(1) * num_cpu_processes(32) = 1280



## running Orion
git checkout main
  278  cd python
  280  uv venv -p 3.10
  uv venv -p 3.12
  281  source .venv/bin/activate

  288  echo "machine artifactory-uw2.adobeitc.com login $ARTIFACTORY_UW2_USER password $ARTIFACTORY_UW2_API_TOKEN" >> ~/.netrc
    294  export PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus
    # this didnt work:   282  uv pip install -e ".[dev,data]"

  290  uv pip install -e ".[data]"
  uv pip install -e plugins/mldp_image/
  292  python scripts/data.py --config-path ./configs/example_config.json --workers 1

(python) colligo@pluto-prod-hshariati-vllm-test-new-1-0:/mnt/localssd/orion/python$ mkdir /mnt/localssd/orion/python/.venv/lib/python3.12/site-packages/orion/data/transforms/data/
(python) colligo@pluto-prod-hshariati-vllm-test-new-1-0:/mnt/localssd/orion/python$ cp src/orion/data/transforms/data/* /mnt/localssd/orion/python/.venv/lib/python3.12/site-packages/orion/data/transforms/data/

## Stable version
This commit:
a925de9cf8c6f191391dbe4e970803b63b3ede26
from this branch: https://github.com/Adobe-Firefly/genie/commits/achicu/scap_prompts/
has been tested to run. 
In his run, chicu installed with -e from the repo, so the actual glimmer_queue version he has is below.
But this was not from a PR build (CI) so was never pushed to artificatory. 
0.0.dev20250921194246+ga925de9

** we actually just pushed this to artifactory (jfrog)
glimmer_queue-0.0.dev20250922164139+ga925de9

**Note: that last digits of the glimmer queue version after g, will correspond to the genie commit that built the queue.
so for 0.0.dev20250921194246+ga925de9 (the genie commit was a925de9).
**Note that genie uses the glimmer_queue version mantioned in the pyptoject.toml unless you do the install -e 
the way chicu does. 

### glimmer postgres db username and password rds
```bash
export GLIMMER_DB=postgresql://glimmer:CbbHcArD8rS7DyIrKzdQtIT3@glimmer-queue-db.cq0ijarroa7i.us-west-2.rds.amazonaws.com:5432/glimmer
  ```
password for Data Framework Support Generic (datasupport):
MB2^sScvHJqTC66@^Ne6
Zi$QsXgeNNO1gS3#f!dS (i changed to this on jan 25, 2026)

## Launching at scale 


0. Locally test your module using
```bash
python -m glimmer.inference --config /mnt/localssd/genie/glimmer/modules/qwen2dot5_structured_captions/video_config.yaml --gpus 2 --test-mode
```
1. Push your code and make a PR (this is necessary). Write down the first 7 digit of the commit:
71c6c69

2. Make sure genie and pluto are all g2g
```bash
genie health
pluto login
```

3. Give new logfile path by editting the file below: 
~/.genie/config.yaml

4. Create a glimmer queue:
```bash
glim create --table /mnt/localssd/genie/glimmer/modules/qwen2dot5_structured_captions/video_config.yaml --job-name hshariati-glim-qwen25-captions-on-audio-v1-2 --row-group-size 256
```

5. You can check the status of your queue using:
```bash
glim stats --job-name hshariati-glim-qwen25-captions-on-audio-v1-2
```

6. Create an entery in the launch.json you need to put the name of your job there. When you click play
it will ask for the commit hash. 
```bash
        {
            "name": "Hooman for local debugging and break points",
            "type": "debugpy",
            "stopOnEntry": false,
            "request": "launch",
            "console": "integratedTerminal",
            "module": "glimmer.inference",
            "args": [
                "--config",
                "${workspaceRoot}/glimmer/modules/qwen2dot5_structured_captions/video_config.yaml",
                "--gpus",
                "1",
            ],
            "cwd": "${workspaceRoot}",
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceRoot}:$PYTHONPATH"
            },
        },
        {
            "name": "Hooman for pluto launch",
            "type": "python",
            "request": "launch",
            "python": "/mnt/localssd/genie/.venv/bin/python",
            "module": "genie.cli.genie_cli_pluto",
            "args": [
                "submit",
                "--num-nodes",
                "10",
                "--num-gpus",
                "8",
                "--show-config",
                "--config",
                "glimmer/modules/qwen2dot5_structured_captions/video_config.yaml",
                "--name",
                "hshariati-glim-qwen25-captions-on-audio-v1-2",
                "--accelerator-type",
                "NVIDIA_A100_80GB",
                "--project",
                "GPU-125-asml-vid-prod-viq",
                "--execute",
                "--install-version",
                "1.0.0+${input:genie_short_sha}",
                "--glimmer",
                "--glimmer-queue-name",
                "hshariati-glim-qwen25-captions-on-audio-v1-2",
                "--glimmer-module",
                "glimmer/modules/qwen2dot5_structured_captions",
                "--image",
                "docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/kineto:asml-data-v1",
                "preemptible",
            ],
            "justMyCode": true
        },
```
### NOTE:
for running the glimmer.inference you also need to run the glim relay server like the first entry below.
First you start the glim server using the play button once that's running, you start the other one.

Also you don't need to set the GLIMMER_DB if it's already set. 
Also note that you don't need the glimmer_vllm_client that's just for testing with vllm.

```bash
        {
            "name": "glim_queue_server",
            "type": "python",
            "request": "launch",
            "module": "glimmer_queue.start_server",
            "console": "integratedTerminal",
            "env": {
                "GLIMMER_DB": "postgresql://glimmer:CbbHcArD8rS7DyIrKzdQtIT3@glimmer-test.cq0ijarroa7i.us-west-2.rds.amazonaws.com:5432/glimmer"
            },
            "justMyCode": false,
            "args": [
                "--job-name", "vllm-not-gen-tech"
            ]
        },
        {
            "name": "glimmer_vllm_client",
            "type": "python",
            "request": "launch",
            "module": "glimmer.inference",
            "console": "integratedTerminal",
            "env": {
                "GLIMMER_DB": "postgresql://glimmer:CbbHcArD8rS7DyIrKzdQtIT3@glimmer-test.cq0ijarroa7i.us-west-2.rds.amazonaws.com:5432/glimmer",
                "CUDA_VISIBLE_DEVICES": "",
                "GLIMMER_JOB_NAME": "vllm-not-gen-tech"

            },
            "justMyCode": false,
            "args": [
                "--config", "glimmer/modules/image_captioning/config_non_gentech.yaml",
                "--gpus", "0",
                "--num-cpu-processes", "1",
            ]
        },
```

7. Check the satus of your initi script (installation) first. On pluto click on the job, then on Brows logs, 
and look at init_script/current
Once this is done you can look at 
main_script/current
You can serach for it/s also to get a sense. Or you can just use the stat function (above).


## Debugging S3 write
Put a break point here. 
https://github.com/Adobe-Firefly/genie/blob/73af6839ca27a2cee0c2275448b1c978572d8e0b/glimmer/base_module/base_writer.py#L301

It'll go to .
https://github.com/Adobe-Firefly/genie/blob/73af6839ca27a2cee0c2275448b1c978572d8e0b/glimmer/base_module/base_writer.py#L344

and then here:
https://github.com/Adobe-Firefly/genie/blob/73af6839ca27a2cee0c2275448b1c978572d8e0b/glimmer/base_module/base_writer.py#L537


##  Accessing Klam S3 database
https://klam.corp.adobe.com/
sensei-asml-stage
stg
administrator_and_support

Account # 760168217311
ASIA3B7MOPLP52OQCA7N
tc84EkxD4UYVqdJQxwd3IXgh1F8B2Z4qf7qpTeni

IQoJb3JpZ2luX2VjEAkaCXVzLWVhc3QtMSJGMEQCIEGaXONwnB8FiQJQdlFnUGgpBP9kBF3PZOCQctVwpbtzAiAXozySajkdiYVapWKQuQLtbvNoF66hBtk57/uuj2UlpSriAgiB//////////8BEAIaDDc2MDE2ODIxNzMxMSIMs5TjW6yXjxUs8nwwKrYChtqli00f1/JIRBzLtHg4sVfElDeaNRcuCkPcyavzSaipxtxG6VrAILTpvAEe+J/tI60iS6mdivoJxi7XSuWO45gWmVckhb+2kttzWJURQKz0R1KJjqhmqNRcfsCLZzZrmWa6a1gcKOyQudEf5PiSye14yPcXF6CEygjXQjKy46xRzoDHq0TPRE+3Vw5hti4xS55yS7j4h/3/768CUfw8TAmq9wX6bXYAjpt30Zv/TZArLoNf5vpIEyvJJlePrBN2YGl/z3Lsk9l53h5lpTso94s0ZxHY6311gU1q9h1dFd3pozpJx601dpGuAtj2oRa+3m0SdQfcN+1eNequgdZFy+MDQaWpGqdeKYuAAxC8AxX4VJLfLpbhONYN6VIuKbjY6lrowP0pwk6gzjeMdxSdF4KVOYztYTDv16LGBjqeAXJuDK+PdUnUWMRBg89qXmmZQP5lE+MoL74HWOfKLvDvusaSG/19MYlH2M0MMsz0WFAsrXXu/fNV/tjOWBsubT38dATm6fOp+fNLhNlYyR6lOOrWQXU8u1ILGdvyeQ/F+WVH5Ls8MnG0aPK78AzxUZnv+a9ar5OBi5cbSEhJGxFMmcBTf9BJNeKLfVWCTCoO0/fQIiHZi2c7HPyDsucA

aws_access_key_id=ASIA3B7MOPLP52OQCA7N
aws_secret_access_key=tc84EkxD4UYVqdJQxwd3IXgh1F8B2Z4qf7qpTeni
aws_session_token=IQoJb3JpZ2luX2VjEAkaCXVzLWVhc3QtMSJGMEQCIEGaXONwnB8FiQJQdlFnUGgpBP9kBF3PZOCQctVwpbtzAiAXozySajkdiYVapWKQuQLtbvNoF66hBtk57/uuj2UlpSriAgiB//////////8BEAIaDDc2MDE2ODIxNzMxMSIMs5TjW6yXjxUs8nwwKrYChtqli00f1/JIRBzLtHg4sVfElDeaNRcuCkPcyavzSaipxtxG6VrAILTpvAEe+J/tI60iS6mdivoJxi7XSuWO45gWmVckhb+2kttzWJURQKz0R1KJjqhmqNRcfsCLZzZrmWa6a1gcKOyQudEf5PiSye14yPcXF6CEygjXQjKy46xRzoDHq0TPRE+3Vw5hti4xS55yS7j4h/3/768CUfw8TAmq9wX6bXYAjpt30Zv/TZArLoNf5vpIEyvJJlePrBN2YGl/z3Lsk9l53h5lpTso94s0ZxHY6311gU1q9h1dFd3pozpJx601dpGuAtj2oRa+3m0SdQfcN+1eNequgdZFy+MDQaWpGqdeKYuAAxC8AxX4VJLfLpbhONYN6VIuKbjY6lrowP0pwk6gzjeMdxSdF4KVOYztYTDv16LGBjqeAXJuDK+PdUnUWMRBg89qXmmZQP5lE+MoL74HWOfKLvDvusaSG/19MYlH2M0MMsz0WFAsrXXu/fNV/tjOWBsubT38dATm6fOp+fNLhNlYyR6lOOrWQXU8u1ILGdvyeQ/F+WVH5Ls8MnG0aPK78AzxUZnv+a9ar5OBi5cbSEhJGxFMmcBTf9BJNeKLfVWCTCoO0/fQIiHZi2c7HPyDsucA



## Connecting to the RDS (glimmer queue) database and investigating stats,etc
-- install psql and connect to database cluster (like RDS)
conda install postgresql
psql "host=glimmer-test.cq0ijarroa7i.us-west-2.rds.amazonaws.com port=5432 dbname=postgres user=glimmer sslmode=require"
--this for glimmer test table
--this is for the actual prod table glimmer-postgres
psql "host=glimmer-postgres.cq0ijarroa7i.us-west-2.rds.amazonaws.com port=5432 dbname=postgres user=glimmer sslmode=require"

--this works for all of them 
username: glimmer
CbbHcArD8rS7DyIrKzdQtIT3

-- this will list all the databases
\l

--You can also use: "\q" to exist a database and "\c name" to connect to name database. 

--You can use "\dt" to listall the tables in the database you're connected to. 


-- See what indices are avialble on a given table
SELECT i.relname AS index_name, sui.idx_scan, sui.idx_tup_read, sui.idx_tup_fetch
FROM pg_stat_user_indexes sui
JOIN pg_class t ON t.oid = sui.relid
JOIN pg_class i ON i.oid = sui.indexrelid
WHERE t.relname = 'tasks'
ORDER BY sui.idx_scan DESC;

-- plan for the slow query (replace with a real UUID)
--The explain... line causes sql to explain the query on the next lines
EXPLAIN (ANALYZE, BUFFERS)
SELECT tasks_row_group FROM public.tasks WHERE job_id = '00000000-0000-0000-0000-000000000000';


export GLIMMER_DB=postgresql://glimmer:CbbHcArD8rS7DyIrKzdQtIT3@glimmer-test.cq0ijarroa7i.us-west-2.rds.amazonaws.com:5432/glimmer



-- Check what enum values exist for the state column
SELECT unnest(enum_range(NULL::taskstate)) AS state_values;

-- Or check what states are actually being used in the table
SELECT DISTINCT state FROM tasks;


-- find the job uui for a glimmer queue id (what you pass to glim stats)
```bash
SELECT DISTINCT id, name FROM jobs WHERE name::text LIKE '%vllm%' LIMIT 10;
```

-- Get completed rows given id
```bash
SELECT 
    count(tasks.row_group) AS total_tasks, 
    sum((tasks.max_ix - tasks.min_ix) + 1) AS total_rows, 
    sum(CASE WHEN (tasks.state = 'Success') THEN (tasks.max_ix - tasks.min_ix) + 1 ELSE 0 END) AS completed_rows, 
    min(tasks.acquired_time) AS first_touch, 
    max(tasks.last_updated) AS last_updated, 
    count(CASE WHEN (tasks.state = 'Active') THEN 1 ELSE NULL END) AS active_tasks, 
    count(CASE WHEN (tasks.state = 'Success') THEN 1 ELSE NULL END) AS success_tasks, 
    count(CASE WHEN (tasks.state = 'CompletedWithFailures') THEN 1 ELSE NULL END) AS failed_tasks 
FROM tasks 
WHERE tasks.job_id = '6bc63465-e1cd-4628-b6d9-127795292db9'::UUID;
```

## Docker images
genie:
docker-matrix-experiments-snapshot.ff.adobe.io/kineto:v34-genie-657bea9

Colligo:
docker-matrix-experiments-snapshot.ff.adobe.io/colligo/colligo-dev:v52



uv pip install -e ".[data]"
python scripts/data.py --config-path ./configs/example_config.json


