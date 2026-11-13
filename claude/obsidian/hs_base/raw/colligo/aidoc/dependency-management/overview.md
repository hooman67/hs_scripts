# Dependency Management: Overview

This document provides an overview of why and how we manage dependencies. Separate documents have been allocated for tutorials and rules; see the [top-level landing page](./index.md) for the URLs.

## Short-lived code [^eng]

In this case, the user wants to access published software with a user-facing API.

### Goals

- Users should be able to access the published libraries from the platform, along with other Adobe or external third-party dependencies for their development.
- Users should have a way to manage dependency mismatches between platform code and other dependencies.
- Users should have a path forward to handle changing dependency constraints as they update the platform code they depend on.
- Sometimes users need to make a quick change or ideate on the platform code. There should be a path forward to facilitate that.

### Solution

Following community trends[^flyte][^3][^metaflow][^ray], we make the platform code available as a Python package that users can install:

  ```bash
  pip install colligo [ --extra-index-url ... ]
  ```

  (The `--extra-index-url` can be omitted for users utilizing compute from the compute platform.)

We will use optional dependency groups to allow users to install only portions of the public code's dependencies, reducing collisions with other dependencies.

  ```bash
  pip install colligo[models,inference,train,...]
  ```

Users can edit the platform code in place in their Python installation. However, if they find themselves doing this too often, they might consider transitioning to a long-lived code use case, rather than a short-lived one.

```{admonition} Note
:class: note
This solution is not yet implemented. The [inference SDK](/pylibs/colligo/sdk/aidoc/index.md) is our starting point, but it is far from stable, published software.
```

## Long-lived code [^eng]

### Goals

- Evolve and maintain a collection of code with dependencies on each other.
- Enforce software engineering practices consistently.
- Maintenance overhead should increase sublinearly as the number of maintainers or code increases.

### Types of Dependencies

Let's identify the different types of dependencies that a piece of code needs to run and how we provide them.

1. **AI Monorepo Tenants**: Managed code that lives in the monorepo ecosystem and over which we have full control. This includes both user code and platform code.
    1. **Code directly checked into source control** (Adobe's solution is GitHub).
    2. **Large Binaries**: Such as model weights, image test fixtures, etc., which GitHub cannot handle at scale.
2. **Internal Adobe Dependencies**: Adobe has code silos managed by different teams. Moving the company to a monorepo is not feasible. So, we need to handle code from other teams within Adobe, whose development ecosystem lives elsewhere. This group is for code that is managed by Adobe teams outside the monorepo, but we need to somehow use it in the monorepo (e.g. [Lagrange library](/third_party/adobe/lagrange-lib/)).
3. **External Dependencies**: Such as Torch or Protobuf libraries.
    1. Some can be used **as-is** from released artifacts.
    2. Some need **custom build**, but **don't need source modification**.
    3. Some also need **code modification**. The code modification is meant as near identical versions of upstream with minor edits that can be up-streamed (mainly due to bugs). **Note that code that is heavily modified should be treated as class 1, not here**.
4. **Containerized System Dependencies**: These are system dependencies controlled within a Docker container, provided by a Docker image. Examples include OS versions and CUDA libraries.
5. **Host System Dependencies**: System dependencies that cannot simply be containerized and need to be controlled on the host system, such as GPU drivers. These are managed by the [compute platform](/pylibs/colligo/pluto/aidoc/index.md) team. The compute provided by the compute platform often includes a recent stable version of these dependencies.

It is not always possible to draw a fine line where a dependency falls. For example, CUDA libraries could be considered as *3.2* or *4*. By maintaining the build rules and an efficient build system, *3.2* reduces the operational overhead for the rest of our engineering stack, as CUDA versions can be tracked with source control. Currently, we treat them as *4*.

Some dependencies that need building C++ code are currently being handled inconsistently, e.g. `ffmpeg`.  You could either
  - Treat them as `4`. In that case they need to either be installed either via `apt` or build from source. The source code should follow the *2* and *3*. For example, you are not allowed to just pull code form other parts in Adobe, and the code needs to be a subtree with the build file checked in.
  - Include them as as `1.1`, and include them in the `build.py` file [^bin].

### Making Dependencies Available

For step by step instructions on what you need to do as a developer see the tutorials section [^tutorials].

Corresponding to the dependency types above:

- **1.1**: We handle this code via our build system [^build].
- **1.2**: We handle these binaries via our tooling. We don't check them into the source control system, but we check in a manifest on where they can be downloaded from and a way to conveniently upload updates. [^bin]
- **2**: We check in these libraries as subtrees in the AI platform monorepo and handle them with our build system [^3p].
- **3.1**: We install these with the language's de facto dependency manager (e.g., pip or npm), orchestrated by our build system. Alternatively, we directly pull the artifacts with our build system, depending on the type of dependency. For example, an executable can be directly pulled, but a Python module needs to be installed via pip [^3p].
- **3.2**: We build these deps with our build system, but their code does not have to be checked-in [^3p].
- **3.3**: We check in these dependencies as subtrees and build them with our build system [^3p].
- **4**: These are provided by an *official* development Docker image. The monorepo development works with only one version of these (see more on [dependency versions](#dependency-versions)). Note that the number of these dependencies should be very low. Most external dependencies should fall under **3.1**. [^docker]
- **5**: These are managed by the **compute platform** team. The compute provided by the compute platform often includes a recent stable version of these. [^compute-platform]


### Dependency Versions

Dealing with conflicting dependencies when we have collection of interdependent code is a challenging problem[^google]. We follow a common strategy in the industry, to limit the version of dependencies as much as possible[^google][^coinbase] which minimizes the space the software needs to operate under, and makes it testable. This is a trade-off between the flexibility of the software and the operational overhead of maintaining it.

From a platform/monorepo perspective, we strongly want all users to migrate to the latest version as quickly as possible. The platform team takes responsibility for regularly updating dependency versions, relying on
  - Tests
  - Reproducible build rules (e.g., not relying on an uploaded custom-built artifact for a specific version of Torch)

At least for the inference workers and pipelines, see [inference platform](/aidoc/inference-platform/index.md), automation has capabilities to run such tests. Nonetheless, the codeowners (i.e. platform users), also need to build the tests that give us the confidence to migrate with little (if any) effort.

**If a user's workflow is broken after an update while their tests were passing (or they did not have any tests), it is their responsibility to get their code working with the new version.**

**We only support a single version of each dependency.** In the context of training vs. inference, there has been discussion about supporting more than one version for certain use cases. We have not yet faced this challenge, particularly because training code is not yet a citizen of the monorepo. We will tackle the problem when the time comes. However, even in that case, only a *limited* (ideally only two) set of versions should be used. Each set of versions means a larger space of use cases that need to be covered and can cause operational nightmares.


```{admonition} Note
:class: note

Not all (and in some cases any) of the code within the monorepo follows the strategy above. Historically, we chose different solutions, which eventually stopped scaling as we evolved.

As we continue improving our testing and build system infrastructure ([FFP-14611]), we might need to use more operationally expensive methods for some upgrades, such as the [Torch 2.3] upgrade.

We are working on improving consistency and converging to the strategy above [FFP-14611]. We did not get into details of how things were in the past and focused on the future in the information above. We will add more details as we move forward with the planned improvements.
```

[FFP-14611]: https://jira.corp.adobe.com/browse/FFP-14611
[Torch 2.3]: /aidoc/announcements/2024-09-01-torch-migration.md
[^eng]: [Short-term vs. long-term code lifecycle](/aidoc/philosophy.md#short-term-vs-long-term-code-lifecycle)
[^flyte]: [Flyte Library](https://docs.flyte.org/en/latest/getting_started_with_workflow_development/installing_development_tools.html#getting-started-installing-development-tools)
[^3]: [MLFlow](https://mlflow.org/docs/latest/getting-started/tracking-server-overview/index.html?highlight=pip%20install)
[^metaflow]: [MetaFlow](https://docs.metaflow.org/v/r/getting-started/install)
[^ray]: [Ray Library](https://docs.ray.io/en/latest/ray-overview/installation.html)
[^tutorials]: [Dependency Management / Monorepo Tutorials](./monorepo-tutorials.md)
[^build]: [Dependency Management / Build System](./build-system.md)
[^bin]: [Dependency Management / Binaries](./binary-management.md)
[^3p]: [Dependency Management / Third Party Code Structure](/third_party/aidoc/index.md)
[^google]: [Software Engineering at Google - Dependency Management](https://abseil.io/resources/swe-book/html/ch21.html)
[^coinbase]: [Coinbase: Building a Python ecosystem for efficient and reliable development](https://www.coinbase.com/blog/part-2-building-a-python-ecosystem-for-efficient-and-reliable-development)
[^docker]: [Monorepo docker images](/docker/aidoc/index.md)
[^compute-platform]: [Compute Platform](/pylibs/colligo/pluto/aidoc/index.md)
