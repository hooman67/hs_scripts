# DSG Foundry token + data-access — Slack thread (raw)

> Source: adoberesearch Slack, channel C0BBQHS2BMZ, thread ts 1784577201.154049 (2026-07-20/21).
> Participants: Hooman Shariati, Mingdong Wang (services), Shayan Hoshyari, Wolfgang Black, ref: Kevin Green (DSG UI). Captured 2026-07-22. Immutable.

**Hooman (parent):** need answers from services for DSG — (1) the credentials question, (2) how/where to store DSG's additional data.

**Wolfgang:** the question is about "a Foundry API token needing to be re-requested every 24 hours."
**Mingdong:** right — Kevin Green wants to set up the service token for his UI.

**Shayan (authoritative answer, via his AI assistant):**
- The token from `foundry-inference-prerelease.adobe.io` is a **user access token — expires in 24h by design**. That site runs the standard **IMS OAuth2 browser flow**; the short-lived token is for **quick testing**, not long-term integration.
- Standard Adobe IMS auth — two correct paths:
  1. **From a UI (browser/desktop) → OAuth2 Authorization Code flow.** Register a **"Web"** IMS client, implement authorize → token exchange, use **refresh tokens (default 2-week)** to silently get fresh access tokens without re-prompting. User logs in once; app renews transparently.
  2. **From a backend service (no user) → Service-to-service client.** Register a **"Service"** IMS client in the **IMSS portal**; get a **permanent authorization code + `client_secret`**; exchange programmatically — no browser, no user, auto-renewable forever.
- **"The 24h expiry is a non-issue once set up properly."** IMS client registration is **self-serve** ("it is up to client itself. Adobe IMS is self serve.").
- Refs: IMS Integration Guide (`wiki.corp.adobe.com/spaces/ims/pages/816562706`), IMS Token API (`.../828144226`), IMSS self-service portal (`imss.corp.adobe.com`), IMSS Reference Docs (`.../1791170705`).
- Shayan (frustrated): "I've answered this ~10 times" / "my tongue grew hair."

**Data-access question (the genuinely-open part):**
- Wolfgang: is DSG's extra data for a checkpoint / training / a data repo for storage/generations? If packaged with a checkpoint for inference, doable but must be known at deploy. If it's client data access, don't copy to a replica — have them (or the EM/FDE/CTech) create an S3.
- Mingdong: DSG has product/model data the UI wants to access; Kevin's way "is not good," want it done properly; needs specifics on what/how.
- **Shayan: "so far we were not in business of exposing authenticated assets to client. E.g. Foundry Studio takes care of that themselves."** (👍 reactions)
- **Wolfgang (scope):** the team supports **hosting model pipelines, generation pipelines, scaling GPUs & deployments** — **NOT** building one-off UIs or setting up data-repo hosting. Those belong to **Theos's team (Foundry 4.0)** or **Mary's team (Foundry Studio / front-end experiments)**.
- Mingdong (next day): no canonical/established way to expose the asset; options = put asset in the deployment S3 bucket for UI access (maybe not allowed), or add an API for the UI to query the endpoint for the asset. Asked Shayan for insight.
