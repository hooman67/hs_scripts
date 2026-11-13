# How HTTP requests and responses work

Saved: 2026-11-12. Internal implementation observations below reflect the inspected code and
clients, not a live audit of the deployed debug UI.

**A normal HTTP response does not require polling.** The server replies over the connection
your client already opened. **Polling is a separate application pattern** used when the first
response says, "Your job has started; check back later."

## Contents

- [How the server knows where to send the response](#1-how-the-server-knows-where-to-send-the-response)
- [What your client does while waiting](#2-what-your-client-does-while-waiting)
- [Why image-generation APIs often use polling](#3-why-image-generation-apis-often-use-polling)
- [What our HP/Colligo code actually does](#4-what-our-hpcolligo-code-actually-does)
- [Alternatives to polling](#5-alternatives-to-polling)
- [A response ending is not a connection closing](#6-a-response-ending-is-not-a-connection-closing)
- [Six small Python examples](#7-six-small-python-examples)
- [Local-demo and production boundaries](#8-local-demo-and-production-boundaries)
- [Example validation](#example-validation)
- [Documentation sources](#documentation-sources)
- [Code references](#code-references)

## 1. How the server knows where to send the response

For a typical HTTPS request, the sequence is:

```text
Your browser                         Server
     |                                  |
     +-- Establish connection --------->|
     +-- Send HTTP request ------------>|
     |                                  | Process request
     |<--------- HTTP response ---------+
```

Usually, the browser first resolves the server's hostname to an IP address, establishes a TCP
connection, and negotiates TLS encryption. It might also reuse an existing connection.
HTTP/3 uses QUIC instead of TCP, but the same basic request/response idea applies.

A connection has two ends, identified by IP addresses and ports. Your computer has a
**socket** -- an operating-system interface for reading and writing that connection -- and
so does the server.

**The server does not need your email address, a callback URL, or another connection to your
computer.** It writes the response to the connection associated with your request. Firewalls
and routers generally recognize this as return traffic on an established connection.

If there is a gateway or reverse proxy, the path can look like:

```text
Browser <-> Gateway <-> Application server
```

There are separate connections along that path. Each component forwards the response back
toward the requester.

GET versus POST does **not** change this delivery mechanism. They express different request
semantics, not different ways of receiving responses.

## 2. What your client does while waiting

Suppose browser code does this:

```javascript
const response = await fetch("/api/example");
const data = await response.json();
```

This is **not** secretly sending repeated requests asking whether the response is ready.

The browser's networking machinery waits for incoming data. The operating system notifies it
when data is available, and the browser resumes the appropriate JavaScript work. Other page
activity can continue meanwhile.

One subtlety: `fetch()` generally resolves when the response headers arrive;
`response.json()` waits for the body and parses it.

Also, **finishing a response does not necessarily close the connection**. HTTP has ways to
identify the end of a response, allowing the connection to be reused. With HTTP/2, multiple
requests can share a connection using separate streams.

**JavaScript `async`/`await` is therefore not the same thing as an asynchronous background-job
API.** You can use `await` for either.

## 3. Why image-generation APIs often use polling

Generating an image might take minutes. Instead of keeping the original request waiting that
whole time, an API can immediately return the following information (illustrative, not a
literal response format):

```text
HTTP 202 Accepted
Job ID: abc123
Result URL: /some/result/abc123
```

That is a **complete response to the original POST**, but it is not the generated image.

The interaction then becomes:

```text
Client                       API                         Worker
  |                           |                            |
  +-- POST generation ------->|-- Start background job --->|
  |<-- 202 + job/result URL ---+                            |
  |                           |                            | Working
  +-- GET result URL -------->|                            |
  |<-- In progress -----------+                            |
  |                           |                            |
  | Wait a few seconds        |                            |
  +-- GET result URL -------->|                            |
  |<-- In progress -----------+                            |
  |                           |<-- Store finished result ---+
  +-- GET result URL -------->|
  |<-- Final result/image URL -+
  +-- GET image URL -------------------------------------> Storage
  |<-- Image bytes ----------------------------------------+
```

**Here, the client is polling.** Every poll is another ordinary HTTP request with its own
response.

The worker does not need someone to poll to keep working. It finishes and makes the result
available. The client discovers completion on its next poll.

Once the original POST's response is complete, the server cannot simply append another
response to that same request later -- even if the underlying connection remains open.

## 4. What our HP/Colligo code actually does

Both the Colligo HP app and our generation clients were inspected:

| Component | Verified behavior |
|---|---|
| Colligo HP generation endpoint | Submits the pipeline with `mode="background"` and returns a background-job response. |
| Colligo smoke client | Follows the returned result link and polls, waiting **2 seconds between unfinished checks**. |
| Our earlier HTTP-based HP evaluation runner | Submits the request, follows its result link, and polls with a **5-second delay between checks**. |
| Completed Colligo image result | Contains image references; the client subsequently downloads the image bytes from a presigned storage URL. |

The backend's `on_complete` and `on_store_result` callbacks are **internal software callbacks**.
They are not the backend calling your browser. The storage callback uploads the images and
constructs the result that a later result request retrieves.

**For the debug UI specifically:** the backend contract and Python callers were verified,
not the deployed frontend's JavaScript. A UI can implement this same submit -> poll ->
download sequence, but that particular UI's mechanism or polling interval cannot be
certified from the backend alone.

There is also an important distinction in our recent work: **the latest V15.8 batch ran the
native Python pipeline directly, not through the debug UI.** Its model SDK calls waited for
their ordinary HTTP responses; the image response contained base64-encoded image data, which
the pipeline decoded. So not every experiment used the same outer job/polling layer.

## 5. Alternatives to polling

| Mechanism | How results arrive |
|---|---|
| **One delayed response** | Server keeps the original request open until work finishes. No status polling is necessary. |
| **Polling** | Client repeatedly asks for status/result. Each response finishes independently. |
| **Long polling** | Client asks for updates; server holds that request until an update or timeout, responds, and the client asks again. |
| **Streaming / SSE** | One HTTP response stays open and delivers incremental chunks or events. SSE is server-to-client; ordinary HTTP can stream too. |
| **WebSocket** | A persistent bidirectional channel carries messages independently of ordinary request/response pairs. |
| **Webhook** | You explicitly provide a reachable callback URL. The backend later makes a **new HTTP request** to that URL -- usually another server, not your browser. |

A streaming response does not have to contain partial images: it could send progress events
and finally an image URL.

Two practical consequences: an accepted background job generally survives closing the
browser tab unless explicitly cancelled; and a client timeout does **not** necessarily mean
the backend stopped working.

**The key distinction:** receiving bytes for an existing request is normal network
communication. Repeatedly issuing new requests to discover whether a separate job has
finished is polling.

## 6. A response ending is not a connection closing

**No: TCP does not automatically close just because an HTTP response finished. Polling does
not inherently create and close a connection for every check.**

Keep these three layers separate:

| Layer | What it is | When it ends |
|---|---|---|
| TCP connection | A two-way transport for bytes between two endpoints. | When an endpoint closes it, a timeout expires, or the network fails. |
| HTTP request/response | One application exchange carried over the transport. | When HTTP's message-framing rules mark the response complete. |
| Background job | Application work identified by a job ID. | When the application completes, fails, or cancels that work. |

For HTTP/1.1, a connection can normally carry multiple exchanges sequentially:

```text
TCP:  OPEN ================================================== CLOSE
HTTP:       [GET -> response]   [GET -> response]   [GET -> response]
             poll 1             poll 2             poll 3
```

The client's connection pool keeps reusable connections available. In Python,
`httpx.Client()` or `requests.Session()` provides this reuse. By contrast, independent
top-level `httpx.get(...)` calls do not share a persistent client pool.

Reuse is possible, not guaranteed: a server, proxy, client, or idle timeout may close a
connection, requiring a new one on the next poll. All of this is separate from the
application's decision to poll.

With HTTP/2, multiple independent request/response **streams** can share one TCP connection
concurrently. Finishing a stream does not close that connection. HTTP/3 uses QUIC rather
than TCP; do not describe every modern HTTP connection as TCP.

### How does the server know a response is finished?

It does not always wait for the connection to close. For example:

- HTTP/1.1 can advertise a `Content-Length`, so the receiver knows how many body bytes to read.
- HTTP/1.1 chunked transfer encoding has an explicit final chunk.
- HTTP/2 marks the end of an individual stream.

Some responses are delimited by closing the connection, but that is not required for every
response. HTTP message boundaries and network packet boundaries are also different things.

### How does a server hold a delayed response open?

**Usually, by not completing the response yet.** The server framework retains the request
context and its connection while the handler waits. No special "keep this request open"
packet needs to be sent every second.

```text
Client                                 Server
  |------ request ---------------------->|
  |                                      | await something
  |       no HTTP response yet           | handle other requests meanwhile
  |                                      | something finishes
  |<----- response ----------------------|
  |       TCP may remain reusable        |
```

In the examples, `await asyncio.sleep(...)` simulates work. The asynchronous handler pauses
without spinning in a loop or blocking the event-loop thread. In long polling, an
`asyncio.Event` provides an in-process notification: another task sets it, waking the waiter.
The TCP socket and some request/task state still consume resources; "waiting efficiently"
does not mean "waiting for free."

The server cannot guarantee unlimited waiting. Client read timeouts, reverse-proxy timeouts,
server settings, disconnects, and restarts can interrupt an active request. An HTTP
**keep-alive idle timeout** usually concerns gaps between requests; increasing it alone does
not solve an active-request timeout. TCP keepalive probes, HTTP connection reuse, and
application heartbeat events are different mechanisms.

**Delayed response versus long polling:** both can leave a request waiting. With a delayed
response, that request typically initiates work and waits for its result. With long polling,
the request usually observes an existing job/event source, waits for an update or a bounded
timeout, returns, and is repeated if necessary.

## 7. Six small Python examples

These are deliberately small, local demonstrations. A pretend computation returns `42`
instead of generating an image. The examples share one server so imports and setup do not
hide the important differences.

The complete runnable server is saved at:

`/home/colligo/hs_scripts/claude/dev_research/learning/first-pass/http_demo.py`

It uses Python 3.10+ and the `fastapi`, `uvicorn`, `httpx`, and `websockets` packages. If
needed, install them in a dedicated virtual environment rather than changing a shared
system environment. Start one worker, without reload, in a terminal:

```bash
python -m uvicorn http_demo:app \
  --app-dir /home/colligo/hs_scripts/claude/dev_research/learning/first-pass \
  --host 127.0.0.1 --port 8000
```

Leave that terminal running while executing a client snippet in another terminal. If a
port is already occupied, use an unused port and update the corresponding client URL;
do not stop another user's process.

**Shared server setup:**

```python
import asyncio
import json
from uuid import uuid4

import httpx
from fastapi import BackgroundTasks, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

app = FastAPI()
receiver = FastAPI()
jobs = {}
CALLBACK_URL = "http://127.0.0.1:8001/callback"
```

### 7.1 One delayed response

**Shape:** one request, a wait, one completed response. No job ID and no repeated status
requests. Suitable when the work fits comfortably within the infrastructure's timeouts.

**Server:**

```python
@app.get("/delayed")
async def delayed():
    await asyncio.sleep(5)
    return {"result": 42}
```

**Client:**

```python
import httpx

response = httpx.get("http://127.0.0.1:8000/delayed", timeout=10)
response.raise_for_status()
print(response.json())
```

The client waits about five seconds. The framework sends the JSON response when the
handler returns. Neither side is issuing status requests.

This is not a reason to run expensive CPU/GPU work directly on the event-loop thread:
real blocking work needs a suitable worker, executor, or asynchronous service client.
Adding `async def` does not automatically make blocking computation nonblocking.

### 7.2 Polling

**Shape:** submit once, get a job ID, then repeatedly ask for a snapshot.

`BackgroundTasks` schedules the demo work after the submission response has been sent.
It is a convenience for this one-process example, not a durable job queue.

**Server:**

```python
async def finish(job_id):
    await asyncio.sleep(5)
    jobs[job_id]["result"] = 42
    jobs[job_id]["ready"].set()


@app.post("/jobs", status_code=202)
async def start_job(tasks: BackgroundTasks):
    job_id = uuid4().hex
    jobs[job_id] = {"result": None, "ready": asyncio.Event()}
    tasks.add_task(finish, job_id)
    return {"job_id": job_id}


@app.get("/jobs/{job_id}")
async def status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(404, "Unknown job")
    job = jobs[job_id]
    return {"done": job["ready"].is_set(), "result": job["result"]}
```

**Client:**

```python
import time
import httpx

with httpx.Client(base_url="http://127.0.0.1:8000", timeout=10) as client:
    submitted = client.post("/jobs")
    submitted.raise_for_status()
    job_id = submitted.json()["job_id"]
    while True:
        response = client.get(f"/jobs/{job_id}")
        response.raise_for_status()
        status = response.json()
        print(status)
        if status["done"]:
            break
        time.sleep(1)
```

Each GET receives its response immediately. The same `Client` can reuse the same TCP
connection across submission and polls. When the client exits the `with` block, it closes
its connection pool.

Trade-off: checking more frequently reduces detection delay but adds requests. Production
clients also need an overall deadline and an appropriate polling/backoff policy.

### 7.3 Long polling

**Shape:** submit once, then ask, "Wait until this job finishes, but no longer than 20
seconds." Reuse the polling example's job creation and worker.

**Server:**

```python
@app.get("/jobs/{job_id}/wait")
async def wait_for_result(job_id: str):
    if job_id not in jobs:
        raise HTTPException(404, "Unknown job")
    job = jobs[job_id]
    try:
        await asyncio.wait_for(job["ready"].wait(), timeout=20)
    except asyncio.TimeoutError:
        pass
    return {"done": job["ready"].is_set(), "result": job["result"]}
```

**Client:**

```python
import httpx

with httpx.Client(base_url="http://127.0.0.1:8000", timeout=25) as client:
    submitted = client.post("/jobs")
    submitted.raise_for_status()
    job_id = submitted.json()["job_id"]
    while True:
        response = client.get(f"/jobs/{job_id}/wait")
        response.raise_for_status()
        status = response.json()
        print(status)
        if status["done"]:
            break
```

The server is not repeatedly checking the dictionary in a sleep loop. The worker's
`ready.set()` wakes the waiting handler. If the event was already set, waiting returns
immediately, so a completion between requests is not lost.

For the five-second demo job, normally one waiting GET is enough. If the job took a minute,
the client could receive unfinished snapshots after bounded waits and issue another GET.
The 25-second client timeout is deliberately longer than the server's 20-second wait;
intermediaries must also allow that wait.

### 7.4 Streaming / server-sent events (SSE)

**Shape:** one HTTP request and one response body that arrives incrementally.

```text
Client                       Server
  |------ GET /events ------->|
  |<----- response headers ---|
  |<----- progress: 25 -------|
  |<----- progress: 50 -------|  Same response, not new responses
  |<----- result: 42 ---------|
  |<----- response ends ------|
```

**Streaming** is the general ability to consume part of a response before the whole body
exists. **SSE** is a standard text event format carried inside such a response, using the
`text/event-stream` content type. Each event ends with a blank line:

```text
data: {"percent": 25}

data: {"percent": 50}

data: {"percent": 100, "result": 42}

```

SSE is one-way at the application-event level: server -> client. The client can still send
a separate ordinary POST, for example to cancel a job. TCP traffic is still bidirectional
underneath; "one-way" does not mean that TCP acknowledgements disappear.

**Server:**

```python
@app.get("/events")
async def events():
    async def stream():
        for percent in (25, 50, 100):
            await asyncio.sleep(1)
            data = {"percent": percent}
            if percent == 100:
                data["result"] = 42
            yield f"data: {json.dumps(data)}\n\n"

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"},
    )
```

**Client:**

```python
import json
import httpx

with httpx.stream("GET", "http://127.0.0.1:8000/events", timeout=10) as response:
    response.raise_for_status()
    for line in response.iter_lines():
        if line.startswith("data: "):
            print(json.loads(line[6:]))
```

The client prints three updates about one second apart, instead of waiting for all updates
to exist. `yield` supplies another piece of the response body; it does not start another
HTTP response. `iter_lines()` handles lines that cross network-read boundaries.

This tiny parser handles our single-line JSON events, not every SSE feature. Browser
`EventSource` handles SSE event parsing and normally reconnects automatically. Reliable
resume additionally needs event IDs and server-side replay; reconnection alone does not
guarantee that missed events are recovered.

Good fit: generation progress, logs, notifications, and token-by-token model output when
the application mainly needs server-to-client updates. Not every token stream is SSE;
other response-body formats are possible.

Operational caveats: proxies may buffer chunks unless configured for streaming; idle
timeouts may require heartbeat comments such as `: ping\n\n`. Receiving a heartbeat proves
connection activity, not that generation is making progress. A slow client also requires
bounded buffering or a backpressure/disconnection policy.

### 7.5 WebSocket

**Shape:** establish a persistent message channel, then exchange messages in either
direction without a new HTTP request for each message.

```text
Client                       Server
  |------ connect /ws ------->|
  |------ "start" ----------->|
  |<----- progress: 25 -------|
  |<----- progress: 50 -------|
  |<----- result: 42 ---------|
  |------ close channel -----|
```

A common HTTP/1.1 setup starts with an HTTP handshake and a `101 Switching Protocols`
response; subsequent data uses WebSocket message framing, not independent HTTP responses.
Other HTTP versions can establish WebSockets differently. `ws://` is unencrypted;
`wss://` is the encrypted form used for production.

Unlike SSE, both sides can send application messages on the same channel at any time.
For example, an interactive application could send commands or cancellation messages
while receiving progress. Doing that concurrently requires corresponding server logic;
this minimal demo accepts one start message and sends three updates.

**Server:**

```python
@app.websocket("/ws")
async def websocket(ws: WebSocket):
    await ws.accept()
    try:
        await ws.receive_text()
        for percent in (25, 50, 100):
            await asyncio.sleep(1)
            data = {"percent": percent}
            if percent == 100:
                data["result"] = 42
            await ws.send_json(data)
        await ws.close()
    except WebSocketDisconnect:
        pass
```

**Client:**

```python
import json
from websockets.sync.client import connect

with connect("ws://127.0.0.1:8000/ws") as socket:
    socket.send("start")
    for _ in range(3):
        print(json.loads(socket.recv(timeout=10)))
```

Good fit: chat, collaborative editing, interactive sessions, or many commands and updates
in both directions. WebSocket is not automatically more reliable or necessary merely
because a job runs for a long time. Authentication, reconnection, job resubscription,
missed-message replay, and slow-client handling remain application responsibilities.

### 7.6 Webhook

**Shape:** the generation server becomes an HTTP client and calls another server later.
There is no original client connection that has to stay open until completion.

```text
Your caller                 Generation service          Your receiver server
    |------ submit job -------->|
    |<----- 202 Accepted -------|
    |                           | Work finishes
    |                           |------ POST callback --------->|
    |                           |<----- acknowledgement --------|
```

The callback URL must be configured or supplied explicitly. It is not inferred from the
original connection's client address. Your laptop/browser usually is not a publicly
reachable HTTP server, so webhooks commonly target your backend.

In this demo, `app` is the generation service and `receiver` is a second application.
Start the receiver in a second terminal:

```bash
python -m uvicorn http_demo:receiver \
  --app-dir /home/colligo/hs_scripts/claude/dev_research/learning/first-pass \
  --host 127.0.0.1 --port 8001
```

**Server:**

```python
@receiver.post("/callback")
async def callback(payload: dict):
    print("Completion delivered to receiver:", payload, flush=True)
    return {"received": True}


async def finish_and_notify(job_id):
    await asyncio.sleep(3)
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            CALLBACK_URL, json={"job_id": job_id, "result": 42}
        )
        response.raise_for_status()


@app.post("/webhook-job", status_code=202)
async def start_webhook_job(tasks: BackgroundTasks):
    job_id = uuid4().hex
    tasks.add_task(finish_and_notify, job_id)
    return {"job_id": job_id, "accepted": True}
```

**Client:**

```python
import httpx

response = httpx.post("http://127.0.0.1:8000/webhook-job", timeout=10)
response.raise_for_status()
print(response.json())
```

The submitting client immediately prints acceptance and exits. Three seconds later, the
**receiver's terminal** prints the result. The original client does not suddenly receive
another response. If a browser must display that result, its backend still needs a way
to notify it, such as polling, SSE, or WebSocket.

Good fit: service-to-service completion notifications, payment events, and integrations
where the receiver should not maintain a connection for the entire job.

Real deliveries can fail or arrive more than once. Production needs durable delivery
records, retry/backoff, and event IDs so the receiver can safely recognize duplicates.
This demo makes one delivery attempt and deliberately does not implement that machinery.

## 8. Local-demo and production boundaries

**These examples are teaching implementations, not production-ready generation services.**

- Bind only to `127.0.0.1`. The unauthenticated demo has no authorization, quotas, or
  persistence; do not expose it on a shared/public network.
- The polling dictionary and `asyncio.Event` objects live in one process. Do not start
  multiple workers and expect shared jobs. Restarts lose state; a real durable queue and
  database solve a different problem than HTTP response delivery.
- The streaming and WebSocket examples simulate work per connection. Real costly
  generation should normally be submitted once and observed using a job ID; reconnecting
  an observer must not silently regenerate an image.
- For production, use HTTPS/WSS, authenticate callers, authorize access to each job,
  bound connection/message/buffer sizes, and configure timeouts and disconnect handling.
  Browser WebSocket servers also need an appropriate origin-validation policy.
- Presigned output URLs are bearer-like access: possession can grant temporary access.
  Avoid putting them into public logs or messages.
- The webhook uses a fixed local callback address. A production service must not blindly
  fetch arbitrary user-provided callback URLs: that could let an attacker reach internal
  services (server-side request forgery, or SSRF). Validate/allowlist destinations and
  control outbound networking. Authenticate webhook deliveries, commonly with a signed
  payload and timestamp, and reject replays.

The most useful selection rule is: **use ordinary requests for individual exchanges,
polling for simple durable-job observation, SSE for mostly one-way live updates,
WebSocket for genuinely bidirectional sessions, and webhooks to notify another server.**
These can be combined; they are not mutually exclusive system architectures.

## Example validation

**VERIFIED, 2026-11-12, local teaching implementation only:** all six exact documented
client snippets were executed against the runnable server over real loopback connections.
The server snippets were also checked against the runnable file's Python syntax tree to
prevent documentation/code drift.

The checks confirmed:

- The delayed response took about five seconds; polling returned unfinished and finished
  snapshots and reused one HTTP/1.1 TCP connection.
- Long polling returned on completion without repeated status GETs. An actual 20-second
  unfinished wait timed out normally, while the server answered another request.
  Already-completed jobs returned immediately; unknown jobs returned 404.
- SSE and WebSocket clients received three distinct incremental updates, ending with
  result `42`, rather than one buffered final batch.
- Webhook submission returned before completion; a separate receiver got the later POST
  with the matching job ID and result. The submitting client did not poll.

Python 3.10, FastAPI 0.115.2, Uvicorn 0.32.0, HTTPX 0.28.1, and websockets 16.1.1 were used.
Correctness lint passed. Both temporary listeners were closed. This does not certify
production durability, TLS, authentication, proxy behavior, HTTP/2, or the live debug UI.

## Documentation sources

Checked 2026-11-12. These support the general mechanisms; the internal references below
support only the scoped implementation observations.

- MDN, HTTP/1.x connection management (persistent connections and reuse):
  https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Connection_management_in_HTTP_1.x
- HTTPX, clients (connection pooling versus top-level one-off requests):
  https://www.python-httpx.org/advanced/clients/
- Python, asyncio synchronization primitives (event notification):
  https://docs.python.org/3/library/asyncio-sync.html#event
- FastAPI, background tasks (execution after a response and process-local limitations):
  https://fastapi.tiangolo.com/tutorial/background-tasks/
- Starlette, responses (streaming an iterator as one response body):
  https://starlette.dev/responses/#streamingresponse
- MDN, server-sent events (event format, reconnection, and heartbeat comments):
  https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
- websockets, quick examples (send/receive on a persistent channel):
  https://websockets.readthedocs.io/en/stable/intro/examples.html

## Code references

These are internal source references inspected on 2026-11-12. They are not claims of
live-deployment verification.

- Colligo submission/storage:
  `/home/colligo/colligo-pr36039-astra-r2/managed_services/services/firefly/foundry/standalone_apps/hp_image/actors/webapp.py:185-191,303-418`
- Colligo smoke client's polling and image download:
  `/home/colligo/colligo-pr36039-astra-r2/managed_services/services/firefly/foundry/standalone_apps/hp_image/scripts/smoke/worker_e2e.py:339-455`
- Our HTTP polling runner:
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_prompt_digital_twin_eval_v1/generation/run_generation.py:376-411`
- Latest native SDK recording:
  `/home/colligo/hs_scripts/claude/hp_lifestyle_pipeline/eval_sets/hp_lifestyle_v6_5_training_full160_pr4619_20261112/generate.py:60-109`
