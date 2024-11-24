import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    cadmium_cloud_ws_url: str = os.getenv("CADMIUM_CLOUD_WS_URL", "wss://cadmium-cloud.example.com/ws")
    cadmium_cloud_api_url: str = os.getenv("CADMIUM_CLOUD_API_URL", "https://cadmium-cloud.example.com/api")
    local_llm_endpoint: str = os.getenv("LOCAL_LLM_ENDPOINT", "http://localhost:8001/llm")

settings = Settings()
