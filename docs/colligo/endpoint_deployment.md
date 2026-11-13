```markdown
# Deploying to Eval Endpoint

**Documentation:** [https://docs.ai.corp.adobe.com/aidoc/inference-platform/tutorials/serve.html#via-ci-devEssentially](https://docs.ai.corp.adobe.com/aidoc/inference-platform/tutorials/serve.html#via-ci-devEssentially) [cite: 1]

## Pre-deployment Checks [cite: 1]

0. If you want to check that everything is good pre deployment run: [cite: 1]

   ```bash
   rm -rf .mypy_cache
   dmypy kill
   ./m deps.lock
   python tools/lint.py
   ./m lint --check
   ```

## Adding New Models [cite: 1]

1. If you are adding new models you need to add them here: [https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/charts/rhode/modules/applications/gen-video/deploy_2_hx00.yaml](https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/charts/rhode/modules/applications/gen-video/deploy_2_hx00.yaml) [cite: 1]

   Note that the above file controls everything A100, H100, H200, the other files here (p4de, p5, p5en) will all be removed. [cite: 1]

   **Use template:** [cite: 2]
   * `_templates.gpu_hx00_x2` means 2 GPUs like for DiT models [cite: 2]
   * `_templates.gpu_hx00_x1` means 1 GPU like for other models [cite: 2]
   * `_templates.gpu_p4d_x1` means 1 A100 [cite: 2]
   * `_templates.gpu_p4d_x2` means 2 A100 [cite: 2]

   Note that the replicas here can all remain 0 because these will all get overridden by the values chart (below). [cite: 2]

## Create Init Script [cite: 3]

2. Create init script (run this command in your colligo folder) [cite: 3]
   ```bash
   ./m package.rhode --spec <application name>
   ./m package.rhode --spec firefly_clineto
   ./m package.rhode --spec foundry
   ```

## Add Init Script to Helm Chart [cite: 3]

3. Add your init script in the relevant helm chart. [cite: 3]

   **For Eval:** [https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/dev/or2/e851/gen-video-eval/values.yaml](https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/dev/or2/e851/gen-video-eval/values.yaml) [cite: 4]
   **For Experimental:** [https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/dev/or2/e851/gen-video-exp/values.yaml](https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/dev/or2/e851/gen-video-exp/values.yaml) [cite: 4]

## Edit Replicas [cite: 4]

4. In the same file, edit the number of replicas for each model. [cite: 4]

   **For replica management:** Basically don't take any more GPUs than what your env already has. [cite: 5]
   Remove from one model to add to another. [cite: 6]

## Update Helm Chart Version (If New Models Added) [cite: 6]

5. If you added new models (in step 1) then you need to update the helm chart version (if you just changed the init script and replica counts without adding new models you don't need this step). [cite: 6]

   Change this: [https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/dev/or2/e851/gen-video-eval/Chart.yaml#L15](https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/dev/or2/e851/gen-video-eval/Chart.yaml#L15) [cite: 7]
   to this: [https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/charts/rhode/Chart.yaml#L6](https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/charts/rhode/Chart.yaml#L6) [cite: 7]

   Above will require to step deployment. [cite: 7]
   First PR will update the version in rhode/Chart.yaml . And then you need another PR to copy that version into gen-video-eval/Chart.yaml. [cite: 8]
   Or you can change gen-video-eval/Chart.yaml to reference whatever is in rhode/Chart.yaml like this (this is the proper way): [cite: 9]
   ```yaml
   version: "^1.0.0"
    repository: "file://../../../../../../charts/rhode"
   ```
   Basically revert of this PR: [https://git.corp.adobe.com/firefly/colligo-deploy/pull/12243/files](https://git.corp.adobe.com/firefly/colligo-deploy/pull/12243/files) [cite: 9]

## Deploy to Dev [cite: 9]

6. If you want to deploy to dev: [https://git.corp.adobe.com/firefly/colligo-deploy/tree/main/k8s/helm/dev/or2/e851/gen-video](https://git.corp.adobe.com/firefly/colligo-deploy/tree/main/k8s/helm/dev/or2/e851/gen-video) [cite: 9]
7. sd [cite: 9]

chart need to change? [cite: 9]
[https://git.corp.adobe.com/firefly/colligo-deploy/blob/a287c989484eaf1301cb098a212abc7426295fbc/k8s/helm/stage/or2/e851/gen-video/Chart.yaml](https://git.corp.adobe.com/firefly/colligo-deploy/blob/a287c989484eaf1301cb098a212abc7426295fbc/k8s/helm/stage/or2/e851/gen-video/Chart.yaml) [cite: 10]
1.4.970 is the latest, you can use - will match dev [cite: 10]
@hshariati I updated the chart [cite: 10]
[https://git.corp.adobe.com/firefly/colligo-deploy/pull/12779](https://git.corp.adobe.com/firefly/colligo-deploy/pull/12779) [cite: 10]
Also, please going forward, use this format for PR titles [cite: 10]
Saved for later [cite: 10]
[gen-video][stage] firefly_clineto-version=0.0.1-main.33454-commit=39ad5f2cFor any environment, this allows us to find deployments easier [cite: 10]

## Existing Environments 


You can click on these links and go to these URLs. But you cannot put the in colligo.dev.yaml  
** You can also put these URLS in firefly (to point ff.com to these)
* DEV - clio-video  [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/) 
* STAGE - clio-video  [https://gen-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/) 
* Eval - gen-video-eval  [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/) 
* EXP: [https://gen-video-exp-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-exp-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/) 

### You can put these URLS in your colligo.dev.yaml: 
To go from endpoint URL to what you can put in your colligo.dev.yaml 
You need to remove the colligov2 and the corp. 
* DEV - clio-video  [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/) 
* STAGE - clio-video  [https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-stage.ethos851-stage-or2.ethos.adobe.net/) 
* Eval - gen-video-eval  [https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-dev.ethos851-stage-or2.ethos.adobe.net/) 
* EXP: [https://gen-video-exp-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-exp-dev.ethos851-stage-or2.ethos.adobe.net/) 

Note that we have changed clio-video to gen-video So you actually should use these: 
debug UI for dev will be  [https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/) 
and in colligo yaml file the new endpoint would be endpoint: [https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-dev.ethos851-stage-or2.ethos.adobe.net/) . 

## Examples [cite: 12]

**Example for eval endpoint:** [cite: 12]
For this endpoint-->  [https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-eval-colligov2-dev.corp.ethos851-stage-or2.ethos.adobe.net/) [cite: 12]
[https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/dev/or2/e851/gen-video-eval/Chart.yaml#L15](https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/dev/or2/e851/gen-video-eval/Chart.yaml#L15) [cite: 12]
So basically you change the version in above, to this one: [cite: 12]
to this:  [https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/charts/rhode/Chart.yaml#L6](https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/charts/rhode/Chart.yaml#L6) [cite: 12]

this one for updating the init_script -->  [https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/dev/or2/e851/gen-video-eval/values.yaml](https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/dev/or2/e851/gen-video-eval/values.yaml) [cite: 12]

**Example for release endpoint:** [cite: 12]
For this endpoint-->  [https://gen-video-release-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/](https://gen-video-release-colligov2-stage.corp.ethos851-stage-or2.ethos.adobe.net/) [cite: 12]
the one below for updating the chart version: [cite: 12]
[https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/stage/or2/e851/gen-video-release/Chart.yaml#L14](https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/stage/or2/e851/gen-video-release/Chart.yaml#L14) [cite: 12]
this one for updating the init_script -->  [https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/stage/or2/e851/gen-video-release/values.yaml](https://git.corp.adobe.com/firefly/colligo-deploy/blob/main/k8s/helm/stage/or2/e851/gen-video-release/values.yaml) [cite: 12]

## Other Deployments [cite: 12]

### Hs notes How to make a new deploy deploying deployment [cite: 12]
To dev deploy from a branch my 1st PR([https://git.corp.adobe.com/firefly/colligo-deploy/pull/518/files](https://git.corp.adobe.com/firefly/colligo-deploy/pull/518/files))  push 4 files into colligo-deploy repo: [cite: 12]
1. .ethos.yaml [cite: 12]
2. charts/rhode/modules/applications/kineto/deploy_2.yaml [cite: 12]
   Specifies the init_script which is what we pushed into s3 with package.py [cite: 13]
   Also the name and types of GPUs [cite: 13]
   Also how many replicas from [cite: 13]
3. k8sk8s/helm/dev/or2/e851/kineto/values.yamlhelm/dev/or2/e851/kineto/Chart.yaml [cite: 13]
   Specifies artifactory path [cite: 13]
   Provides helm chart for kubernates [cite: 13]
4. k8s/helm/dev/or2/e851/kineto/values.yaml [cite: 13]
   Specifies the init_script which is what we pushed into s3 with package.py [cite: 13]
   Also the path to endpoints txt2img [cite: 13]

### Hs notes How to update existing dev deploy [cite: 13]
1. Make a new s3 package [cite: 13]
   a. Open a bash terminal in Vscode [cite: 14]
   b. Run: `"source deactivate"` [cite: 14]
   c. Make sure you include anything that's in your env (local deploy, end point, etc) in bash_profile [cite: 14]
      ```bash
      export ARTIFACTORY_UW2_API_TOKEN=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A
      export ARTIFACTORY_UW2_API_KEY=AKCp8pRjGhLjY21du38okUBmbAWtKG7SkHYn3NrR5Cs2CC97x1Dmp1pQsfaHZHzQWkmt5F76A
      export ARTIFACTORY_UW2_USER=hshariati

      export AWS_ACCESS_KEY_ID=AKIA4KAGRHX6XW442I3D
      export AWS_SECRET_ACCESS_KEY=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
      export AWS_DEFAULT_REGION=us-west-2
      export COLLIGO_LOCAL_DEPLOYS="clio_kineto_v2 clio_v2 diffusion_distil_l86_l87 diffusion_kineto_t2v ldm_decoder_v2 ldm_encoder_v2"
      export COLLIGO_MODEL_CACHE_DIR="/home/hshariati/hs_colligo_cash_dir"
      export COLLIGO_VENVS_PATH=/home/hshariati/venv
      ```
   d. Give new label: `"python pylibs/rhode/scripts/package.py --spec txt2img_kineto --label iter5"` [cite: 15]
   e. Run this test in your dev env: [cite: 15]
      ```bash
      (dev) hshariati@8e9ed1b4f814:/sensei-fs/users/hshariati/colligo$ python pylibs/rhode/scripts/package.py --spec txt2img_kineto
      ```
      You can get the spec name from [cite: 15]
      `/sensei-fs/users/hshariati/colligo/models/build/src/colligo/models/build/app_debug.py` [cite: 15]
      Like: [cite: 15]
      `build.application(name="txt2img_kineto", deployments=[CLIO_KINETO_V2])` [cite: 15]

      **You can also give it a label if you have already ran this once** [cite: 15]
      `python pylibs/rhode/scripts/package.py --spec txt2img_kineto --label iter1` [cite: 15]
2. Change the value of field `"init_script"` in one place [cite: 15]
   a. `/sensei-fs/users/hshariati/colligo-deploy/k8s/helm/dev/or2/e851/kineto/values.yaml` [cite: 16]
   b. Note that the one above will override the one below: [cite: 16]
      i. `/sensei-fs/users/hshariati/colligo-deploy/charts/rhode/modules/applications/kineto/deploy_2.yaml` [cite: 17]
3. Sdf [cite: 17]

### From shayan dev deploy [cite: 17]
1. Create minimal env using: [cite: 17]
   ```bash
   python tools/env.py create --env minimal-dev
   ```
2. Run the test in minimal env: [cite: 17]
   ```bash
   (base) (minimal-dev) hshariati@8e9ed1b4f814:~$ pytest /sensei-fs/users/hshariati/colligo/pylibs/build/tests/minimal_dev/test_load_models.py
   ```

   You can edit this file to only test your model (to make things faster): [cite: 17]
   ```bash
   (dev) hshariati@8e9ed1b4f814:/sensei-fs/users/hshariati/colligo$ git diff pylibs/build/tests/minimal_dev/test_load_models.py
   diff --git a/pylibs/build/tests/minimal_dev/test_load_models.py b/pylibs/build/tests/minimal_dev/test_load_models.py
   index 818e94f80..5f63ab937 100644
   --- a/pylibs/build/tests/minimal_dev/test_load_models.py
   +++ b/pylibs/build/tests/minimal_dev/test_load_models.py
   @@ -21,6 +21,7 @@ from colligo.base.worker_loader import ensure_worker_config_type
    from colligo.build.package import package_for_cloud
    from colligo.data.constants import get_deploy_repo
    from colligo.data.downloader import Downloader
   +from colligo.models.build.api import deploy_args
    from colligo.models.build.deployments import get_deployments

    PASSED = "PASSED"
   @@ -86,6 +87,9 @@ async def test_importable_envs() -> None:
        future_deploys = list[Awaitable[Deploy]]()

        for deploy in
   ```
   ```python
   app_config.deployments:
           if deploy.info.name not in ["txt2img_kineto"]:
               continue

            # Just set it to some GPU so it does not complain.
   ```
   ```python
   config = get_deploy_config(deploy, available_gpu=GpuType.NVIDIA_A100_80GB)
            deploy = deploy.with_config(config)
   (dev) hshariati@8e9ed1b4f814:/sensei-fs/users/hshariati/colligo$
   ```
1. Make sure you include anything that's in your env (local deploy, end point, etc) in bash_profile [cite: 19]
2. Run this test in your dev env: [cite: 19]
   ```bash
   (dev) hshariati@8e9ed1b4f814:/sensei-fs/users/hshariati/colligo$ python pylibs/rhode/scripts/package.py --spec txt2img_kineto
   ```
   You can get the spec name from [cite: 19]
   `/sensei-fs/users/hshariati/colligo/models/build/src/colligo/models/build/app_debug.py` [cite: 19]
   Like: [cite: 19]
   `build.application(name="txt2img_kineto", deployments=[CLIO_KINETO_V2])` [cite: 19]

   You can also give it a label [cite: 19]
   `python pylibs/rhode/scripts/package.py --spec txt2img_kineto --label iter1` [cite: 19]
3. Above will give you a s3 path: [cite: 20]
4. Deactivate every env. [cite: 20]
5. Then run [cite: 20]
   ```bash
   aws s3 cp <path you got above> init.sh
   bash init.sh
   set -x
   source activate.sh
   python -m colligo.rhode.commands.dev_supervisor --app-config ${COLLIGO_BUILD_SPEC}
   ```

### Deploy to experimental area [cite: 20]
1. In your colligo branch run [cite: 20]
   ```bash
   ./m package.rhode --spec firefly_experimental
   ```
   Example: [cite: 20]
   ```bash
   (dev) hshariati@17f176d73ea3:/mnt/localssd/hshariati/colligo$ ./m package.rhode --spec firefly_experimental
   VENV found at /mnt/localssd/hshariati/colligo/.venvs/dev/bin/activate.
   ```
   ```bash
   run tools/tasks.py package.rhode --spec firefly_experimental
   ```
   ```
   Running python package.py --spec firefly_experimental
   firefly_experimental -> s3://colligo-dev-pr/deploy_v2/colligo-rhode/firefly_experimental/firefly_experimental-version=3.0.14-custom-commit=96055060.sh─────────┬────────╮
   (dev) hshariati@17f176d73ea3:/mnt/localssd/hshariati/colligo$
   ```
2. This will give you a s3 path to init script [cite: 21]
   Example: [cite: 21]
   `s3://colligo-dev-pr/deploy_v2/colligo-rhode/firefly_experimental/firefly_experimental-version=3.0.14-custom-commit=96055060.sh` [cite: 21]
3. On github go to: [https://git.corp.adobe.com/firefly/colligo-deploy](https://git.corp.adobe.com/firefly/colligo-deploy) (this is only on git copt there is no github version) [cite: 21]
4. You can create a branch directly on github webpage. [cite: 22]
   Or you can just edit the file, after it will give you and option to create branch and pull request. [cite: 22]
5. Go to : clio-exp/values.yaml [cite: 23]
   Here you need to change the init script to yours: [cite: 23]
6. If you add a new model you also need to add it to the same (values.yaml file).You can reduce the replicas (GPUs) from other model and add to yours [cite: 23]
7. [cite: 23]
8. You also need to add your new model here [cite: 23]
9. You can reduce the replicas (GPUs) from other model and add to yours [cite: 23]
10. Now you can go to [https://argocd.ethos.corp.adobe.com/applications/argocd/firefly--colligo-deploy--ethos851-stage-or2--k8s--helm-dfff40fd?resource=&view=pods](https://argocd.ethos.corp.adobe.com/applications/argocd/firefly--colligo-deploy--ethos851-stage-or2--k8s--helm-dfff40fd?resource=&view=pods) and see the deployments. [cite: 24]
    Click on applications (remove all filters) and then search a keyword. [cite: 24]
11. Once deployed you can go to firefly .com: [https://firefly-stage-pr.corp.adobe.com/PR-5892/generate/images?id=933b3bdd-9fb1-41b7-bf9c-f709ad268a2a](https://firefly-stage-pr.corp.adobe.com/PR-5892/generate/images?id=933b3bdd-9fb1-41b7-bf9c-f709ad268a2a) [cite: 25]
    Here you can remove all filters, at the end of your prompt you can add the debug parameters that you need like: [cite: 25]
    `{"clio_moe_type" : "MOE_3_27_DMD"}` [cite: 25]
    `{"clio_moe_type" : "MOE_3_27_DMD_5_38"}` [cite: 25]

### Adds dmd to experimental [cite: 25]
[https://github.com/Adobe-Firefly/colligo/pull/1411](https://github.com/Adobe-Firefly/colligo/pull/1411) [cite: 25]

### Adds dmd to deploy: [cite: 25]
[https://git.corp.adobe.com/firefly/colligo-deploy/commit/30c4524675c2e0f77f9f4dee6e514fba4f092708](https://git.corp.adobe.com/firefly/colligo-deploy/commit/30c4524675c2e0f77f9f4dee6e514fba4f092708) [cite: 25]

### Run colligo pipeline outside vs code without the run and debug in screen session [cite: 25]
`/mnt/localssd/hshariati/colligo/.venvs/dev/bin/python -m colligo.rhode.commands.dev_supervisor --spec firefly_clineto --locust` [cite: 25]
```