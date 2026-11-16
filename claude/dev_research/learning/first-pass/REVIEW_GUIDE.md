# Lesson 1 — Understanding a Reliable Video-Processing Service

Updated: **2026-11-12** (authentication explanation added; main design reviewed November 10). This is a teaching guide. Read it before attempting the exercise if these
concepts are new. Interview presentation is a separate section near the end.

We will follow one request through one concrete design, then introduce problems one at a time.
The Amazon Web Services (**AWS**) products below are practical implementation choices, not a requirement to use AWS or deploy
anything now. Examples are illustrative; no service has been built or benchmarked for this lesson.

## Contents

- [1. What are we building?](#1-what-are-we-building)
- [2. The whole design in one picture](#2-the-whole-design-in-one-picture)
- [3. Follow one video through the system](#3-follow-one-video-through-the-system)
  - [How login becomes a trusted tenant](#how-login-becomes-a-trusted-tenant)
- [4. Problem: the client does not know whether submission worked](#4-problem-the-client-does-not-know-whether-submission-worked)
- [5. Problem: the database saves the job but nobody hears about it](#5-problem-the-database-saves-the-job-but-nobody-hears-about-it)
- [6. Problem: a worker crashes or two workers receive the same job](#6-problem-a-worker-crashes-or-two-workers-receive-the-same-job)
- [7. Problem: the output is uploaded but completion is not saved](#7-problem-the-output-is-uploaded-but-completion-is-not-saved)
- [8. Problem: cancellation and completion happen together](#8-problem-cancellation-and-completion-happen-together)
- [9. Now add capacity and customer boundaries](#9-now-add-capacity-and-customer-boundaries)
- [10. Practical alternatives and what we implement](#10-practical-alternatives-and-what-we-implement)
- [11. Check your understanding](#11-check-your-understanding)
- [12. Separately: how to present this in an interview](#12-separately-how-to-present-this-in-an-interview)
- [13. Sources and limits](#13-sources-and-limits)

## 1. What are we building?

A customer has a video and asks our service to resize it. Processing may take minutes. We want to
accept the request quickly, let the customer check progress, and eventually return the output.

A **job** is the saved request to do that work: “resize this particular video using these settings.”
A **worker** is a program running on a machine that actually reads the video and performs the
transformation. These are different things: the job should still exist if its worker crashes.

For this lesson, a **durable** record is one stored so it survives ordinary application-process or
worker restarts. A Python dictionary in the API process would not meet that requirement. Durability
against an entire region being destroyed is a larger requirement we have not promised here.

Why not do everything inside one HTTP request? **HTTP** is the request/response protocol the client
uses to communicate with our service. Keeping a request open for a 60-minute job makes disconnects,
timeouts and restarts difficult to handle. Instead, we separate **submission** from **execution**:

```text
Submit video-processing request → receive job ID quickly
                                        ↓
                            processing continues separately
                                        ↓
Check that job ID later → running, failed, cancelled, or a completed result
```

That separation is called **asynchronous processing**: the initial response arrives before the
requested work finishes. It does not mean the system forgets the work or makes the customer guess.

You can read this lesson in three sittings: sections 1–3 for the basic picture, 4–8 for failures,
and 9–12 for constraints, alternatives and practice. There is no need to memorize all of it at once.

Initially remember only three responsibilities: **remember the request, arrange for work to run,
and remember the outcome**. Everything else below protects one of those responsibilities.

## 2. The whole design in one picture

An **API**—application programming interface—is the set of operations our service exposes, such as
“submit a job” and “get its status.” An **endpoint** is a particular HTTP route implementing an
operation, such as `POST /jobs`.

Our API keeps job records in a database. A database **table** groups records with named fields;
a **row** is one record. The `jobs` table has one row per logical job.

The large videos live elsewhere, in **object storage**: a service that stores files as objects
addressed by a name, with accompanying metadata—small descriptive fields about the object. For
example, Amazon S3 (Simple Storage Service) stores an object inside a
**bucket**, its storage container, under a **key**, the object's name/path within that bucket.

A **queue** holds messages until programs receive them. A **message broker** is a service that
sits between senders and receivers and manages message delivery. Here, Amazon SQS (Simple Queue
Service) supplies that
queue/broker function. “Broker” is not another application we must build beside SQS.

```mermaid
flowchart LR
    C[Customer application] -->|Submit or check status| A[Our API program]
    A -->|Save job and notification note| D[(PostgreSQL on Amazon RDS)]
    D -->|Sender reads unsent notes| P[Our background sender]
    P -->|Send small message| Q[Amazon SQS queue]
    Q -->|Reply to a worker's receive request| W[Our worker programs]
    W -->|Read job and update progress| D
    W -->|Read input and upload output| S[(Amazon S3 videos)]
    D -->|Job state and selected output| A
    A -->|Job ID or status/result| C
```

Read the picture left to right for submission and execution. Then follow the database back to the
API to see how the customer learns the outcome. Workers ask SQS for messages; the arrow from SQS
shows the response, not SQS independently calling our worker.

The small **background sender** is our code, running separately from individual API requests. It
reads saved “tell a worker about this job” notes and sends their messages to SQS. Section 5 explains
why saving that note matters. It is a normal process, not a special AWS service.

### Concrete implementation choices

| Piece | A practical choice for this example | What it does; what we write |
|---|---|---|
| API | Python/FastAPI, running on EC2 or in Amazon ECS | We write request validation, customer access checks, submission, status and cancellation. FastAPI provides the HTTP framework. |
| Job database | Amazon RDS (Relational Database Service) running PostgreSQL | RDS operates the database service; we design the tables and write queries and state-change rules. **Relational** means records are organized into related tables. **SQL** (Structured Query Language) is the language we use to read and change those records. |
| Video storage | Amazon S3 | S3 stores input/output bytes; we decide names, permissions, retention and which output belongs to a completed job. |
| Work queue | Amazon SQS Standard | SQS stores/delivers messages. We write the sending, receiving and failure-handling code. A Standard queue can deliver a message more than once and does not promise strict order. |
| Sender and workers | Our Python programs on EC2, possibly managed using ECS | **EC2** provides virtual machines. **ECS** runs and manages packaged application processes in containers. Our code runs the video transformation on suitable machines; see the processor choices below. |

A **container** packages an application and its dependencies so a runtime can start it consistently.
It does not decide which business job to run or make that job reliable. A **CPU** is a general-purpose
processor; a **GPU** is a processor designed for large amounts of parallel computation, often used
for ML. **FFmpeg** is a practical command-line/library toolkit for processing video and audio. A
resize job might call FFmpeg; a model-based job might run our inference code on a GPU machine.
We can learn this design without first learning a container-management platform such as Kubernetes.

We use PostgreSQL to make the record changes easy to see. DynamoDB is a valid alternative, discussed
later; it is not something we also need alongside PostgreSQL in this example.

## 3. Follow one video through the system

### The request and the job record

Our customer is a company called Acme. A **tenant** is one customer organization whose data and
jobs must be isolated from other customers. Here, `tenant_id = "acme"` is its internal identifier.
The API verifies who is calling, then checks our trusted records to determine which tenant that
caller may act for. Merely putting `"tenant_id": "acme"` in a request does not grant Acme access.

### How login becomes a trusted tenant

There are two separate checks. **Authentication** establishes the caller's identity: “this request
carries valid credentials for user 123.” **Authorization** checks permission: “user 123 belongs to
Acme and may create video jobs.” A successful login alone does not grant access to every customer.

For this example, assume Alice works for Acme and uses our browser application. We use **Amazon
Cognito**, an AWS service for user sign-in, as our **identity provider**: the service responsible for
checking login credentials and issuing evidence of the login. Auth0 or Microsoft Entra ID are other
practical choices. This is a teaching implementation, not a claim about Adobe's sign-in system.

```mermaid
sequenceDiagram
    participant U as Alice's browser application
    participant I as Identity provider: Cognito
    participant A as Our video API
    participant D as Our PostgreSQL database
    U->>I: Sign in using hosted login page
    I-->>U: Login completes and app obtains access token
    U->>A: POST /jobs with access token
    Note over A: Verify token signature, issuer, expiry and intended use
    A->>D: Find active membership for verified user
    D-->>A: user-123 belongs to Acme and may create jobs
    A->>D: Save job with tenant_id set to acme
    A-->>U: 202 with job ID
```

**1. Alice signs in; the provider issues an access token.**

The hosted login page checks her password, passkey or company login, and any required second
factor. Our video API does not need to implement password storage. After successful login, the
application obtains an **access token**: a credential intended for calling permitted APIs for a
limited time. A normal browser integration uses an existing login library and an authorization-code
flow: the app receives a short-lived code and exchanges it for tokens. **PKCE** adds a secret
verifier held by that login attempt so a stolen code alone is insufficient to finish the exchange.
These protocol details are handled by the login integration; they are not part of video processing.

With Cognito, the access token is a **JWT** (JSON Web Token), a structured token containing signed
statements called **claims**. **JSON** is a text format for named fields, values and lists. A decoded
view of a few illustrative claims could look like this; this is not a usable token:

```json
{
  "sub": "user-123",
  "client_id": "video-web-application",
  "token_use": "access",
  "scope": "video/jobs.write"
}
```

`sub` identifies the user within that issuer; `client_id` identifies the calling application, not
the customer organization. A **scope** is an allowed category of API action, such as creating jobs.
The complete token also identifies its issuer and expiration. These example values are shortened
for readability. An access token authorizes API use; an **ID token**, also returned by many login
systems, describes the sign-in to the client application and is not interchangeable with it here.

**2. The application attaches the token to each API request.**

```http
POST /jobs
Authorization: Bearer <access-token>
Content-Type: application/json
```

A **bearer token** can be used by whoever possesses it. The application sends it over HTTPS, which
encrypts traffic in transit. Do not put it in URLs, logs or saved example files. Alice does not
normally type her password for every request; the application carries this credential instead.

**3. Our API verifies the token before trusting its claims.**

For the signed-token scheme here, Cognito creates a **digital signature** using a private signing
key it protects. Our API checks that signature with the corresponding public verification key.
Knowing the public key lets us check signatures; it does not let us create valid ones. Changing a
user ID or a permission in the token invalidates its signature.

A configured token-verification library must check the signature and allowed signing algorithm,
trusted issuer, expiry, access-token type, and intended application/API and required scope. Cognito
access tokens identify the app with `client_id`; validate the API audience (`aud`) as well when
using its resource-bound tokens. The exact checks must match the configured provider/token format.
Simply decoding a JWT into a dictionary is not verification. A signature protects integrity; it
does not make the token's contents unreadable.

**What does “our configured issuer” actually mean?**

An **issuer** is the authority that creates and signs a token. “Configured” means our team has
explicitly told the API which authority to trust, using application settings controlled by us.
It does not mean the caller gets to choose a login service and have us trust it automatically.

For Cognito, we create a **user pool**: a particular directory of user accounts and login settings
inside our AWS setup. Cognito is the product; our specific user pool is the issuing authority in
this example. Its issuer identifier is a URL. A fictional example is:

```text
https://cognito-idp.us-west-2.amazonaws.com/us-west-2_EXAMPLE
```

This identifies the region and the particular user pool. It is not our video API URL or Acme's
website. In this design, Alice at Acme and Bob at Globex can both sign in through that same pool;
our own membership table distinguishes their tenants afterward.

Our deployment configuration could contain these non-secret settings. The URLs illustrate the
format; no user pool has been created for this lesson:

```text
AUTH_ISSUER=https://cognito-idp.us-west-2.amazonaws.com/us-west-2_EXAMPLE
AUTH_JWKS_URL=https://cognito-idp.us-west-2.amazonaws.com/us-west-2_EXAMPLE/.well-known/jwks.json
```

The JWT has an `iss` claim, short for issuer. Our verifier requires it to match the configured
issuer exactly and also verifies the signature using keys belonging to that issuer. A matching
`iss` string alone is no proof: an attacker can type the same string into a forged token.

For the membership table below, call that full configured issuer URL `video-login-pool` for
readability. The verified identity is the pair `(issuer, sub)`: **which authority identified the
user, and which user it identified**. Another unrelated provider might also have a `user-123`;
that must not automatically become Alice in our application. This pair still does not establish
customer membership until our database checks it.

**What is JWKS, and where does the API get it?**

A **JWK** (JSON Web Key) is a standard JSON representation of a cryptographic key. **JWKS** means
JSON Web Key Set: a JSON document containing a list of keys. The provider's public JWKS endpoint
publishes its **public verification keys**, never the private signing keys used in this scheme.
For Cognito, that document is served at the issuer URL followed by `/.well-known/jwks.json`, as
shown in `AUTH_JWKS_URL` above. Other providers may use a different documented URL.

Our API makes an ordinary HTTPS GET to this address. It does not need Alice's password or send her
token to download these public keys. Anyone can read them; they verify signatures but cannot create
the provider's signatures. A shortened example of the document's shape is:

```json
{
  "keys": [
    {
      "kid": "signing-key-A",
      "kty": "RSA",
      "alg": "RS256",
      "use": "sig",
      "n": "ILLUSTRATIVE_PUBLIC_KEY_VALUE",
      "e": "AQAB"
    }
  ]
}
```

This is illustrative JSON, not a usable key. `kid` means **key ID**, a label distinguishing keys
within the trusted set. `kty` identifies the key type, `alg` identifies the signing algorithm, and
`use: sig` marks signature use. `n` and `e` encode the public RSA key's mathematical parameters;
our verification library handles them. We do not implement that cryptography ourselves.

The JWT also has a header containing a key ID and algorithm, for example:

```json
{"kid": "signing-key-A", "alg": "RS256"}
```

The verifier uses that `kid` to select a candidate key **from our trusted provider's key set**,
then checks the actual signature. A matching key ID is not authentication by itself, and the API
must still enforce its configured allowed algorithm rather than accept any algorithm a token names.

**How does a public key actually verify a signature?**

A digital-signature algorithm provides two related operations: **sign**, which needs the private
key, and **verify**, which uses the public key. With properly generated keys and a secure
implementation, checking a signature is practical while forging one for chosen content without
the private key is computationally infeasible. We will use Cognito's **RS256** algorithm: an RSA
signature with SHA-256 and a defined signature-encoding format.

A signed JWT in this example has three text sections separated by periods:

```text
encoded_header.encoded_payload.encoded_signature
```

The header identifies the algorithm and key ID. The payload contains claims such as the user,
issuer and expiration. **Base64url encoding** represents bytes as URL-safe text; anyone can reverse
that encoding. It is not encryption. The exact first two encoded sections, including their joining
period, are the **signing input**—the bytes protected by the signature. A verifier must use those
received bytes, not decode the JSON and reconstruct it with potentially different whitespace/order.

When issuing the token, the provider:

1. Computes a **hash**, a fixed-size fingerprint, of those signing-input bytes using SHA-256.
2. Formats that hash using RS256's prescribed signature encoding.
3. Uses the private RSA key to produce the signature and appends its encoded form as section three.

When verifying the token, our API's library:

1. Recomputes SHA-256 from the received header/payload signing input.
2. Uses the trusted public RSA key to check the signature against the required encoded hash.
3. Accepts the signature only if the complete mathematical/format check succeeds.

```text
Signing:
  exact header.payload → hash and format → private-key operation → signature

Verification:
  received header.payload → hash and format ────────────────┐
  received signature      → public-key operation ──────────┴→ must match
```

If an attacker changes `sub` from `user-123` to `admin`, the API computes a different hash. The old
signature no longer matches. Computing the new hash is easy and public; producing a signature that
matches that hash requires the private key. Copying a signature from another token also fails when
the protected contents differ. Changing a header field is detected for the same reason.

<details>
<summary>Optional mechanics: why the two RSA keys can do different things</summary>

The public RSA key contains two integers, `n` and `e`—the same parameters represented in the JWKS.
The private key includes a secret exponent `d`. The value `n` is constructed from large secret prime
numbers; knowledge of those factors enables computing the private-key relationship. Securely sized
keys make recovering the private key from the public information impractical with known classical
methods. This is a computational security assumption, not a claim that no attack can ever exist.

Let `m` represent the correctly formatted hash as an integer. Simplified RSA operations are:

```text
Signing:       s = m^d mod n
Verification:  recovered = s^e mod n
               require recovered == the expected formatted hash
```

`^` here means exponentiation. `mod n` means the remainder after division by `n`. The keys are
constructed so the public operation checks the result of the private operation. Knowing `e` and
`n` makes the verification computation easy; it does not make finding a valid `s` for a chosen
formatted hash easy.

**Why can't we substitute these equations and solve for `d`?**

Substitution gives `m ≡ (m^d)^e ≡ m^(d*e) (mod n)`. The exponent is the product `d*e`,
not `d*n` or `d^e`. The symbol `≡` means the two sides have the same remainder after division by
`n`; it does not mean their ordinary integer values are equal. The modulo cannot be dropped.

For example, `7^21 mod 55 = 7`, although `7^21` is enormously larger than 7. Taking ordinary
logarithms as if `7^21 = 7` would solve an equation we never had. If written as an ordinary equality,
the relation is `m^(d*e) = m + k*n` for some additional unknown integer `k`.

With tiny, deliberately insecure example numbers, let `n = 55`, public exponent `e = 3`, private
exponent `d = 7`, and formatted-message stand-in `m = 7`:

```text
Sign:     7^7 mod 55 = 28
Verify:  28^3 mod 55 = 7
Combined: 7^(7*3) mod 55 = 7
```

Where did `d = 7` come from? For ordinary two-prime RSA, the key generator knows `n = p*q`.
From those secret primes it computes `lambda(n) = lcm(p-1, q-1)`. The **least common multiple**
(`lcm`) is the smallest positive integer divisible by both inputs. This value supplies an exponent
period: for any `m` sharing no factor with `n`, `m^lambda(n) mod n = 1`. The resulting RSA key
construction also works for the other message representatives when `n` is a product of distinct
primes, as it is here.

The generator chooses `d` to satisfy:

```text
e*d ≡ 1 (mod lambda(n))
```

This makes `d` the **modular inverse** of `e` with respect to `lambda(n)`: multiplying them leaves
remainder 1. Computing that inverse is efficient with the extended Euclidean algorithm once the
modulus `lambda(n)` is known. The inverse is taken modulo `lambda(n)`, not modulo the public `n`.

For our toy example:

```text
55 = 5 * 11
lambda(55) = lcm(4, 10) = 20
3 * 7 = 21 = 1 + 20
Therefore d = 7 works.
```

Real RSA uses much larger primes. Multiplying known primes to obtain `n` is easy; factoring a
properly generated, sufficiently large `n` to recover them is believed infeasible with known
classical methods. The provider knows those factors from key generation and can cheaply compute
the needed period and inverse. Publishing `n` and `e` does not publish that period or make the
inverse easy to obtain. Factoring is a sufficient route to recovering the private key; not every
possible signature forgery is proved equivalent to factoring.

A known message/signature pair is expected to be public. It does not turn modular exponentiation
into an ordinary logarithm problem. Multiple exponents can produce the same observed remainder:
`7^7`, `7^27` and `7^47` all have remainder 28 modulo 55. This non-uniqueness alone is not the security
argument—an attacker only needs *one* usable equivalent private exponent. The difficulty is finding
such an exponent efficiently at secure key sizes without the secret structure. These tiny-number
examples explain RSA arithmetic only; actual signatures require the encoding described next.

These equations omit byte conversions, range checks and strict signature formatting. RS256 uses
**PKCS#1 v1.5 signature encoding**, a prescribed structure containing the SHA-256 hash and algorithm
identifier. The complete encoding/checks are essential; signing a bare number with these equations
is not a secure JWT implementation. Other signature algorithms use different mathematics.

This operation verifies origin/integrity under the trusted key. It does not decrypt the token or
prove that Alice is physically present. A stolen, unchanged bearer token can still have a valid
signature. Expiry, trusted issuer, intended API, revocation policy and tenant authorization remain
separate checks.

</details>

**What code performs the check?**

A JWT library normally parses the token, selects a trusted key and performs signature and configured
claim validation. The underlying Python `cryptography` library exposes the RS256 signature check
like this, after a trusted JWK has been converted to an RSA public-key object:

```python
public_key.verify(
    signature_bytes,       # Decoded third token section.
    signing_input_bytes,   # Exact received first section + b"." + second section.
    padding.PKCS1v15(),    # RS256's prescribed RSA signature encoding.
    hashes.SHA256(),
)
```

Success returns normally; an invalid signature raises `InvalidSignature`. The library computes
the hash internally in this call. Passing the right public key and checking the remaining claims
are still our integration's responsibility; the single call is not a complete authentication layer.

<details>
<summary>Optional runnable demonstration: original token passes, modifications fail</summary>

This example requires Python's `cryptography` package. It generates temporary demonstration keys
in memory and never writes or prints them. The local run on November 12 produced the four outcomes
shown below. It exercises signature mechanics only: the minimal example claims are not a complete
production token, and the helper does not implement claim validation or malformed-input handling.
In the real system only the provider holds the private signing key; the API receives public keys.

```python
# Signature demonstration, not an authentication implementation.
import base64
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def encode_bytes(value):
    return base64.urlsafe_b64encode(value).rstrip(b"=")


def encode_json(value):
    return encode_bytes(json.dumps(value, separators=(",", ":")).encode("utf-8"))


private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()
header = encode_json({"alg": "RS256", "kid": "demo-key"})
payload = encode_json({"sub": "user-123"})
signing_input = header + b"." + payload
signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
token = signing_input + b"." + encode_bytes(signature)


def signature_is_valid(candidate, verification_key):
    received_header, received_payload, received_signature = candidate.split(b".")
    decoded_signature = base64.urlsafe_b64decode(
        received_signature + b"=" * (-len(received_signature) % 4)
    )
    try:
        verification_key.verify(
            decoded_signature,
            received_header + b"." + received_payload,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False


changed_payload = header + b"." + encode_json({"sub": "admin"}) + b"." + encode_bytes(signature)
changed_header = encode_json({"alg": "RS256", "kid": "changed"}) + b"." + payload + b"." + encode_bytes(signature)
wrong_public_key = rsa.generate_private_key(public_exponent=65537, key_size=2048).public_key()

print("Original:", signature_is_valid(token, public_key))
print("Changed user:", signature_is_valid(changed_payload, public_key))
print("Changed header:", signature_is_valid(changed_header, public_key))
print("Wrong public key:", signature_is_valid(token, wrong_public_key))
```

Expected and observed output:

```text
Original: True
Changed user: False
Changed header: False
Wrong public key: False
```

</details>

```text
Provider's private key → signs a token → application sends token to our API
Provider's public JWKS → API selects public key → checks that token's signature
Our trusted settings  → restrict issuer, key source and intended token use
```

Why a *set* of keys? A provider can sign different token types with different keys, and it can
**rotate keys**, meaning replace a signing key with a new one. The verifier can **cache** the
public keys—keep a local copy—and refresh them periodically or when it encounters an unfamiliar
key ID. Cache keys must include the trusted issuer/key source as well as `kid` if multiple issuers
are supported. If a trusted refresh still supplies no matching key, verification fails; do not
accept the token or follow a key URL supplied by the caller. This avoids a login-service network
call for every API request without hard-coding one signing key forever.

The critical trust decision happens in our configuration. If the API trusted any `iss` URL a
caller supplied and downloaded that caller's public keys, the caller could sign their own token
claiming to be Alice. A successful signature check with an attacker's key proves nothing about our
trusted login system. The verified identity must then pass the normal tenant/permission checks.

FastAPI can run our shared authentication function before protected endpoint handlers using its
dependency mechanism; the framework alone does not establish trust.

**4. Our application maps the verified user to an allowed tenant.**

The login token need not contain a `tenant_id`. For this walkthrough, our PostgreSQL database has a
membership table maintained by trusted onboarding/invitation and administrator operations:

| Trusted issuer (alias for the URL above) | User ID (`sub`) | Tenant | Role |
|---|---|---|---|
| video-login-pool | user-123 | acme | job_creator |
| video-login-pool | user-456 | globex | viewer |

A **role** groups application permissions. The API looks up the verified issuer and user ID,
checks that membership is active and the role permits this operation, then assigns `tenant_id =
"acme"` to the new job. The user's email domain or a tenant field on a signup form is not enough
to establish membership. User IDs must be scoped to their issuer when multiple providers are used.

Conceptually, our code does this; these helpers represent required logic, not a complete program:

```python
identity = verify_access_token(request.headers["Authorization"])
membership = require_active_membership(identity.issuer, identity.subject)
require_permission(membership.role, "jobs:create")
job = create_job(tenant_id=membership.tenant_id, input=validated_input)
```

For now, assume one tenant per user. If Alice legitimately belongs to several organizations, she
may select `acme` in the URL, header or body. The API must verify that selection against her allowed
memberships before using it. The problem is trusting an unchecked selection, not the existence of
a tenant field. Another valid design uses a signed tenant claim controlled by the trusted issuer;
letting users edit that claim would break the trust boundary.

**5. Apply the same boundary when reading, cancelling and downloading.**

A caller presenting an invalid/expired credential receives an authentication failure, typically
HTTP `401`. A valid caller without the necessary permission receives a permission failure, typically
`403`; a service may use `404` for another tenant's job to avoid revealing its existence. A status
lookup must match both the job ID and the caller's authorized tenant. The same checks protect input
access, cancellation and result-download links. Knowing `job-742` does not grant access to it.

Tokens expire, and possession of a stolen valid token can impersonate its user. Short lifetimes,
careful token storage and active membership checks limit exposure. Checking a signature locally
does not automatically discover logout or token revocation; immediate invalidation needs an
additional server-side session/revocation check. The full sign-in implementation also needs the
login library's redirect protections and a deliberate token renewal/storage policy.

For a customer script with no human present, authenticate a **service account**, an identity for a
program, using the provider's supported machine credential flow or an API key mapped to a tenant.
Apply the same membership/permission checks. An AWS **IAM role** is an AWS identity with permissions to use AWS resources. The role our worker
uses to access S3/SQS is separate from Alice's customer login.

### Now submit the video request

Acme's input is already in S3. Its application submits the following request with the authorization
header above. Our API parses the JSON body into application data.

```http
POST /jobs
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "input": {
    "bucket": "lesson-videos",
    "key": "acme/input/clip-17.mp4",
    "version_id": "example-input-version-A"
  },
  "transform": {"kind": "resize", "width": 1280},
  "pipeline_version": "resize-v3"
}
```

These names are illustrative. S3 **versioning**, when enabled for the bucket, gives separate
versions of an object distinct identifiers. Saving a version avoids silently processing new bytes
if someone later overwrites the same key. `pipeline_version` similarly identifies the processing
implementation/settings we intend to use.

The API validates the transformation, checks that Acme can access the input, and creates a job ID.
We write `job-742` for readability; section 4 explains a practical way to generate identifiers.
The saved row initially looks roughly like this:

```json
{
  "job_id": "job-742",
  "tenant_id": "acme",
  "status": "QUEUED",
  "input_key": "acme/input/clip-17.mp4",
  "input_version": "example-input-version-A",
  "pipeline_version": "resize-v3",
  "output_key": null
}
```

The real record also retains the bucket and transform settings. `null` means no value has been
recorded yet. `QUEUED` means accepted and waiting for execution; it does **not** assert that an SQS
message is currently present. This definition avoids needing perfectly synchronized state across
the database and SQS.

The API saves the job and the sender's notification note together, then returns:

```http
HTTP/1.1 202 Accepted
Content-Type: application/json

{"job_id": "job-742", "status_url": "/jobs/job-742"}
```

`202 Accepted` means the service has accepted responsibility for the work. It does not mean the
video has finished or that it is guaranteed to succeed.

### What actually goes through SQS?

The sender places this small **message body**—the contents of one message—on the queue:

```json
{"job_id": "job-742"}
```

The message is a pointer to the saved work. It is not the 10 GB video and does not need to contain a
second official copy of all settings. The worker obtains those settings from the job row and
the video bytes from S3. SQS does not resize videos or run JSON as code.

Our code uses **Boto3**, AWS's Python software development kit (**SDK**, a library for calling its
services), to call SQS over HTTPS, HTTP with
transport encryption. For example, the sender calls `SendMessage`; Boto3 handles the service request
and authentication using the program's configured AWS identity.

```python
# Illustrative SDK call; not a complete runnable application.
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps({"job_id": "job-742"}),
)
```

A worker calls `ReceiveMessage` on the same queue. Repeatedly asking for available work is
**polling**. SQS **long polling** lets that receive request wait for a message instead of returning
immediately from an empty queue. Our worker initiates an ordinary HTTPS request to AWS; SQS
responds on that connection. No incoming connection to the worker is needed.

Receiving does not permanently remove the message. SQS gives the worker a **receipt handle**, an
identifier for that particular delivery of the message. Our code later passes that handle to
`DeleteMessage` when it is safe to remove the notification. This is the SQS form of
**acknowledgement**: telling the queue the received message no longer needs delivery. The receipt
handle identifies a delivery, not the job or the message for its entire lifetime.

### Why can a receipt handle become old?

The handle does not change inside the worker's memory. **SQS issues another handle when that same
message is received again.** The later receiver might be another worker or the same worker making
a new receive request.

Why would SQS deliver it again? After a receive, SQS normally hides the message for a configured
**visibility timeout**, giving the receiver time to work. If the message is not deleted and that
hiding period expires, the message becomes available again. Holding the handle in a Python variable
does not tell SQS that the worker is healthy or make the hiding period last indefinitely.

For a concrete example, suppose the timeout is 30 seconds. Handle names below are illustrative:

| Time | What happens | Receipt handles |
|---|---|---|
| 0 seconds | Worker A receives message M. SQS temporarily hides M. | A receives `R1`. |
| 30 seconds | A has paused or taken longer than expected and has not extended visibility or deleted M. M becomes available. | A still has the string `R1`. |
| 31 seconds | Worker B receives that same message M. | B receives a new handle, `R2`. A is not automatically sent it. |
| 40 seconds | A resumes and tries to delete M using `R1`. | `R1` belongs to the earlier delivery; deletion with it is no longer reliable. |

AWS documents that an old-handle `DeleteMessage` call can report success without actually deleting
the message. Treat receipt handles as delivery-specific identifiers, not durable ownership locks.
Worker B receiving M also does not automatically give it ownership of the logical job; section 6
explains the separate database check.

If Worker A itself later receives M again, that new receive returns a new handle. Its code must use
the newly returned handle for that delivery instead of a previously saved one. If Worker B received
it, A cannot fetch a guaranteed “latest handle” by looking up M; each receiver handles the receipt
it was actually given. Our tutorial deletes notifications only after the database records a terminal
outcome, so a later receiver can see that the job is already complete and delete its own receipt.

For long work, use `ChangeMessageVisibility` with the current handle **before the timeout expires**
to extend the hiding period. That operation does not issue a replacement handle; another receive
is what supplies a new one. Queue visibility remains separate from database ownership, and Standard
queues can still deliver duplicates even during the timeout. Both layers need their own checks.

### The normal path, with nothing failing

1. The API saves `job-742` and its notification note, then returns `202`.
2. The sender reads the note and sends `{"job_id":"job-742"}` to SQS.
3. A worker receives the message and loads the job row.
4. It takes responsibility for this execution and changes the job to `RUNNING`. Section 6 explains
   how to ensure two workers cannot both take that responsibility.
5. The worker downloads the specified input version from S3 and runs the transformation.
6. It uploads an output, then records `SUCCEEDED` and the selected output key in the database.
7. It deletes its SQS message using the receipt handle.
8. Acme calls `GET /jobs/job-742`. The API checks Acme's access, reads the row, and returns status
   and, when appropriate, a permitted way to download the output.

Only our application performs the video transformation and defines these rules. AWS supplies the
storage, message service and machines. A successful normal path is the beginning of the design;
the following sections make the same path survive ordinary failures.

**Pause:** point to where the video bytes live, where the job's status lives, and what the queue
message contains. If those three are clear, you have the central picture.

## 4. Problem: the client does not know whether submission worked

Imagine the API saved the job, but the connection broke before Acme received `202`. Acme has no
job ID. If it submits again, should we create a second job?

An operation is **idempotent** when repeating the same intended operation does not create an
additional effect beyond doing it once. Here, retrying one submission should identify the existing
logical job. This does not imply the video-processing program can never execute twice.

### Who makes the idempotency key?

The **idempotency key** is a caller-chosen identifier meaning “these attempts all belong to this
one submission.” The caller is the browser, application backend or script invoking our API.

It generates a key **before the first submission**, retains it, and reuses it for retries:

```python
import uuid

submission_key = str(uuid.uuid4())
# Keep this value with this pending submission; do not regenerate inside the retry loop.
```

A **UUID** is an identifier format; UUID version 4 uses randomness to make independently generated
identifiers extremely unlikely to collide. An example key is
`"7c2ae838-9823-4c45-a001-6bde29d4b847"`. It is not a secret, password, or proof of authorization.

The caller adds it to the request as a header:

```http
Idempotency-Key: 7c2ae838-9823-4c45-a001-6bde29d4b847
```

A retry uses the same key and the same intended input. A deliberately new job gets a new key,
even when its parameters happen to match. The client must retain the key across the retry period;
for a browser, its backend can own that submission record. Two clicks that generate two fresh keys
are two different submissions as far as this contract is concerned.

Keep the identifiers distinct:

| Identifier | Created by | Meaning |
|---|---|---|
| Idempotency key | Calling application before submission | One intended submission across retries |
| Job ID | Our API when it accepts a new job | The saved work that status/cancel requests address |
| SQS receipt handle | SQS when a worker receives a message | This receipt of this queue message, used for deletion/visibility changes |

### Why also store a request hash?

What if the caller accidentally reuses its key but changes `width` from `1280` to `640`? Returning
the old job silently would process the wrong intention.

A **request hash** is a compact fingerprint of the request's meaningful content. Our API, not the
caller, calculates and stores it. For these simple JSON examples:

```python
import hashlib
import json

normalized = json.dumps(validated_request, sort_keys=True, separators=(",", ":"))
request_hash = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
```

`SHA-256` is the hash algorithm. **Normalization** means putting equivalent request data into a
consistent representation before hashing. Sorting JSON fields avoids treating a mere field-order
change as a different request. Real code must also consistently resolve defaults and validate
values. Hash stable input identity/version, transformation and pipeline version; omit changing
request timestamps or temporary download URLs. The hash does not replace authorization.

The database stores the key, hash and job ID together. A **unique constraint** is a database rule
preventing two rows from having the same chosen field combination. We require uniqueness for
`(tenant_id, idempotency_key)` on this submission endpoint: two customer organizations can use the
same key text without sharing jobs. Both columns are required (`NOT NULL` in PostgreSQL). The
completed API contract rejects a missing or empty idempotency-key header; add the header above
to the request from section 3. A uniqueness rule alone would allow multiple missing/null values.

| Incoming submission | Our response |
|---|---|
| Acme, new key | Create one job and its notification note. |
| Acme, existing key, same normalized request/hash | Return the same job ID; status may now be more advanced. |
| Acme, existing key, different request/hash | Return a conflict, for example HTTP `409`; do not create or change the job. |
| Another tenant, same key text | Treat it in that tenant's separate scope. |

The unique constraint also handles two simultaneous retries. A “look up, see nothing, then insert”
sequence alone is unsafe: both API processes might see nothing. The database must enforce the
uniqueness during insertion; the loser reads the already-saved existing record and compares the hash.

**Retention choice:** document how long keys remain valid. For this exercise, keeping the key/hash
with the 90-day job record lets us recognize retries as the same operation (**deduplication**)
while that record exists. A retry after the record
has been deleted is outside that guarantee. Generating a UUID alone does not define this policy.

## 5. Problem: the database saves the job but nobody hears about it

Suppose our API instead did these two independent operations:

```text
1. Save job in PostgreSQL.       Succeeds.
2. Send its message to SQS.      Never happens: API process crashes.
```

The customer may already have received acceptance, or retry and discover its accepted job. But
there is no notification for a worker. Reversing the operations creates a different problem: SQS
could deliver a message before a job row exists, or for a database write that never succeeds.

This is the **database-commit/message-publish gap** in the previous guide, in plain terms: the
“remember the job” operation can succeed while the “tell a worker” operation fails.

### Saving a reminder in the same database operation

A **transaction** groups database changes into one all-or-nothing unit. **Commit** means accepting
that unit as saved; **rollback** means discarding it. Here, either both the job and its reminder
become durable, or neither does. This property is called **atomicity**.

An **outbox** is simply a database table of notifications our application still needs to send.
An **outbox row** is one such reminder. It is not another message broker or an AWS queue. For example:

| event_id | job_id | sent_at |
|---|---|---|
| notice-901 | job-742 | null |

`sent_at = null` means our sender has not recorded successful sending. `event_id` identifies this
notification record; it is different from the client's submission key.

**Why have an `event_id` instead of just `job_id` and `sent_at`?**

If each job has only one outbox row, **`job_id` and `sent_at` are sufficient**. Make `job_id`
unique, and it identifies both the job and its one notification. A separate `event_id` is not
required for that simpler design.

This walkthrough uses a separate ID because one job can need several distinct notifications:
the initial dispatch, then a later recovery dispatch if work stops making progress. If we retain
both reminders, they could look like this:

| event_id | job_id | sent_at |
|---|---|---|
| notice-901 | job-742 | 10:00 |
| notice-902 | job-742 | null |

The first reminder has been recorded as sent; the second still needs sending. `job_id` identifies
the shared work, while `event_id` lets the sender update the particular reminder it sent. The names
and time above are illustrative. Retrying delivery of **the same reminder** keeps its ID; creating
**a new reminder** gets another ID. Neither the ID nor `sent_at` prevents duplicate delivery.

In one PostgreSQL transaction, our API inserts the job—with its idempotency key/hash—and the outbox
row. The following is an outline, not complete SQL:

```sql
BEGIN;
  -- Insert the new job, enforcing the tenant/key uniqueness rule.
  -- Insert an outbox row identifying that job.
COMMIT;
-- Only now return acceptance to the caller.
```

The transaction includes **PostgreSQL writes only**. Placing a network call to SQS between `BEGIN`
and `COMMIT` would not make SQS participate in PostgreSQL's transaction.

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant D as PostgreSQL
    participant P as Background sender
    participant Q as SQS
    C->>A: Submit request with submission key
    A->>D: Transaction: save job and unsent outbox row
    D-->>A: Commit succeeded
    A-->>C: 202 with job ID
    P->>D: Read unsent rows
    D-->>P: notice-901 for job-742
    P->>Q: SendMessage containing job-742
    Q-->>P: Send succeeded
    P->>D: Record sent_at for notice-901
```

If the API crashes after commit, the sender can still find the reminder. If the sender crashes
before sending, another run tries again. If it sends successfully and crashes before recording
`sent_at`, it may send again. We deliberately tolerate duplicate notifications; section 6 makes
workers handle them safely. The outbox closes the lost-notification gap, not every possible failure.

For a small implementation, one sender process can repeatedly query unsent rows, send them and mark
them sent. Multiple sender processes need coordination or duplicate-tolerant behavior. Never mark
a reminder sent before SQS reports success. Persist errors, retry with increasing delays, and alert
when old unsent rows accumulate; storing reminders alone does not make an unhealthy sender recover.

### What is a periodic reconciler?

**Reconciliation** means comparing the intended state with what is happening and repairing a
mismatch. A **periodic reconciler** is our program running that check repeatedly—for example,
a small service loop or a scheduled task. It is not a special database feature.

For this service, it could find a job waiting too long without progress, or a worker whose ownership
has expired, and arrange another attempt by saving a new notification reminder. It checks current
state before changing it, so it cannot turn a cancelled job back into running work.

An outbox sender asks, **“Which saved notifications have not been sent?”** A reconciler asks,
**“Which accepted jobs are not making the progress our rules require?”** They can run in one program,
but they solve different problems.

A simpler alternative can omit the outbox and repeatedly discover runnable jobs directly from the
job table. That can be valid if every accepted job is discoverable and scans/retries are reliable;
it trades immediate notification and explicit send tracking for scan delay and database work.
For this walkthrough, keep the explicit outbox, then add recovery checks for stalled execution.

## 6. Problem: a worker crashes or two workers receive the same job

Receiving a notification is not the same as earning exclusive permission to finish that job.
SQS Standard can redeliver, the sender can send twice, and workers can stop responding.

### First layer: SQS visibility

As introduced in section 3, after a receive SQS normally hides the message for its configured
visibility timeout. The message still exists. If the worker does not delete it, it can become
visible again after that timeout. Standard queues still do not guarantee that duplicates cannot
occur during the timeout, so this is not our correctness lock.

A long-running worker can extend visibility using `ChangeMessageVisibility` and its receipt handle.
If it finishes, it calls `DeleteMessage`. In this walkthrough, **delete after the database records
a terminal outcome**, meaning `SUCCEEDED`, `FAILED` or `CANCELLED`, with no further execution planned.
Receiving or deleting an SQS message does not automatically update our database.

Why keep the message until then? If the worker disappears, the notification can return. Later in
this section we explain the extra database recovery mechanism, which also covers notifications
that are no longer available.

### Second layer: the database decides who owns an attempt

An **attempt** is one execution of the logical job. A retry might create attempt 2 for the same
`job-742`. We add these fields to the job record:

| Field | Example while worker A runs | Why it exists |
|---|---|---|
| `status` | `RUNNING` | The job is executing. |
| `owner_id` | `worker-A` | Which worker currently owns this attempt. |
| `attempt_no` | `1` | Identifies this generation of execution. |
| `lease_until` | A database timestamp two minutes ahead | Ownership must be renewed before this time. |

A **lease** is time-limited permission: “you own this work until this deadline, unless our state
rules cancel it.” A **heartbeat** is the worker's periodic update showing it is still active and
renewing its lease. Two minutes and a 30-second heartbeat are illustrative choices, not production
recommendations; renewal must continue during long video/model computation.

<details>
<summary>Question: What if a job takes longer than its lease?</summary>

**Question:** This rule of always accepting the result of latest attempt makes me wonder what
happens if a job genuinely takes longer than expected. We reject the correct results of worker A
because its attempt is now old and worker B owns the new attempt. But then the same thing happens
to B, so we keep rejecting correct results just because they come too late.

**Answer:** Yes—repeated lease expiry could cause that loop. A long-running job should avoid it by
renewing its lease throughout processing. The lease duration is the time allowed between successful
renewals, not the total time allowed for the job. For example, A has a two-minute lease and sends a
heartbeat every 30 seconds: at 10:00:00 it claims attempt 1, deadline 10:02:00; at 10:00:30 it
renews, deadline 10:02:30; at 10:01:00 it renews, deadline 10:03:00; renewals continue during
processing and move the deadline forward. These intervals are illustrative. A can work for 20
minutes and remain attempt 1. B cannot take over while A's database lease remains valid, even if B
receives a duplicate SQS notification. A separately renews SQS visibility.

If A and then B repeatedly lose their leases, the result-selection rule alone will not ensure
completion. Keep heartbeat execution responsive during long computation: a blocking CPU/GPU call
must not prevent renewal code from running. Allow realistic timing margins for scheduling delays,
network latency, and brief database interruptions. Detect repeated failures and bound retries:
repeated expiry should trigger investigation rather than endless replacement attempts.

Separately, a stuck worker could keep renewing forever; a job deadline or progress timeout can stop
that, and this is a different policy from the renewable ownership lease. The concern is valid when
renewals repeatedly fail; ordinary long processing should keep the same attempt alive. Ownership
checks prevent stale publication; responsive renewal and recovery make eventual completion possible.

</details>

A worker **claims** a job by changing the database row only if it is waiting or its previous lease
expired. A **conditional update** applies a change only when its condition is still true. The
condition and update must be evaluated as one protected database operation, not separated by video
processing or an application-level check.

The database briefly protects a row against competing changes using a **row lock**. In this
implementation, acquire that lock first, then check the state and the current database time. Release
the lock immediately after the update; hold the renewable lease, not the database lock, during work.

<details>
<summary>Optional implementation detail: what a claim looks like in PostgreSQL</summary>

Named parameters such as `:job_id` are values supplied by our code, not literal SQL values:

```sql
BEGIN;
SELECT job_id FROM jobs WHERE job_id = :job_id FOR UPDATE;
UPDATE jobs
SET status = 'RUNNING',
    owner_id = :worker_id,
    attempt_no = attempt_no + 1,
    lease_until = clock_timestamp() + INTERVAL '2 minutes'
WHERE job_id = :job_id
  AND (status = 'QUEUED'
       OR (status = 'RUNNING' AND lease_until <= clock_timestamp()))
RETURNING attempt_no;
COMMIT;
```

Assume `attempt_no` starts at zero and all operations use the database's clock. One returned row
means the claim succeeded. No returned row means this worker did not acquire ownership. PostgreSQL
coordinates concurrent changes to the same row. The operation is brief; do **not** hold a database
transaction open while a 60-minute video job runs. `FOR UPDATE` acquires that brief row lock.
`clock_timestamp()` reads the actual database time; PostgreSQL's `CURRENT_TIMESTAMP` instead means
the transaction's start time, which can be stale after waiting for a lock. Start processing only
after this short transaction commits successfully. An optional attempts table can retain history.

</details>

<details>
<summary>Question: Can a worker claim a RUNNING job when its lease has expired?</summary>

**Question:** Does `OR (status = 'RUNNING' AND lease_until <= clock_timestamp())` mean a worker
can claim the job if its status is running and the lease has already expired?

**Answer:** Yes. The row can still say `RUNNING` after the previous owner's lease expires;
passing the deadline does not automatically change that status. The condition allows a worker
to claim a new attempt for the same job. The successful update assigns the claiming worker,
increments `attempt_no`, and sets a fresh lease deadline. It does not continue the expired attempt.
`<=` includes the exact expiration instant. Start work only after the claim transaction commits.
Expiry does not prove the old worker has stopped; the guarded updates reject its late results.

</details>

If another owner is still active, do not start work or delete a nonterminal job's notification.
Leave the message to become visible again, or use `ChangeMessageVisibility` to defer it for a bounded
delay. If the job is terminal, the receiver deletes its own obsolete receipt.

<details>
<summary>Question: Why keep a notification when another worker already owns the job?</summary>

**Question:** If the job is `RUNNING` and its lease has not expired, should this worker leave the
message to become visible again, or change visibility to try again later? Why not delete it as an
incomplete duplicate, since another worker must already have received an SQS message for this job?

**Answer:** Yes: if the database shows another owner with an unexpired lease, this worker should
not start processing. It can let the message become visible again, or extend visibility for a
short, bounded delay before another receive.

An unexpired lease means **another worker still has permission**, not that it is definitely
healthy. It may have crashed moments after renewing its lease. Also, there may be **only one SQS
message**, received again after its visibility timeout. Receiving it does not prove a separate
message exists elsewhere.

Consider this illustrative example:

| Time | What happens |
|---|---|
| 0 seconds | A receives message M and claims the job with a lease lasting until 120 seconds. SQS hides M for 30 seconds. |
| 10 seconds | A crashes. Its database lease remains unexpired. |
| 30 seconds | M becomes visible again. |
| 31 seconds | B receives the same M, checks the database, and sees A's unexpired lease. B cannot claim yet. |
| After 120 seconds | A's lease has expired. When the notification is available and received again, a receiver can claim a new attempt. |

**If B deletes M at 31 seconds, it removes the notification that could trigger later recovery.**
A crashed, and there was no second message. A database recovery scan must now notice the unfinished
job and send another notification.

Keeping M preserves a queue-based recovery path:

```text
Owner disappears → message returns → lease eventually expires → new attempt
```

Even when there are two separate messages, another worker owning the job does not prove its
notification will remain available or that it will finish.

**Deleting can still be a valid design.** The alternative described later in this section deletes
after a durable claim and relies on database leases plus a reliable recovery scan. It reduces
repeated queue deliveries, but makes that scan responsible for recovering unfinished jobs.
Keeping the message gives another recovery path; it is not universally better.

SQS deletion has **no incomplete status**. `DeleteMessage` removes the notification using its
receipt handle. The job's `RUNNING`, `SUCCEEDED`, or other status remains a separate database
record. Once the database records a terminal outcome, no further execution is needed, so receivers
can safely delete leftover notifications.

</details>

For a retryable processing failure, the valid owner conditionally returns the job to `QUEUED`,
stops renewing visibility, and lets the message return after a retry delay. A permanent failure
records `FAILED`. **Backoff** means spacing retries farther apart after failures; combine it with
a maximum attempt count to avoid repeatedly running a permanently bad input.

### Third layer: stop a late worker from overwriting the winner

Now imagine worker A pauses long enough that its lease expires. Worker B takes over. A then resumes.
An operating-system pause or network outage does not necessarily kill A, so two programs may
physically be running.

A **fencing token** is a version number attached to ownership. The resource receiving a write
checks that number and rejects writes from an older owner. Here, `attempt_no` plays that role:

```mermaid
sequenceDiagram
    participant A as Worker A
    participant D as Job row in PostgreSQL
    participant B as Worker B
    A->>D: Claim job and receive attempt 1
    Note over A: Pauses until lease expires
    B->>D: Claim expired job and receive attempt 2
    A->>D: Try to publish result for attempt 1
    D-->>A: Rejected: current attempt is 2
    B->>D: Publish result for attempt 2 with valid lease
    D-->>B: Accepted
```

Our progress updates, heartbeats and final result update check the job's status, worker identity,
attempt number and unexpired lease. An expired owner must stop; it cannot renew an already expired
lease or quietly continue under its old attempt. A renewal or completion whose time check happens
after expiry must fail, even if its request was sent before expiry. To run again, the worker must
claim a new attempt.

<details>
<summary>Question: Why reject a late result if nobody has taken over?</summary>

**Question:** A worker is ready to submit success, but its lease has expired. Its attempt number
is still correct: no other worker has claimed the job since expiry. Why can't we accept its result?

**Answer:** We can allow that under a different, explicitly defined completion policy. Lease
expiry does not by itself prove that the output is incorrect or that a newer attempt exists.
The current tutorial chooses the stricter rule: **expiry ends permission to publish**, even
before another worker takes over. That is a design choice, not a universal database requirement.

Under this strict rule, heartbeats, progress and completion all require an unexpired lease.
This gives ownership one consistent deadline. Its cost is that a finished result can be rejected
even when nobody has replaced the worker.

A valid alternative is **allow late completion while the worker is still the current owner**.
Expiry makes the job eligible for takeover, but completion may still win if the database checks
all of these in the same short, locked operation:

- The job is still `RUNNING`, so cancellation or another terminal outcome has not won.
- `owner_id` still matches the worker.
- `attempt_no` still matches that execution.
- Any separate job deadline and output-validity requirements are still satisfied.

For that alternative, the completion check would not require an unexpired lease. The check and
success update must happen together under the same row lock used by takeover; reading the attempt
number first and submitting success later would leave a race.

| Which operation wins the protected database transition? | Outcome under the late-completion alternative |
|---|---|
| A completes while its owner and attempt still match | Record `SUCCEEDED`; a later claimant finds the job terminal and cannot take it over. |
| B takes over first and increments `attempt_no` | A's completion fails the attempt check, even if A's output was already ready. |
| Cancellation changes the job state first | A's completion fails the `RUNNING` check. |

This can preserve useful finished work without allowing an older attempt to overwrite a newer
one. It remains specific to the guarded database result selection: output isolation and other
external side effects still need their own protections, as section 7 explains.

The distinction is **permission until expiry** versus **late completion permitted until
superseded or cancelled**. The tutorial keeps the first policy. This Q&A explains the second
without changing the existing rule or SQL. This is design reasoning, not a deployed-system test.

</details>

<details>
<summary>Optional implementation detail: the guarded completion update</summary>

As with claiming, lock the row in a fresh, short transaction before checking time. The output
fields identify the exact S3 file version; section 7 explains why:

```sql
BEGIN;
SELECT job_id FROM jobs WHERE job_id = :job_id FOR UPDATE;
UPDATE jobs
SET status = 'SUCCEEDED',
    output_bucket = :output_bucket,
    output_key = :output_key,
    output_version_id = :output_version_id
WHERE job_id = :job_id
  AND status = 'RUNNING'
  AND owner_id = :worker_id
  AND attempt_no = :attempt_no
  AND lease_until > clock_timestamp()
RETURNING job_id;
COMMIT;
```

Use the same ownership and time checks for heartbeats and progress updates. Database locking
serializes these changes; the lease test determines eligibility when evaluated, not a promise that
a process or a commit can never be delayed afterward.

</details>

The **invariant**—a rule that must always hold—is: only the current authorized attempt can choose
the final result. This does not promise exactly one physical execution. Duplicate computation may
cost money, but it must not let the old worker replace the accepted result.

### Two different timers, and a recovery scan

SQS visibility answers **“when may this notification be received again?”** The database lease
answers **“which attempt may update this job?”** Neither automatically renews the other. Our worker
must maintain both, and stop acting as owner when its database ownership is lost.

<details>
<summary>Question: Can SQS message visibility replace the database lease? Why do we need both?</summary>

**Question:** What is the relationship between the RDS lease and SQS message visibility?
Could we use message visibility as the lease instead of maintaining both?

**Answer:** SQS visibility controls delivery of a particular message. The lease in PostgreSQL,
hosted on RDS, controls ownership of the logical job. Our application defines and checks that
lease; RDS does not automatically connect it to SQS.

In the normal flow:

```text
A receives a message about job-742
    → SQS temporarily hides that message
    → A claims job-742 in PostgreSQL
    → PostgreSQL records owner A, attempt 1, and a lease deadline
    → A processes the video and renews both timers
    → A records success using the database ownership checks
    → A deletes its SQS message
```

**Hiding a message does not establish exclusive job ownership.** One job can have several
messages: the outbox sender might send twice after a crash, or recovery might create another
notification. Hiding the first message does not hide the second:

```text
Message M1 → job-742 → received by A and temporarily hidden
Message M2 → job-742 → received by B
```

Both workers hear about the same job, but the database claim lets only one acquire valid ownership.
SQS Standard can also deliver the same message more than once during its visibility timeout.

**The timers can expire independently.** If visibility expires after 30 seconds but A's database
lease remains valid for two minutes, B can receive the message, check PostgreSQL, and avoid starting
another execution. If A's database lease expires while its message remains hidden, A loses permission
to update the job; recovery can arrange another notification. These durations are illustrative.

**The database also protects the final decision.** If A pauses and B takes over, A's late result
must pass checks for the current owner, attempt number, unexpired lease and job state together.
PostgreSQL rejects an old attempt's update. SQS visibility cannot enforce that database write,
and database checks alone cannot protect an unrelated S3 upload; section 7 handles those bytes.

**Both are not mandatory in every system.** A simpler consumer can use visibility plus processing
that safely tolerates duplicates, without a separate database lease. This design keeps durable job
ownership, recovery, cancellation and final-result selection in PostgreSQL. The lease and guarded
writes protect those rules; neither timer guarantees only one physical computation.

The SQS behavior is supported by the existing primary references in section 13. The combined
design and examples are teaching choices, not a new live-queue experiment.

</details>

A reconciler also finds expired running jobs or stranded waiting jobs and, in a short database
transaction, makes eligible work runnable and creates a new outbox notification. It rechecks the
current state/lease before doing so, uses bounded retries, and avoids continuously enqueuing the same
healthy job. Record when a recovery notice was last requested and allow a recovery delay before
sending another, so ordinary SQS redelivery can work without a stream of extra notifications.
Cancelled and terminal jobs are excluded. This is the fallback if a notification has
expired from the queue or ordinary redelivery is not making progress.

**Alternative used in the earlier short guide:** delete the SQS message immediately after recording
a durable claim, then rely on database leases plus the recovery scan for every subsequent worker
failure. That is a valid different contract, but the recovery scan becomes essential once the
message is gone. This tutorial uses deletion after a recorded terminal outcome because it makes
SQS redelivery easier to understand. Do not mix the two acknowledgement policies accidentally.

## 7. Problem: the output is uploaded but completion is not saved

The worker writes a video to S3, then crashes before it marks the database row successful. Or an old
worker finishes after a new one has taken over. Where should each upload go?

If every attempt writes `results/job-742/final.mp4`, a late attempt could overwrite that object even
when PostgreSQL correctly rejects its status update. Our database condition cannot directly protect
an unrelated S3 upload.

Give every upload an **attempt-specific** location and identify the exact object version selected
as the result. For example:

```text
acme/results/job-742/attempt-1/upload-a8.mp4
acme/results/job-742/attempt-2/upload-b3.mp4
```

A distinct upload identifier also separates repeated writes within an attempt. For our baseline,
enable S3 versioning, retain the version ID returned by the completed upload, and save the full
`(bucket, key, version_id)` in PostgreSQL. Every download must request that exact version. Even if
some code later writes to the same key, it creates another version; it does not change the selected
bytes. Versioning alone is insufficient if readers omit the version ID and fetch the latest file.
Workers must not have permission to delete selected object versions.

After upload completes, the current owner conditionally records that reference using the previous
section's update. Only the database-selected version is returned through our API. The bucket stays
private; clients do not browse every attempted output. For large videos, the SDK can upload in
parts; wait for the entire upload to complete before recording success.

An alternative is S3 conditional creation: an `If-None-Match: *` condition tells S3 to create an
object only if that key does not already exist. That needs the corresponding upload and permission
rules. Choose a concrete strategy; merely calling a filename “immutable” does not protect it.

- If upload fails, no successful output is published; the owner can retry according to policy.
- If upload succeeds but the database update's response is lost, read the official job row
  before deciding whether completion failed. It may already have succeeded.
- If the database update truly did not happen, the still-valid owner can try again. If ownership
  has changed, the old attempt cannot finalize the job.
- An upload that no job references is an **orphan object**. Do not delete it merely because it is
  unreferenced right now: a worker might be about to select it. A conservative cleanup rule waits
  for a grace period, then deletes only versions from attempts permanently unable to finalize
  (an older attempt number, or an already-terminal job), excluding the selected version. Leave
  a current, nonterminal attempt's uploads alone. Keep enough job/attempt metadata to make this
  decision before deleting that metadata. This prevents cleanup racing an authorized completion.

<details>
<summary>Question: How can an S3 upload have no job attached?</summary>

**Question:** How could this happen? How can we have an S3 upload with no job attached? We have
the job to know where to upload, no?

**Answer:** Yes—the worker already knows the job. “Orphan” here means that the database has not
selected the uploaded object as the job's official result. It does not necessarily mean the object
has no associated job ID.

Uploading and recording success are two separate operations: (1) worker loads job-742 and claims
attempt 1, (2) uploads its output to S3, (3) records `SUCCEEDED` and that exact output version in
PostgreSQL. Between steps 2 and 3, the S3 video exists while job-742 remains `RUNNING` with selected
output null. The worker knows the producing job, and its object name may contain
`job-742/attempt-1`, but no job's selected-output fields point to it yet.

This may be temporary during normal processing or persist after failure: a worker crashes after
upload but before recording success; or it loses ownership before finalizing, a new attempt takes
over, and its update is rejected, leaving its upload unselected.

Unreferenced right now is insufficient reason for deletion because a valid worker may be about to
select that output; cleanup could delete the file just before the database publishes its reference.
Cleanup therefore checks whether the producing attempt is permanently unable to select that upload,
e.g. a newer attempt replaced it or the job is already terminal, and always preserves the selected
version.

A more precise reading of the existing sentence is: “An uploaded object that no job currently
selects as its official output is an orphan candidate.” The job can exist throughout the sequence.

</details>

<details>
<summary>Question: Why not clean up S3 only after a job is terminal?</summary>

**Question:** That makes sense. But why are we complicating our S3 cleanup policy? Why can't it
be as simple as only doing cleanup for a terminal job, either succeeded or failed?

**Answer:** Yes—cleaning up only after a job becomes terminal is a valid, simpler policy. It avoids
checking whether individual attempts have lost ownership while the job is still running. Once the
job is terminal, no attempt is allowed to publish a new result.

| Job status | Action under the terminal-job-only cleanup alternative |
|---|---|
| `QUEUED`, `RUNNING`, `CANCEL_REQUESTED` | Leave uploads alone. |
| `SUCCEEDED` | Delete unused uploads and preserve the exact selected output version until its retention period ends. |
| `FAILED` or `CANCELLED` | Delete unused uploads. |

The more complicated rule permits deleting an old attempt's unused uploads before the entire job
finishes. Its benefit is earlier storage reclamation, e.g. multiple retries uploading large videos
during a long job. That is an optimization, not a requirement for correct result selection.

Simpler policy limits: jobs must eventually become terminal; a permanently stuck `RUNNING` job
would retain uploads indefinitely, so recovery, retry limits or a job deadline must resolve it.
Cleanup may need another pass: a late worker can finish uploading after the job becomes terminal;
it cannot publish that result, but later cleanup must find it.

The selected output is the essential exception: cleanup of `SUCCEEDED` does not mean deleting the
result while customers are still entitled to download it. For this teaching example,
terminal-job-only cleanup is a reasonable baseline; cleaning abandoned attempts during an active
job adds complexity only when reclaiming storage sooner matters.

This is a design alternative, not a replacement for the cleanup policy above or a new runtime
experiment. It does not record a production-policy choice by Hooman. The existing grace-period,
metadata and selected-version protections remain in place.

</details>

These two writes—S3 upload and database update—are not one shared transaction. We arrange them so
partial completion leaves an extra private file to clean up, rather than an incorrect public result.
The same reasoning matters for emails, billing or external callbacks: those effects would need
their own deduplication/reconciliation contract. The database token alone cannot undo them.

## 8. Problem: cancellation and completion happen together

Acme sends `POST /jobs/job-742/cancel` just as a worker finishes. The system needs one clear answer.

A **state machine** lists the allowed states and changes between them. Use this simplified model:

```mermaid
stateDiagram-v2
    [*] --> QUEUED: Accepted and saved
    QUEUED --> RUNNING: Worker claims
    RUNNING --> QUEUED: Retryable failure or recovery
    RUNNING --> SUCCEEDED: Current owner publishes result
    RUNNING --> FAILED: Permanent failure
    QUEUED --> CANCEL_REQUESTED: Cancel wins
    RUNNING --> CANCEL_REQUESTED: Cancel wins
    CANCEL_REQUESTED --> CANCELLED: Cancellation controller records outcome
```

The API's cancellation update and the worker's success update both require the appropriate current
state. For a running job, they compete over the **same database row**:

| Which protected update commits first? | Result |
|---|---|
| `RUNNING → SUCCEEDED` | The job has succeeded. Cancellation reports that it is already complete. |
| `RUNNING → CANCEL_REQUESTED` | The success update no longer matches `RUNNING`, so its result cannot be published. |

Our cancellation handler/controller is application code that follows through on cancellation and
records `CANCELLED`; repeated cancel calls return the current outcome. Waiting jobs can be cancelled
without ever running. A reconciler must handle cancellation even if the worker is dead.

<details>
<summary>Question: Why do we need a separate cancellation controller?</summary>

**Question:** Why do we even need the cancellation controller? Why can't a worker that sees
`CANCEL_REQUESTED` commit `CANCELLED`? Why need a separate process for cancelling?

**Answer:** A worker can do that. We do not need a separate process just to change
`CANCEL_REQUESTED` to `CANCELLED`. It can conditionally update the job row only if it is still
`CANCEL_REQUESTED`, then delete its SQS notification under the tutorial's terminal-only
acknowledgement rule. If another process already finalized cancellation, it observes terminal state.

“Cancellation controller” names a responsibility, not necessarily a separate deployment; its code
could run in the worker, API, or existing reconciliation loop. A fallback is useful because
cancellation must finish when no worker observes it: a worker may crash, a job may be waiting for
assignment, or a notification may be unavailable. Relying exclusively on an executing worker can
leave `CANCEL_REQUESTED` unresolved.

The two-path arrangement is:

```text
Worker sees CANCEL_REQUESTED
  → conditionally change the database job state to CANCELLED
  → under the tutorial policy, delete its current SQS receipt

No worker sees CANCEL_REQUESTED
  → reconciliation loop discovers the pending database state
  → conditionally change the database job state to CANCELLED
  → a live or later receiver can acknowledge its own notification
```

Practical arrangement: worker sees cancellation → finalize immediately; worker never sees it →
reconciliation loop finalizes it.

An even simpler option for the stated contract is direct conditional API transition to `CANCELLED`,
with physical stopping requested separately. `CANCELLED` means successful publication is prevented,
not that every instruction stopped, so a pending cancellation state is not inherently necessary.
`CANCEL_REQUESTED` is useful when additional cancellation work must finish before declaring the
application outcome complete, e.g. coordinating external systems or confirming resource release in
a different contract.

A separate cancellation process is not essential here. The tutorial separates the responsibility
to make recovery explicit; implement it in a worker plus fallback or simplify into the API if the
contract permits. “Commit `CANCELLED`” here means conditionally changing the database job state; it
does not change the contents of an SQS message.

These are implementation alternatives and explanations, not a selected policy, a new deployment,
or runtime verification. The original state machine, cancellation definition and terminal-only
acknowledgement rule remain unchanged.

</details>

The cancellation controller usually does not have the worker's SQS receipt handle. A receiver
finding `CANCEL_REQUESTED` must defer the notification and avoid starting work. After the database
records `CANCELLED`, a live worker or the next receiver can delete its own current receipt. This
keeps the same “delete after a terminal outcome” rule for cancellation.

<details>
<summary>Question: Why not delete the SQS message at CANCEL_REQUESTED?</summary>

**Question:** Best-effort stopping says `CANCELLED` prevents successful publication but does not
prove GPU execution stopped. Why can't a worker seeing `CANCEL_REQUESTED` in RDS just delete its
SQS receipt? Why keep it and check later, probably at the next heartbeat, for `CANCELLED`?

**Answer:** It can delete its SQS message at `CANCEL_REQUESTED` if another durable mechanism
guarantees that cancellation will finish. SQS does not require waiting for `CANCELLED`. The tutorial
chooses one consistent acknowledgement rule: delete notifications after the database records a
terminal outcome. This is a conservative policy, not an SQS requirement.

`CANCEL_REQUESTED` means cancellation is saved and successful publication is blocked, but our
cancellation controller still must record the final outcome; `CANCELLED` means the application has
recorded that terminal outcome. The tutorial's flow is:

```text
RUNNING
  → cancellation wins the guarded database transition
CANCEL_REQUESTED
  → cancellation controller or reconciler finishes the durable transition
CANCELLED
  → a live worker or later receiver deletes its own current SQS receipt
```

If a worker deletes the message while cancellation is pending, then disappears, something else
must still discover pending cancellation and finish the transition. A reliable controller scanning
PostgreSQL can do this; with that guarantee, early deletion is a valid alternative.

Keeping the message until terminal status preserves another notification a later receiver can
inspect; it does not itself finish cancellation, and the controller still must do that work. The
worker need not hold the receipt or check on every heartbeat. Under the tutorial's policy it can
defer the message or let visibility expire. A later receiver gets its own handle, observes
`CANCELLED`, and deletes its notification.

This does not require waiting for every GPU instruction to stop: `DeleteMessage` does not stop
computation; `CANCELLED` does not certify physical stopping; once `CANCEL_REQUESTED` is recorded,
the guarded success update already prevents publication. Early deletion can be safe when durable
cancellation recovery is independent of that message, rather than when the GPU has physically
stopped.

This is acknowledgement-policy reasoning, not a replacement for the tutorial's terminal-only
message deletion rule, a production-policy choice, or a runtime experiment. SQS alone does not
finish cancellation. Because the job is no longer `RUNNING`, heartbeat, progress and success
updates that require `RUNNING` do not remain valid after `CANCEL_REQUESTED`.

</details>

**Best-effort stopping** means we request that computation stop, but an already-running GPU operation
or unreachable process may continue temporarily. In this contract, `CANCELLED` means the job will
not publish a successful result; it does not certify that every physical instruction has stopped.
The terminal states are stable—retries cannot resurrect a cancelled job.

<details>
<summary>Question: How should we stop GPU work during cancellation?</summary>

**Question:** How should we approach stopping a worker in the middle of an operation for
cancellation? If I have a process running on the GPU, do I kill the process, or what?

**Answer:** Usually first ask the job to stop cooperatively. If it does not stop, terminate its
process only if that process is isolated to the job.

First distinguish two things:

- The **worker process** is the Python/application process running on the CPU. It launches work,
  uses a CUDA context and reacts to cancellation controls.
- A **GPU kernel** is a function that the worker has launched on the GPU. The CPU-side process can
  stop submitting more kernels, but an operation already executing on the GPU may finish before
  the application can act.

The intended flow is:

```text
Cancellation request
  → block official result publication in the database
  → tell the job to stop
  → job checks at a safe boundary
  → stop launching more GPU work and exit
  → if still stuck, terminate only an isolated job process
```

A cooperative loop can look like this:

```python
for batch in video_batches:
    if cancellation_requested(job_id):
        break
    process_batch_on_gpu(batch)
```

Checks can occur between video batches, diffusion denoising steps or generation steps.
**Cancellation latency** is the time between the request and the work actually stopping. Smaller
work units create more safe boundaries and usually reduce that latency. A shared flag, event,
control connection or database poll can carry the request, but the control path must remain
responsive during computation.

This loop is conceptual. It omits exception handling, cleanup, partial-output handling, final state
updates and signal coordination. It also does not interrupt a GPU operation already in flight.
Ordinary PyTorch's documented CUDA interface enqueues asynchronous GPU operations and provides
synchronization; it does not provide a general undo/stop operation for an arbitrary already-launched
kernel. The practical cooperative action is to stop submitting further work at a safe boundary.

For stronger isolation, use a supervisor plus a child process dedicated to one job:

```text
Supervisor
  → starts isolated child job process
  → requests cooperative stop
  → waits a bounded grace period
  → sends SIGTERM if the child is still alive
  → if still alive, escalates to SIGKILL
  → observes process exit and reconciles resources and partial outputs
```

`SIGTERM` is not guaranteed to be cooperative: the child may use the default terminating action,
install a handler, delay handling or be stuck. `SIGKILL` cannot run application cleanup. Python's
process documentation also warns that termination can skip `finally`/exit handlers, corrupt pipes
or queues, strand locks and leave descendant processes running, so a supervisor must manage any
additional processes and recover durable state rather than relying on child cleanup.

Unix signals target the CPU-side process or process group associated with the GPU work; they are not
a promise of immediate GPU-kernel preemption. When a CUDA context is destroyed, the CUDA driver
cleans the resources associated with that context, but these interfaces do not promise that sending
an OS signal instantly stops device execution or instantly releases every allocation. A shared GPU
reset is not the cancellation mechanism for one job.

| Execution arrangement | Preferred cancellation approach |
|---|---|
| Our own batch/step loop | Check cancellation at safe boundaries and stop launching more work. |
| Dedicated process for one job | Request cooperative stop, then terminate that isolated process after a bounded grace period if necessary. |
| Shared inference server serving many jobs | Use the engine's request-level abort/cancellation API; killing the process would interrupt unrelated jobs. |

For example, current vLLM exposes `AsyncLLM.abort(request_id)` and its scheduler handles an external
finish signal, removes that request and frees its request state. That is an example of an
engine-supported per-request boundary, not a claim that every engine behaves identically. Work
already executing in a shared GPU step may still return before the engine observes the abort; the
engine must ignore stale output and stop scheduling the request rather than kill every tenant's
server process.

Supervisor plus isolated job process is a practical design for this video-service example when
forced stopping matters, but shared model serving needs request-level boundaries. Preventing
official result publication and reclaiming computation are separate tasks. This is design guidance,
not a cancellation policy Hooman selected, an implementation, or a runtime experiment.

**Evidence and limits, checked November 15, 2026:**

- PyTorch [CUDA semantics: asynchronous execution](https://docs.pytorch.org/docs/2.15/notes/cuda.html#asynchronous-execution)
  says GPU operations are enqueued asynchronously and documents synchronization. The statement
  about no general PyTorch kernel-undo operation is scoped to this ordinary documented interface;
  it is not a claim about every lower-level CUDA mechanism or engine.
- NVIDIA's CUDA Programming Guide [asynchronous-execution section](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/asynchronous-execution.html)
  says kernel launches return before completion and documents synchronization/query operations;
  destroying a busy stream completes its work before destruction. The CUDA Driver API
  [`cuCtxDestroy`](https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__CTX.html#_CPPv412cuCtxDestroy9CUcontext)
  documents cleanup of resources associated with a context, not instantaneous cancellation timing.
- Python's [`multiprocessing.Process.terminate` and `kill`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Process.terminate)
  documents POSIX `SIGTERM`/`SIGKILL`, skipped cleanup and descendant-process limits. POSIX
  [`kill()`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/kill.html) defines sending a
  signal to a process or process group; it does not provide a GPU-completion guarantee.
- vLLM's current [`AsyncLLM.abort`](https://docs.vllm.ai/en/stable/api/vllm/v1/engine/async_llm.html#vllm.v1.engine.async_llm.AsyncLLM.abort)
  and scheduler [`finish_requests`](https://docs.vllm.ai/en/stable/api/vllm/v1/core/sched/scheduler.html#vllm.v1.core.sched.scheduler.Scheduler.finish_requests)
  provide one primary-source example of request-level abort and request-state cleanup.

The previously recorded internal endpoint source at
`/home/colligo/colligo/pylibs/colligo/fastapi/endpoints/v3_async_jobs.py` is not accessible from
this Mac checkout, so no current internal worker-stop, signal or GPU-cleanup behavior was verified.
No process was signalled, no GPU work was launched or reset, and no cancellation path was executed.

</details>

Check tenant access for both status and cancellation. Knowing a job ID is not permission to view
or cancel it.

## 9. Now add capacity and customer boundaries

Only add these requirements after you can explain one job and the preceding failure cases.

### A queue buys time; it does not create processing capacity

The exercise specifies 2 submissions/second normally and 50/second for a ten-minute burst.
If processing averaged **10 minutes**—an extra assumption, not a measurement—steady-state demand
would be about `2 × 600 = 1,200` concurrent job executions. That is execution capacity, not necessarily
1,200 machines or GPUs: how many jobs fit on a machine depends on the actual workload.

If the fleet can complete only 2 jobs/second throughout the burst, approximately
`(50 − 2) × 600 = 28,800` jobs accumulate. After arrivals return to 2/second, that same fleet does
not drain the backlog; it needs spare capacity or reduced accepted load. Benchmark actual processing
and account for input/output traffic before claiming a capacity number.

**Backpressure** means slowing or refusing incoming work when downstream capacity cannot keep up.
We can impose per-customer outstanding-job limits, return an explicit busy response, or admit work
with a stated wait. A **quota** is a limit allocated to a customer; it protects other tenants and
controls cost. CPU/GPU resource-class queues help match work to compatible workers, but one shared
queue alone does not guarantee fair service among tenants.

### Availability, access and retention are separate requirements

An **SLO**, service-level objective, is a measurable reliability/performance target. The prompt's
99.9% monthly API availability target needs a precise measurement definition and an operational
design: redundant API/sender processes, database failure recovery and monitoring. Drawing S3/SQS/RDS
boxes is not evidence the complete application meets that target.

Practical controls include:

- Authenticate customers, then authorize each input, job and result against their tenant. Validate
  media and allowed transforms; do not run arbitrary commands supplied in a request.
- Keep S3 objects private. A **presigned URL** is a time-limited download link authorized by the
  service; anyone holding it can use that access until it expires, so protect the link. Issue it only after
  the API checks access to the selected output, specifying its exact version ID.
- Give API, sender and workers AWS IAM roles with narrowly scoped permissions,
  rather than embedding long-lived credentials in code. A worker may need specified queue,
  database and S3 access, not access to all customer storage.
- Implement 30-day output and 90-day metadata retention deliberately. S3 lifecycle policies can
  remove objects according to age rules; database cleanup removes expired rows separately. A job
  can remain historically successful after its output expires, so the API should state that the
  output is no longer available. Queue-message retention is a third, separate policy.
- Watch the oldest waiting job, unsent outbox age, expired leases, failed attempts and completion
  latency. A **dead-letter queue** holds messages set aside after repeated delivery failures for
  diagnosis. Moving a message there does not automatically mark the business job `FAILED`.

The original prompt guarantees survival of ordinary process/worker restarts, not every regional
disaster. Cross-region recovery requires additional data copies and defined recovery objectives; identify
that extension rather than claiming it is already solved.

## 10. Practical alternatives and what we implement

Use one coherent baseline first. These alternatives explain why the choices are not universal.

| Decision | Our worked choice | When another choice makes sense |
|---|---|---|
| Job state | PostgreSQL on RDS: SQL tables, unique constraint, transactions and conditional updates | DynamoDB supports key-based records, conditional writes and transactions too. It needs deliberate key/access-pattern design rather than the same SQL pasted into another database. Useful when those access patterns and managed scaling fit. |
| Dispatch | SQS Standard plus a PostgreSQL outbox | A small service can have workers poll a PostgreSQL jobs table directly, avoiding the separate message-send problem. Measure database load and recovery behavior. |
| Worker selection from a DB queue | An SQS message already points to one job ID; lock that row briefly for the claim | `FOR UPDATE SKIP LOCKED` lets database-queue consumers lock eligible rows while skipping rows another consumer locked. The brief row lock protects the claim, as in section 6. It is not needed on every ordinary read, and it is not a lock held during video processing. |
| Queue product | Managed SQS, with our explicit duplicate handling | RabbitMQ, possibly via Amazon MQ, is another broker option when its routing/protocol features matter. Operating it yourself adds maintenance. Kafka is a retained event log useful for replay and multiple readers; it is not an automatic improvement for a simple worker queue. |
| Ordered work | No global ordering required | SQS **FIFO** (first in, first out) supports ordering within message groups and send deduplication features. It still does not make our database, video processing and S3 updates one transaction or guarantee one business side effect. |
| Worker execution | Our program on EC2 or ECS with suitable machines | AWS Batch can manage batch job scheduling. That changes who manages dispatch/retries; do not add SQS and a second scheduler without assigning their responsibilities clearly. **Fargate** runs containers without our managing the underlying machines, but does not support GPU resource requirements. GPU container workloads need a suitable environment such as GPU-equipped EC2 workers. |
| Progress reporting | Client polls our status endpoint | A **callback** is an HTTP request our service sends to an endpoint the client supplies; it can notify the client without repeated status queries, but our code then needs authenticated delivery, retries and duplicate handling. SQS worker messages and customer callbacks are different communication paths. |

<details>
<summary>Question: Can you explain these alternatives in more detail?</summary>

The table is a map of alternative ways to fill responsibilities, not a list of products to stack
together. A design generally chooses a coherent owner for each responsibility:

```text
durable job state   -> PostgreSQL or DynamoDB
work dispatch       -> SQS, a database queue, RabbitMQ, or a deliberately designed Kafka flow
container execution -> ECS on EC2/Fargate, or a batch scheduler such as AWS Batch
```

The boundaries still matter after a product swap. No queue or scheduler automatically makes a
PostgreSQL state change, an S3 upload and an external submission one atomic operation.

#### 1. DynamoDB: what does deliberate key/access-pattern design look like?

**User question:** Dynamodb stores key/values does it mean it cannot be queried the way postgreSql
is? Is dynamo still a RDS (relational database)? “It needs deliberate key/access-pattern design
rather than the same SQL.” Give me example/details on what this would look like.

**Answer:** DynamoDB is a nonrelational database, separate from Amazon RDS. RDS is a managed
relational-database service that offers engines including PostgreSQL and MySQL. A DynamoDB item is
not limited to one opaque scalar value: it can have named attributes containing strings, numbers,
lists, nested maps and other supported types.

A DynamoDB table identifies an item with a **partition key**, or with a composite primary key made
from a partition key and a **sort key**. The partition-key value is input to DynamoDB's internal
placement function; it should not be confused with one fixed physical disk partition. Items with
the same partition-key value can be grouped and ordered by sort key.

An illustrative job item could be:

```json
{
  "PK": "TENANT#acme",
  "SK": "JOB#job-742",
  "status": "RUNNING",
  "owner": "worker-A",
  "attempt": 1,
  "lease_deadline": "2026-11-15T10:03:00Z",
  "input_key": "inputs/acme/video-91",
  "selected_output_version": null
}
```

An exact `GetItem` can load that job from its two key values. A `Query` can read items for
`PK = TENANT#acme`, optionally narrowing their sort keys—for example, keys beginning with `JOB#`.
But suppose the application must answer “give me Acme's queued jobs, oldest first.” PostgreSQL can
express the desired rows first and let indexes support the query:

```sql
SELECT *
FROM jobs
WHERE tenant_id = 'acme' AND status = 'QUEUED'
ORDER BY created_at
LIMIT 20;
```

With DynamoDB, that access pattern normally motivates an alternate index whose keys are written
with each eligible item, for example:

```text
queue_pk = TENANT#acme#STATE#QUEUED
queue_sk = 2026-11-15T10:00:00Z#job-742
```

The worker queries that exact `queue_pk` and reads the lowest sort keys first. A global secondary
index is an alternate key view and is eventually consistent, so seeing `job-742` there is only a
candidate-selection result. A conditional update of the authoritative job item—checking its
current state, attempt and lease rules—decides whether the claim succeeds.

`Query` is key-oriented: it requires a partition-key value and can apply a sort-key condition.
`Scan` examines every item or index entry, and applying a filter afterward does not make those
reads free. DynamoDB supports conditional writes, transactions and a SQL-compatible PartiQL
syntax, but only a DynamoDB-specific subset; this is not PostgreSQL's general join and ad hoc query
model. The job, idempotency mapping and outbox can be distinct DynamoDB items written in one
transaction. Sending to SQS remains outside that database transaction, just as it does with
PostgreSQL.

Primary sources checked November 15, 2026: [DynamoDB core components](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html),
[Query](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html),
[Scan](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html),
[read consistency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html),
[transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html),
[PartiQL support](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html), and
[Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html).

#### 2. What does “measure database load and recovery behavior” mean?

**User question:** More details on how to do this and why exactly we are doing this and the
implications: Measure database load and recovery behavior.

**Answer:** In the database-queue alternative, workers repeatedly ask PostgreSQL for eligible work:

```text
find eligible row -> claim in a short transaction -> commit -> process outside the transaction
        ^                                                        |
        +---------------- back off and poll again ----------------+
```

This can remove a component: job acceptance and dispatch eligibility live in the same database,
so there is no separate PostgreSQL-to-SQS send gap. The implication is that the job database now
also carries queue polling and claim traffic. Empty polling can become the dominant load when many
workers are idle.

For scale intuition only, not a measured result: 100 idle workers polling every 0.1 seconds can
issue about 1,000 polls per second. Polling once per second reduces that to about 100 polls per
second, but a newly eligible job may wait longer to be noticed. Backoff with jitter, notifications
used only as hints, and appropriate indexes are possible ways to change that tradeoff.

Measure at least these scenarios before relying on the design:

| Scenario | Exercise | Observe |
|---|---|---|
| Idle | Workers find no jobs | Polls/second, CPU, reads, connections and backoff behavior |
| Steady work | Jobs arrive near normal rate | Claims/second, claim latency, lock waits, submit/status latency and oldest eligible job age |
| Burst | Many jobs and workers contend | Queue-drain rate, transaction latency, connection saturation, CPU/I/O and fairness |
| Worker failure | Crash after a committed claim | Lease expiry, reclaim delay, duplicate execution and rejection of stale publication |
| Database interruption | Make PostgreSQL temporarily unavailable in a controlled environment | Whether submissions and claims fail safely, and whether eligible jobs resume after recovery |
| Ambiguous completion | Lose the response after the guarded success commit | Whether a retry reads the terminal outcome rather than creating a second official result |

An index should support the exact eligibility/order predicate so each poll does not rescan a large
history of terminal jobs. Database and application measurements should be read together: low query
latency is not success if jobs become stranded, and high throughput is not correctness if a stale
worker can publish. These are proposed design tests and metrics; no benchmark or failure drill was
run for this guide.

Primary sources checked November 15, 2026: PostgreSQL documents the statistics views used to
inspect server activity in [the cumulative statistics system](https://www.postgresql.org/docs/current/monitoring-stats.html)
and explains index tradeoffs in [Indexes](https://www.postgresql.org/docs/current/indexes.html).

#### 3. Is `FOR UPDATE SKIP LOCKED` an alternative to locking the row?

**User question:** How is this an alternative to “locking the row in db for our: Worker selection
from a DB queue”? `FOR UPDATE SKIP LOCKED` lets database-queue consumers lock eligible rows while
skipping rows another consumer locked.

**Answer:** It is not an alternative to row locking. `SKIP LOCKED` changes what a worker does when
a candidate row is already locked by another transaction.

With SQS, the notification already names one job, so the claim transaction can target that row:

```sql
SELECT job_id
FROM jobs
WHERE job_id = :job_id
FOR UPDATE;
```

With a PostgreSQL queue, the database must choose an eligible row:

```sql
SELECT job_id
FROM jobs
WHERE status = 'QUEUED'
ORDER BY created_at, job_id
LIMIT 1
FOR UPDATE SKIP LOCKED;
```

Normal two-worker flow:

```text
worker A: locks oldest eligible row -> marks RUNNING/owner/attempt/lease -> commits
worker B: sees A's short row lock -> skips it -> can lock the next eligible row
```

The selection and the update that marks the row claimed must occur in the **same transaction**.
Selecting a row, committing without marking it, and updating later would let another worker select
the same unclaimed job. Once the claim commits, release the PostgreSQL row lock before the long
video operation. The durable, renewable application lease—not a transaction held open for the
video—then represents ownership.

The SQL above illustrates queued selection. A complete recovery design also makes expired
`RUNNING` rows eligible under the lease policy and still guards the claim update. `SKIP LOCKED`
skips PostgreSQL row locks held by concurrent transactions; it does not skip or replace application
leases stored in columns.

Primary source checked November 15, 2026: PostgreSQL states that `SKIP LOCKED` skips selected rows
that cannot be locked immediately, produces an inconsistent view unsuitable for general-purpose
work, and can avoid contention among consumers of a queue-like table in
[`SELECT`](https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE).

#### 4. RabbitMQ, Amazon MQ and Kafka

**User question:** Teach me more about Rabit MQ and amazon MQ and Kafka: RabbitMQ, possibly via
Amazon MQ, is another broker option when its routing/protocol features matter. Operating it
yourself adds maintenance. Kafka is a retained event log useful for replay and multiple readers;
it is not an automatic improvement for a simple worker queue.

**Answer:** A **message broker** accepts messages from producers and delivers them through configured
routes to consumers. RabbitMQ's central routing object is an **exchange**:

```text
producer -> exchange --binding/routing rule--> queue -> consumer -> acknowledgement
```

A topic exchange matches dot-separated routing keys. For example, a queue bound with
`video.gpu.*` can match `video.gpu.resize`. A fanout exchange ignores the routing key and sends a
copy to every bound queue. That is useful when distinct queues need separate copies, whereas a
work queue normally has competing consumers for one queue.

A **publisher confirm** tells the producer what happened on the producer-to-broker side. A
**consumer acknowledgement** tells the broker that a delivered message was handled on the
broker-to-consumer side. RabbitMQ documents these as independent mechanisms; a publisher confirm
does not prove that a consumer completed the video. Consumer failures or lost connections can
cause requeueing and redelivery, so business operations still need duplicate handling.

Amazon MQ is AWS-managed hosting for RabbitMQ and Apache ActiveMQ Classic. AWS manages broker
setup, operation, maintenance and version upgrades. The application still owns its topology,
routing, acknowledgement, retry and capacity choices. Amazon MQ is not SQS, and it is not managed
Kafka.

Kafka uses a different core model: a topic is a retained, partitioned log of records. Each record
has a position called an **offset**. Consumers in one **consumer group** divide partitions for
parallel processing and track their positions; a separate group has an independent position. For
example, billing, analytics and audit groups can each read the same events. Reading or checkpointing
an offset does not delete the record; topic retention permits later replay. Ordering is defined
within a partition, not across every partition in a topic. Amazon Managed Streaming for Apache
Kafka (Amazon MSK) is AWS's managed Kafka service.

| Need | Usually the more natural starting point |
|---|---|
| Simple managed delivery of work notifications | SQS |
| Broker routing patterns or messaging protocols | RabbitMQ |
| Managed RabbitMQ or ActiveMQ broker hosting | Amazon MQ |
| Retained stream, replay and independent reader groups | Kafka, or Amazon MSK on AWS |

These are fit comparisons, not a selection of a new queue. None makes RDS updates, S3 writes or
external business side effects atomic by itself.

Primary sources checked November 15, 2026: RabbitMQ [exchanges and bindings](https://www.rabbitmq.com/docs/exchanges)
and [publisher confirms versus consumer acknowledgements](https://www.rabbitmq.com/docs/confirms);
AWS [What is Amazon MQ?](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html)
and [What is Amazon MSK?](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html);
Apache Kafka [introduction](https://kafka.apache.org/44/getting-started/introduction/) and
[consumer design](https://kafka.apache.org/44/design/design/#the-consumer).

#### 5. EC2, ECS, Fargate and AWS Batch

**User question:** Give me more infor about “aws batch” and also Fargate. And ECS (if needed): AWS
Batch can manage batch job scheduling. That changes who manages dispatch/retries; do not add SQS
and a second scheduler without assigning their responsibilities clearly. Fargate runs containers
without our managing the underlying machines, but does not support GPU resource requirements. GPU
container workloads need a suitable environment such as GPU-equipped EC2 workers.

**Answer:** Start by separating the layers:

| Layer | Meaning here |
|---|---|
| Container | Packaged application code, runtime and dependencies |
| EC2 | Virtual-machine compute; suitable EC2 instance families can provide GPUs |
| ECS | Service that schedules and runs container **tasks**; a task is one or more containers described together |
| Fargate | Serverless compute capacity for supported ECS tasks, so we do not manage the underlying hosts; GPU resource requirements are not supported |
| AWS Batch | Batch-job queueing and scheduling layer that runs containerized jobs on configured compute environments |

ECS tasks can run on EC2 capacity or Fargate. For an ECS GPU task, use suitable GPU-capable EC2
container instances and declare the GPU requirement. Fargate is attractive for supported CPU
workloads because AWS supplies the compute capacity, but it is not the GPU path described by the
current ECS task-definition documentation.

AWS Batch adds batch-specific objects and policy:

- A **job definition** describes the container image, command, vCPU, memory, environment and roles.
- A **job queue** holds submitted jobs until the scheduler can run them and can express priority.
- A **compute environment** supplies eligible capacity and is associated with job queues.
- A **retry strategy** tells Batch which failed executions it may try again.

Batch supports GPU jobs on supported GPU-equipped EC2 capacity. It schedules the requested GPU
resources to a container; this does not turn Fargate into GPU compute.

The architectural change is easiest to see as two alternative flows:

```text
current teaching flow:
PostgreSQL outbox -> dispatcher -> SQS -> long-running worker on suitable compute

possible Batch flow:
PostgreSQL outbox -> idempotent dispatcher -> Batch SubmitJob -> Batch queue/scheduler -> job container
```

Here, “idempotent dispatcher” describes the application's goal of one logical job and one official
result; it does not guarantee exactly one Batch submission. If Batch accepts a request but its
response is lost, retrying can create multiple Batch jobs. Each launched container must pass the
application's conditional database job/attempt claim before doing work; a duplicate defers or exits
according to that contract. Persisting a returned Batch job ID helps tracking, but cannot by itself
resolve an accepted submission whose ID was never received. The [`SubmitJob` API](https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html)
does not document a client idempotency token, and a repeated job name is not a uniqueness guarantee.
This clarification does not select a new dispatch policy.

The Batch `jobId` returned by `SubmitJob` is different from the application's `job-742`; store the
mapping. The application still owns tenant authorization, request idempotency, official-output
selection and reconciliation of an ambiguous submission response. Do not assume an arbitrary
repeated `SubmitJob` request is deduplicated merely because the job name is repeated.

SQS and Batch can both appear in one design, but only with explicit duties—for example, SQS as a
submission reminder and Batch as the compute scheduler. Then define which system owns dispatch
retry, Batch retry and recovery so their retries do not create uncontrolled overlapping work.
Batch changes who schedules compute; it does not remove the application's atomicity and
idempotency problems.

Primary sources checked November 15, 2026: AWS [What is Amazon ECS?](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html),
[ECS GPU task definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-gpu.html),
[ECS task-definition parameters](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html#container_definition_resource_requirements),
[What is AWS Batch?](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html),
[job definitions](https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html),
[job queues](https://docs.aws.amazon.com/batch/latest/userguide/job_queues.html),
[compute environments](https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html),
[automated retries](https://docs.aws.amazon.com/batch/latest/userguide/job_retries.html),
[GPU jobs](https://docs.aws.amazon.com/batch/latest/userguide/gpu-jobs.html), and
[`SubmitJob`](https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html).

**Evidence boundary:** All identifiers, SQL, rates and flows above are teaching examples. No
service was deployed, benchmarked or failure-tested for this clarification, and these alternatives
do not record a production-policy decision.

</details>

### What would the implementation contain?

These responsibilities can share a deployment; each box does not need its own separate program:

1. Database migrations—versioned changes that create/alter tables—for jobs and outbox records,
   including required tenant/key fields, their unique constraint and useful query indexes. An
   **index** helps the database locate matching rows without scanning all rows.
2. API handlers for submit/status/cancel and tenant authorization.
3. A sender loop for unsent outbox records.
4. A worker loop: receive a job ID, acquire ownership, read input, run code, renew ownership and
   message visibility, upload a result, conditionally finalize, then delete the received message.
5. A recovery/cancellation loop and cleanup policies for expired records and unused outputs.
6. Logs and measurements that show whether each responsibility is working.

For a local learning implementation, PostgreSQL plus local files and a database-polled queue can
teach most correctness rules. For an AWS implementation, S3/SQS/RDS provide the corresponding
managed pieces. Neither path needs to be built before understanding this lesson.

## 11. Check your understanding

You do not need to memorize table fields or cloud product names. Close the guide and answer:

1. Why are the video, job record and queue notification stored separately?
2. If a submit response is lost, who retained the identifier needed to retry safely?
3. What two records must be committed together, and which service is outside that transaction?
4. Why can a message be processed more than once even though we use a queue?
5. What stops an old worker from selecting the final output? What stops it overwriting the actual file?
6. Which database change wins when cancellation and completion race?

<details>
<summary>Question: How do my answers to the six understanding checks hold up?</summary>

**User request:** Check my answer to these questions.

**Reviewer summary:** The answers capture the main design. The main corrections are SQS ordering,
the service outside the transaction and S3 versioning.

### 1. Separate video, job record and notification

**User response:** video object is too large to put in db so needs s3. SQS is for queuing / ordering
messages and messages need to stay small, job record needs a database to maintain consistency, etc.

**Reviewer feedback:** Mostly correct: S3 fits large bytes, PostgreSQL searchable metadata and
state/transaction rules, and SQS notification delivery. SQS Standard does not guarantee order.
Large files can be stored in a database; object storage is a workload choice.

### 2. Lost submit response and safe retry

**User response:** the user/client generates the idempotency key and holds on to it. They can
submit the job with the same key. If it's already been recorded by us we won't create a duplicate
record.

**Reviewer feedback:** Correct: the client retains and reuses the idempotency key. The key is
tenant-scoped, the normalized request is compared, changed input gives a conflict, and database
uniqueness covers concurrent retries.

### 3. Records committed together and the outside service

**User response:** the record in the job table and the one in outbox need to happen together in one
transaction.

**Reviewer feedback:** Correct but incomplete: the job and outbox rows commit together; SQS sending
is outside the PostgreSQL transaction even if a network call is placed between `BEGIN` and `COMMIT`.

### 4. Why a queue message can be processed more than once

**User response:** Worker A takes it but dies before renewing visibility timeout, so worker B takes
the message, but then worker A resumes.

**Reviewer feedback:** This is a valid redelivery example if A pauses or becomes unreachable; a
dead process cannot resume. B receiving after visibility expiry still must pass the database claim.
Other causes include SQS Standard duplicate delivery and sender retries after a successful send but
failure to record that success.

### 5. Selecting the final output and protecting the file

**User response:** only the output from the worker with the latest attempt with an unexpired lease
can be selected (put the final version in job table). We can have per-attempt and per-upload
destinations in S3. Although in the basic implementation database versions can do this job too.

**Reviewer feedback:** The current owner, attempt number, valid lease and `RUNNING` state are checked
together. Attempt/upload-specific paths separate outputs. The version mechanism is S3 object
versioning, not database versioning: PostgreSQL stores the selected S3 version ID and downloads
specify it. Naming alone does not enforce immutability.

### 6. Cancellation versus completion

**User response:** whichever transaction gets committed first. If completion gets committed first,
the cancellation request is rejected. If cancellation gets committed first the result updates get
blocked.

**Reviewer feedback:** Correct under this design: conditional transitions lock or update the same
row. Success first makes cancellation report that the job is already complete; cancellation first
causes completion's `RUNNING` predicate to fail. Commit order alone cannot protect unconditional
writes.

**Key distinction:** receiving a message, owning a job and publishing an output are separate events
and permissions.

These responses and comments were supplied in conversation. Their format does not establish that
the answers were unaided or closed-book, that the companion design exercise is complete, or that
the concepts have been mastered.

</details>

If an answer is unclear, revisit that story and diagram. These are understanding checks, not proof
that you have already passed a timed interview. Once the picture makes sense, attempt the prompt in
`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/STUDY_GUIDE.md`.

## 12. Separately: how to present this in an interview

Only practice this compression after understanding the tutorial. You would not recite every term
or introduce every mechanism in the opening minute.

1. **Clarify the goal:** long-running jobs, accepted-work durability, scale, isolation, cancellation
   and whether regional failure is in scope. Clarify API availability versus job-completion targets.
2. **Draw the simple system:** API, job database, video storage, queue and workers. Explain the
   normal submission/result path. Show the sender when explaining reliable dispatch.
3. **Make one estimate:** arrival rate and average processing time imply needed concurrent work;
   state assumptions and explain burst behavior.
4. **Follow the failure the interviewer cares about:** lost response → submission key; saved job
   without notification → outbox; duplicate/stalled worker → conditional claim/lease/attempt number;
   partial output → separate upload plus conditional publication.
5. **Defend a trade-off:** PostgreSQL queue versus SQS; PostgreSQL versus DynamoDB; redelivery
   versus earlier acknowledgement plus recovery scans. Explain why the chosen contract fits.
6. **Extend if asked:** fairness, rollout/migration, region recovery, pipeline reproducibility and
   ownership across teams. Do not pretend these are already implemented by the diagram.

<details>
<summary>Question: What could a strong spoken interview answer sound like?</summary>

**Request being answered:** Add a closed-by-default interview sample under this presentation
guidance while the next lesson proceeds separately.

This is a rehearsal model, not a claim that the speaker deployed this system, measured its
performance or completed the companion exercise. It is one coherent answer to the fixed exercise,
not a universally “perfect” script.

### Spoken sample

**Me:** “Before I choose the components, I want to clarify a few promises.

“First, the 99.9% monthly target is for submission and status APIs. Is there also a deadline by
which an accepted video must finish, such as 99% within an hour? Second, does ‘survives restarts’
include losing an entire AWS Region, or ordinary process, host and Availability Zone failures in
one Region? Third, is cancellation allowed to mean ‘prevent an official result and stop compute as
soon as practical,’ rather than guaranteed instantaneous GPU preemption? Finally, may the service
run a transform more than once internally as long as the customer sees one logical job and one
official result?”

**Interviewer, using the fixed exercise:** “The 99.9% target applies to the two APIs. There is no
separate job-completion target in the prompt, so state a reasonable assumption rather than inventing
one. Design one Region for ordinary restarts and lost responses; discuss regional recovery only if
asked. Cancellation is best effort, and duplicate execution is acceptable if stale results never
become official.”

**Me:** “Great. I’ll design for durable eventual processing after acceptance, but I will not call
that a quantified completion SLA. I’ll make queue age and completion latency observable so a real
product target can be set from workload measurements. I’ll start with a single-Region, Multi-AZ
design; that is a proposal for the API availability target, not proof that the boxes alone achieve
99.9%, and it does not cover loss of the Region.

“Here is the first-pass architecture.”

```text
                                      status reads / cancel
client -----------------------------> API ----------------------+
  |                                    |                         |
  | submit: input reference +          | one transaction         v
  | transform + idempotency key        +--------------> PostgreSQL
  |                                                       jobs + outbox
  |                                                            |
  | 202 after commit: job ID + status URL                       v
  |                                                      outbox sender
  |                                                            |
  |                                                            v
  |                                                           SQS
  |                                                            |
  |                                  +-------------------------+|
  |                                  v                          |
  +--> private S3 input ----------> CPU/GPU workers <-----------+
                                         |
                                         +--> private S3 per-attempt output/version
                                         |
                                         +--> guarded PostgreSQL completion
```

**Me:** “PostgreSQL is the authoritative job state. S3 stores the large input and output bytes.
SQS carries small work notifications, not the job truth. Stateless API instances, redundant outbox
senders and worker capacity can run across Availability Zones; the database and other dependencies
also need appropriate Multi-AZ configurations and tested recovery. I would measure the actual API
availability rather than infer it from this diagram.

“On submit, the API authenticates the tenant, authorizes the referenced private S3 input, validates
the transform as untrusted input and requires a client-retained idempotency key scoped to that
tenant. In one PostgreSQL transaction it inserts the job and an outbox row. A unique constraint on
tenant plus idempotency key handles concurrent retries. If the same key arrives with the same
normalized request, I return the original job; if its input or transform differs, I return a
conflict rather than silently changing the job.

“Only after the transaction commits do I return `202 Accepted` with the job ID and status URL.
Therefore, if the database commit succeeds but the response is lost, the client retries the same
key and discovers the same job.

“The outbox sender reads committed unsent rows and sends the job ID to SQS. That network call cannot
join the PostgreSQL transaction. A sender crash can therefore cause a retry and a duplicate SQS
notification; the worker path must be safe under duplicate delivery. The sender records progress,
but PostgreSQL remains the authority for whether the business job exists.

“When a worker receives a message, it briefly locks or conditionally updates that job row. It may
claim a queued job, or reclaim an expired running job under the recovery policy. The claim records
an owner ID, increments the attempt and sets a renewable database lease. The worker commits and
releases the row lock before downloading gigabytes or running a two-to-sixty-minute pipeline.

“During processing it renews two independent timers: the database ownership lease and the SQS
visibility timeout. A valid database lease decides who may publish; SQS visibility merely reduces
concurrent delivery of that notification. A long-running job remains on the same attempt as long
as its renewal loop stays responsive. Receiving a duplicate message does not itself grant
ownership.

“On success, the worker uploads to an attempt- and upload-specific S3 destination with bucket
versioning enabled. Then it performs one guarded PostgreSQL update that selects the exact S3
version only if the job is still `RUNNING`, this worker and attempt are current, and the database
lease has not expired. If the predicate fails, its upload is not official. If it succeeds, the job
becomes terminal `SUCCEEDED`; only after that database commit does the worker delete its own SQS
receipt.

“The status API authorizes the tenant and reads the job row. For a succeeded job it creates access
to the exact selected private S3 version, rather than whatever object happens to be latest under a
name. Output bytes are retained for 30 days and job metadata for 90 days. Cleanup always preserves
the selected version through its output-retention period. For an unselected upload, cleanup waits
for the existing grace period, uses producing-job and attempt metadata, rechecks PostgreSQL, and
deletes only when that attempt is permanently unable to publish it. That avoids racing a valid
worker between upload and database finalization.”

**Interviewer:** “Give me one sizing estimate.”

**Me:** “The prompt gives a steady arrival rate but not a mean execution time, so I’ll explicitly
assume ten minutes, or 600 seconds, only for this estimate. Little’s Law gives roughly:

```text
2 jobs/second × 600 seconds = 1,200 concurrent executions
```

“That is not 1,200 GPUs. Jobs have heterogeneous CPU, GPU, memory and I/O requirements, and the
runtime range is two to sixty minutes. I would classify transforms into resource pools, measure
their runtime distributions and bottlenecks, and then translate concurrent work into instance and
accelerator capacity with headroom. The arithmetic is a planning input, not an empirical result.”

**Interviewer:** “What does the ten-minute burst do?”

**Me:** “If arrivals are 50 per second for 600 seconds and the fleet can actually complete only
about 2 per second, backlog grows by approximately:

```text
(50 - 2) jobs/second × 600 seconds = 28,800 jobs
```

“When arrivals return to 2 per second, a fleet whose full throughput is 2 per second has no spare
capacity to drain that backlog. I need temporary or permanent spare capacity, autoscaling whose
startup time fits the burst, or explicit admission control and a communicated waiting-time policy.
By contrast, `50 × 600 = 30,000` would be the concurrent-work estimate only if 50 per second were
sustained with a ten-minute mean and enough compute to start work at that rate. It is not the right
description of a finite burst constrained by a 2-per-second fleet.”

**Me:** “Now I’ll walk the principal failures because they determine the correctness rules.

“One: the client loses the submit response. The tenant-scoped idempotency key and unique constraint
return the already committed job.

“Two: the job commits but no notification is sent. The outbox row was committed with the job, so a
sender retry can deliver it. I also run a durable reconciliation path over PostgreSQL for accepted
`QUEUED` jobs and reclaimable expired `RUNNING` jobs whose work has no effective notification. That
recovery cannot rely only on SQS because notification retention is finite and a message can end up
in a dead-letter queue while the business job still exists. Reconciliation can safely create
another reminder because a reminder does not bypass the database claim.

“Three: worker A pauses, its database lease expires, worker B claims a newer attempt, and then A
resumes. A can consume compute and even upload bytes, but its guarded completion fails because its
owner, attempt or lease is stale. Attempt-specific destinations prevent A from overwriting B’s
bytes, and selecting an exact S3 version prevents a later upload from changing the published result.

“Four: a worker uploads and crashes before recording success. The job remains nonterminal, so its
lease can expire and recovery can start another attempt. The upload is an orphan candidate, but
cleanup does not delete it merely because the database has not selected it yet; it applies the
grace, attempt-state and final selected-version checks I described.

“Terminal states never return to `RUNNING`. Every success transition includes the true current
state and ownership predicates; commit order by itself would not protect an unconditional write.”

**Interviewer:** “How does cancellation race completion?”

**Me:** “The cancel API conditionally transitions a nonterminal job to `CANCEL_REQUESTED` on the
same authoritative row. The success update requires `RUNNING`, so if cancellation commits first,
successful publication is blocked. If guarded success commits first, cancellation observes
`SUCCEEDED` and reports the documented already-complete outcome. Those are the two valid race
results.

“A worker that observes `CANCEL_REQUESTED` can stop launching new work at safe boundaries and may
finalize `CANCELLED`. A durable fallback—such as the existing reconciliation loop—must finish the
transition if no worker observes it. I call that the cancellation-controller responsibility; it
does not require a separate deployment. Under this design, the SQS receipt is deleted after the
database has a terminal outcome. Earlier acknowledgement could also be safe if independent
database recovery were guaranteed, but I am keeping one conservative rule here.

“`CANCELLED` means the application will not publish a successful result. It does not prove that an
already launched GPU kernel stopped instantly. I would first request cooperative stopping between
batches or generation steps. If forced stopping matters, I would isolate one job in a child
process, ask it to stop, and let a supervisor terminate that process after a bounded grace period.
That resource-reclamation mechanism is separate from the guarded publication rule.”

**Interviewer:** “What principal trade-off are you making?”

**Me:** “I chose SQS plus a PostgreSQL outbox over having every worker poll PostgreSQL as the queue.
A database queue is a reasonable simpler baseline: workers can use a short transaction with
`FOR UPDATE SKIP LOCKED`, and it avoids a separate SQS send. Its cost is that idle polling, claims
and queue scans share connections, CPU and I/O with submission and status state.

“SQS gives managed work delivery, long polling and a buffer between dispatch and heterogeneous
workers. The outbox handles the database-to-queue gap without pretending it is a distributed
transaction. The cost is an extra sender, at-least-once notifications and explicit reconciliation.
For this high-concurrency, long-running workload I would start with that separation, then validate
it with measured database, queue-age and recovery behavior rather than claim it is always better.

“I also chose PostgreSQL because unique constraints, job-plus-outbox transactions and guarded
updates express these invariants directly and are familiar to the team. DynamoDB can implement a
sound design with deliberate partition/sort keys, conditional writes and transactions, but it is
not the same SQL query model. I would switch only if known access patterns and measured scaling or
operational needs justified that redesign.”

**Me:** “Finally, I would protect the service boundary: every API request and object reference is
tenant-authorized, S3 remains private, download access names the selected version, workers receive
narrow IAM permissions, and media plus transform parameters are validated rather than executed as
arbitrary commands.

“That gives one durable logical job despite lost responses, duplicate notifications and late
workers. The central invariant is that receiving a notification, owning an attempt and publishing
the official output are three separate permissions.”

*[I pause here. I do not volunteer every extension unless the interviewer asks.]*

### Optional interviewer-triggered extensions

These are continuations of the imagined dialogue, not features claimed by the opening design.

**Interviewer:** “How would you prevent one tenant or job type from taking the fleet?”

**Me:** “I would create resource classes for CPU, GPU type, memory and I/O, then add per-tenant
admission or concurrency limits and a fair scheduler within each class. I would monitor oldest-job
age by tenant, not only global queue depth. Exact weights and limits need product priorities and
measured runtimes; I would not infer them from the tenant count alone.”

**Interviewer:** “How would you roll this out without breaking existing clients?”

**Me:** “I would version the API and job schema compatibly, use expand-and-contract database
migrations, make workers tolerate the old and new record shapes during the transition, and canary
new pipeline versions. I would preserve idempotency semantics across versions so a retry does not
become a new job merely because deployment changed.”

**Interviewer:** “Now include loss of a Region.”

**Me:** “That is a separate contract. I would first ask for recovery-point and recovery-time
objectives. Then I would design cross-Region availability for job metadata, inputs, outputs and the
authority that assigns or accepts idempotency keys and attempt ownership. Copying objects alone is
insufficient if the failover Region cannot determine authoritative job state. I would document
which accepted writes can be lost at the chosen RPO, how DNS or clients fail over, and how split
brain is prevented. None of that is supplied by the single-Region diagram.”

**Interviewer:** “Can a retried ML pipeline reproduce identical output?”

**Me:** “I would pin and record the pipeline version, container or artifact digest, model version,
transform configuration and seed where applicable. That improves auditability and best-effort
reproducibility, but I would not promise bitwise identity when GPU kernels, codecs or external model
services are nondeterministic. The API promise remains one selected official output.”

**Interviewer:** “Who owns all these boundaries?”

**Me:** “I would assign explicit contracts: the API team owns tenant authorization and submission
semantics; the state/dispatch owner owns schema, outbox and reconciliation; the compute team owns
worker leases, resource classes and cooperative stopping; the storage owner owns private access,
version retention and cleanup. Shared dashboards and runbooks would connect their service-level
signals. Those are proposed ownership boundaries, not evidence that such teams already exist.”

### Teaching notes — not part of the spoken opener

- The answer asks about a completion target rather than silently treating 99.9% API availability
  as a promise that every video finishes within a deadline.
- The ten-minute mean is labeled as an added sizing assumption. `1,200` is concurrent executions,
  not an accelerator count; the burst calculation exposes the need for drain capacity.
- The normal path appears before failures. Each later mechanism repairs a named failure rather than
  arriving as an unexplained product list.
- SQS is not treated as the job system of record. PostgreSQL recovery continues after finite queue
  retention or dead-letter handling.
- Logical cancellation, physical compute stopping and queue acknowledgement are kept separate.
- Optional extensions are held until prompted, keeping the opening answer coherent and bounded.

</details>

The previous roughly 20/30/40-minute cues are optional pacing practice, not the teaching sequence.
For self-review, use 0 = cannot explain yet, 1 = needs substantial help, 2 = independently explains
and handles the bounded case, 3 = handles changed constraints and justifies choices. Score
requirements, coherent flow, failure correctness, trade-offs and communication separately. A polished
presentation does not compensate for losing accepted work or publishing a stale result.

## 13. Sources and limits

**Design status:** this is one recommended teaching architecture. Workload figures and retention
come from the exercise; example IDs, table layouts, lease intervals and capacity assumptions are
illustrative. SQL/Python snippets show mechanics and are not a complete tested deployment.

Primary-service references and the internal connection are recorded below. Source verification
supports individual service behavior; it does not prove this whole design is correct or production
ready. The source list is for follow-up, not an additional required reading wall.

**Checked November 10, 2026; high confidence in the documented product behavior.** The composed
architecture and policies are our design recommendations, not vendor promises. These links support
the corresponding sections; use them to answer a question when needed.

| Lesson topic | Primary reference |
|---|---|
| What SQS sends/receives and how deletion works | AWS [SendMessage](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html), [ReceiveMessage](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ReceiveMessage.html), [DeleteMessage](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_DeleteMessage.html), and [Boto3 examples](https://docs.aws.amazon.com/code-library/latest/ug/python_3_sqs_code_examples.html) |
| Duplicate messages, waiting and retry delivery | AWS [at-least-once delivery](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html), [visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html), [long polling](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html) |
| Database hosting, all-or-nothing saves and guarded writes | AWS [RDS PostgreSQL](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html); PostgreSQL [transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html), [unique constraints](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS), [UPDATE](https://www.postgresql.org/docs/current/sql-update.html), and [database time](https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-CURRENT) |
| Saving a notification with application state | Microsoft [transactional outbox pattern](https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos). The general pattern supports section 5; its Cosmos DB implementation is not our PostgreSQL implementation. |
| Identifying and protecting the exact output | AWS [S3 versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html), [retrieving versions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/RetrievingObjectVersions.html), [conditional writes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html) |
| Alternative database mechanics | AWS [DynamoDB conditional writes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html) and [transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html) |

The source audit, including additional FIFO, GPU execution and download-link checks, is at
`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/data/source-checks-2026-11-10.json`.
It records checked excerpts and limitations, including an unavailable AWS outbox URL; that failed
page is not treated as verified evidence. Check the selected PostgreSQL/RDS version before using
version-specific features in an implementation.

**Authentication follow-up, checked November 12, 2026:** high confidence in the documented
Cognito behavior; the membership-table design is our illustrative application policy. Primary
references: AWS [verifying JWTs](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html),
[access-token claims](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-the-access-token.html),
and [authorization-code/PKCE flow](https://docs.aws.amazon.com/cognito/latest/developerguide/authorization-endpoint.html).
A bounded reinspection of the internal endpoint source below did not establish its authentication
layer; this lesson does not assert that Adobe uses Cognito or the illustrated membership schema.
No authentication service was configured or tested for this follow-up.

**Receipt-handle follow-up, rechecked November 12, 2026:** AWS's
[DeleteMessage reference](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_DeleteMessage.html)
states that each receive returns a different handle and an old handle can report success without
deleting the message. The [visibility-timeout guide](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)
explains redelivery after expiry and extensions. High confidence in those documented mechanics;
the two-worker timeline is illustrative and was not executed against SQS.

**Signature mechanics, checked November 12, 2026:** the normative primary references are
[RFC 7515, section 5.2](https://www.rfc-editor.org/rfc/rfc7515.html#section-5.2) for signing-input
validation, [RFC 7518, section 3.3](https://www.rfc-editor.org/rfc/rfc7518.html#section-3.3) for RS256,
and RFC 8017 [key definitions](https://www.rfc-editor.org/rfc/rfc8017.html#section-3.2),
[signature operations](https://www.rfc-editor.org/rfc/rfc8017.html#section-5.2) and
[encoding checks](https://www.rfc-editor.org/rfc/rfc8017.html#section-8.2) for RSA. High confidence for these specified mechanics.
The in-memory Python demo verifies original/modified/wrong-key behavior; it is not a security audit
of a deployed authentication system. No real provider keys or tokens are used or stored.

**Connection to current Adobe code:** a read-only inspection on November 10 of
`/home/colligo/colligo/pylibs/colligo/fastapi/endpoints/v3_async_jobs.py` found status/cancel URLs,
retry guidance while running, a cancellation-pending transition and terminal outcomes. This connects
the lesson's customer-facing job lifecycle to a familiar production-code context. It does not
establish that Adobe uses this SQS/PostgreSQL/S3 architecture, or verify its worker/recovery behavior.
The audit records repository revision `afc6bae7401468ada329774517c6c6f362663d16` and file SHA-256
`48f60658e0fb5a7c26c74f3c419f68f367f7208ab74d9e6d06e17df03e1c6308`.
No internal implementation was reproduced here, and no runtime behavior was tested.
