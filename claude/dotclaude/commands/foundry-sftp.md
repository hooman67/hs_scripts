Create or manage a Foundry customer SFTP endpoint (AWS Transfer Family) for uploading data into a dropbox S3 bucket, and manage a user's SSH keys. Generates Terraform, opens a PR, and applies ONLY after the PR is approved. Triggers: "create sftp", "sftp endpoint", "add sftp user", "add ssh key", "rotate sftp key", "transfer family".

Usage: /foundry-sftp <operation> [args...]

Operations:
- `create`       — a NEW SFTP server for a customer (its own adhoc Terraform root), with one user + key.
- `add-user`     — add a new user (+ key) to an EXISTING customer's SFTP server.
- `add-key`      — add an ADDITIONAL authorized SSH key to an existing user (old keys keep working).
- `rotate-key`   — REPLACE a user's SSH key (old key stops working — use when a private key is lost/compromised).

This skill is self-contained and portable. It hardcodes no accounts, paths, or credentials — those are read from the repo you run it in and from credentials you supply at apply time.

---

## Ground rules (read first)

1. **PR first, apply later.** Every operation produces a branch + PR. Do **not** apply until the user says the PR is approved AND explicitly tells you to apply.
2. **Credentials are supplied by the user, never stored in this skill.** You only need them at apply time (see "Credentials" below). Never print, echo, or commit them.
3. **Match the repo's conventions.** SFTP infra lives under `modeling/terraform/adhoc/`. Copy the provider/backend block from a sibling adhoc root rather than inventing account IDs or bucket names.
4. **Follow the repo's git workflow** (`AGENTS.md`): never commit to `main`; branch as `<whoami>/sftp/<short-desc>`; end commit messages with the `Co-Authored-By:` trailer that `AGENTS.md` specifies.

---

## 0. Set up shell variables (no personal info baked in)

```bash
REPO="$(git rev-parse --show-toplevel)"      # run this from inside the foundry repo
USER_SLUG="$(whoami)"
ADHOC="$REPO/modeling/terraform/adhoc"
ls "$ADHOC" >/dev/null || { echo "Not in the foundry repo (no modeling/terraform/adhoc)"; exit 1; }
```

Gather the inputs for the chosen operation by asking the user for anything missing:
- **customer slug** (lowercase, e.g. `tesco`, `hp`) and the **dropbox bucket** it uploads into (convention: `foundry-dropbox-<slug>-<franchise>`, usually `-enterprise`).
- **username** for the SFTP user (e.g. the slug, or a sub-tenant like `naou`).
- **home folder** (optional): a subpath inside the bucket to scope the user to (e.g. `NAOU`).
- **SSH public key(s)**: the customer's `ssh-ed25519 …` / `ssh-rsa …` public key string(s).
- For `add-user` / `add-key` / `rotate-key`: the **existing adhoc root** for that customer (`ls "$ADHOC" | grep <slug>`) and, for rotate, which key resource to replace.

---

## 1. Create a feature branch

```bash
cd "$REPO"
git fetch origin main -q
git checkout origin/main -b "$USER_SLUG/sftp/<short-desc>"    # e.g. tesco-sftp, naou-add-user, naou-rotate-key
```

---

## 2. Make the change

### operation: `create` — new SFTP server

Create `modeling/terraform/adhoc/<YYYY-MM>-<slug>-sftp/` with two files.

**providers.tf** — copy it from any sibling adhoc root and change ONLY the backend `key`, so account/region/bucket stay consistent with the repo (nothing hardcoded here):

```bash
NEWDIR="$ADHOC/$(date +%Y-%m)-<slug>-sftp"
mkdir -p "$NEWDIR"
SIBLING="$(ls -d "$ADHOC"/*/ | head -1)"
sed "s#terraform/adhoc/[^\"]*/terraform.tfstate#terraform/adhoc/$(basename "$NEWDIR")/terraform.tfstate#" \
    "$SIBLING/providers.tf" > "$NEWDIR/providers.tf"
```

**main.tf** — write this template, substituting `<slug>`, `<Display Name>`, `<dropbox-bucket>`, `<username>`, `<home-subpath-or-empty>`, and the `<ssh-public-key>`:

```hcl
##########################################################
# AWS Transfer Family SFTP Server for <Display Name>
# Uploads land in the <dropbox-bucket> S3 bucket.
##########################################################

locals {
  dropbox_bucket_name = "<dropbox-bucket>"
  tags = {
    Customer = "<Display Name>"
    Purpose  = "SFTP data upload"
  }
}

data "aws_s3_bucket" "dropbox" {
  bucket = local.dropbox_bucket_name
}

resource "aws_cloudwatch_log_group" "sftp" {
  name              = "/aws/transfer/<slug>-sftp"
  retention_in_days = 30
  tags              = local.tags
}

resource "aws_iam_role" "transfer_logging" {
  name = "foundry-<slug>-sftp-logging"
  tags = local.tags
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "transfer.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
}

resource "aws_iam_role_policy" "transfer_logging" {
  name = "cloudwatch-logs"
  role = aws_iam_role.transfer_logging.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["logs:CreateLogStream", "logs:DescribeLogStreams", "logs:CreateLogGroup", "logs:PutLogEvents"]
      Resource = "${aws_cloudwatch_log_group.sftp.arn}:*"
    }]
  })
}

resource "aws_transfer_server" "this" {
  identity_provider_type = "SERVICE_MANAGED"
  endpoint_type          = "PUBLIC"
  protocols              = ["SFTP"]
  logging_role           = aws_iam_role.transfer_logging.arn
  tags                   = merge(local.tags, { Name = "foundry-<slug>-sftp" })
}

resource "aws_iam_role" "sftp_user" {
  name = "foundry-<slug>-sftp-user"
  tags = local.tags
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "transfer.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
}

resource "aws_iam_role_policy" "sftp_user_s3" {
  name = "s3-dropbox-access"
  role = aws_iam_role.sftp_user.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "AllowListBucket"
        Effect   = "Allow"
        Action   = ["s3:ListBucket", "s3:GetBucketLocation"]
        Resource = data.aws_s3_bucket.dropbox.arn
      },
      {
        Sid      = "AllowObjectOperations"
        Effect   = "Allow"
        Action   = ["s3:PutObject", "s3:GetObject", "s3:GetObjectVersion", "s3:DeleteObject", "s3:DeleteObjectVersion"]
        Resource = "${data.aws_s3_bucket.dropbox.arn}/*"
      },
    ]
  })
}

resource "aws_transfer_user" "<username>" {
  server_id           = aws_transfer_server.this.id
  user_name           = "<username>"
  role                = aws_iam_role.sftp_user.arn
  home_directory_type = "LOGICAL"
  home_directory_mappings {
    entry  = "/"
    target = "/${local.dropbox_bucket_name}<home-subpath-or-empty>"  # e.g. .../NAOU ; leave empty for bucket root
  }
  tags = local.tags
}

resource "aws_transfer_ssh_key" "<username>" {
  server_id = aws_transfer_server.this.id
  user_name = aws_transfer_user.<username>.user_name
  body      = "<ssh-public-key>"
}

output "sftp_endpoint"  { value = aws_transfer_server.this.endpoint }
output "sftp_server_id" { value = aws_transfer_server.this.id }
```

### operation: `add-user` — add a user to an EXISTING server

Edit that customer's existing adhoc `main.tf`. Append a `aws_transfer_user.<username>` (LOGICAL home dir, reusing the existing `aws_iam_role.sftp_user`) and a matching `aws_transfer_ssh_key.<username>`. If the user should be scoped to a subfolder, set the home-dir `target` to `/<bucket>/<Subfolder>` and create that folder at apply time:
`aws s3api put-object --bucket <bucket> --key <Subfolder>/ --region us-west-2`.

### operation: `add-key` — additional key for an existing user

Add a second `aws_transfer_ssh_key.<username>_2` (or `_N`) resource pointing at the same server/user with the new `body`. Existing keys remain valid.

### operation: `rotate-key` — replace a user's key

Change the `body` of the user's existing `aws_transfer_ssh_key.<username>` to the new public key. Terraform replaces it (destroy old + create new), so the old private key stops working. Add a one-line comment noting the rotation date and reason.

---

## 3. Format, commit, push, open PR

```bash
cd "$REPO/modeling/terraform" && terraform fmt -recursive ./adhoc/ >/dev/null
cd "$REPO"
git add modeling/terraform/adhoc/<changed-path>
git commit -m "<concise summary>

<what changed and why>

$(sed -n 's/^.*\(Co-Authored-By:.*\)$/\1/p' "$REPO/AGENTS.md" | head -1)"
git push -u origin "$USER_SLUG/sftp/<short-desc>"
gh pr create --repo Adobe-Firefly/foundry --title "<title>" --body "<summary, changes, apply plan, testing>"
```

Show the PR URL. Then **stop** and tell the user:

> PR is up. Once it's approved, tell me to apply and I'll run plan → apply and verify.

---

## 4. Credentials (only at apply time)

When the user is ready to apply, prompt them:

> Paste your klam-vended AWS credentials into a text file (lines like `aws_access_key_id=…`, `aws_secret_access_key=…`, `aws_session_token=…`) and tell me the path. I'll load them into a local AWS profile without printing them.

Then load them WITHOUT echoing (avoids leaking secrets into the transcript/shell history). Substitute `<CRED_FILE>` with the path they gave:

```bash
python3 - "<CRED_FILE>" <<'PY'
import configparser, pathlib, os, sys
src = pathlib.Path(sys.argv[1]).expanduser()
vals = {}
for line in src.read_text().splitlines():
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1); vals[k.strip()] = v.strip()
cfg = pathlib.Path.home() / ".aws" / "credentials"
cfg.parent.mkdir(mode=0o700, exist_ok=True)
cp = configparser.ConfigParser()
if cfg.exists(): cp.read(cfg)
prof = "foundry-sftp"
if not cp.has_section(prof): cp.add_section(prof)
for k in ("aws_access_key_id", "aws_secret_access_key", "aws_session_token"):
    if k in vals: cp.set(prof, k, vals[k])
    else: cp.remove_option(prof, k)
with open(cfg, "w") as f: cp.write(f)
os.chmod(cfg, 0o600)
print("loaded profile foundry-sftp")
PY
AWS_PROFILE=foundry-sftp aws sts get-caller-identity --query Arn --output text
```

klam credentials are short-lived. On `ExpiredToken`/`InvalidClientTokenId`, ask the user to refresh the file and re-run the block.

---

## 5. Apply (only after PR approval + explicit "apply")

```bash
cd "$REPO/modeling/terraform/adhoc/<changed-path>"
AWS_PROFILE=foundry-sftp terraform init -reconfigure
AWS_PROFILE=foundry-sftp terraform plan -no-color -out=tfplan.bin
```

Review the plan and confirm it matches intent (e.g. `create` = new server+user+key; `add-key` = 1 to add; `rotate-key` = 1 add + 1 destroy of the key only; nothing unexpected destroyed). Then apply the reviewed plan (do NOT use `-auto-approve`):

```bash
AWS_PROFILE=foundry-sftp terraform apply -no-color tfplan.bin
rm -f tfplan.bin
```

---

## 6. Verify and report

```bash
SID="$(AWS_PROFILE=foundry-sftp terraform output -raw sftp_server_id 2>/dev/null)"   # for `create`; otherwise use the known server id
AWS_PROFILE=foundry-sftp aws transfer describe-user --server-id "$SID" --user-name "<username>" --region us-west-2 \
  --query "User.{Home:HomeDirectoryMappings[0].Target, Keys:SshPublicKeys[].SshPublicKeyBody}" --output json
```

Confirm the expected user/home-dir/keys, then give the user the connection details:

- **Username:** `<username>`
- **Command:** `sftp <username>@<endpoint>` (endpoint = the `sftp_endpoint` output, or `<server-id>.server.transfer.us-west-2.amazonaws.com`)
- Key-based auth, no password. Optionally compute the key fingerprint for the customer to confirm: `ssh-keygen -lf <(echo "<ssh-public-key>")`.

Remind the user the PR is applied but must be **merged** to keep `main` in sync with the live server.

---

## Notes
- S3 buckets/keys are immutable to rename; `rotate-key` replaces the key resource. A `create` requires the dropbox bucket to already exist (provision it first with `/new-customer-storage`).
- There is no CI for Terraform — an admin reviews the PR, and apply happens here after approval.
