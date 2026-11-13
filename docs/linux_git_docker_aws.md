```markdown
# General Tips and Commands

## Monitor GPUs

```bash
nvitop
pip install nvitop
```

## Github

To take a new worktree branch from another branch:

```bash
git worktree add -b <new_branch> <path/to/new_worktree> <existing_branch>
```

**(this didn't work for me) To carry over the changes in existing worktree branch to new worktree branch:** Make sure you are inside the worktree branch that has your uncommitted changes. And then run the command above. Instead, I just stashed the changes in the first branch and unstashed them in the new branch.

To checkout out a branch in worktree:

```bash
git worktree add  <existing_branch> <path/to/where you want it in worktree>
```

Has this changed? Cuz I had to do:

```bash
git worktree add  <path/to/where you want it in worktree> <existing_branch>
git worktree add ../workTree/alse/DiTInference alse/DiTInference
```

To remove a worktree branch (locally):

```bash
git worktree remove <existing_branch>
```

**This removes the worktree folder.** And then you can remove the branch with:

```bash
git branch -d branchName
```

**Cleanup untracked files** (f is forced d is directories):

```bash
git clean -fd
```

To stash only some of the changed files:

```bash
git stash push -m "Your stash message" -p file1 file2 file3
```

To Ignore the validation of adobe diffusion on your commit:

```bash
git commit -m "changes for mc data" --no-verify
```

Add and Commit changed tracked files at the same time:

```bash
git commit -am "Your commit message"
```

See changes in stashed files: `"git stash show -p stash@{1}"` lists the changes in all the files in this stash. If you wanna see changes in just one of the files you can use:

```bash
git show stash@{1} -- <file_path>
```

Fancy PR review: Just copy the PR number in this URL: [https://vscode.dev/github/Adobe-Firefly/colligo/pull/3230](https://vscode.dev/github/Adobe-Firefly/colligo/pull/3230)

Send empty commit to trigger CI:

```bash
git commit --allow-empty -m "Trigger CI/CD"
```

## Linux

Change permission of someone else's files:

```bash
sudo runuser -u alse -- chmod 777 -R /sensei-fs/projects/firefly/clio/runai_training/dmd_dmd-v11-alse-12
```

Generally, after `"sudo runuser -u alse -- "`, you can add whatever command you want.

See what process is using a port:

```bash
fuser 6379/tcp
```

Disk space free and usage:

* `du -h /path/` shows disk usage
* `df -h /path/.` Shows free disk space

**This will show you the sizes of files in a directory sorted by largest:**

```bash
du -h --max-depth=1 . | sort -hr
```

**This will exclude a certain directory:**

```bash
du -h --max-depth=1 --exclude=/sensei-fs/ .
```

You can also pass this a list:

```bash
du -h --max-depth=1 --exclude=<directory1> --exclude=<directory2> --exclude=<directory3> .
```

**when running out of disk when installing packages (even though conda env is on a partition that has space) I ran this command which fixed the issue:**

```bash
python3 -m pip cache purge
```

**this is because pip stores some stuff in `/tmp`**

### Docker Specific

**this shows you how much each container uses:**

```bash
docker ps --size
```

**this shows total that docker system uses (but usually it's the containers that use the most)**

```bash
docker system df
```

**To see the shm memory available to your container do:**

```bash
docker inspect <container_id_or_name>
```

Then look for: `"HostConfig": { "ShmSize": 67108864 }`. Then convert this from bytes to gb.

### On Going Monitoring

This shows the usage of `/mnt/localssd/mosaic` directory using:

```bash
watch -n0.1 df -h /mnt/localssd/mosaic/
```

or

```bash
watch -n0.1 du -csh /mnt/localssd/mosaic
```

## To Kill Processes

```bash
kill $(ps -e | grep mds | awk '{print $1}')
sudo pkill -9 -f clio
```

## Ssh Key Expiring Restart Ssh Service

1.  Go to ldap click on services, then ssh key then manage ssh key.
2.  Generate a new ssh key (following the instructions ldap gives you) and upload the public one.
3.  Connect to your devbox using `"ssh hshariati@Session-d65c2cef-92b8-4c9b-a526-375a6ddfd838"` and then replace the keys in the `.ssh` folder with the new one.
4.  Go to github, delete the existing key and add the new one. Note that you will have to add two on github one for sign in and one for authentication.
5.  You can also restart the ssh services if you see any error.
    a. For devbox use: `sudo service ssh restart`
    b. For mac use:
        i. `sudo launchctl stop com.openssh.sshd`
        ii. `sudo launchctl start com.openssh.sshd`

## tmux screen

Tmux is just like screen but newer. Install using:

```bash
sudo apt-get install tmux
```

Create a session using:

```bash
tmux
```

To name your session:

```bash
tmux new -s Session1
```

See list of running sessions:

```bash
tmux ls
```

Connect to running sessions:

```bash
tmux attach -t 0
```

Detach from session you're inside: `Ctrl+B` and then press: `D`

### Screen

Create session with:

```bash
Screen -S sessionName
```

Connect using:

```bash
Screen -r sessionName
```

Create tabs using: `Ctrl+a` and `c`

See different tabs: `Ctrl+a` + `" `

Go up in the cmd logs: `Ctrl+a` + `scape` (or `]`)

## Search

```bash
find . -type f -iname "*sd*"
```

Searchers for any files that have sd (case insensitive) in them. In all directories starting from `.`.

## Docker

```bash
docker login -u $ARTIFACTORY_UW2_USER -p $ARTIFACTORY_UW2_API_TOKEN docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com
```

`docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/clio-and-colligo-inference-ubuntu22.04-ait-runai:0.0.3`

### To Login to Adobe Docker

To use docker in dev box:

**Summery:**

```bash
export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A;
export ARTIFACTORY_UW2_USER=hshariati
```

This is the registry that works with runai:

```bash
docker login -u $ARTIFACTORY_UW2_USER -p $ARTIFACTORY_UW2_API_TOKEN docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com
```

To login to this other registry use:

```bash
docker login -u $ARTIFACTORY_UW2_USER -p $ARTIFACTORY_UW2_API_TOKEN docker-clio-release.dr-uw2.adobeitc.com
```

```bash
docker pull [docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/colligo/colligo_ray_cluster:0.0.1](https://www.google.com/search?q=https://docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/colligo/colligo_ray_cluster:0.0.1)
```

```bash
docker run -it --name my_container -u $(id -u):$(id -g) -v /sensei-fs:/sensei-fs -v $(pwd):/local -v /mnt/localssd/hshariati/.clio_dev_cache:/home/hshariati/.cache -v /mnt/localssd/hshariati/.clio_dev_user_data:/home/hshariati/.clio_user_data -v /mnt/localssd/hshariati/.clio_dev_downloads:/home/hshariati/.clio-downloads [docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/colligo/colligo_ray_cluster:0.0.1](https://www.google.com/search?q=https://docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/colligo/colligo_ray_cluster:0.0.1)
```

```bash
docker run -it --name my_container --userns=host -v /sensei-fs:/sensei-fs -v $(pwd):/local -v /mnt/localssd/hshariati/.clio_dev_cache:/home/hshariati/.cache -v /mnt/localssd/hshariati/.clio_dev_user_data:/home/hshariati/.clio_user_data -v /mnt/localssd/hshariati/.clio_dev_downloads:/home/hshariati/.clio-downloads [docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/colligo/colligo_ray_cluster:0.0.1](https://www.google.com/search?q=https://docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/colligo/colligo_ray_cluster:0.0.1)
```

```bash
docker run -it --name my_container --userns=host -u $(id -u):$(id -g) -v /sensei-fs:/sensei-fs -v $(pwd):/local -v /mnt/localssd/hshariati/.clio_dev_cache:/home/hshariati/.cache -v /mnt/localssd/hshariati/.clio_dev_user_data:/home/hshariati/.clio_user_data -v /mnt/localssd/hshariati/.clio_dev_downloads:/home/hshariati/.clio-downloads [docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/colligo/colligo_ray_cluster:0.0.1](https://www.google.com/search?q=https://docker-matrix-experiments-snapshot.dr-uw2.adobeitc.com/colligo/colligo_ray_cluster:0.0.1)
```

```bash
sudo docker run -it --name hs_cont --userns=host -v /sensei-fs:/sensei-fs -v $(pwd):/local -v /mnt/localssd/hshariati/.clio_dev_cache:/home/hshariati/.cache -v /mnt/localssd/hshariati/.clio_dev_user_data:/home/hshariati/.clio_user_data -v /mnt/localssd/hshariati/.clio_dev_downloads:/home/hshariati/.0.0.1
```

```bash
docker exec -it my_container /bin/bash
```

```bash
docker run -it --name my_container [docker-clio-release.dr-uw2.adobeitc.com/inference/clio-and-colligo-inference-ubuntu22.04-ait:latest](https://www.google.com/search?q=https://docker-clio-release.dr-uw2.adobeitc.com/inference/clio-and-colligo-inference-ubuntu22.04-ait:latest)
```

To change the location of docker:

```bash
sudo systemctl stop docker

sudo cp -au /var/lib/docker /path/to/new_partition/docker

sudo mkdir -p /etc/docker
sudo touch /etc/docker/daemon.json

{
    "data-root": "/path/to/new_partition/docker"
}

sudo systemctl restart docker

docker info | grep "Docker Root Dir"
```

To change the location of docker temp file specially when docker image save export to tar ball:

```bash
#export DOCKER_TMPDIR="/mnt/bigdrive/docker-tmp"
```

TO rename a docker:

```bash
docker tag <existing_image> <new_registry>/<new_image_name>:<tag>
```

Use this Registry for runai: `docker-jorb-release.dr-uw2.adobeitc.com`

Like this: `docker-jorb-release.dr-uw2.adobeitc.com/clio-and-colligo-inference-ubuntu22.04-ait:0.0.1"`

### For Nvidia

```bash
ngc config set

docker login nvcr.io Username: $oauthtoken Password: N3J1dmpncHU5cDFoaWhpbDUwOWJxNDNyYnI6YzQ4ZDg3MjItOTk0Ni00N2NlLWFkNjctZjY2MGI0MTI1NmUz
```

Username: `hoomanblack67`

***Above key didn't work. So I generated a personal key:*** `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`

To install colligo ml dependencies directly in the container use this command:

```bash
sudo apt update
sudo apt install redis-server
pip install -U -r envs/requirements.lock.txt
```

```bash
# RUN bash ./install_conda.sh ./miniconda3
# RUN . ./miniconda3/bin/activate && conda activate && mamba install -c conda-forge -y \
#   python=3.10 \
#   redis-server=7.2.3 \
#   s5cmd \
#   conda-pack \
#   jupyter

# RUN echo ". ~/miniconda3/bin/activate" >> .bash_profile
# RUN echo "conda activate" >> .bash_profile


# Make sure these are available when conda is not active
# (we cannot install them with apt, they are not available there)
USER root
# RUN ln -s ${USER_HOME}/miniconda3/bin/s5cmd /usr/bin/s5cmd
# RUN ln -s ${USER_HOME}/miniconda3/bin/redis-server /usr/bin/redis-server
# RUN ln -s ${USER_HOME}/miniconda3/bin/redis-cli /usr/bin/redis-cli
```

## Final Docker Creation

1.  I used the `colligo/docker/dev`, modified the `make.py` to create image and container with the name I wanted. Then just ran the script normally.
2.  Then I installed jupyter (which is needed by runai)
3.  Then I ran: `"pip install -U -r envs/requirements.lock.txt"` to install colligo
4.  Then I installed AD with `"./activate_dev_base_models.sh"`
5.  Then I removed any python from `/usr/bin` and `/usr/local/bin` (python, python3, python3.10, etc)
6.  `sudo apt-get install rsync`
7.  `sudo rsync -av --ignore-existing /home/hshariati/miniconda3/bin/* /usr/bin/`

    ```bash
    for file in /home/hshariati/miniconda3/bin/python*;
    do
        sudo ln -s "$file" /usr/bin/$(basename "$file")
    Done;
    for file in /home/hshariati/miniconda3/bin/pip*;
    do
        sudo ln -s "$file" /usr/bin/$(basename "$file")
    done
    ```
8.
9.  `sudo rsync -av --ignore-existing /home/hshariati/miniconda3/lib/* /usr/lib/`
10. And removed the lines in `.bash_profile`:

    ```bash
    #. ~/miniconda3/bin/activate
    #conda activate
    ```
11. To add a new user you need to run these steps:
    a. Get their UID from devbox:

    ```bash
    hshariati@ip-10-43-2-178:~$ id -u hqu
    122388
    ```
    b. `USER_NAME="hqu"`
    c. `USER_UID=122388`, for hshariati, this is 144328

    ```bash
    USER_HOME=/home/"${USER_NAME}"

    mkdir -p "${USER_HOME}"/code

    mkdir -p /run/sshd

    adduser --group "${USER_NAME}"

    adduser --ingroup "${USER_NAME}" --home "${USER_HOME}" --uid "${USER_UID}" "${USER_NAME}"

    usermod -aG sudo,${USER_NAME},docker,users,adobe_research_team,neural_filters_platform "${USER_NAME}"

    echo "${USER_NAME}:${USER_NAME}" | chpasswd

    chown -R  "${USER_NAME}:${USER_NAME}" "${USER_HOME}"
    ```
    d.
    e. If you cannot access Sensei-AdobeReserachTeam folders, these lines (from colligo Dockerfile) will fix that issue as well.
    f. Sdf
    g. Sdf
    h. Sdf
    i. Sdf
    j. sfd

```bash
shariati@7bc0cd4ae618:/sensei-fs/users/hshariati/worktree_AdobeDiffusion/hqu/test_md_ait$ python scripts/run_inference_app_md.py
The cache for model files in Transformers v4.22.0 has been updated.
Migrating your old cache. This is a one-time only operation.
You can interrupt this and resume the migration later on by calling `transformers.utils.move_cache()`.
0it [00:00, ?it/s]
[2024-03-06 20:41:31,626] [INFO] [real_accelerator.py:161:get_accelerator] Setting ds_accelerator to cuda (auto detect)
2024-03-06 20:41:33.536921: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory; LD_LIBRARY_PATH: /home/hshariati/miniconda3/lib/python3.10/site-packages/cv2/../../lib64:
2024-03-06 20:41:33.536950: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
colligo-sdk is not installed. Cannot be used.
Available Engine folder: sensei='/sensei-fs/users/sharmaa/clio3/prod4_20_a100_v6/' uw2=None raw='/sensei-fs/users/sharmaa/clio3/prod4_20_a100_v6/'
Initializing AIT parameters
```

## AWS

### Look at a Bucket

On cmd (say colligo env) you can ls a s3 bucket like this:

```bash
asw s3 ls s3://clio-web-app/video/data_set/
```

Also you can sometimes do this (but it doesn’t work for our buckets on ss eval ones):

```json
"url": " [https://clio-web-app.s3.amazonaws.com/lite_eval/aws_genfill__nm_cliomd_general_background_tinp/13504_2.png](https://clio-web-app.s3.amazonaws.com/lite_eval/aws_genfill__nm_cliomd_general_background_tinp/13504_2.png)",
  "uri": " s3://clio-web-app/lite_eval/aws_genfill__nm_cliomd_general_background_tinp/13504_2.png",
```

we need to extract key from uri `lite_eval/aws_genfill__nm_cliomd_general_background_tinp/13504_2.png` and suffix it to `https://clio-web-app.s3.amazonaws.com/`.

So:

`s3://clio-web-app/video/data_set/animated_addedaddedJun2024/videos/99786-720.mp4`

Should become:

`https://clio-web-app.s3.amazonaws.com/video/data_set/animated_addedaddedJun2024/videos/99786-720.mp4`

### Copy the Data to Local

```bash
aws s3 cp  s3://clio-web-app/lite_eval/video_initial_result/multiple_fps/0000.mp4 .
```

For folders use this:

```bash
aws s3 cp --recursive s3://[clio.corp.adobe.com/training_logs//sensei-fs/users/kduarte/mori_training_logs_test/kduarte-clineto-v2-5b-stage2-exp-3/checkpoints/ckpt_step00490000.pth](https://www.google.com/search?q=https://clio.corp.adobe.com/training_logs//sensei-fs/users/kduarte/mori_training_logs_test/kduarte-clineto-v2-5b-stage2-exp-3/checkpoints/ckpt_step00490000.pth) .
```


# AWS roles users IAM (Identity and access managment)

### to get the role run this on a machine
colligo@pluto-prod-hshariati-new-glimmer-1-0:/mnt/localssd/genie$ aws sts get-caller-identity
{
    "UserId": "AROAQ3EGP2NKLALKSC6WO:i-044d79f981fb2c524",
    "Account": "058264114004",
    "Arn": "arn:aws:sts::058264114004:assumed-role/colligo-laser01-ng-role-uw2/i-044d79f981fb2c524"
}
** Above shows assumed-role/RoleName/SessionName
so in above we have assumed-role/colligo../i-044d...
Contains user/UserName if you're using an IAM user
ends iwth root if we're using root credentisls (so avoid this)

### workaround for SQS
1. Create an IM role glimmer_pluto_role_sqs
2. give the role permission for SQS
3. File a Jira ticket and say let the pluto-lazer trust this role. Put in AI platform users. 
4. Onces paul is done, inside the pluto instance you can assume that role. Ask chat GPT how to do this. 
5. In the boto3 you can use the assume role to create a client for SQS. 
6. Make sure to test indurance (since credentials need to auto refresh)


### Assuming a role in python script
```python
import boto3

role_arn = "arn:aws:iam::760168217311:role/glimmer_sqs_pluto_role"
sts = boto3.client("sts", region_name="us-west-2")
creds = sts.assume_role(RoleArn=role_arn, RoleSessionName="glimmer-session")["Credentials"]

session = boto3.Session(
    aws_access_key_id=creds["AccessKeyId"],
    aws_secret_access_key=creds["SecretAccessKey"],
    aws_session_token=creds["SessionToken"],
    region_name="us-west-2",
)

print(session.client("sts").get_caller_identity())

sqs = session.client("sqs")
print(sqs.create_queue(QueueName="hs_test_queue", Attributes={"ReceiveMessageWaitTimeSeconds": "10"}))
```

### Assuming a role on a machine to make sure it auto refresh
Add below to ~/.aws/config
```bash
[profile glimmer-sqs-role]
role_arn = arn:aws:iam::760168217311:role/glimmer_sqs_pluto_role
credential_source = Ec2InstanceMetadata
region = us-west-2
```