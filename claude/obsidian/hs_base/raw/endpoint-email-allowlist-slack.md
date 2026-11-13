# HP endpoint email allowlist — Slack thread (raw)

> Source: Slack thread (Foundry). Captured 2026-07-08. Immutable — do not edit.

**Hooman Shariati [6:04 PM]**
@mingdongw HP is requesting for us to white list these two email addresses in our deployment so that
they can hit our endpoint as well:
evgeny.makharadze@hp.com
mirian-thayse.geiser@hp.com
_(Saved for later)_

**Shayan Hoshyari [7:47 PM]**
feel free to make a PR 🙂
https://github.com/Adobe-Firefly/colligo/blob/main/managed_services/services/firefly/foundry/deploys/customer_gateway/prerelease/configmap.yaml#L74
Add an `allowlisted_emails` section and add them
