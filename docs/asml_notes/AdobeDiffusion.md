```markdown
## Make CI/CD Faster

To make CI/CD faster on AdobeDiffusion, navigate to [https://clio-adobe.ci.corp.adobe.com/job/Gentech/job/clio-sdk-gpu/](https://clio-adobe.ci.corp.adobe.com/job/Gentech/job/clio-sdk-gpu/), click on "Build With Parameters", and under the "jenkinsfile\_branch" section, add the name of your feature branch[cite: 1].

To check the status, click on "open blue ocean homepage" and then on your run (usually the last one)[cite: 2]. It shows the last commit in your branch[cite: 3]. Then go to artifacts, pipeline log, and search for "fail" or "error"[cite: 3].

## Debug Unit Tests

First, ensure you can run the test in the command line with `pytest path_to_test.py`[cite: 3]. Then, go to `settings.json` (`/sensei-fs/users/hshariati/AdobeDiffusion/.vscode/settings.json`) and add a block like this:

```json
"python.testing.pytestArgs": [
    "/sensei-fs/users/hshariati/AdobeDiffusion/cliocore/tests"
],
```

Refresh the tests (flask icon) and ensure "unhidden all tests" or "show hidden tests" is enabled[cite: 3]. You might encounter an issue where tests are not found because it appends "gpu0" at the end[cite: 4]. Comment out `# @pytest.mark.gpu`[cite: 5]. After this, you can place your cursor on the test and debug it[cite: 5].

## Issues with Using Wrong GPU

There are two places where you can specify the GPU[cite: 6]:

1.  **In your docker compose:** This only applies when you start the Docker container[cite: 7].

    ```yaml
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              #count: all
              device_ids:
              - "7"
              capabilities: [ gpu ]
    environment:
      - SSHD_PORT=${SSHD_PORT}
    ```
2.  **Inside launch.json:** Under the "Python: Current File" section, you can specify the GPU. This can be applied during runtime as long as you are launching from the current file[cite: 8]. Note that there are `settings.json` for the workspace and one for AdobeDiffusion. You can select the configuration by clicking on the dropdown next to the play button and choosing "Add config"[cite: 8].

    ```json
    {
        "name": "Python: Current File",
        "type": "python",
        "request": "launch",
        "program": "${file}",
        "console": "integratedTerminal",
        "justMyCode": true,
        "args": [
            "--gpus",
            "7,",
        ],
    }
    ```

## Start and Restart Your AdobeDiffusion Docker Container

### Start the Clio Demo Container (env)

1.  Pull the repository on the devbox in `/sensei-fs/users/hshariati/`[cite: 10].
2.  `cd /sensei-fs/users/hshariati/`[cite: 10].
3.  `chmod 777 AdobeDiffusion`[cite: 10].
4.  `cd /sensei-fs/users/hshariati/AdobeDiffusion`[cite: 10].
5.  Make sure to add the GPU you want to target to `docker-compose` (these changes are stashed)[cite: 10, 12].
6.  `USER=hshariati make run-devbox-dev CLIO_SDK_VERSION=2.9.1 SSHD_PORT=4046`[cite: 10]. This runs the `run-devbox-dev` tag from [https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/dev/makefiles/clio_dev.mk](https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/dev/makefiles/clio_dev.mk)[cite: 11].
7.  `docker exec -it -u hshariati clio-dev-hshariati /bin/bash`[cite: 11].
8.  Then continue from step 5 under "Restart your clio container"[cite: 11].

### Restart Your Clio Container

If your container gets killed (e.g., the box restarts), you cannot simply use `docker container start` because this will not set the ports properly[cite: 11]. Instead:

1.  Make sure to add the GPU you want to target to `docker-compose` (these changes are stashed)[cite: 12].
2.  Edit [https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/dev/makefiles/clio_dev.mk](https://git.corp.adobe.com/Clio/AdobeDiffusion/blob/dev/makefiles/clio_dev.mk) under the `run-devbox-dev` tag so that the new container name is used[cite: 12]. You can rename `clio-dev-$(USER)` to `clio-dev2-$(USER)`[cite: 13].
3.  Rename `/home/hshariati` (on the devbox) to `hshariati_backup`[cite: 13].
4.  Run the command from step 6 above: `USER=hshariati make run-devbox-dev CLIO_SDK_VERSION=2.9.1 SSHD_PORT=4046`[cite: 13].
5.  Copy the content of `hshariati_backup` into `/home/hshariati`[cite: 13].
6.  If you encounter a "cannot find 'aitemplate' module" error, and you are on the `MD from MoE_for_MD Branch`, follow the instructions in the "Running Things" section[cite: 13].
7.  Reinstall the necessary VS Code extensions:
    1.  Python Extension Pack by Don Jayamanne[cite: 13].
    2.  Python Test Explorer for Visual Studio Code (by Little Fox Team)[cite: 13].
    3.  Jupyter (by Microsoft)[cite: 13].
    4.  GitHub Copilot (by GitHub)[cite: 13].
8.  If you have issues with GitHub or see the wrong color prompt (white) when you do `ssh my_devbox`, your `/home/hshariati` folder in the devbox might not be mounted correctly. Ensure there is no folder `/home/hshariati/hshariati`. If it exists, delete the inner one and move the content out[cite: 14].

*You can install AD and other libraries in a conda environment inside your Docker container. By selecting the Python kernel in VS Code, you automatically connect to the conda environment[cite: 14]. Just use `which python` after activating the environment to see the Python kernel path[cite: 15].*

## Install Conda on Dev Box

To install conda on the dev box, refer to the instructions for installing conda on a Run:AI box. The password for sudo is "sensei"[cite: 16].

## Connect to Devbox Container Using Jupyter Lab

1.  Start Jupyter Lab from outside the container but on your devbox. Change `8070` to your desired port[cite: 16].
    ```bash
    USER=hshariati JUPYTER_PORT=8070 make run-jupyter
    ```
2.  Start Jupyter from VS Code[cite: 17]. Just create a file with the `.ipynb` extension[cite: 18].
3.  When prompted to select a kernel, choose Python[cite: 18]. Ensure it's pointing to `/opt/venv/bin/python`[cite: 19].
4.  You can get the IP address of the running Jupyter kernel by running `jupyter notebook list` in the VS Code terminal[cite: 19, 20].
5.  If you prefer not to use VS Code:
    1.  From your local machine, run the command below to make Jupyter accessible on your machine. Ensure the port matches the one used above[cite: 20, 21].
        ```bash
        ssh -N -L 8080:localhost:8070 Session-d65c2cef-92b8-4c9b-a526-375a6ddfd838
        ```
        ***Use your LDAP password if prompted[cite: 21]. This command should not return[cite: 21, 22]. If it does, change the ports, including the `8080` one[cite: 22].
    2.  Now you can go to `http://localhost:8080` in your browser (on your laptop)[cite: 23]. If you need a password, use `sensei`[cite: 24].

## Running Things

For MD from MoE\_for\_MD Branch (for getting rid of the "cannot find aitemplate" error):

1.  To change the Python path, use `/opt/venv/bin/python`. You can change this by clicking on Python in the bottom right corner of VS Code[cite: 24, 25].
2.  ```bash
    export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A
    export ARTIFACTORY_UW2_USER=hshariati
    ```
3.  `./uninstall_clio.sh`[cite: 25].
4.  `./activate_dev_basemodels.sh`[cite: 25].
5.  `pip uninstall AITemplate`
    ```bash
    pip install https://${ARTIFACTORY_UW2_API_TOKEN}@[artifactory-uw2.adobeitc.com/artifactory/pypi-clio-release-local/aitemplate/0.3.dev0/aitemplate-0.3.dev0-py3-none-any.whl](https://www.google.com/search?q=https://artifactory-uw2.adobeitc.com/artifactory/pypi-clio-release-local/aitemplate/0.3.dev0/aitemplate-0.3.dev0-py3-none-any.whl)
    ```
6.  If you want to install the full colligo:
    ```bash
    pip install -U colligo.sdk torch --extra-index-url https://${ARTIFACTORY_UW2_API_TOKEN}@[artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple](https://www.google.com/search?q=https://artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple)
    ```
7.  Refer to this Slack post for details: [https://adobesearch.slack.com/archives/C04C3LJLPFV/p1698961807081719](https://adobesearch.slack.com/archives/C04C3LJLPFV/p1698961807081719)[cite: 25].

```bash
pip install https://${ARTIFACTORY_UW2_API_TOKEN}@[artifactory-uw2.adobeitc.com/artifactory/pypi-clio-release-local/aitemplate/0.3.dev0+fa2torch2.1cu12.1/aitemplate-0.3.dev0+fa2torch2.1cu12.1-py3-none-any.whl](https://www.google.com/search?q=https://artifactory-uw2.adobeitc.com/artifactory/pypi-clio-release-local/aitemplate/0.3.dev0%2Bfa2torch2.1cu12.1/aitemplate-0.3.dev0%2Bfa2torch2.1cu12.1-py3-none-any.whl)
```

## Run Commands

3.  To run something, you can use the inference app directly or the model comparison, which is built on top of the inference app[cite: 25].
4.  Look at `.vscode/launch.json` for an example of how to use model comparison[cite: 26].
5.  You can also use the inference app directly. You can put what is in the GitHub documentation in a `.py` script[cite: 26].
6.  You can then go to the Run and Debug section of VS Code and select "Python: Current File"[cite: 26].
7.  Another way is to create a `.ipynb` file in VS Code for Jupyter interactivity[cite: 26].

## Get VS Code Peak Working for Project

1.  Click on `File` -> "Open Workspace from File…"[cite: 26].
2.  Open `/sensei-fs/users/hshariati/AdobeDiffusion/.vscode/AdobeDiffusion.code-workspace`. If this is a new project, copy the sample and rename it to this one[cite: 26, 27].
3.  It will fail to connect to the remote. To fix this, open a separate terminal and do `ssh my_devbox_cont`, then enter your LDAP password[cite: 28]. Once you can access the box from your terminal, VS Code can too[cite: 29].
4.  To open the terminal, use `Ctrl+``[cite: 29, 30].
5.  Make sure to install the "Python Extension Pack by Don Jayamanne"[cite: 30].
6.  Install the Jupyter extension pack by Microsoft[cite: 30].
7.  ***After the migration to GitHub, I had to change the URLs in `.vscode/settings.json` and `.vscode/AdobeDiffusion.code-workspace` like this: [cite: 30, 31]

    ```diff
    -    "github-enterprise.uri": "[https://git.corp.adobe.com](https://git.corp.adobe.com)",
    +    "github-enterprise.uri": "[https://github.com/Adobe-Firefly/](https://github.com/Adobe-Firefly/)",
    ```

## If You Get This Error

Remove `prompty` from `apps/model_comparison/pyproject.toml`[cite: 31].

[https://github.com/Adobe-Firefly/AdobeDiffusion/commit/bd071e68a97ccef317e01f90db69db0e075f9ee4](https://github.com/Adobe-Firefly/AdobeDiffusion/commit/bd071e68a97ccef317e01f90db69db0e075f9ee4) [cite: 31]
```