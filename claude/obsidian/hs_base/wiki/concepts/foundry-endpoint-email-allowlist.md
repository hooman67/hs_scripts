---
type: concept
title: Allowlist an email on a Foundry pre-release endpoint
tags: [foundry, managed-services, gateway, access, deployment, how-to]
created: 2026-07-08
updated: 2026-07-08
sources: ["[[raw/endpoint-email-allowlist-slack]]"]
---

# Allowlist an email on a Foundry pre-release endpoint

**How to grant an external user access to a Foundry inference endpoint:** add their email to the
`allowlisted_emails` section of the **customer-gateway configmap**, then PR it to colligo `main` — the
[[wiki/concepts/colligo-managed-services|managed_services (V3)]] deploy rolls it out via
[[wiki/concepts/v3-deployment|Argo CD]].

> [!note] Which gateway
> This is the **customer gateway** that fronts a customer's Foundry endpoint (controls *which external
> users* may call it). It is **not** the [[wiki/entities/foundry-gateway|foundry-aws-corp.adobe.io]]
> access gateway (which vends AWS/S3 creds to Foundry devs). Different things.

## Steps

1. Edit the customer-gateway configmap for the target stage on `Adobe-Firefly/colligo` `main`:
   - **pre-release:** `managed_services/services/firefly/foundry/deploys/customer_gateway/prerelease/configmap.yaml`
   - **prod:** the sibling `prod/` configmap (make the same edit there if the prod endpoint also needs it).
2. Add (or extend) an `allowlisted_emails:` section with the user's email address(es).
3. Open a PR to colligo `main`. On merge, Argo CD applies it to Ethos and the endpoint accepts the new user.

## Worked example — PR #28089 (2026-07-08)

Hooman used these steps to allowlist HP's two emails on the **pre-release** endpoint:
- `evgeny.makharadze@hp.com`
- `mirian-thayse.geiser@hp.com`

PR: https://github.com/Adobe-Firefly/colligo/pull/28089 (added the `allowlisted_emails` section to
`.../customer_gateway/prerelease/configmap.yaml`). Origin of the request/instructions:
[[raw/endpoint-email-allowlist-slack]] (Shayan Hoshyari pointed to the configmap; Mingdong Wang is a
gateway owner).

## Related
- [[wiki/concepts/colligo-managed-services]]
- [[wiki/concepts/v3-deployment]]
- [[wiki/entities/foundry]]
- [[wiki/entities/foundry-gateway]]
