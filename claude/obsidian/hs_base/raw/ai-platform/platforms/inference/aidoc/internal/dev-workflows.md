# Internal Dev workflows

## Debug python code in Bazel

We allow running build scripts, tests or just normal executables in vscode debugger.

Click on this target in `vscode`, then type the Bazel target and command line args same way you pass them to `bazel run ...`

```
- Python: Bazel Python Run *or* Bazel Python Test *or* Bazel Python Build
- Type in: "//bazel_infra/gitops_test [arg1 arg2]" (only run supports passing args)
```

- `Bazel Python Run`: For `bazel run <target>`. Works for both test and binaries.
- `Bazel Python Test`: Runs `bazel test <target>`.  Works only for tests. The difference is this will have the bazel sand-boxing enabled.
- `Bazel Python Build`: Runs `bazel build <target>`.  Works for build actions (e.g. chart rendering).

## Debug a "failed" build script

Note that you can already debug a build python script using the instructions in [Debug python code in Bazel](#debug-python-code-in-bazel) using the `Bazel Python Build` target.

- We offer some additional debugging functionality for debugging failed build scripts. When a build action fails, it will print something like the script shot below
    <details>
    <summary> 📷 Screenshot </summary> 

    ![](../images/find-work-dir.png)

    </details>
- When you see this, re-run the build again, but pass `--sandbox_debug` to Bazel build.
- Open the printed workdir in vscode or cursor. There will be a `.vscode/launch.json` created for you. It has a `Python: Run Failed Command` defined. Simply run this in vscode, and you have the same step now running in the debugger. You can set break points and see variable values.
    <details>
    <summary> 📷 Screenshot </summary> 

    ![](../images/run-in-debugger.png)

    </details>


## Makefile

```{colligo_list_files} ../../Makefile
```

## Bumping inference stack version in managed services ecosystem

1. Make a tag `release/inference/v<version>` and push it.
2. In the colligo repo, go to `managed_services/MODULE.bazel` and update the `VERSION` here.
    ```
    git_override(
        module_name = "platforms_inference",
        remote = "https://github.com/Adobe-Firefly/ai-platform.git",
        strip_prefix = "platforms/inference",
        tag = "release/inference/<VERSION>",
    )
    ```
3. In `managed_services/`, run `./make lint`
4. Check in all the affected files and make a PR.


How does it work?
- Publishing the tag will make the CI ([frameworks_inference.yaml](/.github/workflows/frameworks_inference_serve.yaml)) publish a wheel for the framework.
- Updating the `git_override` will have two effects:
    * The bazel infra will be pulled from that tag.
    * When you run make lint, the bazel infra parses the same `git_override` call and makes sure the lock files (e.g. `managed_services/requirements.linux.txt` in colligo) are locking to the same version of wheel for framework.

## Using inference platform and framework from source in managed services ecosystem

The managed services ecosystem is now in the [colligo repo](https://github.com/Adobe-Firefly/colligo) at `managed_services/`.

1. In the colligo repo, update `managed_services/MODULE.bazel`:
    - Comment out the `git_override` block
    - Uncomment `local_path_override` and set path to your ai-platform checkout:
      ```python
      local_path_override(
          module_name = "platforms_inference",
          path = "/path/to/ai-platform/platforms/inference"
      )
      ```

2. Update `managed_services/BUILD` - enable gazelle resolve for editable install:
    - Convert
        ```
        # disable:gazelle:resolve py frameworks.inference @platforms_inference//editable_install:framework
        ```
    - To
        ```
        # gazelle:resolve py frameworks.inference @platforms_inference//editable_install:framework
        ```

3. Run `./make lint` in colligo's `managed_services/` folder

4. Now you can do usual development and any changes done to the framework or platform code will be picked up immediately (it is built from source).

```{warning}
- This is not something we can really automatically test. So it might be broken. Sometimes it might be broken, due to the file [platforms/inference/editable_install/BUILD](/platforms/inference/editable_install/BUILD) being out of date. See the file to find out what are things that need to be updated by hand. 
- These changes must not be checked into main in colligo. There is a test `no_editable_install_checks` that ensures to pick up if these changes are made, and fail the pre-merge checks. To revert them:
  - Revert steps 1 and 2.
  - Run step 3 again.
```

How does it work?

- `local_path_override(...)`: Makes sure that the inference platform Bazel infra comes from your local checkout, not a remote repo with a certain tag.
- `gazelle:resolve ...` makes sure we use the target `@platforms_inference//editable_install:framework` for inference framework, instead of the built wheel `@pypi//frameworks_inference`. This is just a wrapper around the code that is in the repo. Code at [platforms/inference/editable_install/BUILD](/platforms/inference/editable_install/BUILD)

## Testing changes in Ethos before merging to main

### The problem

Platform developers often need to manually test a deployment before merging a platform change. However, the normal deployment pipeline is tightly coupled to merging:

* **Update flow:** Platform change → Platform release → Merge to `managed_services` main
* **Deploy flow:** Merge to `managed_services` main → CI syncs to deploy repo → Argo CD deploys

This makes it nearly impossible to validate cross-repository changes during the PR phase. If you have a platform PR that needs end-to-end testing in a real cluster, there is no path through the standard pipeline.

### The solution: test environment branches

The ai-platform repo's [`.ethos.yaml`](/.ethos.yaml) can have entries that deploy from a specific branch instead of `main`. The Ethos provisioner watches the configured `chart_path` on that branch, so any Kubernetes manifests pushed there are deployed automatically — no PR or review required.

For example, `test_env` is one such branch, deploying from [`platforms/inference/bazel_infra/__fixtures__/cloud/dev/test`](/platforms/inference/bazel_infra/__fixtures__/cloud/dev/test). You can add more entries in `.ethos.yaml` following the same pattern to create additional test environments.

The FLEX UI for these environments is at the [ai-platform service on Devhome](https://devhome.corp.adobe.com/catalog/default/Component/SRID_577172/flex).

### Steps

1. **Enable editable install mode** in `managed_services` so your local platform changes are picked up. Follow [Using inference platform and framework from source](#using-inference-platform-and-framework-from-source-in-managed-services-ecosystem).

2. **Build docker images** from [`managed_services/`](https://github.com/Adobe-Firefly/colligo/tree/main/managed_services) using [`smake build-images`](https://github.com/Adobe-Firefly/colligo/tree/main/managed_services#common-commands).

3. **Push docker images** using [`smake push-images`](https://github.com/Adobe-Firefly/colligo/tree/main/managed_services#common-commands) (requires a [compute platform](https://docs.ai.corp.adobe.com/pylibs/colligo/pluto/aidoc/index.html) session).

4. **Update the image / .json spec** in your deployment spec (e.g. `values.inference.yaml`) to reference the newly pushed image.

    ```{warning}
    Also rename `application_name` in `values.inference.yaml` to something unique (e.g. `test-env`) before proceeding. The production deployment in `colligo-v3-deploy/main` uses the real app name (e.g. `sample-e`) and deploys to the same namespace. If you keep the same `application_name`, two Argo CD apps will fight over the same Kubernetes resources, causing pods to restart in a loop.
    ```

5. **Regenerate the Kubernetes manifests** by running [`smake argo-sync`](https://github.com/Adobe-Firefly/colligo/tree/main/managed_services#common-commands) from `managed_services/` (or `smake lint`, but `argo-sync` is faster).

6. **Push the generated manifests** to the test environment branch (e.g. `test_env`):
    ```bash
    # from the ai-platform repo
    git checkout <branch>
    # The generated chart lives in managed_services/, but Ethos watches
    # the chart_path in ai-platform. Copy it over so the provisioner picks it up.
    cp -r <path-to-colligo>/managed_services/cloud/<chart_subpath>/ <path to ai-platform>/<test env subpath in .ethos.yaml>/
    # commit and push
    ```
    The Ethos provisioner will pick up the change and deploy it to the configured cluster/namespace.

## Publish inference chart

Charts are automatically published via GitHub Actions when release tags are created:

```bash
# Create and push a release tag
git tag release/inference/v1.2.3
git push origin release/inference/v1.2.3
```

Manual publishing for development:

```bash
# Publish with version (production)
make publish-chart VERSION="1.0.0"

# Publish without version (development - uses file hash instead of version and uploads to dev folder)
make publish-chart
```

### Publishing a dev chart from a PR

To test chart changes in `managed_services` without merging to main:

1. Add the label `publish-inference-chart` to your ai-platform PR.
   CI publishes a dev version: `0.dev<PR_NUMBER>+sha.<SHORT_SHA>`.

2. In the colligo repo, reference the dev chart in your deploy BUILD:
   ```python
   k8s_remote_python_chart(
       name = "ai-inference-chart-dev",
       py_binary = select({
           "@platforms//os:linux": "https://artifacts.adobeitc.com/artifactory/docker-colligo-release/firefly/v3/inference-chart/0.dev<PR>%2Bsha.<SHA>/inference-chart-linux.zip",
           "@platforms//os:macos": "https://artifacts.adobeitc.com/artifactory/docker-colligo-release/firefly/v3/inference-chart/0.dev<PR>%2Bsha.<SHA>/inference-chart-macos.zip",
       }),
       replaces = "@platforms_inference//:ai-inference-chart",
   )
   ```
   Note: `+` in the version must be URL-encoded as `%2B`.

3. Point `k8s_chart_values` and `python_charts` at `:ai-inference-chart-dev`.

4. Run `smake lint` (or `smake argo-sync`) to render and verify.

5. Once the ai-platform PR merges and a release tag is created, replace
   the dev chart reference with the official `@platforms_inference//:ai-inference-chart`
   (or a pinned version in the root BUILD).

