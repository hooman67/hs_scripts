# THD → Adobe Data Transfer
## Push from Google Cloud Storage to Amazon S3 using Google Cloud Storage Transfer Service (Agentless)

Audience: THD GCP administrators and security reviewers

Goal: THD schedules an automated, secure transfer from a GCS bucket to an Adobe-owned S3 bucket without sharing any long‑lived credentials.

---

## Key Points
- No HMAC or service account keys are shared with Adobe.
- Adobe provides an AWS IAM Role ARN that Google Cloud Storage Transfer Service (STS) will assume using an External ID (THD’s GCP project number).
- THD configures the transfer in Google Cloud; Adobe prepares the S3 role and bucket.

---

## Official Documentation
- Google Cloud • Storage Transfer Service overview: `https://cloud.google.com/storage-transfer/docs/overview`
- Google Cloud • Configure access to AWS (S3 destination): `https://cloud.google.com/storage-transfer/docs/configure-access-to-aws#s3-destination`
- Google Cloud • Create transfer to Amazon S3 (agentless): `https://cloud.google.com/storage-transfer/docs/create-transfers/agentless/s3`
- AWS • S3 bucket policies: `https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html`
- AWS • IAM trust policies (sts:AssumeRole): `https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html#roles-creatingrole-trust-policy`

---

## Information to Exchange (One‑Time)
Adobe → THD:
- AWS S3 bucket name: `<ADOBE_BUCKET_NAME>`
- AWS region: `<ADOBE_REGION>` (e.g., `us-east-1`)
- AWS IAM role ARN for STS to assume: `<ADOBE_ROLE_ARN>`

THD → Adobe:
- THD GCP project number: `<THD_PROJECT_NUMBER>` (used as External ID)

No secrets or keys are exchanged.

---

## High‑Level Steps
1) Adobe configures an AWS IAM role that allows Google’s Storage Transfer Service to assume the role (conditioned on `sts:ExternalId == <THD_PROJECT_NUMBER>`) and grants write access to the Adobe S3 bucket.
2) THD enables Google Cloud APIs and creates a Storage Transfer job from GCS → S3 using the Adobe role ARN.
3) THD schedules/monitors the transfer and can run on‑demand or recurring jobs.

---

## Step 1 (Adobe, for context): Prepare AWS Role and S3 Bucket

Adobe performs this step. Provided here so THD security can review.

1. Create/identify S3 bucket `<ADOBE_BUCKET_NAME>` in region `<ADOBE_REGION>`.
2. Create an IAM role (e.g., `adobe-gcs-ingest-role`) and attach a permissions policy that allows writing to the target bucket/prefix.

Example permissions policy (attached to the role):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3Write",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:AbortMultipartUpload",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": [
        "arn:aws:s3:::<ADOBE_BUCKET_NAME>",
        "arn:aws:s3:::<ADOBE_BUCKET_NAME>/<OPTIONAL_PREFIX>*"
      ]
    }
  ]
}
```

3. Configure the role’s trust policy to allow Google’s Storage Transfer Service to assume the role, constrained by THD’s GCP project number as `sts:ExternalId`.

Use the AWS account IDs listed in Google’s doc for S3 destination: `https://cloud.google.com/storage-transfer/docs/configure-access-to-aws#s3-destination`.

Example trust policy (Adobe sets, values to be replaced):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowGoogleSTSAssume",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::<GOOGLE_STS_AWS_ACCOUNT_ID>:root" },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<THD_PROJECT_NUMBER>"
        }
      }
    }
  ]
}
```

Adobe shares the resulting role ARN (`<ADOBE_ROLE_ARN>`) with THD.

---

## Step 2 (THD): Enable Required Google Cloud APIs

Console (UI):
1. Navigate to Google Cloud Console → APIs & Services → Library.
2. Enable:
   - Storage Transfer API
   - Cloud Resource Manager API

CLI:
```bash
gcloud services enable storagetransfer.googleapis.com cloudresourcemanager.googleapis.com \
  --project=<THD_PROJECT_ID>
```

Identify your project number (used as External ID):
```bash
gcloud projects describe <THD_PROJECT_ID> --format="value(projectNumber)"
```

---

## Step 3 (THD): Prepare or Confirm Source GCS Bucket

Console (UI):
1. Cloud Storage → Buckets → select or create the source bucket (e.g., `gs://thd-adobe-export`).
2. Confirm object layout and optional prefix to transfer (e.g., `exports/daily/`).

CLI (optional checks):
```bash
gsutil ls gs://<THD_SOURCE_BUCKET>/<OPTIONAL_PREFIX>
```

---

## Step 4 (THD): Create Storage Transfer Job (GCS → S3)

Console (UI):
1. Open Storage Transfer Service: `https://console.cloud.google.com/transfer`
2. Click "Create transfer job".
3. Source: Cloud Storage
   - Bucket: `gs://<THD_SOURCE_BUCKET>`
   - Optional prefix: `<OPTIONAL_PREFIX>`
4. Destination: Amazon S3
   - S3 bucket: `<ADOBE_BUCKET_NAME>`
   - AWS role ARN: `<ADOBE_ROLE_ARN>`
   - AWS region: `<ADOBE_REGION>`
   - Optional destination prefix: `<OPTIONAL_DEST_PREFIX>`
5. Options:
   - Overwrite behavior: choose based on requirements (e.g., overwrite or skip existing)
   - Delete from source: typically OFF
   - Metadata preservation: as needed
6. Schedule:
   - On‑demand (run now) or recurring (hourly/daily/weekly at set time)
7. Review and Create.

CLI (example skeleton; consult `gcloud help transfer jobs create` for latest flags):
```bash
gcloud transfer jobs create \
  --source=gs://<THD_SOURCE_BUCKET>/<OPTIONAL_PREFIX> \
  --destination=s3://<ADOBE_BUCKET_NAME>/<OPTIONAL_DEST_PREFIX> \
  --destination-aws-role-arn=<ADOBE_ROLE_ARN> \
  --destination-aws-region=<ADOBE_REGION> \
  --description="THD → Adobe GCS to S3 transfer" \
  --schedule-start-date=2025-10-16 \
  --schedule-repeats=DAILY \
  --schedule-start-time-of-day=01:00 \
  --project=<THD_PROJECT_ID>
```

Common optional flags:
- `--delete-from-source` (use with caution)
- `--overwrite-when=DIFFERENT` (or `ALWAYS`, `NEVER`)
- `--max-bytes-per-second` to throttle

---

## Step 5 (THD): Test and Monitor

Quick test:
1. Start the job (on‑demand) with a small test prefix.
2. Verify objects arrive in Adobe S3 under the expected destination prefix.

Monitor in GCP:
- Storage Transfer Service → Jobs → Job Details → Transfer logs and metrics

Monitor in AWS (Adobe side):
- S3 object listings and sizes; CloudTrail/IAM Access Analyzer (if enabled)

---

## Troubleshooting Guide

"AccessDenied: Not authorized to assume role":
- Ensure the role trust policy Principal uses the correct Google STS AWS account ID(s) from Google doc.
- Ensure `sts:ExternalId` equals the exact THD project number.

"AccessDenied: PutObject":
- Confirm the role permissions policy includes `s3:PutObject` (and `s3:PutObjectAcl` if ACLs are used) for the exact bucket/prefix.
- Check bucket policy doesn’t block the role.

SSE‑KMS failures:
- KMS key policy must allow the role; role needs `kms:Encrypt` and `kms:GenerateDataKey`.

Nothing transferred:
- Confirm source prefix exists; check skip/overwrite settings; review transfer logs in GCP.

Throttle/Costs:
- Use `--max-bytes-per-second`; schedule off‑peak hours.

---

## Security Notes
- No long‑lived credentials are exchanged.
- Least privilege: scope role policy and bucket policy to specific prefixes.
- External ID binding (project number) mitigates confused‑deputy risk.
- THD can stop transfers by disabling the job in GCP; Adobe can revoke the role.

---

## Appendix A: Example AWS Bucket Policy (Optional, Adobe side)

Adobe may further restrict the bucket to only accept writes from the specific role (and optionally, only when assuming with the expected External ID via a condition key exposure through CloudTrail). A simple allow policy example (attach to bucket, adjust as needed):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowWritesFromTransferRole",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::<ADOBE_ACCOUNT_ID>:role/<ROLE_NAME>" },
      "Action": [
        "s3:PutObject",
        "s3:AbortMultipartUpload"
      ],
      "Resource": "arn:aws:s3:::<ADOBE_BUCKET_NAME>/<OPTIONAL_DEST_PREFIX>*"
    }
  ]
}
```

Note: Bucket policy conditions cannot directly evaluate `sts:ExternalId`; enforce External ID in the role’s trust policy.

---

## Appendix B: Quick Commands (THD)

Enable APIs:
```bash
gcloud services enable storagetransfer.googleapis.com cloudresourcemanager.googleapis.com \
  --project=<THD_PROJECT_ID>
```

Get project number:
```bash
gcloud projects describe <THD_PROJECT_ID> --format="value(projectNumber)"
```

List jobs:
```bash
gcloud transfer jobs list --project=<THD_PROJECT_ID>
```

Describe job:
```bash
gcloud transfer jobs describe <JOB_NAME> --project=<THD_PROJECT_ID>
```

Run job now (on‑demand):
```bash
gcloud transfer jobs run <JOB_NAME> --project=<THD_PROJECT_ID>
```

---

## Contacts
THD: Security Reviewer • GCP Admin Team

Adobe: Integration Owner • S3/Bucket Owner • IAM Admin

---

Version: 1.0  
Last updated: 2025‑10‑16


