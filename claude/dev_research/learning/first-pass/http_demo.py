"""Local-only teaching examples; run one Uvicorn worker, not a production service."""

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


@app.get("/delayed")
async def delayed():
    await asyncio.sleep(5)
    return {"result": 42}


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
