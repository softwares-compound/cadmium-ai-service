import asyncio
import re
import websockets
import requests
from app.core.config import API_BASE_URL, WEBSOCKET_URL, WEBSOCKET_HEADERS
from app.services.log_processor import process_log
from app.core.websocket_server import electron_ws_manager 


async def websocket_connect(app):
    """
    Establish a WebSocket connection and process logs asynchronously.

    Args:
        app (FastAPI): The FastAPI app instance to access state.
    """
    while True:
        try:
            print(WEBSOCKET_HEADERS)
            async with websockets.connect(WEBSOCKET_URL, additional_headers=WEBSOCKET_HEADERS) as websocket:
                print("Connected to WebSocket server")
                while True:
                    # Receive log ID from WebSocket
                    message = await websocket.recv()

                    # Define regex pattern to extract log ID and app ID
                    pattern = r"New log ID:\s*(\w+)\s*and App ID:\s*(\w+)"
                    match = re.search(pattern, message)

                    if match:
                        log_id = match.group(1)
                        application_id = match.group(2)
                        print(f"Extracted Log ID: {log_id}")
                        print(f"Extracted App ID: {application_id}")
                        API_HEADERS = {
                            **WEBSOCKET_HEADERS,
                            "Application-ID": application_id,
                        }
                        # Fetch log details via API
                        response = requests.get(
                            f"{API_BASE_URL}/logs/{log_id}",
                            headers=API_HEADERS,
                        )
                        if response.status_code == 200:
                            log_data = response.json()
                            # First, broadcast the raw log to active WebSocket connections
                            await broadcast_log(log_data, application_id, log_id)

                            # Then, process the log asynchronously
                            asyncio.create_task(process_log(log_data, application_id, log_id, app))
                    
                        else:
                            print(
                                f"Failed to fetch log details. Status: {response.status_code}, Error: {response.text}"
                            )
                    else:
                        print(f"Unexpected message format: {message}")
        except websockets.ConnectionClosed as e:
            print(f"WebSocket connection closed: {e}. Retrying in 5 seconds...")
        except Exception as e:
            print(f"WebSocket error: {e}. Retrying in 5 seconds...")
        await asyncio.sleep(5)


def start_websocket_client(app):
    asyncio.create_task(websocket_connect(app))

async def broadcast_log(log_data, application_id, log_id):
    """
    Broadcast the raw log to all active WebSocket connections.

    Args:
        log_data (dict): The raw log data to broadcast.
        application_id (str): The application ID.
        log_id (str): The log ID.
    """
    message = {
        "protocol_version": "1.0",
        "type": "workflow",
        "workflow_id": "log_append",
        "action": "new_log",
        "message_id": f"log_{log_id}",
        "timestamp": asyncio.get_event_loop().time(),
        "data": {
            "log_id": log_id,
            "application_id": application_id,
            "raw_log": log_data
        }
    }

    await electron_ws_manager.broadcast(message)