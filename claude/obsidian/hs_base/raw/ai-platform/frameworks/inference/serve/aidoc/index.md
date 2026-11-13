---
sectnum: true
children:
  - [./api.md, "API"]
  - [./samples/index.md, "Samples"]
  - [./changelog.md, "Changelog"]
  - [../README.md, "Internal Docs"]
---

# frameworks.inference: Serving framework

```{note}
<div style="display:flex;gap:8px;margin:4px 0;justify-content:center">
<span style="background:#1a73e8;color:#fff;padding:4px 12px;border-radius:4px;font-size:0.85em"><b>Framework</b></span>
<a href="https://docs.ai.corp.adobe.com/v3/platforms/inference/aidoc/index.html" style="background:#f0f0f0;color:#666;padding:4px 12px;border-radius:4px;font-size:0.85em;text-decoration:none">Platform</a>
<a href="https://docs.ai.corp.adobe.com/managed_services/README.html" style="background:#f0f0f0;color:#666;padding:4px 12px;border-radius:4px;font-size:0.85em;text-decoration:none">Managed Services</a>
</div>

This is the **Python framework** for building inference services (`pip install frameworks.inference`).
For the deployment platform and big-picture architecture, see the [Inference Platform](/platforms/inference/aidoc/index.md).
To use the managed CI/CD ecosystem where your code lives, see [Managed Services](https://docs.ai.corp.adobe.com/managed_services/README.html).
```

[Request for Comments](https://adobe.sharepoint.com/:w:/r/sites/GenTechWorkingGroup/Shared%20Documents/AI%20Platform/Inference%20Platform/Inference%20Framework%20V3%20RFC.docx?d=wfcb305a4490746698d50ff1031ae1535&csf=1&web=1&e=5tGmyh) | Follow progress at: [FFP-54848 - 25Q4](https://jira.corp.adobe.com/browse/FFP-54848) | [FFP-45633 - 25Q3](https://jira.corp.adobe.com/browse/FFP-45633)

## Use cases

The inference framework enables defining building blocks of inference services. It then allows utilizing these building blocks to run the these services in the following scenarios
1. **Prototyping and development**: Running all or most of components on your developer machine
    ```{figure} ./images/development.png
    :width: 80%
    :align: center
    ```
2. **Deploying the services in the Managed inference platform**: Deployment your service in the managed inference platform. The managed platform takes care of various repetetive cloud related tasks, at the cost of following their opinionated guidelines. Using high end GPUs are supported only through this route.
    ```{figure} ./images/service.png
    :width: 80%
    :align: center
    ```
3. **Deploying the services on your own (e.g. Ethos)**: You take ownership of all cloud components. There is going to be no restrictions, but you are responsible for dealing with all cloud components.
    ```{figure} ./images/user-service.png
    :width: 80%
    :align: center
    ```

## API

[](./api.md)

## Samples

We have a curated set of sample services that demonstrate how to use the inference platform.

- [](./samples/index.md)
- Using the inference framework within the managed services ecosystem: [colligo managed_services samples](https://docs.ai.corp.adobe.com/managed_services/services/samples/README.html)

## Installation

```
[uv] pip install frameworks.inference \
  --extra-index-url https://artifactory-uw2.adobeitc.com/artifactory/api/pypi/pypi-adobeshared-release/simple
```

## Inference service building blocks

The main building blocks in the inference stack are
- "compute workers"
- "pipeline workers"
- "web apps"

Follow the [sample apps above](#samples) to learn more about each component.

<div style="width:80%; margin: 0 auto; text-align: center;">

```{mermaid}
graph LR
    subgraph "Inference Application"
        direction LR
        WebServer[Web Server] -->|API 1| O1["Pipeline Worker 1"]
        O1 -->|remote| A[Compute Worker A]
        O1 -->|remote| B[Compute Worker B]
        O1 -->|remote| C[Compute Worker C]
        WebServer[Web Server] -->|API 2| O2["Pipeline Worker 2"]
        O2 -->|remote| C
        O2 -->|collocated| G[Compute Worker G]
    end
```

</div>
