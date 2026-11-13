```markdown
## Connecting to Machine

If ssh into machines fail:
You can always use:
```bash
./runai bash nemo-training-test1 -p clio-model-efficiency --pod nemo-training-test1-master-0
```
If this is a distributed job, you can get the pod by describe command. [cite: 1]

## Delete a Run:AI Job

To delete a Run:AI job from the command line:
```bash
runai delete job nemo-training-test2 -p clio-model-efficiency
```
Output:
```
Job nemo-training-test2 deleted successfully.
```
[cite: 2]

To check the number of running jobs:
```bash
runai describe job dmd-v12-prod3-27-162k-64n-3 -p clio-model-efficiency | grep RUNNING | wc -l
```
[cite: 3]

## Switching User on a Machine

To log in as your own user from someone else's machine:
```bash
sudo login hshariati
```
And then use your LDAP password. [cite: 4]

## SSH and VS Code Setup

1.  Run port forwarding on your laptop for SSH:
    ```bash
    runai port-forward clio-engine -p asml-demos --port :22 --address localhost
    ```
    This is for SSH. [cite: 4]
2.  To view a Jupyter Notebook, run:
    ```bash
    runai port-forward clio-engine -p asml-demos --port 8888:8888 --address localhost
    ```
    * `hooman` is the name of the job. [cite: 5]
    * `asml_demos` is the name of the project. [cite: 5]
    ***Note:** You need to set the correct cluster environment and log in to Run:AI before you can run this. Use `Set_runai4;runai login;` [cite: 5]
3.  Leave the terminal running (even if you background it, it still sends logs). [cite: 6]
4.  You can have an entry in your `.ssh/config` file like this:
    ```
    Host runai
       UseKeychain yes
       AddKeysToAgent yes
       IdentityFile ~/.ssh/id_ed25519
       ForwardAgent yes
       HostName localhost
       User hshariati
       Port 8080
    ```
    [cite: 6]
5.  Now you can SSH with `ssh runai` or connect to the Run:AI box through VS Code. [cite: 6]
**Note:** To connect to different Run:AI machines, you only need to change the port forwarding command. You don't need to change the `.ssh/config` file. [cite: 7] The file looks at port `8080`. This will be whatever job whose port 22 you map to this port using the `runai port-forward` command above. [cite: 8]

You can look at the script you use for the Clio demo for reference: `/sensei-fs/users/hshariati/clio-engine/AdobeDiffusion/scripts/clioengine/hs_empty_entrypoint.sh` [cite: 9]

```bash
#!/bin/bash

set -e #exit if any command fail
set -x #print each command in terminal before running it, for debug purpos.
uname="$(whoami)"
echo $uname
sudo mkdir -p /home/$uname
sudo mkdir -p /home/user
sudo chmod 777 /home/$uname
sudo chown "$uname:users" /home/$uname
mkdir /home/$uname/.ssh
sudo chmod 700 /home/$uname/.ssh
sudo chown root /usr/bin
sudo chmod 777 /home/user
sudo chown -R $UID:100 /home/user

sudo service rsyslog restart
sudo service ssh restart
sudo service sssd restart

a.
```
[cite: 10]

For Mac, use:
i. `sudo launchctl stop com.openssh.sshd` [cite: 11]
ii. `sudo launchctl start com.openssh.sshd` [cite: 11]

Permission denied (publickey) - Solution not yet known. [cite: 11, 12]

## See Job Status

You can see the status of a job either in the online dashboard or by running this command in your desktop terminal:
```bash
runai describe job clio-engine2 -p asml-demos
```
[cite: 13]

## Connect to a Job for Logs

To see logs in case a job fails:
```bash
set_runai_1
runai login
runai attach --no-tty clio-engine2 -p asml-demos
```
[cite: 13]

## Launching Jobs

You can do this interactively or via script. [cite: 13] If you click on a running job, you can clone it to see the parameters. [cite: 14]

***You also need this label now:** `activity_type -> productization` [cite: 15]

As well as: `asml_project_name -> clio-model-efficiency` [cite: 15]

Another way (most reliable):

1.  Go on a machine that has access to `sensei-fs` and `AdobeDiffusion`. [cite: 15]
    i.  *If there is no runai, there is a binary in `/sensei/users/hshariait` [cite: 16]
2.  `export KUBECONFIG=/sensei-fs/users/hshariati/kube_configs/runai_eks04.yaml` [cite: 16]
    i.  **If this didn't work, you need to do:** [cite: 17]
        ii. `mkdir /home/hshariati/.kube` [cite: 17]
        iii. `cp /sensei-fs/users/hshariati/kube_configs/* /home/hshariati/.kube/` [cite: 17]
        iv. A newer Docker image is: `docker-clio-release.dr-uw2.adobeitc.com/inference/clio-inference-cuda12:0.1.36_2.9.0` [cite: 18]
        v. You will need to also edit this script: `scripts/DockerDev/clio_runai_dev/start_interactive.sh` [cite: 18]

        ```bash
        LABEL2="activity_type=productization"
        CMD="${CMD} -l ${LABEL2}"
        ```
        [cite: 18]
        vi. sdf [cite: 19]
3.  Go inside the `AdobeDiffusion` repository. [cite: 19]
4.  `make start-runai-interactive` [cite: 19]
    i.  Example cluster 4 [cite: 19]
    ii. Job name: hooman-dev [cite: 19]
    iii. Project name: clio-model-efficiency [cite: 19]
    iv. Asml: 0 [cite: 20]
    v. ASML project name: clio-model-efficiency [cite: 20]
    vi. Docker name: `docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v1.0` [cite: 20]
    vii. GPUS: 8 [cite: 20]
    viii. Jupyter: 1 [cite: 21]
5.  Once inside the machine, if you use the above Docker image, then you can run this script to set up the environment:
    ```bash
    bash /sensei-fs/users/hshariati/hs_env_setup.sh /sensei-fs/users/hshariati/worktree_AdobeDiffusion/hshariati/mc-dmd3/
    ```
    [cite: 21]

    Another Docker image: `docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/clio-and-colligo-inference-ubuntu22.04-ait-runai:0.0.3` [cite: 21]

### Interactively

I just cloned an existing job and launched it. [cite: 21] The cloned job had these values (I edited the job name only so anywhere that is hooman, which is in links and job name): [cite: 22]

Make sure you select INTERACTIVE and note TRAINING. [cite: 22]
Project: asml-demos [cite: 22]
Name: clio-engine [cite: 22]
GPUs: 1 [cite: 22]
Image: `docker-clio-release.dr-uw2.adobeitc.com/inference/clio-inference-cuda12:0.1.36_2.15.0` (or `docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v0.9` or `docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v1.0`) [cite: 22]
Jupyter Notebook: On [cite: 22]

Resource Allocation:
Node pools: a100-80gb-1 [cite: 22]
Large SHM: On [cite: 22]

Container Definition:
Command: `/bin/bash` [cite: 22]
Arguments: `-c /sensei-fs/users/hshariati/clio-engine/AdobeDiffusion/scripts/clioengine/hs_engine_entrypoint.sh` [cite: 22]

Environment Variables:
`jname`: clio-engine [cite: 22]
`pname`: asml-demos [cite: 22]

Labels:
`asml_project_name`: asml-demo **note that due to a bug this should not have s at the end.** [cite: 22]

Image Pull: if not present [cite: 23]
Create Home Directory: On [cite: 23]
Service Type: None [cite: 23]

Job URL:
Container port 8888, custom URL: [https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/](https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/) [cite: 23]
Container port: 6000, Custom URL: [https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/v1](https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/v1) [cite: 23]
Container port: 3000, Custom URL: [https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/v2](https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/v2) [cite: 23]

To get the DMD Clio Engine demo working:
Second try (actually worked) to be able to open both Jupyter and ClioEngine ports, I started it using GUI and following this section of notes: Interactively I just made these changes: [cite: 23]
Cluster: 04 [cite: 23]
Job: clio-dmd-inference-1 [cite: 23]
Project: clio-model-efficiency [cite: 23]
Image: [cite: 23]
GPUs: 8 [cite: 23]

Container Definition:
Command: `/bin/bash` [cite: 23]
Arguments: `-c /sensei-fs/users/hshariati/clio-engine/AdobeDiffusion/scripts/clioengine/hs_engine_entrypoint.sh` [cite: 23]

Environment Variables:
`jname`: clio-engine [cite: 24]
`pname`: asml-demos [cite: 24]

Labels:
`asml_project_name`: asml-demo **note that due to a bug this should not have s at the end.** [cite: 24]
`adobe.com/runai_workload_type`: interactive [cite: 24]

Job URL:
Container port 8888, custom URL: [https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/](https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/) [cite: 25]
Container port: 6000, Custom URL: [https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/v1](https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/v1) [cite: 25]
Container port: 3000, Custom URL: [https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/v2](https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/v2) [cite: 25]

First try: This worked, but Jupyter is not accessible from outside because you can only add one port. [cite: 25, 26] So I tried from GUI instead. [cite: 26] I modified the `/sensei-fs/users/hshariati/worktree_AdobeDiffusion/AdobeDiffusion/scripts/DockerDev/clio_runai_dev/start_interactive.sh` like below. Then used the same method as above. [cite: 26]

**Just make sure your job name matches the `clio-dmd-infernece-1` in the link.** [cite: 27]

I used this Docker image: `docker-clio-release.dr-uw2.adobeitc.com/inference/clio-inference-cuda12:0.1.36_2.9.0` [cite: 28]

```bash
CMD="runai submit --interactive"
CMD="${CMD} --name ${JOB_NAME}"
CMD="${CMD} -p ${PROJECT_NAME}"
CMD="${CMD} -g ${NUM_GPUS}"
CMD="${CMD} -i ${IMAGE_NAME}"
CMD="${CMD} -l ${LABEL}"
CMD="${CMD} -l ${LABEL2}"
CMD="${CMD} --node-pool ${NODE_POOL}"
CMD="${CMD} --service-type=external-url"
CMD="${CMD} --port $PORT"
CMD="${CMD} -e pname=${PROJECT_NAME}"
CMD="${CMD} -e jname=${JOB_NAME}"
CMD="${CMD} --large-shm"
CMD="${CMD} --service-type=external-url"
CMD="${CMD} --custom-url=[https://sensei-eks04.infra.adobesensei.io/clio-model-efficiency/clio-dmd-inference-1/v1](https://sensei-eks04.infra.adobesensei.io/clio-model-efficiency/clio-dmd-inference-1/v1)"
CMD="${CMD} --port 6000"
CMD="${CMD}${ATTACH_STR}"
CMD="${CMD} --command -- /bin/bash -c \"/runai_entrypoint.sh\""
```
[cite: 28]

### Via Script

This is the script: [https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/dev/scripts/DockerDev/clio_runai_dev/start_interactive.sh#L99-L114](https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/dev/scripts/DockerDev/clio_runai_dev/start_interactive.sh#L99-L114) [cite: 28] But I have my own version of it that I added a command to: add a `custom_url`. [cite: 28] You can just run mine from your laptop: `/Users/hshariati/hs_launch_clio_engine.sh` [cite: 29]

At the end of it, this script runs my script for launching the `clio_engine`. You can comment this part out if you want. [cite: 29] **Note:** Using the script, you can only open one port (set only one external URL). If you want more, you have to add it manually or launch the job via GUI. [cite: 30] This means that people cannot go to: [https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/lab/](https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine/lab/). They need to have port forwarding on and then go to `http://127.0.0.1:8888/asml-demos/clio-engine/lab`. [cite: 31] To fix this, use the Interactive method above to launch the job. [cite: 32] This will allow you to open ports 6000 and 8888. [cite: 33]

```bash
eval ${CMD}
```
[cite: 33]

## Install Conda on Run:AI Box

```bash
#sudo chmod 777 /opt/
# bash scripts/DockerDev/install_conda.sh /opt/conda    #put this in the run engine script
#source /opt/conda/etc/profile.d/conda.sh
```
[cite: 33]

## See Newly Created Environment in Jupyter

```bash
conda create -n hs_AD_3.10.13 python=3.10.13 -y;
conda activate hs_AD_3.10.13;
#can't run these two on the same line as above
conda install ipykernel -y;
```
(or: `<python -m pip install ipykernel>`) [cite: 35]
```bash
python -m ipykernel install --user --name hs_AD_3.10.13;
```
[cite: 35]
**Install the Jupyter plugin and reload the VS Code window if it doesn’t work.** [cite: 36] *Install `ipykernel` in your conda environment, then run the command, then refresh the webpage with Jupyter in it, restart the Jupyter kernel in your notebook, and you should see the new environment.* [cite: 36]

```bash
#These changes in this order worked to get the env for AIT clio3 demo with sliders
Start from this docker image:
[docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v0.9](https://www.google.com/search?q=https://docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v0.9)

export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A;
export ARTIFACTORY_UW2_USER=hshariati
```
[cite: 37]

## My S3 Creds

```json
{
  "aws_access_key_id": "AKIA4KAGRHX6XW442I3D",
  "aws_secret_access_key": "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",
  "credentials": "[default]\naws_access_key_id=AKIA4KAGRHX6XW442I3D\naws_secret_access_key=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\n\n[text2design]\naws_access_key_id=AKIA55EBG7KC4ST5DIYA\naws_secret_access_key=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\n",
  "presigned_aws_access_key_id": "AKIA4KAGRHX6XW442I3D",
  "presigned_aws_secret_access_key": "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"
}
```
[cite: 38]

```bash
git config --global --add safe.directory /sensei-fs/users/hshariati/clio-engine/AdobeDiffusion/
cd /sensei-fs/users/hshariati/clio-engine/AdobeDiffusion/

chmod +x ./activate_dev_basemodels.sh
./activate_dev_basemodels.sh

FLASH_ATTENTION_FORCE_BUILD=TRUE pip install flash-attn

pip install clip@git+[https://github.com/openai/CLIP.git@a1d071733d7111c9c014f024669f959182114e33](https://github.com/openai/CLIP.git@a1d071733d7111c9c014f024669f959182114e33)

pip install xformers==0.0.23.post1 pip install /sensei-fs/users/mahadik/bf16_fa2/AITemplate/python/dist/aitemplate-0.3.dev0+fa2torch2.1cu12.1-py3-none-any.whl

pip install pandas

pip install torchvision==0.16.2 --no-dependencies

#didn't need to run these:
pip install torchaudio==2.1.2 --no-dependencies

pip install adobeone==0.0.6 --extra-index-url https://${ARTIFACTORY_UW2_API_TOKEN}@[artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeone-release/simple](https://www.google.com/search?q=https://artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeone-release/simple)

pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2
```
[cite: 38]
**xformers need torch2.1.2 but torchvision 0.15.1 requires torch2.0.0, when you just install the latest torchvision, it reinstalls the torch though.** [cite: 38] So I realized that these are the versions I need: [cite: 39]
```bash
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2
```
[cite: 39]

Starting from the colligo container (although Suresh says also starting from this docker: `docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v1.0`), these steps were all I needed: [cite: 39]

```bash
export ARTIFACTORY_UW2_API_TOKEN=AKCp8nGu2aaQsbfn6HNUww9JR9KKNJkX7zZCN3MP8tu5S7i6PHGSzytUMSgsxvu9c5vbRMjuT
export ARTIFACTORY_UW2_USER=cliobot

cd /sensei-fs/users/hshariati/worktree_AdobeDiffusion/hshariati/mc-dmd3
pip install adobeone==0.0.6 --index-url https://${ARTIFACTORY_UW2_USER}:${ARTIFACTORY_UW2_API_TOKEN}@[artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeone-release-local/simple](https://www.google.com/search?q=https://artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeone-release-local/simple) --no-deps
bash activate_dev_basemodels.sh
pip install openai-clip uvicorn pandas
pip install -e /sensei-fs/users/hshariati/piat
pip install -e /sensei-fs/users/hshariati/streaming

runai submit --interactive --name clio-engine2 -p asml-demos -g 1 -i [docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v0.9](https://www.google.com/search?q=https://docker-jorb-release.dr-uw2.adobeitc.com/torch_docker_v12:cuda12.3_v0.9) -l asml_project_name=asml-demo -l activity_type=productization --node-pool a100-80gb-1 --large-shm --service-type=external-url --custom-url=[https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine2/v1](https://sensei-eks01.infra.adobesensei.io/asml-demos/clio-engine2/v1) --port 6000 -e pname=asml-demos -e jname=clio-engine2 --backoff-limit 10 --command -- /bin/bash -c /sensei-fs/users/hshariati/clio-engine/AdobeDiffusion/scripts/clioengine/hs_engine_entrypoint.sh
```
[cite: 39]

```bash
[docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/colligo/colligo_ray_cluster:0.0.2](https://www.google.com/search?q=https://docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/colligo/colligo_ray_cluster:0.0.2)

/bin/bash -c "/sensei-fs/users/hshariati/hs_min_engine_entrypoint.sh"
[adobe.com/runai_department](https://www.google.com/search?q=https://adobe.com/runai_department)
```
[cite: 39]

Some other labels:
`adobe.com/runai_department`: research-ilo [cite: 39]
`adobe.com/runai_distributed_training`: False [cite: 39]
`adobe.com/runai_workload_type`: interactive [cite: 39]
`research_jack_id`: 5505 [cite: 39]

## Final What Worked for AIT 2 for Hui

**This worked with just 1 GPU too.** [cite: 40]

Using the Run:AI GUI (website): [cite: 40]
Cluster: eks01 [cite: 40]
Project: ilo-cliomd [cite: 40]
Name: hs-test2 [cite: 40]
GPUs: 8 [cite: 40]
Image: `docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/clio-and-colligo-inference-ubuntu22.04-ait-runai:0.0.3` [cite: 40]
Jupyter Notebook: Yes [cite: 40]
Node pool: a100-80gb-1 [cite: 40]
Large SHM: Yes [cite: 40]
Container Definition: [cite: 40]
Command: `/bin/bash -c "/sensei-fs/users/hshariati/hs_min_engine_entrypoint2.sh"` [cite: 40]

Environment Variables: [cite: 40]
`jname`: hs-test2 [cite: 40]
`pname`: ilo-cliomd [cite: 40]
Job URL: [cite: 40]
Container Port: 8888 [cite: 40]
Custom Url: [https://sensei-eks01.infra.adobesensei.io/ilo-cliomd/hs-test2/](https://sensei-eks01.infra.adobesensei.io/ilo-cliomd/hs-test2/) [cite: 40]

Labels: [cite: 40]
`adobe.com/runai_department`: research-ilo [cite: 40]
`adobe.com/runai_distributed_training`: False [cite: 40]
`adobe.com/runai_workload_type`: Interactive [cite: 40]
`research_jack_id`: 5505 [cite: 40]

```bash
export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A;
export ARTIFACTORY_UW2_USER=hshariati

mkdir /home/hshariati/venv
 export COLLIGO_VENVS_PATH=/home/hshariati/venv
cd /sensei-fs/users/hshariati/colligo/
python tools/env.py create --env dev
conda deactivate
. /home/hshariati/venv/dev/bin/activate
cd /sensei-fs/users/hshariati/worktree_AdobeDiffusion/hqu/test_md_ait/
./activate_dev_basemodels.sh
```
[cite: 41, 42]

Content of `/sensei-fs/users/hshariati/hs_min_engine_entrypoint2.sh`: [cite: 42]

```bash
#!/bin/bash

set -e
set -x

uname="$(whoami)"
echo $uname
sudo mkdir -p /home/$uname
sudo mkdir -p /home/user
sudo chmod 777 /home/$uname
sudo chown "$uname:users" /home/$uname
mkdir /home/$uname/.ssh
sudo chmod 700 /home/$uname/.ssh
sudo chown root /usr/bin
sudo chmod 777 /home/user
sudo chown -R $UID:100 /home/user

# add ENV vars to /etc/profile to make them available in runai port-forward / ssh shell
env | grep -v NVIDIA_REQUIRE_CUDA | grep -v PWD | grep -v HOME=/home/user | awk '{print "export "$0}' | sudo tee -a /etc/profile
env | grep -v NVIDIA_REQUIRE_CUDA | awk '{print "export "$0}' > /home/user/.bashrc

# Parse command-line arguments
for arg in "$@"; do
  if [[ "$arg" == "--NotebookApp.base_url="* ]]; then
    base_url="${arg#*=}"
  fi
done

# sudo service rsyslog restart
# sudo service ssh restart
# sudo service sssd restart
# /usr/sbin/sshd

source ./miniconda3/bin/activate

# Activate the conda environment again (this is needed after the first activation)
conda activate

# Install packages using mamba
mamba install -c conda-forge -y \
  python=3.10 \
  redis-server=7.2.3 \
  s5cmd \
  conda-pack \
  jupyter

cd /
SHELL=/bin/bash jupyter lab --port=8888 --ip=0.0.0.0 --allow-root --NotebookApp.token='' --NotebookApp.base_url=/${pname}/${jname}/ & sleep infinity
```
[cite: 43, 44, 45]

## Creating Distributed Kubernetes Cluster

Ran my script: [cite: 45]
```bash
hshariati@ip-10-43-93-5:/sensei-fs/users/hshariati$ bash hs_create_runai_cluster.sh
```
Cluster 4: [cite: 46]
Logged in. [cite: 46]

Then ran: [cite: 46]
```bash
runai describe job nemo-training-test1 -p clio-model-efficiency
```
[cite: 46]
To get the pod name. [cite: 46]

Then port forwarding: [cite: 46]
```bash
runai port-forward nemo-training-test1 -p clio-model-efficiency --port 8182:22 --address localhost --pod nemo-training-test1-master-0
```
[cite: 46]
**You need to port forward each pod separately (in a separate tab).** [cite: 46] Then you can SSH into them like this: [cite: 47]
```bash
ssh hshariati@localhost -i ~/.ssh/id_ed25519 -p 8182
```
**This is from the doc but didn't work for me.** [cite: 47, 48] I used bash instead like this: [cite: 48]
```bash
runai bash nemo-training-test1 -p clio-model-efficiency --pod nemo-training-test1-master-0
```
[cite: 48]

`hs_create_runai_cluster.sh` for backup: [cite: 48]
```bash
echo "What cluster number (1, 2, 3, 4)? (default is ${DEFAULT_CLUSTER_NUMBER})"
read CLUSTER_NUMBER
if [ ! -f "${HOME}/.kube/runai_eks0${CLUSTER_NUMBER}.yaml" ]; then
    echo "Kube configuration file for eks0${CLUSTER_NUMBER} cluster does not exist."
    echo "Download it from [https://git.corp.adobe.com/pages/adobesensei/training-framework/runai/install.html#configure-kubernetes](https://git.corp.adobe.com/pages/adobesensei/training-framework/runai/install.html#configure-kubernetes)"
    echo "Then copy it in ${HOME}/.kube/runai_eks0${CLUSTER_NUMBER}.yaml"
    exit 1
fi


CLUSTER_NUMBER=${CLUSTER_NUMBER:-${DEFAULT_CLUSTER_NUMBER}}
export KUBECONFIG="${HOME}/.kube/runai_eks0${CLUSTER_NUMBER}.yaml"

echo "Logging into Run:AI (config: $KUBECONFIG)"
(set -x; runai login || true)

runai submit-pytorch --large-shm \
-e NCCL_SOCKET_IFNAME=eth0 \
-e NUM_GPUS=8 -e NUM_NODES=4 \
-g 8 --workers 3 \
-e FI_PROVIDER=efa -e FI_EFA_USE_DEVICE_RDMA=1 \
--extended-resource [vpc.amazonaws.com/efa=4](https://www.google.com/search?q=https://vpc.amazonaws.com/efa%3D4) \
--extended-resource hugepages-2Mi=2048Mi \
--backoff-limit 4 --node-pool a100-80gb-1 \
-i nvcr.io/nvidia/nemo:24.01.01 \
-p clio-model-efficiency \
-l research_jack_id=5333 \
-l "asml_project_name=clio-model-efficiency" \
--name nemo-training-test2 -- sleep infinity
```
[cite: 49, 50]
```