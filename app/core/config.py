import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    cadmium_cloud_ws_url: str = os.getenv("CADMIUM_CLOUD_WS_URL", "wss://cadmium-cloud.example.com/ws")
    cadmium_cloud_api_url: str = os.getenv("CADMIUM_CLOUD_API_URL", "https://cadmium-cloud.example.com/api")
    local_llm_endpoint: str = os.getenv("LOCAL_LLM_ENDPOINT", "http://localhost:8001/llm")

settings = Settings()


# Configuration for WebSocket connection

# WebSocket server URL
WEBSOCKET_URL = "ws://43.204.216.93/ws"

# Headers required for the WebSocket handshake
WEBSOCKET_HEADERS = {
    "CD-ID": "5c133a93-8dd4-4958-847a-ae81a5e11743",
    "CD-Secret": "2fb5be09-8dba-481c-aaaf-5efad1d0a59c",
    "Application-ID": "673d6733caa30090be5b410d",
}

# Additional configurations can be added here as needed.
