Provision S3 storage infrastructure for a new Foundry customer. Creates the Terraform config, opens a PR, and runs plan/apply.

Usage: /new-customer-storage <company-slug> [display_name="Display Name"] [aws_profile=foundry-prd]

Parse $ARGUMENTS to extract:
- **company-slug** (required): short lowercase identifier used in bucket names (e.g. `acme`, `sony-music`). Everything that isn't a key=value pair.
- **display_name** (optional): human-readable name for tags (e.g. "Acme Corp"). If not provided, derive from the slug by title-casing and replacing hyphens with spaces.
- **aws_profile** (optional): AWS profile for terraform commands. Defaults to `foundry-prd`.

If the slug is missing or ambiguous, ask the user before proceeding.

---

## Step-by-step execution

### 1. Validate the slug

- Must be lowercase, alphanumeric + hyphens only.
- Must NOT already exist in `foundry-prd/storage.tf` (grep for `module "<slug>_storage"`). If it does, tell the user and stop.

### 2. Create a feature branch

```bash
cd /Users/hshariati/foundry
git checkout main && git pull origin main
git checkout -b hshariati/feat/<slug>-storage
```

### 3. Add the Terraform module to `foundry-prd/storage.tf`

Append a new module block at the end of the file following the **current convention** (the newer, simpler pattern — no `create_pluto_iam_user`, us-west-2 only, no external IAM user):

```hcl
# ===================
# <Display Name>
# ===================

module "<slug>_storage" {
  source = "../modules/company-storage"

  providers = {
    aws           = aws
    aws.us_east_2 = aws # <slug> uses us-west-2 only; alias required by module but unused
  }

  company = "<slug>"

  franchises = {
    "enterprise" = {
      force_destroy            = false
      create_external_iam_user = false
      asset_storage_regions    = ["us-west-2"]
      tags = {
        Customer  = "<Display Name>"
        Franchise = "Enterprise"
      }
    }
  }

  base_tags = {
    Customer = "<Display Name>"
  }
}
```

Replace `<slug>` and `<Display Name>` with actual values.

### 4. Format

```bash
cd /Users/hshariati/foundry/modeling/terraform && make fix
```

### 5. Commit and push

Stage only the changed file and commit:

```bash
cd /Users/hshariati/foundry
git add modeling/terraform/foundry-prd/storage.tf
git commit -m "[<Display Name>] add customer storage

Add S3 storage module for <Display Name> (<slug>) with enterprise franchise.
Creates dropbox and adobe-assets buckets in us-west-2.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
git push -u origin hshariati/feat/<slug>-storage
```

### 6. Open a PR

```bash
gh pr create --repo Adobe-Firefly/foundry \
  --title "[<Display Name>] add customer storage" \
  --body "$(cat <<'EOF'
## Summary
- Add S3 storage module for **<Display Name>** (`<slug>`) in `foundry-prd/storage.tf`
- Creates `foundry-dropbox-<slug>-enterprise` and `foundry-<slug>-enterprise-adobe-assets` buckets in us-west-2
- Uses the standard `company-storage` module with no external IAM user (gateway-based access)

## Changes
- `modeling/terraform/foundry-prd/storage.tf`: new `module "<slug>_storage"` block

## Testing
- [ ] `terraform plan -target=module.<slug>_storage` reviewed
- [ ] `terraform apply -target=module.<slug>_storage` executed by admin
- [ ] Buckets verified in AWS console

## Dependencies
- Depends on: None

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Show the PR URL to the user.

### 7. Run Terraform plan

Ask the user to confirm they have valid AWS credentials before proceeding. Then:

```bash
cd /Users/hshariati/foundry/modeling/terraform/foundry-prd
AWS_PROFILE=<aws_profile> terraform init
AWS_PROFILE=<aws_profile> terraform plan -target=module.<slug>_storage
```

Show the plan output to the user for review.

### 8. Apply (only on explicit confirmation)

**Do NOT run apply automatically.** Tell the user:

> The PR is ready and the plan is above. When you're ready to apply, say "apply" and I'll run:
> `AWS_PROFILE=<aws_profile> terraform apply -target=module.<slug>_storage`

Only if the user explicitly says to apply:

```bash
cd /Users/hshariati/foundry/modeling/terraform/foundry-prd
AWS_PROFILE=<aws_profile> terraform apply -target=module.<slug>_storage
```

---

## Important notes

- **Never** use `create_pluto_iam_user = true` for new companies — that is legacy.
- **Never** add `us-east-2` to `asset_storage_regions` for new companies — that was temporary.
- The `aws.us_east_2 = aws` provider alias is required by the module interface but points to the default provider since we only use us-west-2.
- There is no CI for Terraform. An admin reviews, applies, and merges.
