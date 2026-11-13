---
document_type: landing
sectnum: true
children:
    - [/aidoc/announcements/index.md, "Announcements"]
    - /aidoc/monorepo/hardware-setup.md
    - /aidoc/monorepo/env-setup.md
    - /aidoc/monorepo/troubleshooting.md
    - /aidoc/monorepo/code-coverage-report.md
    - /aidoc/monorepo/pyenvs-quick-guide.md
    - /aidoc/monorepo/pyenvs.md
show_children: false
description: "AI Platform Monorepo - A unified codebase for AI services, models, and shared tooling."
---

# Monorepo

The AI Platform Monorepo is a unified codebase that hosts AI services, ML models, shared libraries, and development tooling. It enables teams to build, test, and deploy AI-powered services with shared infrastructure and best practices.

```{attention}
Note that not all use-cases need interacting directly with the AI platform monorepo [philosophy](/aidoc/philosophy.md). This page describes the use-cases that do, and relevant pages to get started.
```

## What Lives in the Monorepo

The monorepo hosts a variety of codebases and services across different stages of maturity:

### Inference Platform Services

Production services and ML models deployed through the Inference Platform, including:

- Inference workers and model serving applications
- Shared libraries and utilities
- Integration with Adobe services (IMS, CAI, ACP, ACMP)

[**Learn more about Inference Platform →**](/aidoc/inference-platform/index.md)

### Compute Platform (Pluto)

Infrastructure and tools for training ML models on GPU and CPU compute instances:

- Job management and scheduling
- GPU resource allocation and quota management
- Interactive development sessions
- Training job monitoring and observability

[**Learn more about Compute Platform →**](/pylibs/colligo/pluto/aidoc/index.md)

### Development Tooling and Infrastructure

Core development experience maintained by the Inference Platform team:

- **Build system** - Unified build and packaging
- **Dependency management** - Centralized Python dependency management
- **CLI tooling** - Command-line tools for development workflows
- **Testing infrastructure** - CPU and GPU unit testing with code coverage
- **CI/CD** - Continuous integration and deployment pipelines
- **Static analysis** - Code quality and type checking

### Research and Training Codebases

Several research and training codebases live within the monorepo but maintain independent workflows. Please contact the owners directly:

- **Evaluation Science** - Model evaluation frameworks (@bylinski's team)
- **AdobeDiffusion** - First generation imaging and video GenAI models and training code

### Related Platforms Outside the Monorepo

Several platforms have moved out of the monorepo and now maintain their own codebases:

- [**Data Platform**](https://docs.ai.corp.adobe.com/aidoc/data-platform/index.html) - Data pipelines, processing, and management
- [**Lineage**](https://docs.ai.corp.adobe.com/v3/frameworks/data/lineage/aidoc/index.html) - Data and model lineage tracking
- [**Mori**](/contrib/Mori/aidoc/index.md) - Second generation imaging and video GenAI models and training code
- [**Training Framework**](https://git.corp.adobe.com/pages/adobesensei/training-framework/) - Traditional Sensei model training infrastructure

---

## Getting Started

### Prerequisites and Access

Before working with the monorepo, ensure you have the necessary access:

1. **Get Access** - [AI platform access groups](/aidoc/access-control.md)

### Development Environment Setup

Set up your development environment for monorepo work:

1. **Hardware Setup** - [Configure your development machine](/aidoc/monorepo/hardware-setup.md)
2. **Environment Setup** - [Install dependencies and configure your environment](/aidoc/monorepo/env-setup.md)
3. **First Steps** - Try running existing services locally through the [Inference Platform guide](/aidoc/inference-platform/index.md)

### Quick Start Paths

```{admonition} I want to develop services in the monorepo
:class: hint

1. Complete [hardware setup](/aidoc/monorepo/hardware-setup.md) and [environment setup](/aidoc/monorepo/env-setup.md)
2. Follow the [Inference Platform guide](/aidoc/inference-platform/index.md) to run existing pipelines in the debugger
3. Familiarize yourself with [software engineering processes](#software-engineering-processes) before making contributions
```

```{admonition} I only need to call existing ML models
:class: hint

You don't need monorepo access for this use case. Use the [Inference SDK](/pylibs/colligo/sdk/aidoc/index.md) to call deployed models from your Python code.
```

```{admonition} I need GPU compute for training or development
:class: hint

You don't need monorepo access for this use case. Follow the [Compute Platform](/pylibs/colligo/pluto/aidoc/index.md) guide to provision GPU resources.
```

---

## Software Engineering Processes

To contribute to the monorepo, familiarize yourself with these processes:

- [**Code Review**](/aidoc/code-review/index.md) - Review guidelines and approval requirements
- [**Testing**](/aidoc/testing/index.md) - Unit testing, integration testing, and code coverage
- [**Dependency Management**](/aidoc/dependency-management/index.md) - Adding and updating dependencies
- [**Static Analysis**](/aidoc/static-analysis/index.md) - Type checking and code quality tools
- [**Continuous Integration**](/aidoc/continuous-integration/index.md) - CI pipelines and checks

---

## Support and Troubleshooting

The **Inference Platform team** maintains and supports the monorepo infrastructure, tooling, and developer experience.

**Need help?** We provide multiple support channels:

- **Slack**: `#firefly-colligo` for immediate questions
- **Jira**: [Official ticket intake](/aidoc/inference-platform/support/index.md#official-ticket-intake-jira) with SLA
- **Documentation**: [Troubleshooting guide](/aidoc/monorepo/troubleshooting.md) for common issues

[**Learn more about support options and SLAs →**](/aidoc/inference-platform/support/index.md)

---

## Additional Resources

- [**Announcements**](/aidoc/announcements/index.md) - Important updates and changes
- [**Code Coverage Report**](/aidoc/monorepo/code-coverage-report.md) - Current test coverage metrics
- [**Python Environments Quick Guide**](/aidoc/monorepo/pyenvs-quick-guide.md) - Managing Python virtual environments
- [**Python Environments**](/aidoc/monorepo/pyenvs.md) - Detailed Python environment documentation
