# Connect AWS bucket to the Role
Below is a clear, copy/paste-ready guide to connect your existing S3 bucket and IAM role for use with Google Cloud Storage Transfer Service (THD pushes data into your S3).

Your resources
- S3 bucket: arn:aws:s3:::foundry-dropbox-thd-enterprise
- IAM role: arn:aws:iam::324037283113:role/foundry-data-transfer-service-role

What you’ll need from THD
- THD’s GCP project number (a numeric value). Google STS will send this as sts:ExternalId. You must require that exact value in your role trust policy.

Official references
- Configure access to AWS for S3 destination: https://cloud.google.com/storage-transfer/docs/configure-access-to-aws#s3-destination
- Create transfers to Amazon S3 (agentless): https://cloud.google.com/storage-transfer/docs/create-transfers/agentless/s3
- IAM trust policy basics: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html#roles-creatingrole-trust-policy
- S3 bucket policies: https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html

Decisions to make
- DESTINATION PREFIX in S3 (recommended): choose a folder/prefix where all THD files will land, e.g., thd/raw/ (you can use empty prefix if you prefer bucket root)
- Encryption: if you use default SSE-S3 (AES-256), no extra steps. If you require SSE-KMS, you’ll need to allow this role to use your KMS key.

Part A — AWS Console (GUI) steps

1) Verify S3 bucket settings
- Go to AWS Console → S3 → Buckets → foundry-dropbox-thd-enterprise
- Recommended checks (not strictly required for STS):
  - Permissions → Block public access: all four ON
  - Properties → Object Ownership: Bucket owner enforced (if you enable this, you don’t need PutObjectAcl in role permissions; do not enable if you rely on ACLs today)
  - Properties → Default encryption: enable (AES-256) or KMS key as per your policy
  - Note the bucket Region (top-right), e.g., us-east-1

### HS: you can check ownership like this too:
aws s3api get-bucket-ownership-controls \
  --bucket foundry-dropbox-thd-enterprise \
  --query 'OwnershipControls.Rules[0].ObjectOwnership' \
  --output text

For us: BucketOwnerEnforced


3) Attach least-privilege S3 permissions to the role
- Console → IAM → Roles → foundry-data-transfer-service-role → Permissions
- Add permissions policy (you can add an inline policy “Add inline policy” → JSON)
- If Object Ownership is Bucket owner enforced: you do NOT need s3:PutObjectAcl. Otherwise include it.

Option A (BucketOwnerEnforced = true) — no PutObjectAcl:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListBucket",
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads"
      ],
      "Resource": "arn:aws:s3:::foundry-dropbox-thd-enterprise",
      "Condition": {
        "StringLike": {
          "s3:prefix": [ "thd/raw/*", "" ]
        }
      }
    },
    {
      "Sid": "WriteObjects",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": "arn:aws:s3:::foundry-dropbox-thd-enterprise/thd/raw/*"
    }
  ]
}
```

Option B (if not using BucketOwnerEnforced) — include PutObjectAcl:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListBucket",
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads"
      ],
      "Resource": "arn:aws:s3:::foundry-dropbox-thd-enterprise",
      "Condition": {
        "StringLike": {
          "s3:prefix": [ "thd/raw/*", "" ]
        }
      }
    },
    {
      "Sid": "WriteObjects",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": "arn:aws:s3:::foundry-dropbox-thd-enterprise/thd/raw/*"
    }
  ]
}
```
- Replace thd/raw/ with the prefix you want (or remove the prefix path to allow bucket root).

4) (Optional) Add a restrictive bucket policy (extra defense)
- Console → S3 → Bucket → Permissions → Bucket policy → Edit
- Example (allows only your role to write under the chosen prefix and denies non-SSL):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonSSL",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::foundry-dropbox-thd-enterprise",
        "arn:aws:s3:::foundry-dropbox-thd-enterprise/*"
      ],
      "Condition": { "Bool": { "aws:SecureTransport": "false" } }
    },
    {
      "Sid": "AllowWritesFromTransferRole",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::324037283113:role/foundry-data-transfer-service-role" },
      "Action": [ "s3:PutObject", "s3:AbortMultipartUpload" ],
      "Resource": "arn:aws:s3:::foundry-dropbox-thd-enterprise/thd/raw/*"
    }
  ]
}
```
Note: ExternalId enforcement happens in the role’s trust policy, not bucket policy.

5) (Only if using SSE-KMS) allow role on KMS key
- If bucket default encryption uses a CMK, ensure the KMS key policy allows this role:
  - kms:Encrypt, kms:GenerateDataKey*, kms:DescribeKey

6) Provide THD these values
- S3 bucket name: foundry-dropbox-thd-enterprise
- S3 region: (from bucket Properties)
- Destination prefix: e.g., thd/raw/ (or blank if you want bucket root)
- IAM role ARN: arn:aws:iam::324037283113:role/foundry-data-transfer-service-role
- If SSE-KMS: KMS key ARN
They’ll configure a Storage Transfer job to S3 with your role ARN. Google will send their GCP project number as ExternalId; your trust policy must match it.




# Setting up the SFTP
Got it. Here’s a detailed, AWS Console-first runbook to set up an AWS Transfer Family SFTP endpoint that lands uploads into your S3 bucket, with CLI equivalents for each step.

Resources
- S3 bucket: arn:aws:s3:::foundry-dropbox-thd-enterprise
- IAM role to use for S3 access: arn:aws:iam::324037283113:role/foundry-data-transfer-service-role

Notes
- If this role is also used for other integrations, you can still use it by adding Transfer Family as a trusted principal and ensuring S3 permissions are sufficient. If you prefer isolation, create a dedicated role for Transfer (same permissions/trust).
- If your bucket uses SSE-KMS, ensure the role can use the CMK (kms:Encrypt, kms:GenerateDataKey*, kms:DescribeKey) and the CMK key policy allows this role.

Step 0 — Prereqs
- Get THD’s SSH public key (ed25519 recommended). You’ll need this when creating the SFTP user.
- Identify the S3 bucket Region (S3 → Buckets → foundry-dropbox-thd-enterprise → upper right shows region).

1) Prepare/verify the S3 bucket
Console (GUI)
- S3 → Buckets → foundry-dropbox-thd-enterprise:
  - Permissions → Block public access: turn all 4 ON.
  - Permissions → Object Ownership: if possible, set to Bucket owner enforced (removes ACLs; simplifies permissions).
  - Properties → Default encryption: enable SSE-S3 (AES-256) or SSE-KMS per policy.
  - Optional: Permissions → Bucket Policy → add:
    - Deny non-SSL
    - Allow writes from your role (extra defense, not required)

CLI (optional)
- Check ownership:
  aws s3api get-bucket-ownership-controls --bucket foundry-dropbox-thd-enterprise --query 'OwnershipControls.Rules[0].ObjectOwnership' --output text
- Set BucketOwnerEnforced:
  aws s3api put-bucket-ownership-controls --bucket foundry-dropbox-thd-enterprise --ownership-controls 'Rules=[{ObjectOwnership=BucketOwnerEnforced}]'
- Block public access:
  aws s3api put-public-access-block --bucket foundry-dropbox-thd-enterprise --public-access-block-configuration '{"BlockPublicAcls":true,"IgnorePublicAcls":true,"BlockPublicPolicy":true,"RestrictPublicBuckets":true}'
- Default encryption (SSE-S3):
  aws s3api put-bucket-encryption --bucket foundry-dropbox-thd-enterprise --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

2) Update the IAM role (trust + permissions)
A. Trust relationship: add AWS Transfer Family as a trusted principal
Console (GUI)
- IAM → Roles → foundry-data-transfer-service-role → Trust relationships → Edit
- Add a statement allowing transfer.amazonaws.com to assume the role (do not remove your existing statements):
{
  "Sid": "AllowAWSTransferAssume",
  "Effect": "Allow",
  "Principal": { "Service": "transfer.amazonaws.com" },
  "Action": "sts:AssumeRole"
}
CLI (replaces the assume-role document; if you have existing statements, merge them first)
- Save merged trust-policy.json including both your existing statements (e.g., for Google STS) and this Transfer statement:
aws iam update-assume-role-policy --role-name foundry-data-transfer-service-role --policy-document file://trust-policy.json


### hs give me the final thing to paste
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowEC2AndTransferToAssume",
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "ec2.amazonaws.com",
          "transfer.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```


B. S3 permissions: ensure role can write to your bucket root (no prefix)
Console (GUI)
- IAM → Roles → foundry-data-transfer-service-role → Permissions → Add inline policy → JSON:
- If Object Ownership = BucketOwnerEnforced (no ACLs needed):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListBucket",
      "Effect": "Allow",
      "Action": [
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads"
      ],
      "Resource": "arn:aws:s3:::foundry-dropbox-thd-enterprise"
    },
    {
      "Sid": "WriteObjects",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": "arn:aws:s3:::foundry-dropbox-thd-enterprise/*"
    }
  ]
}
```
- If NOT BucketOwnerEnforced, add "s3:PutObjectAcl" to WriteObjects actions.


3) Create the AWS Transfer Family SFTP server
Console (GUI)
- AWS Transfer Family → Servers → Create server
  - Protocols: SFTP
  - Identity provider: Service managed
  - Endpoint type: Public (simplest). If THD requires IP allow-lists and fixed egress, use VPC endpoint + NLB.
  - (Optional) Logging: enable CloudWatch logging (you’ll be prompted to set a logging role)
- Create. Note the Server ID (e.g., s-1234567890abcdef).

### HS: server id:
id: "s-ad148db7c0be4c279"
endpoint: "s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com"
sftp -o StrictHostKeyChecking=accept-new -i ~/.ssh/id_ed25519 hs_test_user@s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com

CLI
aws transfer create-server --protocols SFTP --identity-provider-type SERVICE_MANAGED --endpoint-type PUBLIC
- Save the "ServerId" from the output.


### HS: should I create a log group?
- CloudWatch log group
  - What it is: A container in CloudWatch Logs where your Transfer Family server writes activity logs (logins, uploads, errors).
  - Use existing vs new:
    - Existing `/aws/eks/foundry-services/cluster`: mixes SFTP logs with EKS logs; retention/permissions get intertwined; harder to search.
    - Recommended: create a dedicated group (e.g., `/aws/transfer/foundry-thd-sftp`) with its own retention and permissions.
  - Console steps:
    - CloudWatch → Logs → Log groups → Create log group → name `/aws/transfer/foundry-thd-sftp` → set Retention (e.g., 30–90 days).
    - In Transfer Family “Create server”, enable logging, select that log group. If prompted, allow creation of the service-linked role.
  - CLI:
    - Create group:
      ```bash
      aws logs create-log-group --log-group-name /aws/transfer/foundry-thd-sftp
      aws logs put-retention-policy --log-group-name /aws/transfer/foundry-thd-sftp --retention-in-days 90
      ```
    - After server is created, you can keep using the console to attach this log group. (Transfer creates/uses a service-linked role: AWSServiceRoleForTransfer.)

- Managed workflows
  - What it is: Built-in, server-side file-processing pipelines that run on events like “on upload” (implemented via Step Functions). Steps can move/copy/tag files, invoke Lambda, decrypt, notify SNS/SQS, etc.
  - Do you need it? Not for simple “THD uploads → files land in S3”. Start without. Add later if you want auto-move to dated prefixes, checksum/AV checks, or notifications.
  - Console steps (if/when you add one):
    - AWS Transfer Family → Workflows → Create workflow → Trigger: On upload → Add steps (e.g., Copy to s3://bucket/final/, Invoke Lambda, Tag object) → Pick an IAM role that can access your bucket/KMS → Create.
    - Attach workflow: Server → Users → Edit user → Add workflow (on-upload).
  - Notes:
    - Workflows run after the file upload completes (atomic handoff).
    - Keep IAM role least-privileged to only required S3 prefixes/KMS keys.




4) Create THD SFTP user(s) bound to your bucket
You’ll need THD’s SSH public key.

Console (GUI)
- Transfer Family → Servers → select your server → Users → Add user
  - Username: thd_ingest (or per-user)
  - Role: arn:aws:iam::324037283113:role/foundry-data-transfer-service-role
  - Home directory type: PATH
  - Home directory: /foundry-dropbox-thd-enterprise/
  - SSH public keys: paste from THD’s .pub key file
- Save.

CLI
```bash
SERVER_ID=s-ad148db7c0be4c279
ROLE_ARN=arn:aws:iam::324037283113:role/foundry-data-transfer-service-role
aws transfer create-user \
  --server-id "$SERVER_ID" \
  --user-name thd_ingest \
  --role "$ROLE_ARN" \
  --home-directory "/foundry-dropbox-thd-enterprise/" \
  --home-directory-type /foundry-dropbox-thd-enterprise/ \
  --ssh-public-key-body "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDYHzfaTZ5saeb5UmNTOzN9SCLfHt0GdZ98Hzx4BrXei hshariati@hoomans-MacBook-Pro.local"
```
5) Get and share connection details with THD
Console (GUI)
- Transfer Family → Servers → select your server → Endpoints
  - Copy the Endpoint hostname (e.g., s-xxxxxxxxx.server.transfer.us-east-1.amazonaws.com)

Share with THD:
- Host: the endpoint hostname
- Port: 22
- Username: thd_ingest (or the one you created)
- Auth: their SSH private key (they keep it; you stored the public key)
- Start path: their client lands in S3 bucket root (you set home directory to /foundry-dropbox-thd-enterprise/)


6) Time-limited access (expire credentials)
- Disable/delete user at the agreed time:
  Console: Transfer Family → Servers → Users → select user → Delete
  CLI: aws transfer delete-user --server-id "$SERVER_ID" --user-name thd_ingest
- Or rotate/remove the user’s SSH public key:
  Console: Edit user → remove key → Save
  CLI: aws transfer update-user --server-id "$SERVER_ID" --user-name thd_ingest --ssh-public-key-body "ssh-ed25519 NEWKEY..."
- You can automate expiry with EventBridge Scheduler + Lambda calling delete-user.

7) Verify and monitor
- THD test:
  sftp -i ~/.ssh/thd_adobe_sftp thd_ingest@<endpoint>
  put /path/to/sample.file
- Adobe verify: confirm object appears in s3://foundry-dropbox-thd-enterprise/
- Monitoring:
  - Transfer Family dashboard & CloudWatch logs (if enabled)
  - S3 bucket metrics/CloudTrail data events for object-level audit (optional)
- Hygiene:
  - Add S3 lifecycle rule to abort incomplete multipart uploads after 7 days.
  - Keep public access blocked.



### HS: this is how I tested
0. I create a test user on the SFTP on aws.
1. On my mac the private key (whose public version we put in aws hs_test_user) in .ssh/id_25519
2. You can connect to the SFTP server like this:
```bash
sftp -o StrictHostKeyChecking=accept-new -i path/to/ssh/private/key USERNAME@s-xxxxxxxxx.server.transfer.us-west-2.amazonaws.com
```
you can read the endpoint of your SFTP from aws.
The USERNAME is the one created for the SFTP.
So I ran
```bash
sftp -o StrictHostKeyChecking=accept-new -i ~/.ssh/id_ed25519 hs_test_user@s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com
```

Above will not work after the first time you try it, change the host checking to no:
```bash
sftp -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519 hs_test_user@s-ad148db7c0be4c279.server.transfer.us-west-2.amazonaws.com
```

3. You can you this command to put files on the server
```bash
put path/to/file
```
like:
```bash
sftp> put outputs/thd_prompts/images/1.png
Uploading outputs/thd_prompts/images/1.png to /foundry-dropbox-thd-enterprise/hs_test_user/1.png
1.png                                                        100% 2417KB   1.4MB/s   00:01
sftp>
```
4. check with
```bash
aws s3 ls s3://foundry-dropbox-thd-enterprise/
```


### Best way to upload a folder to SFTP
Use SFTP’s recursive upload; for speed/resume, use lftp mirror. Don’t use scp/rsync (not supported by AWS Transfer SFTP).

- Quick (interactive SFTP)
```bash
sftp -o StrictHostKeyChecking=accept-new -i ~/.ssh/id_ed25519 USER@s-xxxxxxxx.server.transfer.<region>.amazonaws.com
# inside sftp:
lcd /path/to/local_folder
cd /foundry-dropbox-thd-enterprise/
put -r .
bye
```
Notes:
- put -r local_folder uploads the whole folder
- mput -r local_folder/* skips dotfiles; use put -r to include them
- Faster: start sftp with bigger buffers: sftp -B 524288 -R 128 ...

- Non-interactive (one-shot)
```bash
sftp -o StrictHostKeyChecking=accept-new -i ~/.ssh/id_ed25519 USER@s-xxxxxxxx.server.transfer.<region>.amazonaws.com << 'EOF'
lcd /path/to/local_folder
cd /foundry-dropbox-thd-enterprise/
put -r .
bye
EOF
```

- Faster and resumable (recommended): lftp mirror with parallel transfers
```bash
lftp -u USER,sftp://s-xxxxxxxx.server.transfer.<region>.amazonaws.com << 'EOF'
set sftp:connect-program "ssh -a -x -i ~/.ssh/id_ed25519"
set net:timeout 30
set net:max-retries 100
set xfer:clobber on
mirror -R --parallel=8 --continue /path/to/local_folder /foundry-dropbox-thd-enterprise/
bye
EOF
```
- --parallel controls concurrent files; --continue resumes partial uploads.