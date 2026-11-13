---
name: feedback_full_working_links
description: "Always give complete, working URLs — never truncate; Confluence needs the full title slug"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3cbb9457-99e9-403c-afe4-3af9de424b48
  modified: 2026-08-22T21:21:20.303Z
---

Always give Hooman **complete, working links** — never truncate or shorten a URL you were given.

**Confluence/wiki specifically:** include the full `+`-encoded title slug after the page ID. The bare
`https://wiki.corp.adobe.com/spaces/<SPACE>/pages/<id>/` form (ID only, no title) **does not resolve for
Hooman** — it 404s / doesn't open. Use the full form, e.g.
`https://wiki.corp.adobe.com/spaces/GenAI/pages/3958951510/Colligo+v3+managed_services+Onboarding+an+App+and+Using+the+Repo`.

**Why:** a truncated link wastes his time (he has to hunt for the real one). Tools like Glean/`glean_search`
return the full URL — paste it verbatim; don't abbreviate it in the reply.

**How to apply:** when citing any URL (Confluence, Jira, GitHub, docs.ai, S3/gateway `/asset/...`), copy the
entire URL exactly as the source gives it. For Confluence, if you only have the page ID, fetch/keep the title
slug rather than emitting the ID-only path.
