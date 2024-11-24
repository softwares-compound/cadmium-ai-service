import asyncio
import websockets
import requests
from app.core.config import WEBSOCKET_URL, WEBSOCKET_HEADERS
from app.services.log_processor import process_log

API_BASE_URL = "http://43.204.216.93"

async def websocket_connect():
    while True:
        try:
            async with websockets.connect(WEBSOCKET_URL, additional_headers=WEBSOCKET_HEADERS) as websocket:
                print("Connected to WebSocket server")
                while True:
                    # Receive log ID from WebSocket
                    message = await websocket.recv()

                    # Extract the log ID from the message
                    if message.startswith("New log ID:"):
                        log_id = message.split("New log ID:")[-1].strip()
                        print(f"Extracted Log ID: {log_id}")

                        # Fetch log details via API
                        response = requests.get(
                            f"{API_BASE_URL}/logs/{log_id}",
                            headers=WEBSOCKET_HEADERS,
                        )
                        if response.status_code == 200:
                            log_data = response.json()

                            # Process the log asynchronously
                            asyncio.create_task(process_log(log_data))  # Schedule the async function
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


def start_websocket_client():
    asyncio.create_task(websocket_connect())
