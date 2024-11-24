from fastapi import FastAPI
from app.api.endpoints import logs
from app.core.websocket_client import start_websocket_client

app = FastAPI()

app.include_router(logs.router, prefix="/logs", tags=["logs"])

@app.on_event("startup")
async def startup_event():
    # Start the WebSocket client
    start_websocket_client()
