---
type: concept
title: Foundry inference auth tokens (IMS) — 24h token vs refresh vs S2S
tags: [foundry, ims, auth, inference, gateway, how-to]
created: 2026-07-22
updated: 2026-07-22
sources: ["[[raw/dsg-foundry-token-slack]]"]
---

# Foundry inference auth tokens (IMS)

**How a caller authenticates to a Foundry inference endpoint** (e.g. `foundry-inference-prerelease.adobe.io`),
and why the "the token expires every 24 hours" complaint is a **non-issue once set up properly**. This
is standard **Adobe IMS OAuth2** — the same pattern every Adobe service uses. Complements
[[wiki/concepts/foundry-aws-access|the gen-foundry endpoint allowlist layers]] (this page = token
*lifecycle*; that page = *who's authorized*) and [[wiki/concepts/foundry-endpoint-email-allowlist|the
email allowlist]].

## The 24-hour token is for testing only

The token you copy from `foundry-inference-prerelease.adobe.io` is a **user access token** from the
**IMS OAuth2 browser flow** — short-lived (~24h) **by design**, meant for quick manual testing, **not**
long-term integration. Re-requesting it daily is *not* the intended path.

## The two correct paths

1. **From a UI (browser / desktop app) → OAuth2 Authorization Code flow.**
   Register a **"Web"** IMS client, implement `authorize → token exchange`, and use **refresh tokens
   (default ~2-week lifetime)** to silently mint fresh access tokens. **The user logs in once; the app
   renews transparently** — no daily manual token.
2. **From a backend service (no user present) → Service-to-service (S2S) client.**
   Register a **"Service"** IMS client in the **IMSS portal** → get a **permanent authorization code +
   `client_secret`** → exchange for access tokens programmatically. No browser, no user, **auto-renewable
   forever**.

**IMS client registration is self-serve** (IMSS) — it is *not* something the Foundry/services team has
to provision or that has to "land." Refs: IMS Integration Guide
(`wiki.corp.adobe.com/spaces/ims/pages/816562706`), IMS Token API (`.../828144226`), IMSS portal
(`imss.corp.adobe.com`), IMSS Reference Docs (`.../1791170705`). (Skills like
[[wiki/concepts/foundry-gateway-skills|/generate-from-endpoint]] call endpoints with an IMS bearer token.)

> [!note] Common misconceptions (seen in the DSG thread)
> - **No VPN is required** for the IMS OAuth2 flow — it's a standard browser/token exchange.
> - The 24h expiry is **not** a blocker: a UI uses refresh tokens (login once); a backend uses an S2S
>   client. Either removes the "daily token" problem *now*, self-serve.

## Related open issue — exposing customer assets to a customer UI

Distinct from auth: DSG also wanted their UI to **read DSG's own product/model data**. Per the same
thread, the ML-deployment/services team's scope is **hosting model + generation pipelines and scaling
GPUs/deployments — NOT building one-off UIs or acting as a data repo**, and "we were not in business of
exposing authenticated assets to client (Foundry Studio does that itself)." There's **no canonical
pattern** yet; candidate owners are **Theos's team (Foundry 4.0)** or **Mary's team (Foundry Studio /
front-end)**. This is the genuinely-unresolved item — see [[raw/dsg-foundry-token-slack]].

## Related
- [[wiki/concepts/foundry-aws-access]]
- [[wiki/concepts/foundry-endpoint-email-allowlist]]
- [[wiki/entities/foundry-gateway]]
