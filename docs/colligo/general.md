# vault token for pod expiring
you can login to vault and copy your token again.
Run: 
```bash
export VAULT_ADDR=https://vault-amer.adobe.net  && vault login
```
Then go to 
https://vault-amer.adobe.net/ui/vault/dashboard
and click on the top right face (profile) icon, and click "copy token".
This is your personal token.




## Calling gpt-image 2 from gateway
https://github.com/Adobe-Firefly/foundry/blob/sharmaa/claude_skills/experimental/sharmaa/claude_skills/firefly_3p_gpt_image2.md



# V3 deploy to dev
  0. source .venv/bin/activate
  1. Regenerate the cloud/ manifest by running
  smake lint
  2. Run
  cd managed_services/services/firefly/foundry/standalone_apps/thd_video/
  make image
  and then bump the tag:
  https://github.com/Adobe-Firefly/colligo/blob/main/managed_services/services/firefly/foundry/deploys/thd_video/dev/values.inference.yaml#L9

  3. Adding new workers
    For the current Pr, main thing missing I think is Sam model calling
    [11:31 AM]We need something similar to https://github.com/Adobe-Firefly/colligo/blob/main/managed_services/services/firefly/foundry/deploys/thd_video/dev/values.inference.yaml#L18 for sam model calling base on my understanding

    hs pr: https://github.com/Adobe-Firefly/colligo/pull/33181

### if you get access errors do this:
What I did is just put this in my netrc
machine artifacts.adobeitc.com
	login hshariati
	password api_key_from_jfrog(https://artifactory-uw2.adobeitc.com/ui/user_profile)
machine artifactory-uw2.adobeitc.com
	login hshariati
	password api_key_from_jfrog(https://artifactory-uw2.adobeitc.com/ui/user_profile)
machine XDG_CACHE_HOME
	login /mnt/localssd/.cache
	password _

### This is from shitong
1. delete content of /home/colligo/.netrc
you got artifactory token from https://artifactory-uw2.adobeitc.com/ui/user_profile?
[4:36 PM]I tried these on my side and it works
  rm -f ~/.netrc
  direnv reload
  smake lintthis will pop artifactory user and token.
Seems nothing to do with Vault?


## Investigations
1. Find argo link here https://foundry-inference-dev.adobe.io/#
sync App after deploy(PR merged) here https://devhome.corp.adobe.com/catalog/default/Component/SRID_527515/flex?repository=github.com%2FAdobe-Firefly%2Fcolligo-v3-deploy

### See live logs from Argo
Go to your pod (which you can find from foundry gateway. See note above). 
Like this: https://argocd-flexbox-003.ethos.corp.adobe.com/applications/argocd/adobe-firefly--colligo-v3-deploy--ethos851-stage-or2---8295564e?resource=&view=pods
Then find the one that is the main pipeine. For example for us this would be "firefly--ai-platform-dev-foundry-thd-video-thd-video-pipelm9xtm"
Click on the little green rectangle with check mark (which takes you to your replica). And then click on logs.

### To use splunk
Splunk for seeing the logs: https://splunk-us.corp.adobe.com/en-US/app/search/search?q=search%20index%3Dnfp_nonprod%20sourcetype%3Dv3-foundry-thd-video-dev&display.page.search.mode=fast&dispatch.sample_ratio=1&earliest=-5m&latest=now&sid=1789510423.292895_0B6244D5-24DA-40AC-8511-D69C6DEAF833

You copy the request id from your request and then just put the id in the search bar of plunk like this:
index=nfp_nonprod sourcetype=v3-foundry-thd-video-dev zk7K90GTa3SJnZuc2UIF

A better way of searching splunk is to DM Chiron like I did here:
https://adoberesearch.slack.com/archives/D0AL4PJ8LET/p1789511042286389


## warm up the worker
Again go through the foundry gateway. https://foundry-inference-dev.adobe.io/#
find the worker (like SMA2-image). And on actions click warmup. 




## I got an error when running make image and these steps fixed it
● That bg job already died — and now I see why a bare ad-hoc run won't work: daemon.sh's final exec uses s6-applyuidgid with PLUTO_GROUP_IDS and other CIS env vars we didn't
  pass, so under set -euo pipefail it aborts (and sudo … setsid swallowed the error, hence the empty log). Fighting that env by hand is fiddly.

  Better path: restart the supervised buildkit service. It's still alive but parked — s6-supervise buildkit (pid 141) with a sleep infinity (pid 200) sitting in the park state
  since boot. Now that uidmap is installed, restarting it re-runs daemon.sh with the correct CIS env, it installs buildkitd+rootlesskit, binds the socket, and stays
  supervised (survives crashes; and it'll also come up cleanly on future reboots). Run:

  #### clear the dead ad-hoc job entry
  kill %1 2>/dev/null

  #### restart the supervised buildkit service
  sudo /opt/cis/command/s6-svc -d /opt/cis/scandir/buildkit    # stop the parked run
  sudo /opt/cis/command/s6-svc -u /opt/cis/scandir/buildkit    # start -> re-runs daemon.sh -> buildkitd

  #### watch it come up (first start downloads buildkitd+rootlesskit, ~30–60s)
  tail -f /opt/job-logs/system/buildkit/current    # Ctrl-C once it looks ready
  ls -l /mnt/localssd/.buildkit/buildkit.sock      # socket should now exist

  Once the socket exists:
  docker buildx create --name pluto-builder --driver remote --use unix:///mnt/localssd/.buildkit/buildkit.sock
  docker buildx inspect pluto-builder      # should connect
  make image

  If, after the restart, /opt/job-logs/system/buildkit/current shows a new failure (not the old newuidmap one), paste it and I'll diagnose. But this should be the last blocker
  — the missing uidmap was the root cause, and that's fixed now.




# V3 deploy to pre-release
 To build and update the image yourself:

  cd /home/colligo/colligo/.worktrees/pr33280/managed_services/services/firefly/foundry/standalone_apps/thd_video
  make image

  Copy the full image reference printed by that command into:

  /home/colligo/colligo/.worktrees/pr33280/managed_services/services/firefly/foundry/deploys/thd_video/prerelease/values.inference.yaml

  Then regenerate and validate:

  cd /home/colligo/colligo/.worktrees/pr33280/managed_services

  PATH="$PWD/private/bin:$PATH" smake lint

  bazel build \
    //services/firefly/foundry/deploys/thd_video/prerelease:foundry_thd_video_ethos855_prerelease_or2

  git status --short
  git diff

  Commit only after reviewing the generated changes:

  cd /home/colligo/colligo/.worktrees/pr33280

  git add \
    managed_services/services/firefly/foundry/deploys/thd_video/prerelease/values.inference.yaml \
    managed_services/cloud/prerelease/foundry-thd-video-ethos855-prerelease-or2

  git commit -m "Update THD prerelease image"
  git push origin shitong/thd-promo

  The image tag will reference 1fcb6fe8d96; the subsequent config-only commit having a newer SHA is normal.



# proxy to connect pluto to laptop
### just run this on your laptop. On a terminal of code.
ssh -L 8000:localhost:8000 colligo@pluto-prod-hshariati-c5-job-framew-5-0 -p 3000


# mine
if it asks you for username give it: "hshariati"
for password give it: "AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A"
```bash
export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A; export ARTIFACTORY_UW2_USER=hshariati; export GITHUB_TOKEN=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
```
inside ARTIFACTORY_UW2_API_TOKEN, you can put both API key (older auth method) and identity tokens. 
I also generated a token (the API keys don't expire but identity token expires). 
```bash
export ARTIFACTORY_UW2_API_TOKEN=cmVmdGtuOjAxOjE3OTE5MDI1MjY6WnBGbkVZTWRBRjNVbmtxZzhRMENsWWlqakph;
```


# eval hubs
```bash
export AWS_ACCESS_KEY_ID=AKIASQRK44BROXTITHNO
export AWS_SECRET_ACCESS_KEY=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
aws s3 ls s3://clio-web-app/evaluation_service/eval_sets/i2v_animal_human_confusion_harm/data/part1/AdobeStock_583412451.jpeg
```


## For v3 pipeline install and run
1. start project in colligo/managed_services
2. ./setup-direnv.sh
3. Open a new shell, and make sure "smake" works, or "smake lint"
4. setup vs code: "smake vscode" this setups up intellisense.
5. Activate the env
    ~/colligo/managed_services$ source .venv/bin/activate
6. To make a worker
    ~/colligo/managed_services$ smake worker services/firefly/ai_platform/workers/sentiment

7. To bring up a pipeline as your claude. Or run these steps:
  In a real terminal on this pod (direnv auto-activates private/bin, so uv/make are on PATH):

  # one-time per shell session — needed for S3/IMS creds
  vault login -method=ldap username=$USER
  **I didn't really run

  cd ~/colligo/managed_services/services/firefly/foundry/standalone_apps/thd_video
  make run

  - Logs stream live to your terminal (stdout) and are tee'd to /tmp/thd_video.log.
  - Server is at http://localhost:8000, Swagger debug UI at http://localhost:8000/docs.
  - To tail logs from another shell: tail -f /tmp/thd_video.log

  make run already sets XDG_CACHE_HOME (weight cache on localssd) and FOUNDRY_AWS_GATEWAY_HOST for you.

8. To attach debugger, add your claude to add what it needs, and then just play through debug UI.
    I set up two things:
    - Added debugpy to the app's dev deps and ran uv sync (installed debugpy 1.8.21).
    - Added a make debug target and a VS Code launch config THD Video: Attach (debugpy 5678) (in .vscode/launch.json at repo
        root).

    Steps:

    1. Start the server under debugpy (blocks until the debugger attaches):
    cd ~/colligo/managed_services/services/firefly/foundry/standalone_apps/thd_video
    make debug
        It prints nothing and waits — that's expected; it's holding for the debugger on port 5678.
    2. In VS Code: set breakpoints (e.g. in actors/thd_video_rewrite_worker.py or prompt_rewrite/rewriter.py), open Run and 
        Debug (Ctrl/Cmd+Shift+D), select "THD Video: Attach (debugpy 5678)", press ▶.
    3. The server finishes booting and serves on :8000. Fire your example request (via /docs or curl) and it'll stop at your
        breakpoints. Backend logs still stream to the terminal + /tmp/thd_video.log.

    Handy overrides:
    - make debug WAIT=0 — start immediately, attach whenever (don't block on startup).
    - make debug DEBUG_PORT=5679 — different port (update the launch config's port to match).

    If VS Code runs on your laptop (not on the pod directly), forward the port first:
    ssh -L 5678:localhost:5678 -L 8000:localhost:8000 <pod-ssh-host>




## For creating SQS etc. 
You can just go on klam, and request credentials, click on copy credentials, and it'll give you something like this:
```bash
aws_access_key_id=ASIA3B7MOPLP4F3UBDCK
aws_secret_access_key=GShVVp77gp9rhDry/B8Sc/ONUgJcnSgEveH/y4cU
aws_session_token=FwoGZXIvYXdzEL7//////////wEaDAvyhSR018K557teDSLtAeIeC2Y5ELjlLQJs+zkG0q0FLPLw2VzTXeByNYzqexkINOUy/CjiFfWzM/GiYU3RcOMf5SeTLYOchTB4s3B/1hXa7umfGLRErAMF57XIi8M4jQoTbD0fjvGY6dZ/nd5EyOBKurxGZkutzN6y0eNb7uawkQok7C0fvLP2IyhBC1S43lH3saTyDOU/BlfKoclCnu4Jy/F2AJrzosJih0ke+1P5APcDySFVyA3ln6woRFmSiR/+VOU/TNSA1J5SMzSM15Vwfu0XPVS1A8t+d/79wCuDl7i5DKKQFvJNZtIOZH4SZdXDCWdx3AGpqkcXrCi37sbGBjItqMB1yz65X8NZ4bC919UisHGdBXij8Bbeag69sHTiJVU41mX0FT4yDT4A+WDQ
```
you then just make them upper case and add the export
```bash
export AWS_ACCESS_KEY_ID=ASIA3B7MOPLP4F3UBDCK
export AWS_SECRET_ACCESS_KEY=GShVVp77gp9rhDry/B8Sc/ONUgJcnSgEveH/y4cU
export AWS_SESSION_TOKEN=FwoGZXIvYXdzEL7//////////wEaDAvyhSR018K557teDSLtAeIeC2Y5ELjlLQJs+zkG0q0FLPLw2VzTXeByNYzqexkINOUy/CjiFfWzM/GiYU3RcOMf5SeTLYOchTB4s3B/1hXa7umfGLRErAMF57XIi8M4jQoTbD0fjvGY6dZ/nd5EyOBKurxGZkutzN6y0eNb7uawkQok7C0fvLP2IyhBC1S43lH3saTyDOU/BlfKoclCnu4Jy/F2AJrzosJih0ke+1P5APcDySFVyA3ln6woRFmSiR/+VOU/TNSA1J5SMzSM15Vwfu0XPVS1A8t+d/79wCuDl7i5DKKQFvJNZtIOZH4SZdXDCWdx3AGpqkcXrCi37sbGBjItqMB1yz65X8NZ4bC919UisHGdBXij8Bbeag69sHTiJVU41mX0FT4yDT4A+WDQ
```bash

# Pluto start up commands:
```bash
export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A;
export ARTIFACTORY_UW2_USER=hshariati; export GITHUB_TOKEN=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;
mkdir /home/colligo/.ssh; cp /sensei-fs/users/hshariati/doc_dont-delete/id_ed25519* /home/colligo/.ssh/; chmod  400 /home/colligo/.ssh/id_ed25519; sudo chmod -R 777 /home/colligo;
sudo chmod -R 777 /home/colligo; chmod 600 /home/colligo/.ssh/id_ed25519; cd /home/colligo; git clone git@github.com:Adobe-Firefly/colligo.git --single-branch; cursor /home/colligo/colligo; 


export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A;
export ARTIFACTORY_UW2_USER=hshariati; export GITHUB_TOKEN=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;
. /opt/conda/bin/activate; ./m sys.setup;

cd colligo;cp /sensei-fs/users/hshariati/copy2remote_colligo.dev.yaml ./colligo.dev.yaml; . /opt/conda/bin/activate; ./m deps.sync; source m;
```


## Connecting VScode to pluto new way
hs run on mcbook
Configure VSCode Remote Explorer easily: 
```bash
aip job configure ssh "img5-thd-debug_2026-01-12_10:42:39" --project "xPU Efficiency, Data, and Frameworks"
aip job configure ssh "img5-thd-debug_2026-01-12_10:42:39" --project "Presale & Partnership Support"
```
if you accidently mess up you config you can clean up like this
```bash
aip job configure ssh <job_name, project> --cleanup
```  


Hi team, we're excited to announce the latest AIP CLI v7.6, which includes:
:computer: SSH Capabilities
SSH directly into pods with  —no need to copy SSH configs or find pod names.
```bash
aip job ssh <job_name_or_id>
```
Run commands inside one or multiple pods: 
```bash
aip job ssh <job_name_or_id> "<your_command>".
```


Passwordless SSH authentication—no more typing “colligo” repeatedly.
:clipboard: List Jobs by Owner
View your jobs: aip list jobs
See jobs owned by another user: aip list jobs --owner <email> --project <name>
:wrench: Improved Job Creation
Use --start in aip job create to launch a job immediately.
For full details, check the documentation or use aip <command> --help.


## Run Colligo Pipeline Outside VS Code

```bash
source m; python -m colligo.rhode.commands.dev_supervisor --spec firefly_clineto --locust
```

```bash
source m; python -m colligo.rhode.commands.dev_supervisor --spec foundry --locust

source m; python -m colligo.rhode.commands.dev_supervisor --spec foundry --locust --replicas image5_dit_gen45_t2i_foundry_tccc 3
```

## With Replicas

```bash
source m; python -m colligo.rhode.commands.dev_supervisor --spec firefly_clineto --locust --replicas filix2_t2v_prod1_8_540p_1 2 --replicas dual_vae_pytorch 2
```


```bash
```bash
echo 'alias hs_clineto="screen -S hs -t tab1 bash -c \"python -m colligo.rhode.commands.dev_supervisor --spec firefly_clineto --locust; exec bash\" \; screen -X screen -t tab2"' >> ~/.bashrc
```

You can hit one Pluto machine from another by putting the IP address:

```python
endpoints = {
    'Pluto': '[http://10.90.197.89:8000/](http://10.90.197.89:8000/)'
}
```

Instead of `https://pluto-prod-siddhantg-sidg-gpu-dev-d2kfez-1-0-8000.colligo.dev/`



This is to run the tests locally:

```bash
python -m unittest models.colligo.models.compare.v2.videos.tests.test_generate_compare
python -m unittest models.colligo.models.compare.v2.videos.tests.test_extend_compare
```

## Rhoade Dashboard

To get the rhoade dashboard:

```bash
./runai port-forward colligo-dev-1 -p integration --port 8003:8003 --address localhost
```

## Debug Params

If you wanna put this in colligo debug UI you cannot have any spaces and any single quotes. To pass to `x-colligo-debug-input`:

```json
{"enable_prompty":false,"enable_dentro_pre":false,"enable_dentro_post":false,"disable_nsfw":true}
```

To send for html generation:

```bash
--debug_params "{'enable_prompty': false, 'enable_dentro_pre': false, 'enable_dentro_post': false, 'disable_nsfw': true,'enable_pre_ssr_output': true}" \
```

## Setup

If your VS code session dies on a runai machine:

**Purge old VS code:**

```bash
killall -9 codexz
sudo rm -rf /usr/bin/code ~/.vscode/* ~/.vscode-server/* /tmp/*
```

**Install new vscode:**

```bash
cd ~;
curl -Lk '[https://update.code.visualstudio.com/1.91.0/cli-linux-x64/stable](https://update.code.visualstudio.com/1.91.0/cli-linux-x64/stable)' --output vscode_cli.tar.gz; tar xvf vscode_cli.tar.gz; sudo mv code /usr/bin/code
```

**Start the tunnel:**

```bash
code tunnel user login --provider microsoft && nohup code tunnel --no-sleep --random-name --accept-server-license-terms & sleep infinity &
```

[https://github.com/Adobe-Firefly/colligo/pull/1558/files#diff-393132185d9054de4f72d5114dc4f29b5ad040b4083f110093af3b422ecc28cfR172](https://github.com/Adobe-Firefly/colligo/pull/1558/files#diff-393132185d9054de4f72d5114dc4f29b5ad040b4083f110093af3b422ecc28cfR172)

## All Startup Commands Together For PLUTO (on /home)

```bash
export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A;
export ARTIFACTORY_UW2_USER=hshariati; export GITHUB_TOKEN=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;
mkdir /home/colligo/.ssh; cp /sensei-fs/users/hshariati/doc_dont-delete/id_ed25519* /home/colligo/.ssh/; chmod  400 /home/colligo/.ssh/id_ed25519; sudo chmod -R 777 /home/colligo;
sudo chmod -R 777 /home/colligo; chmod 600 /home/colligo/.ssh/id_ed25519; cd /home/colligo; git clone git@github.com:Adobe-Firefly/colligo.git; cd colligo;
```

## All Startup Commands Together For PLUTO (on /mnt/localssd)

```bash
export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A; export ARTIFACTORY_UW2_USER=hshariati; export GITHUB_TOKEN=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; mkdir /home/colligo/.ssh; cp /sensei-fs/users/hshariati/doc_dont-delete/id_ed25519* /home/colligo/.ssh/;
chmod  400 /home/colligo/.ssh/id_ed25519; mkdir /mnt/localssd/hshariati; sudo chmod -R 777 /mnt/localssd; sudo chmod -R 777 /mnt/localssd/hshariati; cd /mnt/localssd/hshariati;
git clone git@github.com:Adobe-Firefly/colligo.git; cd colligo;
```

## All Startup Commands Together For RUNAI

```bash
export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A; export ARTIFACTORY_UW2_USER=hshariati; export GITHUB_TOKEN=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; sudo mkdir /home/hshariati;
sudo chown hshariati:users /home/hshariati; mkdir /home/hshariati/.ssh; cp /sensei-fs/users/hshariati/doc_dont-delete/id_ed25519* /home/hshariati/.ssh/; chmod  400 /home/hshariati/.ssh/id_ed25519; mkdir /mnt/localssd/hshariati; sudo chmod -R 777 /mnt/localssd;
sudo chmod -R 777 /mnt/localssd/hshariati; cd /mnt/localssd/hshariati; git clone git@github.com:Adobe-Firefly/colligo.git; cd colligo;
```

## I Used This:

1.  These are examples of setting envs:
    a.

    ```bash
    export SESSION_NAME="hs-colligo-dev-2" export PROJECT="asml-dev" export NODE_POOL="a100-80gb-1 a100-80gb-2 a100-80gb-3" export NUM_GPUS=8 export EXPOSED_PORT=9000 export PREEMTIBLE=0 export EXTRA_FLAGS="-l asml_project_name=clio-model-efficiency -l activity_type=productization"
    ```
    b.

    ```bash
    export SESSION_NAME="colligo-dev-1" export PROJECT="integration" export NODE_POOL="a100-80gb-1" export NUM_GPUS=8 export EXPOSED_PORT=9000 export PREEMTIBLE=0 export EXTRA_FLAGS="-l asml_project_name=clio-model-efficiency -l activity_type=productization -l research_jack_id=5382"
    ```
    c. For H100

    ```bash
    export SESSION_NAME="colligo-01-dev-h100-2gpus-1" export PROJECT="clineto-temp" export NODE_POOL="h100-2" export NUM_GPUS=2 export EXPOSED_PORT=9000 export PREEMTIBLE=0 export EXTRA_FLAGS="-l asml_project_name=clio-model-efficiency -l activity_type=productization -l research_jack_id=5333"
    ```
2.  Pull the latest script into `/Users/hshariati/colligo`
    a.

    ```bash
    vim /Users/hshariati/colligo/docker/dev/runai-interactive-submit.sh
    ```
    b. Change the runai to `/Users/hshariati/runai` so that it uses correct binary
    c. `bash /Users/hshariati/colligo/docker/dev/runai-interactive-submit.sh`
        i. Make sure you're in `~` where the `./runai` bin is available
    d. Shayan sent this in direct DM along with cluster 4 kube and the binary.
    e. **Turns out you need to have the binary just in your home folder or Downloads not in `/user/local/bin`
3.  Copy the link and authentication key from the runai logs. Log in on web-browsers. Then in the remote connections section of Vscode, under ssh, click on the login with microsoft. Then you should see the name of the pod.
4.  In vscode terminal do the rest to install colligo.
5. 
```bash
export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A; export ARTIFACTORY_UW2_USER=hshariati; export GITHUB_TOKEN=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
```
6.  `sudo mkdir /home/hshariati; sudo chown hshariati:users /home/hshariati; mkdir /home/hshariati/.ssh; cp /sensei-fs/users/hshariati/doc_dont-delete/id_ed25519* /home/hshariati/.ssh/;`
7.  `chmod  400 /home/hshariati/.ssh/id_ed25519;`
8.  Use below to install colligo. (similar to Create colligo env after migration to github)
    a.

    ```bash
    mkdir /mnt/localssd/hshariati; sudo chmod -R 777 /mnt/localssd; sudo chmod -R 777 /mnt/localssd/hshariati; cd /mnt/localssd/hshariati
    ```
    b. `git clone git@github.com:Adobe-Firefly/colligo.git; cd colligo`
    c. `# activate base conda environmnet`
    `. /opt/conda/bin/activate`
    i. On devbox: `. /home/hshariati/miniconda3/bin/activate`
    d. `./m sys.setup`
        i. This will add stuff to your `colligo.dev.yaml` and create one if you don't have one already. This is just a one-time thing.
        ii. Or just run below and paste the content
        iii. `vim colligo.dev.yaml`
    e. `./m sys.check`
    f. Set your vscode folder to `/mnt/localssd/hshariati/colligo`
    g. `./m deps.sync`
    h. `source m`
    i. `code .`
    j. ***To go to debug UI go to your opened port: [https://sensei-eks04.infra.adobesensei.io/asml-dev/hs-colligo-dev-2/debug/](https://sensei-eks04.infra.adobesensei.io/asml-dev/hs-colligo-dev-2/debug/)
    ***You must have the `/` at the end of debug. And you must enter the debug manually don't click on the debug Ui button from [https://sensei-eks04.infra.adobesensei.io/asml-dev/hs-colligo-dev-2/](https://sensei-eks04.infra.adobesensei.io/asml-dev/hs-colligo-dev-2/)
9.  `cp /sensei-fs/users/hshariati/colligo_files_backup/colligo.dev.yaml .` Co0y the file content instead because you don't wanna replace the stuff that setup puts in your file.
10. To start the deployment, click on the Run & debug in vscode, and then select the clio\_imaging (or experimental). But you must click this twice. Because there are two clusters and you need to connect to both.
    a. like you click the run&debug button. Then you click the clio\_imaging. This starts the first cluster, and the dialog doesn't go away. But then you click on clio\_imaging a second time, and now the second cluster starts and the dialog goes away.
11. You need port forwarding to connect to the debug UI
    ```bash
    runai port-forward hs-colligo-dev -p clio-model-efficiency --port 8000:8000 --address localhost
    ```
12. Then in your desktop browers you can just connect to: localhost:8000
13. You can install jupyter (in additoon to the extension) with pip:
    ```bash
    python -m pip install ipykernel
    ```
14. sd

## Connecting to Debug UI with Pluto

`https://<pod_name>-<port_numner>.colligo.dev/`

Like:

`https://pluto-prod-hshariati-viq-v175-inte-1-0-8000.colligo.dev/debug/`

## Create Colligo Env After Migration to Github

1.  `sudo chmod -R 777 /mnt/localssd`
2.  Connect to a devbox with your vscode. Run everything else in the vscode terminal.
3.  Pull the repo if not pulled already. MUST BE IN `/mnt/localssd`
    a.

    ```bash
    git clone [https://github.com/Adobe-Firefly/colligo.git](https://github.com/Adobe-Firefly/colligo.git) --single-branch
    ```
4.  Activate a python3.13 env. Create it if it doesn't exist already
    a.

    ```bash
    conda activate hs-pyth-env
    ```
5.  `export LDAP=hshariati SSH_PORT=4041  VERSION=hs2-v1 GPUS='"device=5, 6,7,"'`
6.  `cd /mnt/localssd/hshariati/colligo/docker/dev`
7.  `./make.py build`
8.  `./make.py run &`
9.  Go inside the docker:
    a. Remove the known\_hosts from `.ssh` on your laptop
    b. Then go in using vscode remote explorer. or
    c.

    ```bash
    docker exec -it -u hshariati colligo-container-hshariati-hs2-v1 /bin/bash
    ```
10. `mkdir /mnt/localssd/hshariati/venv`
11. `export COLLIGO_VENVS_PATH=/mnt/localssd/hshariati/venv`
12. This way, colligo will put the env here: `/mnt/localssd/hshariati/colligo/.venvs/dev`
13.
14. `export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A;`
15. `export ARTIFACTORY_UW2_USER=hshariati; export GITHUB_TOKEN=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`
16. `mkdir ~/.aws`
    `vim ~/.aws/credentials`
    a. Paste into it:

    ```ini
    [default]
    aws_access_key_id=AKIA4KAGRHX6XW442I3D
    aws_secret_access_key=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
    ```
17. Only if you don't have s5cmd:
    a.

    ```bash
    sh -c "$(curl -fsSL [https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh](https://raw.githubusercontent.com/Linuxbrew/install/master/install.sh))"
    ```
    b. `/home/linuxbrew/.linuxbrew/bin/brew install peak/tap/s5cmd`
18. `cd /mnt/localssd/hshariati/colligo/`
19. `./m deps.sync`
20. Make sure this runs ok:
    a. `./m sys.check`
21. Then you can source the env using:
    `source m`

## My AWS Creds

```json
{
  "aws_access_key_id": "AKIA4KAGRHX6XW442I3D",
  "aws_secret_access_key": "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",
  "credentials": "[default]\naws_access_key_id=AKIA4KAGRHX6XW442I3D\naws_secret_access_key=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\n\n[text2design]\naws_access_key_id=AKIA55EBG7KC4ST5DIYA\naws_secret_access_key=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\n",
  "presigned_aws_access_key_id": "AKIA4KAGRHX6XW442I3D",
  "presigned_aws_secret_access_key": "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"
}
```

## Xiagens AWS Creds

```bash
export AWS_ACCESS_KEY_ID=AKIA4KAGRHX6XW442I3D;
export AWS_SECRET_ACCESS_KEY=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; export AWS_DEFAULT_REGION=us-west-2
```

```bash
export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A; export ARTIFACTORY_UW2_USER=hshariati; export GITHUB_TOKEN=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
```

## To Create New Colligo Docker (to fix issue of it seeing wrong gpu)

NOTE: to fix the issue of seeing wrong GPU you don't need new image. You can skip step 7.

1.  You need to have a conta env with python 3.10: `conda create --name hs-pyth-env python=3.10`
2.  `Conda activate hs-pyth-env`
3.  `pip install click`
4.  `export LDAP=hshariati SSH_PORT=4047  VERSION=hs2-v1 GPUS='"device=7,"'`
5.  `mkdir /home/hshariati/venv`
6.  `export COLLIGO_VENVS_PATH=/home/hshariati/venv`
7.  `export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A;`
8.  `export ARTIFACTORY_UW2_USER=hshariati`
9.  `cd /sensei-fs/users/hshariati/colligo/docker/dev`
10. `./make.py build`
11. `./make.py run &`
12. `docker exec -it -u hshariati colligo-container-hshariati-hs2-v1 /bin/bash`
13. `mkdir .ssh;cd .ssh`
14. `cp -r /sensei-fs/users/hshariati/doc_dont-delete/* .`
15. Remove known\_hosts folder from your local (.ssh folder)
16. `ssh my_colligo_cont`
17. Install extensions:
    a. Python Test Explorer for Visual Studio Code (by Little Fox Team)
    b. Python Extension Pack by Don Jayamanne
    c. Github copilot (by github)
    d. Even better toml (tamasfe)
    e. Flake8 (microsoft)
    f. gitLens (gitKraken)
    g. Indent-rainbow (oderwat)
    h. Makefile Tools (microsoft)
    i. Docker (microsoft)
    j. Github pull requests and issues (github)
    k. jupyter
    l. gitlens by eamodio
    m. github pull requests

## Create Inside Container (to fix Env stops working)

When your env stops working (say "python tools/lint.py" or "pytest …" returns ModuleNotFoundError:

1.  Remove everything inside your env folder: `rm -rf ~/venvs/*`
2.  Setup artifactory creds: `export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A; export ARTIFACTORY_UW2_USER=hshariati`
3.  `mkdir venv`
4.  `export COLLIGO_VENVS_PATH=/home/hshariati/venv`
5.  `cd /sensei-fs/users/hshariati/colligo/`
6.  Recreate the env: `python tools/env.py create --env dev`
7.  Activate the env (exit and enter docker again if previous env activated): `. ~/venvs/dev/bin/activate`
8.  Then you need to go to colligo\_deploy repo and do the stuff in this PR: for colligo deploy: [https://git.corp.adobe.com/firefly/colligo-deploy/commit/de67a84a0f317e617808d77617d6a5501ee3d6a6](https://git.corp.adobe.com/firefly/colligo-deploy/commit/de67a84a0f317e617808d77617d6a5501ee3d6a6)
9.  sdfds

## Colligo Docker Container Died

Just restart the dead container from inside the devbox with: `docker container start colligo-container-hshariati-hs2-v1`
Then go into the container with "ssh my\_colligo\_cont" from terminal (without doing the 2nd step vs code cant connect).

## Running Tests and Debugging

**Adding input or parameter to debug ui or using debug data**

In staging, you can pass whatever parameters you want. You can access these in the request with `get_request_ctx().debug_data.get("keyName", DefaultValueIfKeyMissing)`.

**Example:** [https://github.com/Adobe-Firefly/colligo/blob/8a3fd08b65ae90444dd4c58f150ac5ce9cf3[…]ls/firefly/clio/call_components/ClioImagingT2ICallComponents.py.](https://github.com/Adobe-Firefly/colligo/blob/8a3fd08b65ae90444dd4c58f150ac5ce9cf3%E2%80%A6ls/firefly/clio/call_components/ClioImagingT2ICallComponents.py.)

```python
moe_name = T2IMoeName[get_request_ctx().debug_data.get("clio_moe_type", T2IMoeName.MOE_5_40_5_38.value)]
```

You can pass it from debug UI like this:

```json
{"clio_moe_type" : "MOE_3_27_DMD_5_38"}
```

Just make sure to include:

```yaml
allow_stage_features: true
```

In your `colligo.dev.yaml`.

**Issue with s5cmd:** Run: `sudo chmod -R 777 /mnt/localssd`. For more details see: [https://git.corp.adobe.com/pages/colligo/troubleshooting.html](https://git.corp.adobe.com/pages/colligo/troubleshooting.html)

**"No gpu for cfg computation" error when running unit tests:** This is more of a compatibility issue between a10g and a100. To temporarily fix this (so that the pipeline runs), comment this line out when you run on single a100. You might also need to relax the mem usage from 23 to 40 in `firefly_v2/diffusion/build.py`:

```python
gpu=build.gpu_info(memory_gb=40, count=1),
```

## How to Decode Image Tensors in Colligo

Encoder and decoder definitions can be found here: `/mnt/localssd/hshariati/colligo/models/colligo/models/firefly/imcoding/decoder_v3/build.py`.

**Unit test with image decode in the end:**

```python
@pytest.fixture(autouse=True, scope="module")
def load_model() -> Iterable[None]:
    with native_deploy_ctx([DIFFUSION_CLIO3_PROD3_27, LDM_DECODER_V3_128_8X]):
        yield


@pytest.mark.slow  # do not run in CI
@pytest.mark.asyncio
async def test_diffusion_component_LP12(test_data: Path) -> None:
    my_output_async = await generic_diffusion._run(input)
    assert my_output_async.images.as_torch().shape == torch.Size([1, 12, height, width])
    ldm_decoder_v3 = LdmDecoderV3("ClioImaging Ldm Decoder V3", LdmDecoderV3Config(cast_to_uint8=True))
    decoder_output = await ldm_decoder_v3.call(
        LdmDecoderV3Input(
            images=my_output_async.images,
        )
    )
    k = to_pil_image(decoder_output.images.as_torch()[0])
    k.save("/mnt/localssd/hshariati/colligo/delete/test.png")
```

You need this in your `colligo.dev.yaml`:

```yaml
remote_deploy:
  local_deploys: [clio_imaging, diffusion_prod3_27, ldm_decoder_v3_128_8x]
  remote_deploys: []
  endpoint: [https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net](https://clio-imaging-dev.ethos851-stage-or2.ethos.adobe.net)
request:
  timeout: 1000000
allow_stage_features: true
```

## Checking Pluto Logs

To check Pluto logs, you can use any of these methods:

1. Use the `cursor` command to view logs directly:
```bash
cursor /logging-fs/logs/pluto/jobs/<username>/pluto-prod-<username>-<job-name>/run-1/pod-0-<date>-<time>/main_scripts/1/current
```

For example:
```bash
cursor /logging-fs/logs/pluto/jobs/hshariati/pluto-prod-hshariati-structure-mat/run-1/pod-0-2025_04_10-18_33_09/main_scripts/1/current
```

2. Click on "Browse Logs" in the Pluto UI to view logs through the web interface. When in vscode click on main_scripts/current

3. Access the Pluto machine directly by clicking on the machine link that Kaizen prints in its output.

## Sub Modules

**Vendor/…. modifications:** To get rid of modification you can run:

```bash
git submodule update --init --recursive
```

To update just a specific one (in case you get an error about LLVm or something) use:

```bash
git submodule update --init --recursive --remote vendor/AdobeDiffusion/
```

**Below didn't work for me. But above command did it.**

```bash
git submodule update --recursive --rebase
```

This command will update the submodules to the commit stored in the main repository. After running this command, you can check the status again with. If you still see changes and you wanna check them out you can do:

```bash
git submodule foreach git reset --hard
```

Or:

```bash
git submodule foreach --recursive git reset --hard
git submodule foreach git clean -df
```

The first command (`git submodule foreach git reset --hard`) will reset each submodule to the commit it's supposed to be at, discarding any local changes. The second command (`git submodule foreach git clean -df`) will clean up any untracked files in the submodules.

## Sub Modules Nanotiny Tiny Nano

## Push to Artifactory

To push to Artifactory with new colligo (April 25, 2024): Inside your colligo env (after running: `source m`) run:

```bash
./m deps.upload_artifact <path to file> <a group name>
```

**Example:**

```bash
./m deps.upload_artifact global_step_30000_Gcombined_colligoSlimmed.ckpt diffusion
```

For a folder, you need to zip it like this (starting from the folder that has your sub-folders):

```bash
zip -r /mnt/localssd/hshariati/dit_t2v_seq_ait_engines.zip ./*
./m deps.upload_artifact /mnt/localssd/hshariati/dit_t2v_seq_ait_engines.zip diffusion
```

Rest of documentation is here: [https://git.corp.adobe.com/pages/colligo/guides/misc/deps.html#binaries](https://git.corp.adobe.com/pages/colligo/guides/misc/deps.html#binaries)

**Old notes:** To push your unit test data to artifactory:

1.  Place the data in the appropriate folder inside `data/test`, such as `/sensei-fs/users/hshariati/colligo/data/test/t5_encoder`.
2.  Add or Edit the `/sensei-fs/users/hshariati/colligo/tiny/test.t5_encoder.txt` (add one if it doesn't exist).
3.  Inside put: `"name of your file" "name of your file"`. **Example:** `"t5_text_embedding_noPad_xxl_the-dog.pkl" "t5_text_embedding_noPad_xxl_the-dog.ebdb96b.pkl"`.
4.  Run the command: `nanotiny write`. This command will update the `test.t5_encoder.txt` and add the hash to it. So it'll become like this: `"t5_text_embedding_noPad_xxl_the-dog.pkl" "t5_text_embedding_noPad_xxl_the-dog.ebdb96b.pkl" ebdb96b654faa68daeb07d2f74ba2f17b2671d54607eed4959daa723502052ce`. It will also push the file to artifactory ahnd update the `tiny.yaml` file.
5.  Commit/Push `test.t5_encoder.txt` to github. You don't need to push the actual file or the `tiny.yaml` to github.
6.  You also need to run `nanotiny deploy`.

## Slimming the Weights

To slim the weigths you can use the colligo script: `/mnt/localssd/hshariati/colligo/pylibs/colligo/dev/scripts/slim_weights.py`.

Or this one: [https://github.com/Adobe-Firefly/colligo/pull/3530/files](https://github.com/Adobe-Firefly/colligo/pull/3530/files)

## Adding Models in `build.py` Local Source `src`

**From Sensei (this will not be deployable):**

```python
CKPT_DIT_V2V_PROD1_1 = build.local_file_source(
    path=Path(
        "/sensei-fs/projects/firefly/clio/runai_training/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-03-28T14-34-13/lightning_logs/version_5/checkpoints/global_step_98000_Gcombined_slimmed.ckpt"
    )
)
```

**From Artifactory:**

```python
CKPT_DIT_V2V_PROD1_1 = build.s3_source(
    bucket="s3://colligo-dev-artifacts/artifacts-v1",
    key="diffusion/may_t2v_dit_mds_phase4_mixed_train-2024-05-25T09-38-06-115k_ema.2024-05-30.15-55.e7716.ckpt",
    version_id="4Bp59RUhvQN8Ly9NNMtCIEbqkxByX2NF",
    sha256="e7716ab09646d4c0b016936b3cb8523d153b08b922b68fdfec9564fdbe5bf38e",
)
```

## Run Colligo Pipeline Outside VS Code (Again)

```bash
/mnt/localssd/hshariati/colligo/.venvs/dev/bin/python -m colligo.rhode.commands.dev_supervisor --spec firefly_clineto --locust
```

## Follow these steps to do profiling using Pluto profiler
1. On the Rhode dashboard (https://pluto-prod-hshariati-colligo-vllm-x631wv-1-0-8003.colligo.dev/)
click start tracing, 
Make sure under State, tracing_config shows active:true
{
    "tracing_config": {
        "active": true
    },
    "version

2. send the requests. You might have to send many to simulate load.
3. download the profile, since it will get deleted once tracing is 
stopped, And then finally stop tracing. 
#### Working with the file
5. Double click on the downloaded zip to unzip it.
6. You can open any of this JSONS in cursor, right click, and select format document, to get it more readable. 
7. The names of the json correspond to client ID, but inside them, they have the server IP address too. Like this:
    "displayTimeUnit": "ms",
    "otherData": {
        "client": {
            "id": "14bda6963e05433b8283b5b126175b0f", (This matches name of the file)
            "host": "10.91.215.233", (This is the container IP of your Pluto job)
            "port": 39495
        },
### Viewing the logs
8. On chrome url box type: "chrome://tracing/"
### Now you can either stay in raw tracing or click on the Perfetto. In later you do this:
https://ui.perfetto.dev/
9. Just drag and drop the zip file. And you can see everything. 

### using just the raw chrome tracing then:
9. Then you can drag and drop any of the json file there. Make sure you have not reformatted the file. You can only do 1 file at a time here.
10. Once there, you can move left and right with S and D and zoom in and out with W and S. 
11. For LLMs for example, you'll see OpenGVLab?internvl3-38b process, under it you see the generate_tokens process, and under it, you can see the time it took for each of the toekns to be generated. 


# start codex with full permissions
codex --sandbox danger-full-access --ask-for-approval never --search
codex resume --sandbox danger-full-access --ask-for-approval never --search
codex -C project_dir --sandbox danger-full-access --ask-for-approval never --search

# Getting bedrock claude on a pluto machine

## Long term creds
1. Go on vault and read the secret from the path below:
dme_colligo/services/foundry/bedrock
https://vault-amer.adobe.net/ui/vault/secrets/dme_colligo/kv/services%2Ffoundry%2Fbedrock%2Ffoundry_bedrock_prod/details?version=1

Then these are the steps:
```bash
export AWS_ACCESS_KEY_ID='xxx'
export AWS_SECRET_ACCESS_KEY='xxx'
export AWS_REGION='us-west-2'
unset AWS_SESSION_TOKEN
export CLAUDE_CODE_USE_BEDROCK=1
export ANTHROPIC_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
claude
```


in one line
```bash
export AWS_ACCESS_KEY_ID='xxx'; export AWS_SECRET_ACCESS_KEY='xxx'; export AWS_REGION='us-west-2'; unset AWS_SESSION_TOKEN; export CLAUDE_CODE_USE_BEDROCK=1; export ANTHROPIC_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'; export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```
claude --dangerously-skip-permissions --resume

The laser project starts from here:
/home/colligo/hs_scripts/claude/auto_research

admin info has the creds too.

## short term creds (easy)
get bedrock creds from the gateway. 
Then 

```bash
source ~/del.txt
export CLAUDE_CODE_USE_BEDROCK=1
export ANTHROPIC_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
claude --dangerously-skip-permissions --resume
```




doc: 
https://github.com/Adobe-Firefly/foundry/blob/main/docs/project-setup-and-access.md#28-ethos-services-llm-access-via-vault-secrets

