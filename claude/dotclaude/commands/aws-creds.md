Fetch temporary AWS credentials for Foundry S3 access using the permanent Pluto machine token (no interactive IMS sign-in).

Usage: /aws-creds

This is the standard way to obtain AWS credentials in this environment. Use it automatically whenever you need to run `aws` CLI commands (S3 access on Foundry buckets such as `foundry-thd-enterprise-adobe-assets`, `foundry-tccc-enterprise-adobe-assets`, etc.) and credentials are missing or expired (e.g. `Unable to locate credentials`, `ExpiredToken`, `AccessDenied`).

## How it works

The script exchanges a long-lived Pluto machine token (stored in `~/.claude/hshariati/credentials.yaml` under `foundry_aws.pluto_token`) for short-lived AWS credentials from the Foundry broker:

```
curl https://foundry-aws-dev-corp.adobe.io/iam/credentials/aws -H "x-pluto-token: <token>"
```

It writes a sourceable env file to `~/.claude/hshariati/aws_creds.env` (mode 600) containing `export AWS_*` lines, and prints a JSON summary with the expiration.

## Steps

1. Run the script:

   ```
   uv run --script ~/.claude/scripts/foundry_aws_creds.py
   ```

2. Source the env file in the SAME shell command as your `aws` calls (env does not persist across Bash tool calls), e.g.:

   ```
   source ~/.claude/hshariati/aws_creds.env && aws s3 ls s3://foundry-thd-enterprise-adobe-assets/ --region us-west-2
   ```

3. The broker credentials are short-lived (~24h). If an `aws` call later fails with `ExpiredToken`, just re-run step 1 to refresh, then re-source.

## Notes

- The Pluto token itself is long-lived (current one expires 2026-11-27). To rotate it, replace `foundry_aws.pluto_token` in `~/.claude/hshariati/credentials.yaml`, or drop a fresh raw token into `~/Downloads/creds.txt` (the script falls back to that).
- Token resolution order: `--token` arg → `PLUTO_TOKEN` env → `credentials.yaml` → `~/Downloads/creds.txt`.
- Default region is `us-west-2`.
