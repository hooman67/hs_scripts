## GCP side Setup
### 0) Prereqs on macOS
```bash
# Homebrew (if missing)
which brew || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Google Cloud SDK (gcloud + gsutil)
brew install --cask google-cloud-sdk
# If your shell doesn’t pick it up, add to PATH for zsh:
echo 'source "/opt/homebrew/Caskroom/google-cloud-sdk/latest/google-cloud-sdk/path.zsh.inc"' >> ~/.zshrc
echo 'source "/opt/homebrew/Caskroom/google-cloud-sdk/latest/google-cloud-sdk/completion.zsh.inc"' >> ~/.zshrc
source ~/.zshrc

# AWS CLI, jq (for JSON), and rclone (optional)
brew install awscli jq rclone
```

### 1) Log in to Google Cloud and select your project
```bash
# Log in via browser
gcloud auth login
```

set the project
```bash
gcloud config set project adbe-gcp0805
```


### 2) Enable required APIs
```bash
# IAM Service Account Credentials API (needed to mint tokens as a service account)
gcloud services enable iamcredentials.googleapis.com --project "$PROJECT_ID"

# IAM and Storage APIs (usually already enabled on most projects)
gcloud services enable iam.googleapis.com
gcloud services enable storage.googleapis.com
```


```bash
# see the bucket content
gcloud storage ls gs://hs-test-bucket-for-thd-1
```

```bash
# export PROJECT_ID="gcp-ml-platform-poc"
export PROJECT_ID="adbe-gcp0805"
export BUCKET_NAME="hs-test-bucket-for-thd-1"
export BUCKET_NAME_ADD="gs://hs-test-bucket-for-thd-1"                  
export SA_NAME="thd-aws-push"                          
export SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
export USER_EMAIL="hshariati@adobe.com"
echo "$SA_EMAIL"
```

```bash
# Provided by Adobe/AWS team
export AWS_ROLE_ARN="arn:aws:iam::324037283113:role/thd-wif-s3-push-role"
```

```bash
# create a service account
gcloud iam service-accounts create "${SA_NAME}" \
  --description="Service account to push from GCS to AWS S3 via WIF" \
  --display-name="THD AWS Push"
```

```bash
# test the service account
gcloud iam service-accounts describe "$SA_EMAIL" --project "$PROJECT_ID"
```
My output:
```
description: Service account to push from GCS to AWS S3 via WIF
displayName: THD AWS Push
email: thd-aws-push@adbe-gcp0805.iam.gserviceaccount.com
etag: MDEwMjE5MjA=
name: projects/adbe-gcp0805/serviceAccounts/thd-aws-push@adbe-gcp0805.iam.gserviceaccount.com
oauth2ClientId: '113980419206634734192'
projectId: adbe-gcp0805
uniqueId: '113980419206634734192'
```

```bash
# Give the SA read access to your bucket (if not already)
gcloud storage buckets add-iam-policy-binding "gs://${BUCKET_NAME}" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/storage.objectViewer"
```

```bash
## This worked instead of above:
gcloud storage buckets add-iam-policy-binding "gs://hs-test-bucket-for-thd-1" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/storage.objectViewer"
```

```bash
# Grant yourself Service Account Token Creator on the SA
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --member="user:${USER_EMAIL}" \
  --role="roles/iam.serviceAccountTokenCreator" \
  --project "$PROJECT_ID"
```

```bash
# (Sometimes required by org policy) Also grant Service Account User
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --member="user:${USER_EMAIL}" \
  --role="roles/iam.serviceAccountUser" \
  --project "$PROJECT_ID"
```

```bash
# Verify the binding is in place
gcloud iam service-accounts get-iam-policy "$SA_EMAIL" --project "$PROJECT_ID" \
  --format="table(bindings.role, bindings.members)"
```
My output:
```bash
ROLE                                                                      MEMBERS
['roles/iam.serviceAccountTokenCreator', 'roles/iam.serviceAccountUser']  [['user:hshariati@adobe.com'], ['user:hshariati@adobe.com']]
```

```bash
# Test impersonation and bucket access
gcloud auth print-identity-token \
  --audiences=sts.amazonaws.com \
  --impersonate-service-account="$SA_EMAIL" | head -c 20; echo
```
my output:
```bash
WARNING: This command is using service account impersonation. All API calls will be executed as [thd-aws-push@adbe-gcp0805.iam.gserviceaccount.com].
eyJhbGciOiJSUzI1NiIs
```
```bash
gcloud storage ls --impersonate-service-account="$SA_EMAIL" "$BUCKET_NAME_ADD"

# above didn't work.
gcloud storage ls --impersonate-service-account="$SA_EMAIL" "gs://hs-test-bucket-for-thd-1"
```
my output:
```bash
WARNING: This command is using service account impersonation. All API calls will be executed as [thd-aws-push@adbe-gcp0805.iam.gserviceaccount.com].
gs://hs-test-bucket-for-thd-1/0e11594e-745d-4f34-b2c9-5ab7a03ebcad.mp4
gs://hs-test-bucket-for-thd-1/basebal_i2v_input.jpg
gs://hs-test-bucket-for-thd-1/i2v_input_2.png
```

Adobe/AWS will lock their role trust to this ID.
```bash
gcloud iam service-accounts describe "${SA_EMAIL}" \
  --format="value(oauth2ClientId)"
```

113980419206634734192

Copy the numeric client ID and send it to Adobe/AWS so they can put it into their trust policy as the “accounts.google.com:sub”.


### 8) Mint a Google OIDC token as the service account (test)
```bash
# This produces a JWT OIDC token with aud=sts.amazonaws.com
gcloud auth print-identity-token \
  --audiences=sts.amazonaws.com \
  --impersonate-service-account="${SA_EMAIL}" > /tmp/google_oidc.jwt

# Optional: quick sanity check that file exists and is non-empty
wc -c /tmp/google_oidc.jwt
```

Test on Mac Os with
```bash
payload=$(cut -d. -f2 /tmp/google_oidc.jwt)
pad=$(( (4 - ${#payload} % 4) % 4 ))
payload="${payload}$(printf '%*s' "$pad" '' | tr ' ' '=')"
echo "$payload" | tr '_-' '/+' | base64 -D | jq .
```
My output:
```bash
{
  "aud": "sts.amazonaws.com",
  "azp": "113980419206634734192",
  "exp": 1762395349,
  "iat": 1762391749,
  "iss": "https://accounts.google.com",
  "sub": "113980419206634734192"
}
```


## AWS Side Setup

This is foundry PRD AWS account id
```bash
export ACCOUNT_ID="324037283113"
```

```bash
foundry-data-transfer-service-role
export ROLE_NAME="thd-wif-s3-push-role"
export PROVIDER_ARN="arn:aws:iam::${ACCOUNT_ID}:oidc-provider/accounts.google.com"
```

This is the destination bucket

```bash
export BUCKET_NAME="foundry-dropbox-thd-enterprise" 
```

This is the client ID from here:
  Copy the numeric client ID and send it to Adobe/AWS so they can put it into their trust policy as the “accounts.google.com:sub”.
```bash
export GOOGLE_SUB="113980419206634734192" 
```

* Set your AWS credentials

1) Ensure the OIDC provider for Google exists and allows audience sts.amazonaws.com
- If it already exists, verify it includes the client ID “sts.amazonaws.com”:
```bash
aws iam get-open-id-connect-provider \
  --open-id-connect-provider-arn "$PROVIDER_ARN" \
  --query 'ClientIDList'
```

If "sts.amazonaws.com" not present, add it:
```bash
aws iam add-client-id-to-open-id-connect-provider \
  --open-id-connect-provider-arn "$PROVIDER_ARN" \
  --client-id sts.amazonaws.com
```
or 
- If it does NOT exist, create it in Console (recommended): IAM → Identity providers → Add provider
  - Type: OpenID Connect
  - Provider URL: https://accounts.google.com
  - Audience (client ID): sts.amazonaws.com
  - Save (provider ARN should match $PROVIDER_ARN)

you should see
```bash
  --query 'ClientIDList'
[
    "sts.amazonaws.com"
]
```

2) Create or update the IAM role trust (Web Identity with Google)
MAKE SURE to replace the accounts.google.com:sub with Client Id you got from customer.
- If creating a new role:
```bash
cat > /tmp/trust.json <<'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::324037283113:oidc-provider/accounts.google.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringEquals": {
                    "accounts.google.com:sub": "113980419206634734192"
                }
            }
        }
    ]
}
EOF
sed -i '' "s|PROVIDER_ARN_PLACEHOLDER|$PROVIDER_ARN|" /tmp/trust.json 2>/dev/null || sed -i "s|PROVIDER_ARN_PLACEHOLDER|$PROVIDER_ARN|" /tmp/trust.json
sed -i '' "s|GOOGLE_SUB_PLACEHOLDER|$GOOGLE_SUB|" /tmp/trust.json 2>/dev/null || sed -i "s|GOOGLE_SUB_PLACEHOLDER|$GOOGLE_SUB|" /tmp/trust.json

aws iam create-role \
  --role-name "$ROLE_NAME" \
  --assume-role-policy-document file:///tmp/trust.json
```

3) Attach S3 write permissions for your bucket
```bash
cat > /tmp/s3-policy.json <<'EOF'
{
  "Version":"2012-10-17",
  "Statement":[
    {
      "Sid":"ListBucket",
      "Effect":"Allow",
      "Action":[
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:ListBucketMultipartUploads"
      ],
      "Resource":"arn:aws:s3:::foundry-dropbox-thd-enterprise"
    },
    {
      "Sid":"ReadObjects",
      "Effect":"Allow",
      "Action":[
        "s3:GetObject"
      ],
      "Resource":"arn:aws:s3:::foundry-dropbox-thd-enterprise/*"
    },
    {
      "Sid":"WriteObjects",
      "Effect":"Allow",
      "Action":[
        "s3:PutObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Resource":"arn:aws:s3:::foundry-dropbox-thd-enterprise/*"
    }
  ]
}
EOF

aws iam put-role-policy \
  --role-name "$ROLE_NAME" \
  --policy-name "s3-write-${BUCKET_NAME}-root" \
  --policy-document file:///tmp/s3-policy.json
```
- If you use SSE-KMS on that bucket, also grant the role kms:Encrypt, kms:GenerateDataKey*, kms:DescribeKey on the KMS key and ensure the KMS key policy allows this role.

You need s3:GetObject on the bucket. rclone (and gsutil rsync) do a HEAD on destination objects, which requires GetObject. Add it and retry.




4) Verify role and provider
```bash
aws iam get-role --role-name "$ROLE_NAME" \
  --query 'Role.AssumeRolePolicyDocument.Statement[?Action==`sts:AssumeRoleWithWebIdentity`]'
aws iam get-open-id-connect-provider --open-id-connect-provider-arn "$PROVIDER_ARN" \
  --query 'ClientIDList'
```

you should see
```bash
[
    {
        "Effect": "Allow",
        "Principal": {
            "Federated": "arn:aws:iam::324037283113:oidc-provider/accounts.google.com"
        },
        "Action": "sts:AssumeRoleWithWebIdentity",
        "Condition": {
            "StringEquals": {
                "accounts.google.com:sub": "113980419206634734192",
                "accounts.google.com:aud": "sts.amazonaws.com"
            }
        }
    }
]
[
    "sts.amazonaws.com"
]
```



### This is the command that I finally ran. With their client id that made the setup work
- Add customer’s client ID to the OIDC provider and verify
```bash
export ACCOUNT_ID=324037283113
export PROVIDER_ARN="arn:aws:iam::${ACCOUNT_ID}:oidc-provider/accounts.google.com"

aws iam add-client-id-to-open-id-connect-provider \
  --open-id-connect-provider-arn "$PROVIDER_ARN" \
  --client-id 116308897482333668165

# Keep sts.amazonaws.com too (if missing, add it again)
aws iam add-client-id-to-open-id-connect-provider \
  --open-id-connect-provider-arn "$PROVIDER_ARN" \
  --client-id sts.amazonaws.com

aws iam get-open-id-connect-provider \
  --open-id-connect-provider-arn "$PROVIDER_ARN" \
  --query 'ClientIDList'
# Should show: ["sts.amazonaws.com","116308897482333668165", ...]
```




## GCP / THD side transfer
Exchange the OIDC token for AWS temporary credentials
Requires Adobe/AWS to have completed their side (OIDC provider + role trust to your SA’s client ID).


```bash
```bash
gcloud auth print-identity-token --audiences=sts.amazonaws.com --impersonate-service-account="$SA_EMAIL" > /tmp/google_oidc.jwt
aws sts assume-role-with-web-identity --role-arn "$AWS_ROLE_ARN" --role-session-name thd-gcs-push --web-identity-token file:///tmp/google_oidc.jwt > /tmp/aws_creds.json

export AWS_ACCESS_KEY_ID=$(jq -r '.Credentials.AccessKeyId' /tmp/aws_creds.json)
export AWS_SECRET_ACCESS_KEY=$(jq -r '.Credentials.SecretAccessKey' /tmp/aws_creds.json)
export AWS_SESSION_TOKEN=$(jq -r '.Credentials.SessionToken' /tmp/aws_creds.json)

aws sts get-caller-identity
aws s3 ls s3://foundry-dropbox-thd-enterprise
```
```

My output:
```bash
WARNING: This command is using service account impersonation. All API calls will be executed as [thd-aws-push@adbe-gcp0805.iam.gserviceaccount.com].
{
    "Credentials": {
        "AccessKeyId": "ASIAUW4RARUUU4F47YRU",
        "SecretAccessKey": "iOAHhjDbCgdUKjvsdxLsU0EpSW1vvphehVuTRP46",
        "SessionToken": "FwoGZXIvYXdzEOP//////////wEaDIoN154S4Sn6OZC2FCLXAfbXK67sxxLOHIe9cpnHmERzND/a+qM1WvRIHSP4EYu86FiqweDdAYNUPkl1dp/dKxaTlnz3Z57hj0ZefFCge31MAZ/kC+Xnk8G6yP3qJHQPgQ5hL1TE9euQtFq0WFPFU+vB491V501TcSAyQd6hqqsYlyF/ivsCYRgRNUTBQSn3m4c2FPVXxWbKzJV0GPhAh0XMLLrv3weL3+O7YWk88vuiPxw9VsFfo1NHqr+jHAdZetzsfUFmlHByXPkABwhQoqqajs23SrRtu55uWSowpAhIPatHd5rZKNn3r8gGMlZTrRFSHBT1Rf/852ER2kVeK7xyA/S7G9UDBpZoeff1gBZ0R2j6jWf5VTIDMklcKhICZ35mutG19Wkad8wMKdRctHJBgv5RGqoWTD1F3hJBfzS8qXOoFg==",
        "Expiration": "2025-11-06T02:37:29+00:00"
    },
    "SubjectFromWebIdentityToken": "113980419206634734192",
    "AssumedRoleUser": {
        "AssumedRoleId": "AROAUW4RARUU67MB44IAR:thd-gcs-push",
        "Arn": "arn:aws:sts::324037283113:assumed-role/thd-wif-s3-push-role/thd-gcs-push"
    },
    "Provider": "accounts.google.com",
    "Audience": "113980419206634734192"
}
```




### Transfer using rsync
```bash
gcloud auth print-identity-token --audiences=sts.amazonaws.com --impersonate-service-account="$SA_EMAIL" > /tmp/google_oidc.jwt
aws sts assume-role-with-web-identity --role-arn "$AWS_ROLE_ARN" --role-session-name thd-gcs-push --web-identity-token file:///tmp/google_oidc.jwt > /tmp/aws_creds.json

export AWS_ACCESS_KEY_ID=$(jq -r '.Credentials.AccessKeyId' /tmp/aws_creds.json)
export AWS_SECRET_ACCESS_KEY=$(jq -r '.Credentials.SecretAccessKey' /tmp/aws_creds.json)
export AWS_SESSION_TOKEN=$(jq -r '.Credentials.SessionToken' /tmp/aws_creds.json)
unset AWS_PROFILE AWS_DEFAULT_PROFILE
```

Sanity check creds
aws sts get-caller-identity
my output
```bash
hshariati@hoomans-mbp:~/hs_scripts$ aws sts get-caller-identity
aws s3 ls s3://foundry-dropbox-thd-enterprise
{
    "UserId": "AROAUW4RARUU67MB44IAR:thd-gcs-push",
    "Account": "324037283113",
    "Arn": "arn:aws:sts::324037283113:assumed-role/thd-wif-s3-push-role/thd-gcs-push"
}
```

```bash
cat > /tmp/boto-aws-s3.ini <<EOF
[Credentials]
aws_access_key_id = $AWS_ACCESS_KEY_ID
aws_secret_access_key = $AWS_SECRET_ACCESS_KEY
aws_session_token = $AWS_SESSION_TOKEN
aws_security_token = $AWS_SESSION_TOKEN

[S3]
use-sigv4 = True
host = s3.amazonaws.com
EOF
```


Run transfer
Note: Creds expire at the shown Expiration; refresh by re-running the mint + assume sequence for long transfers.
```bash
BOTO_CONFIG=/tmp/boto-aws-s3.ini gsutil -m rsync -r "gs://${BUCKET_NAME}" "s3://foundry-dropbox-thd-enterprise"
```









### Transfer using rclone
rclone is reliable with short‑lived AWS creds and avoids gsutil/boto quirks.

1) Ensure AWS STS creds are exported
```bash
# You already did the assume-role; just export again to be safe:
export AWS_ACCESS_KEY_ID=$(jq -r '.Credentials.AccessKeyId' /tmp/aws_creds.json)
export AWS_SECRET_ACCESS_KEY=$(jq -r '.Credentials.SecretAccessKey' /tmp/aws_creds.json)
export AWS_SESSION_TOKEN=$(jq -r '.Credentials.SessionToken' /tmp/aws_creds.json)
unset AWS_PROFILE AWS_DEFAULT_PROFILE
```

2) Give rclone GCS access via ADC
```bash
gcloud auth application-default login
```

3) Create rclone remotes (no prompts)
```bash
# GCS remote using ADC
rclone config create gcs gcs

# S3 remote using your exported AWS_* env vars
rclone config create s3 s3 provider=AWS env_auth=true region=us-east-1
```

4) Quick tests
```bash
rclone ls gcs:hs-test-bucket-for-thd-1 | head
rclone ls s3:foundry-dropbox-thd-enterprise | head
```

5) Run the transfer
```bash
rclone sync gcs:hs-test-bucket-for-thd-1 s3:foundry-dropbox-thd-enterprise --fast-list --transfers=32 --checkers=64
```

Notes
- If your S3 bucket requires ACLs (not BucketOwnerEnforced), add: `--s3-acl private` (or the ACL you need).
- If tokens expire mid‑transfer, re-run the mint+assume step to refresh AWS_* env vars, then rerun rclone; it will skip already-synced files.



