from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import asyncio
from app.services.electron_ws_manager import ElectronWebSocketManager

# Initialize a WebSocket manager for Electron
electron_ws_manager = ElectronWebSocketManager()

async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint to handle Electron communication with keep-alive.
    """
    await electron_ws_manager.connect(websocket)

    try:
        await asyncio.gather(
            websocket_handler(websocket),  # Existing handler for incoming messages
            keep_alive(websocket)         # New keep-alive mechanism
        )
    except WebSocketDisconnect:
        electron_ws_manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        electron_ws_manager.disconnect(websocket)


async def keep_alive(websocket: WebSocket):
    """
    Periodically send a ping message to keep the WebSocket connection alive.
    """
    try:
        while True:
            await websocket.send_json({"type": "ping", "timestamp": datetime.utcnow().isoformat()})
            await asyncio.sleep(30)  # Adjust interval as needed
    except Exception as e:
        print(f"Keep-alive error: {e}")
        raise WebSocketDisconnect


async def websocket_handler(websocket: WebSocket):
    """
    Handle incoming WebSocket messages.
    """
    while True:
        try:
            message = await websocket.receive_json()
            await electron_ws_manager.handle_message(websocket, message)
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
