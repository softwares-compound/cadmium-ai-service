from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import asyncio
from app.services.electron_ws_manager import ElectronWebSocketManager

# Initialize a WebSocket manager for Electron
electron_ws_manager = ElectronWebSocketManager()

async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint to handle Electron communication.
    """
    await electron_ws_manager.connect(websocket)

    try:
        while True:
            # Receive and process messages from Electron
            message = await websocket.receive_json()
            await electron_ws_manager.handle_message(websocket, message)
    except WebSocketDisconnect:
        electron_ws_manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
