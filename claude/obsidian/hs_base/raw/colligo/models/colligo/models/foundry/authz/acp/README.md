# ACP Foundry Authorization

## Runtime Model

The ACP backend is a read-only authorization layer for Foundry traffic. It does not create Projects or mutate ACP policies. Those write operations belong to the future management service and CLI.

At request time, the worker resolves a protected resource to one or more logical entitlements, resolves those entitlements to asset URNs from central config, and performs a two-step RAPI check:

**Step 1 — Discover the RESOLVE URI template (cached per `ACPClient` instance):**
```text
GET platform-cs.adobe.io  →  _links["http://ns.adobe.com/adobecloud/rel/resolve/id"].href
```

**Step 2 — HEAD the resolved URL with the caller's IMS token:**
```text
HEAD {resolve_template.expand(id=asset_urn)}
  Authorization: Bearer {ims_token}
  x-api-key: {x_api_key}
```

The HTTP status code of the HEAD is the authorization decision:
- `200` → authorized
- `403` / `404` → denied
- other → denied, logged as unexpected

The region-specific ACP host comes from ACP itself via the RESOLVE link, not from deployment config.


## In-Process Layers

```text
Worker pipeline
  -> FoundryAuthorizationService protocol
     -> ACPAuthorizationService
        -> AuthorizationCache   (keyed by user_id + asset_urn)
        -> ACPClient
           -> Adobe ACP API (platform-cs.adobe.io)
```

`ACPAuthorizationService` is an in-process policy component, not a separately deployed service. `ACPClient` is the HTTP adapter that talks to Adobe ACP.

## Migration Mode

When both YAML and ACP configs are present, the factory returns a `HybridAuthorizationService`. It allows a request if ACP allows, YAML allows, or both. Logs and metrics record the allow path as `acp`, `yaml`, `both`, or `deny`.

This exists only for migration. Remove it once ACP is authoritative.

## Metadata

Metadata list requests may need to evaluate many asset URNs. The metadata path dedupes configured URNs, uses cached `(user_id, asset_urn)` decisions, and checks cache misses with bounded async fan-out controlled by `metadata_max_concurrent_checks`.

## Follow-Ups

- Review canary latency and decide whether the single-resource authz path must become async.
- Remove temporary ACP+YAML union mode after ACP becomes authoritative.
- Confirm the production ACP `x-api-key` value with ACP/IMS owners.
- Inventory request paths that skip Foundry authz or select NoOp.
- Remove YAML-era alias behavior once ACP entitlement mappings are authoritative.
