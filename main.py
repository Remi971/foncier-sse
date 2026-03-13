from fastapi import FastAPI, Request, Depends
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from dependencies import env, Publisher
import json

app = FastAPI(
    title="CartoFoncier SSE API",
    description="CartoFoncier SSE API - Serveur de données en temps réel pour CartoFoncier",
    version="0.0.1",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=env.BASE_URL.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

publisher = Publisher()

async def event_stream(request: Request):
    pubsub = publisher.subscribe()
    while True:
        if await request.is_disconnected():
            break
        message = pubsub.get_message(timeout=30)
        if message and message["type"] == "message":
            parsed_message = json.loads(message["data"].decode('utf-8'))
            print(f"Message reçu: {parsed_message}")
            yield f"data: {json.dumps(parsed_message)}\n\n"
        else:
            yield "data: \n\n"
        await asyncio.sleep(0.1)

@app.get("/sse")
async def sse(request: Request):
    return StreamingResponse(
        event_stream(request),
        media_type="text/event-stream",
    )