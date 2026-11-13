---
document_type: landing
children: 
  - [./framework/index.md, "Inference Framework"]
  - [./infra/index.md, "Inference Infrastructure"]
  - [/managed_services/README.md, "Managed Services (v3)"]
  - [./support/index.md, "Support"]
  - [./user-guides/index.md, "User Guides"]
  - [./caplan/index.md, "Capacity planning"]    
  - [./internal/index.md, "Internal documentation"]
show_children: false
description: Inference Platform Landing Page
---

# Inference Platform

```{admonition} **v3 is available as a release candidate!**
:class: important
<div style="display:flex;gap:8px;margin:4px 0;justify-content:center">
<span style="background:#1a73e8;color:#fff;padding:4px 12px;border-radius:4px;font-size:0.85em"><b>v2 (stable)</b></span>
<a href="/managed_services/README.html" style="background:#f0f0f0;color:#666;padding:4px 12px;border-radius:4px;font-size:0.85em;text-decoration:none">v3 (release candidate)</a>
</div>

These are the **v2 docs** — the stable and recommended path for production inference services.
**v3 is now available as a release candidate**: a new Bazel-based build system, redesigned worker API, and opinionated managed services workflow. See [Managed Services (v3)](/managed_services/README.md) to get started.
```

The Inference Platform is a managed platform for serving machine learning models and AI applications efficiently and at scale.
It supports the entire lifecycle of AI-powered service development — from local experimentation and testing to operating production-grade services serving real customers.

## Platform Components

The Inference Platform consists of three major product areas, each designed to address a distinct stage of the machine learning feature deployment lifecycle.

In addition, the Platform provides comprehensive operational and engineering support, including:

- Daily engineering assistance and troubleshooting
- Shared on-call support
- Operational readiness and reliability reviews
- Capacity planning and resource management
- Efficiency and performance tracking

### Inference Framework

The core framework for building and running inference workers and applications.

**Key Features:**

- Worker API and orchestration
- Worker-to-worker communication through multiple queue types (FIFO, sticky, priority)
- Resilient durable queues for asynchronous processing with retries
- Temporary asset storage
- Distributed rate limiting and backpressure control
- Built-in profiling, logging, and metrics
- Local development and debugging support
- Integrations with common Adobe services (IMS, CAI, ACP, ACMP etc.)

[**Learn more about Inference Framework →**](./framework/index.md)

### Inference Infrastructure

The platform provides an infrastructure and a set of infrastructure-related features to support
teams through development and productionalization lifecycle.

**Key Features:**

- Deployment to Ethos Clusters with dedicated Development, Staging and Production environments
- AWS S3, Azure storage buckets
- A multi-tenant metadata storage in Redis/MemoryDB
- Autoscaling
- Observability (Grafana, Splunk, Prometheus, NewRelic)

[**Learn more about Inference Infrastructure →**](./infra/index.md)

### Monorepo Developer Experience and Tooling

The Inference Platform is the main tenant and maintainer of the AI platform monorepo.

**Key Features:**

- Build system
- Dependency management
- CLI tooling
- Static analysis
- CPU and GPU unit testing and code coverage
- Integration testing framework
- CI infrastructure

In addition, the Platform governs:

- Code ownership and code reviews
- Monorepo versioning and release strategy
- Monorepo dependency update cadence

[**Learn more about Monorepo Developer Experience and Tooling →**](/aidoc/monorepo/index.md)

---

## Getting Started

### Quick Start Path

New to the Inference Platform?

Check out our [tutorial page](./user-guides/tutorials/index.md)
and follow video instructions!

Or follow this journey to go from local development to production:

1. **Get Access** - [AI platform access groups](/aidoc/access-control.md)
1. **Setup** - [Set up your development environment](/aidoc/monorepo/env-setup.md)
1. **Develop Locally** - [Create your first inference worker](/models/colligo/models/template/t1/aidoc/index.md)
1. **Continue on Pluto** - [Need a GPU for local development? Use Pluto Interactive session](https://docs.ai.corp.adobe.com/v3/platforms/pluto/aidoc/getting-started.html#start-an-interactive-session)
1. **Deploy to Ethos** - [Deploy to Ethos Development environment](./user-guides/tutorials/serve.md#deploy-as-service-to-ethos)
1. **Get Ready for Production** - [Operational Readiness Review](./user-guides/operational-readiness-review/index.md)

### Common Use Cases

```{admonition} I want to deploy a new ML model
:class: hint
Start with the [Inference Framework guide](./framework/index.md) to understand worker APIs, then follow the [tutorial for adding an inference worker](/models/colligo/models/template/t1/aidoc/index.md).
```

```{admonition} I need to call existing models via SDK
:class: hint
See the [Inference SDK documentation](/pylibs/colligo/sdk/aidoc/index.md) to learn how to call deployed models from your Python code.
```

```{admonition} I'm troubleshooting a deployed service
:class: hint
Check the [Infrastructure documentation](./infra/index.md) for observability tools, or jump directly to [troubleshooting in Ethos](/pylibs/colligo/rhode/aidoc/ethos_troubleshooting.md).
```

```{admonition} My service needs a new dependency not present in the monorepo
:class: hint
Check the [Dependency Management: Overview](/aidoc/dependency-management/overview.md#types-of-dependencies).
```

---

## Communication and Support

**Need help?** We provide multiple support channels:

- **Slack**: `#firefly-colligo` for immediate questions, `#firefly-sre-devops` for SRE help
- **Jira**: [Official ticket intake](./support/index.md#official-ticket-intake-jira) with SLA
- **On-call**:  [Shared On-call responsibilities](./support/index.md#on-call-support)

[**Learn more about support options and SLAs →**](./support/index.md)

---

## Additional Resources

- [**Release Notes**](./support/release.md) - Latest updates and changes
- [**Communications**](./support/postmortems/index.md) - Blog posts and postmortems
