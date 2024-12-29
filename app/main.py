import asyncio
import aiohttp
from bson import ObjectId
from fastapi import FastAPI, WebSocket
from app.core.websocket_client import start_websocket_client
from app.core.websocket_server import websocket_endpoint, electron_ws_manager
from app.core.config import API_BASE_URL, settings
from app.rag.paradigms.naive_rag.naive_rag_executer import NaiveRAGService

app = FastAPI()


async def fetch_application_ids():
    """
    Fetch application IDs from the Rust API asynchronously, including custom headers.
    """
    headers = {
        'CD-ID': settings.cd_id,
        'CD-Secret': settings.cd_secret
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_BASE_URL}/applications', headers=headers) as response:
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = await response.json()
            print("Fetched application data:", data)
            # Extract and convert ObjectId strings to ObjectId instances
            application_ids = [str(ObjectId(app['_id']['$oid'])) for app in data]
            return application_ids


@app.on_event("startup")
async def startup_event():
    """
    Initialize services during FastAPI startup.
    - Start WebSocket client
    - Create NaiveRAGService instances for each application ID and store in app state.
    """
    # Start the WebSocket client to listen for logs
    start_websocket_client(app)

    # Fetch application IDs from the Rust API
    application_ids = await fetch_application_ids()
    print(application_ids, "APPLICATION_IDS")
    if settings.preferred_rag_approach == "naive_rag":
        # Initialize NaiveRAGService for each application ID
        app.state.naive_rag_services = {}
        for application_id in application_ids:
            app.state.naive_rag_services[application_id] = NaiveRAGService(
                application_id=application_id, persist_dir="./storage/naive_rag_storage"
            )
        print(f"Initialized NaiveRAGService for application IDs: {application_ids}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Handle cleanup tasks during FastAPI shutdown.
    """
    print("Shutting down FastAPI application...")

    # Cancel all asyncio tasks
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)

    print("Application shutdown complete.")


# Add WebSocket route for Electron communication
@app.websocket("/ws/electron")
async def electron_ws(websocket: WebSocket):
    """
    WebSocket endpoint to handle Electron communication.
    """
    await websocket_endpoint(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6970)