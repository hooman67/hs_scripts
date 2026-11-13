### gRPC: the 60‑second overview
- What it is: A high‑performance RPC framework. You define services and messages once (Protocol Buffers), then generate client/server code.
- Transport: HTTP/2 (multiplexing, flow control). Supports deadlines/timeouts, status codes, and streaming.
- In this repo:
  - Protos live in `src/glimmer_queue/protos/glimmer_queue.proto`.
  - Codegen outputs `glimmer_queue_pb2.py` (messages) and `glimmer_queue_pb2_grpc.py` (service stubs).
  - Server implements `GlimmerQueueServicer` in `server.py`. Clients use a generated `GlimmerQueueStub` (see `client.py`).

### “RPC surface (protos)” explained
- The “surface” is the public API defined in the proto: service methods and message shapes. Here:
  - `Handshake(HandshakeRequest{client_identifier}) -> HandshakeResponse`
  - `QueryJob({}) -> {row_group_size}`
  - `DequeueShards({num_shards?}) -> {is_empty, shards[{row_group,min_ix,max_ix,alreadySucceded?}]}`
  - `UpdateShard({row_group, succeeded, failed, all_succeeded}) -> {state}`
  - `QueryShard({row_group, include_sets}) -> {row_group,min_ix,max_ix,state,succeeded?,failed?}`
- Why it matters: this is the contract workers rely on; the server and clients are generated from it, so types stay in sync.


## give me more details
- Proto definition: You write `src/glimmer_queue/protos/glimmer_queue.proto` declaring the service (`service GlimmerQueue`) and the RPC methods/messages. This is the single source of truth for the API.

- Code generation:
  - `glimmer_queue_pb2.py`: Python classes for messages (e.g., `HandshakeRequest`, `UpdateShardResponse`).
  - `glimmer_queue_pb2_grpc.py`: gRPC glue:
    - `class GlimmerQueueServicer`: abstract base specifying the RPC methods to implement.
    - `class GlimmerQueueStub`: client-side proxy with methods to call the RPCs.
    - `add_GlimmerQueueServicer_to_server(servicer, server)`: registers method handlers on a server.

- Your implementation:
  - `GlimmerQueueService` in `src/glimmer_queue/server.py` subclasses `GlimmerQueueServicer` and implements the RPCs (e.g., `Handshake`, `DequeueShards`, `UpdateShard`, `QueryShard`, `QueryJob`).
  - This is the concrete business logic for each RPC.

- Server wiring:
  - In `start_server.py`, you create a gRPC server and an instance of your service, then call:
    - `glimmer_queue_pb2_grpc.add_GlimmerQueueServicer_to_server(glimmer_queue_service, server)`
  - That call binds each proto-declared RPC name to the corresponding method on your `GlimmerQueueService` instance so incoming requests are dispatched to your code.

- Client usage (for context):
  - Create a channel and stub (e.g., `stub = GlimmerQueueStub(channel)`), then call `stub.UpdateShard(...)`, etc. The stub methods serialize the request messages and handle HTTP/2 calls under the hood.

- Why this pattern:
  - Proto defines the contract.
  - Codegen ensures client/server stay in sync and handles serialization.
  - You only write the service implementation and registration; the framework handles transport, threading, and dispatch.


  ## Give me more info about channels
  - A gRPC “channel” is a client-side HTTP/2 connection to your server. You create it with gRPC, then pass it to the generated stub.

Examples:
- Insecure (local/dev):
```python
import grpc
from glimmer_queue.protos import glimmer_queue_pb2_grpc

addr = "localhost:50051"
with grpc.insecure_channel(addr) as channel:
  stub = glimmer_queue_pb2_grpc.GlimmerQueueStub(channel)
  resp = stub.Handshake(HandshakeRequest(client_identifier="my-client"))
```

- Secure (TLS):
```python
import grpc, ssl
from glimmer_queue.protos import glimmer_queue_pb2_grpc

addr = "my-host:50051"
creds = grpc.ssl_channel_credentials()  # or load certs via ssl.SSLContext
channel = grpc.secure_channel(addr, creds)
stub = glimmer_queue_pb2_grpc.GlimmerQueueStub(channel)
```

- With options (e.g., larger messages, keepalive):
```python
channel = grpc.insecure_channel(
  "localhost:50051",
  options=[
    ("grpc.max_receive_message_length", 50 * 1024 * 1024),
    ("grpc.keepalive_time_ms", 30000),
  ],
)
```

In this repo:
- `glimmer_queue.client.generate_stub(addr)` does:
```python
channel = grpc.insecure_channel(addr)
return glimmer_queue_pb2_grpc.GlimmerQueueStub(channel)
```
So you normally just pass the server address like `"localhost:50051"`.


## Why do we pass a threadpool to the gRPCserver:
- Yes, that ThreadPoolExecutor is the gRPC server’s worker pool. Each incoming RPC is scheduled onto a worker thread to run the handler (e.g., Handshake, DequeueShards, UpdateShard, QueryShard). More workers = more concurrent RPCs can be processed; too few = requests queue; too many = contention.

- What the workers do here:
  - Run your handler code in `GlimmerQueueService`.
  - For UpdateShard/QueryShard they open a short‑lived SQLAlchemy Session and hit the DB (SELECT … FOR UPDATE SKIP LOCKED, updates).
  - For DequeueShards they call into the in‑process `GlimmerClient` (which itself has threads and DB access via `TaskQueue`).
  - Handshake/QueryJob are cheap but still occupy a worker briefly.

- Why increase max_workers 64 → 128:
  - To raise concurrency headroom for bursts of UpdateShard/Handshake/DequeueShards from many clients (reduces queueing latency).
  - Handlers are largely I/O‑bound (DB, gRPC I/O), so extra threads can progress while others wait on the DB/network (GIL isn’t a blocker here).
  - It better aligns with DB pool capacity so workers don’t stall waiting on a connection:
    - Defaults: `GLIMMER_DB_POOL_SIZE=64`, `GLIMMER_DB_MAX_OVERFLOW=64` → up to ~128 concurrent DB connections.
    - Server handlers open a per‑request Session; sizing workers to ≤ pool_size+max_overflow avoids connection starvation.
  - Matches test realities (e.g., 100 concurrent Handshakes) and many clients flushing UpdateShard in parallel.

- Tradeoffs to watch:
  - If workers >> DB pool, threads will block on connections; latency rises.
  - If workers are too high, you can increase context switching and amplify DB lock contention.
  - Tune together: max_workers, DB pool (GLIMMER_DB_POOL_SIZE/GLIMMER_DB_MAX_OVERFLOW), and gRPC client concurrency.


### Roaring bitmaps (what/why/how)
- What: A compressed set representation for non‑negative integers (we use `pyroaring.BitMap`). Efficient for both sparse and dense sets.
- Why:
  - Very fast unions/intersections and cardinalities (used to merge progress and check completion).
  - Compact memory and small serialized payloads (we put them into protobuf `bytes` fields).
- How we use them:
  - Per shard, workers accumulate succeeded and failed row IDs in two bitmaps.
  - On flush, we serialize them into `UpdateShardRequest.succeeded/failed` (bytes).
  - Server deserializes and calls `task.ack(...)` / `task.nack(...)`, which merge with DB bitmaps.
  - Completion is detected by comparing bitmap cardinality vs shard size; errors roll into `CompletedWithFailures`.