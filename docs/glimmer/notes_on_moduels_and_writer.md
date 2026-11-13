# hs notes
## Prediction:
hs to put details here. how PL allows for callbacks, and what methods every modules has, etc

**Prediction Flow** (`predict_step` → `_predict_step`):
   - Preprocesses input via `input_preprocess_fn()`
   - Runs inference via `predict_fn()` (implemented by subclasses)
   - Transforms output via `transform_model_output()` (converts model outputs to standardized format)
   - Updates metrics (samples/second, batch counts, etc.)

## Writing out results:
We decide based on config what write is being used (hs put more details here).

[GlimmerWriter](https://github.com/Adobe-Firefly/genie/blob/5509fde9efd03fc8df584c87f80bc6d4449c96f6/glimmer/base_module/base_writer.py#L29), which is one of glimmer's base (aka default) modules inherits from _GlimmerCoreWriter which inherits from [BasePredictionWriter](https://github.com/Adobe-Firefly/genie/blob/f54c058723f1351ea497791dee6d8efd52649b67/glimmer/base_module/core_writer.py#L32) which is pytorch module [pytorch_lightning.callbacks.prediction_writer](https://github.com/Adobe-Firefly/genie/blob/main/.venv/lib/python3.11/site-packages/pytorch_lightning/callbacks/prediction_writer.py#L156). 

GlimmerWriter's job is to actually write the outputs to S3 through it's upload_prediction(prediction: dict[str, Any]) method.
This determines the s3 path to write to with using the prediction["ids"] it receives. As well as the instance of
[GlimmerOutput](https://github.com/Adobe-Firefly/genie/blob/5509fde9efd03fc8df584c87f80bc6d4449c96f6/glimmer/base_module/base_writer.py#L109)
that user has set in config (hs to add more details). It then writes the bytes to s3. 

BasePredictionWriter is a PL module, all it does is get called from the on_predict_batch_end of it's children, copy the indices (rows) that we have finished and call the write_on_batch_end method of the same child.

The rest of the work is done by _GlimmerCoreWriter. Things start when:
[prediction_fn](https://github.com/Adobe-Firefly/genie/blob/94dffc958eaf986f67de2ef9fe52677110fd7747/glimmer/modules/adobeone/module.py#L41) returns.

The predictions that are returned from module are converted to the format below using the transform_model_output function (see below for details) this will convert every module's output to dict[int, BatchDict] where:
   - Key = iloc_ix (the index location in the original dataset)
   - Value = {"ids": {...}, "data": {...}}

Then somehow (hs to put more details here) PL will call the:
[on_predict_batch_end](https://github.com/Adobe-Firefly/genie/blob/f54c058723f1351ea497791dee6d8efd52649b67/glimmer/base_module/core_writer.py#L61) 
callback that is registered to PL to call (put details of exactly how this is called). 

This guy checks if this is a streaming result or not. 

### none streaming results
for these we just write out the results. We call the
[on_predict_batch_end](https://github.com/Adobe-Firefly/genie/blob/f54c058723f1351ea497791dee6d8efd52649b67/glimmer/base_module/core_writer.py#L77)
method of its parent. All this does is call the
[write_on_batch_end](https://github.com/Adobe-Firefly/genie/blob/f54c058723f1351ea497791dee6d8efd52649b67/glimmer/base_module/core_writer.py#L100)

This method starts 32 threads, and passes them the
[upload_prediction](https://github.com/Adobe-Firefly/genie/blob/5509fde9efd03fc8df584c87f80bc6d4449c96f6/glimmer/base_module/base_writer.py#L67) (defined in base_writer). It also registers a call back to be called by the python thread management lib when this thread is done. This [done_callback](https://github.com/Adobe-Firefly/genie/blob/f54c058723f1351ea497791dee6d8efd52649b67/glimmer/base_module/core_writer.py#L160) method sends the ack/nack to the glimmer_queue.


### For streaming inputs
For the streaming inputs we collect all the results first, and then write them. (hs put aggregator logic here)
https://github.com/Adobe-Firefly/genie/blob/f54c058723f1351ea497791dee6d8efd52649b67/glimmer/base_module/core_writer.py#L86


---
---
---
<br>
<br>







# (question 1)

I'll help you understand the base module, writer patterns, and the differences. Let me start by exploring the codebase to find the writer implementation and related components.


Now I have a comprehensive understanding of the system. Let me explain the architecture, the standard writing flow, and the key differences with the new approach in the image captioning module.

## Overview: What `base_module.py` Does

`GlimmerBaseModule` is the abstract base class that all Glimmer inference modules inherit from. It orchestrates the prediction pipeline:

1. **Prediction Flow** (`predict_step` → `_predict_step`):
   - Preprocesses input via `input_preprocess_fn()`
   - Runs inference via `predict_fn()` (implemented by subclasses)
   - Transforms output via `transform_model_output()` (converts model outputs to standardized format)
   - Updates metrics (samples/second, batch counts, etc.)

2. **Output Structure**: The module returns predictions as `dict[int, BatchDict]` where:
   - Key = `iloc_ix` (the index location in the original dataset)
   - Value = `{"ids": {...}, "data": {...}}`

3. **Error Handling**: Catches exceptions and returns `{"error": "..."}` dict to signal failures

## Standard Writing Flow (Traditional Approach)

Here's the complete flow for most Glimmer modules:

### 1. **PyTorch Lightning Orchestration**

```
trainer.predict()
  → model.predict_step()  [returns predictions]
  → writer.on_predict_batch_end(outputs=predictions)  [callback triggered by Lightning]
      → writer.write_on_batch_end()
```

### 2. **Writer Architecture** (`core_writer.py` + `base_writer.py`)

**Initialization** (`on_predict_start`):
```python
# Lines 50-59 in core_writer.py
- Creates ThreadPoolExecutor with 32 workers
- Initializes GlimmerThinClient for queue management (if enabled)
- Sets up tracking for uploaded items
```

**Per-Batch Writing** (`write_on_batch_end`):
```python
# Lines 100-142 in core_writer.py
for iloc_ix in prediction:
    entry = prediction[iloc_ix]  # {"ids": {...}, "data": {...}}

    # Submit upload task to thread pool
    ft = self.executor.submit(self.upload_prediction, entry)

    # Add callback to handle ack/nack after upload completes
    if self.queue_client:
        ft.add_done_callback(partial(self.done_callback, iloc_ix))
```

**Upload Implementation** (`GlimmerWriter.upload_prediction`):
```python
# Lines 67-86 in base_writer.py
- Converts prediction data to bytes (json, parquet, safetensors, etc.)
- Gets file path from rendition/S3 config
- Writes to S3 or local filesystem
```

### 3. **Acks and Nacks Mechanism**

The queue system tracks which data items have been successfully processed:

**done_callback** (lines 160-165 in `core_writer.py`):
```python
def done_callback(self, iloc_ix, fut):
    if fut.exception():
        # Upload failed → tell queue to retry this item
        self.queue_client.tracker.nack([iloc_ix], None)
        log.error(f"Failed to upload iloc {iloc_ix}: {fut.exception()}")
    else:
        # Upload succeeded → mark as complete
        self.queue_client.tracker.ack([iloc_ix])
```

**When nacks occur:**
- Line 73, 117, 139: If errors happen during prediction or submission
- Line 162: If the upload future raises an exception
- The queue will eventually re-deliver nack'd items to be retried

**Cleanup** (`on_predict_end`):
```python
# Lines 143-153
- Shuts down thread pool (waits for all uploads to complete)
- Flushes all acks/nacks to the queue
- Closes queue client
```

## The Image Captioning Difference (The Better Way)

The `ImageCaptioningGlimmerModule` bypasses PyTorch Lightning's standard callback flow entirely. Here's what makes it different:

### Key Architectural Changes

**1. Module Owns the Writer** (not a separate callback):
```python
# Lines 129-132 in module.py
def on_predict_start(self):
    self.writer = GlimmerWriter(**self.writer_init_args)
    self.writer.on_predict_start(self.trainer, self)
```

**2. Async Event Loop for Concurrency Control**:
```python
# Lines 120-127
- Creates dedicated event loop in background thread
- Uses semaphore for concurrency control (not batch_size × workers)
- Allows precise control over concurrent API requests
```

**3. predict_fn() Triggers Writing Directly**:
```python
# Lines 141-151
def predict_fn(self, batch, batch_idx):
    self.semaphore.acquire()  # Control concurrency

    # Fire-and-forget: schedule async work
    handle = asyncio.run_coroutine_threadsafe(
        self.send_to_frontend(batch, batch_idx),
        self.async_loop
    )

    # Release semaphore when done
    handle.add_done_callback(lambda _: self.semaphore.release())

    return {}  # Empty! No predictions returned to Lightning
```

**4. Writing Happens in Async Context**:
```python
# Lines 81-108
async def send_to_frontend(self, batch, batch_idx):
    # Make async API calls
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results into output format
    out = {"data": ..., "word_count": ..., "unique_id": ...}

    # Write results asynchronously
    asyncio.create_task(self.write_batch_results(batch, out))

async def write_batch_results(self, batch, result):
    # Transform and write using the writer
    outputs = self.transform_model_output(batch, result)
    self.writer.write_on_batch_end(...)
```

### Why This Is Better

**1. Proper Async/Await for I/O-bound work:**
   - Traditional: ThreadPoolExecutor with 32 threads for uploads
   - New: Asyncio for API calls + thread pool only for final uploads
   - Benefit: Better concurrency for network I/O without thread overhead

**2. Fine-grained Concurrency Control:**
   - Traditional: `batch_size` items processed, then all uploaded in thread pool
   - New: Semaphore limits exactly N concurrent API requests in flight
   - Benefit: Prevents overwhelming external services (VLLM server)

**3. Enforces batch_size=1:**
```python
# Lines 110-118
if batch_size != 1:
    raise ValueError("batch_size must be 1. To send more requests, increase concurrency instead.")
```
   - Traditional: Large batches might have bursty behavior
   - New: Steady stream of work items with controlled concurrency
   - Benefit: More predictable load, better resource utilization

**4. Graceful Shutdown:**
```python
# Lines 153-163
def on_predict_end(self):
    self.stop_async_loop()  # Drain all async tasks first
    self.writer.on_predict_end(self.trainer, self)  # Then wait for uploads
```
   - Traditional: Just waits for thread pool to finish
   - New: Two-phase shutdown (async tasks → upload threads)
   - Benefit: Ensures all work is truly complete before exit

**5. Decoupled from Lightning's Callback System:**
   - Traditional: Lightning calls `predict_step()` → returns results → triggers writer callback
   - New: Lightning calls `predict_step()` → module schedules all work → returns immediately
   - Benefit: Module has full control over timing and lifecycle

## Visual Comparison

### Traditional Flow:
```
DataLoader → predict_step() → [predictions dict] → Lightning → on_predict_batch_end()
                                                      ↓
                                                  write_on_batch_end()
                                                      ↓
                                                  ThreadPool.submit(upload)
                                                      ↓
                                                  done_callback (ack/nack)
```

### Image Captioning Flow:
```
DataLoader → predict_step()
                ↓
            semaphore.acquire()
                ↓
            async_loop.submit(send_to_frontend)
                ↓
            [returns {}]  ← Lightning sees empty result, moves on
                ↓
            (meanwhile in background thread)
            async API calls → gather results → transform_output
                ↓
            writer.write_on_batch_end() → ThreadPool.submit(upload)
                ↓
            done_callback (ack/nack)
                ↓
            semaphore.release()
```

## Summary

The **traditional approach** works well for GPU-bound workloads where:
- Most time is spent in model inference
- Writing is just serialization + upload
- PyTorch Lightning's batching semantics match your needs

The **new approach** (image captioning) is better when:
- Work is I/O-bound (API calls to external services)
- You need precise concurrency control independent of batch size
- You want to overlap inference with I/O maximally
- You need explicit lifecycle management for async resources

The new pattern could be generalized for any Glimmer module that does significant I/O work (API calls, database queries, etc.) rather than pure model inference.






# Question 2

### 1) What does `transform_model_output` do? Example with AdobeOne
- It validates model output lengths match the batch size, then converts a batched `model_output` into a dict keyed by per-sample `_iloc_ix`, where each value is:
  - `ids`: the unique identifiers you configured plus, if streaming input, the stream markers (`_ix`, `_uid`, `_iloc_ix`)
  - `data`: the slice of the model outputs for that sample

Code:
```70:101:/mnt/localssd/genie/glimmer/base_module/base_module.py
def transform_model_output(self, batch: BatchDict, model_output: BatchDict) -> dict[int, BatchDict]:
    predictions = {}
    batch_size = len(batch[list(batch.keys())[0]])
    for key, value in model_output.items():
        if len(value) != batch_size:
            logger.error(
                "Input and output batch size mismatch",
                expected=batch_size,
                got=len(value),
                tensor_key=key,
            )
            raise ValueError()

    for b in range(batch_size):
        out = {key: value[b] for key, value in model_output.items()}
        ids = {id_: batch[id_][b] for id_ in self._output_unique_identifier_ids}

        if is_streaming_input(batch):
            ids.update(
                {
                    "_ix": batch["_ix"].tolist()[0],
                    "_uid": batch["_uid"][b],
                    "_iloc_ix": batch["_iloc_ix"].tolist()[0],
                }
            )

        predictions[batch["_iloc_ix"][b].tolist()] = {
            "ids": ids,
            "data": out,
        }

    return predictions
```

The AdobeOne module returns a single key `"chunk_embeddings"`:
```31:41:/mnt/localssd/genie/glimmer/modules/adobeone/module.py
def predict_fn(
    self, batch: BatchDict, batch_idx: int
) -> BatchDict:  # the batch contains a chunk of frames from one video
    preprocessed_frames = batch["preprocessed_frames"]
    chunk_embeddings = self.model.encode_image(preprocessed_frames)
    original_frames = batch["frames"]
    if original_frames.ndim == 5:
        chunk_embeddings = torch.unsqueeze(chunk_embeddings, 0)  # currently only supports batch size of 1

    model_output = {"chunk_embeddings": chunk_embeddings}
    return model_output
```

Example (simplified):
- Suppose the batch size is 1, streaming input, and the model returns `{"chunk_embeddings": tensor([E])}`.
- Suppose `batch["_iloc_ix"] = tensor([42])`, `batch["_ix"] = tensor([0])`, `batch["_uid"] = ["vid-abc"]`, and your unique identifiers are `["cid", "id32"]` so `batch["cid"] = ["C"]`, `batch["id32"] = ["I"]`.
- Then `transform_model_output` returns:
```python
{
  42: {
    "ids": {
      "cid": "C",
      "id32": "I",
      "_ix": 0,
      "_uid": "vid-abc",
      "_iloc_ix": 42
    },
    "data": {
      "chunk_embeddings": E
    }
  }
}
```
If the input batch has `_total` (last chunk), `_predict_step` also copies `_total` into each `ids`:
```125:138:/mnt/localssd/genie/glimmer/base_module/base_module.py
if not transform_output:
    return model_output

# convert model output to a dict of dicts
predictions = self.transform_model_output(batch, model_output)

if "_total" in batch and is_streaming_input(batch):  # the last chunk will have a key = total in the batch
    for b in range(batch_size):
        predictions[batch["_iloc_ix"].tolist()[b]]["ids"]["_total"] = batch["_total"].tolist()[b]

# Update metrics after successful processing
self._update_metrics(batch_size)

return predictions
```

### 2) How to trace from your YAML to the writer callback, parameters, outputs, and who passes `outputs` to `on_predict_batch_end`
- Your YAML includes:
```yaml
callbacks:
  writer:
    params:
      streaming:
        enabled: true
        frame_based: true
      outputs:
        - rendition: hs-adobeone-test-image
          extension: safetensors
```
- The config is loaded and transformed into callbacks in `inference.add_callback_configs`:
  - If `callbacks.writer` exists but lacks `target`, we auto-fill `glimmer.base_module.base_writer.GlimmerWriter`.
  - We then instantiate it from config (the `params` become `GlimmerWriter` kwargs).
```126:155:/mnt/localssd/genie/glimmer/inference.py
if "writer" in callback_config and "target" not in callback_config["writer"]:
    callback_config["writer"]["target"] = "glimmer.base_module.base_writer.GlimmerWriter"
...
callbacks.extend([instantiate_from_config(callback_config[k]) for k in callback_config])
```
- `GlimmerWriter` parses `outputs` and streaming params, and constructs an `Aggregator` if streaming:
```35:51:/mnt/localssd/genie/glimmer/base_module/base_writer.py
def __init__(
    self,
    outputs: list[dict[str, Any]],
    test_mode: bool = False,
    streaming: str | None = None,
    timeout_secs: int = 60 * 30,  # 30 minutes
    write_interval: Literal["batch", "epoch", "batch_and_epoch"] = "batch",
) -> None:
    self.outputs = [GlimmerOutput(**output_item) for output_item in outputs]

    is_streaming, aggregator = self.get_streaming_attributes(streaming)

    super().__init__(write_interval, timeout_secs, is_streaming=is_streaming, aggregator=aggregator)
    self.check_dead_interval = 32
    self.check_dead_counter = 0
    self.test_mode = test_mode
    self.test_samples_counter = 0 if test_mode else None
```
```88:106:/mnt/localssd/genie/glimmer/base_module/base_writer.py
def get_streaming_attributes(self, streaming: str | None) -> tuple[bool, Aggregator | None]:
    if streaming:
        assert len(self.outputs) == 1, "Streaming is not supported for multiple output file types"
        extension = self.outputs[0].extension
        is_streaming = streaming.enabled

        if is_streaming is True:
            frame_based = streaming.frame_based if hasattr(streaming, "frame_based") else False

            def reducer(microbatches):
                return reduce_predictions(microbatches, frame_based, extension)

            assert (
                extension in streamed_extensions
            ), f"Invalid output file type: {extension} for aggregator. Only {streamed_extensions} are supported for streaming."

            aggregator = Aggregator(reducer)
            return is_streaming, aggregator
    return False, None
```
- Who calls the callback and passes `outputs`? PyTorch Lightning’s prediction loop:
  - Calls the strategy `predict_step`, receives `predictions` (our `GlimmerBaseModule._predict_step` result), then calls callbacks’ `on_predict_batch_end(predictions, ...)`.
```255:269:/mnt/localssd/genie/.venv/lib/python3.11/site-packages/pytorch_lightning/loops/prediction_loop.py
predictions = call._call_strategy_hook(trainer, "predict_step", *step_args)
...
call._call_callback_hooks(trainer, "on_predict_batch_end", predictions, *hook_kwargs.values())
call._call_lightning_module_hook(trainer, "on_predict_batch_end", predictions, *hook_kwargs.values())
```

### 3) Non‑streaming case: what does PL’s `on_predict_batch_end` do?
- In our writer, non‑streaming path delegates to the base writer’s `on_predict_batch_end`, which just calls `write_on_batch_end(...)` with the `outputs` unchanged:
```61:79:/mnt/localssd/genie/glimmer/base_module/core_writer.py
if "error" in outputs:  # Prediction code can give up on a batch due to error.
    ...
if is_streaming_output(outputs) is False and self.is_streaming is False:
    super().on_predict_batch_end(trainer, pl_module, outputs, batch, batch_idx, dataloader_idx)
```
```143:157:/mnt/localssd/genie/.venv/lib/python3.11/site-packages/pytorch_lightning/callbacks/prediction_writer.py
def on_predict_batch_end(..., outputs: Any, batch: Any, ...):
    if not self.interval.on_batch:
        return
    batch_indices = trainer.predict_loop.current_batch_indices
    self.write_on_batch_end(trainer, pl_module, outputs, batch_indices, batch, batch_idx, dataloader_idx)
```

### 4) Aggregator: reduce and flush
- The `Aggregator` collects per‑chunk streaming predictions per `_uid`. When it has all chunks (based on `_total` count), it applies `reduce` and places the reduced result into an internal `sink`.
```31:69:/mnt/localssd/genie/glimmer/utilities/aggregator.py
class Aggregator:
    ...
    def store(self, uid, prediction: BatchDict) -> None:
        ...
        self.aggregate[uid].stored[ix] = prediction  # stored = {_ix:  BatchDict}
        ...
        if self.aggregate[uid].is_full():
            self.sink.append(
                self.reduce(list(self.aggregate[uid].stored.values()))
            )  # returns a list of BatchDicts to reduce()
            del self.aggregate[uid]

    def flush(self) -> Iterator[Any]:
        yield from self.sink
        self.sink.clear()
```
- The `reduce` is set by the writer to `reduce_predictions` with `frame_based` and `extension` from config:
```97:105:/mnt/localssd/genie/glimmer/base_module/base_writer.py
def reducer(microbatches):
    return reduce_predictions(microbatches, frame_based, extension)
...
aggregator = Aggregator(reducer)
```
- The reducer sorts microbatches by `_ix`, validates `_total` vs count, then:
  - `frame_based=True`: flattens frames and emits a dict keyed by frame index → tensor (plus metadata)
  - else: merges chunk keys
```50:100:/mnt/localssd/genie/glimmer/utilities/prediction_reducer.py
def reduce_predictions(microbatches: list[BatchDict], frame_based: bool, extension: str) -> PyTree:
    ...
    microbatches.sort(key=lambda x: x["ids"]["_ix"])
    curr_total = max(prediction["ids"].get("_total", 0) for prediction in microbatches)
    if not curr_total == len(microbatches):
        ...
    ...
    if frame_based:
        reduced_predictions = reduce_frames(microbatches, extension)
    else:
        reduced_predictions = reduce_chunks(microbatches)
    ...
    iloc_ix = microbatches[0]["ids"]["_iloc_ix"]
    result = {
        iloc_ix: {
            "ids": ids,
            "data": reduced_predictions,
        }
    }
    return result
```

### 5) Why store then immediately call `.flush()`? What’s the logic in that block?
- In the streaming path, per batch:
  - For each `prediction` in `outputs`, call `store(uid, prediction)` to accumulate for that `_uid`.
  - If `is_full()` for a `_uid`, `store` pushes a reduced result into `sink`.
  - Then `flush()` yields any newly reduced results (could be 0 or more), and we pass each to the base writer to upload.
```79:99:/mnt/localssd/genie/glimmer/base_module/core_writer.py
elif is_streaming_output(outputs) is True and self.is_streaming is True and self.aggregator is not None:
    if not self.aggregator.reduce:
        ...
        self.aggregator.reduce = pl_module.reduce

    for iloc_ix, prediction in outputs.items():
        self.aggregator.store(prediction["ids"]["_uid"], prediction)

    for result in self.aggregator.flush():
        assert isinstance(result, dict), "dict[int, dict[str, Any]] expected while flushing"

        super().on_predict_batch_end(trainer, pl_module, result, batch, batch_idx, dataloader_idx)
```
- Rationale: `flush()` is cheap and returns only completed sequences; calling it every batch ensures timely uploads of completed videos even while later videos are still accumulating.

### 5) What are the `ft = self.executor...` lines? What is `ft` and what is `partial`?
- `self.executor` is a `ThreadPoolExecutor` created at predict start:
```50:60:/mnt/localssd/genie/glimmer/base_module/core_writer.py
def on_predict_start(self, trainer: Trainer, pl_module: LightningModule) -> None:
    super().on_predict_start(trainer, pl_module)
    self.executor = ThreadPoolExecutor(max_workers=32)
    self.upload_results: deque[Any] = deque()
    self.uploaded_ix: deque[int] = deque()
    ...
```
- `ft = self.executor.submit(self.upload_prediction, entry)` returns a `concurrent.futures.Future` representing the async upload task. `partial(self.done_callback, iloc_ix)` binds `iloc_ix` as the first argument so the callback can ack/nack the right message when the future completes.
```120:136:/mnt/localssd/genie/glimmer/base_module/core_writer.py
for iloc_ix in prediction:
    ...
    ft = self.executor.submit(self.upload_prediction, entry)  # entry is a dict[str, Any]

    if self.queue_client:
        ft.add_done_callback(partial(self.done_callback, iloc_ix))
```
```160:169:/mnt/localssd/genie/glimmer/base_module/core_writer.py
def done_callback(self, iloc_ix, fut):  # don't forget
    if fut.exception():
        self.queue_client.tracker.nack([iloc_ix], None)
        log.error(f"Failed to submit upload task for iloc {iloc_ix}: {fut.exception()}")
    else:
        self.queue_client.tracker.ack([iloc_ix])
```

### 6) Who actually calls `write_on_batch_end`?
- PyTorch Lightning’s `BasePredictionWriter.on_predict_batch_end` calls `write_on_batch_end`:
```143:157:/mnt/localssd/genie/.venv/lib/python3.11/site-packages/pytorch_lightning/callbacks/prediction_writer.py
batch_indices = trainer.predict_loop.current_batch_indices
self.write_on_batch_end(trainer, pl_module, outputs, batch_indices, batch, batch_idx, dataloader_idx)
```
- In our writer:
  - Non‑streaming: our `on_predict_batch_end` simply calls the base `on_predict_batch_end`, which then calls our `write_on_batch_end`.
  - Streaming: we aggregate, possibly reduce, then call the base `on_predict_batch_end` with the reduced result, which then calls our `write_on_batch_end`.

### Where the bytes get written to S3
- `GlimmerWriter.write_on_batch_end` submits `upload_prediction` tasks. `upload_prediction` serializes the `prediction["data"]` using the extension mapping and writes to S3/local:
```67:86:/mnt/localssd/genie/glimmer/base_module/base_writer.py
def upload_prediction(self, prediction: dict[str, Any]) -> None:
    try:
        for output in self.outputs:
            if output.extension not in output_type_to_func:
                raise ValueError(f"Invalid output file type: {output.extension}")

            if self.is_streaming or not output.output_key:
                prediction_bytes = output_type_to_func[output.extension](prediction["data"])
            else:
                prediction_bytes = output_type_to_func[output.extension](prediction["data"][output.output_key])

            file_path = output.get_file_path(prediction["ids"])
            self.write_bytes(file_path, prediction_bytes, output.write_location)
    ...
```
```188:201:/mnt/localssd/genie/glimmer/utilities/writer_utils.py
output_type_to_func: dict[str, Callable[[dict[str, Any]], bytes | tuple[bytes, bytes]]] = {
    "safetensors": serde_safetensors,
    "parquet": serde_parquet,
    "json": serde_json,
    "mp4": serde_fmp4,
}
```
- `GlimmerOutput.get_file_path` chooses S3 path by rendition:
```123:141:/mnt/localssd/genie/glimmer/base_module/base_writer.py
def get_file_path(self, prediction_ids: dict[str, Any]) -> str:
    """
    Returns a complete file path to the prediction file.
    """
    ids = get_ids_to_write(prediction_ids)
    if self.write_location == "s3" and self.rendition:
        s3_path = get_s3_path_from_rendition(rendition=self.rendition, ids=ids, extension=self.extension)
        return s3_path.to_url()
    else:
        ...
```
```136:153:/mnt/localssd/genie/glimmer/utilities/writer_utils.py
def get_s3_path_from_rendition(rendition: Rendition, ids: dict[str, Any], extension: str) -> S3Path:
    if len(ids) == 2 and "cid" in ids and "id32" in ids:
        return rendition.resolve_from_cid_id32(**ids, extension=extension)
    elif len(ids) == 3 and "cid" in ids and "id32" in ids and "clip_id" in ids:
        return rendition.resolve_from_clip_id(**ids, extension=extension)
    # if there is only one key, resolve from image identifier
    elif len(ids) == 1:
        image_identifier = next(iter(ids.keys()))
        image_identifier_value = ids[image_identifier]
        if image_identifier_value is None:
            raise ValueError(f"Unique identifier {image_identifier} not found in {ids}")
        return rendition.resolve_from_image_identifier(image_identifier_value, extension=extension)
    else:
        raise ValueError("Unsupported unique identifier combination, please contact the Genie team")
```
- And the actual upload:
```96:120:/mnt/localssd/genie/glimmer/utilities/writer_utils.py
def upload_with_retry(s3_path: S3Path, data_in_bytes: bytes):
    try:
        # Get S3 client when needed
        s3_client = get_lazy_s3_client()
        s3_bucket = s3_path.bucket
        s3_key = s3_path.key

        for attempt in Retrying(
            stop=stop_after_attempt(3),
            reraise=True,
            wait=wait_random_exponential(multiplier=2, max=10),
        ):
            with attempt:
                s3_client.put_object(
                    Bucket=s3_bucket,
                    Key=s3_key,  # problem when we save metadata in prediction.ids
                    Body=data_in_bytes,
                )
    ...
```
```198:212:/mnt/localssd/genie/glimmer/base_module/base_writer.py
def set_write_location(
    self,
    rendition: str | None,
    output_location: str | None,
):
    if rendition or output_location and S3Path.is_s3_url(output_location):
        self.write_location = "s3"
        self.set_s3_args(rendition, output_location)
        self.s3_client = None
        log.warning(f"Writer is set to s3, writing to {self.s3_bucket}/{self.s3_prefix}")
    else:
        self.write_location = "local"
        self.set_local_args(output_location)
        log.warning(f"Writer is set to local, writing to {self.local_dir}")
```

### Quick trace checklist for your config
- Config → `add_callback_configs` injects target → `instantiate_from_config` builds `GlimmerWriter` with your `params`.
- `GlimmerWriter` creates `GlimmerOutput` (S3 renditions) and sets up `Aggregator` if streaming.
- PL `predict_loop` calls model `predict_step` → our `_predict_step` → `transform_model_output` (and adds `_total` when present).
- PL calls writer `on_predict_batch_end(outputs, ...)`.
  - Non‑streaming: directly calls base `on_predict_batch_end` → `write_on_batch_end`.
  - Streaming: aggregate, `flush`, then call base `on_predict_batch_end` with reduced result.
- `write_on_batch_end` submits `upload_prediction` to threads.
- `upload_prediction` serializes bytes and calls `write_bytes` → S3 via `upload_with_retry`.

- Summary of changes/answers:
  - Explained `transform_model_output` with an AdobeOne concrete example.
  - Mapped your YAML to `GlimmerWriter` and showed how PL hands `outputs` to the callback.
  - Clarified non‑streaming path: PL’s base writer simply forwards to `write_on_batch_end`.
  - Detailed the `Aggregator`’s `store`/`reduce`/`flush` flow and why `flush()` is called each batch.
  - Clarified the executor usage, `Future` type, and `partial` callback for ack/nack.
  - Identified who calls `write_on_batch_end` and how S3 paths/serialization are chosen.