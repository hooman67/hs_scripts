---
type: concept
title: Mori Pluto Agent SDK
tags: [mori, pluto, agent, sdk, rest, integration]
created: 2026-07-05
updated: 2026-07-05
sources: ["[[raw/mori-docs.md]]", "[[raw/colligo/mori/aidoc/internal/pluto_agent.md]]"]
---

# Mori Pluto Agent SDK

The bridge that lets a [[wiki/entities/mori|Mori]] training framework running **inside a [[wiki/entities/pluto|Pluto]] job** communicate with the Pluto platform — with minimal impact on the training loop.

## Design

- Runs an **HTTP service in a separate process** (Python multiprocessing) so it doesn't interfere with training — notably avoiding Python **GIL** contention.
- Communication = native multiprocessing queues + HTTP REST endpoints + JSON-serializable payloads.

## Training-framework side (API)

```python
agent.start_pluto_agent(port_number)
# register sync/async handlers for specific task types
agent.run_pluto_agent_handlers()      # call each iteration to process queued tasks
agent.send_pluto_agent_result()       # report results for async operations
```

## Pluto-platform side (REST)

| Endpoint | Purpose |
|---|---|
| `GET /handlers` | list registered task types |
| `POST /run_job/{handler_name}` | start a task (JSON payload) |
| `GET /job_status/{task_id}` | check execution status |
| `PUT /cancel/{task_id}` | cancel a pending/running task |

## Execution modes

- **Synchronous** — handler completes within the call and returns results immediately.
- **Asynchronous** — returns a task id immediately; completion is reported later via `send_pluto_agent_result()`, enabling long-running operations like **snapshot creation** and profiler tracing.

This agent is what backs in-job actions triggered from the [[wiki/concepts/pluto-cli-sdk|`aip` CLI]] (e.g. `aip job run-tracing` for the [[wiki/concepts/mori-observability|on-demand profiler]]) and platform-initiated snapshots in the [[wiki/concepts/pluto-job-lifecycle|Pluto job lifecycle]].

## Related
- [[wiki/entities/mori]]
- [[wiki/entities/pluto]]
- [[wiki/concepts/mori-observability]]
- [[wiki/concepts/pluto-cli-sdk]]
- [[wiki/concepts/pluto-job-lifecycle]]
