# Inference Application Public Endpoints

Inference applications support having public HTTP endpoints. Public HTTP endpoints are useful for making services that are JS friendly and have backward compatibility promises. We briefly touched upon them in the [end to end worker tutorial](/models/colligo/models/template/t1/aidoc/index.md#registering-the-worker-with-inference-platform). Whereas, the [inference SDK](/pylibs/colligo/sdk/aidoc/index.md) can be used to programmatically call workers.

## Sync vs Async Endpoints

Endpoints can be configured to operate in either **synchronous** or **asynchronous** mode:

### Synchronous Endpoints

Synchronous endpoints return results directly in the HTTP response. They are best suited for:

- Fast inference tasks (completing in under 60 seconds)
- Real-time interactions requiring immediate responses
- Simple request-response patterns

**Important Limitations:**

```{warning}
**Gateway Timeout**: Synchronous endpoints have a **60-second gateway timeout** enforced by the infrastructure. If your worker takes longer than 60 seconds to process a request, the gateway will return a `504 Gateway Timeout` error to the client, even if the worker continues processing.

For tasks that may take longer than 60 seconds, use async endpoints instead.
```

**Configuration:**

```python
PublicEndpoint(
    path="/v1/image/quick-generate",
    request_type=HttpRequest,
    response_type=HttpResponse,
    is_async=False,  # Synchronous endpoint (default)
    ...
)
```

Timeout for async endpoint is controlled by request timeout.
It never make sense to set it longer than 60s in Ethos since the gateway will close the connection and you will get a gateway timeout error.

``` {colligo_docstring} colligo.base.config:RequestConfig
```

### Asynchronous Endpoints

Asynchronous endpoints immediately (see details below) return URLs that allow clients to poll for results and cancel the job.
They are designed for:

- Long-running tasks (minutes to hours)
- Tasks with unpredictable completion times
- Batch processing and background jobs

**How it works:**

1. Client submits a request → receives URLs immediately
2. Client polls the status endpoint
3. When complete, client retrieves the result

**Configuration:**

```python
PublicEndpoint(
    path="/v3/video/generate-async",
    request_type=HttpRequest,
    response_type=HttpResponse,
    is_async=True,  # Asynchronous endpoint
    initial_session_ttl_s=600 # Async job timeout
    ...
)
```

Request timeout for individual async endpoint HTTP requests is controlled by request timeout the same
it is for sync endpoint.

Due to implementation details request validation for non-resilient async endpoint still
needs an available pipeline worker, so the links are not returned **immediately** and you
still can encounter a gateway timeout if there is no worker available for 60s.

The timeout of async job is by default controlled by `initial_session_ttl_s`.
If not defined on an endpoint level it is taken form the worker level as
provided in `build.deploy_worker`.

```{note} By default async endpoint is not resilient - if job fails it is not retried.
You need to do an extra step for retries to work.
Resilient Async gives you more control over timeouts as well.
See the [Resilient Async Pipeline documentation](/aidoc/inference-platform/framework/resilient-async-pipeline.md) for more details.
```

```{hint} We support two flavors of async URLs, v2 and v3.
See [Async Job APIs](/aidoc/inference-platform/framework/http_api.md#async-job-apis)
The version is inferred from the path version. e.g. `/v1/...` or `/v2/...` will have v2 links, `/v3/...` will have v3 links.
```

---

## Building blocks

Each endpoint is registered with a pipeline worker. An HTTP endpoint consists of the following building blocks:

- Request and response types.
- Functions that convert the pipeline request and response types to the HTTP request and response types. It is possible (mainly for debugging) to use the same types for both pipeline and HTTP; in that case you can skip the adapters.
- A [`PublicEndpoint`](/aidoc/inference-platform/framework/api.md#making-public-http-apis) object that glues everything together; plus additional information.
- Pass the `PublicEndpoint` to the [`build.deploy_worker(...)`](/aidoc/inference-platform/framework/api.md#making-public-http-apis) call when registering the worker to hook up the endpoint to your worker.

Here is an example:

```{code-block} python
:caption: A file among the worker API file (e.g. types.py)

class HttpRequest(pydantic.BaseModel):
    prompt: str


class HttpResponse(pydantic.BaseModel):
    # This is the format that we usually use for our public facing APIs; due to
    # contracts we have had over time with clients.
    image: PublicBinary
```

```{code-block} python
:caption: A file among internals of the worker (no need to be member of types, to keep deps of types light)

def parse_request(request: HttpRequest) -> PipelineRequest:
    # convert HttpRequest to PipelineRequest


def parse_response(response: PipelineResponse) -> HttpResponse:
    # convert PipelineResponse to HttpResponse
    
```

```{code-block} python
:caption: build.py file for the pipeline

ENDPOINT = PublicEndpoint(
    path="/v1/image/generate",
    to_request = parse_request,
    from_response = parse_response,
    request_type=HttpRequest,
    response_type=HttpResponse,
    ...
)

build.deploy_worker(
    ...
    endpoints=[ENDPOINT],
    ...
)
```

## Dealing with binaries in public APIs

If you are making some APIs to experiment with, you can just use the `EncodedImage`, `Tensor`, ... types in the API, i.e. anything inheriting from [`Binary`](/aidoc/inference-platform/framework/api.md#defining-a-worker).

However, if you want to make an API to ship to users, by convention we use the [`PublicBinary`](/aidoc/inference-platform/framework/api.md#making-public-http-apis) type to represent binaries (images, video, 3D  meshes, ...). It supports accepting and returning ACP file ids, pre-signed URLs, multi-part form, and objects in our S3 storage.

When dealing with multi-part you don't need to directly deal with request parts, and you just need to set or read `public_binary._source` and `public_binary._mime_type` fields.

For other formats, you need to either upload or fetch the data from storage. Some utilities are provided for this purpose and are listed [here](/aidoc/inference-platform/framework/api.md#making-public-http-apis).

## Enabling multi-part request or response encoding

The inference platform by default supports multi-part request and response encodings.

For request encoding, if multi-part is used, by default we inject the mime type and source fields in the binary classes.

For response types, the encoding is chosen via the `ACCEPT` header. The default response encoding is the first entry in `allowed_response_encodings`.

The supported encodings can be restricted via the `allowed_request_encodings` and `allowed_response_encodings` fields in [`PublicEndpoint`](/aidoc/inference-platform/framework/api.md#making-public-http-apis).

We don't require services to restrict the encoding types. That being said in certain cases, it might be advisable to do so. For example:

- If payload sizes are more than ~`15 MB`, and the request rate is high, it is safer to not allow multi-part encoding so the huge traffic goes through ACP or S3 rather than our service's gateway.
- If the service is single region (e.g. US only), but users are sending requests from other regions (like Europe, Asia, ...), multi-part can introduce further latency - <https://www.cloudping.co/grid>.

## WebSocket Endpoints

Colligo provides a [**direct WebSocket streaming API**](/aidoc/inference-platform/framework/websocket.md) to client workers.

How it works:
- Client requests a short‑lived signed WebSocket URL via HTTP
- Open a WebSocket connection using that URL
- Send input data to the worker
- Receive streamed responses (tokens, frames, or custom messages)

All authentication and routing is handled by Cluster Gateway.

Configuration:
WebSocket can be enabled for any `PublicEndpoint` by adding `enable_streaming=True` under `rhode_options` in `deploy_worker`:

```{code-block} python
STREAM_ENDPOINT = PublicEndpoint(
    path="/stream",
    request_type=HttpRequest,
    response_type=HttpResponse,
)
build.deploy_worker(
    ...
    public_http_endpoints=[STREAM_ENDPOINT],
    rhode_options=build.rhode_options(enable_streaming=True),
    ...
)
```
As the result your worker will have WebSocket Endpoint `ws/stream`.

```{seealso}
Please read more details in [WebSocket Streaming API](/aidoc/inference-platform/framework/websocket.md)
```

## SSE Endpoints

Colligo provides a [**Server-Sent Events (SSE) streaming API**](/aidoc/inference-platform/framework/sse.md) that streams typed events back to the client over a single HTTP POST.

How it works:
- Client sends a normal HTTP POST request
- Worker pushes events via `send_event` as they are produced
- Client reads a `text/event-stream` response

SSE can be enabled for any `PublicEndpoint` by setting `is_sse=True` on the endpoint and `enable_sse=True` under `rhode_options` in `deploy_worker`:

```{code-block} python
MY_ENDPOINT = PublicEndpoint(
    path="generate",
    request_type=MyRequest,
    response_type=MyResponse,
    is_sse=True,
)
build.deploy_worker(
    ...
    public_http_endpoints=[MY_ENDPOINT],
    rhode_options=build.rhode_options(enable_sse=True),
    ...
)
```

```{seealso}
Please read more details in [SSE Streaming API](/aidoc/inference-platform/framework/sse.md)
```
