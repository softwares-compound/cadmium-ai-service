import asyncio
import websockets
import json

async def websocket_client():
    uri = "ws://localhost:8000/ws/electron"  # Update the URI if necessary

    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to WebSocket server at {uri}")

            # Send an initialization message to the server
            init_message = {
                "protocol_version": "1.0",
                "type": "workflow",
                "action": "init",
                "message_id": "client_test_001",
                "timestamp": "2024-12-09T12:00:00Z"
            }
            await websocket.send(json.dumps(init_message))
            print(f"Sent initialization message: {init_message}")

            # Listen for messages from the server
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    print(f"Received message from server: {json.dumps(data, indent=2)}")
                except websockets.ConnectionClosed as e:
                    print(f"WebSocket connection closed: {e}")
                    break

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(websocket_client())
